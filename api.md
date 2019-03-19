<!-- - means properties -->
<!-- + means methods -->

# StateGraph
- States: Graph
- visitedNodes: MutableSet

# State
- visited: boolean
- children: [State]
- parents: [State]
+ transitionToState

# Entity

# Quantity
- Quantity space
- value
- derivative value
- influentialRelationships: [{Quantity, (+, -)}]
- proportionalRelationships: [{Quantity, (+, -)}] 
+ affectValueUsingDerivative