import matplotlib.pyplot as plt
import plotly.graph_objects as go


# Plot the city routing solution
# using the PLOTLY library
class PlotFunctions:
    def plot_routes(self, df_cities, city_order):
        df_solution = df_cities.copy()
        df_solution = df_solution.reindex(city_order)

        # pylint: disable=C0103  # Disable snake_case warning for X, Y variables
        X = df_solution["X"]
        Y = df_solution["Y"]
        cities = list(df_solution.index)

        # create graphic object
        fig = go.Figure()

        fig.update_layout(autosize=False, width=500, height=500, showlegend=False)

        # generate lines with routes from the first to the last city
        fig.add_trace(
            go.Scatter(
                x=X,
                y=Y,
                text=cities,
                textposition="bottom center",
                mode="lines+markers+text",
                name="",
            )
        )

        # add line from the last to the first to close the cycle
        fig.add_trace(
            go.Scatter(
                x=X.iloc[[-1, 0]], y=Y.iloc[[-1, 0]], mode="lines+markers", name=""
            )
        )

        fig.show()

    def boxplot_sorted(self, df, rot=0, figsize=(12, 6)):
        df2 = df.T
        meds = df2.median().sort_values(ascending=False)

        # Create figure and axes
        plt.figure(figsize=figsize)

        axes = df2[meds.index].boxplot(
            figsize=figsize,
            rot=rot,
            boxprops=dict(linewidth=4, color="cornflowerblue"),
            whiskerprops=dict(linewidth=4, color="cornflowerblue"),
            medianprops=dict(linewidth=4, color="firebrick"),
            capprops=dict(linewidth=4, color="cornflowerblue"),
            flierprops=dict(
                marker="o",
                markerfacecolor="dimgray",
                markersize=12,
                markeredgecolor="black",
            ),
            return_type="axes",
        )

        axes.set_title("Cost of Algorithms")
        # Display the plot
        plt.show()

    def plot_distances(self, iteration_list, distance_list, best_distances, ax):
        x = iteration_list
        y1 = distance_list
        y2 = best_distances

        ax.set_xlabel("Iterations")
        ax.set_ylabel("Distances (costs)")
        ax.set_title("Total Path Length")

        ax.plot(x, y1, label="Current")
        ax.plot(x, y2, label="Best")
        ax.legend()

    def plot_axes_figure(self, iteration_list, distance_list, best_distances):
        x = iteration_list
        y1 = distance_list
        y2 = best_distances

        fig, ax = plt.subplots(figsize=(8, 6))

        # Plot the distances
        self.plot_distances(x, y1, y2, ax)

        # Adjust the spacing between subplots
        fig.tight_layout()

        # Display the plot
        plt.show()

    def plot_10_cost_graphs(
        self, iteration_lists, distance_lists, best_distances_lists, filepath
    ):
        num_graphs = min(
            10, len(iteration_lists), len(distance_lists), len(best_distances_lists)
        )
        fig, axes = plt.subplots(5, 2, figsize=(10, 15))
        axes = axes.flatten()  # Flatten the 2D array of axes for easy iteration

        for i in range(num_graphs):
            x = iteration_lists[i]
            y1 = distance_lists[i]
            y2 = best_distances_lists[i]

            ax = axes[i]
            self.plot_distances(x, y1, y2, ax)
            ax.set_title(f"Execution: {i+1}")

        # Adjust the spacing between subplots
        fig.tight_layout()

        # Display the plot
        # plt.show()

        # Save the plot to a file
        plt.savefig(filepath)

        # Close the plot to free up memory
        plt.close(fig)
