from helpers.tsp_functions import TSPFunctions
from helpers.rastrigin_functions import RastriginFunctions


class HillClimbing:
    def __init__(self):
        self.tsp_functions = TSPFunctions()
        self.rastrigin_functions = RastriginFunctions()
        self.num_restarts_tsp = 5
        self.num_restarts_rastringin = 20

    def tsp_hill_climbing(self, tsp, max_objective_calls):
        initial_solution = self.tsp_functions.random_solution(tsp)

        best_solution, best_cost, first_objective_calls = (
            self.tsp_functions.get_best_neighbor(tsp, initial_solution)
        )

        iteration_list = []
        best_distances = []

        objective_calls = first_objective_calls
        iteration = 0
        while objective_calls < max_objective_calls:
            new_candidate, new_cost, new_objective_calls = (
                self.tsp_functions.get_best_neighbor(tsp, best_solution)
            )

            if new_cost < best_cost:
                best_cost = new_cost
                best_solution = new_candidate

            iteration_list += [iteration]
            best_distances += [best_cost]
            iteration += 1

            objective_calls += new_objective_calls

        print("Iterations: ", iteration)
        return (
            best_cost,
            best_solution,
            iteration_list,
            best_distances,
            best_distances,
        )

    def tsp_hill_climbing_restart(self, tsp, max_objective_calls):
        # Initialize best solution tracking variables
        best_overall_cost = float("inf")
        best_overall_solution = None

        max_attempt_objective_calls = max_objective_calls // self.num_restarts_tsp

        iteration_list = []
        best_distances = []
        distance_list = []

        # Perform multiple hill climbing attempts with different starting points
        for _ in range(self.num_restarts_tsp):
            (
                current_cost,
                current_solution,
                attempt_iteration_list,
                attempt_distance_list,
                attempt_best_distances,
            ) = self.tsp_hill_climbing(tsp, max_attempt_objective_calls)

            for i in range(len(attempt_iteration_list)):
                iteration_list += [len(iteration_list)]
                if attempt_best_distances[i] < best_overall_cost:
                    best_distances += [attempt_best_distances[i]]
                else:
                    best_distances += [best_overall_cost]

            # Update best solution if current solution is better
            if current_cost < best_overall_cost:
                best_overall_cost = current_cost
                best_overall_solution = current_solution

            distance_list += attempt_distance_list

        return (
            best_overall_cost,
            best_overall_solution,
            iteration_list,
            distance_list,
            best_distances,
        )

    def rastrigin_hill_climbing(self, max_objective_calls):
        initial_solution = self.rastrigin_functions.random_solution()

        best_solution, best_cost, first_objective_calls = (
            self.rastrigin_functions.get_best_neighbor(initial_solution)
        )

        iteration_list = []
        best_distances = []

        objective_calls = first_objective_calls
        iteration = 0
        while objective_calls < max_objective_calls:
            new_candidate, new_cost, new_objective_calls = (
                self.rastrigin_functions.get_best_neighbor(best_solution)
            )

            if new_cost < best_cost:
                best_cost = new_cost
                best_solution = new_candidate

            iteration_list += [iteration]
            best_distances += [best_cost]
            iteration += 1

            objective_calls += new_objective_calls

        return (
            best_cost,
            best_solution,
            iteration_list,
            best_distances,
            best_distances,
        )

    def rastrigin_hill_climbing_restart(self, max_objective_calls):
        # Initialize best solution tracking variables
        best_overall_cost = float("inf")
        best_overall_solution = None

        max_attempt_objective_calls = (
            max_objective_calls // self.num_restarts_rastringin
        )

        iteration_list = []
        best_distances = []
        distance_list = []

        # Perform multiple hill climbing attempts with different starting points
        for _ in range(self.num_restarts_rastringin):
            (
                current_cost,
                current_solution,
                attempt_iteration_list,
                attempt_distance_list,
                attempt_best_distances,
            ) = self.rastrigin_hill_climbing(max_attempt_objective_calls)

            for i in range(len(attempt_iteration_list)):
                iteration_list += [len(iteration_list)]
                if attempt_best_distances[i] < best_overall_cost:
                    best_distances += [attempt_best_distances[i]]
                else:
                    best_distances += [best_overall_cost]

            # Update best solution if current solution is better
            if current_cost < best_overall_cost:
                best_overall_cost = current_cost
                best_overall_solution = current_solution

            distance_list += attempt_distance_list

        return (
            best_overall_cost,
            best_overall_solution,
            iteration_list,
            distance_list,
            best_distances,
        )
