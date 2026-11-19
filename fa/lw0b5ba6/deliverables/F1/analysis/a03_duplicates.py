"""
Duplicate-value forensics (copy/paste re-use of numbers between groups or experiments).
 (1) identical ordered vectors (n>=3) in two different groups/blocks  (same block+group at a later day = LOCF, excluded)
 (2) per-animal trace agreement between different groups/blocks in series & weight blocks
 (3) identical time-to-event vectors in different experiments
"""
from paths import TABLES, FIGS, OUT as OUTDIR, BUILD, PANDOC
import pandas as pd, numpy as np, itertools, collections, psln_blocks as pb
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 3000); pd.set_option('display.max_colwidth', 160)
df = pb.tidy()
df['xs'] = df.x.map(lambda v: 'NA' if v is None or (isinstance(v, float) and v != v) else str(v))
df['col'] = df.cell.str.extract(r'!([A-Z]+)\d+')[0]

# ---------- (1)
vecs = []
for (blk, an, g, x), t in df[df.kind != 'surv'].groupby(['block', 'analyte', 'group', 'xs'], sort=False):
    t = t.sort_values('rep')
    vecs.append((blk, an, g, x, tuple(t.value.round(6)), f'{t.cell.iloc[0]}:{t.cell.iloc[-1].split("!")[1]}'))
trivial = lambda v: len(set(v)) == 1
seen = collections.defaultdict(list)
for v in vecs:
    if len(v[4]) >= 3 and not trivial(v[4]):
        seen[v[4]].append(v)
dups1 = []
for k, lst in seen.items():
    for a, b in itertools.combinations(lst, 2):
        if (a[0], a[2]) == (b[0], b[2]):
            continue    # same block & group at another timepoint -> carried-forward weights, handled elsewhere
        dups1.append(dict(block_a=a[0], group_a=a[2], x_a=a[3], cells_a=a[5], block_b=b[0], group_b=b[2], x_b=b[3], cells_b=b[5], n=len(k), values=list(k)))
d1 = pd.DataFrame(dups1)
print('=== (1) identical ordered vectors in different groups/blocks ===')
print(d1.to_string() if len(d1) else 'none')

# ---------- (2) per-animal traces
ser = df[df.kind.isin(['series', 'weight'])].copy()
traces = {}
for (blk, an, g, col), t in ser.groupby(['block', 'analyte', 'group', 'col'], sort=False):
    traces[(blk, an, g, col)] = {str(r.x): r.value for r in t.itertuples()}
rows = []
for (ka, a), (kb, b) in itertools.combinations(traces.items(), 2):
    common = [k for k in a if k in b and not (a[k] == 100 and b[k] == 100)]
    if len(common) < 3:
        continue
    same = sum(1 for k in common if abs(a[k] - b[k]) < 1e-9)
    if same >= 3 and same / len(common) >= 0.5:
        rows.append(dict(block_a=ka[0], group_a=ka[2], col_a=ka[3], block_b=kb[0], group_b=kb[2], col_b=kb[3],
                         timepoints_compared=len(common), identical=same,
                         a=[a[k] for k in common], b=[b[k] for k in common]))
d2 = pd.DataFrame(rows)
print('\n=== (2) individual-animal traces that coincide (>=3 identical points and >=50% of shared timepoints) ===')
if len(d2):
    agg = d2.groupby(['block_a', 'group_a', 'block_b', 'group_b']).agg(animals=('col_a', 'count'), identical_points=('identical', 'sum'),
                                                                      points_compared=('timepoints_compared', 'sum')).reset_index()
    print(agg.to_string())
    print(d2.to_string())
else:
    print('none')

# ---------- (3)
sv = {}
for (blk, g), t in df[df.kind == 'surv'].groupby(['block', 'group'], sort=False):
    sv[(blk, g)] = tuple(zip(t.value.fillna(-1), t.event))
rows = []
for (ka, a), (kb, b) in itertools.combinations(sv.items(), 2):
    if a == b and sum(e for _, e in a) >= 3:
        rows.append(dict(block_a=ka[0], group_a=ka[1], block_b=kb[0], group_b=kb[1], days=[d for d, _ in a], events=[e for _, e in a]))
d4 = pd.DataFrame(rows)
print('\n=== (3) identical time-to-event vectors (>=3 events) in different blocks/groups ===')
print(d4.to_string() if len(d4) else 'none')

(d1 if len(d1) else pd.DataFrame({'none': []})).to_csv(TABLES + 'T3_identical_vectors.csv', index=False)
(d4 if len(d4) else pd.DataFrame({'none': []})).to_csv(TABLES + 'T3e_identical_survival.csv', index=False)
