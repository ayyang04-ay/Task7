import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats, optimize
plt.rcParams.update({'font.size':9, 'font.family':'DejaVu Sans', 'axes.spines.top':False, 'axes.spines.right':False})
surv = pd.read_csv('survival.csv'); surv.loc[(surv.block=='S03-J') & surv.day.isna(), 'day'] = 21
surv['group']=surv.group.str.replace('Naïve','Naive')
vals = pd.read_csv('values_corrected.csv'); bw = pd.read_csv('bw.csv')
OUT='/tmp/outputs/figures/'
def wilson(k,n,z=1.96):
    p=k/n; den=1+z*z/n; c=(p+z*z/(2*n))/den; h=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den; return c-h,c+h
def newcombe(k1,n1,k0,n0):
    l1,u1=wilson(k1,n1); l0,u0=wilson(k0,n0); p1,p0=k1/n1,k0/n0; d=p1-p0
    return d, d-np.sqrt((p1-l1)**2+(u0-p0)**2), d+np.sqrt((u1-p1)**2+(p0-l0)**2)
# ---------------- Fig 1 forest ----------------
exps = [('S03-I','CA09 H1N1 10xLD50, d14 (homologous)'),('S03-J','wt VN04 H5N1, d2 [n flag]'),('S06-A','PR8 H1N1, d14'),('S06-B','PR8 H1N1, d3'),
        ('S06-C','rgH5N1, d14'),('S06-D','rgH5N1, d3 [EXACT COPY of S06-C]'),('S06-E','PR8 H1N1, d60'),('S06-F','rgH5N1, d60'),('S06-G','Perth H3N2, d60'),
        ('S15-L','C57BL/6 aged'),('S15-N','Swiss Webster aged')]
rows=[]
for b,lab in exps:
    d=surv[surv.block==b]
    k1=int((d[d.group=='PSLN-344'].event==0).sum()); n1=int((d.group=='PSLN-344').sum())
    k0=int((d[d.group=='PSLN-212'].event==0).sum()); n0=int((d.group=='PSLN-212').sum())
    rd,lo,hi=newcombe(k1,n1,k0,n0); rows.append((f'{b}  {lab}',rd,lo,hi,f'{k1}/{n1} vs {k0}/{n0}', b=='S06-D'))
pooled = pd.read_csv('/tmp/outputs/analysis/T3_pooled_survival.csv')
import re
plabels = ['POOLED A: all 11 aged expts as recorded','POOLED B: de-duplicated (S06-D removed)','POOLED C: B + worst-case body-weight reconciliation',
           'POOLED D: only expts concordant with body weights','POOLED E: 14-month animals (imprinting expts)']
for (i,r),pl in zip(pooled.iloc[:5].iterrows(), plabels):
    m = re.match(r'(-?\d+) \(95% CI (-?\d+) to (-?\d+)\)', r.MH_risk_diff_pct)
    rows.append((pl, int(m.group(1))/100, int(m.group(2))/100, int(m.group(3))/100, f'{r.arm1} vs {r.arm0}', False))
fig,ax=plt.subplots(figsize=(10.5,6.4))
y=np.arange(len(rows))[::-1]
for yi,(lab,rd,lo,hi,txt,excl) in zip(y,rows):
    col = '#999999' if excl else ('#b2182b' if lab.startswith('POOLED') else '#2166ac')
    mk = 'D' if lab.startswith('POOLED') else 's'
    ax.plot([lo,hi],[yi,yi],color=col,lw=1.6); ax.plot(rd,yi,mk,color=col,ms=6 if mk=='D' else 5)
    ax.text(1.08,yi,txt,va='center',fontsize=7.5)
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows],fontsize=7.5)
ax.axvline(0,color='k',lw=0.8); ax.set_xlim(-0.4,1.05)
ax.set_xlabel('Difference in survival, PSLN-344 minus PSLN-212 (aged animals)\nper-experiment: Newcombe 95% CI; pooled: Mantel-Haenszel 95% CI')
fig.suptitle('Figure 1. Head-to-head survival, PSLN-344 vs PSLN-212 in aged mice (source blocks S03/S06/S15; analyses T2, T3)',fontsize=9.5,x=0.01,ha='left')
ax.text(1.08,len(rows)-0.3,'survivors 344 vs 212',fontsize=7.5,weight='bold')
plt.tight_layout(); plt.savefig(OUT+'Fig1_forest_survival.png',dpi=200); plt.close()
# ---------------- Fig 2 KM small multiples ----------------
def km(t,e):
    ts=np.sort(np.unique(np.r_[0,t])); S=1.0; xs=[0]; ys=[1.0]
    for u in np.sort(np.unique(t[e==1])):
        n=(t>=u).sum(); d=((t==u)&(e==1)).sum(); xs+= [u,u]; ys += [S, S*(1-d/n)]; S*=1-d/n
    xs.append(max(14,t.max())); ys.append(S); return xs,ys
panels=[('S03-I','Homologous CA09, d14'),('S06-A','Heterosub. PR8, d14'),('S06-B','Heterosub. PR8, d3'),('S06-C','Heterosub. rgH5N1, d14'),
        ('S06-E','PR8, d60'),('S06-F','rgH5N1, d60'),('S06-G','Perth H3N2, d60'),('S15-L','C57BL/6 aged'),('S15-N','Swiss Webster aged'),
        ('S03-J','wt H5N1, d2 (n flag)'),('S15-H','Antigen + PSLN-344 both needed (d3)'),('S06-F2_imprint','14-mo, imprinting, Perth H3N2')]
colors={'Sham':'#7f7f7f','PSLN-212':'#2166ac','PSLN-344':'#b2182b','PSLN-212(Y)':'#4daf4a','Untreated':'#000000','CMP-204':'#984ea3',
        '3d Vaccine':'#7f7f7f','3d PSLN-344':'#ff7f00','3d Vaccine+PSLN-344':'#b2182b','Naive+PSLN-212':'#2166ac','Imprinting+PSLN-212':'#92c5de','Naive+PSLN-344':'#b2182b','Imprinting+PSLN-344':'#f4a582'}
fig,axs=plt.subplots(3,4,figsize=(12,8.2),sharey=True)
for ax,(b,lab) in zip(axs.flat,panels):
    d=surv[surv.block==b]
    for g in dict.fromkeys(d.group):
        t=d[d.group==g].day.values.astype(float); e=d[d.group==g].event.values
        xs,ys=km(t,e); off = {'Sham':0,'PSLN-212':0.01,'PSLN-344':0.02,'PSLN-212(Y)':0.03}.get(g,0.015)
        ax.step(xs,np.array(ys)+off*0,where='post',color=colors.get(g,'#333'),lw=1.5,label=f'{g} ({int((e==0).sum())}/{len(e)})')
    ax.set_title(f'{b}: {lab}',fontsize=8.5); ax.set_ylim(-0.03,1.05); ax.legend(fontsize=6.2,frameon=False,loc='lower left')
for ax in axs[-1]: ax.set_xlabel('days after challenge')
for ax in axs[:,0]: ax.set_ylabel('survival')
fig.suptitle('Figure 2. Kaplan-Meier survival by experiment (aged unless stated; PSLN-212(Y) = young reference). S06-D omitted (identical to S06-C).',fontsize=10,x=0.01,ha='left')
plt.tight_layout(); plt.savefig(OUT+'Fig2_KM_panels.png',dpi=180); plt.close()
# ---------------- Fig 3 restoration index ----------------
ri = pd.read_csv('/tmp/outputs/analysis/T11_restoration_index.csv')
fig,ax=plt.subplots(figsize=(9.5,8))
y=np.arange(len(ri))[::-1]
s = ri.iloc[0]
ax.axvspan(s.ci_lo,s.ci_hi,color='#fddbc7',alpha=0.7,label='survival restoration index 95% CI')
for yi,(_,r) in zip(y,ri.iterrows()):
    col='#b2182b' if r.readout.startswith('Survival') else ('#555555' if r.restoration_index<0.5 else '#2166ac')
    ax.plot([r.ci_lo,r.ci_hi],[yi,yi],color=col,lw=1.5); ax.plot(r.restoration_index,yi,'o',color=col,ms=5)
ax.set_yticks(y); ax.set_yticklabels([f"{r.readout} [{r.source}]" for _,r in ri.iterrows()],fontsize=7.2)
ax.axvline(0,color='k',lw=0.8); ax.axvline(1,color='k',lw=0.8,ls='--')
ax.set_xlabel('Restoration index = (aged PSLN-344 - aged PSLN-212) / (young PSLN-212 - aged PSLN-212)\n0 = no better than PSLN-212 in aged mice; 1 = fully restored to young level\n(log scale for titres/fold-changes; bootstrap 95% CI; grey = less than half restored)',fontsize=8)
ax.set_xlim(-0.2,1.6); ax.legend(fontsize=7.5,loc='lower right',frameon=False)
fig.suptitle('Figure 3. How much of the age-related deficit does PSLN-344 repair? (analysis T11)',fontsize=9.5,x=0.01,ha='left')
plt.tight_layout(); plt.savefig(OUT+'Fig3_restoration_index.png',dpi=200); plt.close()
# ---------------- Fig 4 integrity exhibits ----------------
fig,axs=plt.subplots(1,3,figsize=(13,4.2))
A=vals[vals.block=='S11-A'].copy(); B=vals[vals.block=='S11-B'].copy()
A['rep']=A.groupby(['group','time']).cumcount(); B['rep']=B.groupby(['group','time']).cumcount()
m=A.merge(B,on=['group','time','rep'],suffixes=('_am','_ne'))
ax=axs[0]
for rep,mk,c in [(0,'o','#b2182b'),(1,'s','#ef8a62'),(2,'^','#67a9cf'),(3,'v','#2166ac'),(4,'D','#999999')]:
    x=m[m.rep==rep]; ax.scatter(x.value_am,x.value_ne,marker=mk,color=c,s=18,label=f'replicate column {rep+1}')
ax.plot([10,55],[10,55],'k--',lw=0.7); ax.set_xlabel('S11-A alveolar macrophages (%)'); ax.set_ylabel('S11-B neutrophils (%)')
ax.set_title('(a) S11-A vs S11-B: 35/100 positions identical\n(permutation null max 19/100)',fontsize=8.5); ax.legend(fontsize=6.5,frameon=False)
ax=axs[1]
for blk,ls,c,lab in [('S09-E','-','#2166ac','S09-E col X: young BALB/c, PSLN-344Y, Perth H3N2'),('S15-M','--','#b2182b','S15-M col I: C57BL/6 PSLN-212(Y)')]:
    col = 'X' if blk=='S09-E' else 'I'
    x=bw[(bw.block==blk)&(bw.col==col)]; ax.plot(x.day,x.value,ls,marker='o',color=c,label=lab,ms=4)
ax.set_xlabel('day'); ax.set_ylabel('% of day-0 weight'); ax.legend(fontsize=6.5,frameon=False)
ax.set_title('(b) Same 8-10 digit weight values in two different experiments:\nidentical on days 2,6,8,10,12,14; day 4 differs only in the\ninteger digit (98.98780488 vs 92.98780488)',fontsize=8)
ax=axs[2]
d1=surv[surv.block=='S06-C']; d2=surv[surv.block=='S06-D']
for g,c in [('Sham','#7f7f7f'),('PSLN-212','#2166ac'),('PSLN-344','#b2182b'),('PSLN-212(Y)','#4daf4a')]:
    for dd,ls,lab in [(d1,'-','S06-C (d14)'),(d2,':','S06-D (d3)')]:
        t=dd[dd.group==g].day.values.astype(float); e=dd[dd.group==g].event.values; xs,ys=km(t,e)
        ax.step(xs,ys,where='post',color=c,ls=ls,lw=2 if ls=='-' else 1.2,label=f'{g} {lab}')
ax.set_xlabel('days after challenge'); ax.set_ylabel('survival'); ax.legend(fontsize=5.8,frameon=False,ncol=2,loc='lower left')
ax.set_title('(c) S06-C (challenge d14) and S06-D (challenge d3):\nall 28 rows x 4 groups identical (lines overlap)',fontsize=8.5)
fig.suptitle('Figure 6. Examples of data-integrity findings that must be resolved before investment (audit log A1-A17)',fontsize=10,x=0.01,ha='left')
plt.tight_layout(); plt.savefig(OUT+'Fig6_integrity_exhibits.png',dpi=200); plt.close()
# ---------------- Fig 5 dose response ----------------
d=vals[vals.block=='S08-A'].copy(); d['dose']=d.time.astype(float)
def hill(x,e0,emax,ec50,h): return e0+emax*x**h/(ec50**h+x**h)
fig,ax=plt.subplots(figsize=(5.8,4.2))
for g,c in [('CMP-204','#984ea3'),('PSLN-212','#2166ac'),('PSLN-344','#b2182b'),('PSLN-344/R848','#ff7f00')]:
    x=d[d.group==g]; ax.scatter(x.dose,x.value,color=c,s=14)
    p,_=optimize.curve_fit(hill,x.dose,x.value,p0=[1,x.value.max(),10,1.5],bounds=([0,0,0.1,0.3],[5,500,200,6]),maxfev=20000)
    xx=np.linspace(0.8,42,200); ax.plot(xx,hill(xx,*p),color=c,label=f'{g}: Emax {p[0]+p[1]:.0f}, EC50 {p[2]:.1f} ug')
ax.set_xscale('log'); ax.set_xlabel('dose per mouse (ug), intranasal'); ax.set_ylabel('lung Ifnb1, fold vs untreated (16 h)')
ax.legend(fontsize=7,frameon=False); ax.set_title('Figure 5. Dose-response (S08-A; n=3/dose; analysis T10)',fontsize=9.5,loc='left')
plt.tight_layout(); plt.savefig(OUT+'Fig5_dose_response.png',dpi=200); plt.close()
print('figures written')
