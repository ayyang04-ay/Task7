"""Figure 6: pharmacodynamics (dose-response, kinetics).  Figure 4: safety / tolerability read-outs.  Drawn at printed size."""
import numpy as np, pandas as pd
from figstyle import *
import matplotlib.patches as mp
import tidy
DR = pd.read_csv('../tables/T8_dose_response_S08A.csv').set_index('prep')
def model(p, x):
    emax, ed50, h = p
    return 1 + emax * x ** h / (ed50 ** h + x ** h)

# ------------------------------------------------------------------ Figure 5
fig, axes = plt.subplots(1, 3, figsize=(W, 2.75), gridspec_kw=dict(width_ratios=[1.05, 1.25, 0.9]))
fig.subplots_adjust(left=0.065, right=0.99, top=0.80, bottom=0.27, wspace=0.36)
ax = axes[0]
d = tidy.get('S08-A'); xs = np.linspace(0.8, 45, 200)
for g in ['CMP-204', 'PSLN-212', 'PSLN-344/R848', 'PSLN-344']:
    s = d[d.group == g]
    ax.scatter(s.x, s.value, s=6, color=COL[g], alpha=0.8, zorder=3, lw=0)
    p = (DR.loc[g, 'Emax'], DR.loc[g, 'ED50_ug'], DR.loc[g, 'hill'])
    ax.plot(xs, model(p, xs), color=COL[g], ls='--' if 'R848' in g else '-', lw=1.2)
    ax.text(48, model(p, 45) + {'PSLN-212': 1.5, 'CMP-204': -1.5}.get(g, 0), {'CMP-204': 'CMP-204', 'PSLN-344/R848': '"344/R848"', 'PSLN-212': 'PSLN-212', 'PSLN-344': 'PSLN-344'}[g], color=COL[g], fontsize=5.6, va='center', fontweight='bold')
yb = tidy.vec('S01-A 16h', 'PSLN-212(Y)').mean()
ax.axhline(yb, color=COL['PSLN-212(Y)'], ls=':', lw=1.0); ax.text(0.85, yb + 1.6, 'young mice,\nPSLN-212 20 µg', color='#2e7d32', fontsize=5.6, va='bottom', linespacing=1.0)
ax.set_xscale('log'); ax.set_xlim(0.75, 190); ax.set_xticks([1, 5, 10, 20, 40]); ax.set_xticklabels(['1', '5', '10', '20', '40']); ax.minorticks_off()
ax.set_xlabel('Dose (µg)', x=0.36); ax.set_ylabel('Lung Ifnb1 at 16 h (fold)'); ax.set_ylim(-2, 62)
ax.set_title('a  Dose–response [S08-A]', loc='left')
ax = axes[1]
order = ['Sham', 'CMP-204', 'PSLN-R848', 'PSLN-212/R848', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)', 'PSLN-344(Y)']
xl = ['Sham', 'CMP-204', 'R848', '212/R848', 'PSLN-212', 'PSLN-344', 'PSLN-212', 'PSLN-344']
w = 0.38
for i, g in enumerate(order):
    a = tidy.vec('S01-A 16h', g); b = tidy.vec('S01-A 72h', g)
    ax.bar(i - w / 2, a.mean(), w, color=COL[g], edgecolor='k', lw=0.35); ax.bar(i + w / 2, b.mean(), w, color=COL[g], edgecolor='k', lw=0.35, alpha=0.45, hatch='////')
    ax.scatter(np.full(5, i - w / 2) + np.linspace(-0.1, 0.1, 5), a, s=2.5, color='k', zorder=3, lw=0); ax.scatter(np.full(5, i + w / 2) + np.linspace(-0.1, 0.1, 5), b, s=2.5, color='k', zorder=3, lw=0)
ax.set_xticks(range(len(order))); ax.set_xticklabels(xl, fontsize=5.7, rotation=40, ha='right', rotation_mode='anchor')
ax.set_ylabel('Lung Ifnb1 (fold)'); ax.set_title('b  16 h (solid) and 72 h (hatched) [S01-A]', loc='left')
ax.axvspan(-0.5, 5.5, color='#f2f2f2', zorder=0); ax.text(2.5, 61, 'aged', ha='center', fontsize=6, color='#555555'); ax.text(6.5, 61, 'young', ha='center', fontsize=6, color='#555555'); ax.set_ylim(0, 66)
ax = axes[2]
d = tidy.get('S02-F')
for g in ['Sham', 'PSLN-212', 'PSLN-344']:
    s = d[d.group == g]; mm = s.groupby('x')['value'].mean(); sd = s.groupby('x')['value'].std()
    ax.errorbar(mm.index, mm.values, yerr=sd.values, color=COL[g], marker='o', ms=2.8, capsize=1.8, lw=1.2, elinewidth=0.7, label={'Sham': 'Sham', 'PSLN-212': 'PSLN-212', 'PSLN-344': 'PSLN-344'}[g])
ax.set_xticks([16, 36, 72]); ax.set_xlabel('Hours after dose'); ax.set_ylabel('Lung Gm-csf (fold)'); ax.set_ylim(0, 12.5)
ax.set_title('c  Gm-csf, aged [S02-F]', loc='left'); ax.legend(frameon=False, fontsize=5.8, loc='upper right')
fig.text(0.012, 0.985, 'Figure 6. Pharmacodynamics: Mn²⁺ raises the maximal interferon response and adds a GM-CSF signal', fontsize=8.2, fontweight='bold', va='top')
fig.text(0.012, 0.010, f'a: n = 3 per dose; age not stated (values match aged animals). Fitted maxima: PSLN-344 {DR.loc["PSLN-344","Emax"]:.0f}×, "PSLN-344/R848" {DR.loc["PSLN-344/R848","Emax"]:.0f}×, PSLN-212 {DR.loc["PSLN-212","Emax"]:.0f}×, CMP-204 {DR.loc["CMP-204","Emax"]:.0f}×. "PSLN-344/R848" is printed in the\n'
         'workbook but not described in the annotation (Q11).  b: n = 5; dots are animals; R848 = PSLN-R848, 212/R848 = PSLN-212/R848.  c: n = 5, mean ± SD.', fontsize=5.6, color='#333333', va='bottom', linespacing=1.35)
fig.savefig('../figures/Fig6_pharmacodynamics.png'); plt.close(fig)

# ------------------------------------------------------------------ Figure 6  (2 columns x 3 rows)
fig = plt.figure(figsize=(W, 8.1)); gs = fig.add_gridspec(3, 2, hspace=0.56, wspace=0.30, top=0.925, bottom=0.092, left=0.085, right=0.985)
ax = fig.add_subplot(gs[0, 0])
d = tidy.get('S08-D')
LAB = {'Vaccine': 'Vaccine alone', 'PSLN-212(Y)': 'PSLN-212, young', 'CMP-204': 'CMP-204, aged', 'PSLN-212': 'PSLN-212, aged', 'PSLN-344': 'PSLN-344, aged', 'PSLN-212/R848': 'PSLN-212/R848, aged'}
for g in ['Vaccine', 'PSLN-212(Y)', 'CMP-204', 'PSLN-212', 'PSLN-344', 'PSLN-212/R848']:
    s = d[d.group == g]; mm = s.groupby('x')['value'].mean(); sd = s.groupby('x')['value'].std()
    ax.errorbar(mm.index + {'PSLN-344': 0.12, 'PSLN-212': -0.12}.get(g, 0), mm.values, yerr=sd.values, color=COL[g], marker='o', ms=2.5, capsize=1.6, elinewidth=0.6,
                lw=1.8 if g == 'PSLN-344' else 1.0, ls='--' if g == 'PSLN-212(Y)' else '-', label=LAB[g])
ax.text(10.2, 88.6, 'n = 4', fontsize=5.6, color=COL['PSLN-212/R848'], va='center')
ax.set_xlim(-0.4, 11.6); ax.set_ylim(82, 104); ax.set_xticks([0, 2, 4, 6, 8, 10]); ax.set_xlabel('Days after dose (no challenge)'); ax.set_ylabel('Body weight (% of day 0)')
ax.set_title('a  Body weight after dosing [S08-D]', loc='left'); ax.legend(frameon=False, fontsize=5.6, loc='lower left', handlelength=1.5)
genes = ['Ifnb1', 'Il6', 'Ccl2', 'Ccl3', 'Ccl5', 'Tnf', 'Il10']
groups = ['CMP-204', 'PSLN-212', 'PSLN-344', 'PSLN-212(y)', 'PSLN-R848', 'PSLN-212/R848']
gl = ['CMP-204', 'PSLN-212', 'PSLN-344', 'PSLN-212\nyoung', 'R848', '212/R848']
for pos, panel, tt in [((0, 1), 'S09-A[A:U]', 'b  Lung transcripts, 16 h [S09-A, cols A–U]'), ((1, 0), 'S09-A[X:AS]', 'c  Lung transcripts, 72 h* [S09-A, cols X–AS]')]:
    ax = fig.add_subplot(gs[pos])
    M = np.array([[tidy.vec(f'{panel} {g_}', gr).mean() for gr in groups] for g_ in genes])
    im = ax.imshow(M, cmap='RdBu_r', vmin=-3.2, vmax=3.2, aspect='auto')
    for a in range(M.shape[0]):
        for b in range(M.shape[1]):
            v = 10 ** M[a, b]
            ax.text(b, a, f'{v:,.0f}×' if v >= 10 else f'{v:.1f}×', ha='center', va='center', fontsize=5.9, color='white' if abs(M[a, b]) > 1.7 else 'black')
    ax.set_xticks(range(len(groups))); ax.set_xticklabels(gl, fontsize=5.7); ax.set_yticks(range(len(genes))); ax.set_yticklabels(genes, fontsize=6.3, style='italic')
    ax.set_title(tt, loc='left'); ax.spines[:].set_visible(False); ax.tick_params(length=0); ax.axvline(3.5, color='k', lw=0.7)
ax = fig.add_subplot(gs[1, 1])
gg = ['PBS', 'Sham', 'PSLN-344', 'CT']; cc = ['#d9d9d9', COL['Sham'], COL['PSLN-344'], COL['CT']]
for i, gene in enumerate(['Ifnb1', 'Tnf', 'Isg15']):
    for k, g in enumerate(gg):
        v = tidy.vec(f'S10-A {gene}', g); x = i * 5 + k
        ax.bar(x, v.mean(), 0.8, color=cc[k], edgecolor='k', lw=0.35); ax.errorbar(x, v.mean(), yerr=v.std(ddof=1), color='k', capsize=1.6, lw=0.6)
        ax.scatter(np.full(len(v), x) + np.linspace(-0.2, 0.2, len(v)), v, s=2.5, color='k', zorder=3, lw=0)
ax.set_xticks([1.5, 6.5, 11.5]); ax.set_xticklabels(['Ifnb1', 'Tnf', 'Isg15'], style='italic'); ax.set_ylabel('Brain transcript (fold)'); ax.set_ylim(0, 10.6)
ax.legend(handles=[mp.Patch(fc=c_, ec='k', lw=0.35, label=l_) for c_, l_ in zip(cc, ['Buffer', 'Sham (vaccine + empty liposome)', 'Vaccine + PSLN-344', 'Vaccine + cholera toxin (positive control)'])], frameon=False, fontsize=5.6, loc='upper right')
ax.set_title('d  Brain transcripts, 36 h [S10-A]', loc='left')
LB = {'Sham': 'Sham', 'PSLN-212': 'PSLN-212, aged', 'PSLN-344': 'PSLN-344, aged', 'PSLN-212(Y)': 'PSLN-212, young', 'PSLN-344(Y)': 'PSLN-344, young'}
for j, (b, tt, yl) in enumerate([('S01-D', 'e  Lung monocytes [S01-D]', '% lung monocytes'), ('S01-E', 'f  Lung CD11b⁺ dendritic cells [S01-E]', '% CD11b⁺ dendritic cells')]):
    ax = fig.add_subplot(gs[2, j]); d = tidy.get(b)
    for g in tidy.groups(b):
        s = d[d.group == g]; mm = s.groupby('x')['value'].mean(); sd = s.groupby('x')['value'].std()
        ax.errorbar(mm.index, mm.values, yerr=sd.values, color=COL[g], marker='o', ms=2.5, capsize=1.6, elinewidth=0.6, ls='--' if '(Y)' in g else '-', lw=1.8 if g == 'PSLN-344' else 1.0, label=LB[g])
    ax.set_xticks([0, 2, 4, 6, 8]); ax.set_xlabel('Days after dose'); ax.set_ylabel(yl); ax.set_title(tt, loc='left'); ax.legend(frameon=False, fontsize=5.6, loc='upper left', handlelength=1.5)
    ax.annotate('still above baseline\non day 8; nothing\nmeasured later', xy=(8, d[(d.group == 'PSLN-344') & (d.x == 8)].value.mean()), xytext=(0.66, 0.80), textcoords='axes fraction',
                fontsize=5.5, color=COL['PSLN-344'], ha='left', arrowprops=dict(arrowstyle='->', color=COL['PSLN-344'], lw=0.6))
    ax.set_xlim(-0.3, 9.9)
fig.text(0.012, 0.992, 'Figure 4. Safety and tolerability read-outs available in the dataset', fontsize=8.2, fontweight='bold', va='top')
fig.text(0.012, 0.967, 'No histopathology, clinical chemistry, manganese biodistribution or repeat-dose data exist.', fontsize=6.4, color='#7f0000', va='top')
fig.text(0.012, 0.008, 'a, d, e, f: n = 5, mean ± SD; dots in d are animals.  b, c: n = 3, geometric-mean fold change over untreated; the vertical rule separates the R848 preparations\n'
         '(R848 = PSLN-R848; 212/R848 = PSLN-212/R848).  *c is printed "16 h" in the workbook; its Ifnb1 values are the 72 h values of S01-A (Q8).  Groups are aged unless marked young.',
         fontsize=5.6, color='#333333', va='bottom', linespacing=1.35)
fig.savefig('../figures/Fig4_safety.png'); plt.close(fig)
print('ok')
