#include "canbus.hpp"

#include <cerrno>
#include <chrono>
#include <cstdio>
#include <cstring>
#include <stdexcept>
#include <thread>

#include <linux/can.h>
#include <linux/can/raw.h>
#include <net/if.h>
#include <poll.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <unistd.h>

namespace kmm {

// ---- SocketCanSource ----

SocketCanSource::SocketCanSource(const std::string& interface)
    : interface_(interface), created_(std::chrono::steady_clock::now())
{
    open();  // binds immediately when the interface already exists
}

SocketCanSource::~SocketCanSource()
{
    close();
}

bool SocketCanSource::open()
{
    const int fd = ::socket(PF_CAN, SOCK_RAW, CAN_RAW);
    if (fd < 0) {
        throw std::runtime_error("socket(PF_CAN) failed: " +
                                 std::string(std::strerror(errno)));
    }

    struct ifreq ifr {};
    std::snprintf(ifr.ifr_name, sizeof(ifr.ifr_name), "%s", interface_.c_str());
    if (::ioctl(fd, SIOCGIFINDEX, &ifr) < 0) {
        ::close(fd);
        if (!loggedWaiting_) {
            std::fprintf(stderr, "CAN interface %s not present yet; waiting\n",
                         interface_.c_str());
            loggedWaiting_ = true;
        }
        return false;
    }

    struct sockaddr_can addr {};
    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;
    if (::bind(fd, reinterpret_cast<struct sockaddr*>(&addr), sizeof(addr)) < 0) {
        ::close(fd);
        throw std::runtime_error("bind(" + interface_ + ") failed: " +
                                 std::string(std::strerror(errno)));
    }
    fd_ = fd;
    if (loggedWaiting_) {
        const auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(
                            std::chrono::steady_clock::now() - created_)
                            .count();
        std::fprintf(stderr, "CAN interface %s bound after ~%lld ms\n",
                     interface_.c_str(), static_cast<long long>(ms));
    }
    return true;
}

void SocketCanSource::close()
{
    if (fd_ >= 0) ::close(fd_);
    fd_ = -1;
}

std::optional<CanFrame> SocketCanSource::recv(int timeoutMs)
{
    if (fd_ < 0 && !open()) {
        // Interface still missing: pace the retry with the caller's timeout.
        std::this_thread::sleep_for(std::chrono::milliseconds(timeoutMs));
        return std::nullopt;
    }

    struct pollfd pfd {};
    pfd.fd = fd_;
    pfd.events = POLLIN;
    const int ret = ::poll(&pfd, 1, timeoutMs);
    if (ret <= 0) return std::nullopt;

    struct can_frame frame {};
    const ssize_t n = ::read(fd_, &frame, sizeof(frame));
    if (n < 0 && (errno == ENODEV || errno == ENXIO || errno == ENETDOWN)) {
        // Interface went away (e.g. gateway restarted): re-bind on next call.
        std::fprintf(stderr, "CAN interface %s gone (%s); re-binding\n",
                     interface_.c_str(), std::strerror(errno));
        close();
        return std::nullopt;
    }
    if (n != static_cast<ssize_t>(sizeof(frame))) return std::nullopt;

    // Error frames are not data (mirror of bus.py filtering CAN_ERR_FLAG).
    if (frame.can_id & CAN_ERR_FLAG) return std::nullopt;

    CanFrame out;
    out.id = frame.can_id &
             ((frame.can_id & CAN_EFF_FLAG) ? CAN_EFF_MASK : CAN_SFF_MASK);
    out.dlc = frame.can_dlc > 8 ? 8 : frame.can_dlc;
    std::memcpy(out.data.data(), frame.data, out.dlc);
    return out;
}

// ---- MockCanSource ----

namespace {

void pushU16Be(CanFrame& f, std::uint64_t value)
{
    f.data[f.dlc++] = static_cast<std::uint8_t>((value >> 8) & 0xFF);
    f.data[f.dlc++] = static_cast<std::uint8_t>(value & 0xFF);
}

}  // namespace

MockCanSource::MockCanSource() : nextTick_(std::chrono::steady_clock::now()) {}

// Same waveforms as mock_can_sender.py updateMachine()/toMessages().
void MockCanSource::generateBatch()
{
    const std::uint64_t t = static_cast<std::uint64_t>(
        std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::system_clock::now().time_since_epoch())
            .count());

    CanFrame f0;
    f0.id = 0x5F0;
    pushU16Be(f0, t % 10000);        // rpm
    pushU16Be(f0, t % 1000);         // throttlePosition * 10
    pushU16Be(f0, t % 1400);         // engineTemperature * 10
    pushU16Be(f0, t % 1600);         // oilTemperature * 10
    queue_.push_back(f0);

    CanFrame f1;
    f1.id = 0x5F1;
    pushU16Be(f1, t % 1200);         // oilPressure * 10
    pushU16Be(f1, t % 5000);         // gearVoltage * 1000
    pushU16Be(f1, (t % 13000) / 10); // batteryVoltage * 100
    pushU16Be(f1, 700 + t % 600);    // lambda * 1000
    queue_.push_back(f1);

    CanFrame f2;
    f2.id = 0x5F2;
    pushU16Be(f2, (t % 10000) / 10); // manifoldPressure * 10
    pushU16Be(f2, t % 3000);         // fuelPressure * 10
    pushU16Be(f2, t % 6000);         // brakePressureFront * 10
    pushU16Be(f2, 6000 - t % 6000);  // brakePressureRear * 10
    queue_.push_back(f2);

    const bool fan = ((t % 10000) / 5000) != 0;
    const bool istUp = ((t % 8000) / 4000) != 0;
    CanFrame f3;
    f3.id = 0x5F3;
    pushU16Be(f3, fan ? 1 : 0);
    pushU16Be(f3, istUp ? 2 : 1);    // (istUp, istDown) is always (1,0) or (0,1)
    pushU16Be(f3, t % 5000);         // inputRpm
    pushU16Be(f3, t % 4500);         // outputRpm
    queue_.push_back(f3);

    CanFrame f4;
    f4.id = 0x5F4;
    pushU16Be(f4, t % 1200);         // oilTemperature2 * 10
    pushU16Be(f4, t % 1200);         // oilTemperature3 * 10
    pushU16Be(f4, t % 1200);         // coolantTemperature * 10
    queue_.push_back(f4);
}

std::optional<CanFrame> MockCanSource::recv(int timeoutMs)
{
    using namespace std::chrono;

    if (queue_.empty()) {
        const auto now = steady_clock::now();
        if (nextTick_ > now) {
            const auto wait = duration_cast<milliseconds>(nextTick_ - now);
            if (wait.count() >= timeoutMs) {
                std::this_thread::sleep_for(milliseconds(timeoutMs));
                return std::nullopt;
            }
            std::this_thread::sleep_for(wait);
        }
        generateBatch();
        nextTick_ = steady_clock::now() + milliseconds(33);
    }

    CanFrame frame = queue_.front();
    queue_.pop_front();
    return frame;
}

// ---- CanReader ----

CanReader::CanReader(CanSource& source,
                     std::vector<std::function<void(const CanFrame&)>> listeners)
    : source_(source), listeners_(std::move(listeners)), thread_([this] { run(); })
{
}

CanReader::~CanReader()
{
    stop();
}

void CanReader::run()
{
    while (!stopped_.load()) {
        const auto frame = source_.recv(500);
        if (!frame) continue;
        for (const auto& listener : listeners_) listener(*frame);
    }
}

void CanReader::stop()
{
    stopped_.store(true);
    if (thread_.joinable()) thread_.join();
}

}  // namespace kmm
