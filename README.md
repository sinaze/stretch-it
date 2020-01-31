# Stretch it!

A program to simulate energies of randomly diluted elastic networks with a honeycomb structure.

# Installation

You will need [Python3](https://www.python.org) to run the script and a Fortran95 compiler to build the underlying libraries using [f2py](https://docs.scipy.org/doc/numpy/f2py/). On Linux systems, you can use the precompiled binary, which we include. Python libraries needed are [NumPy](https://numpy.org/), [SciPy](https://www.scipy.org/), [Matplotlib](https://matplotlib.org/) for plotting, and [joblib](https://joblib.readthedocs.io/en/latest/index.html) for parallelization.

At this stage, no install script is available. To be able to run the program, simply clone the repository and make the main script executable:
```sh
    git clone https://gitlabph.physik.fu-berlin.de/zendehroud/stretch-it.git
    cd stretch-it
    chmod +x stretch_it.py
```

# Usage

To run the program, just invoke it from the command line. Parameters are explained in the help function
```sh
    ./stretch_it.py --help
```
