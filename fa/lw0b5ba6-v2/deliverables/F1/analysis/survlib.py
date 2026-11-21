"""Helpers for time-to-event analysis (imported by 03_survival.py, 03b_survival_pooled.py and figure scripts).

Time-to-event analysis of every survival block.

Per group : n, deaths, survivors, survival % with exact Clopper-Pearson 95% CI, median time to death.
Pairwise  : log-rank (asymptotic, = stated method), exact permutation log-rank, Fisher exact on end-of-study survival.
Pooled    : stratified (by experiment) log-rank and Mantel-Haenszel risk difference.
Animals whose flag has no day value (S03-J!J46) are analysed as censored at the block's last recorded day
and the sensitivity of every affected number to dropping them is reported.
"""
import itertools, math, json
import numpy as np, pandas as pd
from scipy import stats
from lifelines.statistics import logrank_test
import tidy

pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500); pd.set_option('display.max_colwidth', 60)

SURV = ['S03-I', 'S03-J', 'S06-A', 'S06-B', 'S06-C', 'S06-D', 'S06-E', 'S06-F', 'S06-G', 'S06-E[r71]', 'S06-F[r71]',
        'S09-B', 'S09-D', 'S09-F', 'S13-E', 'S15-H', 'S15-L', 'S15-N']

def cp(k, n, a=0.05):
    lo = 0.0 if k == 0 else stats.beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(1 - a / 2, k + 1, n - k)
    return lo, hi

def lr_stat(time, event, grp):
    """log-rank O-E for group 1 and its hypergeometric variance"""
    time = np.asarray(time, float); event = np.asarray(event, int); grp = np.asarray(grp, int)
    OE = 0.0; V = 0.0
    for t in np.unique(time[event == 1]):
        at = time >= t
        n = at.sum(); n1 = (at & (grp == 1)).sum()
        d = ((time == t) & (event == 1)).sum(); d1 = ((time == t) & (event == 1) & (grp == 1)).sum()
        OE += d1 - d * n1 / n
        if n > 1:
            V += d * (n1 / n) * (1 - n1 / n) * (n - d) / (n - 1)
    return OE, V

def lr_exact(time, event, grp, max_enum=200000, seed=1):
    """exact (or Monte-Carlo if too many) permutation p-value of the log-rank statistic, two-sided"""
    time = np.asarray(time, float); event = np.asarray(event, int); grp = np.asarray(grp, int)
    OE, V = lr_stat(time, event, grp)
    if V == 0:
        return 1.0
    obs = abs(OE)
    n = len(grp); n1 = int(grp.sum())
    total = math.comb(n, n1)
    cnt = 0; tot = 0
    if total <= max_enum:
        for idx in itertools.combinations(range(n), n1):
            g = np.zeros(n, int); g[list(idx)] = 1
            oe, _ = lr_stat(time, event, g)
            cnt += abs(oe) >= obs - 1e-12; tot += 1
    else:
        rng = np.random.default_rng(seed)
        for _ in range(max_enum):
            g = rng.permutation(grp)
            oe, _ = lr_stat(time, event, g)
            cnt += abs(oe) >= obs - 1e-12; tot += 1
    return cnt / tot

def prep(block):
    d = tidy.get(block).copy()
    d['time_missing'] = d['time'].isna()
    tmax = d['time'].max()
    d.loc[d.time_missing, 'time'] = tmax      # censored at last recorded day (flag says 0)
    return d

