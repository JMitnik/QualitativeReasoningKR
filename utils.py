def tuple2dict(tup):
    return dict((x, y) for x, y in tup)
def dict2tuple(dict):
    return dict.items()
def tuple2str(tup):
    return '\n'.join([' '.join([str(int(tt)) for tt in t]) for t in tup])

if __name__ == "__main__":
    print(tuple2str(((1,1),(2,2))))
