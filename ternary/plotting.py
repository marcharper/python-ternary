
import matplotlib.pyplot as pyplot

from helpers import project_sequence

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
    axes_subplot.set_ylim((-0.05 * scale, .90 * scale))
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
