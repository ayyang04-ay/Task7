import numpy as np, pandas as pd
from blocks import *
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 1000); pd.set_option('display.float_format', lambda x: f'{x:.4g}')

def gm(x):
    x = np.asarray(x, float); return float(np.exp(np.mean(np.log(x))))
rows=[]
for k, df in B.items():
    by = ['group'] + (['analyte'] if 'analyte' in df.columns else [])
    for key, d in df.groupby(by, sort=False):
        g = key[0]; an = key[1] if len(key)>1 else ''
        v = d['value'].values
        cells = d['cellref'].tolist()
        rows.append(dict(block=k, analyte=an, group=g, n=len(v), mean=v.mean(), sd=v.std(ddof=1) if len(v)>1 else np.nan, median=np.median(v), min=v.min(), max=v.max(),
                         gmean=gm(v) if (v>0).all() else np.nan, cells=f'{cells[0]}..{cells[-1].split("!")[1]}'))
desc = pd.DataFrame(rows)
desc.to_csv('desc_endpoint_blocks.csv', index=False)
for k in desc.block.unique():
    print('\n##', k); print(desc[desc.block==k].drop(columns=['block']).to_string(index=False))
