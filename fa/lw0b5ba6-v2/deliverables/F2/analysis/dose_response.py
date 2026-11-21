import numpy as np, pandas as pd
from scipy.optimize import curve_fit
from blocks import *
pd.set_option('display.width', 300); pd.set_option('display.float_format', lambda x: f'{x:.4g}')
d = T['S08-A']
def hill(D, emax, ed50, h): return 1 + emax*D**h/(ed50**h + D**h)
rows=[]
for g, x in d.groupby('group', sort=False):
    D = x['dose_ug'].values.astype(float); y = x['value'].values
    best=None
    for h0 in (1.5, 2, 3):
        try:
            p, cov = curve_fit(hill, D, y, p0=[y.max(), 10, h0], bounds=([0, 0.5, 0.5],[500, 200, 8]), maxfev=20000)
            sse = ((y-hill(D,*p))**2).sum()
            if best is None or sse<best[2]: best=(p,cov,sse)
        except Exception as e: pass
    p, cov, sse = best; se = np.sqrt(np.diag(cov))
    m = x.groupby('dose_ug')['value'].mean()
    rows.append(dict(group=g, Emax_fold=p[0], Emax_se=se[0], ED50_ug=p[1], ED50_se=se[1], hill=p[2], hill_se=se[2], rmse=np.sqrt(sse/len(y)),
                     mean_1=m[1], mean_5=m[5], mean_10=m[10], mean_20=m[20], mean_40=m[40], ratio_20_over_40=m[20]/m[40], pred20_frac_of_top=(hill(20,*p)-1)/p[0]))
r = pd.DataFrame(rows); print(r.to_string(index=False)); r.to_csv('dose_response_S08A.csv', index=False)
# 20 vs 40 ug test within PSLN-344
from scipy import stats
for g in d.group.unique():
    a = d[(d.group==g)&(d.dose_ug==20)]['value']; b = d[(d.group==g)&(d.dose_ug==40)]['value']
    print(g, '20 vs 40 ug: means', a.mean().round(2), b.mean().round(2), 'Welch p=', round(stats.ttest_ind(a,b,equal_var=False).pvalue,3))
# PSLN-344 vs PSLN-212 at each dose
for dose in [1,5,10,20,40]:
    a = d[(d.group=='PSLN-212')&(d.dose_ug==dose)]['value']; b = d[(d.group=='PSLN-344')&(d.dose_ug==dose)]['value']
    print(dose, 'ug: PSLN-344/PSLN-212 =', round(b.mean()/a.mean(),2), 'Welch p=', round(stats.ttest_ind(np.log10(a),np.log10(b),equal_var=False).pvalue,4))
