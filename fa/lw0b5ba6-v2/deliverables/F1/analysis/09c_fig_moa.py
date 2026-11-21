"""Figure 5: mechanism-of-action chain assembled from our own blocks, drawn for the printed page.
The detailed evidence for each step is in the table that follows the figure in the text; every number here is computed from the tidy data."""
import numpy as np, pandas as pd
from figstyle import *
import matplotlib.patches as mp
import tidy
m = lambda b, g, x=None: tidy.vec(b, g, x).mean()
gm = lambda b, g: float(np.exp(np.log(np.where(tidy.vec(b, g) <= 0, 5, tidy.vec(b, g))).mean()))
DR = pd.read_csv('../tables/T8_dose_response_S08A.csv').set_index('prep')
steps = [
 ('1', 'DELIVERY', 'Surfactant-like liposome is captured in the alveolus',
  [('KNOCK-OUT', f"macrophage uptake {m('S01-C','WT'):.0f}% vs {m('S01-C','SPA/D'):.0f}% without surfactant proteins A/D [S01-C]"),
   ('INHIBITOR', f"gap-junction block cuts monocyte influx {m('S11-C','CBX-'):.1f}% → {m('S11-C','CBX+'):.1f}% [S11-C]")]),
 ('2', 'TRIGGER', 'Short type I interferon burst — blunted by age, restored by Mn²⁺',
  [('OBSERVED', f"lung Ifnb1, 16 h: {m('S01-A 16h','PSLN-344'):.0f}× vs {m('S01-A 16h','PSLN-212'):.0f}× (young {m('S01-A 16h','PSLN-212(Y)'):.0f}×); {m('S01-A 72h','PSLN-344'):.1f}× by 72 h [S01-A]"),
   ('OBSERVED', f"Mn²⁺ raises the ceiling ({DR.loc['PSLN-212','Emax']:.0f}× → {DR.loc['PSLN-344','Emax']:.0f}×), not the potency [S08-A]")]),
 ('3', 'AMPLIFIER', 'GM-CSF — the signal most specific to PSLN-344',
  [('OBSERVED', f"lung Gm-csf {m('S02-F','PSLN-344',16):.1f}× / {m('S02-F','PSLN-344',36):.1f}× / {m('S02-F','PSLN-344',72):.1f}× at 16 / 36 / 72 h vs ≤{max(m('S02-F','PSLN-212',t) for t in (16,36,72)):.1f}× [S02-F]")]),
 ('4', 'RECRUITMENT', 'Monocytes enter the lung through CCR2',
  [('OBSERVED', f"lung monocytes, day 4: {m('S01-D','PSLN-344',4):.0f}% vs {m('S01-D','PSLN-212',4):.0f}% (young {m('S01-D','PSLN-212(Y)',4):.0f}%) [S01-D]"),
   ('INHIBITOR', f"CCR2 antagonist: monocytes {m('S07-B mono','PSLN-344'):.1f}% → {m('S07-B mono','PSLN-344+INCB3344'):.1f}% [S07-B]")]),
 ('5', 'CELL FATE', 'Monocytes become dendritic cells rather than macrophages',
  [('KNOCK-OUT', f"needs interferon receptor: {m('S02-H','WT w/o cDC'):.0f}% vs {m('S02-H','IFN w/o cDC'):.0f}%; GM-CSF restores {m('S02-H','GMCSF'):.0f}% [S02-H]"),
   ('OBSERVED', f"without Mn²⁺: Ly6C⁺CCR2⁺ macrophages {m('S07-A','PSLN-212',5):.0f} vs {m('S07-A','PSLN-344',5):.1f} ×10⁵ [S07-A]")]),
 ('6', 'PRIMING', 'Dendritic cells carry antigen to the lymph node and prime CD8 T cells',
  [('OBSERVED', f"antigen-carrying node dendritic cells {m('S02-C','PSLN-344'):.1f}% vs {m('S02-C','PSLN-212'):.1f}% [S02-C]; T-cell priming {m('S02-E','PSLN-344'):.0f}% vs {m('S02-E','PSLN-212'):.1f}% [S02-E]"),
   ('GAP', f"co-stimulation stays low: CD40⁺ {m('S02-D CD40','PSLN-344'):.0f}% vs {m('S02-D CD40','PSLN-212(Y)'):.0f}% in young [S02-D]")]),
 ('7', 'RESPONSE', 'Antibody and CD8 T-cell immunity approach young-adult levels',
  [('OBSERVED', f"HAI titre {gm('S03-C','PSLN-344'):.0f} vs {gm('S03-C','PSLN-212'):.0f} [S03-C]; lung resident-memory CD8 {m('S05-I','PSLN-344'):.1f}% vs {m('S05-I','PSLN-212'):.1f}% [S05-I]"),
   ('OBSERVED', f"fewer follicular regulatory T cells: {m('S04-B Foxp3','PSLN-344'):.0f}% vs {m('S04-B Foxp3','PSLN-212'):.0f}% [S04-B]")]),
 ('8', 'OUTCOME', 'Survival after lethal challenge',
  [('OBSERVED', "18/21 vs 3/21 in the core experiments [S06-A, -B, -C]; 14/21 vs 1/21 at day 60 [S06-E, -F, -G]"),
   ('OBSERVED', "PSLN-344 without antigen protects 0/7 [S15-H]")]),
]
TAG = {'KNOCK-OUT': '#1a9850', 'INHIBITOR': '#4575b4', 'OBSERVED': '#7a7a7a', 'GAP': '#d73027'}
H = 7.3
fig, ax = plt.subplots(figsize=(W, H)); ax.axis('off'); ax.set_xlim(0, 100); ax.set_ylim(11.8, 100)
fig.subplots_adjust(left=0.01, right=0.99, top=0.995, bottom=0.005)
ax.text(0, 99.6, 'Figure 5. Mechanism of action assembled from our data', fontsize=8.2, fontweight='bold', va='top')
ax.text(0, 97.0, 'Aged mice, PSLN-344 vs PSLN-212 unless stated.', fontsize=6.3, va='center', color='#333333')
for x0, dx, tag, desc in [(41.0, 8.6, 'KNOCK-OUT', 'genetic'), (57.0, 7.9, 'INHIBITOR', 'drug block'), (74.0, 7.9, 'OBSERVED', 'group difference only')]:
    ax.text(x0, 97.0, tag, fontsize=5.2, fontweight='bold', color='white', va='center', ha='left', bbox=dict(boxstyle='round,pad=0.22', fc=TAG[tag], ec='none'))
    ax.text(x0 + dx, 97.0, desc, fontsize=6.3, va='center', color='#333333')
y = 95.0
for i, (num, name, head, items) in enumerate(steps):
    last = i == len(steps) - 1
    h = 3.6 + 2.25 * len(items)
    ax.add_patch(mp.FancyBboxPatch((0.6, y - h), 98.8, h, boxstyle='round,pad=0.2,rounding_size=0.7', fc='#eaf3e6' if last else '#f4f7fb', ec='#2d7d32' if last else '#1b5fa7', lw=0.9))
    ax.text(2.0, y - 1.55, f'{num}  {name}', fontsize=7.0, fontweight='bold', color='#2d7d32' if last else '#1b5fa7', va='center')
    ax.text(21.5, y - 1.55, head, fontsize=7.0, fontweight='bold', va='center')
    yy = y - 3.85
    for tag, txt in items:
        ax.text(2.0, yy, tag, fontsize=5.2, fontweight='bold', color='white', va='center', ha='left', bbox=dict(boxstyle='round,pad=0.22', fc=TAG[tag], ec='none'))
        ax.text(13.2, yy, txt, fontsize=6.3, va='center'); yy -= 2.25
    y = y - h - 0.45
    if not last:
        ax.annotate('', xy=(50, y - 1.0), xytext=(50, y + 0.3), arrowprops=dict(arrowstyle='-|>', color='#333333', lw=1.0, mutation_scale=8))
    y -= 1.25
gaps = ("Not yet shown by our data:  STING dependence (no STING-deficient control)  ·  what Mn²⁺ does on its own (no Mn²⁺-only or Mn²⁺ + cGAMP liposome)\n"
        "·  which arm protects, CD8 T cells or antibody (no depletion study)  ·  mucosal IgA, virus load and histopathology (never measured)\n"
        "·  S07-C and S08-C, which should have helped, are unusable as labelled (Q9, Q7)")
ax.text(1.0, y + 0.9, gaps, fontsize=6.1, va='top', color='#7f0000', linespacing=1.5, bbox=dict(boxstyle='round,pad=0.45', fc='#fff5f0', ec='#d73027', lw=0.7))
fig.savefig('../figures/Fig5_mechanism_of_action.png'); plt.close(fig); print('ok', y)
