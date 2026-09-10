// Port of app/src/util/config.py. Reads the same environment variables
// (systemd EnvironmentFile=/data/kmm.env in production). Like dotenv, a
// ./.env file is loaded first without overriding existing variables.
#pragma once

#include <QString>

namespace kmm {

struct Config {
    int machineId = 0;
    QString udpHost;
    quint16 udpPort = 0;
    QString cloudRunApiEndpoint;
    QString cloudMessageApiEndpoint;
    QString cloudLaptimeApiEndpoint;
    bool debug = false;
    // SocketCAN interface kmm reads (CAN_INTERFACE, default "can0"). Boards
    // whose CAN comes through the Cortex-M gateway set rpmsgcan0.
    QString canInterface;

    // Exits the process with a clear message when required keys are missing.
    static Config load();
};

}  // namespace kmm
