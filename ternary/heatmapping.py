
import matplotlib
import matplotlib.pyplot as pyplot
from matplotlib.colors import rgb2hex
import numpy

from helpers import SQRT3, SQRT3OVER2, unzip, normalize, simplex_iterator
from plotting import new_axes_subplot

## Default colormap, other options here: http://www.scipy.org/Cookbook/Matplotlib/Show_colormaps
DEFAULT_COLOR_MAP_NAME = 'jet'

## Matplotlib Colormapping ##

def get_cmap(cmap_name=None):
    """
    Loads a matplotlib colormap if specified or supplies the default.

    Parameters
    ----------
    cmap_name, string
        The name of the Matplotlib colormap to look up.

    Returns
    -------
    The desired Matplotlib colormap

    Raises
    ------
    ValueError if colormap name is not recognized by Matplotlib
    """

    if not cmap_name:
        cmap_name = DEFAULT_COLOR_MAP_NAME
    return pyplot.get_cmap(cmap_name)

def colormapper(value, lower=0, upper=1, cmap=None):
    """
    Maps values to colors by normalizing within [a,b], obtaining rgba from the
    given matplotlib color map for heatmap polygon coloring.

    Parameters
    ----------
    x: float
        The value to be colormapped
    a: float
        Lower bound of colors
    b: float
        Upper bound of colors
    cmap, Matplotlib Colormap Object (optional)
        Colormap object to prevent repeated lookup

    Returns
    -------
    hex_, float
        The value mapped to an appropriate RGBA color value
    """

    if not cmap:
        cmap = get_cmap()
    if upper - lower == 0:
        rgba = cmap(0)
    else:
        rgba = cmap((value - lower) / float(upper - lower))
    hex_ = rgb2hex(rgba)
    return hex_

def colorbar_hack(axes_subplot, vmin, vmax, cmap, scientific=False):
    """Colorbar hack to insert colorbar on ternary plot. Called by heatmap, 
    not intended for direct usage."""
    # http://stackoverflow.com/questions/8342549/matplotlib-add-colorbar-to-a-sequence-of-line-plots
    norm = pyplot.Normalize(vmin=vmin, vmax=vmax)
    sm = pyplot.cm.ScalarMappable(cmap=cmap, norm=norm)
    # Fake up the array of the scalar mappable. Urgh...
    sm._A = []
    cb = pyplot.colorbar(sm, ax=axes_subplot, format='%.4f')
    cb.locator = matplotlib.ticker.LinearLocator(numticks=7)
    if scientific:
        cb.formatter = matplotlib.ticker.ScalarFormatter()
        cb.formatter.set_powerlimits((0, 0))
    cb.update_ticks()

### Heatmap Triangulation Coordinates ###

## Triangular Heatmaps ##

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

    return [(i / 2. + j, i * SQRT3OVER2), (i / 2. + j + 1, i * SQRT3OVER2),
                (i / 2. + j + 0.5, (i + 1) * SQRT3OVER2)]

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

    return [(i/2. + j + 1, i * SQRT3OVER2),
            (i/2. + j + 1.5, (i + 1) * SQRT3OVER2),
            (i/2. + j + 0.5, (i + 1) * SQRT3OVER2)]

def alt_value_iterator(d):
    """
    Compute the average of the neighboring triangles for smoothing. These are
    the colors of the alternative triangles. Called by heatmap, not intended
    for direct usage.
    """
    for key in d.keys():
        i, j = key
        try:
            value = (d[i,j] + d[i, j + 1] + d[i + 1, j]) / 3.
        except KeyError:
            value = None
        yield key, value

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
    i,j,k: enumeration of the desired hexagon

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

def heatmap(d, scale, vmin=None, vmax=None, cmap_name=None, axes_subplot=None,
            scientific=False, style='triangular', colorbar=True):
    """
    Plots heatmap of given color values.

    Parameters
    ----------
    d: dictionary
        A dictionary mapping the i, j polygon to the heatmap color, where
        i + j + k = scale.
    scale: Integer
        The scale used to partition the simplex.
    vmin: float, None
        The minimum color value, used to normalize colors. Computed if absent.
    vmax: float, None
        The maximum color value, used to normalize colors. Computed if absent.
    cmap_name: String, None
        The name of the Matplotlib colormap to use.
    axes_subplot: Matplotlib AxesSubplot, None
        The subplot to draw on.
    scientific: Bool, False
        Whether to use scientific notation for colorbar numbers.
    style: String, "triangular"
        The style of the heatmap, "triangular" or "hexagonal".
    colorbar: bool, True
        Show colorbar.

    Returns
    -------
    axes_subplot, The matplotlib axis
    """
    
    if not axes_subplot:
        axes_subplot = new_axes_subplot()
    cmap = get_cmap(cmap_name)
    if not vmin:
        vmin = min(d.values())
    if not vmax:
        vmax = max(d.values())
    style = style.lower()
    if style not in ["triangular", "hexagonal"]:
        raise ValueError("Heatmap style must be 'triangular' or 'hexagonal'")
    if style == "hexagonal":
        mapping_functions = [(hexagon_coordinates, d.items())]
    else:
        mapping_functions = [(triangle_coordinates, d.items()), (alt_triangle_coordinates, alt_value_iterator(d))]

    # Color data triangles or hexagons
    for vertex_function, iterator in mapping_functions:
        for key, value in iterator:
            if value is not None:
                i, j = key
                k = scale - i - j
                vertices = vertex_function(i, j, k)
                color = colormapper(value, vmin, vmax, cmap=cmap)
                # Matplotlib wants a list of xs and a list of ys
                xs, ys = unzip(vertices)
                axes_subplot.fill(xs, ys, facecolor=color, edgecolor=color)

    if colorbar:
        colorbar_hack(axes_subplot, vmin, vmax, cmap, scientific=scientific)
    return axes_subplot

## User Convenience Functions ##

def heatmap_of_function(func, scale=10, boundary=True, cmap_name=None,
                        axes_subplot=None, style="triangular"):
    """
    Computes func on heatmap partition coordinates and plots heatmap. In other words, computes the function on lattice points of the simplex (normalized points) and creates a heatmap from the values.
    
    Parameters
    ----------
    func: Function
        A function of 3-tuples to be heatmapped
    scale: Integer
        The scale used to partition the simplex
    boundary: Bool, True
        Include the boundary points or not
    cmap_name: String, None
        The name of the Matplotlib colormap to use
    ax: Matplotlib axis object, None
        The axis to draw the colormap on
    style: String, "triangular"
        The style of the heatmap, "triangular" or "hexagonal"

    Returns
    -------
    ax, The matplotlib axis
    """

    # Apply the function to a simplex partition
    d = dict()
    for i, j, k in simplex_iterator(scale=scale, boundary=boundary):
        d[(i, j)] = func(normalize([i, j, k]))
    # Pass everything to the heatmapper
    axes_subplot = heatmap(d, scale, cmap_name=cmap_name,
                           axes_subplot=axes_subplot, style=style)
    return axes_subplot

