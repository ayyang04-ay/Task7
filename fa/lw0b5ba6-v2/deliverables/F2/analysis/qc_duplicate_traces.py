import itertools, numpy as np, pandas as pd
from blocks import *
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500); pd.set_option('display.max_colwidth', 120)
traj = {}
for k, df in list(W.items()):
    for (g, rep), d in df.groupby(['group','rep'], sort=False):
        d = d[d['day']!=0]
        traj[(k,g,rep)] = dict(zip(d['day'], d['value'].round(4)))
for k, df in list(T.items()):
    tcol = [c for c in df.columns if c in ('day','time','dose_ug')][0]
    for (g, rep), d in df.groupby(['group','rep'], sort=False):
        traj[(k,g,rep)] = dict(zip(d[tcol].astype(str), d['value'].round(4)))
keys = list(traj)
rows=[]
for a,b in itertools.combinations(keys,2):
    ta, tb = traj[a], traj[b]
    common = set(ta) & set(tb)
    eqt = [t for t in common if ta[t]==tb[t]]
    if len(set(ta[t] for t in eqt)) >= 3:
        rows.append((a[0],a[1],a[2],b[0],b[1],b[2],len(common),len(eqt), sorted(eqt, key=lambda x: float(str(x).replace('h',''))), [ta[t] for t in sorted(eqt, key=lambda x: float(str(x).replace('h','')))]))
r = pd.DataFrame(rows, columns=['blockA','groupA','repA','blockB','groupB','repB','n_common','n_equal','equal_at','values'])
print(r.to_string())
r.to_csv('qc_duplicate_trajectories_nonflat.csv', index=False)
