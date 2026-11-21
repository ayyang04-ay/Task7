"""Figure 5 - what the workbook says about tolerability of the adjuvant itself."""
import json, numpy as np
from figstyle import *
import matplotlib.gridspec as gridspec
from matplotlib.colors import TwoSlopeNorm
B = json.load(open('/tmp/work/parsed/parsed_blocks.json'))
fig = plt.figure(figsize=(9.2, 9.0))
gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1.12], width_ratios=[1.05, 1], hspace=0.62, wspace=0.24, left=0.075, right=0.945, top=0.925, bottom=0.085)

# (a) body weight after immunization
ax = fig.add_subplot(gs[0, 0]); b = B['S08-D']
sty = {'Vaccine': ('#8A8A8A', 'Vaccine alone', 's', '--'), 'PSLN-212(Y)': (COL['PSLN-212(Y)'], 'PSLN-212, young', 'D', '-'), 'CMP-204': (COL['CMP-204'], 'CMP-204 (cGAMP)', 'v', '-'),
       'PSLN-212': (COL['PSLN-212'], 'PSLN-212', 'o', '-'), 'PSLN-344': (COL['PSLN-344'], 'PSLN-344', 'o', '-'), 'PSLN-212/R848': ('#7A5200', 'PSLN-212/R848', '^', '-')}
days = [int(t) for t in b['times']]
for g in ['Vaccine', 'PSLN-212(Y)', 'CMP-204', 'PSLN-212', 'PSLN-344', 'PSLN-212/R848']:
    c, lab, mk, ls = sty[g]
    mean = [np.mean([x for x in b['groups'][g][t] if x is not None]) for t in b['times']]
    sd = [np.std([x for x in b['groups'][g][t] if x is not None], ddof=1) for t in b['times']]
    ax.errorbar(days, mean, yerr=sd, color=c, marker=mk, ms=4.5, lw=1.7 if g in ('PSLN-344', 'PSLN-212/R848') else 1.1, ls=ls, capsize=2, elinewidth=0.7, label=lab, zorder=3 if g == 'PSLN-344' else 2)
ax.axhline(100, color='#BBBBBB', lw=0.7, zorder=0); ax.set_ylim(83, 103.5); ax.set_xticks(days)
ax.set_xlabel('Days after intranasal immunization (no virus challenge)'); ax.set_ylabel('Body weight (% of day 0)')
ax.annotate('4 of 5 animals\nhave a day-10 value', xy=(10, 90.6), xytext=(6.4, 84.6), fontsize=7, color='#7A5200', arrowprops=dict(arrowstyle='-', color='#7A5200', lw=0.7))
ax.legend(frameon=False, fontsize=7.2, loc='upper center', ncol=3, columnspacing=1.0, handlelength=1.6, bbox_to_anchor=(0.5, -0.2))
ax.set_title('a  Body weight after dosing, aged mice  [S08-D]', fontsize=9)

# (c) CNS transcripts
ax = fig.add_subplot(gs[0, 1])
cg = {'PBS': '#BDBDBD', 'Sham': '#8A8A8A', 'PSLN-344': COL['PSLN-344'], 'CT': '#222222'}
lab = {'PBS': 'Buffer', 'Sham': 'Vaccine + empty liposome', 'PSLN-344': 'Vaccine + PSLN-344', 'CT': 'Vaccine + cholera toxin (positive control)'}
for j, an in enumerate(['Ifnb1', 'Tnf', 'Isg15']):
    g = B[f'S10-A_{an}']['groups']
    for i, k in enumerate(['PBS', 'Sham', 'PSLN-344', 'CT']):
        x0 = j * 5 + i; v = np.array(g[k], float)
        ax.scatter(x0 + np.linspace(-0.2, 0.2, 5), v, s=20, color=cg[k], edgecolor='white', linewidth=0.4, zorder=3, label=lab[k] if j == 0 else None)
        ax.plot([x0 - 0.32, x0 + 0.32], [np.mean(v)] * 2, color=cg[k], lw=2, zorder=2)
ax.axhline(1, color='#BBBBBB', lw=0.7, zorder=0)
ax.set_xticks([1.5, 6.5, 11.5]); ax.set_xticklabels(['Ifnb1', 'Tnf', 'Isg15'], fontstyle='italic'); ax.tick_params(axis='x', length=0)
ax.set_ylabel('CNS transcript (fold vs untreated)'); ax.set_ylim(0, 8.2)
ax.legend(frameon=False, fontsize=7.2, loc='upper right', handletextpad=0.2, borderaxespad=0.1)
ax.set_title('b  Brain transcripts 36 h after dosing  [S10-A]', fontsize=9)

# (b) cytokine heatmap
gs2 = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=gs[1, :], width_ratios=[50, 1], wspace=0.03)
ax = fig.add_subplot(gs2[0]); cax = fig.add_subplot(gs2[1])
grp = ['CMP-204', 'PSLN-212', 'PSLN-344', 'PSLN-212(y)', 'PSLN-R848', 'PSLN-212/R848']
gl = ['CMP-204', 'PSLN-212', 'PSLN-344', 'PSLN-212\nyoung', 'PSLN-\nR848', 'PSLN-212\n/R848']
an = ['Ifnb1', 'Il6', 'Ccl2', 'Ccl3', 'Ccl5', 'Tnf', 'Il10']
M = np.full((len(an), 13), np.nan)
for pi, pid in enumerate(['S09-A_panel1', 'S09-A_panel2']):
    for gi, g in enumerate(grp):
        for ai, a in enumerate(an):
            M[ai, pi * 7 + gi] = float(np.mean(B[pid]['groups'][g][a]))
im = ax.imshow(M, cmap='RdBu_r', norm=TwoSlopeNorm(vmin=-1.2, vcenter=0, vmax=3.2), aspect='auto')
for ai in range(len(an)):
    for ci in range(13):
        if not np.isnan(M[ai, ci]):
            f = 10 ** M[ai, ci]
            ax.text(ci, ai, f"{f:,.0f}" if f >= 10 else f"{f:.1f}", ha='center', va='center', fontsize=7.4, color='white' if (M[ai, ci] > 1.9 or M[ai, ci] < -0.8) else '#111111')
ax.set_xticks(list(range(6)) + list(range(7, 13))); ax.set_xticklabels(gl * 2, fontsize=7.1)
ax.set_yticks(range(len(an))); ax.set_yticklabels(an, fontstyle='italic', fontsize=8.5)
ax.tick_params(length=0)
for s in ax.spines.values(): s.set_visible(False)
ax.add_patch(plt.Rectangle((1.5, -0.5), 1, 7, fill=False, ec=COL['PSLN-344'], lw=2, clip_on=False)); ax.add_patch(plt.Rectangle((8.5, -0.5), 1, 7, fill=False, ec=COL['PSLN-344'], lw=2, clip_on=False))
ax.text(2.5, -0.72, '16 h after dosing', ha='center', va='bottom', fontsize=8.2, fontweight='bold')
ax.text(9.5, -0.72, 'Second panel: labeled 16 h, consistent with 72 h (see text)', ha='center', va='bottom', fontsize=8.2, fontweight='bold')
cb = fig.colorbar(im, cax=cax, ticks=[-1, 0, 1, 2, 3]); cb.ax.set_yticklabels(['0.1', '1', '10', '100', '1,000'], fontsize=7); cb.set_label('fold vs untreated', fontsize=7.5)
ax.set_title('c  Lung cytokine transcripts after adjuvant alone (fold vs untreated, n = 3)  [S09-A]', fontsize=9, pad=26)
fig.suptitle('Tolerability signals in the workbook', x=0.01, ha='left', fontsize=11, fontweight='bold', y=0.99)
fig.text(0.01, 0.006, 'a: mean ± SD, n = 5. b: dots = animals (n = 5), bars = means. c: numbers are fold-change (10^mean of log10 values); all groups aged except "young";\nblue outline = lead candidate. Analysis 08_safety_tolerability.py.', fontsize=7, color='#444444', va='bottom')
fig.savefig(FIGDIR + 'fig5_tolerability.png')
