"""Check gradient."""
import numpy as np
from scipy.optimize import check_grad
import energy
import lattice

dim = (32, 32)
# dim = (4, 4)

P, box = lattice.fill_box(dim)
A, _ = lattice.links_matrix(dim)
l = lattice.create_ll(dim)

# uncomment to check stretched lattice
# P, box = lattice.stretch_it(P, box, 0.8)

err = check_grad(energy.energy, energy.gradient, P.ravel(), box, A, l)
print(err)
