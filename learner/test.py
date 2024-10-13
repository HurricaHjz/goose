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

# Example usage
if __name__ == "__main__":
    # Create an example TGraph
    x = torch.tensor([[1, 0], [0, 1], [1, 1]])  # Node features (3 nodes, 2 features each)
    edge_indices = [
        torch.tensor([[0, 1], [1, 2]]),  # Label 0 edges
        torch.tensor([[2, 0], [1, 0]])   # Label 1 edges
    ]
    tgraph = (x, edge_indices)
    
    # Print the TGraph
    print_tgraph(tgraph)
