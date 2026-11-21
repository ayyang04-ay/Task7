import numpy as np, pandas as pd
from scipy import stats
from blocks import *
pd.set_option('display.width', 300); pd.set_option('display.max_rows', 3000); pd.set_option('display.float_format', lambda x: f'{x:.4g}')
d = W['S08-D']
print(d.pivot_table(index='day', columns='group', values='value', aggfunc='mean', sort=False).round(2).to_string())
print(d.pivot_table(index='day', columns='group', values='value', aggfunc='count', sort=False).to_string())
nad = d[d.day>0].groupby(['group','rep'], sort=False)['value'].agg(['min','idxmin']).reset_index()
nad['nadir_day'] = d.loc[nad['idxmin'],'day'].values
nad['max_loss_pct'] = 100-nad['min']
print(nad.groupby('group', sort=False).agg(n=('min','size'), mean_nadir=('min','mean'), sd=('min','std'), worst=('min','min'), mean_maxloss=('max_loss_pct','mean'), median_nadir_day=('nadir_day','median')).to_string())
g = {k: v['max_loss_pct'].values for k, v in nad.groupby('group', sort=False)}
r = stats.tukey_hsd(*g.values()); names=list(g)
print('ANOVA on max loss:', stats.f_oneway(*g.values()))
for i in range(len(names)):
    for j in range(i+1,len(names)):
        print(f'  {names[i]:15s} vs {names[j]:15s} diff={g[names[j]].mean()-g[names[i]].mean():6.2f}  p_tukey={r.pvalue[i,j]:.4g}  p_welch={stats.ttest_ind(g[names[i]], g[names[j]], equal_var=False).pvalue:.4g}')
# per-animal day-10 recovery
print(d[d.day==10].groupby('group', sort=False)['value'].agg(['count','mean','min','max']).to_string())
nad.to_csv('safety_S08D_nadir.csv', index=False)
