"""Figure 6 - indicative timeline for the proposed next steps (months from the portfolio decision, November 2026)."""
from figstyle import *
import datetime as dt
from matplotlib.patches import FancyBboxPatch
start = dt.date(2026, 11, 1)
def mo(y, m, d=1): return (y - 2026) * 12 + (m - 11) + (d - 1) / 30.0
rows = [
 ('STAGE 0  (proposed now)', None, None, None),
 ('Data audit and dataset lock', mo(2026, 11), mo(2026, 12, 15), 'g0'),
 ('STAGE 1  (proposed now; ends at Gate 1)', None, None, None),
 ('A  Replication + attribution, aged mice, both sexes', mo(2027, 1), mo(2027, 6), 's1'),
 ('B  Delivery route and dose-ranging', mo(2027, 2), mo(2027, 7), 's1'),
 ('C  Pilot safety and manganese distribution', mo(2027, 2), mo(2027, 9), 's1'),
 ('D  Human-cell activity (STING variants, older donors)', mo(2026, 12), mo(2027, 6), 's1'),
 ('E  Licensed antigen + benchmark vs enhanced vaccines', mo(2027, 3), mo(2027, 9), 's1'),
 ('F  Durability to day 180 and age range', mo(2027, 2), mo(2027, 10), 's1'),
 ('Formulation, stability and IP review', mo(2026, 12), mo(2027, 10), 'cmc'),
 ('STAGE 2  (only if Gate 1 is passed)', None, None, None),
 ('G  Ferret immunogenicity and challenge', mo(2027, 11), mo(2028, 9), 's2'),
 ('GLP toxicology (repeat dose)', mo(2028, 1), mo(2028, 11), 's2'),
 ('Process scale-up and clinical batch', mo(2027, 11), mo(2028, 11), 's2'),
 ('Regulatory: pre-IND meeting, IND filing', mo(2028, 2), mo(2028, 12, 15), 'reg'),
 ('STAGE 3', None, None, None),
 ('H  Phase 1 (adults 18-49, then 65+)', mo(2029, 1), mo(2029, 12, 30), 's3'),
]
col = {'g0': '#555555', 's1': '#0072B2', 'cmc': '#56B4E9', 's2': '#009E73', 'reg': '#7FC9AE', 's3': '#CC79A7'}
fig, ax = plt.subplots(figsize=(9.2, 5.6))
y = 0; ys = {}
for lab, a, b, k in rows:
    if a is None:
        ax.text(-0.4, y, lab, fontsize=8.4, fontweight='bold', ha='right', va='center', clip_on=False, color='#222222'); y += 0.8; continue
    ax.barh(y, b - a, left=a, height=0.58, color=col[k], zorder=3)
    ax.text(-0.4, y, lab, fontsize=8.1, ha='right', va='center', clip_on=False)
    ys[lab] = y; y += 1
# gates
g1 = mo(2027, 10, 15); g2 = mo(2028, 12, 15); g0 = mo(2026, 12, 15)
for gx, gl in [(g0, 'Gate 0\ndataset\nlocked'), (g1, 'Gate 1\ngo / no-go'), (g2, 'Gate 2\nIND')]:
    ax.axvline(gx, color='#D55E00', lw=1.4, ls='--', zorder=2)
    ax.text(gx, -1.0, gl, color='#D55E00', fontsize=7.8, fontweight='bold', ha='center', va='bottom', clip_on=False, linespacing=1.05)
ticks = [mo(y_, m_) for y_, m_ in [(2026, 11), (2027, 2), (2027, 5), (2027, 8), (2027, 11), (2028, 2), (2028, 5), (2028, 8), (2028, 11), (2029, 2), (2029, 5), (2029, 8), (2029, 11)]]
tl = ['Nov\n2026', 'Feb\n2027', 'May', 'Aug', 'Nov', 'Feb\n2028', 'May', 'Aug', 'Nov', 'Feb\n2029', 'May', 'Aug', 'Nov']
ax.set_xticks(ticks); ax.set_xticklabels(tl, fontsize=7.6)
for t in ticks: ax.axvline(t, color='#EEEEEE', lw=0.7, zorder=0)
ax.set_xlim(0, mo(2030, 1)); ax.set_ylim(y - 0.2, -0.6); ax.set_yticks([]); ax.spines['left'].set_visible(False)
fig.suptitle('Indicative timeline for the proposed next steps', x=0.01, ha='left', fontsize=11, fontweight='bold', y=0.985)
fig.text(0.01, 0.008, 'Bars show in-life work plus analysis. Assumes mice aged 20 months or older are available from January 2027; Stage 2 and 3 dates are planning placeholders, not commitments.',
         fontsize=7, color='#444444', va='bottom')
fig.subplots_adjust(left=0.40, right=0.985, top=0.83, bottom=0.125)
fig.savefig(FIGDIR + 'fig6_timeline.png')
