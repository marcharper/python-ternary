"""
Wrapper class for all ternary plotting functions.
"""

from collections import namedtuple
from functools import partial

import numpy as np
from matplotlib import pyplot as plt

from . import heatmapping
from . import lines
from . import plotting
from .helpers import project_point, convert_coordinates_sequence


BackgroundParameters = namedtuple('BackgroundParameters', ['color', 'alpha', 'zorder'])


def figure(ax=None, scale=None, permutation=None):
    """
    Wraps a Matplotlib AxesSubplot or generates a new one. Emulates matplotlib's
    > figure, ax = plt.subplots()

    Parameters
    ----------
    ax: AxesSubplot, None
        The matplotlib AxesSubplot to wrap
    scale: float, None
        The scale factor of the ternary plot
    """

    ternary_ax = TernaryAxesSubplot(ax=ax, scale=scale, permutation=permutation)
    return ternary_ax.get_figure(), ternary_ax


def mpl_redraw_callback(event, tax):
    """
    Callback to properly rotate and redraw text labels when the plot is drawn
    or resized.

    Parameters
    ----------
    event: a matplotlib event
        either 'resize_event' or 'draw_event'
    tax: TernaryAxesSubplot
         the TernaryAxesSubplot
    """
    tax._redraw_labels()


class TernaryAxesSubplot(object):
    """
    Wrapper for python-ternary and matplotlib figure. Parameters for member
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
            _, self.ax = plt.subplots()
        self.set_scale(scale=scale)
        self._permutation = permutation
        self._boundary_scale = scale
        # Container for the axis labels supplied by the user
        self._labels = dict()
        self._corner_labels = dict()
        self._ticks = dict()
        self._ticklocs = dict()
        # Container for data limits for the axes. Custom limits can
        # be set by the user
        self.set_axis_limits({"b" : [0, self._scale],
                              "r" : [0, self._scale],
                              "l" : [0, self._scale]})

        # Container for parameters describing a possible truncation
        self._truncation = dict()
        self._axis_min_max = {"b" : [0, self._scale],
                              "r" : [0, self._scale],
                              "l" : [0, self._scale]}
        # Container for the redrawing of labels
        self._to_remove = []
        self._connect_callbacks()
        # Background
        self._background_parameters = None
        # Cache for the background triangle object, so it can be removed and redrawn as needed.
        self._background_triangle = None
        self.set_background_color(color="whitesmoke", zorder=-1000, alpha=0.75)

    def _connect_callbacks(self):
        """Connect resize matplotlib callbacks."""
        figure = self.get_figure()
        callback = partial(mpl_redraw_callback, tax=self)
        event_names = ('resize_event', 'draw_event')
        for event_name in event_names:
            figure.canvas.mpl_connect(event_name, callback)

    def __repr__(self):
        return "TernaryAxesSubplot: %s" % self.ax.__hash__()

    def get_axes(self):
        """Returns the underlying matplotlib AxesSubplot object."""
        return self.ax

    def get_figure(self):
        """Return the underlying matplotlib figure object."""
        ax = self.get_axes()
        return ax.get_figure()

    def set_scale(self, scale=None):
        self._scale = scale
        self.resize_drawing_canvas()

    def get_scale(self):
        return self._scale

    def set_axis_limits(self, axis_limits=None):
        """
        Set min and max data limits for each of the three axes.

        max-min for each axis must be the same as the self._scale

        axis_limits = dict
            keys are 'b','l' and 'r' for the three axes
            vals are lists of the min and max values for the axis in
            data units.
        """
        self._axis_limits = axis_limits

    def get_axis_limits(self):
        """Get the data limits for each axis"""
        return self._axis_limits

    def set_axis_min_max(self, truncation):
        """
        Set the min and max values of the axes in SIMPLEX coords
        (rather than data coords) given various
        truncation points.

        !! Assumes the truncation lines do NOT cross each other!!

        truncation: dict (see main module)
        """
        for k in truncation.keys():
            self._axis_min_max[k[0]][1] = truncation[k]
            self._axis_min_max[k[1]][0] = self._scale - truncation[k]


    def get_axis_min_max(self):
        """Get the simplex limits for each axis"""
        return self._axis_min_max


    def set_truncation(self, truncation_data):
        """
        Set one or more truncation lines which will be used to truncate
        the simplex i.e. cut one or more corners off to remove whitespace.

        The self.axis_limits (data limits) and self.axis_min_max (simplex
        limits) are set by this function.

        Truncation lines may not cross each other!

        Parameters
        ----------
        truncation_data : dict
            keys are 'br', 'rl' and/or 'lb'
            values are a value in DATA coords giving the maximum of the
            first axis mentioned in the key. These are then transformed
            into SIMPLEX coords and stored internally.

        Returns
        -------
        None.

        """
        steps = {i : (j[1] - j[0]) / float(self._scale) for i, j in
                 self._axis_limits.items()}

        axlim = {i : j[:] for i, j in self._axis_limits.items()}

        for k in truncation_data:

            self._truncation[k] = int((truncation_data[k]-
                                       axlim[k[0]][0])/steps[k[0]])

            self._axis_limits[k[0]][1] = truncation_data[k]

            self._axis_limits[k[1]][0] = axlim[k[1]][0] + steps[k[1]] *\
                                         (self._scale - self._truncation[k])

        self.set_axis_min_max(self._truncation)
        self._draw_background()


    def get_truncation(self):
        """
        This returns the truncation in SIMPLEX coords
        """
        return self._truncation

    # Title and Axis Labels

    def set_title(self, title, **kwargs):
        """Sets the title on the underlying matplotlib AxesSubplot."""
        ax = self.get_axes()
        ax.set_title(title, **kwargs)

    def left_axis_label(self, label, position=None, rotation=60, offset=0.08,
                        transform_type="transData", **kwargs):
        """
        Sets the label on the left axis.

        Parameters
        ----------
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
            transform_type = "transAxes"
        self._labels["left"] = (label, position, rotation,
                                transform_type, kwargs)

    def right_axis_label(self, label, position=None, rotation=-60, offset=0.08,
                         transform_type="transData", **kwargs):

        """
        Sets the label on the right axis.

        Parameters
        ----------
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
            position = (2. / 5 + offset, 3. / 5, 0)
            transform_type = "transAxes"
        self._labels["right"] = (label, position, rotation,
                                 transform_type, kwargs)

    def bottom_axis_label(self, label, position=None, rotation=0, offset=0.02,
                          transform_type="transData", **kwargs):
        """
        Sets the label on the bottom axis.

        Parameters
        ----------
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
            position = (0.5, -offset / 2., 0.5)
            transform_type = "transAxes"
        self._labels["bottom"] = (label, position, rotation,
                                  transform_type, kwargs)

    def right_corner_label(self, label, position=None, rotation=0, offset=0.08,
                           transform_type="transData", **kwargs):
        """
        Sets the label on the right corner (complements left axis).

        Parameters
        ----------
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
            position = (1, offset / 2, 0)
            transform_type = "transAxes"
        self._corner_labels["right"] = (label, position, rotation,
                                        transform_type, kwargs)

    def left_corner_label(self, label, position=None, rotation=0, offset=0.08,
                          transform_type="transData", **kwargs):
        """
        Sets the label on the left corner (complements right axis.)

        Parameters
        ----------
        label: string
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
            position = (-offset / 2, offset / 2, 0)
            transform_type="transAxes"
        self._corner_labels["left"] = (label, position, rotation,
                                       transform_type, kwargs)

    def top_corner_label(self, label, position=None, rotation=0, offset=0.2,
                         transform_type="transData", **kwargs):
        """
        Sets the label on the bottom axis.

        Parameters
        ----------
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
            position = (-offset / 2, 1 + offset, 0)
            transform_type="transAxes"
        self._corner_labels["top"] = (label, position, rotation,
                                      transform_type, kwargs)

    def annotate(self, text, position, **kwargs):
        ax = self.get_axes()
        p = project_point(position)
        ax.annotate(text, (p[0], p[1]), **kwargs)

    # Boundary and Gridlines

    def boundary(self, scale=None, axes_colors=None, **kwargs):
        """
        Draw a boundary around the simplex.

        Parameters
        ----------
        scale : INT, optional
            An int describing the scale of the boundary to be drawn.
            Sometimes you may want to draw a bigger boundary than
            specified in the initialisation of the tax. The default is None.
        axes_colors: dict
            Option for coloring boundaries different colors.
            e.g. {'l': 'g'} for coloring the left axis boundary green
        **kwargs : dict
            Any kwargs to pass through to matplotlib..

        Returns
        -------
        None.

        """
        # Sometimes you want to draw a bigger boundary
        if not scale:
            scale = self._boundary_scale # defaults to self._scale
        ax = self.get_axes()
        self.resize_drawing_canvas(scale)

        lines.boundary(ax, scale, self._axis_min_max,
                       axes_colors=axes_colors, **kwargs)


    def gridlines(self, multiple=None, horizontal_kwargs=None,
                  left_kwargs=None, right_kwargs=None, **kwargs):
        """
        Draw gridlines on the simplex (excluding the boundary).

        Parameters
        ----------
        multiple: int, optional
            Specifies which inner gridelines to draw. For example,
            if scale=30 and multiple=6, only 5 inner gridlines will be drawn.
            The default is None.
        horizontal_kwargs: dict, optional
            Any kwargs to pass through to matplotlib for horizontal gridlines
            The default is None.
        left_kwargs: dict, optional
            Any kwargs to pass through to matplotlib for left parallel gridlines
        right_kwargs: dict, optional
            Any kwargs to pass through to matplotlib for right parallel gridlines
            The default is None.
        kwargs:
            Any kwargs to pass through to matplotlib, if not using
            horizontal_kwargs, left_kwargs, or right_kwargs

        Returns
        -------
        None.

        """
        ax = self.get_axes()
        scale = self.get_scale()

        lines.gridlines(ax, scale, self._axis_min_max,
                        multiple=multiple,
                        horizontal_kwargs=horizontal_kwargs,
                        left_kwargs=left_kwargs,
                        right_kwargs=right_kwargs,
                        **kwargs)

    # Various Lines

    def line(self, p1, p2, **kwargs):
        ax = self.get_axes()
        permutation = self._permutation
        lines.line(ax, p1, p2, permutation=permutation, **kwargs)

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

    # Matplotlib passthroughs

    def close(self):
        fig = self.get_figure()
        plt.close(fig)

    def legend(self, *args, **kwargs):
        ax = self.get_axes()
        ax.legend(*args, **kwargs)

    def savefig(self, filename, **kwargs):
        self._redraw_labels()
        fig = self.get_figure()
        if 'dpi' not in kwargs:
            kwargs['dpi'] = 200
        fig.savefig(filename, **kwargs)

    def show(self):
        self._redraw_labels()
        plt.show()

    # Axis ticks

    def clear_matplotlib_ticks(self, axis="both"):
        """Clears the default matplotlib ticks."""
        ax = self.get_axes()
        plotting.clear_matplotlib_ticks(ax=ax, axis=axis)


    def get_ticks_from_axis_limits(self, multiple=1):
        """
        Taking self._axis_limits, self.axis_min_max and self._scale get the
        ticks for all three axes and store them in self._ticks under the
        keys 'b' for bottom, 'l' for left and 'r' for right axes. Get the
        locations of the tickes and store them under self._ticklocs with the
        same keys.

        NB. the tick locations for the left axis have to be shifted if there
        is a truncation of that axis, otherwise they are projected in the
        wrong place by lines.line(), which calls helpers.project_point().
        """
        for k in ['b','l','r']:
            gg = self._axis_min_max[k][1] - self._axis_min_max[k][0]
            ff = self._axis_limits[k][1] - self._axis_limits[k][0]
            step = ff/gg

            self._ticklocs[k] = np.arange(self._axis_min_max[k][0],
                                          self._axis_min_max[k][1] + step,
                                          multiple).astype("int").tolist()

            self._ticks[k] = np.arange(self._axis_limits[k][0],
                                       self._axis_limits[k][1] + step,
                                       step*multiple).tolist()


        self._ticklocs['l'] = [i - self._axis_min_max["l"][0] +
                               (self._scale - self._axis_min_max["l"][1])
                               for i in self._ticklocs['l']]



    def set_custom_ticks(self, clockwise=False, axes_colors=None,
                         tick_formats=None, **kwargs):
        """
        Having called get_ticks_from_axis_limits(), draw the custom ticks on
        the plot. We call self.ticks() for each axis in turn with the ticks
        and ticklocs already defined using get_ticks_from_axis_limits().

        Parameters
        ----------
        clockwise : BOOL, optional
            Whether the axes of the simplex run clockwise or not.
            The default is False.
        axes_colors: Dict, optional
            Option to color ticks differently for each axis, 'l', 'r', 'b'
            e.g. {'l': 'g', 'r':'b', 'b': 'y'}
            The default is None.
        tick_formats: None, Dict, Str, optional
            If None, all axes will be labelled with ints.
            If Dict, the keys are 'b', 'l' and 'r' and the values are
            format strings e.g. "%.3f" for a float with 3 decimal places
            or "%.3e" for scientific format with 3 decimal places or
            "%d" for ints.
            If tick_formats is a string, it is assumed that this is a
            format string to be applied to all axes.
            The default is None
        kwargs:
            Any kwargs to pass through to matplotlib.

        Returns
        -------
        None.

        """
        for k in ['b','l','r']:
            self.ticks(ticks=self._ticks[k], locations=self._ticklocs[k],
                       axis=k, clockwise=clockwise, axes_colors=axes_colors,
                       tick_formats=tick_formats, **kwargs)


    def ticks(self, ticks=None, locations=None, multiple=1, axis='blr',
              clockwise=False, axes_colors=None, tick_formats=None, **kwargs):
        ax = self.get_axes()
        scale = self.get_scale()
        lines.ticks(ax, scale, ticks=ticks, locations=locations,
                    multiple=multiple, clockwise=clockwise, axis=axis,
                    axes_colors=axes_colors, tick_formats=tick_formats,
                    **kwargs)


    def add_extra_tick(self, axis, loc1, offset, tick, fontsize, **kwargs):
        """
        Convenience function passthrough to lines.add_extra_tick.

        Add an extra tick on an axis but not necessarily on
        the boundary of the simplex. This may be useful if a
        truncation is applied.

        Parameters
        ----------
        axis : STR
            A string giving the axis on which the extra tick should be drawn.
            One of 'l', 'b' or 'r'.
        loc1 : 3-tuple
            A 3-tuple giving the location of the extra tick in simplex coords.
        offset : FLOAT
            Defines an offset of the tick label and the length of the tick
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
        lines.add_extra_tick(self.get_axes(), axis, loc1, offset,
                             self.get_scale(), tick, fontsize, **kwargs)


    # Redrawing and resizing

    def resize_drawing_canvas(self, scale=None):
        ax = self.get_axes()
        if not scale:
            scale = self.get_scale()
        plotting.resize_drawing_canvas(ax, scale=scale)


    def _redraw_labels(self):
        """
        Redraw axis labels, typically after draw or resize events.
        """
        ax = self.get_axes()
        # Remove any previous labels
        for mpl_object in self._to_remove:
            mpl_object.remove()
        self._to_remove = []
        # Redraw the labels with the appropriate angles
        label_data = list(self._labels.values())
        label_data.extend(self._corner_labels.values())
        for (label, position, rotation, transform_type, kwargs) in label_data:
            if transform_type == "transAxes":
                transform = ax.transAxes
            elif transform_type == "transData":
                transform = ax.transData

            x, y = project_point(position)
            # Calculate the new angle.
            position = np.array([x, y])
            new_rotation = ax.transData.transform_angles(np.array((rotation,)),
                                                          position.reshape((1, 2)))[0]
            text = ax.text(x, y, label, rotation=new_rotation,
                           transform=transform, horizontalalignment="center",
                           **kwargs)
            text.set_rotation_mode("anchor")
            self._to_remove.append(text)


    def convert_coordinates(self, points, axisorder='blr'):
        """
        Convert data coordinates to simplex coordinates for plotting
        in the case that axis limits have been applied.
        """
        return convert_coordinates_sequence(points, self._boundary_scale,
                                            self._axis_limits, axisorder)

    # Various Plots

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


    def heatmap(self, data, scale=None, cmap=None, scientific=False,
                style='triangular', colorbar=True, use_rgba=False,
                vmin=None, vmax=None, cbarlabel=None, cb_kwargs=None):
        permutation = self._permutation
        if not scale:
            scale = self.get_scale()
        if style.lower()[0] == 'd':
            self._boundary_scale = scale + 1
        ax = self.get_axes()
        heatmapping.heatmap(data, scale, cmap=cmap, style=style, ax=ax,
                            scientific=scientific, colorbar=colorbar,
                            permutation=permutation, use_rgba=use_rgba,
                            vmin=vmin, vmax=vmax, cbarlabel=cbarlabel,
                            cb_kwargs=cb_kwargs)


    def heatmapf(self, func, scale=None, cmap=None, boundary=True,
                 style='triangular', colorbar=True, scientific=False,
                 vmin=None, vmax=None, cbarlabel=None, cb_kwargs=None):
        if not scale:
            scale = self.get_scale()
        if style.lower()[0] == 'd':
            self._boundary_scale = scale + 1
        permutation = self._permutation
        ax = self.get_axes()
        heatmapping.heatmapf(func, scale, cmap=cmap, style=style,
                             boundary=boundary, ax=ax, scientific=scientific,
                             colorbar=colorbar, permutation=permutation,
                             vmin=vmin, vmax=vmax, cbarlabel=cbarlabel,
                             cb_kwargs=cb_kwargs)


    def set_background_color(self, color="whitesmoke", zorder=-1000, alpha=0.75):
        self._background_parameters = BackgroundParameters(color=color, alpha=alpha, zorder=zorder)
        self._draw_background()


    def _draw_background(self):
        color, alpha, zorder = self._background_parameters
        scale = self.get_scale()
        ax = self.get_axes()
        axis_min_max = self.get_axis_min_max()

        # Remove any existing background
        if self._background_triangle:
            self._background_triangle.remove()

        # Draw the background
        self._background_triangle = heatmapping.background_color(ax, color, scale,
                                                                 axis_min_max,
                                                                 alpha=alpha,
                                                                 zorder=zorder)[0]
