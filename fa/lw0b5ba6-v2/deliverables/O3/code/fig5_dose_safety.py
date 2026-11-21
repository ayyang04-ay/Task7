from loadcsv import *
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats
fig,axs=plt.subplots(1,3,figsize=(18,5.6))
col={'CMP-204':'#ff7f00','PSLN-212':'#1f78b4','PSLN-344':'#d7301f','PSLN-344/R848':'#6a3d9a'}
def emax(x,e0,emax,ed50,h): return e0+emax*x**h/(ed50**h+x**h)
ax=axs[0]; d=DF[DF.block=='S08-A'].copy(); d['dose']=d.dose_ug.astype(float)
for g,c in col.items():
    z=d[d.group==g]; ax.scatter(z.dose*np.exp(np.random.default_rng(0).normal(0,0.03,len(z))),z.value,color=c,s=18,alpha=.7)
    p,_=curve_fit(emax,z.dose,z.value,p0=[1,max(z.value),10,1.5],bounds=([0,0,0.1,0.3],[5,500,200,6]),maxfev=20000)
    xs=np.logspace(0,np.log10(40),100); ax.plot(xs,emax(xs,*p),color=c,label=f"{g}: Emax {p[1]:.0f}x, ED50 {p[2]:.1f} ug")
ax.set_xscale('log'); ax.set_xlabel('dose (ug adjuvant, intranasal)'); ax.set_ylabel('lung Ifnb1 fold at 16 h')
ax.axvline(20,color='grey',ls=':',lw=1); ax.text(20.5,52,'dose used in\nall efficacy studies',fontsize=7,color='grey')
ax.set_title('A. Dose-response (S08-A; n=3/dose; age not stated)\nMn2+ raises the ceiling ~3.4x; R848 co-loading lowers it',fontsize=9); ax.legend(fontsize=7.5,loc='upper left')
ax=axs[1]; d=DF[DF.block=='S08-D'].copy(); d['day']=d.day.astype(float)
c2={'Vaccine':'black','PSLN-212(Y)':'#33a02c','CMP-204':'#ff7f00','PSLN-212':'#1f78b4','PSLN-344':'#d7301f','PSLN-212/R848':'#6a3d9a'}
for g,c in c2.items():
    z=d[d.group==g].groupby('day').value.agg(['mean','std','count'])
    ax.errorbar(z.index+list(c2).index(g)*0.08,z['mean'],yerr=z['std'],color=c,marker='o',ms=4,capsize=2,label=g+(' (1 animal missing d10)' if g=='PSLN-212/R848' else ''))
ax.axhline(90,color='grey',ls=':',lw=1); ax.set_xlabel('days after intranasal vaccination (no challenge)'); ax.set_ylabel('% of day-0 body weight (mean+/-SD, n=5)')
ax.set_title('B. Reactogenicity (S08-D): PSLN-344 nadir 96.4% vs vaccine 98.2%\n(p=0.065); PSLN-212/R848 nadir 90.0%, 4/5 mice lost >=10%',fontsize=9); ax.legend(fontsize=7.5,loc='lower left')
ax=axs[2]
an=['Ifnb1','Tnf','Isg15']; gs=['PBS','Sham','PSLN-344','CT']; cc=['#bdbdbd','#969696','#d7301f','#238b45']
for i,a in enumerate(an):
    for j,g in enumerate(gs):
        x=DF[(DF.block==f'S10-A_{a}')&(DF.group==g)].value.values
        pos=i*5+j; ax.bar(pos,stats.gmean(x),color=cc[j],alpha=.8,label=(g if i==0 else None)); ax.scatter(np.full(len(x),pos),x,color='k',s=8,zorder=3)
ax.set_xticks([1.5,6.5,11.5]); ax.set_xticklabels(an); ax.set_ylabel('CNS transcript, fold vs untreated (36 h)')
ax.set_title('C. CNS inflammation 36 h after IN dosing, aged (S10-A, n=5)\nPSLN-344 vs sham: Ifnb1 1.14x (0.69-1.86); cholera toxin 5.4x',fontsize=9); ax.legend(fontsize=8)
plt.tight_layout(); plt.savefig('/tmp/outputs/figures/Fig4_dose_reactogenicity_CNS.png',dpi=150); print('ok')
