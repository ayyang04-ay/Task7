from loadcsv import *
import numpy as np, pandas as pd
from scipy import stats
from lifelines.statistics import logrank_test
from lifelines import CoxPHFitter
from statsmodels.stats.contingency_tables import StratifiedTable
import warnings; warnings.filterwarnings('ignore')
SV2 = SV.copy()
SV2['time'] = SV2['time'].fillna(21.0)   # S03-J PSLN-344 row with missing time: censored (event=0) -> set to end of follow-up (21)
# integrity tier for each aged head-to-head study
TIER = {'S03-I':'C','S03-J':'C','S06-A':'B','S06-B':'B','S06-C':'B','S06-D':'C-dup','S06-E':'B','S06-F':'B','S06-G':'B',
        'S15-L':'C','S15-N':'C'}
WHY = {'S03-I':'companion weights (S13-F) contradict survival (PSLN-212: 7/7 dead by d6 vs weights to d14); group lists differ',
       'S03-J':'companion weights (S13-G) mislabelled & contradict Sham deaths; 1 missing time; stated n 9 vs 10 rows',
       'S06-A':'minor: more Sham weights at d6 than survivors',
       'S06-B':'minor: PSLN-212 weights after recorded deaths; PSLN-344 deaths 2 vs 3 implied by weights',
       'S06-C':'its survival block is duplicated as S06-D; its PSLN-344 weights duplicated into S15-I',
       'S06-D':'row-for-row identical to S06-C; its own weights (S15-D) imply 2 PSLN-344 and 2 young deaths',
       'S06-E':'minor: death counts differ by 1 vs weights; "unchallenged" Untreated animal died',
       'S06-F':'minor: PSLN-212 weights after recorded deaths',
       'S06-G':'PSLN-344 deaths 3 vs 2 implied by weights; 3/7 "unchallenged" Untreated animals died',
       'S15-L':'challenge virus/timing not stated; companion weights (S15-M) contain columns copied from S09-E/S15-A/S15-J',
       'S15-N':'challenge virus/timing not stated; companion weights (S15-O) share copied sequences with S15-A/S15-M'}
rows=[]
for b in TIER:
    d = SV2[SV2.block==b]
    a = d[d.group=='PSLN-212']; c = d[d.group=='PSLN-344']; y = d[d.group=='PSLN-212(Y)']; s = d[d.group=='Sham']
    lr = logrank_test(a.time,c.time,a.event,c.event)
    ft = stats.fisher_exact([[c.event.sum(),len(c)-c.event.sum()],[a.event.sum(),len(a)-a.event.sum()]])
    rows.append(dict(study=b, model=d.model.iloc[0], tier=TIER[b],
                     sham=f"{s.event.sum()}/{len(s)}" if len(s) else '', aged_212=f"{a.event.sum()}/{len(a)}", aged_344=f"{c.event.sum()}/{len(c)}",
                     young_212=(f"{y.event.sum()}/{len(y)}" if len(y) else ''), p_fisher=ft[1], p_logrank=lr.p_value, flag=WHY[b]))
R = pd.DataFrame(rows)
pd.set_option('display.width',300); pd.set_option('display.max_colwidth',90)
print(R[['study','tier','model','sham','aged_212','aged_344','young_212','p_fisher','p_logrank']].to_string(index=False))
print()
def pooled(studies, label):
    tabs=[]; D=[]
    for b in studies:
        d = SV2[SV2.block==b]
        a = d[d.group=='PSLN-212']; c = d[d.group=='PSLN-344']
        tabs.append(np.array([[c.event.sum(),len(c)-c.event.sum()],[a.event.sum(),len(a)-a.event.sum()]]))
        for _,r in pd.concat([a,c]).iterrows(): D.append(dict(T=r.time,E=r.event,trt=int(r.group=='PSLN-344'),study=b))
    st = StratifiedTable([t.astype(float)+0 for t in tabs])
    # MH risk ratio (death) 344 vs 212
    num = sum(t[0,0]*(t[1].sum())/t.sum() for t in tabs); den = sum(t[1,0]*(t[0].sum())/t.sum() for t in tabs)
    rr = num/den
    # Greenland-Robins variance for log MH RR
    P = sum(((t[0].sum())*(t[1].sum())*(t[0,0]+t[1,0]) - t[0,0]*t[1,0]*t.sum())/t.sum()**2 for t in tabs)
    R_ = sum(t[0,0]*t[1].sum()/t.sum() for t in tabs); S_ = sum(t[1,0]*t[0].sum()/t.sum() for t in tabs)
    se = np.sqrt(P/(R_*S_)); lo,hi = np.exp(np.log(rr)-1.96*se), np.exp(np.log(rr)+1.96*se)
    D = pd.DataFrame(D)
    cph = CoxPHFitter(penalizer=0.0); cph.fit(D[['T','E','trt','study']],'T','E',strata=['study'])
    hr = cph.hazard_ratios_['trt']; ci = np.exp(cph.confidence_intervals_.loc['trt'].values)
    d344 = int(sum(t[0,0] for t in tabs)); n344=int(sum(t[0].sum() for t in tabs)); d212=int(sum(t[1,0] for t in tabs)); n212=int(sum(t[1].sum() for t in tabs))
    print(f"{label}\n   studies={studies}\n   deaths PSLN-344 {d344}/{n344} ({d344/n344:.0%})  vs PSLN-212 {d212}/{n212} ({d212/n212:.0%})"
          f"\n   MH risk ratio of death (344 vs 212) = {rr:.2f} (95% CI {lo:.2f}-{hi:.2f});  CMH p = {st.test_null_odds().pvalue:.1e}"
          f"\n   stratified Cox HR (344 vs 212) = {hr:.2f} (95% CI {ci[0]:.2f}-{ci[1]:.2f}), p = {cph.summary.loc['trt','p']:.1e}"
          f"\n   absolute mortality reduction = {d212/n212-d344/n344:.0%} points")
    return dict(label=label,d344=d344,n344=n344,d212=d212,n212=n212,rr=rr,lo=lo,hi=hi,hr=hr,hlo=ci[0],hhi=ci[1])
P=[]
P.append(pooled(['S03-I','S03-J','S06-A','S06-B','S06-C','S06-E','S06-F','S06-G','S15-L','S15-N'],'ALL aged head-to-head studies (S06-D excluded as duplicate)'))
P.append(pooled(['S06-A','S06-B','S06-C','S06-E','S06-F','S06-G'],'Sensitivity 1: BALB/c S06 series only (drop S03-I, S03-J, S15-L, S15-N)'))
P.append(pooled(['S06-A','S06-B','S06-E','S06-F','S06-G'],'Sensitivity 2 (most conservative): also drop S06-C (duplication-linked)'))
P.append(pooled(['S06-E','S06-F','S06-G'],'Durability subset: challenge at day 60'))
P.append(pooled(['S06-B'],'Early-onset subset: challenge 3 days after vaccination (S06-B only; S06-D is a duplicate)'))
pd.DataFrame(P).to_csv('/tmp/work/survival_pooled.csv',index=False)
R.to_csv('/tmp/work/survival_by_study.csv',index=False)
# imprinting / middle-aged (14 mo)
print('\nImprinting study (14-month-old at vaccination):')
for b in ["S06-E'(imprint)","S06-F'(imprint)"]:
    d=SV2[SV2.block==b]
    out=[]
    for g in ['Naive+PSLN-212','Naive+PSLN-344','Imprinting+PSLN-212','Imprinting+PSLN-344']:
        x=d[d.group==g]; out.append(f"{g}: {x.event.sum()}/{len(x)} died")
    n212=d[d.group.str.endswith('PSLN-212')]; n344=d[d.group.str.endswith('PSLN-344')]
    ft=stats.fisher_exact([[n344.event.sum(),len(n344)-n344.event.sum()],[n212.event.sum(),len(n212)-n212.event.sum()]])
    print('  ',b,' | '.join(out),f'| pooled 344 vs 212 Fisher p={ft[1]:.1e}')
print('\nSpecificity (S15-H, aged, rgH5N1 challenge 3 d after dosing):')
d=SV2[SV2.block=='S15-H']
for g in d.group.unique():
    x=d[d.group==g]; print(f"   {g}: {x.event.sum()}/{len(x)} died, median death day {x[x.event==1].time.median() if x.event.sum() else '-'}")
a=d[d.group=='3d PSLN-344']; c=d[d.group=='3d Vaccine+PSLN-344']
print('   PSLN-344 alone vs Vaccine+PSLN-344: Fisher p=%.4f' % stats.fisher_exact([[a.event.sum(),len(a)-a.event.sum()],[c.event.sum(),len(c)-c.event.sum()]])[1])
print('\nYoung animals (ceiling): ')
for b in ['S09-B','S09-D','S09-F','S13-E']:
    d=SV2[SV2.block==b]; print('  ',b,d.model.iloc[0],' | '.join(f"{g}: {x.event.sum()}/{len(x)}" for g,x in d.groupby('group',sort=False)))
