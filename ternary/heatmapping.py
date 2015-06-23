"""
Various Heatmaps.
"""

import numpy
from matplotlib import pyplot

from helpers import SQRT3, SQRT3OVER2, unzip, normalize, simplex_iterator, project_point
import plotting
from colormapping import get_cmap, colormapper, colorbar_hack

### Heatmap Triangulation Coordinates ###

## Triangular Heatmaps ##

def blend_value(data, i, j, k=None, keys=None):
    """Computes the average value of the three vertices of a triangule in the
    simplex triangulation, where two of the vertices are on the lower
    horizontal."""

    key_size = len(data.keys()[0])
    if not keys:
        keys = [(i, j, k), (i, j + 1, k - 1), (i + 1, j, k - 1)]
    # Reduce key from (i, j, k) to (i, j) if necessary
    keys = [tuple(key[:key_size]) for key in keys]

    # Sum over the values of the points to blend
    try:
        s = sum(data[key] for key in keys)
        value = s / 3.
    except KeyError:
        value = None
    return value

def alt_blend_value(data, i, j, k=None):
    """Computes the average value of the three vertices of a triangule in the
    simplex triangulation, where two of the vertices are on the upper
    horizontal."""

    keys = [(i, j, k), (i, j + 1, k - 1), (i + 1, j - 1, k)]
    return blend_value(data, i, j, k, keys=keys)

def triangle_coordinates(i, j, k=None):
    """
    Computes coordinates of the constituent triangles of a triangulation for the
    simplex. These triangules are parallel to the lower axis on the lower side.

    Parameters
    ----------
    i,j,k: enumeration of the desired triangle

    Returns
    -------
    A numpy array of coordinates of the hexagon
    """

    return map(project_point, [(j, i), (j + 1, i), (j, i + 1)])

def alt_triangle_coordinates(i, j, k=None):
    """
    Computes coordinates of the constituent triangles of a triangulation for the
    simplex. These triangules are parallel to the lower axis on the upper side.

    Parameters
    ----------
    i,j,k: enumeration of the desired triangle

    Returns
    -------
    A numpy array of coordinates of the hexagon
    """

    return map(project_point, [(j + 1, i), (j + 1, i + 1), (j, i+1)])

## Hexagonal Heatmaps ##
## Original Hexagonal heatmap code submitted by https://github.com/btweinstein
# Hexagonal heatmaps do no smooth the colors as in the triangular case.

_alpha = numpy.array([0, 1. / SQRT3])
_deltaup = numpy.array([1. / 2., 1. / (2. * SQRT3)])
_deltadown = numpy.array([1. / 2., - 1. / (2. * SQRT3)])
_i_vec = numpy.array([1. / 2., SQRT3 / 2.])
_i_vec_down = numpy.array([1. / 2., -SQRT3 / 2.])
_deltaX_vec = numpy.array([1. / 2, 0])

def hexagon_coordinates(i, j, k):
    """
    Computes coordinates of the constituent hexagons of a heaxagonal heatmap.

    Parameters
    ----------
    i, j, k: enumeration of the desired hexagon

    Returns
    -------
    A numpy array of coordinates of the hexagon
    """

    steps = i + j + k
    ij = numpy.array([i / 2. + j, SQRT3 / 2 * i])

    # Corner cases (literally)
    if i == steps: # j == k == 0
        coords = [ij, ij + _i_vec_down / 2., ij - _alpha, ij - _i_vec / 2.]
    elif k == steps: # i == j == 0
        coords = [ij, ij + _i_vec / 2., ij + _deltaup, ij + _deltaX_vec]
    elif j == steps: # i == k == 0
        coords = [ij, ij - _deltaX_vec, ij - _deltadown, ij - _i_vec_down / 2.]
    # Now the edges
    elif i == 0:
        coords = [ij - _deltaX_vec, ij - _deltadown,
                  ij + _alpha, ij + _deltaup, ij + _deltaX_vec]
    elif j == 0:
        coords = [ij + _i_vec / 2., ij + _deltaup, ij + _deltadown,
                  ij - _alpha, ij - _i_vec / 2.]
    elif k == 0:
        coords = [ij + _i_vec_down / 2., ij - _alpha, ij - _deltaup,
                  ij - _deltadown, ij - _i_vec_down / 2.]
    # Must be an interior point
    else:
        coords = [ij + _alpha, ij + _deltaup, ij + _deltadown,
                  ij - _alpha, ij - _deltaup, ij - _deltadown]

    return numpy.array(coords)

## Heatmaps ##

def polygon_iterator(data, scale, style):
    """Iterator for the vertices of the polygon to be colored and its color,
    depending on style. Called by heatmap."""

    for key, value in sorted(data.items()):
        if value is None:
            continue
        i = key[0]
        j = key[1]
        k = scale - i - j
        if style == 'h':
            vertices = hexagon_coordinates(i, j, k)
            yield (vertices, value)
        elif style == 'd':
            # Upright triangles
            vertices = triangle_coordinates(i, j, k)
            yield (vertices, value)
            # Upside-down triangles
            vertices = alt_triangle_coordinates(i, j, k)
            value = blend_value(data, i, j, k)
            yield (vertices, value)
        elif style == 't':
            # Upright triangles
            vertices = triangle_coordinates(i, j, k)
            value = blend_value(data, i, j, k)
            yield (vertices, value)
            # If not on the boundary add the upside-down triangle
            if (j == 0) or (j == scale):
                continue
            vertices = alt_triangle_coordinates(i, j - 1, k + 1)
            value = alt_blend_value(data, i, j, k)
            yield (vertices, value)

def heatmap(data, scale, vmin=None, vmax=None, cmap=None, ax=None,
            scientific=False, style='triangular', colorbar=True):
    """
    Plots heatmap of given color values.

    Parameters
    ----------
    data: dictionary
        A dictionary mapping the i, j polygon to the heatmap color, where
        i + j + k = scale.
    scale: Integer
        The scale used to partition the simplex.
    vmin: float, None
        The minimum color value, used to normalize colors. Computed if absent.
    vmax: float, None
        The maximum color value, used to normalize colors. Computed if absent.
    cmap: String or matplotlib.colors.Colormap, None
        The name of the Matplotlib colormap to use.
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    scientific: Bool, False
        Whether to use scientific notation for colorbar numbers.
    style: String, "triangular"
        The style of the heatmap, "triangular", "dual-triangular" or "hexagonal"
    colorbar: bool, True
        Show colorbar.

    Returns
    -------
    ax: The matplotlib axis
    """

    if not ax:
        fig, ax = pyplot.subplots()
    cmap = get_cmap(cmap)
    if not vmin:
        vmin = min(data.values())
    if not vmax:
        vmax = max(data.values())
    style = style.lower()[0]
    if style not in ["t", "h", 'd']:
        raise ValueError("Heatmap style must be 'triangular', 'dual-triangular', or 'hexagonal'")

    vertices_values = polygon_iterator(data, scale, style=style)

    # Draw the polygons and color them
    for vertices, value in vertices_values:
        if value is None:
            continue
        color = colormapper(value, vmin, vmax, cmap=cmap)
        # Matplotlib wants a list of xs and a list of ys
        xs, ys = unzip(vertices)
        ax.fill(xs, ys, facecolor=color, edgecolor=color)

    if colorbar:
        colorbar_hack(ax, vmin, vmax, cmap, scientific=scientific)
    return ax

## User Convenience Functions ##

def heatmapf(func, scale=10, boundary=True, cmap=None, ax=None,
             scientific=False, style='triangular', colorbar=True):
    """
    Computes func on heatmap partition coordinates and plots heatmap. In other
    words, computes the function on lattice points of the simplex (normalized
    points) and creates a heatmap from the values.

    Parameters
    ----------
    func: Function
        A function of 3-tuples to be heatmapped
    scale: Integer
        The scale used to partition the simplex
    boundary: Bool, True
        Include the boundary points or not
    cmap: String, None
        The name of the Matplotlib colormap to use
    ax: Matplotlib axis object, None
        The axis to draw the colormap on
    style: String, "triangular"
        The style of the heatmap, "triangular", "dual-triangular" or "hexagonal"
    scientific: Bool, False
        Whether to use scientific notation for colorbar numbers.
    colorbar: bool, True
        Show colorbar.

    Returns
    -------
    ax, The matplotlib axis
    """

    # Apply the function to a simplex partition
    data = dict()
    for i, j, k in simplex_iterator(scale=scale, boundary=boundary):
        data[(i, j)] = func(normalize([i, j, k]))
    # Pass everything to the heatmapper
    ax = heatmap(data, scale, cmap=cmap, ax=ax, style=style,
                           scientific=scientific, colorbar=colorbar)
    return ax
