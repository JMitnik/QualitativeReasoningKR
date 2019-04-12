import json

from causal_graph import CausalGraph
from derivative import Derivative
from entity import Entity
from magnitude import Magnitude
from q_spaces import mag_q_space
from quantity import Quantity
from relation import Relation
from state import State
from state_graph import StateGraph
from q_spaces import *

def test_quantity():
    qa = Quantity("a", Magnitude(MagThreeSpace, 1), Derivative(val=1))
    qb = Quantity("b", Magnitude(MagThreeSpace, 1), Derivative(val=1))
    s = State([Entity('a', qa),Entity('b', qb)])
    rel1 = Relation('I+', 'a', 'b')
    rel2 = Relation('I-', 'a', 'b')
    rels = [rel1, rel2]
    print(qb.apply_relations_v2(rels, s))


def main():
    with open("./causal_graph_specs.json", "r+") as specs_file:
        specs = json.load(specs_file)

    # Initialize the starting CausalGraph with the initial settings
    init_entities = bootstrap_entities(specs['entities'])
    init_relations = bootstrap_relations(specs['relations'])

    ent_dict = {ent.name:ent for ent in init_entities}
    rel_dict = {rel.rel_type:rel for rel in init_relations}
    init_state = State(init_entities)
    # test_quantity(ent_dict['container'].quantity, [
                #   rel_dict['I+'], rel_dict['I-']], init_state)
    # test_quantity()

    # causal_graph = CausalGraph(init_entities, init_relations)

    # Initialize the state graph and connect the causal graph.
    # state_graph = StateGraph(causal_graph)

    # Build the state graph
    # state_graph.build_graph()
    # state_graph.plot_graph()


def bootstrap_relations(relations_specs):
    relations = []

    for relation_spec in relations_specs:
        rel = Relation(relation_spec['type'], relation_spec[
                       'from'], relation_spec['to'], relation_spec['args'])
        relations.append(rel)
        # print(rel.fr, rel.rel_type, rel.args)
    return relations


def bootstrap_entities(entities_specs):
    entities = []

    for entity in entities_specs:
        entity_q_magnitude = Magnitude(mag_q_space[entity['mag_q_space']], mag_q_space[
                                       entity['mag_q_space']](int(entity['mag_value'])))
        entity_q_derivative = Derivative(
            Derivative.space, Derivative.space(int(entity['d_value'])))
        entity_quantity = Quantity(
            entity['title'], entity_q_magnitude, entity_q_derivative)
        entities.append(Entity(entity['title'], entity_quantity))

    return entities

if __name__ == "__main__":
    main()
