#!/usr/bin/env python
"""
Step 8 - (a) leave-out sensitivity of the pooled aged-animal survival result to the data-integrity flags,
         (b) durability and early-protection contrasts, (c) weight at death: challenged PSLN-344 vs unchallenged untreated,
         (d) sample sizes for the proposed confirmatory studies, using the effect sizes observed in this dataset.
Run in `core` env.  Output: stats/sensitivity_power.txt, stats/survival_sensitivity.csv, stats/power_table.csv
"""
import pandas as pd, numpy as np, itertools
from scipy import stats
from statsmodels.stats.contingency_tables import StratifiedTable
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 500)
O = "/tmp/outputs/analysis/stats"
A = pd.read_csv(f"{O}/survival_by_arm.csv", keep_default_na=False)
D = pd.read_csv("/tmp/outputs/analysis/integrity/D_bodyweight_animal_status.csv", keep_default_na=False)
out = open(f"{O}/sensitivity_power.txt", "w")
def P(*a):
    m = " ".join(str(x) for x in a); print(m); out.write(m + "\n")
def cp(k, n):
    lo = 0.0 if k == 0 else stats.beta.ppf(0.025, k, n - k + 1); hi = 1.0 if k == n else stats.beta.ppf(0.975, k + 1, n - k)
    return 100 * lo, 100 * hi
def arm(block, grp):
    r = A[(A.block == block) & (A.group == grp)].iloc[0]; return int(r.survivors), int(r.n)

strata = [(b, b, "PSLN-344", "PSLN-212", "Sham") for b in ["S03-I", "S03-J", "S06-A", "S06-B", "S06-C", "S06-D", "S06-E", "S06-F", "S06-G", "S15-L", "S15-N"]]
strata += [("S06-E(2) naive", "S06-E(2) imprinting/PR8", "Naive+PSLN-344", "Naive+PSLN-212", None),
           ("S06-E(2) imprinted", "S06-E(2) imprinting/PR8", "Imprinting+PSLN-344", "Imprinting+PSLN-212", None),
           ("S06-F(2) naive", "S06-F(2) imprinting/Perth", "Naive+PSLN-344", "Naive+PSLN-212", None),
           ("S06-F(2) imprinted", "S06-F(2) imprinting/Perth", "Imprinting+PSLN-344", "Imprinting+PSLN-212", None),
           ("S15-H", "S15-H", "3d Vaccine+PSLN-344", None, "3d Vaccine")]
FLAGS = {  # integrity flags touching the time-to-event block or its paired body-weight block (see integrity report)
 "S03-I": "PSLN-212 arm: 0/7 in S03-I vs 3/7 implied by S13-F; group sets differ (CMP-204 vs Naive)",
 "S03-J": "stated n=9 vs 10 rows; one PSLN-344 row has no time; control-arm labels differ from S13-G",
 "S06-C": "Sham and PSLN-212 arms identical to S06-D; S15-C PSLN-344 weights duplicated in S15-I; S15-C PSLN-212 1/7 vs 2/7",
 "S06-D": "Sham and PSLN-212 arms identical to S06-C; S15-D implies 5/7 for PSLN-344 and for PSLN-212(Y)",
 "S06-E": "S15-E implies PSLN-212 1/7 (vs 0/7) and PSLN-344 6/7 (vs 5/7)",
 "S06-G": "S15-G implies PSLN-344 5/7 (vs 4/7)",
 "S15-L": "S15-M weights share series with S15-A, S15-C and S09-E; young arm 6/7 vs 7/7; challenge virus not stated",
 "S15-H": "S15-I Vaccine+PSLN-344 weights duplicate S15-C PSLN-344",
 "S15-N": "challenge virus not stated (survival and weight blocks agree)",
}
def pooled(keep, comp):
    tabs = []; k1 = n1 = k0 = n0 = 0
    for lab, blk, a344, a212, asham in strata:
        if not keep(lab, blk): continue
        c = a212 if comp == "212" else asham
        if c is None: continue
        a = arm(blk, a344); b = arm(blk, c)
        tabs.append(np.array([[a[0], a[1] - a[0]], [b[0], b[1] - b[0]]])); k1 += a[0]; n1 += a[1]; k0 += b[0]; n0 += b[1]
    st = StratifiedTable(tabs); t = st.test_null_odds(correction=False)
    return len(tabs), k1, n1, k0, n0, stats.chi2.sf(t.statistic, 1)
rows = []
subsets = {
 "all aged experiments (as printed)": lambda lab, blk: True,
 "excluding S06-D (arms duplicate S06-C)": lambda lab, blk: blk != "S06-D",
 "excluding every experiment with any integrity flag": lambda lab, blk: blk not in FLAGS or blk == "S15-N",
 "20-month BALB/c only (S03, S06-A..G)": lambda lab, blk: blk in ["S03-I", "S03-J", "S06-A", "S06-B", "S06-C", "S06-D", "S06-E", "S06-F", "S06-G"],
 "heterosubtypic d14 only (S06-A, S06-C)": lambda lab, blk: blk in ["S06-A", "S06-C"],
 "early d2-d3 only (S03-J, S06-B, S06-D, S15-H)": lambda lab, blk: blk in ["S03-J", "S06-B", "S06-D", "S15-H"],
 "durable d60 only (S06-E, S06-F, S06-G)": lambda lab, blk: blk in ["S06-E", "S06-F", "S06-G"],
 "other strains (S15-L C57BL/6, S15-N Swiss Webster)": lambda lab, blk: blk in ["S15-L", "S15-N"],
 "14-month, +/- imprinting (S06-E(2), S06-F(2))": lambda lab, blk: "(2)" in blk,
}
for name, keep in subsets.items():
    for comp in ["212", "sham"]:
        try:
            ns, k1, n1, k0, n0, p = pooled(keep, comp)
        except Exception as e:
            continue
        l1, h1 = cp(k1, n1); l0, h0 = cp(k0, n0)
        rows.append(dict(subset=name, comparator="PSLN-212 (aged)" if comp == "212" else "Sham / vaccine alone", strata=ns, psln344=f"{k1}/{n1}", psln344_pct=round(100 * k1 / n1, 1),
                         psln344_ci95=f"{l1:.0f}-{h1:.0f}", comparator_surv=f"{k0}/{n0}", comparator_pct=round(100 * k0 / n0, 1), comparator_ci95=f"{l0:.0f}-{h0:.0f}", cmh_p=p))
S = pd.DataFrame(rows); S.to_csv(f"{O}/survival_sensitivity.csv", index=False)
P("(a) POOLED SURVIVAL IN AGED ANIMALS - SENSITIVITY TO SUBSETS (time-to-event blocks as printed; CMH stratified by experiment)")
P(S.to_string(index=False, float_format=lambda v: f"{v:.2g}"))
P("\nIntegrity flags used for the 'no flag' subset:"); [P(f"   {k}: {v}") for k, v in FLAGS.items()]

P("\n(b) DURABILITY / TIMING CONTRASTS FOR PSLN-344 IN AGED BALB/c (time-to-event blocks)")
def fis(a, b): return stats.fisher_exact([[a[0], a[1] - a[0]], [b[0], b[1] - b[0]]])[1]
d14 = (20, 21); d60 = (14, 21); early = (28, 31); unt = (17, 21); d14m = (13, 14); d60m = (10, 14)
P(f"   d14 (S03-I, S06-A, S06-C) 20/21 vs d60 (S06-E, S06-F, S06-G) 14/21: Fisher p = {fis(d14, d60):.3f}")
P(f"   matched models only: d14 S06-A + S06-C 13/14 vs d60 S06-E + S06-F 10/14: Fisher p = {fis(d14m, d60m):.3f}")
P(f"   d60 PSLN-344 challenged 14/21 vs untreated unchallenged 17/21: Fisher p = {fis(d60, unt):.3f}")
P(f"   early d2-d3 28/31 vs d14 20/21: Fisher p = {fis(early, d14):.3f}")
P(f"   young PSLN-212(Y) at d60: 21/21; young PSLN-344Y/PSLN-212Y at d180 (S09-F): 8/8 and 8/8")

P("\n(c) LAST REAL BODY WEIGHT (% of day 0) OF ANIMALS THAT DID NOT SURVIVE, d60 experiments (S15-E, S15-F, S15-G)")
q = D[D.block.isin(["S15-E", "S15-F", "S15-G"]) & (D.status != "complete")].copy()
b = pd.read_csv("/tmp/outputs/analysis/tidy/bodyweight.csv", keep_default_na=False); b["value"] = pd.to_numeric(b["value"], errors="coerce"); b["day"] = b["day"].astype(float)
q["last_real_day"] = q["last_real_day"].astype(float)
q = q.merge(b[["block", "animal", "day", "value", "cell"]], left_on=["block", "animal", "last_real_day"], right_on=["block", "animal", "day"])
for g in ["PSLN-344", "Untreated", "PSLN-212", "Sham"]:
    v = q[q.group == g]
    P(f"   {g:<10} n={len(v)}  last weights: {', '.join(f'{x:.1f}' for x in v.value)}  mean {v.value.mean():.1f}%   cells: {', '.join(v.block + ':' + v.cell)}")
a = q[q.group == "PSLN-344"].value; u = q[q.group == "Untreated"].value
P(f"   PSLN-344 non-survivors vs untreated non-survivors: Welch p = {stats.ttest_ind(a, u, equal_var=False).pvalue:.4f}; Mann-Whitney exact p = {stats.mannwhitneyu(a, u, method='exact').pvalue:.4f}")

P("\n(d) SAMPLE SIZE (per arm) FOR THE PROPOSED STUDIES - two-sided Fisher exact, alpha 0.05, exact power by enumeration")
def power(p1, p0, n):
    pw = 0.0
    for k1 in range(n + 1):
        for k0 in range(n + 1):
            if stats.fisher_exact([[k1, n - k1], [k0, n - k0]])[1] < 0.05:
                pw += stats.binom.pmf(k1, n, p1) * stats.binom.pmf(k0, n, p0)
    return pw
prow = []
for label, p1, p0 in [("PSLN-344 vs PSLN-212, pooled observed (85% vs 14%)", 0.85, 0.14), ("PSLN-344 vs PSLN-212, worst-case reading (83% vs 18%)", 0.83, 0.18),
                      ("PSLN-344 vs an active comparator giving 50% (85% vs 50%)", 0.85, 0.50), ("durability: d14 95% vs d60 67%", 0.95, 0.67),
                      ("durability: 90% vs 67%", 0.90, 0.67)]:
    for n in [8, 10, 12, 15, 20, 25, 30, 40, 50]:
        pw = power(p1, p0, n); prow.append(dict(scenario=label, n_per_arm=n, power=round(pw, 3)))
PT = pd.DataFrame(prow); PT.to_csv(f"{O}/power_table.csv", index=False)
P(PT.pivot(index="scenario", columns="n_per_arm", values="power").to_string())
out.close()
