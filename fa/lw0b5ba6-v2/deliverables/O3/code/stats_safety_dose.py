from loadcsv import *
import numpy as np, pandas as pd
from scipy import stats
from scipy.optimize import curve_fit
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import warnings; warnings.filterwarnings('ignore')
print("== S08-A Ifnb1 dose-response (16h, fold; n=3/dose; age not stated) ==")
d = DF[DF.block=='S08-A'].copy(); d['dose']=d.dose_ug.astype(float)
tab = d.groupby(['group','dose']).value.apply(lambda x: stats.gmean(x)).unstack().round(2)
print(tab.to_string())
def emax(x,e0,emax,ed50,h): return e0+emax*x**h/(ed50**h+x**h)
fits={}
for g in ['CMP-204','PSLN-212','PSLN-344','PSLN-344/R848']:
    x=d[d.group==g].dose.values; y=d[d.group==g].value.values
    try:
        p,cov=curve_fit(emax,x,y,p0=[1,max(y),10,1.5],bounds=([0,0,0.1,0.3],[5,500,200,6]),maxfev=20000)
        se=np.sqrt(np.diag(cov)); fits[g]=p
        print(f"  {g:14s} Emax fit: E0={p[0]:.2f}, Emax={p[1]:.1f} (SE {se[1]:.1f}), ED50={p[2]:.1f} ug (SE {se[2]:.1f}), Hill={p[3]:.2f}; ED90={p[2]*9**(1/p[3]):.1f} ug")
    except Exception as e: print(g,'fit failed',e)
for dose in [5,10,20,40]:
    a=np.log(d[(d.group=='PSLN-212')&(d.dose==dose)].value); c=np.log(d[(d.group=='PSLN-344')&(d.dose==dose)].value); r=np.log(d[(d.group=='PSLN-344/R848')&(d.dose==dose)].value)
    print(f"  dose {dose:2d} ug: 344/212 = {np.exp(c.mean()-a.mean()):.2f}x (Welch p={stats.ttest_ind(c,a,equal_var=False).pvalue:.2g}); 344+R848/344 = {np.exp(r.mean()-c.mean()):.2f}x (p={stats.ttest_ind(r,c,equal_var=False).pvalue:.2g})")
# what dose of PSLN-344 matches PSLN-212 at 20/40 ug?
p=fits['PSLN-344']; target=stats.gmean(d[(d.group=='PSLN-212')&(d.dose==40)].value)
xs=np.linspace(0.5,40,4000); ys=emax(xs,*p); print(f"  PSLN-344 dose giving the Ifnb1 response of PSLN-212 at 40 ug ({target:.1f}x): ~{xs[np.argmin(abs(ys-target))]:.1f} ug")

print("\n== S08-B encapsulation efficiency (%; n=3 batches/preparations) ==")
for g in ['CMP-204','PSLN-212','PSLN-R848','PSLN-212/R848','PSLN-344']:
    x=DF[(DF.block=='S08-B')&(DF.group==g)].value.values; print(f"  {g:14s} mean {x.mean():.1f} (SD {x.std(ddof=1):.1f}) {list(x)}")
a=DF[(DF.block=='S08-B')&(DF.group=='PSLN-212')].value.values; c=DF[(DF.block=='S08-B')&(DF.group=='PSLN-344')].value.values
print(f"  PSLN-344 vs PSLN-212: diff {c.mean()-a.mean():+.1f} pts, Welch p={stats.ttest_ind(c,a,equal_var=False).pvalue:.2f}")

print("\n== S08-D reactogenicity: body weight after IN vaccination (no challenge), per-animal nadir ==")
d = DF[DF.block=='S08-D'].copy(); d['day']=d.day.astype(float)
nad = d[d.day>0].groupby(['group','animal_col']).value.min().reset_index()
for g in ['Vaccine','PSLN-212(Y)','CMP-204','PSLN-212','PSLN-344','PSLN-212/R848']:
    x=nad[nad.group==g].value.values
    d10 = d[(d.group==g)&(d.day==10)].value
    print(f"  {g:14s} nadir mean {x.mean():5.1f}% (min {x.min():.1f}); animals with >=10% loss: {(x<=90).sum()}/{len(x)}; day-10 weights present: {len(d10)}")
vac=nad[nad.group=='Vaccine'].value.values
for g in ['PSLN-212','PSLN-344','PSLN-212/R848','CMP-204']:
    x=nad[nad.group==g].value.values
    t=stats.ttest_ind(x,vac,equal_var=False); print(f"   nadir {g} vs Vaccine: diff {x.mean()-vac.mean():+.1f} pts (Welch p={t.pvalue:.2g})")

print("\n== S10-A CNS transcripts 36h after IN vaccination (aged) ==")
for an in ['Ifnb1','Tnf','Isg15']:
    b=f'S10-A_{an}'; dd=DF[DF.block==b]
    tk = pairwise_tukeyhsd(np.log2(dd.value.values), dd.group.values)
    T = pd.DataFrame(tk._results_table.data[1:],columns=tk._results_table.data[0])
    gm = dd.groupby('group').value.apply(stats.gmean)
    s = np.log2(dd[dd.group=='Sham'].value); p344=np.log2(dd[dd.group=='PSLN-344'].value); pbs=np.log2(dd[dd.group=='PBS'].value)
    diff=p344.mean()-s.mean(); se=np.sqrt(p344.var(ddof=1)/5+s.var(ddof=1)/5); tt=stats.ttest_ind(p344,s,equal_var=False)
    q=stats.t.ppf(0.975,tt.df)
    def tp(a,b):
        r=T[((T.group1==a)&(T.group2==b))|((T.group1==b)&(T.group2==a))]; return float(r['p-adj'].iloc[0])
    print(f"  {an:6s} GM fold: PBS {gm['PBS']:.2f}, Sham {gm['Sham']:.2f}, PSLN-344 {gm['PSLN-344']:.2f}, CT {gm['CT']:.2f} | PSLN-344/Sham {2**diff:.2f}x (95% CI {2**(diff-q*se):.2f}-{2**(diff+q*se):.2f}) "
          f"Tukey p(344 vs Sham)={tp('PSLN-344','Sham'):.3f}, p(344 vs PBS)={tp('PSLN-344','PBS'):.3f}, p(CT vs Sham)={tp('CT','Sham'):.4f}")
