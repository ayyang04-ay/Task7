"""(a) Morbidity after challenge from the body-weight blocks (supportive only - see QC: these blocks share values across experiments).
   Per-animal nadir uses all recorded values; animals that leave the record early keep their last recorded weight as nadir.
(b) Age x Mn factorial on early innate read-outs that have all four cells (aged/young x 212/344)."""
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.formula.api as smf, statsmodels.api as sm
import tidy
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500)
idx = pd.read_csv('../data_tidy/psln_block_index.csv').set_index('block')
rows = []
for b in idx.index[idx.kind == 'bw']:
    if b == 'S08-D':
        continue
    d = tidy.get(b)
    for g in tidy.groups(b):
        s = d[(d.group == g) & (d.x > 0)]
        nad = s.groupby('rep')['value'].min()
        last = d[(d.group == g)].sort_values('x').groupby('rep').tail(1)
        complete = last[last.x == 14]
        rows.append(dict(bw_block=b, surv_block=idx.loc[b, 'pair'], group=g, n=nad.size, mean_nadir=nad.mean(), sd_nadir=nad.std(ddof=1),
                         mean_max_loss_pct=100 - nad.mean(), n_with_d14=len(complete), d14_mean_of_recorded=complete.value.mean() if len(complete) else np.nan))
M = pd.DataFrame(rows); M.to_csv('../tables/T11_morbidity_bodyweight.csv', index=False)
print(M.round(1).to_string(index=False))
print('\nMean maximum weight loss (%), aged BALB/c challenge blocks S15-A..G:')
sel = M[M.bw_block.isin(['S15-A', 'S15-B', 'S15-C', 'S15-D', 'S15-E', 'S15-F', 'S15-G'])]
print(sel.groupby('group')['mean_max_loss_pct'].agg(['mean', 'min', 'max', 'count']).round(1))
print('Young BALB/c S09-C/E/G:'); print(M[M.bw_block.isin(['S09-C', 'S09-E', 'S09-G'])].groupby('group')['mean_max_loss_pct'].agg(['mean', 'min', 'max']).round(1))

print('\n=== Age x Mn factorial (log2 scale) ===')
def fact(block, x=None, label=''):
    recs = []
    for g, age, mn in [('PSLN-212', 'aged', 0), ('PSLN-344', 'aged', 1), ('PSLN-212(Y)', 'young', 0), ('PSLN-344(Y)', 'young', 1)]:
        for v in tidy.vec(block, g, x):
            recs.append(dict(age=age, mn=mn, y=np.log2(v)))
    f = pd.DataFrame(recs); m = smf.ols('y ~ C(age) * mn', data=f).fit(); an = sm.stats.anova_lm(m, typ=2)
    ma = f.groupby(['age', 'mn'])['y'].mean()
    fa = 2 ** (ma['aged', 1] - ma['aged', 0]); fy = 2 ** (ma['young', 1] - ma['young', 0])
    print(f"{label}: Mn effect aged {fa:.2f}x, young {fy:.2f}x; age deficit without Mn {100*(1-2**(ma['aged',0]-ma['young',0])):.0f}%, with Mn {100*(1-2**(ma['aged',1]-ma['young',1])):.0f}%; interaction p = {an.loc['C(age):mn','PR(>F)']:.3g}")
fact('S01-A 16h', label='Ifnb1 16 h (S01-A)')
fact('S01-A 72h', label='Ifnb1 72 h (S01-A)')
fact('S01-E', 4, 'CD11b+ DC d4 (S01-E)')
fact('S01-F', None, 'cDC1 72 h (S01-F)')
fact('S02-C', None, 'OVA+ MLN DC 36 h (S02-C)')
fact('S02-E', None, 'OT-I priming by MLN DC (S02-E)')
