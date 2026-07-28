from dataclasses import dataclass


@dataclass
class Message:
    """A classic CAN 2.0 frame. Field names mirror python-can's Message."""

    arbitration_id: int = 0
    data: bytes = b""
    is_extended_id: bool = False
    timestamp: float = 0.0

    def __post_init__(self) -> None:
        # Accept bytearray/list like python-can does
        if not isinstance(self.data, bytes):
            self.data = bytes(self.data)
        if len(self.data) > 8:
            raise ValueError(
                f"classic CAN payload is at most 8 bytes, got {len(self.data)}"
            )

    @property
    def dlc(self) -> int:
        return len(self.data)
