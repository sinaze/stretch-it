"""Compute energy and gradient of given system."""
import numpy as np
import distance as dist
import fenergy


def energy(P, box, A, l):
    """Calculate the potential energy of the system."""
    # reshape flattened matrix into (:,2)-matrix
    P = P.reshape((-1, 2))
    # get distance matrix
    D = dist.dist_mat(P, box)
    # return potential energy
    return .5 * (A * (D - l)**2).sum()


def gradient(P, box, A, l):
    """Calculate the gradient of the energy function."""
    n = A.shape[0]
    P = P.reshape((-1, 2))
    D = dist.dist_mat(P, box)
    np.fill_diagonal(D, 1)
    grad = np.zeros((n, 2))
    grad = fenergy.gradient(A, D, P, box, l, grad)
    return grad.ravel()
