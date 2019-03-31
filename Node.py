from dataclasses import dataclass

@dataclass
class Node:
    children: Node
    parents: Node