from entity_tuple import EntityTuple
from entity import Entity
from quantity import Quantity
from relation import Relation
from q_spaces import DerivativeSpace, mag_q_space
from derivative import Derivative
from magnitude import Magnitude
<<<<<<< HEAD
from itertools import product

from copy import deepcopy
from collections import defaultdict
=======
from copy import deepcopy
>>>>>>> c1ce6fabeed956fcd7280b6fe8f8bcab93d56867

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
        self.incoming_relation_map = defaultdict(list)

        for rel in relations:
            self.incoming_relation_map[rel.to].append(rel)

        self.incoming_relation_map
=======
        self.entities_map = {ent.name:ent for ent in entities}
        self.incoming_relation_map = {rel.to: rel for rel in relations }
>>>>>>> c1ce6fabeed956fcd7280b6fe8f8bcab93d56867

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
        # print(state)
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
        # states = [((q.mag.val, q.der.val) for q in s) for s in states]
        # print(states)
        tmp  =[]
        for s in states:
            print(s[0])
            tmp.append(tuple([tuple([EntityTuple(q.mag.val, q.der.val) for q in s])]))
        states = tuple(tmp)
        print(states[0])
        # We might have some strange errors in these states. We want to ensure
        # that our states follow the proportional principle. If one relation

        return set(states)

    def discover_states(self, state: tuple):
        '''Discover new states from the given state
        '''
        self._load_state(state)
        # TODO: Include exo variables

        deriv_states_set = self._apply_derivative_to_entities(self.entities)
        relation_states_set = self._apply_relations_to_entities(self.entities)
        
        # PIN: Currently, we have the proportional relations in opposite directions ocassionally.
        # PIN: Also, possibly might be pruning too many states, but can't be sure yet.
        # FIXME The implemenetation suggests that it might be possible if say, relation has been going downhill,
        # and the other relation suddenly goes uphill twice, but in theory can't convince the downhill proportionality.
        # This might be a problem coming from the relations.

        states = deriv_states_set | relation_states_set
        # TODO 4. Ensure all are consistent.
        states = self.fix_consistent_states(states)
        return states
        

    def fix_consistent_states(self, states):
        # We need to check a number of things:
        states = self.fix_VC_states(states)
        states = self.constrain_extreme_derivatives(states)
        # Ensure we clip all of derivatives 
        return states

    def load_entities_from_state(self, state):
        result = []

        # print(state)
        if len(state)==1:
            state = state[0]
        for index, entity_state in enumerate(state):
            current_entity = self.entities[index]
            result.append(current_entity.create_new_from_tuple(entity_state))

        return result

    def fix_VC_states(self, states):
        VC_relations = [relation for relation in self.relations if relation.rel_type == 'VC']
        result = []

        for state in states:
            entities = self.load_entities_from_state(state)
            satisfiable = True
            # Now we have a list of entities
            for VC_relation in VC_relations:
                value = VC_relation.args
                entity_from = [entity for entity in entities if entity.name ==  VC_relation.fr][0]
                entity_to = [entity for entity in entities if entity.name ==  VC_relation.to][0]
            
                if (entity_from.quantity.mag.val == entity_from.quantity.mag.q_space[value]
                    and entity_from.quantity.mag.val != entity_to.quantity.mag.val):
                    satisfiable = False

            if satisfiable:
                result.append(state)

        return set(result)

    def constrain_extreme_derivatives(self, states):
        result = []

        for state in states:
            state_result = []
            entities = self.load_entities_from_state(state)

            for entity in entities:
                entity.constrain_extreme_derivatives()
                state_result.append(entity.to_tuple())
            
            result.append(tuple(state_result))
        
        return set(result)


    def trace_template_intra_states(states):
        result_entities_text = []

        for state in states:
            # We can have terminal states in our trace for our state.
            # Add in entities.
            entity_template = 'In this state, our {} has reached value {}.'.format

<<<<<<< HEAD

=======
    def propagate(self, state: tuple):
        all_possible_states = []
        new_entities = lambda : deepcopy(self.entities_map)
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
        return self._to_states(new_entities)
>>>>>>> c1ce6fabeed956fcd7280b6fe8f8bcab93d56867
if __name__ == "__main__":
    pass
