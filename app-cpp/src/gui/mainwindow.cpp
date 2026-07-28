#include "gui/mainwindow.hpp"

#include <QApplication>
#include <QColor>
#include <QGridLayout>
#include <QPalette>

namespace kmm {

MainWindow::MainWindow(QWidget* parent) : QDialog(parent)
{
    resize(800, 480);

    connect(&timer_, &QTimer::timeout, this, [this] {
        if (onUpdate_) onUpdate_();
    });
    timer_.start(50);

    QPalette palette = QApplication::palette();
    palette.setColor(backgroundRole(), QColor(QStringLiteral("#000")));
    palette.setColor(foregroundRole(), QColor(QStringLiteral("#FFF")));
    setPalette(palette);

    createAllWidgets();
    createTopGroupBox();
    createLeftGroupBox();
    createCenterGroupBox();
    createRightGroupBox();
    createBottomGroupBox();

    auto* mainLayout = new QGridLayout();
    mainLayout->setContentsMargins(0, 0, 0, 0);
    mainLayout->setSpacing(0);
    setLayout(mainLayout);
    mainLayout->addWidget(topGroupBox_, 0, 0, 1, 3);
    mainLayout->addWidget(leftGroupBox_, 1, 0, 1, 1);
    mainLayout->addWidget(centerGroupBox_, 1, 1, 1, 1);
    mainLayout->addWidget(rightGroupBox_, 1, 2, 1, 1);
    mainLayout->addWidget(bottomGroupBox_, 2, 0, 1, 3);

    mainLayout->setColumnStretch(0, 3);
    mainLayout->setColumnStretch(1, 2);
    mainLayout->setColumnStretch(2, 3);
    mainLayout->setRowStretch(0, 1);
    mainLayout->setRowStretch(1, 6);
    mainLayout->setRowStretch(2, 1);
}

void MainWindow::setUpdateCallback(std::function<void()> onUpdate)
{
    onUpdate_ = std::move(onUpdate);
}

void MainWindow::updateDashboard(const models::DashMachineInfo& info,
                                 const Message& message)
{
    rpmLightBar_->updateRpmBar(info.rpm);
    rpmLabel_->updateRpmLabel(info.rpm);
    gearLabel_->updateGearLabel(models::gearFromVoltage(info.gearVoltage));
    waterTempTitleValueBox_->updateValueLabel(info.waterTemp);
    waterTempTitleValueBox_->updateWaterTempWarning(info.waterTemp);
    oilTempTitleValueBox_->updateValueLabel(info.oilTemp);
    oilTempTitleValueBox_->updateOilTempWarning(info.oilTemp);
    oilPressTitleValueBox_->updateValueLabel(info.oilPress.value);
    oilPressTitleValueBox_->updateOilPressWarning(info.oilPress);
    messageIconValueBox_->updateMessageLabel(message.text);
    lapTimeLabel_->updateLapTimeLabel(message.laptime);
    timeIconValueBox_->updateTime();
    fuelPressTitleValueBox_->updateValueLabel(info.fuelPress);
    fanSwitchStateTitleValueBox_->updateBoolValueLabel(info.fanEnabled);
    fanSwitchStateTitleValueBox_->updateFanWarning(info.fanEnabled);
    brakeBiasTitleValueBox_->updateValueLabel(info.brakePress.bias());
    tpsTitleValueBox_->updateValueLabel(info.throttlePosition);
    bpsFTitleValueBox_->updateValueLabel(info.brakePress.front);
    bpsRTitleValueBox_->updateValueLabel(info.brakePress.rear);
    tpsBar_->updatePedalBar(info.throttlePosition);
    bpsFBar_->updatePedalBar(info.brakePress.front);
    bpsRBar_->updatePedalBar(info.brakePress.rear);
    batteryIconValueBox_->updateBatteryValueLabel(info.batteryVoltage);
}

void MainWindow::createAllWidgets()
{
    rpmLabel_ = new RpmLabel(this);
    gearLabel_ = new GearLabel(this);
    lapTimeLabel_ = new LapTimeLabel(this);

    waterTempTitleValueBox_ = new TitleValueBox(QStringLiteral("Water Temp"), this);
    oilTempTitleValueBox_ = new TitleValueBox(QStringLiteral("Oil Temp"), this);
    oilPressTitleValueBox_ = new TitleValueBox(QStringLiteral("Oil Press"), this);
    fuelPressTitleValueBox_ = new TitleValueBox(QStringLiteral("Fuel Press"), this);
    fanSwitchStateTitleValueBox_ =
        new TitleValueBox(QStringLiteral("Fan Switch"), this);
    switchStateReminderLabel_ = new TitleValueBox(
        QStringLiteral("SWITCH CHECK! \n1. Fan \n2. TPS MAX"), this);
    switchStateReminderLabel_->titleLabel->setAlignment(Qt::AlignVCenter);
    switchStateReminderLabel_->titleLabel->setFontScale(0.25);
    switchStateReminderLabel_->layout->setRowStretch(0, 1);
    switchStateReminderLabel_->layout->setRowStretch(1, 0);

    tpsTitleValueBox_ = new TitleValueBox(QStringLiteral("TPS"), this);
    bpsFTitleValueBox_ = new TitleValueBox(QStringLiteral("BPS F"), this);
    bpsRTitleValueBox_ = new TitleValueBox(QStringLiteral("BPS R"), this);
    brakeBiasTitleValueBox_ =
        new TitleValueBox(QStringLiteral("Brake\nBias F%"), this);
    tpsBar_ = new PedalBar(QStringLiteral("#0F0"), 100, this);
    bpsFBar_ = new PedalBar(QStringLiteral("#F00"), 600, this);
    bpsRBar_ = new PedalBar(QStringLiteral("#F00"), 600, this);
    bpsRBar_->setInvertedAppearance(true);

    batteryIconValueBox_ =
        new IconValueBox(QStringLiteral(":/icons/BatteryIcon.png"), this);
    timeIconValueBox_ =
        new IconValueBox(QStringLiteral(":/icons/TimeIcon.png"), this);
    messageIconValueBox_ =
        new IconValueBox(QStringLiteral(":/icons/MeesageIcon.png"), this);
    messageIconValueBox_->valueLabel->setAlignment(Qt::AlignVCenter);
    messageIconValueBox_->layout->setColumnStretch(0, 1);
    messageIconValueBox_->layout->setColumnStretch(1, 6);
}

void MainWindow::createTopGroupBox()
{
    topGroupBox_ = new QGroupBox(this);
    topGroupBox_->setFlat(true);

    auto* layout = new QGridLayout();
    rpmLightBar_ = new RpmLightBar(this);
    layout->addWidget(rpmLightBar_, 0, 0);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->setSpacing(0);

    topGroupBox_->setLayout(layout);
}

void MainWindow::createLeftGroupBox()
{
    leftGroupBox_ = new QGroupBox(this);
    leftGroupBox_->setFlat(true);
    leftGroupBox_->setObjectName(QStringLiteral("LeftBox"));
    leftGroupBox_->setStyleSheet(
        QStringLiteral("QGroupBox#LeftBox { border: 2px solid white;}"));

    auto* layout = new QGridLayout();
    layout->addWidget(waterTempTitleValueBox_, 0, 0);
    layout->addWidget(oilTempTitleValueBox_, 1, 0);
    layout->addWidget(oilPressTitleValueBox_, 1, 1);
    layout->addWidget(fuelPressTitleValueBox_, 0, 1);
    layout->addWidget(fanSwitchStateTitleValueBox_, 2, 0);
    layout->addWidget(switchStateReminderLabel_, 2, 1);
    layout->setRowStretch(0, 1);
    layout->setRowStretch(1, 1);
    layout->setRowStretch(2, 1);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->setSpacing(0);

    leftGroupBox_->setLayout(layout);
}

void MainWindow::createCenterGroupBox()
{
    centerGroupBox_ = new QGroupBox(this);
    centerGroupBox_->setFlat(true);
    centerGroupBox_->setStyleSheet(QStringLiteral("border: 2px solid white;"));

    auto* layout = new QGridLayout();
    layout->addWidget(rpmLabel_, 0, 0, 1, 2);
    layout->addWidget(gearLabel_, 1, 0, 1, 2);
    layout->addWidget(lapTimeLabel_, 2, 0, 1, 2);
    layout->setRowStretch(0, 2);
    layout->setRowStretch(1, 10);
    layout->setRowStretch(2, 3);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->setSpacing(0);

    centerGroupBox_->setLayout(layout);
}

void MainWindow::createRightGroupBox()
{
    rightGroupBox_ = new QGroupBox(this);
    rightGroupBox_->setFlat(true);
    rightGroupBox_->setObjectName(QStringLiteral("RightBox"));
    rightGroupBox_->setStyleSheet(
        QStringLiteral("QGroupBox#RightBox { border: 2px solid white;}"));

    auto* layout = new QGridLayout();
    layout->addWidget(brakeBiasTitleValueBox_, 0, 0, 1, 1);
    layout->addWidget(tpsTitleValueBox_, 1, 0, 1, 1);
    layout->addWidget(tpsBar_, 0, 1, 2, 1);
    layout->addWidget(bpsFBar_, 0, 2);
    layout->addWidget(bpsFTitleValueBox_, 0, 3);
    layout->addWidget(bpsRBar_, 1, 2);
    layout->addWidget(bpsRTitleValueBox_, 1, 3);

    layout->setColumnStretch(0, 2);
    layout->setColumnStretch(1, 1);
    layout->setColumnStretch(2, 1);
    layout->setColumnStretch(3, 2);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->setSpacing(0);

    rightGroupBox_->setLayout(layout);
}

void MainWindow::createBottomGroupBox()
{
    bottomGroupBox_ = new QGroupBox(this);
    bottomGroupBox_->setFlat(true);
    bottomGroupBox_->setStyleSheet(QStringLiteral("border: 0px;"));

    auto* layout = new QGridLayout();
    layout->addWidget(messageIconValueBox_, 0, 0);
    layout->addWidget(batteryIconValueBox_, 0, 1);
    layout->addWidget(timeIconValueBox_, 0, 2);

    layout->setColumnStretch(0, 3);
    layout->setColumnStretch(1, 1);
    layout->setColumnStretch(2, 1);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->setSpacing(0);

    bottomGroupBox_->setLayout(layout);
}

}  // namespace kmm
