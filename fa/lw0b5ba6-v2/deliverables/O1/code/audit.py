import pandas as pd, numpy as np, itertools, re
V = pd.read_csv('/tmp/work/tidy/values.csv'); T = pd.read_csv('/tmp/work/tidy/tte.csv'); B = pd.read_csv('/tmp/work/tidy/bw.csv')
out = []
def log(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s)

log('=== 1. Exact duplicate vectors across/within blocks (per group x analyte x time, >=3 values) ===')
vec = {}
for (b, a, g, t), d in V.groupby(['block', 'analyte', 'group', 'time'], dropna=False):
    vec[(b, a, g, t)] = d.sort_values('animal')['value'].round(4).tolist()
keys = list(vec)
for k1, k2 in itertools.combinations(keys, 2):
    v1, v2 = vec[k1], vec[k2]
    if len(v1) >= 3 and v1 == v2:
        log('IDENTICAL:', k1, '==', k2, v1)
log('\n=== 1b. Partial overlap: >=3 shared identical values at same animal positions (excluding 100/0) ===')
for k1, k2 in itertools.combinations(keys, 2):
    v1, v2 = vec[k1], vec[k2]
    m = min(len(v1), len(v2))
    same = [i for i in range(m) if v1[i] == v2[i] and v1[i] not in (0, 100)]
    if len(same) >= 2 and v1 != v2:
        log('PARTIAL:', k1, 'vs', k2, 'shared positions', same, [v1[i] for i in same])

log('\n=== 1c. Shared value multiset (order-free) >=3 values, across different blocks ===')
for k1, k2 in itertools.combinations(keys, 2):
    if k1[0] == k2[0]: continue
    s1, s2 = set(vec[k1]) - {0, 100}, set(vec[k2]) - {0, 100}
    inter = s1 & s2
    if len(inter) >= 3:
        log('SHARED-VALUES:', k1, 'vs', k2, sorted(inter))

log('\n=== 2. TTE duplicate experiments ===')
tt = {}
for (b, g), d in T.groupby(['block', 'group']):
    tt[(b, g)] = sorted(zip(d['time'].fillna(-1), d['event']))
blocks = T.block.unique()
for b1, b2 in itertools.combinations(blocks, 2):
    g1 = {g: v for (b, g), v in tt.items() if b == b1}; g2 = {g: v for (b, g), v in tt.items() if b == b2}
    common = set(g1) & set(g2)
    if common and all(g1[g] == g2[g] for g in common):
        log(f'IDENTICAL TTE blocks: {b1} == {b2} for all common groups {sorted(common)}')

log('\n=== 3. Missing time values in TTE ===')
log(T[T.time.isna()].to_string())

log('\n=== 4. Body-weight: identical rows between groups within a block (same day) ===')
for (b, day), d in B.groupby(['block', 'day']):
    if day == 0: continue
    gv = {g: dd.sort_values('animal')['value'].round(3).tolist() for g, dd in d.groupby('group')}
    for g1, g2 in itertools.combinations(gv, 2):
        a, c = gv[g1], gv[g2]
        m = min(len(a), len(c))
        same = sum(1 for i in range(m) if a[i] == c[i])
        if same >= 4:
            log(f'{b} day {day}: {g1} vs {g2}: {same}/{m} identical values')

log('\n=== 4b. Body-weight: identical values across different blocks (same group/day/animal, >=4 animals) ===')
bw_vec = {(b, g, day): d.sort_values('animal')['value'].round(3).tolist() for (b, g, day), d in B.groupby(['block', 'group', 'day']) if day > 0}
bk = list(bw_vec)
for k1, k2 in itertools.combinations(bk, 2):
    if k1[0] == k2[0]: continue
    a, c = bw_vec[k1], bw_vec[k2]
    m = min(len(a), len(c))
    same = sum(1 for i in range(m) if a[i] == c[i])
    if same >= 4:
        log(f'{k1} vs {k2}: {same}/{m} identical')

log('\n=== 5. Range checks ===')
pct = V[V.analyte.str.contains('%|DC|cells|CD8|monocytes|macrophages|Tfh ICOS|Tfr|Treg|GC|tetramer|OT-I|SRB|DiD|IgG\\+|neutrophils|NK', regex=True)]
log('values > 100 in percent-type blocks:', pct[pct.value > 100][['block', 'group', 'value', 'cell']].to_string())
log('negative values (non-log blocks):', V[(V.value < 0) & ~V.block.str.startswith('S09-A')][['block', 'value', 'cell']].to_string())
for blk in ['S03-C', 'S03-G', 'S03-D', 'S03-H']:
    d = V[V.block == blk]
    off = d[~d.value.isin([0] + [10 * 2 ** i for i in range(0, 15)] + [15 * 2 ** i for i in range(0, 15)])]
    log(blk, 'values not on a 2-fold dilution grid:', off[['group', 'value', 'cell']].to_string() if len(off) else 'none')
    log(blk, 'zeros (below LOD 1:10):', d[d.value == 0][['group', 'cell']].values.tolist())

open('/tmp/work/audit_raw.txt', 'w').write('\n'.join(out))
