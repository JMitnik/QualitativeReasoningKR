from dataclasses import dataclass
from enum import Enum, EnumMeta

@dataclass
class Magnitude:
    q_space: EnumMeta
    val: Enum=0
    def __hash__(self):
        return hash(str(self.val)+str(self.q_space))