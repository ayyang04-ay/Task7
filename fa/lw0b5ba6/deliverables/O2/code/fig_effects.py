import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
R=pd.read_csv('continuous_results.csv')
k='PSLN-344 vs PSLN-212'
stage={'Ifnb1 lung 16h (fold)':'1 Innate/PD','Ifnb1 lung 72h (fold)':'1 Innate/PD','Ifnb1 lung 16h, 20ug dose arm of dose-response (fold)':'1 Innate/PD',
'Gm-csf lung 16h (fold)':'1 Innate/PD','Gm-csf lung 36h (fold)':'1 Innate/PD','Gm-csf lung 72h (fold)':'1 Innate/PD','Ccl2 lung 16h (log10 fold)':'1 Innate/PD',
'Il6 lung 16h (log10 fold)':'1 Innate/PD','Tnf lung 16h (log10 fold)':'1 Innate/PD','Ccl3 lung 16h (log10 fold)':'1 Innate/PD','Ccl5 lung 16h (log10 fold)':'1 Innate/PD','Il10 lung 16h (log10 fold)':'1 Innate/PD',
'Lung monocytes d4 (%)':'2 Myeloid/DC','Lung CD11b+ DC d4 (%)':'2 Myeloid/DC','Lung cDC1 72h (%)':'2 Myeloid/DC','Lung cDC2 72h (%)':'2 Myeloid/DC','CCR7+ migratory CD11b+ DC 72h (%)':'2 Myeloid/DC',
'MLN CD11b+CD103- DC 72h (%)':'2 Myeloid/DC','MLN DC antigen(AF647-OVA)+ 36h (%)':'2 Myeloid/DC','MLN CD11b+ DC CD40+ d3 (%)':'2 Myeloid/DC','MLN CD11b+ DC CD86+ d3 (%)':'2 Myeloid/DC',
'OT-I proliferation with MLN DC (%)':'2 Myeloid/DC','CD206+ lung macrophages (%)':'2 Myeloid/DC',
'GC B cells MLN d7 (%)':'3 Tfh/GC','Aicda MLN B d5 (fold)':'3 Tfh/GC','E47 MLN B d5 (fold)':'3 Tfh/GC','ICOS-hi Tfh MLN d7 (%)':'3 Tfh/GC','ICOS-lo Tfh MLN d7 (%)':'3 Tfh/GC',
'Tfr (Foxp3+ of CXCR5+ICOShi) d7 (%)':'3 Tfh/GC','Tfr d30 (%)':'3 Tfh/GC','Lung Treg d7 (%)':'3 Tfh/GC','IgG+ of B220+ MLN (%)':'3 Tfh/GC',
'IgG anti-CA09 d14 (titre)':'4 Antibody','HAI anti-CA09 d14 (titre)':'4 Antibody','Neut anti-CA09 d14 (titre)':'4 Antibody','IgG anti-Aichi d14 (titre)':'4 Antibody','HAI anti-Aichi d14 (titre)':'4 Antibody',
'Neut anti-Aichi d14 (titre)':'4 Antibody','IgG2a anti-CA09 d14 (titre)':'4 Antibody','IgG1 anti-CA09 d14 (titre)':'4 Antibody','IgG2a anti-Aichi d14 (titre)':'4 Antibody','IgG1 anti-Aichi d14 (titre)':'4 Antibody',
'IgG anti-CA09 d28 post-boost (titre)':'4 Antibody','IgG anti-Aichi d28 post-boost (titre)':'4 Antibody',
'Ki-67+ CD8 lung d3 (%)':'5 CD8 T cell','GZMB+ CD8 lung d3 (%)':'5 CD8 T cell','IFNg+ CD8 MLN d14, H5 restim (%)':'5 CD8 T cell','IFNg+ CD8 MLN d60, H5 restim (%)':'5 CD8 T cell',
'GZMB+ CD8 MLN d60 (%)':'5 CD8 T cell','Lung TRM CD8 d25 (%)':'5 CD8 T cell','IFNg+ CD8 MLN, H1N1 restim (%)':'5 CD8 T cell','IFNg+ CD8 MLN, H3N2 restim (%)':'5 CD8 T cell'}
flag={'S02-E':'MHC-restriction caveat','S09-A_blk1(B:V)':'','S11-E':'timepoint not stated','S13-H':'timepoint not stated','S14-A_H1N1':'timepoint not stated','S14-A_H3N2':'timepoint not stated'}
d=R[R.readout.isin(stage)].copy()
d['stage']=d.readout.map(stage)
d['g']=d[f'{k}|hedges_g']
n1=d['PSLN-344|n']; n2=d['PSLN-212|n']
d['se']=np.sqrt((n1+n2)/(n1*n2)+d.g**2/(2*(n1+n2)))
d['sig']=d[f'{k}|welch_p']<0.05
d=d.sort_values(['stage','g'],ascending=[False,True]).reset_index(drop=True)
fig,ax=plt.subplots(figsize=(9,13))
cols={'1 Innate/PD':'#1f77b4','2 Myeloid/DC':'#9467bd','3 Tfh/GC':'#2ca02c','4 Antibody':'#d62728','5 CD8 T cell':'#ff7f0e'}
for i,r in d.iterrows():
    c=cols[r.stage]
    ax.errorbar(r.g,i,xerr=1.96*r.se,fmt='o' if r.sig else 'o',mfc=c if r.sig else 'white',mec=c,ecolor=c,ms=6,capsize=2)
lab=[f"{r.readout}  [{r.block}]" for _,r in d.iterrows()]
ax.set_yticks(range(len(d))); ax.set_yticklabels(lab,fontsize=7)
ax.axvline(0,color='k',lw=0.8)
ax.set_xlabel("Hedges' g, PSLN-344 vs PSLN-212 in aged mice (95% CI)\n(negative = lower with PSLN-344; expected for Tfr, Treg, cDC2, CD206+ macrophages)",fontsize=8)
for s,c in cols.items(): ax.plot([],[],'o',color=c,label=s[2:])
ax.plot([],[],'o',mfc='white',mec='grey',label='not significant (Welch p≥0.05)')
ax.legend(loc='lower right',fontsize=7,frameon=True)
ax.set_title('Fig. 1  Incremental effect of Mn$^{2+}$ (PSLN-344) over the non-Mn formulation (PSLN-212)\nin aged mice, all continuous readouts (n=3–5/group per block)',fontsize=9)
ax.set_xlim(-12,14); plt.tight_layout(); plt.savefig('/tmp/outputs/figures/fig1_forest_PSLN344_vs_PSLN212.png',dpi=180)
d.to_csv('fig1_data.csv',index=False)

# Fig 2 restoration index
ri=R[~R.restoration_index.isna()&R.readout.isin(stage)].copy()
ri['stage']=ri.readout.map(stage)
ri=ri.sort_values(['stage','restoration_index'],ascending=[False,True]).reset_index(drop=True)
fig,ax=plt.subplots(figsize=(8,9))
ax.barh(range(len(ri)),ri.restoration_index,color=[cols[s] for s in ri.stage])
ax.set_yticks(range(len(ri))); ax.set_yticklabels([f"{r.readout} [{r.block}]" for _,r in ri.iterrows()],fontsize=7)
ax.axvline(0,color='k',lw=0.8); ax.axvline(1,color='k',ls='--',lw=0.8)
ax.text(1.01,len(ri)-0.5,'young\nbenchmark',fontsize=7,va='top'); ax.text(0.01,len(ri)-0.5,'aged\nPSLN-212',fontsize=7,va='top')
for i,v in enumerate(ri.restoration_index): ax.text(max(v,0)+0.02,i,f"{v:.2f}",va='center',fontsize=6.5)
ax.set_xlabel('Restoration index = (PSLN-344 aged − PSLN-212 aged) / (PSLN-212 young − PSLN-212 aged)\n(log10 scale for titres/fold-changes; 1.0 = fully restored to young benchmark)',fontsize=8)
ax.set_xlim(-0.3,1.25)
ax.set_title('Fig. 2  How much of the age-related deficit does PSLN-344 close?',fontsize=9)
plt.tight_layout(); plt.savefig('/tmp/outputs/figures/fig2_restoration_index.png',dpi=180)
ri[['readout','block','restoration_index']].to_csv('fig2_data.csv',index=False)
print(ri[['readout','restoration_index']].round(2).to_string(index=False))
