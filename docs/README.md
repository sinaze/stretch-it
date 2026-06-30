# Stretch-it — Overview & Usage

This repository simulates energies of randomly diluted elastic honeycomb networks.

**Quick summary**
- Purpose: simulate stretching cycles and compute minimal energy configurations for diluted honeycomb lattices.
- Languages: Python 3 (+ a Fortran95 source compiled via `f2py`).

**Primary scripts**
- [stretch_it.py](stretch_it.py) — main runner: run full stretching simulation and optimization for one set of parameters (CLI).
- [fixit.py](fixit.py) — helper script for fixing or preparing systems (uses CLI).
- [postprocess.py](postprocess.py) — analyzes and post-processes saved results.
- [tools.py](tools.py), [system.py](system.py), [lattice.py](lattice.py), [inout.py](inout.py), [energy.py](energy.py) — library modules used by the main scripts.

**Basic requirements**
- Python 3.9 required to compile the Fortran backend (build with `f2py`).
- Fortran95 compiler (e.g., `gfortran`) and `f2py` to build the Fortran extension.
- Python packages listed in `docs/dependencies.md`.

**Quick install & build**
1. Install Python packages:

```sh
python -m pip install --user numpy scipy matplotlib joblib
```

2. Build the Fortran extension (from repo root):

```sh
python -m numpy.f2py -c fast_energy.f90 -m fenergy
```

3. Make the main script executable and run:

```sh
chmod +x stretch_it.py
./stretch_it.py NX NY -d DILUTE -dn SAMPLES -k INCR -it ITER -f output.pkl
```

Replace the CLI placeholders with integers and strings as described by the script help: run `./stretch_it.py --help` for complete options.

**Example**
Run a small test (10x10 lattice, remove 0 sites, 1 sample, increment 10, 5 iterations):

```sh
./stretch_it.py 10 10 -d 0 -dn 1 -k 10 -it 5 -f test_out.pkl
```

**Notes & tips**
- If `f2py` can't find a compiler, install `gfortran` (Homebrew on macOS: `brew install gcc`).
- The Fortran module is imported as `fenergy` by the Python code — ensure the compiled module is placed on `PYTHONPATH` or in the repo root.
- Use `-nt` to control parallel workers via `joblib`.

For dependency details, see `docs/dependencies.md`.
