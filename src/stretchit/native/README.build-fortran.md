Building the Fortran extension

Use `f2py` to compile `fast_energy.f90` into a Python-extension module named
`fenergy` and place it where it can be imported by the package. Example:

```sh
cd src/stretchit/native
python -m numpy.f2py -c fast_energy.f90 -m fenergy
# move compiled extension into package or install in site-packages
```

Alternatively, build in-place and ensure `PYTHONPATH=src` when running.
