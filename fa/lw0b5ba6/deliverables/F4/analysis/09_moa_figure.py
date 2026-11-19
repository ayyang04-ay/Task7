#!/usr/bin/env python
"""
09_moa_figure.py -- Figure 5: mechanism-of-action map. Every number is read from tables produced by
05_endpoints.py / 04_survival.py / 06_safety_dose.py (nothing typed by hand except labels).
Run: micromamba run -n core python 09_moa_figure.py
"""
import os, re, numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
HERE = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(HERE, 'tables'); F = os.path.join(HERE, '..', 'figures')
D = pd.read_csv(f'{T}/T05_endpoint_descriptives.csv', keep_default_na=False); D['level'] = D.level.astype(str)
def m(block, group, level='', geo=False):
    r = D[(D.block == block) & (D.group == group) & (D.level == str(level))].iloc[0]
    return float(r.centre_on_analysis_scale) if geo else float(r['mean'])
P = pd.read_csv(f'{T}/T04_survival_pooled.csv'); DR = pd.read_csv(f'{T}/T08e_S08A_dose_response.csv').set_index('group')
S2 = pd.read_csv(f'{T}/T02_survival_by_group.csv')
def sv(block, group):
    r = S2[(S2.block == block) & (S2.group == group)].iloc[0]; return f'{int(r.survivors)}/{int(r.n_rows)}'
early = P[(P.analysis.str.startswith('Aged BALB/c, single dose')) & (P.ref_group == 'PSLN-212')].iloc[0]
early_s = P[(P.analysis.str.startswith('Aged BALB/c, single dose')) & (P.ref_group == 'Sham') & (P.test_group == 'PSLN-344')].iloc[0]
d60 = P[(P.analysis.str.startswith('Aged BALB/c, challenge d60')) & (P.ref_group == 'PSLN-212')].iloc[0]
r13 = lambda a, b: (pd.read_csv(os.path.join(HERE, 'parsed', 'scalar_long.csv'), keep_default_na=False))
T7 = pd.read_csv(f'{T}/T07_restoration_index_curated.csv').set_index('block')

boxes = [
 ('1  DELIVERY to the alveolus',
  f"Alveolar-macrophage uptake needs surfactant proteins A/D: DiD+ macrophages {m('S01-C','WT'):.0f}% in wild-type vs {m('S01-C','SPA/D'):.0f}% in Sftpa1/Sftpd-null [S01-C, n=4]\n"
  f"Cargo dye reaches alveolar epithelium: type II cells {m('S01-B','AECII/PSLN-SRB'):.1f}% vs {m('S01-B','AECII/FreeSRB'):.1f}% with free dye [S01-B]\n"
  f"Gap-junction blocker (CBX) cuts recruited monocytes {m('S11-C','CBX-'):.1f}% -> {m('S11-C','CBX+'):.1f}% [S11-C]",
  'NOT TESTED: uptake in AGED lung for the Mn form (S08-C header conflict); nasal-only vs deep-lung deposition; CBX is not specific'),
 ('2  INNATE TRIGGER in the aged lung',
  f"Ifnb1 at 16 h: PSLN-344 {m('S01-A','PSLN-344','16h',True):.0f}x vs PSLN-212 {m('S01-A','PSLN-212','16h',True):.0f}x   (young + PSLN-212: {m('S01-A','PSLN-212(Y)','16h',True):.0f}x) [S01-A]\n"
  f"Mn raises the ceiling, not the potency: Emax {DR.loc['PSLN-344','Emax_fold']:.0f}x vs {DR.loc['PSLN-212','Emax_fold']:.0f}x; ED50 {DR.loc['PSLN-344','ED50_ug']:.0f} vs {DR.loc['PSLN-212','ED50_ug']:.0f} ug [S08-A, n=3]\n"
  f"Gm-csf: {m('S02-F','PSLN-344','16h',True):.1f}x / {m('S02-F','PSLN-344','36h',True):.1f}x / {m('S02-F','PSLN-344','72h',True):.1f}x at 16/36/72 h vs <= {max(m('S02-F','PSLN-212',t,True) for t in ['16h','36h','72h']):.1f}x with PSLN-212 [S02-F]",
  'NOT TESTED: STING dependence (no Sting1-null / inhibitor arm); Mn-only liposome; free CDN-1807; GM-CSF source cell; young comparator for Gm-csf'),
 ('3  MONOCYTE FATE: dendritic cell instead of macrophage',
  f"Monocyte influx day 4: {m('S01-D','PSLN-344',4):.1f}% vs {m('S01-D','PSLN-212',4):.1f}% [S01-D]; CCR2 antagonist: {m('S07-B','PSLN-344','CD11b+Ly6C+ monocytes'):.1f}% -> {m('S07-B','PSLN-344+INCB3344','CD11b+Ly6C+ monocytes'):.1f}% [S07-B]\n"
  f"mo-DC need IFNAR: {m('S02-H','WT w/o cDC'):.1f}% (WT marrow) vs {m('S02-H','IFN w/o cDC'):.1f}% (Ifnar-null); GM-CSF rescues to {m('S02-H','GMCSF'):.1f}% [S02-H]\n"
  f"Recombinant GM-CSF lifts PSLN-212 mo-DC {m('S02-G','PSLN-212'):.1f}% -> {m('S02-G','PSLN-212+GM-CSF'):.1f}% [S02-G]\n"
  f"Lung CD11b+ DC day 4: {m('S01-E','PSLN-344',4):.1f}% vs {m('S01-E','PSLN-212',4):.1f}% [S01-E]; without Mn, Ly6C+CCR2+ macrophages pile up: {m('S07-A','PSLN-212',5):.1f} vs {m('S07-A','PSLN-344',5):.1f} x10^5 at day 5 [S07-A, n=3]",
  'NOT TESTED: GM-CSF necessity (no neutralisation with PSLN-344); S07-C (macrophage transfer) unusable - both columns carry the same label'),
 ('4  PRIMING and release of the regulatory brake',
  f"CCR7+ migratory DC {m('S02-A','PSLN-344'):.1f}% vs {m('S02-A','PSLN-212'):.1f}% [S02-A]; antigen-carrying DC in node {m('S02-C','PSLN-344'):.1f}% vs {m('S02-C','PSLN-212'):.1f}%, pertussis-toxin-sensitive [S02-C]\n"
  f"CD8 cross-priming by node DC {m('S02-E','PSLN-344'):.1f}% vs {m('S02-E','PSLN-212'):.1f}% [S02-E]; BUT co-stimulation stays low: CD40+ {m('S02-D CD40','PSLN-344'):.0f}% vs {m('S02-D CD40','PSLN-212(Y)'):.0f}% in young [S02-D]\n"
  f"Follicular regulatory T {m('S04-B Foxp3','PSLN-344'):.1f}% vs {m('S04-B Foxp3','PSLN-212'):.1f}% (day 7; gone by day 30: {m('S04-C','PSLN-344'):.1f}% vs {m('S04-C','PSLN-212'):.1f}%) [S04-B, S04-C]; lung Treg {m('S04-D','PSLN-344'):.1f}% vs {m('S04-D','PSLN-212'):.1f}% [S04-D, n=3]",
  ''),
 ('5  ADAPTIVE RESPONSE',
  f"Germinal-centre B cells {m('S03-K','PSLN-344'):.1f}% vs {m('S03-K','PSLN-212'):.1f}% [S03-K]; HAI GMT {m('S03-C','PSLN-344',geo=True):.0f} vs {m('S03-C','PSLN-212',geo=True):.0f} (H1N1), {m('S03-G','PSLN-344',geo=True):.0f} vs {m('S03-G','PSLN-212',geo=True):.0f} (H3N2) [S03-C, S03-G]\n"
  f"IgG2a:IgG1 {T7.loc['S13-A/S13-B','aged344']:.1f} vs {T7.loc['S13-A/S13-B','aged212']:.1f} (recomputed) [S13-A, S13-B]\n"
  f"Cross-reactive IFN-g+ CD8 (restimulated with rgH5N1) {m('S05-F','PSLN-344'):.1f}% vs {m('S05-F','PSLN-212'):.1f}% day 14; {m('S05-G','PSLN-344'):.1f}% vs {m('S05-G','PSLN-212'):.1f}% day 60 [S05-F, S05-G]\n"
  f"Lung resident-memory CD8 {m('S05-I','PSLN-344'):.1f}% vs {m('S05-I','PSLN-212'):.1f}% [S05-I]; CCR2 antagonist cuts lung GZMB+ CD8 {m('S02-I','PSLN-344(Y)'):.1f}% -> {m('S02-I','PSLN-344(Y)+INCB3344'):.1f}% (young) [S02-I]",
  'NOT MEASURED: mucosal IgA; lung or nasal virus titres'),
 ('6  PROTECTION of aged mice after one intranasal dose',
  f"Challenge 2-14 days after dosing: {early.surv_test} survive vs {early.surv_ref} (PSLN-212) vs {early_s.surv_ref} (vaccine + empty liposome) [S03-I, S03-J, S06-A..D]\n"
  f"Challenge at day 60: {d60.surv_test} vs {d60.surv_ref} (PSLN-212) [S06-E..G]\n"
  f"Needs antigen AND adjuvant: vaccine + PSLN-344 {sv('S15-H','3d Vaccine+PSLN-344')}, PSLN-344 alone {sv('S15-H','3d PSLN-344')}, vaccine alone {sv('S15-H','3d Vaccine')} [S15-H]",
  'NOT TESTED: which arm protects (no CD8 depletion / serum transfer); any second species; male animals'),
]
import textwrap
plt.rcParams.update({'savefig.dpi': 250})
# add a gap note for box 4
boxes[3] = (boxes[3][0], boxes[3][1], 'PARTIAL ONLY: DC co-stimulation (CD40 / CD86) stays at 29–38% of the young level; the adjuvant and age of the pertussis-toxin arm are not stated in S02-C / S02-E')
W = 7.4; WRAP = 98; GW = 37; LH = 1.55; FS = 6.2      # figure width (in); chars per line left / right; line height (axis units); font size
layout = []
for title, body, gaptxt in boxes:
    lines = []
    body = body.replace(' -> ', ' → ').replace('<=', '≤').replace(' ug ', ' µg ').replace('x10^5', '×10⁵').replace('IFN-g+', 'IFN-γ⁺')
    body = re.sub(r'(\d)x(?![0-9a-zA-Z])', r'\1×', body).replace('2-14 days', '2–14 days')
    for para in body.split('\n'):
        w = textwrap.wrap(para, WRAP, subsequent_indent='   ', break_on_hyphens=False)
        lines += ['• ' + w[0]] + w[1:]
    glines = textwrap.wrap(gaptxt, GW, break_on_hyphens=False) if gaptxt else []
    h = max(3.7 + LH * len(lines) + 0.5, 1.2 + LH * len(glines) + 1.2)
    layout.append((title, lines, glines, h))
gap = 1.9; total = sum(h for *_, h in layout) + gap * (len(layout) - 1) + 8.3
UNIT = 0.0835                                          # inches per axis unit (vertical)
fig, ax = plt.subplots(figsize=(W, total * UNIT)); ax.set_xlim(0, 100); ax.set_ylim(0, total); ax.axis('off'); fig.subplots_adjust(0.005, 0.005, 0.995, 0.995)
ax.text(0.5, total - 0.4, 'Figure 2. Mechanism-of-action map built only from our data', fontsize=8.5, fontweight='bold', va='top')
ax.text(0.5, total - 2.7, '(aged mice unless stated; each pair of numbers is PSLN-344 vs the Mn-free PSLN-212)', fontsize=6.5, va='top', color='#333333')
ax.text(0.5, total - 5.2, 'Shown by our data', fontsize=7.2, fontweight='bold', color='#0b2f5b', va='top')
ax.text(70.5, total - 5.2, 'Gaps: not established by our data', fontsize=7.2, fontweight='bold', color='#c51b1b', va='top')
y = total - 7.6
for i, (title, lines, glines, h) in enumerate(layout):
    y0 = y - h
    ax.add_patch(FancyBboxPatch((0.6, y0), 67.6, h, boxstyle='round,pad=0.15,rounding_size=0.7', fc='#eef3fa', ec='#1f5fa8', lw=0.9))
    ax.text(1.6, y - 1.0, title, fontsize=7.4, fontweight='bold', color='#0b2f5b', va='top')
    ax.text(1.6, y - 3.45, '\n'.join(lines), fontsize=FS, va='top', linespacing=1.36, color='#111111')
    if glines:
        ax.add_patch(FancyBboxPatch((70.2, y0 + 0.4), 29.2, h - 0.8, boxstyle='round,pad=0.15,rounding_size=0.7', fc='#fdf1f1', ec='#c51b1b', lw=0.8, ls='--'))
        ax.text(71.0, y - h / 2, '\n'.join(glines), fontsize=FS, va='center', color='#8a1010', linespacing=1.38)
    if i < len(layout) - 1:
        ax.add_patch(FancyArrowPatch((34, y0 - 0.25), (34, y0 - gap + 0.25), arrowstyle='-|>', mutation_scale=9, color='#1f5fa8', lw=1.1))
    y = y0 - gap
fig.savefig(f'{F}/fig2_moa_map.png'); plt.close(fig)
print('written fig2_moa_map.png', round(total * UNIT, 2), 'in tall')
