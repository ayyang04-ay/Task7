import datetime as dt
import matplotlib.dates as mdates
from fig_style import *
D = lambda s: dt.datetime.strptime(s, '%Y-%m-%d')
rows = [
 ('STAGE 1: requested now', None, None, None, None),
 ('0  Reconcile the data (no animals)', '2026-11-02', '2026-12-11', '#555555', ''),
 ('1  Human STING and human cells; STING knockout', '2026-11-16', '2027-02-26', '#1F5FA8', ''),
 ('2  Components, dose, nose-only dosing (aged mice)', '2027-01-18', '2027-04-23', '#1F5FA8', ''),
 ('3  Manganese distribution and local safety', '2027-01-18', '2027-06-18', '#1F5FA8', 'interim: April'),
 ('4  Benchmark vs licensed-type vaccines', '2027-02-08', '2027-06-04', '#1F5FA8', ''),
 ('5  Durability in the aged: day 90 and day 180', '2027-01-18', '2027-09-03', '#1F5FA8', 'd90: May · d180: Sep'),
 ('Formulation characterization', '2026-11-16', '2027-06-18', '#7FB3E6', ''),
 ('STAGE 2: only if Gate 1 is passed', None, None, None, None),
 ('6  Ferret: immunogenicity, challenge, shedding', '2027-07-12', '2028-02-25', '#E08214', ''),
 ('7  GLP repeat-dose toxicology, two species', '2027-09-06', '2028-06-16', '#E08214', ''),
 ('Scale-up and clinical-grade lot', '2027-07-12', '2028-06-16', '#F2C185', ''),
]
fig, ax = plt.subplots(figsize=(FIGW, 3.9)); fig.subplots_adjust(left=0.385, right=0.985, top=0.88, bottom=0.12)
y = 0; yt=[]; yl=[]
for lab, a, b, c, note in rows:
    if a is None:
        ax.text(-0.62, y, lab, fontsize=7.6, fontweight='bold', va='center', ha='left', color='#222222', transform=ax.get_yaxis_transform()); y -= 0.9; continue
    ax.barh(y, (D(b)-D(a)).days, left=D(a), height=0.58, color=c, edgecolor='none')
    if note:
        inside = lab.startswith('3 ') or lab.startswith('5 ')
        ax.text(D(a)+dt.timedelta(days=5) if inside else D(b)+dt.timedelta(days=6), y, note, fontsize=5.8, va='center', color='white' if inside else '#555555')
    yt.append(y); yl.append(lab); y -= 1
for date, lab, col in [('2026-11-01','Today\n1 Nov 2026','#888888'), ('2027-01-15','Checkpoint\nmid-Jan','#B8860B'), ('2027-06-28','GATE 1\nlate June','#C0392B'), ('2028-06-30','GATE 2\nmid-2028','#C0392B')]:
    ax.axvline(D(date), color=col, lw=1.1, ls='--' if col in ('#888888','#B8860B') else '-')
    ha = 'right' if lab.startswith('Today') else ('left' if lab.startswith('Checkpoint') else 'center')
    dx = dt.timedelta(days=-4) if ha == 'right' else (dt.timedelta(days=4) if ha == 'left' else dt.timedelta(0))
    ax.text(D(date)+dx, 1.0, lab, fontsize=6.4, ha=ha, va='bottom', color=col, fontweight='bold')
ax.set_yticks(yt); ax.set_yticklabels(yl, fontsize=6.9); ax.set_ylim(y+0.35, 0.9)
ax.set_xlim(D('2026-10-10'), D('2028-08-10')); ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1,4,7,10])); ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
ax.xaxis.set_minor_locator(mdates.MonthLocator()); ax.grid(axis='x', color='#EEEEEE', lw=0.5); ax.set_axisbelow(True)
ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
fig.savefig(OUT+'Fig6_timeline.png'); print('ok')
