from dataclasses import dataclass, field
from entity_tuple import EntityTuple

from enum import Enum, EnumMeta
from magnitude import Magnitude
from derivative import Derivative
from q_spaces import DerivativeSpace, MagThreeSpace, MagTwoSpace

@dataclass
class Quantity:
    name: str
    mag: Magnitude
    der: Derivative

    def set_from_tuple(self, entity_tuple: EntityTuple):
        self.mag.val = entity_tuple.mag
        self.der.val = entity_tuple.der

    def to_tuple(self):
        return EntityTuple(self.mag.val, self.der.val)

    def generate_effects(self, derivative=None):
        if not derivative:
            derivative = self.der
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

        if derivative not in self.valid_derivatives():
            derivative = self.der.space(0)
        
        

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




if __name__ == "__main__":
    q = Quantity("Test", Magnitude(MagThreeSpace, 2), MagThreeSpace.ZERO)
    print(q.plausible_der())

