from entity import Entity
from quantity import Quantity
from relation import Relation
from q_spaces import DerivativeSpace, mag_q_space
from derivative import Derivative
from magnitude import Magnitude

class CausalGraph(object):
    def __init__(self, specs):
        self.specs=specs
        self.entities={}
        self.relations=[]
        self.incoming_relation_map = {}

        self.entities = self._load_entities(specs['entities'])
        self.relations = self._lad_relations(specs['relations'])
    
    def _load_entities(self, entities_specs):
        for entity in entities_specs:
            if self.entities.get(entity['title']) == None:
                self.entities[entity['title']] = Entity.create_from_tuple(entity['title'], entity)
            else:
                self.entities[entity].load_tuple(entity)

        return entities

    def _load_relations(self, relations_specs):        
        for rel_spec in relations_specs:
            rel = Relation(rel_spec['type'], [rel_spec['from'], rel_spec['to']], rel_spec['args'])
            self.relations.append(rel)

        for rel in self.relations:
            self.incoming_relation_map[rel.to] = rel

    def _to_states(self, states):
        result = []

        for state in states:
            result.append(self._to_state(state))

        return tuple(result)

    def _to_state(self, entities):
        s = []

        for ent in entities:
            s.append(ent.to_tuple())

        return set(s)

    @property
    def state(self):
        return self._to_state(self.entities)

    def propagate(self, entities_specs):
        self._load_entities(entities_specs)
        
        all_possible_states = []
        new_entities = lambda : deepcopy(self.entities)
        # 1. check the ambiguity of exogenous variable
        # TODO: Make this a consistent Enum
        exo_var_n = 'inlet'
        exo_var = self.entities[exo_var_n]
        # if exo_var.quantity.derivative==0:

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
