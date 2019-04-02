from dataclasses import dataclass

from enum import Enum, EnumMeta
from magnitude import Magnitude
from derivative import Derivative
from q_spaces import DerivativeSpace, MagThreeSpace, MagTwoSpace

@dataclass
class Quantity:
    name: str
    mag: Magnitude
    der: Derivative

if __name__ == "__main__":
    q = Quantity("Test", MagThree, MagThree.ZERO)
    print(q)