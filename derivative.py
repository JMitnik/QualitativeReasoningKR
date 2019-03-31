class Derivative(object):
    def __init__(self, name, space, init_val):
        self.name = name
        self.space = space
        self.init_val = init_val
    def __repr__(self):
        return '{}\n\t space:{}\t init:{}\n'.format(self.name, self.space, self.init_val)