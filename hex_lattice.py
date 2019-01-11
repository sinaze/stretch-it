"""Create hexagonal lattice."""
import numpy as np
import periodicarray as pbc
import tools


def create_lattice(dim, e=1.):
    """Create node position array for a hexagonal lattice.

    Parameters:
    dim -- dim = (nx, ny)
    nx -- number of columns of nodes (must be even)
    ny -- number of rows of nodes (must be even)
    e -- distance between nodes (default: 1.0)

    Returns:
    P -- array of node positions, P[i, j] = [x_i, y_i]

    """
    # create rectangular basis
    c = np.sqrt(3) * e
    assert dim[0] % 2 == 0
    x = np.linspace(0, (dim[0] - 1)*e, num=int(dim[0]))
    assert dim[1] % 2 == 0
    y = np.linspace(0, c*(dim[1]/2 - 1), num=int(dim[1]/2))
    grid_x, grid_y = np.meshgrid(x, y, indexing='xy')
    P0 = np.column_stack((grid_x.ravel(), grid_y.ravel()))
    # add shifted rectangular lattice to create a hexagonal
    P1 = np.concatenate((P0,
                        np.column_stack((P0[:, 0]+e/2., P0[:, 1]+c/2.))))
    # sort positions starting with lower row from left to right
    P3 = P1[np.lexsort(P1.T)]
    return P3

# TODO: raise exception when nx, ny are not even


def create_mesh(dim):
    """Create hexagonal mesh with numbered nodes."""
    n = dim[0]
    m = dim[1]
    M = np.array([[[x, 0] if j % 2 is 0 else [0, x]
                 for x in range(j*n+1, j*n+1+n)]
                 for j in range(0, m)])
    M = M.ravel().reshape((m, 2*n))
    return np.flipud(M)


def links_matrix(dim):
    """Create adjacency Matrix A; AA w/o PBC for plotting."""
    # create mesh to assign numbers to the nodes
    n = dim[0] * dim[1]
    mesh = create_mesh(dim)
    periodic_mesh = pbc.Periodic_Lattice(mesh)
    # create neighbor list
    neighbors = np.zeros((n, 6))
    for node in range(1, n+1):
        idx = tools.get_idx(periodic_mesh, node)
        neighbors[node-1][:] = np.array([periodic_mesh[idx[0]-1, idx[1]-1],
                                         periodic_mesh[idx[0]-1, idx[1]+1],
                                         periodic_mesh[idx[0]+1, idx[1]-1],
                                         periodic_mesh[idx[0]+1, idx[1]+1],
                                         periodic_mesh[idx[0], idx[1]+2],
                                         periodic_mesh[idx[0], idx[1]-2]])
    # create A
    A = np.zeros((n, n))
    for i in range(n):
        for j in range(6):
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
    for i in range(dim[0]):
        for j in range(dim[0]):
            AA[lower[i]-1, upper[j]-1] = 0
            AA[upper[i]-1, lower[j]-1] = 0
    for i in range(int(dim[0]/2)):
        for j in range(int(dim[0]/2)):
            AA[left[i]-1, right[j]-1] = 0
            AA[right[i]-1, left[j]-1] = 0
    return A, AA

# TODO: reduce for-loops


def construct_box(P, e=1.):
    """Construct box and center lattice."""
    x_length = P[-1, 0] - P[0, 0]
    y_length = P[-1, 1] - P[0, 1]
    c = np.sqrt(3) * e
    x_gap = e/4.
    y_gap = c/4.
    P1 = np.column_stack((P[:, 0] + x_gap, P[:, 1] + y_gap))
    x_box = 2 * x_gap + x_length
    y_box = 2 * y_gap + y_length
    box = (x_box, y_box)
    return P1, box


def fill_box(dim):
    """Fill a box of suitable size with nx x ny lattice."""
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
