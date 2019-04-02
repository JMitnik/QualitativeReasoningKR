from entity import Entity
from quantity import Quantity

class CausalGraph(object):
    def __init__(self, specs):
        self.specs=specs
        self.entities=[]
        self.relations=[]
        entities_specs = specs['entities']
        relations_specs = specs['relations']
        init_vals = specs['init_state']
        
        for entity_name in entities_specs:
            entity_spec = entities_specs[entity_name]
            init_val = init_vals[entity_name]
            q_n, d_n = tuple(init_val)
            quant = Quantity(q_n, entity_spec[q_n], init_val[q_n])
            deriv = Derivative(d_n, entity_spec[d_n], init_val[d_n])
            self.entities.append(Entity(entity_name, quant, deriv))
        # print(self.entities)
        for rel_spec in relations_specs:
            print(rel_spec)
            rel = Relation(rel_spec['ty'], [rel_spec['from'], rel_spec['to']], rel_spec['args'])
            self.relations.append(rel)
        print(self.relations)

if __name__ == "__main__":
    from causal_graph_specs import specs
    CausalGraph(specs)
