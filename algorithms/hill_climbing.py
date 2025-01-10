from helpers.tsp_functions import TSPFunctions


class HillClimbing:
    def __init__(self):
        self.tsp_functions = TSPFunctions()
        self.num_restarts = 50  # default: 50

    def tsp_hill_climbing(self, tsp):
        initial_solution = self.tsp_functions.random_solution(tsp)
        # best solution so far
        best_solution, best_cost = self.tsp_functions.get_best_neighbor(
            tsp, initial_solution
        )

        while True:
            # try to get a better candidate
            new_candidate, new_cost = self.tsp_functions.get_best_neighbor(
                tsp, best_solution
            )

            if new_cost < best_cost:
                best_cost = new_cost
                best_solution = new_candidate
            else:
                break  # cost did not improve, so exit the while

        return best_cost, best_solution

    def tsp_hill_climbing_restart(self, tsp):
        # Initialize best solution tracking variables
        best_overall_cost = float("inf")
        best_overall_solution = None

        # Perform multiple hill climbing attempts with different starting points
        for _ in range(self.num_restarts):
            current_cost, current_solution = self.tsp_hill_climbing(tsp)
            # Update best solution if current solution is better
            if current_cost < best_overall_cost:
                best_overall_cost = current_cost
                best_overall_solution = current_solution

        return best_overall_cost, best_overall_solution
