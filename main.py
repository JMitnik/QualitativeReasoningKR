import json
from causal_graph import CausalGraph
from q_spaces import mag_q_space
from state_graph import StateGraph
from quantity import Quantity
from magnitude import Magnitude
from derivative import Derivative
from relation import Relation
from entity import Entity

def main():
    with open("./causal_graph_specs.json", "r+") as specs_file:
        specs = json.load(specs_file)
    
    # Initialize the starting CausalGraph with the initial settings
    init_entities = bootstrap_entities(specs['entities'])
    init_relations = bootstrap_relations(specs['relations'])
    causal_graph = CausalGraph(init_entities, init_relations)

    # Initialize the state graph and connect the causal graph.
    state_graph = StateGraph(causal_graph)

    # Build the state graph
    state_graph.build_graph()

def bootstrap_relations(relations_specs):
    relations = []

    for relation_spec in relations_specs:
        rel = Relation(relation_spec['type'], [relation_spec['from'], relation_spec['to']], relation_spec['args'])
        relations.append(rel)

    return relations

def bootstrap_entities(entities_specs):
    entities = []

    for entity in entities_specs:
        entity_q_magnitude = Magnitude(mag_q_space[entity['mag_q_space']], mag_q_space[entity['mag_q_space']](int(entity['mag_value'])))
        entity_q_derivative = Derivative(Derivative.space, Derivative.space(int(entity['d_value'])))
        entity_quantity = Quantity(entity['title'], entity_q_magnitude, entity_q_derivative)
        entities.append(Entity(entity['title'], entity_quantity))

    return entities

if __name__ == "__main__":
    main()
