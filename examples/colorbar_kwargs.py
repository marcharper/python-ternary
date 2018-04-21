import ternary

## Boundary and Gridlines
scale = 9
figure, tax = ternary.figure(scale=scale)
tax.ax.axis("off")
figure.set_facecolor('w')

# Draw Boundary and Gridlines
tax.boundary(linewidth=1.0)
tax.gridlines(color="black", multiple=1, linewidth=0.5,ls='-')

# Set Axis labels and Title
fontsize = 15
tax.left_axis_label("Barleygrow", fontsize=fontsize, offset=0.12)
tax.right_axis_label("Beans", fontsize=fontsize, offset=0.12)
tax.bottom_axis_label("Oats", fontsize=fontsize, offset=0.025)

# Set ticks
tax.ticks(axis='blr', linewidth=1,multiple=1)



# Scatter some points
points = [(2,3,5),(3,6,1),(5,4,1),(3,4,3),(2,2,6)]
c = [90,20,30,10,64]

cb_kwargs = {"shrink" : 0.6,
             "orientation" : "horizontal",
             "fraction" : 0.1,
             "pad" : 0.05,
             "aspect" : 30}

tax.scatter(points,marker='s',c=c,edgecolor='k',s=40,linewidths=0.5,
            vmin=0,vmax=100,colorbar=True,colormap='jet',cbarlabel='Farmers',
            cb_kwargs=cb_kwargs,zorder=3)


tax._redraw_labels()

# Color coded heatmap example with colorbar kwargs
# Slight modification so that we don't have to re-import pyplot
# but make use of ternary.plt


# Function to visualize for heat map
def f(x):
    return 1.0 * x[0] / (1.0 * x[0] + 0.2 * x[1] + 0.05 * x[2])

# dictionary of axes colors for bottom (b), left (l), right (r)
axes_colors = {'b': 'g', 'l': 'r', 'r':'b'}

scale = 10

figure, tax = ternary.figure(scale=scale)
tax.ax.axis("off")
cb_kwargs = {"shrink" : 0.6,
             "pad" : 0.05,
             "aspect" : 30,
             "orientation" : "horizontal"}

tax.heatmapf(f, boundary=False, 
            style="hexagonal", cmap=ternary.plt.cm.get_cmap('Blues'),
            cbarlabel='Component 0 uptake',
            vmax=1.0, vmin=0.0, cb_kwargs=cb_kwargs)

tax.boundary(linewidth=2.0, axes_colors=axes_colors)

tax.left_axis_label("$x_1$", offset=0.16, color=axes_colors['l'])
tax.right_axis_label("$x_0$", offset=0.16, color=axes_colors['r'])
tax.bottom_axis_label("$x_2$", offset=-0.06, color=axes_colors['b'])

tax.gridlines(multiple=1, linewidth=2,
              horizontal_kwargs={'color':axes_colors['b']},
              left_kwargs={'color':axes_colors['l']},
              right_kwargs={'color':axes_colors['r']},
              alpha=0.7)

ticks = [round(i / float(scale), 1) for i in range(scale+1)]
tax.ticks(ticks=ticks, axis='rlb', linewidth=1, clockwise=True,
          axes_colors=axes_colors, offset=0.03)

tax.clear_matplotlib_ticks()
tax._redraw_labels()
ternary.plt.tight_layout()
ternary.plt.show()
