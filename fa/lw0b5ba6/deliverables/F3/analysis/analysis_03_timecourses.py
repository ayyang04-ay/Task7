"""
Analysis 3 - time-course blocks (terminal sampling: different animals at each timepoint).
Stated method: two-way ANOVA (group x time) with Tukey.  Added: per-timepoint Welch contrasts with Holm adjustment
inside each block, peak statistics, and Bailer AUC (mean +/- SE) for destructive sampling.
Outputs: timecourse_descriptives.csv, timecourse_anova.csv, timecourse_contrasts.csv, timecourse_auc.csv
"""
import numpy as np, pandas as pd, warnings
from scipy import stats
import statsmodels.api as sm, statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests
warnings.filterwarnings('ignore')
pd.set_option('display.width',260); pd.set_option('display.max_rows',900)
d=pd.read_csv('tidy_all_observations.csv'); d['group']=d.group.str.strip()
TC={ # block: (measurand, unit, scale, time unit)
 'S01-D':('Lung monocytes (CD11b+Ly6C+CD11c-Ly6G-)','%','linear','day'),
 'S01-E':('Lung CD11b+ DC','%','linear','day'),
 'S02-F':('Lung Gm-csf (Csf2) mRNA','fold vs untreated','log10','hour'),
 'S05-A':('Lung NP366-374 tetramer+ CD8 T (n=2 observed; stated n=3)','%','linear','day'),
 'S05-B':('MLN NP366-374 tetramer+ CD8 T (n=2 observed; stated n=3)','%','linear','day'),
 'S07-A':('Lung Ly6C+CCR2+ macrophages','x10^5 cells','log10','day'),
 'S08-A':('Lung Ifnb1 mRNA, 16 h, dose-response','fold vs untreated','log10','ug'),
 'S11-A':('Lung alveolar macrophages','%','linear','day'),
 'S11-B':('Lung neutrophils','%','linear','day'),
 'S11-D':('Lung NK cells','%','linear','day'),
}
def tnum(t):
    t=str(t); return float(t.replace('h','')) if t.endswith('h') else float(t)
DD=[];AA=[];CC=[];UU=[]
for blk,(meas,unit,scale,tu) in TC.items():
    x=d[d.block==blk].copy(); x['t']=x.time.map(tnum); x['y']=np.log10(x.value) if scale=='log10' else x.value
    for (g,t),a in x.groupby(['group','t'],sort=False):
        DD.append(dict(block=blk,measurand=meas,unit=unit,group=g,time=t,time_unit=tu,cells=f'{a.sheet.iloc[0]}!{a.cell.iloc[0]}:{a.cell.iloc[-1]}',n=len(a),
                      mean=a.value.mean(),sd=a.value.std(ddof=1),geo_mean=(10**a.y.mean() if scale=='log10' else np.nan),values=' '.join(f'{v:g}' for v in a.value)))
    # two-way ANOVA
    x['G']=x.group.astype('category'); x['T']=x.t.astype(str)
    mod=smf.ols('y ~ C(G)*C(T)',data=x).fit(); an=sm.stats.anova_lm(mod,typ=2)
    AA.append(dict(block=blk,measurand=meas,scale=scale,p_group=an.loc['C(G)','PR(>F)'],p_time=an.loc['C(T)','PR(>F)'],p_interaction=an.loc['C(G):C(T)','PR(>F)'],df_resid=int(an.loc['Residual','df'])))
    # per-timepoint contrasts
    gs=list(dict.fromkeys(x.group))
    pairs=[(a,b) for a,b in [('PSLN-344','PSLN-212'),('PSLN-344','Sham'),('PSLN-344','Vaccine'),('PSLN-344','PSLN-212(Y)'),('PSLN-344','PSLN-212Y'),('PSLN-212','Sham'),('PSLN-212','Vaccine'),
                             ('PSLN-344(Y)','PSLN-212(Y)'),('PSLN-344','CMP-204'),('PSLN-344','PSLN-344/R848')] if a in gs and b in gs]
    for a,b in pairs:
        rows=[]
        for t in sorted(x.t.unique()):
            ya=x[(x.group==a)&(x.t==t)].y.values; yb=x[(x.group==b)&(x.t==t)].y.values
            va=x[(x.group==a)&(x.t==t)].value.values; vb=x[(x.group==b)&(x.t==t)].value.values
            p=stats.ttest_ind(ya,yb,equal_var=False).pvalue if len(ya)>1 and len(yb)>1 else np.nan
            eff=(10**(ya.mean()-yb.mean()) if scale=='log10' else ya.mean()-yb.mean())
            rows.append(dict(block=blk,measurand=meas,g1=a,g2=b,time=t,time_unit=tu,mean1=va.mean(),mean2=vb.mean(),effect=('ratio' if scale=='log10' else 'difference'),estimate=eff,welch_p=p,n1=len(ya),n2=len(yb)))
        r=pd.DataFrame(rows); ok=r.welch_p.notna()
        r.loc[ok,'holm_p_within_block_pair']=multipletests(r.loc[ok,'welch_p'],method='holm')[1]
        CC.append(r)
    # Bailer AUC on raw scale
    for g in gs:
        ts=sorted(x[x.group==g].t.unique()); m=[];v=[]
        for t in ts:
            a=x[(x.group==g)&(x.t==t)].value.values; m.append(a.mean()); v.append(a.var(ddof=1)/len(a))
        ts=np.array(ts); w=np.zeros(len(ts)); w[0]=(ts[1]-ts[0])/2; w[-1]=(ts[-1]-ts[-2])/2
        for i in range(1,len(ts)-1): w[i]=(ts[i+1]-ts[i-1])/2
        auc=float((w*np.array(m)).sum()); se=float(np.sqrt((w**2*np.array(v)).sum()))
        pk=int(np.argmax(m))
        UU.append(dict(block=blk,measurand=meas,group=g,auc=auc,auc_se=se,peak_mean=m[pk],peak_time=ts[pk],time_unit=tu,baseline_mean=m[0],last_mean=m[-1],last_time=ts[-1]))
D=pd.DataFrame(DD);A=pd.DataFrame(AA);C=pd.concat(CC,ignore_index=True);U=pd.DataFrame(UU)
# AUC z-tests PSLN-344 vs PSLN-212
Z=[]
for blk in U.block.unique():
    u=U[U.block==blk].set_index('group')
    for a,b in [('PSLN-344','PSLN-212'),('PSLN-344','PSLN-212(Y)'),('PSLN-344','PSLN-212Y'),('PSLN-344','Sham'),('PSLN-344','Vaccine')]:
        if a in u.index and b in u.index:
            z=(u.loc[a,'auc']-u.loc[b,'auc'])/np.sqrt(u.loc[a,'auc_se']**2+u.loc[b,'auc_se']**2)
            Z.append(dict(block=blk,g1=a,g2=b,auc1=u.loc[a,'auc'],auc2=u.loc[b,'auc'],ratio=u.loc[a,'auc']/u.loc[b,'auc'],z=z,p=2*stats.norm.sf(abs(z))))
Z=pd.DataFrame(Z)
D.to_csv('timecourse_descriptives.csv',index=False);A.to_csv('timecourse_anova.csv',index=False);C.to_csv('timecourse_contrasts.csv',index=False);U.to_csv('timecourse_auc.csv',index=False);Z.to_csv('timecourse_auc_tests.csv',index=False)
f=lambda v:f'{v:.3g}'
print(A.to_string(float_format=f)); print()
piv=D.pivot_table(index=['block','group'],columns='time',values='mean',sort=False); print(piv.round(2).to_string()); print()
print(C[C.g2.isin(['PSLN-212','PSLN-212(Y)','PSLN-212Y','Vaccine','Sham'])&(C.g1=='PSLN-344')].to_string(float_format=f)); print()
print(U.to_string(float_format=f)); print(); print(Z.to_string(float_format=f))
