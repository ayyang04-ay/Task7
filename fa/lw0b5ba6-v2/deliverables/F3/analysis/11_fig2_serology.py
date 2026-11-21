"""Figure 2 - serology 14 days after one intranasal dose (aged mice + young benchmark): individual animals and GMT."""
import json, numpy as np
from figstyle import *
B = json.load(open('/tmp/work/parsed/parsed_blocks.json'))
G = lambda b: B[b]['groups']
panels = [('S03-A', 'IgG (ELISA endpoint titer)', 'H1N1 (CA09)'), ('S03-C', 'Hemagglutination inhibition', 'H1N1 (CA09)'), ('S03-D', 'Neutralizing titer', 'H1N1 (CA09)'),
          ('S03-E', 'IgG (ELISA endpoint titer)', 'H3N2 (Aichi)'), ('S03-G', 'Hemagglutination inhibition', 'H3N2 (Aichi)'), ('S03-H', 'Neutralizing titer', 'H3N2 (Aichi)')]
order = ['Sham', 'CMP-204', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']
xl = ['Sham', 'CMP-\n204', 'PSLN-\n212', 'PSLN-\n344', 'PSLN-212\nyoung']
rng = np.random.default_rng(3)
fig, axes = plt.subplots(2, 3, figsize=(9.2, 6.3))
for ax, (bid, name, virus) in zip(axes.ravel(), panels):
    hai = bid in ('S03-C', 'S03-G')
    for i, g in enumerate(order):
        v = np.array([5 if (x == 0 and hai) else x for x in G(bid)[g]], float)
        xs = i + np.linspace(-0.16, 0.16, len(v))
        ax.scatter(xs, v, s=26, color=COL[g], edgecolor='white', linewidth=0.5, zorder=3, alpha=0.95)
        gmt = np.exp(np.mean(np.log(v)))
        ax.plot([i - 0.3, i + 0.3], [gmt, gmt], color=COL[g], lw=2.2, zorder=2)
        ax.text(i, max(v) * (1.75 if not hai else 1.32), f"{gmt:,.0f}", ha='center', va='bottom', fontsize=7.6, color=COL[g], fontweight='bold')
    ax.set_yscale('log', base=2)
    if hai:
        ax.axhline(40, color='#777777', ls='--', lw=0.9, zorder=1); ax.text(4.45, 40, '1:40', fontsize=7, va='bottom', ha='right', color='#555555')
        ax.axhline(10, color='#BBBBBB', ls=':', lw=0.9, zorder=1); ax.text(4.45, 10, 'lowest dilution tested', fontsize=6.5, va='bottom', ha='right', color='#888888')
        ax.set_yticks([5, 10, 20, 40, 80, 160, 320, 640]); ax.set_yticklabels(['<10', '10', '20', '40', '80', '160', '320', '640']); ax.set_ylim(3.5, 1500)
    else:
        ticks = [2 ** k * 10 for k in range(0, 13, 2)]
        ax.set_yticks(ticks); ax.set_yticklabels([f"{t:,}" for t in ticks]); ax.set_ylim(8, 90000)
    ax.set_xticks(range(5)); ax.set_xticklabels(xl, fontsize=7.4); ax.set_xlim(-0.55, 4.55)
    ax.set_title(f"{name}\n{virus}   [{bid}]", fontsize=8.6)
    ax.tick_params(axis='x', length=0)
    ax.minorticks_off()
    ax.axvspan(3.5, 4.55, color='#F3F7F4', zorder=0)
for ax in axes[:, 0]: ax.set_ylabel('Reciprocal titer (log scale)')
fig.suptitle('Antibody titers 14 days after one intranasal dose of vaccine + adjuvant', x=0.01, ha='left', fontsize=10.5, fontweight='bold', y=0.995)
fig.text(0.01, 0.005, 'Dots = individual animals (n = 5 per group); bars and numbers = geometric mean titer (GMT). All groups are aged (20 months or older)\n'
         'except the shaded young benchmark. HAI values recorded as 0 are plotted as <10 (set to 5 for the GMT). Source blocks in panel titles;\n'
         'analysis 07_immunogenicity_moa.py.', fontsize=7, color='#444444', va='bottom')
fig.tight_layout(rect=(0, 0.06, 1, 0.965))
fig.savefig(FIGDIR + 'fig2_serology.png')
