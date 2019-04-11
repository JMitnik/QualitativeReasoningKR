from enum import Enum, IntEnum

class MagThreeSpace(IntEnum):
    ZERO = 0
    PLUS = 1
    MAX = 2

class MagTwoSpace(IntEnum):
    ZERO = 0
    PLUS = 1

class DerivativeSpace(IntEnum):
    NEG = -1
    ZERO = 0
    PLUS = 1

mag_q_space = {
    '2': MagTwoSpace,
    '3': MagThreeSpace
}
