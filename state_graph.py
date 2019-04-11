from dataclasses import dataclass, field
from causal_graph import CausalGraph
from node import Node

@dataclass
class StateGraph:
    causal_graph: CausalGraph
    root: Node = None
    foundStates: set = field(default_factory=set)
    visitedStates: set = field(default_factory=set)

    def build_graph(self):
        '''Starts the graph building process.
        '''

        # We extract our current state from the causal_graph, and ensure we add it
        self.foundStates.add(self.causal_graph.state)
        self.root = Node(self.causal_graph.state)

        # While we sitll haven't explored all states
        while (self.foundStates - self.visitedStates):
            current_state = list(self.foundStates - self.visitedStates)[0]

            # We propagate and discover new states
            possible_states = self.causal_graph.discover_states(current_state)

            # Ensure we denote this state as visited
            self.visitedStates.add(current_state)
            self.foundStates = self.foundStates | possible_states