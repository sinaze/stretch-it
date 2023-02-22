#!/usr/bin/env python3
"""Simulate complete stretching cycle for one system / dilution."""
import lattice
import energy
import system
import inout
import numpy as np
import scipy.optimize as opt
from joblib import Parallel, delayed
import argparse
import toml
from pydantic import BaseModel
import os
import sys


class Config(BaseModel):
    nx: int
    ny: int
    dilute: int
    nsamples: int
    increment: int
    nstretch: int
    incrementinit: int = 0
    subset: bool = True
    horizontal: bool = False

    @classmethod
    def from_toml(cls, path):
        data = toml.load(open(path, encoding='UTF-8'))
        return cls(**data)


parser = argparse.ArgumentParser(description='Calculates energy curve of a\
                                 stretching process of a honeycomb lattice')
# parser.add_argument('nx', help='Number of lattice points to fill the box',
#                     type=int)
# parser.add_argument('ny', help='Number of lattice points to fill the box',
#                     type=int)
parser.add_argument('-v', '--verbosity', help='control verbosity, default: 10',
                    type=int, default=10)
# parser.add_argument('--hor', help='stretch horizontally', default=1,
#                     action='store_const', const=0)
# parser.add_argument('--subset', help='only dilute a subset of sites',
#                     default=0, action='store_const', const=1)
parser.add_argument('-nt', help='Number of threads, default: all available',
                    type=int, default=-1)
# parser.add_argument('-ki', help='Initial value for stretching iteration\
#                     (optional)', type=int, default=0)
required = parser.add_argument_group('required arguments')
required.add_argument('-c', '--config',
                      help='Input file in toml format', type=str,
                      required=True)
# required.add_argument('-d', '--dilute', type=int, help='Number of sites / bonds\
#                       to remove, can be 0', required=True)
# required.add_argument('-dn', '--diluteno', help='Number of sample runs',
#                       type=int, required=True)
# required.add_argument('-k', '--increment', help='stretching increment 1/k',
#                       type=int, required=True)
# required.add_argument('-it', '--iteration', help='points on curve',
#                       type=int, required=True)
required.add_argument('-f', '--fname',
                      help='Save results to filename.pkl', type=str,
                      required=True)
args = parser.parse_args()

conf = Config.from_toml(args.config)
if os.path.exists(args.fname):
    ans = input('File exists, continue? ')
    if ans == 'y' or ans == 'yes':
        print('Continuing...')
    else:
        print('Abort program...')
        sys.exit(0)


def init(dim):
    """Initialize."""
    # create adjacency matrix, read in by file eventually
    A, AA = lattice.links_matrix(dim)
    # get nonzero indices
    I, J = np.nonzero(A)
    II, JJ = np.nonzero(AA)
    III, JJJ = np.nonzero(A - AA)
    ll = lattice.create_ll(dim)
    return A, AA, I, J, II, JJ, III, JJJ, ll


if __name__ == '__main__':
    try:
        # dimensions
        dim = (conf.nx, conf.ny)
        # initialize
        A, AA, I, J, II, JJ, III, JJJ, ll = init(dim)

        # create list of stretched system copies
        systems = []
        for _ in range(conf.nsamples):
            systems.append([system.LatticeSystem(dim, A, AA, I, J, II,
                                                JJ, III, JJJ, ll)])

        # dilute
        if conf.subset:
            for i in range(conf.nsamples):
                systems[i][0].dilute_site_subset(conf.dilute)
        elif conf.subset == False:
            for i in range(conf.nsamples):
                systems[i][0].dilute_site(conf.dilute)

        # stretch
        if conf.horizontal:
            stretchax = 0
        else:
            stretchax = 1
        
        for i in range(conf.nsamples):
            for k in range(conf.nstretch - conf.incrementinit):
                systems[i].append(system.stretch_sys_site(
                    systems[i][0],
                    (conf.incrementinit+k+1)/conf.increment, ax=stretchax))

        # optimize positions for minimal total energy
        for j in range(conf.nsamples):
            print('Run ' + str(j+1) + ' of ' + str(conf.nsamples))
            # minimize energy function
            r = Parallel(n_jobs=args.nt, verbose=args.verbosity, batch_size=1)(
                delayed(opt.minimize)(energy.energy,
                                    systems[j][k].P.ravel(),
                                    args=(systems[j][k].box,
                                            systems[j][k].A,
                                            systems[j][k].ll),
                                    method='CG',
                                    jac=energy.gradient,
                                    options={'disp': True,
                                            'gtol': 1e-7})
                for k in range(conf.nstretch - conf.incrementinit + 1))
            # feed optimized positions back to system objects
            for k in range(conf.nstretch - conf.incrementinit + 1):
                systems[j][k].P = r[k].x.reshape((-1, 2))
                systems[j][k].ener = r[k].fun

        inout.save_object(systems, args.fname)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
