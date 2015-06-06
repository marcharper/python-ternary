"""
Line plotting functions, draw boundary and gridlines.
"""

from numpy import arange
from matplotlib.lines import Line2D
from matplotlib import pyplot

from helpers import project_point
import plotting


## Lines ##

def line(ax, p1, p2, **kwargs):
    """
    Draws a line on `ax` from p1 to p2.

    Parameters
    ----------
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    p1: 2-tuple
        The (x,y) starting coordinates
    p2: 2-tuple
        The (x,y) ending coordinates
    kwargs:
        Any kwargs to pass through to Matplotlib.
    """

    ax.add_line(Line2D((p1[0], p2[0]), (p1[1], p2[1]), **kwargs))

def horizontal_line(ax, scale, i, **kwargs):
    """
    Draws the i-th horizontal line parallel to the lower axis.

    Parameters
    ----------
    ax: Matplotlib AxesSubplot
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
    line(ax, p1, p2, **kwargs)

def left_parallel_line(ax, scale, i,  **kwargs):
    """
    Draws the i-th line parallel to the left axis.

    Parameters
    ----------
    ax: Matplotlib AxesSubplot
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
    line(ax, p1, p2, **kwargs)

def right_parallel_line(ax, scale, i, **kwargs):
    """
    Draws the i-th line parallel to the right axis.

    Parameters
    ----------
    ax: Matplotlib AxesSubplot
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
    line(ax, p1, p2, **kwargs)

## Boundary, Gridlines ##

def boundary(ax, scale, **kwargs):
    """
    Plots the boundary of the simplex. Creates and returns matplotlib axis if
    none given.

    Parameters
    ----------
    scale: float, 1.0
        Simplex scale size.
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    kwargs:
        Any kwargs to pass through to matplotlib.
    """

    horizontal_line(ax, scale, 0, **kwargs)
    left_parallel_line(ax, scale, 0, **kwargs)
    right_parallel_line(ax, scale, 0, **kwargs)
    return ax

## TODO: left_kwargs, right_kwargs

def gridlines(ax, scale, multiple=None, **kwargs):
    """
    Plots grid lines excluding boundary.

    Parameters
    ----------
    scale: float, 1.0
        Simplex scale size.
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    multiple: float, None
        Specifies which inner gridelines to draw. For example, if scale=30 and
        multiple=6, only 5 inner gridlines will be drawn.
    kwargs:
        Any kwargs to pass through to matplotlib.
    """

    if 'linewidth' not in kwargs:
        kwargs["linewidth"] = 0.5
    if 'linestyle' not in kwargs:
        kwargs["linestyle"] = ':'
    ## Draw grid-lines
    if multiple:
        # Parallel to horizontal axis
        for i in arange(0, scale, multiple):
            horizontal_line(ax, scale, i, **kwargs)
        # Parallel to left and right axes
        for i in arange(0, scale + multiple, multiple):
            left_parallel_line(ax, scale, i, **kwargs)
            right_parallel_line(ax, scale, i, **kwargs)
    return ax
