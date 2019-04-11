from dataclasses import dataclass, field
from copy import deepcopy

from entity_tuple import EntityTuple
import utils
from derivative import Derivative, DerivativeSpace
from magnitude import Magnitude
from quantity import Quantity
from q_spaces import mag_q_space

@dataclass
class Entity:
    name: str
    quantity: Quantity

    def load_from_tuple(self, entity_tuple: EntityTuple):
        '''Given an entity_tuple state, set the values of the entity's quantity
        '''
        
        self.quantity.set_from_tuple(entity_tuple)
    def __hash__(self):
        return self.quantity.__hash__()
        
    def generate_effects(self):
        return self.quantity.generate_effects()
    
    def to_tuple(self):
        return self.quantity.to_tuple()

    @staticmethod
    def create_from_tuple(name, tup):
        tmp = Entity(name, Quantity.create_from_tuple(tup))
        return tmp
    
    def __repr__(self):
        res = r'{}:{} {}'
        if self.quantity is not None:
            res = res.format(self.name, self.quantity.mag.val, self.quantity.der.val)
            return res
        else:
            return self.name
    def __str__(self):
        return self.__repr__()

    def set_der(self, der_val):
        self.quantity.set_derivative(der_val)

    def apply_der(self):
        res_li = []
        for der in self.quantity.valid_derivatives():
            # tmp_ent = deepcopy(self)
            # print(self.quantity.valid_derivatives())
            qs = self.quantity.generate_effects(der)
            for q in qs:
                res_li.append(Entity(self.name, q))
            # res_li.append(tmp_ent)
        return list(set(res_li))

if __name__ == "__main__":
    dict_ = {'der':1, 'mag_q_space':'2', 'mag':1, 'title':'jona'}
    tup = EntityTuple(**dict_)
    s = Entity.create_from_tuple('jona', tup)
    print(s.to_tuple())
    s.set_der(-1)
    print(s.apply_der())
