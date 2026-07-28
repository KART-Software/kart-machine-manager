// Port of app/src/gui/self_defined_widgets.py.
#pragma once

#include <array>
#include <optional>

#include <QColor>
#include <QFont>
#include <QGridLayout>
#include <QGroupBox>
#include <QHash>
#include <QLabel>
#include <QProgressBar>
#include <QString>
#include <QWidget>

#include "models.hpp"

namespace kmm {

// QLabel whose font pixel size tracks the widget size:
// pixelSize = min(width / 2, height) * fontScale.
class QCustomLabel : public QLabel {
    Q_OBJECT
public:
    explicit QCustomLabel(QWidget* parent = nullptr);

    void setFontFamily(const QString& family);
    void setFontScale(double scale);

protected:
    void resizeEvent(QResizeEvent* event) override;

private:
    QFont font_;
    double fontScale_ = 1.0;
};

// Title (amber, scale 0.55) over value (white bold, scale 0.75), with cached
// warning background styles and a dirty check to avoid re-setting styles.
class TitleValueBox : public QGroupBox {
    Q_OBJECT
public:
    explicit TitleValueBox(const QString& title, QWidget* parent = nullptr);

    void updateValueLabel(int value);
    void updateValueLabel(double value);  // one decimal, like Python str(x/10)
    void updateBoolValueLabel(bool value);

    void updateWaterTempWarning(int waterTemp);
    void updateOilTempWarning(int oilTemp);
    void updateOilPressWarning(const models::OilPress& oilPress);
    void updateFanWarning(bool fanEnabled);

    // Public like the Python attributes: MainWindow tweaks these directly
    // (SWITCH CHECK box, message box).
    QGridLayout* layout = nullptr;
    QCustomLabel* titleLabel = nullptr;
    QCustomLabel* valueLabel = nullptr;

private:
    void applyWarningStyle(const QString& color);

    QHash<QString, QString> warningStyles_;
    QString lastWarningStyle_;
};

// Icon + auto-scaling value label (battery voltage / clock / message).
class IconValueBox : public QGroupBox {
    Q_OBJECT
public:
    explicit IconValueBox(const QString& iconPath, QWidget* parent = nullptr);

    void updateBatteryValueLabel(double batteryVoltage);
    void updateMessageLabel(const QString& text);
    void updateTime();  // JST (UTC+9) HH:MM, dirty-checked

    QGridLayout* layout = nullptr;
    QLabel* iconLabel = nullptr;
    QCustomLabel* valueLabel = nullptr;
};

// Vertical progress bar for pedals (TPS green /100, BPS red /600).
class PedalBar : public QProgressBar {
    Q_OBJECT
public:
    PedalBar(const QString& barColor, int maxValue, QWidget* parent = nullptr);

    void updatePedalBar(double value);
};

// One light of the shift light bar.
class RpmLight : public QWidget {
    Q_OBJECT
public:
    static constexpr int SHIFT_RPM = 8700;

    RpmLight(int onRpm, const QString& onColor, QWidget* parent = nullptr);

    void updateRpmLightColor(int rpm);

private:
    int onRpm_;
    QColor offColor_;
    QColor onColor_;
    QColor shiftColor_;
    std::optional<QColor> lastColor_;
};

// 12 lights: 4 green, 4 yellow, 2 red, 2 blue (shift point 9000 tuning).
class RpmLightBar : public QGroupBox {
    Q_OBJECT
public:
    explicit RpmLightBar(QWidget* parent = nullptr);

    void updateRpmBar(int rpm);

private:
    std::array<RpmLight*, 12> lights_{};
};

class GearLabel : public QCustomLabel {
    Q_OBJECT
public:
    explicit GearLabel(QWidget* parent = nullptr);

    void updateGearLabel(int gearType);  // 0 = Neutral

private:
    std::optional<int> lastGearType_;
    QString neutralStyle_;
    QString normalStyle_;
    QString lastStyle_;
};

class RpmLabel : public QCustomLabel {
    Q_OBJECT
public:
    explicit RpmLabel(QWidget* parent = nullptr);

    void updateRpmLabel(int rpm);
};

class LapTimeLabel : public QCustomLabel {
    Q_OBJECT
public:
    explicit LapTimeLabel(QWidget* parent = nullptr);

    void updateLapTimeLabel(double laptime);
};

}  // namespace kmm
