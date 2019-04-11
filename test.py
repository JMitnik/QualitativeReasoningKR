import json
from causal_graph import CausalGraph
from entity import Entity

def test():
    with open("./causal_graph_specs.json", "r+") as specs_file:
        specs = json.load(specs_file)

    print()
    specs = tuple([tuple(a.items()) for a in specs['entities']])
    Entity.create_from_tuple(specs[0][0][0], specs[0])

if __name__ == "__main__":
    test()
