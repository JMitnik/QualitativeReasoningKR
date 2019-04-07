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
            mag = Magnitude(mag_space, mag_space(entity['mag_value']))
            # Todo: for completeness, maybe we should just set the spec to have a list of quantities within an entity (even-though we only have one quantity per entity)
            quantity = Quantity(entity['title'], mag, d)
            entities.append(Entity(entity['title'], quantity))

        return entities

if __name__ == "__main__":
    from causal_graph_specs import specs
    CausalGraph(specs)
