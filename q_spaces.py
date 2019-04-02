from enum import Enum

class MagThreeSpace(Enum):
    ZERO = 0
    PLUS = 1
    MAX = 2

class MagTwoSpace(Enum):
    ZERO = 0
    MAX = 1

class DerivativeSpace(Enum):
    NEG = -1
    ZERO = 0
    PLUS = 1

mag_q_space = {
    '2': MagTwoSpace,
    '3': MagThreeSpace
}
