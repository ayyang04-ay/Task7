#!/usr/bin/env python
"""
Step 4 - Time-to-event analysis (run in the `core` env: lifelines).

Per block: survivors / n per arm with exact (Clopper-Pearson) 95% CI, median survival, log-rank p
(asymptotic, cross-checked with lifelines, plus an exact permutation p because arms are n = 7-10),
Fisher exact on end-of-observation survival.
Pooled: PSLN-344 vs PSLN-212 vs Sham in aged animals, stratified by experiment (stratified log-rank and
Mantel-Haenszel), under three readings of the data:
   (1) time-to-event blocks as printed (primary)
   (2) survivors implied by the paired body-weight block
   (3) worst case for PSLN-344 = min(1,2) for PSLN-344 and max(1,2) for the comparator
Outputs: stats/survival_by_arm.csv, stats/survival_pairwise.csv, stats/survival_pooled.txt
"""
import pandas as pd, numpy as np, itertools, os, math
from scipy import stats
from lifelines.statistics import logrank_test
from lifelines import KaplanMeierFitter
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 2000); pd.set_option("display.max_columns", 40)
T = "/tmp/outputs/analysis/tidy"; O = "/tmp/outputs/analysis/stats"; os.makedirs(O, exist_ok=True)
s = pd.read_csv(f"{T}/survival.csv", keep_default_na=False); s["time"] = pd.to_numeric(s["time"], errors="coerce")

# --- experiment registry: design facts transcribed from the annotation PDF (page refs in the proposal appendix)
REG = {
 "S03-I": dict(age="aged BALB/c", vaccine="bivalent (CA09 H1N1 + Aichi H3N2)", challenge="10x mLD50 CA09 H1N1", interval="d14", match="homologous", bw="S13-F"),
 "S03-J": dict(age="aged", vaccine="rgH5N1, single dose", challenge="wild-type VN04 H5N1 (dose not stated)", interval="d2", match="homologous (H5N1), early", bw="S13-G"),
 "S06-A": dict(age="aged BALB/c", vaccine="Aichi H3N2", challenge="5x mLD50 PR8 H1N1", interval="d14", match="heterosubtypic", bw="S15-A"),
 "S06-B": dict(age="aged BALB/c", vaccine="Aichi H3N2", challenge="5x mLD50 PR8 H1N1", interval="d3", match="heterosubtypic, early", bw="S15-B"),
 "S06-C": dict(age="aged BALB/c", vaccine="bivalent", challenge="5x mLD50 rgH5N1", interval="d14", match="heterosubtypic", bw="S15-C"),
 "S06-D": dict(age="aged BALB/c", vaccine="bivalent", challenge="5x mLD50 rgH5N1", interval="d3", match="heterosubtypic, early", bw="S15-D"),
 "S06-E": dict(age="aged BALB/c", vaccine="Aichi H3N2", challenge="5x mLD50 PR8 H1N1", interval="d60", match="heterosubtypic, durable", bw="S15-E"),
 "S06-F": dict(age="aged BALB/c", vaccine="bivalent", challenge="5x mLD50 rgH5N1", interval="d60", match="heterosubtypic, durable", bw="S15-F"),
 "S06-G": dict(age="aged BALB/c", vaccine="CA09 H1N1", challenge="5x mLD50 Perth H3N2", interval="d60", match="heterosubtypic, durable", bw="S15-G"),
 "S06-E(2) imprinting/PR8": dict(age="14-month BALB/c (10 mo + 4 mo), +/- prior PR8 infection", vaccine="bivalent", challenge="5x LD50 PR8 H1N1", interval="not stated", match="imprinting model", bw="S15-J"),
 "S06-F(2) imprinting/Perth": dict(age="14-month BALB/c (10 mo + 4 mo), +/- prior PR8 infection", vaccine="bivalent", challenge="5x LD50 Perth H3N2", interval="d14", match="imprinting model", bw="S15-K"),
 "S15-H": dict(age="aged BALB/c", vaccine="bivalent / none", challenge="5x mLD50 VN04 rgH5N1", interval="d3", match="component control, early", bw="S15-I"),
 "S15-L": dict(age="aged C57BL/6 (20 mo)", vaccine="bivalent", challenge="not stated", interval="not stated", match="second inbred strain", bw="S15-M"),
 "S15-N": dict(age="aged Swiss Webster (20 mo)", vaccine="bivalent", challenge="not stated", interval="not stated", match="outbred strain", bw="S15-O"),
 "S09-B": dict(age="young BALB/c", vaccine="Aichi H3N2", challenge="5x mLD50 PR8 H1N1", interval="d21", match="heterosubtypic", bw="S09-C"),
 "S09-D": dict(age="young BALB/c", vaccine="CA09 H1N1", challenge="5x mLD50 Perth H3N2", interval="d21", match="heterosubtypic", bw="S09-E"),
 "S09-F": dict(age="young BALB/c", vaccine="bivalent", challenge="5x mLD50 VN04 rgH5N1", interval="d180", match="heterosubtypic, durable", bw="S09-G"),
 "S13-E": dict(age="young BALB/c", vaccine="as S03-I", challenge="10x mLD50 CA09 H1N1", interval="d14", match="homologous", bw=None),
}

def cp(k, n, a=0.05):
    lo = 0.0 if k == 0 else stats.beta.ppf(a / 2, k, n - k + 1); hi = 1.0 if k == n else stats.beta.ppf(1 - a / 2, k + 1, n - k)
    return lo, hi

def logrank_OE(t1, e1, t2, e2):
    """return (O1 - E1, V) for group 1"""
    t = np.concatenate([t1, t2]); e = np.concatenate([e1, e2]); g = np.concatenate([np.ones(len(t1)), np.zeros(len(t2))])
    OE = V = 0.0
    for tt in np.unique(t[e == 1]):
        at = t >= tt; n = at.sum(); n1 = (at & (g == 1)).sum(); d = ((t == tt) & (e == 1)).sum(); d1 = ((t == tt) & (e == 1) & (g == 1)).sum()
        OE += d1 - d * n1 / n
        if n > 1: V += d * (n1 / n) * (1 - n1 / n) * (n - d) / (n - 1)
    return OE, V

def perm_logrank(t1, e1, t2, e2, max_enum=400000, rng=np.random.default_rng(1)):
    """exact (or Monte-Carlo if too many) two-sided permutation p for the log-rank statistic"""
    t = np.concatenate([t1, t2]); e = np.concatenate([e1, e2]); n1 = len(t1); N = len(t)
    obs, V = logrank_OE(t1, e1, t2, e2)
    if V == 0: return np.nan
    ncomb = math.comb(N, n1)
    def stat(idx):
        m = np.zeros(N, bool); m[list(idx)] = True
        return logrank_OE(t[m], e[m], t[~m], e[~m])[0]
    if ncomb <= max_enum:
        vals = np.array([stat(ix) for ix in itertools.combinations(range(N), n1)])
    else:
        vals = np.array([stat(rng.choice(N, n1, replace=False)) for _ in range(100000)])
    return float((np.abs(vals) >= abs(obs) - 1e-12).mean())

arm_rows, pair_rows = [], []
for blk, g in s.groupby("block", sort=False):
    groups = list(dict.fromkeys(g.group)); reg = REG[blk]
    for grp in groups:
        q = g[g.group == grp]; n = len(q); d = int(q.event.sum()); surv = n - d
        lo, hi = cp(surv, n)
        qq = q.dropna(subset=["time"])
        kmf = KaplanMeierFitter().fit(qq.time, qq.event)
        arm_rows.append(dict(block=blk, **{k: reg[k] for k in ["age", "vaccine", "challenge", "interval", "match"]}, group=grp, n=n, deaths=d, survivors=surv,
                             survival_pct=100 * surv / n, ci95_lo=100 * lo, ci95_hi=100 * hi, median_survival_d=kmf.median_survival_time_,
                             death_days=" ".join(str(int(x)) for x in sorted(qq[qq.event == 1].time)), n_missing_time=int(q.time.isna().sum()),
                             cells=f"{q.sheet.iloc[0]}!{q.cell.iloc[0].split('/')[1]}:{q.cell.iloc[-1].split('/')[1]}"))
    for a, b in itertools.combinations(groups, 2):
        qa, qb = g[(g.group == a)].dropna(subset=["time"]), g[(g.group == b)].dropna(subset=["time"])
        OE, V = logrank_OE(qa.time.values, qa.event.values, qb.time.values, qb.event.values)
        p_asym = stats.chi2.sf(OE ** 2 / V, 1) if V > 0 else np.nan
        p_ll = logrank_test(qa.time, qb.time, qa.event, qb.event).p_value if V > 0 else np.nan
        p_perm = perm_logrank(qa.time.values, qa.event.values, qb.time.values, qb.event.values) if V > 0 else np.nan
        sa, sb = int((g[g.group == a].event == 0).sum()), int((g[g.group == b].event == 0).sum()); na, nb = (g.group == a).sum(), (g.group == b).sum()
        p_f = stats.fisher_exact([[sa, na - sa], [sb, nb - sb]])[1]
        pair_rows.append(dict(block=blk, group_a=a, group_b=b, surv_a=f"{sa}/{na}", surv_b=f"{sb}/{nb}", p_logrank=p_asym, p_logrank_lifelines=p_ll,
                              p_logrank_exact_perm=p_perm, p_fisher=p_f))
A = pd.DataFrame(arm_rows); PW = pd.DataFrame(pair_rows)
A.to_csv(f"{O}/survival_by_arm.csv", index=False); PW.to_csv(f"{O}/survival_pairwise.csv", index=False)
print(A[["block", "age", "vaccine", "challenge", "interval", "group", "n", "survivors", "survival_pct", "ci95_lo", "ci95_hi", "median_survival_d", "death_days", "cells"]].to_string(index=False, float_format=lambda v: f"{v:.0f}"))
print()
key = PW[((PW.group_a.str.contains("344")) | (PW.group_b.str.contains("344")))]
print(key.to_string(index=False, float_format=lambda v: f"{v:.4g}"))
