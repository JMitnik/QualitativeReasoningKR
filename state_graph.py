from dataclasses import dataclass, field
from causal_graph import CausalGraph
from node import Node

@dataclass
class StateGraph:
    causal_graph: CausalGraph
    root: Node = None
    visitedStates: set = field(default_factory=set)

    def build_graph(self):
        '''Starts the graph building process.
        '''

        # We extract our current state from the causal_graph, and ensure we add it
        current_state = self.causal_graph.state
        self.visitedStates.add(current_state)
        self.root = Node(current_state)

        # We propagate and discover new states
        possible_states = self.causal_graph.discover_states(current_state)
