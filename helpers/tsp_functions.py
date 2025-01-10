from math import sqrt
import random

import numpy as np
import pandas as pd


class TSPFunctions:
    # Euclidean distance between two points
    def distance(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        return sqrt(dx**2 + dy**2)

    # Calculate distance matrix.
    # NOTE: It is not strictly necessary to calculate them beforehand.
    #       This was done only for didactic purposes.
    #       Instead, distances can be calculated on demand.
    def generate_distance_matrix(self, coordinates):
        n_cities = len(coordinates)
        dist = np.zeros((n_cities, n_cities), dtype=float)

        for i in range(0, n_cities):
            for j in range(i + 1, n_cities):
                x1, y1 = coordinates.iloc[i]
                x2, y2 = coordinates.iloc[j]

                dist[i, j] = self.distance(x1, y1, x2, y2)
                dist[j, i] = dist[i, j]

        return dist

    # Receives a list with the real coordinates of a city and
    # generates a distance matrix between the cities.
    # Note: the matrix is symmetric and with a null diagonal
    def generate_tsp_problem(self, df_cities: pd.DataFrame) -> pd.DataFrame:
        # fictitious city names
        cities = df_cities.index

        # calculate distance matrix
        distances = self.generate_distance_matrix(df_cities)

        # create structure to store the distances between all cities
        tsp = pd.DataFrame(distances, columns=cities, index=cities)

        return tsp

    # Create an initial solution with cities in a random order
    def random_solution(self, tsp):
        cities = list(tsp.keys())
        solution = []

        # the 3 lines below are not strictly necessary, they serve
        # only to fix the first city of the list in the solution
        city = cities[0]
        solution.append(city)
        cities.remove(city)

        for _ in range(0, len(cities)):
            # print(_, cities, solution)
            city = random.choice(cities)

            solution.append(city)
            cities.remove(city)

        return solution

    # Objective Function: calculates the cost of a given solution.
    # Note: In this case of the traveling salesman problem (TSP),
    # the cost is the length of the route between all cities.
    def calculate_cost(self, tsp, solution):
        n = len(solution)
        cost = 0

        for i in range(n):

            # When reaching the last city, it will be necessary
            # to return to the start to add the
            # length of the route from the last city
            # to the first city, closing the cycle.
            #
            # Therefore, the line below:
            k = (i + 1) % n
            city_a = solution[i]
            city_b = solution[k]

            cost += tsp.loc[city_a, city_b]

            # print(tsp.loc[cityA, cityB], cityA, cityB)

        return cost

    def generate_neighbor(self, route):
        new_route = route.copy()

        # Use random.sample to get two different indices
        index_a, index_b = random.sample(range(len(route)), 2)

        new_route[index_a], new_route[index_b] = new_route[index_b], new_route[index_a]

        return new_route

    # From a given solution, generates several variations (neighbors)
    def generate_neighbors(self, solution):
        n = len(solution)
        for i in range(1, n):  # keep the first fixed
            for j in range(i + 1, n):
                neighbor = solution.copy()
                neighbor[i] = solution[j]
                neighbor[j] = solution[i]

                yield neighbor

    def get_best_neighbor(self, tsp, solution):
        best_cost = self.calculate_cost(tsp, solution)
        best_neighbor = solution

        for neighbor in self.generate_neighbors(solution):
            current_cost = self.calculate_cost(tsp, neighbor)
            if current_cost < best_cost:
                best_cost = current_cost
                best_neighbor = neighbor

        return best_neighbor, best_cost
