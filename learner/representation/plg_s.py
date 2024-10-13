""" Probabilistic Lifted Learning Graph Simple """
import torch
import networkx as nx
from enum import Enum
from torch import Tensor
from .planning.translate.pddl import Atom, NegatedAtom, Literal, Truth, Effect
from .base_class import Representation, LiftedState, TGraph, CGraph



# WL_colour for Edge indices, consist of:
# 0-3: pre/effs X pos/neg
# 4-6: (ap/ug/ag) 
# 7: (probabilistic action) 
# i (largest pred param size)
class PlgsEdgeLabel(Enum):
    PRE_POS = 0 #precon +
    PRE_NEG = 1 #precon -
    EFF_ADD = 2 #eff +
    EFF_DEL = 3 #eff -
    ACH_POS = 4 #achieved non goal prop
    U_GOAL = 5 # unachieved goal
    A_GOAL = 6 # achieved goal
    PROB_EFF = 7 # for probabilistic effect node

_E = len(PlgsEdgeLabel) #length counter for edge label

PROB_VAL = 0.05
NUM_PROB_BUCKETS = 21 # num of probability buckets as edges, default 0.05, total 21 
GROUND_PROP_COLOUR = 0
# WL_Colour for nodes consist of:
# ### archieved
# # 0：ground proposition node
# # [1, 21]: the probability node for partial action node
# # [22, 22 + O): the object type node
# # [22 + O, 22 + O + P): the predicate schema nodes
# # [22 + O + P, 22 + O + P + A): the action schema nodes 

# 0：ground proposition node
# [1, 1 + O): the object type node
# [1 + O, 1 + O + P): the predicate schema nodes
# [1 + O + P, 1 + O + P + A): the action schema nodes 
# [1 + O + P + A, 21 + O + P + A]: the probability node for partial action node
# however, the last 21 probability node are transformed into a single probability node in GNN
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

class ProbabilisitcLiftedLearningGraphSimple(Representation):
    name = "plg_s"
    lifted = True

    def __init__(self, domain_pddl: str, problem_pddl: str):
        self._get_problem_info(domain_pddl, problem_pddl)
        self.colour_explanation = {
            0: "grounded proposition",  # ground prop nodes
        }
        counter = 1
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
            counter += 1
        self.PROB_IDX_COUNTER = counter # counter for transfer back to color
        for i in range(NUM_PROB_BUCKETS):
            self.colour_explanation[counter] = f"probabilistic action with chance {i/(NUM_PROB_BUCKETS - 1)}" # prob nodes
            counter += 1

        super().__init__(
            domain_pddl,
            problem_pddl,
            n_node_features= 1 + self.n_obj_types + self.n_predicates + self.n_actions + 1, # the last one is for prob node in GNN
            n_edge_labels=_E + self.largest_predicate_size,
        )
        print(self.n_node_features, self.PROB_IDX_COUNTER)
        
    def edge_explanation(self, edge_label:int)->str:
        """help to print out edge label in result graph"""
        if edge_label < _E:
            return str(PlgsEdgeLabel(edge_label).name)
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
            G.add_edge(u_of_edge=goal_node, v_of_edge=pred, edge_label = PlgsEdgeLabel.U_GOAL.value) # need to be updated later


            for k, arg in enumerate(args):
                # connect fact to object
                G.add_edge(u_of_edge=goal_node, v_of_edge=arg, edge_label=_E+k)
        
        # Actions
        for action in self.actions:
            G.add_node(action.name, x = self.act_to_idx[action.name] + self.ACT_IDX_COUNTER) # add action schema node a
            # link action/pred schema together with preconditions of the action node a
            for fact in action.precondition.parts:
                pred = fact.predicate
                # args = fact.args
                if pred == "=":
                    continue
                assert pred in G.nodes(), f"Error, {pred} not in created nodes"
                if type(fact) == Atom:
                    G.add_edge(u_of_edge=pred, v_of_edge=action.name, edge_label=PlgsEdgeLabel.PRE_POS.value)
                elif type(fact) == NegatedAtom:
                    G.add_edge(u_of_edge=pred, v_of_edge=action.name, edge_label=PlgsEdgeLabel.PRE_NEG.value)
                else:
                    raise NotImplementedError("parser error in preconditions")
            
            def add_edges_effects_wrapper(act_node, effects: list[Effect]):
                ''' help function wrapper to add (probabilistic) effects'''
                def add_edges_effects(act_node, edge_label:int, facts: list[Literal]):
                    ''' help function to add (probabilistic) effects'''
                    for fact in facts:
                        pred = fact.predicate
                        assert fact.predicate in G.nodes(), f"Error, {pred} not in created nodes"
                        G.add_edge(u_of_edge=act_node, v_of_edge=pred, edge_label=edge_label)
                
                pos_effs = []
                neg_effs = []
                for p in effects:
                    if type(p.condition) != Truth:
                        raise NotImplementedError("Conditional effects not implemented")
                    if type(p.literal) == Atom:
                        pos_effs.append(p.literal)
                    elif type(p.literal) == NegatedAtom:
                        neg_effs.append(p.literal)
                    else:
                        raise NotImplementedError("parser error in effects")
                add_edges_effects(act_node, PlgsEdgeLabel.EFF_ADD.value, pos_effs)
                add_edges_effects(act_node, PlgsEdgeLabel.EFF_DEL.value, neg_effs)

            # parse action effects
            if action.is_probabilistic_action:
                for i, (prob, effects) in enumerate(action.prob_effects):
                    prob_node = (action.name, f"out-{i+1}-prob={prob}")
                    G.add_node(prob_node, x=prob_to_colour(prob)+self.PROB_IDX_COUNTER) # add probability effect node a-i
                    G.add_edge(u_of_edge=action.name, v_of_edge=prob_node, edge_label=PlgsEdgeLabel.PROB_EFF.value)
                    add_edges_effects_wrapper(prob_node, effects) # link effects with a-i
            else:
                prob_node = (action.name, f"single-out-prob=1")
                G.add_node(prob_node, x=prob_to_colour(1.0)+self.PROB_IDX_COUNTER) # add probability effect node a-0 that is the sinlge probabilistic outcome node
                G.add_edge(u_of_edge=action.name, v_of_edge=prob_node, edge_label=PlgsEdgeLabel.PROB_EFF.value)
                add_edges_effects_wrapper(prob_node, action.effects) # if normal action, link effect to the single out node
        # end goal


        # map node name to index
        self._node_to_i = {}
        for i, node in enumerate(G.nodes):
            self._node_to_i[node] = i
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
                c_graph.add_edge(u_of_edge=node, v_of_edge=pred, edge_label = PlgsEdgeLabel.A_GOAL.value) #update existing edge to achieved goal
                continue

            # else add node and corresponding edges to graph
            c_graph.add_node(node, x=GROUND_PROP_COLOUR)
            c_graph.add_edge(u_of_edge=node, v_of_edge=pred, edge_label = PlgsEdgeLabel.ACH_POS.value)

            for k, obj in enumerate(args):
                # connect fact to object
                assert obj in c_graph.nodes, f"obj {obj} not in existing nodes"
                c_graph.add_edge(u_of_edge=node, v_of_edge=obj, edge_label=_E+k)
                c_graph.add_edge(v_of_edge=node, u_of_edge=obj, edge_label=_E+k)

        return c_graph
    
    def _colour_to_tensor(self, colour: int) -> Tensor:
        ret = torch.zeros(self.n_node_features)
        if colour<self.PROB_IDX_COUNTER:
            ret[colour] = 1
        else:
            prob_colour = colour - self.PROB_IDX_COUNTER
            ret[-1] = prob_colour * PROB_VAL
        
        return ret
    

    def state_to_tgraph(self, state: LiftedState) -> TGraph:
        """Converts nx graph into pytorch_geometric tensors and stores them.
        Use a variant of convert_to_pyg to combine with state_to_cgraph and achieve computation
        no longer require an pre calling of convert_to_pyg() before training

        The tensors are (x, edge_index or edge_indices)
        x: torch.tensor(N x F)  # N = num_nodes, F = num_features
        if n_edge_labels = 1:
          edge_index: torch.tensor(2 x E)  # E = num_edges
        else:
          edge_indices: List[torch.tensor(2 x E_i)]
        """
        from torch_geometric.utils.convert import from_networkx

        G: nx.Graph = self.state_to_cgraph(state)
        for node in G.nodes:
            G.nodes[node]["x"] = self._colour_to_tensor(G.nodes[node]["x"])
        pyg_G = from_networkx(G)
        x = pyg_G.x

        if self.n_edge_labels == 1:
            edge_indices = pyg_G.edge_index
        else:
            assert self.n_edge_labels > 1
            edge_indices = [[] for _ in range(self.n_edge_labels)]
            edge_index_T = pyg_G.edge_index.T
            for i, edge_label in enumerate(pyg_G.edge_label):
                edge_indices[edge_label].append(edge_index_T[i])
            for i in range(self.n_edge_labels):
                if len(edge_indices[i]) > 0:
                    edge_indices[i] = (
                        torch.vstack(edge_indices[i]).long().T
                    )
                else:
                    edge_indices[i] = torch.tensor([[], []]).long()
        return x, edge_indices
    
    
