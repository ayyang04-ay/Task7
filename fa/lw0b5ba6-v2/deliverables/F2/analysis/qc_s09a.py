import numpy as np, pandas as pd
from blocks import *
for side, ref in [('S09-A_left','S01-A_16h'),('S09-A_left','S01-A_72h'),('S09-A_right','S01-A_16h'),('S09-A_right','S01-A_72h')]:
    a = B[side]; a = a[a.analyte=='Ifnb1']
    r = B[ref]
    print(f'\n--- {side} Ifnb1 (10^value) vs {ref} (linear)')
    tot=0; hit=0
    for g in a.group.unique():
        g2 = {'PBS':'Sham','PSLN-212(y)':'PSLN-212(Y)'}.get(g,g)
        lin = np.round(10**a[a.group==g]['value'].values, 2)
        refv = r[r.group==g2]['value'].values
        m = [any(abs(x-y)<0.011 for y in refv) for x in lin]
        tot+=len(m); hit+=sum(m)
        print(f'  {g:14s} 10^x = {lin}   {ref}[{g2}] = {refv}   matched {sum(m)}/{len(m)}')
    print('  total matched', hit, '/', tot)
