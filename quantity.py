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

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        return '{}:{} {}'.format(self.name, self.mag.val, self.der.val)

    def set_from_tuple(self, entity_tuple: EntityTuple):
        self.mag.val = entity_tuple[0]
        self.der.val = entity_tuple[1]

    @staticmethod
    def create_from_tuple(entity_tuple: EntityTuple):
        der = Derivative()
        mag = Magnitude(mag_q_space[entity_tuple.mag_q_space])
        tmp = Quantity(entity_tuple.title, mag, der)
        tmp.set_from_tuple(entity_tuple)
        return tmp

    def to_tuple(self):
        return tuple((self.mag.val, self.der.val))

    def constrain_extreme_derivatives(self):
        if self.der.val not in self.valid_derivatives():
            self.der.val = DerivativeSpace.ZERO

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
        # print(nr_effects)
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

    def set_der_v2(self, der):
        new_q = lambda d:Quantity(self.name, deepcopy(self.mag), deepcopy(self.der).set_to(d))
        if isinstance(der, list):
            return [new_q(d) for d in der]
        return new_q(der)

    def apply_relations_v2(self, relations, state):
        end_states = []
        rels = {rel.rel_type:rel for rel in relations}
        d_influence = []
        q_influence = None
        for rel_n in rels:
            rel = rels[rel_n]
            if rel_n == 'I+':
                influ = state[rel.fr].quantity.mag.effect() * 1
                d_influence.append(influ)
            if rel_n == 'I-':
                influ = state[rel.fr].quantity.mag.effect() * -1
                d_influence.append(influ)
            if rel_n == 'P+':
                influ = state[rel.fr].quantity.der.val * 1
                q_influence = influ
            if rel_n == 'P-':
                influ = state[rel.fr].quantity.der.val * -1
                q_influence = influ
        prune_val = lambda x: [i+self.der.val for i in x if ((self.der.val+i) in 
                        self.valid_derivatives())]
        # print([int(i) for i in self.valid_derivatives()])
        # print([int(i) for i in self.valid_derivatives()])
        # print(d_influence)
        # print(prune_val([-1, 0, 1]), '\n',
            #   self.valid_derivatives(), '\n', self.der.val, '\n', (self.der.val+1))
        if -1 in d_influence and 1 in d_influence:
            return self.set_der_v2(prune_val([-1, 0, 1]))
        elif -1 in d_influence:
            return self.set_der_v2(prune_val([-1,0]))
        elif 1 in d_influence:
            return self.set_der_v2(prune_val([1,0]))
        elif 0 in d_influence:
            return self.set_der_v2(prune_val([0]))
        if not (q_influence is None):
            return self.set_der_v2(([q_influence, ]))
        # print(relations, state)
        # print(self.mag.val)
        return self.set_der_v2([self.der.val,])
        # raise ValueError()

    def apply_relations(self, relations, entities):
        end_states = []

        # TODO: Refactor this code.
        for relation in relations:
            relation_states = []
            related_entity = [entity for entity in entities if entity.name == relation.fr][0]
            relation_type = relation.rel_type

            # If the relation type is P proportional and the derivative is actual not zero of our related entity.
            if relation_type == "P+" and related_entity.quantity.der.val != related_entity.quantity.der.space.ZERO:
                
                # If not growing, or if they are equal, then the derivative of the related entity is just taken
                if self.der.val == Derivative.space.ZERO or self.der.val == related_entity.quantity.der.val:
                    end_states.append(EntityTuple(self.mag.val, related_entity.quantity.der.val))
                    continue

                # If we arrive at this state, then that means we will have an ambiguity! Generate the current state,
                # and the state in case the related entity will win!
                end_states.append(EntityTuple(self.mag.val, related_entity.quantity.der.val))
                end_states.append(EntityTuple(self.mag.val, Derivative.space(related_entity.quantity.der.val + self.der.val)))
            
            if relation_type == "P-" and related_entity.quantity.der.val != related_entity.quantity.der.space.ZERO:
                # If not growing or if they are equal, take the derivative.
                if self.der.val == Derivative.space.ZERO or self.der.val == related_entity.quantity.der.val:
                    end_states.append(EntityTuple(self.mag.val, related_entity.quantity.der.val))
                    continue

                # If we arrive at this state, then that means we will have an ambiguity! Generate the current state,
                # and the state in case the related entity will win!
                end_states.append(EntityTuple(self.mag.val, related_entity.quantity.der.val))
                end_states.append(EntityTuple(self.mag.val, Derivative.space(related_entity.quantity.der.val - self.der.val)))
            
            if relation_type == "I+" and related_entity.quantity.mag.val != related_entity.quantity.mag.q_space.ZERO:
                # If not growing, then a positive influence of a present entity will cause this to grow.
                if self.der.val == Derivative.space.ZERO:
                    end_states.append(EntityTuple(self.mag.val, Derivative.space.PLUS))
                    continue

                # If we are dealing with a positive derivative, then the positive influence will just keep the growth alive.
                # WARNING: We assume magnitude never reaches negative here
                if self.der.val == Derivative.space.PLUS:
                    end_states.append(EntityTuple(self.mag.val, self.der.val))
                    continue
                
                # We are thus at the ambiguity (negative). Let's add in case the influence doesn't win (current derivative),
                # our ambiguity and the increase might be zero. 
                end_states.append(EntityTuple(self.mag.val, self.der.val))
                end_states.append(EntityTuple(self.mag.val, Derivative.space.ZERO))

            if relation_type == "I-" and related_entity.quantity.mag.val != related_entity.quantity.mag.q_space.ZERO:
                
                if self.der.val == Derivative.space.ZERO:
                    end_states.append(EntityTuple(self.mag.val, Derivative.space.NEG))
                    continue

                # If we are dealing with a positive derivative
                # WARNING: We assume magnitude never reaches negative here
                if self.der.val == Derivative.space.NEG:
                    end_states.append(EntityTuple(self.mag.val, self.der.val))
                    continue
                
                # We are thus at positive
                end_states.append(EntityTuple(self.mag.val, self.der.val))
                end_states.append(EntityTuple(self.mag.val, Derivative.space.ZERO))

        return end_states


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
        return self.mag.val == self.mag.q_space.ZERO or (self.mag.q_space ==MagThreeSpace and self.mag.val == self.mag.q_space.MAX )

    def set_derivative(self, der):
        self.der.set_to(der)
        return


if __name__ == "__main__":
    q = Quantity("Test", Magnitude(MagTwoSpace, 1), Derivative(val=0))
    from relation import Relation
    from state import State
    rel = Relation('I+', 'a', 'b')
    rel = Relation('I-', 'a', 'b')
    
    q.apply_relations_v2()
    print(q.valid_derivatives())
    print(q.generate_effects(0))
    s = {q:1}


