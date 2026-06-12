"""Compatibility shim for `stretchit.tools`.

Preserves top-level `import tools` by re-exporting package contents.
"""
from stretchit.tools import *  # noqa: F401,F403
