from entity_tuple import EntityTuple
from entity import Entity
from quantity import Quantity
from relation import Relation
from q_spaces import DerivativeSpace, mag_q_space
from derivative import Derivative
from magnitude import Magnitude
<<<<<<< HEAD
from itertools import product

=======
from copy import deepcopy
>>>>>>> finish entity&quantity, small bug fix

class CausalGraph:
    def __init__(self, entities: list, relations: list):
        '''Initialize a causal-graph.

        Arguments:
            entities
            relations {[type]} -- [description]
        '''
        self.entities = entities
        self.relations = relations
<<<<<<< HEAD
        self.incoming_relation_map = {rel.to: rel for rel in relations}
=======
        self.entities_map = {ent.name:ent for ent in entities}
        self.incoming_relation_map = {rel.to: rel for rel in relations }
>>>>>>> finish entity&quantity, small bug fix

    def _to_states(self, states):
        result = []

        for entities_state in states:
            result.append(self._to_state(entities_state))

        return set(result)  # Unique values only

    def _to_state(self, entities_state):
        s = []

        for ent in entities_state:
            s.append(ent.to_tuple())

        return tuple(s)

    @property
    def state(self):
        return self._to_state(self.entities)

    def _load_state(self, state):
        # The index of each namedtuple in the state corresponds to the entity in
        # self.entities.

        # Go over each entity, and set their value
        for index, entity in enumerate(state):
            self.entities[index].load_from_tuple(entity)

    def _apply_relations_to_entities(self, entities):
        # 1. Go through all the entities, and check all to's.
        result = []

        for entity in entities:
            incoming_relations = self.incoming_relation_map[entity]

            # We have a conflict if:
            # 1. Two relations fight over one entity. Three possible resulting states for this entity:
            # a) Either the first loses
            # b) Either the second loses
            # c) They are equally strong.
            # 2. A relation fights with the flow of the entity itself.

            # Possible idea: let the entity deal with the incoming relations,
            # and return the possible values it can assume.

            # With the possible values of the entities (list of varying entity
            # values), we can generate a complete state based purely off of
            # this. Grab all entities except for this one, and turn it into a state
            # using _to_states(). Add that to result.

        return result

    def _apply_derivative_to_entities(self, entities):
        # For each entity, apply the current derivative in its current state.

        # If we are on landmark, return two states.
        entity_effects = []

        # TODO: Ensure we only execute the non-exo variables
        for entity in entities:
            # Generate all possible effects
            entity_effects.append(entity.generate_effects())

        test_product = list(product(*entity_effects))

        return entity_effects

    def discover_states(self, state: tuple):
        '''Discover new states from the given state
        '''
        self._load_state(state)
        generated_states = []

        # For all entities:
        # 1. Apply all derivatives.
        self._apply_derivative_to_entities(self.entities)

        # 2. Apply all relations.
        # PIN: We want to apply the relations

        # 3. Apply a union.
        # MAYBE SWAP
        # 4. Ensure all are consistent.

    def propagate(self, state: tuple):
        all_possible_states = []
<<<<<<< HEAD
        def new_entities(): return deepcopy(self.entities)
=======
        new_entities = lambda : deepcopy(self.entities_map)
>>>>>>> finish entity&quantity, small bug fix
        # 1. check the ambiguity of exogenous variable

        # TODO Make this a consistent Enum

        exo_var_n = 'inflow'
        exo_var = self.entities_map[exo_var_n]
        # TODO: Make valid_derivatives method
        for valid_der in exo_var.quantity.valid_derivatives():
            new_s = new_entities()
            new_exo_var = new_s[exo_var_n]

            # TODO: Make set_derivative method
            new_exo_var.quantity.set_derivative(valid_der)
            all_possible_states.append(new_s)

        # 2. check the ambiguity of derivative applying
        state_li_after_applying = []

        for entity_n in self.entities_map:
            entity = self.entities_map[entity_n]
            ent_li = entity.apply_der()
            state_li_after_applying.append(ent_li)
            # if entity.derivative!=0:
            #     if entity.quantity==0:
            #         new_s = new_entities()
            #         new_s[entity_n].apply_der()
        new_entities += list(product(state_li_after_applying))

        # TODO: Create another loop which checks for exogenous states within possible ambigutiies (other than stable)

        # 3. check the ambiguity of relations
        for entity_n in self.relation_map:
            rels = self.relation_map[entity_n]
            rels_n = {r.ty: r for r in rels}
            q_influence = []
            d_influence = []

            # {from: q1, to: q2, type: vc} , {}
            for rel_n in rels_n:
                rel = rels[rel_n]
                if rel_n == 'I+':
                    influ = self.entities[rel.fr].quantity.val * 1
                    d_influence.append(influ)
                if rel_n == 'I-':
                    influ = self.entities[rel.fr].quantity.val * -1
                    d_influence.append(influ)
                if rel_n == 'P+':
                    influ = self.entities[rel.fr].quantity.val * 1
                    q_influence.append(influ)
                if rel_n == 'P-':
                    influ = self.entities[rel.fr].quantity.val * -1
                    q_influence.append(influ)
                if rel_n == 'VC':
                    # TODO: Use entitiy instead of entity_n
                    # TODO: Check if the 'from' enttity has reached the VC value as well
                    self.entities[rel.to].quantity.val = self.entities[rel.fr].quantity.val
                    break

            # If q and d influence have conflicts, generate new states and append
<<<<<<< HEAD


=======
        return self._to_states(new_entities)
>>>>>>> finish entity&quantity, small bug fix
if __name__ == "__main__":
    pass
