// Port of app/src/models/models.py — pure data + status logic, Qt-free.
#pragma once

#include <algorithm>
#include <array>
#include <cmath>
#include <cstddef>

namespace kmm::models {

// ---- Rpm ----
enum class RpmStatus { Low, Middle, High, Shift };

struct Rpm {
    static constexpr int LOW_THRESHOLD = 4000;
    static constexpr int HIGH_THRESHOLD = 7000;
    static constexpr int SHIFT_THRESHOLD = 9000;
    static constexpr int MAX = 10000;
};

inline RpmStatus rpmStatus(int rpm)
{
    if (rpm < Rpm::LOW_THRESHOLD) return RpmStatus::Low;
    if (rpm < Rpm::HIGH_THRESHOLD) return RpmStatus::Middle;
    if (rpm < Rpm::SHIFT_THRESHOLD) return RpmStatus::High;
    return RpmStatus::Shift;
}

// ---- WaterTemp ----
enum class WaterTempStatus { Low, Middle, High };

inline WaterTempStatus waterTempStatus(int temp)
{
    if (temp < 100) return WaterTempStatus::Low;
    if (temp < 108) return WaterTempStatus::Middle;
    return WaterTempStatus::High;
}

// ---- OilTemp ----
enum class OilTempStatus { Low, Middle, High };

inline OilTempStatus oilTempStatus(int temp)
{
    if (temp < 120) return OilTempStatus::Low;
    if (temp < 140) return OilTempStatus::Middle;
    return OilTempStatus::High;
}

// ---- OilPress (required pressure scales with rpm^2) ----
enum class OilPressStatus { Low, Middle, High };

struct OilPress {
    static constexpr double COEFFICIENT_LOW = 0.00000172;
    static constexpr double COEFFICIENT_HIGH = 0.00000241088030949;

    double value = 0.0;
    int rpm = 0;

    OilPressStatus status() const
    {
        const double rpm2 = static_cast<double>(rpm) * rpm;
        if (value < COEFFICIENT_LOW * rpm2) return OilPressStatus::Low;
        if (value < COEFFICIENT_HIGH * rpm2) return OilPressStatus::Middle;
        return OilPressStatus::High;
    }
};

// ---- FuelPress ----
enum class FuelPressStatus { Low, High };

inline FuelPressStatus fuelPressStatus(double press)
{
    return press < 50.0 ? FuelPressStatus::Low : FuelPressStatus::High;
}

// ---- Gear (IST voltage table; index 0 = Neutral) ----
inline constexpr std::array<double, 5> GEAR_EACH_VOLTAGES = {0.8, 1.53, 2.16, 2.84, 3.52};

inline int gearFromVoltage(double voltage)
{
    std::size_t best = 0;
    double bestDev = std::abs(voltage - GEAR_EACH_VOLTAGES[0]);
    for (std::size_t i = 1; i < GEAR_EACH_VOLTAGES.size(); ++i) {
        const double dev = std::abs(voltage - GEAR_EACH_VOLTAGES[i]);
        if (dev < bestDev) {
            bestDev = dev;
            best = i;
        }
    }
    return static_cast<int>(best);
}

// ---- Battery ----
enum class BatteryStatus { Low, High };

inline BatteryStatus batteryStatus(double voltage)
{
    return voltage < 11.0 ? BatteryStatus::Low : BatteryStatus::High;
}

// ---- BrakePress ----
struct BrakePress {
    double front = 0.0;
    double rear = 0.0;

    double bias() const
    {
        if (front <= 0.0 && rear <= 0.0) return 0.0;
        const double f = std::max(0.0, front);
        const double r = std::max(0.0, rear);
        return std::round(100.0 * f / (f + r) * 10.0) / 10.0;
    }
};

// ---- Aggregate ----
struct DashMachineInfo {
    int rpm = 0;
    double throttlePosition = 0.0;
    int waterTemp = 0;
    int oilTemp = 0;
    OilPress oilPress;
    double gearVoltage = GEAR_EACH_VOLTAGES[0];
    double batteryVoltage = 0.0;
    bool fanEnabled = false;
    double fuelPress = 0.0;
    BrakePress brakePress;

    void setRpm(int r)
    {
        rpm = r;
        oilPress.rpm = r;
    }
};

}  // namespace kmm::models
