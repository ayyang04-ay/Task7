import numpy as np
from figstyle import *
import pandas as pd
_LED = pd.read_csv('evidence_ledger.csv', dtype=str, keep_default_na=False)      # written by ledger_numbers.py
N = dict(zip(_LED.Key, _LED.Value_as_cited))
def r0(key):      # '37.1' -> '37', '18.9%' -> '19%'
    v = N[key]; num = float(v.rstrip('%×').replace(',', '')); return f'{num:.0f}' + ('%' if v.endswith('%') else '')
def frac(key): return N[key].split(' ')[0]      # '56/66 (85%)' -> '56/66'
def pct(key): return N[key].split('(')[1].rstrip(')')
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(7.3, 3.95))
ax.set_xlim(0, 100); ax.set_ylim(6.5, 90.5); ax.axis('off')
BW, BH = 12.4, 17.5
xs = [1.0 + i*14.3 for i in range(7)]
yT, yB = 55.5, 14.0
blue, blue_e = '#d6e6f5', '#2b5d8a'; orange, orange_e = '#fbe9c8', '#b57a00'
def box(x, y, title, body, fc, ec, bold_body=False):
    ax.add_patch(FancyBboxPatch((x, y), BW, BH, boxstyle='round,pad=0.15,rounding_size=1.0', fc=fc, ec=ec, lw=0.9))
    ax.text(x+BW/2, y+BH-1.6, title, ha='center', va='top', fontsize=6.3, fontweight='bold', linespacing=1.08, color='#111')
    ax.text(x+BW/2, y+1.5, body, ha='center', va='bottom', fontsize=6.0, linespacing=1.12, color='#111', fontweight='bold' if bold_body else 'normal')
def arrow(x1,y1,x2,y2,c, style='-|>', lw=1.1, ls='-'):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2), arrowstyle=style, mutation_scale=8, color=c, lw=lw, linestyle=ls, shrinkA=0, shrinkB=0))
top = [('Alveolar\nuptake','macrophage →\nepithelium'), ('STING →\ninterferon-β', f"{r0('ifn16_344')}× at 16 h\n(young: {r0('ifn16_young')}×)"), ('GM-CSF\nand CCL2', f"Gm-csf {N['gm_344_36h']}×\nat 36 h"),
       ('Monocytes →\nCD11b+ DC', f"{N['dc4_344']} of lung\ncells, day 4"), ('DC migration,\nT-cell priming', f"antigen+ DC in\nnode: {N['agdc_344']}"), ('Germinal centre,\nCD8 memory', f"HAI {N['hai_h1_344']}\nlung TRM {N['trm_344']}"), ('Survival', f"{frac('survA_344')}\n({pct('survA_344')})")]
bot = [('Alveolar\nuptake','same liposome,\nsame route'), ('STING →\ninterferon-β', f"{r0('ifn16_212')}× at 16 h"), ('GM-CSF\nand CCL2', f"Gm-csf {N['gm_212_36h']}×\nat 36 h"),
       ('Monocytes →\nLy6C+ macro-\nphages', f"{N['mac5_212']} ×10⁵, day 5\n(PSLN-344: {N['mac5_344']})"), ('DC migration,\nT-cell priming', f"antigen+ DC in\nnode: {N['agdc_212']}"), ('Tfr / Treg high,\nweak memory', f"HAI {N['hai_h1_212']}\nlung TRM {N['trm_212']}"), ('Survival', f"{frac('survA_212')}\n({pct('survA_212')})")]
ax.text(0.8, yT+BH+13.2, 'PSLN-344 (CDN-1807 + Mn²⁺) in aged lung', fontsize=7.6, fontweight='bold', color=blue_e)
ax.text(0.8, yB-5.2, 'PSLN-212 (CDN-1807, no Mn²⁺) in aged lung', fontsize=7.6, fontweight='bold', color=orange_e)
for i,(t,b) in enumerate(top):
    box(xs[i], yT, t, b, blue, blue_e, bold_body=(i==6))
    if i<6: arrow(xs[i]+BW+0.25, yT+BH/2, xs[i+1]-0.25, yT+BH/2, blue_e)
for i,(t,b) in enumerate(bot):
    box(xs[i], yB, t, b, orange, orange_e, bold_body=(i==6))
    if i<6: arrow(xs[i]+BW+0.25, yB+BH/2, xs[i+1]-0.25, yB+BH/2, orange_e, ls=(0,(3,2)) if i>=1 else '-')
# perturbation tags (top lane)
def tag(x, y, s, ha='center'):
    ax.text(x, y, s, ha=ha, va='bottom', fontsize=5.6, color='#a3262a', linespacing=1.1)
tag(xs[0]+BW/2+1.0, yT+BH+1.3, f"SP-A/D knockout:\nuptake {r0('spad_a')} → {r0('spad_b')}\nGap-junction blocker:\nmonocytes {N['cbx_a']} → {N['cbx_b']}")
tag(xs[2]+BW/2-7.0, yT+BH+1.3, 'No Mn-only, free-CDN or\nSTING-knockout arm (gap)')
tag(xs[3]+BW/2-6.0, yT+BH+1.3+5.2, ' ')
tag(xs[3]+BW/2-1.5, yT+BH+1.3, f"Ifnar-knockout marrow:\nDC {N['ifnar_a']} → {N['ifnar_b']}\nCCR2 antagonist:\nmonocytes {N['ccr2mono_a']} → {N['ccr2mono_b']}")
tag(xs[4]+BW/2+1.0, yT+BH+1.3, f"Pertussis toxin:\n{N['agdc_344']} → {N['ptx_dc']}")
tag(xs[5]+BW/2+1.2, yT+BH+1.3, 'No CD8 or antibody\ndepletion (gap)')
tag(xs[6]+BW/2, yT+BH+1.3, f"PSLN-344 without\nantigen: {N['h_adj']}")
# rescue arrow from bottom GM-CSF box to top monocyte->DC box
arrow(xs[2]+BW*0.75, yB+BH+0.4, xs[3]+BW*0.22, yT-0.5, '#2a7f3f', lw=1.2)
ax.text(xs[2]+BW*0.75-1.0, (yB+BH+yT)/2-1.2, f"Rescue: adding GM-CSF to PSLN-212\nrestores DC {N['gmres_a']} → {N['gmres_b']}", fontsize=5.8, color='#2a7f3f', ha='right', va='center', linespacing=1.1)
ax.text(xs[4]-1.0, (yB+BH+yT)/2-0.2, 'Boxes: values in aged mice. Red: what happens when the step is blocked,\nor a test that is missing. Source blocks for every number: Table 7.', fontsize=5.6, color='#444', va='center', linespacing=1.15)
fig.subplots_adjust(left=0.003, right=0.997, top=0.997, bottom=0.003)
fig.savefig(OUT+'fig3_mechanism.png'); print('ok')
