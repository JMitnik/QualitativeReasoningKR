from dataclasses import dataclass, field
from causal_graph import CausalGraph
from node import Node, Edge
from utils import tuple2str
from pygraphviz import AGraph
from enum import Enum

class Differences(Enum):
    much_smaller_than = -2
    smaller_than = -1
    equal_to = 0
    larger_than = 1
    much_larger_than = 2

@dataclass
class StateGraph:
    causal_graph: CausalGraph
    root: Node = None
    visitedStates: dict = field(default_factory=dict)
    edges: list = field(default_factory=list)
    nodeCount: int = 0

    def build_graph(self):
        '''Starts the graph building process.
        '''

        # We extract our current state from the causal_graph, and ensure we add it
        current_state = self.causal_graph.state
        self.visitedStates[str(current_state)] = True
        self.root = Node(current_state, self.nodeCount)

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
                if str(s) not in self.visitedStates:
                    stop = False
                    self.visitedStates[str(s)] = True
                    # print(state)
                    # self.dfs(child_node)
                self.nodeCount += 1
                child_node.index = self.nodeCount
                self.edges.append(Edge(node, child_node))
                    # continue
            break
        return 

    def get_state_trace(self, node_index):
        nodes_from = [edge._from for edge in self.edges if edge._from.index == node_index]
        nodes_to = [edge._to for edge in self.edges if edge._to.index == node_index]

        nr_pointed_to = len(nodes_to)
        if nodes_from:
            node = nodes_from[0]

        if nodes_to:
            node = nodes_to[0]

        if node:
            template = ''' State {} has {} number of nodes pointing out, and {} pointing in. 
                - Inflow: The magnitude is {} and derivative is {}!
                - Outflow: The magnitude is {} and derivative is {}!
                - Container: The magnitude is {} and derivative is {}!
            '''.format(node_index, len(nodes_from), len(nodes_to), node.state['inflow'].quantity.mag.val, node.state['inflow'].quantity.der.val, node.state['outflow'].quantity.mag.val, node.state['outflow'].quantity.der.val, node.state['container'].quantity.mag.val, node.state['container'].quantity.der.val)
            print(template)
            return node

    def get_inter_state_trace(self, node_index_from, node_index_to):
        nodes_from = [edge._from for edge in self.edges if edge._from.index == node_index_from]
        nodes_to = [edge._to for edge in self.edges if edge._to.index == node_index_to]

        entities = ['inflow', 'container', 'outflow']
        differences = []

        try:
            node_from = nodes_from[0]
            node_to = nodes_to[0]

            template = f''' States {node_from.index} and {node_to.index} have a number of differences between them.'''

            for entity in entities:
                magnitude_difference = node_from.state[entity].quantity.mag.val - node_to.state[entity].quantity.mag.val
                derivative_difference = node_from.state[entity].quantity.der.val - node_to.state[entity].quantity.der.val

                if magnitude_difference or derivative_difference:
                    template += f'\n\nThere is a difference for the {entity} entity!'

                if magnitude_difference != 0:
                    if magnitude_difference > 0:
                        magnitude_difference = str(magnitude_difference) + ' greater'

                    else:
                        magnitude_difference = str(magnitude_difference) + ' lesser'

                    template += f'\n\tThe magnitude is not the same anymore! The difference of state {node_from.index} for {entity} is {magnitude_difference} compared to state {node_to.index}'
                
                if derivative_difference != 0:
                    if derivative_difference > 0:
                        magnitude_difference = str(derivative_difference) + ' greater'

                    else:
                        magnitude_difference = str(derivative_difference) + ' lesser'

                    template += f'\n\tThe derivative is not the same! The difference of state {node_from.index} for {entity} is {derivative_difference} compared to state {node_to.index}'
            
            print(template)
            return (node_from, node_to)

        except:
            print("Invalid indices. Are you sure these nodes exist?")
            return

    def plot_graph(self):
        A=AGraph(directed=True)

        # set some default node attributes
        A.node_attr['style']='filled'
        A.node_attr['shape']='box'
        # A.node_attr['fixedsize']='true'
        A.node_attr['fontcolor']='#fff'

        for index, edge in enumerate(self.edges):
            # print(edge)
            from_node = edge._from
            to_node = edge._to
            from_state = edge._from.state
            to_state = edge._to.state
            if str(from_state) != str(to_state):
                A.add_edge(str(from_node), str(to_node), index)

        A.write("result.dot") # write to simple.dot

        print("Wrote result.dot")
        A.draw('result.png',prog="dot") # draw to png using circo
        print("Wrote result.png")

            
