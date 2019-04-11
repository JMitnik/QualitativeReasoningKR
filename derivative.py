from dataclasses import dataclass
from enum import Enum, EnumMeta
from q_spaces import DerivativeSpace

@dataclass
class Derivative:
    space: EnumMeta = DerivativeSpace
    val: Enum = DerivativeSpace.ZERO
    
    def set_to(self, num):
        enum_map = {0: DerivativeSpace.ZERO,
                    1: DerivativeSpace.PLUS, -1: DerivativeSpace.NEG}
        self.val = enum_map[num]
<<<<<<< HEAD

    def __hash__(self):
        return hash(str(self.val)+str(self.space))

=======
>>>>>>> c1ce6fabeed956fcd7280b6fe8f8bcab93d56867
if __name__ == "__main__":
    Derivative().set_to(1)
