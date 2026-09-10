// kmm — kart dashboard application.
//
// Starts the GUI immediately at process start. Readiness ordering is
// systemd's job: the unit runs After=weston.service (compositor up) and
// After=can0-up.service. The old daemon + notifier split (unix-socket
// START/PING/STOP protocol, kmm-start.service) existed only to hide the
// ~1.5s PyQt6 import behind weston startup; with the C++ port there is
// nothing left to hide, so it was removed.
//
// Type=notify support: READY=1 is sent on the first window expose (i.e.
// "pixels are on screen"), implemented without libsystemd.
#include <cerrno>
#include <csignal>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <memory>

#include <fcntl.h>
#include <stddef.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

#include <QApplication>
#include <QEvent>
#include <QSocketNotifier>
#include <QTimer>
#include <QWindow>

#include "canbus.hpp"
#include "cloud.hpp"
#include "config.hpp"
#include "gui/mainwindow.hpp"
#include "stores.hpp"
#include "udp_transmitter.hpp"

namespace {

int g_signalPipe[2] = {-1, -1};

void handleSignal(int /*signum*/)
{
    const char byte = 1;
    [[maybe_unused]] const ssize_t n = ::write(g_signalPipe[1], &byte, 1);
}

// Minimal sd_notify("READY=1") — no-op unless NOTIFY_SOCKET is set.
void notifySystemdReady()
{
    static bool sent = false;
    if (sent) return;

    const char* path = std::getenv("NOTIFY_SOCKET");
    if (path == nullptr || path[0] == '\0') return;

    struct sockaddr_un addr {};
    addr.sun_family = AF_UNIX;
    const size_t len = std::strlen(path);
    if (len >= sizeof(addr.sun_path)) return;
    std::memcpy(addr.sun_path, path, len);
    if (addr.sun_path[0] == '@') addr.sun_path[0] = '\0';  // abstract namespace

    const int fd = ::socket(AF_UNIX, SOCK_DGRAM | SOCK_CLOEXEC, 0);
    if (fd < 0) return;
    const char msg[] = "READY=1";
    ::sendto(fd, msg, sizeof(msg) - 1, 0,
             reinterpret_cast<struct sockaddr*>(&addr),
             static_cast<socklen_t>(offsetof(struct sockaddr_un, sun_path) + len));
    ::close(fd);
    sent = true;
}

// Logs when the compositor first exposes the window — the closest journal
// marker to "pixels are on screen" (boot-time measurements key off this) —
// and reports readiness to systemd at that moment.
class ExposeLogger : public QObject {
public:
    bool eventFilter(QObject* watched, QEvent* event) override
    {
        if (event->type() == QEvent::Expose && !logged_) {
            logged_ = true;
            std::fprintf(stderr, "First window expose.\n");
            notifySystemdReady();
        }
        return QObject::eventFilter(watched, event);
    }

private:
    bool logged_ = false;
};

// weston と並行起動するための wayland ソケット待ち。
// unit の After=weston を外して両者を同時に fork し、Qt ライブラリの
// ロード/リンク (~0.4s) を weston の初期化と重ねる。QApplication は
// ソケットが無いと即死するので、生成直前にここで待つ (kart-splash-wl と
// 同じ 10ms ポーリング。weston 稼働済みなら一巡もせず抜ける)。
void waitForWaylandSocket()
{
    const char* runtimeDir = std::getenv("XDG_RUNTIME_DIR");
    const char* display = std::getenv("WAYLAND_DISPLAY");
    if (runtimeDir == nullptr || display == nullptr) return;

    std::string path = std::string(runtimeDir) + "/" + display;
    for (int i = 0; i < 1000; ++i) {  // 最大 10s
        if (::access(path.c_str(), F_OK) == 0) {
            if (i > 0)
                std::fprintf(stderr, "Wayland socket appeared after ~%d ms\n",
                             i * 10);
            return;
        }
        ::usleep(10 * 1000);
    }
    std::fprintf(stderr, "Wayland socket did not appear; proceeding\n");
}

}  // namespace

int main(int argc, char** argv)
{
    using namespace kmm;

    const Config config = Config::load();
    std::fprintf(stderr, "kmm starting in %s mode\n",
                 config.debug ? "DEBUG" : "PROD");

    if (::pipe(g_signalPipe) != 0) {
        std::perror("pipe");
        return 1;
    }
    ::fcntl(g_signalPipe[0], F_SETFL, O_NONBLOCK);
    ::fcntl(g_signalPipe[1], F_SETFL, O_NONBLOCK);
    std::signal(SIGINT, handleSignal);
    std::signal(SIGTERM, handleSignal);
    std::signal(SIGPIPE, SIG_IGN);

    waitForWaylandSocket();
    QApplication app(argc, argv);

    // SIGINT/SIGTERM quit the event loop cleanly (self-pipe pattern).
    QSocketNotifier signalNotifier(g_signalPipe[0], QSocketNotifier::Read);
    QObject::connect(&signalNotifier, &QSocketNotifier::activated, &app, [&] {
        char byte;
        [[maybe_unused]] const ssize_t n = ::read(g_signalPipe[0], &byte, 1);
        std::fprintf(stderr, "Signal received. Shutting down.\n");
        app.quit();
    });

    // CAN source: real SocketCAN (CAN_INTERFACE, default can0) or the built-in
    // mock generator (DEBUG=TRUE).
    std::unique_ptr<CanSource> canSource;
    if (config.debug) {
        canSource = std::make_unique<MockCanSource>();
    } else {
        std::fprintf(stderr, "CAN interface: %s\n", config.canInterface.toUtf8().constData());
        canSource = std::make_unique<SocketCanSource>(config.canInterface.toStdString());
    }

    DashInfoStore dashInfoStore;
    UdpPayloadStore udpPayloadStore;
    CanReader canReader(*canSource,
                        {[&](const CanFrame& f) { dashInfoStore.onFrame(f); },
                         [&](const CanFrame& f) { udpPayloadStore.onFrame(f); }});

    UdpTransmitter udpTransmitter(udpPayloadStore, config);
    RunIdFetcher runIdFetcher(config, [&](std::uint32_t runId) {
        udpTransmitter.start(runId);
    });
    runIdFetcher.start();

    Messenger messenger(config);
    messenger.start();

    MainWindow window;
    window.setUpdateCallback([&] {
        window.updateDashboard(dashInfoStore.snapshot(), messenger.snapshot());
    });
    window.show();
    std::fprintf(stderr, "Main window shown; entering event loop.\n");
    ExposeLogger exposeLogger;
    if (window.windowHandle() != nullptr) {
        window.windowHandle()->installEventFilter(&exposeLogger);
    }
    // Fallback for platforms that never deliver Expose (e.g. offscreen):
    // still report READY shortly after the event loop starts.
    QTimer::singleShot(1000, &app, [] { notifySystemdReady(); });

    const int rc = app.exec();

    udpTransmitter.stop();
    canReader.stop();
    return rc;
}
