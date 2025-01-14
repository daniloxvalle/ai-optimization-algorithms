import numpy as np
import pandas as pd

from helpers.plot_functions import PlotFunctions
from helpers.coordinates import df_coordinates


class ReportFunctions:
    def __init__(self):
        self.plot_functions = PlotFunctions()

    # Create data structure (DataFrame) to store multiple results
    # and visualize them through statistics
    def create_costs_df(self, algorithms, n_times):
        algorithm_names = algorithms.keys()

        n_rows = len(algorithm_names)
        n_cols = n_times

        df_results = pd.DataFrame(np.zeros((n_rows, n_cols)), index=algorithm_names)
        df_results.index.name = "ALGORITHM"

        return df_results

    # Execute N times to generate cost variable statistics
    def execute_n_times_tsp(
        self,
        tsp,
        algorithms,
        n_times,
        max_objective_calls,
        print_costs=False,
        print_routes=False,
    ):
        # Create DataFrame to store the results
        df_cost = self.create_costs_df(algorithms, n_times)

        for algorithm, algorithm_function in algorithms.items():
            print(algorithm)
            iteration_lists = []
            distance_lists = []
            best_distances_lists = []
            best_cost = float("inf")
            best_solution = []

            for i in range(n_times):
                cost, solution, iteration_list, distance_list, best_distances = (
                    algorithm_function(tsp, max_objective_calls)
                )
                df_cost.loc[algorithm, i] = cost

                print(f"{cost:10.3f}  {solution}")
                if cost < best_cost:
                    best_cost = cost
                    best_solution = solution

                iteration_lists += [iteration_list]
                distance_lists += [distance_list]
                best_distances_lists += [best_distances]

            if print_costs:
                self.plot_functions.plot_10_cost_graphs(
                    iteration_lists,
                    distance_lists,
                    best_distances_lists,
                    filepath=f"results_tsp/{algorithm}.png",
                )

            if print_routes:
                self.plot_functions.plot_routes(df_coordinates, best_solution)

        return df_cost

    def execute_n_times_rastrigin(
        self,
        algorithms,
        n_times,
        max_objective_calls,
        print_costs=False,
    ):
        df_cost = self.create_costs_df(algorithms, n_times)

        for algorithm, algorithm_function in algorithms.items():
            print(algorithm)
            iteration_lists = []
            distance_lists = []
            best_distances_lists = []

            for i in range(n_times):
                cost, solution, iteration_list, distance_list, best_distances = (
                    algorithm_function(max_objective_calls)
                )
                df_cost.loc[algorithm, i] = cost

                print(f"{cost:10.3f}  {solution}")

                iteration_lists += [iteration_list]
                distance_lists += [distance_list]
                best_distances_lists += [best_distances]

            if print_costs:
                self.plot_functions.plot_10_cost_graphs(
                    iteration_lists,
                    distance_lists,
                    best_distances_lists,
                    filepath=f"results_rastrigin/{algorithm}.png",
                )

        return df_cost
