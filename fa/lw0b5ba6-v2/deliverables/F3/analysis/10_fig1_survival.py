"""Figure 1 - survival at end of observation in every aged-animal challenge experiment (survival tables as printed)."""
import json, numpy as np
from scipy import stats
from figstyle import *
B = json.load(open('/tmp/work/parsed/parsed_blocks.json'))
def sn(bid, g):
    a = B[bid]['groups'][g]; return sum(1 for x in a if x['event'] == 0), len(a)
def cp(k, n):
    lo = 0.0 if k == 0 else stats.beta.ppf(.025, k, n - k + 1); hi = 1.0 if k == n else stats.beta.ppf(.975, k + 1, n - k); return 100 * lo, 100 * hi
rows = [
 ('Challenge 2-3 days after one dose', None),
 ('S03-J', 'rgH5N1 vaccine → wild-type H5N1, day 2 †'),
 ('S06-B', 'H3N2 vaccine → H1N1 (PR8), day 3'),
 ('S06-D', 'H1N1+H3N2 vaccine → rgH5N1, day 3'),
 ('Challenge 14 days after one dose', None),
 ('S03-I', 'H1N1+H3N2 vaccine → matched H1N1 (CA09), day 14 †'),
 ('S06-A', 'H3N2 vaccine → H1N1 (PR8), day 14'),
 ('S06-C', 'H1N1+H3N2 vaccine → rgH5N1, day 14'),
 ('Challenge 60 days after one dose', None),
 ('S06-E_r34', 'H3N2 vaccine → H1N1 (PR8), day 60'),
 ('S06-F_r34', 'H1N1+H3N2 vaccine → rgH5N1, day 60'),
 ('S06-G', 'H1N1 vaccine → H3N2 (Perth), day 60'),
 ('Other strains (challenge virus not stated)', None),
 ('S15-L', 'C57BL/6, 20 months'),
 ('S15-N', 'Swiss Webster, 20 months'),
]
groups = ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']
mk = {'Sham': ('X', 46), 'PSLN-212': ('o', 52), 'PSLN-344': ('o', 52), 'PSLN-212(Y)': ('D', 34)}
off = {'Sham': 0.30, 'PSLN-212': 0.10, 'PSLN-344': -0.10, 'PSLN-212(Y)': -0.30}
fig, ax = plt.subplots(figsize=(8.8, 8.0))
y = 0; tot = {g: [0, 0] for g in groups}
XL = -5; XR = 106
for bid, lab in rows:
    if lab is None:
        ax.text(XL, y + 0.05, bid, fontsize=8.8, fontweight='bold', va='center', ha='right', clip_on=False); y += 0.85; continue
    vals = {}
    for g in groups:
        if g in B[bid]['groups']:
            s, n = sn(bid, g); vals[g] = (s, n); tot[g][0] += s; tot[g][1] += n
    p2 = 100 * vals['PSLN-212'][0] / vals['PSLN-212'][1]; p3 = 100 * vals['PSLN-344'][0] / vals['PSLN-344'][1]
    ax.plot([p2, p3], [y + off['PSLN-212'], y + off['PSLN-344']], color='#CFCFCF', lw=2.0, zorder=1, solid_capstyle='round')
    for g, (s, n) in vals.items():
        ax.scatter(100 * s / n, y + off[g], marker=mk[g][0], s=mk[g][1], color=COL[g] if g != 'PSLN-212(Y)' else 'white', edgecolor=COL[g], linewidth=1.3, zorder=3, clip_on=False)
    ax.text(XL, y, lab, fontsize=8.2, va='center', ha='right', clip_on=False)
    ax.text(XR, y, f"{bid.replace('_r34', ''):<6} {vals['PSLN-344'][0]:>2}/{vals['PSLN-344'][1]:<2}  vs {vals['PSLN-212'][0]:>2}/{vals['PSLN-212'][1]:<2}", fontsize=8, va='center', ha='left', clip_on=False, family='DejaVu Sans Mono')
    y += 1
y += 0.25
ax.axhline(y - 0.7, color='#555555', lw=0.8)
ax.text(XL, y, 'All 11 experiments pooled\n(exact 95% CI)', fontsize=8.8, fontweight='bold', va='center', ha='right', clip_on=False)
for g in groups:
    s, n = tot[g]; lo, hi = cp(s, n)
    ax.plot([lo, hi], [y + off[g] * 1.35, y + off[g] * 1.35], color=COL[g], lw=1.6, zorder=2)
    ax.scatter(100 * s / n, y + off[g] * 1.35, marker=mk[g][0], s=mk[g][1], color=COL[g] if g != 'PSLN-212(Y)' else 'white', edgecolor=COL[g], linewidth=1.3, zorder=3, clip_on=False)
ax.text(XR, y, f"{'pooled':<6} {tot['PSLN-344'][0]}/{tot['PSLN-344'][1]}  vs {tot['PSLN-212'][0]}/{tot['PSLN-212'][1]}\n{'':<6} sham {tot['Sham'][0]}/{tot['Sham'][1]}; young {tot['PSLN-212(Y)'][0]}/{tot['PSLN-212(Y)'][1]}",
        fontsize=8, va='center', ha='left', clip_on=False, family='DejaVu Sans Mono')
ax.set_ylim(y + 0.75, -0.75); ax.set_xlim(-2.5, 102.5); ax.set_yticks([])
ax.set_xticks([0, 25, 50, 75, 100]); ax.set_xlabel('Animals alive at end of observation (%)')
ax.spines['left'].set_visible(False)
for x in [0, 25, 50, 75, 100]: ax.axvline(x, color='#EDEDED', lw=0.8, zorder=0)
ax.text(XR, -0.02, 'block    344   vs  212', fontsize=8, fontweight='bold', ha='left', va='center', clip_on=False, family='DejaVu Sans Mono')
h = [plt.Line2D([], [], marker=mk[g][0], ls='', markersize=7, markerfacecolor=COL[g] if g != 'PSLN-212(Y)' else 'white', markeredgecolor=COL[g], markeredgewidth=1.3, label=NICE[g]) for g in ['PSLN-344', 'PSLN-212', 'Sham', 'PSLN-212(Y)']]
fig.legend(handles=h, loc='lower center', bbox_to_anchor=(0.5, 0.075), ncol=2, frameon=False, columnspacing=1.6, handletextpad=0.3)
fig.text(0.02, 0.012, '† Group labels in this survival table differ from those in its paired body-weight table (S13-G, S13-F); PSLN-344 result unaffected.\n'
         'Aged = 20 months or older, female; n = 7 per arm (10 in S03-J). Survival tables as printed. Analysis: 06_survival.py.', fontsize=7.2, color='#444444', va='bottom')
fig.suptitle('Survival after lethal influenza challenge in aged mice, by experiment', x=0.02, y=0.985, ha='left', fontsize=11, fontweight='bold')
fig.subplots_adjust(left=0.43, right=0.755, top=0.945, bottom=0.205)
fig.savefig(FIGDIR + 'fig1_survival_by_experiment.png')
print('ok', tot)
