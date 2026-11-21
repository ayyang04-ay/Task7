import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from lifelines import KaplanMeierFitter
from scipy.optimize import curve_fit
plt.rcParams.update({'font.size':9,'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False})
OUT='/tmp/outputs/figures/'
COL={'Sham':'#8c8c8c','CMP-204':'#c49a6c','PSLN-212':'#3b75af','PSLN-344':'#d6452a','PSLN-212(Y)':'#2e9e5b','PSLN-344(Y)':'#16623a','Untreated':'#222222'}
S=pd.read_csv('/tmp/work/tidy/survival.csv'); S.loc[S.time.isna()&(S.event==0),'time']=21.0
P=pd.read_csv('/tmp/work/tables/survival_by_group.csv'); Q=pd.read_csv('/tmp/work/tables/survival_pooled.csv')
C=pd.read_csv('/tmp/work/tidy/continuous.csv'); C['time']=C['time'].astype(str)
C.loc[C.block.isin(['S03-C','S03-G'])&(C.value<10),'value']=5.0

# ---------- Fig 1: survival overview ----------
rows=[('S03-I','Homologous CA09, challenge d14'),('S06-A','Heterosubtypic PR8 (H3 vaccine), d14'),('S06-C','Heterosubtypic rgH5N1, d14'),
      ('S03-J','Wild-type VN04 H5N1 (rgH5 vaccine), d2'),('S06-B','Heterosubtypic PR8, d3'),
      ('S06-E(d60)','Heterosubtypic PR8, d60'),('S06-F(d60)','Heterosubtypic rgH5N1, d60'),('S06-G(d60)','Heterosubtypic Perth H3N2, d60')]
fig=plt.figure(figsize=(11.5,5.8)); ax=fig.add_axes([0.34,0.10,0.38,0.72])
groups=['Sham','PSLN-212','PSLN-344','PSLN-212(Y)','Untreated']
off={'Sham':-0.30,'PSLN-212':-0.15,'PSLN-344':0.0,'PSLN-212(Y)':0.15,'Untreated':0.30}
lab={'Sham':'Vaccine + empty liposome (Sham)','PSLN-212':'Vaccine + PSLN-212','PSLN-344':'Vaccine + PSLN-344','PSLN-212(Y)':'Young + PSLN-212 (reference)','Untreated':'Untreated, unchallenged (background)'}
handles={}
for i,(b,lb) in enumerate(rows):
    yy=len(rows)-i
    for g in groups:
        r=P[(P.block==b)&(P.group==g)]
        if len(r)==0: continue
        r=r.iloc[0]
        h=ax.errorbar(r.pct_survival,yy+off[g],xerr=[[r.pct_survival-r.cp_lo],[r.cp_hi-r.pct_survival]],fmt='o',color=COL[g],ms=4.5,capsize=0,lw=1,
                    mfc=COL[g] if g!='Untreated' else 'white',clip_on=False)
        handles[g]=h
pr=Q[Q.analysis.str.startswith('PRIMARY')].iloc[0]
pool={'Sham':(1,59),'PSLN-212':(7,59),'PSLN-344':(49,59),'PSLN-212(Y)':(49,49)}
from scipy import stats
for g,(s_,n) in pool.items():
    lo=stats.beta.ppf(.025,s_,n-s_+1) if s_>0 else 0; hi=stats.beta.ppf(.975,s_+1,n-s_) if s_<n else 1
    ax.errorbar(100*s_/n,-0.3+off[g],xerr=[[100*s_/n-100*lo],[100*hi-100*s_/n]],fmt='D',color=COL[g],ms=6,lw=1.4,clip_on=False)
ax.axhline(0.45,color='k',lw=0.6)
ax.set_xlim(0,100); ax.set_ylim(-0.9,len(rows)+0.6)
ax.set_yticks([len(rows)-i for i in range(len(rows))]+[-0.3])
ax.set_yticklabels([f"{b}   {lb}" for b,lb in rows]+['POOLED, 8 experiments (S06-D excluded)\nSham 1/59 | PSLN-212 7/59 | PSLN-344 49/59 | young 49/49'],fontsize=8)
ax.get_yticklabels()[-1].set_fontweight('bold'); ax.tick_params(axis='y',length=0)
ax.set_xlabel('Survival at end of follow-up, % (95% Clopper-Pearson CI)')
ax.spines['left'].set_visible(False)
fig.text(0.745,0.80,'PSLN-344 vs PSLN-212\n(pooled, stratified by experiment)',fontsize=8.5,fontweight='bold',va='top')
fig.text(0.745,0.70,f"Cox hazard ratio {pr.cox_HR:.3f}\n(95% CI {pr.HR_lo:.3f} to {pr.HR_hi:.3f}), p < 0.0001\n\nMantel-Haenszel risk difference\nin death {100*pr.MH_RD_death:.0f} pp ({100*pr.RD_lo:.0f} to {100*pr.RD_hi:.0f})\n\nDay-60 blocks: PSLN-344 14/21 vs\nyoung 21/21 (p = 0.009) and\nunchallenged background 17/21 (p = 0.48)",fontsize=8,va='top')
fig.legend([handles[g] for g in groups],[lab[g] for g in groups],loc='upper left',bbox_to_anchor=(0.02,0.945),ncol=5,frameon=False,fontsize=7.5,handletextpad=0.2,columnspacing=1.0)
fig.text(0.01,0.975,'Fig 1. Aged (20-month) BALB/c influenza challenge outcomes by adjuvant (n = 7-10 per arm; single intranasal vaccination)',fontsize=10,fontweight='bold')
fig.savefig(OUT+'fig1_survival_overview.png',dpi=200); plt.close()

# ---------- Fig 2: KM panels ----------
panels=[('S03-I','S03-I homologous CA09 (d14)'),('S06-A','S06-A PR8 after H3N2 vaccine (d14)'),('S06-C','S06-C rgH5N1 after bivalent (d14)'),
        ('S03-J','S03-J WT H5N1 2 d after rgH5N1 vaccine'),('S06-E(d60)','S06-E PR8 at d60 (durability)'),('S06-G(d60)','S06-G Perth H3N2 at d60 (durability)')]
fig,axs=plt.subplots(2,3,figsize=(10.5,6),sharey=True)
for ax,(b,t) in zip(axs.flat,panels):
    d=S[S.block==b]
    for g in ['Sham','CMP-204','PSLN-212','PSLN-344','PSLN-212(Y)','Untreated']:
        dd=d[d.group==g]
        if len(dd)==0: continue
        k=KaplanMeierFitter().fit(dd.time,dd.event,label=f"{g} ({int((dd.event==0).sum())}/{len(dd)})")
        k.plot_survival_function(ax=ax,ci_show=False,color=COL[g],lw=1.6,ls='--' if g=='Untreated' else '-')
    ax.set_title(t,fontsize=8.5); ax.set_xlabel('Days after challenge'); ax.set_ylim(-0.03,1.05); ax.legend(fontsize=6.5,frameon=False,loc='lower left')
axs[0,0].set_ylabel('Fraction surviving'); axs[1,0].set_ylabel('Fraction surviving')
fig.suptitle('Fig 2. Kaplan-Meier survival, representative aged-mouse experiments (log-rank results in Table 3)',x=0.01,ha='left',fontsize=10)
plt.tight_layout(); fig.savefig(OUT+'fig2_km_panels.png',dpi=200); plt.close()

# ---------- Fig 3: age-gap closure ----------
Gc=pd.read_csv('/tmp/work/tables/age_gap_curated.csv')
stcol={'1 Innate sensing':'#7b3294','2 Myeloid recruitment':'#c2a5cf','3 DC migration & priming':'#5aae61','4 Tfh / germinal centre':'#1b7837',
       '5 Antibody':'#2166ac','6 CD8 T cells':'#d6604d','7 Memory (d60)':'#b2182b'}
Gc=Gc.iloc[::-1].reset_index(drop=True)
fig,ax=plt.subplots(figsize=(8,9))
for i,r in Gc.iterrows():
    ax.barh(i,100*r.gap_closed,color=stcol[r.stage],height=0.7)
    ax.plot([100*r.lo,100*r.hi],[i,i],color='k',lw=0.8)
ax.set_yticks(range(len(Gc))); ax.set_yticklabels([f"{r.readout}  [{r.block.split(' panel')[0]}]" for _,r in Gc.iterrows()],fontsize=7)
ax.axvline(100,color='k',ls='--',lw=0.8); ax.axvline(0,color='k',lw=0.8)
med=100*Gc.gap_closed.median(); ax.axvline(med,color='grey',ls=':',lw=1)
ax.text(med+1,len(Gc)-0.3,f'median {med:.0f}%',fontsize=8,color='grey')
ax.set_xlabel('% of aged-vs-young deficit closed by Mn2+\n0% = aged PSLN-212, 100% = young PSLN-212; bars = estimate, lines = bootstrap 95% CI\n(log scale for titres and fold-changes)',fontsize=8)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=c,label=s[2:]) for s,c in stcol.items()],fontsize=7,loc='lower right',frameon=False)
ax.set_xlim(-10,160)
q1,q3=Gc.gap_closed.quantile([.25,.75])
ax.set_title(f'Fig 3. Share of the age-related deficit closed by Mn2+\n{len(Gc)} readouts, one pre-specified timepoint each; median {100*Gc.gap_closed.median():.0f}% (IQR {100*q1:.0f}-{100*q3:.0f}%)\n* S09-A cytokines come from the same animals as S01-A (DI-08)',loc='left',fontsize=9)
plt.tight_layout(); fig.savefig(OUT+'fig3_age_gap_closure.png',dpi=200); plt.close()

# ---------- Fig 4: immunogenicity ----------
pan=[('S03-C','HAI anti-CA09 H1N1 (d14)'),('S03-G','HAI anti-Aichi H3N2 (d14)'),('S03-D','Neutralising anti-CA09 (d14)'),('S03-A','Serum IgG anti-CA09 (d14)'),
     ('S04-A','ICOS-high Tfh, MLN d7 (%)'),('S05-F','IFN-g+ CD8, MLN d14 (%)'),('S05-I','Lung TRM CD8, d25 (%)'),('S13-A/B','IgG2a/IgG1 anti-CA09 (from S13-A/B)')]
fig,axs=plt.subplots(2,4,figsize=(11,5.6))
order=['Sham','CMP-204','PSLN-212','PSLN-344','PSLN-212(Y)']
rng=np.random.default_rng(3)
for ax,(b,t) in zip(axs.flat,pan):
    if b=='S13-A/B':
        a=C[C.block=='S13-A']; bb=C[C.block=='S13-B']
        d=a.merge(bb,on=['group','rep'],suffixes=('_a','_b')); d['value']=d.value_a/d.value_b
    elif b=='S04-A':
        d=C[(C.block==b)&(C.measurand.str.contains('ICOS-high'))]
    else: d=C[C.block==b]
    gl=[g for g in order if g in d.group.unique()]
    logy=b.startswith('S03') or b=='S13-A/B'
    for j,g in enumerate(gl):
        v=d[d.group==g].value.values
        ax.scatter(j+rng.uniform(-.12,.12,len(v)),v,s=14,color=COL[g],zorder=3)
        m=10**np.log10(v).mean() if logy else v.mean()
        ax.plot([j-.25,j+.25],[m,m],color='k',lw=1.5,zorder=4)
    if logy: ax.set_yscale('log')
    ax.set_xticks(range(len(gl))); ax.set_xticklabels([g.replace('PSLN-','') for g in gl],rotation=35,fontsize=7.5)
    ax.set_title(f"{t}\n[{b}]",fontsize=8)
fig.suptitle('Fig 4. Immunogenicity in aged mice (bars = geometric mean for titres/ratios, arithmetic mean for %); "212(Y)" = young reference',x=0.01,ha='left',fontsize=10)
plt.tight_layout(); fig.savefig(OUT+'fig4_immunogenicity.png',dpi=200); plt.close()

# ---------- Fig 5: dose-response ----------
DR=pd.read_csv('/tmp/work/tables/dose_response_S08A.csv')
def hill(D,E0,Emax,ED50,h): return E0+Emax*D**h/(ED50**h+D**h)
fig,ax=plt.subplots(figsize=(5.6,4))
cc={'CMP-204':COL['CMP-204'],'PSLN-212':COL['PSLN-212'],'PSLN-344':COL['PSLN-344'],'PSLN-344/R848':'#9e4fa5'}
xx=np.linspace(0.8,45,300)
for _,r in DR.iterrows():
    d=C[(C.block=='S08-A')&(C.group==r.formulation)]
    ax.scatter(d.time.astype(float)*np.exp(rng.uniform(-.05,.05,len(d))),d.value,s=14,color=cc[r.formulation])
    ax.plot(xx,hill(xx,r.E0,r.Emax,r.ED50,r.hill),color=cc[r.formulation],lw=1.4,label=f"{r.formulation}: top {r.top:.0f}x, ED50 {r.ED50:.0f} ug")
ax.set_xscale('log'); ax.set_xticks([1,5,10,20,40]); ax.set_xticklabels(['1','5','10','20','40'])
ax.set_xlabel('Intranasal dose (ug per mouse)'); ax.set_ylabel('Lung Ifnb1 at 16 h (fold vs untreated)')
ax.legend(fontsize=7,frameon=False); ax.set_title('Fig 5. Mn2+ raises the IFN-b ceiling ~3.4x [S08-A]\n(4-parameter Hill fits, n=3 per dose)',loc='left',fontsize=9.5)
plt.tight_layout(); fig.savefig(OUT+'fig5_dose_response.png',dpi=200); plt.close()

# ---------- Fig 7: safety ----------
CN=pd.read_csv('/tmp/work/tables/cns_S10A.csv'); RG=pd.read_csv('/tmp/work/tables/reactogenicity_S08D.csv')
B=pd.read_csv('/tmp/work/tidy/bodyweight.csv')
fig,axs=plt.subplots(1,2,figsize=(10,3.8))
ax=axs[0]; meas=['CNS Ifnb1 (fold)','CNS Tnf (fold)','CNS Isg15 (fold)']; gg=['PBS','Sham','PSLN-344','CT']
cg={'PBS':'#cccccc','Sham':COL['Sham'],'PSLN-344':COL['PSLN-344'],'CT':'#6a3d9a'}
w=0.2
for i,m in enumerate(meas):
    for j,g in enumerate(gg):
        r=CN[(CN.measurand==m)&(CN.group==g)].iloc[0]
        ax.bar(i+(j-1.5)*w,r['mean'],w,yerr=r['sd'],color=cg[g],capsize=2,label=g if i==0 else None)
        v=C[(C.block=='S10-A')&(C.measurand==m)&(C.group==g)].value.values
        ax.scatter(i+(j-1.5)*w+rng.uniform(-.05,.05,len(v)),v,s=6,color='k',zorder=3)
ax.set_xticks(range(3)); ax.set_xticklabels(['Ifnb1','Tnf','Isg15']); ax.set_ylabel('CNS transcript, fold vs untreated (mean +/- SD)')
ax.legend(fontsize=7,frameon=False); ax.set_title('CNS inflammation 36 h after intranasal dosing [S10-A]\nPSLN-344 vs PBS: Tukey p = 0.87 / 0.54 / 0.96; CT (positive control) p <= 0.0002',fontsize=8.5,loc='left')
ax=axs[1]
d=B[B.block=='S08-D']
for g in ['Vaccine','PSLN-212(Y)','PSLN-212','PSLN-344','CMP-204','PSLN-212/R848']:
    dd=d[d.group==g].groupby('day').value.mean()
    ax.plot(dd.index,dd.values,marker='o',ms=3,label=g,color=COL.get(g,'#9e4fa5' if 'R848' in g else '#444444'))
ax.axhline(90,color='k',ls=':',lw=0.7)
ax.set_xlabel('Days after vaccination'); ax.set_ylabel('Body weight, % of day 0 (group mean)')
ax.set_title('Reactogenicity: weight after vaccination, no challenge [S08-D]\nmean nadir PSLN-344 96.4% vs vaccine 98.2% (Tukey p=0.86);\nPSLN-212/R848 90.0% (p<0.001), one animal missing at d10',fontsize=8.5,loc='left')
ax.legend(fontsize=7,frameon=False)
fig.suptitle('Fig 7. Safety signals available in the dataset',x=0.01,ha='left',fontsize=10)
plt.tight_layout(); fig.savefig(OUT+'fig7_safety.png',dpi=200); plt.close()
print('ok')
