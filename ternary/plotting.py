"""
Plotting functions: scatter, plot (curves), axis labelling.
"""

from functools import partial

import matplotlib
from matplotlib import pyplot
import numpy as np

from helpers import project_sequence, project_point
from colormapping import get_cmap

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

def plot(points, ax=None, **kwargs):
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
    xs, ys = project_sequence(points)
    ax.plot(xs, ys, **kwargs)
    return ax

def plot_colored_trajectory(points, cmap=None, ax=None, **kwargs):
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
    xs, ys = project_sequence(points)

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

def scatter(points, ax=None, **kwargs):
    """Plots trajectory points where each point satisfies x + y + z = scale. First argument is a list or numpy array of tuples of length 3.

    Parameters
    ----------
    points: List of 3-tuples
        The list of tuples to be scatter-plotted.
    scale: float, 1.0
        Simplex scale size.
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    kwargs:
        Any kwargs to pass through to matplotlib.
    """
    if not ax:
        fig, ax = pyplot.subplots()
    xs, ys = project_sequence(points)
    ax.scatter(xs, ys, **kwargs)
    return ax

## Axes Labels ##

def mpl_callback(event, rotation=60, hash_=None):
    """
    Callback to properly rotate side text labels when the plot is resized.
    """

    #http://stackoverflow.com/questions/4018860/text-box-with-line-wrapping-in-matplotlib

    # Find the Text objects we want to update.
    figure = event.canvas.figure
    for ax in figure.axes:
        for artist in ax.get_children():
            if not (artist.__hash__() == hash_):
                continue
            # Calculate the new angle.
            x, y = artist.get_transform().transform(artist.get_position())
            position = np.array([x,y])
            new_rotation = ax.transData.transform_angles(np.array((rotation,)), position.reshape((1,2)))[0]
            artist.set_rotation(new_rotation)

    # Temporarily disconnect any callbacks to the draw event...
    # (To avoid recursion)
    func_handles = figure.canvas.callbacks.callbacks[event.name]
    figure.canvas.callbacks.callbacks[event.name] = {}
    # Re-draw the figure..
    figure.canvas.draw()
    # Reset the draw event callbacks
    figure.canvas.callbacks.callbacks[event.name] = func_handles

def set_ternary_axis_label(ax, label, position, rotation, event_names=None,
                           **kwargs):
    """
    Sets axis labels and registers a callback to adjust text angle when the
    user resizes or triggers a redraw in interactive mode. Not intended to
    be called directly by the user.

    Parameters
    ----------
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    label: String
        The axis label.
    position: 3-tuple
        The coordinates to place the label at.
    rotation: float
        The angle of rotation of the label.
    event_names: sequence of strings
        The Matplotlib events to callback on.
    kwargs:
        Any kwargs to pass through to matplotlib.
    """

    # http://stackoverflow.com/questions/4018860/text-box-with-line-wrapping-in-matplotlib

    if not event_names:
        event_names = ('resize_event', 'draw_event')
    transform = ax.transAxes
    x, y = project_point(position)
    text = ax.text(x, y, label, rotation=rotation, transform=transform,
                   **kwargs)
    text.set_rotation_mode("anchor")
    # Set callback. Make sure that we don't rotate other text fields, like the
    # title.
    hash_ = text.__hash__()
    callback = partial(mpl_callback, rotation=rotation, hash_=hash_)
    figure = ax.get_figure()
    for event_name in event_names:
        figure.canvas.mpl_connect(event_name, callback)

def left_axis_label(ax, label, rotation=60, offset=0.08, **kwargs):
    """
    Sets axis label on the left triangular axis. The label can include
    LaTeX.

    Parameters
    ----------
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    label: String
        The axis label
    kwargs:
        Any kwargs to pass through to matplotlib.
    """

    position = (1./2, -offset, 1./2)
    set_ternary_axis_label(ax, label, position, rotation, **kwargs)

def right_axis_label(ax, label, rotation=-60, offset=0.08, **kwargs):
    """
    Sets axis label on the right triangular axis. The label can include
    LaTeX.

    Parameters
    ----------
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    label: String
        The axis label
    kwargs:
        Any kwargs to pass through to matplotlib.
    """
    #position = (offset, 1./2 + offset, 1./2)
    position = (0, 2./5 + offset, 3./5)
    set_ternary_axis_label(ax, label, position, rotation,
                           horizontalalignment="center", **kwargs)

def bottom_axis_label(ax, label, rotation=0, offset=0.04, **kwargs):
    """
    Sets axis label on the bottom (lower) triangular axis. The label can include
    LaTeX.

    Parameters
    ----------
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    label: String
        The axis label
    kwargs:
        Any kwargs to pass through to matplotlib.
    """

    position = (1./2, 1./2, offset)
    set_ternary_axis_label(ax, label, position, rotation,
                           horizontalalignment="center", **kwargs)
