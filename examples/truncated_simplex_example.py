"""
This script gives two examples of truncation i.e. cutting one
or more corners off the simplex to save whitespace in a figure.

The first example is simple: only the top corner is truncated and the data
coordainates are the same as the simplex coordinates.

The second example is more complex: all three corners have been truncated
and we set axis data limits which are not the same as the simplex coords.
"""

import ternary

## Simple example with the top corner truncated
scale = 10
figure, tax = ternary.figure(scale=scale)
figure.subplots_adjust(left=-0.1, right=1.1, bottom=0.1, top=1.1)
tax.set_truncation({'rl' : 8})
tax.ax.axis("off")


# Draw Boundary and Gridlines
tax.boundary(linewidth=0.25)
tax.gridlines(color="black", multiple=1, linewidth=0.25, ls='-')


# Set Axis labels
tax.left_axis_label(r"$\longleftarrow$ Hogs", fontsize=10)
tax.right_axis_label(r"$\longleftarrow$ Dogs", fontsize=10)
tax.bottom_axis_label(r"Logs $\longrightarrow$", fontsize=10, offset=0.08)


# As we have set a truncation, we need to get and set custom ticks
tax.get_ticks_from_axis_limits(multiple=2)
offset=0.013
tax.set_custom_ticks(fontsize=8, offset=offset,
                     tick_formats="%.1f", linewidth=0.25)
# here we have used a tick formatting string to label all the axes with
# floats to one decimal place.

tax.ax.axis("scaled")
tax._redraw_labels()
figure.canvas.draw()







## More complex example with truncations on all 3 corners of the simplex
## and axes with data coordinates which are different to simplex coordinates.
scale = 14
figure, tax = ternary.figure(scale=scale)
w_i,h_i = 3.15, 2.36
figure.set_size_inches((w_i,h_i))
figure.set_dpi(150)
tax.ax.axis("off")
figure.subplots_adjust(left=0, right=1, bottom=0, top=1)

# here we set the data limits of the axes (of the complete simplex)
tax.set_axis_limits({'b' : [52, 59], 'r' : [0, 7], 'l' : [41, 48]})

# now we set the truncation of all 3 corners in data coords. The truncation
# point refers to the first axis in the key e.g. "b" will be cut off at 57.5
# parallel to the left axis until we reach the "r" axis for "br" : 57.5
tax.set_truncation({'br' : 57.5, 'rl' : 4, 'lb' : 46.5})

# Draw Boundary and Gridlines
tax.boundary(linewidth=0.25)
tax.gridlines(color="black", multiple=1, linewidth=0.25, ls='-')

# As the truncated figure is no longer a triangle, we need to set custom
# positions for the axis labels. One way is to enter positions as 2-tuples
# in xy data coords (e.g. obtained interactively by the hovering the mouse
# over the matplotlib figure axes) and convert them to simplex coords
# (3-tuples) for plotting:
qs = {"l" : (1.94, 5.80),
      "b" : (6.67, -1.5),
      "r" : (12.34, 5.58)
      }

pos = {i : ternary.helpers.planar_to_coordinates(j, tax._scale).tolist()
        for i, j in qs.items()
        }

fontsize = 10
tax.left_axis_label(r"$\longleftarrow$ Hogs", position=pos["l"],
                    fontsize=fontsize)
tax.right_axis_label(r"$\longleftarrow$ Dogs", position=pos["r"],
                      fontsize=fontsize)
tax.bottom_axis_label(r"Logs $\longrightarrow$", position=pos["b"],
                      fontsize=fontsize)


# We also need to set custom ticks for this example.
# We could use tax.get_ticks_from_axis_limits(multiple=1) and this gives
# us all the ticks on the remaining visible parts of the simplex boundary.
# Instead we show here how to plot specific ticks.
# define ticks in data coords along each axis:
tax._ticks = {'b' : [54,55,56,57],
              'r' : [2,3,4],
              'l' : [44,45,46]}
# define tick locations along each axis in simplex coords:
tax._ticklocs = {'b' : [4,6,8,10],
                  'r' : [4,6,8],
                  'l' : [4,6,8]}

offset=0.013
tax.set_custom_ticks(fontsize=8, offset=offset, tick_formats="%i",
                      linewidth=0.25)

# As we have applied a truncation, it can be helpful to plot extra
# ticks which are not located on the simplex boundary. We specify
# which axis the tick belongs to so that the tick can be drawn with
# the correct orientation: horizontal, right parallel or left parallel.
# Then give the position of the tick in simplex coordinates and specify
# the tick label as a string in data coordinates:
tax.add_extra_tick('r', (11,2,1), offset, '1', fontsize=8, color='k',
                    linewidth=0.25)
tax.add_extra_tick('r', (11,0,3), offset, '0', fontsize=8, color='k',
                    linewidth=0.25)

tax.add_extra_tick('l', (2,8,4), offset, '43', fontsize=8, color='k',
                    linewidth=0.25)
tax.add_extra_tick('l', (4,8,2), offset, '42', fontsize=8, color='k',
                    linewidth=0.25)
tax.add_extra_tick('l', (6,8,0), offset, '41', fontsize=8, color='k',
                    linewidth=0.25)

tax.add_extra_tick('b', (2,1,11), offset, '53', fontsize=8, color='k',
                    linewidth=0.25)


tax.ax.axis("scaled")
tax.ax.axis([0, 14, -2, 9])
tax._redraw_labels()

ternary.plt.show()
