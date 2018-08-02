#!/usr/bin/env python3
"""Fix missing values in old simulation files."""
import numpy as np
import pickle
import argparse
import os

parser = argparse.ArgumentParser(description='Fix missing values.')
parser.add_argument('path', help='Path to the pkl-file to be fixed.',
                    type=str)
args = parser.parse_args()

with open(args.path, 'rb') as inputs:
    obj = pickle.load(inputs)

obj = np.array(obj)
runs, incrs = obj.shape

# fix popped
for i in range(runs):
    for j in range(1, incrs):
        obj[i, j].popped = obj[i, 0].popped

# fix III, JJJ
for i in range(runs):
    for j in range(incrs):
        obj[i, j].III, obj[i, j].JJJ = np.nonzero(obj[i, j].A - obj[i, j].AA)

# save it
new_path = args.path[:-4] + '_fixed' + args.path[-4:]

if os.path.exists(new_path):
    ans = input('File exists, overwrite? ')
    if ans == 'y' or ans == 'yes':
        with open(new_path, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(obj, output, -1)
        print('Averaged pkl saved to ', new_path)
else:
    with open(new_path, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, -1)
    print('Averaged pkl saved to ', new_path)
