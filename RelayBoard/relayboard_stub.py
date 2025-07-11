from __future__ import annotations

from .relayboard_base import RelayBoard, log


class StubRelayBoard(RelayBoard):
    """
    Stub implementation of RelayBoard for testing purposes.
    """

    @property
    def relay_count(self) -> int:
        return 24

    def close(self) -> None:
        pass

    def set_relay(self, relay: int, state: bool) -> None:
        if not 0 <= relay <= self.relay_count:
            log.error(f"Cannot set relay {relay} to {'A' if state else 'U'}, "
                      f"out of range of available relays "
                      f"[0, {self.relay_count}]")
        else:
            state_text = 'A' if state else 'U'
            log.info(f"*** Setting relay #{relay} to {state_text} ***")

    def get_firmware_version(self) -> str:
        return "Stub RelayBoard v1.0"

    @staticmethod
    def create() -> StubRelayBoard:
        return StubRelayBoard()

    @staticmethod
    def list_boards() -> list[str]:
        return ["Type: 3 (Stub Relay Board)"]
