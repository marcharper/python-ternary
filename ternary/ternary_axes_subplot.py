"""
Wrapper class for all ternary plotting functions.
"""

from matplotlib import pyplot

import heatmapping
import lines
import plotting
from helpers import project_point


def figure(ax=None, scale=None, permutation=None):
    """
    Wraps a Matplotlib AxesSubplot or generates a new one. Emulates matplotlib's
    > figure, ax = pyplot.subplots()

    Parameters
    ----------
    ax: AxesSubplot, None
        The AxesSubplot to wrap
    scale: float, None
        The scale factor of the ternary plot
    """

    ternary_ax = TernaryAxesSubplot(ax=ax, scale=scale, permutation=permutation)
    return ternary_ax.get_figure(), ternary_ax


class TernaryAxesSubplot(object):
    """Wrapper for python-ternary and matplotlib figure. Parameters for member
    functions simply pass through to ternary's functions with the same names.
    This class manages the matplotlib axes, the scale, and the boundary scale
    to ease the use of ternary plotting functions.
    """

    def __init__(self, ax=None, scale=None, permutation=None):
        if not scale:
            scale = 1.0
        if ax:
            self.ax = ax
        else:
            _, self.ax = pyplot.subplots()
        self._permutation = None
        self.set_scale(scale=scale)
        self._boundary_scale = scale

    def __repr__(self):
        return "TernaryAxesSubplot: %s" % self.ax.__hash__()

    def get_figure(self):
        ax = self.get_axes()
        return ax.get_figure()

    def set_scale(self, scale=None):
        self._scale = scale
        self.resize_drawing_canvas()

    def get_scale(self):
        return self._scale

    def get_axes(self):
        return self.ax

    def annotate(self, text, position, **kwargs):
        ax = self.get_axes()
        p = project_point(position)
        ax.annotate(text, (p[0], p[1]), **kwargs)

    def scatter(self, points, **kwargs):
        ax = self.get_axes()
        permutation = self._permutation
        plot_ = plotting.scatter(points, ax=ax, permutation=permutation,
                                 **kwargs)
        return plot_

    def plot(self, points, **kwargs):
        ax = self.get_axes()
        permutation = self._permutation
        plotting.plot(points, ax=ax, permutation=permutation,
                      **kwargs)

    def plot_colored_trajectory(self, points, cmap=None, **kwargs):
        ax = self.get_axes()
        permutation = self._permutation
        plotting.plot_colored_trajectory(points, cmap=cmap, ax=ax,
                                         permutation=permutation, **kwargs)

    def clear_matplotlib_ticks(self, axis="both"):
        ax = self.get_axes()
        plotting.clear_matplotlib_ticks(ax=ax, axis=axis)

    def left_axis_label(self, label, position=None, **kwargs):
        ax = self.get_axes()
        plotting.left_axis_label(ax, label, position=position, **kwargs)

    def right_axis_label(self, label, position=None, **kwargs):
        ax = self.get_axes()
        plotting.right_axis_label(ax, label, position=position, **kwargs)

    def bottom_axis_label(self, label, position=None, **kwargs):
        ax = self.get_axes()
        plotting.bottom_axis_label(ax, label, position=position, **kwargs)

    def heatmap(self, data, scale=None, cmap=None, scientific=False,
                style='triangular', colorbar=True):
        permutation = self._permutation
        if not scale:
            scale = self.get_scale()
        if style.lower()[0] == 'd':
            self._boundary_scale = scale + 1
        ax = self.get_axes()
        heatmapping.heatmap(data, scale, cmap=cmap, style=style, ax=ax,
                            scientific=scientific, colorbar=colorbar,
                            permutation=permutation)

    def heatmapf(self, func, scale=None, cmap=None, boundary=True,
                 style='triangular', colorbar=True, scientific=True):
        if not scale:
            scale = self.get_scale()
        if style.lower()[0] == 'd':
            self._boundary_scale = scale + 1
        permutation = self._permutation
        ax = self.get_axes()
        heatmapping.heatmapf(func, scale, cmap=cmap, style=style,
                             boundary=boundary, ax=ax, scientific=scientific,
                             colorbar=colorbar, permutation=permutation)

    def line(self, p1, p2, **kwargs):
        ax = self.get_axes()
        lines.line(ax, p1, p2, **kwargs)

    def horizontal_line(self, i, **kwargs):
        ax = self.get_axes()
        scale = self.get_scale()
        lines.horizontal_line(ax, scale, i, **kwargs) 

    def left_parallel_line(self, i, **kwargs):
        ax = self.get_axes()
        scale = self.get_scale()
        lines.left_parallel_line(ax, scale, i, **kwargs)

    def right_parallel_line(self, i, **kwargs):
        ax = self.get_axes()
        scale = self.get_scale()
        lines.right_parallel_line(ax, scale, i, **kwargs)

    def boundary(self, scale=None, **kwargs):
        # Sometimes you want to draw a bigger boundary
        if not scale:
            scale = self._boundary_scale # defaults to self._scale
        ax = self.get_axes()
        self.resize_drawing_canvas(scale)
        lines.boundary(scale=scale, ax=ax, **kwargs)

    def gridlines(self, multiple=None, horizontal_kwargs=None, left_kwargs=None,
                  right_kwargs=None, **kwargs):
        ax = self.get_axes()
        scale = self.get_scale()
        lines.gridlines(scale=scale, multiple=multiple,
                        ax=ax, horizontal_kwargs=horizontal_kwargs,
                        left_kwargs=left_kwargs, right_kwargs=right_kwargs,
                        **kwargs)

    def set_title(self, title, **kwargs):
        ax = self.get_axes()
        ax.set_title(title, **kwargs)

    def savefig(self, filename, dpi=200, format=None):
        figure = self.get_figure()
        figure.savefig(filename, format=format, dpi=dpi)

    def legend(self, *args, **kwargs):
        ax = self.get_axes()
        ax.legend(*args, **kwargs)

    def resize_drawing_canvas(self, scale=None):
        ax = self.get_axes()
        if not scale:
            scale = self.get_scale()
        plotting.resize_drawing_canvas(ax, scale=scale)

    def show(self):
        pyplot.show()
