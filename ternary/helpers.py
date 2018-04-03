"""
Helper functions and utilities for projecting to the simplex and various tasks.
"""

import numpy


### Constants ###

SQRT3 = numpy.sqrt(3)
SQRT3OVER2 = SQRT3 / 2.

### Auxilliary Functions ###


def unzip(l):
    """[(a1, b1), ..., (an, bn)] ----> ([a1, ..., an], [b1, ..., bn])"""
    return list(zip(*l))


def normalize(l):
    """
    Normalizes input list.

    Parameters
    ----------
    l: list
        The list to be normalized

    Returns
    -------
    The normalized list or numpy array

    Raises
    ------
    ValueError, if the list sums to zero
    """

    s = float(sum(l))
    if s == 0:
        raise ValueError("Cannot normalize list with sum 0")
    return [x / s for x in l]


def simplex_iterator(scale, boundary=True):
    """
    Systematically iterates through a lattice of points on the 2-simplex.

    Parameters
    ----------
    scale: Int
        The normalized scale of the simplex, i.e. N such that points (x,y,z)
        satisify x + y + z == N

    boundary: bool, True
        Include the boundary points (tuples where at least one
        coordinate is zero)

    Yields
    ------
    3-tuples, There are binom(n+2, 2) points (the triangular
    number for scale + 1, less 3*(scale+1) if boundary=False
    """

    start = 0
    if not boundary:
        start = 1
    for i in range(start, scale + (1 - start)):
        for j in range(start, scale + (1 - start) - i):
            k = scale - i - j
            yield (i, j, k)


## Ternary Projections ##

def permute_point(p, permutation=None):
    """
    Permutes the point according to the permutation keyword argument. The
    default permutation is "012" which does not change the order of the
    coordinate. To rotate counterclockwise, use "120" and to rotate clockwise
    use "201"."""
    if not permutation:
        return p
    return [p[int(permutation[i])] for i in range(len(p))]


def project_point(p, permutation=None):
    """
    Maps (x,y,z) coordinates to planar simplex.

    Parameters
    ----------
    p: 3-tuple
        The point to be projected p = (x, y, z)
    permutation: string, None, equivalent to "012"
        The order of the coordinates, counterclockwise from the origin
    """
    permuted = permute_point(p, permutation=permutation)
    a = permuted[0]
    b = permuted[1]
    x = a + b/2.
    y = SQRT3OVER2 * b
    return numpy.array([x, y])


def project_sequence(s, permutation=None):
    """
    Projects a point or sequence of points using `project_point` to lists xs, ys
    for plotting with Matplotlib.

    Parameters
    ----------
    s, Sequence-like
        The sequence of points (3-tuples) to be projected.

    Returns
    -------
    xs, ys: The sequence of projected points in coordinates as two lists 
    """

    xs, ys = unzip([project_point(p, permutation=permutation) for p in s])
    return xs, ys


# Convert coordinates for custom plots with limits

def convert_coordinates(q, conversion, axisorder):
    """
    Convert a 3-tuple in data coordinates into to simplex data
    coordinates for plotting.

    Parameters
    ----------
    q: 3-tuple
       the point to be plotted in data coordinates

    conversion: dict
        keys = ['b','l','r']
        values = lambda function giving the conversion
    axisorder: String giving the order of the axes for the coordinate tuple
        e.g. 'blr' for bottom, left, right coordinates.

    Returns
    -------
    p: 3-tuple
       The point converted to simplex coordinates.
    """
    p = []
    for k in range(3):
        p.append(conversion[axisorder[k]](q[k]))

    return tuple(p)


def get_conversion(scale, limits):
    """
    Get the conversion equations for each axis.

    limits: dict of min and max values for the axes in the order blr.
    """
    fb = float(scale) / float(limits['b'][1] - limits['b'][0])
    fl = float(scale) / float(limits['l'][1] - limits['l'][0])
    fr = float(scale) / float(limits['r'][1] - limits['r'][0])

    conversion = {"b": lambda x: (x - limits['b'][0]) * fb,
                  "l": lambda x: (x - limits['l'][0]) * fl,
                  "r": lambda x: (x - limits['r'][0]) * fr}

    return conversion
    

def convert_coordinates_sequence(qs, scale, limits, axisorder):
    """
    Take a sequence of 3-tuples in data coordinates and convert them
    to simplex coordinates for plotting. This is needed for custom
    plots where the scale of the simplex axes is set within limits rather
    than being defined by the scale parameter.

    Parameters
    ----------
    qs, sequence of 3-tuples
       The points to be plotted in data coordinates.

    scale: int
        The scale parameter for the plot.
    limits: dict
        keys = ['b','l','r']
        values = min,max data values for this axis.
    axisorder: String giving the order of the axes for the coordinate tuple
        e.g. 'blr' for bottom, left, right coordinates.

    Returns
    -------
    s, list of 3-tuples
       the points converted to simplex coordinates
    """
    conversion = get_conversion(scale, limits)
    
    return [convert_coordinates(q, conversion, axisorder) for q in qs]
