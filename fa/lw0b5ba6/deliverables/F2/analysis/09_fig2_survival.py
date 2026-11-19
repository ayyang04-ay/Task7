#!/usr/bin/env python
"""Figure 1 - survival in every lethal-challenge experiment in aged animals, + pooled estimate."""
import pandas as pd, numpy as np, sys
sys.path.insert(0, "/tmp/outputs/analysis")
from figstyle import *
from scipy import stats
style()
O = "/tmp/outputs/analysis/stats"
A = pd.read_csv(f"{O}/survival_by_arm.csv", keep_default_na=False)
REC = pd.read_csv(f"{O}/survival_reconciliation.csv", keep_default_na=False)
def cp(k, n):
    lo = 0.0 if k == 0 else stats.beta.ppf(0.025, k, n - k + 1); hi = 1.0 if k == n else stats.beta.ppf(0.975, k + 1, n - k)
    return 100 * lo, 100 * hi
rows = [  # (label, block, {role: group})
 ("Matched strain, d14 †\nbivalent → CA09 H1N1  [S03-I]", "S03-I", dict(sham="Sham", p212="PSLN-212", p344="PSLN-344", young="PSLN-212(Y)")),
 ("Wild-type H5N1, d2 after one dose †\nrgH5N1 vaccine → VN04  [S03-J]", "S03-J", dict(sham="Sham", p212="PSLN-212", p344="PSLN-344")),
 ("Cross-subtype, d14\nH3N2 → PR8 H1N1  [S06-A]", "S06-A", dict(sham="Sham", p212="PSLN-212", p344="PSLN-344", young="PSLN-212(Y)")),
 ("Cross-subtype, d14\nbivalent → rgH5N1  [S06-C]", "S06-C", dict(sham="Sham", p212="PSLN-212", p344="PSLN-344", young="PSLN-212(Y)")),
 ("Cross-subtype, d3\nH3N2 → PR8 H1N1  [S06-B]", "S06-B", dict(sham="Sham", p212="PSLN-212", p344="PSLN-344", young="PSLN-212(Y)")),
 ("Cross-subtype, d3 ‡\nbivalent → rgH5N1  [S06-D]", "S06-D", dict(sham="Sham", p212="PSLN-212", p344="PSLN-344", young="PSLN-212(Y)")),
 ("Cross-subtype, d3 (component control)\nbivalent → rgH5N1  [S15-H]", "S15-H", dict(sham="3d Vaccine", p344="3d Vaccine+PSLN-344", alone="3d PSLN-344")),
 ("Cross-subtype, d60\nH3N2 → PR8 H1N1  [S06-E]", "S06-E", dict(sham="Sham", p212="PSLN-212", p344="PSLN-344", young="PSLN-212(Y)", unt="Untreated")),
 ("Cross-subtype, d60\nbivalent → rgH5N1  [S06-F]", "S06-F", dict(sham="Sham", p212="PSLN-212", p344="PSLN-344", young="PSLN-212(Y)", unt="Untreated")),
 ("Cross-subtype, d60\nH1N1 → Perth H3N2  [S06-G]", "S06-G", dict(sham="Sham", p212="PSLN-212", p344="PSLN-344", young="PSLN-212(Y)", unt="Untreated")),
 ("14-month, naive; → PR8 H1N1\n[S06-E, 2nd block]", "S06-E(2) imprinting/PR8", dict(p212="Naive+PSLN-212", p344="Naive+PSLN-344")),
 ("14-month, PR8-imprinted; → PR8 H1N1\n[S06-E, 2nd block]", "S06-E(2) imprinting/PR8", dict(p212="Imprinting+PSLN-212", p344="Imprinting+PSLN-344")),
 ("14-month, naive; → Perth H3N2\n[S06-F, 2nd block]", "S06-F(2) imprinting/Perth", dict(p212="Naive+PSLN-212", p344="Naive+PSLN-344")),
 ("14-month, PR8-imprinted; → Perth H3N2\n[S06-F, 2nd block]", "S06-F(2) imprinting/Perth", dict(p212="Imprinting+PSLN-212", p344="Imprinting+PSLN-344")),
 ("Aged C57BL/6; challenge not stated\n[S15-L]", "S15-L", dict(sham="Sham", p212="PSLN-212", p344="PSLN-344", young="PSLN-212(Y)")),
 ("Aged Swiss Webster (outbred);\nchallenge not stated  [S15-N]", "S15-N", dict(sham="Sham", p212="PSLN-212", p344="PSLN-344", young="PSLN-212(Y)")),
]
role_style = {"sham": ("Sham", "s", "Sham / vaccine alone (aged)"), "p212": ("PSLN-212", "D", "PSLN-212, no Mn (aged)"), "p344": ("PSLN-344", "o", "PSLN-344 (aged)"),
              "young": ("PSLN-212(Y)", "^", "PSLN-212 in young animals (benchmark)"), "unt": ("Untreated", "x", "Untreated, unchallenged aged animals"),
              "alone": ("PSLN-R848", "P", "PSLN-344 alone, no vaccine (aged)")}
off = {"sham": 0.27, "p212": 0.09, "p344": -0.09, "young": -0.27, "unt": 0.36, "alone": -0.27}
fig, ax = plt.subplots(figsize=(9.6, 10.2))
N = len(rows); seen = set()
for i, (lab, blk, roles) in enumerate(rows):
    y0 = N - i
    ax.axhspan(y0 - 0.5, y0 + 0.5, color="#F4F4F4" if i % 2 == 0 else "white", zorder=0)
    for role, grp in roles.items():
        r = A[(A.block == blk) & (A.group == grp)].iloc[0]; k, n = int(r.survivors), int(r.n); pct = 100 * k / n
        colkey, mk, leg = role_style[role]; y = y0 + off[role]
        if role == "p344":
            lo, hi = cp(k, n); ax.plot([lo, hi], [y, y], color=COL[colkey], lw=1.2, alpha=0.6, zorder=2)
        ax.scatter([pct], [y], marker=mk, s=70 if role == "p344" else 36, color=COL[colkey], zorder=3, label=leg if role not in seen else None,
                   edgecolor="white" if mk != "x" else None, linewidth=0.6)
        seen.add(role)
        if role in ("p344",):
            # body-weight-implied value if different
            rr = REC[(REC.tte_block == blk) & (REC.group == grp)].iloc[0]
            note = f"{k}/{n}"
            if rr.survivors_agree == "NO": note += f"  (weights: {rr.bw_survivors})"
            ax.text(104, y0 - 0.09, note, va="center", ha="left", fontsize=8, color=COL["PSLN-344"], fontweight="bold")
        if role == "p212":
            rr = REC[(REC.tte_block == blk) & (REC.group == grp)].iloc[0]
            note = f"{k}/{n}" + (f"  (weights: {rr.bw_survivors})" if rr.survivors_agree == "NO" else "")
            ax.text(140, y0 - 0.09, note, va="center", ha="left", fontsize=8, color="#B37700")
# pooled
P = pd.read_csv(f"{O}/survival_pooled.csv")
y = -0.3
ax.axhline(0.5, color="k", lw=0.8)
for j, (reading, lab) in enumerate([("TTE", "Pooled, as printed"), ("WORST", "Pooled, worst case for PSLN-344")]):
    yy = -0.1 - j * 0.9
    r2 = P[(P.reading == reading) & P.comparator.str.startswith("PSLN-212")].iloc[0]; rs = P[(P.reading == reading) & P.comparator.str.startswith("Sham")].iloc[0]
    for val, ci, colkey, mk, o in [(r2.psln344_pct, r2.psln344_ci, "PSLN-344", "o", -0.09), (r2.comparator_pct, r2.comparator_ci, "PSLN-212", "D", 0.09), (rs.comparator_pct, rs.comparator_ci, "Sham", "s", 0.27)]:
        lo, hi = [float(x) for x in ci.split("-")]
        ax.plot([lo, hi], [yy + o, yy + o], color=COL[colkey], lw=1.6); ax.scatter([val], [yy + o], marker=mk, s=80, color=COL[colkey], zorder=3, edgecolor="k", linewidth=0.6)
    ax.text(104, yy - 0.09, r2.psln344, va="center", fontsize=8, color=COL["PSLN-344"], fontweight="bold")
    ax.text(140, yy - 0.09, r2.comparator_surv, va="center", fontsize=8, color="#B37700")
    ax.text(140, yy + 0.27, f"sham {rs.comparator_surv}", va="center", fontsize=7.5, color=COL["Sham"])
ylabels = [r[0] for r in rows] + ["POOLED (15 comparisons)\nsurvival blocks as printed", "POOLED, worst case\nfor PSLN-344 (see text)"]
ax.set_yticks(list(range(N, 0, -1)) + [-0.1, -1.0]); ax.set_yticklabels(ylabels, fontsize=7.6)
ax.set_xlim(-4, 178); ax.set_ylim(-1.6, N + 0.7); ax.set_xticks([0, 20, 40, 60, 80, 100]); ax.set_xlabel("Survival at end of observation (%)")
ax.text(104, N + 0.62, "PSLN-344", fontsize=8, color=COL["PSLN-344"], fontweight="bold"); ax.text(140, N + 0.62, "PSLN-212", fontsize=8, color="#B37700", fontweight="bold")
ax.axvline(100, color="#DDDDDD", lw=0.6, zorder=1)
h, l = ax.get_legend_handles_labels()
order = ["PSLN-344 (aged)", "PSLN-212, no Mn (aged)", "Sham / vaccine alone (aged)", "PSLN-212 in young animals (benchmark)", "Untreated, unchallenged aged animals", "PSLN-344 alone, no vaccine (aged)"]
hl = dict(zip(l, h)); ax.legend([hl[o] for o in order if o in hl], [o for o in order if o in hl], loc="upper center", bbox_to_anchor=(0.40, -0.055), ncol=2, fontsize=8)
ax.set_title("Survival after lethal influenza challenge — every aged-animal experiment in the workbook", fontsize=9.5, x=-0.42)
fig.text(0.01, 0.0, "Points: survivors / n from the time-to-event blocks (n = 7 per arm; 10 in S03-J). Bars: exact 95% CI for PSLN-344. “(weights: k/n)” = survivors implied by the paired body-weight\n"
         "block where it disagrees with the time-to-event block. † comparator-arm labels differ between the survival block and its body-weight block. ‡ Sham and PSLN-212 arms are\n"
         "identical to S06-C. Pooled rows: each experiment is its own stratum; worst case = lower of the two readings for PSLN-344, higher for comparators. Scripts 04, 05.", fontsize=6.8, color="#444444")
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig("/tmp/outputs/figures/fig2_survival_all_aged_experiments.png", bbox_inches="tight")
print("ok")
