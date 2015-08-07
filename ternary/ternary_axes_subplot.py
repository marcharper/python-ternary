"""
Wrapper class for all ternary plotting functions.
"""

from functools import partial

import numpy
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

def mpl_redraw_callback(event, tax):
    """
    Callback to properly rotate and redraw text labels when the plot is drawn 
    or resized.

    Parameters:
    event: a matplotlib event
        either 'resize_event' or 'draw_event'
    tax: TernaryAxesSubplot
         the TernaryAxesSubplot 
    """

    #http://stackoverflow.com/questions/4018860/text-box-with-line-wrapping-in-matplotlib

    ax = tax.get_axes()
    figure = tax.get_figure()

    ## Axis Labels
    # Remove any previous labels
    for mpl_object in tax._to_remove:
        mpl_object.remove()
    tax._to_remove = []
    # Redraw the labels with the appropriate angles
    for (label, position, rotation, kwargs) in tax._labels.values():
        transform = ax.transAxes
        x, y = project_point(position)
        # Calculate the new angle.
        position = numpy.array([x,y])
        new_rotation = ax.transData.transform_angles(numpy.array((rotation,)), position.reshape((1,2)))[0]
        text = ax.text(x, y, label, rotation=new_rotation, transform=transform,
                       horizontalalignment="center", **kwargs)
        text.set_rotation_mode("anchor")
        tax._to_remove.append(text)

    # Temporarily disconnect any callbacks to the draw event...
    # (To avoid recursion)
    func_handles = figure.canvas.callbacks.callbacks[event.name]
    figure.canvas.callbacks.callbacks[event.name] = {}
    # Re-draw the figure..
    figure.canvas.draw()
    # Reset the draw event callbacks
    figure.canvas.callbacks.callbacks[event.name] = func_handles


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
        self._labels = dict() # Container for the axis labels supplied by the user
        self._to_remove = [] # Container for the redrawing of labels

        # Connect resize and redraw matplotlib callbacks
        event_names = ('resize_event', 'draw_event')
        figure = self.get_figure()
        callback = partial(mpl_redraw_callback, tax=self)
        for event_name in event_names:
            figure.canvas.mpl_connect(event_name, callback)

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

    def left_axis_label(self, label, position=None,  rotation=60, offset=0.08,
                        **kwargs):
        """
        Sets the label on the left axis.

        Parameters
        ----------
        ax: Matplotlib AxesSubplot, None
            The subplot to draw on.
        label: String
            The axis label
        position: 3-Tuple of floats, None
            The position of the text label
        rotation: float, 60
            The angle of rotation of the label
        offset: float,
            Used to compute the distance of the label from the axis
        kwargs:
            Any kwargs to pass through to matplotlib.
        """

        if not position:
            position = (-offset, 3./5, 2./5)
        self._labels["left"] = (label, position, rotation, kwargs)

    def right_axis_label(self, label, position=None, rotation=-60, offset=0.08,
                         **kwargs):
        """
        Sets the label on the right axis.

        Parameters
        ----------
        ax: Matplotlib AxesSubplot, None
            The subplot to draw on.
        label: String
            The axis label
        position: 3-Tuple of floats, None
            The position of the text label
        rotation: float, -60
            The angle of rotation of the label
        offset: float,
            Used to compute the distance of the label from the axis
        kwargs:
            Any kwargs to pass through to matplotlib.
        """

        if not position:
            position = (2./5 + offset, 3./5, 0)
        self._labels["right"] = (label, position, rotation, kwargs)

    def bottom_axis_label(self, label, position=None, rotation=0, offset=0.02,
                          **kwargs):
        """
        Sets the label on the bottom axis.

        Parameters
        ----------
        ax: Matplotlib AxesSubplot, None
            The subplot to draw on.
        label: String
            The axis label
        position: 3-Tuple of floats, None
            The position of the text label
        rotation: float, 0
            The angle of rotation of the label
        offset: float,
            Used to compute the distance of the label from the axis
        kwargs:
            Any kwargs to pass through to matplotlib.
        """

        if not position:
            position = (1./2, offset, 1./2)
        self._labels["bottom"] = (label, position, rotation, kwargs)

    def heatmap(self, data, scale=None, cmap=None, scientific=False,
                style='triangular', colorbar=True, colormap=True):
        permutation = self._permutation
        if not scale:
            scale = self.get_scale()
        if style.lower()[0] == 'd':
            self._boundary_scale = scale + 1
        ax = self.get_axes()
        heatmapping.heatmap(data, scale, cmap=cmap, style=style, ax=ax,
                            scientific=scientific, colorbar=colorbar,
                            permutation=permutation, colormap=colormap)

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

    def ticks(self, ticks=None, locations=None, multiple=1, axis='b',
              clockwise=False, **kwargs):
        ax = self.get_axes()
        scale = self.get_scale()
        lines.ticks(ax, scale, ticks=ticks, locations=locations,
                    multiple=multiple, clockwise=clockwise, axis=axis, 
                    **kwargs)

    def show(self):
        pyplot.show()
