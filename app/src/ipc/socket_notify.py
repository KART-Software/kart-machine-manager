import argparse
import os
import socket
import sys
import time

from .socket_trigger_server import DEFAULT_SOCKET_PATH

RETRY_INTERVAL = 0.1


def send_command(command: str, socket_path: str) -> str:
    while True:
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
                client.connect(socket_path)
                client.sendall((command.strip() + "\n").encode("utf-8"))
                res = client.recv(1024)
            return res.decode("utf-8", errors="ignore").strip()
        except (FileNotFoundError, ConnectionRefusedError):
            time.sleep(RETRY_INTERVAL)


def main() -> int:
    parser = argparse.ArgumentParser(description="Send command to kart daemon")
    parser.add_argument("command", nargs="?", default="START")
    parser.add_argument(
        "--socket-path",
        default=os.getenv("KMM_SOCKET_PATH", DEFAULT_SOCKET_PATH),
    )
    args = parser.parse_args()

    try:
        response = send_command(args.command, args.socket_path)
    except OSError as exc:
        print(f"Socket connection failed: {exc}", file=sys.stderr)
        return 1

    print(response)
    if response in {"ACK_STARTED", "ACK_ALREADY_RUNNING", "PONG", "ACK_STOPPING"}:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
