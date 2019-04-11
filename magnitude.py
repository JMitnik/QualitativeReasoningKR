from dataclasses import dataclass
from enum import Enum, EnumMeta

@dataclass
class Magnitude:
    q_space: EnumMeta
    val: Enum=0
<<<<<<< HEAD
    def __hash__(self):
        return hash(str(self.val)+str(self.q_space))
=======
>>>>>>> c1ce6fabeed956fcd7280b6fe8f8bcab93d56867
