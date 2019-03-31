<!-- - means properties -->
<!-- + means methods -->

# CausalGraph
Stores relations and current state. Responsible for propagating the state to next state.
- entities
- relations
- propagate

# StateGraph
Stores current states in a graph format. Responsible for keeping graph structure and call the propagate function. Should be able to keep record of the traversed states.
- States: Graph
- visitedNodes: MutableSet

# StateNode
The core structure should be made immutable to be stored in set.
- visited: boolean
- children: [StateNode]
- parents: [StateNode]
- state: State
<!-- + transitionToState(probably should be implemented in causalgraph) -->

# State
Or we can omit this data structure and express it as a tuple.
- Entities

# Entity
- name
- quantity
- derivative

# Quantity
- name
- Quantity space
- value

# derivative
- name
- derivative space
- value

# relations
- type
- args
- apply
<!-- - influentialRelationships: [{Quantity, (+, -)}]
- proportionalRelationships: [{Quantity, (+, -)}] 
+ affectValueUsingDerivative -->