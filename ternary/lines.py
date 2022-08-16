"""
Line plotting functions, draw boundary and gridlines.
"""

from numpy import arange
from matplotlib.lines import Line2D

from .helpers import project_point


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


def horizontal_line(ax, scale, i, axis_min_max, **kwargs):
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
    axis_min_max: dict
        The min and max values of the axes in simplex coordinates.
        These may not be equal to (0, scale) if a truncation has been
        applied.
    kwargs: Dictionary
        Any kwargs to pass through to Matplotlib.
    """
    if i <= axis_min_max['r'][1]:
        if i < scale-axis_min_max['l'][1]:
            p1 = (axis_min_max['b'][0] - i,
                  i,
                  axis_min_max['l'][1])
        else:
            p1 = (0, i, scale-i)

        if i < axis_min_max['r'][0]:
            p2 = (axis_min_max['b'][1],
                  i,
                  scale - axis_min_max['b'][1] - i)
        else:
            p2 = (scale - i, i, 0)

        line(ax, p1, p2, **kwargs)


def left_parallel_line(ax, scale, i,  axis_min_max, **kwargs):
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
    axis_min_max: dict
        The min and max values of the axes in simplex coordinates.
        These may not be equal to (0, scale) if a truncation has been
        applied.
    kwargs: Dictionary
        Any kwargs to pass through to Matplotlib.
    """
    if i <= axis_min_max['b'][1]:
        if i < scale-axis_min_max['r'][1]:
            p1 = (i,
                  axis_min_max['r'][1],
                  axis_min_max['l'][0] - i)
        else:
            p1 = (i, scale - i, 0)

        if i < axis_min_max['b'][0]:
            p2 = (i,
                  scale - axis_min_max['l'][1] - i,
                  axis_min_max['l'][1])
        else:
            p2 = (i, 0, scale - i)

        line(ax, p1, p2, **kwargs)


def right_parallel_line(ax, scale, i, axis_min_max=None, **kwargs):
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
    axis_min_max: dict
        The min and max values of the axes in simplex coordinates.
        These may not be equal to (0, scale) if a truncation has been
        applied.
    kwargs: Dictionary
        Any kwargs to pass through to Matplotlib.
    """
    if i <= axis_min_max['l'][1]:
        if i < axis_min_max['l'][0]:
            p1 = (scale - axis_min_max['r'][1] - i,
                  axis_min_max['r'][1],
                  i)
        else:
            p1 = (0, scale - i, i)

        if i < scale - axis_min_max['b'][1]:
            p2 = (axis_min_max['b'][1],
                  scale - axis_min_max['b'][1] - i,
                  i)
        else:
            p2 = (scale - i, 0, i)

        line(ax, p1, p2, **kwargs)


## Boundary, Gridlines ##

def boundary(ax, scale, axis_min_max, axes_colors=None, **kwargs):
    """
    Plots the boundary of the simplex. Creates and returns matplotlib axis if
    none given.

    Parameters
    ----------
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    scale: float
        Simplex scale size.
    axis_min_max: dict
        The min and max values of the axes in simplex coordinates.
        These may not be equal to (0, scale) if a truncation has been
        applied.
    axes_colors: dict
        Option for coloring boundaries different colors.
        e.g. {'l': 'g'} for coloring the left axis boundary green
    kwargs:
        Any kwargs to pass through to matplotlib.
    """

    # set default color as black
    if axes_colors is None:
        axes_colors = dict()
    for _axis in ['l', 'r', 'b']:
        if _axis not in axes_colors.keys():
            axes_colors[_axis] = 'black'

    horizontal_line(ax, scale, 0, axis_min_max,
                    color=axes_colors['b'], **kwargs)
    left_parallel_line(ax, scale, 0, axis_min_max,
                       color=axes_colors['l'], **kwargs)
    right_parallel_line(ax, scale, 0, axis_min_max,
                        color=axes_colors['r'], **kwargs)

    if axis_min_max['r'][1] < scale:
        horizontal_line(ax, scale, axis_min_max['r'][1],
                        axis_min_max=axis_min_max,
                        color=axes_colors['r'], **kwargs)
    if axis_min_max['b'][1] < scale:
        left_parallel_line(ax, scale, axis_min_max['b'][1],
                           axis_min_max=axis_min_max,
                           color=axes_colors['b'], **kwargs)
    if axis_min_max['l'][1] < scale:
        right_parallel_line(ax, scale, axis_min_max['l'][1],
                            axis_min_max=axis_min_max,
                            color=axes_colors['l'], **kwargs)


    return ax


def merge_dicts(base, updates):
    """
    Given two dicts, merge them into a new dict as a shallow copy.

    Parameters
    ----------
    base: dict
        The base dictionary.
    updates: dict
        Secondary dictionary whose values override the base.
    """
    if not base:
        base = dict()
    if not updates:
        updates = dict()
    z = base.copy()
    z.update(updates)
    return z


def gridlines(ax, scale, axis_min_max, multiple=None,
              horizontal_kwargs=None, left_kwargs=None, right_kwargs=None,
              **kwargs):
    """
    Plots grid lines excluding boundary.

    Parameters
    ----------
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    scale: float
        Simplex scale size.
    axis_min_max: dict
        The min and max values of the axes in simplex coordinates.
        These may not be equal to (0, scale) if a truncation has been
        applied.
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
        horizontal_line(ax, scale, i, axis_min_max, **horizontal_kwargs)
    # Parallel to left and right axes
    for i in arange(0, scale + multiple, multiple):
        left_parallel_line(ax, scale, i, axis_min_max, **left_kwargs)
        right_parallel_line(ax, scale, i, axis_min_max, **right_kwargs)

    return ax


def normalize_tick_formats(tick_formats):
    if type(tick_formats) == dict:
        return tick_formats
    if tick_formats is None:
        s = '%d'
    elif type(tick_formats) == str:
        s = tick_formats
    else:
        raise TypeError("tick_formats must be a dictionary of strings"
                        " a string, or None.")
    return {'b': s, 'l': s, 'r': s}


def ticks(ax, scale, ticks=None, locations=None, multiple=1, axis='b',
          offset=0.01, clockwise=False, axes_colors=None, fontsize=10,
          tick_formats=None, **kwargs):
    """
    Sets tick marks and labels.

    Parameters
    ----------
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    scale: float, 1.0
        Simplex scale size.
    ticks: list of strings, None
        The tick labels
    locations: list of points, None
        The locations of the ticks
    multiple: float, None
        Specifies which ticks gridelines to draw. For example, if scale=30 and
        multiple=6, only 5 ticks will be drawn.
    axis: str, 'b'
        The axis or axes to draw the ticks for. `axis` must be a substring of
        'lrb' (as sets)
    offset: float, 0.01
        controls the length of the ticks
    clockwise: bool, False
        Draw ticks marks clockwise or counterclockwise
    axes_colors: Dict, None
        Option to color ticks differently for each axis, 'l', 'r', 'b'
        e.g. {'l': 'g', 'r':'b', 'b': 'y'}
    tick_formats: None, Dict, Str
        If None, all axes will be labelled with ints. If Dict, the keys are
        'b', 'l' and 'r' and the values are format strings e.g. "%.3f" for
        a float with 3 decimal places or "%.3e" for scientific format with
        3 decimal places or "%d" for ints. If tick_formats is a string, it
        is assumed that this is a format string to be applied to all axes.
    kwargs:
        Any kwargs to pass through to matplotlib.

    """

    axis = axis.lower()
    valid_axis_chars = set(['l', 'r', 'b'])
    axis_chars = set(axis)
    if not axis_chars.issubset(valid_axis_chars):
        raise ValueError("axis must be some combination of 'l', 'r', and 'b'")

    if ticks and not locations:
        num_ticks = len(ticks)
        if num_ticks != 0:
            multiple = scale / (num_ticks - 1)
            locations = arange(0, scale + multiple, multiple)

    if not ticks:
        locations = arange(0, scale + multiple, multiple)
        ticks = locations

    tick_formats = normalize_tick_formats(tick_formats)

    # Default color: black
    if axes_colors is None:
        axes_colors = dict()
    for _axis in valid_axis_chars:
        if _axis not in axes_colors:
            axes_colors[_axis] = 'black'

    offset *= scale

    if 'r' in axis:
        for index, i in enumerate(locations):
            loc1 = (scale - i, i, 0)
            if clockwise:
                # Right parallel
                loc2 = (scale - i, i + offset, 0)
                text_location = (scale - i, i + 2 * offset, 0)
                tick = ticks[-(index+1)]
            else:
                # Horizontal
                loc2 = (scale - i + offset, i, 0)
                text_location = (scale - i + 3.1 * offset, i - 0.5 * offset, 0)
                tick = ticks[index]
            line(ax, loc1, loc2, color=axes_colors['r'], **kwargs)
            x, y = project_point(text_location)
            if isinstance(tick, str):
                s = tick
            else:
                s = tick_formats['r'] % tick
            ax.text(x, y, s, horizontalalignment="center",
                    color=axes_colors['r'], fontsize=fontsize)

    if 'l' in axis:
        for index, i in enumerate(locations):
            loc1 = (0, i, 0)
            if clockwise:
                # Horizontal
                loc2 = (-offset, i, 0)
                text_location = (-2 * offset, i - 0.5 * offset, 0)
                tick = ticks[index]
            else:
                # Right parallel
                loc2 = (-offset, i + offset, 0)
                text_location = (-2 * offset, i + 1.5 * offset, 0)
                tick = ticks[-(index+1)]
            line(ax, loc1, loc2, color=axes_colors['l'], **kwargs)
            x, y = project_point(text_location)
            if isinstance(tick, str):
                s = tick
            else:
                s = tick_formats['l'] % tick
            ax.text(x, y, s, horizontalalignment="center",
                    color=axes_colors['l'], fontsize=fontsize)

    if 'b' in axis:
        for index, i in enumerate(locations):
            loc1 = (i, 0, 0)
            if clockwise:
                # Right parallel
                loc2 = (i + offset, -offset, 0)
                text_location = (i + 3 * offset, -3.5 * offset, 0)
                tick = ticks[-(index+1)]
            else:
                # Left parallel
                loc2 = (i, -offset, 0)
                text_location = (i + 0.5 * offset, -3.5 * offset, 0)
                tick = ticks[index]
            line(ax, loc1, loc2, color=axes_colors['b'], **kwargs)
            x, y = project_point(text_location)
            if isinstance(tick, str):
                s = tick
            else:
                s = tick_formats['b'] % tick
            ax.text(x, y, s, horizontalalignment="center",
                    color=axes_colors['b'], fontsize=fontsize)


def add_extra_tick(ax, axis, loc1, offset, scale, tick, fontsize, **kwargs):
    """
    Add an extra tick on an axis but not necessarily on
    the boundary of the simplex. This may be useful if a truncation is applied.

    Parameters
    ----------
    ax : matplotlib.Axes
        The matplotlib Axes object containing the plot.
    axis : STR
        A string giving the axis on which the extra tick should be drawn.
        One of 'l', 'b' or 'r'.
    loc1 : 3-tuple
        A 3-tuple giving the location of the extra tick in simplex coords.
    offset : FLOAT
        Defines an offset of the tick label and the length of the tick
    scale : INT
        The self._scale attibute of the simplex
    tick : STR
        A string giving the text for the tick label
    fontsize : INT
        Describing the font size of the tick label
    **kwargs : DICT
        Kwargs to pass through to matplotlib Line2D.

    Returns
    -------
    None.

    """
    toff = offset * scale

    if axis == 'r':
        loc2 = (loc1[0] + toff, loc1[1], loc1[2]-toff)
        text_location = (loc1[0] + 2.6 * toff,
                         loc1[1] - 0.5 * toff,
                         loc1[2] - 2.6 * toff)

    elif axis == 'l':
        loc2 = (loc1[0] - toff, loc1[1] + toff, loc1[2])
        text_location = (loc1[0] - 2 * toff,
                         loc1[1] + 1.5 * toff,
                         loc1[2] + 2 * toff)

    elif axis == 'b':
        loc2 = (loc1[0], loc1[1] - toff, loc1[2] + toff)
        text_location = (loc1[0] - 0.5 * toff,
                         loc1[1] - 3.5 * toff,
                         loc1[2] + 2 * toff)


    line(ax, loc1, loc2, **kwargs)
    x, y = project_point(text_location)
    ax.text(x,y,tick,horizontalalignment='center',fontsize=fontsize)
