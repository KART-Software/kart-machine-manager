// Port of app/src/can/can_listeners.py:
//   DashInfoStore  <- DashInfoListener   (latest DashMachineInfo, locked)
//   UdpPayloadStore <- UdpPayloadListener (latest frame per CAN ID -> payload)
#pragma once

#include <cstdint>
#include <mutex>
#include <unordered_map>
#include <vector>

#include "canbus.hpp"
#include "models.hpp"

namespace kmm {

class DashInfoStore {
public:
    void onFrame(const CanFrame& frame);
    models::DashMachineInfo snapshot() const;

private:
    mutable std::mutex mutex_;
    models::DashMachineInfo info_;
};

class UdpPayloadStore {
public:
    void onFrame(const CanFrame& frame);

    // machineId u32le | runId u32le | errorCode u8 | epoch-ms u64le |
    // fixed slots: 0x5F0..0x5F3 len 8, 0x5F4 len 6, 0x700..0x70E len 8
    std::vector<std::uint8_t> payload(std::uint32_t machineId,
                                      std::uint32_t runId,
                                      std::uint8_t errorCode) const;

private:
    mutable std::mutex mutex_;
    std::unordered_map<std::uint32_t, CanFrame> latest_;
};

}  // namespace kmm
