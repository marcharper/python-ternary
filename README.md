
# python-ternary

<a href="https://pypi.python.org/pypi/python-ternary"><img src="https://img.shields.io/pypi/v/python-ternary.svg"/></a>
[![DOI](https://zenodo.org/badge/19505/marcharper/python-ternary.svg)](https://zenodo.org/badge/latestdoi/19505/marcharper/python-ternary)
[![Join the chat at https://gitter.im/marcharper/python-ternary](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/marcharper/python-ternary?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

This is a plotting library for use with [matplotlib](http://matplotlib.org/index.html) to make [ternary plots](http://en.wikipedia.org/wiki/Ternary_plot)
plots in the two dimensional simplex projected onto a two dimensional plane.

The library provides functions for plotting projected lines, curves (trajectories), scatter plots, and heatmaps. There are [several examples](examples/) and a short tutorial below.

# Gallery

<div style="text-align:center">

<img src="/readme_images/16_80_1.png" width="150" height="150"/>
<img src="/readme_images/16_80_stationary.png" width="150" height="150"/>
<img src="/readme_images/23_80_0.png" width="150" height="150"/>
<img src="/readme_images/24_80_1.png" width="150" height="150"/>
<img src="/readme_images/heatmap_rsp.png" width="150" height="150"/>
<img src="/readme_images/colored_boundary.png" width="150" height="150"/>
<img src="/readme_images/rgba_example.png" width="150" height="150"/>
<img src="/readme_images/various_lines.png" width="150" height="150"/>
<img src="/readme_images/colored_trajectory.png" width="150" height="150"/>
<img src="/readme_images/scatter.png" width="150" height="150"/><br/>
<br/>
<img src="/readme_images/btweinstein_example2.png" width="300" height="150"/>
<img src="/readme_images/btweinstein_example.png" width="300" height="150"/>
<br/>
Last image from: <a href="http://biorxiv.org/content/early/2017/06/07/145631">Genetic Drift and Selection in Many-Allele Range Expansions</a>.<br/>
<br/>
See the citations below for more example images.
</div>

# Citations and Recent Usage in Publications

[![DOI](https://zenodo.org/badge/19505/marcharper/python-ternary.svg)](https://zenodo.org/badge/latestdoi/19505/marcharper/python-ternary)

Have you used python-ternary in a publication? Open a PR or issue to include
your citations or example plots!

See the [partial list of citations](citations.md) and
[instructions on how to cite](CITATION.md).

# Installation

### Anaconda

You can install python-ternary with conda:

```bash
conda config --add channels conda-forge
conda install python-ternary
```

See [here](https://github.com/conda-forge/python-ternary-feedstock) for more
information.

### Pip

You can install the current release (1.0.6) with pip:
```bash
    pip install python-ternary
```

### With setup.py

Alternatively you can clone the repository and run `setup.py` in the usual
manner:

```bash
    git clone git@github.com:marcharper/python-ternary.git
    cd python-ternary
    python setup.py install
```

# Usage, Examples, Plotting Functions

You can explore some of these examples with
[this Jupyter notebook](examples/Ternary-Examples.ipynb).

The easiest way to use python-ternary is with the wrapper class
`TernaryAxesSubplot`, which mimics Matplotlib's AxesSubplot. Start with:

```python
    fig, tax = ternary.figure()
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

If you need to act directly on the underlying matplotlib axes, you can access
them easily:

```python
    ax = tax.get_axes()
```

You can also wrap an existing Matplotlib AxesSubplot object:

```
    figure, ax = pyplot.subplots()
    tax = ternary.TernaryAxesSubplot(ax=ax)
```

This is useful if you want to use ternary as a part of another figure, such as

```python
    from matplotlib import pyplot, gridspec

    pyplot.figure()
    gs = gridspec.GridSpec(2, 2)
    ax = pyplot.subplot(gs[0, 0])
    figure, tax = ternary.figure(ax=ax)
    ...
```

Some ternary functions expect the simplex to be partitioned into some number
of steps, determined by the `scale` parameter. A few functions will do this
partitioning automatically for you, but when working with real data or
simulation output, you may have partitioned already. If you are working with
probability distributions, just use `scale=1` (the default). Otherwise the scale
parameter effectively controls the resolution of many plot types
(e.g. heatmaps).

`TernaryAxesSubplot` objects keep track of the scale, axes, and other
parameters, supplying them as needed to other functions.

## Simplex Boundary and Gridlines

The following code draws a boundary for the simplex and gridlines.

```python
    import ternary

    ## Boundary and Gridlines
    scale = 40
    figure, tax = ternary.figure(scale=scale)

    # Draw Boundary and Gridlines
    tax.boundary(linewidth=2.0)
    tax.gridlines(color="black", multiple=5)
    tax.gridlines(color="blue", multiple=1, linewidth=0.5)

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

    ternary.plt.show()
```
<p align="center">
<img src="/readme_images/boundary_and_gridlines.png" width="600" height="450"/>
</p>

## Drawing lines

You can draw individual lines between any two points with `line` and lines
parallel to the axes with `horizonal_line`, `left_parallel_line`, and
`right_parallel_line`:

```python
    import ternary
    
    scale = 40
    figure, tax = ternary.figure(scale=scale)
    
    # Draw Boundary and Gridlines
    tax.boundary(linewidth=2.0)
    tax.gridlines(color="blue", multiple=5)
    
    # Set Axis labels and Title
    fontsize = 12
    offset = 0.14
    tax.set_title("Various Lines\n", fontsize=fontsize)
    tax.right_corner_label("X", fontsize=fontsize)
    tax.top_corner_label("Y", fontsize=fontsize)
    tax.left_corner_label("Z", fontsize=fontsize)
    tax.left_axis_label("Left label $\\alpha^2$", fontsize=fontsize, offset=offset)
    tax.right_axis_label("Right label $\\beta^2$", fontsize=fontsize, offset=offset)
    tax.bottom_axis_label("Bottom label $\\Gamma - \\Omega$", fontsize=fontsize, offset=offset)
    
    # Draw lines parallel to the axes
    tax.horizontal_line(16)
    tax.left_parallel_line(10, linewidth=2., color='red', linestyle="--")
    tax.right_parallel_line(20, linewidth=3., color='blue')

    # Draw an arbitrary line, ternary will project the points for you
    p1 = (22, 8, 10)
    p2 = (2, 22, 16)
    tax.line(p1, p2, linewidth=3., marker='s', color='green', linestyle=":")
    
    tax.ticks(axis='lbr', multiple=5, linewidth=1, offset=0.025)
    tax.get_axes().axis('off')
    tax.clear_matplotlib_ticks()
    tax.show()
```

The line drawing functions accept the matplotlib keyword arguments of
[Line2D](http://matplotlib.org/api/lines_api.html).

<p align="center">
<img src="/readme_images/various_lines.png" width="500" height="500"/>
</p>

## Curves

Curves can be plotted by specifying the points of the curve, just like
matplotlib's plot. Simply use:

```
    ternary.plot(points)
```

Points is a list of tuples or numpy arrays, such as
`[(0.5, 0.25, 0.25), (1./3, 1./3, 1./3)]`,

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
            points.append(list(map(float, line.split(' '))))
    # Plot the data
    tax.plot(points, linewidth=2.0, label="Curve")
    tax.ticks(axis='lbr', multiple=0.2, linewidth=1, tick_formats="%.1f")
    tax.legend()
    tax.show()
```

<p align="center">
<img src="/readme_images/trajectory.png" width="500" height="375"/>
</p>

There are many more examples in [this paper](http://arxiv.org/abs/1210.5539).

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
    tax.ticks(axis='lbr', linewidth=1, multiple=5)

    tax.show()
```

<p align="center">
<img src="/readme_images/scatter.png" width="500" height="375"/>
</p>

## Heatmaps

Ternary can plot heatmaps in two ways and three styles. Given a function, ternary
will evaluate the function at the specified number of steps (determined by the
scale, expected to be an integer in this case). The simplex can be split up into
triangles or hexagons and colored according to one of three styles:

- Triangular -- `triangular` (default): coloring triangles by summing the values on the
vertices
- Dual-triangular  -- `dual-triangular`: mapping (i,j,k) to the upright
triangles &#9651; and blending the neigboring triangles for the downward
triangles &#9661;
- Hexagonal  -- `hexagonal`: which does not blend values at all, and divides
the simplex up into hexagonal regions

The two triangular heatmap styles and the hexagonal heatmap style can be visualized
as follows: left is triangular, right is dual triangular.

<p align="center">
<img src="/readme_images/heatmap-grids.png" width="500" height="250"/><br/>
<img src="/readme_images/heatmap_styles_cubehelix.png"/><br/>
</p>


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

In this case the keyword argument *boundary* indicates whether you wish to
evaluate points on the boundary of the partition (which is sometimes
undesirable). Specify `style="hexagonal"` for hexagons. Large scalings can use
a lot of RAM since the number of polygons rendered is O(n^2).

You may specify a [matplotlib colormap](http://matplotlib.org/examples/color/colormaps_reference.html)
(an instance or the colormap name) in the cmap argument.

<p style="text-align:center">
<img src="/readme_images/heatmap_shannon.png"/> <br/>
</p>

Ternary can also make heatmaps from data. In this case you need to supply a
dictionary mapping `(i, j)` or `(i, j, k)` for `i + j + k = scale` to a float
as input for a heatmap. It is not necessary to include `k` in the dictionary
keys since it can be determined from `scale`, `i`, and `j`. This reduces the
memory requirements when the partition is very fine (significant when `scale`
is in the hundreds).

Make the heatmap as follows:

```python
    ternary.heatmap(data, scale, ax=None, cmap=None)
```

or on a `TernaryAxesSubplot` object:

```python
    tax.heatmap(data, cmap=None)
```

This can produces images such as:

<p align="center">
<img src="/readme_images/heatmap-dual_vs_triangular.png" width="1200" height="260"/> <br/>
<img src="/readme_images/heatmap_rsp.png" width="500" height="375"/>
</p>

# Axes Ticks and Orientations

For a given ternary plot there are two valid ways to label the axes ticks
corresponding to the clockwise and counterclockwise orientations. However note
that the axes labels need to be adjusted accordingly, and `ternary` does not
do so automatically when you pass `clockwise=True` to `tax.ticks()`.

<p align="center">
<img src="/readme_images/orientations.png"/>
</p>

There is a [more detailed discussion](https://github.com/marcharper/python-ternary/issues/18)
on issue #18 (closed).


# RGBA colors

You can alternatively specify colors as rgba tuples `(r, g, b, a)`
(all between zero and one). To use this feature, pass `colormap=False` to
`heatmap()` so that the library will not attempt to map the tuple to a value
with a matplotlib colormap. Note that this disables the inclusion of a colorbar.
Here is an example:

```python
import math
from matplotlib import pyplot as plt
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


scale = 80
data = generate_heatmap_data(scale)
figure, tax = ternary.figure(scale=scale)
tax.heatmap(data, style="hexagonal", use_rgba=True)
tax.boundary()
tax.set_title("RGBA Heatmap")
plt.show()

```

This produces the following image:

<p align="center">
<img src="/readme_images/rgba_example.png" width="450" height="450"/>
</p>

# Unittests

You can run the test suite as follows:

```python
python -m unittest discover tests
```

# Contributing

Contributions are welcome! Please share any nice example plots, contribute
features, and add unit tests! Use the pull request and issue systems to
contribute.

# Selected Contributors

- Marc Harper [marcharper](https://github.com/marcharper): maintainer
- Bryan Weinstein [btweinstein](https://github.com/btweinstein): Hexagonal heatmaps, colored trajectory plots
- [chebee7i](https://github.com/chebee7i): Docs and figures, triangular heatmapping
- [Cory Simon](https://github.com/CorySimon): Axis Colors, colored heatmap example

# Known-Issues

At one point there was an issue on macs that causes the axes
labels not to render. The workaround is to manually call
```
tax._redraw_labels()
```
before showing or rendering the image.
