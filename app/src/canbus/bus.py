import queue
import socket
import struct
import threading
import time
from typing import Dict, List, Optional

from src.canbus.message import Message

# struct can_frame (linux/can.h): u32 can_id, u8 dlc, 3 pad bytes, u8 data[8]
_CAN_FRAME_FMT = "<IB3x8s"
_CAN_FRAME_SIZE = struct.calcsize(_CAN_FRAME_FMT)  # 16

_CAN_EFF_FLAG = 0x80000000
_CAN_RTR_FLAG = 0x40000000
_CAN_ERR_FLAG = 0x20000000
_CAN_EFF_MASK = 0x1FFFFFFF
_CAN_SFF_MASK = 0x000007FF


def pack_frame(msg: Message) -> bytes:
    """Message -> raw struct can_frame bytes."""
    can_id = msg.arbitration_id
    if msg.is_extended_id:
        can_id = (can_id & _CAN_EFF_MASK) | _CAN_EFF_FLAG
    else:
        can_id = can_id & _CAN_SFF_MASK
    padded = msg.data.ljust(8, b"\x00")
    return struct.pack(_CAN_FRAME_FMT, can_id, len(msg.data), padded)


def unpack_frame(frame: bytes, timestamp: float) -> Optional[Message]:
    """Raw struct can_frame bytes -> Message. Returns None for error frames."""
    can_id, dlc, data = struct.unpack(_CAN_FRAME_FMT, frame)
    if can_id & _CAN_ERR_FLAG:
        return None
    extended = bool(can_id & _CAN_EFF_FLAG)
    arbitration_id = can_id & (_CAN_EFF_MASK if extended else _CAN_SFF_MASK)
    return Message(
        arbitration_id=arbitration_id,
        data=data[:dlc],
        is_extended_id=extended,
        timestamp=timestamp,
    )


class CanBus:
    """Abstract bus. recv() returns None on timeout."""

    def recv(self, timeout: Optional[float] = None) -> Optional[Message]:
        raise NotImplementedError

    def send(self, msg: Message) -> None:
        raise NotImplementedError

    def shutdown(self) -> None:
        raise NotImplementedError


class SocketCanBus(CanBus):
    """Raw SocketCAN via the standard library (Linux only)."""

    def __init__(self, channel: str) -> None:
        if not hasattr(socket, "AF_CAN"):
            raise OSError("SocketCAN is not available on this platform")
        self._sock = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        self._sock.bind((channel,))
        self.channel = channel

    def recv(self, timeout: Optional[float] = None) -> Optional[Message]:
        self._sock.settimeout(timeout)
        try:
            frame = self._sock.recv(_CAN_FRAME_SIZE)
        except (TimeoutError, socket.timeout):
            return None
        except OSError:
            # Socket closed during shutdown
            return None
        return unpack_frame(frame, time.time())

    def send(self, msg: Message) -> None:
        self._sock.send(pack_frame(msg))

    def shutdown(self) -> None:
        self._sock.close()


class VirtualBus(CanBus):
    """In-process broadcast bus for tests / DEBUG mode (any platform).

    All VirtualBus instances sharing a channel name see each other's sends
    (the sender does not receive its own frames) — same semantics as
    python-can's "virtual" interface within one process.
    """

    _registry: Dict[str, List["VirtualBus"]] = {}
    _registry_lock = threading.Lock()

    def __init__(self, channel: str) -> None:
        self.channel = channel
        self._queue: "queue.Queue[Message]" = queue.Queue()
        with VirtualBus._registry_lock:
            VirtualBus._registry.setdefault(channel, []).append(self)

    def recv(self, timeout: Optional[float] = None) -> Optional[Message]:
        try:
            return self._queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def send(self, msg: Message) -> None:
        stamped = Message(
            arbitration_id=msg.arbitration_id,
            data=msg.data,
            is_extended_id=msg.is_extended_id,
            timestamp=time.time(),
        )
        with VirtualBus._registry_lock:
            buses = VirtualBus._registry.get(self.channel, [])
            peers = [b for b in buses if b is not self]
        for peer in peers:
            peer._queue.put(stamped)

    def shutdown(self) -> None:
        with VirtualBus._registry_lock:
            buses = VirtualBus._registry.get(self.channel, [])
            if self in buses:
                buses.remove(self)


def Bus(channel: str, interface: str = "socketcan") -> CanBus:
    """Factory mirroring python-can's can.Bus(channel=..., interface=...)."""
    if interface == "socketcan":
        return SocketCanBus(channel)
    if interface == "virtual":
        return VirtualBus(channel)
    raise ValueError(f"unsupported interface: {interface}")
