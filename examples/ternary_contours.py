""" Compute ternary contours using matplotlib.pyplot.contour function """
import numpy as np
import matplotlib.pyplot as plt
import ternary
import math
import itertools


def shannon_entropy(p):
    """Computes the Shannon Entropy at a distribution in the simplex."""
    s = 0.
    for i in range(len(p)):
        try:
            s += p[i] * math.log(p[i])
        except ValueError:
            continue
    return -1. * s

scale = 20
level = [0.25, 0.5, 0.8, 0.9]       # values for contours

# === prepare coordinate list for contours
x_range = np.arange(0, 1.01, 0.01)   # ensure that grid spacing is small enough to get smooth contours
coordinate_list = np.asarray(list(itertools.product(x_range, repeat=2)))
coordinate_list = np.append(coordinate_list, (1 - coordinate_list[:, 0] - coordinate_list[:, 1]).reshape(-1, 1), axis=1)

# === calculate data with coordinate list
data_list = []
for point in coordinate_list:
    data_list.append(shannon_entropy(point))
data_list = np.asarray(data_list)
data_list[np.sum(coordinate_list[:, 0:2], axis=1) > 1] = np.nan  # remove data outside triangle

# === reshape coordinates and data for use with pyplot contour function
x = coordinate_list[:, 0].reshape(x_range.shape[0], -1)
y = coordinate_list[:, 1].reshape(x_range.shape[0], -1)

h = data_list.reshape(x_range.shape[0], -1)

# === use pyplot to calculate contours
contours = plt.contour(x, y, h, level)  # this needs to be BEFORE figure definition
plt.clf()  # makes sure that contours are not plotted in carthesian plot

fig, tax = ternary.figure(scale=scale)

# === plot contour lines
for ii, contour in enumerate(contours.allsegs):
    for jj, seg in enumerate(contour):
        tax.plot(seg[:, 0:2] * scale, color='r')

# === plot regular data
tax.heatmapf(shannon_entropy, boundary=True, style='hexagonal', colorbar=True)

plt.show()
