import os
import random

from matplotlib import pyplot as plt

import ternary


def load_sample_trajectory_data(filename="curve.txt", directory="sample_data"):
    full_filename = os.path.join(directory, filename)
    points = []
    with open(full_filename) as handle:
        for line in handle:
            points.append(list(map(float, line.split(' '))))
    return points


def random_points(num_points=25, scale=40):
    points = []
    for i in range(num_points):
        x = random.randint(1, scale)
        y = random.randint(0, scale - x)
        z = scale - x - y
        points.append((x, y, z))
    return points

if __name__ == '__main__':
    # Show Coordinates
    scale = 3
    fig, tax = ternary.figure(scale=scale, permutation="120")
    points_lists = [[(0, 0, 3), (1, 0, 2), (2, 0, 1)],
                    [(3, 0, 0), (2, 1, 0), (1, 2, 0)],
                    [(0, 3, 0), (0, 2, 1), (0, 1, 2)],
                    [(1, 1, 1)]]
    colors = ['b', 'r', 'g', 'black']
    markers = ['o', 'v', '*', 'd']
    for i, points in enumerate(points_lists):
        for point in points:
            tax.scatter([tuple(point)], color=colors[i], marker=markers[i])
            tax.annotate("".join(map(str, point)), tuple(point), color=colors[i])
    tax.gridlines(multiple=1.)

    ## Boundary and Gridlines
    scale = 40
    fig, tax = ternary.figure(scale=scale)

    left_kwargs = {'color': 'blue'}
    right_kwargs = {'color': 'red'}

    # Draw Boundary and Gridlines
    tax.boundary(linewidth=2.0)
    tax.gridlines(color="blue", multiple=5, left_kwargs=left_kwargs,
                  right_kwargs=right_kwargs)

    # Draw Boundary and Gridlines
    tax.boundary(linewidth=2.0)
    tax.gridlines(color="black", multiple=5)
    tax.gridlines(color="blue", multiple=1, linewidth=0.5)

    # Set Axis labels and Title
    fontsize = 20
    tax.set_title("Simplex Boundary and Gridlines", fontsize=fontsize)
    tax.left_axis_label("Left label $\\alpha^2$", fontsize=fontsize)
    tax.right_axis_label("Right label $\\beta^2$", fontsize=fontsize)
    tax.bottom_axis_label("Bottom label $\\Gamma - \\Omega$",
                          fontsize=fontsize)
    tax.get_axes().axis('off')
    tax.ticks(axis='lbr', clockwise=True, multiple=5, linewidth=1)

    # Remove default Matplotlib Axes
    tax.get_axes().axis('off')
    tax.clear_matplotlib_ticks()

    ### Plot Various lines
    scale = 40
    fig, tax = ternary.figure(scale=scale)

    # Draw Boundary and Gridlines
    tax.boundary(linewidth=2.0)
    tax.gridlines(color="blue", multiple=5)

    # Set Axis labels and Title
    fontsize = 20
    tax.top_corner_label("X", fontsize=fontsize)
    tax.left_corner_label("Y", fontsize=fontsize)
    tax.right_corner_label("Z", fontsize=fontsize)

    # Draw lines parallel to the axes
    tax.horizontal_line(16)
    tax.left_parallel_line(10, linewidth=2., color='red', linestyle="--")
    tax.right_parallel_line(20, linewidth=3., color='blue')
    # Draw an arbitrary line
    p1 = (12, 8, 10)
    p2 = (2, 26, 2)
    tax.line(p1, p2, linewidth=3., marker='s', color='green', linestyle=":")

    tax.get_axes().axis('off')
    tax.clear_matplotlib_ticks()
    tax.ticks(axis='lbr', multiple=5, linewidth=1)

    ### Scatter Plot
    scale = 40
    fig, tax= ternary.figure(scale=scale)
    tax.set_title("Scatter Plot", fontsize=20)
    tax.boundary(linewidth=2.0)
    tax.gridlines(multiple=5, color="blue")
    # Plot a few different styles with a legend
    points = random_points(30, scale=scale)
    tax.scatter(points, marker='s', color='red', label="Red Squares")
    points = random_points(30, scale=scale)
    tax.scatter(points, marker='D', color='green', label="Green Diamonds")
    tax.legend()
    tax.ticks(axis='lbr', multiple=5, linewidth=1)
    tax.get_axes().axis('off')
    tax.clear_matplotlib_ticks()

    ## Sample trajectory plot
    fig, tax = ternary.figure(scale=1.0)
    tax.boundary()
    tax.set_title("Plotting of sample trajectory data", fontsize=20)
    points = load_sample_trajectory_data()
    tax.gridlines(multiple=0.2, color="black")
    tax.plot(points, linewidth=2.0, label="Curve")
    tax.legend()
    tax.get_axes().axis('off')
    tax.clear_matplotlib_ticks()

    ## Sample colored trajectory plot
    fig, tax = ternary.figure(scale=1.0)
    tax.boundary()
    tax.set_title("Plotting of sample trajectory data", fontsize=20)
    points = load_sample_trajectory_data()
    tax.gridlines(multiple=0.2, color="black")
    tax.plot_colored_trajectory(points, linewidth=2.0)
    points = [(y, z, x) for (x, y, z) in points]
    tax.plot_colored_trajectory(points, cmap="hsv", linewidth=2.0)
    tax.legend()
    tax.get_axes().axis('off')
    tax.clear_matplotlib_ticks()
    tax.ticks(axis='lbr', linewidth=1, multiple=0.1)

    plt.show()
