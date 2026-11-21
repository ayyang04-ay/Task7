"""Figure 1: Kaplan-Meier grid (aged and 14-month animals).  Figure 2: pooled survival with exact CIs."""
import numpy as np, pandas as pd
from figstyle import *
from matplotlib.lines import Line2D
import tidy, survlib as S

def km(time, event, tmax):
    t = np.asarray(time, float); e = np.asarray(event, int)
    xs = [0]; ys = [1.0]; s = 1.0
    for u in np.unique(t[e == 1]):
        n = (t >= u).sum(); d = ((t == u) & (e == 1)).sum()
        xs += [u, u]; ys += [s, s * (1 - d / n)]; s *= (1 - d / n)
    xs.append(tmax); ys.append(s)
    return np.array(xs), np.array(ys) * 100

panels = [   # block, line 1, line 2, flagged?
    ('S06-A', 'H3N2 vaccine → H1N1', 'challenge day 14', False), ('S06-B', 'H3N2 vaccine → H1N1', 'challenge day 3', False),
    ('S06-C', 'H1N1+H3N2 → H5N1', 'challenge day 14', True), ('S15-H', 'H1N1+H3N2 → H5N1, day 3', 'is antigen needed?', False),
    ('S03-I', 'H1N1+H3N2 → H1N1', 'matched strain, day 14', True), ('S03-J', 'H5N1 → wild-type H5N1', 'challenge day 2', True),
    ('S06-E', 'H3N2 vaccine → H1N1', 'challenge day 60', False), ('S06-F', 'H1N1+H3N2 → H5N1', 'challenge day 60', False),
    ('S06-G', 'H1N1 vaccine → H3N2', 'challenge day 60', False), ('S15-L', 'C57BL/6, 20 months', 'challenge not stated', True),
    ('S15-N', 'Swiss Webster, 20 months', 'challenge not stated', True), ('S06-F[r71]', '14-month BALB/c', 'H1N1+H3N2 → H3N2, day 14', False)]
fig, axes = plt.subplots(3, 4, figsize=(W, 6.9))
fig.subplots_adjust(left=0.065, right=0.95, top=0.85, bottom=0.125, hspace=0.72, wspace=0.56)
offs = [0.0, -2.2, 2.2, -4.4, 4.4]
for ax, (b, l1, l2, flag) in zip(axes.ravel(), panels):
    d = S.prep(b); tmax = 21 if b == 'S03-J' else 14
    gs = list(pd.unique(d.group)); used = {}; ends = []
    for g in gs:
        s_ = d[d.group == g]; x, y = km(s_.time, s_.event, tmax)
        key = tuple(np.round(y, 3)) + tuple(x); k = used.get(key, 0); used[key] = k + 1
        ls = '--' if ('(Y)' in g or g.endswith('Y')) else (':' if g == 'Untreated' else '-')
        ax.step(x, y + offs[k], where='post', color=COL.get(g, 'k'), ls=ls, lw=1.9 if 'PSLN-344' in g and 'Imprinting' not in g and g != '3d PSLN-344' else 1.2)
        ends.append([y[-1], f"{int((s_.event == 0).sum())}/{len(s_)}", COL.get(g, 'k')])
    # survivors / animals at the right-hand end of each curve, nudged apart where curves end together
    ends.sort(key=lambda e: e[0]); pos = []
    for e in ends:
        yv = e[0] if not pos else max(e[0], pos[-1] + 11.5); pos.append(yv)
    shift = max(0, pos[-1] - 101)
    for e, yv in zip(ends, pos):
        ax.text(1.03, (yv - shift + 8) / 118, e[1], transform=ax.transAxes, fontsize=5.8, color=e[2], va='center', ha='left', fontweight='bold')
    ax.set_ylim(-8, 110); ax.set_xlim(0, tmax + 0.2); ax.set_yticks([0, 50, 100]); ax.set_xticks(range(0, tmax + 1, 7))
    ax.text(0, 1.235, f"{b.replace('[r71]', ', rows 71–105')}{'  ⚑' if flag else ''}", transform=ax.transAxes, fontsize=6.6, fontweight='bold', va='bottom', ha='left', color='#b2182b' if flag else 'black')
    ax.text(0, 1.03, f'{l1}\n{l2}', transform=ax.transAxes, fontsize=5.7, va='bottom', ha='left', linespacing=1.1)
    if b == 'S15-H':
        ax.legend(handles=[Line2D([], [], color=COL['3d Vaccine+PSLN-344'], lw=1.9, label='both'), Line2D([], [], color=COL['3d PSLN-344'], lw=1.2, label='344 only'),
                           Line2D([], [], color=COL['3d Vaccine'], lw=1.2, label='vaccine only')], frameon=False, fontsize=5.5, loc='center right', bbox_to_anchor=(1.02, 0.48), handlelength=0.9, handletextpad=0.4, borderaxespad=0)
    if b == 'S06-F[r71]':
        ax.legend(handles=[Line2D([], [], color=COL['Naive+PSLN-344'], lw=1.9, label='344 naive'), Line2D([], [], color=COL['Imprinting+PSLN-344'], lw=1.2, label='344 prior inf.'),
                           Line2D([], [], color=COL['Naive+PSLN-212'], lw=1.2, label='212 naive'), Line2D([], [], color=COL['Imprinting+PSLN-212'], lw=1.2, label='212 prior inf.')],
                  frameon=False, fontsize=5.3, loc='center right', bbox_to_anchor=(1.03, 0.48), handlelength=0.9, handletextpad=0.4, borderaxespad=0)
for ax in axes[-1]: ax.set_xlabel('Days after challenge')
for ax in axes[:, 0]: ax.set_ylabel('Survival (%)')
h = [Line2D([], [], color=COL['PSLN-344'], lw=1.9, label='PSLN-344, aged'), Line2D([], [], color=COL['PSLN-212'], lw=1.2, label='PSLN-212, aged'),
     Line2D([], [], color=COL['Sham'], lw=1.2, label='Sham (vaccine + empty liposome)'), Line2D([], [], color=COL['PSLN-212(Y)'], lw=1.2, ls='--', label='PSLN-212, young'),
     Line2D([], [], color=COL['CMP-204'], lw=1.2, label='CMP-204 (cGAMP), aged'), Line2D([], [], color='k', lw=1.2, ls=':', label='Untreated, not challenged')]
fig.legend(handles=h, loc='upper left', bbox_to_anchor=(0.055, 0.962), ncol=3, frameon=False, fontsize=6.4, columnspacing=1.6)
fig.text(0.012, 0.985, 'Figure 1. Survival after lethal challenge: one intranasal dose of vaccine with 20 µg adjuvant', fontsize=8.2, fontweight='bold', va='top')
fig.text(0.012, 0.012, 'Numbers at the right of each panel: survivors / animals, in the colour of the curve. Coincident curves are drawn slightly apart.\n'
         'In S15-H and the 14-month panel the groups differ and are named inside the panel (naive = never infected; prior inf. = recovered from influenza four months earlier).\n'
         '⚑ data-integrity flag: S06-C is identical to S06-D (Q4); S03-I and S03-J comparator labels are disputed (Q2, Q3); S15-L and S15-N share body-weight values with S06-A (Q5).',
         fontsize=5.7, va='bottom', color='#333333', linespacing=1.35)
fig.savefig('../figures/Fig1_survival_KM_grid.png'); plt.close(fig)

# ----------------------------------------------------------------------------- Figure 2 pooled (forest-style)
def pooled(blocks, g):
    k = n = 0
    for b in blocks:
        d = S.prep(b); s_ = d[d.group == g]; k += int((s_.event == 0).sum()); n += len(s_)
    lo, hi = S.cp(k, n); return k, n, 100 * k / n, 100 * lo, 100 * hi
G4 = ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']
sets = [
    ('A. Aged BALB/c, challenge 2–14 d after the dose: all six experiments as printed', ['S03-I', 'S03-J', 'S06-A', 'S06-B', 'S06-C', 'S06-D'], G4),
    ('B. Core experiments only (S06-A, S06-B, S06-C)', ['S06-A', 'S06-B', 'S06-C'], G4),
    ('C. Aged BALB/c, challenge 60 d after the dose (S06-E, S06-F, S06-G)', ['S06-E', 'S06-F', 'S06-G'], G4 + ['Untreated']),
    ('D. Aged C57BL/6 and Swiss Webster (S15-L, S15-N)', ['S15-L', 'S15-N'], G4),
    ('E. 14-month BALB/c, with or without earlier influenza infection (S06-E and S06-F at rows 71–105)', ['S06-E[r71]', 'S06-F[r71]'], ['Naive+PSLN-212', 'Imprinting+PSLN-212', 'Naive+PSLN-344', 'Imprinting+PSLN-344']),
    ('F. Young BALB/c, challenge 21–180 d after the dose (S09-B, S09-D, S09-F)', ['S09-B', 'S09-D', 'S09-F'], ['Sham', 'PSLN-212Y', 'PSLN-344Y'])]
LAB = {'Sham': 'Sham (vaccine + empty liposome)', 'PSLN-212': 'PSLN-212, aged', 'PSLN-344': 'PSLN-344, aged', 'PSLN-212(Y)': 'PSLN-212, young',
       'Untreated': 'Untreated, not challenged', 'Naive+PSLN-212': 'PSLN-212, never infected', 'Imprinting+PSLN-212': 'PSLN-212, prior infection',
       'Naive+PSLN-344': 'PSLN-344, never infected', 'Imprinting+PSLN-344': 'PSLN-344, prior infection', 'PSLN-212Y': 'PSLN-212, young', 'PSLN-344Y': 'PSLN-344, young'}
nrows = sum(len(g) + 1.5 for _, _, g in sets)
fig, ax = plt.subplots(figsize=(W, 0.192 * nrows + 0.75))
fig.subplots_adjust(left=0.29, right=0.78, top=0.955, bottom=0.075)
y = 0; yt = []; yl = []
for lab, bl, gs in sets:
    ax.text(-0.405, y, lab, fontsize=6.7, fontweight='bold', va='center', ha='left', transform=ax.get_yaxis_transform())
    y += 1.0
    for g in gs:
        bl_g = [b for b in bl if g in tidy.groups(b)]
        k, n, p, lo, hi = pooled(bl_g, g)
        ax.plot([lo, hi], [y, y], color=COL[g], lw=1.8, solid_capstyle='butt')
        ax.plot([p], [y], marker='D' if g == 'Untreated' else 'o', ms=4.6, color=COL[g], mec='k', mew=0.4)
        ax.text(1.03, y, f'{k}/{n} = {p:.0f}%  ({lo:.0f}–{hi:.0f})', va='center', fontsize=6.5, transform=ax.get_yaxis_transform())
        yt.append(y); yl.append(LAB[g]); y += 1
    y += 0.5
ax.set_yticks(yt); ax.set_yticklabels(yl, fontsize=6.5)
ax.set_ylim(y - 0.9, -0.9); ax.set_xlim(-2, 102); ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xlabel('Survival at end of observation, %  (point = estimate, bar = exact 95% confidence interval)')
for v in [0, 25, 50, 75, 100]: ax.axvline(v, color='#e6e6e6', lw=0.5, zorder=0)
ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
fig.text(0.012, 0.992, 'Figure 2. Pooled survival after lethal challenge (survivors / animals = %, 95% CI)', fontsize=8.2, fontweight='bold', va='top')
fig.savefig('../figures/Fig2_survival_pooled.png'); plt.close(fig)
print('ok')
