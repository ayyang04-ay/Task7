import numpy as np, pandas as pd
from blocks import *
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 1000); pd.set_option('display.float_format', lambda x: f'{x:.3g}')
rows=[]
for k, df in T.items():
    tcol = [c for c in df.columns if c in ('day','time','dose_ug')][0]
    piv_m = df.pivot_table(index=tcol, columns='group', values='value', aggfunc='mean', sort=False)
    piv_s = df.pivot_table(index=tcol, columns='group', values='value', aggfunc=lambda x: np.std(x, ddof=1), sort=False)
    piv_n = df.pivot_table(index=tcol, columns='group', values='value', aggfunc='count', sort=False)
    print('\n##', k, '(mean)'); print(piv_m.to_string())
    print('   (sd)'); print(piv_s.to_string())
    print('   (n)'); print(piv_n.to_string())
    for (g,t), d in df.groupby(['group',tcol], sort=False):
        v=d['value'].values; cells=d['cellref'].tolist()
        rows.append(dict(block=k, group=g, time=t, timevar=tcol, n=len(v), mean=v.mean(), sd=v.std(ddof=1), min=v.min(), max=v.max(), cells=f'{cells[0]}..{cells[-1].split("!")[1]}'))
pd.DataFrame(rows).to_csv('desc_timecourse_blocks.csv', index=False)
