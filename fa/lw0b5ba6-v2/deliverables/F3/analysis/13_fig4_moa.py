"""Figure 4 - mechanism of action assembled from the workbook; each step carries its own numbers and evidence type."""
import json, numpy as np
from figstyle import *
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
B = json.load(open('/tmp/work/parsed/parsed_blocks.json'))
G = lambda b: B[b]['groups']
def gm(v): return float(np.exp(np.mean(np.log(v))))
m = lambda b, k: float(np.mean(G(b)[k]))
tcm = lambda b, k, t: float(np.mean(G(b)[k][t]))
tcg = lambda b, k, t: gm(G(b)[k][t])
def hai(b, k): return gm([5 if x == 0 else x for x in G(b)[k]])
A3 = ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']
N = {}
N['did'] = (m('S01-C', 'WT'), m('S01-C', 'SPA/D')); N['srb'] = (m('S01-B', 'AECII/PSLN-SRB'), m('S01-B', 'AECII/FreeSRB')); N['cbx'] = (m('S11-C', 'CBX-'), m('S11-C', 'CBX+'))
N['ifn'] = tuple(gm(G('S01-A_16h')[k]) for k in A3)
N['gmcsf'] = (tcg('S02-F', 'PSLN-212', '36h'), tcg('S02-F', 'PSLN-344', '36h'))
N['ccl2'] = tuple(10 ** float(np.mean(G('S09-A_panel1')[k]['Ccl2'])) for k in ['PSLN-212', 'PSLN-344', 'PSLN-212(y)'])
N['mono'] = tuple(tcm('S01-D', k, '4') for k in A3); N['dc'] = tuple(tcm('S01-E', k, '4') for k in A3)
N['mac'] = (tcm('S07-A', 'PSLN-212', '5'), tcm('S07-A', 'PSLN-344', '5'))
N['incb'] = (m('S07-B_mono', 'PSLN-344'), m('S07-B_mono', 'PSLN-344+INCB3344'))
N['ifnar'] = (m('S02-H', 'WT w/o cDC'), m('S02-H', 'IFN w/o cDC'), m('S02-H', 'GMCSF'))
for key, blk in [('ccr7', 'S02-A'), ('ova', 'S02-C'), ('oti', 'S02-E'), ('cd40', 'S02-D_CD40'), ('cd86', 'S02-D_CD86'), ('tfh', 'S04-A_ICOShi'), ('tfr', 'S04-B_Foxp3'),
                 ('gc', 'S03-K'), ('ki67', 'S05-D'), ('ifng', 'S05-F'), ('trm', 'S05-I')]:
    N[key] = tuple(m(blk, k) for k in A3)
N['ptx'] = (m('S05-C', 'MLN'), m('S05-C', 'MLN+PTX'))
N['hai'] = tuple(hai('S03-C', k) for k in A3)
N['sub'] = tuple(gm([a / b for a, b in zip(G('S13-A')[k], G('S13-B')[k])]) for k in A3)
N['gzmb_incb'] = (m('S02-I', 'PSLN-344(Y)'), m('S02-I', 'PSLN-344(Y)+INCB3344'))
json.dump(N, open('/tmp/work/parsed/moa_numbers.json', 'w'), indent=1)
t3 = lambda k, f='{:.1f}', u='': f"{f.format(N[k][0])} → {f.format(N[k][1])} ({f.format(N[k][2])}){u}"

CI = '#E8F1F8'; CE = '#0072B2'; CC = '#FFF4E5'; CCe = '#C77700'
W_IN = 9.0; MARG = 0.12
steps = [
 dict(title='1  Delivery to the deep lung', kind='I',
      what=['The surfactant-mimetic liposome is taken up by alveolar macrophages (needs surfactant proteins A and D). Its cargo then',
            'reaches the alveolar epithelium, and blocking gap junctions blunts the downstream response.'],
      data=[f"liposome-positive alveolar macrophages: {N['did'][0]:.0f}% in wild-type vs {N['did'][1]:.0f}% in SP-A/D-knockout mice  [S01-C]",
            f"dye-positive type II epithelial cells:  {N['srb'][0]:.1f}% with liposomal dye vs {N['srb'][1]:.1f}% with free dye  [S01-B]",
            f"gap-junction blocker (carbenoxolone):   recruited monocytes {N['cbx'][0]:.1f}% → {N['cbx'][1]:.1f}%  [S11-C]"]),
 dict(title='2  Innate trigger: type I interferon, GM-CSF, chemokines', kind='C',
      what=['Aging more than halves the interferon response to the STING agonist. The Mn²⁺-containing particle restores it to the',
            'young level and switches on GM-CSF.'],
      data=[f"Ifnb1, 16 h:   {t3('ifn', u='-fold')}  [S01-A]",
            f"Gm-csf, 36 h:  {N['gmcsf'][0]:.1f} → {N['gmcsf'][1]:.1f}-fold (no young arm)  [S02-F]",
            f"Ccl2, 16 h:    {N['ccl2'][0]:.0f} → {N['ccl2'][1]:.0f} ({N['ccl2'][2]:,.0f})-fold  [S09-A]"]),
 dict(title='3  Monocyte recruitment and fate', kind='I',
      what=['Monocytes enter through CCR2. Interferon-receptor signaling plus GM-CSF turns them into CD11b⁺ dendritic cells.',
            'When those signals are weak (aged + PSLN-212) they accumulate as Ly6C⁺CCR2⁺ macrophages instead.'],
      data=[f"lung monocytes, day 4:            {t3('mono', u='%')}  [S01-D]",
            f"lung CD11b+ dendritic cells, d4:  {t3('dc', u='%')}  [S01-E]",
            f"Ly6C+CCR2+ macrophages, day 5:    {N['mac'][0]:.1f} → {N['mac'][1]:.1f} ×10⁵ cells (n = 3, no young arm)  [S07-A]",
            f"CCR2 antagonist:                  monocytes {N['incb'][0]:.1f}% → {N['incb'][1]:.1f}%  [S07-B]",
            f"interferon-receptor-deficient marrow: monocyte-derived DC {N['ifnar'][0]:.1f}% → {N['ifnar'][1]:.1f}%; recombinant GM-CSF rescues to {N['ifnar'][2]:.1f}%  [S02-H]"]),
 dict(title='4  Migration to the lymph node and T-cell priming', kind='I',
      what=['CCR7⁺ dendritic cells carry antigen to the mediastinal node and prime T cells; blocking cell migration with pertussis',
            'toxin stops this. Co-stimulatory molecules are the weak point: they stay far below the young benchmark.'],
      data=[f"CCR7+ lung dendritic cells, 72 h:    {t3('ccr7', u='%')}  [S02-A]",
            f"antigen-carrying DC in node, 36 h:   {t3('ova', u='%')}  [S02-C]",
            f"CD8 cross-priming by node DC:        {t3('oti', u='%')}  [S02-E]",
            f"pertussis toxin:                     T-cell proliferation in node {N['ptx'][0]:.0f}% → {N['ptx'][1]:.0f}% (n = 3)  [S05-C]",
            f"CD40+ / CD86+ node DC, day 3:        {t3('cd40', u='%')}  /  {t3('cd86', u='%')}  [S02-D]"]),
]
split = [
 dict(title='5a  Antibody arm', kind='C',
      what=['More follicular helper and fewer follicular regulatory', 'T cells, larger germinal centers, and neutralizing', 'antibody with an IgG2a bias.'],
      data=[f"ICOS-high Tfh, d7:  {t3('tfh', u='%')}  [S04-A]", f"Tfr share, d7:      {t3('tfr', u='%')}  [S04-B]", f"GC B cells, d7:     {t3('gc', u='%')}  [S03-K]",
            f"HAI H1N1, d14:      {t3('hai', '{:.0f}')}  [S03-C]", f"IgG2a:IgG1, H1N1:   {t3('sub', '{:.2f}')}  [S13-A/B]"]),
 dict(title='5b  CD8 T-cell arm', kind='C',
      what=['Proliferating, cross-reactive CD8 T cells and', 'lung-resident memory; the effector response', 'depends on monocyte influx.'],
      data=[f"Ki-67+ lung CD8, d3:       {t3('ki67', u='%')}  [S05-D]", f"H5N1-cross-reactive IFN-γ+: {t3('ifng', u='%')}  [S05-F]",
            f"lung resident memory, d25: {t3('trm', u='%')}  [S05-I]", f"CCR2 antagonist (young):   granzyme B+ CD8", f"                           {N['gzmb_incb'][0]:.1f}% → {N['gzmb_incb'][1]:.1f}%  [S02-I]"]),
]
LT, LW, LD, PAD, GAP, ARR = 0.215, 0.165, 0.152, 0.11, 0.07, 0.26
def bh(s): return PAD + LT + len(s['what']) * LW + GAP + len(s['data']) * LD + PAD
H_title = 0.62; H_out = 0.92; H_leg = 1.05
total = H_title + sum(bh(s) + ARR for s in steps) + max(bh(s) for s in split) + ARR + H_out + H_leg
fig = plt.figure(figsize=(W_IN, total)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W_IN); ax.set_ylim(0, total); ax.axis('off')
def draw(s, x, ytop, w):
    h = bh(s); fc, ec = (CI, CE) if s['kind'] == 'I' else (CC, CCe)
    ax.add_patch(FancyBboxPatch((x, ytop - h), w, h, boxstyle='round,pad=0,rounding_size=0.09', fc=fc, ec=ec, lw=1.3, zorder=2))
    y = ytop - PAD
    ax.text(x + 0.12, y - LT / 2, s['title'], fontsize=9.8, fontweight='bold', va='center', ha='left', zorder=3); y -= LT
    for ln in s['what']:
        ax.text(x + 0.12, y - LW / 2, ln, fontsize=8.3, va='center', ha='left', zorder=3, color='#222222'); y -= LW
    y -= GAP
    for ln in s['data']:
        ax.text(x + 0.12, y - LD / 2, ln, fontsize=7.6, va='center', ha='left', zorder=3, family='DejaVu Sans Mono', color='#111111'); y -= LD
    return h
def arr(x0, y0, x1, y1):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='-|>', mutation_scale=13, lw=1.5, color='#555555', zorder=1))
y = total - 0.16
ax.text(MARG, y, 'Mechanism of action reconstructed from the PSLN workbook', fontsize=11.4, fontweight='bold', va='top')
ax.text(MARG, y - 0.27, 'Numbers read:  aged + PSLN-212  →  aged + PSLN-344  (young + PSLN-212 benchmark). Group means; block IDs in brackets.', fontsize=8.3, va='top', color='#333333')
y = total - H_title
for i, s in enumerate(steps):
    h = draw(s, MARG, y, W_IN - 2 * MARG); y -= h
    if i < len(steps) - 1:
        arr(W_IN / 2, y - 0.02, W_IN / 2, y - ARR + 0.02); y -= ARR
wh = (W_IN - 2 * MARG - 0.2) / 2
arr(W_IN * 0.30, y - 0.02, W_IN * 0.27, y - ARR + 0.02); arr(W_IN * 0.70, y - 0.02, W_IN * 0.73, y - ARR + 0.02); y -= ARR
hs = max(bh(s) for s in split)
for s, x in zip(split, [MARG, MARG + wh + 0.2]):
    s2 = dict(s); s2['data'] = s['data'] + [''] * int(round((hs - bh(s)) / LD)); draw(s2, x, y, wh)
y -= hs
arr(W_IN * 0.27, y - 0.02, W_IN * 0.36, y - ARR + 0.02); arr(W_IN * 0.73, y - 0.02, W_IN * 0.64, y - ARR + 0.02); y -= ARR
ax.add_patch(FancyBboxPatch((MARG, y - (H_out - 0.12)), W_IN - 2 * MARG, H_out - 0.12, boxstyle='round,pad=0,rounding_size=0.09', fc='#EAF5EF', ec='#009E73', lw=1.4, zorder=2))
ax.text(MARG + 0.12, y - 0.2, '6  Protection from lethal challenge', fontsize=9.8, fontweight='bold', ha='left', va='center', zorder=3)
ax.text(MARG + 0.12, y - 0.44, 'survival at end of observation:  14% → 85% (99%), pooled over 11 experiments  [Figure 1]', fontsize=7.6, ha='left', va='center', family='DejaVu Sans Mono', zorder=3)
ax.text(MARG + 0.12, y - 0.60, 'needs antigen and adjuvant together:  adjuvant alone 0/7, vaccine alone 0/7, both 6/7  [S15-H]', fontsize=7.6, ha='left', va='center', family='DejaVu Sans Mono', zorder=3)
y -= H_out
ax.add_patch(FancyBboxPatch((MARG, y - 0.22), 0.3, 0.16, boxstyle='round,pad=0,rounding_size=0.03', fc=CI, ec=CE, lw=1.2)); ax.text(MARG + 0.42, y - 0.14, 'step supported by an intervention experiment (knockout, inhibitor, antagonist or rescue)', fontsize=7.8, va='center')
ax.add_patch(FancyBboxPatch((MARG, y - 0.47), 0.3, 0.16, boxstyle='round,pad=0,rounding_size=0.03', fc=CC, ec=CCe, lw=1.2)); ax.text(MARG + 0.42, y - 0.39, 'step supported only by comparing formulations (association; cause not yet proven)', fontsize=7.8, va='center')
ax.text(MARG, y - 0.70, 'Not tested in the workbook: Mn²⁺ without the STING agonist; STING- or cGAS-deficient animals; whether antibody or CD8 T cells\nare required for protection; mucosal IgA; lung virus load.',
        fontsize=7.6, va='top', color='#7A1F1F', linespacing=1.3)
fig.savefig(FIGDIR + 'fig4_mechanism.png')
print('height in', round(total, 2))
