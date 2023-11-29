from optimization import genetic_algorithm
from load_data import load_data

def main():
    # Load data
    X, Y, substation_pos, cable_costs, turbines_per_cable = load_data()

    # Parameters for the genetic algorithm
    population_size = 50  # Adjust as needed
    num_generations = 100  # Adjust as needed

    # Run the optimization
    best_solution, best_fitness = genetic_algorithm(
        X, Y, substation_pos, cable_costs, turbines_per_cable, 
        population_size, num_generations
    )

    print("Best Solution:", best_solution)
    print("Best Fitness:", best_fitness)

if __name__ == "__main__":
    main()

