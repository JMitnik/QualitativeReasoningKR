from dataclasses import dataclass
from enum import Enum

RelationTypes = Enum('RelationTypes', 'I+ I- P+ P- CV')

@dataclass
class Relation:
    type: RelationTypes
    entities_n: int = 2
    
    def apply(self, entities):
        pass        

if __name__ == "__main__":
    relation = Relation()
    relation