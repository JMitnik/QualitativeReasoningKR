from dataclasses import dataclass, field

@dataclass
class Node:
    state: tuple
    index: int = None

    def __repr__(self):
        return '\n'.join([str('State: {}'.format(self.index)), str(self.state)])

    def __str__(self):
        return self.__repr__()

@dataclass
class Edge:
    _from: Node = None
    _to: Node = None
    note: str = ''
