from entity_tuple import EntityTuple
from entity import Entity
from quantity import Quantity
from relation import Relation
from q_spaces import DerivativeSpace, mag_q_space
from derivative import Derivative
from magnitude import Magnitude

class CausalGraph:
    def __init__(self, entities: list, relations: list):
        '''Initialize a causal-graph.
        
        Arguments:
            entities
            relations {[type]} -- [description]
        '''
        self.entities = entities
        self.relations = relations
        self.incoming_relation_map = {rel.to: rel for rel in relations }

    def _to_states(self, states):
        result = []

        for entities_state in states:
            result.append(self._to_state(entities_state))

        return tuple(result)

    def _to_state(self, entities_state):
        s = []

        for ent in entities_state:
            s.append(ent.to_tuple())

        return tuple(s)

    @property
    def state(self):
        return self._to_state(self.entities)

    def _load_state(self, state):
        # The index of each namedtuple in the state corresponds to the entity in
        # self.entities.

        # Go over each entity, and set their value
        for index, entity in enumerate(state):
            self.entities[index].load_from_tuple(entity)

    def discover_states(self, state: tuple):
        '''Discover new states from the given state
        '''
        discovered_states = []
        self._load_state(state)

        '''
            0: we have a setting, set our derivatives and magnitudes.

            State 1: Inflow(+, +), Volume(+, +), Outflow(+, +).
        -------
            1. Start with the exogenous variables. Go through all of the
               possible values. We get to the state where Inflow is (+ +)

            IDEA 1: Grab some Entity

                1.1. Start with one of the two other entities, e.g. Volume.

                1.1.1. Look at all of the incoming relations, that being Inflow and
                Outflow.

                Case: Ambiguity

                In theory, these have both an influence on this entity. If both of
                these influences are **active**, then that means that we have an ambiguity.

                We can't instantly set set the current state and apply the derivative,
                because we don't know what the derivative will do on the next state.
                Thus, we need to create at least 3 new states to resolve this ambiguity.

                    *  We also need to account for the fact that our exogenous might act
                    differently, so we generate for each of these 3 states also an extra
                    state in which the exogenous acts differently Inflow(0, 0) and Inflow(+, +).

                ? How do we generate these states?
                    * Exogenous is already accounted for.
                    * Volume is resolved based on the ambiguity
                    * Outflow will follow Volume based on the P (and thus, might reach max before Volume?)
                        * This is part of the ambiguity handling: if an ambiguity is found, this function
                            will decide the state of the outflow quantity.

                Before pushing the final state, we need to ensure that value correspondences are met. We prune the states which are not value correspondent.

            State 2: Inflow(0, 0), Volume(+, +), Outflow(+, +)
        -------
            Can we reach this state, or is it immediately ammended to become
            Outflow(0, +)? -> No, we probably need to ensure that a State is
            resolved before actually being generated.

            PRIOR STATE: So let's assume we are in the prior state, Inflow(0,
            0), Volume(+, +), Outflow(0, +).

            GENERATING STATES FROM PRIOR STATE: We generate the state that
            Inflow is positive, ie Inflow(+, +). According to our relationships
            that should influence Outflow to have a negative influence on volume
            again (magnitude becomes positive),

            ENSURING PROPER CHILD STATES FROM PRIOR STATE: Ambiguity starts
            again! Within inflow, we know that outflow has become + and +.
            However, how this impacts our volume is unknown. When checking the
            the generated next state, we see that our 

            Question is, where do we decide this ambiguity.

            
            # `proportional relationship implies that the derivative of the to entity should always stay the same with 

            AGAIN, EXAMPLE:

            Inflow(0,0), Volume(+, +), Outflow(0, +).

            # STAGE 0: CHECK FOR AMBIGUITIES
            
            # STAGE 1: APPLY DERIVATIVES
            Inflow might be +,0 or 0,0.
            Volume might be +,+ or (max,+ = max, 0)
            Outflow can only be +, +,

            # We want to generate top-level all ambiguities as well, and in the check-stage, ensure that the relationships are met.

            Start_Generate_states([{
                Inflow(0, 0),
                Volume(+, +),
                Outflow(+, +)
            }, {
                Inflow(0, 0),
                Volume(max, +), <- Will be pruned, can't be the case
                Outflow(+, +) 
            }, {
                Inflow(+, +),
                Volume(+, +),
                Outflow(+, +)
            },
            {
                Inflow(+, +),
                Volume(max, +), <- Will be pruned, can't be the case anyways!
                Outflow(+, +)
            }
            ])

            Now we have 4 possible states future, but we don't know how 'correct' they are.

            So, we now check each state for possible inconsistencies or conflicts.

            Substate1
                Inflow(0, 0),
                Volume(+, +),
                Outflow(+, +)

            Let's go by value correspondences first: VC(Vol 0 and maz -> Outflow 0 and max), no inconsistencies!

            Next, the relations, we examine them by the incoming relations.
            * Inflow has no incoming relations, all is well!
            * Volume has two incoming relations, but only one is active. 
                By piping the output of one supposed relation to the entity, we notice a difference in result: either volume goes up, or it becomes neutral.

            Substate1-childa <-
                Inflow(0, 0),
                Volume(+, +),
                Outflow(+, +)

            ❗ If we somehow pass that the ambiguity between volume and outflow has been resolved (maybe a list of confirmed relations), then we are done.

            Substate1-childb <-
                Inflow(0, 0),
                Volume(+, 0),
                Outflow(+, +)

            This is wrong, we can't have two different derivatives for volume and outflow, so we change the outflow derivative to 0

            Substate1bv2
                Inflow(0, 0),
                Volume(+, 0),
                Outflow(+, 0)
            
            One more check, all relations are satisfied, and our original ambiguity was marked as resolved.

            We noticed an inconsistency, and thus, we split this substate into two child substates, each with a different result. Now, we need to examine both split
            states and see if there are other inconsistencies in the direct instantaneous relations! 

            SO IN THE END:

            1a. Apply relations in current state: of each of the individual ambigiuties, apply new subchild.
            1b. Apply derivatives, ensure that we have both landmark and interval derivatvie results.
            2. Union this set of states;.
            3. Ensure that each are consistent to the relation (except for the actual ambiguity: thus, change values / prune values which are not consistent.)
        '''

        # TODO: Generate states from possible ambiguities
        
        entity_effects = []
        for entity in self.entities:
            # Generate all possible effects
            entity_effects = entity.generate_effects()
            entity_effects.append(entity.generate_effects())

    def propagate(self, state: tuple):
        all_possible_states = []
        new_entities = lambda : deepcopy(self.entities)
        # 1. check the ambiguity of exogenous variable

        # TODO Make this a consistent Enum

        exo_var_n = 'inlet'
        exo_var = self.entities[exo_var_n]
        # TODO: Make valid_der method
        for valid_der in exo_var.quantity.valid_der():
            new_s = new_entities()
            new_exo_var = new_s[exo_var_n]

            # TODO: Make set_der method
            new_exo_var.set_der(valid_der)
            all_possible_states.append(new_s)

        # 2. check the ambiguity of derivative applying
        state_li_after_applying = []

        for entity_n in self.entities:
            entity = self.entities[entity_n]
            ent_li = entity.apply_der()
            state_li_after_applying.append(ent_li)
            # if entity.derivative!=0:
            #     if entity.quantity==0:
            #         new_s = new_entities()
            #         new_s[entity_n].apply_der()
        new_entities+=list(product(state_li_after_applying))

        # TODO: Create another loop which checks for exogenous states within possible ambigutiies (other than stable)

        # 3. check the ambiguity of relations
        for entity_n in self.relation_map:
            rels = self.relation_map[entity_n]
            rels_n = {r.ty:r for r in rels}
            q_influence = []
            d_influence = []

            # {from: q1, to: q2, type: vc} , {}
            for rel_n in rels_n:
                rel = rels[rel_n]
                if rel_n == 'I+':
                    influ = self.entities[rel.fr].quantity.val * 1
                    d_influence.append(influ)
                if rel_n == 'I-':
                    influ = self.entities[rel.fr].quantity.val * -1
                    d_influence.append(influ)
                if rel_n == 'P+':
                    influ = self.entities[rel.fr].quantity.val * 1
                    q_influence.append(influ)
                if rel_n == 'P-':
                    influ = self.entities[rel.fr].quantity.val * -1
                    q_influence.append(influ)
                if rel_n == 'VC':
                    # TODO: Use entitiy instead of entity_n
                    # TODO: Check if the 'from' enttity has reached the VC value as well
                    self.entities[rel.to].quantity.val = self.entities[rel.fr].quantity.val
                    break

            # If q and d influence have conflicts, generate new states and append

if __name__ == "__main__":
    pass
