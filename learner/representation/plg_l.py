""" Probabilistic Lifted Learning Graph Simple """
import torch
import copy
from collections import defaultdict
from enum import Enum
from torch import Tensor
from .planning.translate.pddl import Atom, NegatedAtom, Literal, Truth, Effect
from .base_class import Representation, LiftedState, TGraph, CGraph



# WL_colour for Edge indices, consist of:
# 0-3: pre/effs X pos/neg
# 4-6: (ap/ug/ag) 
# 7: (probabilistic action) 
# i (max of the largest pred param/action param size)
class PlglEdgeLabel(Enum):
    PRE_POS = 0 #precon +
    PRE_NEG = 1 #precon -
    EFF_ADD = 2 #eff +
    EFF_DEL = 3 #eff -
    ACH_POS = 4 #achieved non goal prop
    U_GOAL = 5 # unachieved goal
    A_GOAL = 6 # achieved goal
    PROB_EFF = 7 # for probabilistic effect node

_E = len(PlglEdgeLabel) #length counter for edge label

NUM_PROB_BUCKETS = 21 # num of probability buckets as edges, default 0.05, total 21 
GROUND_PROP_COLOUR = 0
SCHEMA_PRECDIATE_COLOUR = 1
# WL_Colour for nodes consist of:
# 0：ground proposition node
# 1: lifted predicate node (used for predicate schema to connect action)
# [2, 22]: the probability node for partial action node
# [23, 23 + O): the object type node
# [23 + O, 23 + O + P): the predicate schema nodes
# [23 + O + P, 23 + O + P + A): the action schema nodes 
def prob_to_colour(probability:float) -> int:
    """ transfer probability node to colour index
    """
    # Ensure the probability is within the expected range
    if not (0 <= probability <= 1):
        raise ValueError("Probability must be between 0 and 1.")
    
    p = NUM_PROB_BUCKETS - 1 # devision should be 1 less than total num of buckets

    # Scale the probability to range 0-20 and round to the nearest integer
    bucket = round(probability * p)
    
    # Ensure the bucket is between 0 and 20 (in case of rounding errors or float precision)
    return max(0, min(bucket, p))

class ProbabilisitcLiftedLearningGraphLarge(Representation):
    name = "plg_l"
    lifted = True

    def __init__(self, domain_pddl: str, problem_pddl: str):
        self._get_problem_info(domain_pddl, problem_pddl)
        self.colour_explanation = {
            0: "grounded proposition",  # ground prop nodes
            1: "schema predicate"
        }
        counter = 2
        self.PROB_IDX_COUNTER = counter # counter for transfer back to color for probability
        for i in range(NUM_PROB_BUCKETS):
            self.colour_explanation[counter] = f"probabilistic action with chance {i/(NUM_PROB_BUCKETS - 1)}" # prob nodes
            counter += 1
        self.TYPE_IDX_COUNTER = counter
        for i in range(self.n_obj_types):
            self.colour_explanation[counter] = f"object type: {self.obj_types[i]}"
            counter += 1
        self.PRED_IDX_COUNTER = counter    
        for i in range(self.n_predicates):
            self.colour_explanation[counter] = f"predicate schema: {self.predicates[i].name}"
            counter += 1
        self.ACT_IDX_COUNTER = counter     
        for i in range(self.n_actions):
            self.colour_explanation[counter] = f"action schema: {self.actions[i].name}"
            # counter += 1

        super().__init__(
            domain_pddl,
            problem_pddl,
            n_node_features= 2 + NUM_PROB_BUCKETS + self.n_obj_types + self.n_predicates + self.n_actions,
            n_edge_labels=_E + max(self.largest_action_size, self.largest_predicate_size),
        )
        
    def edge_explanation(self, edge_label:int)->str:
        """help to print out edge label in result graph"""
        if edge_label < _E:
            return str(PlglEdgeLabel(edge_label).name)
        else:
            return f"Arg-{edge_label-_E+1}"

    def str_to_state(self, s) -> LiftedState:
        # this function takes input s as a list of facts for example: "(clear b1)" -- type: <class 'str'>
        """Used in dataset construction to convert string representation of facts into a (pred, [args]) representation"""
        state = []
        for fact in s:
            fact = fact.replace(")", "").replace("(", "")
            toks = fact.split()
            if toks[0] == "=":
                continue
            if len(toks) > 1:
                state.append((toks[0], toks[1:]))
            else:
                state.append((toks[0], ()))
        return state
    


    def _compute_graph_representation(self) -> None:
        G = self._init_graph() #undirected graph

        # objects
        for obj in self.problem.objects:
            G.add_node(obj.name, x=self.type_to_idx[obj.type_name]+self.TYPE_IDX_COUNTER)  # add object node
        
        # predicates
        for pred in self.predicates:
            G.add_node(pred.name, x=self.pred_to_idx[pred.name]+self.PRED_IDX_COUNTER) # add predicate schema node
        
        
        # goal (state gets dealt with in state_to_tgraph)
        if len(self.problem.goal.parts) == 0:
            goals = [self.problem.goal]
        else:
            goals = self.problem.goal.parts
        for fact in sorted(goals):
            assert type(fact) in {Atom, NegatedAtom}

            # may have negative goals
            if type(fact) == NegatedAtom:
                raise NotImplementedError

            pred = fact.predicate
            args = fact.args
            goal_node = (pred, args)

            G.add_node(goal_node, x=GROUND_PROP_COLOUR)  # add fact node as un achieved goal yet
            self._pos_goal_nodes.add(goal_node)
            G.add_edge(u_of_edge=goal_node, v_of_edge=pred, edge_label = PlglEdgeLabel.U_GOAL.value) # need to be updated later


            for k, arg in enumerate(args):
                # connect fact proposition to object
                G.add_edge(u_of_edge=goal_node, v_of_edge=arg, edge_label=_E+k)
        
        # Actions
        for action in self.actions:
            G.add_node(action.name, x = self.act_to_idx[action.name] + self.ACT_IDX_COUNTER) # add action schema node A
            # map each action arg to a tuple of corresponding (arg_index, precondition schema node), ?x : [(0, p_1(?x)), (1, p_2(?y, ?x))] 
            action_arg_to_pre = defaultdict(list) # args dictionary to preconditions
        
            # link action/pred schema together with preconditions of the action node a
            for fact in action.precondition.parts:
                pred = fact.predicate
                args = fact.args
                if pred == "=":
                    continue
                assert pred in G.nodes(), f"Error, {pred} not in created nodes"

                if type(fact) == Atom:
                    schema_node = (pred, "PRE_POS")
                    G.add_node(schema_node, x = SCHEMA_PRECDIATE_COLOUR) # add precondition node, nx.Graph automatically delete duplicates
                    G.add_edge(u_of_edge=schema_node, v_of_edge=action.name, edge_label=PlglEdgeLabel.PRE_POS.value)
                    G.add_edge(u_of_edge=schema_node, v_of_edge=pred, edge_label=PlglEdgeLabel.PRE_POS.value) # link precondiiton schema node to action
                    for k, arg in enumerate(args):
                        action_arg_to_pre[arg].append((k, schema_node)) # append (0, p_1()+) to act_to_pre+[?x] for pre: p_1(?x)

                elif type(fact) == NegatedAtom:
                    schema_node = (pred, "PRE_NEG")
                    G.add_node(schema_node, x = SCHEMA_PRECDIATE_COLOUR) # add precondition node
                    G.add_edge(u_of_edge=schema_node, v_of_edge=action.name, edge_label=PlglEdgeLabel.PRE_NEG.value) # link precondiiton schema node to action
                    G.add_edge(u_of_edge=schema_node, v_of_edge=pred, edge_label=PlglEdgeLabel.PRE_NEG.value)
                    for k, arg in enumerate(args):
                        action_arg_to_pre[arg].append((k, schema_node)) # append (0, p_1()-) to act_to_pre-[?x] for pre: -p_1(?x)
                else:
                    raise NotImplementedError("parser error in preconditions")
            
            def add_edges_effects_wrapper(act_node, effects: list[Effect]):
                ''' help function wrapper to add (probabilistic) effects'''
                # store and add effects to a-i node
                action_arg_to_eff = defaultdict(list) # action args to effects
                for p in effects:
                    if type(p.condition) != Truth:
                        raise NotImplementedError("Conditional effects not implemented")
                    if type(p.literal) == Atom:
                        pred = p.literal.predicate
                        args = p.literal.args
                        assert pred in G.nodes(), f"Error, {pred} not in created nodes"
                        schema_node = (pred, "EFF_ADD")
                        G.add_node(schema_node, x = SCHEMA_PRECDIATE_COLOUR) # add positive effect node, nx.Graph automatically delete duplicates
                        G.add_edge(u_of_edge=schema_node, v_of_edge=act_node, edge_label=PlglEdgeLabel.EFF_ADD.value) 
                        G.add_edge(u_of_edge=schema_node, v_of_edge=pred, edge_label=PlglEdgeLabel.EFF_ADD.value) # link effect schema node to action effect node
                        for k, arg in enumerate(args):
                            action_arg_to_eff[arg].append((k, schema_node)) # append (0, p_1()+) to act_to_pre+[?x] for eff: p_1(?x)
                    elif type(p.literal) == NegatedAtom:
                        pred = p.literal.predicate
                        args = p.literal.args
                        assert pred in G.nodes(), f"Error, {pred} not in created nodes"
                        schema_node = (pred, "EFF_DEL")
                        G.add_node(schema_node, x = SCHEMA_PRECDIATE_COLOUR) # add negative effect node, nx.Graph automatically delete duplicates
                        G.add_edge(u_of_edge=schema_node, v_of_edge=act_node, edge_label=PlglEdgeLabel.EFF_DEL.value) 
                        G.add_edge(u_of_edge=schema_node, v_of_edge=pred, edge_label=PlglEdgeLabel.EFF_DEL.value) # link effect schema node to action effect node
                        for k, arg in enumerate(args):
                            action_arg_to_eff[arg].append((k, schema_node)) # append (0, p_1()+) to act_to_pre+[?x] for eff: p_1(?x)
                    else:
                        raise NotImplementedError("parser error in effects")
                # loop for all action parameters
                for k, arg in enumerate(action.parameters): #here arg is TypedObj with .name and .type_name
                    arg_node = (act_node, arg.name) # create a-i.?x
                    G.add_node(arg_node, x = self.type_to_idx[arg.type_name] + self.TYPE_IDX_COUNTER) # ?x - block has the node feature as b1 - block
                    G.add_edge(u_of_edge=arg_node, v_of_edge=act_node, edge_label=_E + k) # link ?x to a-i with edge label being index k
                    for j, pre_node in action_arg_to_pre[arg.name]:
                        G.add_edge(u_of_edge=pre_node, v_of_edge=arg_node, edge_label=_E + j) # link ?x to corresponding effects/preconditions as stored earlier
                    for j, eff_node in action_arg_to_eff[arg.name]:
                        G.add_edge(u_of_edge=eff_node, v_of_edge=arg_node, edge_label=_E + j) # link ?x to corresponding effects/preconditions as stored earlier

            # parse action effects
            if action.is_probabilistic_action:
                for i, (prob, effects) in enumerate(action.prob_effects):
                    prob_node = (action.name, f"out-{i+1}-prob={prob}")
                    G.add_node(prob_node, x=prob_to_colour(prob)+self.PROB_IDX_COUNTER) # add probability effect node a-i
                    G.add_edge(u_of_edge=action.name, v_of_edge=prob_node, edge_label=PlglEdgeLabel.PROB_EFF.value)
                    add_edges_effects_wrapper(prob_node, effects) # link effects with a-i
            else:
                prob_node = (action.name, f"single-out-prob=1")
                G.add_node(prob_node, x=prob_to_colour(1.0)+self.PROB_IDX_COUNTER) # add probability effect node a-0 that is the sinlge probabilistic outcome node
                G.add_edge(u_of_edge=action.name, v_of_edge=prob_node, edge_label=PlglEdgeLabel.PROB_EFF.value)
                add_edges_effects_wrapper(prob_node, action.effects) # if normal action, link effect to the single out node
                

        # # end goal
        # # map node name to index
        # self._node_to_i = {}
        # for i, node in enumerate(G.nodes):
        #     self._node_to_i[node] = i
        self.G = G

        return

    
    
    def state_to_cgraph(self, state: LiftedState) -> CGraph:
        """States are represented as a list of (pred, [args])"""
        c_graph = self.G.copy()
        
        for fact in state:
            pred = fact[0]
            args = fact[1]

            if len(pred) == 0:
                continue

            node = (pred, tuple(args))

            # activated proposition overlaps with a goal Atom
            if node in self._pos_goal_nodes:
                c_graph.add_edge(u_of_edge=node, v_of_edge=pred, edge_label = PlglEdgeLabel.A_GOAL.value) #update existing edge to achieved goal
                continue

            # else add node and corresponding edges to graph
            c_graph.add_node(node, x=GROUND_PROP_COLOUR)
            c_graph.add_edge(u_of_edge=node, v_of_edge=pred, edge_label = PlglEdgeLabel.ACH_POS.value)

            for k, obj in enumerate(args):
                # connect fact to object
                assert obj in c_graph.nodes, f"obj {obj} not in existing nodes"
                c_graph.add_edge(u_of_edge=node, v_of_edge=obj, edge_label=_E +k)
                c_graph.add_edge(v_of_edge=node, u_of_edge=obj, edge_label=_E +k)

        return c_graph
    
    def _colour_to_tensor(self, colour: int) -> Tensor:
        return self._one_hot_node(colour)
    

    def state_to_tgraph(self, state: LiftedState) -> TGraph:
        """States are represented as a list of (pred, [args])"""
        return None
        # x = self.x.clone()
        # edge_indices = self.edge_indices.copy()
        # i = len(x)

        # to_add = sum(len(fact[1]) + 1 for fact in state)
        # x = torch.nn.functional.pad(x, (0, 0, 0, to_add), "constant", 0)
        # new_edges = {i: [] for i in range(-1, self.largest_predicate_size)}

        # for fact in state:
        #     pred = fact[0]
        #     args = fact[1]

        #     if len(pred) == 0:
        #         continue

        #     colour_start = 1 + _F * self.pred_to_idx[pred]

        #     if len(pred) == 0:
        #         continue

        #     node = (pred, tuple(args))

        #     # activated proposition overlaps with a goal
        #     if node in self._node_to_i:
        #         col = colour_start + WlColours.T_POS_GOAL.value
        #         x[self._node_to_i[node]][col] = 1
        #         continue

        #     # activated proposition does not overlap with a goal
        #     col = colour_start + WlColours.T_NON_GOAL.value
        #     x[i][col] = 1

        #     true_node_i = i
        #     i += 1

        #     # connect fact to objects
        #     for k, arg in enumerate(args):
        #         new_edges[k].append((true_node_i, self._node_to_i[arg]))
        #         new_edges[k].append((self._node_to_i[arg], true_node_i))

        # for i, new_edges in new_edges.items():
        #     edge_indices[i] = torch.hstack(
        #         (edge_indices[i], torch.tensor(new_edges).T)
        #     ).long()

        # return x, edge_indices
    
    
