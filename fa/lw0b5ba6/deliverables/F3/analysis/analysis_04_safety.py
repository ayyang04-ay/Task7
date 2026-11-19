"""
Analysis 4 - tolerability / safety-relevant blocks.
  S08-D : body weight after intranasal vaccination (no challenge) - reactogenicity
  S09-A : lung cytokine / chemokine transcripts (stored as log10 fold vs untreated), 16 h panel and the second
          panel (printed "16h", shown by audit_04 to be the 72 h samples of S01-A)
  S10-A : CNS transcripts 36 h after intranasal dosing, cholera toxin as positive control
Outputs: safety_weight_after_vaccination.csv, safety_cytokines.csv, safety_cns.csv
"""
import numpy as np, pandas as pd, warnings
from scipy import stats
warnings.filterwarnings('ignore')
pd.set_option('display.width',260); pd.set_option('display.max_rows',900)
d=pd.read_csv('tidy_all_observations.csv'); d['group']=d.group.str.strip()
f=lambda v:f'{v:.3g}'

# ---------------- S08-D ------------------------------------------------------------------------------
x=d[d.block=='S08-D'].copy(); x['t']=x.time.astype(float)
rows=[]; per=[]
for g in dict.fromkeys(x.group):
    a=x[x.group==g]
    w=a.pivot(index='t',columns='rep',values='value')
    nad=w.min(); nadday=w.idxmin(); d10=w.loc[10]
    for r in w.columns: per.append(dict(group=g,rep=r,nadir=nad[r],nadir_day=nadday[r],day10=d10[r],missing_day10=bool(np.isnan(d10[r]))))
    rows.append(dict(group=g,cells=f"S08!{a.cell.iloc[0]}:{a.cell.iloc[-1]}",n_day0=w.loc[0].notna().sum(),n_day10=d10.notna().sum(),
                     **{f'mean_d{int(t)}':w.loc[t].mean() for t in w.index},
                     mean_nadir=nad.mean(),sd_nadir=nad.std(ddof=1),worst_animal=nad.min(),max_loss_pct=100-nad.min(),
                     n_loss_ge5pct=int((nad<=95).sum()),n_loss_ge10pct=int((nad<=90).sum())))
W=pd.DataFrame(rows); P=pd.DataFrame(per)
tests=[]
for a,b in [('PSLN-344','Vaccine'),('PSLN-344','PSLN-212'),('PSLN-344','PSLN-212(Y)'),('PSLN-344','CMP-204'),('PSLN-212/R848','PSLN-344'),('PSLN-212/R848','Vaccine'),('PSLN-212','Vaccine')]:
    na=P[P.group==a].nadir.values; nb=P[P.group==b].nadir.values
    t=stats.ttest_ind(na,nb,equal_var=False)
    se=np.sqrt(na.var(ddof=1)/len(na)+nb.var(ddof=1)/len(nb)); dfw=se**4/((na.var(ddof=1)/len(na))**2/(len(na)-1)+(nb.var(ddof=1)/len(nb))**2/(len(nb)-1))
    ci=stats.t.ppf(0.975,dfw)*se
    tests.append(dict(contrast=f'{a} vs {b}',nadir1=na.mean(),nadir2=nb.mean(),diff=na.mean()-nb.mean(),ci_lo=na.mean()-nb.mean()-ci,ci_hi=na.mean()-nb.mean()+ci,welch_p=t.pvalue,
                      mw_exact_p=stats.mannwhitneyu(na,nb,method='exact').pvalue))
WT=pd.DataFrame(tests)
W.to_csv('safety_weight_after_vaccination.csv',index=False); WT.to_csv('safety_weight_after_vaccination_tests.csv',index=False)
print('S08-D body weight after vaccination (percent of day 0)'); print(W.to_string(float_format=f)); print(WT.to_string(float_format=f))

# ---------------- S09-A ------------------------------------------------------------------------------
c=d[d.block.str.startswith('S09-A')].copy()
c['panel']=np.where(c.block.str.contains('panel1'),'16 h','72 h [printed as 16h; = S01-A 72 h animals]')
rows=[]
for (pan,an,g),a in c.groupby(['panel','analyte','group'],sort=False):
    v=a.value.values
    rows.append(dict(panel=pan,analyte=an,group=g,cells=f'S09!{a.cell.iloc[0]}:{a.cell.iloc[-1]}',n=len(v),mean_log10=v.mean(),sd_log10=v.std(ddof=1),geo_fold=10**v.mean(),
                     lo=10**(v.mean()-stats.t.ppf(.975,len(v)-1)*stats.sem(v)),hi=10**(v.mean()+stats.t.ppf(.975,len(v)-1)*stats.sem(v))))
CY=pd.DataFrame(rows)
tests=[]
for (pan,an),a in c.groupby(['panel','analyte'],sort=False):
    G={g:b.value.values for g,b in a.groupby('group')}
    for g1,g2 in [('PSLN-344','PBS'),('PSLN-344','PSLN-212'),('PSLN-344','PSLN-212(y)'),('PSLN-212','PBS'),('PSLN-212(y)','PBS'),('PSLN-212/R848','PSLN-344'),('PSLN-R848','PBS'),('PSLN-212/R848','PBS')]:
        t=stats.ttest_ind(G[g1],G[g2],equal_var=False)
        tests.append(dict(panel=pan,analyte=an,g1=g1,g2=g2,fold_ratio=10**(G[g1].mean()-G[g2].mean()),welch_p=t.pvalue,student_p=stats.ttest_ind(G[g1],G[g2]).pvalue))
CT=pd.DataFrame(tests)
CY.to_csv('safety_cytokines.csv',index=False); CT.to_csv('safety_cytokines_tests.csv',index=False)
print('\nS09-A geometric-mean fold vs untreated'); print(CY.pivot_table(index=['panel','analyte'],columns='group',values='geo_fold',sort=False).round(1).to_string())
print(CT[CT.g1.eq('PSLN-344')].to_string(float_format=f))

# ---------------- S10-A ------------------------------------------------------------------------------
n=d[d.block.str.startswith('S10-A')].copy(); rows=[];tests=[]
for an,a in n.groupby('analyte',sort=False):
    G={g:b.value.values for g,b in a.groupby('group',sort=False)}
    for g,v in G.items():
        rows.append(dict(analyte=an,group=g,cells=f"S10!{a[a.group==g].cell.iloc[0]}:{a[a.group==g].cell.iloc[-1]}",n=len(v),mean=v.mean(),sd=v.std(ddof=1),geo=np.exp(np.log(v).mean())))
    for g1,g2 in [('PSLN-344','PBS'),('PSLN-344','Sham'),('CT','PBS'),('CT','PSLN-344'),('Sham','PBS')]:
        l1,l2=np.log10(G[g1]),np.log10(G[g2]); t=stats.ttest_ind(l1,l2,equal_var=False)
        se=np.sqrt(l1.var(ddof=1)/len(l1)+l2.var(ddof=1)/len(l2)); dfw=se**4/((l1.var(ddof=1)/len(l1))**2/(len(l1)-1)+(l2.var(ddof=1)/len(l2))**2/(len(l2)-1)); ci=stats.t.ppf(.975,dfw)*se
        tests.append(dict(analyte=an,g1=g1,g2=g2,ratio=10**(l1.mean()-l2.mean()),ci_lo=10**(l1.mean()-l2.mean()-ci),ci_hi=10**(l1.mean()-l2.mean()+ci),welch_p=t.pvalue,
                          mw_exact_p=stats.mannwhitneyu(G[g1],G[g2],method='exact').pvalue))
    F,p=stats.f_oneway(*[np.log10(v) for v in G.values()]); tests.append(dict(analyte=an,g1='ANOVA (4 groups, log10)',g2='',ratio=np.nan,welch_p=p))
N=pd.DataFrame(rows); NT=pd.DataFrame(tests); N.to_csv('safety_cns.csv',index=False); NT.to_csv('safety_cns_tests.csv',index=False)
print('\nS10-A CNS transcripts'); print(N.to_string(float_format=f)); print(NT.to_string(float_format=f))
