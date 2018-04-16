"""Simulate complete stretching cycle for one system / dilution."""
import lattice
import energy
import system
import inout
import numpy as np
import scipy.optimize as opt
from joblib import Parallel, delayed
import argparse

parser = argparse.ArgumentParser(description="Calculates energy curve of a\
                                 stretching process of a honeycomb lattice")
parser.add_argument("nx", help="Number of lattice points to fill the box",
                    type=int)
parser.add_argument("ny", help="Number of lattice points to fill the box",
                    type=int)
parser.add_argument("-d", "--dilute", type=int, help="<Required> Set flag",
                    required=True)
parser.add_argument("-dn", "--diluteno", help="Number sample runs",
                    type=int, required=True)
parser.add_argument("-k", "--increment", help="stretching increment 1/k",
                    type=int, required=True)
parser.add_argument("-v", help="verbosity",
                    type=int, required=True)
parser.add_argument("-it", "--iteration", help="points on curve",
                    type=int, required=True)
parser.add_argument("-f", "--fname", help="Filename.pkl", type=str,
                    required=True)
args = parser.parse_args()

# dimensions
dim = (args.nx, args.ny)


def init():
    """Initialize."""
    # create adjacency matrix, read in by file eventually
    A_, AA_ = lattice.links_matrix(dim)
    # get nonzero indices
    I_, J_ = np.nonzero(A_)
    II_, JJ_ = np.nonzero(AA_)
    return A_, AA_, I_, J_, II_, JJ_


A_, AA_, I_, J_, II_, JJ_ = init()

# create list of stretched system copies
systems = []
for _ in range(args.diluteno):
    systems.append([system.LatticeSystem(dim, A_, AA_, II_, JJ_)])

# dilute
for i in range(args.diluteno):
    systems[i][0].dilute_site(args.dilute)

# stretch
for i in range(args.diluteno):
    for k in range(args.iteration):
        systems[i].append(system.stretch_sys_site(systems[i][0],
                                                  (k+1)/args.increment, ax=0))

# optimize positions for minimal total energy
for j in range(args.diluteno):
    r = Parallel(n_jobs=-1, verbose=args.v)(delayed(opt.minimize)
                                            (energy.energy,
                                             systems[j][k].P.ravel(),
                                             args=(systems[j][k].box,
                                                   systems[j][k].A,
                                                   systems[j][k].ll),
                                             method='CG',
                                             jac=energy.gradient,
                                             options={'disp': True,
                                                      'gtol': 1e-5})
                                            for k in range(args.iteration+1))
    for k in range(args.iteration+1):
        # feed optimized positions back to system objects
        systems[j][k].P = r[k].x.reshape((-1, 2))
        systems[j][k].ener = r[k].fun

inout.save_object(systems, args.fname)
