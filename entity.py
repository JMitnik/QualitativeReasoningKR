from collections.abc import MutableSet
from dataclasses import dataclass
from quantity import Quantity
@dataclass
class Entity:
    name: str
    quantity: Quantity

    def from_tuple(self, tuple):
        # TODO: Convert tuple to hashable object
        pass
    
    def to_tuple(self):
        # TODO: Convert to tuple
        pass

if __name__ == "__main__":
    test_set = MutableSet()
    test_set.add([3, 4, 5])
    test_set.add([3, 4, 5, 6])
    test_set.add([3, 4, 5])
    print(test_set)