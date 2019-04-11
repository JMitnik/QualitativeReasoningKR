from entity_tuple import EntityTuple
from entity import Entity
from quantity import Quantity
from relation import Relation
from q_spaces import DerivativeSpace, mag_q_space
from derivative import Derivative
from magnitude import Magnitude
from itertools import product
from collections import defaultdict

class CausalGraph:
    def __init__(self, entities: list, relations: list):
        '''Initialize a causal-graph.

        Arguments:
            entities
            relations {[type]} -- [description]
        '''
        self.entities = entities
        self.relations = relations
        self.incoming_relation_map = defaultdict(list)

        for rel in relations:
            self.incoming_relation_map[rel.to].append(rel)

        self.incoming_relation_map

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
        for index, entity in enumerate(state):
            self.entities[index].load_from_tuple(entity)

    def _apply_relations_to_entities(self, entities):
        result = []

        for entity in entities:
            try:
                incoming_relations = self.incoming_relation_map[entity.name]
            except:
                # No incoming relations found, we don't have anything to apply.
                continue

            relation_states = entity.apply_relations(incoming_relations, entities)

            if not relation_states:
                result.append([EntityTuple(entity.quantity.mag.val, entity.quantity.der.val)])
            else:
                result.append(relation_states)

        states = set(product(*result))

        return states

    def _apply_derivative_to_entities(self, entities):
        # For each entity, apply the current derivative in its current state.
        entity_effects = []

        # TODO: Ensure we only execute the non-exo variables
        for entity in entities:
            # Generate all possible effects
            entity_effects.append(entity.generate_effects())

        states = list(product(*entity_effects))

        return set(states)

    def discover_states(self, state: tuple):
        '''Discover new states from the given state
        '''
        self._load_state(state)
        # TODO: Include exo variables
        deriv_states_set = self._apply_derivative_to_entities(self.entities)
        relation_states_set = self._apply_relations_to_entities(self.entities)

        states = deriv_states_set | relation_states_set

        # 4. Ensure all are consistent.
        return states
        

    def fix_consistent_states(self, states):
        # We need to check a number of things:
        # Check that simple proportional relations are met. (If one is 0 while another is +, fix it! I guess only for 0)
        # Check that VC's are met!
        # Ensure we clip all of derivatives 
        pass

if __name__ == "__main__":
    pass
