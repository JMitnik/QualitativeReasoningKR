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
        
        # print(self.entities)
        for rel_spec in relations_specs:
            print(rel_spec)
            rel = Relation(rel_spec['ty'], [rel_spec['from'], rel_spec['to']], rel_spec['args'])
            self.relations.append(rel)
        print(self.relations)
    
    def _load_entities(entities_specs):
        entities = []

        for entity in entities_specs:
            d = Derivative(DerivativeSpace, DerivativeSpace(entity['d_value']))
            mag_space = mag_q_space[entity['mag_q_space']]
            mag = Magnitude(mag_space, entity['mag_value'])
            entities.append(Entity(entity['title'], mag, d))

        return entities

    def _load_relations(relations_specs):


if __name__ == "__main__":
    from causal_graph_specs import specs
    CausalGraph(specs)
