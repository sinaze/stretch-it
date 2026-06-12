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

## New layout (non-breaking)

The repository has been reorganized into a package while keeping the original
top-level runnable scripts as thin wrappers. Relevant paths (workspace-relative):

- `src/stretchit/` — package modules (`system.py`, `lattice.py`, `energy.py`, `inout.py`, `periodicarray.py`, `tools.py`, `fenergy.py` shim)
- `src/stretchit/native/fast_energy.f90` — Fortran source
- `cli/` — package-aware CLI scripts (`stretch_it.py`, `stretch_it_eps.py`, `postprocess.py`, `fixit.py`)
- root-level wrappers: `stretch_it.py`, `stretch_it_eps.py`, `postprocess.py`, `fixit.py` (call into `cli/`)

Old imports like `import system` and `import lattice` are preserved via compatibility
shims at the repository root to avoid breaking existing workflows and pickles.

## Running (recommended)

Use the project's `stretch` conda environment (example). Activate it, then run the
top-level wrappers (they invoke the package-aware CLI scripts):

```sh
CONDA_BASE=$(conda info --base)
source "$CONDA_BASE/etc/profile.d/conda.sh"
conda activate stretch
./stretch_it.py --help
```

You can also run with the package on `PYTHONPATH`:

```sh
PYTHONPATH=src python -c "import stretchit; from stretchit import system; print(system.LatticeSystem)"
```

## Fortran / f2py build

The Fortran backend is in `src/stretchit/native/fast_energy.f90`. Build an extension named
`fenergy` (so the package shim can find it) using `numpy.f2py`, for example:

```sh
cd src/stretchit/native
python -m numpy.f2py -c fast_energy.f90 -m fenergy
# this creates a compiled module that should be importable by the package
```

See `src/stretchit/native/README.build-fortran.md` for notes.

## Pickles and compatibility

`LatticeSystem` remains importable at `system.LatticeSystem` via a compatibility shim,
so existing saved `.pkl` files should unpickle without change. New code should prefer
`from stretchit import system` or `import stretchit`.
