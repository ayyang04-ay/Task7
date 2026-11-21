import pandas as pd, numpy as np
bw = pd.read_csv('bw.csv')
b = bw.dropna(subset=['value']).copy()
b = b[b.day>0]
# values with more than 2 decimals (not a 0.1 or 0.01 resolution reading)
def ndec(x):
    s = repr(float(x))
    return len(s.split('.')[1]) if '.' in s else 0
b['nd'] = b.value.map(ndec)
hp = b[b.nd>=4].copy()
hp['frac'] = hp.value.map(lambda x: f'{x:.8f}'.split('.')[1][:6])   # first 6 decimals of fractional part
print('high-precision BW values (>=4 decimals):', len(hp), 'in blocks', sorted(hp.block.unique()))
g = hp.groupby('frac')
shared = []
for f,d in g:
    if d.animal.nunique()>1:
        shared.append((f, len(d), d.animal.nunique(), sorted(d.block.unique()), list(zip(d.cell, d.value))))
shared.sort(key=lambda x:-x[1])
print('fractional parts shared by >1 animal:', len(shared))
for s in shared: print(' .'+s[0], 'n=',s[1], 'animals=',s[2], s[3]); print('        ', s[4])
