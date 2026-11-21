"""06_survival.py -- per-block KM/log-rank/Fisher and pooled stratified analyses (PSLN-344 vs PSLN-212)."""
import pandas as pd, numpy as np, warnings
from scipy import stats
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test
from statsmodels.stats.contingency_tables import StratifiedTable
warnings.filterwarnings('ignore')
S = pd.read_csv('/tmp/work/tidy/survival.csv')
# DI-13: S03-J record with no day value -> censored at end of follow-up (21 d)
S['time_imputed'] = S.time.isna()
S.loc[S.time.isna() & (S.event==0), 'time'] = 21.0

META = {  # block: (population, vaccine->challenge, challenge day post-vaccination, status)
 'S03-I': ('Aged BALB/c (20 mo)','Bivalent -> 10x mLD50 CA09 H1N1 (homologous)','d14','primary (PSLN-212 arm uncertain: DI-05)'),
 'S03-J': ('BALB/c, age not stated (aged by default)','rgH5N1 -> wild-type VN04 H5N1','d2','primary (DI-13)'),
 'S06-A': ('Aged BALB/c (20 mo)','Aichi H3N2 -> 5x PR8 H1N1 (heterosubtypic)','d14','primary'),
 'S06-B': ('Aged BALB/c (20 mo)','Aichi H3N2 -> 5x PR8 H1N1 (heterosubtypic)','d3','primary'),
 'S06-C': ('Aged BALB/c (20 mo)','Bivalent -> 5x rgH5N1 (heterosubtypic)','d14','primary'),
 'S06-D': ('Aged BALB/c (20 mo)','Bivalent -> 5x rgH5N1','d3','EXCLUDED: duplicate of S06-C (DI-01)'),
 'S06-E(d60)': ('Aged BALB/c (20 mo)','Aichi H3N2 -> 5x PR8 H1N1 (heterosubtypic)','d60','primary (background mortality DI-07)'),
 'S06-F(d60)': ('Aged BALB/c (20 mo)','Bivalent -> 5x rgH5N1 (heterosubtypic)','d60','primary'),
 'S06-G(d60)': ('Aged BALB/c (20 mo)','CA09 H1N1 -> 5x Perth H3N2 (heterosubtypic)','d60','primary (background mortality DI-07)'),
 'S06-E(imprint)': ('BALB/c 14 mo, +/- prior PR8 infection','Bivalent -> 5x PR8 H1N1','d14 (stated for S06-F only)','middle-aged cohort'),
 'S06-F(imprint)': ('BALB/c 14 mo, +/- prior PR8 infection','Bivalent -> 5x Perth H3N2','d14','middle-aged cohort'),
 'S15-H': ('Aged BALB/c (20 mo)','Bivalent +/- PSLN-344 -> 5x VN04 rgH5N1','d3','SENSITIVITY ONLY: DI-02'),
 'S15-L': ('Aged C57BL/6 (20 mo); young ref','Bivalent -> challenge (virus not stated)','not stated','SENSITIVITY ONLY: DI-03'),
 'S15-N': ('Aged Swiss Webster (20 mo); young ref','Bivalent -> challenge (virus not stated)','not stated','SENSITIVITY ONLY: DI-03'),
 'S09-B': ('Young BALB/c','Aichi H3N2 -> 5x PR8 H1N1','d21','young'),
 'S09-D': ('Young BALB/c','CA09 H1N1 -> 5x Perth H3N2','d21','young'),
 'S09-F': ('Young BALB/c','Bivalent -> 5x VN04 rgH5N1','d180','young'),
 'S13-E': ('Young BALB/c','CA09 H1N1 -> 10x CA09','d14','young'),
}
per=[]; tests=[]
for blk, d in S.groupby('block', sort=False):
    for g, dd in d.groupby('group', sort=False):
        kmf=KaplanMeierFitter().fit(dd.time, dd.event)
        n=len(dd); deaths=int(dd.event.sum()); surv=n-deaths
        lo,hi=stats.beta.ppf(0.025,surv,n-surv+1) if surv>0 else 0.0, stats.beta.ppf(0.975,surv+1,n-surv) if surv<n else 1.0
        med=kmf.median_survival_time_
        per.append(dict(block=blk,group=g,n=n,deaths=deaths,survivors=surv,pct_survival=100*surv/n,cp_lo=100*lo,cp_hi=100*hi,
                        median_survival=(med if np.isfinite(med) else np.nan),
                        cells=f"{dd.cell.iloc[0]}..{dd.cell.iloc[-1]}",population=META.get(blk,('',))[0],
                        design=META.get(blk,('','',))[1],challenge_day=META.get(blk,('','','',))[2],status=META.get(blk,('','','',''))[3]))
    groups=d.group.unique().tolist()
    def pair(a,b):
        A=d[d.group==a]; B=d[d.group==b]
        lr=logrank_test(A.time,B.time,A.event,B.event)
        tab=[[int(A.event.sum()),int(len(A)-A.event.sum())],[int(B.event.sum()),int(len(B)-B.event.sum())]]
        fp=stats.fisher_exact(tab)[1]
        tests.append(dict(block=blk,contrast=f'{a} vs {b}',surv_a=f"{len(A)-A.event.sum()}/{len(A)}",surv_b=f"{len(B)-B.event.sum()}/{len(B)}",
                          logrank_p=lr.p_value,fisher_p=fp,status=META.get(blk,('','','',''))[3]))
    for a,b in [('PSLN-344','PSLN-212'),('PSLN-344','Sham'),('PSLN-344','PSLN-212(Y)'),('PSLN-212','Sham'),('PSLN-212','PSLN-212(Y)'),
                ('PSLN-344','Untreated'),('CMP-204','Sham'),('PSLN-344','CMP-204'),('PSLN-212','CMP-204'),
                ('PSLN-344(Y)','Sham'),('PSLN-212(Y)','Sham'),('PSLN-344(Y)','PSLN-212(Y)'),('CMP-204(Y)','Sham'),('Sham','Naive'),
                ('Naive+PSLN-344','Naive+PSLN-212'),('Imprinting+PSLN-344','Imprinting+PSLN-212'),('Imprinting+PSLN-212','Naive+PSLN-212'),
                ('Imprinting+PSLN-344','Naive+PSLN-344'),('3d Vaccine+PSLN-344','3d Vaccine'),('3d Vaccine+PSLN-344','3d PSLN-344'),('3d PSLN-344','3d Vaccine')]:
        if a in groups and b in groups: pair(a,b)
P=pd.DataFrame(per); T=pd.DataFrame(tests)
P.to_csv('/tmp/work/tables/survival_by_group.csv',index=False); T.to_csv('/tmp/work/tables/survival_tests.csv',index=False)

# ---------- pooled PSLN-344 vs PSLN-212 (aged) ----------
def pooled(blocks, label, arms=('PSLN-344','PSLN-212'), drop=None):
    d=S[S.block.isin(blocks)&S.group.isin(arms)].copy()
    if drop is not None: d=d[~d.apply(drop,axis=1)]
    d['trt']=(d.group==arms[0]).astype(int)
    cph=CoxPHFitter(penalizer=0.0)
    try:
        cph.fit(d[['time','event','trt','block']],'time','event',strata=['block'])
        hr=float(np.exp(cph.params_['trt'])); ci=np.exp(cph.confidence_intervals_.loc['trt']).values; p=float(cph.summary.loc['trt','p'])
        # score (stratified log-rank) test
        sc=cph.log_likelihood_ratio_test().p_value
    except Exception as e:
        hr,ci,p,sc=np.nan,[np.nan,np.nan],np.nan,np.nan
    tabs=[]
    for b,bb in d.groupby('block'):
        A=bb[bb.trt==1]; B=bb[bb.trt==0]
        tabs.append(np.array([[A.event.sum(),len(A)-A.event.sum()],[B.event.sum(),len(B)-B.event.sum()]],float))
    st=StratifiedTable(tabs)
    # Mantel-Haenszel risk difference (death) by hand
    num=sum((t[0,0]*(t[1].sum())-t[1,0]*(t[0].sum()))/t.sum() for t in tabs); den=sum(t[0].sum()*t[1].sum()/t.sum() for t in tabs)
    rd=num/den
    # Greenland-Robins variance for MH RD (Sato)
    var_num=0.0
    for t in tabs:
        n1,n0=t[0].sum(),t[1].sum(); N=t.sum(); a,c=t[0,0],t[1,0]; b,dd=t[0,1],t[1,1]
        var_num+= (a*b*n0**3 + c*dd*n1**3)/(n1*n0*N**2)
    se=np.sqrt(var_num)/den
    a_surv=sum(t[0,1] for t in tabs); a_n=sum(t[0].sum() for t in tabs); b_surv=sum(t[1,1] for t in tabs); b_n=sum(t[1].sum() for t in tabs)
    return dict(analysis=label, blocks=', '.join(blocks), k=len(tabs),
                surv_344=f"{int(a_surv)}/{int(a_n)} ({100*a_surv/a_n:.0f}%)", surv_212=f"{int(b_surv)}/{int(b_n)} ({100*b_surv/b_n:.0f}%)",
                MH_RD_death=rd, RD_lo=rd-1.96*se, RD_hi=rd+1.96*se,
                MH_OR_death=st.oddsratio_pooled, OR_lo=st.oddsratio_pooled_confint()[0], OR_hi=st.oddsratio_pooled_confint()[1],
                CMH_p=st.test_null_odds(correction=True).pvalue, cox_HR=hr, HR_lo=ci[0], HR_hi=ci[1], cox_p=p, LRT_p=sc)
prim=['S03-I','S03-J','S06-A','S06-B','S06-C','S06-E(d60)','S06-F(d60)','S06-G(d60)']
R=[pooled(prim,'PRIMARY: all aged BALB/c experiments not compromised (8)'),
   pooled([b for b in prim if b!='S03-I'],'Sens-1: drop S03-I (DI-05)'),
   pooled([b for b in prim if b!='S03-J'],'Sens-2: drop S03-J (age not stated; DI-13)'),
   pooled(['S03-I','S06-A','S06-C'],'Challenge 14 d post-vaccination (3)'),
   pooled(['S03-J','S06-B'],'Challenge 2-3 d post-vaccination (2)'),
   pooled(['S06-E(d60)','S06-F(d60)','S06-G(d60)'],'Challenge 60 d post-vaccination (3)'),
   pooled(['S06-A','S06-B','S06-C','S06-E(d60)','S06-F(d60)','S06-G(d60)'],'Heterosubtypic challenges only (6)'),
   pooled(prim+['S06-D'],'Sens-3: add duplicate S06-D (should NOT be used)'),
   pooled(prim+['S15-L','S15-N'],'Sens-4: add compromised cross-strain blocks S15-L, S15-N'),
   pooled(['S06-E(imprint)','S06-F(imprint)'],'Middle-aged (14 mo) naive animals', arms=('Naive+PSLN-344','Naive+PSLN-212')),
   pooled(['S06-E(imprint)','S06-F(imprint)'],'Middle-aged (14 mo) imprinted animals', arms=('Imprinting+PSLN-344','Imprinting+PSLN-212')),
  ]
Q=pd.DataFrame(R); Q.to_csv('/tmp/work/tables/survival_pooled.csv',index=False)
pd.set_option('display.width',260); pd.set_option('display.max_columns',30)
print(P[['block','group','n','deaths','pct_survival','cp_lo','cp_hi','median_survival','status']].round(1).to_string(index=False))
print(T[T.contrast.isin(['PSLN-344 vs PSLN-212','PSLN-344 vs Sham','PSLN-344 vs PSLN-212(Y)','PSLN-344 vs Untreated','Naive+PSLN-344 vs Naive+PSLN-212','Imprinting+PSLN-344 vs Imprinting+PSLN-212'])].round(5).to_string(index=False))
print(Q.drop(columns=['blocks']).round(4).to_string(index=False))
