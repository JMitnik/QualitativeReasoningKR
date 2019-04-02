from dataclasses import dataclass
from enum import Enum, EnumMeta

@dataclass
class Magnitude:
    q_space: EnumMeta
    val: Enum