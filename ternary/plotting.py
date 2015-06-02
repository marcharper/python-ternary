import math
import numpy

import matplotlib
import matplotlib.pyplot as pyplot
from matplotlib.lines import Line2D

from hexagonal import hexagon_coordinates

"""Matplotlib Ternary plotting utility."""

## Constants ##

SQRT3OVER2 = math.sqrt(3) / 2.

## Default colormap, other options here: http://www.scipy.org/Cookbook/Matplotlib/Show_colormaps
DEFAULT_COLOR_MAP_NAME = 'jet'

def get_cmap(cmap_name=DEFAULT_COLOR_MAP_NAME):
    """Loads a matplotlib colormap if specified or supplies the default."""
    return pyplot.get_cmap(cmap_name)

## Helpers ##

def unzip(l):
    return zip(*l)

def normalize(xs):
    """Normalize input list."""
    s = float(sum(xs))
    if s == 0:
        raise ValueError("Cannot normalize list with sum 0")
    return [x / s for x in xs]

## Ternary Projections ##

def project_point(p):
    """Maps (x,y,z) coordinates to planar-simplex."""
    a, b, c = p
    x = b + c/2.
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

## Boundary, Gridlines, Sizing ##

def resize_drawing_canvas(ax, scale):
    """Makes sure the drawing surface is large enough to display projected content."""
    ax.set_ylim((-0.05 * scale, .90 * scale))
    ax.set_xlim((-0.05 * scale, 1.05 * scale))

def draw_line(ax, p1, p2, **kwargs):
    ax.add_line(Line2D((p1[0], p2[0]), (p1[1], p2[1]), **kwargs))

def draw_horizontal_line(ax, scale, i,   **kwargs):
    p1 = project_point((0, scale-i, i))
    p2 = project_point((scale-i, 0, i))
    draw_line(ax, p1, p2, **kwargs)

def draw_left_parallel_line(ax, scale, i,  **kwargs):
    p1 = project_point((0, i, scale-i))
    p2 = project_point((scale-i, i, 0))
    draw_line(ax, p1, p2, **kwargs)

def draw_right_parallel_line(ax, scale, i, **kwargs):
    p1 = project_point((i, scale-i, 0))
    p2 = project_point((i, 0, scale-i))
    draw_line(ax, p1, p2, **kwargs)

def draw_boundary(scale=1.0, ax=None, **kwargs):
    """Plots the boundary of the simplex. Creates and returns matplotlib axis if none given."""
    if not ax:
        ax = pyplot.subplot()
    scale = float(scale)
    resize_drawing_canvas(ax, scale)
    draw_horizontal_line(ax, scale, 0, **kwargs)
    draw_left_parallel_line(ax, scale, 0, **kwargs)
    draw_right_parallel_line(ax, scale, 0, **kwargs)
    return ax

def draw_gridlines(scale=1., multiple=None, ax=None, **kwargs):
    """Plots grid lines excluding boundary. Creates and returns matplotlib axis if none given."""
    if not ax:
        ax = pyplot.subplot()
    if 'linewidth' not in kwargs:
        kwargs["linewidth"] = 0.5
    if 'linestyle' not in kwargs:
        kwargs["linestyle"] = ':'
    resize_drawing_canvas(ax, scale)
    ## Draw grid-lines
    if multiple:
        # Parallel to horizontal axis
        for i in numpy.arange(0, scale, multiple):
            draw_horizontal_line(ax, scale, i, **kwargs)
        # Parallel to left and right axes
        for i in numpy.arange(0, scale + multiple, multiple):
            draw_left_parallel_line(ax, scale, i, **kwargs)
            draw_right_parallel_line(ax, scale, i, **kwargs)
    return ax

def clear_matplotlib_ticks(ax, axis="both"):
    if axis.lower() in ["both", "x", "horizontal"]:
        ax.set_xticks([], [])
    if axis.lower() in ["both", "y", "vertical"]:
        ax.set_yticks([], [])
    pass

## Curve Plotting ##

def plot(t, ax=None, **kwargs):
    """Plots trajectory points where each point satisfies x + y + z = scale. First argument is a list or numpy array of tuples of length 3."""
    if not ax:
        ax = pyplot.subplot()
    xs, ys = project(t)
    ax.plot(xs, ys, **kwargs)
    return ax

## Heatmaps##

# Matplotlib Colormapping

def colormapper(x, a=0, b=1, cmap=None):
    """Maps color values to [0,1] and obtains rgba from the given color map for triangle coloring."""
    if not cmap:
        cmap = get_cmap()
    if b - a == 0:
        rgba = cmap(0)
    else:
        rgba = cmap((x - a) / float(b - a))
    #rgba = numpy.array(rgba)
    #rgba = rgba.flatten()
    hex_ = matplotlib.colors.rgb2hex(rgba)
    return hex_

def colorbar_hack(ax, vmin, vmax, cmap, scientific=False):
    """Colorbar hack to insert colorbar on ternary plot."""
    # http://stackoverflow.com/questions/8342549/matplotlib-add-colorbar-to-a-sequence-of-line-plots
    sm = pyplot.cm.ScalarMappable(cmap=cmap, norm=pyplot.Normalize(vmin=vmin, vmax=vmax))
    # Fake up the array of the scalar mappable. Urgh...
    sm._A = []
    cb = pyplot.colorbar(sm, ax=ax, format='%.4f')
    cb.locator = matplotlib.ticker.LinearLocator(numticks=7)
    if scientific:
        cb.formatter = matplotlib.ticker.ScalarFormatter()
        cb.formatter.set_powerlimits((0, 0))
    cb.update_ticks()

# Triangular Coordinates and Vertices

def simplex_points(scale=100, boundary=True):
    """Systematically iterate through a lattice of points on the 2 dimensional
    simplex."""
    start = 0
    if not boundary:
        start = 1
    for i in range(start, scale + (1 - start)):
        for j in range(start, scale + (1 - start) - i):
            k = scale - i - j
            yield (i, j, k)

def triangle_coordinates(i, j, k=None):
    """Returns the ordered coordinates of the triangle vertices for i + j + k = scale, parallel to the horizontal axis on the lower end"""
    return [(i / 2. + j, i * SQRT3OVER2), (i / 2. + j + 1, i * SQRT3OVER2),
                (i / 2. + j + 0.5, (i + 1) * SQRT3OVER2)]

def alt_triangle_coordinates(i, j, k=None):
    """Returns the ordered coordinates of the triangle vertices for i + j + k = scaleparallel to the horizontal axis on the upper end (for color blending)"""
    return [(i/2. + j + 1, i * SQRT3OVER2), (i/2. + j + 1.5, (i + 1) * SQRT3OVER2), (i/2. + j + 0.5, (i + 1) * SQRT3OVER2)]

def alt_value_iterator(d):
    """Compute the average of the neighboring triangles for smoothing."""
    for key in d.keys():
        i, j = key
        try:
            value = (d[i,j] + d[i, j + 1] + d[i + 1, j]) / 3.
        except KeyError:
            value = None
        yield key, value

def heatmap(d, scale, vmin=None, vmax=None, cmap_name=None, ax=None, scientific=False, style='triangular', colorbar=True):
    """Plots values in the dictionary d as a heatmap. d is a dictionary of (i,j) --> c pairs where N = scale = i + j + k. Uses triangles for heatmap and blends surrounding triangles to fill the unspecified triangles or hexagons, as specified by the style argument (must be either 'triangular' or 'hexagonal'."""
    if not ax:
        ax = pyplot.subplot()
    cmap = get_cmap(cmap_name)
    if not vmin:
        vmin = min(d.values())
    if not vmax:
        vmax = max(d.values())
    style = style.lower()
    if style not in ["triangular", "hexagonal"]:
        raise ValueError("Heatmap style must be 'triangular' or 'hexagonal'. Default is triangular.")

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
                x, y = unzip(vertices)
                ax.fill(x, y, facecolor=color, edgecolor=color)

    if colorbar:
        colorbar_hack(ax, vmin, vmax, cmap, scientific=scientific)
    return ax

def scatter(points, scale=1., ax=None, **kwargs):
    """Plots trajectory points where each point satisfies x + y + z = scale. First argument is a list or numpy array of tuples of length 3."""
    if not ax:
        ax = pyplot.subplot()
    xs, ys = project(points)
    ax.scatter(xs, ys, **kwargs)
    return ax

## User Convenience Functions ##

def function_heatmap(func, scale=40, boundary=True, cmap_name=None, ax=None, style="triangular"):
    """Computes func on heatmap partition coordinates and plots heatmap. In other words, computes the function on sample points of the simplex (normalized points) and creates a heatmap from the values."""
    d = dict()
    for i, j, k in simplex_points(scale=scale, boundary=boundary):
        d[(i, j)] = func(normalize([i, j, k]))
    ax = heatmap(d, scale, cmap_name=cmap_name, ax=ax, style=style)
    return ax

def plot_multiple(trajectories, linewidth=2.0, ax=None):
    """Plots multiple trajectories and the boundary. Trajectory is a list of lists of tuples (x1, x2, x3) where x1+x2+x3=1"""
    if not ax:
        ax = pyplot.subplot()
    for t in trajectories:
        plot(t, linewidth=linewidth, ax=ax)
    draw_boundary(ax=ax)
    return ax
