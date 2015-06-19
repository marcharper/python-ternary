"""
Wrapper class for all ternary plotting functions.
"""

from matplotlib import pyplot

import heatmapping
import lines
import plotting


def figure(ax=None, scale=None):
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

    ternary_ax = TernaryAxesSubplot(ax=ax, scale=scale)
    return ternary_ax.get_figure(), ternary_ax


class TernaryAxesSubplot(object):
    """Wrapper for python-ternary and matplotlib figure."""

    def __init__(self, ax=None, scale=None):
        if not scale:
            scale = 1.0
        if ax:
            self.ax = ax
        else:
            _, self.ax = pyplot.subplots()
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

    def scatter(self, points, **kwargs):
        plot_ = plotting.scatter(points, ax=self.get_axes(), **kwargs)
        return plot_

    def plot(self, points, **kwargs):
        plotting.plot(points, ax=self.get_axes(), **kwargs)

    def plot_colored_trajectory(self, points, cmap=None, **kwargs):
        plotting.plot_colored_trajectory(points, cmap=cmap, ax=self.get_axes(), **kwargs)

    def clear_matplotlib_ticks(self, axis="both"):
        plotting.clear_matplotlib_ticks(ax=self.get_axes(),
                                        axis=axis)

    def left_axis_label(self, label, position=None, **kwargs):
        plotting.left_axis_label(self.get_axes(), label, position=position,
                                 **kwargs)

    def right_axis_label(self, label, position=None, **kwargs):
        plotting.right_axis_label(self.get_axes(), label, position=position,
                                  **kwargs)

    def bottom_axis_label(self, label, position=None, **kwargs):
        plotting.bottom_axis_label(self.get_axes(), label, position=position,
                                   **kwargs)

    def heatmap(self, data, scale=None, cmap=None, scientific=False,
                style='triangular', colorbar=True):
        if not scale:
            scale = self.get_scale()
        if style.lower()[0] == 'd':
            self._boundary_scale = scale + 1
        ax = self.get_axes()
        heatmapping.heatmap(data, scale, cmap=cmap, style=style,
                            ax=ax, scientific=scientific,
                            colorbar=colorbar)

    def heatmapf(self, func, scale=None, cmap=None,
                            boundary=True, style='triangular', colorbar=True,
                            scientific=True):
        if not scale:
            scale = self.get_scale()
        if style.lower()[0] == 'd':
            self._boundary_scale = scale + 1
        ax = self.get_axes()
        heatmapping.heatmapf(func, scale, cmap=cmap,
                                        style=style, boundary=boundary, 
                                        ax=ax, scientific=scientific,
                                        colorbar=colorbar)

    def line(self, p1, p2, **kwargs):
        lines.line(self.ax, p1, p2, **kwargs)

    def horizontal_line(self, i, **kwargs):
        lines.horizontal_line(self.get_axes(), self.get_scale(), i, **kwargs) 

    def left_parallel_line(self, i, **kwargs):
        lines.left_parallel_line(self.get_axes(), self.get_scale(), i, **kwargs)

    def right_parallel_line(self, i, **kwargs):
        lines.right_parallel_line(self.get_axes(), self.get_scale(), i, **kwargs)

    def boundary(self, scale=None, **kwargs):
        # Sometimes you want to draw a bigger boundary
        if not scale:
            scale = self._boundary_scale
        self.resize_drawing_canvas(scale)
        ax = self.get_axes()
        lines.boundary(scale=scale, ax=ax, **kwargs)

    def gridlines(self, multiple=None, horizontal_kwargs=None, left_kwargs=None,
                  right_kwargs=None, **kwargs):
        lines.gridlines(scale=self.get_scale(), multiple=multiple,
                        ax=self.get_axes(), horizontal_kwargs=horizontal_kwargs,
                        left_kwargs=left_kwargs, right_kwargs=right_kwargs,
                        **kwargs)

    def set_title(self, title, **kwargs):
        ax = self.get_axes()
        ax.set_title(title, **kwargs)

    def save_fig(self, filename, dpi=200, format=None):
        figure = self.get_figure()
        figure.save_fig(filename, format=format, dpi=dpi)
    
    def legend(self, *args, **kwargs):
        ax = self.get_axes()
        ax.legend(*args, **kwargs)

    def resize_drawing_canvas(self, scale=None):
        if not scale:
            scale = self.get_scale()
        plotting.resize_drawing_canvas(self.ax, scale=scale)

    def show(self):
        pyplot.show()
