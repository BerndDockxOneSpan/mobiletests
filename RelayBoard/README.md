# RelayBoard

A Python package for controlling various types of relay boards through a unified interface.

## Overview

This package provides a simple, unified API for controlling different types of relay boards, including:

- **OneSpan Relay Board** (24 relays) - Internal OneSpan relay board via serial communication
- **D2XX Relay Board** (4 relays) - 4-relay board with D2XX chip via USB
- **FTDI I2C Relay Board** (4 relays) - I2C relay board using FTDI interface
- **Stub Relay Board** - Testing/simulation board

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

**Note**: Some dependencies are optional:
- `pyserial` - Required for OneSpan Relay Board support
- `ftd2xx` - Required for D2XX Relay Board support
- `pyftdi` - Required for FTDI I2C Relay Board support

## Quick Start

### Basic Usage

```python
from relayboard import create_board, BoardType

# Auto-detect and create a board
board = create_board()

# Or specify a board type
board = create_board(BoardType.ONESPAN)
board = create_board(BoardType.D2XX)
board = create_board(BoardType.FTDI)
board = create_board(BoardType.STUB)

# Use the board
with board:
    # Close relay 1 (activate)
    board.set_relay(1, True)
    
    # Open relay 1 (deactivate)
    board.set_relay(1, False)
    
    # Switch relay 2 for 500ms
    board.switch_relay(2, 500)
    
    # Get board information
    print(f"Board has {board.relay_count} relays")
    print(f"Firmware: {board.get_firmware_version()}")
```

### Board-Specific Parameters

```python
# OneSpan board with specific COM port
board = create_board(BoardType.ONESPAN, port="COM5")

# D2XX board with specific device index or serial number
board = create_board(BoardType.D2XX, port=0)  # Device index
board = create_board(BoardType.D2XX, port="FT1234")  # Serial number

# FTDI I2C board with custom I2C address
board = create_board(BoardType.FTDI, i2c_addr=0x12)
```

### Board Discovery

```python
from relayboard import OneSpanRelayBoard, UsbRelayBoard, FtdiI2cRelayBoard

# List available boards
if UsbRelayBoard:
    d2xx_boards = UsbRelayBoard.list_boards()
    for board_info in d2xx_boards:
        print(board_info)

onespan_boards = OneSpanRelayBoard.list_boards()
for board_info in onespan_boards:
    print(board_info)
```

## Command Line Interface

The package includes a command-line interface for direct board control:

```bash
# List available boards
python -m relayboard list

# Auto-detect board and close relay 1
python -m relayboard close 1

# Open relay 2 on OneSpan board
python -m relayboard -b 0 open 2

# Switch relay 3 for 1000ms on D2XX board
python -m relayboard -b 1 -p 0 switch 3 1000

# Use FTDI I2C board with custom address
python -m relayboard -b 2 --i2c-addr 0x12 close 1
```

### Command Line Options

- `-b, --board`: Board type (0=OneSpan, 1=D2XX, 2=FTDI I2C, 3=Stub)
- `-p, --port`: COM port (OneSpan) or device index (D2XX)
- `--i2c-addr`: I2C address for FTDI boards (e.g., 0x11)

### Available Commands

- `list`: List all available boards
- `close <relay>`: Close (activate) a relay
- `open <relay>`: Open (deactivate) a relay  
- `switch <relay> <time_ms>`: Switch relay for specified time in milliseconds

**Relay Numbering**: Relays are numbered starting from 1. Use 0 to control all relays.

## API Reference

### Main Functions

#### `create_board(board_type=None, port=None, i2c_addr=None)`

Creates and returns a relay board instance.

**Parameters:**
- `board_type`: Board type (BoardType enum, int, string, or None for auto-detect)
- `port`: Port/device identifier (varies by board type)
- `i2c_addr`: I2C address for FTDI boards (default: 0x11)

**Returns:** RelayBoard instance

### BoardType Enum

```python
class BoardType(Enum):
    ONESPAN = 0  # OneSpan relay board
    D2XX = 1     # D2XX relay board with USB connection
    FTDI = 2     # FTDI I2C relay board
    STUB = 3     # Stub board for testing
```

### RelayBoard Interface

All board implementations provide the same interface:

#### Properties
- `relay_count`: Number of relays on the board

#### Methods
- `set_relay(relay: int, state: bool)`: Set relay state (True=closed/active, False=open/inactive)
- `switch_relay(relay: int, time_ms: int = 200)`: Temporarily activate relay
- `get_firmware_version() -> str`: Get board firmware/version info
- `close()`: Close connection to board

#### Context Manager Support
```python
with create_board() as board:
    board.set_relay(1, True)
# Board automatically closed when exiting context
```

## Board-Specific Details

### OneSpan Relay Board
- **Relays**: 24
- **Connection**: Serial (COM port)
- **Baud Rate**: 38400
- **Auto-detection**: Checks for "CODE:" in firmware version

### D2XX Relay Board (USB)
- **Relays**: 4
- **Connection**: USB via FTDI D2XX driver
- **Library**: Requires `ftd2xx` package
- **Device Selection**: By index (0, 1, 2...) or serial number

### FTDI I2C Relay Board
- **Relays**: 4
- **Connection**: I2C via FTDI interface
- **Library**: Requires `pyftdi` package
- **Default Address**: 0x11
- **URL Format**: 'ftdi:///1'

### Stub Relay Board
- **Relays**: 24 (configurable)
- **Purpose**: Testing and simulation
- **Output**: Prints relay actions to console

## Error Handling

The package includes comprehensive error handling:

```python
try:
    board = create_board(BoardType.D2XX)
except ValueError as e:
    print(f"Board not supported: {e}")
except ConnectionError as e:
    print(f"Could not connect: {e}")
```

Common exceptions:
- `ValueError`: Invalid board type or unsupported board
- `ConnectionError`: Board not found or connection failed
- `ImportError`: Required library not installed

## Development

### Requirements
- Python 3.7+ (uses `from __future__ import annotations`)
- Optional: `ftd2xx`, `pyftdi`, `pyserial` depending on board types

### Code Structure
- `relayboard.py` - Main entry point and CLI
- `relayboard_base.py` - Abstract base class
- `relayboard_onespan.py` - OneSpan board implementation
- `relayboard_usb.py` - D2XX board implementation  
- `relayboard_ftdi_i2c.py` - FTDI I2C board implementation
- `relayboard_stub.py` - Stub board for testing
