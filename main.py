import json
from causal_graph import CausalGraph

def main():
    with open("./causal_graph_specs.json", "r+") as specs_file:
        specs = json.load(specs_file)
    
    print([tuple(a.items()) for a in specs['entities']])

if __name__ == "__main__":
    main()
