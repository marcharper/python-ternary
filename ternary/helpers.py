
import numpy

### Constants ###

SQRT3 = numpy.sqrt(3)
SQRT3OVER2 = SQRT3 / 2.

### Auxilliary Functions ###

def unzip(l):
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

## Ternary Projections ##

def project_point(p):
    """
    Maps (x,y,z) coordinates to planar simplex.

    Parameters
    ----------
    p: 3-tuple
        The point to be projected p = (x, y, z)
    """

    a, b, c = p
    x = b + c/2.
    y = SQRT3OVER2 * c
    return (x, y)

def project_sequence(s):
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

    xs, ys = unzip(map(project_point, s))
    return xs, ys
