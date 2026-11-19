import pandas as pd, numpy as np, warnings
import statsmodels.formula.api as smf, statsmodels.api as sm
warnings.filterwarnings('ignore')
D = pd.read_csv('/tmp/work/tidy/continuous.csv'); D['time'] = D['time'].astype(str)
out=[]
for blk, meas in [('S01-D','Lung monocytes CD11b+Ly6C+ (%)'),('S01-E','Lung CD11b+ DC (%)'),('S02-F','Lung Gm-csf (fold vs untreated)'),
                  ('S11-D','Lung NK cells (%)'),('S07-A','Lung Ly6C+CCR2+ macrophages (x10^5 cells)'),('S01-A','Lung Ifnb1 (fold vs untreated)')]:
    d = D[(D.block==blk)].copy()
    d['y'] = np.log10(d.value) if 'fold' in meas else d.value
    m = smf.ols('y ~ C(group)*C(time)', data=d).fit()
    a = sm.stats.anova_lm(m, typ=2)
    for term in ['C(group)','C(time)','C(group):C(time)']:
        out.append(dict(block=blk, measurand=meas, term=term, F=a.loc[term,'F'], p=a.loc[term,'PR(>F)'], df=a.loc[term,'df']))
O = pd.DataFrame(out); print(O.to_string(index=False)); O.to_csv('/tmp/work/tidy/twoway_anova.csv', index=False)
