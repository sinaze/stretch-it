"""Compatibility shim re-exporting package `stretchit.system`.

This module preserves the old import path `import system` so existing
pickles and external scripts continue to work while the package layout
is adopted. Prefer importing from `stretchit.system` in new code.
"""
from stretchit.system import *  # noqa: F401,F403

