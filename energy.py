"""Compatibility shim for `stretchit.energy`.

Preserves top-level `import energy` by re-exporting package contents.
"""
from stretchit.energy import *  # noqa: F401,F403
