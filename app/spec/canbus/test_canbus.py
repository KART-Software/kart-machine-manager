import time

import pytest

from src.canbus.bus import VirtualBus, pack_frame, unpack_frame
from src.canbus.message import Message
from src.canbus.notifier import Listener, Notifier


class TestFramePacking:
    def test_roundtrip_standard_id(self):
        msg = Message(arbitration_id=0x5F0, data=b"\x12\x34\x56\x78\x9a\xbc\xde\xf0")
        out = unpack_frame(pack_frame(msg), timestamp=1.0)
        assert out is not None
        assert out.arbitration_id == 0x5F0
        assert out.data == msg.data
        assert out.is_extended_id is False
        assert out.dlc == 8

    def test_roundtrip_extended_id(self):
        msg = Message(arbitration_id=0x1ABCDE, data=b"\x01", is_extended_id=True)
        out = unpack_frame(pack_frame(msg), timestamp=1.0)
        assert out is not None
        assert out.arbitration_id == 0x1ABCDE
        assert out.is_extended_id is True

    def test_short_dlc_preserved(self):
        msg = Message(arbitration_id=0x5F3, data=b"\x00\x01")
        out = unpack_frame(pack_frame(msg), timestamp=1.0)
        assert out is not None
        assert out.dlc == 2
        assert out.data == b"\x00\x01"

    def test_error_frame_is_filtered(self):
        # CAN_ERR_FLAG (0x20000000) set -> treated as error frame
        import struct

        frame = struct.pack("<IB3x8s", 0x20000001, 8, b"\x00" * 8)
        assert unpack_frame(frame, timestamp=1.0) is None

    def test_frame_is_16_bytes(self):
        assert len(pack_frame(Message(arbitration_id=1, data=b""))) == 16


class TestMessage:
    def test_bytearray_coerced(self):
        msg = Message(arbitration_id=1, data=bytearray(b"\x01\x02"))
        assert isinstance(msg.data, bytes)
        assert msg.dlc == 2

    def test_oversized_payload_rejected(self):
        with pytest.raises(ValueError):
            Message(arbitration_id=1, data=b"\x00" * 9)


class TestVirtualBus:
    def test_broadcast_to_peers_not_self(self):
        a = VirtualBus("t1")
        b = VirtualBus("t1")
        try:
            a.send(Message(arbitration_id=0x100, data=b"\x01"))
            got = b.recv(timeout=1.0)
            assert got is not None and got.arbitration_id == 0x100
            assert got.timestamp > 0
            assert a.recv(timeout=0.05) is None  # sender does not self-receive
        finally:
            a.shutdown()
            b.shutdown()

    def test_channels_are_isolated(self):
        a = VirtualBus("t2")
        b = VirtualBus("t3")
        try:
            a.send(Message(arbitration_id=0x100, data=b"\x01"))
            assert b.recv(timeout=0.05) is None
        finally:
            a.shutdown()
            b.shutdown()

    def test_recv_timeout_returns_none(self):
        a = VirtualBus("t4")
        try:
            assert a.recv(timeout=0.05) is None
        finally:
            a.shutdown()


class _Recorder(Listener):
    def __init__(self):
        self.received = []

    def on_message_received(self, msg):
        self.received.append(msg)


class _Exploder(Listener):
    def on_message_received(self, msg):
        raise RuntimeError("boom")


class TestNotifier:
    def _wait_for(self, cond, timeout=2.0):
        deadline = time.time() + timeout
        while time.time() < deadline:
            if cond():
                return True
            time.sleep(0.01)
        return False

    def test_dispatches_to_listeners(self):
        rx = VirtualBus("n1")
        tx = VirtualBus("n1")
        rec1, rec2 = _Recorder(), _Recorder()
        notifier = Notifier(rx, [rec1, rec2])
        try:
            tx.send(Message(arbitration_id=0x5F0, data=b"\x01\x02"))
            assert self._wait_for(lambda: rec1.received and rec2.received)
            assert rec1.received[0].arbitration_id == 0x5F0
        finally:
            notifier.stop()
            rx.shutdown()
            tx.shutdown()

    def test_listener_exception_does_not_kill_thread(self):
        rx = VirtualBus("n2")
        tx = VirtualBus("n2")
        rec = _Recorder()
        notifier = Notifier(rx, [_Exploder(), rec])
        try:
            tx.send(Message(arbitration_id=1, data=b"\x01"))
            tx.send(Message(arbitration_id=2, data=b"\x02"))
            assert self._wait_for(lambda: len(rec.received) == 2)
        finally:
            notifier.stop()
            rx.shutdown()
            tx.shutdown()
