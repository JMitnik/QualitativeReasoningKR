class StateGraph(object):
    def __init__(self, causal_graph):
        self.causal_graph = causal_graph
        self.root = None
        