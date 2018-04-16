"""Old distance functions for periodic boundary conditions.

Depreciated. Use f2py function in distance.f90.

"""
import numpy as np
from numba import jit


@jit
def min_d(a, b, P, box):
    """Return minimum image distance between two nodes in the simulation box.

    Parameters:
    P    -- Position array of system
    box  -- box vectors
    a    -- node from wich to measure
    b    -- node wich is measured to

    Returns:
    d    -- Difference vector between a and b using minimum image convention

    """
    d = np.zeros((2, ))
    d = P[a] - P[b]
    if (np.absolute(d[0]) > 0.5*box[0]).all():
        if d[0] > 0:
            d[0] = P[a][0] - (P[b][0]+box[0])
        elif d[0] < 0:
            d[0] = P[a][0] - (P[b][0]-box[0])
    if (np.absolute(d[1]) > 0.5*box[1]).all():
        if d[1] > 0:
            d[1] = P[a][1] - (P[b][1]+box[1])
        elif d[1] < 0:
            d[1] = P[a][1] - (P[b][1]-box[1])
    return d


@jit
def min_dn(a, b, P, box):
    """Return euclidian distance between a and b."""
    d = min_d(a, b, P, box)
    return np.linalg.norm(d)


def mdist(P, box):
    """Calculate distance matrix."""
    n = P.shape[0]
    D = np.array([min_dn(i, j, P, box) for i in range(n) for j in range(n)])\
        .reshape((n, n))
    return D


@jit
def mdist_loop(P, box):
    """Calculate mindist matrix with for loops."""
    n = P.shape[0]
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            D[i, j] = min_dn(i, j, P, box)
    return D
