"""System class."""
import lattice
import inout
import energy
import pbc
import random
import numpy as np
import numba


class LatticeSystem:
    """Class for a simulation system."""

    def __init__(self, dim, A, AA, II, JJ):
        """Initialize as filled box."""
        self.P, self.box = lattice.fill_box(dim)
        self.dim = dim
        self.II, self.JJ = np.copy(II), np.copy(JJ)
        self.A, self.AA = np.copy(A), np.copy(AA)
        self.ll = 1.0

    @numba.jit
    def show(self):
        """Plot system configuration."""
        self.create_mdist()
        inout.show_system(self.P, self.II, self.JJ, self.D, self.ll,
                          box=self.box)

    @numba.jit
    def save(self, name):
        """Save system configuration."""
        self.create_mdist()
        inout.save_system(name, self.P, self.II, self.JJ, self.D, self.ll,
                          box=self.box)

    @numba.jit
    def energy(self):
        """Compute energy of system."""
        self.ener = energy.energy(self.P, self.box, self.A, self.ll)
        return self.ener

    @numba.jit
    def grad(self):
        """Compute Jacobi matrix."""
        return energy.gradient(self.P, self.box, self.A, self.ll)

    @numba.jit
    def dist(self, a, b, euc=True):
        """Return distance."""
        return pbc.min_d(a, b, self.P, self.box, norm=euc)

    @numba.jit
    def create_mdist(self):
        """Create distance matrix."""
        self.D = pbc.mdist_loop(self.P, self.box)

    def dilute_bond(self, s):
        """Dilute network by removing links in matrix."""
        self.nonzero_list = [(i, j) for i, j in zip(self.II, self.JJ)]
        random.shuffle(self.nonzero_list)
        self.popped = []
        for _ in range(s):
            # pop random link
            self.rm_index = self.nonzero_list.pop()
            self.popped.append(self.rm_index)
            self.A[self.rm_index] = 0
            self.AA[self.rm_index] = 0
        self.I, self.J = np.nonzero(self.A)
        self.II, self.JJ = np.nonzero(self.AA)

    def dilute_site(self, s):
        """Dilute by removing a node (site)."""
        n = int(self.dim[0]/2) * self.dim[1]
        numbers = list(range(n))
        # select random site for deletion
        self.popped = []
        random.shuffle(numbers)
        for _ in range(s):
            site = numbers.pop()
            self.popped.append(site)
            for i in range(len(numbers)):
                if numbers[i] >= site:
                    numbers[i] -= 1
            # delete
            self.P = np.delete(self.P, site, 0)
            self.A = np.delete(self.A, site, 0)
            self.A = np.delete(self.A, site, 1)
            self.AA = np.delete(self.AA, site, 0)
            self.AA = np.delete(self.AA, site, 1)
        self.I, self.J = np.nonzero(self.A)
        self.II, self.JJ = np.nonzero(self.AA)


def stretch_sys(sys, alpha, ax=1):
    """Return system instance for a streched system."""
    sys_s = LatticeSystem(sys.dim, sys.A, sys.AA, sys.II, sys.JJ)
    sys_s.P, sys_s.box = lattice.stretch_it(sys_s.P, sys_s.box, alpha, axis=ax)
    return sys_s


def stretch_sys_site(sys, alpha, ax=1):
    """Return system instance for a streched system."""
    sys_s = LatticeSystem(sys.dim, sys.A, sys.AA, sys.II, sys.JJ)
    sys_s.P = sys.P
    sys_s.A = sys.A
    sys_s.A = sys.A
    sys_s.AA = sys.AA
    sys_s.AA = sys.AA
    sys_s.I, sys.J = np.nonzero(sys_s.A)
    sys_s.II, sys.JJ = np.nonzero(sys_s.AA)
    sys_s.P, sys_s.box = lattice.stretch_it(sys_s.P, sys_s.box, alpha, axis=ax)
    return sys_s
