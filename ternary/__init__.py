from matplotlib import pyplot as plt

from .plotting import (
    clear_matplotlib_ticks,
    plot,
    resize_drawing_canvas,
    scatter,
)

from .lines import (
    boundary,
    gridlines,
    line,
    horizontal_line,
    left_parallel_line,
    right_parallel_line,
)

from .helpers import project_point

from .colormapping import get_cmap
from .heatmapping import heatmap, heatmapf, svg_heatmap

from .ternary_axes_subplot import figure, TernaryAxesSubplot