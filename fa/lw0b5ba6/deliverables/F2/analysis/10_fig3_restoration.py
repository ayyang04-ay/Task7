#!/usr/bin/env python
"""Figure 2 - how much of the young-animal response does each formulation reach in aged animals, step by step along the mechanism.
   Writes stats/restoration_chain.csv (numbers behind the figure)."""
import pandas as pd, numpy as np, sys
sys.path.insert(0, "/tmp/outputs/analysis")
from figstyle import *
style()
O = "/tmp/outputs/analysis/stats"
S = pd.read_csv(f"{O}/continuous_summary.csv", keep_default_na=False)
for c_ in ["mean", "geo_mean"]: S[c_] = pd.to_numeric(S[c_], errors="coerce")
PW = pd.read_csv(f"{O}/continuous_pairwise.csv", keep_default_na=False)
for c_ in ["p_welch", "p_welch_log", "p_mannwhitney_exact"]: PW[c_] = pd.to_numeric(PW[c_], errors="coerce")
A = pd.read_csv(f"{O}/survival_by_arm.csv", keep_default_na=False)
chain = [  # (stage, label, block, panel, x, use_geo)
 ("Innate sensing (lung)", "Ifnb1 mRNA, 16 h", "S01-A", "Ifnb1 16h", "16h", True),
 ("Cell recruitment (lung)", "Monocytes, day 4", "S01-D", "", "4", False),
 ("Cell recruitment (lung)", "CD11b+ dendritic cells, day 4", "S01-E", "", "4", False),
 ("Cell recruitment (lung)", "cDC1, 72 h", "S01-F", "", "72h", False),
 ("DC migration & priming", "CCR7+ migratory CD11b+ DC (lung)", "S02-A", "", "", False),
 ("DC migration & priming", "CD11b+ DC in draining node", "S02-B", "", "", False),
 ("DC migration & priming", "Antigen-carrying DC in node", "S02-C", "", "", False),
 ("DC migration & priming", "CD40+ of node CD11b+ DC", "S02-D CD40", "", "", False),
 ("DC migration & priming", "CD86+ of node CD11b+ DC", "S02-D CD86", "", "", False),
 ("DC migration & priming", "Cross-priming of CD8 T cells ex vivo", "S02-E", "", "", False),
 ("Helper T / germinal centre", "ICOS-high Tfh, day 7", "S04-A", "ICOS-high Tfh", "ICOS+", False),
 ("Helper T / germinal centre", "Germinal-centre B cells, day 7", "S03-K", "", "", False),
 ("Helper T / germinal centre", "IgG+ B cells in node", "S13-H", "", "", False),
 ("Antibody, day 14 (one dose)", "Serum IgG, H1N1 (GMT)", "S03-A", "IgG CA09 d14", "", True),
 ("Antibody, day 14 (one dose)", "Serum IgG, H3N2 (GMT)", "S03-E", "IgG Aichi d14", "", True),
 ("Antibody, day 14 (one dose)", "HAI, H1N1 (GMT)", "S03-C", "HAI CA09 d14", "", True),
 ("Antibody, day 14 (one dose)", "HAI, H3N2 (GMT)", "S03-G", "HAI Aichi d14", "", True),
 ("Antibody, day 14 (one dose)", "Neutralising titre, H1N1 (GMT)", "S03-D", "NAb CA09 d14", "", True),
 ("Antibody, day 14 (one dose)", "Neutralising titre, H3N2 (GMT)", "S03-H", "NAb Aichi d14", "", True),
 ("Antibody, day 14 (one dose)", "IgG2a, H1N1 (GMT)", "S13-A", "IgG2a CA09 d14", "", True),
 ("CD8 T cells", "Ki-67+ CD8 in lung, day 3", "S05-D", "", "", False),
 ("CD8 T cells", "GZMB+ CD8 in lung, day 3", "S05-E", "", "", False),
 ("CD8 T cells", "IFN-γ+ CD8, heterosubtypic recall, day 14", "S05-F", "", "", False),
 ("CD8 T cells", "IFN-γ+ CD8, heterosubtypic recall, day 60", "S05-G", "", "", False),
 ("CD8 T cells", "Lung resident-memory CD8, day 25", "S05-I", "", "", False),
]
rows = []
for stage, lab, blk, pan, x, geo in chain:
    q = S[(S.block == blk) & (S.panel == pan) & (S.x == x)]
    col = "geo_mean" if geo else "mean"
    v = dict(zip(q.group, q[col])); cells = dict(zip(q.group, q.cells))
    pw = PW[(PW.block == blk) & (PW.panel == pan) & (PW.x == x)]
    def p(a, b):
        r = pw[((pw.group_a == a) & (pw.group_b == b)) | ((pw.group_a == b) & (pw.group_b == a))].iloc[0]
        return (r.p_welch_log if geo and not np.isnan(r.p_welch_log) else r.p_welch), r.p_mannwhitney_exact
    p1, m1 = p("PSLN-344", "PSLN-212"); p2, m2 = p("PSLN-344", "PSLN-212(Y)")
    rows.append(dict(stage=stage, readout=lab, block=blk, statistic="geometric mean" if geo else "mean", aged_212=v["PSLN-212"], aged_344=v["PSLN-344"], young_212=v["PSLN-212(Y)"],
                     fold_344_vs_212=v["PSLN-344"] / v["PSLN-212"], aged212_pct_young=100 * v["PSLN-212"] / v["PSLN-212(Y)"], aged344_pct_young=100 * v["PSLN-344"] / v["PSLN-212(Y)"],
                     p_344_vs_212=p1, mwu_344_vs_212=m1, p_344_vs_young=p2, mwu_344_vs_young=m2, cells_212=cells["PSLN-212"], cells_344=cells["PSLN-344"], cells_young=cells["PSLN-212(Y)"]))
# survival row: the 10 aged experiments that carry a young PSLN-212 arm
blks = ["S03-I", "S06-A", "S06-B", "S06-C", "S06-D", "S06-E", "S06-F", "S06-G", "S15-L", "S15-N"]
def tot(g):
    q = A[A.block.isin(blks) & (A.group == g)]; return int(q.survivors.sum()), int(q.n.sum())
s212, s344, sy = tot("PSLN-212"), tot("PSLN-344"), tot("PSLN-212(Y)")
rows.append(dict(stage="Protection", readout=f"Survival, 10 experiments with a young arm ({s344[0]}/{s344[1]} vs {s212[0]}/{s212[1]}; young {sy[0]}/{sy[1]})", block="S03-I, S06-A..G, S15-L, S15-N",
                 statistic="pooled proportion", aged_212=100 * s212[0] / s212[1], aged_344=100 * s344[0] / s344[1], young_212=100 * sy[0] / sy[1],
                 fold_344_vs_212=(s344[0] / s344[1]) / (s212[0] / s212[1]), aged212_pct_young=100 * (s212[0] / s212[1]) / (sy[0] / sy[1]), aged344_pct_young=100 * (s344[0] / s344[1]) / (sy[0] / sy[1])))
R = pd.DataFrame(rows); R.to_csv(f"{O}/restoration_chain.csv", index=False)
print(R[["stage", "readout", "block", "aged_212", "aged_344", "young_212", "fold_344_vs_212", "aged212_pct_young", "aged344_pct_young", "p_344_vs_212", "p_344_vs_young"]].to_string(index=False, float_format=lambda v: f"{v:.3g}"))

fig, ax = plt.subplots(figsize=(8.6, 8.4))
n = len(R); ys = []; y = 0; prev = None; stage_pos = {}
for i, r in R.iterrows():
    if r.stage != prev:
        y -= 0.9; stage_pos[r.stage] = y; prev = r.stage; y -= 0.75
    ys.append(y); y -= 1
R["y"] = ys
for _, r in R.iterrows():
    ax.plot([r.aged212_pct_young, r.aged344_pct_young], [r.y, r.y], color="#BBBBBB", lw=2, zorder=1)
    ax.scatter(r.aged212_pct_young, r.y, color=COL["PSLN-212"], s=46, zorder=3, marker="D", edgecolor="white", linewidth=0.5)
    ax.scatter(r.aged344_pct_young, r.y, color=COL["PSLN-344"], s=62, zorder=3, edgecolor="white", linewidth=0.5)
    lab = r.readout if r.stage == "Protection" else f"{r.readout}  [{r.block}]"
    ax.text(-4, r.y, lab, ha="right", va="center", fontsize=7.6)
    ax.text(118, r.y, f"{r.fold_344_vs_212:.1f}×" if r.fold_344_vs_212 < 10 else f"{r.fold_344_vs_212:.0f}×", ha="left", va="center", fontsize=7.6, color=COL["PSLN-344"])
for st, yy in stage_pos.items():
    ax.text(-4, yy, st, ha="right", va="center", fontsize=8.3, fontweight="bold", color="#222222")
ax.plot([100, 100], [min(ys) - 1, -0.3], color=COL["PSLN-212(Y)"], lw=1.4, ls="--", zorder=0)
ax.text(100, 0.0, "young benchmark\n(PSLN-212 in young = 100%)", ha="center", va="bottom", fontsize=7.5, color=COL["PSLN-212(Y)"])
ax.text(118, 0.0, "PSLN-344 ÷\nPSLN-212 (aged)", ha="left", va="bottom", fontsize=7.5, color=COL["PSLN-344"])
ax.set_xlim(0, 132); ax.set_ylim(min(ys) - 1, 1.6); ax.set_yticks([]); ax.spines["left"].set_visible(False)
ax.set_xticks([0, 25, 50, 75, 100]); ax.set_xlabel("Response in aged animals, % of the young benchmark")
ax.scatter([], [], color=COL["PSLN-212"], marker="D", s=46, label="PSLN-212 (no Mn), aged"); ax.scatter([], [], color=COL["PSLN-344"], s=62, label="PSLN-344 (with Mn), aged")
ax.legend(loc="lower center", bbox_to_anchor=(0.42, -0.12), ncol=2)
ax.set_title("Aged animals: share of the young-animal response reached, step by step", x=-0.62, fontsize=9.5)
fig.savefig("/tmp/outputs/figures/fig3_restoration_along_mechanism.png", bbox_inches="tight")
