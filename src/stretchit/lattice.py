"""Create honeycomb lattice."""
import numpy as np
from . import periodicarray as pbc
from . import tools


def create_lattice(dim, e=1.):
    """Create node position array for a honeycomb lattice.

    Parameters:
    nx -- number of columns of nodes (must be even)
    ny -- number of rows of nodes (must be multiple of 4)
    e -- distance between nodes (default: 1.0)

    Returns:
    P -- array of node positions, P[i, j] = [x_i, y_i]

    """
    # create rectangular basis
    c = np.sqrt(3) * e
    assert dim[0] % 2 == 0
    x = np.linspace(0, (dim[0]/2 - 1)*c, num=int(dim[0]/2))
    assert dim[1] % 4 == 0
    y = np.linspace(0, 3*e*(dim[1]/4 - 1), num=int(dim[1]/4))
    grid_x, grid_y = np.meshgrid(x, y, indexing='xy')
    P0 = np.column_stack((grid_x.ravel(), grid_y.ravel()))
    # add shifted rectangular lattice to create a hexagonal
    P1 = np.concatenate((P0,
                        np.column_stack((P0[:, 0]+c/2., P0[:, 1]+3.*e/2.))))
    # add two shifted hexagonals to create honeycomb
    P2 = np.concatenate((P1, np.column_stack((P1[:, 0], P1[:, 1] + e))))
    # sort positions starting with lower row from left to right
    P3 = P2[np.lexsort(P2.T)]
    return P3

# TODO: raise exception when nx, ny are not even / multiple of 4


def create_mesh(dim):
    """Create honeycomb mesh with numbered nodes."""
    n = int(dim[0]/2)
    m = dim[1]
    M = np.array([[[x, 0] if j % 2 == 0 else [0, x]
                 for x in range(j*2*n+1, j*2*n+1+2*n)]
                 for j in range(0, round(m/2))])
    M = M.ravel().reshape((m, 2*n))
    return np.flipud(M)


def links_matrix(dim):
    """Create adjacency Matrix A; AA w/o PBC for plotting."""
    # create mesh to assign numbers to the nodes
    assert dim[0] % 2 == 0
    n = int(dim[0]/2) * dim[1]
    mesh = create_mesh(dim)
    periodic_mesh = pbc.Periodic_Lattice(mesh)
    # create neighbor list
    neighbors = np.zeros((n, 3))
    for node in range(1, n+1):
        idx = tools.get_idx(periodic_mesh, node)
        if periodic_mesh[idx[0]-1, idx[1]] != 0:
            neighbors[node-1][:] = np.array([periodic_mesh[idx[0]-1, idx[1]],
                                             periodic_mesh[idx[0]+1, idx[1]-1],
                                             periodic_mesh[idx[0]+1,
                                                           idx[1]+1]])
        elif periodic_mesh[idx[0]+1, idx[1]] != 0:
            neighbors[node-1][:] = np.array([periodic_mesh[idx[0]+1, idx[1]],
                                             periodic_mesh[idx[0]-1, idx[1]-1],
                                             periodic_mesh[idx[0]-1,
                                                           idx[1]+1]])
    # create A
    A = np.zeros((n, n))
    for i in range(n):
        for j in range(3):
            if neighbors[i][j] > i:
                A[i][int(neighbors[i][j]-1)] = 1
    # remove periodic links manually
    AA = np.copy(A)
    upper = mesh[0, :]
    lower = mesh[-1, :]
    left = mesh[:, 0]
    right = mesh[:, -1]
    upper = upper[upper != 0]
    lower = lower[lower != 0]
    left = left[left != 0]
    right = right[right != 0]
    for i in range(int(dim[0]/2)):
        for j in range(int(dim[0]/2)):
            AA[lower[i]-1, upper[j]-1] = 0
            AA[left[i]-1, right[j]-1] = 0
            AA[upper[i]-1, lower[j]-1] = 0
            AA[right[i]-1, left[j]-1] = 0
    return A, AA

# TODO: reduce for-loops


def construct_box(P, e=1.):
    """Construct box and center lattice."""
    x_length = P[-1, 0] - P[0, 0]
    y_length = P[-1, 1] - P[0, 1]
    c = np.sqrt(3) * e
    x_gap = c/4.
    y_gap = e/4.
    P1 = np.column_stack((P[:, 0] + x_gap, P[:, 1] + y_gap))
    x_box = 2 * x_gap + x_length
    y_box = 2 * y_gap + y_length
    box = (x_box, y_box)
    return P1, box


def fill_box(dim):
    """Fill a box of suitable size with nx x ny honeycomb lattice."""
    P = create_lattice(dim)
    P1, box = construct_box(P)
    return P1, box


def stretch_it(P, box, alpha, axis=1):
    """Stretch box uniformly in given axis."""
    alpha_t = 1 + alpha
    x_box, y_box = box[0], box[1]
    assert axis == 0 or axis == 1
    if axis == 1:
        P1 = np.column_stack((P[:, 0], P[:, 1]*alpha_t))
        y_box = y_box*alpha_t
    elif axis == 0:
        P1 = np.column_stack((P[:, 0]*alpha_t, P[:, 1]))
        x_box = x_box*alpha_t
    box = (x_box, y_box)
    return P1, box
