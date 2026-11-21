import pandas as pd, numpy as np, itertools
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 2000); pd.set_option('display.max_colwidth', 120)
Q = pd.read_csv('quant_long.csv'); S = pd.read_csv('surv_long.csv'); W = pd.read_csv('wt_long.csv')

# ---------- 1. QUANT: group vectors ----------
vecs = []
for (blk, an, t, g), d in Q.groupby(['block','analyte','time','group'], sort=False, dropna=False):
    d = d.sort_values('rep')
    vecs.append(dict(key=f"{blk} | {an} | t={t} | {g}", block=blk, vals=tuple(d.value.round(6)), cells=f"{d.cell.iloc[0]}:{d.cell.iloc[-1].split('!')[1]}"))
discrete_blocks = {'S03-C','S03-D','S03-G','S03-H'}  # dilution-series titers: repeats expected
print("=== QUANT: group vectors sharing >=2 identical values at the same replicate position (excluding discrete titer blocks) ===")
hits=[]
for a, b in itertools.combinations(vecs, 2):
    if a['block'] in discrete_blocks or b['block'] in discrete_blocks: continue
    n = min(len(a['vals']), len(b['vals']))
    same = sum(1 for i in range(n) if a['vals'][i] == b['vals'][i])
    # also set overlap irrespective of order
    setov = len(set(a['vals']) & set(b['vals']))
    if same >= 2 or setov >= 3:
        hits.append((same, setov, n, a['key'], a['cells'], b['key'], b['cells']))
H = pd.DataFrame(hits, columns=['same_pos','set_overlap','n','A','A_cells','B','B_cells']).sort_values(['same_pos','set_overlap'], ascending=False)
print(H.to_string())
H.to_csv('audit_dups_quant.csv', index=False)

# ---------- 2. WEIGHTS: per (block, group) matrix; compare all pairs of groups ----------
print("\n=== WEIGHTS: pairs of group matrices with many identical cells (days>0, same animal position & day) ===")
mats = {}
for (blk, g), d in W.groupby(['block','group'], sort=False):
    m = d.pivot(index='day', columns='animal', values='value')
    mats[(blk, g)] = m
hits=[]
for (ka, ma), (kb, mb) in itertools.combinations(mats.items(), 2):
    days = [x for x in ma.index if x in mb.index and x > 0]
    na = min(ma.shape[1], mb.shape[1])
    a = ma.loc[days].iloc[:, :na].values; b = mb.loc[days].iloc[:, :na].values
    both = ~np.isnan(a) & ~np.isnan(b)
    same = (a == b) & both
    if both.sum() == 0: continue
    # any-position overlap by row (same day): count values in row of A that appear in row of B
    rowset = 0
    for i in range(len(days)):
        ra = set(np.round(a[i][~np.isnan(a[i])], 4)); rb = set(np.round(b[i][~np.isnan(b[i])], 4))
        rowset += len(ra & rb)
    if same.sum() >= 5 or rowset >= 8:
        per_day = {int(d): int(same[i].sum()) for i, d in enumerate(days) if same[i].sum() > 0}
        hits.append((int(same.sum()), int(both.sum()), rowset, f"{ka[0]} {ka[1]}", f"{kb[0]} {kb[1]}", per_day))
HW = pd.DataFrame(hits, columns=['same_pos','n_compared','same_day_set_overlap','A','B','identical_by_day']).sort_values('same_pos', ascending=False)
print(HW.to_string())
HW.to_csv('audit_dups_weights.csv', index=False)

# ---------- 3. SURVIVAL: identical blocks / groups ----------
print("\n=== SURVIVAL: identical (day,event) multisets between groups in different blocks (non-trivial: at least one death) ===")
sg = {}
for (blk, g), d in S.groupby(['block','group'], sort=False):
    sg[(blk, g)] = tuple(sorted(zip(d.day.fillna(-1), d.event)))
hits=[]
for (ka, va), (kb, vb) in itertools.combinations(sg.items(), 2):
    if va == vb and sum(e for _, e in va) >= 1 and ka[0] != kb[0]:
        hits.append((f"{ka[0]} {ka[1]}", f"{kb[0]} {kb[1]}", [int(d) for d, e in va if e == 1], len(va)))
HS = pd.DataFrame(hits, columns=['A','B','death_days','n'])
print(HS.to_string())
HS.to_csv('audit_dups_surv.csv', index=False)
# whole-block identity
blocks = {}
for blk, d in S.groupby('block', sort=False):
    blocks[blk] = tuple((g, tuple(sorted(zip(x.day.fillna(-1), x.event)))) for g, x in d.groupby('group', sort=False))
for a, b in itertools.combinations(blocks, 2):
    if blocks[a] == blocks[b]: print("IDENTICAL SURVIVAL BLOCKS:", a, b)
