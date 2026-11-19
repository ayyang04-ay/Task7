"""Exact power / sample-size calculations used for the next-study designs (two-sided Fisher exact, alpha = 0.05)."""
from paths import TABLES, FIGS, OUT as OUTDIR, BUILD, PANDOC
import numpy as np, pandas as pd, math
from scipy import stats
pd.set_option('display.width', 250)
from stats_util import fisher_power, clopper_pearson
def n_for(p1, p0, target=0.9, nmax=80):
    for n in range(4, nmax + 1):
        if fisher_power(p1, p0, n) >= target:
            return n, fisher_power(p1, p0, n)
    return None, None
rows = []
scen = [('Observed effect: PSLN-344 84% vs PSLN-212 12% (T7, excl. S06-D)', 0.84, 0.12),
        ('Conservative planning: 75% vs 25%', 0.75, 0.25),
        ('Attribution arm (e.g. Mn-only or cGAMP+Mn) 80% vs 40%', 0.80, 0.40),
        ('Attribution arm 80% vs 50%', 0.80, 0.50),
        ('Durability: d14 93% vs d60 67% (T8)', 0.93, 0.67),
        ('Sex effect / strain effect 85% vs 55%', 0.85, 0.55)]
for lab, p1, p0 in scen:
    for tgt in (0.8, 0.9):
        n, pw = n_for(p1, p0, tgt)
        rows.append(dict(scenario=lab, p1=p1, p0=p0, target_power=tgt, n_per_group=n, achieved_power=pw))
P = pd.DataFrame(rows); print(P.round(3).to_string())
# what the existing n=7 design could detect
print('\npower of the historical design (n = 7 per group):')
for p1, p0 in [(0.84, 0.12), (0.75, 0.25), (0.8, 0.4), (0.93, 0.67)]:
    print(f'  {p1} vs {p0}: power = {fisher_power(p1, p0, 7):.2f}')
hist = pd.DataFrame([dict(scenario=f'historical n=7: {p1} vs {p0}', p1=p1, p0=p0, target_power=np.nan, n_per_group=7, achieved_power=fisher_power(p1, p0, 7))
                     for p1, p0 in [(0.84, 0.12), (0.75, 0.25), (0.8, 0.4), (0.93, 0.67)]])
# continuous endpoint: weight nadir (pooled SD from T12)
G = pd.read_csv(TABLES + 'T12_weight_nadir_by_group.csv')
sd = G[G.group.isin(['PSLN-344', 'PSLN-212(Y)'])].sd_nadir
pooled_sd = float(np.sqrt((sd ** 2).mean()))
print('\npooled SD of weight nadir (PSLN-344 aged & PSLN-212(Y) groups):', round(pooled_sd, 2))
def n_cont(delta, sd, power=0.8, alpha=0.05, one_sided=False):
    za = stats.norm.ppf(1 - alpha / (1 if one_sided else 2)); zb = stats.norm.ppf(power)
    return math.ceil(2 * (za + zb) ** 2 * (sd / delta) ** 2) + 1
cont = []
for d in (3, 4, 5):
    cont.append(dict(scenario=f'weight-nadir difference / NI margin of {d} points (SD {pooled_sd:.1f})', n_per_group_80=n_cont(d, pooled_sd, 0.8), n_per_group_90=n_cont(d, pooled_sd, 0.9)))
print(pd.DataFrame(cont).to_string())
# precision of background-mortality estimate
for n in (7, 15, 20, 30):
    k = round(0.19 * n); lo, hi = clopper_pearson(k, n); print(f'background mortality 19%: n={n}: {k}/{n} -> 95% CI {100*lo:.0f}-{100*hi:.0f}%')
pd.concat([P, hist]).to_csv(TABLES + 'T16_power_sample_size.csv', index=False)
pd.DataFrame(cont).to_csv(TABLES + 'T16b_power_continuous.csv', index=False)
