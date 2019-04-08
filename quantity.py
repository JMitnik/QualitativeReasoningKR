from dataclasses import dataclass, field
from entity_tuple import EntityTuple

from enum import Enum, EnumMeta
from magnitude import Magnitude
from derivative import Derivative
from q_spaces import DerivativeSpace, MagThreeSpace, MagTwoSpace

@dataclass
class Quantity:
    name: str
    mag: Magnitude
    der: Derivative

    def set_from_tuple(self, entity_tuple: EntityTuple):
        self.mag.val = entity_tuple.mag
        self.der.val = entity_tuple.der

    def to_tuple(self):
        return EntityTuple(self.mag.val, self.der.val)

    def plausible_der(self):
        # all the possible derivative in such quantity
        if mag==mag.q_space:
            pass

if __name__ == "__main__":
    print(q)