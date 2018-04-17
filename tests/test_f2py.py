"""Test f2py functions."""
import distance as dist
import lattice
import pbc
import numpy as np
import energy
import fenergy

dim = (20, 20)
A, AA = lattice.links_matrix(dim)
I, J = np.nonzero(A)
II, JJ = np.nonzero(AA)
P, box = lattice.fill_box(dim)
ll = 1.0

print(dist.__doc__)
print(fenergy.__doc__)

old = [[pbc.min_d(i, j, P, box) for j in range(200)] for i in range(200)]

new = [[dist.mindist(i, j, P, box) for j in range(200)] for i in range(200)]

np.nonzero(np.array(old)-np.array(new))

dist.mindist(2, 46, P, box)
np.linalg.norm(dist.mindist(2, 46, P, box))
pbc.min_dn(2, 46, P, box)
dist.mindist_norm(2, 46, P, box)

D = pbc.mdist_loop(P, box)
DD = dist.dist_mat(P, box)
np.nonzero(D - DD)

energy.energy(P, box, A, ll)
energy.gradient(P, box, A, ll)
D = dist.dist_mat(P, box)
np.fill_diagonal(D, 1)
grad = np.zeros((200, 2))
fenergy.gradient(A, D, P, box, ll, grad)

P, box = lattice.stretch_it(P, box, 1.5)
