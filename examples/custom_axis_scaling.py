import ternary

# Simple example:
## Boundary and Gridlines
scale = 9
figure, tax = ternary.figure(scale=scale)

tax.ax.axis("off")
figure.set_facecolor('w')

# Draw Boundary and Gridlines
tax.boundary(linewidth=1.0)
tax.gridlines(color="black", multiple=1, linewidth=0.5, ls='-')

# Set Axis labels and Title
fontsize = 16
tax.left_axis_label("Logs", fontsize=fontsize, offset=0.13)
tax.right_axis_label("Dogs", fontsize=fontsize, offset=0.12)
tax.bottom_axis_label("Hogs", fontsize=fontsize, offset=0.06)


# Set custom axis limits by passing a dict into set_limits.
# The keys are b, l and r for the three axes and the vals are a list
# of the min and max in data coords for that axis. max-min for each
# axis must be the same as the scale i.e. 9 in this case.
tax.set_axis_limits({'b': [67, 76], 'l': [24, 33], 'r': [0, 9]})
# get and set the custom ticks:
tax.get_ticks_from_axis_limits()
tax.set_custom_ticks(fontsize=10, offset=0.02)

# data can be plotted by entering data coords (rather than simplex coords):
points = [(70, 3, 27), (73, 2, 25), (68, 6, 26)]
points_c = tax.convert_coordinates(points,axisorder='brl')
tax.scatter(points_c, marker='o', s=25, c='r')

tax.ax.set_aspect('equal', adjustable='box')
tax._redraw_labels()


## Simple example with axis tick formatting:
## Boundary and Gridlines
scale = 9
figure, tax = ternary.figure(scale=scale)

tax.ax.axis("off")
figure.set_facecolor('w')

# Draw Boundary and Gridlines
tax.boundary(linewidth=1.0)
tax.gridlines(color="black", multiple=1, linewidth=0.5, ls='-')

# Set Axis labels and Title
fontsize = 16
tax.left_axis_label("Logs", fontsize=fontsize, offset=0.13)
tax.right_axis_label("Dogs", fontsize=fontsize, offset=0.12)
tax.bottom_axis_label("Hogs", fontsize=fontsize, offset=0.06)


# Set custom axis limits by passing a dict into set_limits.
# The keys are b, l and r for the three axes and the vals are a list
# of the min and max in data coords for that axis. max-min for each
# axis must be the same as the scale i.e. 9 in this case.
tax.set_axis_limits({'b': [67, 76], 'l': [24, 33], 'r': [0, 9]})
# get and set the custom ticks:
# custom tick formats:
# tick_formats can either be a dict, like below or a single format string
# e.g. "%.3e" (valid for all 3 axes) or None, in which case, ints are
# plotted for all 3 axes.
tick_formats = {'b': "%.2f", 'r': "%d", 'l': "%.1f"}

tax.get_ticks_from_axis_limits()
tax.set_custom_ticks(fontsize=10, offset=0.02, tick_formats=tick_formats)

# data can be plotted by entering data coords (rather than simplex coords):
points = [(70, 3, 27), (73, 2, 25), (68, 6, 26)]
points_c = tax.convert_coordinates(points,axisorder='brl')
tax.scatter(points_c, marker='o', s=25, c='r')

tax.ax.set_aspect('equal', adjustable='box')
tax._redraw_labels()

## Zoom example:
## Draw a plot with the full range on the left and a second plot which
## shows a zoomed region of the left plot.
fig = ternary.plt.figure(figsize=(11, 6))
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

tax1 = ternary.TernaryAxesSubplot(ax=ax1, scale=100)
tax1.boundary(linewidth=1.0)
tax1.gridlines(color="black", multiple=10, linewidth=0.5, ls='-')
tax1.ax.axis("equal")
tax1.ax.axis("off")

tax2 = ternary.TernaryAxesSubplot(ax=ax2,scale=30)
axes_colors = {'b': 'r', 'r': 'r', 'l': 'r'}
tax2.boundary(linewidth=1.0, axes_colors=axes_colors)
tax2.gridlines(color="r", multiple=5, linewidth=0.5, ls='-')
tax2.ax.axis("equal")
tax2.ax.axis("off")

fontsize = 16
tax1.set_title("Entire range")
tax1.left_axis_label("Logs", fontsize=fontsize, offset=0.12)
tax1.right_axis_label("Dogs", fontsize=fontsize, offset=0.12)
tax1.bottom_axis_label("Hogs", fontsize=fontsize, offset=0.)
tax2.set_title("Zoomed region",color='r')
tax2.left_axis_label("Logs", fontsize=fontsize, offset=0.17, color='r')
tax2.right_axis_label("Dogs", fontsize=fontsize, offset=0.17, color='r')
tax2.bottom_axis_label("Hogs", fontsize=fontsize, offset=0.03, color='r')

tax1.ticks(multiple=10,offset=0.02)

tax2.set_axis_limits({'b': [60, 75], 'l': [15, 30], 'r': [10, 25]})
tax2.get_ticks_from_axis_limits(multiple=5)
tick_formats = "%.1f"
tax2.set_custom_ticks(fontsize=10, offset=0.025, multiple=5,
                      axes_colors=axes_colors, tick_formats=tick_formats)

# plot some data
points = [(62, 12, 26), (63.5, 13.5, 23), (65, 14, 21), (61, 15, 24),
          (62, 16, 22), (67.5, 14.5, 18), (68.2, 16.5, 15.3), (62, 22.5, 15.5)]

# data coords == simplex coords:
tax1.scatter(points, marker='^', s=25, c='b')
# data coords != simplex coords:
points_c = tax2.convert_coordinates(points, axisorder='brl')
tax2.scatter(points_c, marker='^', s=25, c='b')

# draw the zoom region on the first plot
tax1.line((60, 10, 30), (75, 10, 15), color='r', lw=2.0)
tax1.line((60, 10, 30), (60, 25, 15), color='r', lw=2.0)
tax1.line((75, 10, 15), (60, 25, 15), color='r', lw=2.0)

fig.set_facecolor("w")

tax1.ax.set_position([0.01, 0.05, 0.46, 0.8])
tax2.ax.set_position([0.50, 0.05, 0.46, 0.8])

tax1.resize_drawing_canvas()
tax2.resize_drawing_canvas()
ternary.plt.show()
