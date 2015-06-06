import math
import random

import matplotlib
from matplotlib import pyplot, gridspec
from scipy import stats
from scipy.special import gamma, gammaln

import ternary

## Functions to plot #

def beta(alphas):
    """Multivariate beta function"""
    #return math.exp(sum(map(gammaln, alphas)) - gammaln(sum(alphas)))
    return sum(map(gammaln, alphas)) - gammaln(sum(alphas))

def dirichlet(alphas):
    """Computes Dirichlet probability distribution assuming all parameters alphas > 1."""
    B = beta(alphas)
    def f(x):
        s = 0.
        for i in range(len(alphas)):
            try:
                t = (alphas[i]-1.) * math.log(x[i])
                s += t
            except ValueError:
                return 0.
        return math.exp(s - B)
    return f

def shannon_entropy(p):
    """Computes the Shannon Entropy at a distribution in the simplex."""
    s = 0.
    for i in range(len(p)):
        try:
            s += p[i] * math.log(p[i])
        except ValueError:
            continue
    return -1.*s

def boundary_and_gridlines(axes_subplot=None, scale=30, multiple=5, color="black"):
    axes_subplot = ternary.boundary(scale, color=color, axes_subplot=axes_subplot)
    ternary.gridlines(scale, multiple=multiple, axes_subplot=axes_subplot, color=color)
    return axes_subplot

def various_lines(axes_subplot, scale=30):
    ternary.boundary(scale, linewidth=2., color='black', axes_subplot=axes_subplot)
    ternary.horizontal_line(axes_subplot, scale, 16)
    ternary.left_parallel_line(axes_subplot, scale, 10, linewidth=2., color='red', linestyle="--")
    ternary.right_parallel_line(axes_subplot, scale, 20, linewidth=3., color='blue')
    p1 = ternary.project_point((12,8,10))
    p2 = ternary.project_point((2, 26, 2))
    ternary.line(axes_subplot, p1, p2, linewidth=3., marker='s', color='green', linestyle=":")

if __name__ == '__main__':
    ## Boundary and Gridlines
    pyplot.figure()
    scale = 10
    gs = gridspec.GridSpec(1,1)
    axes_subplot = pyplot.subplot(gs[0,0])
    boundary_and_gridlines(axes_subplot, scale, multiple=5)
    axes_subplot.set_title("Simplex Boundary and Gridlines")
    ternary.resize_drawing_canvas(axes_subplot, scale=scale)
    ternary.clear_matplotlib_ticks(axes_subplot)
    ternary.left_axis_label(axes_subplot, "Left label $\\alpha^2$", fontsize=20)
    ternary.right_axis_label(axes_subplot, "Right label $\\beta^2$", fontsize=20)
    ternary.bottom_axis_label(axes_subplot, "Bottom label $\\Gamma - \\Omega$", fontsize=20)


    pyplot.show()
    exit()

    ## Various lines
    axes_subplot = pyplot.subplot(gs[0,1])
    various_lines(axes_subplot, scale)
    ternary.clear_matplotlib_ticks(axes_subplot)
    axes_subplot.set_title("Various Lines")

    # Scatter Plot
    pyplot.figure()
    scale = 40
    axes_subplot = ternary.boundary(scale, color="black")
    ternary.gridlines(scale, multiple=5, axes_subplot=axes_subplot, color="black")
    points = []
    for i in range(100):
        x = random.randint(1, scale)
        y = random.randint(0, scale - x)
        z = scale - x - y
        points.append((x,y,z))
    ternary.scatter(points, scale=scale, axes_subplot=axes_subplot)
    axes_subplot.set_title("Scatter Plot")

    ## Sample trajectory plot
    pyplot.figure()
    axes_subplot = ternary.boundary(color='black')
    axes_subplot.set_title("Plotting of sample trajectory data")
    points = []
    with open("curve.txt") as handle:
        for line in handle:
            points.append(map(float, line.split(' ')))
    ternary.gridlines(multiple=0.2, axes_subplot=axes_subplot, color="black")
    ternary.plot(points, linewidth=2.0, axes_subplot=axes_subplot)

    ## Heatmap roundup
    scale = 60
    for function in [shannon_entropy, dirichlet([4, 8, 13])]:
        pyplot.figure()
        gs = gridspec.GridSpec(2,2)
        axes_subplot = pyplot.subplot(gs[0,0])
        ternary.heatmap_of_function(function, scale=scale, boundary=True,
                                    axes_subplot=axes_subplot)
        ternary.boundary(scale+1, axes_subplot=axes_subplot, color='black')
        axes_subplot.set_title("Triangular with Boundary")

        axes_subplot = pyplot.subplot(gs[0,1])
        ternary.heatmap_of_function(function, scale=scale, boundary=False,
                                 axes_subplot=axes_subplot)
        ternary.boundary(scale+1, axes_subplot=axes_subplot, color='black')
        axes_subplot.set_title("Triangular without Boundary")

        axes_subplot = pyplot.subplot(gs[1,0])
        ternary.heatmap_of_function(function, scale=scale, boundary=True,
                                 axes_subplot=axes_subplot, style="hexagonal")
        ternary.boundary(scale, axes_subplot=axes_subplot, color='black')
        axes_subplot.set_title("Hexagonal with Boundary")

        axes_subplot = pyplot.subplot(gs[1,1])
        ternary.heatmap_of_function(function, scale=scale, boundary=False,
                                 axes_subplot=axes_subplot, style="hexagonal")
        ternary.boundary(scale, axes_subplot=axes_subplot, color='black')
        axes_subplot.set_title("Hexagonal without Boundary")

    pyplot.show()

