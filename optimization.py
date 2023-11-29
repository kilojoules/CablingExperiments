# optimization.py

import numpy as np
from constraints import check_capacity_constraint, check_non_crossing_constraint, check_connectivity_to_substation
from utilities import calculate_distance, generate_random_connectivity

def calculate_total_cost(connectivity, X, Y, substation_pos, cable_costs):
    """
    Calculates the total cost of the wind farm layout based on the connectivity matrix.

    Args:
    - connectivity (numpy.ndarray): Connectivity matrix representing the network.
    - X, Y (list[float]): Coordinates of the turbines.
    - substation_pos (list[float]): Coordinates of the substation.
    - cable_costs (list[float]): Cost per unit length for each type of cable.

    Returns:
    - cost (float): Total cost of the layout.
    """
    cost = 0
    num_turbines = len(X)

    for i in range(num_turbines):
        for j in range(num_turbines + 1):  # Including the substation
            cable_type = connectivity[i, j]
            if cable_type > 0:
                if j == num_turbines:  # Connection to substation
                    dist = calculate_distance(X[i], Y[i], substation_pos[0], substation_pos[1])
                else:  # Connection to another turbine
                    dist = calculate_distance(X[i], Y[i], X[j], Y[j])
                cost += dist * cable_costs[cable_type - 1]

    return cost

def generate_initial_population(pop_size, num_turbines, num_cable_types):
    """
    Generates an initial population for the GA.

    Args:
    - pop_size (int): Size of the population.
    - num_turbines (int): Number of turbines.
    - num_cable_types (int): Number of cable types.

    Returns:
    - population (list[numpy.ndarray]): List of connectivity matrices.
    """
    return [generate_random_connectivity(num_turbines, num_cable_types) for _ in range(pop_size)]

def fitness_function(connectivity, X, Y, substation_pos, cable_costs, turbines_per_cable):
    """
    Fitness function for evaluating the quality of a solution.

    Args:
    - connectivity, X, Y, substation_pos, cable_costs, turbines_per_cable: Parameters needed for cost calculation and constraint checking.

    Returns:
    - fitness (float): The fitness of the solution, lower is better.
    """
    if not check_capacity_constraint(connectivity, turbines_per_cable) or \
       not check_non_crossing_constraint(connectivity, X, Y) or \
       not check_connectivity_to_substation(connectivity, len(X)):
        return float('inf')  # Invalid solution

    return calculate_total_cost(connectivity, X, Y, substation_pos, cable_costs)

def genetic_algorithm(X, Y, substation_pos, cable_costs, turbines_per_cable, pop_size, num_generations):
    """
    Genetic Algorithm for optimizing the wind farm layout.

    Args:
    - X, Y, substation_pos, cable_costs, turbines_per_cable: Parameters for the wind farm.
    - pop_size (int): Size of the population.
    - num_generations (int): Number of generations for the GA to run.

    Returns:
    - best_solution (numpy.ndarray): The best solution found.
    - best_fitness (float): Fitness of the best solution.
    """
    num_turbines = len(X)
    num_cable_types = len(cable_costs)

    # Generate initial population
    population = generate_initial_population(pop_size, num_turbines, num_cable_types)

    best_solution = None
    best_fitness = float('inf')

    for generation in range(num_generations):
        # Evaluate fitness
        fitness_scores = [fitness_function(individual, X, Y, substation_pos, cable_costs, turbines_per_cable) for individual in population]

        # Selection, crossover, and mutation steps go here
        # ...

        # Update best solution
        for i, fitness in enumerate(fitness_scores):
            if fitness < best_fitness:
                best_fitness = fitness
                best_solution = population[i]

    return best_solution, best_fitness

# Example usage
# X, Y, substation_pos, cable_costs, turbines_per_cable = ...
# best_solution, best_fitness = genetic_algorithm(X, Y, substation_pos, cable_costs, turbines_per_cable, 50, 100)

