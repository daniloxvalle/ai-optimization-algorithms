from helpers.coordinates import df_coordinates
from helpers.tsp_functions import TSPFunctions

from helpers.plot_functions import PlotFunctions
from helpers.report_functions import ReportFunctions
from algorithms.hill_climbing import HillClimbing
from algorithms.simulated_annealing import SimulatedAnnealing


class Main:
    def __init__(self):
        self.tsp_functions = TSPFunctions()
        self.plot_functions = PlotFunctions()
        self.report_functions = ReportFunctions()
        self.hill_climbing = HillClimbing()
        self.simulated_annealing = SimulatedAnnealing()
        # number of times each algorithm will be executed
        self.n_times = 10

    def run(self):
        print("*** Starting")
        # Optimal tour length: 27.603
        tsp = self.tsp_functions.generate_tsp_problem(df_coordinates)

        individual_test = 1
        if individual_test:
            best_distance_hc, _ = self.hill_climbing.tsp_hill_climbing(tsp)
            print(f"Hill Climbing - Best distance: {best_distance_hc:,.2f}")
            best_distance_hc_r, _ = self.hill_climbing.tsp_hill_climbing_restart(tsp)
            print(
                f"Hill Climbing with Restart - Best distance: {best_distance_hc_r:,.2f}"
            )

        algorithms = {
            # "Hill-Climbing": self.algorithms.hill_climbing,
            # "Hill-Climbing Restart": self.algorithms.hill_climbing_restart,
            "Simulated Annealing": self.simulated_annealing.tsp_simulated_annealing,
        }

        # Execute N times to generate cost variable statistics
        df_cost = self.report_functions.execute_n_times(tsp, algorithms, self.n_times)

        print(df_cost.T.describe())
        # self.plot_functions.boxplot_sorted(df_cost)


if __name__ == "__main__":
    app = Main()
    app.run()
