import math
import numpy

## Original Hexagonal heatmap code submitted by https://github.com/btweinstein

SQRT3 = math.sqrt(3)

def i_j_to_x_y(i, j):
    return numpy.array([i / 2. + j, SQRT3 / 2 * i])

_alpha = numpy.array([0, 1. / SQRT3])
_deltaup = numpy.array([1. / 2., 1. / (2. * SQRT3)])
_deltadown = numpy.array([1. / 2., - 1. / (2. * SQRT3)])

_i_vec = numpy.array([1. / 2., SQRT3 / 2.])
_i_vec_down = numpy.array([1. / 2., -SQRT3 / 2.])

_deltaX_vec = numpy.array([_deltadown[0], 0])

def hexagon_coordinates(i, j, k):
    ij = i_j_to_x_y(i, j)
    steps = i + j + k
    coords = numpy.array([ij + _alpha, ij + _deltaup, ij + _deltadown, ij - _alpha, ij - _deltaup, ij - _deltadown])
    if i == 0:
        # Along the base of the triangle
        if (j != steps) and (j != 0):  # Not a bizarre corner entity
            # Bound at y = zero
            coords = numpy.array([ij - _deltaX_vec, ij - _deltadown, ij + _alpha, ij + _deltaup, ij + _deltaX_vec])

    if j == 0:
        # Along the left of the triangle
        if (i != steps) and (i != 0):  # Not a corner
            coords = numpy.array([ij + _i_vec / 2., ij + _deltaup, ij + _deltadown, ij - _alpha, ij - _i_vec / 2.])

    if i + j == steps:
        # Along the right of the triangle
        if (i != 0 ) and (j != 0):
            coords = numpy.array(
                [ij + _i_vec_down / 2., ij - _alpha, ij - _deltaup, ij - _deltadown, ij - _i_vec_down / 2.])

    # Deal with pathological border cases
    if i == steps and j == 0:
        coords = numpy.array([ij, ij + _i_vec_down / 2., ij - _alpha, ij - _i_vec / 2.])
    if i == 0 and j == 0:
        coords = numpy.array([ij, ij + _i_vec / 2., ij + _deltaup, ij + _deltaX_vec])
    if j == steps and i == 0:
        coords = numpy.array([ij, ij - _deltaX_vec, ij - _deltadown, ij - _i_vec_down / 2.])

    return coords