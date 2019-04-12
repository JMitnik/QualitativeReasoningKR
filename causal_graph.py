from entity_tuple import EntityTuple
from entity import Entity
from quantity import Quantity
from relation import Relation
from q_spaces import DerivativeSpace, mag_q_space
from derivative import Derivative
from magnitude import Magnitude
from itertools import product
from state import State

from copy import deepcopy, copy
from collections import defaultdict

class CausalGraph:
    def __init__(self, entities: list, relations: list):
        '''Initialize a causal-graph.

        Arguments:
            entities
            relations {[type]} -- [description]
        '''
        # self.entities = entities
        self.state = State(entities)
        self.relations = relations
        self.incoming_relation_map = defaultdict(list)

        for rel in relations:
            self.incoming_relation_map[rel.to].append(rel)

        self.incoming_relation_map

    def _to_states(self, states):
        result = []

        for entities_state in states:
            result.append(self._to_state(entities_state))

        return list(set(deepcopy(result)))  # Unique values only

    # def _to_state(self, entities_state):
    #     s = []
    #     for ent in entities_state:
    #         s.append(ent.to_tuple())

    #     return tuple(s)

    # @property
    # def state(self):
    #     # return self._to_state(self.entities)
    #     return self.state

    def _load_state_v2(self, state):
        self.state = deepcopy(state)

    def _load_state(self, state):
        # print(state)
        for index, entity in enumerate(state):
            self.state[index].load_from_tuple(entity)

    def _apply_relations_to_entities(self, states, ty='I'):
        result = []
        for s in states:
            s_res = [[],[],[]]
            for i, ent in enumerate(s):
                # ent_li = []
                try:
                    incoming_relations = self.incoming_relation_map[ent.name]
                except:
                    # No incoming relations found, we don't have anything to apply.
                    s_res[i]+=([deepcopy(ent)])
                    print('rua')
                    continue
                if len(incoming_relations)==0:
                    s_res[i]+=([deepcopy(ent)])
                    continue
                # print(ent)
                for rel in incoming_relations:
                    if not rel.rel_type.startswith(ty):
                        if (ent) not in s_res[i]:
                            s_res[i]+=([deepcopy(ent)])
                        continue
                    relation_results = ent.apply_relations_v2([rel], s)
                    # print(ent, relation_results)
                    s_res[i]+=(relation_results)
                    # ent_tmp_li = []
                    # if relation_results:
                    #     for ent_res in relation_results:
                    #         ent_n = deepcopy(ent)
                    #         # new_entities = list(new_entities)
                    #         ent_n = ent_n.create_new_from_tuple(ent_res)
                    #         ent_tmp_li.append(ent_n)
                    # else:
                    #     ent_n = deepcopy(ent)
                    #     ent_tmp_li.append(ent_n)
            # print(s_res)
            s_res = [s.gen_child(deepcopy(ss)) for ss in product(*s_res)]
            result+=s_res

        states = set(result)

        return states

    def _apply_derivative_to_entities_v2(self, state):
        # For each entity, apply the current derivative in its current state.
        entity_effects = []

        # TODO: Ensure we only execute the non-exo variables
        for entity in state:
            # Generate all possible effects
            entity_effects.append(entity.generate_effects_v2())
        states = [state.gen_child(deepcopy(s))
                  for s in product(*entity_effects)]
        return states


    def _apply_derivative_to_entities(self, state):
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

    def _apply_exo_var(self, states):
        res = []
        for state in states:
            # li = []
            for ent in state:
                if ent.name == 'inflow':
                    ns = deepcopy(state)
                    nent = ent.set_der_v2(state.pop_exo())
                    ns[ent.name] = nent
                    res+=[ns, deepcopy(state)]
        return res

    def discover_states(self, state):
        '''Discover new states from the given state
        '''
        self._load_state_v2(state)
        # TODO: Include exo variables

        deriv_states = self._apply_derivative_to_entities_v2(self.state)
        relation_states = self._apply_relations_to_entities(deriv_states, 'I')
        relation_states = self._apply_relations_to_entities(relation_states, 'P')
        # exo_states = self._apply_exo_var(relation_states)
        
        # PIN: Currently, we have the proportional relations in opposite directions ocassionally.
        # PIN: Also, possibly might be pruning too many states, but can't be sure yet.
        # FIXME The implemenetation suggests that it might be possible if say, relation has been going downhill,
        # and the other relation suddenly goes uphill twice, but in theory can't convince the downhill proportionality.
        # This might be a problem coming from the relations.

        # states = deriv_states_set | relation_states_set
        # TODO 4. Ensure all are consistent.
        # states = self.fix_consistent_states_v2(exo_states)
        states = relation_states
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

    def fix_VC_states_v2(self, states):
        VC_relations = [relation for relation in self.relations if relation.rel_type == 'VC']
        result = []

        for state in states:
            state = self.load_entities_from_state(state)
            satisfiable = True
            # Now we have a list of state
            for VC_relation in VC_relations:
                value = VC_relation.args
                entity_from = [entity for entity in state if entity.name ==  VC_relation.fr][0]
                entity_to = [entity for entity in state if entity.name ==  VC_relation.to][0]
            
                if (entity_from.quantity.mag.val == entity_from.quantity.mag.q_space[value]
                    and entity_from.quantity.mag.val != entity_to.quantity.mag.val):
                    satisfiable = False

            if satisfiable:
                result.append(state)

        return list(set(result))

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

    def constrain_extreme_derivatives_v2(self, states):
        # result = []

        for state in states:
            state_result = []
            # entities = self.load_entities_from_state(state)

            for entity in state:
                entity.constrain_extreme_derivatives()
                # state_result.append(entity.to_tuple())
            
            # result.append(tuple(state_result))
        
        return list(set(states))

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

if __name__ == "__main__":
    pass
