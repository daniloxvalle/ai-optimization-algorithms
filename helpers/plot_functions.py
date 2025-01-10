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

    # rot=90 for vertical labels, fontsize=20 default font size
    def boxplot_sorted(self, df, rot=0, figsize=(12, 6), fontsize=16):
        df2 = df.T
        meds = df2.median().sort_values(ascending=False)

        # Create figure and axes
        plt.figure(figsize=figsize)

        axes = df2[meds.index].boxplot(
            figsize=figsize,
            rot=rot,
            fontsize=fontsize,
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

        axes.set_title("Cost of Algorithms", fontsize=fontsize)
        # Display the plot
        plt.show()
