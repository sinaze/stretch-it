"""Distance functions for periodic boundary conditions."""
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
    norm -- return euclidian distance when True, else return distance vector

    Returns:
    d    -- (Euclidian) distance between a and b using minimum image convention

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
    """Return minimum image distance between two nodes in the simulation box.

    Parameters:
    P    -- Position array of system
    box  -- box vectors
    a    -- node from wich to measure
    b    -- node wich is measured to
    norm -- return euclidian distance when True, else return distance vector

    Returns:
    d    -- (Euclidian) distance between a and b using minimum image convention

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
    return np.linalg.norm(d)


def mdist(P, box):
    """Calculate distance matrix."""
    n = P.shape[0]
    D = np.array([min_dn(i, j, P, box) for i in range(n) for j in range(n)])\
        .reshape((n, n))
    return D

# TODO: replace list comprehension


@jit
def mdist_loop(P, box):
    """Calculate mindist matrix with for loops."""
    n = P.shape[0]
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            D[i, j] = min_dn(i, j, P, box)
    return D


# ----------------------------------------------------------------------------
# depreciated functions follow
def mdist_2(P, box):
    """Calculate distance matrix."""
    PP = periodic_positions(P, box)
    n = P.shape[0]
    mindist_table = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            mindist_table[i, j] = mindist(PP, i, j)
    return mindist_table


def mindist(PP, a, b):
    """Return minimum distance between two atoms a and b."""
    distance = np.zeros(9)
    for image in range(9):
        distance[image] = np.sqrt((PP[0][a][0] - PP[image][b][0])**2 +
                                  (PP[0][a][1] - PP[image][b][1])**2)
    return distance.min()


def min_img_idx(P, box, a, b):
    """Return image index corresponding to the minimum distance."""
    PP = periodic_positions(P, box)
    distance = np.zeros(9)
    for image in range(9):
        distance[image] = np.sqrt((PP[0][a][0] - PP[image][b][0])**2 +
                                  (PP[0][a][1] - PP[image][b][1])**2)
    return np.argmin(distance)


def periodic_positions(P, box):
    """Create position matrix for periodic images."""
    x_box, y_box = box[0], box[1]
    n = P.shape[0]
    P_x_plus = np.column_stack((P[:, 0] + np.ones(n)*x_box, P[:, 1]))
    P_x_minus = np.column_stack((P[:, 0] - np.ones(n)*x_box, P[:, 1]))
    P_y_plus = np.column_stack((P[:, 0], P[:, 1] + np.ones(n)*y_box))
    P_y_minus = np.column_stack((P[:, 0], P[:, 1] - np.ones(n)*y_box))
    P_x_plus_y_plus = np.column_stack((P[:, 0] + np.ones(n)*x_box,
                                       P[:, 1] + np.ones(n)*y_box))
    P_x_plus_y_minus = np.column_stack((P[:, 0] + np.ones(n)*x_box,
                                        P[:, 1] - np.ones(n)*y_box))
    P_x_minus_y_plus = np.column_stack((P[:, 0] - np.ones(n)*x_box,
                                        P[:, 1] + np.ones(n)*y_box))
    P_x_minus_y_minus = np.column_stack((P[:, 0] - np.ones(n)*x_box,
                                        P[:, 1] - np.ones(n)*y_box))
    # PP[image][atom], image=x_plus, x_minus, ...
    return np.array([P, P_x_plus, P_x_plus_y_minus, P_y_minus,
                    P_x_minus_y_minus, P_x_minus, P_x_minus_y_plus,
                    P_y_plus, P_x_plus_y_plus])
