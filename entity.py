from dataclasses import dataclass, field

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

    def generate_effects(self):
        self.quantity.generate_effects()
    
    def to_tuple(self):
        return self.quantity.to_tuple()

    @staticmethod
    def create_from_tuple(name, tup):
        tmp = Entity(name, None)
        tmp.load_from_tuple(tup)
        return tmp
    
    def __repr__(self):
        res = '{}:{} {}'
        if self.quantity is not None:
            res = res.format(self.name, self.quantity.mag, self.quantity.der)
            return res
        else:
            return self.name
    def __str__(self):
        return self.__repr__()

    def set_der(self, der_val):
        self.quantity.set_der(der_val)

    def apply_der(self):
        res_li = []
        for der in self.quantity.plausible_der:
            tmp_ent = deepcopy(self)
            tmp_ent.quantity.apply_der(der)
            res_li.append(tmp_ent)
            

if __name__ == "__main__":
    dict_ = {'d_value':1, 'mag_q_space':'2', 'mag_value':1, 'title':'jona'}
    s = Entity.create_from_tuple('jona', dict_)
    print(s.to_tuple())
    s.set_der(1)
