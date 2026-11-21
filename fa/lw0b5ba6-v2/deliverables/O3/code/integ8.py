from load import *
import numpy as np, pandas as pd, itertools
d = DF[~DF.measurand.str.contains('body weight')].copy()
# informative values: not integers <=100 that are common titres; require >=3 significant digits & not a round titre
def informative(x):
    s = repr(float(x))
    if float(x).is_integer(): return False  # titres/round numbers excluded
    digits = s.replace('.','').lstrip('0').replace('-','')
    return len(digits)>=3
d = d[d.value.map(informative)]
blocks = d.block.unique()
res=[]
for b1,b2 in itertools.combinations(blocks,2):
    s1 = d[d.block==b1]; s2=d[d.block==b2]
    common = set(np.round(s1.value,6)) & set(np.round(s2.value,6))
    if len(common)>=2:
        ex = []
        for v in list(common)[:6]:
            c1 = s1[np.isclose(s1.value,v)].cell.tolist(); c2 = s2[np.isclose(s2.value,v)].cell.tolist()
            ex.append(f"{v}:{c1[0]}={c2[0]}")
        res.append((b1,b2,len(common),len(s1),len(s2),ex))
res.sort(key=lambda x:-x[2])
for r in res: print(f"{r[0]:14s} vs {r[1]:14s}: {r[2]:3d} shared informative values (of {r[3]},{r[4]})  e.g. {r[5][:4]}")
# within-block: S11-A vs S11-B fraction of identical aligned cells
a = DF[DF.block=='S11-A'].copy(); b = DF[DF.block=='S11-B'].copy()
a['pos']=a.cell.str.replace('S11!','').str.extract(r'([A-Z]+)')[0]+'|'+a['day'].astype(str)
b['pos']=b.cell.str.replace('S11!','').str.extract(r'([A-Z]+)')[0]+'|'+b['day'].astype(str)
m = a.merge(b,on='pos',suffixes=('_AM','_neut'))
print('\nS11-A (alveolar macrophages) vs S11-B (neutrophils): aligned cells identical =', int(np.isclose(m.value_AM,m.value_neut).sum()),'of',len(m))
print(m.assign(same=np.isclose(m.value_AM,m.value_neut)).groupby(m.pos.str.split('|').str[0])['same'].sum().to_dict())
