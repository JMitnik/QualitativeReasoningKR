from dataclasses import dataclass, field
from causal_graph import CausalGraph
from node import Node

@dataclass
class StateGraph:
    causal_graph: CausalGraph
    root: Node = None
    visitedStates: set = field(default_factory=set)

    def build_graph(self):
        '''Builds a graph from the start
        '''

        # First we extract our initial state from the causal_graph
        test_state = self.causal_graph.state
        test_state

