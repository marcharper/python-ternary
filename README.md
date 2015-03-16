==============
python-ternary
==============

This is a plotting library for use with matplotlib to allow ternary plots,
plots in the two dimensional simplex projected onto a two dimensional plane.

The library provides functions for plotting projected lines, curves (trajectories), and heatmaps.

========================
Basic Plotting Functions
========================

Most ternary functions expect the simplex to be partititioned into some number of steps. A few functions will do this partitioning for you, but when working with real data or simulation output, you may have partitioned already.

Simplex Boundary and Gridlines
------------------------------

The following code draws a boundary for the simplex and gridlines.

> from maplotlib import pyplot
>
> import ternary
> steps = 30
>
> ax = ternary.draw_boundary(steps)
> ternary.draw_gridlines(steps, ax=ax)
>
> ax.set_title("Simplex Boundary and Gridlines")
>
> pyplot.show()

[Image]

Drawing lines
-------------

You can draw individual lines between any two points with draw_line and lines parallel to the axes with draw_horizonal_line, draw_left_parallel_line, and draw_right_parallel_line:

> from maplotlib import pyplot
>
> import ternary
> steps = 30
>
> ax = ternary.draw_boundary(steps)
> ternary.draw_horizontal_line(ax, steps, 10)
> ternary.draw_left_parallel_line(ax, steps, 15, linewidth=2., color='red')
> ternary.draw_right_parallel_line(ax, steps, 15, linewidth=3., color='blue')
>
> ax.set_title("Various Lines")
>
> pyplot.show()

The line drawing functions accept the matplotlib keyword arguments of Line2D [http://matplotlib.org/api/lines_api.html]

Curves
------

Curves can be plotted by specifying the points of the curve, just like matplotlib's plot. Simply use:

> ternary.plot(points)

Ternary assumes that the points are probability distributions (e.g. x+y+z=1) unless you specify otherwise. Again you can specify axes and line options:

> ternary.plot(points, ax=ax, steps=100, linewidth=2.0)

Heatmaps
--------

Ternary can plot heatmaps in two ways. Given a function, ternary will evaluate the function at the specified number of steps. For example:

> def shannon_entropy(p):
>    """Computes the Shannon Entropy at a distribution in the simplex."""
>    s = 0.
>    for i in range(len(p)):
>        try:
>            s += p[i] * math.log(p[i])
>        except ValueError:
>            continue
>    return -1.*s

Then we can get a heatmap by:

> from maplotlib import pyplot
>
> import ternary
> pyplot.figure()
> ax = ternary.plot_heatmap(func, steps=steps, boundary=True)
> ternary.draw_boundary(steps, ax=ax)
> ax.set_title("Shannon Entropy Heatmap")

In this case the kwarg boundary indicates whether you wish to evaluate points on the boundary of the partition (which is sometimes undesirable).

Ternary can also take a dictionary mapping (x,y) to a float as input for a heatmap, using the function

> heatmap(d, steps, cmap_name=None, boundary=True, ax=None, scientific=False)

You may specify a matplotlib heatmap in the cmap_name argument.




