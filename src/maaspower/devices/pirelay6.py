"""
pirelay6.py
------------

Classes to represent the configuration and functionality for devices
that can be controlled via a PiRelay 6 https://learn.sb-components.co.uk/PiRelay-6.
"""
from dataclasses import dataclass

from typing_extensions import Annotated as A
from typing_extensions import Literal

from maaspower.maas_globals import desc
from maaspower.maasconfig import SwitchDevice

import RPi.GPIO as GPIO


GPIO.setwarnings(False)

pi_relaypins = [29, 31, 33, 35, 37, 40]
cm4_relaypins = [5, 6, 13, 19, 26, 21]
    

@dataclass(kw_only=True)
class PiRelay6(SwitchDevice):
    """A device controlled via a PiRelay 6"""

    cm4: A[bool, desc("Running on a CM4 device")] = False
    relay_index: A[int, desc("Index of the relay")] = 0

    type: Literal["PiRelay6"] = "PiRelay6"

    def __post_init__(self):
        if self.cm4:    
            GPIO.setmode(GPIO.BCM)
            self.pin = cm4_relaypins[self.relay_index]
        else:
            GPIO.setmode(GPIO.BOARD)
            self.pin = pi_relaypins[self.relay_index]

        GPIO.setup(self.pin,GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def turn_on(self):
        print(f"{self.relay_index} - ON")
        GPIO.output(self.pin,GPIO.HIGH)

    def turn_off(self):
        print(f"{self.relay_index} - OFF")
        GPIO.output(self.pin,GPIO.LOW)
    
    def query_state(self) -> str:
        if GPIO.input(self.pin) == 0:
            return 'off'
        else:
            return 'on'
