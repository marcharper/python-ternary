import math

import matplotlib
import matplotlib.pyplot as pyplot
import seaborn as sns
import numpy as np

"""Matplotlib Ternary plotting utility."""

# # Constants ##

SQRT3OVER2 = math.sqrt(3) / 2.

## Use the default colormap of seaborn
DEFAULT_COLOR_MAP = sns.cubehelix_palette(as_cmap=True)

## Helpers ##
def unzip(l):
    return zip(*l)


def normalize(xs):
    """Normalize input list."""
    s = float(sum(xs))
    return [x / s for x in xs]

## Boundary ##

def draw_boundary(scale=1.0, linewidth=2.0, color='black', ax=None):
    # Plot boundary of 3-simplex.
    if not ax:
        ax = pyplot.subplot()
    scale = float(scale)
    # Note that the math.sqrt term is such to prevent noticable roundoff on the top corner point.
    ax.plot([0, scale, scale / 2, 0], [0, 0, math.sqrt(scale * scale * 3.) / 2, 0], color, linewidth=linewidth)
    ax.set_ylim((-0.05 * scale, .90 * scale))
    ax.set_xlim((-0.05 * scale, 1.05 * scale))
    return ax


## Curve Plotting ##
def project_point(p):
    """Maps (x,y,z) coordinates to planar-simplex."""
    a = p[0]
    b = p[1]
    c = p[2]
    x = 0.5 * (2 * b + c)
    y = SQRT3OVER2 * c
    return (x, y)


def project(s):
    """Maps (x,y,z) coordinates to planar-simplex."""
    # Is s an appropriate sequence or just a single point?
    try:
        return unzip(map(project_point, s))
    except TypeError:
        return project_point(s)
    except IndexError:  # for numpy arrays
        return project_point(s)


def plot(t, color=None, linewidth=1.0, ax=None):
    """Plots trajectory points where each point satisfies x + y + z = 1.
    First argument is a list or numpy array of tuples of length 3."""
    if not ax:
        ax = pyplot.subplot()
    xs, ys = project(t)
    if color:
        ax.plot(xs, ys, c=color, linewidth=linewidth)
    else:
        ax.plot(xs, ys, linewidth=linewidth)
    return ax


## Heatmaps##

def simplex_points(steps=100, boundary=True):
    """Systematically iterate through a lattice of points on the 2 dimensional
    simplex."""
    start = 0
    if not boundary:
        start = 1
    for x1 in range(start, steps + (1 - start)):
        for x2 in range(start, steps + (1 - start) - x1):
            x3 = steps - x1 - x2
            yield (x1, x2, x3)


def colormapper(x, a=0, b=1, cmap=None):
    """Maps color values to [0,1] and obtains rgba from the given color map for triangle coloring."""
    if b - a == 0:
        rgba = cmap(0)
    else:
        rgba = cmap((x - a) / float(b - a))
    rgba = np.array(rgba)
    rgba = rgba.flatten()
    hex_ = matplotlib.colors.rgb2hex(rgba)
    return hex_


def triangle_coordinates(i, j, alt=False):
    """Returns the ordered coordinates of the triangle vertices for i + j + k = N. Alt refers to the averaged triangles;
    the ordinary triangles are those with base  parallel to the axis on the lower end (rather than the upper end)"""
    # N = i + j + k
    if not alt:
        return [(i / 2. + j, i * SQRT3OVER2), (i / 2. + j + 1, i * SQRT3OVER2),
                (i / 2. + j + 0.5, (i + 1) * SQRT3OVER2)]
    else:
        # Alt refers to the inner triangles not covered by the default case
        return [(i / 2. + j + 1, i * SQRT3OVER2), (i / 2. + j + 1.5, (i + 1) * SQRT3OVER2),
                (i / 2. + j + 0.5, (i + 1) * SQRT3OVER2)]


# _rot_matrix = np.array([[3**.5/2, -1./2.], [1./2., 3**.5/2.]])
#
# def hex_coordinates(i, j):
# i_list = np.array([i + 1./2., i + 1./2., i         , i - 1./2., i - 1./2., i        ])
#     j_list = np.array([j - 1./2., j        , j + 1./2. , j + 1./2., j        , j - 1./2.])
#     x_y_list = i_j_to_x_y(i_list, j_list).T
#     # Rotate each by 30 degrees, as that gives us the correct hexagon
#
#     origin = i_j_to_x_y(i, j)
#     for zeta in range(x_y_list.shape[0]):
#         x_y_list[zeta] = np.dot(_rot_matrix, x_y_list[zeta] - origin)
#
#     print x_y_list
#     return x_y_list

def i_j_to_x_y(i, j):
    return np.array([i / 2. + j, SQRT3OVER2 * i])


_alpha = np.array([0, 1. / np.sqrt(3)])
_deltaup = np.array([1. / 2., 1. / (2. * np.sqrt(3))])
_deltadown = np.array([1. / 2., - 1. / (2. * np.sqrt(3))])

_i_vec = np.array([1. / 2., np.sqrt(3) / 2.])
_i_vec_down = np.array([1. / 2., -np.sqrt(3) / 2.])


def hex_coordinates(i, j, steps):
    ij = i_j_to_x_y(i, j)
    coords = np.array([ij + _alpha, ij + _deltaup, ij + _deltadown, ij - _alpha, ij - _deltaup, ij - _deltadown])
    if i == 0:
        # Along the base of the triangle
        if (j != steps) and (j != 0):  # Not a bizarre corner entity
            # Bound at y = zero
            deltaX_vec = np.array([_deltadown[0], 0])
            coords = np.array([ij - deltaX_vec, ij - _deltadown, ij + _alpha, ij + _deltaup, ij + deltaX_vec])
        else:
            coords = None
    if j == 0:
        # Along the left of the triangle
        if (i != steps) and (i != 0):  # Not a corner
            coords = np.array([ij + _i_vec / 2., ij + _deltaup, ij + _deltadown, ij - _alpha, ij - _i_vec / 2.])
        else:
            coords = None
    if i + j == steps:
        if (i != 0 ) and (j != 0):
            coords = np.array(
                [ij + _i_vec_down / 2., ij - _alpha, ij - _deltaup, ij - _deltadown, ij - _i_vec_down / 2.])
        else:
            coords = None

    return coords


def heatmap(d, steps, cmap_name=None, boundary=True, ax=None, scientific=False):
    """Plots values in the dictionary d as a heatmap. d is a dictionary of (i,j) --> c pairs where N = steps = i + j + k."""
    if not ax:
        ax = pyplot.subplot()
    if not cmap_name:
        cmap = DEFAULT_COLOR_MAP
    else:
        cmap = pyplot.get_cmap(cmap_name)
    a = min(d.values())
    b = max(d.values())
    # Color data triangles.

    for k, v in d.items():
        i, j = k
        vertices = hex_coordinates(i, j, steps)
        if vertices is not None:
            x, y = unzip(vertices)
            color = colormapper(d[i, j], a, b, cmap=cmap)
            ax.fill(x, y, facecolor=color, edgecolor=color)
    # # Color smoothing triangles. THIS IS BAD FOR US, NO SMOOTHING
    # offset = 0
    # if not boundary:
    # offset = 1
    # for i in range(offset, steps + 1 - offset):
    #     for j in range(offset, steps - i - offset):
    #         try:
    #             alt_color = (d[i, j + 1] + d[i + 1, j]) / 2.
    #             color = colormapper(alt_color, a, b, cmap=cmap)
    #             vertices = triangle_coordinates(i, j, alt=True)
    #             x, y = unzip(vertices)
    #             pyplot.fill(x, y, facecolor=color, edgecolor=color)
    #         except KeyError:
    #             # Allow for some portions to have no color, such as the boundary
    #             pass
    # Colorbar hack
    # http://stackoverflow.com/questions/8342549/matplotlib-add-colorbar-to-a-sequence-of-line-plots
    sm = pyplot.cm.ScalarMappable(cmap=cmap, norm=pyplot.Normalize(vmin=a, vmax=b))
    # Fake up the array of the scalar mappable. Urgh...
    sm._A = []
    cb = pyplot.colorbar(sm, ax=ax, format='%.3f')
    if scientific:
        cb.formatter = matplotlib.ticker.ScalarFormatter()
        cb.formatter.set_powerlimits((0, 0))
        cb.update_ticks()
    return ax


## Convenience Functions ##

def plot_heatmap(func, steps=40, boundary=True, cmap_name=None, ax=None):
    """Computes func on heatmap coordinates and plots heatmap. In other words, computes the function on sample points
    of the simplex (normalized points) and creates a heatmap from the values."""
    d = dict()
    for x1, x2, x3 in simplex_points(steps=steps, boundary=boundary):
        d[(x1, x2)] = func(normalize([x1, x2, x3]))
    heatmap(d, steps, cmap_name=cmap_name, ax=ax)


def plot_multiple(trajectories, linewidth=2.0, ax=None):
    """Plots multiple trajectories and the boundary."""
    if not ax:
        ax = pyplot.subplot()
    for t in trajectories:
        plot(t, linewidth=linewidth, ax=ax)
    draw_boundary(ax=ax)
    return ax
