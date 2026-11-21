import numpy as np
from fig_style import *
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
BLUE='#1F5FA8'; GRN='#1B7F4B'; GREY='#666666'; RED='#C0392B'
steps = [
 ('1  DELIVERY', 'Liposome → alveolar macrophage → type II epithelium',
  ['Cargo reaches type II cells: 15.8% vs 0.4% for free dye (S01-B)'],
  ['Uptake needs SP-A/SP-D: 43.1% → 12.7%', '   in the double knockout (S01-C)', 'Gap-junction blocker: monocyte influx', '   7.3% → 3.1% (S11-C)']),
 ('2  SENSING (16 h)', 'Type I interferon burst: blunted with age, restored by Mn²⁺',
  ['Ifnb1 mRNA: 37× vs 17×; young benchmark 38× (S01-A)', 'Dose-dependent; Mn²⁺ lifts the ceiling ~3.5×, same ED50 (S08-A)'],
  None),
 ('3  SIGNALS (16–36 h)', 'Chemokines and GM-CSF',
  ['Ccl2 mRNA: 590× vs 7.6× (S09-A, n=3)', 'Gm-csf mRNA: 6.0–8.5× vs 1.4–1.6× (S02-F)'],
  None),
 ('4  RECRUITMENT (day 2–6)', 'CCR2⁺ monocytes → monocyte-derived dendritic cells (DC)',
  ['Lung monocytes, day 4: 30.6% vs 16.7% (S01-D)', 'CD11b⁺ DC, day 4: 18.9% vs 8.3% (S01-E)'],
  ['CCR2 antagonist: monocytes 9.9% → 3.3% (S07-B)', 'Ifnar-null marrow: monocyte-derived DC', '   19.7% → 2.1%; GM-CSF rescues to 12.4% (S02-H)', 'GM-CSF added to PSLN-212: 5.9% → 13.8% (S02-G)']),
 ('5  MIGRATION + PRIMING (day 1.5–4)', 'Antigen carried to lymph node; CD8 priming also in the lung',
  ['CCR7⁺ migratory DC: 30.7% vs 7.3% (S02-A)', 'Antigen-bearing DC in lymph node: 7.1% vs 1.8% (S02-C)'],
  ['Pertussis toxin blocks T-cell priming in the', '   node (30.9% → 6.8%) but not in the lung', '   (59.0% vs 55.1%) (S05-C, n=3)']),
 ('6  ADAPTIVE IMMUNITY (day 3–60)', 'Germinal centers, IgG2a-skewed antibody, CD8 T cells',
  ['HAI titer: 368 vs 46 (S03-C)', 'IgG2a:IgG1 ratio: 1.85 vs 0.54 (recomputed from S13-A/B)', 'IFN-γ⁺ CD8 T cells against H5N1: 6.4% vs 1.5% (S05-F)', 'Lung-resident memory CD8 T cells: 4.0% vs 1.0% (S05-I)'],
  ['CCR2 antagonist removes the lung effector', '   CD8 response: GZMB⁺ CD8 6.8% → 1.4%', '   (S02-I, young animals)']),
 ('7  PROTECTION', 'Survival after lethal matched or mismatched challenge',
  ['Aged BALB/c, 7 experiments: 39/49 vs 4/49 (vaccine alone 0/49)'],
  ['Antigen is required: PSLN-344 alone 0/7;', '   vaccine + PSLN-344 6/7 (S15-H)']),
]
nb = ['That the effect runs through STING or cGAS: there is no knockout arm anywhere in the dataset',
      'What Mn²⁺ does, and whether Mn²⁺ alone or with plain cGAMP would do the same: those arms were never run',
      'Whether antibody or CD8 T cells protect against mismatched virus: no depletion or transfer experiment',
      'The macrophage → regulatory-T-cell arm: S07-A conflicts with S01-D/S11-E; S07-C has duplicate labels',
      'Any step in human cells, in male animals, or in a second species']
LH = 0.155; PADT = 0.40; GAP = 0.13; X0 = 0.05; WL = 4.05; XR = 4.32; WR = 2.93
hs = [PADT + LH*len(n) + 0.05 for _,_,n,_ in steps]
nb_h = 0.33 + LH*len(nb) + 0.02
H = 0.30 + sum(hs) + GAP*len(steps) + nb_h + 0.28
fig = plt.figure(figsize=(FIGW, H)); ax = fig.add_axes([0,0,1,1]); ax.set_xlim(0, FIGW); ax.set_ylim(0, H); ax.axis('off')
y = H - 0.30
ax.text(X0, H-0.13, 'Causal chain  (aged + PSLN-344 vs aged + PSLN-212)', fontsize=8.6, fontweight='bold', va='center')
ax.text(XR, H-0.13, 'Interventional evidence', fontsize=8.6, fontweight='bold', va='center', color=GRN)
for i,(hd, sub, nums, interv) in enumerate(steps):
    h = hs[i]; yb = y-h
    ax.add_patch(FancyBboxPatch((X0, yb), WL, h, boxstyle='round,pad=0.0,rounding_size=0.06', fc='#F3F7FC', ec=BLUE, lw=1.0))
    ax.text(X0+0.09, y-0.12, hd, fontsize=7.8, fontweight='bold', color=BLUE, va='center')
    ax.text(X0+0.09, y-0.285, sub, fontsize=7.0, color='#222222', va='center', style='italic')
    for k, line in enumerate(nums):
        ax.text(X0+0.09, y-PADT-0.045-LH*k, line, fontsize=6.9, color='#111111', va='center')
    if interv:
        hh = LH*len(interv)+0.14; yc = y-h/2
        ax.add_patch(FancyBboxPatch((XR, yc-hh/2), WR, hh, boxstyle='round,pad=0.0,rounding_size=0.06', fc='#EEF7F1', ec=GRN, lw=0.9))
        for k, line in enumerate(interv):
            ax.text(XR+0.07, yc+hh/2-0.07-LH*(k+0.5), line, fontsize=6.7, color='#114B2D', va='center')
        ax.add_patch(FancyArrowPatch((XR-0.02, yc), (X0+WL+0.03, yc), arrowstyle='-|>', mutation_scale=7, color=GRN, lw=0.9))
    else:
        ax.text(XR+0.07, y-h/2+0.07, 'association only', fontsize=6.7, color=GREY, va='center', style='italic')
        ax.text(XR+0.07, y-h/2-0.08, '(no knockout, blocker or add-back)', fontsize=6.7, color=GREY, va='center', style='italic')
    if i < len(steps)-1:
        ax.add_patch(FancyArrowPatch((X0+WL/2, yb-0.005), (X0+WL/2, yb-GAP+0.01), arrowstyle='-|>', mutation_scale=8, color=BLUE, lw=1.2))
    y = yb - GAP
yb = y - nb_h + 0.02
ax.add_patch(FancyBboxPatch((X0, yb), FIGW-2*X0, nb_h, boxstyle='round,pad=0.0,rounding_size=0.06', fc='#FFF6F0', ec=RED, lw=1.0))
ax.text(X0+0.09, yb+nb_h-0.13, 'NOT established by our data', fontsize=7.8, fontweight='bold', color=RED, va='center')
for k, line in enumerate(nb):
    ax.text(X0+0.09, yb+nb_h-0.33-LH*k, '•  '+line, fontsize=6.9, color='#222222', va='center')
ax.text(X0, yb-0.13, 'Group means (geometric means for titers and mRNA). Block IDs in brackets; cell ranges are in the analysis workbook.', fontsize=6.0, color=GREY, va='center')
fig.savefig(OUT+'Fig5_mechanism.png'); print('ok', round(H,2))
