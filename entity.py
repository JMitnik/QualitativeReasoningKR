from dataclasses import dataclass

# from collections import namedtuple
import utils
from derivative import Derivative, DerivativeSpace
from magnitude import Magnitude
from quantity import Quantity


@dataclass
class Entity:
    name: str
    quantity: Quantity

    @staticmethod
    def create_from_tuple(name, tup):
        tmp = Entity(name, None)
        tmp.from_tuple(tup)
        return 
    
    def from_tuple(self, tup):
        # TODO: Convert tuple to hashable object
        dict_spec = utils.tuple2dict(tup)
        print(dict_spec)
        d = Derivative(DerivativeSpace, DerivativeSpace(dict_spec['d_value']))
        mag_space = mag_q_space[dict_spec['mag_q_space']]
        mag = Magnitude(mag_space, mag_space(dict_spec['mag_value']))
        # Todo: for completeness, maybe we should just set the spec to have a list of quantities within an entity (even-though we only have one quantity per entity)
        self.quantity = Quantity(dict_spec['title'], mag, d)
        # entities.append(Entity(tup['title'], self.quantity))
    
    def to_tuple(self):
        # TODO: Convert to tuple
        pass

if __name__ == "__main__":
    # test_set = set()
    # test_set.add([3, 4, 5])
    # test_set.add([3, 4, 5, 6])
    # test_set.add([3, 4, 5])
    # print(test_set)
    pass
