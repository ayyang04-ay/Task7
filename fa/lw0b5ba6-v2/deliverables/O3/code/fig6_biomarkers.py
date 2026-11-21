import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
R=pd.read_csv('/tmp/work/h2h_344_vs_212.csv'); R=R[R.tier!='C']
P=pd.read_csv('/tmp/work/s09a_panel.csv')
# time (hours) per readout
T={'S01-A_16h':16,'S01-A_72h':72,'S02-F':None,'S01-D':96,'S01-E':96,'S01-F':72,'S02-A':72,'S02-B':72,'S02-C':36,'S02-D_CD40':72,'S02-D_CD86':72,'S02-E':72,
   'S11-E':None,'S04-A_ICOShi':168,'S04-B_Tfr':168,'S04-C':720,'S04-D':168,'S03-K':168,'S03-L_Aicda':120,'S03-L_E47':120,'S13-H':None,
   'S03-A':336,'S03-E':336,'S03-C':336,'S03-G':336,'S03-D':336,'S03-H':336,'S13-A':336,'S13-C':336,'S13-B':336,'S13-D':336,'S13-I':672,'S13-J':672,
   'S05-D':72,'S05-E':72,'S05-F':336,'S05-G':1440,'S05-H':1440,'S05-I':600,'S14-A_H1N1':None,'S14-A_H3N2':None}
rows=[]
for _,r in R.iterrows():
    t=T.get(r.block)
    if r.block=='S02-F': t={'Lung Gm-csf 16h (fold)':16,'Lung Gm-csf 36h (fold)':36,'Lung Gm-csf 72h (fold)':72}[r.readout]
    if t is None: continue
    g=abs(r.hedges_g); rows.append((t,g,r.readout.split(' (')[0],r.domain,r.p_holm_welch<0.05))
col={'Innate':'#7b3294','Myeloid/DC':'#c2a5cf','Tfh/GC':'#008837','Humoral':'#1f78b4','CD8 T cell':'#e66101'}
fig,ax=plt.subplots(figsize=(15,8))
rng=np.random.default_rng(3)
for t,g,lab,dom,sig in rows:
    x=t*np.exp(rng.normal(0,0.06))
    ax.scatter(x,g,s=60,color=col[dom],edgecolor='k' if sig else 'none',zorder=3)
    ax.text(x*1.04,g,lab,fontsize=7,va='center')
# add S09-A chemokines (n=3) as hollow markers - compute g from csv not available; annotate fold instead
ax.set_xscale('log'); ax.set_xticks([16,36,72,120,168,336,600,720,1440]); ax.set_xticklabels(['16 h','36 h','72 h','d5','d7','d14','d25','d30','d60'])
ax.set_xlabel('time after intranasal vaccination'); ax.set_ylabel("|Hedges' g|, aged PSLN-344 vs aged PSLN-212 (black edge = Holm p<0.05)")
ax.set_title('Biomarker cascade: readouts that separate PSLN-344 from PSLN-212 in aged mice, by time of measurement\n'
             'Earliest strong separators (16-36 h): lung Ifnb1 (2.2x), Gm-csf (4.2-5.4x), Ccl2 (77x, S09-A n=3) -> candidate pharmacodynamic markers',fontsize=10)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=c,label=d) for d,c in col.items()],fontsize=8,loc='upper right')
ax.axvspan(12,45,color='#f2f0f7',zorder=0); ax.text(13,0.3,'PD window\n(nasal lining fluid /\nblood ISG in humans)',fontsize=8,color='#54278f')
ax.axvspan(100,200,color='#e5f5e0',zorder=0); ax.text(102,0.3,'mechanism window\n(cTfh, plasmablasts)',fontsize=8,color='#006d2c')
ax.axvspan(300,1600,color='#deebf7',zorder=0); ax.text(320,0.3,'efficacy-surrogate window (HAI, MN,\nIFN-g ELISpot; nasal TRM)',fontsize=8,color='#08519c')
ax.set_ylim(0,9); plt.tight_layout(); plt.savefig('/tmp/outputs/figures/Fig6_biomarker_cascade.png',dpi=150); print('ok')
