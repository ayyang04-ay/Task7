#!/usr/bin/env python
"""
Step 5 - Pooled survival in AGED animals (vaccine + adjuvant arms), stratified by experiment, under
three readings of the workbook:
   TTE   = time-to-event blocks as printed (primary)
   BW    = survivors implied by the paired body-weight block (animal alive = real, non-frozen reading on the last day)
   WORST = worst case for PSLN-344: min(TTE,BW) for PSLN-344, max(TTE,BW) for the comparator
Run in `core` env.  Output: stats/survival_pooled.csv, stats/survival_pooled.txt, stats/survival_reconciliation.csv
"""
import pandas as pd, numpy as np, os
from scipy import stats
from statsmodels.stats.contingency_tables import StratifiedTable
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 2000); pd.set_option("display.max_columns", 40)
O = "/tmp/outputs/analysis/stats"
A = pd.read_csv(f"{O}/survival_by_arm.csv", keep_default_na=False)
D = pd.read_csv("/tmp/outputs/analysis/integrity/D_bodyweight_animal_status.csv", keep_default_na=False)
s = pd.read_csv("/tmp/outputs/analysis/tidy/survival.csv", keep_default_na=False); s["time"] = pd.to_numeric(s["time"], errors="coerce")
out = open(f"{O}/survival_pooled.txt", "w")
def P(*a):
    m = " ".join(str(x) for x in a); print(m); out.write(m + "\n")

BW_OF = {"S03-I": "S13-F", "S03-J": "S13-G", "S06-A": "S15-A", "S06-B": "S15-B", "S06-C": "S15-C", "S06-D": "S15-D", "S06-E": "S15-E", "S06-F": "S15-F",
         "S06-G": "S15-G", "S06-E(2) imprinting/PR8": "S15-J", "S06-F(2) imprinting/Perth": "S15-K", "S15-H": "S15-I", "S15-L": "S15-M", "S15-N": "S15-O",
         "S09-B": "S09-C", "S09-D": "S09-E", "S09-F": "S09-G"}
def bw_surv(bwblk, grp):
    q = D[(D.block == bwblk) & (D.group == grp)]
    if not len(q): return None
    return int((q.status == "complete").sum()), len(q), int(q.status.str.contains(r"\?").sum())

# ---------------- reconciliation table (all arms, all experiments)
rec = []
for _, r in A.iterrows():
    bwblk = BW_OF.get(r.block)
    b = bw_surv(bwblk, r.group) if bwblk else None
    # timing: TTE death days vs body-weight last real day (death expected within 2 days after the last real weight)
    tte_days = sorted(int(x) for x in str(r.death_days).split()) if str(r.death_days).strip() else []
    bw_last = sorted(float(x) for x in D[(D.block == bwblk) & (D.group == r.group) & (D.status != "complete")].last_real_day) if bwblk else []
    timing_ok = ""
    if b is not None and len(tte_days) == len(bw_last) and len(tte_days) > 0:
        timing_ok = "yes" if all(l <= t <= l + 2 for t, l in zip(tte_days, bw_last)) else "no"
    rec.append(dict(tte_block=r.block, bw_block=bwblk or "", group=r.group, tte_survivors=f"{r.survivors}/{r.n}",
                    bw_survivors=(f"{b[0]}/{b[1]}" if b else "group absent"), tte_death_days=" ".join(map(str, tte_days)),
                    bw_last_real_day_of_nonsurvivors=" ".join(f"{int(x)}" for x in bw_last),
                    survivors_agree=("" if b is None else ("yes" if (b[0] == r.survivors and b[1] == r.n) else "NO")), death_timing_compatible=timing_ok))
REC = pd.DataFrame(rec); REC.to_csv(f"{O}/survival_reconciliation.csv", index=False)
P("SURVIVAL (time-to-event block) vs BODY-WEIGHT-IMPLIED SURVIVAL, every arm"); P(REC.to_string(index=False))

# ---------------- pooled, aged, vaccine+adjuvant arms
AGED = ["S03-I", "S03-J", "S06-A", "S06-B", "S06-C", "S06-D", "S06-E", "S06-F", "S06-G", "S15-L", "S15-N"]
strata = []   # (label, block, arm344, arm212, armSham)
for b in AGED: strata.append((b, b, "PSLN-344", "PSLN-212", "Sham"))
strata.append(("S06-E(2) naive", "S06-E(2) imprinting/PR8", "Naive+PSLN-344", "Naive+PSLN-212", None))
strata.append(("S06-E(2) imprinted", "S06-E(2) imprinting/PR8", "Imprinting+PSLN-344", "Imprinting+PSLN-212", None))
strata.append(("S06-F(2) naive", "S06-F(2) imprinting/Perth", "Naive+PSLN-344", "Naive+PSLN-212", None))
strata.append(("S06-F(2) imprinted", "S06-F(2) imprinting/Perth", "Imprinting+PSLN-344", "Imprinting+PSLN-212", None))
strata.append(("S15-H", "S15-H", "3d Vaccine+PSLN-344", None, "3d Vaccine"))

def get(block, grp, reading):
    r = A[(A.block == block) & (A.group == grp)].iloc[0]; tte = (int(r.survivors), int(r.n))
    b = bw_surv(BW_OF.get(block), grp)
    if reading == "TTE" or b is None: return tte
    if reading == "BW": return (b[0], b[1])
    return tte, (b[0], b[1])

rows = []
for lab, blk, a344, a212, asham in strata:
    row = dict(stratum=lab)
    for nm, arm in [("344", a344), ("212", a212), ("sham", asham)]:
        if arm is None: continue
        t = get(blk, arm, "TTE"); b = get(blk, arm, "BW")
        row[f"{nm}_TTE"] = t; row[f"{nm}_BW"] = b
        row[f"{nm}_WORST"] = (min(t[0], b[0]), t[1]) if nm == "344" else (max(t[0], b[0]), t[1])
    rows.append(row)
PO = pd.DataFrame(rows)
def fmt(x): return "" if not isinstance(x, tuple) else f"{x[0]}/{x[1]}"
P("\nPER-STRATUM SURVIVORS (aged animals; vaccine + adjuvant)"); P(PO.map(fmt).to_string(index=False))
PO.map(fmt).to_csv(f"{O}/survival_pooled_strata.csv", index=False)

def cp(k, n):
    lo = 0.0 if k == 0 else stats.beta.ppf(0.025, k, n - k + 1); hi = 1.0 if k == n else stats.beta.ppf(0.975, k + 1, n - k)
    return 100 * lo, 100 * hi
res = []
for reading in ["TTE", "BW", "WORST"]:
    for comp in ["212", "sham"]:
        tabs = []; k1 = n1 = k0 = n0 = 0
        for _, r in PO.iterrows():
            a, b = r.get(f"344_{reading}"), r.get(f"{comp}_{reading}")
            if not isinstance(a, tuple) or not isinstance(b, tuple): continue
            tabs.append(np.array([[a[0], a[1] - a[0]], [b[0], b[1] - b[0]]])); k1 += a[0]; n1 += a[1]; k0 += b[0]; n0 += b[1]
        st = StratifiedTable(tabs)
        cmh = st.test_null_odds(correction=False)
        l1, h1 = cp(k1, n1); l0, h0 = cp(k0, n0)
        res.append(dict(reading=reading, comparator={"212": "PSLN-212 (aged)", "sham": "Sham / vaccine alone (aged)"}[comp], n_strata=len(tabs),
                        psln344=f"{k1}/{n1}", psln344_pct=100 * k1 / n1, psln344_ci=f"{l1:.0f}-{h1:.0f}",
                        comparator_surv=f"{k0}/{n0}", comparator_pct=100 * k0 / n0, comparator_ci=f"{l0:.0f}-{h0:.0f}",
                        cmh_chi2=cmh.statistic, cmh_p=stats.chi2.sf(cmh.statistic, 1), mh_risk_diff_pct=100 * (sum(t[0, 0] * t[1].sum() / t.sum() for t in tabs) - sum(t[1, 0] * t[0].sum() / t.sum() for t in tabs)) / sum(t[0].sum() * t[1].sum() / t.sum() for t in tabs)))
RES = pd.DataFrame(res); RES.to_csv(f"{O}/survival_pooled.csv", index=False)
P("\nPOOLED SURVIVAL, AGED ANIMALS, stratified by experiment (Cochran-Mantel-Haenszel)"); P(RES.to_string(index=False, float_format=lambda v: f"{v:.3g}"))

# ---------------- stratified log-rank on the TTE blocks (primary reading)
def logrank_OE(t1, e1, t2, e2):
    t = np.concatenate([t1, t2]); e = np.concatenate([e1, e2]); g = np.concatenate([np.ones(len(t1)), np.zeros(len(t2))]); OE = V = 0.0
    for tt in np.unique(t[e == 1]):
        at = t >= tt; n = at.sum(); n1 = (at & (g == 1)).sum(); d = ((t == tt) & (e == 1)).sum(); d1 = ((t == tt) & (e == 1) & (g == 1)).sum()
        OE += d1 - d * n1 / n
        if n > 1: V += d * (n1 / n) * (1 - n1 / n) * (n - d) / (n - 1)
    return OE, V
P("\nSTRATIFIED LOG-RANK (time-to-event blocks as printed)")
for comp in ["212", "sham"]:
    OE = V = 0; k = 0
    for lab, blk, a344, a212, asham in strata:
        arm = a212 if comp == "212" else asham
        if arm is None: continue
        qa = s[(s.block == blk) & (s.group == a344)].dropna(subset=["time"]); qb = s[(s.block == blk) & (s.group == arm)].dropna(subset=["time"])
        oe, v = logrank_OE(qa.time.values, qa.event.values, qb.time.values, qb.event.values); OE += oe; V += v; k += 1
    chi = OE ** 2 / V
    P(f"   PSLN-344 vs {'PSLN-212 (aged)' if comp=='212' else 'Sham / vaccine alone'}: strata={k}  O-E={OE:.1f}  V={V:.1f}  chi2={chi:.1f}  p={stats.chi2.sf(chi,1):.2e}  hazard ratio (Peto) = {np.exp(OE/V):.3f} [{np.exp(OE/V-1.96/np.sqrt(V)):.3f}-{np.exp(OE/V+1.96/np.sqrt(V)):.3f}]")

# ---------------- day-60 experiments vs unchallenged untreated animals
P("\nDAY-60 CHALLENGES vs UNCHALLENGED, UNTREATED AGED ANIMALS (S06-E, S06-F, S06-G)")
for grp in ["Sham", "PSLN-212", "PSLN-344", "PSLN-212(Y)", "Untreated"]:
    q = A[A.block.isin(["S06-E", "S06-F", "S06-G"]) & (A.group == grp)]
    k, n = int(q.survivors.sum()), int(q.n.sum()); lo, hi = cp(k, n)
    P(f"   {grp:<12} {k}/{n} = {100*k/n:.0f}%  (95% CI {lo:.0f}-{hi:.0f})   per experiment: {', '.join(f'{a}/{b}' for a,b in zip(q.survivors,q.n))}   death days: {' | '.join(q.death_days.astype(str))}")
k344, n344 = 14, 21; ku, nu = 17, 21
P("   Fisher exact PSLN-344 (14/21) vs Untreated-unchallenged (17/21): p =", round(stats.fisher_exact([[14, 7], [17, 4]])[1], 3))
P("   Fisher exact PSLN-344 d60 (14/21) vs PSLN-344 d14 same models S06-A,S06-C (13/14): p =", round(stats.fisher_exact([[14, 7], [13, 1]])[1], 3))
# early (d2-d3) vs d14
P("\nEARLY (d2/d3) vs d14 vs d60, PSLN-344 aged BALB/c, TTE blocks")
for lab, blks in [("d2-d3", ["S03-J", "S06-B", "S06-D", "S15-H"]), ("d14", ["S03-I", "S06-A", "S06-C"]), ("d60", ["S06-E", "S06-F", "S06-G"])]:
    q = A[A.block.isin(blks) & A.group.isin(["PSLN-344", "3d Vaccine+PSLN-344"])]
    k, n = int(q.survivors.sum()), int(q.n.sum()); lo, hi = cp(k, n); P(f"   {lab:<6} {k}/{n} = {100*k/n:.0f}% (95% CI {lo:.0f}-{hi:.0f})  blocks {blks}")
out.close()
