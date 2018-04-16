"""Compute energy and gradient of given system."""
import numpy as np
import distance as dist
from numba import jit


@jit
def energy(P, box, A, l):
    """Calculate the potential energy of the system."""
    # reshape flattened matrix into (:,2)-matrix
    P = P.reshape((-1, 2))
    # get distance matrix
    D = dist.dist_mat(P, box)
    # return potential energy
    return .5 * (A * (D - l)**2).sum()


@jit
def gradient(P, box, A, l):
    """Calculate the gradient of the energy function."""
    n = A.shape[0]
    P = P.reshape((-1, 2))
    D = dist.dist_mat(P, box)
    np.fill_diagonal(D, 1)
    grad = np.zeros((n, 2))
    for i in range(n):
        for j in range(n):
            grad[i] += A[i, j] * dist.mindist(i, j, P, box) \
                * (1. - l/D[i, j])\
                + A[j, i] * dist.mindist(i, j, P, box) \
                * (1. - l/D[i, j])
    return grad.ravel()

# TODO: vectorize gradient
