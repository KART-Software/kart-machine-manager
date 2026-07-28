#include "cloud.hpp"

#include <QDateTime>
#include <QJsonDocument>
#include <QJsonObject>
#include <QNetworkReply>
#include <QNetworkRequest>
#include <QTimeZone>

namespace kmm {

// ---- RunIdFetcher ----

RunIdFetcher::RunIdFetcher(const Config& config,
                           std::function<void(std::uint32_t)> onRunId,
                           QObject* parent)
    : QObject(parent),
      endpoint_(config.cloudRunApiEndpoint),
      machineId_(config.machineId),
      onRunId_(std::move(onRunId))
{
}

void RunIdFetcher::start()
{
    attempt();
}

void RunIdFetcher::attempt()
{
    // getRunId() posts the UTC start time with microsecond precision (%f).
    const QDateTime now = QDateTime::currentDateTimeUtc();
    const QString startAt =
        now.toString(QStringLiteral("yyyy-MM-ddTHH:mm:ss.zzz")) +
        QStringLiteral("000Z");

    QJsonObject body;
    body[QStringLiteral("start_at")] = startAt;
    body[QStringLiteral("machine_id")] = machineId_;

    QNetworkRequest request{QUrl(endpoint_)};
    request.setHeader(QNetworkRequest::ContentTypeHeader,
                      QStringLiteral("application/json"));

    QNetworkReply* reply =
        manager_.post(request, QJsonDocument(body).toJson(QJsonDocument::Compact));
    connect(reply, &QNetworkReply::finished, this, [this, reply] {
        reply->deleteLater();
        bool ok = false;
        std::uint32_t runId = 0;
        const int status =
            reply->attribute(QNetworkRequest::HttpStatusCodeAttribute).toInt();
        if (reply->error() == QNetworkReply::NoError && status == 200) {
            const QJsonDocument doc = QJsonDocument::fromJson(reply->readAll());
            const QJsonValue id = doc.object()
                                      .value(QStringLiteral("run"))
                                      .toObject()
                                      .value(QStringLiteral("id"));
            if (id.isDouble()) {
                runId = static_cast<std::uint32_t>(id.toDouble());
                ok = true;
            }
        }
        if (ok) {
            qInfo("Run ID: %u", runId);
            onRunId_(runId);
        } else {
            QTimer::singleShot(1000, this, [this] { attempt(); });
        }
    });
}

// ---- Messenger ----

Messenger::Messenger(const Config& config, QObject* parent)
    : QObject(parent),
      messageEndpoint_(config.cloudMessageApiEndpoint),
      laptimeEndpoint_(config.cloudLaptimeApiEndpoint)
{
    timer_.setInterval(5000);
    connect(&timer_, &QTimer::timeout, this, [this] { poll(); });
}

void Messenger::start()
{
    poll();
    timer_.start();
}

void Messenger::poll()
{
    QNetworkRequest messageRequest{QUrl(messageEndpoint_)};
    messageRequest.setTransferTimeout(5000);
    QNetworkReply* messageReply = manager_.get(messageRequest);
    connect(messageReply, &QNetworkReply::finished, this, [this, messageReply] {
        messageReply->deleteLater();
        if (messageReply->error() != QNetworkReply::NoError) {
            qWarning("Get message failed!");
            return;
        }
        const QJsonDocument doc = QJsonDocument::fromJson(messageReply->readAll());
        const QJsonValue text = doc.object()
                                    .value(QStringLiteral("message"))
                                    .toObject()
                                    .value(QStringLiteral("text"));
        if (text.isString()) message_.text = text.toString();
    });

    QNetworkRequest laptimeRequest{QUrl(laptimeEndpoint_)};
    laptimeRequest.setTransferTimeout(5000);
    QNetworkReply* laptimeReply = manager_.get(laptimeRequest);
    connect(laptimeReply, &QNetworkReply::finished, this, [this, laptimeReply] {
        laptimeReply->deleteLater();
        if (laptimeReply->error() != QNetworkReply::NoError) {
            qWarning("Get laptime failed!");
            return;
        }
        const QJsonDocument doc = QJsonDocument::fromJson(laptimeReply->readAll());
        const QJsonValue laptime = doc.object().value(QStringLiteral("laptime"));
        if (laptime.isDouble()) {
            message_.laptime = laptime.toDouble();
        } else if (laptime.isString()) {
            bool ok = false;
            const double value = laptime.toString().toDouble(&ok);
            if (ok) message_.laptime = value;
        }
    });
}

}  // namespace kmm
