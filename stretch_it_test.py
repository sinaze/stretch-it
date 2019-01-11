#!/usr/bin/env python3
"""Simulate complete stretching cycle for one hex_system / dilution."""
import hex_lattice
import energy
import hex_system
import hex_inout
import numpy as np
import scipy.optimize as opt
from joblib import Parallel, delayed
import os
import sys
%matplotlib inline


def init(dim):
    """Initialize."""
    # create adjacency matrix, read in by file eventually
    A, AA = hex_lattice.links_matrix(dim)
    # get nonzero indices
    I, J = np.nonzero(A)
    II, JJ = np.nonzero(AA)
    III, JJJ = np.nonzero(A - AA)
    return A, AA, I, J, II, JJ, III, JJJ


# dimensions
dim = (8, 8)
# initialize
A, AA, I, J, II, JJ, III, JJJ = init(dim)

# create list of stretched hex_system copies
systems = []
for _ in range(1):
    systems.append([hex_system.LatticeSystem(dim, A, AA, I, J, II,
                                             JJ, III, JJJ)])

# dilute
for i in range(1):
    systems[i][0].dilute_site(3)

# systems[0][0].show()

# stretch
for i in range(1):
    for k in range(10):
        systems[i].append(hex_system.stretch_sys_site(systems[i][0],
                                                      (k+1)/10,
                                                      ax=1))

# optimize positions for minimal total energy
for j in range(1):
    # print('Run ' + str(j+1) + ' of ' + str(1))
    # minimize energy function
    r = Parallel(n_jobs=6, verbose=0, batch_size=1)(
        delayed(opt.minimize)(energy.energy,
                              systems[j][k].P.ravel(),
                              args=(systems[j][k].box,
                                    systems[j][k].A,
                                    systems[j][k].ll),
                              method='CG',
                              jac=energy.gradient,
                              options={'disp': True,
                                       'gtol': 1e-7})
        for k in range(10+1))
    # feed optimized positions back to system objects
    for k in range(10+1):
        systems[j][k].P = r[k].x.reshape((-1, 2))
        systems[j][k].ener = r[k].fun

systems[0][0].show2()
# hex_inout.save_object(systems, args.fname)
systems
