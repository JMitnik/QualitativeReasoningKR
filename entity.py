from dataclasses import dataclass, field

from entity_tuple import EntityTuple
import utils
from derivative import Derivative, DerivativeSpace
from magnitude import Magnitude
from quantity import Quantity

@dataclass
class Entity:
    name: str
    quantity: Quantity

    def load_from_tuple(self, entity_tuple: EntityTuple):
        '''Given an entity_tuple state, set the values of the entity's quantity
        '''
        
        self.quantity.set_from_tuple(entity_tuple)

    def generate_effects(self):
        self.quantity.generate_effects()
    
    def to_tuple(self):
        return self.quantity.to_tuple()

if __name__ == "__main__":
    pass
