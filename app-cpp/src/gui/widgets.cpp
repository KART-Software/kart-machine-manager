#include "gui/widgets.hpp"

#include <algorithm>
#include <cmath>

#include <QDateTime>
#include <QPalette>
#include <QPixmap>
#include <QResizeEvent>
#include <QSizePolicy>

namespace kmm {
namespace {

// Python str(round(x, n)): fixed n decimals, then trailing zeros stripped
// down to at least one decimal ("12.30" -> "12.3", "12.00" -> "12.0").
QString pyRound(double value, int decimals)
{
    QString s = QString::number(value, 'f', decimals);
    while (s.endsWith(QLatin1Char('0')) && !s.endsWith(QLatin1String(".0"))) {
        s.chop(1);
    }
    return s;
}

}  // namespace

// ---- QCustomLabel ----

QCustomLabel::QCustomLabel(QWidget* parent) : QLabel(parent)
{
    setAlignment(Qt::AlignVCenter | Qt::AlignHCenter);
    setSizePolicy(QSizePolicy::Ignored, QSizePolicy::Ignored);
}

void QCustomLabel::setFontFamily(const QString& family)
{
    font_.setFamily(family);
}

void QCustomLabel::setFontScale(double scale)
{
    fontScale_ = scale;
}

void QCustomLabel::resizeEvent(QResizeEvent* /*event*/)
{
    const double width = size().width() / 2.0;
    const double height = size().height();
    const double baseSize = std::min(width, height);
    font_.setPixelSize(std::max(1, static_cast<int>(baseSize * fontScale_)));
    setFont(font_);
}

// ---- TitleValueBox ----

TitleValueBox::TitleValueBox(const QString& title, QWidget* parent)
    : QGroupBox(parent)
{
    setFlat(true);
    setObjectName(QStringLiteral("TitleValueBox"));
    setStyleSheet(QStringLiteral(
        "QGroupBox#TitleValueBox { border: 1px solid #333; border-radius: 3px;}"));

    titleLabel = new QCustomLabel(this);
    titleLabel->setText(title);
    titleLabel->setFontFamily(QStringLiteral("Arial"));
    titleLabel->setFontScale(0.55);
    titleLabel->setStyleSheet(QStringLiteral(
        "color : #FD6; background-color: #000;font-weight: bold"));

    valueLabel = new QCustomLabel(this);
    valueLabel->setAlignment(Qt::AlignCenter);
    valueLabel->setFontFamily(QStringLiteral("Arial"));
    valueLabel->setFontScale(0.75);
    valueLabel->setStyleSheet(QStringLiteral("font-weight: bold; color : #FFF;"));

    layout = new QGridLayout();
    layout->addWidget(titleLabel, 0, 0);
    layout->addWidget(valueLabel, 1, 0);
    layout->setRowStretch(0, 1);
    layout->setRowStretch(1, 2);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->setSpacing(0);
    setLayout(layout);
}

void TitleValueBox::updateValueLabel(int value)
{
    valueLabel->setText(QString::number(value));
}

void TitleValueBox::updateValueLabel(double value)
{
    valueLabel->setText(QString::number(value, 'f', 1));
}

void TitleValueBox::updateBoolValueLabel(bool value)
{
    valueLabel->setText(value ? QStringLiteral("ON") : QStringLiteral("OFF"));
}

void TitleValueBox::applyWarningStyle(const QString& color)
{
    QString style = warningStyles_.value(color);
    if (style.isEmpty()) {
        style = QStringLiteral("font-weight: bold; border-radius: 5px;"
                               " color: #FFF; background-color: %1;")
                    .arg(color);
        warningStyles_.insert(color, style);
    }
    if (style != lastWarningStyle_) {
        lastWarningStyle_ = style;
        valueLabel->setStyleSheet(style);
    }
}

void TitleValueBox::updateWaterTempWarning(int waterTemp)
{
    QString color;
    switch (models::waterTempStatus(waterTemp)) {
    case models::WaterTempStatus::Low: color = QStringLiteral("#000"); break;
    case models::WaterTempStatus::Middle: color = QStringLiteral("#FB0"); break;
    case models::WaterTempStatus::High: color = QStringLiteral("#F00"); break;
    }
    applyWarningStyle(color);
}

void TitleValueBox::updateOilTempWarning(int oilTemp)
{
    QString color;
    switch (models::oilTempStatus(oilTemp)) {
    case models::OilTempStatus::Low: color = QStringLiteral("#000"); break;
    case models::OilTempStatus::Middle: color = QStringLiteral("#FB0"); break;
    case models::OilTempStatus::High: color = QStringLiteral("#F00"); break;
    }
    applyWarningStyle(color);
}

void TitleValueBox::updateOilPressWarning(const models::OilPress& oilPress)
{
    // Inverted: low oil pressure is the dangerous state.
    QString color;
    switch (oilPress.status()) {
    case models::OilPressStatus::Low: color = QStringLiteral("#F00"); break;
    case models::OilPressStatus::Middle: color = QStringLiteral("#FB0"); break;
    case models::OilPressStatus::High: color = QStringLiteral("#000"); break;
    }
    applyWarningStyle(color);
}

void TitleValueBox::updateFanWarning(bool fanEnabled)
{
    applyWarningStyle(fanEnabled ? QStringLiteral("#000") : QStringLiteral("#F00"));
}

// ---- IconValueBox ----

IconValueBox::IconValueBox(const QString& iconPath, QWidget* parent)
    : QGroupBox(parent)
{
    setFlat(true);

    iconLabel = new QLabel(this);
    iconLabel->setPixmap(QPixmap(iconPath));
    iconLabel->setAlignment(Qt::AlignCenter);

    valueLabel = new QCustomLabel(this);
    valueLabel->setAlignment(Qt::AlignCenter);
    valueLabel->setFontScale(0.6);
    valueLabel->setFontFamily(QStringLiteral("Arial"));
    valueLabel->setStyleSheet(
        QStringLiteral("QLabel { font-weight: bold; color : #FFF; }"));

    layout = new QGridLayout();
    layout->addWidget(iconLabel, 0, 0);
    layout->addWidget(valueLabel, 0, 1);
    layout->setColumnStretch(0, 1);
    layout->setColumnStretch(1, 3);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->setSpacing(0);
    setLayout(layout);
}

void IconValueBox::updateBatteryValueLabel(double batteryVoltage)
{
    valueLabel->setText(pyRound(batteryVoltage, 2) + QStringLiteral(" V"));
}

void IconValueBox::updateMessageLabel(const QString& text)
{
    valueLabel->setText(text);
}

void IconValueBox::updateTime()
{
    const QString text = QDateTime::currentDateTimeUtc()
                             .addSecs(9 * 3600)
                             .toString(QStringLiteral("HH:mm"));
    if (text != valueLabel->text()) {
        valueLabel->setText(text);
    }
}

// ---- PedalBar ----

PedalBar::PedalBar(const QString& barColor, int maxValue, QWidget* parent)
    : QProgressBar(parent)
{
    setSizePolicy(QSizePolicy::Ignored, QSizePolicy::Ignored);
    setMaximum(maxValue);
    setTextVisible(false);
    setOrientation(Qt::Vertical);
    setStyleSheet(QStringLiteral(R"(
            QProgressBar
                {
                    border: 2px solid;
                    border-color: #AAA;
                    border-radius: 5px;
                    background-color: #333;
                }
            QProgressBar::chunk
                {
                    background-color: %1;
                    height: 1px;
                }
            )")
                      .arg(barColor));
}

void PedalBar::updatePedalBar(double value)
{
    setValue(static_cast<int>(value));
}

// ---- RpmLight / RpmLightBar ----

RpmLight::RpmLight(int onRpm, const QString& onColor, QWidget* parent)
    : QWidget(parent),
      onRpm_(onRpm),
      offColor_(QStringLiteral("#333")),
      onColor_(onColor),
      shiftColor_(QStringLiteral("#8FF"))
{
    setAutoFillBackground(true);
    QPalette pal = palette();
    pal.setColor(QPalette::Window, offColor_);
    setPalette(pal);
}

void RpmLight::updateRpmLightColor(int rpm)
{
    QColor color;
    if (rpm < onRpm_) {
        color = offColor_;
    } else if (rpm < SHIFT_RPM) {
        color = onColor_;
    } else {
        color = shiftColor_;
    }
    if (!lastColor_ || color != *lastColor_) {
        lastColor_ = color;
        QPalette pal = palette();
        pal.setColor(QPalette::Window, color);
        setPalette(pal);
    }
}

RpmLightBar::RpmLightBar(QWidget* parent) : QGroupBox(parent)
{
    setFlat(true);
    setObjectName(QStringLiteral("RpmLightBar"));
    setStyleSheet(QStringLiteral("QGroupBox#RpmLightBar { border: 0; }"));

    // shift point 9000
    static constexpr int LIGHT_RPMS[12] = {1000, 2000, 3000, 4000, 5000, 5500,
                                           6000, 6500, 7000, 7500, 8000, 8500};
    static const char* LIGHT_COLORS[12] = {"#0F0", "#0F0", "#0F0", "#0F0",
                                           "#FF0", "#FF0", "#FF0", "#FF0",
                                           "#F00", "#F00", "#8FF", "#8FF"};

    auto* lightLayout = new QGridLayout();
    for (int i = 0; i < 12; ++i) {
        lights_[i] = new RpmLight(LIGHT_RPMS[i],
                                  QString::fromLatin1(LIGHT_COLORS[i]), this);
        lightLayout->addWidget(lights_[i], 0, i);
    }
    setLayout(lightLayout);
}

void RpmLightBar::updateRpmBar(int rpm)
{
    for (auto* light : lights_) light->updateRpmLightColor(rpm);
}

// ---- GearLabel / RpmLabel / LapTimeLabel ----

GearLabel::GearLabel(QWidget* parent) : QCustomLabel(parent)
{
    setAlignment(Qt::AlignCenter);
    setFontFamily(QStringLiteral("Arial"));
    setFontScale(2.5);
    setStyleSheet(
        QStringLiteral("font-weight: bold; color: #FFF; background-color: #000"));
    neutralStyle_ =
        QStringLiteral("font-weight: bold; color: #FD6; background-color: #000");
    normalStyle_ =
        QStringLiteral("font-weight: bold; color: #FFF; background-color: #000");
}

void GearLabel::updateGearLabel(int gearType)
{
    if (lastGearType_ && gearType == *lastGearType_) return;
    lastGearType_ = gearType;

    QString style;
    if (gearType == 0) {
        setText(QStringLiteral("N"));
        style = neutralStyle_;
    } else {
        setText(QString::number(gearType));
        style = normalStyle_;
    }
    if (style != lastStyle_) {
        lastStyle_ = style;
        setStyleSheet(style);
    }
}

RpmLabel::RpmLabel(QWidget* parent) : QCustomLabel(parent)
{
    setAlignment(Qt::AlignCenter);
    setFontFamily(QStringLiteral("Arial"));
    setFontScale(0.8);
    setStyleSheet(
        QStringLiteral("font-weight: bold; color : #FFF; background-color: #000"));
}

void RpmLabel::updateRpmLabel(int rpm)
{
    setText(QString::number(rpm));
}

LapTimeLabel::LapTimeLabel(QWidget* parent) : QCustomLabel(parent)
{
    setAlignment(Qt::AlignCenter);
    setFontFamily(QStringLiteral("Times New Roman"));
    setFontScale(0.8);
    setStyleSheet(QStringLiteral("color : #B6F; background-color: #000"));
}

void LapTimeLabel::updateLapTimeLabel(double laptime)
{
    setText(pyRound(laptime, 2) + QStringLiteral(" s"));
}

}  // namespace kmm
