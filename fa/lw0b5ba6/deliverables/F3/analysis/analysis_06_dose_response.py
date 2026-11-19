"""
Analysis 6 - S08-A: lung Ifnb1 at 16 h versus intranasal dose (1, 5, 10, 20, 40 ug; n=3 per dose; age of animals not stated).
Model: fold = 1 + Emax * D^h / (ED50^h + D^h), fitted on the log10 scale (multiplicative error); parametric bootstrap CIs.
Output: dose_response_fit.csv, dose_response_by_dose.csv
"""
import numpy as np, pandas as pd, warnings
from scipy.optimize import least_squares
from scipy import stats
warnings.filterwarnings('ignore')
d=pd.read_csv('tidy_all_observations.csv'); x=d[d.block=='S08-A'].copy(); x['dose']=x.time.astype(float)
def model(p,D): Emax,ED50,h=p; return 1+Emax*D**h/(ED50**h+D**h)
def fit(D,y,p0=(50,10,2)):
    r=least_squares(lambda p: np.log10(model(p,D))-np.log10(y),p0,bounds=([0.1,0.5,0.3],[500,200,8]))
    return r.x
rows=[];bd=[]
rng=np.random.default_rng(11)
for g in dict.fromkeys(x.group):
    a=x[x.group==g]; D=a.dose.values; y=a.value.values
    p=fit(D,y); res=np.log10(y)-np.log10(model(p,D)); s=res.std(ddof=3)
    bs=[]
    for _ in range(2000):
        yb=10**(np.log10(model(p,D))+rng.normal(0,s,len(D)))
        try: bs.append(fit(D,yb,p))
        except Exception: pass
    bs=np.array(bs); lo=np.percentile(bs,2.5,axis=0); hi=np.percentile(bs,97.5,axis=0)
    top=model(p,40.0); e20=model(p,20.0)
    rows.append(dict(group=g,cells=f'S08!{a.cell.iloc[0]}:{a.cell.iloc[-1]}',Emax_fold=p[0],Emax_lo=lo[0],Emax_hi=hi[0],ED50_ug=p[1],ED50_lo=lo[1],ED50_hi=hi[1],hill=p[2],hill_lo=lo[2],hill_hi=hi[2],
                     resid_sd_log10=s,pred_20ug=e20,pred_40ug=top,frac_of_plateau_at_20ug=(e20-1)/p[0]))
    for dose,b in a.groupby('dose'):
        bd.append(dict(group=g,dose_ug=dose,n=len(b),mean=b.value.mean(),sd=b.value.std(ddof=1),geo=10**np.log10(b.value).mean(),values=' '.join(f'{v:g}' for v in b.value)))
F=pd.DataFrame(rows); Bd=pd.DataFrame(bd); F.to_csv('dose_response_fit.csv',index=False); Bd.to_csv('dose_response_by_dose.csv',index=False)
pd.set_option('display.width',250); f=lambda v:f'{v:.3g}'
print(Bd.pivot(index='dose_ug',columns='group',values='mean').round(2).to_string()); print(); print(F.to_string(float_format=f))
# 20 vs 40 ug within PSLN-344; PSLN-344 vs PSLN-212 at matched doses
a=x[x.group=='PSLN-344']
print('\nPSLN-344 20 vs 40 ug (Welch on log10): p=%.3f; ratio 40/20 = %.2f'%(stats.ttest_ind(np.log10(a[a.dose==40].value),np.log10(a[a.dose==20].value),equal_var=False).pvalue, a[a.dose==40].value.mean()/a[a.dose==20].value.mean()))
for dose in [1,5,10,20,40]:
    u=np.log10(x[(x.group=='PSLN-344')&(x.dose==dose)].value); v=np.log10(x[(x.group=='PSLN-212')&(x.dose==dose)].value)
    print(f'  dose {dose:>2} ug: PSLN-344/PSLN-212 ratio = {10**(u.mean()-v.mean()):.2f}  Welch p={stats.ttest_ind(u,v,equal_var=False).pvalue:.4f}')
# dose of PSLN-344 giving the PSLN-212 20-ug response
p=F.set_index('group').loc['PSLN-344']; target=Bd[(Bd.group=='PSLN-212')&(Bd.dose_ug==20)]['mean'].iloc[0]
Dg=np.linspace(0.5,40,4000); yy=model((p.Emax_fold,p.ED50_ug,p.hill),Dg)
print(f'\nPSLN-344 dose predicted to match the PSLN-212 20-ug response ({target:.1f}-fold): {Dg[np.argmin(abs(yy-target))]:.1f} ug')
