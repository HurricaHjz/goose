from representation.base_class import *
from representation.slg import StripsLearningGraph


class DLG_FEATURES(Enum):
  ACTION=0
  POSITIVE_GOAL=1
  NEGATIVE_GOAL=2
  STATE=3

class DLG_EDGE_TYPES(Enum):
  PRE_EDGE=0
  ADD_EDGE=1


class DeleteLearningGraph(StripsLearningGraph, ABC):

  @property
  def name(self):
    return "dlg"

  @property
  def n_node_features(self):
    return len(DLG_FEATURES)

  @property
  def n_edge_labels(self):
    return len(DLG_EDGE_TYPES)

  @property
  def directed(self):
    return False

  @property
  def lifted(self):
    return False

  def __init__(self, domain_pddl: str, problem_pddl: str):
    super().__init__(domain_pddl, problem_pddl)

  def _compute_graph_representation(self) -> None:
    """ TODO: reference definition of this graph representation
    """

    G = self._create_graph()

    propositions, actions, positive_goals, negative_goals, _ = self._get_grounded_problem_info()

    """ nodes """
    for proposition in propositions:
      node_p = self._proposition_to_str(proposition)
      # these features may get updated in state encoding
      if proposition in positive_goals:
        x_p = self._one_hot_node(DLG_FEATURES.POSITIVE_GOAL.value)
      elif proposition in negative_goals:
        x_p = self._one_hot_node(DLG_FEATURES.NEGATIVE_GOAL.value)
      else:
        x_p = self._zero_node()
      G.add_node(node_p, x=x_p)

    for action in actions:
      node_a = action.name
      x_a = self._one_hot_node(DLG_FEATURES.ACTION.value)
      G.add_node(node_a, x=x_a)

    """ edges """
    for action in actions:
      a_node = action.name
      for proposition in action.precondition:
        p_node = self._proposition_to_str(proposition)
        assert p_node in G.nodes, f"{p_node} not in nodes"
        assert a_node in G.nodes, f"{a_node} not in nodes"
        G.add_edge(u_of_edge=p_node, v_of_edge=a_node, edge_type=DLG_EDGE_TYPES.PRE_EDGE.value)
      for _, proposition in action.add_effects:  # ignoring conditional effects
        p_node = self._proposition_to_str(proposition)
        assert p_node in G.nodes, f"{p_node} not in nodes"
        assert a_node in G.nodes, f"{a_node} not in nodes"
        G.add_edge(u_of_edge=p_node, v_of_edge=a_node, edge_type=DLG_EDGE_TYPES.ADD_EDGE.value)

      """ Delete relaxation means ignoring delete edges """
      # for _, proposition in action.del_effects:  # ignoring conditional effects
      #   p_node = self._proposition_to_str(proposition)
      #   assert p_node in G.nodes, f"{p_node} not in nodes"
      #   assert a_node in G.nodes, f"{a_node} not in nodes"
      #   G.add_edge(u_of_edge=p_node, v_of_edge=a_node, edge_type=SDG_EDGE_TYPES.DEL_EDGE.value)

    # map node names to tensor indices; only do this for propositions
    self._node_to_i = {}
    for i, node in enumerate(G.nodes):
      if G.nodes[node]['x'][DLG_FEATURES.ACTION.value] == 1:
        continue
      self._node_to_i[node] = i

    # convert to PyG tensors
    self._graph_to_representation(G)

    return

  def get_state_enc(self, state: State) -> Tuple[Tensor, Tensor]:

    x = self.x.clone()  # not time nor memory efficient, but no other way in Python
    for p in state:
      if p in self._node_to_i:
        x[self._node_to_i[p]][DLG_FEATURES.STATE.value] = 1

    return x, self.edge_indices
