#!/usr/bin/env python3
"""Simulate complete stretching cycle for one system / dilution (eps variant)."""
from stretchit import lattice, energy, system, inout
import numpy as np
import scipy.optimize as opt
from joblib import Parallel, delayed
import argparse
import os
import sys

parser = argparse.ArgumentParser(description='Calculates energy curve of a\
                                 stretching process of a honeycomb lattice')
parser.add_argument('nx', help='Number of lattice points to fill the box',
                    type=int)
parser.add_argument('ny', help='Number of lattice points to fill the box',
                    type=int)
parser.add_argument('-v', '--verbosity', help='control verbosity, default: 10',
                    type=int, default=10)
parser.add_argument('--hor', help='stretch horizontally', default=1,
                    action='store_const', const=0)
parser.add_argument('-nt', help='Number of threads, default: all available',
                    type=int, default=-1)
required = parser.add_argument_group('required arguments')
required.add_argument('-d', '--dilute', type=int, help='Number of sites / bonds\
                      to remove, can be 0', required=True)
required.add_argument('-dn', '--diluteno', help='Number of sample runs',
                      type=int, required=True)
required.add_argument('-k', '--increment', help='stretching increment 1/k',
                      type=int, required=True)
required.add_argument('-it', '--iteration', help='points on curve',
                      type=int, required=True)
required.add_argument('-f', '--fname', help='filename.pkl', type=str,
                      required=True)
args = parser.parse_args()

if os.path.exists(args.fname):
    ans = input('File exists, continue? ')
    if ans == 'y' or ans == 'yes':
        print('Continuing...')
    else:
        print('Abort program...')
        sys.exit(0)


def init(dim):
    """Initialize."""
    A, AA = lattice.links_matrix(dim)
    I, J = np.nonzero(A)
    II, JJ = np.nonzero(AA)
    III, JJJ = np.nonzero(A - AA)
    return A, AA, I, J, II, JJ, III, JJJ


try:
    dim = (args.nx, args.ny)
    A, AA, I, J, II, JJ, III, JJJ = init(dim)

    systems = []
    for _ in range(args.diluteno):
        systems.append([system.LatticeSystem(dim, A, AA, I, J, II,
                                             JJ, III, JJJ)])

    for i in range(args.diluteno):
        systems[i][0].dilute_site(args.dilute)

    for i in range(args.diluteno):
        for k in range(args.iteration):
            systems[i].append(system.stretch_sys_site(systems[i][0],
                                                      (k+1)/args.increment,
                                                      ax=args.hor))

    for j in range(args.diluteno):
        print('Run ' + str(j+1) + ' of ' + str(args.diluteno))
        r = Parallel(n_jobs=args.nt, verbose=args.verbosity, batch_size=1)(
            delayed(opt.minimize)(energy.energy,
                                  systems[j][k].P.ravel(),
                                  args=(systems[j][k].box,
                                        systems[j][k].A,
                                        systems[j][k].ll),
                                  method='CG',
                                  jac=energy.gradient,
                                  options={'disp': True,
                                           'gtol': 1e-9})
            for k in range(args.iteration+1))
        for k in range(args.iteration+1):
            systems[j][k].P = r[k].x.reshape((-1, 2))
            systems[j][k].ener = r[k].fun

    inout.save_object(systems, args.fname)
except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
