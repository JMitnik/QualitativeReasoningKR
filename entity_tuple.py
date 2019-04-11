from collections import namedtuple

# Currently takes the simple assumption that an entity only has one quantity.
EntityTuple = namedtuple('EntityTuple', ['mag', 'der', 'mag_q_space', 'title'])