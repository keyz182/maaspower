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

import gpiod
from gpiod.line import Direction, Value


line_values = {
    5: Value.INACTIVE, 
    6: Value.INACTIVE, 
    13: Value.INACTIVE, 
    19: Value.INACTIVE, 
    26: Value.INACTIVE, 
    21: Value.INACTIVE,
}

request = gpiod.request_lines(
    '/dev/gpiochip4',
    consumer="maaspower",
    config={
        tuple(line_values.keys()): gpiod.LineSettings(direction=Direction.OUTPUT)
    },
    output_values=line_values,
)

relay_map = {
    0:5,
    1:6,
    2:13,
    3:19,
    4:26,
    5:21
}


@dataclass(kw_only=True)
class PiRelay6(SwitchDevice):
    """A device controlled via a PiRelay 6"""
    relay_index: A[int, desc("Index of the relay")] = 0
    type: Literal["PiRelay6"] = "PiRelay6"

    def __post_init__(self):
        self.relay = relay_map[self.relay_index]
    
    def update_line(self, value):
        line_values[self.relay] = value
        request.set_values(line_values)

    def turn_on(self):
        print(f"{self.relay_index} - ON")
        self.update_line(Value.ACTIVE)

    def turn_off(self):
        print(f"{self.relay_index} - OFF")
        self.update_line(Value.INACTIVE)
    
    def query_state(self) -> str:
        if line_values[self.relay] == Value.INACTIVE:
            return 'off'
        else:
            return 'on'
