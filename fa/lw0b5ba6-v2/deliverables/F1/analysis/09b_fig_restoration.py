"""Figure 3: how much of the young-adult response does each preparation recover in aged animals?"""
import numpy as np, pandas as pd
from figstyle import *
from matplotlib.lines import Line2D
R = pd.read_csv('../tables/T7_restoration_table.csv')
cats = [
 ('Innate trigger', ['S01-A 16h']),
 ('Myeloid recruitment, dendritic-cell migration and priming', ['S01-D (x=4)', 'S01-E (x=4)', 'S01-F', 'S02-A', 'S02-B', 'S02-C', 'S02-D CD40', 'S02-D CD86', 'S02-E']),
 ('CD8 T cells', ['S05-D', 'S05-E', 'S05-F', 'S14-A H1N1', 'S14-A H3N2', 'S05-G', 'S05-H', 'S05-I']),
 ('Follicular helper T cells, germinal centre, B cells', ['S04-A ICOShi', 'S04-A ICOSlo', 'S03-K', 'S13-H']),
 ('Serum antibody (geometric mean titre)', ['S03-C', 'S03-G', 'S03-D', 'S03-H', 'S03-A', 'S03-E', 'S13-A', 'S13-C', 'S13-B', 'S13-D', 'S13-I', 'S13-J']),
 ('Regulatory populations (lower = closer to young)', ['S04-B Foxp3', 'S04-C', 'S04-D', 'S11-E']),
]
SHORT = {'Ifnb1 lung 16 h (fold)': 'Lung Ifnb1, 16 h', '% lung monocytes d4': 'Lung monocytes, day 4', '% lung CD11b+ DC d4': 'Lung CD11b⁺ DC, day 4', '% lung cDC1 72 h': 'Lung cDC1, 72 h',
         '% CCR7+ lung CD11b+ DC 72 h': 'CCR7⁺ lung DC, 72 h', '% MLN CD11b+CD103- DC 72 h': 'Node CD11b⁺ DC, 72 h', '% OVA+ MLN DC 36 h': 'Antigen⁺ node DC, 36 h',
         '% CD40+ MLN CD11b+ DC d3': 'CD40⁺ node DC, day 3', '% CD86+ MLN CD11b+ DC d3': 'CD86⁺ node DC, day 3', 'OT-I proliferation by MLN DC (%)': 'T-cell priming by node DC',
         '% Ki-67+ lung CD8 d3': 'Ki-67⁺ lung CD8, day 3', '% GZMB+ lung CD8 d3': 'Granzyme-B⁺ lung CD8, day 3', '% IFN-g+ CD8 MLN d14 (rgH5N1 restim)': 'IFN-γ⁺ CD8, H5N1 restim., day 14',
         '% IFN-g+ CD8 MLN (H1N1 restim)': 'IFN-γ⁺ CD8, H1N1 restim.', '% IFN-g+ CD8 MLN (H3N2 restim)': 'IFN-γ⁺ CD8, H3N2 restim.', '% IFN-g+ CD8 MLN d60': 'IFN-γ⁺ CD8, day 60',
         '% GZMB+ CD8 MLN d60': 'Granzyme-B⁺ CD8, day 60', '% lung CD8 TRM d25': 'Lung resident-memory CD8, day 25', '% Tfh ICOS-hi MLN d7': 'Tfh ICOS-high, day 7', '% Tfh ICOS-lo MLN d7': 'Tfh ICOS-low, day 7',
         '% GC B cells MLN d7': 'Germinal-centre B cells, day 7', '% IgG+ MLN B cells': 'IgG⁺ node B cells', 'HAI H1N1 d14': 'HAI, H1N1, day 14', 'HAI H3N2 d14': 'HAI, H3N2, day 14',
         'Neutralising H1N1 d14': 'Neutralising, H1N1, day 14', 'Neutralising H3N2 d14': 'Neutralising, H3N2, day 14', 'IgG anti-H1N1 d14': 'IgG, H1N1, day 14', 'IgG anti-H3N2 d14': 'IgG, H3N2, day 14',
         'IgG2a anti-H1N1 d14': 'IgG2a, H1N1, day 14', 'IgG2a anti-H3N2 d14': 'IgG2a, H3N2, day 14', 'IgG1 anti-H1N1 d14': 'IgG1, H1N1, day 14', 'IgG1 anti-H3N2 d14': 'IgG1, H3N2, day 14',
         'IgG anti-H1N1 d28 (boost d14)': 'IgG, H1N1, day 28 after boost', 'IgG anti-H3N2 d28 (boost d14)': 'IgG, H3N2, day 28 after boost',
         '% Tfr (Foxp3+ of CXCR5+) d7': 'Follicular regulatory T, day 7', '% Tfr d30': 'Follicular regulatory T, day 30', '% lung Treg d7': 'Lung regulatory T, day 7', '% CD206+ lung macrophages': 'CD206⁺ lung macrophages'}
n = sum(len(b) for _, b in cats) + len(cats) * 1.35
fig, ax = plt.subplots(figsize=(W, 0.158 * n + 1.0))
fig.subplots_adjust(left=0.36, right=0.77, top=0.922, bottom=0.068)
y = 0; yt = []; yl = []
for cat, bl in cats:
    ax.text(-0.86, y, cat, fontsize=6.8, fontweight='bold', va='center', ha='left', transform=ax.get_yaxis_transform())
    y += 1
    for b in bl:
        r = R[R.block == b].iloc[0]; a, c = r['a212_pct_of_young'], r['a344_pct_of_young']
        ax.plot([a, c], [y, y], color='#bbbbbb', lw=0.9, zorder=1)
        ax.scatter([a], [y], s=17, color=COL['PSLN-212'], edgecolor='k', lw=0.35, zorder=3); ax.scatter([c], [y], s=17, color=COL['PSLN-344'], edgecolor='k', lw=0.35, zorder=3)
        p = r['p_344_vs_212']; ptxt = 'p<0.0001' if p < 1e-4 else f'p={p:.2g}'
        ax.text(1.04, y, f"{a:.0f}% → {c:.0f}%   {r['fold_344_vs_212']:.1f}×,  {ptxt}", va='center', fontsize=6.1, transform=ax.get_yaxis_transform())
        yt.append(y); yl.append(f"{SHORT[r['readout']]}  [{b.split(' (')[0].replace(' 16h', '')}]"); y += 1
    y += 0.35
ax.set_yticks(yt); ax.set_yticklabels(yl, fontsize=6.2)
ax.set_xscale('log'); ax.set_xlim(1.3, 520); ax.set_ylim(y - 0.6, -0.9)
ax.axvline(100, color=COL['PSLN-212(Y)'], lw=1.5, ls='--', zorder=0)
ax.set_xticks([2, 5, 10, 20, 50, 100, 200, 400]); ax.set_xticklabels(['2', '5', '10', '20', '50', '100', '200', '400'])
ax.set_xlabel('Response in aged mice, % of the young-adult PSLN-212 response (log scale)')
ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
fig.legend(handles=[Line2D([], [], marker='o', ls='', ms=4.5, color=COL['PSLN-212'], mec='k', mew=0.35, label='PSLN-212, aged'), Line2D([], [], marker='o', ls='', ms=4.5, color=COL['PSLN-344'], mec='k', mew=0.35, label='PSLN-344, aged'),
                    Line2D([], [], color=COL['PSLN-212(Y)'], lw=1.5, ls='--', label='young-adult PSLN-212 = 100%')], frameon=False, loc='upper left', bbox_to_anchor=(0.01, 0.972), ncol=3, fontsize=6.6)
fig.text(0.012, 0.994, 'Figure 3. How much of the young-adult immune response each asset recovers in aged mice', fontsize=8.2, fontweight='bold', va='top')
fig.text(0.787, 0.932, '212 → 344, % of young;\nfold 344 / 212; Tukey p', fontsize=5.8, color='#333333', va='bottom', linespacing=1.2)
fig.text(0.012, 0.006, 'DC = dendritic cells; Tfh = follicular helper T cells; HAI = haemagglutination inhibition; restim. = restimulated in vitro. Titres: p on log2 scale.', fontsize=5.6, color='#333333', va='bottom')
fig.savefig('../figures/Fig3_immune_restoration.png'); plt.close(fig)
up = R[R.block.isin(sum([bl for _, bl in cats[:5]], []))]
print(len(up), round(up.a344_pct_of_young.median(), 1), round(up.a212_pct_of_young.median(), 1))
