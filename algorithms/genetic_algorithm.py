from typing import List, Tuple
import random
import numpy as np
import pandas as pd

from helpers.tsp_functions import TSPFunctions


class GeneticAlgorithm:
    def __init__(self):
        self.tsp_functions = TSPFunctions()
        self.population_size = 200  # 200
        self.elite_percentage = 0.2  # 0.2
        self.max_generations = 200  # 200
        self.mutation_prob = 0.3  # 0.3

    def tsp_genetic_algorithm(self, tsp):
        population = self._generate_initial_population(tsp)
        elite_count = int(self.population_size * self.elite_percentage)

        for _ in range(self.max_generations):
            # Keep best individuals (elitism)
            elites = self._elite_selection(tsp, population, elite_count)
            # If odd, increment by 1 to make even
            if elite_count % 2 != 0:
                elite_count += 1

            new_population = []
            for _ in range(self.population_size // 2 - elite_count // 2):
                parent_1 = self._tournament_selection(tsp, population)
                remaining_population = [p for p in population if p != parent_1]
                parent_2 = self._tournament_selection(tsp, remaining_population)

                child_1, child_2 = self._order_crossover_tsp(parent_1, parent_2)

                child_1 = self._mutation_tsp(child_1)
                child_2 = self._mutation_tsp(child_2)

                new_population.append(child_1)
                new_population.append(child_2)

            # Add elites directly to new population
            new_population += elites

            population = new_population
            best_individual = self._get_best_individual(tsp, population)[0]
            print(f"Best distance: {best_individual}")

        return self._get_best_individual(tsp, population)

    def _elite_selection(
        self, tsp: pd.DataFrame, population: List[List[int]], elite_count: int
    ) -> List[List[int]]:
        """Return the top 'elite_count' individuals with lowest cost from population."""
        # Sort population by ascending route cost
        sorted_population = sorted(
            population, key=lambda ind: self.tsp_functions.calculate_cost(tsp, ind)
        )
        return sorted_population[:elite_count]

    def _get_best_individual(
        self, tsp: pd.DataFrame, population: List[List[int]]
    ) -> List[int]:
        best_cost = float("inf")
        best_route = None

        for route in population:
            cost = self.tsp_functions.calculate_cost(tsp, route)
            if cost < best_cost:
                best_cost = cost
                best_route = route

        return best_cost, best_route

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
        self, tsp: pd.DataFrame, population: List[List[int]]
    ) -> List[int]:
        candidate_1 = random.choice(population)
        # Select second candidate ensuring it's different
        remaining_population = [p for p in population if p != candidate_1]
        candidate_2 = random.choice(remaining_population)

        distance_1 = self.tsp_functions.calculate_cost(tsp, candidate_1)
        distance_2 = self.tsp_functions.calculate_cost(tsp, candidate_2)

        # Select candidate with shortest route
        winner = candidate_1 if distance_1 <= distance_2 else candidate_2

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
