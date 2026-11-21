"""QC 4: order-insensitive scan for value re-use between groups of different blocks (non-survival, non-body-weight)."""
import numpy as np, pandas as pd, itertools
import tidy
T = tidy.T()
idx = pd.read_csv('../data_tidy/psln_block_index.csv').set_index('block')
sel = [b for b in idx.index if idx.loc[b, 'kind'] in ('cols', 'rows', 'tc')]
vecs = {}
for b in sel:
    d = T[T.block == b]
    for (g, x), s in d.groupby(['group', d['x'].fillna(-1)], sort=False):
        vecs[(b, g, x)] = np.round(s.value.values, 6)
res = []
keys = list(vecs)
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        a, c = vecs[keys[i]], vecs[keys[j]]
        if keys[i][0] == keys[j][0] and keys[i][1] == keys[j][1]:
            continue
        if len(a) < 3 or len(c) < 3:
            continue
        # multiset intersection
        from collections import Counter
        inter = sum((Counter(a.tolist()) & Counter(c.tolist())).values())
        # titre blocks have few discrete levels -> skip when both are titre-like (all values multiples of 10 and ints)
        titre_like = lambda v: np.all(np.mod(v, 10) == 0)
        if titre_like(a) and titre_like(c):
            continue
        if inter >= 3 or (inter >= 2 and min(len(a), len(c)) <= 3):
            res.append((keys[i], keys[j], len(a), len(c), inter, sorted(set(a.tolist()) & set(c.tolist()))))
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 90)
R = pd.DataFrame(res, columns=['vec_a', 'vec_b', 'n_a', 'n_b', 'n_shared', 'shared_values'])
print(R.to_string(index=False))
R.to_csv('../tables/QC_shared_values_nonBW.csv', index=False)
