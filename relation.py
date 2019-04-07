from dataclasses import dataclass
from enum import Enum

RelationTypes = Enum('RelationTypes', 'I+ I- P+ P- CV')

@dataclass
class Relation:
    rel_type: RelationTypes
    fr:''
    to:''
    args:str=''
    entities_n: int = 2
    
    def apply(self, entities):
        pass        

if __name__ == "__main__":
    relation = Relation('I+', 'rua', 'pua')
    relation