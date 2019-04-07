from dataclasses import dataclass
from enum import Enum, EnumMeta

<<<<<<< HEAD
@dataclass
class Magnitude:
    q_space: EnumMeta
    val: Enum
=======

class MagThree(Enum):
    ZERO = 1
    PLUS = 2
    MAX = 3

class MagTwo(Enum):
    ZERO = 1
    MAX = 2

class DThree(Enum):
    MINUS = -1
    ZERO = 0
    PLUS = 1
>>>>>>> example for pyviz
