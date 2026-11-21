import itertools, numpy as np, pandas as pd
from blocks import *
vecs = {}
for k, df in B.items():
    if 'analyte' in df.columns:
        for (g,a), d in df.groupby(['group','analyte'], sort=False): vecs[(k, g, a)] = np.array(d['value'])
    else:
        for g, d in df.groupby('group', sort=False): vecs[(k, g, '')] = np.array(d['value'])
for k, df in T.items():
    tcol = [c for c in df.columns if c in ('day','time','dose_ug')][0]
    for (g,t), d in df.groupby(['group', tcol], sort=False): vecs[(k, g, str(t))] = np.array(d['value'])
keys=list(vecs); out=[]
for a,b in itertools.combinations(keys,2):
    va, vb = np.sort(vecs[a]), np.sort(vecs[b])
    if len(va)!=len(vb) or len(va)<4: continue
    if a[0]==b[0] and a[1]==b[1]: continue
    if np.all(va>0) and np.all(vb>0):
        rel = np.max(np.abs(va-vb)/np.maximum(va,vb))
        if rel < 0.04 and len(set(np.round(va,3)))>=4: out.append((a,b,round(rel,4), va.tolist(), vb.tolist()))
for o in out: print(o)
print(len(out))
# group-mean profile similarity between time-course blocks
for k1,k2 in itertools.combinations(['S11-A','S11-B','S11-D','S01-D','S01-E'],2):
    d1 = T[k1].groupby(['group','day'])['value'].mean(); d2 = T[k2].groupby(['group','day'])['value'].mean()
    idx = d1.index.intersection(d2.index)
    if len(idx)>5: print(k1,k2,'n cells',len(idx),'corr of cell means', round(np.corrcoef(d1[idx], d2[idx])[0,1],4), 'max abs diff', round(np.max(np.abs(d1[idx]-d2[idx])),2))
