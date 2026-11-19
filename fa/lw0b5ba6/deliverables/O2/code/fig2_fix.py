import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy import stats
exec(open('fig_effects.py').read().split("# Fig 2 restoration index")[0].split("d=R[R.readout.isin(stage)]")[0])
cols={'1 Innate/PD':'#1f77b4','2 Myeloid/DC':'#9467bd','3 Tfh/GC':'#2ca02c','4 Antibody':'#d62728','5 CD8 T cell':'#ff7f0e'}
t=pd.read_csv('tidy.csv'); t['time']=t['time'].astype(str)
spec={r.readout:(r.block,r.transform) for _,r in R.iterrows()}
filt={'Lung monocytes d4 (%)':('time','4'),'Lung CD11b+ DC d4 (%)':('time','4')}
an={'Ccl2 lung 16h (log10 fold)':'Ccl2','Il6 lung 16h (log10 fold)':'Il6','Tnf lung 16h (log10 fold)':'Tnf','Ccl3 lung 16h (log10 fold)':'Ccl3','Ccl5 lung 16h (log10 fold)':'Ccl5','Il10 lung 16h (log10 fold)':'Il10'}
def vals(readout,g):
    b,tr=spec[readout]; d=t[(t.block==b)&(t.group==g)]
    if readout in filt: d=d[d[filt[readout][0]].astype(str)==filt[readout][1]]
    if readout in an: d=d[d.analyte==an[readout]]
    x=d.value.values.astype(float)
    if tr=='log':
        x=np.where(x<=0,5,x); x=np.log10(x)
    return x
rows=[]
for _,r in R[~R.restoration_index.isna()].iterrows():
    if r.readout not in stage: continue
    a=vals(r.readout,'PSLN-212'); y=vals(r.readout,'PSLN-212(Y)')
    p=stats.ttest_ind(y,a,equal_var=False).pvalue
    rows.append(dict(readout=r.readout,block=r.block,stage=stage[r.readout],RI=r.restoration_index,age_gap_p=p))
ri=pd.DataFrame(rows)
ri['included']=(ri.age_gap_p<0.05)&(ri.readout!='Ifnb1 lung 72h (fold)')  # 72h IFN: higher is not 'better' (kinetic readout)
print(ri.sort_values('RI').round(3).to_string(index=False))
ri.to_csv('fig2_data.csv',index=False)
ri=ri[ri.included].sort_values(['stage','RI'],ascending=[False,True]).reset_index(drop=True)
fig,ax=plt.subplots(figsize=(8.5,9))
ax.barh(range(len(ri)),ri.RI,color=[cols[s] for s in ri.stage])
ax.set_yticks(range(len(ri))); ax.set_yticklabels([f"{r.readout} [{r.block}]" for _,r in ri.iterrows()],fontsize=7)
ax.axvline(0,color='k',lw=0.8); ax.axvline(1,color='k',ls='--',lw=0.8)
for i,v in enumerate(ri.RI): ax.text(max(v,0)+0.02,i,f"{v:.2f}",va='center',fontsize=6.5)
ax.set_xlabel('Restoration index = (PSLN-344 aged − PSLN-212 aged) / (PSLN-212 young − PSLN-212 aged)\n0 = no better than aged PSLN-212; 1 = equal to young benchmark (log10 scale for titres/fold-changes)',fontsize=8)
ax.set_xlim(-0.05,1.2)
import matplotlib.patches as mpatches
ax.legend(handles=[mpatches.Patch(color=c,label=s[2:]) for s,c in cols.items()],fontsize=7,loc='lower right')
ax.set_title('Fig. 2  Share of the age-related deficit closed by PSLN-344\n(readouts with a significant young-vs-aged gap, Welch p<0.05)',fontsize=9)
plt.tight_layout(); plt.savefig('/tmp/outputs/figures/fig2_restoration_index.png',dpi=180)
print('median RI (included):',ri.RI.median().round(2),' n=',len(ri))
for s in ri.stage.unique(): print(s, ri[ri.stage==s].RI.median().round(2))
