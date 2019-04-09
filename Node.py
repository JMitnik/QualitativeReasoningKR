from dataclasses import dataclass, field

@dataclass
class Node:
    state: tuple
    note: str = ''

@dataclass
class Edge:
    _from: Node = None
    _to: Node = None
    note: str = ''