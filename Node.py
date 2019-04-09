from dataclasses import dataclass, field

@dataclass
class Node:
    state: tuple
    parents = None
    children: [] = field(default_factory=list)

    