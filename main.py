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
        # Optimal tour length: 27.603
        # best_route: 27601.17377
        # [29, 23, 22, 21, 17, 18, 19, 15, 12, 11, 10, 6, 2, 1, 5, 8, 4, 3, 7, 9, 13, 14, 16, 24, 27, 25, 20, 26, 28]
        self.tsp = self.tsp_functions.generate_tsp_problem(df_coordinates)
        # number of times each algorithm will be executed
        self.n_times = 1  # 10

    def run(self):
        print("*** Starting")

        run_individual = 1
        if run_individual:
            # best_distance_hc, _ = self.hill_climbing.tsp_hill_climbing(self.tsp)
            # print(f"Hill Climbing - Best distance: {best_distance_hc:,.2f}")
            # best_distance_hc_r, _ = self.hill_climbing.tsp_hill_climbing_restart(
            #     self.tsp
            # )
            # print(
            #     f"Hill Climbing with Restart - Best distance: {best_distance_hc_r:,.2f}"
            # )
            best_distance_ga, best_solution_ga = (
                self.genetic_algorithm.tsp_genetic_algorithm(self.tsp)
            )
            print(f"Genetic Algorithm - Best distance: {best_distance_ga:,.2f}")
            self.plot_functions.plot_routes(df_coordinates, best_solution_ga)

        run_report = 0
        if run_report:
            algorithms = {
                # "Hill-Climbing": self.hill_climbing.tsp_hill_climbing,
                # "Hill-Climbing Restart": self.hill_climbing.tsp_hill_climbing_restart,
                # "Simulated Annealing": self.simulated_annealing.tsp_simulated_annealing,
                "Genetic Algorithm": self.genetic_algorithm.tsp_genetic_algorithm,
            }

            # Execute N times to generate cost variable statistics
            df_cost = self.report_functions.execute_n_times(
                self.tsp, algorithms, self.n_times
            )

            print(df_cost.T.describe())
            self.plot_functions.boxplot_sorted(df_cost)

    def test(self):
        parent_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        parent_2 = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        child_1, child_2 = self.genetic_algorithm._order_crossover_tsp(
            parent_1, parent_2
        )
        print(f"Child 1: {child_1}")
        print(f"Child 2: {child_2}")

        parent_1 = self.tsp_functions.random_solution(self.tsp)
        parent_2 = self.tsp_functions.random_solution(self.tsp)
        population = [parent_1, parent_2]
        winner = self.genetic_algorithm._tournament_selection(self.tsp, population)
        print(f"Winner: {winner}")

        to_mutate = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        mutated = self.genetic_algorithm._mutation_tsp(to_mutate)
        print(f"Mutated: {mutated}")


if __name__ == "__main__":
    app = Main()
    app.run()
    # app.test()
