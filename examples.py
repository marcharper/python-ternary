import math
import os
import random

import matplotlib
from matplotlib import pyplot, gridspec

import ternary

def load_sample_trajectory_data(filename="curve.txt", directory="sample_data"):
    full_filename = os.path.join(directory, filename)
    points = []
    with open(full_filename) as handle:
        for line in handle:
            points.append(list(map(float, line.split(' '))))
    return points

def load_sample_heatmap_data(filename="sample_heatmap_data.txt",
                             directory="sample_data"):
    """Loads sample heatmap data."""
    full_filename = os.path.join(directory, filename)
    data = dict()
    handle = open(full_filename)
    for line in handle:
        line = line.strip()
        i, j, k, v = line.split(' ')
        data[(int(i), int(j), int(k))] = float(v)
    return data

def generate_random_heatmap_data(scale=5):
    from ternary.helpers import simplex_iterator
    d = dict()
    for (i,j,k) in simplex_iterator(scale):
        d[(i,j)] = random.random()
    return d

def shannon_entropy(p):
    """Computes the Shannon Entropy at a distribution in the simplex."""
    s = 0.
    for i in range(len(p)):
        try:
            s += p[i] * math.log(p[i])
        except ValueError:
            continue
    return -1.*s

def random_points(num_points=25, scale=40):
    points = []
    for i in range(num_points):
        x = random.randint(1, scale)
        y = random.randint(0, scale - x)
        z = scale - x - y
        points.append((x,y,z))
    return points

def random_heatmap(scale=4):
    d = generate_random_heatmap_data(scale)
    figure, tax = ternary.figure(scale=scale, ax=ax)
    tax.heatmap(d, style="t")
    tax.boundary(color='black')
    tax.set_title("Heatmap Test: Triangular")

    ax = pyplot.subplot(gs[0,1])
    figure, tax = ternary.figure(scale=scale, ax=ax)
    tax.heatmap(d, style="d")
    tax.boundary(color='black')
    tax.set_title("Heatmap Test Dual")
    pyplot.show()

if __name__ == '__main__':
    # Show Coordinates
    scale = 3
    figure, tax = ternary.figure(scale=scale, permutation="120")
    points_lists = [[(0,0,3), (1,0,2), (2,0,1)],
                    [(3,0,0), (2,1,0), (1,2,0)],
                    [(0,3,0), (0,2,1), (0,1,2)],
                    [(1,1,1)]]
    colors = ['b', 'r', 'g', 'black']
    markers = ['o', 'v', '*', 'd']
    for i, points in enumerate(points_lists):
        for point in points:
            tax.scatter([tuple(point)], color=colors[i], marker=markers[i])
            tax.annotate("".join(map(str, point)), tuple(point), color=colors[i])
    tax.gridlines(multiple=1.)

    ## Boundary and Gridlines
    scale = 40
    figure, ternary_ax = ternary.figure(scale=scale)

    left_kwargs = {'color': 'blue'}
    right_kwargs = {'color': 'red'}

    # Draw Boundary and Gridlines
    ternary_ax.boundary(linewidth=2.0)
    ternary_ax.gridlines(color="blue", multiple=5, left_kwargs=left_kwargs,
                         right_kwargs=right_kwargs)

    # Draw Boundary and Gridlines
    ternary_ax.boundary(linewidth=2.0)
    ternary_ax.gridlines(color="black", multiple=5)
    ternary_ax.gridlines(color="blue", multiple=1, linewidth=0.5)

    # Set Axis labels and Title
    fontsize = 20
    ternary_ax.set_title("Simplex Boundary and Gridlines", fontsize=fontsize)
    ternary_ax.left_axis_label("Left label $\\alpha^2$", fontsize=fontsize)
    ternary_ax.right_axis_label("Right label $\\beta^2$", fontsize=fontsize)
    ternary_ax.bottom_axis_label("Bottom label $\\Gamma - \\Omega$", fontsize=fontsize)

    ternary_ax.ticks(axis='lbr', clockwise=True, multiple=5, linewidth=1)

    # Remove default Matplotlib Axes
    ternary_ax.clear_matplotlib_ticks()

    ### Plot Various lines
    scale = 40
    figure, ternary_ax = ternary.figure(scale=scale)

    # Draw Boundary and Gridlines
    ternary_ax.boundary(linewidth=2.0)
    ternary_ax.gridlines(color="blue", multiple=5)

    # Set Axis labels and Title
    fontsize = 20
    ternary_ax.set_title("Various Lines", fontsize=20)
    ternary_ax.left_axis_label("Left label $\\alpha^2$", fontsize=fontsize)
    ternary_ax.right_axis_label("Right label $\\beta^2$", fontsize=fontsize)
    ternary_ax.bottom_axis_label("Bottom label $\\Gamma - \\Omega$", fontsize=fontsize)

    # Draw lines parallel to the axes
    ternary_ax.horizontal_line(16)
    ternary_ax.left_parallel_line(10, linewidth=2., color='red', linestyle="--")
    ternary_ax.right_parallel_line(20, linewidth=3., color='blue')
    # Draw an arbitrary line
    p1 = (12,8,10)
    p2 = (2, 26, 2)
    ternary_ax.line(p1, p2, linewidth=3., marker='s', color='green', linestyle=":")

    ternary_ax.clear_matplotlib_ticks()
    ternary_ax.ticks(axis='lbr', multiple=5, linewidth=1)

    ### Scatter Plot
    scale = 40
    figure, ternary_ax = ternary.figure(scale=scale)
    ternary_ax.set_title("Scatter Plot", fontsize=20)
    ternary_ax.boundary(linewidth=2.0)
    ternary_ax.gridlines(multiple=5, color="blue")
    # Plot a few different styles with a legend
    points = random_points(30, scale=scale)
    ternary_ax.scatter(points, marker='s', color='red', label="Red Squares")
    points = random_points(30, scale=scale)
    ternary_ax.scatter(points, marker='D', color='green', label="Green Diamonds")
    ternary_ax.legend()
    ternary_ax.clear_matplotlib_ticks()
    ternary_ax.ticks(axis='lbr', multiple=5, linewidth=1)

    ## Sample trajectory plot
    figure, tax = ternary.figure(scale=1.0)
    tax.boundary()
    tax.set_title("Plotting of sample trajectory data", fontsize=20)
    points = load_sample_trajectory_data()
    tax.gridlines(multiple=0.2, color="black")
    tax.plot(points, linewidth=2.0, label="Curve")
    tax.legend()

    ## Sample colored trajectory plot
    figure, tax = ternary.figure(scale=1.0)
    tax.boundary()
    tax.set_title("Plotting of sample trajectory data", fontsize=20)
    points = load_sample_trajectory_data()
    tax.gridlines(multiple=0.2, color="black")
    tax.plot_colored_trajectory(points, linewidth=2.0)
    points = [(y,z,x) for (x,y,z) in points]
    tax.plot_colored_trajectory(points, cmap="hsv", linewidth=2.0)
    tax.legend()
    tax.clear_matplotlib_ticks()
    tax.ticks(axis='lbr', linewidth=1, multiple=0.1)

    pyplot.show()

    ## Heatmap roundup
    # Careful -- these can use a lot of RAM!
    scale = 60
    function = shannon_entropy
    pyplot.figure()
    gs = gridspec.GridSpec(2,3)

    ax = pyplot.subplot(gs[0,0])
    figure, tax = ternary.figure(ax=ax, scale=scale)
    tax.heatmapf(function, boundary=True, style="triangular")
    tax.boundary()
    tax.set_title("Triangular with Boundary")

    ax = pyplot.subplot(gs[1,0])
    figure, tax = ternary.figure(ax=ax, scale=scale)
    tax.heatmapf(function, boundary=False, style="t")
    tax.boundary()
    tax.set_title("Triangular without Boundary")

    ax = pyplot.subplot(gs[0,1])
    figure, tax = ternary.figure(ax=ax, scale=scale)
    tax.heatmapf(function, boundary=True, style="dual-triangular")
    tax.boundary()
    tax.set_title("Dual Triangular with Boundary")

    ax = pyplot.subplot(gs[1,1])
    figure, tax = ternary.figure(ax=ax, scale=scale)
    tax.heatmapf(function, boundary=False, style="d")
    tax.boundary()
    tax.set_title("Dual Triangular without Boundary")

    ax = pyplot.subplot(gs[0,2])
    figure, tax = ternary.figure(ax=ax, scale=scale)
    tax.heatmapf(function, boundary=True, style="hexagonal")
    tax.boundary()
    tax.set_title("Hexagonal with Boundary")

    ax = pyplot.subplot(gs[1,2])
    figure, tax = ternary.figure(ax=ax, scale=scale)
    tax.heatmapf(function, boundary=False, style="h")
    tax.boundary()
    tax.set_title("Hexagonal without Boundary")

    ## Heatmaps from data
    # Careful -- these can use a lot of RAM!
    scale = 60
    data = load_sample_heatmap_data()
    pyplot.figure()
    gs = gridspec.GridSpec(1, 3)
    ax = pyplot.subplot(gs[0,0])
    figure, tax = ternary.figure(ax=ax, scale=scale)
    tax.heatmap(data, style="dual-triangular")
    tax.boundary()
    tax.set_title("Dual-Triangular Heatmap from Data")

    ax = pyplot.subplot(gs[0,1])
    figure, tax = ternary.figure(ax=ax, scale=scale)
    tax.heatmap(data, style="triangular")
    tax.boundary()
    tax.set_title("Triangular Heatmap from Data")

    ax = pyplot.subplot(gs[0,2])
    figure, tax = ternary.figure(ax=ax, scale=scale)
    tax.heatmap(data, style="hexagonal")
    tax.boundary()
    tax.set_title("Hexagonal Heatmap from Data")

    pyplot.show()
