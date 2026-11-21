import itertools, numpy as np, pandas as pd
from blocks import *
vec={}
for k, df in S.items():
    for g, d in df.groupby('group', sort=False):
        vec[(k,g)] = tuple(sorted(zip(d['day'].fillna(-1), d['event'])))
print('Identical time-to-event columns containing at least 3 deaths:')
for a,b in itertools.combinations(vec,2):
    if vec[a]==vec[b] and sum(e for _,e in vec[a])>=3:
        print(' ', a, '==', b, [int(d) for d,e in vec[a] if e==1], 'survivors', sum(1 for d,e in vec[a] if e==0))
print()
for k, df in S.items():
    print(k)
    for g, d in df.groupby('group', sort=False):
        dd = sorted(d[d.event==1]['day'].tolist()); cc = sorted(d[d.event==0]['day'].tolist())
        print(f'   {g:22s} n={len(d)} deaths={len(dd)} at {[int(x) if x==x else None for x in dd]}  censored={len(cc)} at {sorted(set([int(x) if x==x else None for x in cc], ), key=lambda x: (x is None, x))}')
