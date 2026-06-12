#!/usr/bin/env python3
"""Top-level wrapper that runs the package-aware CLI module.

This wrapper ensures `src/` is on `sys.path` so `import stretchit` works
without requiring the user to set `PYTHONPATH` manually.
"""
import os
import sys
import runpy

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, 'src')
    if src not in sys.path:
        sys.path.insert(0, src)
    runpy.run_module('cli.stretch_it', run_name='__main__')
