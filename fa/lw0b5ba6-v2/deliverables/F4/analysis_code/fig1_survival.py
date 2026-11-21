import pandas as pd, numpy as np
from scipy import stats
from fig_style import *
G = pd.read_csv('surv_groups.csv'); WG = pd.read_csv('wt_group_status.csv'); PO = pd.read_csv('pooled_survival.csv')
pairs = {'S03-I':'S13-F','S06-A':'S15-A','S06-B':'S15-B','S06-C':'S15-C','S06-D':'S15-D','S06-E':'S15-E','S06-F':'S15-F','S06-G':'S15-G','S15-L':'S15-M','S15-N':'S15-O'}
blocks = [('S03-I','matched H1N1 · day 14'), ('S06-A','H3N2 vaccine → H1N1 · day 14'), ('S06-C','seasonal vaccine → H5N1 · day 14'), ('S06-B','H3N2 vaccine → H1N1 · day 3'),
          ('S06-D','seasonal → H5N1 · day 3 (copied table)'), ('S06-E','H3N2 vaccine → H1N1 · day 60'), ('S06-F','seasonal vaccine → H5N1 · day 60'), ('S06-G','H1N1 vaccine → H3N2 · day 60'),
          ('S15-L','C57BL/6 (virus not stated)'), ('S15-N','Swiss Webster (virus not stated)'), ('S03-J','wild-type H5N1 · day 2')]
def cp(k,n,a=0.05):
    lo = 0.0 if k==0 else stats.beta.ppf(a/2,k,n-k+1); hi = 1.0 if k==n else stats.beta.ppf(1-a/2,k+1,n-k); return lo,hi
def newcombe(k1,n1,k2,n2):
    def wil(k,n):
        z=1.96; p=k/n; den=1+z*z/n; c=(p+z*z/(2*n))/den; h=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den; return c-h,c+h
    p1=k1/n1; p2=k2/n2; l1,u1=wil(k1,n1); l2,u2=wil(k2,n2); d=p1-p2
    return d, d-np.sqrt((p1-l1)**2+(u2-p2)**2), d+np.sqrt((u1-p1)**2+(p2-l2)**2)
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(FIGW, 5.9), gridspec_kw={'width_ratios':[1.5,1], 'wspace':0.05, 'left':0.335, 'right':0.995, 'top':0.945, 'bottom':0.15}, sharey=True)
groups = ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']; off = {'Sham':0.30,'PSLN-212':0.10,'PSLN-344':-0.10,'PSLN-212(Y)':-0.30}
xcol = {'Sham':112,'PSLN-212':131,'PSLN-344':150,'PSLN-212(Y)':169}
ypos = {}; y = 0; yt=[]; yl=[]
for b, lab in blocks:
    ypos[b] = y; yt.append(y); yl.append(f"{b}  {lab}"); y -= 1.15
for g, t in zip(groups, ['Vacc.\nalone','PSLN\n-212','PSLN\n-344','Young']):
    ax.text(xcol[g], 0.72, t, ha='center', va='bottom', fontsize=6, color=COL[g], fontweight='bold', linespacing=0.95)
for b, lab in blocks:
    for g in groups:
        r = G[(G.block==b)&(G.group==g)]
        if len(r)==0: continue
        k, n = int(r.survivors.iloc[0]), int(r.n.iloc[0]); lo, hi = cp(k,n)
        yy = ypos[b]+off[g]
        ax.plot([100*lo,100*hi],[yy,yy], color=COL[g], lw=1.0, alpha=0.5)
        ax.plot(100*k/n, yy, 'o', color=COL[g], ms=4.6, zorder=3)
        ax.text(xcol[g], ypos[b], f"{k}/{n}", va='center', ha='center', fontsize=6.4, color=COL[g])
        if b in pairs:
            w = WG[(WG.block==pairs[b])&(WG.group==g)]
            if len(w) and (int(w.alive_d_end.iloc[0])!=k or int(w.n.iloc[0])!=n):
                ax.plot(100*int(w.alive_d_end.iloc[0])/int(w.n.iloc[0]), yy, 'D', mfc='white', mec=COL[g], ms=4.4, mew=0.9, zorder=4)
    a = G[(G.block==b)&(G.group=='PSLN-344')]; c = G[(G.block==b)&(G.group=='PSLN-212')]
    d, lo, hi = newcombe(int(a.survivors.iloc[0]), int(a.n.iloc[0]), int(c.survivors.iloc[0]), int(c.n.iloc[0]))
    ax2.plot([100*lo,100*hi],[ypos[b],ypos[b]], color='#333333', lw=1.1); ax2.plot(100*d, ypos[b], 's', color='#1F5FA8', ms=4.6)
    ax2.text(112, ypos[b], f"{100*d:+.0f} [{100*lo:+.0f}, {100*hi:+.0f}]", va='center', fontsize=6.4)
def pooled_row(label, key, yy, source='table', marker='D'):
    r = PO[(PO.label==key)&(PO.source==source)].iloc[0]
    for g in groups:
        k, n = [int(x) for x in r[g].split('/')]; lo, hi = cp(k,n)
        y2 = yy+off[g]
        ax.plot([100*lo,100*hi],[y2,y2], color=COL[g], lw=1.4, alpha=0.6); ax.plot(100*k/n, y2, marker, color=COL[g], ms=5.6, zorder=3)
        ax.text(xcol[g], yy, f"{k}/{n}", va='center', ha='center', fontsize=6.0, color=COL[g], fontweight='bold')
    ax2.plot([r['PSLN-344 vs PSLN-212 MH_lo'], r['PSLN-344 vs PSLN-212 MH_hi']],[yy,yy], color='black', lw=1.8)
    ax2.plot(r['PSLN-344 vs PSLN-212 MH_RD'], yy, marker, color='black', ms=6.5)
    ax2.text(112, yy, f"{r['PSLN-344 vs PSLN-212 MH_RD']:+.0f} [{r['PSLN-344 vs PSLN-212 MH_lo']:+.0f}, {r['PSLN-344 vs PSLN-212 MH_hi']:+.0f}]", va='center', fontsize=6.4, fontweight='bold')
    yt.append(yy); yl.append(label)
y -= 0.2
ax.axhline(y+0.7, color='k', lw=0.6); ax2.axhline(y+0.7, color='k', lw=0.6)
pooled_row('POOLED, 7 aged BALB/c experiments\nsurvival tables, S06-D excluded', 'Aged BALB/c, single dose, excluding S06-D (row-for-row duplicate of S06-C)', y)
pooled_row('POOLED, same 7 experiments\nre-derived from body-weight records', 'Aged BALB/c, excl. S06-D', y-1.15, source='weights')
ax.set_yticks(yt); ax.set_yticklabels(yl, fontsize=6.8)
ax.set_xlim(-4, 181); ax.set_xticks([0,25,50,75,100]); ax.set_xlabel('Survival, % (exact 95% CI)'); ax.xaxis.set_label_coords(0.29, -0.05)
ax.set_title('A  Survivors / n by experiment', loc='left', fontweight='bold')
ax2.axvline(0, color='grey', lw=0.7, ls='--'); ax2.set_xlim(-30, 250); ax2.set_xticks([0,50,100])
ax2.set_xlabel('Percentage points (95% CI)'); ax2.xaxis.set_label_coords(0.28, -0.05)
ax2.set_title('B  PSLN-344 − PSLN-212', loc='left', fontweight='bold')
from matplotlib.lines import Line2D
h = [Line2D([0],[0], marker='o', color=COL[g], lw=0, ms=4.6, label=LAB[g]) for g in groups] + [Line2D([0],[0], marker='D', mfc='white', mec='k', lw=0, ms=4.4, label='count implied by the paired body-weight record, where it differs')]
fig.legend(handles=h, loc='lower center', bbox_to_anchor=(0.5, 0.005), ncol=2, frameon=False, fontsize=6.8, columnspacing=1.5, handletextpad=0.4)
ax.set_ylim(y-1.9, 1.45)
fig.savefig(OUT+'Fig1_survival_by_experiment.png'); print('ok')
