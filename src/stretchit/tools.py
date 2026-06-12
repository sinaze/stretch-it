"""Small useful functions."""
import numpy as np


def get_idx(array, value):
    """Return indices of an array for given value."""
    idx = np.where(array == value)
    return idx[0][0], idx[1][0]
