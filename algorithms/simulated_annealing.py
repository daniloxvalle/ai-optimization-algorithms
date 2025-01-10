import math
import random
from helpers.tsp_functions import TSPFunctions


class SimulatedAnnealing:
    def __init__(self):
        self.tsp_functions = TSPFunctions()

    def tsp_simulated_annealing(
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

    # for simulated annealing
    def _acceptance_probability(self, current_distance, new_distance, temperature):
        if new_distance < current_distance:  # melhor == menor (<)
            return 1.0
        return math.exp((current_distance - new_distance) / temperature)
