from dataclasses import dataclass, field
from causal_graph import CausalGraph
from node import Node, Edge
from utils import tuple2str
from pygraphviz import AGraph

@dataclass
class StateGraph:
    causal_graph: CausalGraph
    root: Node = None
    visitedStates: dict = field(default_factory=dict)
    edges: list = field(default_factory=list)

    def build_graph(self):
        '''Starts the graph building process.
        '''

        # We extract our current state from the causal_graph, and ensure we add it
        current_state = self.causal_graph.state
        self.visitedStates[tuple2str(current_state)] = True
        self.root = Node(current_state)

        # We propagate and discover new states
        # possible_states = self.causal_graph.discover_states(current_state)
        self.dfs(self.root)
        print(self.visitedStates)

    def dfs(self, node):
        stop = False
        state = node.state
        while not stop:
            stop = True
            for s in self.causal_graph.discover_states(state):
                # print(stop)
                child_node = Node(s)
                if tuple2str(s) not in self.visitedStates:
                    stop = False
                    self.visitedStates[tuple2str(s)] = True
                    # print(state)
                    self.dfs(child_node)
                self.edges.append(Edge(node, child_node, ''))
                    # continue
        return 

    def plot_graph(self):

        A=AGraph(directed=True)

        # set some default node attributes
        A.node_attr['style']='filled'
        A.node_attr['shape']='box'
        # A.node_attr['fixedsize']='true'
        A.node_attr['fontcolor']='#000000'

        for edge in self.edges:
            # print(edge)
            from_state = edge._from.state
            to_state = edge._to.state
            if from_state != to_state:
                A.add_edge(tuple2str(from_state), tuple2str(to_state))
        A.write("result.dot") # write to simple.dot
        print("Wrote result.dot")
        A.draw('result.png',prog="dot") # draw to png using circo
        print("Wrote result.png")

            
