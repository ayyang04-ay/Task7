import numpy as np, pandas as pd
from statlib import *
pd.set_option('display.width', 300); pd.set_option('display.max_rows', 3000); pd.set_option('display.float_format', lambda x: f'{x:.4g}')
rows=[]
for k, df in B.items():
    if 'analyte' in df.columns:
        for an in df.analyte.unique():
            gs = list(df.group.unique())
            for ref in gs:
                for test in gs:
                    if ref!=test: rows.append(contrast(k, ref, test, analyte=an))
    else:
        gs = list(df.group.unique())
        for ref in gs:
            for test in gs:
                if ref!=test: rows.append(contrast(k, ref, test))
res = pd.DataFrame(rows)
res.to_csv('stats_contrasts_all.csv', index=False)
print(len(res))
