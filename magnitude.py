from dataclasses import dataclass
from enum import Enum, EnumMeta
from q_spaces import MagThreeSpace, MagTwoSpace

@dataclass
class Magnitude:
    q_space: EnumMeta
    val: Enum=0

    def effect(self):
        if self.q_space is MagThreeSpace:
            return self.val-1
        elif self.q_space is MagTwoSpace:
            return self.val*2-1

    def __hash__(self):
        return hash(str(self.val)+str(self.q_space))
