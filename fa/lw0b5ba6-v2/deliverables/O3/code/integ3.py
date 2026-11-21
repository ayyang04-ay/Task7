from load import *
import numpy as np, pandas as pd, itertools, re
# ---------- (a) aligned animal-vector comparison for all time-course blocks ----------
tc = DF[DF['day'].notna() & DF['animal_col'].notna()].copy()
tc['day'] = pd.to_numeric(tc['day'], errors='coerce')
vecs = {}
for (b,g,c), d in tc.groupby(['block','group','animal_col']):
    s = d.set_index('day')['value']
    s = s[s.index!=0]  # drop day 0 (=100 for BW; baseline for flow)
    vecs[(b,g,c)] = s
keys = list(vecs)
hits=[]
for i in range(len(keys)):
    for j in range(i+1,len(keys)):
        a, b = vecs[keys[i]], vecs[keys[j]]
        common = a.index.intersection(b.index)
        if len(common)==0: continue
        eq = [(d) for d in common if abs(a[d]-b[d])<1e-9]
        # exclude trivially frozen LOCF pairs? keep but report
        if len(eq)>=2:
            hits.append((keys[i],keys[j],len(eq),len(common),sorted(eq)))
hits = sorted(hits, key=lambda x:(-x[2]))
print("Animal-column pairs sharing >=2 identical non-baseline values at the same day:")
for h in hits:
    (b1,g1,c1),(b2,g2,c2),n,m,days = h
    print(f"  {b1}:{g1}[{c1}]  <->  {b2}:{g2}[{c2}]   identical on {n}/{m} days {days}")
