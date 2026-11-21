import numpy as np
from figstyle import *
import datetime as dt
from matplotlib.patches import FancyBboxPatch
def m(y, mo, d=1): return (y-2026)*12 + (mo-11) + (d-1)/30.0     # months since 1 Nov 2026
fig, ax = plt.subplots(figsize=(7.3, 3.55))
rows = [
 ('Gate 0   Source-data audit and dataset re-lock', m(2026,11), m(2026,12,20), '#7f7f7f', None),
 ('Study 1  Aged mice, both sexes: replication,\n              attribution, benchmark vs enhanced IM', m(2027,1), m(2027,8,30), '#0072B2', ('interim read-out:\nday-14 challenge', m(2027,4,15))),
 ('Study 2  Dose range, airway and manganese safety', m(2027,1), m(2027,7,30), '#D55E00', None),
 ('Study 3  Human cells: STING alleles, older donors', m(2026,12), m(2027,4,30), '#009E73', None),
 ('Study 4  CMC and delivery device', m(2027,1), m(2027,9,30), '#CC79A7', None),
 ('Study 5  Ferret: efficacy with human-type delivery', m(2027,10,8), m(2028,7), '#56B4E9', None),
 ('IND-enabling (GLP toxicology, GMP batch)', m(2028,8), m(2029,3), '#bbbbbb', None),
]
for i,(lab, a, b, c, note) in enumerate(rows):
    ax.barh(i, b-a, left=a, height=0.56, color=c, zorder=2, alpha=0.95 if i<6 else 0.6, hatch=None if i<6 else '///', edgecolor='white' if i<6 else '#888')
    ax.text(-0.4, i, lab, ha='right', va='center', fontsize=6.8, linespacing=1.05)
    if note:
        ax.plot([note[1], note[1]], [i-0.28, i+0.28], color='white', lw=1.4, zorder=3); ax.text(note[1]+0.15, i-0.34, note[0], fontsize=5.6, color='#0072B2', va='bottom', ha='left', linespacing=1.0)
# gates
for x, lab in [(m(2026,12,20), 'Gate 0'), (m(2027,10,4), 'Gate 1:\nkeep / stop'), (m(2028,7,15), 'Gate 2:\nIND-enabling\nspend')]:
    ax.axvline(x, color='#a3262a', lw=1.0, ls='--', zorder=1)
    ax.text(x, -0.95, lab, ha='center', va='bottom', fontsize=6.3, color='#a3262a', fontweight='bold', linespacing=1.0)
ax.set_ylim(len(rows)-0.45, -1.0); ax.set_xlim(0, m(2029,1))
ticks = [(2026,11),(2027,1),(2027,4),(2027,7),(2027,10),(2028,1),(2028,4),(2028,7),(2028,10),(2029,1)]
ax.set_xticks([m(y,mo) for y,mo in ticks]); ax.set_xticklabels([dt.date(y,mo,1).strftime('%b\n%Y') for y,mo in ticks], fontsize=6.5)
ax.set_yticks([]); ax.spines['left'].set_visible(False); ax.grid(axis='x', color='#eeeeee', lw=0.6); ax.set_axisbelow(True)
ax.text(m(2028,10,15), len(rows)-1+0.02, 'only if Gate 2 passed', fontsize=5.8, color='#333', ha='center', va='center', zorder=4)
fig.subplots_adjust(left=0.385, right=0.985, top=0.90, bottom=0.115)
fig.savefig(OUT+'fig6_timeline.png'); print('ok')
