import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from lifelines import KaplanMeierFitter
from statsmodels.stats.proportion import proportion_confint
from scipy import optimize
OUT = '/tmp/outputs/figures'; import os; os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.size': 9, 'font.family': 'DejaVu Sans', 'axes.spines.top': False, 'axes.spines.right': False})
T = pd.read_csv('/tmp/work/tidy/tte.csv'); T['group'] = T.group.str.replace('PSLN-212Y', 'PSLN-212(Y)').str.replace('PSLN-344Y', 'PSLN-344(Y)')
T.loc[(T.block == 'S03-J') & T.time.isna(), 'time'] = 21.0
V = pd.read_csv('/tmp/work/tidy/values.csv'); V['time'] = V.time.fillna('')
C344, C212, CY, CS = '#C0392B', '#2E86C1', '#7D3C98', '#7F8C8D'

def newcombe(x1, n1, x2, n2):
    l1, u1 = proportion_confint(x1, n1, method='wilson'); l2, u2 = proportion_confint(x2, n2, method='wilson')
    p1, p2 = x1 / n1, x2 / n2; d = p1 - p2
    return d, d - np.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), d + np.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)

# ---------------- Figure 1: forest plot ----------------
strata = [('S03-I', 'PSLN-344', 'PSLN-212', 'Homologous CA09 H1N1, d14 (aged)', 'BW conflict'),
          ('S03-J', 'PSLN-344', 'PSLN-212', 'wt VN04 H5N1, d2 (aged*)', 'BW conflict'),
          ('S06-A', 'PSLN-344', 'PSLN-212', 'H3 vacc -> PR8 H1N1, d14 (aged)', ''),
          ('S06-B', 'PSLN-344', 'PSLN-212', 'H3 vacc -> PR8 H1N1, d3 (aged)', ''),
          ('S06-C', 'PSLN-344', 'PSLN-212', 'Bivalent -> rgH5N1, d14 (aged)', 'dup. as S06-D'),
          ('S06-E', 'PSLN-344', 'PSLN-212', 'H3 vacc -> PR8 H1N1, d60 (aged)', 'BW conflict'),
          ('S06-F', 'PSLN-344', 'PSLN-212', 'Bivalent -> rgH5N1, d60 (aged)', ''),
          ('S06-G', 'PSLN-344', 'PSLN-212', 'H1 vacc -> Perth H3N2, d60 (aged)', 'BW conflict'),
          ('S06-E[imprint]', 'Naive+PSLN-344', 'Naive+PSLN-212', '14-mo naive -> PR8', ''),
          ('S06-E[imprint]', 'Imprinting+PSLN-344', 'Imprinting+PSLN-212', '14-mo PR8-imprinted -> PR8', ''),
          ('S06-F[imprint]', 'Naive+PSLN-344', 'Naive+PSLN-212', '14-mo naive -> Perth H3N2', ''),
          ('S06-F[imprint]', 'Imprinting+PSLN-344', 'Imprinting+PSLN-212', '14-mo PR8-imprinted -> Perth H3N2', ''),
          ('S15-L', 'PSLN-344', 'PSLN-212', 'Aged C57BL/6 (challenge not stated)', 'BW recycled'),
          ('S15-N', 'PSLN-344', 'PSLN-212', 'Aged Swiss Webster (challenge not stated)', 'BW recycled')]
fig, ax = plt.subplots(figsize=(9.5, 7.2))
y = len(strata) + 4
ylabs = []
for blk, a, b, lab, flag in strata:
    d = T[T.block == blk]; da, db = d[d.group == a], d[d.group == b]
    sa, sb = int((da.event == 0).sum()), int((db.event == 0).sum())
    dd, lo, hi = newcombe(sa, len(da), sb, len(db))
    ax.plot([100 * lo, 100 * hi], [y, y], color='k', lw=1)
    ax.plot(100 * dd, y, 's', color=C344 if not flag else '#E59866', ms=7)
    ax.text(103, y, f'{sa}/{len(da)} vs {sb}/{len(db)}', va='center', fontsize=8)
    ax.text(127, y, flag, va='center', fontsize=7.5, color='#A04000')
    ylabs.append((y, f'{blk}: {lab}')); y -= 1
pooled = pd.read_csv('/tmp/work/survival_pooled.csv')
y -= 0.5
for i, r in pooled.iloc[[0, 1, 2]].iterrows():
    ax.plot([r.RD_newcombe_lo, r.RD_newcombe_hi], [y, y], color='k', lw=1.5)
    ax.plot(r.MH_RD_pp, y, 'D', color='#641E16', ms=9)
    ax.text(103, y, f'{r.surv_344} vs {r.surv_212}', va='center', fontsize=8, weight='bold')
    lab = ['Pooled, as recorded (S06-D duplicate excluded)', 'Pooled, excluding BW-conflict experiments', 'Pooled, worst case for PSLN-344'][i]
    ylabs.append((y, lab)); y -= 1
ax.axvline(0, color='grey', ls='--', lw=0.8)
ax.set_yticks([t for t, _ in ylabs]); ax.set_yticklabels([l for _, l in ylabs], fontsize=8)
ax.set_xlim(-40, 150); ax.set_xticks([-40, -20, 0, 20, 40, 60, 80, 100])
ax.set_xlabel('Survival difference, PSLN-344 minus PSLN-212 (percentage points, Newcombe 95% CI)')
ax.text(103, len(strata) + 4.9, 'Survivors\n344 vs 212', fontsize=8, weight='bold', va='bottom'); ax.text(127, len(strata) + 4.9, 'Integrity\nflag', fontsize=8, weight='bold', va='bottom')
ax.set_ylim(y + 0.3, len(strata) + 6.2)
fig.suptitle('Figure 1. Head-to-head survival in aged/middle-aged mice: the point estimate favours PSLN-344 in all 14 strata', fontsize=10, x=0.01, ha='left')
fig.text(0.01, 0.01, '*S03-J age not stated; no (Y) label, so aged by the annotation convention. Stratified log-rank chi2 = 117 (R survival::survdiff), '
         'stratified Cox HR 0.076 (0.043-0.134).\nSource: tidy/tte.csv; analysis survival.py / newcombe.py / strat.R', fontsize=7)
plt.tight_layout(rect=(0, 0.04, 1, 0.96)); fig.savefig(f'{OUT}/fig1_survival_forest.png', dpi=200); plt.close()

# ---------------- Figure 2: KM small multiples ----------------
blocks = [('S03-I', 'Homologous CA09 (10x LD50), challenge d14'), ('S03-J', 'wt VN04 H5N1, challenge d2'),
          ('S06-A', 'Aichi H3 vacc -> PR8 H1N1, d14'), ('S06-B', 'Aichi H3 vacc -> PR8 H1N1, d3'),
          ('S06-C', 'Bivalent -> rgH5N1, d14'), ('S06-E', 'Aichi H3 vacc -> PR8, d60'),
          ('S06-F', 'Bivalent -> rgH5N1, d60'), ('S06-G', 'CA09 H1 vacc -> Perth H3N2, d60'), ('S15-H', 'Antigen requirement, rgH5N1 d3')]
colors = {'Sham': CS, 'PSLN-212': C212, 'PSLN-344': C344, 'PSLN-212(Y)': CY, 'CMP-204': '#27AE60', 'Untreated': '#D4AC0D',
          '3d Vaccine': CS, '3d PSLN-344': '#E59866', '3d Vaccine+PSLN-344': C344}
fig, axes = plt.subplots(3, 3, figsize=(11, 8.5), sharey=True)
for ax, (blk, title) in zip(axes.flat, blocks):
    d = T[T.block == blk]
    for g, dd in d.groupby('group'):
        kmf = KaplanMeierFitter(); kmf.fit(dd.time, dd.event, label=f'{g} ({int((dd.event == 0).sum())}/{len(dd)})')
        kmf.plot_survival_function(ax=ax, ci_show=False, color=colors.get(g, 'k'), lw=1.6,
                                   ls='--' if g in ('PSLN-212(Y)', 'Untreated') else '-')
    ax.set_title(f'{blk}: {title}', fontsize=8.5); ax.set_xlabel('Days after challenge', fontsize=8); ax.set_ylim(-0.03, 1.05)
    ax.legend(fontsize=6.5, loc='lower left', frameon=False)
axes[0, 0].set_ylabel('Survival'); axes[1, 0].set_ylabel('Survival'); axes[2, 0].set_ylabel('Survival')
fig.suptitle('Figure 2. Kaplan-Meier curves, aged mice unless stated (dashed purple = young PSLN-212 benchmark; dashed gold = unchallenged aged controls)', fontsize=9.5, x=0.01, ha='left')
fig.text(0.01, 0.005, 'S06-D omitted (identical to S06-C). S15-H body-weight record for the combination arm duplicates S15-C (see integrity audit). Source: tidy/tte.csv', fontsize=7)
plt.tight_layout(rect=(0, 0.02, 1, 0.97)); fig.savefig(f'{OUT}/fig2_km_grid.png', dpi=200); plt.close()

# ---------------- Figure 3: immune cascade effect map + restoration ----------------
H = pd.read_csv('/tmp/work/h2h.csv'); R = pd.read_csv('/tmp/work/restoration_index.csv')
sel = [('S01-A', 'Ifnb1', '16h', 'Ifnb1 16 h (lung)'), ('S09-A panel1[A:U]', 'Ccl2', None, 'Ccl2 16 h'), ('S09-A panel1[A:U]', 'Il6', None, 'Il6 16 h'),
       ('S02-F', 'Gm-csf (lung)', '36h', 'Gm-csf 36 h'), ('S01-D', 'Lung monocytes', 'd4', 'Lung monocytes d4'),
       ('S01-E', 'Lung CD11b+ DC', 'd4', 'Lung CD11b+ DC d4'), ('S01-F', 'Lung cDC1', '72h', 'Lung cDC1 72 h'),
       ('S02-A', 'CCR7+ migratory CD11b+ DC (lung)', '72h', 'CCR7+ migratory DC 72 h'), ('S02-C', 'MLN AF647-OVA+ DC', '36h', 'Antigen+ DC in MLN 36 h'),
       ('S02-D CD40', 'CD40+ of MLN CD11b+ DC', 'd3', 'CD40+ MLN DC d3'), ('S02-D CD86', 'CD86+ of MLN CD11b+ DC', 'd3', 'CD86+ MLN DC d3'),
       ('S02-E', 'OT-I proliferation (DC co-culture)', '72h+3d', 'OT-I priming by MLN DC'), ('S05-D', 'Lung Ki-67+ CD8', 'd3', 'Ki-67+ CD8 lung d3'),
       ('S05-E', 'Lung GZMB+ CD8', 'd3', 'GZMB+ CD8 lung d3'), ('S04-A', 'Tfh ICOS-hi', 'd7', 'ICOS-hi Tfh d7'),
       ('S03-K', 'MLN GC B cells', 'd7', 'GC B cells d7'), ('S04-B Foxp3', 'Tfr (Foxp3+ of CXCR5+ICOShi)', 'd7', 'Tfr d7 (lower = better)'),
       ('S03-A', 'IgG CA09 H1N1', 'd14', 'IgG H1N1 d14'), ('S03-C', 'HAI CA09 H1N1', 'd14', 'HAI H1N1 d14'), ('S03-G', 'HAI Aichi H3N2', 'd14', 'HAI H3N2 d14'),
       ('S03-D', 'Neut CA09 H1N1', 'd14', 'Neut H1N1 d14'), ('S13-A', 'IgG2a CA09 H1N1', 'd14', 'IgG2a H1N1 d14'),
       ('S13-I', 'IgG CA09 H1N1 post-boost', 'd28', 'IgG H1N1 post-boost d28'), ('S05-F', 'MLN IFNg+ CD8 (rgH5N1 restim)', 'd14', 'IFNg+ CD8 d14'),
       ('S05-I', 'Lung TRM CD8', 'd25', 'Lung TRM CD8 d25'), ('S05-G', 'MLN IFNg+ CD8 (rgH5N1 restim)', 'd60', 'IFNg+ CD8 d60'),
       ('S05-H', 'MLN GZMB+ CD8', 'd60', 'GZMB+ CD8 d60')]
rows = []
for blk, an, t, lab in sel:
    h = H[(H.block == blk) & (H.analyte == an)]
    if t: h = h[h.time == t]
    h = h.iloc[0]
    if h.scale == 'linear %':
        fold = h.summary344 / h.summary212
        # approximate CI on ratio via delta method from Welch CI on difference
        lo = (h.summary212 + h.lo) / h.summary212; hi = (h.summary212 + h.hi) / h.summary212
    else:
        fold, lo, hi = h.est, h.lo, h.hi
    r = R[(R.block == blk) & (R.analyte == an)]
    if t: r = r[r.time == t]
    ri = r.RI.iloc[0] if len(r) else np.nan; rlo = r.RI_lo.iloc[0] if len(r) else np.nan; rhi = r.RI_hi.iloc[0] if len(r) else np.nan
    rows.append((lab, fold, max(lo, 1e-2), hi, h.q_BH, ri, rlo, rhi))
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 8), sharey=True, gridspec_kw={'width_ratios': [1.3, 1]})
yy = np.arange(len(rows))[::-1]
for yv, (lab, f, lo, hi, q, ri, rlo, rhi) in zip(yy, rows):
    a1.plot([np.log2(lo), np.log2(hi)], [yv, yv], color='k', lw=0.9)
    a1.plot(np.log2(f), yv, 'o', color=C344 if f > 1 else C212, ms=6)
    a1.text(10.2, yv, f'q={q:.3f}' if q >= 0.001 else 'q<0.001', fontsize=7, va='center')
    if not np.isnan(ri):
        a2.plot([max(rlo, -0.2), min(rhi, 1.6)], [yv, yv], color='k', lw=0.9)
        a2.plot(ri, yv, 'o', color='#117864', ms=6)
a1.axvline(0, color='grey', ls='--', lw=0.8); a1.set_xlim(-3.2, 11.8)
a1.set_yticks(yy); a1.set_yticklabels([r[0] for r in rows], fontsize=8)
a1.set_xlabel('log2 ratio PSLN-344 / PSLN-212 (aged), 95% CI\n(titres/qPCR: geometric mean ratio; %: ratio of means)')
a1.set_title('A. Aged PSLN-344 vs PSLN-212 along the immune cascade', fontsize=9.5, loc='left')
a2.axvline(0, color='grey', ls='--', lw=0.8); a2.axvline(1, color=CY, ls='--', lw=0.8)
a2.set_xlim(-0.2, 1.6); a2.set_xlabel('Restoration index = (344 - 212) / (young 212 - aged 212)\n0 = no rescue, 1 = young level (bootstrap 95% CI)')
a2.set_title('B. Fraction of the young-aged gap closed by Mn2+', fontsize=9.5, loc='left')
fig.suptitle('Figure 3. Mn2+ (PSLN-344) rescues the aged response at every layer; co-stimulation and memory are only partly restored', fontsize=10, x=0.01, ha='left')
fig.text(0.01, 0.005, 'q = Benjamini-Hochberg FDR across 83 eligible endpoints (h2h.csv). Tfr: lower is better (ratio < 1 favours PSLN-344). Source blocks in h2h.csv.', fontsize=7)
plt.tight_layout(rect=(0, 0.02, 1, 0.97)); fig.savefig(f'{OUT}/fig3_cascade_restoration.png', dpi=200); plt.close()

# ---------------- Figure 4: dose response ----------------
dr = V[V.block == 'S08-A'].copy(); dr['dose'] = dr.time.str.replace('ug', '').astype(float)
E = pd.read_csv('/tmp/work/dose_response.csv').set_index('group')
fig, ax = plt.subplots(figsize=(6.2, 4.3))
cols = {'CMP-204': '#27AE60', 'PSLN-212': C212, 'PSLN-344': C344, 'PSLN-344/R848': '#E59866'}
xx = np.linspace(0.8, 45, 200)
for g, d in dr.groupby('group'):
    m = d.groupby('dose').value.agg(['mean', 'std'])
    ax.errorbar(m.index * (1.03 if g == 'PSLN-344' else 1), m['mean'], yerr=m['std'], fmt='o', color=cols[g], capsize=2, ms=4,
                label=f"{g}{' (formulation not defined in Materials)' if g == 'PSLN-344/R848' else ''}")
    e = E.loc[g]; ax.plot(xx, e.E0 + e.Emax * xx ** e.hill / (e.ED50_ug ** e.hill + xx ** e.hill), color=cols[g], lw=1)
ax.set_xscale('log'); ax.set_xticks([1, 5, 10, 20, 40]); ax.set_xticklabels(['1', '5', '10', '20', '40'])
ax.set_xlabel('Adjuvant dose per mouse (ug), intranasal'); ax.set_ylabel('Lung Ifnb1, fold vs untreated (16 h)')
ax.axhline(E.loc['PSLN-212', 'mean_at_20'], color=C212, ls=':', lw=0.8)
ax.annotate('PSLN-344 at ~7 ug matches\nPSLN-212 at 20 ug (~3x dose-sparing)', xy=(7.3, 12.6), xytext=(1.1, 32), fontsize=7.5,
            arrowprops=dict(arrowstyle='->', lw=0.7))
ax.legend(fontsize=7, frameon=False, loc='upper left', bbox_to_anchor=(0, 0.85))
ax.set_title('Figure 4. Ifnb1 dose-response (S08-A, n=3/dose): Mn2+ raises the ceiling\n(Emax 49 vs 14-fold; ED50 ~11 vs ~10 ug)', fontsize=9, loc='left')
plt.tight_layout(); fig.savefig(f'{OUT}/fig4_dose_response.png', dpi=200); plt.close()

print('figures written')
