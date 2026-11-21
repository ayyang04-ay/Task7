"""05_continuous_stats.py -- per-block summaries, stated tests (one-way ANOVA + Tukey), effect sizes,
age-gap closure. All outputs carry the source block + cell range."""
import pandas as pd, numpy as np, warnings
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
warnings.filterwarnings('ignore')
rng = np.random.default_rng(20261101)
C = pd.read_csv('/tmp/work/tidy/continuous.csv'); C['time'] = C['time'].astype(str)

# --- corrections driven by the integrity log ---
# DI-18: HAI below LOD -> 5
m = C.block.isin(['S03-C','S03-G']) & (C.value < 10); C.loc[m,'value'] = 5.0
# DI-04: build corrected IgG2a/IgG1 ratios from S13 source titres
rows=[]
for a,b,lab in [('S13-A','S13-B','IgG2a/IgG1 ratio anti-CA09 (from S13-A/B)'),('S13-C','S13-D','IgG2a/IgG1 ratio anti-Aichi (from S13-C/D)')]:
    for g in ['PSLN-212','PSLN-344','PSLN-212(Y)']:
        x=C[(C.block==a)&(C.group==g)].sort_values('rep'); y=C[(C.block==b)&(C.group==g)].sort_values('rep')
        for (_,rx),(_,ry) in zip(x.iterrows(),y.iterrows()):
            rows.append(dict(block=f'{a}/{b[-1]}', measurand=lab, group=g, time='d14', rep=rx.rep, value=rx.value/ry.value, cell=f'{rx.cell}/{ry.cell}'))
C = pd.concat([C, pd.DataFrame(rows)], ignore_index=True)

EXCLUDE = {'S11-A':'DI-06','S11-B':'DI-06','S07-C':'DI-10','S05-A':'DI-12','S05-B':'DI-12',
           'S03-B':'DI-04','S03-F':'DI-04','S04-B Tfh:Tfr':'DI-11'}
import re as _re
def scale_of(meas):
    # word-boundary match: 'proliferation' must NOT count as 'ratio' (bug fixed)
    return 'log' if _re.search(r'\b(titre|fold|ratio)\b', meas.lower()) else 'linear'
AGED = {'Sham','CMP-204','PSLN-212','PSLN-344','PSLN-R848','PSLN-212/R848','PTX','Vaccine','PBS','CT'}

def summarize(v, scale):
    v = np.asarray(v, float); n=len(v)
    out = dict(n=n, mean=v.mean(), sd=v.std(ddof=1) if n>1 else np.nan, median=np.median(v), min=v.min(), max=v.max())
    if scale=='log' and (v>0).all():
        lv=np.log10(v); se=lv.std(ddof=1)/np.sqrt(n); t=stats.t.ppf(.975,n-1)
        out.update(gmean=10**lv.mean(), gm_lo=10**(lv.mean()-t*se), gm_hi=10**(lv.mean()+t*se))
    else:
        se=out['sd']/np.sqrt(n); t=stats.t.ppf(.975,n-1)
        out.update(ci_lo=out['mean']-t*se, ci_hi=out['mean']+t*se)
    return out

def hedges_g(a,b):
    na,nb=len(a),len(b); sp=np.sqrt(((na-1)*np.var(a,ddof=1)+(nb-1)*np.var(b,ddof=1))/(na+nb-2))
    if sp==0: return np.nan
    d=(np.mean(a)-np.mean(b))/sp; J=1-3/(4*(na+nb)-9); return d*J

def contrast(a, b, scale):
    a=np.asarray(a,float); b=np.asarray(b,float)
    if scale=='log':
        la,lb=np.log10(a),np.log10(b)
        t=stats.ttest_ind(la,lb,equal_var=False)
        # Welch CI for difference of log means
        va,vb=la.var(ddof=1)/len(la), lb.var(ddof=1)/len(lb); se=np.sqrt(va+vb)
        df=(va+vb)**2/(va**2/(len(la)-1)+vb**2/(len(lb)-1)); q=stats.t.ppf(.975,df)
        d=la.mean()-lb.mean()
        eff=dict(effect='GMR', est=10**d, lo=10**(d-q*se), hi=10**(d+q*se), g=hedges_g(la,lb), welch_p=t.pvalue)
    else:
        t=stats.ttest_ind(a,b,equal_var=False)
        va,vb=a.var(ddof=1)/len(a), b.var(ddof=1)/len(b); se=np.sqrt(va+vb)
        df=(va+vb)**2/(va**2/(len(a)-1)+vb**2/(len(b)-1)); q=stats.t.ppf(.975,df)
        d=a.mean()-b.mean()
        eff=dict(effect='diff', est=d, lo=d-q*se, hi=d+q*se, ratio=a.mean()/b.mean() if b.mean()!=0 else np.nan,
                 g=hedges_g(a,b), welch_p=t.pvalue)
    try: eff['mw_p']=stats.mannwhitneyu(a,b,alternative='two-sided',method='exact').pvalue
    except Exception: eff['mw_p']=np.nan
    return eff

def gap_closure(x212, x344, xY, scale, B=5000):
    f=(np.log10 if scale=='log' else (lambda z:z))
    a,b,c=f(np.asarray(x212,float)),f(np.asarray(x344,float)),f(np.asarray(xY,float))
    est=(b.mean()-a.mean())/(c.mean()-a.mean()) if c.mean()!=a.mean() else np.nan
    bs=[]
    for _ in range(B):
        aa,bb,cc=rng.choice(a,len(a)),rng.choice(b,len(b)),rng.choice(c,len(c))
        den=cc.mean()-aa.mean()
        if abs(den)>1e-12: bs.append((bb.mean()-aa.mean())/den)
    bs=np.array(bs); bs=bs[np.isfinite(bs)]
    return est, np.percentile(bs,2.5), np.percentile(bs,97.5)

PAIRS=[('PSLN-344','PSLN-212'),('PSLN-344','Sham'),('PSLN-344','PSLN-212(Y)'),('PSLN-212','PSLN-212(Y)'),
       ('PSLN-212','Sham'),('PSLN-344(Y)','PSLN-212(Y)'),('PSLN-344','CMP-204'),('PSLN-212','CMP-204'),('CMP-204','Sham')]
summ_rows=[]; con_rows=[]; gap_rows=[]
for (blk,meas,time),d in C.groupby(['block','measurand','time'],sort=False):
    if blk.startswith('S09-A'): meas_scale='log_already'
    sc = scale_of(meas)
    vals = {g: dd.sort_values('rep').value.values for g,dd in d.groupby('group',sort=False)}
    if blk.startswith('S09-A'):   # values are log10 already -> back-transform to fold for uniform handling
        vals = {g: 10**v for g,v in vals.items()}; sc='log'
    cells = {g: f"{dd.cell.iloc[0]}..{dd.cell.iloc[-1]}" for g,dd in d.groupby('group',sort=False)}
    excl = EXCLUDE.get(blk,'')
    for g,v in vals.items():
        s=summarize(v,sc); s.update(block=blk,measurand=meas,time=time,group=g,scale=sc,cells=cells[g],excluded=excl)
        summ_rows.append(s)
    # ANOVA + Tukey (stated method), on log10 scale for log-type data
    gs=[g for g in vals if len(vals[g])>=2]
    tuk={}
    if len(gs)>=3:
        endog=np.concatenate([np.log10(vals[g]) if sc=='log' else vals[g] for g in gs]); grp=np.concatenate([[g]*len(vals[g]) for g in gs])
        an=stats.f_oneway(*[np.log10(vals[g]) if sc=='log' else vals[g] for g in gs])
        try:
            tk=pairwise_tukeyhsd(endog,grp,alpha=0.05); tab=pd.DataFrame(tk.summary().data[1:],columns=tk.summary().data[0])
            for _,r in tab.iterrows(): tuk[(r.group1,r.group2)]=float(r['p-adj']); tuk[(r.group2,r.group1)]=float(r['p-adj'])
        except Exception as e: pass
        anova_p=an.pvalue
    else: anova_p=np.nan
    for a,b in PAIRS:
        if a in vals and b in vals and len(vals[a])>=2 and len(vals[b])>=2:
            e=contrast(vals[a],vals[b],sc)
            e.update(block=blk,measurand=meas,time=time,contrast=f'{a} vs {b}',scale=sc,
                     mean_a=(10**np.log10(vals[a]).mean() if sc=='log' else vals[a].mean()),
                     mean_b=(10**np.log10(vals[b]).mean() if sc=='log' else vals[b].mean()),
                     n_a=len(vals[a]),n_b=len(vals[b]),anova_p=anova_p,tukey_p=tuk.get((a,b),np.nan),
                     cells_a=cells[a],cells_b=cells[b],excluded=excl)
            con_rows.append(e)
    if all(k in vals for k in ['PSLN-212','PSLN-344','PSLN-212(Y)']):
        est,lo,hi=gap_closure(vals['PSLN-212'],vals['PSLN-344'],vals['PSLN-212(Y)'],sc)
        gap_rows.append(dict(block=blk,measurand=meas,time=time,scale=sc,gap_closed=est,lo=lo,hi=hi,excluded=excl,
                             m212=(10**np.log10(vals['PSLN-212']).mean() if sc=='log' else vals['PSLN-212'].mean()),
                             m344=(10**np.log10(vals['PSLN-344']).mean() if sc=='log' else vals['PSLN-344'].mean()),
                             mY=(10**np.log10(vals['PSLN-212(Y)']).mean() if sc=='log' else vals['PSLN-212(Y)'].mean())))
S=pd.DataFrame(summ_rows); K=pd.DataFrame(con_rows); G=pd.DataFrame(gap_rows)
S.to_csv('/tmp/work/tables/continuous_summary.csv',index=False)
K.to_csv('/tmp/work/tables/continuous_contrasts.csv',index=False)
G.to_csv('/tmp/work/tables/age_gap_closure.csv',index=False)
pd.set_option('display.width',250); pd.set_option('display.max_rows',400)
k=K[K.contrast=='PSLN-344 vs PSLN-212'][['block','measurand','time','effect','mean_a','mean_b','est','lo','hi','g','tukey_p','welch_p','mw_p','excluded']]
print(k.round(4).to_string(index=False))
