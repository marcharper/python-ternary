
from functools import partial

import matplotlib
import matplotlib.pyplot as pyplot
import numpy

from helpers import project_sequence, project_point

text_rotate_events = ('resize_event', 'draw_event')

### Drawing Helpers ###

def new_axes_subplot():
    """Returns a new Matplotlib AxesSubplot object."""
    return pyplot.subplot()

def resize_drawing_canvas(axes_subplot, scale=1.):
    """
    Makes sure the drawing surface is large enough to display projected
    content.

    Parameters
    ----------
    axes_subplot: Matplotlib AxesSubplot, None
        The subplot to draw on.
    scale: float, 1.0
        Simplex scale size.
    """
    axes_subplot.set_ylim((-0.10 * scale, .90 * scale))
    axes_subplot.set_xlim((-0.05 * scale, 1.05 * scale))

def clear_matplotlib_ticks(axes_subplot=None, axis="both"):
    """
    Clears the default matplotlib axes, or the one specified by the axis
    argument.

    Parameters
    ----------
    axes_subplot: Matplotlib AxesSubplot, None
        The subplot to draw on.
    axis: string, "both"
        The axis to clear: "x" or "horizontal", "y" or "vertical", or "both"
    """
    if not axes_subplot:
        return
    if axis.lower() in ["both", "x", "horizontal"]:
        axes_subplot.set_xticks([], [])
    if axis.lower() in ["both", "y", "vertical"]:
        axes_subplot.set_yticks([], [])

## Curve Plotting ##

def plot(points, axes_subplot=None, **kwargs):
    """
    Analogous to maplotlib.plot. Plots trajectory points where each point is a
    tuple (x,y,z) satisfying x + y + z = scale (not checked). The tuples are
    projected and plotted as a curve.

    Parameters
    ----------
    points: List of 3-tuples
        The list of tuples to be plotted as a connected curve.
    axes_subplot: Matplotlib AxesSubplot, None
        The subplot to draw on.
    kwargs:
        Any kwargs to pass through to matplotlib.
    """
    if not axes_subplot:
        axes_subplot = new_axes_subplot()
    xs, ys = project_sequence(points)
    axes_subplot.plot(xs, ys, **kwargs)
    return axes_subplot

def scatter(points, scale=1., axes_subplot=None, **kwargs):
    """Plots trajectory points where each point satisfies x + y + z = scale. First argument is a list or numpy array of tuples of length 3.

    Parameters
    ----------
    points: List of 3-tuples
        The list of tuples to be scatter-plotted.
    scale: float, 1.0
        Simplex scale size.
    axes_subplot: Matplotlib AxesSubplot, None
        The subplot to draw on.
    kwargs:
        Any kwargs to pass through to matplotlib.
    """
    if not axes_subplot:
        axes_subplot = new_axes_subplot()
    xs, ys = project_sequence(points)
    axes_subplot.scatter(xs, ys, **kwargs)
    return axes_subplot

## Axes Labels ##

def mpl_callback(event, rotation=60, hash_=None):
    figure = event.canvas.figure
    for ax in figure.axes:
        for artist in ax.get_children():
            if not (artist.__hash__() == hash_):
                continue
            x, y = artist.get_transform().transform(artist.get_position())
            position = numpy.array([x,y])
            new_rotation = ax.transData.transform_angles(numpy.array((rotation,)), position.reshape((1,2)))[0]
            artist.set_rotation(new_rotation)

def set_ternary_axis_label(axes_subplot, label, position, rotation,
                   event_names=text_rotate_events, **kwargs):
    transform = axes_subplot.transAxes
    x, y = position
    text = axes_subplot.text(x, y, label, rotation=rotation, transform=transform,
                             #horizontalalignment="center",
                             #verticalalignment="center", 
                             **kwargs)
    text.set_rotation_mode("anchor")
    # Set Callback
    hash_ = text.__hash__()
    callback = partial(mpl_callback, rotation=rotation, hash_=hash_)
    figure = axes_subplot.get_figure()
    for event_name in event_names:
        figure.canvas.mpl_connect(event_name, callback)

def left_axis_label(axes_subplot, label, rotation=60, offset=0.08, **kwargs):
    
    position = project_point((1./2, -offset, 1./2))
    set_ternary_axis_label(axes_subplot, label, position, rotation, **kwargs)

def right_axis_label(axes_subplot, label, rotation=-60, offset=0.08, **kwargs):
    
    #position = project_point((offset, 1./2 + offset, 1./2))
    position = project_point((0, 2./5 + offset, 3./5))
    set_ternary_axis_label(axes_subplot, label, position, rotation,
                           horizontalalignment="center", **kwargs)

def bottom_axis_label(axes_subplot, label, rotation=0, offset=0.04, **kwargs):
    
    position = project_point((1./2, 1./2, offset))
    set_ternary_axis_label(axes_subplot, label, position, rotation,
                           horizontalalignment="center", **kwargs)
