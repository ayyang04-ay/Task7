"""Two-way ANOVA (group x time) for the time-course blocks, as per the stated methods; plus peak-day summaries."""
from paths import TABLES, FIGS, OUT as OUTDIR, BUILD, PANDOC
import pandas as pd, numpy as np, warnings
import statsmodels.formula.api as smf, statsmodels.api as sm
import psln_blocks as pb
warnings.filterwarnings('ignore')
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500)
df = pb.tidy()
rows = []
for blk, an in [('S01-D', None), ('S01-E', None), ('S02-F', None), ('S05-A', None), ('S05-B', None), ('S07-A', None), ('S11-A', None), ('S11-B', None), ('S11-D', None), ('S08-A', None)]:
    t = df[df.block == blk].copy()
    t['xx'] = t.x.astype(str); t['y'] = np.log10(t.value) if blk in ('S02-F', 'S08-A') else t.value
    m = smf.ols('y ~ C(group) * C(xx)', data=t).fit()
    a = sm.stats.anova_lm(m, typ=2)
    rows.append(dict(block=blk, analyte=t.analyte.iloc[0], scale='log10' if blk in ('S02-F', 'S08-A') else 'linear', n_obs=len(t),
                     F_group=a.loc['C(group)', 'F'], p_group=a.loc['C(group)', 'PR(>F)'], F_time=a.loc['C(xx)', 'F'], p_time=a.loc['C(xx)', 'PR(>F)'],
                     F_inter=a.loc['C(group):C(xx)', 'F'], p_inter=a.loc['C(group):C(xx)', 'PR(>F)']))
R = pd.DataFrame(rows); R.to_csv(TABLES + 'T15_timecourse_two_way_anova.csv', index=False)
print(R.to_string())
