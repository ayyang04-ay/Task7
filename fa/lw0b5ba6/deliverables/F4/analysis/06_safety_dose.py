#!/usr/bin/env python
"""
06_safety_dose.py -- tolerability / safety-relevant read-outs and dose-response.
Run: micromamba run -n core python 06_safety_dose.py
  S08-D  body weight after intranasal immunisation (aged; vaccine + 20 ug adjuvant)
  S09-A  lung cytokine transcripts (log10) at 16 h and in the panel whose Ifnb1 values equal the S01-A 72 h panel
  S10-A  CNS transcripts 36 h after immunisation (cholera toxin = positive control)
  S08-A  Ifnb1 dose-response (1-40 ug)
  post-challenge body-weight nadir in survivors (supporting only; weight tables carry integrity flags)
Outputs: tables/T08_*.csv
"""
import os, warnings, itertools
import numpy as np, pandas as pd
from scipy import stats, optimize
from statsmodels.stats.multicomp import pairwise_tukeyhsd
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, 'parsed'); T = os.path.join(HERE, 'tables')
sc = pd.read_csv(f'{P}/scalar_long.csv', keep_default_na=False); sc['factor'] = sc.factor.astype(str)
wt = pd.read_csv(f'{P}/weight_long.csv', keep_default_na=False)
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500); pd.options.display.float_format = '{:.4g}'.format
rng = np.random.default_rng(20261101)

# ---------- S08-D ----------
print('=' * 90); print('S08-D body weight after immunisation (percent of day 0)')
d = wt[wt.block == 'S08-D']
piv = d.groupby(['group', 'day']).value.agg(['count', 'mean', 'std', 'min']).unstack('day')
print(piv['count'].to_string()); print(piv['mean'].round(2).to_string()); print(piv['min'].round(1).to_string())
rows = []
per_animal = d[d.day > 0].groupby(['group', 'animal']).value.agg(nadir='min', last='last', n_obs='count').reset_index()
for g, x in per_animal.groupby('group', sort=False):
    rows.append(dict(group=g, n_day0=int((d[(d.group == g) & (d.day == 0)]).shape[0]), n_day10=int((d[(d.group == g) & (d.day == 10)]).shape[0]),
                     mean_nadir_pct=x.nadir.mean(), sd_nadir=x.nadir.std(ddof=1), worst_animal_nadir=x.nadir.min(),
                     mean_max_loss_pct=100 - x.nadir.mean(), animals_losing_ge5pct=int((x.nadir <= 95).sum()), animals_losing_ge10pct=int((x.nadir <= 90).sum()),
                     mean_day10=d[(d.group == g) & (d.day == 10)].value.mean()))
t8a = pd.DataFrame(rows); print(t8a.to_string())
grp = [g for g in per_animal.group.unique()]
res = pairwise_tukeyhsd(per_animal.nadir.values, per_animal.group.values)
tk = pd.DataFrame(res.summary().data[1:], columns=res.summary().data[0]); print(tk.to_string())
for g in ['PSLN-344', 'PSLN-212', 'CMP-204', 'PSLN-212/R848', 'PSLN-212(Y)']:
    a = per_animal[per_animal.group == g].nadir; b = per_animal[per_animal.group == 'Vaccine'].nadir
    print(f'  nadir {g} vs Vaccine: diff {a.mean() - b.mean():+.2f} pts; Welch p={stats.ttest_ind(a, b, equal_var=False).pvalue:.4f}; MWU exact p={stats.mannwhitneyu(a, b, method="exact").pvalue:.4f}')
t8a.to_csv(f'{T}/T08a_S08D_postvaccination_weight.csv', index=False); tk.to_csv(f'{T}/T08a2_S08D_tukey_nadir.csv', index=False)

# ---------- S09-A ----------
print('=' * 90); print('S09-A lung cytokine transcripts; geometric-mean fold vs untreated (back-transformed from log10)')
rows = []
for blk, tp in [('S09-A(cols A-V)', '16 h (as labelled)'), ('S09-A(cols X-AS)', '72 h (labelled 16h; Ifnb1 values = S01-A 72h panel)')]:
    x = sc[sc.block == blk]
    for (f, g), y in x.groupby(['factor', 'group'], sort=False):
        rows.append(dict(panel=tp, analyte=f, group=g, n=len(y), log10_mean=y.value.mean(), log10_sd=y.value.std(ddof=1), geo_fold=10 ** y.value.mean(),
                         fold_min=10 ** y.value.min(), fold_max=10 ** y.value.max()))
t8b = pd.DataFrame(rows); t8b.to_csv(f'{T}/T08b_S09A_cytokines.csv', index=False)
for tp, x in t8b.groupby('panel', sort=False):
    print(tp); print(x.pivot(index='analyte', columns='group', values='geo_fold').loc[['Ifnb1', 'Il6', 'Ccl2', 'Ccl3', 'Ccl5', 'Tnf', 'Il10'],
          ['PBS', 'CMP-204', 'PSLN-212', 'PSLN-R848', 'PSLN-212/R848', 'PSLN-344', 'PSLN-212(y)']].round(2).to_string())
# contrasts at "72h": PSLN-344 vs PBS, vs PSLN-212, vs young
rows = []
for blk, tp in [('S09-A(cols A-V)', '16h'), ('S09-A(cols X-AS)', '72h*')]:
    x = sc[sc.block == blk]
    for f in x.factor.unique():
        y = {g: z.value.values for g, z in x[x.factor == f].groupby('group')}
        for a, b in [('PSLN-344', 'PBS'), ('PSLN-344', 'PSLN-212'), ('PSLN-344', 'PSLN-212(y)'), ('PSLN-212(y)', 'PBS'), ('PSLN-212/R848', 'PBS'), ('PSLN-212', 'PBS')]:
            rows.append(dict(panel=tp, analyte=f, a=a, b=b, fold_a_over_b=10 ** (y[a].mean() - y[b].mean()), p_welch=stats.ttest_ind(y[a], y[b], equal_var=False).pvalue,
                             p_student=stats.ttest_ind(y[a], y[b]).pvalue))
t8c = pd.DataFrame(rows); t8c.to_csv(f'{T}/T08c_S09A_contrasts.csv', index=False)
print(t8c[(t8c.a == 'PSLN-344')].to_string())

# ---------- S10-A ----------
print('=' * 90); print('S10-A CNS transcripts, 36 h (linear, relative to untreated)')
x = sc[sc.block == 'S10-A']; rows = []
for f in ['Ifnb1', 'Tnf', 'Isg15']:
    y = {g: z.value.values for g, z in x[x.factor == f].groupby('group', sort=False)}
    res = pairwise_tukeyhsd(np.concatenate(list(y.values())), np.concatenate([[g] * len(v) for g, v in y.items()]))
    tuk = {frozenset((r[0], r[1])): r[3] for r in res.summary().data[1:]}
    for a, b in [('PSLN-344', 'PBS'), ('PSLN-344', 'Sham'), ('CT', 'PBS'), ('Sham', 'PBS'), ('CT', 'PSLN-344')]:
        diff = y[a].mean() - y[b].mean()
        se = np.sqrt(y[a].var(ddof=1) / len(y[a]) + y[b].var(ddof=1) / len(y[b]))
        dfw = se ** 4 / ((y[a].var(ddof=1) / len(y[a])) ** 2 / (len(y[a]) - 1) + (y[b].var(ddof=1) / len(y[b])) ** 2 / (len(y[b]) - 1))
        ci = stats.t.ppf(0.975, dfw) * se
        rows.append(dict(analyte=f, a=a, b=b, mean_a=y[a].mean(), sd_a=y[a].std(ddof=1), mean_b=y[b].mean(), sd_b=y[b].std(ddof=1), ratio=y[a].mean() / y[b].mean(),
                         diff=diff, diff_ci95_lo=diff - ci, diff_ci95_hi=diff + ci, p_tukey=tuk[frozenset((a, b))],
                         p_welch=stats.ttest_ind(y[a], y[b], equal_var=False).pvalue, p_mwu_exact=stats.mannwhitneyu(y[a], y[b], method='exact').pvalue))
t8d = pd.DataFrame(rows); t8d.to_csv(f'{T}/T08d_S10A_CNS.csv', index=False); print(t8d.to_string())
# minimum detectable fold-change given the observed SD (n=5/group, alpha .05 two-sided, 80% power) for PSLN-344 vs PBS
from statsmodels.stats.power import TTestIndPower
for f in ['Ifnb1', 'Tnf', 'Isg15']:
    y = {g: z.value.values for g, z in x[x.factor == f].groupby('group', sort=False)}
    sp = np.sqrt((y['PSLN-344'].var(ddof=1) + y['PBS'].var(ddof=1)) / 2)
    es = TTestIndPower().solve_power(nobs1=5, alpha=0.05, power=0.8, ratio=1)
    print(f'  {f}: pooled SD {sp:.2f}; with n=5/arm the design had 80% power only for a difference >= {es * sp:.2f} (i.e. >= {1 + es * sp / y["PBS"].mean():.1f}-fold over PBS)')

# ---------- S08-A dose-response ----------
print('=' * 90); print('S08-A Ifnb1 dose-response (16 h, no vaccine)')
x = sc[sc.block == 'S08-A'].copy(); x['dose'] = x.factor.astype(float)
tab = x.groupby(['group', 'dose']).value.agg(['mean', 'std', 'count']).unstack('group'); print(tab['mean'].round(2).to_string())
def hill(dose, emax, ed50, h): return 1 + (emax - 1) * dose ** h / (ed50 ** h + dose ** h)
rows = []
for g, y in x.groupby('group', sort=False):
    try:
        p, cov = optimize.curve_fit(hill, y.dose, y.value, p0=[y.value.max(), 10, 2], bounds=([1, 0.5, 0.3], [500, 200, 8]), maxfev=20000)
        bs = []
        for _ in range(2000):
            yy = y.groupby('dose', group_keys=False).apply(lambda z: z.sample(len(z), replace=True, random_state=int(rng.integers(1e9))))
            try:
                q, _ = optimize.curve_fit(hill, yy.dose, yy.value, p0=p, bounds=([1, 0.5, 0.3], [500, 200, 8]), maxfev=20000); bs.append(q)
            except Exception: pass
        bs = np.array(bs); lo, hi = np.percentile(bs, [2.5, 97.5], axis=0)
        m = y.groupby('dose').value.mean()
        rows.append(dict(group=g, Emax_fold=p[0], Emax_ci=f'{lo[0]:.1f}-{hi[0]:.1f}', ED50_ug=p[1], ED50_ci=f'{lo[1]:.1f}-{hi[1]:.1f}', hill=p[2],
                         obs_1ug=m[1], obs_5ug=m[5], obs_10ug=m[10], obs_20ug=m[20], obs_40ug=m[40], ratio_40_over_20=m[40] / m[20],
                         pct_of_40ug_at_5ug=100 * m[5] / m[40], pct_of_40ug_at_10ug=100 * m[10] / m[40], pct_of_40ug_at_20ug=100 * m[20] / m[40]))
    except Exception as e:
        print('fit failed', g, e)
t8e = pd.DataFrame(rows); t8e.to_csv(f'{T}/T08e_S08A_dose_response.csv', index=False); print(t8e.to_string())

# ---------- S08-B encapsulation ----------
print('=' * 90); print('S08-B encapsulation efficiency (%)')
x = sc[sc.block == 'S08-B']; print(x.groupby('group', sort=False).value.agg(['mean', 'std', 'min', 'max', 'count']).round(1).to_string())
y = {g: z.value.values for g, z in x.groupby('group')}
print('  PSLN-344 vs PSLN-212 Welch p =', round(stats.ttest_ind(y['PSLN-344'], y['PSLN-212'], equal_var=False).pvalue, 3))
