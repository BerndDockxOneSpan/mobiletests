"""
Created on 11 mars 2024
shamelessly copied and adapted from kaizen framework
@author: verstla1
"""
from __future__ import annotations

from enum import Enum
from typing import Any

import argparse
import logging

from .relayboard_base import RelayBoard
from .relayboard_stub import StubRelayBoard
from .relayboard_onespan import OneSpanRelayBoard

# Optional import for USB relay board
try:
    from .relayboard_usb import UsbRelayBoard
except (ImportError, FileNotFoundError):
    # ftd2xx library not available, USB relay board will not be available
    UsbRelayBoard = None
    
# Optional import for pyftdi I2C relay board
try:
    from .relayboard_ftdi_i2c import FtdiI2cRelayBoard
except (ImportError, FileNotFoundError):
    # pyftdi library not available, FTDI I2C relay board will not be available
    FtdiI2cRelayBoard = None

log = logging.getLogger(__name__)

class BoardType(Enum):
    """
    Enumeration of the different types of relay boards.
    """
    ONESPAN = 0
    D2XX = 1
    FTDI = 2
    STUB = 3


# Constants for command line interface
BOARD_TYPE_CHOICES = [0, 1, 2, 3]


def create_board(board_type: BoardType | str | int | None = None,
                 port: str | int | None = None,
                 i2c_addr: int | None = None) -> RelayBoard:
    """
    Create a board depending on the board_type parameter,
    useful for creating a board based on a configuration parameters.

    Parameters
    ----------
    board_type : BoardType | str | int | None
        The type of the board you wish to create:
        0 | ONESPAN | "ONESPAN" : internal OneSpan relay board.
        1 | D2XX    | "D2XX"    : 4 relay relay board with D2XX chip.
        2 | FTDI    | "FTDI"    : FTDI I2C relay board.
        3 | STUB    | "STUB"    : Stub relay board for testing purposes.
        If this is set to None (the default), we will attempt to find the
        type.
    port : str | int | None
        For the OneSpan board: The COM port the board is on (for example
                               'COM5'), if none is set it will try to find
                               the correct port.
        For the D2XX board:    The index or serial number of the board,
                               defaults to 0.
    """

    # If no board_type is specified, try to create one for each defined type
    if board_type is None:
        possible_types = [BoardType.ONESPAN, BoardType.STUB]
        if UsbRelayBoard is not None:
            # Start with type D2XX since it is faster to check if connected
            possible_types.insert(0, BoardType.D2XX)

        for possible_type in possible_types:
            try:
                return create_board(possible_type, port, i2c_addr)
            except (ConnectionError, ValueError, ImportError):
                pass
        raise ConnectionError("Could not find a board.")

    match _parse_board_type(board_type):
        case BoardType.ONESPAN:
            return OneSpanRelayBoard.create(port)
        case BoardType.D2XX:
            if UsbRelayBoard is None:
                raise ValueError("USB relay board support not available "
                                 "(ftd2xx library not found)")
            return UsbRelayBoard.create(port)
        case BoardType.FTDI:
            if FtdiI2cRelayBoard is None:
                raise ValueError("FTDI I2C relay board support not available "
                                 "(pyftdi library not found)")
            return FtdiI2cRelayBoard.create(i2c_addr)
        case BoardType.STUB:
            return StubRelayBoard.create()
        case _:
            raise ValueError(f"Unknown board {board_type}")


def _parse_board_type(board_type: BoardType | str | int | None) -> BoardType:
    match board_type:
        case BoardType():
            return board_type
        case int() as i:
            try:
                return BoardType(i)
            except ValueError:
                pass
        case str() as s:
            try:
                return BoardType[s]
            except KeyError:
                try:
                    return BoardType(int(s))
                except (ValueError, KeyError):
                    pass
        case _:
            pass
    raise ValueError(f"Invalid BoardType: {board_type}")


# Command line interface functions
def _close_relay(board: RelayBoard, args: argparse.Namespace) -> None:
    """Close a relay on the board."""
    board.set_relay(args.relay, True)


def _open_relay(board: RelayBoard, args: argparse.Namespace) -> None:
    """Open a relay on the board."""
    board.set_relay(args.relay, False)


def _switch_relay(board: RelayBoard, args: argparse.Namespace) -> None:
    """Switch a relay for a specified time."""
    board.switch_relay(args.relay, args.time)


def _list_boards(args: argparse.Namespace) -> None:
    """List all available relay boards."""
    devices_info: list[str] = []

    # USB relay board
    if UsbRelayBoard is not None:
        devices_info.extend(UsbRelayBoard.list_boards())

    # OneSpan relay board
    devices_info.extend(OneSpanRelayBoard.list_boards())

    # FTDI I2C relay board
    if FtdiI2cRelayBoard is not None:
        devices_info.extend(FtdiI2cRelayBoard.list_boards())
    
    if len(devices_info) == 0:
        print("No relay boards found.")
    else:
        print(f"{len(devices_info)} relay board(s) found:")
        print('\n'.join(devices_info))


def _setup_argument_parser() -> argparse.ArgumentParser:
    """Set up and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Control relay boards from the command line."
    )

    # Global parameters used for all subcommands
    parser.add_argument(
        "-b", "--board", choices=BOARD_TYPE_CHOICES, type=int,
        help="The type of board: 0 for OneSpan board, 1 for 4x Relay USB "
             "Relay Board with D2XX chip, 2 for FTDI I2C Relay Board, or "
             "3 for Stub board. If not set, will auto-detect."
    )
    parser.add_argument(
        "-p", "--port",
        help='COM port of the OneSpan relay board, or board index for D2XX '
             'board. Not used for FTDI I2C relay board.'
    )
    parser.add_argument(
        "--i2c-addr", type=lambda x: int(x, 0), default=None,
        help="I2C address for FTDI I2C relay board (e.g., 0x11)."
    )

    subparsers = parser.add_subparsers(required=True, dest='command')
    relay_help = ("The index of the relay you want to control, starting at 1. "
                  "To control all relays set this to 0.")

    # Close relay subcommand
    close_parser = subparsers.add_parser("close", help="Close a relay")
    close_parser.add_argument("relay", type=int, help=relay_help)
    close_parser.set_defaults(func=_close_relay, requires_board=True)

    # Open relay subcommand
    open_parser = subparsers.add_parser("open", help="Open a relay")
    open_parser.add_argument("relay", type=int, help=relay_help)
    open_parser.set_defaults(func=_open_relay, requires_board=True)

    # Switch relay subcommand
    switch_parser = subparsers.add_parser(
        "switch", help="Close the relay for a defined period of time, "
                       "then close it again"
    )
    switch_parser.add_argument("relay", type=int, help=relay_help)
    switch_parser.add_argument("time", type=int, 
                               help="The time (in ms) to close the relay for.")
    switch_parser.set_defaults(func=_switch_relay, requires_board=True)

    # List board subcommand
    list_parser = subparsers.add_parser("list", 
                                        help="List the available boards")
    list_parser.set_defaults(func=_list_boards, requires_board=False)

    return parser


def main() -> None:
    """Main entry point for the command line interface."""
    parser = _setup_argument_parser()
    args = parser.parse_args()

    if not args.requires_board:
        args.func(args)
        return

    # Create the board
    try:
        board = create_board(args.board, args.port, args.i2c_addr)
    except (ConnectionError, ValueError) as e:
        parser.error(f"Failed to create board: {e}")

    try:
        # Validate relay number if present
        if hasattr(args, 'relay') and args.relay > board.relay_count:
            parser.error(f"This board only has {board.relay_count} relays!")
        
        args.func(board, args)
    finally:
        # Always close the connection to the board
        board.close()


# Command line code
if __name__ == "__main__":
    main()
