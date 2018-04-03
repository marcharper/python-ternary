import ternary
import matplotlib.pyplot as plt


# Function to visualize for heat map
def f(x):
    return 1.0 * x[0] / (1.0 * x[0] + 0.2 * x[1] + 0.05 * x[2])

# Dictionary of axes colors for bottom (b), left (l), right (r).
axes_colors = {'b': 'g', 'l': 'r', 'r': 'b'}

scale = 10

fig, ax = plt.subplots()
ax.axis("off")
figure, tax = ternary.figure(ax=ax, scale=scale)

tax.heatmapf(f, boundary=False,
             style="hexagonal", cmap=plt.cm.get_cmap('Blues'),
             cbarlabel='Component 0 uptake',
             vmax=1.0, vmin=0.0)

tax.boundary(linewidth=2.0, axes_colors=axes_colors)

tax.left_axis_label("$x_1$", offset=0.16, color=axes_colors['l'])
tax.right_axis_label("$x_0$", offset=0.16, color=axes_colors['r'])
tax.bottom_axis_label("$x_2$", offset=0.06, color=axes_colors['b'])

tax.gridlines(multiple=1, linewidth=2,
              horizontal_kwargs={'color': axes_colors['b']},
              left_kwargs={'color': axes_colors['l']},
              right_kwargs={'color': axes_colors['r']},
              alpha=0.7)

# Set and format axes ticks.
ticks = [i / float(scale) for i in range(scale+1)]
tax.ticks(ticks=ticks, axis='rlb', linewidth=1, clockwise=True,
          axes_colors=axes_colors, offset=0.03, tick_formats="%0.1f")

tax.clear_matplotlib_ticks()
tax._redraw_labels()
plt.tight_layout()
tax.show()
