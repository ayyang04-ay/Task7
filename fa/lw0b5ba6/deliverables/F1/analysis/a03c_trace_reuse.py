"""Strict test for re-used body-weight traces: two animals in DIFFERENT blocks (or different groups of one block)
whose traces share >=5 identical values on days 2-14 where the shared values are not just a carried-forward constant."""
from paths import TABLES, FIGS, OUT as OUTDIR, BUILD, PANDOC
import pandas as pd, numpy as np, itertools, psln_blocks as pb
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500); pd.set_option('display.max_colwidth', 90)
df = pb.tidy(); w = df[df.kind == 'weight'].copy()
w['col'] = w.cell.str.extract(r'!([A-Z]+)\d+')[0]; w['x'] = w.x.astype(float)
tr = {}
for (blk, g, col), t in w.groupby(['block', 'group', 'col'], sort=False):
    tr[(blk, g, col)] = {r.x: r.value for r in t.itertuples() if r.x > 0}
rows = []
for (ka, a), (kb, b) in itertools.combinations(tr.items(), 2):
    if ka[0] == kb[0] and ka[1] == kb[1]: continue
    common = sorted(set(a) & set(b))
    same = [x for x in common if abs(a[x] - b[x]) < 1e-9]
    if len(same) >= 5 and len(set(a[x] for x in same)) >= 4:
        rows.append(dict(block_a=ka[0], group_a=ka[1], col_a=ka[2], block_b=kb[0], group_b=kb[1], col_b=kb[2], shared_days=len(same), of_days=len(common),
                         a=[a[x] for x in common], b=[b[x] for x in common]))
R = pd.DataFrame(rows)
print(R.to_string())
print()
agg = R.groupby(['block_a', 'group_a', 'block_b', 'group_b']).agg(animals=('col_a', 'count'), shared_points=('shared_days', 'sum'), compared=('of_days', 'sum')).reset_index()
print(agg.to_string())
R.to_csv(TABLES + 'T3c_reused_weight_traces.csv', index=False); agg.to_csv(TABLES + 'T3d_reused_weight_traces_summary.csv', index=False)
# how often would two independent animals share a value on a given day?  empirical base rate within block type
import random
random.seed(1)
keys = list(tr)
hits = tot = 0
for _ in range(200000):
    ka, kb = random.sample(keys, 2)
    if ka[0] == kb[0]: continue
    common = set(tr[ka]) & set(tr[kb])
    for x in common:
        tot += 1; hits += abs(tr[ka][x] - tr[kb][x]) < 1e-9
print('empirical per-day coincidence rate between random animals of different blocks:', round(hits / tot, 4))
