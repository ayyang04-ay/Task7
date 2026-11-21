import pandas as pd, numpy as np, warnings, itertools
from scipy import stats
import statsmodels.api as sm, statsmodels.formula.api as smf
from statsmodels.stats.multicomp import pairwise_tukeyhsd
warnings.filterwarnings('ignore')
pd.set_option('display.width', 300); pd.set_option('display.max_rows', 3000)
Q = pd.read_csv('quant_long.csv'); W = pd.read_csv('wt_long.csv')

print("=== S10-A CNS transcripts (36 h), linear fold; Tukey on log10 ===")
for an in ['CNS Ifnb1 (fold)','CNS Tnf (fold)','CNS Isg15 (fold)']:
    d = Q[(Q.block=='S10-A')&(Q.analyte==an)]
    print(an, d.groupby('group', sort=False).value.agg(['mean','std']).round(2).T.to_dict())
    tk = pairwise_tukeyhsd(np.log10(d.value), d.group)
    for a,b,md,p,lo,hi,rej in tk.summary().data[1:]:
        if 'PSLN-344' in (a,b): 
            xa=d[d.group==a].value; xb=d[d.group==b].value
            print(f"    {a} vs {b}: ratio(B/A)={10**md:.2f} [{10**lo:.2f},{10**hi:.2f}] Tukey p={p:.3f}; Welch(log) p={stats.ttest_ind(np.log10(xa),np.log10(xb),equal_var=False).pvalue:.3f}; MWU p={stats.mannwhitneyu(xa,xb,method='exact').pvalue:.3f}")

print("\n=== S08-D body weight after immunization (percent of day 0) ===")
d = W[W.block=='S08-D']
m = d.groupby(['group','day'], sort=False).value.agg(['mean','min','count']).reset_index()
print(m.pivot(index='day', columns='group', values='mean').round(2).to_string())
print(m.pivot(index='day', columns='group', values='min').round(1).to_string())
print(m.pivot(index='day', columns='group', values='count').to_string())
for day in [2,4,6,8,10]:
    a = d[(d.group=='PSLN-344')&(d.day==day)].value.dropna(); b = d[(d.group=='Vaccine')&(d.day==day)].value.dropna()
    c = d[(d.group=='PSLN-212')&(d.day==day)].value.dropna(); r = d[(d.group=='PSLN-212/R848')&(d.day==day)].value.dropna()
    print(f"day {day}: PSLN-344 {a.mean():.2f} vs Vaccine {b.mean():.2f}: diff {a.mean()-b.mean():.2f}, Welch p={stats.ttest_ind(a,b,equal_var=False).pvalue:.3f}, MWU p={stats.mannwhitneyu(a,b,method='exact').pvalue:.3f} | PSLN-344 vs PSLN-212 diff {a.mean()-c.mean():.2f} p={stats.ttest_ind(a,c,equal_var=False).pvalue:.3f} | R848 combo {r.mean():.2f} vs Vaccine p={stats.ttest_ind(r,b,equal_var=False).pvalue:.4f}")
# per-animal nadir
nad = d[d.day>0].groupby(['group','animal'], sort=False).value.min().reset_index()
print(nad.groupby('group', sort=False).value.agg(['mean','min','max']).round(2))
tk = pairwise_tukeyhsd(nad.value, nad.group); 
for a,b,md,p,lo,hi,rej in tk.summary().data[1:]:
    if 'PSLN-344' in (a,b) or 'R848' in a or 'R848' in b: print(f"   nadir {a} vs {b}: diff={md:.2f} [{lo:.2f},{hi:.2f}] p={p:.4f}")

print("\n=== two-way ANOVA (group x time) for time-course blocks (stated method) ===")
for blk in ['S01-D','S01-E','S02-F','S11-A','S11-B','S11-D','S07-A','S05-A','S05-B']:
    d = Q[Q.block==blk].copy(); d['t']=d['time'].astype(str)
    y = np.log10(d.value) if blk in ('S02-F','S07-A') else d.value
    d['y']=y
    mod = smf.ols('y ~ C(group)*C(t)', data=d).fit()
    a = sm.stats.anova_lm(mod, typ=2)
    print(blk, {k: f"F={a.loc[k,'F']:.1f}, p={a.loc[k,'PR(>F)']:.1e}" for k in a.index[:3]})

print("\n=== AUC-type summaries for time courses: per-group mean over days 2-8 ===")
for blk in ['S01-D','S01-E','S11-A','S11-B','S11-D']:
    d = Q[(Q.block==blk)]
    print(blk, d[d.time.astype(float)>0].groupby('group', sort=False).value.mean().round(1).to_dict(), ' peak day means:', d.groupby(['group','time'], sort=False).value.mean().groupby('group', sort=False).max().round(1).to_dict())
