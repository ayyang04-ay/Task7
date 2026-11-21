"""QC 3: identical or near-identical numeric vectors in blocks that should be independent."""
import numpy as np, pandas as pd, itertools
import psln_blocks as P
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 80); pd.set_option('display.max_rows', 500)

# ---------- (a) time-to-event blocks: whole-block and per-group identity
S = {bid: P.load(bid) for bid, b in P.BLOCKS.items() if b['kind'] == 'surv'}
def sig(df, g):
    s = df[df.group == g]
    return tuple(sorted(zip(s.time.fillna(-1).astype(int), s.event)))
print('=== identical group-level time-to-event vectors with >=1 event (different blocks)')
seen = {}
for bid, df in S.items():
    for g in df.group.unique():
        sg = sig(df, g)
        if sum(e for _, e in sg) >= 2:     # at least two deaths, otherwise trivially identical
            seen.setdefault(sg, []).append((bid, g))
for sg, lst in seen.items():
    if len(lst) > 1:
        print('  ', lst, '->', [t for t, e in sg if e == 1], '+', sum(1 for t, e in sg if e == 0), 'censored')
print('\n=== whole-block identity')
for a, b in itertools.combinations(S, 2):
    ga, gb = list(S[a].group.unique()), list(S[b].group.unique())
    if ga == gb and all(sig(S[a], g) == sig(S[b], g) for g in ga):
        print(f'   {a} == {b} for every group {ga}')

# ---------- (b) element-wise identity between same-shaped non-survival blocks
print('\n=== element-wise identical cells between same-layout blocks (fraction of positions identical)')
NS = {bid: P.load(bid) for bid, b in P.BLOCKS.items() if b['kind'] != 'surv'}
def key(df):
    cols = ['group', 'rep'] + (['x'] if 'x' in df.columns and df['x'].notna().any() else [])
    return df.set_index(cols)['value']
res = []
for a, b in itertools.combinations(NS, 2):
    ka, kb = key(NS[a]), key(NS[b])
    # compare by position (rep, x) irrespective of group label -> also catches shifted labels
    if len(ka) != len(kb) or len(ka) < 8:
        continue
    va, vb = ka.values, kb.values
    same = np.isclose(va, vb, rtol=0, atol=1e-9)
    # ignore trivial 100s (day-0 body weights)
    nontrivial = ~((va == 100) & (vb == 100))
    if nontrivial.sum() >= 8:
        frac = same[nontrivial].mean()
        if frac >= 0.25:
            res.append((a, b, int(nontrivial.sum()), int(same[nontrivial].sum()), round(frac, 2)))
print(pd.DataFrame(res, columns=['block_a', 'block_b', 'n_positions', 'n_identical', 'fraction']).to_string(index=False))

# ---------- (c) group-vs-group trajectory identity for body-weight blocks (any block pair, any group pair)
print('\n=== body-weight: group-level matrices sharing identical non-100 values at the same (animal, day) positions')
BW = {bid: NS[bid] for bid, b in P.BLOCKS.items() if b['kind'] == 'bw'}
mats = {}
for bid, df in BW.items():
    for g in df.group.unique():
        m = df[df.group == g].pivot(index='x', columns='rep', values='value')
        mats[(bid, g)] = m
res = []
for (ka, ma), (kb, mb) in itertools.combinations(mats.items(), 2):
    idx = ma.index.intersection(mb.index); cols = ma.columns.intersection(mb.columns)
    A = ma.loc[idx, cols].values; Bm = mb.loc[idx, cols].values
    ok = ~np.isnan(A) & ~np.isnan(Bm) & ~((A == 100) & (Bm == 100))
    if ok.sum() < 10:
        continue
    same = np.isclose(A, Bm, atol=1e-9) & ok
    if same.sum() >= 5:
        res.append((ka[0], ka[1], kb[0], kb[1], int(ok.sum()), int(same.sum()), round(same.sum() / ok.sum(), 2)))
dd = pd.DataFrame(res, columns=['block_a', 'group_a', 'block_b', 'group_b', 'n_comparable', 'n_identical', 'fraction']).sort_values('fraction', ascending=False)
print(dd.to_string(index=False))
dd.to_csv('../tables/QC_bodyweight_shared_values.csv', index=False)
