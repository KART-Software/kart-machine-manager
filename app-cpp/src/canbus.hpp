// Port of app/src/canbus (SocketCanBus / VirtualBus / Notifier).
// SocketCanSource reads real SocketCAN frames; MockCanSource generates the
// same synthetic frames as app/src/can/mock_can_sender.py at a 33ms cadence.
#pragma once

#include <array>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <deque>
#include <functional>
#include <optional>
#include <string>
#include <thread>
#include <vector>

namespace kmm {

struct CanFrame {
    std::uint32_t id = 0;
    std::uint8_t dlc = 0;
    std::array<std::uint8_t, 8> data{};
};

class CanSource {
public:
    virtual ~CanSource() = default;
    // Blocks up to timeoutMs; returns std::nullopt on timeout.
    virtual std::optional<CanFrame> recv(int timeoutMs) = 0;
};

class SocketCanSource : public CanSource {
public:
    explicit SocketCanSource(const std::string& interface);
    ~SocketCanSource() override;

    std::optional<CanFrame> recv(int timeoutMs) override;

private:
    int fd_ = -1;
};

class MockCanSource : public CanSource {
public:
    MockCanSource();

    std::optional<CanFrame> recv(int timeoutMs) override;

private:
    void generateBatch();

    std::deque<CanFrame> queue_;
    std::chrono::steady_clock::time_point nextTick_;
};

// Port of canbus.Notifier: reader thread dispatching frames to listeners.
// A listener exception must not kill the thread — listeners here are plain
// callbacks and are expected not to throw.
class CanReader {
public:
    CanReader(CanSource& source,
              std::vector<std::function<void(const CanFrame&)>> listeners);
    ~CanReader();

    void stop();

private:
    void run();

    CanSource& source_;
    std::vector<std::function<void(const CanFrame&)>> listeners_;
    std::atomic<bool> stopped_{false};
    std::thread thread_;
};

}  // namespace kmm
