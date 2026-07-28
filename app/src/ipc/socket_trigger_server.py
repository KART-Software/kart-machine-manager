import os
import socket
import stat
from typing import Optional

DEFAULT_SOCKET_PATH = f"/run/user/{os.getuid()}/kmm.sock"


class UnixTriggerServer:
    def __init__(self, socket_path: str) -> None:
        self.socket_path = socket_path
        self._server_socket: Optional[socket.socket] = None

    def _cleanup_socket_file(self) -> None:
        if not os.path.exists(self.socket_path):
            return

        mode = os.stat(self.socket_path).st_mode
        if stat.S_ISSOCK(mode):
            os.unlink(self.socket_path)
            return

        raise RuntimeError(f"Path exists and is not a socket: {self.socket_path}")

    def start(self) -> None:
        self._cleanup_socket_file()

        self._server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._server_socket.bind(self.socket_path)
        self._server_socket.listen(1)

    def stop(self) -> None:
        if self._server_socket is not None:
            self._server_socket.close()
            self._server_socket = None

        self._cleanup_socket_file()

    def wait_command(
        self, timeout_sec: float = 1.0
    ) -> tuple[Optional[socket.socket], Optional[str]]:
        if self._server_socket is None:
            raise RuntimeError("Server socket is not started")

        self._server_socket.settimeout(timeout_sec)
        try:
            conn, _ = self._server_socket.accept()
        except TimeoutError:
            return None, None

        raw = conn.recv(1024)
        if not raw:
            return conn, ""

        command = raw.decode("utf-8", errors="ignore").strip().upper()
        return conn, command
