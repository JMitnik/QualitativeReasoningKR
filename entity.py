class Entity(object):
    def __init__(self, name, quantity, derivative):
        self.name = name
        self.quantity = quantity
        self.derivative = derivative
    def __repr__(self):
        return '{}\n\t quantity:{}\t derivative:{}\n'.format(self.name, self.quantity, self.derivative)
