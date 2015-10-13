"""
Plotting functions: scatter, plot (curves), axis labelling.
"""

from functools import partial

import matplotlib
from matplotlib import pyplot
import numpy as np

from .helpers import project_sequence, project_point
from .colormapping import get_cmap

### Drawing Helpers ###

def resize_drawing_canvas(ax, scale=1.):
    """
    Makes sure the drawing surface is large enough to display projected
    content.

    Parameters
    ----------
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    scale: float, 1.0
        Simplex scale size.
    """
    ax.set_ylim((-0.10 * scale, .90 * scale))
    ax.set_xlim((-0.05 * scale, 1.05 * scale))

def clear_matplotlib_ticks(ax=None, axis="both"):
    """
    Clears the default matplotlib axes, or the one specified by the axis
    argument.

    Parameters
    ----------
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    axis: string, "both"
        The axis to clear: "x" or "horizontal", "y" or "vertical", or "both"
    """
    if not ax:
        return
    if axis.lower() in ["both", "x", "horizontal"]:
        ax.set_xticks([], [])
    if axis.lower() in ["both", "y", "vertical"]:
        ax.set_yticks([], [])

## Curve Plotting ##

def plot(points, ax=None, permutation=None, **kwargs):
    """
    Analogous to maplotlib.plot. Plots trajectory points where each point is a
    tuple (x,y,z) satisfying x + y + z = scale (not checked). The tuples are
    projected and plotted as a curve.

    Parameters
    ----------
    points: List of 3-tuples
        The list of tuples to be plotted as a connected curve.
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    kwargs:
        Any kwargs to pass through to matplotlib.
    """
    if not ax:
        fig, ax = pyplot.subplots()
    xs, ys = project_sequence(points, permutation=permutation)
    ax.plot(xs, ys, **kwargs)
    return ax

def plot_colored_trajectory(points, cmap=None, ax=None, permutation=None,
                            **kwargs):
    """
    Plots trajectories with changing color, simlar to `plot`. Trajectory points 
    are tuples (x,y,z) satisfying x + y + z = scale (not checked). The tuples are
    projected and plotted as a curve.

    Parameters
    ----------
    points: List of 3-tuples
        The list of tuples to be plotted as a connected curve.
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    cmap: String or matplotlib.colors.Colormap, None
        The name of the Matplotlib colormap to use.
    kwargs:
        Any kwargs to pass through to matplotlib.
    """
    if not ax:
        fig, ax = pyplot.subplots()
    cmap = get_cmap(cmap)
    xs, ys = project_sequence(points, permutation=permutation)

    # We want to color each segment independently...which is annoying.
    segments = []
    for i in range(len(xs) - 1):
        cur_line = []
        x_before = xs[i]
        y_before = ys[i]
        x_after = xs[i+1]
        y_after = ys[i+1]

        cur_line.append([x_before, y_before])
        cur_line.append([x_after, y_after])
        segments.append(cur_line)
    segments = np.array(segments)

    line_segments = matplotlib.collections.LineCollection(segments, cmap=cmap, **kwargs)
    line_segments.set_array(np.arange(len(segments)))
    ax.add_collection(line_segments)

    return ax

def scatter(points, ax=None, permutation=None, **kwargs):
    """Plots trajectory points where each point satisfies x + y + z = scale. First argument is a list or numpy array of tuples of length 3.

    Parameters
    ----------
    points: List of 3-tuples
        The list of tuples to be scatter-plotted.
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    kwargs:
        Any kwargs to pass through to matplotlib.
    """
    if not ax:
        fig, ax = pyplot.subplots()
    xs, ys = project_sequence(points, permutation=permutation)
    ax.scatter(xs, ys, **kwargs)
    return ax
