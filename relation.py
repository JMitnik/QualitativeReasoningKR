class Relation(object):
    def __init__(self, ty, entities_n, args):
        self.ty = ty
        self.entities_n = entities_n
        self.args = args
    def apply(self, entities):
        pass        
