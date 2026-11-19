import pandas as pd, numpy as np, re
df = pd.read_csv('/tmp/work/tidy.csv')
w = df[df.event.isna()].copy()
# high-precision values: >=4 decimals that are not trailing zeros
def ndec(x):
    s = repr(float(x))
    if 'e' in s: return 0
    d = s.split('.')[1] if '.' in s else ''
    return len(d.rstrip('0'))
w['ndec'] = w.value.apply(ndec)
hp = w[w.ndec>=4].copy()
hp['frac'] = ((hp.value % 1)).round(5)
hp['int'] = np.floor(hp.value).astype(int)
print('high-precision values:', len(hp), 'in blocks:', hp.block.value_counts().to_dict())
# Exclude derived-ratio blocks which are computed (S03-B/F, S04-B_TfhTfr, S09-A log10, S04-A) -- fingerprints there are expected to be unique computations
weights = hp[hp.unit=='% of d0']
g = weights.groupby('frac')
rows=[]
for f,s in g:
    locs = s[['block','group','time','value','cell']].values.tolist()
    ident = set((b,gg) for b,gg,_,_,_ in locs)
    if len(ident)>=2:
        rows.append(dict(frac=f, n=len(s), n_block_groups=len(ident), occurrences='; '.join(f'{c} ({b} {gg} d{int(t)}: {v})' for b,gg,t,v,c in locs)))
fp = pd.DataFrame(rows).sort_values('n', ascending=False)
pd.set_option('display.width',300); pd.set_option('display.max_colwidth',400)
print(len(fp))
print(fp.to_string())
fp.to_csv('/tmp/work/fingerprints.csv', index=False)
