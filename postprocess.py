#!/usr/bin/env python3
"""Post-process system arrays read in from pkl-files."""
import numpy as np
#!/usr/bin/env python3
"""Wrapper to run cli.postprocess module.

Adds `src/` to `sys.path` so imports work without `PYTHONPATH`.
"""
import os
import sys
import runpy

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, 'src')
    if src not in sys.path:
        sys.path.insert(0, src)
    runpy.run_module('cli.postprocess', run_name='__main__')
                    type=str)
