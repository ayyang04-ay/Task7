#!/usr/bin/env python
"""
08_figures.py -- figures for the proposal, sized for a 7.4-inch (A4 portrait) text block.
Run: micromamba run -n core python 08_figures.py      Writes PNGs to ../figures/
"""
import os, warnings
import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy import stats
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, 'parsed'); T = os.path.join(HERE, 'tables')
F = os.path.join(HERE, '..', 'figures'); os.makedirs(F, exist_ok=True)
sc = pd.read_csv(f'{P}/scalar_long.csv', keep_default_na=False); sc['factor'] = sc.factor.astype(str)
sv = pd.read_csv(f'{P}/survival_long.csv', keep_default_na=False); sv['day'] = pd.to_numeric(sv.day, errors='coerce'); sv['group'] = sv.group.str.replace('Naïve', 'Naive')
wt = pd.read_csv(f'{P}/weight_long.csv', keep_default_na=False); wt['group'] = wt.group.str.replace('Naïve', 'Naive')
W = 7.4
plt.rcParams.update({'font.size': 7, 'axes.spines.top': False, 'axes.spines.right': False, 'savefig.dpi': 250, 'axes.titlesize': 7.5, 'axes.labelsize': 7,
                     'legend.frameon': False, 'xtick.labelsize': 6.5, 'ytick.labelsize': 6.5, 'axes.linewidth': 0.6, 'xtick.major.width': 0.6, 'ytick.major.width': 0.6})
COL = {'Sham': '#8c8c8c', 'PSLN-212': '#e08214', 'PSLN-344': '#1f5fa8', 'PSLN-212(Y)': '#4d9a4d', 'CMP-204': '#b28fce', 'Untreated': '#222222', 'Naive': '#c9c9c9', 'Vaccine': '#8c8c8c'}
LAB = {'Sham': 'Aged + vaccine + empty liposome (Sham)', 'PSLN-212': 'Aged + vaccine + PSLN-212 (no Mn)', 'PSLN-344': 'Aged + vaccine + PSLN-344 (asset)',
       'PSLN-212(Y)': 'Young + vaccine + PSLN-212 (benchmark)', 'Untreated': 'Aged, untreated, NOT challenged'}
def cp(k, n, a=0.05):
    lo = 0.0 if k == 0 else stats.beta.ppf(a / 2, k, n - k + 1); hi = 1.0 if k == n else stats.beta.ppf(1 - a / 2, k + 1, n - k); return lo, hi
def km(t, e, tmax):
    t, e = np.asarray(t, float), np.asarray(e); xs, ys = [0], [1.0]; s = 1.0
    for tj in np.unique(t[e == 1]):
        s_new = s * (1 - ((t == tj) & (e == 1)).sum() / (t >= tj).sum()); xs += [tj, tj]; ys += [s, s_new]; s = s_new
    xs.append(tmax); ys.append(s); return xs, ys

# ================================================================== Figure 1: survival overview
rows1 = [('S03-I', 'homologous H1N1 (10x LD50), day 14', 'Aged BALB/c, challenged 2-14 days after one dose'),
         ('S03-J', 'wild-type H5N1 after rgH5N1 vaccine, day 2', 'Aged BALB/c, challenged 2-14 days after one dose'),
         ('S06-A', 'H3N2 vaccine → H1N1, day 14', 'Aged BALB/c, challenged 2-14 days after one dose'),
         ('S06-B', 'H3N2 vaccine → H1N1, day 3', 'Aged BALB/c, challenged 2-14 days after one dose'),
         ('S06-C', 'H1N1+H3N2 vaccine → rgH5N1, day 14', 'Aged BALB/c, challenged 2-14 days after one dose'),
         ('S06-D', 'H1N1+H3N2 vaccine → rgH5N1, day 3', 'Aged BALB/c, challenged 2-14 days after one dose'),
         ('S06-E', 'H3N2 vaccine → H1N1, day 60', 'Aged BALB/c, challenged 60 days after one dose'),
         ('S06-F', 'H1N1+H3N2 vaccine → rgH5N1, day 60', 'Aged BALB/c, challenged 60 days after one dose'),
         ('S06-G', 'H1N1 vaccine → H3N2, day 60', 'Aged BALB/c, challenged 60 days after one dose'),
         ('S15-L', 'aged C57BL/6 (challenge not stated)', 'Other aged strains'),
         ('S15-N', 'aged Swiss Webster (challenge not stated)', 'Other aged strains')]
order = ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)', 'Untreated']; off = {'Sham': 0.30, 'PSLN-212': 0.15, 'PSLN-344': 0.0, 'PSLN-212(Y)': -0.15, 'Untreated': -0.30}
fig, ax = plt.subplots(figsize=(W, 5.3))
ypos = {}; yy = 0; prev = None; sec = []
for b, lab, s_ in rows1:
    if s_ != prev:
        yy += 0.95 if prev is not None else 0.0; sec.append((yy - 0.66, s_)); prev = s_
    ypos[b] = yy; yy += 1
X0, DX = 110, 13.5
for b, lab, s_ in rows1:
    y0 = ypos[b]
    for g in order:
        d = sv[(sv.block == b) & (sv.group == g)]
        if not len(d): continue
        k, n = int((d.event == 0).sum()), len(d); lo, hi = cp(k, n)
        ax.errorbar(100 * k / n, y0 + off[g], xerr=[[100 * (k / n - lo)], [100 * (hi - k / n)]], fmt='o' if g != 'Untreated' else 's', color=COL[g], ms=5.5 if g == 'PSLN-344' else 3.6,
                    capsize=1.5, lw=0.8, mfc=COL[g] if g != 'Untreated' else 'white', zorder=3 if g == 'PSLN-344' else 2)
        ax.text(X0 + order.index(g) * DX, y0, f'{k}/{n}', ha='center', va='center', fontsize=6.8, color=COL[g], fontweight='bold' if g == 'PSLN-344' else 'normal')
for j, g in enumerate(['Sham', '212', '344', 'Young', 'No virus']):
    ax.text(X0 + j * DX, -0.78, g, ha='center', va='bottom', fontsize=6.0, color=COL[order[j]], fontweight='bold')
ax.text(X0 + 2 * DX, -1.22, 'survivors / animals', ha='center', va='bottom', fontsize=6.2, color='#555555')
for ys_, s_ in sec:
    ax.text(-2, ys_, s_, fontsize=6.8, style='italic', color='#444444', ha='left', va='center'); ax.axhline(ys_ + 0.14, color='#e3e3e3', lw=0.6, xmin=0, xmax=0.62)
ax.set_yticks([ypos[b] for b, _, _ in rows1]); ax.set_yticklabels([f'{b}  {lab}' for b, lab, _ in rows1], fontsize=6.8)
ax.set_ylim(yy - 0.4, -1.6); ax.set_xlim(-3, X0 + 4.6 * DX); ax.set_xticks([0, 25, 50, 75, 100]); ax.spines['bottom'].set_bounds(0, 100)
ax.set_xlabel('Survivors at end of observation, % (exact 95% CI)' + ' ' * 52)
ax.legend(handles=[Line2D([], [], marker='o' if g != 'Untreated' else 's', ls='', ms=4, color=COL[g], mfc=COL[g] if g != 'Untreated' else 'white', label=LAB[g]) for g in order],
          loc='upper center', bbox_to_anchor=(0.30, -0.10), ncol=2, fontsize=6.5, columnspacing=1.0, handletextpad=0.3)
fig.suptitle('Figure 1. Survival after lethal influenza challenge following ONE intranasal dose\n(survival tables as printed; 7 animals per arm, 10 rows per arm in S03-J)', fontsize=8, x=0.01, ha='left', y=0.995)
fig.tight_layout(rect=(0, 0, 1, 0.985)); fig.savefig(f'{F}/fig1_survival_overview.png', bbox_inches='tight'); plt.close(fig)

# ================================================================== Figure A1: KM grid
grid = [('S03-I', 'homologous H1N1, d14'), ('S03-J', 'wild-type H5N1, d2'), ('S06-A', 'H3N2 vacc → H1N1, d14'), ('S06-B', 'H3N2 vacc → H1N1, d3'),
        ('S06-C', 'bivalent → rgH5N1, d14'), ('S06-D', 'bivalent → rgH5N1, d3'), ('S06-E', 'H3N2 vacc → H1N1, d60'), ('S06-F', 'bivalent → rgH5N1, d60'),
        ('S06-G', 'H1N1 vacc → H3N2, d60'), ('S15-L', 'aged C57BL/6'), ('S15-N', 'aged Swiss Webster'), ('S15-H', 'components, rgH5N1, d3'),
        ('S06-E(r71)', '14-mo, PR8 challenge'), ('S06-F(r71)', '14-mo, Perth H3N2 challenge')]
C2 = dict(COL); C2.update({'3d Vaccine': '#8c8c8c', '3d PSLN-344': '#74a9cf', '3d Vaccine+PSLN-344': '#1f5fa8', 'Naive+PSLN-212': '#e08214', 'Imprinting+PSLN-212': '#a6611a',
                           'Naive+PSLN-344': '#1f5fa8', 'Imprinting+PSLN-344': '#0b2f5b'})
SHORT = {'PSLN-212(Y)': 'Young+212', 'Untreated': 'Unchallenged', '3d Vaccine': 'Vaccine only', '3d PSLN-344': '344 only', '3d Vaccine+PSLN-344': 'Vaccine+344',
         'Naive+PSLN-212': 'Naive+212', 'Imprinting+PSLN-212': 'Imprinted+212', 'Naive+PSLN-344': 'Naive+344', 'Imprinting+PSLN-344': 'Imprinted+344', 'PSLN-212': '212', 'PSLN-344': '344'}
fig, axes = plt.subplots(4, 4, figsize=(W, 8.0)); axes = axes.ravel()
for axx, (b, ttl) in zip(axes, grid):
    d = sv[sv.block == b]; tmax = 22 if b == 'S03-J' else 14
    for j, g in enumerate(d.group.unique()):
        x = d[(d.group == g) & d.day.notna()]; xs, ys = km(x.day, x.event, tmax)
        axx.plot(xs, 100 * (np.array(ys) + (j - 2) * 0.008), color=C2.get(g, 'k'), lw=1.5 if '344' in g else 0.9,
                 ls='--' if g in ('Untreated', '3d PSLN-344', 'Imprinting+PSLN-212', 'Imprinting+PSLN-344') else '-', label=SHORT.get(g, g))
    axx.set_title(f"{b.replace('(r71)', ' rows 71-105')}\n{ttl}", fontsize=6.3); axx.set_ylim(-5, 108); axx.set_xlim(0, tmax); axx.set_yticks([0, 50, 100])
    axx.legend(fontsize=4.8, loc='lower left', handlelength=1.4, labelspacing=0.2, borderaxespad=0.2)
for axx in axes[len(grid):]: axx.axis('off')
for axx in axes[12:14]: axx.set_xlabel('days after challenge', fontsize=6.5)
for axx in axes[::4]: axx.set_ylabel('% surviving', fontsize=6.5)
fig.suptitle('Figure A1. Kaplan-Meier curves for every challenge block with aged or 14-month hosts\n(curves offset slightly so that overlapping lines stay visible)', fontsize=8, x=0.01, ha='left', y=0.998)
fig.tight_layout(rect=(0, 0, 1, 0.985)); fig.savefig(f'{F}/figA1_km_grid.png', bbox_inches='tight'); plt.close(fig)

# ================================================================== Figure 2: restoration cascade
T7 = pd.read_csv(f'{T}/T07_restoration_index_curated.csv')
SL = {'Antigen-carrying DC in draining node, 36 h': 'Antigen-carrying DC in node, 36 h', 'CCR7+ migratory CD11b+ DC (lung), 72 h': 'CCR7+ migratory DC (lung), 72 h',
      'IFN-g+ CD8 vs rgH5N1 (cross-reactive), day 14': 'IFN-g+ CD8 vs rgH5N1, day 14', 'IgG2a:IgG1 anti-H1N1 (recomputed S13-A/S13-B)': 'IgG2a:IgG1 anti-H1N1 (recomputed)',
      'IgG2a:IgG1 anti-H3N2 (recomputed S13-C/S13-D)': 'IgG2a:IgG1 anti-H3N2 (recomputed)', 'Survival, heterosubtypic challenge d3/d14 (4 expts pooled)': 'Survival, heterosubtypic, day 3/14 (4 expts)',
      'Survival, heterosubtypic challenge d60 (3 expts pooled)': 'Survival, heterosubtypic, day 60 (3 expts)', 'IgG anti-H1N1 after boost, day 28 (GMT)': 'IgG anti-H1N1 after boost (GMT)',
      'IgG anti-H3N2 after boost, day 28 (GMT)': 'IgG anti-H3N2 after boost (GMT)', 'Follicular regulatory T (Foxp3+), day 7': 'Follicular regulatory T, day 7'}
fig, ax = plt.subplots(figsize=(W, 9.3))
ys = []; yy = 0; prev = None; sec_y = []
for r in T7.itertuples():
    if r.step != prev:
        yy += 0.9; sec_y.append((yy - 0.1, r.step)); yy += 0.85; prev = r.step
    ys.append(yy); yy += 1
XN1, XN2, XB = 420, 760, 900
for yi, r in zip(ys, T7.itertuples()):
    a, b = r.aged212_pct_of_young, r.aged344_pct_of_young
    ax.plot([a, b], [yi, yi], color='#c4c4c4', lw=0.8, zorder=1)
    ax.plot([r.pct_lo, r.pct_hi], [yi, yi], color=COL['PSLN-344'], lw=3.6, alpha=0.25, zorder=2, solid_capstyle='butt')
    ax.scatter(a, yi, color=COL['PSLN-212'], s=14, zorder=3); ax.scatter(b, yi, color=COL['PSLN-344'], s=20, zorder=4)
    ax.text(XN1, yi, f'{a:.0f}%', color=COL['PSLN-212'], fontsize=6.2, va='center', ha='right')
    ax.text(XN2, yi, f'{b:.0f}%', color=COL['PSLN-344'], fontsize=6.2, va='center', ha='right', fontweight='bold')
    ax.text(XB, yi, r.block.replace('S06-A+S06-B+S06-C+S06-D', 'S06-A..D').replace('S06-E+S06-F+S06-G', 'S06-E..G').replace('S13-A/S13-B', 'S13-A, S13-B').replace('S13-C/S13-D', 'S13-C, S13-D'),
            color='#555555', fontsize=5.8, va='center', ha='left')
for y0, s_ in sec_y:
    ax.text(1.25, y0, s_.split(' ', 1)[1].replace('(inverted)', '(lower = younger; plotted inverted)').replace('->', 'to'), fontsize=7, fontweight='bold', color='#333333', va='center', ha='left')
ax.text(XN1, -0.3, 'aged\n+212', color=COL['PSLN-212'], fontsize=6.2, ha='right', va='bottom'); ax.text(XN2, -0.3, 'aged\n+344', color=COL['PSLN-344'], fontsize=6.2, ha='right', va='bottom', fontweight='bold')
ax.text(XB, -0.3, 'source\nblock', color='#555555', fontsize=6.2, ha='left', va='bottom')
ax.plot([100, 100], [0.4, yy - 0.3], color=COL['PSLN-212(Y)'], lw=1.1, ls='--', zorder=0)
ax.set_xscale('log'); ax.set_xlim(1.2, 4200); ax.set_ylim(yy, -1.9)
ax.set_xticks([2, 5, 10, 25, 50, 100, 200]); ax.set_xticklabels(['2', '5', '10', '25', '50', '100', '200']); ax.minorticks_off(); ax.spines['bottom'].set_bounds(1.5, 220)
ax.set_yticks(ys); ax.set_yticklabels([SL.get(r.label, r.label).replace('IFN-g+', 'IFN-γ⁺') for r in T7.itertuples()], fontsize=6.5); ax.tick_params(axis='y', length=0)
ax.set_xlabel('Response in aged mice as % of the young + PSLN-212 benchmark (log scale)' + ' ' * 48, fontsize=6.8)
ax.legend(handles=[Line2D([], [], marker='o', ls='', ms=4, color=COL['PSLN-212'], label='Aged + PSLN-212 (no Mn)'), Line2D([], [], marker='o', ls='', ms=4.5, color=COL['PSLN-344'], label='Aged + PSLN-344 (bar = 95% CI)'),
                   Line2D([], [], ls='--', color=COL['PSLN-212(Y)'], label='Young + PSLN-212 = 100%')], loc='lower center', bbox_to_anchor=(0.33, 1.0), ncol=3, fontsize=6.5, columnspacing=1.2)
fig.suptitle('Figure A3. How much of the young-adult response PSLN-344 restores in aged mice, step by step (n = 5 per group unless noted)', fontsize=8, x=0.01, ha='left', y=0.998)
fig.tight_layout(rect=(0, 0, 1, 0.985)); fig.savefig(f'{F}/figA3_restoration_cascade.png', bbox_inches='tight'); plt.close(fig)

# ================================================================== Figure A2: safety / tolerability / dose (2 x 2)
fig, axes = plt.subplots(2, 2, figsize=(W, 6.3)); axes = axes.ravel()
axx = axes[0]; d = wt[wt.block == 'S08-D']
cc = {'Vaccine': '#8c8c8c', 'PSLN-212': COL['PSLN-212'], 'PSLN-344': COL['PSLN-344'], 'PSLN-212(Y)': COL['PSLN-212(Y)'], 'CMP-204': COL['CMP-204'], 'PSLN-212/R848': '#c51b1b'}
for g in ['Vaccine', 'PSLN-212(Y)', 'CMP-204', 'PSLN-212', 'PSLN-344', 'PSLN-212/R848']:
    m = d[d.group == g].groupby('day').value.agg(['mean', 'std', 'count'])
    axx.errorbar(m.index, m['mean'], yerr=m['std'], color=cc[g], marker='o', ms=2.5, lw=1.4 if g in ('PSLN-344', 'PSLN-212/R848') else 0.8, capsize=1.5, label=g + (' (n=4 at d10)' if g == 'PSLN-212/R848' else ''))
axx.axhline(100, color='#cccccc', lw=0.6); axx.set_xlabel('days after intranasal immunisation'); axx.set_ylabel('body weight, % of day 0 (mean ± SD, n=5)')
axx.set_title('a  Post-dose body weight, aged mice [S08-D]', loc='left'); axx.legend(fontsize=5.6, loc='lower left'); axx.set_ylim(83, 103)
axx = axes[1]; t = pd.read_csv(f'{T}/T08b_S09A_cytokines.csv'); an = ['Ifnb1', 'Il6', 'Tnf', 'Il10', 'Ccl2']
gg = [('PSLN-212', COL['PSLN-212']), ('PSLN-344', COL['PSLN-344']), ('PSLN-212(y)', COL['PSLN-212(Y)']), ('PSLN-212/R848', '#c51b1b')]; w = 0.1
for pi, (pn, hatch) in enumerate([('16 h (as labelled)', None), ('72 h (labelled 16h; Ifnb1 values = S01-A 72h panel)', '////')]):
    for gi, (g, c) in enumerate(gg):
        v = [t[(t.panel == pn) & (t.analyte == a) & (t.group == g)].geo_fold.values[0] for a in an]
        axx.bar(np.arange(len(an)) + (gi - 1.5) * 2 * w + pi * w, v, width=w, color=c, alpha=1 if pi == 0 else 0.5, hatch=hatch, edgecolor='white' if pi else c, lw=0.2)
axx.set_yscale('log'); axx.axhline(1, color='k', lw=0.5); axx.set_xticks(range(len(an))); axx.set_xticklabels(an, style='italic')
axx.set_ylabel('lung transcript, fold vs untreated (geo. mean, n=3)'); axx.set_title('b  Lung cytokines: solid 16 h, hatched 72 h* [S09-A]', loc='left')
axx.legend(handles=[Line2D([], [], marker='s', ls='', ms=4, color=c, label=g.replace('(y)', ' young').replace('PSLN-212', '212' if False else 'PSLN-212')) for g, c in gg], fontsize=5.6, loc='upper left')
axx.set_xlabel('*the 72 h panel is labelled 16 h in the workbook (Appendix A, #2)', fontsize=5.6, color='#555555')
axx = axes[2]; d = sc[sc.block == 'S10-A']; gs = ['PBS', 'Sham', 'PSLN-344', 'CT']; cs = ['#c9c9c9', '#8c8c8c', COL['PSLN-344'], '#c51b1b']
for ai, a in enumerate(['Ifnb1', 'Tnf', 'Isg15']):
    for gi, g in enumerate(gs):
        v = d[(d.factor == a) & (d.group == g)].value.values; x0 = ai + (gi - 1.5) * 0.2
        axx.bar(x0, v.mean(), width=0.18, color=cs[gi], alpha=0.55); axx.scatter(np.full(len(v), x0) + np.linspace(-0.05, 0.05, len(v)), v, s=5, color=cs[gi], zorder=3, edgecolor='k', lw=0.2)
axx.set_xticks(range(3)); axx.set_xticklabels(['Ifnb1', 'Tnf', 'Isg15'], style='italic'); axx.axhline(1, color='k', lw=0.5)
axx.set_ylabel('CNS transcript, fold vs untreated (36 h, n=5)'); axx.set_title('c  CNS transcripts [S10-A]', loc='left')
axx.legend(handles=[Line2D([], [], marker='s', ls='', ms=4, color=c, label=g if g != 'CT' else 'Cholera toxin (positive control)') for g, c in zip(gs, cs)], fontsize=5.6, loc='upper right')
axx = axes[3]; d = sc[sc.block == 'S08-A'].copy(); d['dose'] = d.factor.astype(float); fit = pd.read_csv(f'{T}/T08e_S08A_dose_response.csv').set_index('group')
for g, c in [('CMP-204', COL['CMP-204']), ('PSLN-212', COL['PSLN-212']), ('PSLN-344', COL['PSLN-344'])]:
    x = d[d.group == g]; axx.scatter(x.dose, x.value, s=7, color=c, alpha=0.8)
    xx = np.linspace(0.8, 45, 200); e, ed, h = fit.loc[g, ['Emax_fold', 'ED50_ug', 'hill']]
    axx.plot(xx, 1 + (e - 1) * xx ** h / (ed ** h + xx ** h), color=c, lw=1.2, label=f'{g}: Emax {e:.0f}x, ED50 {ed:.0f} µg')
axx.axvline(20, color='#999999', ls=':', lw=0.8); axx.text(22.2, 29, 'dose used in all efficacy studies', fontsize=5.4, color='#666666', rotation=90, va='center', ha='left')
axx.set_xscale('log'); axx.set_xticks([1, 5, 10, 20, 40]); axx.set_xticklabels(['1', '5', '10', '20', '40']); axx.minorticks_off(); axx.set_xlabel('adjuvant dose (µg per mouse, intranasal)')
axx.set_ylabel('lung Ifnb1 at 16 h, fold vs untreated (n=3)'); axx.set_title('d  Dose-response [S08-A]', loc='left'); axx.legend(fontsize=5.6, loc='upper left')
fig.suptitle('Figure A2. Tolerability and dose read-outs available in the dataset\n(no histopathology, manganese-exposure or repeat-dose data exist)', fontsize=8, x=0.01, ha='left', y=0.998)
fig.tight_layout(rect=(0, 0, 1, 0.975)); fig.savefig(f'{F}/figA2_safety_dose.png', bbox_inches='tight'); plt.close(fig)

# ================================================================== Figure 4: data-integrity evidence (2 x 2)
fig, axes = plt.subplots(2, 2, figsize=(W, 6.3)); axes = axes.ravel()
axx = axes[0]; a, b = sc[sc.block == 'S13-A'], sc[sc.block == 'S13-B']; pr = sc[sc.block == 'S03-B']; gs = ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']
for i, g in enumerate(gs):
    rec = a[a.group == g].sort_values('rep').value.values / b[b.group == g].sort_values('rep').value.values; p = pr[pr.group == g].sort_values('rep').value.values
    axx.scatter(np.full(5, i - 0.17), p, color='#c51b1b', s=10, label='S03-B as printed' if i == 0 else None)
    axx.scatter(np.full(5, i + 0.17), rec, color='#1f5fa8', s=10, marker='D', label='recomputed: S13-A / S13-B' if i == 0 else None)
    axx.plot([i - 0.27, i - 0.07], [p.mean()] * 2, color='#c51b1b', lw=1); axx.plot([i + 0.07, i + 0.27], [rec.mean()] * 2, color='#1f5fa8', lw=1)
axx.axhline(1, color='#999999', lw=0.5, ls=':'); axx.set_xticks(range(3)); axx.set_xticklabels(['aged\nPSLN-212', 'aged\nPSLN-344', 'young\nPSLN-212'])
axx.set_ylabel('IgG2a : IgG1 (anti-CA09 H1N1)'); axx.set_title('a  S03-B headers are rotated by one column', loc='left'); axx.legend(fontsize=5.8, loc='upper center')
axx = axes[1]; A = sc[sc.block == 'S11-A'].set_index(['group', 'factor', 'rep']).value; B = sc[sc.block == 'S11-B'].set_index(['group', 'factor', 'rep']).value; same = (A == B)
axx.scatter(A[~same], B[~same], s=6, color='#999999', label=f'different ({int((~same).sum())})'); axx.scatter(A[same], B[same], s=10, color='#c51b1b', label=f'identical value, same cell ({int(same.sum())})')
axx.plot([15, 55], [15, 55], color='k', lw=0.4); axx.set_xlabel('S11-A "alveolar macrophages" (%)'); axx.set_ylabel('S11-B "neutrophils" (%)'); axx.set_title('b  S11-A and S11-B share 35 of 100 values', loc='left'); axx.legend(fontsize=5.8)
axx = axes[2]
for k in range(1, 8):
    x = wt[(wt.block == 'S15-C') & (wt.group == 'PSLN-344') & (wt.animal == k)]; y = wt[(wt.block == 'S15-I') & (wt.group == '3d Vaccine+PSLN-344') & (wt.animal == k)]
    axx.plot(x.day, x.value, color='#1f5fa8', lw=2.2, alpha=0.35, label='S15-C PSLN-344 (challenge day 14)' if k == 1 else None)
    axx.plot(y.day, y.value, color='#c51b1b', lw=0.8, ls='--', label='S15-I vaccine + PSLN-344 (challenge day 3)' if k == 1 else None)
axx.set_xticks(range(0, 15, 2)); axx.set_xlabel('days after challenge'); axx.set_ylabel('body weight, % of day 0'); axx.set_title('c  Two different experiments, same seven trajectories', loc='left'); axx.legend(fontsize=5.8, loc='lower left')
axx = axes[3]
for k in range(1, 8):
    x = wt[(wt.block == 'S15-D') & (wt.group == 'PSLN-344') & (wt.animal == k)]; frozen = k in (1, 7)
    axx.plot(x.day, x.value, color='#c51b1b' if frozen else '#1f5fa8', lw=1.3 if frozen else 0.8, marker='o', ms=1.8,
             label=('value frozen from day 8 (carried forward = death?)' if k == 1 else None) if frozen else ('weight still changing' if k == 2 else None))
axx.set_xticks(range(0, 15, 2)); axx.set_xlabel('days after challenge'); axx.set_ylabel('body weight, % of day 0'); axx.set_title('d  S15-D weights imply 5/7; S06-D table says 7/7', loc='left'); axx.legend(fontsize=5.8, loc='upper right'); axx.set_ylim(77.5, 103.5)
fig.suptitle('Figure 3. Examples of the data-integrity findings (full list in Appendix A; evidence in tables T01a-g)', fontsize=8, x=0.01, ha='left', y=0.998)
fig.tight_layout(rect=(0, 0, 1, 0.99)); fig.savefig(f'{F}/fig3_data_integrity.png', bbox_inches='tight'); plt.close(fig)
print('figures written:', sorted(os.listdir(F)))
