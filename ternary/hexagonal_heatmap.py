import math
import numpy as numpy
from matplotlib import pyplot

SQRT3OVER2 = math.sqrt(3) / 2.

def i_j_to_x_y(i, j):
    return numpy.array([i / 2. + j, SQRT3OVER2 * i])

_alpha = numpy.array([0, 1. / numpy.sqrt(3)])
_deltaup = numpy.array([1. / 2., 1. / (2. * numpy.sqrt(3))])
_deltadown = numpy.array([1. / 2., - 1. / (2. * numpy.sqrt(3))])

_i_vec = numpy.array([1. / 2., numpy.sqrt(3) / 2.])
_i_vec_down = numpy.array([1. / 2., -numpy.sqrt(3) / 2.])

_deltaX_vec = numpy.array([_deltadown[0], 0])

def hex_coordinates(i, j, steps):
    ij = i_j_to_x_y(i, j)
    coords = numpy.array([ij + _alpha, ij + _deltaup, ij + _deltadown, ij - _alpha, ij - _deltaup, ij - _deltadown])
    if i == 0:
        # Along the base of the triangle
        if (j != steps) and (j != 0):  # Not a bizarre corner entity
            # Bound at y = zero
            coords = numpy.array([ij - _deltaX_vec, ij - _deltadown, ij + _alpha, ij + _deltaup, ij + _deltaX_vec])

    if j == 0:
        # Along the left of the triangle
        if (i != steps) and (i != 0):  # Not a corner
            coords = numpy.array([ij + _i_vec / 2., ij + _deltaup, ij + _deltadown, ij - _alpha, ij - _i_vec / 2.])

    if i + j == steps:
        # Along the right of the triangle
        if (i != 0 ) and (j != 0):
            coords = numpy.array(
                [ij + _i_vec_down / 2., ij - _alpha, ij - _deltaup, ij - _deltadown, ij - _i_vec_down / 2.])

    # Deal with pathological border cases
    if i == steps and j == 0:
        coords = numpy.array([ij, ij + _i_vec_down / 2., ij - _alpha, ij - _i_vec / 2.])
    if i == 0 and j == 0:
        coords = numpy.array([ij, ij + _i_vec / 2., ij + _deltaup, ij + _deltaX_vec])
    if j == steps and i == 0:
        coords = numpy.array([ij, ij - _deltaX_vec, ij - _deltadown, ij - _i_vec_down / 2.])

    return coords

def hexagonal_heatmap(d, steps, cmap_name=None, boundary=True, ax=None, scientific=False, min_max_scale=None):
    """Plots values in the dictionary d as a heatmap. d is a dictionary of (i,j) --> c pairs where N = steps = i + j + k."""
    if not ax:
        ax = pyplot.subplot()
    if not cmap_name:
        cmap = DEFAULT_COLOR_MAP
    else:
        cmap = pyplot.get_cmap(cmap_name)
    if min_max_scale is None:
        a = min(d.values())
        b = max(d.values())
    else:
        a = min_max_scale[0]
        b = min_max_scale[1]
    # Color data triangles.

    for k, v in d.items():
        i, j = k
        vertices = hex_coordinates(i, j, steps)
        if vertices is not None:
            x, y = unzip(vertices)
            color = colormapper(d[i, j], a, b, cmap=cmap)
            ax.fill(x, y, facecolor=color, edgecolor=color)

    # Colorbar hack
    # http://stackoverflow.com/questions/8342549/matplotlib-add-colorbar-to-a-sequence-of-line-plots
    sm = pyplot.cm.ScalarMappable(cmap=cmap, norm=pyplot.Normalize(vmin=a, vmax=b))

    # Fake up the array of the scalar mappable. Urgh...
    sm._A = []
    cb = pyplot.colorbar(sm, ax=ax, format='%.4f')
    cb.locator = matplotlib.ticker.LinearLocator(numticks=7)
    if scientific:
        cb.formatter = matplotlib.ticker.ScalarFormatter()
        cb.formatter.set_powerlimits((0, 0))
    cb.update_ticks()
    return ax