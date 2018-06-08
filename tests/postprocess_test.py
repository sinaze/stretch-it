"""Post-process system arrays read in from pkl-files."""
import numpy as np
import pickle
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

test = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
test
test[2][0]

np.mean(test, axis=0)

with open('/net/storage/zendehroud/honey_big_highres/16x32_d5_100.pkl', 'rb') as input:
    d5 = pickle.load(input)

d5 = np.array(d5)
d5.shape
d5[1, 10].ener
dir(d5[0, 0])
d5[0, 0].__dict__
vars(d5[0, 0])
[vars(d5[0, i])['ener'] for i in range(17)]
mean = np.mean([[vars(d5[i, j])['box'] for j in range(17)]
                for i in range(100)], axis=0)
plt.plot(mean)

getattr(d5[0, 0], 'box')
callable(d5[0, 0].energy)
[f for f in dir(d5[0, 0]) if not callable(getattr(d5[0, 0], f))]
fields = ['ener', 'box']
pd.DataFrame([{fn: getattr(d5[0, i], fn) for fn in fields} for i in range(17)])
