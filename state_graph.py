from dataclasses import dataclass
from causal_graph import CausalGraph

@dataclass
class StateGraph:
    causal_graph: CausalGraph
    root: Node = None