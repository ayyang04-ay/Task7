#!/usr/bin/env python
"""Appendix figure A1 - Kaplan-Meier curves for every time-to-event block (as printed)."""
import pandas as pd, numpy as np, sys
sys.path.insert(0, "/tmp/outputs/analysis")
from figstyle import *
style()
s = pd.read_csv("/tmp/outputs/analysis/tidy/survival.csv", keep_default_na=False); s["time"] = pd.to_numeric(s["time"], errors="coerce")
s = s.dropna(subset=["time"])
def km(t, e, tmax):
    t = np.asarray(t, float); e = np.asarray(e, int); xs = [0]; ys = [1.0]; n = len(t); surv = 1.0
    for tt in np.unique(t[e == 1]):
        at = (t >= tt).sum(); d = ((t == tt) & (e == 1)).sum(); xs += [tt, tt]; ys += [surv, surv * (1 - d / at)]; surv *= (1 - d / at)
    xs.append(tmax); ys.append(surv); return xs, ys
panels = [("S03-I", "S03-I  matched strain CA09 H1N1, d14", 14), ("S03-J", "S03-J  wild-type H5N1, d2 after one dose", 21), ("S06-A", "S06-A  H3N2 vaccine → PR8 H1N1, d14", 14), ("S06-B", "S06-B  H3N2 vaccine → PR8 H1N1, d3", 14),
          ("S06-C", "S06-C  bivalent → rgH5N1, d14", 14), ("S06-D", "S06-D  bivalent → rgH5N1, d3", 14), ("S06-E", "S06-E  H3N2 vaccine → PR8 H1N1, d60", 14), ("S06-F", "S06-F  bivalent → rgH5N1, d60", 14),
          ("S06-G", "S06-G  H1N1 vaccine → Perth H3N2, d60", 14), ("S15-H", "S15-H  components, rgH5N1 at d3", 14), ("S06-E(2) imprinting/PR8", "S06-E (2nd)  14-month ± imprinting → PR8", 14),
          ("S06-F(2) imprinting/Perth", "S06-F (2nd)  14-month ± imprinting → Perth", 14), ("S15-L", "S15-L  aged C57BL/6", 14), ("S15-N", "S15-N  aged Swiss Webster", 14),
          ("S09-B", "S09-B  young, H3N2 vaccine → PR8, d21", 14), ("S09-D", "S09-D  young, H1N1 vaccine → Perth, d21", 14), ("S09-F", "S09-F  young, bivalent → rgH5N1, d180", 14), ("S13-E", "S13-E  young, matched strain CA09, d14", 14)]
cmap = {"Sham": COL["Sham"], "CMP-204": COL["CMP-204"], "PSLN-212": COL["PSLN-212"], "PSLN-344": COL["PSLN-344"], "PSLN-212(Y)": COL["PSLN-212(Y)"], "Untreated": "#000000",
        "Naive+PSLN-212": COL["PSLN-212"], "Imprinting+PSLN-212": "#8C6A00", "Naive+PSLN-344": COL["PSLN-344"], "Imprinting+PSLN-344": "#56B4E9",
        "3d Vaccine": COL["Sham"], "3d PSLN-344": COL["PSLN-R848"], "3d Vaccine+PSLN-344": COL["PSLN-344"], "PSLN-344Y": COL["PSLN-344(Y)"], "PSLN-212Y": COL["PSLN-212(Y)"],
        "Naive": "#BBBBBB", "CMP-204(Y)": COL["CMP-204"], "PSLN-344(Y)": COL["PSLN-344(Y)"]}
fig, axs = plt.subplots(5, 4, figsize=(11.6, 12.6), sharey=True); axs = axs.ravel()
for k, (blk, title, tmax) in enumerate(panels):
    ax = axs[k]; g = s[s.block == blk]; groups = list(dict.fromkeys(g.group))
    for j, grp in enumerate(groups):
        q = g[g.group == grp]; xs, ys = km(q.time, q.event, tmax); off = (j - (len(groups) - 1) / 2) * 0.012
        ax.plot(xs, np.array(ys) * 100 + off * 100, color=cmap[grp], lw=1.8, ls="--" if grp in ("Untreated", "Imprinting+PSLN-212", "Imprinting+PSLN-344") else "-",
                label=f"{grp}  {int((q.event==0).sum())}/{len(q)}")
    ax.set_title(title, fontsize=7.6); ax.set_xlim(0, tmax + 0.5); ax.set_ylim(-6, 108); ax.set_xticks([0, 7, 14] if tmax == 14 else [0, 7, 14, 21]); ax.legend(fontsize=6, loc="lower left", handlelength=1.6, labelspacing=0.2)
    if k % 4 == 0: ax.set_ylabel("Survival (%)")
    if k >= 14: ax.set_xlabel("Days after challenge")
for k in range(len(panels), len(axs)): axs[k].axis("off")
fig.suptitle("Kaplan–Meier curves for every time-to-event block, as printed in the workbook (legend: survivors / n)", fontsize=10, fontweight="bold", y=0.995)
fig.tight_layout(rect=(0, 0, 1, 0.985))
fig.savefig("/tmp/outputs/figures/figA1_kaplan_meier_all_blocks.png", bbox_inches="tight")
print("ok")
