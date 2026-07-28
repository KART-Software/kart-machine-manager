// Port of app/src/gui/gui.py (MainWindow). The 50ms QTimer drives an
// onUpdate callback (the Python WindowListener), which pulls fresh snapshots
// and calls updateDashboard().
#pragma once

#include <functional>

#include <QDialog>
#include <QGroupBox>
#include <QTimer>

#include "cloud.hpp"
#include "gui/widgets.hpp"
#include "models.hpp"

namespace kmm {

class MainWindow : public QDialog {
    Q_OBJECT
public:
    explicit MainWindow(QWidget* parent = nullptr);

    void setUpdateCallback(std::function<void()> onUpdate);
    void updateDashboard(const models::DashMachineInfo& info,
                         const Message& message);

private:
    void createAllWidgets();
    void createTopGroupBox();
    void createLeftGroupBox();
    void createCenterGroupBox();
    void createRightGroupBox();
    void createBottomGroupBox();

    QTimer timer_;
    std::function<void()> onUpdate_;

    QGroupBox* topGroupBox_ = nullptr;
    QGroupBox* leftGroupBox_ = nullptr;
    QGroupBox* centerGroupBox_ = nullptr;
    QGroupBox* rightGroupBox_ = nullptr;
    QGroupBox* bottomGroupBox_ = nullptr;

    RpmLightBar* rpmLightBar_ = nullptr;
    RpmLabel* rpmLabel_ = nullptr;
    GearLabel* gearLabel_ = nullptr;
    LapTimeLabel* lapTimeLabel_ = nullptr;

    TitleValueBox* waterTempTitleValueBox_ = nullptr;
    TitleValueBox* oilTempTitleValueBox_ = nullptr;
    TitleValueBox* oilPressTitleValueBox_ = nullptr;
    TitleValueBox* fuelPressTitleValueBox_ = nullptr;
    TitleValueBox* fanSwitchStateTitleValueBox_ = nullptr;
    TitleValueBox* switchStateReminderLabel_ = nullptr;
    TitleValueBox* tpsTitleValueBox_ = nullptr;
    TitleValueBox* bpsFTitleValueBox_ = nullptr;
    TitleValueBox* bpsRTitleValueBox_ = nullptr;
    TitleValueBox* brakeBiasTitleValueBox_ = nullptr;

    PedalBar* tpsBar_ = nullptr;
    PedalBar* bpsFBar_ = nullptr;
    PedalBar* bpsRBar_ = nullptr;

    IconValueBox* batteryIconValueBox_ = nullptr;
    IconValueBox* timeIconValueBox_ = nullptr;
    IconValueBox* messageIconValueBox_ = nullptr;
};

}  // namespace kmm
