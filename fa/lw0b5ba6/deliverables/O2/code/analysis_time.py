import pandas as pd, numpy as np, warnings
from scipy import stats
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
warnings.filterwarnings('ignore')
t=pd.read_csv('tidy.csv'); t['time']=t['time'].astype(str)
for blk,log in [('S01-D',False),('S01-E',False),('S02-F',True),('S07-A',False),('S11-A',False),('S11-B',False),('S11-D',False),('S05-A',False),('S05-B',False)]:
    d=t[t.block==blk].copy(); d['y']=np.log10(d.value) if log else d.value
    d['g']=d.group.str.replace(r'[^A-Za-z0-9]','_',regex=True)
    m=smf.ols('y ~ C(g)*C(time)',data=d).fit(); a=anova_lm(m,typ=2)
    print(f"=== {blk} two-way ANOVA ({'log10' if log else 'linear'}) ===")
    print(a[['F','PR(>F)']].round(4).to_string())
    piv=d.groupby(['time','group']).value.mean().unstack().round(2)
    piv=piv.loc[sorted(piv.index,key=lambda x: float(x.replace('h','')))]
    print(piv.to_string())
    # Tukey within each time for PSLN-344 vs PSLN-212
    for tm in piv.index:
        dd=d[d.time==tm]
        if {'PSLN-344','PSLN-212'}<=set(dd.group):
            tk=pairwise_tukeyhsd(dd.y,dd.group); tb=pd.DataFrame(tk._results_table.data[1:],columns=tk._results_table.data[0])
            r=tb[((tb.group1=='PSLN-212')&(tb.group2=='PSLN-344'))|((tb.group1=='PSLN-344')&(tb.group2=='PSLN-212'))]
            print(f"   t={tm}: PSLN-344 vs PSLN-212 Tukey p-adj={float(r['p-adj'].iloc[0]):.3g}")
