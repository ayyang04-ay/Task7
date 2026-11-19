"""Audit 3: search the whole workbook for repeated data.
 (a) identical per-group vectors (>=3 values) appearing in two different places;
 (b) identical survival tables;
 (c) cell-by-cell overlap between same-shaped blocks (partial copy/paste)."""
import itertools, numpy as np, pandas as pd
from psln_blocks import df
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',200); pd.set_option('display.max_rows',500)

d = df[~df.kind.isin(['orphan'])].copy()
d['time'] = d['time'].map(lambda x: '-' if pd.isna(x) else str(x))
d['analyte'] = d['analyte'].map(lambda x: '-' if pd.isna(x) else str(x))

# (a) vectors: for each (block, group, time, analyte) -> tuple of values in replicate order
vecs = {}
for key, a in d[d.kind!='survival'].groupby(['block','group','time','analyte'], sort=False):
    v = tuple(np.round(a.sort_values('rep').value.astype(float).values, 4))
    if len(v) >= 3 and len(set(v)) > 1:                       # ignore constant rows such as day-0 = 100
        vecs[key] = (v, f"{a.cell.iloc[0]}:{a.cell.iloc[-1]}")
hits = []
keys = list(vecs)
for i in range(len(keys)):
    for j in range(i+1, len(keys)):
        vi, ci = vecs[keys[i]]; vj, cj = vecs[keys[j]]
        if vi == vj:
            hits.append(dict(kind='identical ordered vector', a=keys[i], a_cells=ci, b=keys[j], b_cells=cj, n=len(vi), values=vi))
        elif len(vi)==len(vj) and sorted(vi)==sorted(vj):
            hits.append(dict(kind='identical multiset (order differs)', a=keys[i], a_cells=ci, b=keys[j], b_cells=cj, n=len(vi), values=vi))
        else:
            # partial positional overlap for same-length vectors
            if len(vi)==len(vj) and len(vi)>=5:
                same = sum(x==y for x,y in zip(vi,vj))
                if same >= len(vi)-2 and same>=4:
                    hits.append(dict(kind=f'near-identical vector ({same}/{len(vi)} positions equal)', a=keys[i], a_cells=ci, b=keys[j], b_cells=cj, n=len(vi), values=(vi,vj)))
H = pd.DataFrame(hits)
# LOCF inside a weight block produces identical vectors across *time* within same group; remove those (same block & group)
if len(H):
    H['same_block_group'] = H.apply(lambda r: r.a[0]==r.b[0] and r.a[1]==r.b[1], axis=1)
    H2 = H[~H.same_block_group].drop(columns='same_block_group')
else:
    H2 = H
H2.to_csv('audit_03a_duplicate_vectors.csv', index=False)
print('(a) duplicated vectors across different block/group:', len(H2))
print(H2.to_string())

# (b) identical survival tables
s = df[df.kind=='survival']
tabs = {}
for b, a in s.groupby('block', sort=False):
    tabs[b] = tuple(sorted((g, tuple(sorted(zip(x.time.fillna(-1), x.event)))) for g, x in a.groupby('group')))
print('\n(b) survival tables identical in every group:')
for b1, b2 in itertools.combinations(tabs, 2):
    if tabs[b1] == tabs[b2]:
        print('   ', b1, '==', b2)
    else:
        # group-level identity among groups with deaths
        g1 = dict(tabs[b1]); g2 = dict(tabs[b2])
        for g in set(g1) & set(g2):
            ev = [e for _, e in g1[g]]
            if g1[g] == g2[g] and sum(ev) >= 3:
                print(f'    group-level: {b1} / {b2}  group {g}: {g1[g]}')

# (c) cell-by-cell overlap between same-shaped non-survival blocks
print('\n(c) positional overlap between blocks of identical layout (excluding 100-at-day-0 rows):')
blocks = {}
for b, a in d[d.kind!='survival'].groupby('block', sort=False):
    a = a[~((a.kind=='weight') & (a.value==100))]
    blocks[b] = {(r.col_order, r.rep, r.time, r.analyte): round(float(r.value),4) for r in a.itertuples()}
res=[]
for b1, b2 in itertools.combinations(blocks, 2):
    k = set(blocks[b1]) & set(blocks[b2])
    if len(k) < 10: continue
    same = sum(blocks[b1][x]==blocks[b2][x] for x in k)
    if same >= 5:
        res.append(dict(block1=b1, block2=b2, comparable_cells=len(k), identical_cells=same, pct=round(100*same/len(k),1)))
R = pd.DataFrame(res).sort_values('identical_cells', ascending=False)
R.to_csv('audit_03c_positional_overlap.csv', index=False)
print(R.to_string())
