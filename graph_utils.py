# graph_utils.py

import networkx as nx
import numpy as np

def create_graph_from_matrix(connectivity_matrix):
    """
    Creates a directed graph from a connectivity matrix.

    Args:
    - connectivity_matrix (numpy.ndarray): A square matrix where a non-zero element
      indicates a directed edge from the row index to the column index.

    Returns:
    - G (networkx.DiGraph): A directed graph created from the connectivity matrix.
    """
    num_nodes = connectivity_matrix.shape[0]
    G = nx.DiGraph()
    G.add_nodes_from(range(num_nodes))

    for i in range(num_nodes):
        for j in range(num_nodes):
            if connectivity_matrix[i, j] != 0:
                G.add_edge(i, j)

    return G

def check_loops(connectivity_matrix):
    """
    Checks for the presence of loops in a graph represented by a connectivity matrix.

    Args:
    - connectivity_matrix (numpy.ndarray): Connectivity matrix of the graph.

    Returns:
    - (bool): False if there are loops in the graph, True otherwise.
    """
    G = create_graph_from_matrix(connectivity_matrix)
    try:
        nx.find_cycle(G, orientation='original')
        return False  # Cycle found
    except nx.NetworkXNoCycle:
        return True  # No cycle

def check_connectivity_to_substation(connectivity_matrix, substation_index):
    """
    Verifies if every node in the graph is connected to the substation.

    Args:
    - connectivity_matrix (numpy.ndarray): Connectivity matrix of the graph.
    - substation_index (int): Index of the substation node in the graph.

    Returns:
    - (bool): True if all nodes are connected to the substation, False otherwise.
    """
    G = create_graph_from_matrix(connectivity_matrix)

    # Ensure the substation node is in the graph
    if substation_index not in G:
        return False

    for node in G.nodes():
        if node != substation_index and not nx.has_path(G, node, substation_index):
            return False

    return True

