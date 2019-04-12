class State(object):

    def __init__(self, state_tup, exo_stack=[-1, 1]):
        self.state_tup = list(state_tup)
        self.state_dict = {e.name:e for e in state_tup}
        self.exo_stack = exo_stack
        self.note = ''

    def __hash__(self):
        return hash(''.join([str(ent) for ent in self.state_tup]))

    def __repr__(self):
        return '\n'.join([str(ent) for ent in self.state_tup])

    def __str__(self):
        return self.__repr__()
    
    def __iter__(self):
        for ent in self.state_tup:
            yield ent
    def __getitem__(self, i):
        if isinstance(i, int):
            return self.state_tup[i]
        elif isinstance(i, str):
            return self.state_dict[i]
        else:
            raise ValueError()

    def __setitem__(self, k, v):
        if isinstance(k, int):
            self.state_tup[k] = v
            self.state_dict = {e.name: e for e in state_tup}
            return 
        elif isinstance(k, str):
            self.state_dict[k] = v
            self.state_tup = list(self.state_dict.values())
            return 
        else:
            raise ValueError()
    def pop_exo(self):
        if len(self.exo_stack) == 0:
            return 0
        else:
            return self.exo_stack.pop()
    def gen_child(self, state_tup):
        return State(state_tup, self.exo_stack)

    def funcname(parameter_list):
        pass

if __name__ == "__main__":
    from entity import Entity
    a = Entity('a', None)
    b = Entity('b', None)
    c = Entity('c', None)
    s = State([a, b, c])
    print(s)
    s['a'] = 'rua'
    print(s)
