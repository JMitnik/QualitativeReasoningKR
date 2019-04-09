from dataclasses import dataclass, field

@dataclass
class Node:
    state: tuple
    note: str

@dataclass
class Edge:
    from: Node = None
    to: Node = None
    note: str