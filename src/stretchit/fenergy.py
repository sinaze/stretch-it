"""Shim for the Fortran `fenergy` extension.

This module tries to import an extension built from `fast_energy.f90` and
exposes the expected functions. If the compiled extension is not present,
importing functions will raise a clear ImportError.
"""
try:
    from .native import fenergy as _fenergy
except Exception:
    try:
        import fenergy as _fenergy
    except Exception:
        _fenergy = None

def _missing():
    raise ImportError("fenergy extension not built; build with f2py and place the module in src/stretchit/native or install it as 'fenergy'. See src/stretchit/native/README.build-fortran.md")

def dist_mat(Pos, box):
    if _fenergy is None:
        _missing()
    return _fenergy.dist_mat(Pos, box)

def mindist(a, b, Pos, box, norm=True):
    if _fenergy is None:
        _missing()
    return _fenergy.mindist(a, b, Pos, box, norm)

def gradient(A, D, P, box, l, grad):
    if _fenergy is None:
        _missing()
    return _fenergy.gradient(A, D, P, box, l, grad)
