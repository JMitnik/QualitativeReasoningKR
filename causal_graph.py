from entity import Entity
from quantity import Quantity
from q_spaces import DerivativeSpace, mag_q_space
from derivative import Derivative
from magnitude import Magnitude

class CausalGraph(object):
    def __init__(self, specs):
        self.specs=specs
        self.entities=_load_entities(specs['entities'])
        self.relations=[]
        entities_specs = specs['entities']
        relations_specs = specs['relations']
        init_vals = specs['init_state']
        # fill up the entities list, set the init state
        # for entity_name in entities_specs:
        #     entity_spec = entities_specs[entity_name]
        #     init_val = init_vals[entity_name]
        #     q_n, d_n = tuple(init_val)
        #     quant = Quantity(q_n, entity_spec[q_n], init_val[q_n])
        #     deriv = Derivative(d_n, entity_spec[d_n], init_val[d_n])
        #     self.entities.append(Entity(entity_name, quant, deriv))
        # fill up the relations
        for rel_spec in relations_specs:
            print(rel_spec)
            rel = Relation(rel_spec['ty'], [rel_spec['from'], rel_spec['to']], rel_spec['args'])
            self.relations.append(rel)
        self.relation_map = {}
        for rel in self.relations:
            self.relation_map[rel.to] = rel
        print(self.relations)
    
    def _load_entities(self, entities_specs):
        if self.entities == None:
            self.entities = {}
            
        for entity_n in entities_specs:
            if self.entities[entity_n] == None:
                self.entities[entity_n] = Entity.create_from_tuple(
                    entity_n, entities_specs[entity_n])
            else:
                self.entities[entity_n].load_tuple(entities_specs[entity_n])

        return entities
    # def _load_entities(self, entities_specs):
    #     entities = []

    #     for entity in entities_specs:
    #         d = Derivative(DerivativeSpace, DerivativeSpace(entity['d_value']))
    #         mag_space = mag_q_space[entity['mag_q_space']]
    #         mag = Magnitude(mag_space, mag_space(entity['mag_value']))
    #         # Todo: for completeness, maybe we should just set the spec to have a list of quantities within an entity (even-though we only have one quantity per entity)
    #         quantity = Quantity(entity['title'], mag, d)
    #         entities.append(Entity(entity['title'], quantity))

    #     return entities

    def _to_state(self, entities):
        s = []
        for ent in entities:
            s.append(ent.to_tuple())
        return set(s)

    def propagate(self, entities_specs):
        self._load_entities(entities_specs)
        
        all_possible_states = []
        new_states = lambda : deepcopy(self.entities)
        # 1. check the ambiguity of exogenous variable
        exo_var_n = 'inlet'
        exo_var = self.entities[exo_var_n]
        # if exo_var.quantity.derivative==0:
        for d in exo_var.quantity.valid_der():
            new_s = new_states()
            new_exo_var = new_s[exo_var_n]
            new_exo_var.set_der()
            all_possible_states.append(new_s)
        # 2. check the ambiguity of derivative applying
        state_li_after_applying = []
        for entity_n in self.entities:
            entity = self.entities[entity_n]
            ent_li = entity.apply_der()
            state_li_after_applying.append(ent_li)
            # if entity.derivative!=0:
            #     if entity.quantity==0:
            #         new_s = new_states()
            #         new_s[entity_n].apply_der()
        new_states+=list(product(state_li_after_applying))

        # 3. check the ambiguity of relations
        for entity_n in self.relation_map:
            rels = self.relation_map[entity_n]
            rels_n = {r.ty:r for r in rels}
            q_influence = []
            d_influence = []
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
                    pass
            if 'I-' in rels_n and 'I+' in rels_n:
                minus_rel = rels[rels_n.index('I-')]
                minus_rel = rels[rels_n.index('I-')]

if __name__ == "__main__":
    from causal_graph_specs import specs
    CausalGraph(specs)
