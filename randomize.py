"""Random dilution of network."""
import random
import numpy as np


def dilute(A_, AA_, II_, JJ_, s):
    """Remove links randomly."""
    if s == 0:
        pass
    else:
        nonzero_list = [(i, j) for i, j in zip(II_, JJ_)]
        random.shuffle(nonzero_list)
        popped = []
        for _ in range(s):
            # pop random link
            rm_index = nonzero_list.pop()
            popped.append(rm_index)
            A_[rm_index[0], rm_index[1]] = 0
            AA_[rm_index[0], rm_index[1]] = 0
        I_, J_ = np.nonzero(A_)
        # return A_, AA_, I_, J_, popped
