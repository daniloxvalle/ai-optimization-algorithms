from typing import List, Tuple
import random
import pandas as pd

from helpers.tsp_functions import TSPFunctions


class GeneticAlgorithm:
    def __init__(self):
        self.tsp_functions = TSPFunctions()
        self.population_size = 200
        self.elite_percentage = 0.2
        self.mutation_prob = 0.2

    # def tsp_genetic_algorithm(self, tsp, max_generations: int):
    def tsp_genetic_algorithm(self, tsp, max_objective_calls: int):
        population = self._generate_initial_population(tsp)
        elite_count = int(self.population_size * self.elite_percentage)
        # If odd, increment by 1 to make even
        if elite_count % 2 != 0:
            elite_count += 1

        objective_calls = 0
        iteration_list = []
        best_distances = []

        while objective_calls < max_objective_calls:
            cost_tuples = self._generate_cost_tuples(tsp, population)

            objective_calls += self.population_size

            # Keep best individuals (elitism)
            sorted_cost_tuples = sorted(cost_tuples, key=lambda x: x[0])
            elites = sorted_cost_tuples[:elite_count]

            new_population = []
            for _ in range(self.population_size // 2 - elite_count // 2):
                parent_1 = self._tournament_selection(cost_tuples)
                remaining_cost_tuple = [ct for ct in cost_tuples if ct != parent_1]
                parent_2 = self._tournament_selection(remaining_cost_tuple)

                child_1, child_2 = self._order_crossover_tsp(parent_1, parent_2)

                child_1 = self._mutation_tsp(child_1)
                child_2 = self._mutation_tsp(child_2)

                new_population.append(child_1)
                new_population.append(child_2)

            # Add elites directly to new population
            new_population += [elite[1] for elite in elites]

            population = new_population
            best_individual, best_solution = min(cost_tuples, key=lambda x: x[0])
            iteration_list.append(len(iteration_list))
            best_distances += [best_individual]

        return (
            best_individual,
            best_solution,
            iteration_list,
            best_distances,
            best_distances,
        )

    def _order_crossover_tsp(
        self, parent_1: List[int], parent_2: List[int]
    ) -> tuple[List[int], List[int]]:
        size = len(parent_1)

        # Step 1: Choose two random crossover points
        start, end = sorted(random.sample(range(size), 2))

        # Step 2: Create the first child
        child_1 = [None] * size
        # Copy the segment from parent_1
        child_1[start : end + 1] = parent_1[start : end + 1]

        # Fill the remaining positions with the order from parent_2
        current_pos = (end + 1) % size
        for city in parent_2:
            if city not in child_1:
                child_1[current_pos] = city
                current_pos = (current_pos + 1) % size

        # Step 3: Create the second child
        child_2 = [None] * size
        # Copy the segment from parent_2
        child_2[start : end + 1] = parent_2[start : end + 1]

        # Fill the remaining positions with the order from parent_1
        current_pos = (end + 1) % size
        for city in parent_1:
            if city not in child_2:
                child_2[current_pos] = city
                current_pos = (current_pos + 1) % size

        return child_1, child_2

    def _tournament_selection(
        self, cost_tuple: List[Tuple[float, List[int]]]
    ) -> List[int]:
        # Select first candidate
        candidate_1 = random.choice(cost_tuple)
        # Select second candidate ensuring it's different
        remaining_population = [ct for ct in cost_tuple if ct != candidate_1]
        candidate_2 = random.choice(remaining_population)

        # Extract distances
        distance_1, route_1 = candidate_1
        distance_2, route_2 = candidate_2

        # Select candidate with shortest route
        winner = route_1 if distance_1 <= distance_2 else route_2

        return winner

    def _mutation_tsp(self, solution: List[int]) -> List[int]:
        if random.random() < self.mutation_prob:
            return self.tsp_functions.generate_neighbor(solution)

        return solution

    def _generate_initial_population(self, tsp: pd.DataFrame) -> List[List[int]]:
        population = []
        for _ in range(self.population_size):
            individual = self.tsp_functions.random_solution(tsp)
            population.append(individual)

        return population

    def _generate_cost_tuples(
        self, tsp: pd.DataFrame, population: List[List[int]]
    ) -> List[Tuple[float, List[int]]]:
        cost_tuples = []
        for individual in population:
            cost = self.tsp_functions.calculate_cost(tsp, individual)
            cost_tuples.append((cost, individual))

        return cost_tuples
