import pandas as pd

from helpers.coordinates import df_coordinates
from helpers.tsp_functions import TSPFunctions
from helpers.plot_functions import PlotFunctions
from helpers.report_functions import ReportFunctions
from algorithms.hill_climbing import HillClimbing
from algorithms.simulated_annealing import SimulatedAnnealing
from algorithms.genetic_algorithm import GeneticAlgorithm


class Main:
    def __init__(self):
        self.tsp_functions = TSPFunctions()
        self.plot_functions = PlotFunctions()
        self.report_functions = ReportFunctions()
        self.hill_climbing = HillClimbing()
        self.simulated_annealing = SimulatedAnnealing()
        self.genetic_algorithm = GeneticAlgorithm()
        self.tsp = self.tsp_functions.generate_tsp_problem(df_coordinates)
        # number of times each algorithm will be executed
        self.n_times = 10  # 10
        # iterations will be limited by objective functions calls
        self.max_objective_calls = 50000  # 50000

    def run(self):
        print("*** Starting")

        run_report = 1
        if run_report:
            algorithms = {
                "Hill-Climbing": self.hill_climbing.tsp_hill_climbing,
                "Hill-Climbing Restart": self.hill_climbing.tsp_hill_climbing_restart,
                "Simulated Annealing": self.simulated_annealing.tsp_simulated_annealing_linear_cooling,
                "Genetic Algorithm": self.genetic_algorithm.tsp_genetic_algorithm,
            }

            # Execute N times to generate cost variable statistics
            df_cost = self.report_functions.execute_n_times(
                self.tsp,
                algorithms,
                self.n_times,
                self.max_objective_calls,
                print_costs=True,
                print_routes=True,
            )
            # Summary of Results
            pd.options.display.float_format = "{:,.2f}".format
            print(df_cost.T.describe())
            df_cost.to_json(
                "results_tsp/df_cost_results.json", orient="columns", index=True
            )

            # Boxplot
            self.plot_functions.boxplot_sorted(df_cost)


if __name__ == "__main__":
    app = Main()
    app.run()
