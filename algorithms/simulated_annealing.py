import math
import random
import pandas as pd

from helpers.tsp_functions import TSPFunctions


class SimulatedAnnealing:
    def __init__(self):
        self.tsp_functions = TSPFunctions()

    def tsp_simulated_annealing_linear_cooling(
        self,
        tsp: pd.DataFrame,
        max_objective_calls: int,
        acceptance_prob: float = 1.0,
    ):
        current_solution = self.tsp_functions.random_solution(tsp)
        current_fitness = self.tsp_functions.calculate_cost(tsp, current_solution)
        # each iteration is an objective function call
        max_iterations = max_objective_calls
        iteration = 1

        best_solution = current_solution
        best_fitness = current_fitness

        iteration_list = []
        best_distances = []
        distance_list = []

        while iteration < max_iterations:
            new_solution = self.tsp_functions.generate_neighbor(current_solution)
            new_fitness = self.tsp_functions.calculate_cost(tsp, new_solution)
            iteration += 1

            # Linearly reduce acceptance probability to 0 after 90% iterations
            acceptance_prob = max(0.0, 1.0 - (iteration / (0.9 * max_iterations)))

            if new_fitness < current_fitness:
                current_solution = new_solution
                current_fitness = new_fitness
            elif random.random() < acceptance_prob:
                current_solution = new_solution
                current_fitness = new_fitness

            if new_fitness < best_fitness:
                best_solution = new_solution
                best_fitness = new_fitness

            iteration_list += [iteration]
            best_distances += [best_fitness]
            distance_list += [current_fitness]

        return (
            best_fitness,
            best_solution,
            iteration_list,
            distance_list,
            best_distances,
        )

    def tsp_simulated_annealing_classic(
        self, tsp, initial_temperature=1000.0, cooling_rate=0.997
    ):
        current_solution = self.tsp_functions.random_solution(tsp)
        current_fitness = self.tsp_functions.calculate_cost(tsp, current_solution)

        best_solution = current_solution
        best_fitness = current_fitness

        temperature = initial_temperature

        while temperature > 0.1:
            new_solution = self.tsp_functions.generate_neighbor(current_solution)
            new_fitness = self.tsp_functions.calculate_cost(tsp, new_solution)

            acceptance_prob = self._acceptance_probability(
                current_fitness, new_fitness, temperature
            )

            if random.random() < acceptance_prob:
                current_solution = new_solution
                current_fitness = new_fitness

            if new_fitness < best_fitness:
                best_solution = new_solution
                best_fitness = new_fitness

            temperature *= cooling_rate

        return best_fitness, best_solution

    # for simulated annealing classic
    def _acceptance_probability(self, current_distance, new_distance, temperature):
        if new_distance < current_distance:  # melhor == menor (<)
            return 1.0
        return math.exp((current_distance - new_distance) / temperature)
