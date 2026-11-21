"""Figure 8: the six data-integrity findings that matter most, shown with the data themselves (drawn at printed size)."""
import numpy as np, pandas as pd
from figstyle import *
import tidy
fig, axes = plt.subplots(3, 2, figsize=(W, 8.3))
fig.subplots_adjust(left=0.085, right=0.985, top=0.915, bottom=0.115, hspace=0.60, wspace=0.27)

ax = axes[0, 0]      # Q1
gs = ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']; lab = ['PSLN-212\naged', 'PSLN-344\naged', 'PSLN-212\nyoung']
printed = [tidy.vec('S03-B', g) for g in gs]; recomputed = [tidy.vec('S13-A', g) / tidy.vec('S13-B', g) for g in gs]
for i, g in enumerate(gs):
    ax.bar(i - 0.2, printed[i].mean(), 0.38, color='#d9d9d9', edgecolor='k', lw=0.4, hatch='////', label='as printed in S03-B' if i == 0 else None)
    ax.bar(i + 0.2, recomputed[i].mean(), 0.38, color=COL[g], edgecolor='k', lw=0.4, label='recomputed: S13-A ÷ S13-B' if i == 0 else None)
    ax.scatter(np.full(5, i - 0.2) + np.linspace(-0.1, 0.1, 5), printed[i], s=3.5, color='k', zorder=3, lw=0); ax.scatter(np.full(5, i + 0.2) + np.linspace(-0.1, 0.1, 5), recomputed[i], s=3.5, color='k', zorder=3, lw=0)
ax.set_xticks(range(3)); ax.set_xticklabels(lab); ax.set_ylabel('IgG2a / IgG1 quotient, H1N1'); ax.legend(frameon=False, fontsize=5.8, loc='upper left'); ax.set_ylim(0, 6.6)
ax.set_title('a  Q1: S03-B headers are rotated one place', loc='left')

ax = axes[0, 1]      # Q2
d = tidy.get('S13-F'); s = d[d.group == 'PSLN-212']
for rep, t in s.groupby('rep'):
    t = t.sort_values('x'); flat = t.value.iloc[-1] == t.value.iloc[-2]
    ax.plot(t.x, t.value, color=COL['PSLN-212'], lw=1.0, marker='o', ms=1.8, ls=':' if flat else '-')
ax.axvspan(6, 14.3, color='#fee0d2', alpha=0.6, zorder=0)
ax.text(10.15, 103.3, 'S03-I: all 7 "PSLN-212" animals\ndead by day 6', ha='center', va='center', fontsize=5.7, color='#a50f15')
ax.text(11.6, 84.0, 'S13-F, same animals:\n7 weighed on day 8; 3 recover;\n4 flat-line (dotted)', ha='center', va='center', fontsize=5.4, linespacing=1.1)
ax.set_xlim(-0.3, 14.3); ax.set_ylim(74, 107); ax.set_xlabel('Days after challenge'); ax.set_ylabel('Body weight (% of day 0)'); ax.set_xticks(range(0, 15, 2))
ax.set_title('b  Q2: survival and weight tables disagree', loc='left')

ax = axes[1, 0]      # Q4
ax.axis('off')
rows = []
for g in ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']:
    r = []
    for b_ in ['S06-C', 'S06-D']:
        s_ = tidy.get(b_); s_ = s_[s_.group == g]; dd = sorted(s_[s_.event == 1].time.astype(int))
        r.append((' '.join(map(str, dd)) if dd else 'none') + f"  ({int((s_.event == 0).sum())}/{len(s_)})")
    rows.append([g.replace('(Y)', ' young')] + r)
tb = ax.table(cellText=rows, colLabels=['Group', 'S06-C\n(challenge day 14)', 'S06-D\n(challenge day 3)'], loc='center', cellLoc='center', colWidths=[0.26, 0.37, 0.37])
tb.auto_set_font_size(False); tb.set_fontsize(6.1); tb.scale(1, 1.75)
for (r_, c_), cell in tb.get_celld().items():
    cell.set_edgecolor('#bbbbbb'); cell.set_linewidth(0.5)
    if r_ == 0: cell.set_facecolor('#f0f0f0'); cell.set_text_props(fontweight='bold'); cell.set_height(cell.get_height() * 1.35)
ax.set_title('c  Q4: two experiments, identical in all 28 animals', loc='left')

ax = axes[1, 1]      # Q5
c = tidy.get('S15-C'); c = c[c.group == 'PSLN-344']; i_ = tidy.get('S15-I'); i_ = i_[i_.group == '3d Vaccine+PSLN-344']
for rep in range(1, 8):
    t1 = c[c.rep == rep].sort_values('x'); t2 = i_[i_.rep == rep].sort_values('x')
    ax.plot(t1.x, t1.value, color=COL['PSLN-344'], lw=2.0, alpha=0.5, label='S15-C, challenge on day 14' if rep == 1 else None)
    ax.plot(t2.x, t2.value, color='k', lw=0.6, ls='--', marker='x', ms=2.2, mew=0.5, label='S15-I, challenge on day 3' if rep == 1 else None)
ax.set_xlabel('Days after challenge'); ax.set_ylabel('Body weight (% of day 0)'); ax.legend(frameon=False, fontsize=5.8, loc='lower left'); ax.set_xticks(range(0, 15, 2)); ax.set_ylim(72, 104)
ax.set_title('d  Q5: same weights in two experiments', loc='left')

ax = axes[2, 0]      # Q6
a = tidy.get('S11-A').sort_values(['group', 'x', 'rep']); b = tidy.get('S11-B').sort_values(['group', 'x', 'rep'])
same = np.isclose(a.value.values, b.value.values)
ax.scatter(a.value.values[~same], b.value.values[~same], s=5, color='#9e9e9e', lw=0, label=f'different ({(~same).sum()})')
ax.scatter(a.value.values[same], b.value.values[same], s=9, color='#d73027', marker='D', lw=0, label=f'identical ({same.sum()} of {len(same)})', zorder=3)
ax.plot([15, 55], [15, 55], color='k', lw=0.4, ls='--')
ax.set_xlabel('S11-A "% alveolar macrophages"'); ax.set_ylabel('S11-B "% neutrophils"'); ax.legend(frameon=False, fontsize=5.8, loc='upper left')
ax.set_title('e  Q6: two cell types, identical values', loc='left')

ax = axes[2, 1]      # Q7
items = [('S01-B\ntype II', 'S01-B', 'AECII/PSLN-SRB', '#4d4d4d'), ('S01-B\ntype I', 'S01-B', 'AECI/PSLN-SRB', '#4d4d4d'),
         ('col A\n"type II"', 'S08-C', 'AECII-PSLN-SRB', '#9970ab'), ('col B\n"type II\n+Mn"', 'S08-C', 'AECII-PSLN-344-SRB', '#9970ab'),
         ('col C\n"type I"', 'S08-C', 'AECI-PSLN-SRB', '#9970ab'), ('col D\n"type I\n+Mn"', 'S08-C', 'AECI-PSLN-344-SRB', '#9970ab')]
for i, (l, b_, g, col) in enumerate(items):
    v = tidy.vec(b_, g); ax.bar(i, v.mean(), 0.7, color=col, edgecolor='k', lw=0.4, alpha=0.85); ax.scatter(np.full(5, i) + np.linspace(-0.18, 0.18, 5), v, s=3.5, color='k', zorder=3, lw=0)
    ax.text(i, v.max() + 0.8, f'{v.mean():.1f}', ha='center', fontsize=5.8)
ax.set_xticks(range(6)); ax.set_xticklabels([i[0] for i in items], fontsize=5.5); ax.set_ylabel('% tracer-positive cells'); ax.set_ylim(0, 23.5)
ax.annotate('', xy=(3, 7.3), xytext=(1, 7.3), arrowprops=dict(arrowstyle='<->', color='#d73027', lw=0.8)); ax.text(2, 7.9, 'same values', ha='center', fontsize=5.6, color='#d73027')
ax.text(3.5, 21.8, 'S08-C, headers as printed', ha='center', fontsize=5.8, color='#6a3d9a'); ax.text(0.5, 21.8, 'reference', ha='center', fontsize=5.8, color='#333333')
ax.set_title('f  Q7: S08-C headers probably out of order', loc='left')
fig.text(0.012, 0.993, 'Figure 8. The six most consequential data-integrity findings', fontsize=8.2, fontweight='bold', va='top')
fig.text(0.012, 0.968, 'Each panel shows the workbook values themselves. Q numbers refer to the table in section 10.', fontsize=6.4, color='#333333', va='top')
fig.text(0.012, 0.008, 'a: dots are animals (n = 5).  b: the seven S13-F weight traces labelled PSLN-212.  c: day of each death, with survivors / animals in brackets.\n'
         'd: PSLN-344 groups, seven animals per block; 40 of 49 values are identical.  e: each point is one animal slot (group, day, position) in the two tables.\n'
         'f: column B of S08-C (printed as type II cells with the Mn²⁺ liposome) repeats the type I column of S01-B (liposome without Mn²⁺).',
         fontsize=5.6, color='#333333', va='bottom', linespacing=1.35)
fig.savefig('../figures/Fig8_data_integrity.png'); plt.close(fig)
print('identical S11:', same.sum(), len(same))
