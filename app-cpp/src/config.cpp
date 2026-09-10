#include "config.hpp"

#include <QFile>
#include <QStringList>
#include <QTextStream>

#include <cstdio>
#include <cstdlib>

namespace kmm {
namespace {

// Minimal dotenv: KEY=VALUE lines, '#' comments, does not override existing env.
void loadDotEnv(const QString& path)
{
    QFile file(path);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) return;

    QTextStream in(&file);
    while (!in.atEnd()) {
        QString line = in.readLine().trimmed();
        if (line.isEmpty() || line.startsWith('#')) continue;
        const int eq = line.indexOf('=');
        if (eq <= 0) continue;
        QString key = line.left(eq).trimmed();
        QString value = line.mid(eq + 1).trimmed();
        if ((value.startsWith('"') && value.endsWith('"') && value.size() >= 2) ||
            (value.startsWith('\'') && value.endsWith('\'') && value.size() >= 2)) {
            value = value.mid(1, value.size() - 2);
        }
        ::setenv(key.toUtf8().constData(), value.toUtf8().constData(), /*overwrite=*/0);
    }
}

QString requireEnv(const char* name, QStringList& missing)
{
    const char* value = std::getenv(name);
    if (value == nullptr || *value == '\0') {
        missing.append(QString::fromLatin1(name));
        return {};
    }
    return QString::fromUtf8(value);
}

}  // namespace

Config Config::load()
{
    loadDotEnv(QStringLiteral(".env"));

    QStringList missing;
    Config cfg;
    cfg.machineId = requireEnv("MACHINE_ID", missing).toInt();
    cfg.udpHost = requireEnv("UDP_ADDRESS", missing);
    cfg.udpPort = static_cast<quint16>(requireEnv("UDP_PORT", missing).toUInt());
    cfg.cloudRunApiEndpoint = requireEnv("CLOUD_RUN_API_ENDPOINT", missing);
    cfg.cloudMessageApiEndpoint = requireEnv("CLOUD_MESSAGE_API_ENDPOINT", missing);
    cfg.cloudLaptimeApiEndpoint = requireEnv("CLOUD_LAPTIME_API_ENDPOINT", missing);

    const char* canIf = std::getenv("CAN_INTERFACE");
    cfg.canInterface = (canIf != nullptr && *canIf != '\0') ? QString::fromUtf8(canIf)
                                                             : QStringLiteral("can0");

    const char* debugEnv = std::getenv("DEBUG");
    cfg.debug = debugEnv != nullptr &&
                QString::fromUtf8(debugEnv).toLower() == QStringLiteral("true");

    if (!missing.isEmpty()) {
        std::fprintf(stderr, "Missing required environment variables: %s\n",
                     missing.join(QStringLiteral(", ")).toUtf8().constData());
        std::exit(1);
    }
    return cfg;
}

}  // namespace kmm
