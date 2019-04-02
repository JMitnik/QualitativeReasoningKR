from dataclasses import dataclass
from enum import Enum, EnumMeta
from q_spaces import DerivativeSpace

@dataclass
class Derivative:
    space: EnumMeta = DerivativeSpace
    val: Enum = DerivativeSpace.ZERO