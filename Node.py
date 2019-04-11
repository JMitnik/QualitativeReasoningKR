from dataclasses import dataclass, field

@dataclass
class Node:
    state: tuple
<<<<<<< HEAD
    note: str = ''

@dataclass
class Edge:
    _from: Node = None
    _to: Node = None
    note: str = ''
=======
    parents = None
    children: [] = field(default_factory=list)

    
>>>>>>> c1ce6fabeed956fcd7280b6fe8f8bcab93d56867
