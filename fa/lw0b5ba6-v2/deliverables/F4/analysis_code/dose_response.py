import pandas as pd, numpy as np, warnings
from scipy.optimize import curve_fit
from scipy import stats
warnings.filterwarnings('ignore')
Q = pd.read_csv('quant_long.csv')
d = Q[Q.block=='S08-A'].copy(); d['dose']=d.time.astype(float)
def hill(x, emax, ed50, h):  # fold induction; baseline fixed at 1 (fold vs untreated)
    return 1 + (emax-1) * x**h/(ed50**h + x**h)
res=[]
for g, x in d.groupby('group', sort=False):
    m = x.groupby('dose').value.agg(['mean','std'])
    gm = x.groupby('dose').value.apply(lambda v: np.exp(np.log(v).mean()))
    # fit on log scale
    f = lambda dose, emax, ed50, h: np.log(hill(dose, emax, ed50, h))
    try:
        p, cov = curve_fit(f, x.dose.values, np.log(x.value.values), p0=[x.value.max(), 8, 2], bounds=([1.01, 0.5, 0.3],[500, 100, 8]))
        se = np.sqrt(np.diag(cov))
    except Exception as e:
        p = [np.nan]*3; se=[np.nan]*3
    r20_40 = gm.loc[40]/gm.loc[20]
    res.append(dict(group=g, **{f"GM_{int(k)}ug": round(v,2) for k,v in gm.items()}, Emax=p[0], Emax_se=se[0], ED50=p[1], ED50_se=se[1], hill=p[2], hill_se=se[2], ratio_40_vs_20=r20_40,
                    frac_of_40_at_20=gm.loc[20]/gm.loc[40], cells=f"{x.cell.iloc[0]}:{x.cell.iloc[-1].split('!')[1]}"))
R = pd.DataFrame(res); pd.set_option('display.width', 250)
print(R.round(2).to_string())
R.to_csv('dose_response_fit.csv', index=False)
# 20 vs 40 ug tests (log scale)
for g, x in d.groupby('group', sort=False):
    a = np.log10(x[x.dose==20].value); b = np.log10(x[x.dose==40].value)
    print(g, '40 vs 20 ug: ratio', round(10**(b.mean()-a.mean()),2), 'Welch p', round(stats.ttest_ind(a,b,equal_var=False).pvalue,3))
# key cross-formulation comparisons
gm = d.groupby(['group','dose']).value.apply(lambda v: np.exp(np.log(v).mean())).unstack()
print(gm.round(2))
a = np.log10(d[(d.group=='PSLN-344')&(d.dose==10)].value); b = np.log10(d[(d.group=='PSLN-212')&(d.dose==40)].value)
print('PSLN-344 @10ug vs PSLN-212 @40ug: ratio', round(10**(a.mean()-b.mean()),2), 'Welch p', round(stats.ttest_ind(a,b,equal_var=False).pvalue,3))
a = np.log10(d[(d.group=='PSLN-344')&(d.dose==5)].value); b = np.log10(d[(d.group=='PSLN-212')&(d.dose==20)].value)
print('PSLN-344 @5ug vs PSLN-212 @20ug: ratio', round(10**(a.mean()-b.mean()),2), 'Welch p', round(stats.ttest_ind(a,b,equal_var=False).pvalue,3))
a = np.log10(d[(d.group=='PSLN-344')&(d.dose==20)].value); b = np.log10(d[(d.group=='PSLN-344/R848')&(d.dose==20)].value)
print('PSLN-344 vs PSLN-344/R848 @20ug: ratio', round(10**(a.mean()-b.mean()),2), 'Welch p', round(stats.ttest_ind(a,b,equal_var=False).pvalue,3))
