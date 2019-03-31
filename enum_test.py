from enum import Enum

class Pressure(Enum):
    ZERO = 1
    PLUS = 2
    MAX = 3

if __name__ == "__main__":
    p = Pressure.ZERO