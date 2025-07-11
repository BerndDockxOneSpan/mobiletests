from __future__ import annotations

from .relayboard_base import RelayBoard

from pyftdi.i2c import I2cController


class FtdiI2cRelayBoard(RelayBoard):
    """
    Implementation of the RelayBoard class for the FTDI I2C relay board
    """
    CMD_CHANNEL_CTRL = 0x10
    CMD_SAVE_I2C_ADDR = 0x11
    CMD_READ_I2C_ADDR = 0x12
    CMD_READ_FIRMWARE_VER = 0x13
    DEFAULT_I2C_URL = 'ftdi:///1'
    DEFAULT_I2C_ADDRESS = 0x11

    def __init__(self, i2c_url: str = DEFAULT_I2C_URL, 
                 address: int = DEFAULT_I2C_ADDRESS) -> None:
        if I2cController is None:
            raise ImportError("pyftdi is required for FTDI I2C relay board "
                              "support.")
        self.i2c_url = i2c_url
        self.address = address
        self.i2c = I2cController()
        self.i2c.configure(self.i2c_url)
        self.slave = self.i2c.get_port(self.address)
        self.channel_state = 0

    @property
    def relay_count(self) -> int:
        return 4

    def close(self) -> None:
        self.i2c.close()

    def set_relay(self, relay: int, state: bool) -> None:
        if not 1 <= relay <= self.relay_count:
            raise ValueError(f"Relay {relay} is out of range for FTDI I2C "
                             f"relay board (1-{self.relay_count})")
        if not state:
            self.channel_state |= (1 << (relay - 1))
        else:
            self.channel_state &= ~(1 << (relay - 1))
        self.slave.write([self.CMD_CHANNEL_CTRL, self.channel_state])

    def get_firmware_version(self) -> str:
        self.slave.write([self.CMD_READ_FIRMWARE_VER])
        return str(self.slave.read(1)[0])

    @staticmethod
    def create(i2c_addr: int | None = None) -> FtdiI2cRelayBoard:
        address = (i2c_addr if i2c_addr is not None 
                   else FtdiI2cRelayBoard.DEFAULT_I2C_ADDRESS)
        return FtdiI2cRelayBoard(address=address)

    @staticmethod
    def scan_i2c_devices(i2c_url: str = DEFAULT_I2C_URL) -> list[int]:
        if I2cController is None:
            raise ImportError("pyftdi is required for FTDI I2C relay board "
                              "support.")
        i2c = I2cController()
        i2c.configure(i2c_url)
        found = []
        for addr in range(1, 128):
            try:
                port = i2c.get_port(addr)
                port.write([FtdiI2cRelayBoard.CMD_READ_FIRMWARE_VER])
                fw = port.read(1)
                if fw:
                    found.append(addr)
                    print(f"Found a relayboard at address {hex(addr)}")
            except Exception:
                continue
        i2c.close()
        return found

    @staticmethod
    def list_boards() -> list[str]:
        return [f"Type: 2 (FTDI I2C Relay Board), address: {hex(addr)}"
                for addr in FtdiI2cRelayBoard.scan_i2c_devices()]
