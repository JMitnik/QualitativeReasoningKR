from collections.abc import MutableSet

class Entity(object):
    def __init__(self, name, quantity, derivative):
        self.name = name
        self.quantity = quantity
        self.derivative = derivative
    def __repr__(self):
        return '{}\n\t quantity:{}\t derivative:{}\n'.format(self.name, self.quantity, self.derivative)

    def from_tuple(self, tuple):
        # Convert tuple to e

if __name__ == "__main__":
    test_set = MutableSet()
    test_set.add([3, 4, 5])
    test_set.add([3, 4, 5, 6])
    test_set.add([3, 4, 5])
    print(test_set)