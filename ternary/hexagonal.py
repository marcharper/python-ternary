import numpy

## Original Hexagonal heatmap code submitted by https://github.com/btweinstein

SQRT3 = numpy.sqrt(3)

_alpha = numpy.array([0, 1. / SQRT3])
_deltaup = numpy.array([1. / 2., 1. / (2. * SQRT3)])
_deltadown = numpy.array([1. / 2., - 1. / (2. * SQRT3)])
_i_vec = numpy.array([1. / 2., SQRT3 / 2.])
_i_vec_down = numpy.array([1. / 2., -SQRT3 / 2.])
_deltaX_vec = numpy.array([1. / 2, 0])

def i_j_to_x_y(i, j):
    return numpy.array([i / 2. + j, SQRT3 / 2 * i])

def hexagon_coordinates(i, j, k):
    steps = i + j + k
    ij = i_j_to_x_y(i, j)
    
    # Corner cases (literally)
    if i == steps: # j == k == 0
        coords = numpy.array([ij, ij + _i_vec_down / 2., ij - _alpha, ij - _i_vec / 2.])
    elif k == steps: # i == j == 0
        coords = numpy.array([ij, ij + _i_vec / 2., ij + _deltaup, ij + _deltaX_vec])
    elif j == steps: # i == k == 0
        coords = numpy.array([ij, ij - _deltaX_vec, ij - _deltadown, ij - _i_vec_down / 2.])
    # Now the edges
    elif i == 0:
        coords = numpy.array([ij - _deltaX_vec, ij - _deltadown, ij + _alpha, ij + _deltaup, ij + _deltaX_vec])
    elif j == 0:
        coords = numpy.array([ij + _i_vec / 2., ij + _deltaup, ij + _deltadown, ij - _alpha, ij - _i_vec / 2.])
    elif k == 0:
        coords = numpy.array([ij + _i_vec_down / 2., ij - _alpha, ij - _deltaup, ij - _deltadown, ij - _i_vec_down / 2.])
    # Must be an interior point
    else:
        coords = numpy.array([ij + _alpha, ij + _deltaup, ij + _deltadown, ij - _alpha, ij - _deltaup, ij - _deltadown])

    return coords