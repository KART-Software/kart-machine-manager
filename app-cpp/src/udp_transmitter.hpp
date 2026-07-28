// Port of app/src/udp/udp_transmitter.py. The 30ms cadence uses the same
// modulo scheduling against a base time. Sending starts only after the run ID
// has been obtained (see cloud.hpp RunIdFetcher), like the Python thread that
// blocks in getRunId() first.
#pragma once

#include <atomic>
#include <cstdint>
#include <string>
#include <thread>

#include "config.hpp"
#include "stores.hpp"

namespace kmm {

class UdpTransmitter {
public:
    UdpTransmitter(const UdpPayloadStore& store, const Config& config);
    ~UdpTransmitter();

    void start(std::uint32_t runId);
    void stop();

private:
    void run();

    const UdpPayloadStore& store_;
    std::uint32_t machineId_;
    std::string host_;
    std::uint16_t port_;
    std::uint32_t runId_ = 0;
    int fd_ = -1;
    std::atomic<bool> stopped_{false};
    std::thread thread_;
};

}  // namespace kmm
