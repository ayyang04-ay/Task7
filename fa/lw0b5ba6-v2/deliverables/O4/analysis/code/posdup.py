import pandas as pd, numpy as np, itertools
vals = pd.read_csv('values.csv')
vals['rep'] = vals.groupby(['block','group','time','analyte'], dropna=False).cumcount()
vals['tkey'] = vals.time.astype(str)
def mat(b):
    d = vals[vals.block==b].copy()
    d['gi'] = d.groupby('block').group.transform(lambda s: pd.factorize(s)[0])
    return d.set_index(['gi','tkey','rep']).value
blocks = vals.block.unique()
res=[]
for a,b in itertools.combinations(blocks,2):
    A, B = mat(a), mat(b)
    common = A.index.intersection(B.index)
    if len(common) < 8: continue
    eq = (A.loc[common].round(6) == B.loc[common].round(6))
    res.append((a,b,len(common),int(eq.sum()), eq.mean()))
res = pd.DataFrame(res, columns=['blockA','blockB','positions','identical','frac']).sort_values('identical', ascending=False)
print(res.head(15).to_string())
# detail for S11-A vs S11-B
A = vals[vals.block=='S11-A']; B = vals[vals.block=='S11-B']
m = A.merge(B, on=['group','time','rep'], suffixes=('_AM','_Neut'))
m['same'] = np.isclose(m.value_AM, m.value_Neut)
print()
print(m.pivot_table(index='rep', columns='group', values='same', aggfunc='sum'))
print('total identical positions:', m.same.sum(), 'of', len(m))
# chance expectation: permutation - shuffle S11-B values within group/time and count identical positions
rng = np.random.default_rng(1)
null=[]
for i in range(5000):
    mm = m.copy()
    mm['perm'] = mm.groupby(['group','time']).value_Neut.transform(lambda s: rng.permutation(s.values))
    null.append(np.isclose(mm.value_AM, mm.perm).sum())
null=np.array(null)
print('permutation null (within group x day): mean identical =', null.mean(), ' 99.9th pct =', np.percentile(null,99.9), ' max =', null.max())
