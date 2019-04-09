from dataclasses import dataclass, field
from entity_tuple import EntityTuple
from copy import deepcopy

from enum import Enum, EnumMeta
from magnitude import Magnitude
from derivative import Derivative
from q_spaces import DerivativeSpace, MagThreeSpace, MagTwoSpace, mag_q_space

@dataclass
class Quantity:
    name: str
    mag: Magnitude
    der: Derivative

    def set_from_tuple(self, entity_tuple: EntityTuple):
        self.mag.val = entity_tuple.mag
        self.der.val = entity_tuple.der

    @staticmethod
    def create_from_tuple(entity_tuple: EntityTuple):
        der = Derivative()
        mag = Magnitude(mag_q_space[entity_tuple.mag_q_space])
        tmp = Quantity(entity_tuple.title, mag, der)
        tmp.set_from_tuple(entity_tuple)
        return tmp

    def to_tuple(self):
        return EntityTuple(self.mag.val, self.der.val, self.mag.q_space, self.name)

    def generate_effects(self, derivative=None):
        if not derivative:
            derivative = self.der.val
        else:
            derivative = int(derivative)
        # Checks:
        #  1. Ensure that if we are at landmark, we would generate at most one
        #       state.

        #   WARNING: This might be a flawed assumption.
        #   2. Ensure that our derivative fits in the possible derivatives,
        #       otherwise, the next state will be the same magnitude but no more 
        #       derivative (?).

        # WARNING: Possibly we missed something.
        # 3. If we are here, then that means we will generate two states with
        #    the current derivative
        
        nr_effects = 2

        if self.is_at_landmark():
            nr_effects = 1
        if derivative == 0:
            nr_effects = 1
        if derivative not in [int(i) for i in self.valid_derivatives()]:
            derivative = self.der.space(0)
        print(nr_effects)
        q_applied = deepcopy(self)
        q_applied.mag.val+=derivative
        if nr_effects==1:
            results = [q_applied,]
        elif nr_effects==2:
            results = [q_applied, deepcopy(self)]
        else:
            raise ValueError()
        return [Quantity._validify(q) for q in results]
        
    @staticmethod
    def _validify(q):
        # clip the derivative to zero after transform to a landmark
        if q.is_at_landmark():
            q.der.set_to(0)
        return q

    def valid_derivatives(self):
        valid_derivatives = []

        for derivative in self.der.space:
            try:
                self.mag.q_space(self.mag.val + derivative)
                # If it crashes, then it's not possible
                valid_derivatives.append(derivative)
            except:
                continue

        return valid_derivatives

    def is_at_landmark(self):
        # If magnitude is at landmark, we will want to generate only one
        # possible effect. Else, we generate two possible effect: the current
        # effect, and the effect if the interval has been broken.
        
        # We are at landmark if we are at ZERO or MAX, basically. We can
        # hard-code that, more or less.

        # WARNING: This assumes that all Magnitude Q Spaces have zero and Max,
        # and that these are the extremes.
        return self.mag.val == self.mag.q_space.ZERO or self.mag.val == self.mag.q_space.MAX 

    def set_derivative(self, der):
        self.der.set_to(der)
        return


if __name__ == "__main__":
    q = Quantity("Test", Magnitude(MagThreeSpace, 1), Derivative(val=0))
    print(q.valid_derivatives())
    print(q.generate_effects(0))

