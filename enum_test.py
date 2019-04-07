from enum import IntEnum

class Pressure(IntEnum):
    ZERO = 1
    PLUS = 2
    MAX = 3

if __name__ == "__main__":
    p_zero = Pressure.ZERO
    p_zero_2 = Pressure.ZERO
    p_plus = Pressure.PLUS
    print(p_plus)