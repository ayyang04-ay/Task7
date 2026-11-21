import numpy as np, pandas as pd
from figstyle import *
from statlib import *
from matplotlib.colors import LinearSegmentedColormap
import matplotlib as mpl
sv = pd.read_csv('stats_survival_groups.csv')
def get(b,g):
    r = sv[(sv.block==b)&(sv.group==g)]
    if len(r)==0: return None
    r = r.iloc[0]; return int(r.survivors), int(r.n)
rows = [
 ('AGED BALB/c (≥20 months): challenge 2–3 days after the single dose', None),
 ('S03-J   H5N1 vaccine → wild-type H5N1, day 2', dict(b='S03-J', flag='Q11, Q12')),
 ('S06-B   H3N2 vaccine → H1N1 (PR8), day 3', dict(b='S06-B')),
 ('S06-D   H1N1+H3N2 vaccine → rgH5N1, day 3', dict(b='S06-D', flag='Q03, Q10')),
 ('S15-H   H1N1+H3N2 vaccine → rgH5N1, day 3', dict(b='S15-H', special=True)),
 ('AGED BALB/c: challenge at day 14', None),
 ('S03-I   H1N1+H3N2 vaccine → H1N1 (CA09, matched), day 14', dict(b='S03-I', flag='Q10, Q11')),
 ('S06-A   H3N2 vaccine → H1N1 (PR8), day 14', dict(b='S06-A')),
 ('S06-C   H1N1+H3N2 vaccine → rgH5N1, day 14', dict(b='S06-C', flag='Q03, Q05')),
 ('AGED BALB/c: challenge at day 60', None),
 ('S06-E   H3N2 vaccine → H1N1 (PR8), day 60', dict(b='S06-E', flag='Q10, Q20')),
 ('S06-F   H1N1+H3N2 vaccine → rgH5N1, day 60', dict(b='S06-F', flag='Q20')),
 ('S06-G   H1N1 vaccine → H3N2 (Perth), day 60', dict(b='S06-G', flag='Q10, Q20')),
 ('OTHER STRAINS, aged 20 months (challenge virus not stated)', None),
 ('S15-L   C57BL/6', dict(b='S15-L', flag='Q06, Q10')),
 ('S15-N   Swiss Webster', dict(b='S15-N', flag='Q07')),
 ('MIDDLE-AGED BALB/c (14 months), with or without prior PR8 infection', None),
 ('S06-E2  no prior infection → H1N1 (PR8)', dict(b='S06-E2', pre='Naïve+')),
 ('S06-E2  prior infection → H1N1 (PR8)', dict(b='S06-E2', pre='Imprinting+')),
 ('S06-F2  no prior infection → H3N2 (Perth), day 14', dict(b='S06-F2', pre='Naïve+')),
 ('S06-F2  prior infection → H3N2 (Perth), day 14', dict(b='S06-F2', pre='Imprinting+')),
 ('YOUNG BALB/c (7–8 weeks)', None),
 ('S13-E   H1N1+H3N2 vaccine → H1N1 (CA09, matched), day 14', dict(b='S13-E', young=True, flag='Q12')),
 ('S09-B   H3N2 vaccine → H1N1 (PR8), day 21', dict(b='S09-B', young=True)),
 ('S09-D   H1N1 vaccine → H3N2 (Perth), day 21', dict(b='S09-D', young=True)),
 ('S09-F   H1N1+H3N2 vaccine → rgH5N1, day 180', dict(b='S09-F', young=True, flag='Q12')),
]
cols = ['Empty\nliposome','PSLN-212','PSLN-344','PSLN-212\n(young)','PSLN-344\n(young)']
cmap = LinearSegmentedColormap.from_list('s', ['#f2f2f2','#c6dbef','#6baed6','#2171b5','#08306b'])
fig, ax = plt.subplots(figsize=(7.3, 7.9))
n = len(rows); X0 = -5.9; ax.set_xlim(X0, 6.15); ax.set_ylim(n+0.1, -1.75)
ax.text(2.5, -1.62, 'Adjuvant given with the vaccine', ha='center', va='bottom', fontsize=7.2, color='#444')
for j,c in enumerate(cols): ax.text(j+0.5, -0.25, c, ha='center', va='bottom', fontsize=7, fontweight='bold', linespacing=1.05)
ax.text(5.15, -0.25, 'Data-quality\nflag (App. A)', ha='left', va='bottom', fontsize=6.6, color='#a33', linespacing=1.05)
def cell(j, i, k, nn, note=None):
    f = k/nn
    ax.add_patch(plt.Rectangle((j+0.04, i+0.07), 0.92, 0.86, color=cmap(f), lw=0))
    ax.text(j+0.5, i+0.5, f'{k}/{nn}' + (f'\n{note}' if note else ''), ha='center', va='center', fontsize=7.6 if not note else 6.0, color='white' if f>0.55 else 'black',
            fontweight='bold' if not note else 'normal', linespacing=0.95)
for i,(lab, spec) in enumerate(rows):
    if spec is None:
        ax.text(X0+0.02, i+0.58, lab, fontsize=7.0, fontweight='bold', va='center', color='#222'); ax.plot([X0+0.02, 5.0],[i+0.98,i+0.98], color='#999', lw=0.5); continue
    ax.text(X0+0.12, i+0.5, lab, fontsize=6.9, va='center')
    b = spec['b']
    if spec.get('special'):
        k,nn = get(b,'3d Vaccine'); cell(0,i,k,nn,'vaccine alone')
        k,nn = get(b,'3d Vaccine+PSLN-344'); cell(2,i,k,nn)
        k,nn = get(b,'3d PSLN-344'); ax.text(3.06, i+0.5, f'PSLN-344 alone,\nno vaccine: {k}/{nn}', fontsize=6.6, va='center', color='#a33', fontweight='bold', linespacing=1.0)
    elif spec.get('pre'):
        for j,g in [(1,'PSLN-212'),(2,'PSLN-344')]:
            k,nn = get(b, spec['pre']+g); cell(j,i,k,nn)
    elif spec.get('young'):
        k,nn = get(b,'Sham'); cell(0,i,k,nn,'young')
        for j,g in [(3,'PSLN-212Y'),(4,'PSLN-344Y'),(4,'PSLN-344(Y)')]:
            r = get(b,g)
            if r: cell(j,i,*r)
        if b=='S13-E':
            k,nn = get(b,'CMP-204(Y)'); ax.text(3.5, i+0.5, f'CMP-204\n(cGAMP): {k}/{nn}', fontsize=5.8, va='center', ha='center', linespacing=1.0)
    else:
        for j,g in enumerate(['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']):
            r = get(b,g)
            if r: cell(j,i,*r)
    if spec.get('flag'): ax.text(5.15, i+0.5, spec['flag'], fontsize=6.6, va='center', color='#a33')
ax.axis('off')
cax = fig.add_axes([0.735, 0.968, 0.2, 0.011]); cb = mpl.colorbar.ColorbarBase(cax, cmap=cmap, orientation='horizontal', norm=mpl.colors.Normalize(0,100))
cb.set_ticks([0,50,100]); cb.ax.tick_params(labelsize=6, length=2, pad=1); cax.set_title('% surviving', fontsize=6.5, pad=2, fontweight='normal', loc='center')
fig.subplots_adjust(left=0.005, right=0.995, top=0.93, bottom=0.005)
fig.savefig(OUT+'fig1_survival_by_experiment.png'); print('ok')
