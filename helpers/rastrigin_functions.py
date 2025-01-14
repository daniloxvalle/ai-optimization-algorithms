from math import cos, pi
import random


class RastriginFunctions:
    def __init__(self):
        self.lower_bound = -5.12
        self.upper_bound = 5.12

    # Rastrigin function: 𝒇 𝒙,𝒚 = 𝟐𝟎 + 𝒙𝟐 −𝟏𝟎𝐜𝐨𝐬 𝟐𝝅𝒙 + 𝒚𝟐 −𝟏𝟎𝐜𝐨𝐬 𝟐𝝅𝒚
    def rastrigin(self, x, y):
        return 20 + x**2 - 10 * cos(2 * pi * x) + y**2 - 10 * cos(2 * pi * y)

    def random_solution(self):
        x = random.uniform(self.lower_bound, self.upper_bound)
        y = random.uniform(self.lower_bound, self.upper_bound)
        return x, y

    def calculate_cost(self, solution):
        x, y = solution
        return self.rastrigin(x, y)

    def generate_neighbor(self, solution, std_dev=0.2):
        x, y = solution
        neighbor_x = x + random.gauss(0, std_dev)
        neighbor_y = y + random.gauss(0, std_dev)

        # Ensure the neighbor values are within the bounds
        neighbor_x = max(min(neighbor_x, self.upper_bound), self.lower_bound)
        neighbor_y = max(min(neighbor_y, self.upper_bound), self.lower_bound)

        return neighbor_x, neighbor_y

    def generate_neighbors(self, solution, num_neighbors=10):
        neighbors = []
        for _ in range(num_neighbors):
            neighbors.append(self.generate_neighbor(solution))
        return neighbors

    def get_best_neighbor(self, solution, num_neighbors=10):
        best_cost = self.calculate_cost(solution)
        best_neighbor = solution
        objective_calls = 0

        neighbors = self.generate_neighbors(solution, num_neighbors)

        for neighbor in neighbors:
            current_cost = self.calculate_cost(neighbor)
            objective_calls += 1
            if current_cost < best_cost:
                best_cost = current_cost
                best_neighbor = neighbor

        return best_neighbor, best_cost, objective_calls
