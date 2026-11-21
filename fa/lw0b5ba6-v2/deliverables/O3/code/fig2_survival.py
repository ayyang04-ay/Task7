from loadcsv import *
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
SV2=SV.copy(); SV2['time']=SV2['time'].fillna(21.0)
studies=[('S06-A','B','PR8 (H1N1) het., d14'),('S06-B','B','PR8 het., d3 (early)'),('S06-C','B','rgH5N1 het., d14'),
         ('S06-E','B','PR8 het., d60'),('S06-F','B','rgH5N1 het., d60'),('S06-G','B','Perth H3N2 het., d60'),
         ('S03-I','C','CA09 homologous 10xLD50, d14'),('S03-J','C','wt VN04 H5N1, d2 (BSL-3)'),('S15-L','C','C57BL/6, challenge not stated'),('S15-N','C','Swiss Webster, challenge not stated')]
col={'Sham':'#7f7f7f','PSLN-212':'#1f78b4','PSLN-344':'#d7301f','PSLN-212(Y)':'#33a02c','CMP-204':'#ff7f00'}
fig=plt.figure(figsize=(17,12))
gs=fig.add_gridspec(3,5,height_ratios=[1,1,1.15])
for k,(s,t,lab) in enumerate(studies):
    ax=fig.add_subplot(gs[k//5,k%5])
    d=SV2[SV2.block==s]
    for g in ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']:
        x=d[d.group==g]
        if len(x)==0: continue
        km=KaplanMeierFitter().fit(x.time,x.event,label=f"{g}: alive {len(x)-x.event.sum()}/{len(x)}")
        km.plot_survival_function(ax=ax,ci_show=False,color=col[g],lw=2 if g=='PSLN-344' else 1.4)
    ax.set_title(f"{s} [tier {t}]\n{lab}",fontsize=9,color=('black' if t=='B' else '#b2182b'))
    ax.set_ylim(-0.03,1.03); ax.set_xlabel('days post-challenge',fontsize=8); ax.legend(fontsize=6.5,loc='lower left'); ax.tick_params(labelsize=7)
    if k%5==0: ax.set_ylabel('survival',fontsize=8)
# forest of per-study RR (death, 344 vs 212), Haldane correction for zero cells
ax=fig.add_subplot(gs[2,:3])
rows=[]
for s,t,lab in studies:
    d=SV2[SV2.block==s]; a=d[d.group=='PSLN-344']; b=d[d.group=='PSLN-212']
    x1,n1,x2,n2=a.event.sum(),len(a),b.event.sum(),len(b)
    if x1==0 or x2==0 or x1==n1 or x2==n2: x1c,x2c,n1c,n2c=x1+.5,x2+.5,n1+1,n2+1
    else: x1c,x2c,n1c,n2c=x1,x2,n1,n2
    rr=(x1c/n1c)/(x2c/n2c); se=np.sqrt(1/x1c-1/n1c+1/x2c-1/n2c)
    rows.append((s,t,lab,rr,np.exp(np.log(rr)-1.96*se),np.exp(np.log(rr)+1.96*se),f"{x1}/{n1} vs {x2}/{n2}"))
P=pd.read_csv('/tmp/work/survival_pooled.csv')
for i,(s,t,lab,rr,lo,hi,txt) in enumerate(rows):
    c='black' if t=='B' else '#b2182b'
    ax.errorbar(rr,-i,xerr=[[rr-lo],[hi-rr]],fmt='s',color=c,capsize=3)
    ax.text(3.2,-i,f"{s} {txt}",va='center',fontsize=8,color=c)
for j,(lab,idx) in enumerate([('Pooled, all 10 aged studies (MH)',0),('Pooled, S06 series (6 studies)',1),('Pooled, most conservative (5 studies)',2)]):
    r=P.iloc[idx]; yy=-len(rows)-0.8-j
    ax.errorbar(r.rr,yy,xerr=[[r.rr-r.lo],[r.hi-r.rr]],fmt='D',color='#d7301f',ms=8,capsize=3)
    ax.text(3.2,yy,f"{lab}: RR {r.rr:.2f} ({r.lo:.2f}-{r.hi:.2f}); {int(r.d344)}/{int(r.n344)} vs {int(r.d212)}/{int(r.n212)}",va='center',fontsize=8,color='#d7301f')
ax.axvline(1,color='k',lw=.8); ax.set_xscale('log'); ax.set_xlim(0.02,30); ax.set_yticks([])
ax.set_xlabel('Risk ratio of death, PSLN-344 vs PSLN-212 (aged), 95% CI (log scale; 0.5 added to zero cells for display only)',fontsize=8)
ax.set_title('Per-study and pooled mortality risk ratio. Black = tier B (minor inconsistencies); red = tier C (integrity flags, see Appendix)',fontsize=9)
ax2=fig.add_subplot(gs[2,3:]); ax2.axis('off')
ax2.text(0,1,("How to read: every aged study shows PSLN-344 >> PSLN-212.\n"
 "S06-D (rgH5N1, d3) is omitted: it is a row-for-row copy of S06-C.\n\n"
 "Most conservative estimate (S06-A,B,E,F,G):\n"
 f"  mortality 29% (PSLN-344) vs 94% (PSLN-212)\n"
 f"  MH risk ratio 0.30 (0.18-0.51); stratified Cox HR 0.12 (0.06-0.26)\n\n"
 "Young PSLN-212 reference: 0/42 deaths in S06 series;\n"
 "aged PSLN-344 10/42 (p=0.0011 vs young) -> restoration is\n"
 "substantial but not complete.\n\n"
 "Sham (vaccine + empty liposome): 42/42 deaths in S06 series."),va='top',fontsize=9,family='monospace')
plt.tight_layout(); plt.savefig('/tmp/outputs/figures/Fig2_survival.png',dpi=150); print('ok')
