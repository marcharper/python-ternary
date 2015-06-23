"""
Various Heatmaps.
"""

import functools
import numpy
from matplotlib import pyplot

from helpers import SQRT3, SQRT3OVER2, unzip, normalize, simplex_iterator, project_point
import plotting
from colormapping import get_cmap, colormapper, colorbar_hack


hexagon_deltas = generate_hexagon_deltas()

### Heatmap Triangulation Coordinates ###

## Triangular Heatmaps ##

def blend_value(data, i, j, k, keys=None):
    """Computes the average value of the three vertices of a triangule in the
    simplex triangulation, where two of the vertices are on the lower
    horizontal."""

    key_size = len(data.keys()[0])
    if not keys:
        keys = triangle_coordinates(i, j, k)
    # Reduce key from (i, j, k) to (i, j) if necessary
    keys = [tuple(key[:key_size]) for key in keys]

    # Sum over the values of the points to blend
    try:
        s = sum(data[key] for key in keys)
        value = s / 3.
    except KeyError:
        value = None
    return value

def alt_blend_value(data, i, j, k):
    """Computes the average value of the three vertices of a triangule in the
    simplex triangulation, where two of the vertices are on the upper
    horizontal."""

    keys = alt_triangle_coordinates(i, j, k)
    return blend_value(data, i, j, k, keys=keys)

def triangle_coordinates(i, j, k):
    """
    Computes coordinates of the constituent triangles of a triangulation for the
    simplex. These triangules are parallel to the lower axis on the lower side.

    Parameters
    ----------
    i,j,k: enumeration of the desired triangle

    Returns
    -------
    A numpy array of coordinates of the hexagon (unprojected)
    """

    return [(i, j, k), (i + 1, j, k - 1), (i, j + 1, k - 1)]

def alt_triangle_coordinates(i, j, k):
    """
    Computes coordinates of the constituent triangles of a triangulation for the
    simplex. These triangules are parallel to the lower axis on the upper side.

    Parameters
    ----------
    i,j,k: enumeration of the desired triangle

    Returns
    -------
    A numpy array of coordinates of the hexagon (unprojected)
    """

    return [(i, j + 1, k - 1), (i + 1, j + 1, k), (i + 1, j, k - 1)]

## Hexagonal Heatmaps ##

def generate_hexagon_deltas():
    """
    Generates a dictionary of the necessary additive vectors to generate the
    heaxagon points for the haxagonal heatmap.
    """

    zero = numpy.array([0, 0, 0])
    alpha = numpy.array([-1./3, 2./3, 0])
    deltaup = numpy.array([1./3, 1./3, 0])
    deltadown = numpy.array([2./3, -1./3, 0])
    i_vec = numpy.array([0, 1./2, -1./2])
    i_vec_down = numpy.array([1./2, -1./2, 0])
    deltaX_vec = numpy.array([1./2, 0, -1./2])

    d = dict()
    # Corner Points
    d["100"] = [zero, -deltaX_vec, -deltadown, -i_vec_down]
    d["010"] = [zero, i_vec_down, -alpha, -i_vec]
    d["001"] = [zero, i_vec, deltaup, deltaX_vec]
    # On the Edges
    d["011"] = [i_vec, deltaup, deltadown, -alpha, -i_vec]
    d["101"] = [-deltaX_vec, -deltadown, alpha, deltaup, deltaX_vec]
    d["110"] = [i_vec_down, -alpha, -deltaup, -deltadown, -i_vec_down]
    # Interior point
    d["111"] = [alpha, deltaup, deltadown, -alpha, -deltaup, -deltadown]

    return d

def hexagon_coordinates(i, j, k):
    """
    Computes coordinates of the constituent hexagons of a heaxagonal heatmap.

    Parameters
    ----------
    i, j, k: enumeration of the desired hexagon

    Returns
    -------
    A numpy array of coordinates of the hexagon (unprojected)
    """

    signature = ""
    for x in [i, j, k]:
        if x == 0:
            signature += "0"
        else:
            signature += "1"
    deltas = hexagon_deltas[signature]
    center = numpy.array([i, j, k])
    return numpy.array([center + x for x in deltas])

## Heatmaps ##

def polygon_generator(data, scale, style, permutation=None):
    """Generator for the vertices of the polygon to be colored and its color,
    depending on style. Called by heatmap."""

    # We'll project the coordinates inside this function to prevent
    # passing around permutation more than necessary
    project = functools.partial(project_point, permutation=permutation)

    for key, value in sorted(data.items()):
        if value is None:
            continue
        i = key[0]
        j = key[1]
        k = scale - i - j
        if style == 'h':
            vertices = hexagon_coordinates(i, j, k)
            yield (map(project, vertices), value)
        elif style == 'd':
            # Upright triangles
            vertices = triangle_coordinates(i, j, k)
            yield (map(project, vertices), value)
            # Upside-down triangles
            vertices = alt_triangle_coordinates(i, j, k)
            value = blend_value(data, i, j, k)
            yield (map(project, vertices), value)
        elif style == 't':
            # Upright triangles
            vertices = triangle_coordinates(i, j, k)
            value = blend_value(data, i, j, k)
            yield (map(project, vertices), value)
            # If not on the boundary add the upside-down triangle
            if i == scale:
                continue
            vertices = alt_triangle_coordinates(i, j, k)
            value = alt_blend_value(data, i, j, k)
            yield (map(project, vertices), value)

def heatmap(data, scale, vmin=None, vmax=None, cmap=None, ax=None,
            scientific=False, style='triangular', colorbar=True,
            permutation=None):
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
    permutation: string, None
        A permutation of the coordinates

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

    vertices_values = polygon_generator(data, scale, style,
                                       permutation=permutation)

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
             scientific=False, style='triangular', colorbar=True,
             permutation=None):
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
    permutation: string, None
        A permutation of the coordinates

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
                 scientific=scientific, colorbar=colorbar,
                 permutation=permutation)
    return ax
