"""
Line plotting functions, draw boundary and gridlines.
"""

from numpy import arange
from matplotlib.lines import Line2D
from matplotlib import pyplot

from helpers import project_point
import plotting


## Lines ##

def line(ax, p1, p2, permutation=None, **kwargs):
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

    pp1 = project_point(p1, permutation=permutation)
    pp2 = project_point(p2, permutation=permutation)
    ax.add_line(Line2D((pp1[0], pp2[0]), (pp1[1], pp2[1]), **kwargs))

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

    p1 = (0, scale-i, i)
    p2 = (scale-i, 0, i)
    line(ax, p1, p2, **kwargs)

def left_parallel_line(ax, scale, i,  **kwargs):
    """
    Draws the i-th line parallel to the left axis.

    Parameters
    ----------
    ax: Matplotlib AxesSubplot
        The subplot to draw on.
    scale: float
        Simplex scale size.
    i: float
        The index of the line to draw
    kwargs: Dictionary
        Any kwargs to pass through to Matplotlib.
    """

    p1 = (0, i, scale-i)
    p2 = (scale-i, i, 0)
    line(ax, p1, p2, **kwargs)

def right_parallel_line(ax, scale, i, **kwargs):
    """
    Draws the i-th line parallel to the right axis.

    Parameters
    ----------
    ax: Matplotlib AxesSubplot
        The subplot to draw on.
    scale: float
        Simplex scale size.
    i: float
        The index of the line to draw
    kwargs: Dictionary
        Any kwargs to pass through to Matplotlib.
    """

    p1 = (i, scale-i, 0)
    p2 = (i, 0, scale-i)
    line(ax, p1, p2, **kwargs)

## Boundary, Gridlines ##

def boundary(ax, scale, **kwargs):
    """
    Plots the boundary of the simplex. Creates and returns matplotlib axis if
    none given.

    Parameters
    ----------
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    scale: float
        Simplex scale size.
    kwargs:
        Any kwargs to pass through to matplotlib.
    """

    horizontal_line(ax, scale, 0, **kwargs)
    left_parallel_line(ax, scale, 0, **kwargs)
    right_parallel_line(ax, scale, 0, **kwargs)
    return ax

def merge_dicts(base, updates):
    '''
    Given two dicts, merge them into a new dict as a shallow copy.
    
    Parameters
    ----------
    base: dict
        The base dictionary
    updates: dict
        Secondary dictionary whose values override the base
    '''
    if not base:
        base = dict()
    if not updates:
        updates = dict()
    z = base.copy()
    z.update(updates)
    return z

def gridlines(ax, scale, multiple=None, horizontal_kwargs=None, left_kwargs=None, right_kwargs=None, **kwargs):
    """
    Plots grid lines excluding boundary.

    Parameters
    ----------
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    scale: float
        Simplex scale size.
    multiple: float, None
        Specifies which inner gridelines to draw. For example, if scale=30 and
        multiple=6, only 5 inner gridlines will be drawn.
    horizontal_kwargs: dict, None
        Any kwargs to pass through to matplotlib for horizontal gridlines
    left_kwargs: dict, None
        Any kwargs to pass through to matplotlib for left parallel gridlines
    right_kwargs: dict, None
        Any kwargs to pass through to matplotlib for right parallel gridlines
    kwargs:
        Any kwargs to pass through to matplotlib, if not using
        horizontal_kwargs, left_kwargs, or right_kwargs
    """

    if 'linewidth' not in kwargs:
        kwargs["linewidth"] = 0.5
    if 'linestyle' not in kwargs:
        kwargs["linestyle"] = ':'
    horizontal_kwargs = merge_dicts(kwargs, horizontal_kwargs)
    left_kwargs = merge_dicts(kwargs, left_kwargs)
    right_kwargs = merge_dicts(kwargs, right_kwargs)
    if not multiple:
        multiple = 1.
    ## Draw grid-lines
    # Parallel to horizontal axis
    for i in arange(0, scale, multiple):
        horizontal_line(ax, scale, i, **horizontal_kwargs)
    # Parallel to left and right axes
    for i in arange(0, scale + multiple, multiple):
        left_parallel_line(ax, scale, i, **left_kwargs)
        right_parallel_line(ax, scale, i, **right_kwargs)
    return ax
