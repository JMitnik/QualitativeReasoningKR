import json
from causal_graph import CausalGraph
from state_graph import StateGraph

def main():
    with open("./causal_graph_specs.json", "r+") as specs_file:
        specs = json.load(specs_file)
    
    init_causal_graph = CausalGraph(specs)
    app_state_graph = StateGraph(init_causal_graph)
    app_state_graph.build_graph()

    # Create a state_graph with this causal graph
    # state_graph.build_graph() -> Iterative process, go on until no more new states or something
    # At the end, we have a graph
    
    print([tuple(a.items()) for a in specs['entities']])

if __name__ == "__main__":
    main()
