from entity_tuple import EntityTuple
from entity import Entity
from quantity import Quantity
from relation import Relation
from q_spaces import DerivativeSpace, mag_q_space
from derivative import Derivative
from magnitude import Magnitude

class CausalGraph:
    def __init__(self, entities: list, relations: list):
        '''Initialize a causal-graph.
        
        Arguments:
            entities
            relations {[type]} -- [description]
        '''
        self.entities = entities
        self.relations = relations
        self.incoming_relation_map = {rel.to: rel for rel in relations }

    def _to_states(self, states):
        result = []

        for entities_state in states:
            result.append(self._to_state(entities_state))

        return tuple(result)

    def _to_state(self, entities_state):
        s = []

        for ent in entities_state:
            s.append(ent.to_tuple())

        return set(s)

    @property
    def state(self):
        return self._to_state(self.entities)

    def _load_state(self, state):
        # The index of each namedtuple in the state corresponds to the entity in
        # self.entities.

        # Go over each entity, and set their value
        pass

    def propagate(self, state: tuple):
        # We take in some 'state'
        self._load_state(state)

        all_possible_states = []
        new_entities = lambda : deepcopy(self.entities)
        # 1. check the ambiguity of exogenous variable
        # TODO: Make this a consistent Enum

        exo_var_n = 'inlet'
        exo_var = self.entities[exo_var_n]
        # TODO: Make valid_der method
        for valid_der in exo_var.quantity.valid_der():
            new_s = new_entities()
            new_exo_var = new_s[exo_var_n]

            # TODO: Make set_der method
            new_exo_var.set_der(valid_der)
            all_possible_states.append(new_s)

        # 2. check the ambiguity of derivative applying
        state_li_after_applying = []

        for entity_n in self.entities:
            entity = self.entities[entity_n]
            ent_li = entity.apply_der()
            state_li_after_applying.append(ent_li)
            # if entity.derivative!=0:
            #     if entity.quantity==0:
            #         new_s = new_entities()
            #         new_s[entity_n].apply_der()
        new_entities+=list(product(state_li_after_applying))

        # TODO: Create another loop which checks for exogenous states within possible ambigutiies (other than stable)

        # 3. check the ambiguity of relations
        for entity_n in self.relation_map:
            rels = self.relation_map[entity_n]
            rels_n = {r.ty:r for r in rels}
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

if __name__ == "__main__":
    pass
