#!/usr/bin/env python
"""
Step 3 - Statistics for every continuous block.

For each block / panel / x-level:
  * per-group n, mean, SD, median, geometric mean
  * the method stated in the annotation: one-way ANOVA + Tukey HSD (all pairs)
  * robustness: Welch t-test and exact Mann-Whitney for every pair, on the raw scale and (ratio-type
    readouts: titres, qPCR fold-change) on the log10 scale
  * effect sizes: ratio of means, Hedges g
  * "restoration" of the aged response toward the young benchmark:
        R = (PSLN-344 - PSLN-212) / (PSLN-212(Y) - PSLN-212)       (aged groups unless labelled (Y))
Outputs: stats/continuous_summary.csv, stats/continuous_pairwise.csv, stats/restoration_all_blocks.csv
"""
import pandas as pd, numpy as np, itertools, os, warnings
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
warnings.filterwarnings("ignore")
T = "/tmp/outputs/analysis/tidy"; O = "/tmp/outputs/analysis/stats"; os.makedirs(O, exist_ok=True)
c = pd.read_csv(f"{T}/continuous.csv", keep_default_na=False); c["value"] = c["value"].astype(float)

LOGSCALE_BLOCKS = {  # ratio-scale readouts analysed on log10 as well (titres, qPCR fold-changes, quotients)
    "S01-A", "S02-F", "S03-A", "S03-C", "S03-D", "S03-E", "S03-G", "S03-H", "S03-L", "S08-A", "S10-A",
    "S13-A", "S13-B", "S13-C", "S13-D", "S13-I", "S13-J", "S03-B", "S03-F", "S04-B Tfh:Tfr"}
ALREADY_LOG = {"S09-A"}          # printed on log10 scale
HAI_BLOCKS = {"S03-C", "S03-G"}  # lowest dilution tested 1:10; a printed 0 = below limit -> set to 5 for log analysis

def hedges_g(a, b):
    na, nb = len(a), len(b); sp = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    if sp == 0: return np.nan
    return (a.mean() - b.mean()) / sp * (1 - 3 / (4 * (na + nb) - 9))

summ_rows, pair_rows = [], []
for (block, panel, x), g in c.groupby(["block", "panel", "x"], sort=False):
    groups = list(dict.fromkeys(g["group"]))
    data = {k: g[g.group == k].sort_values("rep")["value"].to_numpy() for k in groups}
    log_ok = block in LOGSCALE_BLOCKS
    def tolog(v):
        v = np.array(v, float)
        if block in HAI_BLOCKS: v = np.where(v <= 0, 5.0, v)
        return np.log10(v)
    for k, v in data.items():
        cells = g[g.group == k]["cell"]
        row = dict(block=block, panel=panel, x=x, group=k, n=len(v), mean=v.mean(), sd=v.std(ddof=1) if len(v) > 1 else np.nan,
                   sem=v.std(ddof=1) / np.sqrt(len(v)) if len(v) > 1 else np.nan, median=np.median(v), min=v.min(), max=v.max(),
                   cells=f"{g['sheet'].iloc[0]}!{cells.iloc[0]}:{cells.iloc[-1]}")
        if block in ALREADY_LOG:
            row["geo_mean"] = 10 ** v.mean(); row["scale_note"] = "printed log10; geo_mean = 10^mean(log10) = fold vs untreated"
        elif log_ok and (np.all(v > 0) or block in HAI_BLOCKS):
            row["geo_mean"] = 10 ** tolog(v).mean(); row["scale_note"] = "linear; geo_mean on log10" + (" (0 -> 5, below 1:10)" if block in HAI_BLOCKS and np.any(v <= 0) else "")
        else:
            row["geo_mean"] = np.nan; row["scale_note"] = "linear"
        summ_rows.append(row)
    # ---- omnibus + Tukey (stated method), raw scale and log scale
    if len(groups) >= 2 and all(len(v) >= 2 for v in data.values()):
        tuk = {}
        for scale in (["raw", "log10"] if log_ok else ["raw"]):
            vals = {k: (tolog(v) if scale == "log10" else v) for k, v in data.items()}
            if len(groups) >= 3:
                F, pA = stats.f_oneway(*vals.values())
                res = pairwise_tukeyhsd(np.concatenate(list(vals.values())), np.concatenate([[k] * len(v) for k, v in vals.items()]))
                for (a, b2), p in zip(itertools.combinations(res.groupsunique, 2), res.pvalues):
                    tuk[(scale, a, b2)] = p; tuk[(scale, b2, a)] = p
            else:
                pA = np.nan
            tuk[(scale, "anova")] = pA
        for a, b2 in itertools.combinations(groups, 2):
            va, vb = data[a], data[b2]
            tw = stats.ttest_ind(va, vb, equal_var=False)
            ts = stats.ttest_ind(va, vb, equal_var=True)
            try: mw = stats.mannwhitneyu(va, vb, alternative="two-sided", method="exact").pvalue
            except Exception: mw = np.nan
            row = dict(block=block, panel=panel, x=x, group_a=a, group_b=b2, n_a=len(va), n_b=len(vb), mean_a=va.mean(), mean_b=vb.mean(),
                       diff=va.mean() - vb.mean(), ratio_of_means=va.mean() / vb.mean() if vb.mean() != 0 else np.nan, hedges_g=hedges_g(va, vb),
                       p_welch=tw.pvalue, p_student=ts.pvalue, p_mannwhitney_exact=mw,
                       anova_p=tuk.get(("raw", "anova"), np.nan), p_tukey=tuk.get(("raw", a, b2), np.nan),
                       no_overlap=bool(va.min() > vb.max() or vb.min() > va.max()))
            if block in ALREADY_LOG:
                d = va.mean() - vb.mean(); row["geo_ratio"] = 10 ** d
            if log_ok and (block in HAI_BLOCKS or (np.all(va > 0) and np.all(vb > 0))):
                la, lb = tolog(va), tolog(vb); d = la.mean() - lb.mean()
                se = np.sqrt(la.var(ddof=1) / len(la) + lb.var(ddof=1) / len(lb))
                df = se ** 4 / ((la.var(ddof=1) / len(la)) ** 2 / (len(la) - 1) + (lb.var(ddof=1) / len(lb)) ** 2 / (len(lb) - 1)) if se > 0 else np.nan
                tcrit = stats.t.ppf(0.975, df) if se > 0 else np.nan
                row.update(geo_ratio=10 ** d, geo_ratio_lo=10 ** (d - tcrit * se) if se > 0 else np.nan, geo_ratio_hi=10 ** (d + tcrit * se) if se > 0 else np.nan,
                           p_welch_log=stats.ttest_ind(la, lb, equal_var=False).pvalue if se > 0 else np.nan,
                           anova_p_log=tuk.get(("log10", "anova"), np.nan), p_tukey_log=tuk.get(("log10", a, b2), np.nan))
            pair_rows.append(row)
S = pd.DataFrame(summ_rows); PW = pd.DataFrame(pair_rows)
S.to_csv(f"{O}/continuous_summary.csv", index=False); PW.to_csv(f"{O}/continuous_pairwise.csv", index=False)

# ---- restoration index for every block/panel/x that has the three groups
rest = []
alias = {"PSLN-212Y": "PSLN-212(Y)", "PSLN-212(y)": "PSLN-212(Y)"}
S2 = S.assign(g2=S.group.replace(alias))
for (block, panel, x), g in S2.groupby(["block", "panel", "x"], sort=False):
    m = dict(zip(g.g2, g["mean"])); gm = dict(zip(g.g2, g["geo_mean"]))
    if all(k in m for k in ["PSLN-212", "PSLN-344", "PSLN-212(Y)"]):
        den = m["PSLN-212(Y)"] - m["PSLN-212"]
        r = dict(block=block, panel=panel, x=x, sham=m.get("Sham", m.get("PBS", m.get("Vaccine", np.nan))), aged_212=m["PSLN-212"], aged_344=m["PSLN-344"], young_212=m["PSLN-212(Y)"],
                 ratio_344_vs_212=m["PSLN-344"] / m["PSLN-212"] if m["PSLN-212"] else np.nan,
                 aged344_pct_of_young=100 * m["PSLN-344"] / m["PSLN-212(Y)"] if m["PSLN-212(Y)"] else np.nan,
                 aged212_pct_of_young=100 * m["PSLN-212"] / m["PSLN-212(Y)"] if m["PSLN-212(Y)"] else np.nan,
                 restoration_pct=100 * (m["PSLN-344"] - m["PSLN-212"]) / den if den else np.nan)
        if not np.isnan(gm.get("PSLN-344", np.nan)):
            r.update(geo_aged_212=gm["PSLN-212"], geo_aged_344=gm["PSLN-344"], geo_young_212=gm["PSLN-212(Y)"],
                     geo_ratio_344_vs_212=gm["PSLN-344"] / gm["PSLN-212"], geo_aged344_pct_of_young=100 * gm["PSLN-344"] / gm["PSLN-212(Y)"])
        rest.append(r)
R = pd.DataFrame(rest); R.to_csv(f"{O}/restoration_all_blocks.csv", index=False)
print("summary rows", len(S), "pairwise rows", len(PW), "restoration rows", len(R))
