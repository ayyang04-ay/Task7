import pandas as pd, numpy as np
import matplotlib, matplotlib.ticker
from fig_style import *
Q = pd.read_csv('quant_long.csv'); W = pd.read_csv('wt_long.csv'); Q['time']=Q['time'].astype(str)
fig, axes = plt.subplots(2, 2, figsize=(FIGW, 5.8), gridspec_kw={'wspace':0.27, 'hspace':0.6, 'left':0.08, 'right':0.99, 'top':0.955, 'bottom':0.08})
# (A) IgG2a/IgG1 ratio: as printed vs recomputed
ax = axes[0,0]
def v(b, g): return Q[(Q.block==b)&(Q.group==g)].sort_values('rep').value.values
rec = {g: v('S13-A', g)/v('S13-B', g) for g in ['PSLN-212','PSLN-344','PSLN-212(Y)']}
pr = {g: v('S03-B', g) for g in ['PSLN-212','PSLN-344','PSLN-212(Y)']}
xs = {'PSLN-212':0,'PSLN-344':1,'PSLN-212(Y)':2}
for g in xs:
    ax.plot([xs[g]-0.17]*5, pr[g], 'o', mfc='white', mec=COL[g], ms=4.2); ax.plot([xs[g]-0.28, xs[g]-0.06], [np.exp(np.log(pr[g]).mean())]*2, color=COL[g], lw=1.5, ls='--')
    ax.plot([xs[g]+0.17]*5, rec[g], 'o', color=COL[g], ms=4.2); ax.plot([xs[g]+0.06, xs[g]+0.28], [np.exp(np.log(rec[g]).mean())]*2, color=COL[g], lw=1.5)
ax.axhline(1, color='#999999', lw=0.8, ls=':'); ax.set_yscale('log'); ax.set_yticks([0.25,0.5,1,2,4]); ax.set_yticklabels(['0.25','0.5','1','2','4']); ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_xticks([0,1,2]); ax.set_xticklabels(['Aged +\nPSLN-212','Aged +\nPSLN-344','Young +\nPSLN-212']); ax.set_ylabel('IgG2a : IgG1, anti-H1N1 (log scale)')
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([0],[0], marker='o', mfc='white', mec='k', lw=0, label='as printed under this label (S03-B)'), Line2D([0],[0], marker='o', color='k', lw=0, label='recomputed from raw titers (S13-A ÷ S13-B)')], frameon=False, fontsize=6.2, loc='upper center', bbox_to_anchor=(0.46,-0.19), ncol=1, handletextpad=0.2)
ax.set_title('A  S03-B column labels are rotated', loc='left', fontweight='bold')
# (B) S09-A panel 2 vs S01-A 72h
ax = axes[0,1]
mp = {'PBS':'Sham','CMP-204':'CMP-204','PSLN-212':'PSLN-212','PSLN-R848':'PSLN-R848','PSLN-212/R848':'PSLN-212/R848','PSLN-344':'PSLN-344','PSLN-212(y)':'PSLN-212(Y)'}
for panel, t, mk, lab in [('panel1(A-U)','16h','s','first panel vs S01-A 16 h'), ('panel2(X-AS)','72h','o','second panel (labeled “16h”) vs S01-A 72 h')]:
    X=[]; Y=[]
    for g9, g1 in mp.items():
        a = 10**Q[(Q.block=='S09-A')&(Q.analyte.str.startswith('Ifnb1'))&(Q.group==g9)&(Q.time==panel)].sort_values('rep').value.values
        b = Q[(Q.block=='S01-A')&(Q.group==g1)&(Q.time==t)].value.values
        for x in a:
            j = np.argmin(np.abs(b-x)); X.append(b[j]); Y.append(x)
    ax.plot(X, Y, mk, ms=3.6, alpha=0.8, label=f"{lab}: 21/21 identical", color='#1F5FA8' if t=='72h' else '#999999')
ax.plot([0.5,60],[0.5,60], color='k', lw=0.7, ls='--'); ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlabel('S01-A Ifnb1, fold (stored linear)'); ax.set_ylabel('S09-A Ifnb1, back-transformed'); ax.legend(frameon=False, fontsize=6.0, loc='upper left', handletextpad=0.2, borderaxespad=0.1)
ax.set_title('B  Second S09-A panel is the 72-h data', loc='left', fontweight='bold')
# (C) S15-C PSLN-344 vs S15-I Vaccine+PSLN-344
ax = axes[1,0]
a = W[(W.block=='S15-C')&(W.group=='PSLN-344')]; b = W[(W.block=='S15-I')&(W.group=='3d Vaccine+PSLN-344')]
for an in range(1,8):
    x = a[a.animal==an]; y = b[b.animal==an]
    ax.plot(x.day, x.value, '-', color='#1F5FA8', lw=2.6, alpha=0.35, label='S15-C PSLN-344 (challenge day 14)' if an==1 else None)
    ax.plot(y.day, y.value, '--', color='k', lw=0.8, label='S15-I Vaccine+PSLN-344 (challenge day 3)' if an==1 else None)
ax.set_xlabel('Days after challenge'); ax.set_ylabel('Body weight, % of day 0'); ax.legend(frameon=False, fontsize=6.2, loc='lower left', borderaxespad=0.1)
ax.set_ylim(75.5, 105)
ax.plot([14],[90.1], 'o', mfc='none', mec='#C0392B', ms=9, mew=1.0)
ax.text(2.6, 103.6, 'circled: 77.9 → 90.1 in S15-C; flat (dead) in S15-I', fontsize=6, color='#C0392B', va='center')
ax.set_title('C  S15-C and S15-I share 40 of 42 weights', loc='left', fontweight='bold')
# (D) S11-A vs S11-B
ax = axes[1,1]
a = Q[Q.block=='S11-A'].set_index(['group','time','rep']).value; b = Q[Q.block=='S11-B'].set_index(['group','time','rep']).value
df = pd.concat([a.rename('AM'), b.rename('Neut')], axis=1).reset_index(); same = df.AM==df.Neut
ax.plot(df.AM[~same], df.Neut[~same], 'o', color='#BBBBBB', ms=3.2, label=f'different value (n={int((~same).sum())})')
ax.plot(df.AM[same], df.Neut[same], 'o', color='#C0392B', ms=3.8, label=f'identical, same cell position (n={int(same.sum())} of 100)')
ax.plot([15,55],[15,55], color='k', lw=0.7, ls='--'); ax.set_xlabel('S11-A “alveolar macrophages”, %'); ax.set_ylabel('S11-B “neutrophils”, %')
ax.legend(frameon=False, fontsize=6.2, loc='upper left', handletextpad=0.2, borderaxespad=0.1); ax.set_title('D  Neutrophil block is not independent', loc='left', fontweight='bold')
fig.savefig(OUT+'FigA1_data_integrity_examples.png'); print('ok')
