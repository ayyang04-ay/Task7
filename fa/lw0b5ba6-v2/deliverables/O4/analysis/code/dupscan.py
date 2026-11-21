import pandas as pd, numpy as np, itertools
vals = pd.read_csv('values.csv'); surv = pd.read_csv('survival.csv'); bw = pd.read_csv('bw.csv')

# 1) survival: identical (day,event) vectors per group across blocks
print('=== Survival blocks: identical group vectors across different blocks ===')
sig = {}
for (b,g),d in surv.groupby(['block','group'], sort=False):
    key = tuple(zip(d.day.fillna(-1), d.event))
    sig.setdefault(key, []).append(f'{b}:{g}')
for k,v in sig.items():
    blocks = set(x.split(':')[0] for x in v)
    if len(blocks)>1 and any(e==1 for _,e in k):
        print('  ', v, k)
# whole-block identity
blk = {}
for b,d in surv.groupby('block', sort=False):
    blk.setdefault(tuple(zip(d.group, d.day.fillna(-1), d.event)), []).append(b)
for k,v in blk.items():
    if len(v)>1: print('  WHOLE BLOCK IDENTICAL:', v)

# 2) continuous: matching values between distinct blocks (same value, >=3 sig digits), count per block pair
print('\n=== Continuous blocks: shared exact values between different blocks (value with >=3 significant digits) ===')
v = vals.copy()
v['s'] = v.value.map(lambda x: f'{x:.6g}')
def sigdig(s):
    s=s.replace('-','').replace('.','').lstrip('0'); return len(s)
v = v[v.s.map(sigdig)>=3]
pairs = {}
for s,d in v.groupby('s'):
    bl = d.block.unique()
    if len(bl)>1:
        for a,b in itertools.combinations(sorted(bl),2):
            pairs.setdefault((a,b), []).append((s, list(d[d.block.isin([a,b])].cell)))
for (a,b),lst in sorted(pairs.items(), key=lambda x:-len(x[1])):
    if len(lst)>=3:
        print(f'  {a} vs {b}: {len(lst)} shared values')
        for s,c in lst[:40]: print('      ', s, c)
