
========================================================
ternary : A python ternary plotting library based on matplotlib
========================================================

This library provides a few basic functions for creating ternary plots that are not included in matplotlib. In particular, with ternary you can plots curves in the 2-simplex and also make heatmaps. There are several examples in examples.py for both types of plots. See the following URL for information on ternary plots.

http://en.wikipedia.org/wiki/Ternary_plot

Curve plotting
--------------

Simply use the function ternary.plot to plot a sequence of probability distributions in the 2-simplex, which can be given as lists, tuples, or numpy arrays of length 3. It is assummed that the distributions have not yet been projected into the planar representation of the simplex. You can manually project distributions or sequences of distributions with ternary.project .

The boundary of the simplex can be plotted with ternary.draw_boundary() . Both draw_boundary and plot accept color and linewidth parameters that are passed through to pyplot. draw_boundary also accepts a scale parameter for use with heatmaps and non-normalized data.

Heatmaps
--------

The heatmap functionality is a bit more complex. The simplex is divided into triangular regions that are indentified with integer indices (analogous to a partition of an interval or a rectangle), with the number of steps specified by the user. The heatmap function accepts a dictionary on these indices with values that are used to create the colors of the heatmap. Complementary triangles take the average of neighboring triangles to produce a smooth coloration.

The easiest way to use the heatmap functionality is to pass a function to ternary.plot_heatmap, which has signature:

    def plot_heatmap(func, steps=40, boundary=True, cmap_name=None)

ternary will divide up the simplex based on the parameter steps and evaluate the function at the appropriate simplex points.

Tips for nice looking plots
---------------------------

-- If a heatmap looks grainy, use steps = 100 or steps = 200 to get a smoother image. This will take longer (since many more triangular regions are drawn individually).

-- Lack of color variation: try a different colormap (just pass the matplotlib name of the colormap to plot_heatmap in the cmap_name kwarg) and/or try transforming the data (take the log, for instance). See the following URL for a list of built in matplotlib colormaps.

http://www.scipy.org/Cookbook/Matplotlib/Show_colormaps

-- Removing/altering the axis ticks: use pyplot.xticks([]) and pyplot.yticks([])
