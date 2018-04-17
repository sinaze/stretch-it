"""Plot for testing."""
import pickle
# %matplotlib inline

with open('test.pkl', 'rb') as input:
    test = pickle.load(input)

[test[0][i].ener for i in range(8)]

for i in range(8):
    test[0][i].show()
