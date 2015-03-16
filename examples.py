import math

from matplotlib import pyplot
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

## Examples #

def heatmap_example(func, steps=100, boundary=True):
    ax = ternary.plot_heatmap(func, steps=steps, boundary=boundary)
    ternary.draw_boundary(steps, ax=ax)
    return ax

if __name__ == '__main__':
    ## Boundary and Gridlines
    pyplot.figure()
    steps = 30
    ax = ternary.draw_boundary(steps, color='black')
    ternary.draw_gridlines(steps, ax=ax, color='black')
    ax.set_title("Simplex Boundary and Gridlines")

    ## Various lines
    pyplot.figure()
    steps = 30
    ax = ternary.draw_boundary(steps, linewidth=2., color='black')
    ternary.draw_horizontal_line(ax, steps, 16)
    ternary.draw_left_parallel_line(ax, steps, 10, linewidth=2., color='red', linestyle="--")
    ternary.draw_right_parallel_line(ax, steps, 20, linewidth=3., color='blue')
    p1 = ternary.project_point((12,8,10))
    p2 = ternary.project_point((2, 26, 2))
    ternary.draw_line(ax, p1, p2, linewidth=3., marker='s', color='green', linestyle=":")
    ax.set_title("Various Lines")

    pyplot.show()
    exit()

    ## Heatmap of a function
    pyplot.figure()
    ax = heatmap_example(shannon_entropy, steps=100, boundary=True)
    ax.set_title("Shannon Entropy Heatmap")

    ## Heatmap of a function
    pyplot.figure()
    func = dirichlet([6, 10, 13])
    ax = heatmap_example(func, steps=100, boundary=False)
    ax.set_title("Ternary heatmap of Dirichlet function evaluated on partition")

    ## Sample trajectory plot
    pyplot.figure()
    ax = ternary.draw_boundary()
    ax.set_title("Plotting of sample trajectory data")
    points = []
    with open("curve.txt") as handle:
        for line in handle:
            points.append(map(float, line.split(' ')))
    ternary.plot(points, linewidth=2.0, ax=ax)

    pyplot.show()

