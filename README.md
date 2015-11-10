# Welcome!

<a href="https://pypi.python.org/pypi/python-ternary"><img src="https://img.shields.io/pypi/v/python-ternary.svg"/></a>
[![Join the chat at https://gitter.im/marcharper/python-ternary](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/marcharper/python-ternary?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

# python-ternary

This is a plotting library for use with [matplotlib](http://matplotlib.org/index.html) to make [ternary plots](http://en.wikipedia.org/wiki/Ternary_plot)
plots in the two dimensional simplex projected onto a two dimensional plane.

The library provides functions for plotting projected lines, curves (trajectories), scatter plots, and heatmaps. There are [several examples](https://github.com/marcharper/python-ternary/blob/master/examples.py) and a short tutorial below.

Most ternary functions expect the simplex to be partititioned into some number of steps, determined by the scale parameter. A few functions will do this partitioning for you, but when working with real data or simulation output, you may have partitioned already. if you are working with probability distributions, just use `scale=1` (the default). Otherwise the scale parameter effectively controls the resolution of many plot types (e.g. heatmaps).

# Gallery

<div style="text-align:center">

<img src ="/readme_images/boundary_and_gridlines.png" width="150" height="150"/>
<img src ="/readme_images/various_lines.png" width="150" height="150"/>
<img src ="/readme_images/colored_trajectory.png" width="150" height="150"/>
<img src ="/readme_images/scatter.png" width="150" height="150"/>
<img src ="/readme_images/heatmap_rsp.png" width="150" height="150"/>
<img src ="/readme_images/16_80_1.png" width="150" height="150"/>
<img src ="/readme_images/16_80_stationary.png" width="150" height="150"/>
<img src ="/readme_images/23_80_0.png" width="150" height="150"/>
<img src ="/readme_images/24_80_1.png" width="150" height="150"/>
<img src ="/readme_images/colored_boundary.png" width="150" height="150"/>
</div>

# Installation

You can install the current release (0.1) with pip (you may need to use sudo):
```bash
    pip install python-ternary
```

Alternatively you can clone the repository and run `setup.py` in the usual manner:

```bash
    git clone git@github.com:marcharper/python-ternary.git
    cd python-ternary
    sudo python setup.py install
```

New features are still being added to python-ternary.

# Basic Plotting Functions

The easiest way to use python-ternary is with the wrapper class `TernaryAxesSubplot`,
which mimics Matplotlib's AxesSubplot. Start with

```python
    figure, tax = ternary.figure()
```

With a ternary axes object `tax` you can use many of the usual matplotlib 
axes object functions:

```python
    tax.set_title("Scatter Plot", fontsize=20)
    tax.scatter(points, marker='s', color='red', label="Red Squares")
    tax.legend()
```

Most drawing functions can take standard matplotlib keyword arguments such as
[linestyle](http://matplotlib.org/api/lines_api.html#matplotlib.lines.Line2D.set_linestyle)
and linewidth. You can use LaTeX in titles and labels.

If you need to act directly on the underyling matplotlib axes, you can access them:

```python
    ax = tax.get_axes()
```

You can also wrap a Matplotlib AxesSubplot object:

```
    figure, ax = pyplot.subplots()
    tax = ternary.TernaryAxesSubplot(ax=ax)
```

This is useful if you want to use ternary as part of another figure, such as

```python
    from matplotlib import pyplot, gridspec

    pyplot.figure()
    gs = gridspec.GridSpec(2,2)
    ax = pyplot.subplot(gs[0,0])
    figure, tax = ternary.figure(ax=ax)
    ...
````

`TernaryAxesSubplot` objects keep track of the scale, axes, and other parameters,
supplying them as needed to other functions.

## Simplex Boundary and Gridlines

The following code draws a boundary for the simplex and gridlines.

```python
    from matplotlib import pyplot
    import ternary

    ## Boundary and Gridlines
    scale = 40
    figure, tax = ternary.figure(scale=scale)

    # Draw Boundary and Gridlines
    tax.boundary(linewidth=2.0)
    tax.gridlines(color="blue", multiple=5) # Every 5th gridline, can be a float

    # Set Axis labels and Title
    fontsize = 20
    tax.set_title("Simplex Boundary and Gridlines", fontsize=fontsize)
    tax.left_axis_label("Left label $\\alpha^2$", fontsize=fontsize)
    tax.right_axis_label("Right label $\\beta^2$", fontsize=fontsize)
    tax.bottom_axis_label("Bottom label $\\Gamma - \\Omega$", fontsize=fontsize)

    # Set ticks
    tax.ticks(axis='lbr', linewidth=1)

    # Remove default Matplotlib Axes
    tax.clear_matplotlib_ticks()

    pyplot.show()
```

![Ternary Plot -- Boundary and Gridlines](/readme_images/boundary_and_gridlines.png)

## Drawing lines

You can draw individual lines between any two points with `line` and lines parallel to the axes with `horizonal_line`, `left_parallel_line`, and `right_parallel_line`:

```python
    import ternary

    scale = 40
    figure, tax = ternary.figure(scale=scale)

    # Draw Boundary and Gridlines
    tax.boundary(linewidth=2.0)
    tax.gridlines(color="blue", multiple=5)

    # Set Axis labels and Title
    fontsize = 20
    tax.set_title("Various Lines", fontsize=20)
    tax.left_axis_label("Left label $\\alpha^2$", fontsize=fontsize)
    tax.right_axis_label("Right label $\\beta^2$", fontsize=fontsize)
    tax.bottom_axis_label("Bottom label $\\Gamma - \\Omega$", fontsize=fontsize)

    # Draw lines parallel to the axes
    tax.horizontal_line(16)
    tax.left_parallel_line(10, linewidth=2., color='red', linestyle="--")
    tax.right_parallel_line(20, linewidth=3., color='blue')
    # Draw an arbitrary line, ternary will project the points for you
    p1 = (12,8,10)
    p2 = (2, 26, 2)
    tax.line(p1, p2, linewidth=3., marker='s', color='green', linestyle=":")

    tax.ticks(axis='lbr', multiple=5, linewidth=1)

    tax.show()
```

The line drawing functions accept the matplotlib keyword arguments of [Line2D](http://matplotlib.org/api/lines_api.html).

![Ternary Plot -- Various Lines](/readme_images/various_lines.png)

## Curves

Curves can be plotted by specifying the points of the curve, just like matplotlib's plot. Simply use:

```
    ternary.plot(points)
```

Points is a list of tuples or numpy arrays, such as [(0.5, 0.25, 0.25), (1./3, 1./3, 1./3)],

```python
    import ternary

    ## Sample trajectory plot
    figure, tax = ternary.figure(scale=1.0)
    tax.boundary()
    tax.gridlines(multiple=0.2, color="black")
    tax.set_title("Plotting of sample trajectory data", fontsize=20)
    points = []
    # Load some data, tuples (x,y,z)
    with open("sample_data/curve.txt") as handle:
        for line in handle:
            points.append(map(float, line.split(' ')))
    # Plot the data
    tax.plot(points, linewidth=2.0, label="Curve")
    tax.legend()
    tax.show()
```

![Ternary Curve Plot](/readme_images/trajectory.png)

There are many more examples in [this paper](http://arxiv.org/abs/1210.5539).

You can also color the curves with a Matplotlib heatmap using:
```
    plot_colored_trajectory(points, cmap="hsv", linewidth=2.0)
```

![Ternary Curve Plot](/readme_images/colored_trajectory.png)

## Scatter Plots

Similarly, ternary can make scatter plots:

```python
    import ternary

    ### Scatter Plot
    scale = 40
    figure, tax = ternary.figure(scale=scale)
    tax.set_title("Scatter Plot", fontsize=20)
    tax.boundary(linewidth=2.0)
    tax.gridlines(multiple=5, color="blue")
    # Plot a few different styles with a legend
    points = random_points(30, scale=scale)
    tax.scatter(points, marker='s', color='red', label="Red Squares")
    points = random_points(30, scale=scale)
    tax.scatter(points, marker='D', color='green', label="Green Diamonds")
    tax.legend()
    tax.ticks(axis='lbr', linewidth=1, multiple=0.1)

    tax.show()

```

![Ternary Scatter Plot Example](/readme_images/scatter.png)

## Heatmaps

Ternary can plot heatmaps in two ways and three styles. Given a function, ternary
will evaluate the function at the specified number of steps (determined by the 
scale, expected to be an integer in this case). The simplex can be split up into
triangles or hexagons and colored according to one of three styles:

- Triangular -- `triangular`: coloring triangles by summing the values on the
vertices
- Dual-triangular  -- `dual-triangular`: mapping (i,j,k) to the upright 
triangles &#9651; and blending the neigboring triangles for the downward 
triangles &#9661;
- Hexagonal  -- `hexagonal`: which does not blend values at all, and divides
the simplex up into heaxagonal regions

The two triangular heatmap styles and the hexagonal heatmap style can be visualized as follows. The `dual-triangular` style plots the true values on the upright triangles, mapping ternary coordinates to upright triangles otherwise. The `triangular` style
maps ternary coordinates to vertices and computes the triangle color based on the
values at the vertices.

<img src ="/readme_images/heatmap-grids.png" width="500" height="250"/>

![](/readme_images/heatmap_styles_cubehelix.png)

Thanks to [chebee7i](https://github.com/chebee7i) for the above images.

Let's define a function on the simplex for illustration, the [Shannon entropy](http://en.wikipedia.org/wiki/Entropy_%28information_theory%29) of a probability distribution:

```python
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

We can get a heatmap of this function as follows:

```python
    import ternary
    scale = 60

    figure, tax = ternary.figure(scale=scale)
    tax.heatmapf(shannon_entropy, boundary=True, style="triangular")
    tax.boundary(linewidth=2.0)
    tax.set_title("Shannon Entropy Heatmap")

    tax.show()
```

In this case the keyword argument *boundary* indicates whether you wish to evaluate points on the boundary of the partition (which is sometimes undesirable). Specify `style="hexagonal"` for hexagons. Large scalings can use a lot of RAM since the number of polygons rendered is O(n^2).

You may specify a [matplotlib colormap](http://matplotlib.org/examples/color/colormaps_reference.html) (an instance or the colormap name) in the cmap argument.

![Ternary Heatmap Examples](/readme_images/heatmap_shannon.png)

Ternary can also make heatmaps from data. In this case you need to supply a dictionary 
mapping `(i, j)` or `(i, j, k)` for `i + j + k = scale` to a float as input for a heatmap. It is not necessary to include `k` in the dictionary keys since it can be determined from `scale`, `i`, and `j`. This reduces the memory requirements when the partition is very fine (significant when `scale` is in the hundreds). 

Make the heatmap as follows:

```python
    ternary.heatmap(data, scale, ax=None, cmap=None)
```

or on a `TernaryAxesSubplot` object

```python
    tax.heatmap(data, cmap=None)
```

This can produces images such as:


![Ternary Heatmap Examples](/readme_images/heatmap-dual_vs_triangular.png)

![Ternary Heatmap Examples](/readme_images/heatmap_rsp.png)

There is a large set of heatmap examples [here](http://people.mbi.ucla.edu/marcharper/stationary_stable/3x3/incentive.html).


# RGBA colors

You can alternatively specify colors as rgba
tuples `(r,g,b,a)` (all between zero and one). To use this feature, pass
`colormap=False` to `heatmap()` so that the library will not attempt to map the
tuple to a value with a matplotlib colormap. Note that this disables the
inclusion of a colorbar. Here is an example:

```python
    import math
    from matplotlib import pyplot
    import ternary

    def color_point(x, y, z, scale):
        w = 255
        x_color = x * w / float(scale)
        y_color = y * w / float(scale)
        z_color = z * w / float(scale)
        r = math.fabs(w - y_color) / w
        g = math.fabs(w - x_color) / w
        b = math.fabs(w - z_color) / w
        return (r, g, b, 1.)

    def generate_heatmap_data(scale=5):
        from ternary.helpers import simplex_iterator
        d = dict()
        for (i, j, k) in simplex_iterator(scale):
            d[(i, j, k)] = color_point(i, j, k, scale)
        return d

    if __name__ == "__main__":
        ## Heatmaps from data

        scale = 80
        data = generate_heatmap_data(scale)
        figure, tax = ternary.figure(scale=scale, permutation="210")
        tax.heatmap(data, style="hexagonal", colormap=False) # Allow colors as rgba tuples
        tax.boundary()
        tax.set_title("Hexagonal Heatmap from Data")
        pyplot.show()

```

This produces the following image:

![Ternary Heatmap Examples](/readme_images/rgba_example.png)


# Unittests

You can run the test suite as follows:

```python
python -m unittest discover tests
```

The included script of [examples](https://github.com/marcharper/python-ternary/blob/master/examples.py) is intended to act as a series of extended tests.

# Contributing

Contributions are welcome! Please share any nice example plots, contribute 
features, and add unit tests! Use the pull request and issue systems to contribute.

# Citation

Please cite as follows:

```
Marc Harper, Python-ternary: A python library for ternary plots, 2011-2015, available at: https://github.com/marcharper/python-ternary
```

# Contributors

- Marc Harper [marcharper](https://github.com/marcharper)
- Bryan Weinstein [btweinstein](https://github.com/btweinstein): Hexagonal heatmaps, colored trajectory plots
- [chebee7i](https://github.com/chebee7i): Docs and figures, triangular heatmapping


