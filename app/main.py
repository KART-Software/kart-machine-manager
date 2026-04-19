import datetime
import logging
import logging.config
import os
import signal

from src.application.application import Application
from src.ipc.socket_trigger_server import DEFAULT_SOCKET_PATH, UnixTriggerServer
from src.util import config


def setup_logging() -> None:
    log_file_path = "log/app_{}.log".format(
        datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    file_path = os.path.dirname(log_file_path)
    if not os.path.exists(file_path):
        os.makedirs(file_path)

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
                    "class": "logging.FileHandler",
                    "level": "DEBUG",
                    "formatter": "common",
                    "filename": log_file_path,
                    "mode": "w",
                    "encoding": "utf-8",
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

    should_stop = False
    is_started = False
    app: Application | None = None

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

                conn.sendall(b"ACK_STARTED\n")
                is_started = True

            logging.info("START command received. Launching Application.")
            app = Application()
            logging.info("Initializing Application...")
            app.initialize()
    finally:
        server.stop()


if __name__ == "__main__":
    setup_logging()
    run_daemon()
