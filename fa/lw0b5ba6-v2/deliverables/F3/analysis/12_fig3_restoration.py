"""Figure 3 - how much of the age-related deficit is recovered by the Mn2+-containing formulation.
restoration = (PSLN-344 aged - PSLN-212 aged) / (PSLN-212 young - PSLN-212 aged); log scale for titers and fold-changes."""
import json, numpy as np
from figstyle import *
B = json.load(open('/tmp/work/parsed/parsed_blocks.json'))
G = lambda b: B[b]['groups']
def gm(v): return float(np.exp(np.mean(np.log(v))))
def static(bid, log=False, hai=False):
    g = G(bid); f = (lambda v: gm([5 if (x == 0 and hai) else x for x in v])) if log else (lambda v: float(np.mean(v)))
    return f(g['PSLN-212']), f(g['PSLN-344']), f(g['PSLN-212(Y)'])
def tc(bid, t):
    g = G(bid); return tuple(float(np.mean(g[k][t])) for k in ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)'])
def ratio(num, den):
    return tuple(gm([a / b for a, b in zip(G(num)[k], G(den)[k])]) for k in ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)'])
def surv():
    ids = ['S03-I', 'S06-A', 'S06-B', 'S06-C', 'S06-D', 'S06-E_r34', 'S06-F_r34', 'S06-G', 'S15-L', 'S15-N']
    out = []
    for k in ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']:
        s = sum(sum(1 for x in B[b]['groups'][k] if x['event'] == 0) for b in ids); n = sum(len(B[b]['groups'][k]) for b in ids); out.append(100 * s / n)
    return tuple(out)
rows = [
 ('Innate sensing', None),
 ('Ifnb1 mRNA, lung, 16 h  [S01-A]', static('S01-A_16h', log=True), True, '{:.1f}', '-fold'),
 ('Antigen-presenting cells', None),
 ('Lung monocytes, day 4  [S01-D]', tc('S01-D', '4'), False, '{:.1f}', '%'),
 ('Lung CD11b+ DC, day 4  [S01-E]', tc('S01-E', '4'), False, '{:.1f}', '%'),
 ('CCR7+ migratory DC, 72 h  [S02-A]', static('S02-A'), False, '{:.1f}', '%'),
 ('Antigen-carrying DC in lymph node, 36 h  [S02-C]', static('S02-C'), False, '{:.1f}', '%'),
 ('CD40+ lymph-node DC, day 3  [S02-D]', static('S02-D_CD40'), False, '{:.1f}', '%'),
 ('CD86+ lymph-node DC, day 3  [S02-D]', static('S02-D_CD86'), False, '{:.1f}', '%'),
 ('DC cross-priming of CD8 T cells, ex vivo  [S02-E]', static('S02-E'), False, '{:.1f}', '%'),
 ('T-cell help and B cells', None),
 ('ICOS-high Tfh, day 7  [S04-A]', static('S04-A_ICOShi'), False, '{:.1f}', '%'),
 ('Tfr share (lower is better), day 7  [S04-B]', static('S04-B_Foxp3'), False, '{:.1f}', '%'),
 ('Germinal-center B cells, day 7  [S03-K]', static('S03-K'), False, '{:.1f}', '%'),
 ('Antibody, day 14', None),
 ('IgG, H1N1  [S03-A]', static('S03-A', log=True), True, '{:,.0f}', ''),
 ('IgG, H3N2  [S03-E]', static('S03-E', log=True), True, '{:,.0f}', ''),
 ('HAI, H1N1  [S03-C]', static('S03-C', log=True, hai=True), True, '{:,.0f}', ''),
 ('HAI, H3N2  [S03-G]', static('S03-G', log=True, hai=True), True, '{:,.0f}', ''),
 ('Neutralizing titer, H1N1  [S03-D]', static('S03-D', log=True), True, '{:,.0f}', ''),
 ('Neutralizing titer, H3N2  [S03-H]', static('S03-H', log=True), True, '{:,.0f}', ''),
 ('IgG2a:IgG1 ratio, H1N1  [S13-A/B, recomputed]', ratio('S13-A', 'S13-B'), True, '{:.2f}', ''),
 ('CD8 T cells', None),
 ('Ki-67+ lung CD8, day 3  [S05-D]', static('S05-D'), False, '{:.1f}', '%'),
 ('Granzyme B+ lung CD8, day 3  [S05-E]', static('S05-E'), False, '{:.1f}', '%'),
 ('H5N1-cross-reactive IFN-γ+ CD8, day 14  [S05-F]', static('S05-F'), False, '{:.1f}', '%'),
 ('H5N1-cross-reactive IFN-γ+ CD8, day 60  [S05-G]', static('S05-G'), False, '{:.1f}', '%'),
 ('Lung resident-memory CD8, day 25  [S05-I]', static('S05-I'), False, '{:.1f}', '%'),
 ('Outcome', None),
 ('Survival, 10 challenge experiments with all three arms', surv(), False, '{:.0f}', '%'),
]
tiercol = {'Innate sensing': '#0072B2', 'Antigen-presenting cells': '#0072B2', 'T-cell help and B cells': '#0072B2', 'Antibody, day 14': '#0072B2', 'CD8 T cells': '#0072B2', 'Outcome': '#003B5C'}
fig, ax = plt.subplots(figsize=(8.8, 8.6))
y = 0; cur = None; out = []
for r in rows:
    if r[1] is None:
        cur = r[0]; ax.text(-3, y + 0.05, r[0], ha='right', va='center', fontsize=8.8, fontweight='bold', clip_on=False); y += 0.8; continue
    lab, (a, m, yg), log, fmt, unit = r
    f = np.log if log else (lambda v: v)
    rest = 100 * (f(m) - f(a)) / (f(yg) - f(a)); out.append((lab, a, m, yg, rest))
    ax.barh(y, 100, height=0.62, color='#EFEFEF', zorder=1)
    ax.barh(y, max(rest, 0), height=0.62, color=tiercol[cur], zorder=2, alpha=0.92 if rest >= 50 else 0.55)
    ax.text(min(rest, 100) - 2 if rest > 22 else rest + 2, y, f"{rest:.0f}%", ha='right' if rest > 22 else 'left', va='center', fontsize=7.8, color='white' if rest > 22 else '#222222', fontweight='bold', zorder=3)
    ax.text(-3, y, lab, ha='right', va='center', fontsize=7.9, clip_on=False)
    ax.text(106, y, f"{fmt.format(a)} → {fmt.format(m)}   ({fmt.format(yg)}){unit and ' ' + unit}", ha='left', va='center', fontsize=7.6, family='DejaVu Sans Mono', clip_on=False)
    y += 1
ax.axvline(100, color='#009E73', lw=1.6, ls='-', zorder=4); ax.axvline(0, color='#D55E00', lw=1.6, zorder=4)
ax.text(0, -1.25, 'PSLN-212\naged', color='#D55E00', ha='center', va='bottom', fontsize=8, fontweight='bold', clip_on=False)
ax.text(100, -1.25, 'PSLN-212\nyoung', color='#009E73', ha='center', va='bottom', fontsize=8, fontweight='bold', clip_on=False)
ax.text(106, 0.05, 'aged 212 → aged 344   (young 212)', ha='left', va='center', fontsize=7.6, fontweight='bold', family='DejaVu Sans Mono', clip_on=False)
ax.set_ylim(y - 0.3, -0.6); ax.set_xlim(0, 104); ax.set_yticks([]); ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xlabel('Share of the aged-versus-young gap closed by PSLN-344 (%)')
ax.spines['left'].set_visible(False)
fig.suptitle('How far PSLN-344 moves aged mice towards the young benchmark, step by step', x=0.01, ha='left', fontsize=10.8, fontweight='bold', y=0.992)
fig.text(0.01, 0.006, 'Gap closed = (PSLN-344 aged − PSLN-212 aged) ÷ (PSLN-212 young − PSLN-212 aged); log scale for titers, ratios and fold-changes, linear for percentages.\n'
         'Group means, n = 5 per group (7 per arm for survival; the 10 experiments are those in Figure 1 that include a young arm). Group-level comparison only:\n'
         'the animals that gave biomarker samples are not the animals that were challenged. Analysis 12_fig3_restoration.py.',
         fontsize=6.6, color='#444444', va='bottom')
fig.subplots_adjust(left=0.40, right=0.745, top=0.915, bottom=0.115)
fig.savefig(FIGDIR + 'fig3_gap_closed.png')
json.dump(out, open('/tmp/work/parsed/restoration.json', 'w'), indent=1)
for o in out: print(f"{o[0]:<58} {o[1]:>10.2f} {o[2]:>10.2f} {o[3]:>10.2f}  {o[4]:6.0f}%")
