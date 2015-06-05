from numpy import arange
from matplotlib.lines import Line2D

from helpers import project_point
from plotting import resize_drawing_canvas, new_axes_subplot

## Lines ##

def line(axes_subplot, p1, p2, **kwargs):
    """
    Draws a line on `axes_subplot` from p1 to p2.

    Parameters
    ----------
    axes_subplot: Matplotlib AxesSubplot, None
        The subplot to draw on.
    p1: 2-tuple
        The (x,y) starting coordinates
    p2: 2-tuple
        The (x,y) ending coordinates
    kwargs:
        Any kwargs to pass through to Matplotlib.
    """

    axes_subplot.add_line(Line2D((p1[0], p2[0]), (p1[1], p2[1]), **kwargs))

def horizontal_line(axes_subplot, scale, i, **kwargs):
    """
    Draws the i-th horizontal line parallel to the lower axis.

    Parameters
    ----------
    axes_subplot: Matplotlib AxesSubplot
        The subplot to draw on.
    scale: float, 1.0
        Simplex scale size.
    i: float
        The index of the line to draw
    kwargs: Dictionary
        Any kwargs to pass through to Matplotlib.
    """

    p1 = project_point((0, scale-i, i))
    p2 = project_point((scale-i, 0, i))
    line(axes_subplot, p1, p2, **kwargs)

def left_parallel_line(axes_subplot, scale, i,  **kwargs):
    """
    Draws the i-th line parallel to the left axis.

    Parameters
    ----------
    axes_subplot: Matplotlib AxesSubplot
        The subplot to draw on.
    scale: float, 1.0
        Simplex scale size.
    i: float
        The index of the line to draw
    kwargs: Dictionary
        Any kwargs to pass through to Matplotlib.
    """

    p1 = project_point((0, i, scale-i))
    p2 = project_point((scale-i, i, 0))
    line(axes_subplot, p1, p2, **kwargs)

def right_parallel_line(axes_subplot, scale, i, **kwargs):
    """
    Draws the i-th line parallel to the right axis.

    Parameters
    ----------
    axes_subplot: Matplotlib AxesSubplot
        The subplot to draw on.
    scale: float, 1.0
        Simplex scale size.
    i: float
        The index of the line to draw
    kwargs: Dictionary
        Any kwargs to pass through to Matplotlib.
    """

    p1 = project_point((i, scale-i, 0))
    p2 = project_point((i, 0, scale-i))
    line(axes_subplot, p1, p2, **kwargs)

## Boundary, Gridlines ##

def boundary(scale=1.0, axes_subplot=None, **kwargs):
    """
    Plots the boundary of the simplex. Creates and returns matplotlib axis if
    none given.

    Parameters
    ----------
    scale: float, 1.0
        Simplex scale size.
    axes_subplot: Matplotlib AxesSubplot, None
        The subplot to draw on.
    kwargs:
        Any kwargs to pass through to matplotlib.
    """

    if not axes_subplot:
        axes_subplot = new_axes_subplot()
    resize_drawing_canvas(axes_subplot, scale)
    horizontal_line(axes_subplot, scale, 0, **kwargs)
    left_parallel_line(axes_subplot, scale, 0, **kwargs)
    right_parallel_line(axes_subplot, scale, 0, **kwargs)
    return axes_subplot

## TODO: left_kwargs, right_kwargs

def gridlines(scale=1., multiple=None, axes_subplot=None, **kwargs):
    """
    Plots grid lines excluding boundary.

    Parameters
    ----------
    scale: float, 1.0
        Simplex scale size.
    axes_subplot: Matplotlib AxesSubplot, None
        The subplot to draw on.
    multiple: float, None
        Specifies which inner gridelines to draw. For example, if scale=30 and
        multiple=6, only 5 inner gridlines will be drawn.
    kwargs:
        Any kwargs to pass through to matplotlib.
    """

    if not axes_subplot:
        axes_subplot = new_axes_subplot()
    if 'linewidth' not in kwargs:
        kwargs["linewidth"] = 0.5
    if 'linestyle' not in kwargs:
        kwargs["linestyle"] = ':'
    resize_drawing_canvas(axes_subplot, scale)
    ## Draw grid-lines
    if multiple:
        # Parallel to horizontal axis
        for i in arange(0, scale, multiple):
            horizontal_line(axes_subplot, scale, i, **kwargs)
        # Parallel to left and right axes
        for i in arange(0, scale + multiple, multiple):
            left_parallel_line(axes_subplot, scale, i, **kwargs)
            right_parallel_line(axes_subplot, scale, i, **kwargs)
    return axes_subplot
