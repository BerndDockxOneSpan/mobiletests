from __future__ import annotations

from .relayboard_base import RelayBoard, log

import serial
import serial.tools.list_ports
import time


class OneSpanRelayBoard(RelayBoard):
    """
    Implementation of the RelayBoard class for the internal OneSpan relay board
    """
    READ_TIMEOUT = 1.0
    BAUDRATE = 38400
    FIRMWARE_VERSION_IDENTIFIER = "CODE:"

    def __init__(self, port: str) -> None:
        self.port = port
        self.conn = serial.Serial(port,
                                  timeout=OneSpanRelayBoard.READ_TIMEOUT,
                                  baudrate=OneSpanRelayBoard.BAUDRATE)

    @property
    def relay_count(self) -> int:
        return 24

    def close(self) -> None:
        self.conn.close()

    def set_relay(self, relay: int, state: bool) -> None:
        state_str = 'A' if state else 'U'
        if not 0 <= relay <= self.relay_count:
            log.error(f"Cannot set relay {relay} to {state_str}, out of range "
                      f"of available relays [0, {self.relay_count}]")
        else:
            self.send(f'R{relay:02d}{state_str}')

    def get_firmware_version(self) -> str:
        return self.send('V')

    def send(self, command: str) -> str:
        message = f"${command}#".encode("ascii")
        eol = message + b"\r\n"
        self.conn.write(message)
        buf = b''
        end = time.time() + OneSpanRelayBoard.READ_TIMEOUT
        while not buf.endswith(eol):
            buf += self.conn.read()
            if time.time() > end:
                raise TimeoutError(f"Unexpected message returned from "
                                   f"connection: {buf!r}, expected {eol!r}")
        data = buf[:-len(eol)].decode("ascii")
        return data
    
    @staticmethod
    def _is_onespan_board(port: str) -> bool:
        """Check if a board on the given port is a OneSpan relay board."""
        board = None
        try:
            board = OneSpanRelayBoard(port)
            firmware_version = board.get_firmware_version()
            return (OneSpanRelayBoard.FIRMWARE_VERSION_IDENTIFIER in 
                    firmware_version)
        except (serial.SerialException, TimeoutError):
            return False
        finally:
            if board:
                board.close()

    @staticmethod
    def list_boards() -> list[str]:
        devices_info = []
        ports = [port.device for port in serial.tools.list_ports.comports()]
        for possible_port in ports:
            if OneSpanRelayBoard._is_onespan_board(possible_port):
                devices_info.append(f"Type: 0 (OneSpan Relay Board), "
                                     f"port: {possible_port}")
        return devices_info
    
    @staticmethod
    def create(port: str | int | None = None) -> OneSpanRelayBoard:
        # Get the list of available com ports
        com_ports_list = list(serial.tools.list_ports.comports())
        ports = [port.device for port in com_ports_list]

        # If no port is defined, try to find it by checking if the version
        # command returns what we expect
        if port is None:
            for possible_port in ports:
                if OneSpanRelayBoard._is_onespan_board(possible_port):
                    print(f"Detected board on {possible_port}")
                    return OneSpanRelayBoard(possible_port)
            raise ConnectionError("Could not find a board.")
        
        if port in ports:
            board = OneSpanRelayBoard(port)
        else:
            raise ConnectionError(f"No board found on port {port}")

        return board
