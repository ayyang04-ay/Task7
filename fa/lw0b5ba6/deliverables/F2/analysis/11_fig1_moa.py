#!/usr/bin/env python
"""Figure 3 - mechanism of action assembled from the dataset; every box carries its numbers and source block.
   Numbers are read from the stats tables (not typed)."""
import pandas as pd, numpy as np, sys, textwrap
sys.path.insert(0, "/tmp/outputs/analysis")
from figstyle import *
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
style()
O = "/tmp/outputs/analysis/stats"
S = pd.read_csv(f"{O}/continuous_summary.csv", keep_default_na=False)
for c_ in ["mean", "geo_mean"]: S[c_] = pd.to_numeric(S[c_], errors="coerce")
def m(block, group, panel="", x="", geo=False):
    q = S[(S.block == block) & (S.group == group) & (S.panel == panel) & (S.x == x)]
    assert len(q) == 1, (block, group, panel, x, len(q))
    return float(q["geo_mean" if geo else "mean"].iloc[0])
DR = pd.read_csv(f"{O}/S08A_dose_response_fit.csv").set_index("group")
G9 = pd.read_csv(f"{O}/S09A_geomean_fold.csv").set_index(["panel", "x"])
POOL = pd.read_csv(f"{O}/survival_pooled.csv"); p = POOL[(POOL.reading == "TTE") & POOL.comparator.str.startswith("PSLN-212")].iloc[0]
A = pd.read_csv(f"{O}/survival_by_arm.csv", keep_default_na=False)
alone = A[(A.block == "S15-H") & (A.group == "3d PSLN-344")].iloc[0]
f0 = lambda v: f"{v:.0f}"; f1 = lambda v: f"{v:.1f}"
boxes = {
 "A1": ("1  Uptake by alveolar macrophages", "Needs surfactant proteins A/D",
        f"Labelled particle in {f0(m('S01-C','WT'))}% of alveolar macrophages in wild-type vs {f0(m('S01-C','SPA/D'))}% in Sftpa1/Sftpd-knockout mice  [S01-C]", "KNOCKOUT"),
 "A2": ("2  Cargo passes on to alveolar epithelium", "Through gap junctions; type II > type I cells",
        f"Tracer from the Mn-free particle in {f1(m('S01-B','AECII/PSLN-SRB'))}% of type II cells vs {f1(m('S01-B','AECII/FreeSRB'))}% with free tracer [S01-B]. "
        f"Gap-junction blocker cuts monocyte influx after PSLN-344 {f1(m('S11-C','CBX-'))}% → {f1(m('S11-C','CBX+'))}%  [S11-C]", "INHIBITOR"),
 "A3": ("3  STING signal, amplified by Mn²⁺", "Type-I interferon, GM-CSF, chemokines",
        f"Ifnb1 {f0(m('S01-A','PSLN-344','Ifnb1 16h','16h'))}× with Mn vs {f0(m('S01-A','PSLN-212','Ifnb1 16h','16h'))}× without (young {f0(m('S01-A','PSLN-212(Y)','Ifnb1 16h','16h'))}×) [S01-A]; "
        f"ceiling {f0(DR.loc['PSLN-344','Emax'])}× vs {f0(DR.loc['PSLN-212','Emax'])}×, ED50 {f0(DR.loc['PSLN-344','ED50_ug'])} vs {f0(DR.loc['PSLN-212','ED50_ug'])} µg [S08-A]. "
        f"Gm-csf {f1(m('S02-F','PSLN-344','','16h'))}× vs {f1(m('S02-F','PSLN-212','','16h'))}× [S02-F]; Ccl2 {f0(G9.loc[('16h (panel 1)','Ccl2'),'PSLN-344'])}× vs {f0(G9.loc[('16h (panel 1)','Ccl2'),'PSLN-212'])}× [S09-A]", "FORMULATION\nCOMPARISON"),
 "B1": ("4  Monocytes recruited to the lung", "CCR2-dependent",
        f"Lung monocytes on day 4: {f0(m('S01-D','PSLN-344','','4'))}% vs {f0(m('S01-D','PSLN-212','','4'))}% [S01-D]. "
        f"CCR2 antagonist: {f1(m('S07-B','PSLN-344','CD11b+Ly6C+ monocytes','Mono'))}% → {f1(m('S07-B','PSLN-344+INCB3344','CD11b+Ly6C+ monocytes','Mono'))}%  [S07-B]", "INHIBITOR"),
 "B2": ("5  Monocytes become CD11b⁺ dendritic cells", "Needs the type-I IFN receptor and GM-CSF",
        f"CD11b⁺ DC on day 4: {f0(m('S01-E','PSLN-344','','4'))}% vs {f0(m('S01-E','PSLN-212','','4'))}% [S01-E]. Donor cells lacking IFNAR: {f0(m('S02-H','IFN w/o cDC'))}% vs {f0(m('S02-H','WT w/o cDC'))}%; "
        f"GM-CSF restores to {f0(m('S02-H','GMCSF'))}% [S02-H]. GM-CSF added to PSLN-212: {f0(m('S02-G','PSLN-212'))}% → {f0(m('S02-G','PSLN-212+GM-CSF'))}%  [S02-G]", "KNOCKOUT +\nRESCUE"),
 "B3": ("6  DCs carry antigen to the lymph node", "and cross-prime CD8 T cells",
        f"CCR7⁺ migratory DC {f0(m('S02-A','PSLN-344'))}% vs {f0(m('S02-A','PSLN-212'))}% [S02-A]; antigen-carrying DC {f1(m('S02-C','PSLN-344'))}% vs {f1(m('S02-C','PSLN-212'))}%, "
        f"{f1(m('S02-C','PTX'))}% with pertussis toxin [S02-C]; ex vivo CD8 priming {f0(m('S02-E','PSLN-344'))}% vs {f1(m('S02-E','PSLN-212'))}%  [S02-E]", "INHIBITOR"),
 "C1": ("7a  Antibody arm", "More helper T cells, fewer regulatory cells",
        f"ICOS-high Tfh {f1(m('S04-A','PSLN-344','ICOS-high Tfh','ICOS+'))}% vs {f1(m('S04-A','PSLN-212','ICOS-high Tfh','ICOS+'))}% [S04-A]; follicular regulatory T {f0(m('S04-B Foxp3+ in CXCR5+','PSLN-344'))}% vs "
        f"{f0(m('S04-B Foxp3+ in CXCR5+','PSLN-212'))}% [S04-B]; germinal-centre B {f1(m('S03-K','PSLN-344'))}% vs {f1(m('S03-K','PSLN-212'))}% [S03-K]; "
        f"IgG {f0(m('S03-A','PSLN-344','IgG CA09 d14','',True)/m('S03-A','PSLN-212','IgG CA09 d14','',True))}×, HAI {f0(m('S03-C','PSLN-344','HAI CA09 d14','',True)/m('S03-C','PSLN-212','HAI CA09 d14','',True))}× [S03-A, S03-C]", "FORMULATION\nCOMPARISON"),
 "C2": ("7b  CD8 T-cell arm", "Cross-reactive effectors and lung-resident memory",
        f"IFN-γ⁺ CD8 recalled by H5N1 antigen {f1(m('S05-F','PSLN-344'))}% vs {f1(m('S05-F','PSLN-212'))}% [S05-F]; lung resident-memory CD8 {f1(m('S05-I','PSLN-344'))}% vs {f1(m('S05-I','PSLN-212'))}% [S05-I]. "
        f"CCR2 antagonist (young): GZMB⁺ CD8 {f1(m('S02-I','PSLN-344(Y)'))}% → {f1(m('S02-I','PSLN-344(Y)+INCB3344'))}%  [S02-I]", "INHIBITOR\n(young)"),
 "C3": ("8  Protection from lethal challenge", "Needs antigen + adjuvant together",
        f"Aged animals: {p.psln344} survive ({f0(p.psln344_pct)}%) vs {p.comparator_surv} ({f0(p.comparator_pct)}%) without Mn [13 experiment blocks]. "
        f"Adjuvant without vaccine: {int(alone.survivors)}/{int(alone.n)}  [S15-H]", "CHALLENGE"),
}
side = ("Without Mn in the aged lung the same monocytes take the other fork",
        f"Ly6C⁺CCR2⁺ macrophages on day 5: {f0(m('S07-A','PSLN-212','','5'))} vs {f1(m('S07-A','PSLN-344','','5'))} ×10⁵ [S07-A, n = 3]; CD206⁺ macrophages {f0(m('S11-E','PSLN-212'))}% vs {f0(m('S11-E','PSLN-344'))}% [S11-E]; "
        f"lung regulatory T cells {f1(m('S04-D','PSLN-212'))}% vs {f1(m('S04-D','PSLN-344'))}% [S04-D, n = 3]. "
        f"Transferring one sorted macrophage subset doubled lung regulatory T cells ({f1(m('S07-C','Ly6C-CD206+ MPhi [col B]'))}% vs {f1(m('S07-C','Ly6C-CD206+ MPhi [col C]'))}%), "
        f"but both columns of S07-C carry the same label, so which subset does this cannot be read from the workbook.")
gaps = ("Links NOT yet shown in our data:  (a) that PSLN-344 acts through STING — no STING-deficient control;  (b) what Mn²⁺ contributes on its own — no Mn-only particle;  "
        "(c) epithelial delivery by the Mn particle itself — S08-C column labels unresolved;  (d) anything in human cells.")
W, H = 11.6, 7.5
fig = plt.figure(figsize=(W, H)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
bw, bh = 3.45, 1.44; gap = 0.36; xs = [0.25, 4.075, 7.9]
yA = H - 0.84 - bh; ysr = {"A": yA, "B": yA - gap - bh, "C": yA - 2 * (gap + bh)}
tagcol = {"KNOCKOUT": "#00695C", "INHIBITOR": "#00695C", "KNOCKOUT +\nRESCUE": "#00695C", "INHIBITOR\n(young)": "#00695C", "FORMULATION\nCOMPARISON": "#5C6F82", "CHALLENGE": "#0072B2"}
for key, (title, sub, body, tag) in boxes.items():
    x = xs[int(key[1]) - 1]; y = ysr[key[0]]
    ax.add_patch(FancyBboxPatch((x, y), bw, bh, boxstyle="round,pad=0.02,rounding_size=0.08", fc="white", ec="#333333", lw=1.0))
    ax.add_patch(FancyBboxPatch((x, y + bh - 0.50), bw, 0.50, boxstyle="round,pad=0.02,rounding_size=0.08", fc="#E8EEF4", ec="#333333", lw=1.0))
    ax.text(x + 0.10, y + bh - 0.17, title, fontsize=9.2, fontweight="bold", va="center", color="#111111")
    ax.text(x + 0.10, y + bh - 0.39, sub, fontsize=7.6, va="center", color="#333333", style="italic")
    ax.text(x + 0.10, y + bh - 0.60, textwrap.fill(body, 57), fontsize=7.2, va="top", color="#111111", linespacing=1.25)
    ax.text(x + bw - 0.07, y + 0.07, tag, fontsize=5.8, fontweight="bold", color="white", ha="right", va="bottom",
            bbox=dict(boxstyle="round,pad=0.22", fc=tagcol[tag], ec="none"), linespacing=1.0)
def arrow(a, b, **kw):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=15, lw=1.5, color="#333333", shrinkA=0, shrinkB=0, **kw))
for r in "AB":
    for i in (0, 1):
        arrow((xs[i] + bw + 0.04, ysr[r] + bh / 2), (xs[i + 1] - 0.04, ysr[r] + bh / 2))
# row A -> row B connector
xa = xs[2] + bw / 2; ymid = ysr["A"] - gap / 2; xb = xs[0] + bw / 2
ax.plot([xa, xa, xb], [ysr["A"] - 0.03, ymid, ymid], color="#333333", lw=1.5); arrow((xb, ymid), (xb, ysr["B"] + bh + 0.03))
# row B (step 6) -> both arms 7a and 7b
ymid = ysr["B"] - gap / 2; xc1 = xs[0] + bw / 2; xc2 = xs[1] + bw / 2
ax.plot([xa, xa, xc1], [ysr["B"] - 0.03, ymid, ymid], color="#333333", lw=1.5)
arrow((xc1, ymid), (xc1, ysr["C"] + bh + 0.03)); arrow((xc2, ymid), (xc2, ysr["C"] + bh + 0.03))
# both arms -> protection
arrow((xs[1] + bw + 0.04, ysr["C"] + bh / 2), (xs[2] - 0.04, ysr["C"] + bh / 2))
yl = ysr["C"] - 0.15; xc3 = xs[2] + bw / 2
ax.plot([xc1, xc1, xc3], [ysr["C"] - 0.03, yl, yl], color="#333333", lw=1.5); arrow((xc3, yl), (xc3, ysr["C"] - 0.03))
ax.text(W / 2, H - 0.27, "Mechanism of action of PSLN-344 in the aged lung, as supported by the programme dataset", fontsize=12, fontweight="bold", ha="center")
ax.text(W / 2, H - 0.55, "Numbers compare PSLN-344 (with Mn) against PSLN-212 (same CDN, no Mn) in aged mice unless stated.   Green tag = the step was tested by removing or blocking it.",
        fontsize=8, ha="center", color="#333333")
ys = 0.64; hs = ysr["C"] - 0.30 - ys
ax.add_patch(FancyBboxPatch((0.25, ys), W - 0.5, hs, boxstyle="round,pad=0.02,rounding_size=0.08", fc="#FFF6E5", ec="#B37700", lw=1.0))
ax.text(0.37, ys + hs - 0.17, side[0], fontsize=8.6, fontweight="bold", va="center", color="#7A5200")
ax.text(0.37, ys + hs - 0.33, textwrap.fill(side[1], 190), fontsize=7.3, va="top", color="#111111", linespacing=1.25)
ax.add_patch(FancyBboxPatch((0.25, 0.08), W - 0.5, 0.44, boxstyle="round,pad=0.02,rounding_size=0.08", fc="#FBEAEA", ec="#B71C1C", lw=1.0, ls="--"))
ax.text(0.37, 0.30, textwrap.fill(gaps, 205), fontsize=7.3, va="center", color="#7F0000", linespacing=1.25)
fig.savefig("/tmp/outputs/figures/fig1_mechanism_of_action.png", dpi=200)
print("ok")
