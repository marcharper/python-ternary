"""
Various Heatmaps.
"""

import functools
import numpy
from matplotlib import pyplot

from .helpers import unzip, normalize, simplex_iterator, project_point
from .colormapping import get_cmap, colormapper, colorbar_hack

### Heatmap Triangulation Coordinates

## Triangular Heatmaps


def blend_value(data, i, j, k, keys=None):
    """Computes the average value of the three vertices of a triangle in the
    simplex triangulation, where two of the vertices are on the lower
    horizontal."""

    key_size = len(list(data.keys())[0])
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
    """Computes the average value of the three vertices of a triangle in the
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

    return [(i, j + 1, k - 1), (i + 1, j, k - 1), (i + 1, j + 1, k - 2)]


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


hexagon_deltas = generate_hexagon_deltas()


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

    if isinstance(data, dict):
        data_gen = data.items()
    else:
        # Only works with style == 'h'
        data_gen = data

    for key, value in data_gen:
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
            if (i <= scale) and (j <= scale) and (k >= 0):
                vertices = triangle_coordinates(i, j, k)
                yield (map(project, vertices), value)
            # Upside-down triangles
            if (i < scale) and (j < scale) and (k >= 1):
                vertices = alt_triangle_coordinates(i, j, k)
                value = blend_value(data, i, j, k)
                yield (map(project, vertices), value)
        elif style == 't':
            # Upright triangles
            if (i < scale) and (j < scale) and (k > 0):
                vertices = triangle_coordinates(i, j, k)
                value = blend_value(data, i, j, k)
                yield (map(project, vertices), value)
            # If not on the boundary add the upside-down triangle
            if (i < scale) and (j < scale) and (k > 1):
                vertices = alt_triangle_coordinates(i, j, k)
                value = alt_blend_value(data, i, j, k)
                yield (map(project, vertices), value)


def heatmap(data, scale, vmin=None, vmax=None, cmap=None, ax=None,
            scientific=False, style='triangular', colorbar=True,
            permutation=None, use_rgba=False, cbarlabel=None, cb_kwargs=None):
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
    use_rgba: bool, False
        Use rgba color values
    cbarlabel: string, None
        Text label for the colorbar
    cb_kwargs: dict
        dict of kwargs to pass to colorbar

    Returns
    -------
    ax: The matplotlib axis
    """

    if not ax:
        fig, ax = pyplot.subplots()
    # If use_rgba, make the RGBA values numpy arrays so that they can
    # be averaged.
    if use_rgba:
        for k, v in data.items():
            data[k] = numpy.array(v)
    else:
        cmap = get_cmap(cmap)
        if vmin is None:
            vmin = min(data.values())
        if vmax is None:
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
        if not use_rgba:
            color = colormapper(value, vmin, vmax, cmap=cmap)
        else:
            color = value  # rgba tuple (r,g,b,a) all in [0,1]
        # Matplotlib wants a list of xs and a list of ys
        xs, ys = unzip(vertices)
        ax.fill(xs, ys, facecolor=color, edgecolor=color)

    if not cb_kwargs:
        cb_kwargs = dict()
    if colorbar:
        colorbar_hack(ax, vmin, vmax, cmap, scientific=scientific,
                      cbarlabel=cbarlabel, **cb_kwargs)
    return ax


## User Convenience Functions ##


def heatmapf(func, scale=10, boundary=True, cmap=None, ax=None,
             scientific=False, style='triangular', colorbar=True,
             permutation=None, vmin=None, vmax=None, cbarlabel=None,
             cb_kwargs=None):
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
    vmin: float
        The minimum color value, used to normalize colors.
    vmax: float
        The maximum color value, used to normalize colors.
    cb_kwargs: dict
        dict of kwargs to pass to colorbar

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
                 permutation=permutation, vmin=vmin, vmax=vmax, 
                 cbarlabel=cbarlabel, cb_kwargs=cb_kwargs)
    return ax


def svg_polygon(coordinates, color):
    """
    Create an svg triangle for the stationary heatmap.

    Parameters
    ----------
    coordinates: list
        The coordinates defining the polygon
    color: string
        RGB color value e.g. #26ffd1

    Returns
    -------
    string, the svg string for the polygon
    """

    coord_str = []
    for c in coordinates:
        coord_str.append(",".join(map(str, c)))
    coord_str = " ".join(coord_str)
    polygon = '<polygon points="%s" style="fill:%s;stroke:%s;stroke-width:0"/>\n' % (coord_str, color, color)
    return polygon


def svg_heatmap(data, scale, filename, vmax=None, vmin=None, style='h',
                permutation=None, cmap=None):
    """
    Create a heatmap in SVG format. Intended for use with very large datasets,
    which would require large amounts of RAM using matplotlib. You can convert
    the image to another format with e.g. ImageMagick:

    convert -density 1200 -resize -rotate 180 1000x1000 your.svg your.png

    Parameters
    ----------

    data: dictionary or k, v generator
        A dictionary mapping the i, j polygon to the heatmap color, where
        i + j + k = scale. If using a generator, style must be 'h'.
    scale: Integer
        The scale used to partition the simplex.
    filename: string
        The filename to write the SVG data to.
    vmin: float
        The minimum color value, used to normalize colors.
    vmax: float
        The maximum color value, used to normalize colors.
    cmap: String or matplotlib.colors.Colormap, None
        The name of the Matplotlib colormap to use.
    style: String, "h"
        The style of the heatmap, "triangular", "dual-triangular" or "hexagonal"
    permutation: string, None
        A permutation of the coordinates
    """

    style = style.lower()[0]
    if style not in ["t", "h", 'd']:
        raise ValueError("Heatmap style must be 'triangular', 'dual-triangular', or 'hexagonal'")

    if not isinstance(data, dict):
        if not style == 'h':
            raise ValueError("Data can only be given as a generator for hexagonal style heatmaps because of blending for adjacent polygons.")
        elif vmax is None or vmin is None:
            raise ValueError("vmax and vmin must be supplied for data given as a generator.")

    cmap = get_cmap(cmap)

    if not vmin:
        vmin = min(data.values())
    if not vmax:
        vmax = max(data.values())

    height = scale * numpy.sqrt(3) / 2 + 2

    output_file = open(filename, 'w')
    output_file.write('<svg height="%s" width="%s">\n' % (height, scale))

    vertices_values = polygon_generator(data, scale, style,
                                        permutation=permutation)

    # Draw the polygons and color them
    for vertices, value in vertices_values:
        color = colormapper(value, vmin, vmax, cmap=cmap)
        output_file.write(svg_polygon(vertices, color))

    output_file.write('</svg>\n')
