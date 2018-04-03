import matplotlib
from matplotlib import pyplot as plt
from matplotlib.colors import rgb2hex

## Default colormap, other options here: http://www.scipy.org/Cookbook/Matplotlib/Show_colormaps
s = matplotlib.__version__.split('.')
if int(s[0]) >= 2 or (int(s[0]) >= 1 and int(s[1]) >= 5):
    DEFAULT_COLOR_MAP_NAME = "viridis"
else:
    DEFAULT_COLOR_MAP_NAME = "jet"


## Matplotlib Colormapping ##

def get_cmap(cmap=None):
    """
    Loads a matplotlib colormap if specified or supplies the default.

    Parameters
    ----------
    cmap: string or matplotlib.colors.Colormap instance
        The name of the Matplotlib colormap to look up.

    Returns
    -------
    The desired Matplotlib colormap

    Raises
    ------
    ValueError if colormap name is not recognized by Matplotlib
    """

    if isinstance(cmap, matplotlib.colors.Colormap):
        return cmap
    if isinstance(cmap, str):
        cmap_name = cmap
    else:
        cmap_name = DEFAULT_COLOR_MAP_NAME
    return plt.get_cmap(cmap_name)


def colormapper(value, lower=0, upper=1, cmap=None):
    """
    Maps values to colors by normalizing within [a,b], obtaining rgba from the
    given matplotlib color map for heatmap polygon coloring.

    Parameters
    ----------
    value: float
        The value to be colormapped
    lower: float
        Lower bound of colors
    upper: float
        Upper bound of colors
    cmap: String or matplotlib.colors.Colormap (optional)
        Colormap object to prevent repeated lookup

    Returns
    -------
    hex_, float
        The value mapped to an appropriate RGBA color value
    """

    cmap = get_cmap(cmap)
    if upper - lower == 0:
        rgba = cmap(0)
    else:
        rgba = cmap((value - lower) / float(upper - lower))
    hex_ = rgb2hex(rgba)
    return hex_


def colorbar_hack(ax, vmin, vmax, cmap, scientific=False, cbarlabel=None,
                  **kwargs):
    """
    Colorbar hack to insert colorbar on ternary plot. 
    
    Called by heatmap, not intended for direct usage.
    
    Parameters
    ----------
    vmin: float
        Minimum value to portray in colorbar
    vmax: float
        Maximum value to portray in colorbar
    cmap: Matplotlib colormap
        Matplotlib colormap to use

    """
    # http://stackoverflow.com/questions/8342549/matplotlib-add-colorbar-to-a-sequence-of-line-plots
    norm = plt.Normalize(vmin=vmin, vmax=vmax)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm._A = []
    cb = plt.colorbar(sm, ax=ax, **kwargs)
    if cbarlabel is not None:
        cb.set_label(cbarlabel)
    if scientific:
        cb.locator = matplotlib.ticker.LinearLocator(numticks=7)
        cb.formatter = matplotlib.ticker.ScalarFormatter()
        cb.formatter.set_powerlimits((0, 0))
        cb.update_ticks()
