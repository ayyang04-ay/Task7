import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({'font.size': 8.5, 'font.family': 'DejaVu Sans', 'axes.spines.top': False, 'axes.spines.right': False})
FIG = '/tmp/outputs/figures/'
c = pd.read_csv('tidy_continuous.csv'); c['level'] = c.level.fillna('').astype(str)
C = pd.read_csv('block_contrasts.csv'); C['level'] = C.level.fillna('').astype(str)
COL = {'Sham': '#9e9e9e', 'PSLN-212': '#e6862e', 'PSLN-344': '#1f5fa8', 'PSLN-212(Y)': '#8cc084', 'PSLN-344(Y)': '#2e7d32',
       'CMP-204': '#8e6bbf', 'Vaccine': '#bdbdbd', 'PBS': '#cfcfcf', 'CT': '#c0392b', 'PSLN-212/R848': '#b5651d', 'PSLN-R848': '#d4a373'}
LAB = {'Sham': 'Sham\n(aged)', 'PSLN-212': 'PSLN-212\n(aged)', 'PSLN-344': 'PSLN-344\n(aged)', 'PSLN-212(Y)': 'PSLN-212\n(young)', 'PSLN-344(Y)': 'PSLN-344\n(young)'}

def pstr(p):
    return 'p<0.001' if p < 0.001 else f'p={p:.3f}' if p < 0.01 else f'p={p:.2f}'

def dotpanel(ax, blk, lvl, groups, title, log=False, ylab=''):
    d = c[(c.block == blk) & (c.level == lvl)]
    for i, g in enumerate(groups):
        v = d[d.group == g].value.values
        if blk in ('S03-C', 'S03-G'):
            v = np.where(v <= 0, 5, v)
        x = i + np.linspace(-0.12, 0.12, len(v))
        ax.scatter(x, v, s=16, color=COL[g], edgecolor='k', linewidth=0.3, zorder=3)
        m = np.exp(np.mean(np.log(v))) if log else np.mean(v)
        ax.plot([i - 0.25, i + 0.25], [m, m], color='k', lw=1.2, zorder=4)
    if log: ax.set_yscale('log')
    ax.set_xticks(range(len(groups))); ax.set_xticklabels([LAB.get(g, g) for g in groups], fontsize=6.5)
    k = C[(C.block == blk) & (C.level == lvl) & C.contrast.str.startswith('Mn effect in aged')]
    eff = k.effect.iloc[0]; p = k.p_welch.iloc[0]; et = k.effect_type.iloc[0]
    es = f'{eff:.1f}x' if 'fold' in et else f'+{eff:.1f} pts'
    ax.set_title(f'{title}\n[{blk.replace("_ICOShi","")}{" " + lvl if lvl else ""}]  344 vs 212: {es}, {pstr(p)}', fontsize=7)
    ax.set_ylabel(ylab, fontsize=7)

# ---------------- Figure 1: key efficacy read-outs
G4 = ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']
fig, axs = plt.subplots(2, 4, figsize=(11, 5.6))
dotpanel(axs[0, 0], 'S01-A_16h', '', G4, 'Lung Ifnb1, 16 h', log=True, ylab='fold vs untreated (log)')
dotpanel(axs[0, 1], 'S02-F', '36h', ['Sham', 'PSLN-212', 'PSLN-344'], 'Lung Gm-csf (Csf2), 36 h', log=True, ylab='fold (log)')
dotpanel(axs[0, 2], 'S01-F', '', G4, 'Lung cDC1 (XCR1+), 72 h', ylab='% of CD11c+CD26+')
dotpanel(axs[0, 3], 'S04-A_ICOShi', '', G4, 'MLN ICOS-hi Tfh, d7', ylab='%')
dotpanel(axs[1, 0], 'S03-A', '', G4, 'Serum IgG anti-H1N1, d14', log=True, ylab='endpoint titre (log)')
dotpanel(axs[1, 1], 'S03-C', '', G4, 'HAI anti-H1N1, d14', log=True, ylab='HAI titre (log; <10 plotted as 5)')
axs[1, 1].axhline(40, ls='--', lw=0.8, color='grey'); axs[1, 1].text(3.4, 42, '1:40', fontsize=6, color='grey')
dotpanel(axs[1, 2], 'S05-F', '', G4, 'IFN-g+ CD8 (H5N1 restim), d14', ylab='% of MLN cells')
dotpanel(axs[1, 3], 'S05-I', '', G4, 'Lung TRM CD8 (CD69+CD103+), d25', ylab='%')
fig.suptitle('Figure 1. PSLN-344 vs PSLN-212 in aged mice - selected read-outs from blocks without integrity flags (n=5/group; bar = mean or geometric mean)', fontsize=9)
fig.tight_layout(rect=[0, 0, 1, 0.95]); fig.savefig(FIG + 'fig1_key_efficacy_readouts.png', dpi=200); plt.close(fig)

# ---------------- Figure 2: restoration index
ri = C[C.contrast.str.startswith('Restoration')].copy()
clean = {'S01-A_16h': 'Ifnb1 16 h (lung)', 'S01-D': 'Monocytes d4 (lung)', 'S01-F': 'cDC1 72 h (lung)', 'S02-A': 'Migratory CCR7+ DC (lung)',
         'S02-B': 'CD11b+ DC (MLN)', 'S02-C': 'Antigen+ DC (MLN)', 'S02-D_CD40': 'CD40+ DC (MLN)', 'S02-D_CD86': 'CD86+ DC (MLN)',
         'S03-A': 'IgG H1N1 d14', 'S03-C': 'HAI H1N1 d14', 'S03-D': 'Neut H1N1 d14', 'S03-E': 'IgG H3N2 d14', 'S03-G': 'HAI H3N2 d14', 'S03-H': 'Neut H3N2 d14',
         'S03-K': 'GC B cells d7 (MLN)', 'S04-A_ICOShi': 'ICOS-hi Tfh d7', 'S04-B_Foxp3': 'Tfr (reduction) d7', 'S04-D': 'Lung Treg (reduction) d7',
         'S05-D': 'Ki-67+ CD8 d3', 'S05-E': 'GZMB+ CD8 d3', 'S05-F': 'IFN-g+ CD8 H5N1 d14', 'S05-G': 'IFN-g+ CD8 H5N1 d60', 'S05-H': 'GZMB+ CD8 d60',
         'S05-I': 'Lung TRM d25', 'S13-A': 'IgG2a H1N1', 'S13-B': 'IgG1 H1N1', 'S13-C': 'IgG2a H3N2', 'S13-D': 'IgG1 H3N2', 'S13-I': 'IgG H1N1 d28 (boost)',
         'S13-J': 'IgG H3N2 d28 (boost)', 'S14-A_H1N1': 'IFN-g+ CD8 H1N1', 'S14-A_H3N2': 'IFN-g+ CD8 H3N2'}
sel = ri[ri.block.isin(clean) & ~((ri.block == 'S01-D') & (ri.level != '4'))].copy()
sel['name'] = sel.block.map(clean) + ' [' + sel.block + ']'
sel = sel.sort_values('effect')
fig, ax = plt.subplots(figsize=(7.2, 7.4))
colors = ['#c0392b' if v < 0.4 else '#f0ad4e' if v < 0.6 else '#1f5fa8' for v in sel.effect]
ax.barh(range(len(sel)), sel.effect, color=colors)
ax.set_yticks(range(len(sel))); ax.set_yticklabels(sel.name, fontsize=6.6)
ax.axvline(1, color='k', lw=0.8, ls='--'); ax.axvline(0, color='k', lw=0.6)
ax.axvline(sel.effect.median(), color='grey', lw=0.8, ls=':')
ax.text(sel.effect.median() + 0.01, len(sel) - 0.5, f'median {sel.effect.median():.2f}', fontsize=7, color='grey')
ax.set_xlabel('Restoration index = (PSLN-344 aged - PSLN-212 aged) / (PSLN-212 young - PSLN-212 aged)\n0 = no improvement over PSLN-212 in aged; 1 = young level (titres/fold-changes on log2 scale)', fontsize=7)
ax.set_title('Figure 2. How much of the age-related deficit does Mn2+ (PSLN-344) close?\n32 read-outs from blocks without integrity flags', fontsize=9)
fig.tight_layout(); fig.savefig(FIG + 'fig2_restoration_index.png', dpi=200); plt.close(fig)

# ---------------- Figure 3: survival strata + pooled sensitivity
st = pd.read_csv('survival_strata_flags.csv'); pooled = pd.read_csv('survival_pooled_sensitivity.csv')
FC = {'none detected': '#2e7d32', 'minor': '#8cc084', 'moderate': '#f0ad4e', 'major': '#e67e22', 'critical': '#c0392b'}
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5.4), gridspec_kw={'width_ratios': [1.2, 1]})
for i, r in st.iloc[::-1].reset_index(drop=True).iterrows():
    s344 = eval(r.PSLN344.replace('/', '/')); s212 = eval(r.PSLN212.replace('/', '/'))
    a1.plot([100 * s212, 100 * s344], [i, i], color='#bbbbbb', lw=1.5, zorder=1)
    a1.scatter(100 * s212, i, color=COL['PSLN-212'], s=28, zorder=3, edgecolor='k', lw=0.3)
    a1.scatter(100 * s344, i, color=COL['PSLN-344'], s=28, zorder=3, edgecolor='k', lw=0.3)
    a1.text(103, i, r.integrity_flag, fontsize=6.5, va='center', color=FC[r.integrity_flag])
a1.set_yticks(range(len(st))); a1.set_yticklabels([f'{s} ({p344} vs {p212})' for s, p344, p212 in zip(st.stratum[::-1], st.PSLN344[::-1], st.PSLN212[::-1])], fontsize=6.5)
a1.set_xlim(-3, 125); a1.set_xlabel('End-of-observation survival, % (day 14; S03-J day 21)')
a1.scatter([], [], color=COL['PSLN-344'], label='PSLN-344'); a1.scatter([], [], color=COL['PSLN-212'], label='PSLN-212'); a1.legend(fontsize=7, loc='lower center', bbox_to_anchor=(0.45, 1.0), ncol=2, frameon=False)
a1.set_title('Per-experiment survival (aged / middle-aged strata) with integrity flag', fontsize=8, pad=16)
y = np.arange(len(pooled))[::-1]
a2.barh(y, pooled.MH_risk_difference_pct_points, color='#1f5fa8')
for yy, (_, r) in zip(y, pooled.iterrows()):
    a2.text(r.MH_risk_difference_pct_points + 1, yy, f"{r.PSLN344_surv} vs {r.PSLN212_surv}; p={r.exact_stratified_p_one_sided:.1e}", fontsize=6.3, va='center')
SHORT = ['A. All strata as recorded (15)', 'B. S06-D removed (duplicate of S06-C)', 'C. B + worst-case weight reconciliation', 'D. C restricted to >=20-month strata', 'E. C restricted to strata w/o critical/major flags', 'F. Only stratum with no flag (S06-B)']
a2.set_yticks(y); a2.set_yticklabels(SHORT, fontsize=6.8)
a2.set_xlim(0, 150); a2.set_xlabel('MH survival difference, % points (PSLN-344 minus PSLN-212)')
a2.set_title('Pooled (stratified by experiment): sensitivity analyses', fontsize=8, pad=16)
fig.suptitle('Figure 3. Survival advantage of PSLN-344 over PSLN-212 is large in every scenario, but most strata carry integrity flags (exact stratified test, one-sided)', fontsize=8.6)
fig.tight_layout(rect=[0, 0, 1, 0.94]); fig.savefig(FIG + 'fig3_survival_strata_sensitivity.png', dpi=200); plt.close(fig)

# ---------------- Figure 4: integrity evidence
bw = pd.read_csv('tidy_bodyweight.csv')
fig, axs = plt.subplots(2, 2, figsize=(10.5, 7.4))
ax = axs[0, 0]
for col in ['W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC']:
    a = bw[(bw.block == 'S15-C') & (bw.col == col)].sort_values('day'); b = bw[(bw.block == 'S15-I') & (bw.col == col)].sort_values('day')
    ax.plot(a.day, a.value, '-', color='#1f5fa8', lw=2.4, alpha=0.35)
    ax.plot(b.day, b.value, '--', color='#c0392b', lw=1, marker='o', ms=2.5)
ax.plot([], [], '-', color='#1f5fa8', lw=2.4, alpha=0.35, label='S15-C PSLN-344 (vaccinated d0, H5N1 challenge at d14)')
ax.plot([], [], '--', color='#c0392b', marker='o', ms=2.5, label='S15-I "3d Vaccine+PSLN-344" (challenge 3 d after vaccine)')
ax.legend(fontsize=6.3, loc='lower left'); ax.set_xlabel('day after challenge'); ax.set_ylabel('% of day-0 weight')
ax.set_title('(a) Two different experiments, near-identical animal trajectories\n(6 of 7 animals identical on days 2-12; S15!W24:AC29 vs S15!W73:AC78)', fontsize=7.5)
ax = axs[0, 1]
pairs = [('S09-E', 'X', 'S15-M', 'I'), ('S09-E', 'Y', 'S15-M', 'J'), ('S09-E', 'Z', 'S15-M', 'K'), ('S09-E', 'AA', 'S15-M', 'L'), ('S09-E', 'AB', 'S15-M', 'M'), ('S09-E', 'AC', 'S15-M', 'N')]
for (b1, c1, b2, c2) in pairs:
    a = bw[(bw.block == b1) & (bw.col == c1)].sort_values('day'); b = bw[(bw.block == b2) & (bw.col == c2)].sort_values('day')
    ax.plot(a.day, a.value, '-', color='#2e7d32', lw=2.4, alpha=0.35); ax.plot(b.day, b.value, '--', color='#8e6bbf', lw=1, marker='o', ms=2.5)
ax.plot([], [], '-', color='#2e7d32', lw=2.4, alpha=0.35, label='S09-E young BALB/c, PSLN-344(Y), Perth H3N2 challenge')
ax.plot([], [], '--', color='#8e6bbf', marker='o', ms=2.5, label='S15-M young C57BL/6, "PSLN-212(Y)" control')
ax.legend(fontsize=6.3, loc='lower left'); ax.set_xlabel('day after challenge')
ax.set_title('(b) Different strain, different adjuvant, different experiment:\nsame weights (d4 values differ by exact integers, e.g. +6.0, +2.0)', fontsize=7.5)
ax = axs[1, 0]
m = pd.read_csv('dup_S11A_vs_S11B_positionwise.csv')
ax.scatter(m.value_AM[~m.match], m.value_Neut[~m.match], s=12, color='#9e9e9e', label='different values (65)')
ax.scatter(m.value_AM[m.match], m.value_Neut[m.match], s=16, color='#c0392b', label='identical values (35)')
ax.plot([10, 55], [10, 55], 'k:', lw=0.8)
ax.set_xlabel('S11-A alveolar macrophages, % (same animal position)'); ax.set_ylabel('S11-B neutrophils, %')
ax.legend(fontsize=6.5); ax.set_title('(c) Two different cell types, same numbers:\n35/100 position-matched values identical (chance expectation 0.85)', fontsize=7.5)
ax = axs[1, 1]
bm = pd.read_csv('dup_chance_benchmark.csv')
k = bm.k_live_exact_matches
ax.bar(k - 0.18, bm.observed_pairs, width=0.36, color='#c0392b', label='observed')
ax.bar(k + 0.18, np.maximum(bm.expected_pairs_by_chance, 1e-3), width=0.36, color='#9e9e9e', label='expected by chance')
ax.set_yscale('log'); ax.set_xlabel('k = identical live weight readings shared\nby two animals from different experiments (>= k)')
ax.set_ylabel('number of animal pairs (log)'); ax.legend(fontsize=7)
for kk, o, e in zip(k, bm.observed_pairs, bm.expected_pairs_by_chance):
    ax.text(kk - 0.18, o * 1.15, str(o), ha='center', fontsize=6.5)
    ax.text(kk + 0.18, max(e, 1e-3) * 1.15, ('<0.001' if e < 1e-3 else (f'{e:.3f}' if e < 1 else f'{e:.0f}')), ha='center', fontsize=5.8, color='#555555')
ax.set_title('(d) Cross-experiment trajectory matches vs chance\n(126,074 animal pairs; chance from per-day value frequencies; grey bars floored at 0.001)', fontsize=7.5)
fig.suptitle('Figure 6. Data-integrity findings that block an investment decision on the current package', fontsize=9.5)
fig.tight_layout(rect=[0, 0, 1, 0.95]); fig.savefig(FIG + 'fig6_integrity_evidence.png', dpi=200); plt.close(fig)

# ---------------- Figure 6: safety / reactogenicity
fig, axs = plt.subplots(1, 3, figsize=(11.5, 3.8))
ax = axs[0]
for j, an in enumerate(['Ifnb1', 'Tnf', 'Isg15']):
    d = c[c.block == f'S10-A_{an}']
    for i, g in enumerate(['PBS', 'Sham', 'PSLN-344', 'CT']):
        v = d[d.group == g].value.values; x = j * 5 + i + np.linspace(-0.12, 0.12, len(v))
        ax.scatter(x, v, s=12, color=COL[g], edgecolor='k', lw=0.3); ax.plot([j * 5 + i - .3, j * 5 + i + .3], [v.mean()] * 2, 'k', lw=1)
ax.set_xticks([1.5, 6.5, 11.5]); ax.set_xticklabels(['Ifnb1', 'Tnf', 'Isg15'])
for g in ['PBS', 'Sham', 'PSLN-344', 'CT']: ax.scatter([], [], color=COL[g], label=g)
ax.legend(fontsize=6.5, ncol=2); ax.set_ylabel('CNS transcript, fold vs untreated')
ax.set_title('(a) CNS transcripts 36 h after intranasal dose [S10-A]\nPSLN-344 vs Sham: Tnf 1.20x (p=0.36); CT: 2.6-4.8x', fontsize=7.5)
ax = axs[1]
d = bw[bw.block == 'S08-D']
for g in ['Vaccine', 'PSLN-212', 'PSLN-344', 'CMP-204', 'PSLN-212(Y)', 'PSLN-212/R848']:
    x = d[d.group == g].groupby('day').value.mean()
    ax.plot(x.index, x.values, marker='o', ms=3, color=COL[g], label=g)
ax.set_xlabel('day after intranasal vaccination'); ax.set_ylabel('% day-0 weight (group mean)')
ax.legend(fontsize=6.3); ax.set_title('(b) Post-vaccination body weight [S08-D]\nPSLN-344 nadir 96.4%; PSLN-212/R848 90.0% (1 animal lost by d10)', fontsize=7.5)
ax = axs[2]
rows = []
for pan, t in [('S09-A_panel1', '16 h'), ('S09-A_panel2', '72 h*')]:
    for an in ['Il6', 'Tnf', 'Il10']:
        for g in ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']:
            v = c[(c.block == pan) & (c.level == an) & (c.group == g)].value.values
            rows.append((f'{an}\n{t}', g, 10 ** v.mean()))
R = pd.DataFrame(rows, columns=['an', 'g', 'gm'])
labs = R.an.unique()
for i, g in enumerate(['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']):
    ax.bar(np.arange(len(labs)) + (i - 1) * 0.26, R[R.g == g].gm.values, width=0.26, color=COL[g], label={'PSLN-212': 'PSLN-212 aged', 'PSLN-344': 'PSLN-344 aged', 'PSLN-212(Y)': 'PSLN-212 young'}[g])
ax.set_yscale('log'); ax.set_xticks(range(len(labs))); ax.set_xticklabels(labs, fontsize=7); ax.axhline(1, color='k', lw=0.6)
ax.legend(fontsize=6.3); ax.set_ylabel('lung mRNA, geometric mean fold (log)')
ax.set_title('(c) Inflammatory transcripts [S09-A] (*panel printed as 16 h,\nvalues match S01-A 72 h): aged PSLN-344 Tnf/Il10 exceed young', fontsize=7.5)
fig.suptitle('Figure 4. Tolerability and safety-relevant read-outs available in the package (no Mn2+ biodistribution, histopathology or repeat-dose data exist)', fontsize=9)
fig.tight_layout(rect=[0, 0, 1, 0.92]); fig.savefig(FIG + 'fig4_safety.png', dpi=200); plt.close(fig)

# ---------------- Figure 7: dose response
from scipy.optimize import curve_fit
E = pd.read_csv('dose_response_S08A_emax.csv')
d = c[c.block == 'S08-A'].copy(); d['dose'] = d.level.astype(float)
fig, ax = plt.subplots(figsize=(5.6, 3.9))
cc = {'CMP-204': COL['CMP-204'], 'PSLN-212': COL['PSLN-212'], 'PSLN-344': COL['PSLN-344'], 'PSLN-344/R848': '#b5651d'}
xx = np.linspace(0.5, 45, 200)
for g in ['CMP-204', 'PSLN-212', 'PSLN-344', 'PSLN-344/R848']:
    x = d[d.group == g]; ax.scatter(x.dose, x.value, color=cc[g], s=14, edgecolor='k', lw=0.3)
    r = E[E.group == g].iloc[0]
    ax.plot(xx, r.E0 + r.Emax * xx ** r.hill / (r.ED50_ug ** r.hill + xx ** r.hill), color=cc[g], label=f'{g}: Emax {r.Emax:.0f}x, ED50 {r.ED50_ug:.0f} ug')
ax.set_xlabel('intranasal dose, ug per animal'); ax.set_ylabel('lung Ifnb1 at 16 h, fold')
ax.legend(fontsize=6.8); ax.set_title('Figure 5. Dose-response [S08-A]: Mn2+ raises the ceiling (Emax ~3.4x),\nnot the potency (ED50 ~10 ug for both); response plateaus at 20-40 ug', fontsize=8)
fig.tight_layout(); fig.savefig(FIG + 'fig5_dose_response.png', dpi=200); plt.close(fig)
print('figures written')
