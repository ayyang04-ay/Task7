#!/usr/bin/env python
"""Figure 4 - innate pharmacodynamics (dose-response, Gm-csf time course, cytokine panel).
   Figure 5 - tolerability (post-vaccination body weight, CNS transcripts, resolution of lung cytokines)."""
import pandas as pd, numpy as np, sys
sys.path.insert(0, "/tmp/outputs/analysis")
from figstyle import *
from matplotlib.colors import TwoSlopeNorm
style()
O = "/tmp/outputs/analysis/stats"
c = pd.read_csv("/tmp/outputs/analysis/tidy/continuous.csv", keep_default_na=False); c["value"] = c["value"].astype(float)
DR = pd.read_csv(f"{O}/S08A_dose_response_fit.csv").set_index("group")

# ------------------------------------------------------------------ Figure 4
fig = plt.figure(figsize=(11.2, 7.4)); gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.02], hspace=0.42, wspace=0.28)
ax = fig.add_subplot(gs[0, 0])
d = c[c.block == "S08-A"].copy(); d["dose"] = d["x"].astype(float); xx = np.logspace(np.log10(0.8), np.log10(50), 200)
for g, lab in [("PSLN-344", "PSLN-344"), ("PSLN-344/R848", "“PSLN-344/R848”"), ("PSLN-212", "PSLN-212 (no Mn)"), ("CMP-204", "CMP-204 (cGAMP)")]:
    q = d[d.group == g]; E, ED, h = DR.loc[g, ["Emax", "ED50_ug", "hill"]]
    ax.plot(xx, 1 + (E - 1) * xx ** h / (ED ** h + xx ** h), color=COL[g], lw=1.6, ls="--" if "R848" in g else "-")
    ax.scatter(q.dose, q.value, color=COL[g], s=20, label=f"{lab}: ceiling {E:.0f}×, ED50 {ED:.0f} µg", zorder=3, marker="s" if "R848" in g else "o", edgecolor="white", linewidth=0.4)
ax.axvline(20, color="#999999", lw=0.8, ls=":"); ax.text(19.2, 0.82, "20 µg = dose used in\nall efficacy studies", fontsize=6.8, color="#555555", va="bottom", ha="right")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xticks([1, 5, 10, 20, 40]); ax.set_xticklabels(["1", "5", "10", "20", "40"]); ax.set_yticks([1, 3, 10, 30, 60]); ax.set_yticklabels(["1", "3", "10", "30", "60"])
ax.set_xlabel("Intranasal dose (µg per animal)"); ax.set_ylabel("Lung Ifnb1 at 16 h (fold vs untreated)"); ax.set_ylim(0.75, 75)
ax.legend(fontsize=6.8, loc="upper left", bbox_to_anchor=(0.0, 1.0), handletextpad=0.3, borderaxespad=0.2, labelspacing=0.25)
ax.set_title("a  Ifnb1 dose–response  [S08-A, n = 3 per dose]", fontsize=9)

ax = fig.add_subplot(gs[0, 1])
d = c[c.block == "S02-F"]; tx = {"16h": 16, "36h": 36, "72h": 72}
for g in ["PSLN-344", "PSLN-212", "Sham"]:
    q = d[d.group == g]; mm_ = q.groupby("x", sort=False)["value"].agg(["mean", "std"]); t = [tx[i] for i in mm_.index]
    ax.errorbar(t, mm_["mean"], yerr=mm_["std"], color=COL[g], marker="o", ms=5, lw=1.6, capsize=3, label={"PSLN-344": "PSLN-344, aged", "PSLN-212": "PSLN-212, aged", "Sham": "Sham, aged"}[g])
    ax.scatter([tx[i] + {"PSLN-344": -1.2, "PSLN-212": 0, "Sham": 1.2}[g] for i in q.x], q.value, color=COL[g], s=8, alpha=0.45, zorder=1)
ax.set_xticks([16, 36, 72]); ax.set_xlabel("Hours after intranasal vaccine + adjuvant"); ax.set_ylabel("Lung Gm-csf (fold vs untreated)"); ax.legend(fontsize=7.5)
ax.set_title("b  Gm-csf time course in aged lung  [S02-F, n = 5]", fontsize=9)

ax = fig.add_subplot(gs[1, :])
G = pd.read_csv(f"{O}/S09A_geomean_fold.csv")
cols = ["CMP-204", "PSLN-R848", "PSLN-212/R848", "PSLN-212", "PSLN-344", "PSLN-212(y)"]
clab = ["CMP-204\n(cGAMP)\naged", "PSLN-R848\naged", "PSLN-212/R848\naged", "PSLN-212\n(no Mn)\naged", "PSLN-344\n(with Mn)\naged", "PSLN-212\nyoung\nbenchmark"]
an = ["Ifnb1", "Il6", "Ccl2", "Ccl3", "Ccl5", "Tnf", "Il10"]
M = []
for pan in ["16h (panel 1)", "72h (panel 2, printed '16h')"]:
    q = G[G.panel == pan].set_index("x").loc[an, cols]; M.append(q.values)
M = np.hstack([M[0], np.full((len(an), 1), np.nan), M[1]])
im = ax.imshow(np.log10(M), cmap="RdBu_r", norm=TwoSlopeNorm(vmin=-1.2, vcenter=0, vmax=3.2), aspect="auto")
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        if not np.isnan(M[i, j]):
            v = M[i, j]; ax.text(j, i, f"{v:.0f}" if v >= 10 else f"{v:.1f}", ha="center", va="center", fontsize=7.6, color="white" if (v > 60 or v < 0.2) else "black")
ax.set_xticks(list(range(6)) + list(range(7, 13))); ax.set_xticklabels(clab * 2, fontsize=6.8); ax.set_yticks(range(len(an))); ax.set_yticklabels(an, fontsize=8.5, style="italic")
ax.tick_params(length=0); [sp.set_visible(False) for sp in ax.spines.values()]
ax.text(2.5, -0.72, "16 hours", ha="center", fontsize=9, fontweight="bold"); ax.text(9.5, -0.72, "72 hours  (panel printed “16h” in the workbook; identified as 72 h — see text)", ha="center", fontsize=9, fontweight="bold")
for j in (4, 11): ax.add_patch(plt.Rectangle((j - 0.5, -0.5), 1, len(an), fill=False, ec=COL["PSLN-344"], lw=2))
cb = fig.colorbar(im, ax=ax, fraction=0.018, pad=0.012, ticks=[-1, 0, 1, 2, 3]); cb.ax.set_yticklabels(["0.1×", "1×", "10×", "100×", "1000×"], fontsize=7); cb.outline.set_visible(False)
ax.set_title("c  Lung transcripts, geometric-mean fold vs untreated  [S09-A, n = 3; printed as log10 in the workbook]", fontsize=9, pad=22)
fig.savefig("/tmp/outputs/figures/fig4_innate_pharmacodynamics.png", bbox_inches="tight")

# ------------------------------------------------------------------ Figure 5
b = pd.read_csv("/tmp/outputs/analysis/tidy/bodyweight.csv", keep_default_na=False); b["value"] = pd.to_numeric(b["value"], errors="coerce"); b["day"] = b["day"].astype(float)
fig, axs = plt.subplots(1, 3, figsize=(11.6, 3.7), gridspec_kw=dict(wspace=0.33, width_ratios=[1.05, 1, 1.05]))
ax = axs[0]; q = b[b.block == "S08-D"]
for g, lab in [("Vaccine", "Vaccine alone"), ("PSLN-212", "PSLN-212"), ("PSLN-344", "PSLN-344"), ("CMP-204", "CMP-204"), ("PSLN-212/R848", "PSLN-212/R848")]:
    gg = q[q.group == g]
    for an_, ga in gg.groupby("animal"): ax.plot(ga.day, ga.value, color=COL[g], lw=0.5, alpha=0.35)
    mm_ = gg.groupby("day")["value"].mean(); ax.plot(mm_.index, mm_.values, color=COL[g], lw=2, marker="o", ms=3.5, label=lab)
ax.axhline(100, color="#BBBBBB", lw=0.6); ax.set_ylim(83, 104); ax.set_xlabel("Days after intranasal vaccination (no challenge)"); ax.set_ylabel("Body weight (% of day 0)")
ax.legend(fontsize=6.8, loc="lower left", labelspacing=0.25); ax.set_title("a  Weight after dosing, aged  [S08-D, n = 5]", fontsize=8.6)
ax.annotate("1 of 5 has no\nday-10 value", xy=(8, 88.3), xytext=(4.7, 84.4), fontsize=6.6, color=COL["PSLN-212/R848"], arrowprops=dict(arrowstyle="-", color=COL["PSLN-212/R848"], lw=0.6))

ax = axs[1]; q = c[c.block == "S10-A"]; order = ["PBS", "Sham", "PSLN-344", "CT"]; colr = {"PBS": "#BBBBBB", "Sham": "#7F7F7F", "PSLN-344": COL["PSLN-344"], "CT": COL["CT"]}
for i, an_ in enumerate(["Ifnb1", "Tnf", "Isg15"]):
    for j, g in enumerate(order):
        v = q[(q.x == an_) & (q.group == g)].value; x0 = i + (j - 1.5) * 0.2
        ax.bar(x0, v.mean(), width=0.18, color=colr[g], label={"PBS": "PBS", "Sham": "Vaccine + empty liposome", "PSLN-344": "Vaccine + PSLN-344", "CT": "Vaccine + cholera toxin\n(positive control)"}[g] if i == 0 else None, zorder=2)
        ax.errorbar(x0, v.mean(), yerr=v.std(ddof=1), color="k", lw=0.8, capsize=2, zorder=3); ax.scatter([x0] * len(v), v, color="k", s=5, zorder=4, alpha=0.6)
ax.axhline(1, color="#999999", lw=0.6, ls=":"); ax.set_xticks(range(3)); ax.set_xticklabels(["Ifnb1", "Tnf", "Isg15"], style="italic"); ax.set_ylabel("CNS transcript at 36 h (fold vs untreated)")
ax.legend(fontsize=6.6, loc="upper right"); ax.set_title("b  CNS transcripts, aged  [S10-A, n = 5]", fontsize=8.6)

ax = axs[2]; G2 = G.set_index(["panel", "x"])
labs = ["Tnf", "Il6", "Il10", "Ifnb1"]; w = 0.26
for k, (g, lab) in enumerate([("PSLN-212(y)", "PSLN-212, young"), ("PSLN-212", "PSLN-212, aged"), ("PSLN-344", "PSLN-344, aged")]):
    vals = [G2.loc[("72h (panel 2, printed '16h')", a), g] for a in labs]
    ax.bar(np.arange(len(labs)) + (k - 1) * w, vals, width=w * 0.92, color=COL["PSLN-212(Y)" if g.endswith("(y)") else g], label=lab, zorder=2)
    for i, v in enumerate(vals): ax.text(i + (k - 1) * w, v * 1.08, f"{v:.1f}", ha="center", va="bottom", fontsize=6.5)
ax.axhline(1, color="#999999", lw=0.6, ls=":"); ax.set_yscale("log"); ax.set_ylim(0.08, 30); ax.set_yticks([0.1, 1, 10]); ax.set_yticklabels(["0.1×", "1×", "10×"])
ax.set_xticks(range(len(labs))); ax.set_xticklabels(labs, style="italic"); ax.set_ylabel("Lung transcript at 72 h (fold vs untreated)"); ax.legend(fontsize=7, loc="upper right")
ax.set_title("c  Lung transcripts at 72 h  [S09-A, n = 3]", fontsize=8.6)
fig.savefig("/tmp/outputs/figures/fig5_tolerability.png", bbox_inches="tight")
print("ok")
