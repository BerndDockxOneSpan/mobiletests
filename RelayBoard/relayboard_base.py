"""
Created on 11 mars 2024
shamelessly copied and adapted from kaizen framework
@author: verstla1
"""

from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod


log = logging.getLogger(__name__)


class RelayBoard(ABC):
    """
    An abstract class for a relayboard so you can control multiple types of
    relayboards in the same manner
    """
    ACTIVATE = True
    DEACTIVATE = False

    def __enter__(self) -> RelayBoard:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.close()
        return False  # Propagate exceptions if any

    @property
    @abstractmethod
    def relay_count(self) -> int:
        """
        Abstract property to get the amount of relays on the relay board
        """

    @abstractmethod
    def close(self) -> None:
        """
        Abstract function to close the connection to a relay board
        """

    @abstractmethod
    def set_relay(self, relay: int, state: bool) -> None:
        """
        Abstract function to enable set the state of a relay

        Parameters
        ----------
        relay : int
            The index of the relay you want to control, starting at 1
            0 will set all relays on the board to the desired state
        state : bool
            The state you wish to set the relay to
        """

    @abstractmethod
    def get_firmware_version(self) -> str:
        """
        Abstract function to get the firmware version of the relay board
        """

    def switch_relay(self, relay: int, time_ms: int = 200) -> None:
        """
        Enable a relay for a specified period of time then disable it again

        Parameters
        ----------
        relay : int
            The index of the relay you want to control, starting at 1
            0 will control all relays
        time_ms : int
            How long (in ms) the relay should stay on
        """
        self.set_relay(relay, self.ACTIVATE)
        time.sleep(float(time_ms) / 1000)
        self.set_relay(relay, self.DEACTIVATE)
