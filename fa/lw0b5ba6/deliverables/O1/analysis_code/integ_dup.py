import pandas as pd, numpy as np, itertools
df = pd.read_csv('/tmp/work/tidy.csv')
num = df[df.event.isna() & (df.block!='S08-UNLABELLED')].copy()
# exclude discrete dilution-series titres (HAI / neutralising) and day-0 weights (all 100 by definition)
excl_blocks = {'S03-C','S03-D','S03-G','S03-H'}
num = num[~num.block.isin(excl_blocks)]
num = num[~((num.unit=='% of d0') & (num.time==0))]
num['tkey'] = num.time.fillna(-1).astype(str) + '|' + num.get('analyte').fillna('').astype(str)
vecs = {}
for (b,g,t),s in num.groupby(['block','group','tkey']):
    vecs[(b,g,t)] = s.sort_values('rep')[['rep','value','cell']].values.tolist()
keys = list(vecs)
res=[]
for a,b in itertools.combinations(keys,2):
    if a[0]==b[0] and a[1]==b[1]: continue   # same block & group (different times) handled separately
    va = {r:v for r,v,c in vecs[a]}; vb = {r:v for r,v,c in vecs[b]}
    same_pos = [(r, va[r]) for r in va if r in vb and va[r]==vb[r]]
    if len(same_pos)>=2:
        ca = {r:c for r,v,c in vecs[a]}; cb={r:c for r,v,c in vecs[b]}
        res.append(dict(A=f'{a[0]}|{a[1]}|t={a[2]}', B=f'{b[0]}|{b[1]}|t={b[2]}', n_same_position=len(same_pos),
                        n_A=len(va), n_B=len(vb), values=[v for r,v in same_pos],
                        cells=[f'{ca[r]}={cb[r]}' for r,v in same_pos]))
r = pd.DataFrame(res).sort_values('n_same_position', ascending=False)
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',120)
print(len(r))
print(r.head(80).to_string())
r.to_csv('/tmp/work/dup_pairs.csv', index=False)
