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
    def plausible_der(self):
        # all the possible derivative in such quantity
        if mag==mag.q_space:
            pass

if __name__ == "__main__":
    q = Quantity("Test", MagThree, MagThree.ZERO)
    print(q)