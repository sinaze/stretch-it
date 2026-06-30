# Dependencies

This project requires a mix of Python packages and a Fortran compiler to build the numerical backend.

Note: the Fortran backend (the `fenergy` module built with `f2py`) must be compiled using Python 3.9. While the Python scripts may run on other Python 3.x interpreters, building the Fortran extension requires Python 3.9.

## Python packages
The codebase imports the following third-party Python packages (to be installed via `pip`):

- numpy
- scipy
- matplotlib
- joblib

Standard-library modules used: `pickle`, `argparse`, `os`, `sys`.

Install the packages with (use the Python 3.9 interpreter when preparing the Fortran build):

```sh
python3.9 -m pip install --user numpy scipy matplotlib joblib
```

## Fortran / compiled extension
The Fortran source file `fast_energy.f90` is built into a Python extension module (imported in Python as `fenergy`) using `numpy.f2py`.

Build example (from project root — run with the Python 3.9 interpreter):

```sh
python3.9 -m numpy.f2py -c fast_energy.f90 -m fenergy
```

Requirements for the above:
- A Fortran compiler (e.g., `gfortran`).
- `numpy` installed before building with `f2py`.

After building, the produced `fenergy` extension (shared object) should be placed in the repository root or somewhere on `PYTHONPATH` so that `import fenergy` succeeds.

## Platform notes (macOS)
- Install a Fortran compiler with Homebrew: `brew install gcc`.
Use a Python 3.9 virtual environment if you prefer isolation:

```sh
python3.9 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install numpy scipy matplotlib joblib
```
