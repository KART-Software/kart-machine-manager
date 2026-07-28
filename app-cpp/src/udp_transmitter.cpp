#include "udp_transmitter.hpp"

#include <chrono>
#include <cstdio>
#include <cstring>

#include <netdb.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>

namespace kmm {

namespace {
constexpr auto UDP_INTERVAL = std::chrono::milliseconds(30);
}

UdpTransmitter::UdpTransmitter(const UdpPayloadStore& store, const Config& config)
    : store_(store),
      machineId_(static_cast<std::uint32_t>(config.machineId)),
      host_(config.udpHost.toStdString()),
      port_(config.udpPort)
{
}

UdpTransmitter::~UdpTransmitter()
{
    stop();
    if (fd_ >= 0) ::close(fd_);
}

void UdpTransmitter::start(std::uint32_t runId)
{
    if (thread_.joinable()) return;
    runId_ = runId;
    thread_ = std::thread([this] { run(); });
}

void UdpTransmitter::stop()
{
    stopped_.store(true);
    if (thread_.joinable()) thread_.join();
}

void UdpTransmitter::run()
{
    // Resolve the destination once; the network is already up because the
    // run ID fetch has succeeded before start() is called. Retry to be safe.
    struct sockaddr_storage dest {};
    socklen_t destLen = 0;
    while (!stopped_.load()) {
        struct addrinfo hints {};
        hints.ai_family = AF_INET;
        hints.ai_socktype = SOCK_DGRAM;
        struct addrinfo* res = nullptr;
        const std::string portStr = std::to_string(port_);
        if (::getaddrinfo(host_.c_str(), portStr.c_str(), &hints, &res) == 0) {
            std::memcpy(&dest, res->ai_addr, res->ai_addrlen);
            destLen = static_cast<socklen_t>(res->ai_addrlen);
            ::freeaddrinfo(res);
            break;
        }
        std::fprintf(stderr, "UDP destination resolve failed, retrying: %s\n",
                     host_.c_str());
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    if (destLen == 0) return;

    fd_ = ::socket(AF_INET, SOCK_DGRAM, 0);
    if (fd_ < 0) {
        std::fprintf(stderr, "UDP socket creation failed\n");
        return;
    }

    const auto baseTime = std::chrono::steady_clock::now();
    while (!stopped_.load()) {
        const auto payload = store_.payload(machineId_, runId_, 0);
        if (::sendto(fd_, payload.data(), payload.size(), 0,
                     reinterpret_cast<struct sockaddr*>(&dest), destLen) < 0) {
            std::fprintf(stderr, "UDP send failed!\n");
        }

        // Sleep until the next 30ms boundary relative to baseTime.
        const auto elapsed = std::chrono::steady_clock::now() - baseTime;
        const auto sleep = UDP_INTERVAL - (elapsed % UDP_INTERVAL);
        std::this_thread::sleep_for(sleep);
    }
}

}  // namespace kmm
