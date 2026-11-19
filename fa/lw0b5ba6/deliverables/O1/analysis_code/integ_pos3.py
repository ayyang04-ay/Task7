import pandas as pd, numpy as np, itertools, re
from scipy.stats import binom
df = pd.read_csv('/tmp/work/tidy.csv')
x = df[df.event.isna() & (df.unit!='% of d0') & (df.block!='S08-UNLABELLED')].copy()
x = x[~x.block.isin(['S03-C','S03-D','S03-G','S03-H'])]   # dilution-series titres: matches expected
x['gnorm'] = x.group.str.replace(r'[^A-Za-z0-9]','',regex=True).str.upper().str.replace('PSLNSRB','PSLNSRB')
x['tk'] = x.time.fillna(-1)
x['an'] = x['analyte'].fillna('')
blocks = x.block.unique()
rows=[]
for A,B in itertools.combinations(blocks,2):
    a = x[x.block==A]; b = x[x.block==B]
    m = a.merge(b, on=['gnorm','tk','an'], suffixes=('_a','_b'))
    if m.empty: continue
    diag = m[m.rep_a==m.rep_b]; off = m[m.rep_a!=m.rep_b]
    k = int((diag.value_a==diag.value_b).sum()); n=len(diag)
    ko = int((off.value_a==off.value_b).sum()); no=len(off)
    rows.append(dict(A=A,B=B,shared_groups=m.gnorm.nunique(),n_aligned=n,k_same_pos=k,n_off=no,k_off=ko,
                     cells='; '.join((diag[diag.value_a==diag.value_b].cell_a+'='+diag[diag.value_a==diag.value_b].cell_b).tolist()[:12])))
R = pd.DataFrame(rows)
p0 = (R.k_off.sum()+1)/(R.n_off.sum()+1)
R['expected'] = R.n_aligned*p0
R['p'] = binom.sf(R.k_same_pos-1, R.n_aligned, p0)
R['bonf_sig'] = R.p < 0.05/len(R)
pd.set_option('display.width',320); pd.set_option('display.max_colwidth',220)
print('pooled chance rate', round(p0,4), 'pairs', len(R))
print(R.sort_values('p').head(15).to_string())
R.to_csv('/tmp/work/nonweight_copy.csv',index=False)
# S11 detail: per group/time
a = x[x.block=='S11-A']; b = x[x.block=='S11-B']; d = x[x.block=='S11-D']
m = a.merge(b,on=['group','time'],suffixes=('_A','_B'))
m = m[m.rep_A==m.rep_B]
print(pd.crosstab(m.rep_A, m.value_A==m.value_B))
