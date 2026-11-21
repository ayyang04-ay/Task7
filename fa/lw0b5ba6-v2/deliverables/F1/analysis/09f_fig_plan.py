"""Figure 7: indicative sequence of the next studies with decision gates (planning estimates, not data)."""
import datetime as dt
from figstyle import *
import matplotlib.dates as mdates
M0 = dt.date(2026, 11, 1)
def m(x): return M0 + dt.timedelta(days=round(x * 30.44))
rows = [
 ('Step 0   Data reconciliation', [(0, 1.5, '#7f7f7f', '')]),
 ('Study 1  Efficacy, attribution, benchmark', [(1, 3, '#c6dbef', 'animals'), (3, 5.5, '#1b5fa7', 'in life'), (5.5, 7.5, '#6baed6', 'analysis')]),
 ('Study 2  Safety and biodistribution', [(2, 6, '#d6604d', 'in life, recovery'), (6, 7.5, '#f4a582', 'path.')]),
 ('Study 3  Human cells', [(1, 5, '#41ab5d', 'in vitro')]),
 ('Study 4  Manufacturing and analytics', [(1, 7, '#8c6bb1', 'analytical package'), (7, 16, '#c9b6dd', 'stability 3 / 6 / 12 months')]),
 ('Study 5  Dose, regimen, durability', [(6, 8, '#c6dbef', 'animals'), (8, 14.5, '#1b5fa7', 'in life to day 180'), (14.5, 15.7, '#6baed6', '')]),
 ('Study 6  Ferret, spray vs aerosol', [(8, 13, '#41ab5d', 'in life'), (13, 15, '#a1d99b', 'analysis')]),
 ('Study 7  IND-enabling (only after Gate 2)', [(16.5, 27, '#d9d9d9', 'GLP toxicology, GMP: conditional')]),
]
fig, ax = plt.subplots(figsize=(W, 2.95))
fig.subplots_adjust(left=0.30, right=0.985, top=0.875, bottom=0.115)
for i, (lab, segs) in enumerate(rows):
    for a, b, col, txt in segs:
        ax.barh(i, (m(b) - m(a)).days, left=mdates.date2num(m(a)), color=col, edgecolor='k', lw=0.35, height=0.62)
        if txt:
            ax.text(mdates.date2num(m(a)) + (m(b) - m(a)).days / 2, i, txt, ha='center', va='center', fontsize=5.4, color='white' if col in ('#1b5fa7', '#7f7f7f', '#d6604d', '#8c6bb1', '#41ab5d') else 'black')
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=6.5); ax.invert_yaxis()
for x, lab, col in [(1.5, 'Gate 0\ndata lock', '#555555'), (8, 'Gate 1\nefficacy, active\ningredient, safety', '#b2182b'), (16, 'Gate 2\ndurability, second\nspecies, manufacturing', '#b2182b')]:
    ax.axvline(mdates.date2num(m(x)), color=col, lw=1.0, ls='--', zorder=0)
    ax.text(mdates.date2num(m(x)) + 8, -0.75, lab, color=col, fontsize=5.8, va='bottom', ha='left', fontweight='bold', linespacing=1.1)
ax.xaxis_date(); ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7])); ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y')); ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[4, 10]))
ax.set_xlim(mdates.date2num(m(-0.3)), mdates.date2num(m(27.5))); ax.set_ylim(len(rows) - 0.45, -2.2)
ax.grid(axis='x', which='both', color='#eeeeee', lw=0.5); ax.set_axisbelow(True); ax.tick_params(axis='y', length=0)
fig.text(0.012, 0.985, 'Figure 7. Indicative sequence of next studies and decision gates', fontsize=8.2, fontweight='bold', va='top')
fig.text(0.012, 0.012, 'Planning estimates from 1 November 2026, not data. The limiting item is the supply of mice aged 18–20 months.', fontsize=5.8, color='#333333', va='bottom')
fig.savefig('../figures/Fig7_plan_timeline.png'); plt.close(fig); print('ok')
