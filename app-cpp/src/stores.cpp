#include "stores.hpp"

#include <algorithm>
#include <chrono>

namespace kmm {
namespace {

std::uint32_t u16be(const CanFrame& f, int index)
{
    return (static_cast<std::uint32_t>(f.data[index]) << 8) |
           static_cast<std::uint32_t>(f.data[index + 1]);
}

struct CanIdLength {
    std::uint32_t id;
    int length;
};

// MOTEC + data logger IDs, ascending (can_listeners.py sorts the same way).
constexpr CanIdLength CAN_ID_LENGTHS[] = {
    {0x5F0, 8}, {0x5F1, 8}, {0x5F2, 8}, {0x5F3, 8}, {0x5F4, 6},
    {0x700, 8}, {0x701, 8}, {0x702, 8}, {0x703, 8}, {0x704, 8},
    {0x705, 8}, {0x706, 8}, {0x707, 8}, {0x708, 8}, {0x709, 8},
    {0x70A, 8}, {0x70B, 8}, {0x70C, 8}, {0x70D, 8}, {0x70E, 8},
};

void pushLe(std::vector<std::uint8_t>& out, std::uint64_t value, int bytes)
{
    for (int i = 0; i < bytes; ++i) {
        out.push_back(static_cast<std::uint8_t>((value >> (8 * i)) & 0xFF));
    }
}

}  // namespace

void DashInfoStore::onFrame(const CanFrame& frame)
{
    std::lock_guard<std::mutex> lock(mutex_);
    switch (frame.id) {
    case 0x5F0:
        if (frame.dlc < 8) return;
        info_.setRpm(static_cast<int>(u16be(frame, 0)));
        info_.throttlePosition = u16be(frame, 2) / 10.0;
        info_.waterTemp = static_cast<int>(u16be(frame, 4) / 10);
        info_.oilTemp = static_cast<int>(u16be(frame, 6) / 10);
        break;
    case 0x5F1:
        if (frame.dlc < 6) return;
        info_.oilPress.value = u16be(frame, 0) / 10.0;
        info_.gearVoltage = u16be(frame, 2) / 1000.0;
        info_.batteryVoltage = u16be(frame, 4) / 100.0;
        break;
    case 0x5F2:
        if (frame.dlc < 8) return;
        info_.fuelPress = u16be(frame, 2) / 10.0;
        info_.brakePress.front = u16be(frame, 4) / 10.0;
        info_.brakePress.rear = u16be(frame, 6) / 10.0;
        break;
    case 0x5F3:
        if (frame.dlc < 2) return;
        info_.fanEnabled = frame.data[1] != 0;
        break;
    default:
        break;
    }
}

models::DashMachineInfo DashInfoStore::snapshot() const
{
    std::lock_guard<std::mutex> lock(mutex_);
    return info_;
}

void UdpPayloadStore::onFrame(const CanFrame& frame)
{
    std::lock_guard<std::mutex> lock(mutex_);
    latest_[frame.id] = frame;
}

std::vector<std::uint8_t> UdpPayloadStore::payload(std::uint32_t machineId,
                                                   std::uint32_t runId,
                                                   std::uint8_t errorCode) const
{
    std::unordered_map<std::uint32_t, CanFrame> messages;
    {
        std::lock_guard<std::mutex> lock(mutex_);
        messages = latest_;
    }

    const auto epochMs = static_cast<std::uint64_t>(
        std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::system_clock::now().time_since_epoch())
            .count());

    std::vector<std::uint8_t> bs;
    bs.reserve(17 + 5 * 8 - 2 + 15 * 8);
    pushLe(bs, machineId, 4);
    pushLe(bs, runId, 4);
    pushLe(bs, errorCode, 1);
    pushLe(bs, epochMs, 8);

    for (const auto& il : CAN_ID_LENGTHS) {
        const std::size_t start = bs.size();
        bs.resize(start + il.length, 0);
        const auto it = messages.find(il.id);
        if (it != messages.end()) {
            const int n = std::min<int>(il.length, it->second.dlc);
            for (int i = 0; i < n; ++i) bs[start + i] = it->second.data[i];
        }
    }
    return bs;
}

}  // namespace kmm
