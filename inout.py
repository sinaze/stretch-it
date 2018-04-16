"""Input/Output function definitions."""
import numpy as np
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches


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
    for i, j in zip(II, JJ):
        c = D[i, j] - l
        plt.plot(P[[i, j], 0], P[[i, j], 1], lw=1,
                 color=plt.cm.copper(c*c_max))
        plt.plot(P[[i, j], 0], P[[i, j], 1], '.k')
    plt.xlim((-1, x_box + 1))
    plt.ylim((-1, y_box + 1))
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
