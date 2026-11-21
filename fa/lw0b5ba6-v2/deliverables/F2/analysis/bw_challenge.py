import numpy as np, pandas as pd
from scipy import stats
from blocks import *
pd.set_option('display.width', 300); pd.set_option('display.max_rows', 3000); pd.set_option('display.float_format', lambda x: f'{x:.4g}')
rows=[]
for k, df in W.items():
    if k=='S08-D': continue
    for g, d in df.groupby('group', sort=False):
        per = d[d.day>0].groupby('rep')['value'].min()
        d14 = d[d.day==14]['value']
        # day of group-mean nadir among animals with data
        m = d.groupby('day')['value'].mean()
        rows.append(dict(block=k, group=g, n_d0=d[d.day==0].shape[0], mean_nadir=per.mean(), sd_nadir=per.std(ddof=1), worst=per.min(), mean_max_loss=100-per.mean(),
                         n_with_d14=len(d14), mean_d14=d14.mean() if len(d14) else np.nan, n_d14_below90=int((d14<90).sum()) if len(d14) else 0))
r = pd.DataFrame(rows); r.to_csv('bw_challenge_nadir.csv', index=False)
print(r.to_string(index=False))
