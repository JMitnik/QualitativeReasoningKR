from dataclasses import dataclass

@dataclass
class Node:
    children: List[Node]
    parents: Node = None