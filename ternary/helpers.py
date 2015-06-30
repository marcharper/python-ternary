"""
Helper functions and utilities for projecting to the simplex and various tasks.
"""

import numpy


### Constants ###

SQRT3 = numpy.sqrt(3)
SQRT3OVER2 = SQRT3 / 2.
PERMUTATIONS = set(["012", "120", "201", "102", "021", "210"])

### Auxilliary Functions ###

def unzip(l):
    """
    [(a1, b1), ..., (an, bn)] ----> ([a1, ..., an], [b1, ..., bn])
    """

    return zip(*l)

def normalize(l):
    """
    Normalizes input list.

    Parameters
    ----------
    l, List
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

## Ternary Projections and Point Operations

translation_dict = dict(zip("brl", "012"))
reverse_translation_dict = dict(zip("012", "brl"))

def represent_permutation(permutation, reverse=False):
    """
    Maps a permutation from the 'brl' specification to or from the '012'
    internal representation.
    """

    p = ""
    if reverse:
        translator = reverse_translation_dict
    else:
        translator = translation_dict
    for i in permutation:
        p += translator[i]
    return p

def compose_permutations(inner, outer):
    """
    Composes the two permutations p1 and p2 as if they were functions in the
    symmetric group. That is, p3 = p1 o p2.

    Parameters
    ----------
    inner: string
        The inner (first applied) permutation, a string of '012'
    outer: string, None
        The outer (second applied) permutation, a string of '012'

    Returns
    -------
    composite, string
        The permutaton composite = outer o inner
    """

    if inner not in PERMUTATIONS:
        inner = represent_permutation(inner)
    if outer not in PERMUTATIONS:
        outer = represent_permutation(outer)

    d_inner = dict(zip("012", inner))
    d_outer = dict(zip("012", outer))
    composite = "".join(d_outer[d_inner[i]] for i in "012")
    return represent_permutation(composite, reverse=True)

def permute_point(point, permutation=None):
    """
    Permutes the point according to the permutation keyword argument. The
    default permutation is "012" which does not change the order of the
    coordinate. To rotate counterclockwise, use "120" and to rotate clockwise
    use "201".

    Parameters
    ----------
    point: 3-tuple, (i, j, k)
        The point to be permuted.
    permutation: string
        The permutation, a string of '012'

    Raises
    ------
    ValueError, if permutation is not valid

    Returns
    -------
    permuted, 3-tuple, (i, j, k)
        The permutation point
    """

    if not permutation:
        return point
    if permutation == "brl" or permutation == "012":
        return point

    if permutation not in PERMUTATIONS:
        r_permutation = represent_permutation(permutation)
        if r_permutation not in PERMUTATIONS:
            raise ValueError, "Invalid permutation: %s" % permutation
        permutation = r_permutation

    permuted_point = tuple(point[int(permutation[i])] for i in range(len(point)))
    return permuted_point

def project_point(p, permutation=None):
    """
    Maps (x,y,z) coordinates to planar simplex.

    Parameters
    ----------
    p: 3-tuple
        The point to be projected p = (i, j, k)
    permutation, string, None, equivalent to "012"
        The order of the coordinates, counterclockwise from the origin

    Returns
    -------
    projected, numpy.array of projected tuple (x, y)
    """

    permuted = permute_point(p, permutation=permutation)
    i = permuted[0]
    j = permuted[1]
    x = i + j / 2.
    y = SQRT3OVER2 * j
    projected = numpy.array([x, y])
    return projected

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

    xs, ys = unzip(project_point(p, permutation=permutation) for p in s)
    return xs, ys
