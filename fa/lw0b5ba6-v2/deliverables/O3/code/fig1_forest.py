import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
R = pd.read_csv('/tmp/work/h2h_344_vs_212.csv')
R = R[R.tier!='C'].copy()
n1,n2=R.n212,R.n344
R['se_g']=np.sqrt((n1+n2)/(n1*n2)+R.hedges_g**2/(2*(n1+n2)))
# orient so that positive = favours PSLN-344 (for suppressive readouts lower is better)
lower_better = R.readout.str.contains('Tfr|Treg|CD206')
R['g_fav'] = np.where(lower_better, -R.hedges_g, R.hedges_g)
order = ['Innate','Myeloid/DC','Tfh/GC','Humoral','CD8 T cell']
R['dom_i']=R.domain.map({d:i for i,d in enumerate(order)})
R=R.sort_values(['dom_i','g_fav'],ascending=[False,True]).reset_index(drop=True)
fig,ax=plt.subplots(1,2,figsize=(15,13),gridspec_kw={'width_ratios':[1.5,1]},sharey=True)
cols={'Innate':'#7b3294','Myeloid/DC':'#c2a5cf','Tfh/GC':'#008837','Humoral':'#1f78b4','CD8 T cell':'#e66101'}
y=np.arange(len(R))
for i,r in R.iterrows():
    c=cols[r.domain]
    sig = r.p_holm_welch<0.05
    ax[0].errorbar(r.g_fav,i,xerr=1.96*r.se_g,fmt='o' if sig else 'o',mfc=c if sig else 'white',mec=c,ecolor=c,ms=7,capsize=2)
    rp=r.restoration_pct
    if not np.isnan(rp) and abs(rp)<200:
        ax[1].barh(i,rp,color=c,alpha=0.85)
        ax[1].text(max(rp,0)+3,i,f"{rp:.0f}%",va='center',fontsize=8)
    elif not np.isnan(rp):
        ax[1].text(3,i,f"n/a (young resolves; aged stays elevated)",va='center',fontsize=7,color='grey')
    else:
        ax[1].text(3,i,'no young arm',va='center',fontsize=7,color='grey')
ax[0].axvline(0,color='k',lw=0.8)
ax[0].set_yticks(y); ax[0].set_yticklabels([f"{r.readout}  [{r.block}]" for _,r in R.iterrows()],fontsize=8)
ax[0].set_xlabel("Hedges' g, PSLN-344 vs PSLN-212 in aged mice (95% CI)\n>0 favours PSLN-344 (sign flipped for Tfr/Treg/CD206+, where lower = less suppression)")
ax[0].set_title("A. Head-to-head effect size, aged mice (n=3-5/group)\nfilled = Holm-adjusted p<0.05 across 43 readouts",fontsize=10)
ax[1].axvline(100,color='k',ls='--',lw=0.8); ax[1].axvline(0,color='k',lw=0.8)
ax[1].set_xlim(-10,150); ax[1].set_xlabel("Aged PSLN-344 response as % of the young-PSLN-212 response\n(0% = sham or aged PSLN-212 floor; 100% = young level)")
ax[1].set_title("B. Restoration toward young-adult immunity",fontsize=10)
from matplotlib.patches import Patch
ax[0].legend(handles=[Patch(color=cols[d],label=d) for d in order],loc='lower right',fontsize=8)
plt.tight_layout(); plt.savefig('/tmp/outputs/figures/Fig1_head_to_head_forest.png',dpi=160); print('ok')
