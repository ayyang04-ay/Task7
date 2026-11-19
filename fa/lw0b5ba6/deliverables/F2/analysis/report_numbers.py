"""Helpers that read the analysis outputs so that every number in the proposal is pulled from a table, never typed."""
import pandas as pd, numpy as np
O = "/tmp/outputs/analysis/stats"; I = "/tmp/outputs/analysis/integrity"
S = pd.read_csv(f"{O}/continuous_summary.csv", keep_default_na=False)
for c_ in ["n", "mean", "sd", "sem", "median", "min", "max", "geo_mean"]: S[c_] = pd.to_numeric(S[c_], errors="coerce")
PW = pd.read_csv(f"{O}/continuous_pairwise.csv", keep_default_na=False)
for c_ in [c for c in PW.columns if c not in ("block", "panel", "x", "group_a", "group_b", "no_overlap")]: PW[c_] = pd.to_numeric(PW[c_], errors="coerce")
A = pd.read_csv(f"{O}/survival_by_arm.csv", keep_default_na=False)
SP = pd.read_csv(f"{O}/survival_pairwise.csv", keep_default_na=False)
for c_ in ["p_logrank", "p_logrank_exact_perm", "p_fisher"]: SP[c_] = pd.to_numeric(SP[c_], errors="coerce")
POOL = pd.read_csv(f"{O}/survival_pooled.csv"); SENS = pd.read_csv(f"{O}/survival_sensitivity.csv"); REC = pd.read_csv(f"{O}/survival_reconciliation.csv", keep_default_na=False)
CHAIN = pd.read_csv(f"{O}/restoration_chain.csv"); DR = pd.read_csv(f"{O}/S08A_dose_response_fit.csv").set_index("group")
G9 = pd.read_csv(f"{O}/S09A_geomean_fold.csv").set_index(["panel", "x"]); C9 = pd.read_csv(f"{O}/S09A_contrasts.csv")
BWA = pd.read_csv(f"{O}/bodyweight_by_arm.csv"); POWER = pd.read_csv(f"{O}/power_table.csv")
P16, P72 = "16h (panel 1)", "72h (panel 2, printed '16h')"

def row(block, group, panel="", x=""):
    q = S[(S.block == block) & (S.group == group) & (S.panel == panel) & (S.x == x)]
    assert len(q) == 1, f"summary lookup failed: {block}|{group}|{panel}|{x} -> {len(q)}"
    return q.iloc[0]
def m(block, group, panel="", x=""): return float(row(block, group, panel, x)["mean"])
def gm(block, group, panel="", x=""): return float(row(block, group, panel, x)["geo_mean"])
def sd(block, group, panel="", x=""): return float(row(block, group, panel, x)["sd"])
def nn(block, group, panel="", x=""): return int(row(block, group, panel, x)["n"])
def rng(block, group, panel="", x=""):
    r = row(block, group, panel, x); return float(r["min"]), float(r["max"])
def cells(block, group, panel="", x=""): return row(block, group, panel, x)["cells"]
def pair(block, a, b, panel="", x=""):
    q = PW[(PW.block == block) & (PW.panel == panel) & (PW.x == x) & (((PW.group_a == a) & (PW.group_b == b)) | ((PW.group_a == b) & (PW.group_b == a)))]
    assert len(q) == 1, f"pair lookup failed: {block}|{a}|{b}|{panel}|{x} -> {len(q)}"
    return q.iloc[0]
def pw(block, a, b, panel="", x="", log=False):
    r = pair(block, a, b, panel, x); return float(r["p_welch_log"] if log else r["p_welch"])
def pmw(block, a, b, panel="", x=""): return float(pair(block, a, b, panel, x)["p_mannwhitney_exact"])
def ptk(block, a, b, panel="", x="", log=False):
    r = pair(block, a, b, panel, x); return float(r["p_tukey_log"] if log else r["p_tukey"])
def arm(block, group):
    q = A[(A.block == block) & (A.group == group)]; assert len(q) == 1, (block, group); r = q.iloc[0]; return int(r.survivors), int(r.n)
def armcells(block, group): return A[(A.block == block) & (A.group == group)].iloc[0]["cells"]
def sp(block, a, b, col="p_logrank_exact_perm"):
    q = SP[(SP.block == block) & (((SP.group_a == a) & (SP.group_b == b)) | ((SP.group_a == b) & (SP.group_b == a)))]; assert len(q) == 1, (block, a, b); return float(q.iloc[0][col])
def pool(reading, comp):
    q = POOL[(POOL.reading == reading) & POOL.comparator.str.startswith(comp)]; assert len(q) == 1; return q.iloc[0]
def sens(subset, comp):
    q = SENS[SENS.subset.str.startswith(subset) & SENS.comparator.str.startswith(comp)]; assert len(q) == 1, (subset, comp, len(q)); return q.iloc[0]
def g9(panel, analyte, group): return float(G9.loc[(panel, analyte), group])
def c9(panel, analyte, a, b):
    q = C9[(C9.panel == panel) & (C9.analyte == analyte) & (C9.a == a) & (C9.b == b)]; assert len(q) == 1, (panel, analyte, a, b); return q.iloc[0]
def bwa(block, group):
    q = BWA[(BWA.block == block) & (BWA.group == group)]; assert len(q) == 1; return q.iloc[0]
def power(scn, n):
    q = POWER[POWER.scenario.str.startswith(scn) & (POWER.n_per_arm == n)]; assert len(q) == 1, (scn, n); return float(q.iloc[0].power)
def fp(p):
    """format a p-value"""
    if p is None or (isinstance(p, float) and np.isnan(p)): return "n/a"
    if p < 0.0001: return "<0.0001"
    if p < 0.001: return f"{p:.4f}"
    if p < 0.01: return f"{p:.3f}"
    return f"{p:.2f}" if p >= 0.095 else f"{p:.3f}"
def sumk(blocks, group):
    k = n = 0
    for b in blocks:
        a, c = arm(b, group); k += a; n += c
    return k, n
