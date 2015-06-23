from __future__ import division

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import ternary

SQRT3OVER2 = np.sqrt(3) / 2

def project(p):
    # project using the same transformation that was used for the triangles
    a, b, c = p
    x = a/2 + b
    y = SQRT3OVER2 * a
    return (x, y)

def matplotlib_plot(scale, cmap, filename=None):

    points = list(ternary.helpers.simplex_iterator(scale))
    xs, ys = zip(*map(project, points))
    values = range(len(points))

    f, axes = plt.subplots(1,3, figsize=(8.5, 4.5))

    styles = ['triangular', 'dual-triangular', 'hexagonal']
    ticks_list = [range(scale + 1), range(scale + 2), range(scale + 1)]
    shift = True
    for ax, style, ticks in zip(axes, styles, ticks_list):
        ax.set_aspect('equal')
        ax.set_title(style)
        ternary.heatmap(dict(zip(points, values)),
                        scale=scale, ax=ax,
                        cmap=cmap, vmax=len(points) + 1,
                        style=style, colorbar=False)
        if style == 'dual-triangular' and shift:
            xvals = np.array(xs) + .5
            yvals = np.array(ys) + 1/3
        else:
            xvals = xs
            yvals = ys

        ax.scatter(xvals, yvals, s=150, c='c', zorder=3)
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        for x, y, value in zip(xvals, yvals, values):
            ax.text(x, y, str(value),
                    fontsize=8,
                    horizontalalignment='center',
                    verticalalignment='center')

    # Colorbar
    f.tight_layout()
    cbax = f.add_axes([0.025, 0.1, 0.95, 0.10])
    norm = mpl.colors.Normalize(vmin=0, vmax=len(points))
    ticks = np.linspace(0, len(points), num=len(points) + 1)
    cb1 = mpl.colorbar.ColorbarBase(cbax, cmap=cmap,
                                    norm=norm,
                                    orientation='horizontal')
    cb1.set_ticks(ticks)

    if filename is not None:
        plt.savefig(filename)

    return ax

if __name__ == '__main__':
    import subprocess

    scale = 3
    cmaps = [plt.cm.gray, plt.cm.cubehelix]

    basename = 'heatmap_styles_{}.pdf'
    filenames = [basename.format(cmap.name) for cmap in cmaps]

    cmd = 'convert -density 300 -trim {} -quality 100 {}'
    for cmap, pdf in zip(cmaps, filenames):
        png = pdf[:-3] + 'png'
        matplotlib_plot(scale, cmap, filename=pdf)
        subprocess.call(cmd.format(pdf, png), shell=True)

