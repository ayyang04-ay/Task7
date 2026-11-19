#!/usr/bin/env python
"""
Step 2 - Data-integrity checks on the extracted tables.  Nothing is "fixed" here; every finding is
written to integrity/ so that it can be cited (and challenged) by block and cell.

Checks
  A. stated n (from the printed block label) vs number of observations actually present
  B. exact / near-exact duplication of replicate series between blocks that should be independent
     (body-weight series that recur between blocks: see 02b_bodyweight_duplicates.py)
  C. derived quantities recomputed from their source blocks (IgG2a/IgG1, Tfh:Tfr, log10 vs linear panels)
  D. body-weight blocks: carried-forward (frozen) values, and implied survivors vs the paired time-to-event block
  E. time-to-event blocks: rows with a status but no time, identical arms across experiments
"""
import pandas as pd, numpy as np, re, os, itertools, json
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 5000); pd.set_option("display.max_columns", 40)
T = "/tmp/outputs/analysis/tidy"; O = "/tmp/outputs/analysis/integrity"; os.makedirs(O, exist_ok=True)
c = pd.read_csv(f"{T}/continuous.csv", keep_default_na=False); c["value"] = c["value"].astype(float)
s = pd.read_csv(f"{T}/survival.csv", keep_default_na=False)
s["time"] = pd.to_numeric(s["time"], errors="coerce")
b = pd.read_csv(f"{T}/bodyweight.csv", keep_default_na=False); b["value"] = pd.to_numeric(b["value"], errors="coerce"); b["day"] = b["day"].astype(float)
out = open(f"{O}/integrity_report.txt", "w")
def P(*a):
    msg = " ".join(str(x) for x in a); print(msg); out.write(msg + "\n")

# ------------------------------------------------------------------ A. stated n vs observed n
import openpyxl
wb = openpyxl.load_workbook("/tmp/world/filesystem/psln_program_dataset.xlsx", data_only=True)
stated = {}
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, str):
                m = re.match(r"^(S\d\d-[A-Z])(.*?)n=(\d+)", cell.value.strip())
                if m:
                    stated.setdefault(m.group(1), []).append((ws.title, cell.coordinate, cell.value.strip(), int(m.group(3))))
P("=" * 110); P("A. STATED n (printed label) vs OBSERVED n"); P("=" * 110)
rowsA = []
for key, lst in sorted(stated.items()):
    for (sheet, coord, label, n) in lst:
        obs = None
        cc = c[(c.sheet == sheet) & (c.block.str.startswith(key))]
        ss = s[(s.sheet == sheet) & (s.block.str.startswith(key))]
        bb = b[(b.sheet == sheet) & (b.block.str.startswith(key)) & (b.day == 0)]
        if len(cc):
            # restrict to the exact printed label where several blocks share the letter (S02-D, S04-B, S14-A)
            sub = cc
            if key in ("S02-D", "S04-B", "S14-A"):
                tag = label.replace(key, "").split("n=")[0].strip()
                sub = cc[cc.block.str.contains(re.escape(tag.split()[0]))] if tag else cc
            counts = sub.groupby(["block", "panel", "x", "group"])["value"].count()
            obs = sorted(set(counts.values))
        elif len(ss):
            # the two re-used labels on S06 need row disambiguation
            if key in ("S06-E", "S06-F"):
                r = int(re.sub(r"[A-Z]", "", coord)); tag = "(2)" if r > 60 else None
                ss = ss[ss.block.str.contains(r"\(2\)")] if tag else ss[~ss.block.str.contains(r"\(2\)")]
            counts = ss.groupby(["block", "group"])["event"].count()
            obs = sorted(set(counts.values))
            detail = counts.to_dict()
        elif len(bb):
            counts = bb.groupby(["block", "group"])["value"].count(); obs = sorted(set(counts.values))
        flag = "" if obs == [n] else "  <-- MISMATCH"
        rowsA.append(dict(sheet=sheet, label_cell=coord, label=label, stated_n=n, observed_n=str(obs), flag=flag.strip()))
        P(f"{sheet}!{coord:<5} {label:<34} stated n={n:<3} observed per group={obs}{flag}")
pd.DataFrame(rowsA).to_csv(f"{O}/A_stated_vs_observed_n.csv", index=False)

# ------------------------------------------------------------------ B. duplicated series
P(""); P("=" * 110); P("B. DUPLICATED REPLICATE SERIES BETWEEN BLOCKS / GROUPS (continuous data)"); P("=" * 110)
ser = {}
for k, g in c.groupby(["sheet", "block", "panel", "x", "group"], sort=False):
    ser[k] = (g["value"].tolist(), f"{g['cell'].iloc[0]}:{g['cell'].iloc[-1]}")
keys = list(ser)
discrete_blocks = ("S03-C", "S03-D", "S03-G", "S03-H")   # doubling-dilution titres: ties are expected
rowsB = []
for i, j in itertools.combinations(range(len(keys)), 2):
    a, bq = keys[i], keys[j]
    if a[1] in discrete_blocks or bq[1] in discrete_blocks: continue
    va, vb = ser[a][0], ser[bq][0]
    n = min(len(va), len(vb))
    if n < 3: continue
    same_pos = sum(1 for p in range(n) if abs(va[p] - vb[p]) < 1e-9)
    shared = len(set(np.round(va, 6)) & set(np.round(vb, 6)))
    if same_pos >= 2 or shared >= 3:
        rowsB.append(dict(a=" | ".join(a), a_cells=ser[a][1], b=" | ".join(bq), b_cells=ser[bq][1], n=n,
                          identical_same_position=same_pos, shared_values_any_position=shared,
                          a_values=va, b_values=vb))
dfB = pd.DataFrame(rowsB)
dfB.to_csv(f"{O}/B_duplicate_series_continuous.csv", index=False)
if len(dfB):
    summ = dfB.assign(pair=dfB.a.str.split(" \| ").str[1] + "  vs  " + dfB.b.str.split(" \| ").str[1]).groupby("pair").agg(
        n_series_pairs=("n", "size"), identical_positions=("identical_same_position", "sum"), shared=("shared_values_any_position", "sum"))
    P(summ.to_string())
    P("\n(first rows of detail; full table in B_duplicate_series_continuous.csv)")
    P(dfB.head(60)[["a", "a_cells", "b", "b_cells", "identical_same_position", "shared_values_any_position"]].to_string())

# (animal-level series that recur between blocks are handled in 02b_bodyweight_duplicates.py, after frozen tails are identified)
# same-day whole-row duplication between groups in the same block (e.g. one day copied across groups)
P(""); P("-" * 110); P("B3. identical day-rows between two groups (same or different block), >=5 animals identical on that day"); P("-" * 110)
rowvec = {}
from openpyxl.utils import column_index_from_string as _ci
b["colidx"] = b["col"].map(_ci)
for k, g in b[(b.day > 0)].groupby(["block", "group", "day"], sort=False):
    v = g.sort_values("colidx")["value"].tolist()
    if sum(pd.notna(x) for x in v) >= 5: rowvec[k] = v
rk = list(rowvec); rowsB3 = []
for i, j in itertools.combinations(range(len(rk)), 2):
    a, bq = rk[i], rk[j]; va, vb = rowvec[a], rowvec[bq]
    n = min(len(va), len(vb)); same = sum(1 for p in range(n) if pd.notna(va[p]) and pd.notna(vb[p]) and abs(va[p] - vb[p]) < 1e-9)
    if same >= 5 and not (a[0] == bq[0] and a[1] == bq[1]): rowsB3.append(dict(a=a, b=bq, identical=same, n=n))
dfB3 = pd.DataFrame(rowsB3); dfB3.to_csv(f"{O}/B3_duplicate_bodyweight_dayrows.csv", index=False)
P(dfB3.to_string() if len(dfB3) else "none")

# ------------------------------------------------------------------ C. derived quantities
P(""); P("=" * 110); P("C. DERIVED QUANTITIES RECOMPUTED FROM SOURCE BLOCKS"); P("=" * 110)
def vec(block, group, panel=None, x=None):
    q = c[(c.block == block) & (c.group == group)]
    if panel is not None: q = q[q.panel == panel]
    if x is not None: q = q[q.x == x]
    return q.sort_values("rep")["value"].to_numpy()
rowsC = []
for virus, ratio_blk, a_blk, b_blk in [("CA09 H1N1", "S03-B", "S13-A", "S13-B"), ("Aichi H3N2", "S03-F", "S13-C", "S13-D")]:
    P(f"\nIgG2a/IgG1 ({virus}): {ratio_blk} as printed  vs  {a_blk}/{b_blk} recomputed per animal")
    rec = {g: vec(a_blk, g) / vec(b_blk, g) for g in ["PSLN-212", "PSLN-344", "PSLN-212(Y)"]}
    for g_print in ["PSLN-212", "PSLN-344", "PSLN-212(Y)"]:
        printed = vec(ratio_blk, g_print)
        match = [g for g, r in rec.items() if np.allclose(np.sort(r), np.sort(printed), rtol=2e-3)]
        P(f"   {ratio_blk} column printed '{g_print}': {np.round(printed,3)}  mean={printed.mean():.3f}  == recomputed ratio of group {match}")
        rowsC.append(dict(check=f"IgG2a/IgG1 {virus}", printed_block=ratio_blk, printed_group=g_print, printed_mean=printed.mean(),
                          matches_recomputed_group="; ".join(match)))
    for g, r in rec.items():
        P(f"   recomputed {a_blk}/{b_blk} for '{g}': {np.round(r,3)}  mean={r.mean():.3f}  geo-mean={np.exp(np.log(r).mean()):.3f}")
P("\nTfh:Tfr (S04-B) vs (100 - Foxp3+%)/Foxp3+% from S04-B Foxp3+ block, and vs S04-A total Tfh / Foxp3+%")
for g in ["Sham", "PSLN-212", "PSLN-344", "PSLN-212(Y)"]:
    fr = vec("S04-B Foxp3+ in CXCR5+", g); ratio = vec("S04-B Tfh:Tfr", g)
    tfh_total = vec("S04-A", g, x="ICOS-") + vec("S04-A", g, x="ICOS+")
    P(f"   {g:<12} printed ratio={np.round(ratio,3)}  (100-Tfr)/Tfr={np.round((100-fr)/fr,3)}  match={np.allclose(ratio,(100-fr)/fr,rtol=1e-4)}"
      f" | S04-A totalTfh/Tfr%={np.round(tfh_total/fr,3)}")
    rowsC.append(dict(check="Tfh:Tfr", printed_block="S04-B Tfh:Tfr", printed_group=g, printed_mean=ratio.mean(),
                      matches_recomputed_group="(100-Foxp3%)/Foxp3% of same group" if np.allclose(ratio, (100 - fr) / fr, rtol=1e-4) else "NO MATCH"))
P("\nS04-A: ICOS-low + ICOS-high per animal (is the split a partition of a round total?)")
for g in ["Sham", "PSLN-212", "PSLN-344", "PSLN-212(Y)"]:
    lo, hi = vec("S04-A", g, x="ICOS-"), vec("S04-A", g, x="ICOS+")
    P(f"   {g:<12} sum={np.round(lo+hi,4)}  ICOS-high fraction={np.round(hi/(lo+hi),3)}")
P("\nS09-A (log10) vs S01-A (linear) Ifnb1: are the S09-A values the log10 of S01-A values?")
for panel, lin_panel in [("panel1 (cols A-V, printed 16h)", "Ifnb1 16h"), ("panel2 (cols X-AS, printed 16h)", "Ifnb1 72h")]:
    for lin_try in ["Ifnb1 16h", "Ifnb1 72h"]:
        hits = tot = 0
        for g9, g1 in [("PBS", "Sham"), ("CMP-204", "CMP-204"), ("PSLN-212", "PSLN-212"), ("PSLN-R848", "PSLN-R848"),
                       ("PSLN-212/R848", "PSLN-212/R848"), ("PSLN-344", "PSLN-344"), ("PSLN-212(y)", "PSLN-212(Y)")]:
            lg = 10 ** vec("S09-A", g9, panel=panel, x="Ifnb1"); lin = vec("S01-A", g1, panel=lin_try)
            for v in lg:
                tot += 1; hits += int(np.any(np.abs(lin - v) < 0.006))
        P(f"   S09-A {panel:<34} back-transformed values found in S01-A '{lin_try}': {hits}/{tot}")
        rowsC.append(dict(check="S09-A vs S01-A", printed_block=f"S09-A {panel}", printed_group="all 7 groups (Ifnb1 row)",
                          printed_mean=np.nan, matches_recomputed_group=f"{hits}/{tot} values equal 10^x of S01-A {lin_try}"))
pd.DataFrame(rowsC).to_csv(f"{O}/C_derived_quantities.csv", index=False)

P("\nS08-C (as printed) vs S01-B: SRB+ alveolar epithelial cells")
for blk in ["S01-B", "S08-C"]:
    q = c[c.block == blk].groupby("group", sort=False)["value"].agg(["mean", "min", "max"]).round(2)
    P(f"  {blk}\n" + q.to_string())

# ------------------------------------------------------------------ D. body weight: frozen values, implied survival
P(""); P("=" * 110); P("D. BODY-WEIGHT BLOCKS: blanks, carried-forward values, implied survivors vs paired time-to-event block"); P("=" * 110)
pairs = {  # body-weight block -> (time-to-event block, {bw group: survival group})
    "S13-F": ("S03-I", None), "S13-G": ("S03-J", None),
    "S15-A": ("S06-A", None), "S15-B": ("S06-B", None), "S15-C": ("S06-C", None), "S15-D": ("S06-D", None),
    "S15-E": ("S06-E", None), "S15-F": ("S06-F", None), "S15-G": ("S06-G", None),
    "S15-I": ("S15-H", None), "S15-J": ("S06-E(2) imprinting/PR8", None), "S15-K": ("S06-F(2) imprinting/Perth", None),
    "S15-M": ("S15-L", None), "S15-O": ("S15-N", None),
    "S09-C": ("S09-B", None), "S09-E": ("S09-D", None), "S09-G": ("S09-F", None), "S08-D": (None, None)}
def classify(days, vals):
    """Return (last_real_day, status) for one animal.
       blank tail -> 'blank-after'; >=2 trailing identical values (frozen) -> 'frozen-after' (treated as carried forward);
       otherwise 'complete'."""
    obs = [(d, v) for d, v in zip(days, vals) if pd.notna(v)]
    last_day = max(days)
    if not obs: return (None, "no data")
    d_last, v_last = obs[-1]
    if d_last < last_day:
        return (d_last, "blank-after")
    # complete to last day: look for frozen tail (same value on >=2 final consecutive readings, i.e. >=1 repeat)
    k = len(obs) - 1
    while k > 0 and abs(obs[k - 1][1] - v_last) < 1e-9: k -= 1
    n_rep = len(obs) - 1 - k
    if n_rep >= 2 and obs[k][0] > 0:          # value repeated on >=3 consecutive readings through day 14
        return (obs[k][0], "frozen-after")
    if n_rep == 1 and obs[k][0] > 0 and v_last < 90:
        return (obs[k][0], "frozen-after?(1 repeat)")
    return (d_last, "complete")
rowsD = []; animal_rows = []
for blk, g in b.groupby("block", sort=False):
    tte_blk = pairs.get(blk, (None, None))[0]
    for grp, gg in g.groupby("group", sort=False):
        stat = []
        for an, ga in gg.groupby("animal", sort=False):
            ga = ga.sort_values("day"); ld, st = classify(ga.day.tolist(), ga.value.tolist())
            alive_vals = ga[(ga.day <= (ld if ld is not None else -1))]["value"]
            nadir = alive_vals.min()
            stat.append((an, ld, st, nadir))
            animal_rows.append(dict(block=blk, group=grp, animal=an, col=ga["col"].iloc[0], last_real_day=ld, status=st,
                                    nadir_pct=nadir, final_value=ga["value"].dropna().iloc[-1] if ga["value"].notna().any() else np.nan))
        n = len(stat); n_complete = sum(1 for x in stat if x[2] == "complete")
        n_blank = sum(1 for x in stat if x[2] == "blank-after"); n_frozen = sum(1 for x in stat if x[2].startswith("frozen-after") and "?" not in x[2])
        n_q = sum(1 for x in stat if "?" in x[2])
        tte = ""
        if tte_blk is not None:
            q = s[(s.block == tte_blk) & (s.group == grp)]
            if len(q): tte = f"{int((q.event == 0).sum())}/{len(q)}"
            else: tte = "group not in TTE block"
        rowsD.append(dict(bw_block=blk, group=grp, n_animals=n, complete_to_last_day=n_complete, blank_after_death=n_blank,
                          frozen_tail=n_frozen, ambiguous_single_repeat=n_q, implied_survivors_bw=f"{n_complete}" + (f"-{n_complete+n_q}" if n_q else "") + f"/{n}",
                          paired_tte_block=tte_blk or "", survivors_tte=tte))
dfD = pd.DataFrame(rowsD); dfD.to_csv(f"{O}/D_bodyweight_vs_survival.csv", index=False)
pd.DataFrame(animal_rows).to_csv(f"{O}/D_bodyweight_animal_status.csv", index=False)
P(dfD.to_string(index=False))

# ------------------------------------------------------------------ E. time-to-event block checks
P(""); P("=" * 110); P("E. TIME-TO-EVENT BLOCKS"); P("=" * 110)
miss = s[s.time.isna()]
P("rows with a status but no elapsed-days value:"); P(miss.to_string(index=False) if len(miss) else "   none")
sig = {}
for (blk, grp), g in s.groupby(["block", "group"], sort=False):
    sig[(blk, grp)] = tuple(sorted(zip(g.time.fillna(-1), g.event)))
P("\nidentical arms (same multiset of day/status) across different blocks, arms with >=1 event only:")
rowsE = []
for (a, b2) in itertools.combinations(sig, 2):
    if a[0] != b2[0] and sig[a] == sig[b2] and any(e == 1 for _, e in sig[a]):
        rowsE.append(dict(block_a=a[0], group_a=a[1], block_b=b2[0], group_b=b2[1], series=str([f"d{int(t)}{'+' if e==0 else ''}" for t, e in sig[a]])))
dfE = pd.DataFrame(rowsE); dfE.to_csv(f"{O}/E_identical_survival_arms.csv", index=False)
P(dfE.to_string(index=False) if len(dfE) else "   none")
out.close()
