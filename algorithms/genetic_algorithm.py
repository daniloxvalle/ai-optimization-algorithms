from typing import List, Tuple
import random
import pandas as pd

from helpers.tsp_functions import TSPFunctions
from helpers.rastrigin_functions import RastriginFunctions


class GeneticAlgorithm:
    def __init__(self):
        self.tsp_functions = TSPFunctions()
        self.rastrigin_functions = RastriginFunctions()
        self.population_size_tsp = 200
        self.elite_percentage = 0.2
        self.mutation_prob = 0.2
        self.population_size_rastrigin = 20
        self.generations_rastrigin = 50

    def tsp_genetic_algorithm(self, tsp, max_objective_calls):
        population = self._generate_initial_population_tsp(tsp)
        elite_count = int(self.population_size_tsp * self.elite_percentage)
        # If odd, increment by 1 to make even
        if elite_count % 2 != 0:
            elite_count += 1

        objective_calls = 0
        iteration_list = []
        best_distances = []

        while objective_calls < max_objective_calls:
            cost_tuples = self._generate_cost_tuples_tsp(tsp, population)

            objective_calls += self.population_size_tsp

            # Keep best individuals (elitism)
            sorted_cost_tuples = sorted(cost_tuples, key=lambda x: x[0])
            elites = sorted_cost_tuples[:elite_count]

            new_population = []
            for _ in range(self.population_size_tsp // 2 - elite_count // 2):
                parent_1 = self._tournament_selection_tsp(cost_tuples)
                remaining_cost_tuple = [ct for ct in cost_tuples if ct[1] != parent_1]
                parent_2 = self._tournament_selection_tsp(remaining_cost_tuple)

                child_1, child_2 = self._order_crossover_tsp(parent_1, parent_2)

                child_1 = self._mutation_tsp(child_1)
                child_2 = self._mutation_tsp(child_2)

                new_population.append(child_1)
                new_population.append(child_2)

            # Add elites directly to new population
            new_population += [elite[1] for elite in elites]

            population = new_population
            best_cost, best_solution = min(cost_tuples, key=lambda x: x[0])
            iteration_list.append(len(iteration_list))
            best_distances += [best_cost]

        return (
            best_cost,
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

    def _tournament_selection_tsp(
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

    def _generate_initial_population_tsp(self, tsp: pd.DataFrame) -> List[List[int]]:
        population = []
        for _ in range(self.population_size_tsp):
            individual = self.tsp_functions.random_solution(tsp)
            population.append(individual)

        return population

    def _generate_cost_tuples_tsp(
        self, tsp: pd.DataFrame, population: List[List[int]]
    ) -> List[Tuple[float, List[int]]]:
        cost_tuples = []
        for individual in population:
            cost = self.tsp_functions.calculate_cost(tsp, individual)
            cost_tuples.append((cost, individual))

        return cost_tuples

    def rastrigin_genetic_algorithm(self, _):
        population = self._generate_initial_population_rastrigin()

        elite_count = int(self.population_size_rastrigin * self.elite_percentage)
        # If odd, increment by 1 to make even
        if elite_count % 2 != 0:
            elite_count += 1

        iteration_list = []
        best_costs = []

        for _ in range(self.generations_rastrigin):
            cost_tuples = self._generate_cost_tuples_rastrigin(population)

            # Keep best individuals (elitism)
            sorted_cost_tuples = sorted(cost_tuples, key=lambda x: x[0])
            elites = sorted_cost_tuples[:elite_count]

            new_population = []
            for _ in range(self.population_size_rastrigin // 2 - elite_count // 2):
                parent_1 = self._tournament_selection_rastrigin(cost_tuples)
                remaining_cost_tuple = [ct for ct in cost_tuples if ct[1] != parent_1]
                parent_2 = self._tournament_selection_rastrigin(remaining_cost_tuple)

                child_1, child_2 = self._crossover_rastrigin(parent_1, parent_2)

                child_1 = self._mutation_rastrigin(child_1)
                child_2 = self._mutation_rastrigin(child_2)

                new_population.append(child_1)
                new_population.append(child_2)

            # Add elites directly to new population
            new_population += [elite[1] for elite in elites]

            population = new_population
            best_cost, best_solution = min(cost_tuples, key=lambda x: x[0])
            iteration_list.append(len(iteration_list))
            best_costs += [best_cost]

        return (
            best_cost,
            best_solution,
            iteration_list,
            best_costs,
            best_costs,
        )

    def _generate_initial_population_rastrigin(self):
        population = []
        for _ in range(self.population_size_rastrigin):
            individual = self.rastrigin_functions.random_solution()
            population.append(individual)

        return population

    def _generate_cost_tuples_rastrigin(self, population):
        cost_tuples = []
        for individual in population:
            cost = self.rastrigin_functions.calculate_cost(individual)
            cost_tuples.append((cost, individual))

        return cost_tuples

    def _tournament_selection_rastrigin(self, cost_tuple):
        candidate_1 = random.choice(cost_tuple)
        remaining_population = [ct for ct in cost_tuple if ct != candidate_1]
        candidate_2 = random.choice(remaining_population)

        cost_1, solution_1 = candidate_1
        cost_2, solution_2 = candidate_2

        winner = solution_1 if cost_1 <= cost_2 else solution_2

        return winner

    def _mutation_rastrigin(self, solution):
        if random.random() < self.mutation_prob:
            return self.rastrigin_functions.generate_neighbor(solution)

        return solution

    def _crossover_rastrigin(self, parent1, parent2):
        # Generate alpha from a uniform distribution between 0 and 1
        alpha = random.uniform(0, 1)

        # Perform weighted average crossover for each coordinate
        child1_x = parent1[0] * alpha + parent2[0] * (1 - alpha)
        child1_y = parent1[1] * alpha + parent2[1] * (1 - alpha)
        child2_x = parent2[0] * alpha + parent1[0] * (1 - alpha)
        child2_y = parent2[1] * alpha + parent1[1] * (1 - alpha)

        child1 = (child1_x, child1_y)
        child2 = (child2_x, child2_y)

        return child1, child2
