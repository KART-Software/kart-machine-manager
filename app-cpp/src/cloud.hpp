// Cloud HTTP clients (Qt Network, all on the main event loop):
//   RunIdFetcher — port of udp_transmitter.py getRunId(): POST until 200,
//                  1s between attempts, then hand the run ID to a callback.
//   Messenger    — port of message/message.py: poll message + laptime
//                  endpoints every 5s, keep the latest snapshot.
#pragma once

#include <functional>

#include <QNetworkAccessManager>
#include <QObject>
#include <QString>
#include <QTimer>

#include "config.hpp"

namespace kmm {

struct Message {
    QString text;
    double laptime = 0.0;
};

class RunIdFetcher : public QObject {
    Q_OBJECT
public:
    RunIdFetcher(const Config& config, std::function<void(std::uint32_t)> onRunId,
                 QObject* parent = nullptr);

    void start();

private:
    void attempt();

    QNetworkAccessManager manager_;
    QString endpoint_;
    int machineId_;
    std::function<void(std::uint32_t)> onRunId_;
};

class Messenger : public QObject {
    Q_OBJECT
public:
    explicit Messenger(const Config& config, QObject* parent = nullptr);

    void start();
    Message snapshot() const { return message_; }

private:
    void poll();

    QNetworkAccessManager manager_;
    QString messageEndpoint_;
    QString laptimeEndpoint_;
    QTimer timer_;
    Message message_;
};

}  // namespace kmm
