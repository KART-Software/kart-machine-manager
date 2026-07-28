import datetime
import logging
import logging.config
import os
import signal
import threading
from typing import TYPE_CHECKING

from src.ipc.socket_trigger_server import DEFAULT_SOCKET_PATH, UnixTriggerServer
from src.util import config

if TYPE_CHECKING:
    from src.application.application import Application

# Socket-first startup: open the trigger socket immediately and import the
# heavy application stack (PyQt6, python-can, ...) in a background thread.
# START then only waits for whichever finishes later (weston or the preload)
# instead of serializing them.
_preload_done = threading.Event()
_preload_error: BaseException | None = None


def _preload_application() -> None:
    global _preload_error
    try:
        import src.application.application  # noqa: F401
    except BaseException as exc:
        _preload_error = exc
        logging.exception("Preload of application modules failed")
    finally:
        _preload_done.set()


def setup_logging() -> None:
    log_dir = config.logDir
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    base_name = "app_{}".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    log_file_path = os.path.join(log_dir, f"{base_name}.log")
    seq = 1
    while os.path.exists(log_file_path):
        log_file_path = os.path.join(log_dir, f"{base_name}_{seq}.log")
        seq += 1

    logging.config.dictConfig(
        {
            "version": 1,
            "formatters": {
                "common": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                }
            },
            "handlers": {
                "logFileHandler": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "common",
                    "filename": log_file_path,
                    "mode": "w",
                    "encoding": "utf-8",
                    "maxBytes": 10_000_000,
                    "backupCount": 10,
                },
                "info": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "common",
                    "stream": "ext://sys.stdout",
                },
                "error": {
                    "class": "logging.StreamHandler",
                    "level": "ERROR",
                    "formatter": "common",
                    "stream": "ext://sys.stderr",
                },
            },
            "root": {"level": "DEBUG", "handlers": ["logFileHandler", "info", "error"]},
            "disable_existing_loggers": False,
        }
    )
    if config.debug:
        logging.info("Daemon started in DEBUG Mode!")
    else:
        logging.info("Daemon started in PROD Mode!")


def run_daemon() -> None:
    socket_path = os.getenv("KMM_SOCKET_PATH", DEFAULT_SOCKET_PATH)
    socket_path_env = os.getenv("KMM_SOCKET_PATH")
    server = UnixTriggerServer(socket_path)

    threading.Thread(target=_preload_application, daemon=True).start()

    should_stop = False
    is_started = False
    app: "Application | None" = None

    def handle_signal(signum: int, _frame) -> None:
        nonlocal should_stop
        logging.info("Signal %s received. Stopping daemon.", signum)
        should_stop = True
        if app is not None:
            app.shutdown()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    try:
        server.start()
    except PermissionError:
        if socket_path_env is not None:
            raise
        socket_path = "/tmp/kmm.sock"
        server = UnixTriggerServer(socket_path)
        server.start()
        logging.warning(
            "No permission to use %s. Fallback to %s",
            DEFAULT_SOCKET_PATH,
            socket_path,
        )

    logging.info("Listening on unix socket: %s", socket_path)
    logging.info("Send START command to launch the application.")

    try:
        while not should_stop:
            conn, command = server.wait_command()
            if conn is None:
                continue

            with conn:
                if command == "PING":
                    conn.sendall(b"PONG\n")
                    continue

                if command == "STOP":
                    conn.sendall(b"ACK_STOPPING\n")
                    should_stop = True
                    continue

                if command != "START":
                    conn.sendall(b"ERR_UNKNOWN_COMMAND\n")
                    continue

                if is_started:
                    conn.sendall(b"ACK_ALREADY_RUNNING\n")
                    continue

                # Wait for the background preload before ACKing so that
                # kmm-start completion still means "GUI is imminent" (delayed
                # timers for resolved/timesyncd key off kmm-start).
                _preload_done.wait()
                if _preload_error is not None:
                    conn.sendall(b"ERR_PRELOAD_FAILED\n")
                    raise _preload_error

                conn.sendall(b"ACK_STARTED\n")
                is_started = True

            logging.info("START command received. Launching Application.")
            from src.application.application import Application

            app = Application()
            logging.info("Initializing Application...")
            app.initialize()
    finally:
        server.stop()


if __name__ == "__main__":
    setup_logging()
    run_daemon()
