# constraints.py

import numpy as np
from utilities import do_intersect, calculate_distance

def check_capacity_constraint(connectivity, turbines_per_cable):
    """
    Checks if the capacity constraint is met for each cable.

    Args:
    - connectivity (numpy.ndarray): Connectivity matrix representing the network.
    - turbines_per_cable (list[int]): Maximum number of turbines that can be connected per cable type.

    Returns:
    - (bool): True if the capacity constraint is satisfied for all cables, False otherwise.
    """
    num_turbines = connectivity.shape[0] - 1  # Excluding the substation node
    for i in range(num_turbines):
        if sum(connectivity[i, :]) > turbines_per_cable[-1]:
            return False
    return True

def check_non_crossing_constraint(connectivity, X, Y):
    """
    Ensures that no cables cross each other.

    Args:
    - connectivity (numpy.ndarray): Connectivity matrix of the wind farm.
    - X (list[float]): X-coordinates of the turbines.
    - Y (list[float]): Y-coordinates of the turbines.

    Returns:
    - (bool): True if no cables cross each other, False otherwise.
    """
    num_turbines = len(X)
    for i in range(num_turbines):
        for j in range(i + 1, num_turbines):
            if connectivity[i, j] != 0:
                for k in range(num_turbines):
                    for l in range(k + 1, num_turbines):
                        if connectivity[k, l] != 0 and {i, j} != {k, l}:
                            if do_intersect((X[i], Y[i]), (X[j], Y[j]), (X[k], Y[k]), (X[l], Y[l])):
                                return False
    return True

def check_connectivity_to_substation(connectivity, substation_index):
    """
    Verifies if every node in the graph is connected to the substation.

    Args:
    - connectivity (numpy.ndarray): Connectivity matrix of the graph.
    - substation_index (int): Index of the substation node in the graph.

    Returns:
    - (bool): True if all nodes are connected to the substation, False otherwise.
    """
    # Assuming the last node is the substation
    num_turbines = connectivity.shape[0] - 1

    for i in range(num_turbines):
        if not np.any(connectivity[i, substation_index]) and not np.any(connectivity[substation_index, i]):
            return False

    return True

