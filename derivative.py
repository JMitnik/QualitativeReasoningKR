from dataclasses import dataclass
from enum import Enum

class DerivativeQSpace(Enum):
    MIN = -1
    ZERO = 0
    POS = 1

@dataclass
class Derivative:
    space: EnumMeta = DerivativeQSpace
    name: str = ''
    init_val: DerivativeQSpace = DerivativeQSpace.ZERO

if __name__ == "__main__":
    test = Derivative()
    test.init_val