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

    def create_new_from_tuple(self, entity_tuple: EntityTuple):
        quantity = Quantity(self.name, Magnitude(self.quantity.mag.q_space, entity_tuple.mag), Derivative(DerivativeSpace ,entity_tuple.der))
        return Entity(self.name, quantity)

    def constrain_extreme_derivatives(self):
        self.quantity.constrain_extreme_derivatives()

    def generate_effects(self):
        return self.quantity.generate_effects()

    def apply_relations(self, relations, entities):
        return self.quantity.apply_relations(relations, entities)
    
    def to_tuple(self):
        return self.quantity.to_tuple()

if __name__ == "__main__":
    pass
