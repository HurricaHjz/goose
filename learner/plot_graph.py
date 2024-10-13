from representation import plg_s, llg, ilg, plg_l
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os
import torch
from typing import Tuple, List, Union

TGraph = Union[Tuple[torch.Tensor, torch.Tensor], Tuple[torch.Tensor, List[torch.Tensor]]]

def print_tgraph(tgraph: TGraph) -> None:
    """
    Helper function to print the TGraph in a readable format.
    The TGraph is assumed to be in the format Tuple[Tensor, List[Tensor]],
    where the first Tensor represents node features and the List[Tensor] represents edges.
    """
    x, edge_indices = tgraph
    
    # Check if edge_indices is a list of tensors
    if not isinstance(edge_indices, list):
        print("Error: edge_indices should be a list of tensors.")
        return
    
    # Print nodes and their features
    print("Nodes and their features:")
    for idx, features in enumerate(x):
        print(f"  Node {idx}: Features = {features.tolist()}")
    
    # Print edges for each label
    print("\nEdges by label:")
    for label_idx, edge_tensor in enumerate(edge_indices):
        if edge_tensor.numel() == 0:
            print(f"  Label {label_idx}: No edges")
            continue

        print(f"  Label {label_idx}: Edges =")
        for edge in edge_tensor.T:
            u, v = edge.tolist()
            print(f"    ({u}, {v})")

if __name__ == "__main__":
        domain_filename= "/home/moss/COMP4550/goose/benchmarks/mcmp/test/test_domain.pddl"
        task_filename="/home/moss/COMP4550/goose/benchmarks/mcmp/test/test_task.pddl"
        # prob = plg_s.ProbabilisitcLiftedLearningGraphSimple(domain_filename, task_filename)
        prob = plg_l.ProbabilisitcLiftedLearningGraphLarge(domain_filename, task_filename)
        # prob = ilg.InstanceLearningGraph(domain_filename, task_filename)
        initial_state = prob.str_to_state(["(p3 a b)","(p3 b c)","(p1 a)","(p2 b)","(p4)"])
        G = prob.state_to_cgraph(initial_state)
        print_tgraph(prob.state_to_tgraph(initial_state))

        
        # G = prob.G

        
        # domain_filename= "/home/moss/COMP4550/goose/benchmarks/mcmp/exbw.domain_det.NO-COND.pddl"
        # task_filename="/home/moss/COMP4550/goose/benchmarks/mcmp/tasks_exbw/exbw_p01-n2-N5-s1.pddl"
        # prob = llg.LiftedLearningGraph(domain_filename, task_filename)
        # G = prob.G.copy()

        # Define positions for the nodes
        pos = nx.shell_layout(G)

        # Generate a unique color map for each unique value of "x" attribute
        unique_x_values = list(set(nx.get_node_attributes(G, 'x').values()))
        colors = list(mcolors.TABLEAU_COLORS)  # Use built-in Tableau colors
        color_map = {value: colors[i % len(colors)] for i, value in enumerate(unique_x_values)}

        # Assign colors to nodes based on the "x" attribute
        node_colors = [color_map[G.nodes[node]['x']] for node in G.nodes]

        # Draw the graph with custom node colors and display original node IDs as labels
        # nx.draw(G, pos, with_labels=True, labels={node: str(node) for node in G.nodes}, node_color=node_colors, edge_color='gray', font_size=6)
        nx.draw(G, pos, with_labels=True, labels={node: G.nodes[node]['x'] for node in G.nodes}, node_size=2000, node_color=node_colors, edge_color='gray', font_size=12, font_weight='bold')
        
        # edge_labels = {(u, v): G[u][v]["edge_label"] for u, v in G.edges}
        edge_labels = {(u, v): prob.edge_explanation(G[u][v]["edge_label"]) for u, v in G.edges}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=6)

        # Show the plot
        plt.title('Graph with Nodes Colored by "x" Attribute and Original Node IDs as Labels')
        save_directory = "/home/moss/COMP4550/goose/benchmarks/mcmp/test"
        os.makedirs(save_directory, exist_ok=True)  # Create the directory if it doesn't exist

        # Save the figure in the specified directory with a custom filename
        save_path = os.path.join(save_directory, "sample_plot.png")
        plt.savefig(save_path)