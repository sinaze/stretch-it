"""Input/Output function definitions."""
import numpy as np
import pickle
import lattice
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1 import make_axes_locatable


def save_object(obj, filename):
    """Save object in file."""
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, -1)


def show_system(P, II, JJ, D, l, size=7, box=None):
    """Plot the current system."""
    if box is not None:
        x_box, y_box = box[0], box[1]
    aspect_r = (x_box+1) / (y_box+1)
    fig = plt.figure(figsize=(size, size/aspect_r))
    ax = fig.add_subplot(111, aspect='equal')
    if box is not None:
        ax.add_patch(patches.Rectangle(
                    (0., 0.), x_box, y_box, fill=False, edgecolor='red'))
    c_max = np.amax(D)/l - 1.
    norm = matplotlib.colors.Normalize(vmin=0., vmax=c_max)
    for i, j in zip(II, JJ):
        c = D[i, j] - l
        im = plt.plot(P[[i, j], 0], P[[i, j], 1], lw=1,
                      color=plt.cm.copper(c*c_max))
        plt.plot(P[[i, j], 0], P[[i, j], 1], '.k')
    # plt.colorbar(im, norm=norm)
    plt.xlim((-1, x_box + 1))
    plt.ylim((-1, y_box + 1))
    plt.show()


def show_system2(P, I, J, II, JJ, III, JJJ, D, l, popped, size=7, box=None):
    """Plot the current system."""
    if box is not None:
        x_box, y_box = box[0], box[1]
    aspect_r = (x_box+1) / (y_box+1)
    fig = plt.figure(figsize=(size, size/aspect_r))
    ax = fig.add_subplot(111, aspect='equal')
    if box is not None:
        ax.add_patch(patches.Rectangle(
                    (0., 0.), x_box, y_box, fill=False, edgecolor='k',
                    lw=3))
    c_max = np.amax(D[I, J] - 1.)
    if c_max < 1e-5:
        norm = matplotlib.colors.Normalize(vmin=0., vmax=0.01)
    else:
        norm = matplotlib.colors.Normalize(vmin=0., vmax=c_max)
    c_m = matplotlib.cm.cool
    s_m = matplotlib.cm.ScalarMappable(cmap=c_m, norm=norm)
    s_m.set_array([])
    # TODO remove hardcoding
    mesh = lattice.create_mesh((32, 32))
    for i in popped:
        mesh[mesh == i] = 0
        mesh[mesh > i] -= 1
    # cell
    for i, j in zip(II, JJ):
        c = D[i, j] - l
        plt.plot(P[[i, j], 0], P[[i, j], 1], '-k', lw=2,
                 color=s_m.to_rgba(c))
        # right
        plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1], '-k', lw=2,
                 color=s_m.to_rgba(c))
        # left
        plt.plot(P[[i, j], 0]-x_box, P[[i, j], 1], '-k', lw=2,
                 color=s_m.to_rgba(c))
        # up
        plt.plot(P[[i, j], 0], P[[i, j], 1]+y_box, '-k', lw=2,
                 color=s_m.to_rgba(c))
        # down
        plt.plot(P[[i, j], 0], P[[i, j], 1]-y_box, '-k', lw=2,
                 color=s_m.to_rgba(c))
        # rightup
        plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]+y_box, '-k', lw=2,
                 color=s_m.to_rgba(c))
        # leftup
        plt.plot(P[[i, j], 0]-x_box, P[[i, j], 1]+y_box, '-k', lw=2,
                 color=s_m.to_rgba(c))
        # rightdown
        plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]-y_box, '-k', lw=2,
                 color=s_m.to_rgba(c))
        # leftdown
        plt.plot(P[[i, j], 0]-x_box, P[[i, j], 1]-y_box, '-k', lw=2,
                 color=s_m.to_rgba(c))
    # connect
    for i, j in zip(III[:], JJJ[:]):
        c = D[i, j] - l
        if i in mesh[:, -1]-1 and j in mesh[:, 0]-1:
            # right
            plt.plot(P[[i, j], 0]+[0, x_box], P[[i, j], 1], '-k', lw=2,
                     color=s_m.to_rgba(c))
            plt.plot(P[[i, j], 0]+[0, x_box], P[[i, j], 1]+y_box, '-k', lw=2,
                     color=s_m.to_rgba(c))
            plt.plot(P[[i, j], 0]+[0, x_box], P[[i, j], 1]-y_box, '-k', lw=2,
                     color=s_m.to_rgba(c))
            # left
            plt.plot(P[[i, j], 0]-[x_box, 0], P[[i, j], 1], '-k', lw=2,
                     color=s_m.to_rgba(c))
            plt.plot(P[[i, j], 0]-[x_box, 0], P[[i, j], 1]+y_box, '-k', lw=2,
                     color=s_m.to_rgba(c))
            plt.plot(P[[i, j], 0]-[x_box, 0], P[[i, j], 1]-y_box, '-k', lw=2,
                     color=s_m.to_rgba(c))
    #     if j in mesh[:, -1]-1 and i in mesh[:, 0]-1:
    #         # right
    #         plt.plot(P[[i, j], 0]+[x_box, 0], P[[i, j], 1], '-k', lw=2,
    #                  color=s_m.to_rgba(c))
    #         plt.plot(P[[i, j], 0]+[x_box, 0], P[[i, j], 1]+y_box, '-k', lw=2,
    #                  color=s_m.to_rgba(c))
    #         plt.plot(P[[i, j], 0]+[x_box, 0], P[[i, j], 1]-y_box, '-k', lw=2,
    #                  color=s_m.to_rgba(c))
    #         # left
    #         plt.plot(P[[i, j], 0]-[0, x_box], P[[i, j], 1], '-k', lw=2,
    #                  color=s_m.to_rgba(c))
    #         plt.plot(P[[i, j], 0]-[0, x_box], P[[i, j], 1]+y_box, '-k', lw=2,
    #                  color=s_m.to_rgba(c))
    #         plt.plot(P[[i, j], 0]-[0, x_box], P[[i, j], 1]-y_box, '-k', lw=2,
    #                  color=s_m.to_rgba(c))
    #     if i in mesh[-1, :] and j in mesh[0, :]:
    #         # up
    #         plt.plot(P[[i, j], 0], P[[i, j], 1]+[y_box, 0], '-k', lw=2,
    #                  color=s_m.to_rgba(c))
    #         plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]+[y_box, 0], '-k', lw=2,
    #                  color=s_m.to_rgba(c))
    #         plt.plot(P[[i, j], 0]-x_box, P[[i, j], 1]+[y_box, 0], '-k', lw=2,
    #                  color=s_m.to_rgba(c))
    #         # down
    #         plt.plot(P[[i, j], 0], P[[i, j], 1]-[0, y_box], '-k', lw=2,
    #                  color=s_m.to_rgba(c))
    #         plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]-[0, y_box], '-k', lw=2,
    #                  color=s_m.to_rgba(c))
    #         plt.plot(P[[i, j], 0]-x_box, P[[i, j], 1]-[0, y_box], '-k', lw=2,
    #                  color=s_m.to_rgba(c))
    # for i, j in zip(III[:1], JJJ[:1]):
    #     c = D[i, j] - l
    #     plt.plot(P[[i, j], 0], P[[i, j], 1]-[0, y_box], '-k', lw=2,
    #              color=s_m.to_rgba(c))
    #     plt.plot(P[[i, j], 0], P[[i, j], 1]-[0, y_box]+y_box, '-k', lw=2,
    #              color=s_m.to_rgba(c))
    #     plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]-[0, y_box], '-k', lw=2,
    #              color=s_m.to_rgba(c))
    #     plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]-[0, y_box]+y_box, '-k', lw=2,
    #              color=s_m.to_rgba(c))
    # for i, j in zip(III[1:2], JJJ[1:2]):
    #     c = D[i, j] - l
    #     plt.plot(P[[i, j], 0]-[0, x_box], P[[i, j], 1]-[0, y_box], '-k', lw=2,
    #              color=s_m.to_rgba(c))
    #     plt.plot(P[[i, j], 0]-[0, x_box], P[[i, j], 1]-[0, y_box]+y_box, '-k',
    #              lw=2, color=s_m.to_rgba(c))
    #     plt.plot(P[[i, j], 0]-[0, x_box]+x_box, P[[i, j], 1]-[0, y_box], '-k',
    #              lw=2, color=s_m.to_rgba(c))
    #     plt.plot(P[[i, j], 0]-[0, x_box]+x_box, P[[i, j], 1]-[0, y_box]+y_box,
    #              '-k', lw=2, color=s_m.to_rgba(c))
    # for i, j in zip(III[2:3], JJJ[2:3]):
    #     c = D[i, j] - l
    #     plt.plot(P[[i, j], 0], P[[i, j], 1]-[0, y_box], '-k', lw=2,
    #              color=s_m.to_rgba(c))
    #     plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]-[0, y_box], '-k', lw=2,
    #              color=s_m.to_rgba(c))
    #     plt.plot(P[[i, j], 0], P[[i, j], 1]-[0, y_box]+y_box, '-k', lw=2,
    #              color=s_m.to_rgba(c))
    #     plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]-[0, y_box]+y_box, '-k', lw=2,
    #              color=s_m.to_rgba(c))
    plt.xlim((-2, x_box + 2))
    plt.ylim((-2, y_box + 2))
    divider = make_axes_locatable(ax)
    cax1 = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(s_m, cax=cax1)
    plt.show()


def save_system(name, P, II, JJ, D, l, size=7, box=None):
    """Plot the current system."""
    if box is not None:
        x_box, y_box = box[0], box[1]
    aspect_r = (x_box+1) / (y_box+1)
    fig = plt.figure(figsize=(size, size/aspect_r))
    ax = fig.add_subplot(111, aspect='equal')
    if box is not None:
        ax.add_patch(patches.Rectangle(
                    (0., 0.), x_box, y_box, fill=False, edgecolor='red'))
    for i, j in zip(II, JJ):
        c = D[i, j] - l
        plt.plot(P[[i, j], 0], P[[i, j], 1], lw=1, color=plt.cm.copper(c*5))
        plt.plot(P[[i, j], 0], P[[i, j], 1], '.k')
    plt.xlim((-1, x_box + 1))
    plt.ylim((-1, y_box + 1))
    plt.savefig(str(name) + '.png', dpi=300)
    plt.close()


def save_system2(name, P, I, J, II, JJ, III, JJJ, D, l, popped, size=7,
                 box=None, max=1.):
    """Plot the current system."""
    if box is not None:
        x_box, y_box = box[0], box[1]
    aspect_r = (x_box+1) / (y_box+1)
    fig = plt.figure(figsize=(size, size/aspect_r))
    ax = fig.add_subplot(111, aspect='equal')
    if box is not None:
        ax.add_patch(patches.Rectangle(
                    (0., 0.), x_box, y_box, fill=False, edgecolor='k',
                    lw=3))
    # c_max = np.amax(D[I, J] - 1.)
    # if c_max < 1e-5:
    #     norm = matplotlib.colors.Normalize(vmin=0., vmax=0.01)
    # else:
    norm = matplotlib.colors.Normalize(vmin=0., vmax=max)
    c_m = matplotlib.cm.cool
    s_m = matplotlib.cm.ScalarMappable(cmap=c_m, norm=norm)
    s_m.set_array([])
    # TODO remove hardcoding
    mesh = lattice.create_mesh((32, 32))
    for i in popped:
        mesh[mesh == i] = 0
        mesh[mesh > i] -= 1
    # cell
    for i, j in zip(II, JJ):
        c = D[i, j] - l
        plt.plot(P[[i, j], 0], P[[i, j], 1], '-k', lw=2,
                 color=s_m.to_rgba(c))
        # right
        plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1], '-k', lw=2,
                 color=s_m.to_rgba(c))
        # left
        plt.plot(P[[i, j], 0]-x_box, P[[i, j], 1], '-k', lw=2,
                 color=s_m.to_rgba(c))
        # up
        plt.plot(P[[i, j], 0], P[[i, j], 1]+y_box, '-k', lw=2,
                 color=s_m.to_rgba(c))
        # down
        plt.plot(P[[i, j], 0], P[[i, j], 1]-y_box, '-k', lw=2,
                 color=s_m.to_rgba(c))
        # rightup
        plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]+y_box, '-k', lw=2,
                 color=s_m.to_rgba(c))
        # leftup
        plt.plot(P[[i, j], 0]-x_box, P[[i, j], 1]+y_box, '-k', lw=2,
                 color=s_m.to_rgba(c))
        # rightdown
        plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]-y_box, '-k', lw=2,
                 color=s_m.to_rgba(c))
        # leftdown
        plt.plot(P[[i, j], 0]-x_box, P[[i, j], 1]-y_box, '-k', lw=2,
                 color=s_m.to_rgba(c))
    # connect
    for i, j in zip(III[3:], JJJ[3:]):
        c = D[i, j] - l
        if i in mesh[:, -1]-1 and j in mesh[:, 0]-1:
            # right
            plt.plot(P[[i, j], 0]+[0, x_box], P[[i, j], 1], '-k', lw=2,
                     color=s_m.to_rgba(c))
            plt.plot(P[[i, j], 0]+[0, x_box], P[[i, j], 1]+y_box, '-k', lw=2,
                     color=s_m.to_rgba(c))
            plt.plot(P[[i, j], 0]+[0, x_box], P[[i, j], 1]-y_box, '-k', lw=2,
                     color=s_m.to_rgba(c))
            # left
            plt.plot(P[[i, j], 0]-[x_box, 0], P[[i, j], 1], '-k', lw=2,
                     color=s_m.to_rgba(c))
            plt.plot(P[[i, j], 0]-[x_box, 0], P[[i, j], 1]+y_box, '-k', lw=2,
                     color=s_m.to_rgba(c))
            plt.plot(P[[i, j], 0]-[x_box, 0], P[[i, j], 1]-y_box, '-k', lw=2,
                     color=s_m.to_rgba(c))
        if j in mesh[:, -1]-1 and i in mesh[:, 0]-1:
            # right
            plt.plot(P[[i, j], 0]+[x_box, 0], P[[i, j], 1], '-k', lw=2,
                     color=s_m.to_rgba(c))
            plt.plot(P[[i, j], 0]+[x_box, 0], P[[i, j], 1]+y_box, '-k', lw=2,
                     color=s_m.to_rgba(c))
            plt.plot(P[[i, j], 0]+[x_box, 0], P[[i, j], 1]-y_box, '-k', lw=2,
                     color=s_m.to_rgba(c))
            # left
            plt.plot(P[[i, j], 0]-[0, x_box], P[[i, j], 1], '-k', lw=2,
                     color=s_m.to_rgba(c))
            plt.plot(P[[i, j], 0]-[0, x_box], P[[i, j], 1]+y_box, '-k', lw=2,
                     color=s_m.to_rgba(c))
            plt.plot(P[[i, j], 0]-[0, x_box], P[[i, j], 1]-y_box, '-k', lw=2,
                     color=s_m.to_rgba(c))
        if i in mesh[-1, :] and j in mesh[0, :]:
            # up
            plt.plot(P[[i, j], 0], P[[i, j], 1]+[y_box, 0], '-k', lw=2,
                     color=s_m.to_rgba(c))
            plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]+[y_box, 0], '-k', lw=2,
                     color=s_m.to_rgba(c))
            plt.plot(P[[i, j], 0]-x_box, P[[i, j], 1]+[y_box, 0], '-k', lw=2,
                     color=s_m.to_rgba(c))
            # down
            plt.plot(P[[i, j], 0], P[[i, j], 1]-[0, y_box], '-k', lw=2,
                     color=s_m.to_rgba(c))
            plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]-[0, y_box], '-k', lw=2,
                     color=s_m.to_rgba(c))
            plt.plot(P[[i, j], 0]-x_box, P[[i, j], 1]-[0, y_box], '-k', lw=2,
                     color=s_m.to_rgba(c))
    for i, j in zip(III[:1], JJJ[:1]):
        c = D[i, j] - l
        plt.plot(P[[i, j], 0], P[[i, j], 1]-[0, y_box], '-k', lw=2,
                 color=s_m.to_rgba(c))
        plt.plot(P[[i, j], 0], P[[i, j], 1]-[0, y_box]+y_box, '-k', lw=2,
                 color=s_m.to_rgba(c))
        plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]-[0, y_box], '-k', lw=2,
                 color=s_m.to_rgba(c))
        plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]-[0, y_box]+y_box, '-k', lw=2,
                 color=s_m.to_rgba(c))
    for i, j in zip(III[1:2], JJJ[1:2]):
        c = D[i, j] - l
        plt.plot(P[[i, j], 0]-[0, x_box], P[[i, j], 1]-[0, y_box], '-k', lw=2,
                 color=s_m.to_rgba(c))
        plt.plot(P[[i, j], 0]-[0, x_box], P[[i, j], 1]-[0, y_box]+y_box, '-k',
                 lw=2, color=s_m.to_rgba(c))
        plt.plot(P[[i, j], 0]-[0, x_box]+x_box, P[[i, j], 1]-[0, y_box], '-k',
                 lw=2, color=s_m.to_rgba(c))
        plt.plot(P[[i, j], 0]-[0, x_box]+x_box, P[[i, j], 1]-[0, y_box]+y_box,
                 '-k', lw=2, color=s_m.to_rgba(c))
    for i, j in zip(III[2:3], JJJ[2:3]):
        c = D[i, j] - l
        plt.plot(P[[i, j], 0], P[[i, j], 1]-[0, y_box], '-k', lw=2,
                 color=s_m.to_rgba(c))
        plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]-[0, y_box], '-k', lw=2,
                 color=s_m.to_rgba(c))
        plt.plot(P[[i, j], 0], P[[i, j], 1]-[0, y_box]+y_box, '-k', lw=2,
                 color=s_m.to_rgba(c))
        plt.plot(P[[i, j], 0]+x_box, P[[i, j], 1]-[0, y_box]+y_box, '-k', lw=2,
                 color=s_m.to_rgba(c))
    plt.xlim((-2, x_box + 2))
    plt.ylim((-2, y_box + 2))
    divider = make_axes_locatable(ax)
    cax1 = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(s_m, cax=cax1)
    plt.savefig(str(name) + '.png', dpi=300)
    plt.close()
