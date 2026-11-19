#!/usr/bin/env python
"""
Step 7 - Block-specific analyses that the generic pipeline does not cover.
  a. S08-A  dose-response of lung Ifnb1 (sigmoid Emax fit per formulation, bootstrap CI)
  b. S09-A  cytokine/chemokine panel on the printed log10 scale -> geometric-mean fold, both panels
  c. S11-A vs S11-B  cell-by-cell duplication
  d. time courses (S01-D, S01-E, S02-F, S07-A, S11-A, S11-D): two-way ANOVA (group x day) and peak / AUC
  e. single dose (d14) vs prime-boost (d28) IgG: S03-A/E vs S13-I/J
  f. Mn effect in YOUNG animals (PSLN-344(Y) vs PSLN-212(Y)) wherever both exist
Output: stats/special_analyses.txt (+ csv tables)
"""
import pandas as pd, numpy as np, os, warnings, itertools
from scipy import stats, optimize
import statsmodels.api as sm, statsmodels.formula.api as smf
warnings.filterwarnings("ignore")
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 2000); pd.set_option("display.max_columns", 40)
O = "/tmp/outputs/analysis/stats"
c = pd.read_csv("/tmp/outputs/analysis/tidy/continuous.csv", keep_default_na=False); c["value"] = c["value"].astype(float)
out = open(f"{O}/special_analyses.txt", "w")
def P(*a):
    m = " ".join(str(x) for x in a); print(m); out.write(m + "\n")

# ------------------------------------------------------------------ a. dose-response
P("=" * 100); P("a. S08-A  lung Ifnb1 (fold vs untreated, 16 h) vs dose; sigmoid Emax model  E = 1 + (Emax-1) * D^h / (ED50^h + D^h), fitted on log10(E)"); P("=" * 100)
d = c[c.block == "S08-A"].copy(); d["dose"] = d["x"].astype(float)
P(d.pivot_table(index="dose", columns="group", values="value", aggfunc=["mean", "std"]).round(2).to_string())
def model(D, Emax, ED50, h): return np.log10(1 + (Emax - 1) * D ** h / (ED50 ** h + D ** h))
rng = np.random.default_rng(7); rowsA = []
for g, q in d.groupby("group", sort=False):
    x, y = q.dose.values, np.log10(q.value.values)
    p0 = [q.value.max(), 10, 2]; bnd = ([1.01, 0.5, 0.3], [500, 200, 8])
    popt, _ = optimize.curve_fit(model, x, y, p0=p0, bounds=bnd, maxfev=20000)
    boots = []
    for _ in range(2000):
        idx = np.concatenate([rng.choice(np.where(x == dd)[0], size=(x == dd).sum(), replace=True) for dd in np.unique(x)])
        try:
            pb, _ = optimize.curve_fit(model, x[idx], y[idx], p0=popt, bounds=bnd, maxfev=20000); boots.append(pb)
        except Exception: pass
    boots = np.array(boots); lo, hi = np.percentile(boots, [2.5, 97.5], axis=0)
    e20 = 10 ** model(20.0, *popt); frac20 = (e20 - 1) / (popt[0] - 1)
    m20, m40 = q[q.dose == 20].value.mean(), q[q.dose == 40].value.mean()
    t = stats.ttest_ind(np.log10(q[q.dose == 20].value), np.log10(q[q.dose == 40].value), equal_var=False)
    rowsA.append(dict(group=g, Emax=popt[0], Emax_lo=lo[0], Emax_hi=hi[0], ED50_ug=popt[1], ED50_lo=lo[1], ED50_hi=hi[1], hill=popt[2], hill_lo=lo[2], hill_hi=hi[2],
                      fitted_E_at_20ug=e20, fraction_of_Emax_at_20ug=frac20, mean_20ug=m20, mean_40ug=m40, ratio_40_vs_20=m40 / m20, p_40_vs_20_welch_log=t.pvalue))
DA = pd.DataFrame(rowsA); DA.to_csv(f"{O}/S08A_dose_response_fit.csv", index=False)
P(DA.to_string(index=False, float_format=lambda v: f"{v:.3g}"))
P("\nPSLN-344 vs PSLN-212 at each dose (ratio of geometric means, Welch on log10):")
for dose in [1, 5, 10, 20, 40]:
    a = np.log10(d[(d.group == "PSLN-344") & (d.dose == dose)].value); b = np.log10(d[(d.group == "PSLN-212") & (d.dose == dose)].value)
    P(f"   {dose:>2} ug: {10**(a.mean()-b.mean()):.2f}x   p={stats.ttest_ind(a,b,equal_var=False).pvalue:.4f}")
P("Cross-check at 20 ug against S01-A 16 h (independent block label, aged): "
  + "; ".join(f"{g}: S08-A {d[(d.group==g)&(d.dose==20)].value.mean():.1f} vs S01-A {c[(c.block=='S01-A')&(c.panel=='Ifnb1 16h')&(c.group==g)].value.mean():.1f}" for g in ["CMP-204", "PSLN-212", "PSLN-344"]))

# ------------------------------------------------------------------ b. S09-A
P(""); P("=" * 100); P("b. S09-A  (printed log10, relative to untreated) -> geometric-mean fold; panel 2 is treated as 72 h (see integrity check C)"); P("=" * 100)
q = c[c.block == "S09-A"].copy(); q["panel"] = q.panel.map(lambda s: "16h (panel 1)" if "panel1" in s else "72h (panel 2, printed '16h')")
gm = q.groupby(["panel", "x", "group"], sort=False)["value"].mean().rpow(10).unstack("group")
gm = gm[["PBS", "CMP-204", "PSLN-212", "PSLN-R848", "PSLN-212/R848", "PSLN-344", "PSLN-212(y)"]]
P(gm.round(1).to_string()); gm.to_csv(f"{O}/S09A_geomean_fold.csv")
rowsB = []
for (pan, an), g in q.groupby(["panel", "x"], sort=False):
    v = {k: g[g.group == k].value.values for k in g.group.unique()}
    for a, b in [("PSLN-344", "PSLN-212"), ("PSLN-344", "PSLN-212(y)"), ("PSLN-212", "PSLN-212(y)"), ("PSLN-344", "PBS"), ("PSLN-212/R848", "PSLN-344"), ("PSLN-R848", "PSLN-344")]:
        t = stats.ttest_ind(v[a], v[b], equal_var=False)
        rowsB.append(dict(panel=pan, analyte=an, a=a, b=b, fold_a=10 ** v[a].mean(), fold_b=10 ** v[b].mean(), ratio=10 ** (v[a].mean() - v[b].mean()), p_welch_log=t.pvalue))
DB = pd.DataFrame(rowsB); DB.to_csv(f"{O}/S09A_contrasts.csv", index=False)
P("\nKey contrasts (ratio of geometric means; n=3 per group, Welch on log10):")
P(DB[DB.a.eq("PSLN-344")].to_string(index=False, float_format=lambda v: f"{v:.3g}"))
P("\nR848-containing formulations vs PSLN-344 at 16 h:"); P(DB[(DB.b == "PSLN-344") & DB.panel.str.startswith("16h")].to_string(index=False, float_format=lambda v: f"{v:.3g}"))

# ------------------------------------------------------------------ c. S11-A vs S11-B
P(""); P("=" * 100); P("c. S11-A (alveolar macrophages) vs S11-B (neutrophils): cell-by-cell comparison"); P("=" * 100)
A = c[c.block == "S11-A"].set_index(["group", "x", "rep"])["value"]; B = c[c.block == "S11-B"].set_index(["group", "x", "rep"])["value"]
same = (A - B).abs() < 1e-9
P(f"identical values in the same position: {int(same.sum())} of {len(same)}")
P(same.groupby(level=["group", "rep"], sort=False).sum().unstack("rep").to_string())
mA = A.groupby(level=["group", "x"], sort=False).mean(); mB = B.groupby(level=["group", "x"], sort=False).mean()
P(f"group-by-day means: Pearson r = {np.corrcoef(mA, mB)[0,1]:.4f}; max |difference| = {np.abs(mA-mB).max():.2f} percentage points; mean |difference| = {np.abs(mA-mB).mean():.2f}")
P(pd.DataFrame({"S11-A mean": mA, "S11-B mean": mB}).round(1).unstack("x").to_string())

# ------------------------------------------------------------------ d. time courses
P(""); P("=" * 100); P("d. TIME COURSES: two-way ANOVA (group x day, type II) + peak-day contrast"); P("=" * 100)
for blk in ["S01-D", "S01-E", "S02-F", "S07-A", "S11-A", "S11-D"]:
    q = c[c.block == blk].copy(); q["g"] = q["group"]; q["t"] = q["x"]
    fit = smf.ols("value ~ C(g) * C(t)", q).fit(); an = sm.stats.anova_lm(fit, typ=2)
    P(f"\n{blk}:  group p={an.loc['C(g)','PR(>F)']:.2e}  day p={an.loc['C(t)','PR(>F)']:.2e}  interaction p={an.loc['C(g):C(t)','PR(>F)']:.2e}")
    P(q.pivot_table(index="x", columns="group", values="value", aggfunc="mean", sort=False).round(2).to_string())

# ------------------------------------------------------------------ e. single dose vs prime-boost
P(""); P("=" * 100); P("e. IgG after one dose (d14: S03-A, S03-E) vs after prime-boost (d28, boost d14: S13-I, S13-J); geometric means"); P("=" * 100)
for virus, b1, b2 in [("CA09 H1N1", "S03-A", "S13-I"), ("Aichi H3N2", "S03-E", "S13-J")]:
    P(f"  {virus}")
    for g in ["Sham", "CMP-204", "PSLN-212", "PSLN-344", "PSLN-212(Y)"]:
        a = c[(c.block == b1) & (c.group == g)].value; b = c[(c.block == b2) & (c.group == g)].value
        P(f"     {g:<12} d14 GMT {10**np.log10(a).mean():>8.0f}   d28 post-boost GMT {10**np.log10(b).mean():>8.0f}   boost/prime = {10**(np.log10(b).mean()-np.log10(a).mean()):.1f}x")
    one344 = np.log10(c[(c.block == b1) & (c.group == "PSLN-344")].value); two212 = np.log10(c[(c.block == b2) & (c.group == "PSLN-212")].value)
    P(f"     one dose PSLN-344 vs two doses PSLN-212 (aged): ratio {10**(one344.mean()-two212.mean()):.2f}x, Welch p={stats.ttest_ind(one344,two212,equal_var=False).pvalue:.3f}")

# ------------------------------------------------------------------ f. Mn effect in young animals
P(""); P("=" * 100); P("f. DOES Mn ADD ANYTHING IN YOUNG ANIMALS?  PSLN-344(Y) vs PSLN-212(Y)"); P("=" * 100)
for (blk, pan, x), g in c.groupby(["block", "panel", "x"], sort=False):
    gs = set(g.group)
    if "PSLN-344(Y)" in gs and "PSLN-212(Y)" in gs:
        a = g[g.group == "PSLN-344(Y)"].value; b = g[g.group == "PSLN-212(Y)"].value
        P(f"   {blk:<7} {pan:<10} {x:<4} 344(Y) {a.mean():6.2f} vs 212(Y) {b.mean():6.2f}  ratio {a.mean()/b.mean():.2f}  Welch p={stats.ttest_ind(a,b,equal_var=False).pvalue:.3f}  MWU p={stats.mannwhitneyu(a,b,method='exact').pvalue:.3f}")
out.close()
