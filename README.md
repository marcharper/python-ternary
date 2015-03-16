# python-ternary

This is a plotting library for use with [matplotlib](http://matplotlib.org/index.html) to make [ternary plots](http://en.wikipedia.org/wiki/Ternary_plot),
plots in the two dimensional simplex projected onto a two dimensional plane.

The library provides functions for plotting projected lines, curves (trajectories), and heatmaps.

# Basic Plotting Functions

Most ternary functions expect the simplex to be partititioned into some number of steps. A few functions will do this partitioning for you, but when working with real data or simulation output, you may have partitioned already.

## Simplex Boundary and Gridlines

The following code draws a boundary for the simplex and gridlines.

```
from maplotlib import pyplot
import ternary

steps = 30

ax = ternary.draw_boundary(steps)
ternary.draw_gridlines(steps, ax=ax)
ax.set_title("Simplex Boundary and Gridlines")

pyplot.show()
```

![](https://camo.githubusercontent.com/7892a5bc0c1d4023d02e3d9dfe616b9667a77d65/687474703a2f2f692e696d6775722e636f6d2f647074723655412e6a7067)

## Drawing lines

You can draw individual lines between any two points with draw_line and lines parallel to the axes with draw_horizonal_line, draw_left_parallel_line, and draw_right_parallel_line:

```
from maplotlib import pyplot

import ternary
steps = 30

ax = ternary.draw_boundary(steps)
ternary.draw_horizontal_line(ax, steps, 10)
ternary.draw_left_parallel_line(ax, steps, 15, linewidth=2., color='red')
ternary.draw_right_parallel_line(ax, steps, 15, linewidth=3., color='blue')

ax.set_title("Various Lines")

pyplot.show()
```

The line drawing functions accept the matplotlib keyword arguments of Line2D [http://matplotlib.org/api/lines_api.html]

![](https://camo.githubusercontent.com/1723ffcaa3c843b74b802ba0c0e5a9e8535ea8a7/687474703a2f2f692e696d6775722e636f6d2f49426b454646332e6a7067)

## Curves

Curves can be plotted by specifying the points of the curve, just like matplotlib's plot. Simply use:

```
ternary.plot(points)
```

Points is a list of tuples or numpy arrays, e.g. [(0.5, 0.25, 0.25), (1./3, 1./3, 1//3)]. Ternary assumes that the points are probability distributions (e.g. x+y+z=1) unless you specify otherwise. Again you can specify axes and line options:

```
ternary.plot(points, ax=ax, steps=100, linewidth=2.0)
```

![](https://camo.githubusercontent.com/023639b15fbdf421df2462bc5eed646c326be152/687474703a2f2f692e696d6775722e636f6d2f687753524439372e6a7067)

## Heatmaps

Ternary can plot heatmaps in two ways. Given a function, ternary will evaluate the function at the specified number of steps. For example:

```
def shannon_entropy(p):
    """Computes the Shannon Entropy at a distribution in the simplex."""
    s = 0.
    for i in range(len(p)):
        try:
            s += p[i] * math.log(p[i])
        except ValueError:
            continue
    return -1.*s
```

Then we can get a heatmap as follows:

```
from maplotlib import pyplot

import ternary
pyplot.figure()
ax = ternary.plot_heatmap(func, steps=steps, boundary=True)
ternary.draw_boundary(steps, ax=ax)
ax.set_title("Shannon Entropy Heatmap")

pyplot.show()
```

In this case the keyword argument *boundary* indicates whether you wish to evaluate points on the boundary of the partition (which is sometimes undesirable).

![](https://camo.githubusercontent.com/c8727b30461d45b860cb49bfde4f48e0f76526ff/687474703a2f2f692e696d6775722e636f6d2f6b586d317075462e6a7067)

Ternary can also take a dictionary mapping (x,y) to a float as input for a heatmap, using the function

```
ternary.heatmap(d, steps, cmap_name=None, boundary=True, ax=None, scientific=False)
```

![](https://camo.githubusercontent.com/30fb63ec53deb0fda2c892c0732a97620699500b/687474703a2f2f692e696d6775722e636f6d2f64555a6b3355302e6a7067)

[](https://camo.githubusercontent.com/b66c280914cb4a38130b83a3eb4311f94274aefb/687474703a2f2f692e696d6775722e636f6d2f6935516a5147542e6a7067)


You may specify a [matplotlib colormap](http://matplotlib.org/examples/color/colormaps_reference.html) in the cmap_name argument.

