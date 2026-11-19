import pandas as pd, numpy as np, matplotlib, warnings
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from scipy import stats
warnings.filterwarnings('ignore')
OUT = '/tmp/outputs/figures'
import os; os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False,
                     'savefig.dpi': 200, 'savefig.bbox': 'tight'})
COL = {'Sham': '#8c8c8c', 'PSLN-212': '#4a90d9', 'PSLN-344': '#d9534f', 'PSLN-212(Y)': '#2ca02c', 'CMP-204': '#9467bd'}
LAB = {'Sham': 'Vaccine + vehicle (aged)', 'PSLN-212': 'PSLN-212, no Mn (aged)', 'PSLN-344': 'PSLN-344, +Mn (aged)',
       'PSLN-212(Y)': 'PSLN-212 (young reference)'}
R = pd.read_csv('/tmp/work/tidy/summary_survival.csv')
T = pd.read_csv('/tmp/work/tidy/aged_experiment_table.csv')
Cc = pd.read_csv('/tmp/work/tidy/continuous.csv'); Cc['time'] = Cc['time'].astype(str)
W = pd.read_csv('/tmp/work/tidy/weights.csv')

# ---------------- Figure 1: survival by experiment ----------------
fig, ax = plt.subplots(figsize=(9.2, 7.4))
exps = list(T.experiment)
labels = []
for i, e in enumerate(exps):
    r = T[T.experiment == e].iloc[0]
    d = '' if pd.isna(r.day) or r.day == '' else f', challenged d{int(float(r.day))}'
    ch = 'challenge not stated' if r.challenge == 'NOT STATED' else r.challenge.replace(' (homologous)', ' (homologous)')
    lab = f"{e}: {ch}{d}\n{r.model}"
    labels.append(lab)
    y = len(exps) - i
    if isinstance(r.integrity_flag, str) and r.integrity_flag:
        ax.axhspan(y - 0.45, y + 0.45, color='#fff3cd', zorder=0)
    for j, g in enumerate(['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']):
        rr = R[(R.block == e) & (R.group == g)]
        if not len(rr):
            continue
        rr = rr.iloc[0]
        yy = y + (j - 1.5) * 0.17
        ax.plot([rr.surv_95lo, rr.surv_95hi], [yy, yy], color=COL[g], lw=1.2, alpha=0.6)
        ax.plot(rr.survival_pct, yy, 'o', color=COL[g], ms=6, mec='white', mew=0.5, label=LAB[g] if i == 0 else None)
ax.set_yticks(range(len(exps), 0, -1)); ax.set_yticklabels(labels, fontsize=7.2)
ax.set_xlim(-3, 103); ax.set_xlabel('Survival at end of observation, % (95% exact CI)')
ax.set_title('Figure 1. Aged-mouse challenge experiments: survival by arm\n(shaded rows = experiments carrying a data-integrity flag; see Section 4)', fontsize=10, loc='left')
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=4, frameon=False, fontsize=7.5)
ax.grid(axis='x', ls=':', alpha=0.5)
plt.savefig(f'{OUT}/fig1_survival_by_experiment.png'); plt.close()

# ---------------- Figure 1b: pooled survival under integrity scenarios ----------------
Pp = pd.read_csv('/tmp/work/tidy/pooled_survival.csv')
fig, ax = plt.subplots(figsize=(8.6, 3.4))
sets = ['All aged experiments (11)', 'Excluding integrity-flagged experiments', 'All aged; weight-inferred deaths where paired weights exist',
        'All aged; worst case for PSLN-344 (max deaths for 344, min for comparator)']
short = ['As recorded\n(11 experiments)', 'Excluding 7 flagged\nexperiments (4 left)', 'Weight-inferred deaths\n(where paired weights exist)',
         'Worst case for\nPSLN-344']
def frac(s):
    a, b = s.split(' ')[0].split('/'); return 100 * int(a) / int(b), s.split(' ')[0]
x = np.arange(len(sets)); w = 0.26
for k, (g, comp, side) in enumerate([('Sham', 'PSLN-344 vs Sham', 'b'), ('PSLN-212', 'PSLN-344 vs PSLN-212', 'b'), ('PSLN-344', 'PSLN-344 vs Sham', 'a')]):
    vals, labs = [], []
    for s in sets:
        r = Pp[(Pp.comparison == comp) & (Pp.set == s)].iloc[0]
        v, l = frac(r.surv_b if side == 'b' else r.surv_a); vals.append(v); labs.append(l)
    bars = ax.bar(x + (k - 1) * w, vals, w, color=COL[g], label=LAB[g])
    for bx, v, l in zip(x + (k - 1) * w, vals, labs):
        ax.text(bx, v + 1.5, l, ha='center', va='bottom', fontsize=6.6)
ax.set_xticks(x); ax.set_xticklabels(short, fontsize=7.6); ax.set_ylim(0, 105); ax.set_ylabel('Pooled survival, %')
ax.set_title('Figure 2. Pooled aged-mouse survival is robust to every data-integrity scenario', fontsize=10, loc='left')
ax.legend(frameon=False, fontsize=7.5, ncol=3, loc='upper center', bbox_to_anchor=(0.5, -0.22))
plt.savefig(f'{OUT}/fig2_pooled_survival_scenarios.png'); plt.close()

# ---------------- Figure 3: forest of PSLN-344 vs PSLN-212 (ratio of geometric means) & % of young ----------------
items = [
 ('S01-A', 'Lung Ifnb1 (fold vs untreated)', '16h', 'Lung Ifnb1, 16 h', 'Innate (hours)'),
 ('S02-F', 'Lung Gm-csf (fold vs untreated)', '36h', 'Lung Gm-csf, 36 h', 'Innate (hours)'),
 ('S01-D', 'Lung monocytes CD11b+Ly6C+ (%)', '4', 'Lung monocytes, d4', 'Innate cells (d2-4)'),
 ('S01-E', 'Lung CD11b+ DC (%)', '4', 'Lung CD11b+ DC, d4', 'Innate cells (d2-4)'),
 ('S01-F', 'Lung cDC1 (%)', '72h', 'Lung cDC1, 72 h', 'Innate cells (d2-4)'),
 ('S02-A', 'Lung migratory CCR7+ CD11b+ DC (%)', '72h', 'Migratory CCR7+ DC, 72 h', 'Innate cells (d2-4)'),
 ('S02-C', 'MLN DC AF647-OVA+ (%)', '36h', 'Antigen+ DC in MLN, 36 h', 'Innate cells (d2-4)'),
 ('S02-D CD86', 'MLN CD11b+ DC CD86+ (%)', 'd3', 'MLN DC CD86+, d3', 'Innate cells (d2-4)'),
 ('S05-E', 'Lung GZMB+ CD8 T (%)', 'd3', 'Lung GZMB+ CD8, d3', 'T/B priming (d3-7)'),
 ('S04-A', 'MLN Tfh ICOS-high (%)', 'd7', 'Tfh ICOS-high, d7', 'T/B priming (d3-7)'),
 ('S03-K', 'MLN GC B cells CXCR5+GL7+ (%)', 'd7', 'GC B cells, d7', 'T/B priming (d3-7)'),
 ('S03-C', 'HI titre CA09 H1N1', 'd14', 'HI titre H1N1, d14', 'Antibody (d14-28)'),
 ('S03-G', 'HI titre Aichi H3N2', 'd14', 'HI titre H3N2, d14', 'Antibody (d14-28)'),
 ('S03-D', 'Neutralising titre CA09 H1N1', 'd14', 'Neutralising H1N1, d14', 'Antibody (d14-28)'),
 ('S03-H', 'Neutralising titre Aichi H3N2', 'd14', 'Neutralising H3N2, d14', 'Antibody (d14-28)'),
 ('S03-A', 'Serum IgG anti-CA09 H1N1 (titre)', 'd14', 'IgG H1N1, d14', 'Antibody (d14-28)'),
 ('S13-A', 'Serum IgG2a anti-CA09 (titre)', 'd14', 'IgG2a H1N1, d14', 'Antibody (d14-28)'),
 ('S13-J', 'Serum IgG anti-Aichi d28 post-boost (titre)', 'd28', 'IgG H3N2 post-boost, d28', 'Antibody (d14-28)'),
 ('S05-F', 'MLN IFNg+ CD8 T, H5N1 restim (%) d14', 'd14', 'IFN-g+ CD8 (H5N1), d14', 'T-cell memory (d14-60)'),
 ('S05-I', 'Lung CD8 TRM CD69+CD103+ (%)', 'd25', 'Lung CD8 TRM, d25', 'T-cell memory (d14-60)'),
 ('S05-G', 'MLN IFNg+ CD8 T, H5N1 restim (%) d60', 'd60', 'IFN-g+ CD8 (H5N1), d60', 'T-cell memory (d14-60)'),
 ('S05-H', 'MLN GZMB+ CD8 T (%) d60', 'd60', 'GZMB+ CD8, d60', 'T-cell memory (d14-60)'),
]
rows = []
for blk, meas, t, lab, stage in items:
    d = Cc[(Cc.block == blk) & (Cc.measurand == meas) & (Cc.time == t)]
    f = lambda g: np.log(np.clip(d[d.group == g].value.values, 5 if 'HI' in meas else 1e-9, None))
    a, b = f('PSLN-344'), f('PSLN-212')
    diff = a.mean() - b.mean(); se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    dfw = se ** 4 / ((a.var(ddof=1) / len(a)) ** 2 / (len(a) - 1) + (b.var(ddof=1) / len(b)) ** 2 / (len(b) - 1))
    q = stats.t.ppf(0.975, dfw)
    y = f('PSLN-212(Y)') if 'PSLN-212(Y)' in set(d.group) else None
    pct_y = 100 * np.exp(a.mean() - y.mean()) if y is not None else np.nan
    rows.append(dict(label=lab, stage=stage, ratio=np.exp(diff), lo=np.exp(diff - q * se), hi=np.exp(diff + q * se), pct_young=pct_y, block=blk))
F = pd.DataFrame(rows); F.to_csv('/tmp/work/tidy/forest_344_vs_212.csv', index=False)
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.4, 8.2), gridspec_kw={'width_ratios': [2.2, 1]}, sharey=True)
ys = np.arange(len(F))[::-1]
stcol = {'Innate (hours)': '#7b3294', 'Innate cells (d2-4)': '#c2a5cf', 'T/B priming (d3-7)': '#a6dba0', 'Antibody (d14-28)': '#008837', 'T-cell memory (d14-60)': '#e08214'}
for y, r in zip(ys, F.itertuples()):
    ax.plot([r.lo, r.hi], [y, y], color='k', lw=1)
    ax.plot(r.ratio, y, 's', color=stcol[r.stage], ms=7, mec='k', mew=0.5)
    ax.text(max(r.hi, r.ratio) * 1.12, y, f'{r.ratio:.1f}x', va='center', fontsize=7)
    if not np.isnan(r.pct_young):
        ax2.barh(y, r.pct_young, color=COL['PSLN-344'], alpha=0.75, height=0.6)
        ax2.text(r.pct_young + 2, y, f'{r.pct_young:.0f}%', va='center', fontsize=7)
ax.axvline(1, color='grey', ls='--', lw=0.8)
ax.set_xscale('log'); ax.set_xlim(0.7, 120)
ax.set_yticks(ys); ax.set_yticklabels([f'{r.label}  [{r.block}]' for r in F.itertuples()], fontsize=7.4)
ax.set_xlabel('PSLN-344 / PSLN-212 (aged), ratio of geometric means (95% CI, log scale)')
ax2.axvline(100, color=COL['PSLN-212(Y)'], ls='--', lw=1); ax2.set_xlim(0, 130)
ax2.set_xlabel('Aged PSLN-344 as % of young\nreference (geometric mean)')
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=c, label=s) for s, c in stcol.items()], fontsize=7, frameon=False, loc='lower right')
fig.suptitle('Figure 3. What Mn2+ adds in aged lungs: PSLN-344 vs PSLN-212 across the immune cascade', fontsize=10, x=0.02, ha='left')
plt.savefig(f'{OUT}/fig3_forest_344_vs_212.png'); plt.close()

# ---------------- Figure 4: MoA schematic ----------------
fig, ax = plt.subplots(figsize=(10, 7.4)); ax.axis('off'); ax.set_xlim(0, 100); ax.set_ylim(0, 100)
def box(x, y, w, h, title, body, fc, ec='k', ls='-', lw=1.0):
    p = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.6,rounding_size=1.5', fc=fc, ec=ec, lw=lw, ls=ls)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h - 1.6, title, ha='center', va='top', fontsize=8.2, weight='bold')
    ax.text(x + 1.2, y + h - 5.6, body, ha='left', va='top', fontsize=6.6, linespacing=1.25)
def arrow(x1, y1, x2, y2, style='-'):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', mutation_scale=12, lw=1.3, color='#333333', ls=style))
box(1, 76, 30, 21, '1  Delivery (vehicle)', 'Surfactant-mimetic liposome: AECII uptake\n15.8% vs 0.4% free dye (S01-B, ~42x)\nAM uptake needs SP-A/D: 43.1% vs 12.7%\nin Sftpa1/Sftpd-/- (S01-C)\nMn form: less AEC uptake 3.8% vs 15.8%\n(S08-C; values overlap S01-B - flagged)', '#e8f1fb', ls='--')
box(35, 76, 30, 21, '2  STING/IFN activation (16-36 h)', 'Ifnb1 16 h: PSLN-344 37x vs PSLN-212 17x\nvs vehicle 1x; young ref 37x (S01-A)\nDose-response: 20 ug = 91% of 40 ug (S08-A)\nGm-csf 36 h: 8.7x vs 1.6x (S02-F)\nCcl2 16 h ~590x (S09-A, n=3)\nSTING dependence NOT tested (no Sting-/-)', '#fde9e8', lw=0.8)
box(69, 76, 30, 21, '3  Monocyte recruitment (d2-6)', 'Monocytes d4: 30.6% vs 16.7% vs 10.4%\n(S01-D); young 32.2%\nCCR2 antagonist: 9.9% -> 3.3% (S07-B)\nGap-junction block (CBX): 7.3% -> 3.1% (S11-C)\nIFNAR-/- BM: 21.3 -> 15.4% (S12-A, n=3, ns)', '#fde9e8', lw=3)
box(69, 46, 30, 24, '4  moDC differentiation', 'IFNAR-/- precursors: moDC 2.1% vs 19.7%\nWT (S02-H); GM-CSF rescues to 12.4%\nGM-CSF add-back to PSLN-212:\n5.9% -> 13.8% (S02-G)\nPSLN-212 instead expands Ly6C+CCR2+\nmacrophages (19 vs 3.4 x10^5, d5; S07-A)\nCD206+ macrophages 49% vs 71% (S11-E)', '#fde9e8', lw=3)
box(35, 46, 30, 24, '5  DC migration & priming (d3)', 'Lung cDC1 37.5% vs 22.8% (S01-F)\nCCR7+ migratory DC 30.7% vs 7.3% (S02-A)\nAntigen+ DC in MLN 7.1% vs 1.8%;\nPTX blocks: 2.4% (S02-C)\nCD40/CD86 only 29-38% of young (S02-D)\nOT-I priming 18.7% vs 0.8% (S02-E);\nin vivo MLN priming PTX-sensitive (S05-C)', '#fff7e6', lw=3)
box(1, 46, 30, 24, '6  T-follicular / B-cell (d5-7)', 'Tfh ICOS-hi 10.3% vs 3.8% vs 0.3% (S04-A)\nTfr 10.8% vs 26.7% (S04-B)\nGC B 6.5% vs 2.3% vs 1.2% (S03-K)\nAicda 12x, E47 25x vs 3-6x (S03-L, n=3)\nLung Treg 3.0% vs 6.7% (S04-D, n=3)', '#e9f5e9', lw=0.8)
box(1, 12, 30, 27, '7  Antibody (d14-28)', 'HI GMT H1N1 368 vs 46 vs 8; young 485\nHI GMT H3N2 320 vs 35 vs 10; young 368\nNeut. ~9x, IgG 13-19x vs PSLN-212 (S03)\nIgG2a/IgG1 ~1.9-2.3 vs ~0.5 (S13-A-D;\nS03-B/F labels rotated - not used)\nNot measured: mucosal IgA', '#e9f5e9', lw=0.8)
box(35, 12, 30, 27, '8  CD8 T-cell memory (d3-60)', 'Lung GZMB+ CD8 d3 5.7% vs 3.0% (S05-E)\nCCR2 blockade: 6.8% -> 1.4% (S02-I, young)\nIFN-g+ CD8 (H5N1) d14 6.4% vs 1.5%,\nd60 9.9% vs 3.0% (S05-F/G)\nLung TRM d25 4.0% vs 1.0% (S05-I)', '#fff7e6', lw=3)
box(69, 12, 30, 27, '9  Protection (aged mice)', 'Pooled survival, 11 experiments:\nPSLN-344 68/80 (85%) vs PSLN-212 11/80\n(14%) vs vehicle 1/80 (1%)\nHomologous, H5N1, heterosubtypic,\n60-day durability; day 2-3 onset\nPSLN-344 alone (no antigen): 0/7 (S15-H)\nYoung ref 69/70 (99%)', '#e6e6fa', lw=0.8)
arrow(31.5, 86, 34.5, 86); arrow(65.5, 86, 68.5, 86); arrow(84, 75.5, 84, 70.6); arrow(68.5, 58, 65.5, 58); arrow(34.5, 58, 31.5, 58)
arrow(16, 45.5, 16, 39.6); arrow(50, 45.5, 50, 39.6); arrow(31.5, 25, 34.5, 25); arrow(65.5, 25, 68.5, 25)
ax.text(1, 4.5, 'Numbers: aged PSLN-344 vs aged PSLN-212 vs aged vehicle (vaccine + empty liposome) unless stated; source block in brackets. '
        'THICK border = step tested by a\nperturbation (blockade / knockout / add-back); thin border = correlative only (formulation comparison); dashed = tracer data with an integrity flag.\n'
        'Missing links: no Sting-/- or cGAS-/- test, no Mn-only or free-CDN arm, so the STING attribution and the Mn-CDN synergy are inferred, not shown.', fontsize=6.6, va='top')
ax.set_title('Figure 4. Mechanism of action reconstructed from the program data (PSLN-344 in aged lungs)', fontsize=10, loc='left')
plt.savefig(f'{OUT}/fig4_moa.png'); plt.close()

# ---------------- Figure 5: data-integrity evidence ----------------
fig, axs = plt.subplots(2, 2, figsize=(9.6, 7.6))
ax = axs[0, 0]
for a in range(1, 8):
    c = W[(W.block == 'S15-C') & (W.group == 'PSLN-344') & (W.animal == a)].sort_values('day')
    i = W[(W.block == 'S15-I') & (W.group == '3d Vaccine+PSLN-344') & (W.animal == a)].sort_values('day')
    ax.plot(c.day, c.value, '-', color='#d9534f', lw=2.2, alpha=0.45, label='S15-C PSLN-344 (d14 rgH5N1 challenge)' if a == 1 else None)
    ax.plot(i.day, i.value, '--', color='k', lw=0.9, label='S15-I Vaccine+PSLN-344 (d3 challenge)' if a == 1 else None)
ax.set_title('(a) Two different experiments, same weight curves\n40 of 42 day-2-12 values identical (7/7 animals)', fontsize=8.5, loc='left')
ax.set_xlabel('Day after challenge'); ax.set_ylabel('Body weight, % of day 0'); ax.legend(fontsize=6.5, frameon=False, loc='lower left')
ax = axs[0, 1]
a = Cc[Cc.block == 'S11-A'].set_index(['group', 'time', 'rep']).value
b = Cc[Cc.block == 'S11-B'].set_index(['group', 'time', 'rep']).value
j = pd.concat([a.rename('AM'), b.rename('N')], axis=1).dropna().reset_index()
same = np.isclose(j.AM, j.N)
ax.scatter(j.AM[~same], j.N[~same], s=14, color='#4a90d9', alpha=0.7, label=f'different ({(~same).sum()})')
ax.scatter(j.AM[same], j.N[same], s=22, color='#d9534f', label=f'identical to 0.1% ({same.sum()})')
ax.plot([10, 56], [10, 56], 'k:', lw=0.8)
ax.set_xlabel('S11-A alveolar macrophages, % (per animal)'); ax.set_ylabel('S11-B neutrophils, % (same animal slot)')
ax.set_title('(b) Two cell types, 35/100 identical animal values\n(other panel pairs on the sheet: 0-1/100)', fontsize=8.5, loc='left'); ax.legend(fontsize=7, frameon=False)
ax = axs[1, 0]
for a_, (gE, gM) in enumerate([(2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6)]):
    e = W[(W.block == 'S09-E') & (W.group == 'PSLN-344(Y)') & (W.animal == gE)].sort_values('day')
    m = W[(W.block == 'S15-M') & (W.group == 'PSLN-212(Y)') & (W.animal == gM)].sort_values('day')
    ax.plot(e.day, e.value, '-', color='#2ca02c', lw=2.2, alpha=0.45, label='S09-E young BALB/c, PSLN-344' if a_ == 0 else None)
    ax.plot(m.day, m.value, '--', color='k', lw=0.9, label='S15-M young C57BL/6, PSLN-212' if a_ == 0 else None)
ax.set_title('(c) Different strain, formulation and challenge, same curves\n32 shared values incl. 8-decimal matches (6 animals)', fontsize=8.5, loc='left')
ax.set_xlabel('Day after challenge'); ax.set_ylabel('Body weight, % of day 0'); ax.legend(fontsize=6.5, frameon=False, loc='lower left')
ax = axs[1, 1]
grp = ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']
pr = [np.exp(np.mean(np.log(Cc[(Cc.block == 'S03-B') & (Cc.group == g)].value))) for g in grp]
cp = []
for g in grp:
    x2a = Cc[(Cc.block == 'S13-A') & (Cc.group == g)].sort_values('rep').value.values
    x1 = Cc[(Cc.block == 'S13-B') & (Cc.group == g)].sort_values('rep').value.values
    cp.append(np.exp(np.mean(np.log(x2a / x1))))
xx = np.arange(3)
ax.bar(xx - 0.18, pr, 0.36, color='#bbbbbb', label='S03-B as printed')
ax.bar(xx + 0.18, cp, 0.36, color=[COL[g] for g in grp], label='recomputed from S13-A/B titres')
ax.axhline(1, color='k', lw=0.6, ls=':')
ax.set_xticks(xx); ax.set_xticklabels(['PSLN-212', 'PSLN-344', 'young PSLN-212'])
ax.set_ylabel('IgG2a / IgG1 anti-H1N1, geometric mean')
ax.set_title('(d) Printed ratio labels are rotated vs their source titres\n(as printed, PSLN-344 would look Th2-skewed)', fontsize=8.5, loc='left'); ax.legend(fontsize=7, frameon=False)
fig.suptitle('Figure 5. Examples of data-integrity findings that must be resolved before further investment', fontsize=10, x=0.02, ha='left')
plt.tight_layout(); plt.savefig(f'{OUT}/fig5_integrity_examples.png'); plt.close()

# ---------------- Figure 6: safety ----------------
fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.6), gridspec_kw={'width_ratios': [1.3, 1]})
ax = axs[0]
d = W[W.block == 'S08-D']
gcol = {'Vaccine': '#8c8c8c', 'PSLN-212': COL['PSLN-212'], 'PSLN-344': COL['PSLN-344'], 'CMP-204': COL['CMP-204'], 'PSLN-212/R848': '#ff7f0e', 'PSLN-212(Y)': COL['PSLN-212(Y)']}
for g, c in gcol.items():
    s = d[d.group == g].groupby('day').value.agg(['mean', 'std', 'count'])
    ax.errorbar(s.index + (list(gcol).index(g) - 2.5) * 0.08, s['mean'], yerr=s['std'], color=c, marker='o', ms=3.5, lw=1.2, capsize=2,
                label=('Vaccine alone' if g == 'Vaccine' else g))
ax.axhline(90, color='k', ls=':', lw=0.7); ax.text(0.1, 90.3, '10% loss', fontsize=6.5)
ax.set_xlabel('Day after intranasal vaccination (no challenge)'); ax.set_ylabel('Body weight, % of day 0 (mean ± SD)')
ax.set_title('(a) Reactogenicity, aged mice (S08-D, n=5/arm)', fontsize=8.5, loc='left'); ax.legend(fontsize=6.5, frameon=False, ncol=2, loc='lower left')
ax = axs[1]
an = ['CNS Ifnb1 (fold)', 'CNS Tnf (fold)', 'CNS Isg15 (fold)']; gg = ['PBS', 'Sham', 'PSLN-344', 'CT']
gc = {'PBS': '#cccccc', 'Sham': '#8c8c8c', 'PSLN-344': COL['PSLN-344'], 'CT': '#ff7f0e'}
for i, m in enumerate(an):
    for k, g in enumerate(gg):
        v = Cc[(Cc.block == 'S10-A') & (Cc.measurand == m) & (Cc.group == g)].value.values
        xx = i + (k - 1.5) * 0.2
        ax.scatter(np.full(len(v), xx) + np.random.default_rng(k).uniform(-0.04, 0.04, len(v)), v, s=9, color=gc[g], alpha=0.8,
                   label=(('Cholera toxin (CT)' if g == 'CT' else ('Vehicle (Sham)' if g == 'Sham' else g)) if i == 0 else None))
        ax.plot([xx - 0.07, xx + 0.07], [v.mean(), v.mean()], color='k', lw=1)
ax.set_xticks(range(3)); ax.set_xticklabels(['Ifnb1', 'Tnf', 'Isg15']); ax.set_ylabel('CNS transcript, fold vs untreated')
ax.set_title('(b) CNS inflammation 36 h after IN dosing (S10-A)', fontsize=8.5, loc='left'); ax.legend(fontsize=6.5, frameon=False)
fig.suptitle('Figure 6. Tolerability signals available in the dataset (aged mice)', fontsize=10, x=0.02, ha='left')
plt.tight_layout(); plt.savefig(f'{OUT}/fig6_safety.png'); plt.close()

# ---------------- Figure 7: biomarker timeline ----------------
B = pd.read_csv('/tmp/work/tidy/biomarker_candidates.csv')
tmap = {'16h': 16, '16h (as printed)': 16, '36h': 36, '4': 96, '72h': 72, 'd3': 72, 'd7': 168, 'd14': 336, 'd25': 600, 'd60': 1440}
short = {'Lung Ifnb1 (fold vs untreated)': 'IFN-b (Ifnb1)', 'Lung Gm-csf (fold vs untreated)': 'GM-CSF (Csf2)', 'Lung Ccl2 (log10 fold)': 'CCL2 / MCP-1',
         'Lung monocytes CD11b+Ly6C+ (%)': 'monocytes', 'Lung cDC1 (%)': 'cDC1', 'Lung migratory CCR7+ CD11b+ DC (%)': 'CCR7+ DC',
         'Lung GZMB+ CD8 T (%)': 'GZMB+ CD8', 'MLN Tfh ICOS-high (%)': 'Tfh ICOS-hi', 'MLN Tfr Foxp3+ in CXCR5+ICOShi (%)': 'Tfr (lower = better)',
         'MLN GC B cells CXCR5+GL7+ (%)': 'GC B cells', 'HI titre CA09 H1N1': 'HI H1N1', 'HI titre Aichi H3N2': 'HI H3N2',
         'Neutralising titre CA09 H1N1': 'MN H1N1', 'Serum IgG anti-CA09 H1N1 (titre)': 'IgG H1N1', 'Serum IgG2a anti-CA09 (titre)': 'IgG2a H1N1',
         'MLN IFNg+ CD8 T, H5N1 restim (%) d14': 'IFN-g+ CD8 d14', 'MLN IFNg+ CD8 T, H5N1 restim (%) d60': 'IFN-g+ CD8 d60',
         'Lung CD8 TRM CD69+CD103+ (%)': 'lung TRM'}
off = {'IFN-b (Ifnb1)': (6, -10), 'CCL2 / MCP-1': (6, 2), 'GM-CSF (Csf2)': (6, 2), 'HI H1N1': (6, 2), 'HI H3N2': (6, -9), 'MN H1N1': (6, -9),
       'IgG H1N1': (-66, -12), 'IgG2a H1N1': (6, 4), 'IFN-g+ CD8 d14': (-78, 2), 'lung TRM': (6, 2), 'IFN-g+ CD8 d60': (-78, 4),
       'GC B cells': (6, 2), 'Tfr (lower = better)': (6, -4), 'Tfh ICOS-hi': (6, -9), 'CCR7+ DC': (-84, -3), 'monocytes': (-8, 9),
       'GZMB+ CD8': (-58, -8), 'cDC1': (-30, -8)}
B['hours'] = B.time.map(tmap); B['short'] = B.marker.map(short)
fig, ax = plt.subplots(figsize=(9.4, 4.8))
for r in B.itertuples():
    human = not r.human_analogue.startswith('(')
    ax.scatter(r.hours, abs(r.g_344_vs_212), s=70, marker='o', color=('#1f4e79' if human else 'white'), edgecolor='#1f4e79', linewidths=1.2, zorder=3)
    py = '' if np.isnan(r.pct_young_restored) else f' ({r.pct_young_restored:.0f}%)'
    dx, dy = off.get(r.short, (6, 2))
    ax.annotate(r.short + py, (r.hours, abs(r.g_344_vs_212)), fontsize=7, xytext=(dx, dy), textcoords='offset points')
ax.scatter([], [], s=60, color='#1f4e79', label='has a human-measurable analogue (proposed clinical biomarker)')
ax.scatter([], [], s=60, color='white', edgecolor='#1f4e79', label='animal tissue only (mechanism / research)')
ax.set_xscale('log'); ax.set_xticks([16, 36, 72, 168, 336, 600, 1440]); ax.set_xticklabels(['16 h', '36 h', '3 d', '7 d', '14 d', '25 d', '60 d'])
ax.set_xlim(11, 2600); ax.set_ylim(1.6, 8.9)
ax.set_ylabel('Separation of PSLN-344 from PSLN-212\n(|Hedges g|, aged mice, n=3-5/arm)'); ax.set_xlabel('Time after intranasal dosing')
ax.legend(fontsize=7.2, frameon=False, loc='upper right')
fig.text(0.01, -0.03, 'Label (x%) = aged PSLN-344 response as % of the young-reference response above the vehicle baseline (analysis scale). Tfr: lower is better (|g| shown).', fontsize=6.8)
ax.set_title('Figure 7. Candidate efficacy biomarkers by time point: every marker separates PSLN-344 from PSLN-212 (AUC 0.98-1.00)', fontsize=9.5, loc='left')
plt.savefig(f'{OUT}/fig7_biomarker_timeline.png'); plt.close()
print('figures written:', sorted(os.listdir(OUT)))
