"""Light-weight access to the tidy export (no openpyxl needed)."""
import os
import pandas as pd, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
_T = None
def T():
    global _T
    if _T is None:
        _T = pd.read_csv(os.path.join(HERE, '..', 'data_tidy', 'psln_tidy_all_blocks.csv'))
    return _T
def get(block):
    t = T(); d = t[t.block == block].copy()
    if d.empty:
        raise KeyError(block)
    return d
def vec(block, group, x=None):
    d = get(block); d = d[d.group == group]
    if x is not None:
        d = d[d.x == x]
    return d.sort_values('rep')['value'].values
def groups(block):
    return list(pd.unique(get(block)['group']))
