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
    ternary.plot_heatmap(func, steps=steps, boundary=boundary)
    ternary.draw_boundary(scale=steps)

def plot_shell(steps=10, fill_color='black'):
    """Plot an empty heatmap shell for illustration."""
    for i in range(steps+1):
        for j in range(steps - i):
            vertices = ternary.triangle_coordinates(i,j, alt=False)
            x,y = ternary.unzip(vertices)
            pyplot.fill(x, y, facecolor=fill_color, edgecolor='black')
    for i in range(steps+1):
        for j in range(steps - i-1):
            vertices = ternary.triangle_coordinates(i,j, alt=True)
            x,y = ternary.unzip(vertices)
            pyplot.fill(x, y, facecolor='w', edgecolor='black')
    ternary.draw_boundary(scale=steps, linewidth=1)

if __name__ == '__main__':
    pyplot.figure()
    ternary.draw_gridlines(20)
    pyplot.figure()
    heatmap_example(shannon_entropy, steps=100, boundary=True)
    pyplot.figure()
    func = dirichlet([6, 10, 13])
    heatmap_example(func, steps=100, boundary=False)
    pyplot.figure()
    points = []
    with open("curve.txt") as handle:
        for line in handle:
            points.append(map(float, line.split(' ')))
    ternary.plot(points, linewidth=2.0)
    ternary.draw_boundary()
    pyplot.show()

