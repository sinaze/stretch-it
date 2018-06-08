"""Post-process system arrays read in from pkl-files."""
import numpy as np
import pickle
import argparse
import os

parser = argparse.ArgumentParser(description='Average over realizations.')
parser.add_argument('path', help='Path to the pkl-file to be averaged.',
                    type=str)
args = parser.parse_args()

with open(args.path, 'rb') as inputs:
    obj = pickle.load(inputs)

obj = np.array(obj)
dil = len(obj[0, 0].popped)
tot = int(obj[0, 0].dim[0]/2 * obj[0, 0].dim[1])
phi = dil/tot

mean_en = np.mean([[vars(obj[i, j])['ener'] for j in range(obj.shape[1])]
                   for i in range(obj.shape[0])], axis=0)
mean_box = np.mean([[vars(obj[i, j])['box'] for j in range(obj.shape[1])]
                    for i in range(obj.shape[0])], axis=0)


class ReducedSystem:
    """Reduced system only containing box size and averaged energies."""

    def __init__(self, mean_box, mean_en, dil, tot):
        """Initialize."""
        self.ener = mean_en
        self.box = mean_box
        self.dil = dil
        self.tot = tot
        self.phi = dil/tot


obj_a = ReducedSystem(mean_box, mean_en, dil, tot)
new_path = args.path[:-4] + '_a' + args.path[-4:]

if os.path.exists(new_path):
    ans = input('File exists, overwrite? ')
    if ans == 'y' or ans == 'yes':
        with open(new_path, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(obj_a, output, -1)
        print('Averaged pkl saved to ', new_path)
else:
    with open(new_path, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj_a, output, -1)
    print('Averaged pkl saved to ', new_path)
