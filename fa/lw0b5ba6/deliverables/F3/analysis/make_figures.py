"""Figures for the committee proposal, drawn at their printed size (fonts are true point sizes on the page).
Every plotted number is read from the CSVs produced by the analysis scripts."""
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from statsmodels.stats.proportion import proportion_confint
import warnings; warnings.filterwarnings('ignore')
plt.rcParams.update({'font.size':7.5,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':300,'savefig.bbox':'tight','savefig.pad_inches':0.03,'font.family':'DejaVu Sans',
                     'axes.linewidth':0.6,'xtick.major.width':0.6,'ytick.major.width':0.6,'axes.labelsize':7.5,'xtick.labelsize':7,'ytick.labelsize':7})
OUT='/tmp/outputs/figures/'
COL={'Sham':'#8c8c8c','PSLN-212':'#e08a1e','PSLN-344':'#1f5fa8','PSLN-212(Y)':'#3a9d5d','Untreated':'#222222','CMP-204':'#9467bd'}
LAB={'Sham':'Aged, vaccine + empty liposome ("Sham")','PSLN-212':'Aged, vaccine + PSLN-212 (no manganese)','PSLN-344':'Aged, vaccine + PSLN-344','PSLN-212(Y)':'Young, vaccine + PSLN-212','Untreated':'Aged, untreated, not challenged'}
per=pd.read_csv('survival_per_experiment.csv'); d=pd.read_csv('tidy_all_observations.csv')

# ------------------------------------------------ Fig 1: survival by experiment (6.5 in wide) -------------
order=[('S03-I','E01  Same-strain H1N1, 10x LD50, day 14','b'),('S03-J','E02  Wild-type H5N1, day 2','b'),('S06-A','E03  H3N2 vaccine, H1N1 challenge, day 14',''),('S06-B','E04  H3N2 vaccine, H1N1 challenge, day 3',''),
       ('S06-C','E05  H1+H3 vaccine, H5N1 challenge, day 14','a'),('S06-D','E06  H1+H3 vaccine, H5N1 challenge, day 3','c'),('S06-E(r34)','E07  H3N2 vaccine, H1N1 challenge, day 60','c'),('S06-F(r34)','E08  H1+H3 vaccine, H5N1 challenge, day 60',''),
       ('S06-G','E09  H1N1 vaccine, H3N2 challenge, day 60','c'),('S15-L','E13  C57BL/6, 20 months',''),('S15-N','E14  Swiss Webster, 20 months','')]
fig=plt.figure(figsize=(6.5,3.95)); ax=fig.add_axes([0.385,0.19,0.585,0.70])
for i,(b,lab,flag) in enumerate(order):
    y=len(order)-i
    for k,arm in enumerate(['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']):
        r=per[(per.block==b)&(per.arm==arm)]
        if len(r)==0: continue
        r=r.iloc[0]; yy=y+0.3-0.2*k
        ax.plot([r.ci_lo,r.ci_hi],[yy,yy],color=COL[arm],lw=0.8,alpha=.75); ax.plot(r.surv_pct,yy,'o',color=COL[arm],ms=3.3,zorder=3)
    r3=per[(per.block==b)&(per.arm=='PSLN-344')].iloc[0]; r2=per[(per.block==b)&(per.arm=='PSLN-212')].iloc[0]
    ax.text(104,y+0.2,f'{int(r2.survivors)}/{int(r2.n)}',va='center',fontsize=6.0,color=COL['PSLN-212']); ax.text(104,y-0.22,f'{int(r3.survivors)}/{int(r3.n)}',va='center',fontsize=6.0,color=COL['PSLN-344'])
    ax.text(-3,y,lab+(f'  [{flag}]' if flag else ''),ha='right',va='center',fontsize=6.8); ax.axhline(y-0.5,color='#eeeeee',lw=.5)
pool=pd.read_csv('survival_pooled.csv').iloc[1]
for k,(arm,txt) in enumerate([('PSLN-212',pool.arm2_surv),('PSLN-344',pool.arm1_surv)]):
    kk,nn=map(int,txt.split('/')); lo,hi=proportion_confint(kk,nn,method='beta'); yy=0.2-0.4*k
    ax.plot([100*lo,100*hi],[yy,yy],color=COL[arm],lw=1.8); ax.plot(100*kk/nn,yy,'D',color=COL[arm],ms=5); ax.text(104,yy,txt,va='center',fontsize=6.6,color=COL[arm],fontweight='bold')
ax.text(-3,0,'Pooled, E05 excluded',ha='right',va='center',fontsize=7.2,fontweight='bold')
ax.set_xlim(-2,114); ax.set_ylim(-0.7,len(order)+0.7); ax.set_yticks([]); ax.spines['left'].set_visible(False); ax.set_xlabel('Survival at end of observation (%), exact 95% CI'); ax.set_xticks([0,25,50,75,100])
h=[plt.Line2D([],[],marker='o',ls='',ms=4,color=COL[a],label=LAB[a]) for a in ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']]
fig.legend(handles=h,loc='upper center',bbox_to_anchor=(0.5,1.0),ncol=2,frameon=False,fontsize=6.8,columnspacing=1.2,handletextpad=0.3)
fig.text(0.01,0.075,'[a] survival table identical to E06 in all four arms; excluded from pooling.   [b] comparator arms do not reconcile with the paired body-weight table;\nthe PSLN-344 arm agrees.   [c] the paired body-weight table implies a different death count in at least one arm.\nNumbers at right: survivors / animals for PSLN-212 (upper) and PSLN-344 (lower).',fontsize=5.9,va='top',linespacing=1.4)
fig.savefig(OUT+'fig1_survival_by_experiment.png'); plt.close(fig)

# ------------------------------------------------ Fig 2: pooled KM (6.5 in) -------------------------------
s=d[d.kind=='survival'].copy(); s=s[s.time.notna()]; s['time']=s.time.astype(float); s['event']=s.event.astype(int)
early=['S03-I','S06-A','S06-B','S06-D','S15-L','S15-N']; late=['S06-E(r34)','S06-F(r34)','S06-G']
fig,axs=plt.subplots(1,2,figsize=(6.5,2.75),sharey=True)
for ax,blocks,title,arms in [(axs[0],early,'A  Challenge 3 to 14 days after one dose\n    (E01, E03, E04, E06, E13, E14)',['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']),
                             (axs[1],late,'B  Challenge 60 days after one dose\n    (E07, E08, E09)',['Sham','PSLN-212','PSLN-344','PSLN-212(Y)','Untreated'])]:
    for arm in arms:
        x=s[s.block.isin(blocks)&(s.group.str.strip()==arm)]
        km=KaplanMeierFitter().fit(x.time,x.event,label=f'{LAB[arm]} (n={len(x)})')
        km.plot_survival_function(ax=ax,ci_show=(arm in('PSLN-344','PSLN-212')),color=COL[arm],lw=1.4,ls=('--' if arm=='Untreated' else '-'),ci_alpha=0.12)
    ax.set_ylim(-0.02,1.03); ax.set_xlim(0,14.3); ax.set_xlabel('Days after challenge'); ax.set_title(title,fontsize=7.5,loc='left')
    ax.legend(frameon=False,fontsize=6.4,loc='upper center',bbox_to_anchor=(0.5,-0.22),ncol=1,handlelength=1.6)
axs[0].set_ylabel('Fraction surviving'); fig.subplots_adjust(wspace=0.12)
fig.savefig(OUT+'fig2_pooled_kaplan_meier.png'); plt.close(fig)

# ------------------------------------------------ Fig 3: share of age gap closed (5.3 in) ------------------
R=pd.read_csv('immunology_restoration_index.csv')
sel=[('S01-A/16h','Lung Ifnb1, 16 h','Innate'),('S01-F','Lung cDC1, 72 h','Dendritic cells'),('S02-A','Lung CCR7+ migratory DC','Dendritic cells'),('S02-C','Antigen+ DC in lymph node','Dendritic cells'),('S02-D CD40','CD40 on lymph-node DC','Dendritic cells'),('S02-D CD86','CD86 on lymph-node DC','Dendritic cells'),
     ('S02-E','DC priming of CD8 (ex vivo)','Dendritic cells'),('S04-A/ICOShi','ICOS-high Tfh','Follicular / B'),('S04-B Foxp3','Tfr (lower is better)','Follicular / B'),('S03-K','Germinal-centre B cells','Follicular / B'),
     ('S03-A','IgG to H1N1','Antibody'),('S03-C','HAI to H1N1','Antibody'),('S03-D','Neutralising to H1N1','Antibody'),('S03-G','HAI to H3N2','Antibody'),('S03-H','Neutralising to H3N2','Antibody'),
     ('IgG2a/IgG1 anti-H1N1 RECOMPUTED from S13-A / S13-B','IgG2a/IgG1 (recomputed)','Antibody'),
     ('S05-D','Lung Ki-67+ CD8, day 3','CD8 T cells'),('S05-E','Lung GZMB+ CD8, day 3','CD8 T cells'),('S05-F','IFN-g+ CD8 to H5N1, day 14','CD8 T cells'),('S05-G','IFN-g+ CD8 to H5N1, day 60','CD8 T cells'),('S05-I','Lung resident-memory CD8, day 25','CD8 T cells')]
cc={'Innate':'#6a51a3','Dendritic cells':'#2b8cbe','Follicular / B':'#41ab5d','Antibody':'#d95f0e','CD8 T cells':'#c51b7d'}
fig,ax=plt.subplots(figsize=(5.3,4.2))
for i,(blk,lab,cat) in enumerate(sel):
    r=R[R.block==blk].iloc[0]; y=len(sel)-i
    ax.barh(y,r.restoration_pct,color=cc[cat],height=.62,alpha=.9); ax.plot([r.boot_lo,r.boot_hi],[y,y],color='k',lw=.7)
    ax.text(-3,y,lab,ha='right',va='center',fontsize=6.8); ax.text(max(r.boot_hi,r.restoration_pct)+3,y,f'{r.restoration_pct:.0f}%',va='center',fontsize=6.3)
ax.axvline(100,color='k',ls=':',lw=.7); ax.axvline(0,color='k',lw=.5); ax.set_yticks([]); ax.spines['left'].set_visible(False); ax.set_xlim(0,178)
ax.set_xlabel('Share of the age gap closed by PSLN-344 (%)\n0% = aged + PSLN-212;  100% = young + PSLN-212;  lines = bootstrap 95% CI')
ax.legend(handles=[plt.Rectangle((0,0),1,1,color=c,label=k) for k,c in cc.items()],frameon=False,fontsize=6.5,loc='upper right')
fig.savefig(OUT+'fig3_restoration_of_aged_response.png'); plt.close(fig)

# ------------------------------------------------ Fig 4: tolerability (6.77 in) ----------------------------
fig,axs=plt.subplots(1,3,figsize=(6.77,2.95),gridspec_kw={'width_ratios':[1.0,1.2,0.95]})
x=d[d.block=='S08-D'].copy(); x['t']=x.time.astype(float); ax=axs[0]
cs={'Vaccine':'#8c8c8c','PSLN-212(Y)':'#3a9d5d','PSLN-212':'#e08a1e','PSLN-344':'#1f5fa8','CMP-204':'#9467bd','PSLN-212/R848':'#c0392b'}
nm={'Vaccine':'Vaccine alone','PSLN-212(Y)':'PSLN-212, young','PSLN-212':'PSLN-212','PSLN-344':'PSLN-344','CMP-204':'CMP-204','PSLN-212/R848':'PSLN-212/R848'}
for g in ['Vaccine','PSLN-212(Y)','CMP-204','PSLN-212','PSLN-344','PSLN-212/R848']:
    a=x[x.group.str.strip()==g].groupby('t').value.agg(['mean','std'])
    ax.errorbar(a.index,a['mean'],yerr=a['std'],color=cs[g],marker='o',ms=2.2,lw=(1.6 if g=='PSLN-344' else 1.0),capsize=1.5,elinewidth=.6,label=nm[g])
ax.axhline(95,color='k',ls=':',lw=.5); ax.set_xlabel('Days after intranasal vaccination'); ax.set_ylabel('Body weight (% of day 0), mean ± SD'); ax.set_ylim(83.5,103); ax.legend(frameon=False,fontsize=5.8,loc='upper center',bbox_to_anchor=(0.5,-0.2),ncol=2,handlelength=1.4,labelspacing=0.25,columnspacing=1.0); ax.set_title('A  Weight after vaccination (S08-D)',fontsize=7.2,loc='left')
cy=pd.read_csv('safety_cytokines.csv'); ax=axs[1]
an=['Ifnb1','Il6','Tnf','Il10','Ccl2']; gl=[('PSLN-212(y)','#3a9d5d','Young, PSLN-212'),('PSLN-212','#e08a1e','Aged, PSLN-212'),('PSLN-344','#1f5fa8','Aged, PSLN-344')]
w=0.13
for j,(pan,hatch) in enumerate([('16 h',''),('72 h','////')]):
    for k,(g,c,l) in enumerate(gl):
        v=[cy[(cy.panel.str.startswith(pan))&(cy.analyte==a)&(cy.group==g)].geo_fold.iloc[0] for a in an]
        ax.bar(np.arange(len(an))+(k-1)*2*w+(j-0.5)*w,v,width=w,color=c,alpha=(1 if j==0 else .5),hatch=hatch,edgecolor='white',lw=.2,label=f'{l}, {pan}')
ax.set_yscale('log'); ax.axhline(1,color='k',lw=.5); ax.set_xticks(range(len(an))); ax.set_xticklabels(an,style='italic'); ax.set_ylabel('Lung mRNA, fold vs untreated'); ax.set_ylim(0.05,3000)
ax.legend(frameon=False,fontsize=5.8,ncol=2,loc='upper center',bbox_to_anchor=(0.5,-0.13),handlelength=1.2,columnspacing=1.0,labelspacing=0.25); ax.set_title('B  Lung cytokines, 16 h and 72 h (S09-A)',fontsize=7.2,loc='left')
cn=pd.read_csv('safety_cns.csv'); ax=axs[2]
gc={'PBS':'#c9c9c9','Sham':'#8c8c8c','PSLN-344':'#1f5fa8','CT':'#c0392b'}
for k,g in enumerate(['PBS','Sham','PSLN-344','CT']):
    a=cn[cn.group==g].set_index('analyte').loc[['Ifnb1','Tnf','Isg15']]
    ax.bar(np.arange(3)+(k-1.5)*0.2,a['mean'],yerr=a['sd'],width=0.2,color=gc[g],capsize=1.2,label={'CT':'Vaccine + cholera toxin','Sham':'Vaccine + empty liposome','PBS':'Buffer','PSLN-344':'Vaccine + PSLN-344'}[g],error_kw={'lw':.6})
ax.set_xticks(range(3)); ax.set_xticklabels(['Ifnb1','Tnf','Isg15'],style='italic'); ax.set_ylabel('CNS mRNA at 36 h, fold (mean ± SD)')
ax.legend(frameon=False,fontsize=5.8,loc='upper center',bbox_to_anchor=(0.5,-0.13),ncol=1,handlelength=1.2,labelspacing=0.25); ax.set_ylim(0,7.2); ax.set_title('C  CNS transcripts (S10-A)',fontsize=7.2,loc='left')
fig.tight_layout(w_pad=0.8); fig.savefig(OUT+'fig4_safety.png'); plt.close(fig)

# ------------------------------------------------ Fig 5: dose response (3.35 in) ---------------------------
F=pd.read_csv('dose_response_fit.csv').set_index('group'); x=d[d.block=='S08-A'].copy(); x['dose']=x.time.astype(float)
fig,ax=plt.subplots(figsize=(3.35,2.6)); Dg=np.linspace(0.7,45,300)
cs={'CMP-204':'#9467bd','PSLN-212':'#e08a1e','PSLN-344':'#1f5fa8','PSLN-344/R848':'#c0392b'}
for g in ['PSLN-344','PSLN-344/R848','PSLN-212','CMP-204']:
    a=x[x.group.str.strip()==g]; p=F.loc[g]
    ax.plot(a.dose,a.value,'o',color=cs[g],ms=2.4,alpha=.8); ax.plot(Dg,1+p.Emax_fold*Dg**p.hill/(p.ED50_ug**p.hill+Dg**p.hill),color=cs[g],lw=1.2,label=f'{g}: max {p.Emax_fold:.0f}x, half-max {p.ED50_ug:.0f} µg')
ax.axvline(20,color='k',ls=':',lw=.6); ax.text(21.5,19.5,'dose used in all\nefficacy studies',fontsize=5.6,va='center')
ax.set_xscale('log'); ax.set_xticks([1,5,10,20,40]); ax.set_xticklabels(['1','5','10','20','40']); ax.set_xlabel('Intranasal dose (µg per animal)'); ax.set_ylabel('Lung Ifnb1 at 16 h (fold vs untreated)'); ax.legend(frameon=False,fontsize=5.8,loc='upper left',handlelength=1.3,labelspacing=0.25)
fig.savefig(OUT+'fig5_dose_response.png'); plt.close(fig)

# ------------------------------------------------ Supplementary: onset / durability bars -------------------
W=pd.read_csv('survival_by_window.csv'); W=W[W.window.isin(['d2-3','d14 excl. S06-C','d60'])]
fig,ax=plt.subplots(figsize=(4.6,2.9)); wins=['d2-3','d14 excl. S06-C','d60']; names=['Challenge 2-3 days\nafter one dose','Challenge at\nday 14','Challenge at\nday 60']
for k,arm in enumerate(['Sham','PSLN-212','PSLN-344','PSLN-212(Y)','Untreated']):
    for i,wn in enumerate(wins):
        r=W[(W.window==wn)&(W.arm==arm)]
        if len(r)==0: continue
        r=r.iloc[0]; kk,nn=map(int,r.surv.split('/')); lo,hi=proportion_confint(kk,nn,method='beta'); xx=i+(k-2)*0.16
        ax.bar(xx,r.pct,width=0.15,color=('white' if arm=='Untreated' else COL[arm]),edgecolor=(COL[arm] if arm=='Untreated' else 'none'),hatch=('///' if arm=='Untreated' else None),lw=.6,label=(LAB[arm] if i==2 else None)); ax.plot([xx,xx],[100*lo,100*hi],color='k',lw=.6); ax.text(xx,100*hi+3,r.surv,ha='center',fontsize=5.2,rotation=90)
ax.set_xticks(range(3)); ax.set_xticklabels(names,fontsize=6.8); ax.set_ylabel('Survival (%), exact 95% CI'); ax.set_ylim(0,130); ax.set_yticks([0,25,50,75,100]); ax.legend(frameon=False,fontsize=5.8,loc='lower center',bbox_to_anchor=(0.5,1.0),ncol=2)
fig.savefig(OUT+'supp_onset_and_durability.png'); plt.close(fig)
print('figures written')
