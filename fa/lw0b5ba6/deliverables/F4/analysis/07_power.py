#!/usr/bin/env python
"""
07_power.py -- sample-size planning for the proposed replication / attribution study (Study 1) using effect sizes
observed in this dataset. Run: micromamba run -n core python 07_power.py
  * survival endpoint: exact power of two-sided Fisher's exact test (alpha 0.05) by full enumeration
  * titre endpoint: two-sample t-test on log10 titres, SD taken from S03-C/G/D/H (pooled within-group SD)
Output: tables/T11_power.csv
"""
import os, numpy as np, pandas as pd
from scipy import stats
from statsmodels.stats.power import TTestIndPower
HERE = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(HERE, 'tables')
sc = pd.read_csv(os.path.join(HERE, 'parsed', 'scalar_long.csv'), keep_default_na=False)

def fisher_power(p1, p0, n, alpha=0.05):
    pw = 0.0
    for a in range(n + 1):
        pa = stats.binom.pmf(a, n, p1)
        if pa < 1e-12: continue
        for b in range(n + 1):
            pb = stats.binom.pmf(b, n, p0)
            if pb < 1e-12: continue
            if stats.fisher_exact([[a, n - a], [b, n - b]])[1] <= alpha: pw += pa * pb
    return pw

rows = []
scen = [('observed pooled effect (92% vs 18%)', 0.92, 0.18), ('conservative (85% vs 30%)', 0.85, 0.30), ('more conservative (80% vs 35%)', 0.80, 0.35),
        ('weight-table-adjusted (88% vs 20%)', 0.88, 0.20), ('pessimistic (75% vs 40%)', 0.75, 0.40)]
for name, p1, p0 in scen:
    for n in [7, 8, 10, 12, 14, 15, 16, 18, 20, 24, 30]:
        rows.append(dict(endpoint='survival (Fisher exact, 2-sided 0.05)', scenario=name, p_test=p1, p_ref=p0, n_per_arm=n, power=round(fisher_power(p1, p0, n), 3)))
# titres
sds = []
for b in ['S03-C', 'S03-G', 'S03-D', 'S03-H', 'S03-A', 'S03-E']:
    d = sc[sc.block == b].copy(); d['y'] = np.log10(d.value.where(d.value > 0, 5.0))
    sds.append((b, np.sqrt(d.groupby('group').y.var(ddof=1).mean())))
print('pooled within-group SD of log10 titre:', [(b, round(s, 3)) for b, s in sds])
sd = max(s for b, s in sds if b in ('S03-C', 'S03-G', 'S03-D', 'S03-H'))
for fold in [2, 4, 8]:
    es = np.log10(fold) / sd
    for pw in [0.8, 0.9]:
        n = TTestIndPower().solve_power(effect_size=es, alpha=0.05, power=pw)
        rows.append(dict(endpoint=f'HAI/neutralising GMT ratio (t-test on log10, SD={sd:.2f})', scenario=f'{fold}-fold difference', p_test=np.nan, p_ref=np.nan,
                         n_per_arm=int(np.ceil(n)), power=pw))
t = pd.DataFrame(rows); t.to_csv(os.path.join(T, 'T11_power.csv'), index=False)
pd.set_option('display.width', 200); pd.set_option('display.max_rows', 200)
print(t[t.endpoint.str.startswith('survival')].pivot(index='n_per_arm', columns='scenario', values='power').to_string())
print(t[~t.endpoint.str.startswith('survival')].to_string())
# what the existing n=7 design could detect
print('power of the existing n=7 design:', {s: round(fisher_power(p1, p0, 7), 2) for s, p1, p0 in scen})
