"""Minimal python-can replacement for this project.

Drop-in for the subset of python-can we actually use:

    from src import canbus as can

    bus = can.Bus(channel="can0", interface="socketcan")   # or "virtual"
    can.Notifier(bus, [listener])                          # listener: can.Listener

Implemented with the standard library only (socket.AF_CAN + struct), which
removes python-can's ~0.25s cold import cost (pkg_resources plugin scan).
Classic CAN 2.0 frames only (no FD) — matches the kart's 1Mbps bus.
"""

from src.canbus.bus import Bus, CanBus, SocketCanBus, VirtualBus
from src.canbus.message import Message
from src.canbus.notifier import Listener, Notifier

# python-can compatibility alias (e.g. `bus: can.BusABC` annotations)
BusABC = CanBus

__all__ = [
    "Bus",
    "BusABC",
    "CanBus",
    "SocketCanBus",
    "VirtualBus",
    "Message",
    "Listener",
    "Notifier",
]
