import ternary

## Simple example with one corner truncated
## Boundary and Gridlines
scale = 10
figure, tax = ternary.figure(scale=scale)
tax.set_truncation({'rl' : 8})
tax.ax.axis("off")


# Draw Boundary and Gridlines
tax.boundary(linewidth=0.25)
tax.gridlines(color="black", multiple=1, linewidth=0.25, ls='-')

# Set Axis labels and Title

tax.left_axis_label(r"$\longleftarrow$ Hogs", fontsize=10)
tax.right_axis_label(r"$\longleftarrow$ Dogs", fontsize=10)
tax.bottom_axis_label(r"Logs $\longrightarrow$", fontsize=10, offset=0.08)


# Set custom ticks
tax.get_ticks_from_truncation(multiple=2)
#tax.get_ticks_from_truncation()
offset=0.013
tax.set_custom_ticks(fontsize=8, offset=offset, multiple=2,
                      tick_formats="%.1f", linewidth=0.25)


tax.ax.axis("scaled")
tax._redraw_labels()






## Boundary and Gridlines
scale = 14
figure, tax = ternary.figure(scale=scale)
figure.set_facecolor('w')
w_i,h_i = 3.15, 2.36
figure.set_size_inches((w_i,h_i))
figure.set_dpi(150)

tax.set_axis_limits({'b':[52,59],'r':[0,7],'l':[41,48]})

tax.set_truncation({'br' : 57.5, 'rl' : 4, 'lb' : 46.5})


tax.ax.axis("off")
left = 0
right = 1
bottom = 0
top = 1
figure.subplots_adjust(left=left,right=right,bottom=bottom,top=top)

# Draw Boundary and Gridlines
tax.boundary(linewidth=0.25)
tax.gridlines(color="black", multiple=1, linewidth=0.25, ls='-')

# Set Axis labels and Title
fontsize = 10
qs = [(55.9, -0.62, 44.5),(56.1, 3.30, 40.5),(51.5, 3.35, 45.0)]

pos = ternary.helpers.convert_coordinates_sequence(qs,tax._boundary_scale,
                                                    tax._axis_limits,
                                                    axisorder='brl')
tax.left_axis_label(r"$\longleftarrow$ Hogs",
                    position=pos[2],fontsize=fontsize)
tax.right_axis_label(r"$\longleftarrow$ Dogs",
                      position=pos[1],fontsize=fontsize)
tax.bottom_axis_label(r"Logs $\longrightarrow$",
                      position=pos[0],fontsize=fontsize)


# Set custom ticks
tax.get_ticks_from_truncation(multiple=1)
#tax.get_ticks_from_axis_limits()
# ticks = {'b' : [54,55,56,57],
#           'r' : [2,3,4],
#           'l' : [46,45,44]}
# ticklocs = {'b' : [4,6,8,10],
#             'r' : [4,6,8],
#             'l' : [8,6,4]}
# tax._ticks = ticks
# tax._ticklocs = ticklocs

offset=0.013
tax.set_custom_ticks(fontsize=8, offset=offset,
                      tick_formats="%.1f", linewidth=0.25)


tax.add_extra_tick('r',(11,2,1),offset,scale,'1',fontsize=8,color='k',
                      linewidth=0.25)
tax.add_extra_tick('r',(11,0,3),offset,scale,'0',fontsize=8,color='k',
                      linewidth=0.25)

tax.add_extra_tick('l',(2,8,4),offset,scale,'43',fontsize=8,color='k',
                      linewidth=0.25)
tax.add_extra_tick('l',(4,8,2),offset,scale,'42',fontsize=8,color='k',
                      linewidth=0.25)
tax.add_extra_tick('l',(6,8,0),offset,scale,'41',fontsize=8,color='k',
                      linewidth=0.25)

tax.add_extra_tick('b',(2,1,11),offset,scale,'53',fontsize=8,color='k',
                      linewidth=0.25)


tax.ax.axis("scaled")
tax.ax.axis([1.1, 12.8, -0.7, 7.4])
tax.ax.set_position([0,0.02,1,1])
tax._redraw_labels()

ternary.plt.show()
