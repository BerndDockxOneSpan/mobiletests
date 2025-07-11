from __future__ import annotations

from .relayboard_base import RelayBoard

import ftd2xx as ft


class UsbRelayBoard(RelayBoard):
    """
    Implementation of the RelayBoard class for the 4 relay relay board with
    the D2XX chip
    """
    # A list of bytes to control the relays
    # 0: 0x01
    # 1: 0x02
    # 2: 0x04
    # 3: 0x08
    # All: 0x0F
    RELAY_VALUES = [0x0F, 0x01, 0x02, 0x04, 0x08]
    
    def __init__(self, index: int | str) -> None:
        if isinstance(index, str):
            for i in range(ft.createDeviceInfoList()):
                info = ft.getDeviceInfoDetail(i, False)
                if info['serial'].decode('ascii') == index:
                    index = info['index']
                    break
        if isinstance(index, str):
            raise ValueError(f"Could not find board for Serial number {index}")
        self.device = ft.open(index)  # Opens the device, if it's connected
        # Set up the FTDI device as "Bit Bang" mode.
        self.device.setBitMode(0xFF, 0x01)

    @property
    def relay_count(self) -> int:
        return 4

    def close(self) -> None:
        self.device.close()

    def set_relay(self, relay: int, state: bool) -> None:
        if relay > self.relay_count:
            raise ValueError(f"This board only has 4 relays, relay {relay} is "
                             f"outside of this range")
        self._set_relay(UsbRelayBoard.RELAY_VALUES[relay], state)

    def get_firmware_version(self) -> str:
        device_details = ft.getDeviceInfoDetail(0, False)
        return (f"Relay board {device_details['serial'].decode()}: "
                f"{device_details['description'].decode()}")

    def _set_relay(self, relay_value: int, state: bool) -> None:
        # get the current state of the relay
        relay_states = self.device.getBitMode()
        if state:
            self.device.write(bytes([relay_states | relay_value]))
        else:
            self.device.write(bytes([relay_states & ~relay_value]))
    
    @staticmethod
    def list_boards() -> list[str]:
        devices_info = []
        for i in range(ft.createDeviceInfoList()):
            info = ft.getDeviceInfoDetail(i, False)
            devices_info.append(f"Type: 1 (USB Relay Board), "
                                f"index: {info['index']}, id: {info['id']}, "
                                f"serial: {info['serial'].decode('ascii')}, "
                                f"description: "
                                f"{info['description'].decode('ascii')}")
        return devices_info

    @staticmethod
    def create(port: str | int | None = None) -> UsbRelayBoard:
        if port is None:
            port_to_use = 0
        elif isinstance(port, str) and port.isnumeric():
            port_to_use = int(port)
        else:
            port_to_use = port
        return UsbRelayBoard(port_to_use)
