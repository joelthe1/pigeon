'''
A dataclass to hold queue items
'''
from dataclasses import dataclass

import typing

@dataclass
class Qitem:
    message: typing.Any
    passthrough: bool = False
    attempts: int = 0
