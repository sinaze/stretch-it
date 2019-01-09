"""Analyze."""
import numpy as np
import pickle
import matplotlib.pyplot as plt
# %matplotlib inline


class ReducedSystem:
    """Reduced system only containing box size and averaged energies."""

    def __init__(self, mean_box, mean_en, std_en, err_en, dil, tot):
        """Initialize."""
        self.ener = mean_en
        self.std = std_en
        self.err = err_en
        self.box = mean_box
        self.dil = dil
        self.tot = tot
        self.phi = dil/tot


path = '/net/storage/zendehroud/honey_big_highres/16x32_d5_100_a.pkl'
with open(path, 'rb') as inputs:
    obj = pickle.load(inputs)

path_h = '/net/storage/zendehroud/honey_big_highres/16x32_d5_100_h_a.pkl'
with open(path_h, 'rb') as inputs:
    obj_h = pickle.load(inputs)

np.array([obj.box[:, 1], obj.ener])[:, 1]
plt.plot(obj.box[:, 1], obj.ener)
plt.plot(obj.box[:, 1], np.gradient(obj.ener, edge_order=2))
