# utilities.py

import numpy as np

def calculate_distance(x1, y1, x2, y2):
    """
    Calculates the Euclidean distance between two points.

    Args:
    - x1, y1: Coordinates of the first point.
    - x2, y2: Coordinates of the second point.

    Returns:
    - distance (float): The Euclidean distance between the two points.
    """
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def do_intersect(p1, q1, p2, q2):
    """
    Checks if two line segments (p1, q1) and (p2, q2) intersect.

    Args:
    - p1, q1: Endpoints of the first line segment.
    - p2, q2: Endpoints of the second line segment.

    Returns:
    - (bool): True if the line segments intersect, False otherwise.
    """
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # colinear
        return 1 if val > 0 else 2  # clock or counterclockwise

    def on_segment(p, q, r):
        if (q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1])):
            return True
        return False

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(p1, p2, q1): return True
    if o2 == 0 and on_segment(p1, q2, q1): return True
    if o3 == 0 and on_segment(p2, p1, q2): return True
    if o4 == 0 and on_segment(p2, q1, q2): return True

    return False

def generate_random_connectivity(num_turbines, num_cable_types):
    """
    Generates a random connectivity matrix for a given number of turbines and cable types.

    Args:
    - num_turbines (int): Number of turbines in the wind farm.
    - num_cable_types (int): Number of different types of cables.

    Returns:
    - connectivity (numpy.ndarray): A randomly generated connectivity matrix.
    """
    connectivity = np.zeros((num_turbines + 1, num_turbines + 1), dtype=int)
    for i in range(num_turbines):
        # Randomly decide to connect with the substation or other turbines
        if np.random.choice([True, False]):
            connectivity[i, num_turbines] = np.random.choice(range(1, num_cable_types + 1))
        else:
            for j in range(num_turbines):
                if i != j and np.random.choice([True, False]):
                    connectivity[i, j] = np.random.choice(range(1, num_cable_types + 1))
    return connectivity

