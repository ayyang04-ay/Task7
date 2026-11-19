import pandas as pd, numpy as np, itertools, collections
cont = pd.read_csv('tidy_continuous.csv')
bw = pd.read_csv('tidy_bodyweight.csv')
bw = bw[bw.value.notna() & (bw.day != 0)]  # day-0 weights are all 100 by definition

# ---------- 1. Shared exact values between (block,group) units in continuous data
cont['unit'] = cont.block + ' | ' + cont.group.astype(str) + (' | ' + cont.level.astype(str)).where(cont.level.notna() & (cont.level.astype(str) != 'nan'), '')
units = {u: d for u, d in cont.groupby('unit')}
pairs = []
keys = list(units)
for a, b in itertools.combinations(keys, 2):
    da, db = units[a], units[b]
    if da.block.iloc[0].split('_')[0] == db.block.iloc[0].split('_')[0] and da.block.iloc[0] == db.block.iloc[0]:
        pass
    va = collections.Counter(np.round(da.value, 4)); vb = collections.Counter(np.round(db.value, 4))
    shared = sum((va & vb).values())
    if shared >= 2:
        # ignore trivially common integers (titres like 10, 20, 40...) and values of 0/100
        sv = list((va & vb).elements())
        nontrivial = [v for v in sv if not (float(v).is_integer() and v in (0, 10, 20, 30, 40, 60, 80, 100, 120, 160, 240, 320, 480, 640, 960, 1920, 3840, 7680, 15360))]
        if len(nontrivial) >= 2:
            pairs.append(dict(unit_a=a, unit_b=b, n_a=len(da), n_b=len(db), shared=len(nontrivial), shared_values=sorted(nontrivial)))
P = pd.DataFrame(pairs).sort_values('shared', ascending=False)
pd.set_option('display.width', 300); pd.set_option('display.max_colwidth', 90); pd.set_option('display.max_rows', 500)
print('=== continuous (block|group) units sharing >=2 non-trivial exact values')
print(P.to_string())
P.to_csv('dup_shared_values_continuous.csv', index=False)

# ---------- 2. Body weights: identical rows across groups (same day, same vector)
print('\n=== identical per-day vectors between groups within BW blocks')
for (b, d), x in bw.groupby(['block', 'day']):
    vecs = {g: tuple(np.round(y.sort_values('col').value, 4)) for g, y in x.groupby('group')}
    for g1, g2 in itertools.combinations(vecs, 2):
        if vecs[g1] == vecs[g2]:
            print(b, 'day', d, g1, '==', g2, vecs[g1])

# ---------- 3. High-precision fractional parts recycled across cells
print('\n=== recycled high-precision fractional parts (>=5 decimals) in BW data')
bw['frac'] = bw.value.apply(lambda v: round(v - np.floor(v), 6))
bw['ndec'] = bw.value.apply(lambda v: len(repr(float(v)).split('.')[1]) if '.' in repr(float(v)) else 0)
hp = bw[bw.ndec >= 5]
grp = hp.groupby('frac')
rows = []
for f, x in grp:
    if len(x) >= 2:
        rows.append(dict(frac=f, n=len(x), cells='; '.join(f"{c}={v}" for c, v in zip(x.cell, x.value))))
R = pd.DataFrame(rows).sort_values('n', ascending=False)
print(R.to_string())
R.to_csv('dup_recycled_fractions_bw.csv', index=False)
print('\nnumber of high-precision BW cells:', len(hp), ' distinct fractional parts:', hp.frac.nunique())
