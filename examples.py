import math

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

if __name__ == '__main__':
    ## Boundary and Gridlines
    pyplot.figure()
    steps = 30
    gs = gridspec.GridSpec(1,2)
    ax = pyplot.subplot(gs[0,0])
    ax = ternary.draw_boundary(steps, color='black', ax=ax)
    ternary.draw_gridlines(steps, ax=ax, color='black')
    ax.set_title("Simplex Boundary and Gridlines")

    ## Various lines
    ax = pyplot.subplot(gs[0,1])
    ternary.draw_boundary(steps, linewidth=2., color='black', ax=ax)
    ternary.draw_horizontal_line(ax, steps, 16)
    ternary.draw_left_parallel_line(ax, steps, 10, linewidth=2., color='red', linestyle="--")
    ternary.draw_right_parallel_line(ax, steps, 20, linewidth=3., color='blue')
    p1 = ternary.project_point((12,8,10))
    p2 = ternary.project_point((2, 26, 2))
    ternary.draw_line(ax, p1, p2, linewidth=3., marker='s', color='green', linestyle=":")
    ax.set_title("Various Lines")

    ## Heatmap roundup
    steps = 60
    for function in [shannon_entropy, dirichlet([4, 8, 13])]:
        pyplot.figure()
        gs = gridspec.GridSpec(2,2)
        ax = pyplot.subplot(gs[0,0])
        ternary.function_heatmap(function, steps=steps, boundary_points=True, ax=ax)
        ternary.draw_boundary(steps+1, ax=ax, color='black')
        ax.set_title("Triangular with Boundary")

        ax = pyplot.subplot(gs[0,1])
        ternary.function_heatmap(function, steps=steps, boundary_points=False, ax=ax)
        ternary.draw_boundary(steps+1, ax=ax, color='black')
        ax.set_title("Triangular without Boundary")

        ax = pyplot.subplot(gs[1,0])
        ternary.function_heatmap(function, steps=steps, boundary_points=True, ax=ax, style="hexagonal")
        ternary.draw_boundary(steps, ax=ax, color='black')
        ax.set_title("Hexagonal with Boundary")

        ax = pyplot.subplot(gs[1,1])
        ternary.function_heatmap(function, steps=steps, boundary_points=False, ax=ax, style="hexagonal")
        ternary.draw_boundary(steps, ax=ax, color='black')
        ax.set_title("Hexagonal without Boundary")

    ## Sample trajectory plot
    pyplot.figure()
    ax = ternary.draw_boundary(color='black')
    ax.set_title("Plotting of sample trajectory data")
    points = []
    with open("curve.txt") as handle:
        for line in handle:
            points.append(map(float, line.split(' ')))
    ternary.plot(points, linewidth=2.0, ax=ax)

    pyplot.show()

