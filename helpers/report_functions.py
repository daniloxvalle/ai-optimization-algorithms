import numpy as np
import pandas as pd


class ReportFunctions:
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
    def execute_n_times(self, tsp, algorithms, n_times):
        # Create DataFrame to store the results
        df_cost = self.create_costs_df(algorithms, n_times)

        for algorithm, algorithm_function in algorithms.items():

            print(algorithm)

            for i in range(n_times):

                cost, solution = algorithm_function(tsp)
                df_cost.loc[algorithm, i] = cost

                print(f"{cost:10.3f}  {solution}")

        return df_cost
