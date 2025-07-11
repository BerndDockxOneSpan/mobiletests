"""
RelayBoard package for controlling various types of relay boards.

This package provides a unified interface for controlling different types of relay boards,
including OneSpan relay boards and stub boards for testing.
"""

from .relayboard import BoardType, create_board
from .relayboard_base import RelayBoard
from .relayboard_onespan import OneSpanRelayBoard
from .relayboard_stub import StubRelayBoard

# Optional imports that may not be available
try:
    from .relayboard_usb import UsbRelayBoard
except Exception:
    # ftd2xx library not available, USB relay board will not be available
    UsbRelayBoard = None
try:
    from .relayboard_ftdi_i2c import FtdiI2cRelayBoard
except Exception:
    # pyftdi library not available, FTDI I2C relay board will not be available
    FtdiI2cRelayBoard = None

__all__ = [
    'create_board',
    'RelayBoard',
    'BoardType', 
    'OneSpanRelayBoard',
    'StubRelayBoard'
]

# Add UsbRelayBoard to __all__ only if it was successfully imported
if UsbRelayBoard is not None:
    __all__.append('UsbRelayBoard')
if FtdiI2cRelayBoard is not None:
    __all__.append('FtdiI2cRelayBoard')