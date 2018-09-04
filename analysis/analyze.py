"""Analyze."""
import numpy as np
import pickle
import lattice
import matplotlib.pyplot as plt
import matplotlib.patches as patches
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


path = '/net/storage/zendehroud/honey_big_highres/16x32_d35_100_fixed.pkl'
with open(path, 'rb') as inputs:
    obj = pickle.load(inputs)

path_h = '/net/storage/zendehroud/honey_big_highres/16x32_d5_100_h_a.pkl'
with open(path_h, 'rb') as inputs:
    obj_h = pickle.load(inputs)

np.array([obj.box[:, 1], obj.ener])[:, 1]
plt.plot(obj.box[:, 1], obj.ener)
plt.plot(obj.box[:, 1], np.gradient(obj.ener, edge_order=2))

obj[0][0].P.shape
len(obj)
for i in range(len(obj)):
    for j in range(len(obj[i])):
        obj[i][j].popped = obj[i][0].popped
obj[0][5].popped = obj[0][0].popped
[obj[0][i].box[1] for i in range(9)]

obj[10][16].I, obj[10][16].J = np.nonzero(obj[10][16].A)
obj[10][16].III, obj[10][16].JJJ = np.nonzero(obj[10][16].A - obj[10][16].AA)
obj[8][32].show2()

last = len(obj[8]) - 1
obj[8][last].create_mdist()
max_val = np.amax(obj[8][last].D[obj[8][last].I, obj[8][last].J] - 1.)
max_val
for i in range(0, last+1, 4):
    obj[8][i].save2('d35_100_fix_' + str(i), max_val)

[obj[j][i].ener for i in range(32) for j in range(100)]
obj[10][0].save2('d20_10_0')
for i in range(0, 17, 2):
    obj[70][i].save2('d5_70_fix_' + str(i))
np.sort(obj[4][0].popped)
for i in range(len(obj[3][12].III)):
    print(obj[3][12].III[i], obj[3][12].JJJ[i])

obj[0][7].D[0, 16]-1.
np.amax(obj[0][7].D[obj[0][7].I, obj[0][7].J]-1.)

obj_np = np.array(obj)
runs, incrs = obj_np.shape
for i in range(runs):
    for j in range(1, incrs):
        obj_np[i, j].popped = obj_np[i, 0].popped
[obj_np[1][i].popped for i in range(17)]
for i in range(runs):
    for j in range(incrs):
        obj_np[i, j].III, obj_np[i, j].JJJ = np.nonzero(obj_np[i, j].A
                                                        - obj_np[i, j].AA)

obj_np[0, 1].III
np.nonzero(obj[0][0].A)

np.nonzero(obj[0][0].A - obj[0][0].AA)
obj[0][0].P[[1, 32], 1]

P, box = lattice.fill_box((32, 32))
mesh = lattice.create_mesh((32, 32))
A, AA = lattice.links_matrix((32, 32))
I, J = np.nonzero(A)
II, JJ = np.nonzero(AA)
III, JJJ = np.nonzero(A-AA)

upper = mesh[0, :]
lower = mesh[-1, :]
left = mesh[:, 0]
right = mesh[:, -1]
# upper = upper[upper != 0]
# lower = lower[lower != 0]
# left = left[left != 0]
# right = right[right != 0]
for i, j in zip(I, J):
    print(i, j)
    if i in lower-1:
        print('ok')
lower-1
upper-1

test_mesh = lattice.create_mesh((8, 8))
test_mesh
test_mesh[test_mesh == 9] = 0
test_mesh
test_mesh[test_mesh > 9] -= 1
test_mesh

for i, j in zip(obj[0][0].I, obj[0][0].J):
    # if i in upper-1 and j in lower-1:
    #     print('*')
    #     print('i= ', i)
    #     print('j= ', j)
    if i in lower-1 and j in upper-1:
        # print('#')
        print('i= ', i)
        print('j= ', j)

if box is not None:
    x_box, y_box = box[0], box[1]
aspect_r = (x_box+1) / (y_box+1)
fig = plt.figure(figsize=(7, 7/aspect_r))
ax = fig.add_subplot(111, aspect='equal')
if box is not None:
    ax.add_patch(patches.Rectangle(
                (0., 0.), x_box, y_box, fill=False, edgecolor='red', lw=2))
# cell
for i, j in zip(II, JJ):
    plt.plot(P[[i, j], 0], P[[i, j], 1], '-k', lw=1)
    # right
    plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1], '-k', lw=1)
    # left
    plt.plot(P[[i, j], 0]-x_box, P[[i, j], 1], '-k', lw=1)
    # up
    plt.plot(P[[i, j], 0], P[[i, j], 1]+y_box, '-k', lw=1)
    # down
    plt.plot(P[[i, j], 0], P[[i, j], 1]-y_box, '-k', lw=1)
    # rightup
    plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]+y_box, '-k', lw=1)
    # leftup
    plt.plot(P[[i, j], 0]-x_box, P[[i, j], 1]+y_box, '-k', lw=1)
    # rightdown
    plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]-y_box, '-k', lw=1)
    # leftdown
    plt.plot(P[[i, j], 0]-x_box, P[[i, j], 1]-y_box, '-k', lw=1)
# connect
for i, j in zip(III[3:], JJJ[3:]):
    if i in mesh[:, -1]-1 and j in mesh[:, 0]-1:
        # right
        plt.plot(P[[i, j], 0]+[0, x_box], P[[i, j], 1], '-k', lw=1)
        plt.plot(P[[i, j], 0]+[0, x_box], P[[i, j], 1]+y_box, '-k', lw=1)
        plt.plot(P[[i, j], 0]+[0, x_box], P[[i, j], 1]-y_box, '-k', lw=1)
        # left
        plt.plot(P[[i, j], 0]-[x_box, 0], P[[i, j], 1], '-k', lw=1)
        plt.plot(P[[i, j], 0]-[x_box, 0], P[[i, j], 1]+y_box, '-k', lw=1)
        plt.plot(P[[i, j], 0]-[x_box, 0], P[[i, j], 1]-y_box, '-k', lw=1)
    if j in mesh[:, -1]-1 and i in mesh[:, 0]-1:
        # right
        plt.plot(P[[i, j], 0]+[x_box, 0], P[[i, j], 1], '-k', lw=1)
        plt.plot(P[[i, j], 0]+[x_box, 0], P[[i, j], 1]+y_box, '-k', lw=1)
        plt.plot(P[[i, j], 0]+[x_box, 0], P[[i, j], 1]-y_box, '-k', lw=1)
        # left
        plt.plot(P[[i, j], 0]-[0, x_box], P[[i, j], 1], '-k', lw=1)
        plt.plot(P[[i, j], 0]-[0, x_box], P[[i, j], 1]+y_box, '-k', lw=1)
        plt.plot(P[[i, j], 0]-[0, x_box], P[[i, j], 1]-y_box, '-k', lw=1)
    if i in mesh[-1, :] and j in mesh[0, :]:
        # up
        plt.plot(P[[i, j], 0], P[[i, j], 1]+[y_box, 0], '-k', lw=1)
        plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]+[y_box, 0], '-k', lw=1)
        plt.plot(P[[i, j], 0]-x_box, P[[i, j], 1]+[y_box, 0], '-k', lw=1)
        # down
        plt.plot(P[[i, j], 0], P[[i, j], 1]-[0, y_box], '-k', lw=1)
        plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]-[0, y_box], '-k', lw=1)
        plt.plot(P[[i, j], 0]-x_box, P[[i, j], 1]-[0, y_box], '-k', lw=1)
for i, j in zip(III[:1], JJJ[:1]):
    plt.plot(P[[i, j], 0], P[[i, j], 1]-[0, y_box], '-k')
    plt.plot(P[[i, j], 0], P[[i, j], 1]-[0, y_box]+y_box, '-k')
    plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]-[0, y_box], '-k')
    plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]-[0, y_box]+y_box, '-k')
for i, j in zip(III[1:2], JJJ[1:2]):
    plt.plot(P[[i, j], 0]-[0, x_box], P[[i, j], 1]-[0, y_box], '-k')
    plt.plot(P[[i, j], 0]-[0, x_box], P[[i, j], 1]-[0, y_box]+y_box, '-k')
    plt.plot(P[[i, j], 0]-[0, x_box]+x_box, P[[i, j], 1]-[0, y_box], '-k')
    plt.plot(P[[i, j], 0]-[0, x_box]+x_box, P[[i, j], 1]-[0, y_box]+y_box,
             '-k')
for i, j in zip(III[2:3], JJJ[2:3]):
    plt.plot(P[[i, j], 0], P[[i, j], 1]-[0, y_box], '-k')
    plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]-[0, y_box], '-k')
    plt.plot(P[[i, j], 0], P[[i, j], 1]-[0, y_box]+y_box, '-k')
    plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]-[0, y_box]+y_box, '-k')
plt.xlim((-2, x_box + 2))
plt.ylim((-2, y_box + 2))
plt.show()
