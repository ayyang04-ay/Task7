"""
Analysis 1 - challenge survival (primary efficacy evidence).

Inputs : tidy_all_observations.csv (built by psln_blocks.py; one row per animal for survival blocks)
         weights_decoded_per_animal.csv (built by audit_02_survival_vs_weight.py)
Outputs: survival_per_experiment.csv, survival_tests.csv, survival_pooled.csv, survival_sensitivity.csv
"""
import itertools, math, numpy as np, pandas as pd
from scipy import stats
from statsmodels.stats.proportion import proportion_confint
from statsmodels.stats.contingency_tables import StratifiedTable
pd.set_option('display.width',250); pd.set_option('display.max_rows',500); pd.set_option('display.max_colwidth',80)

d = pd.read_csv('tidy_all_observations.csv')
s = d[d.kind=='survival'].copy()
s['event']=s.event.astype(int)

# ---------------------------------------------------------------------------------------------------------
# experiment metadata (from the annotation PDF); 'cells' = full block range in the workbook
META = {
 'S03-I':      dict(exp='E01',age='aged >=20 mo BALB/c',vaccine='bivalent H1N1+H3N2',challenge='10x mLD50 CA09 H1N1 (homologous)',chal_day=14,window='d14',cells='S03!A16:F51'),
 'S03-J':      dict(exp='E02',age='aged >=20 mo BALB/c',vaccine='rgH5N1',challenge='wild-type VN04 H5N1 (BSL-3)',chal_day=2,window='d2-3',cells='S03!G16:J46'),
 'S06-A':      dict(exp='E03',age='aged >=20 mo BALB/c',vaccine='Aichi H3N2',challenge='5x mLD50 PR8 H1N1 (heterosubtypic)',chal_day=14,window='d14',cells='S06!A2:E30'),
 'S06-B':      dict(exp='E04',age='aged >=20 mo BALB/c',vaccine='Aichi H3N2',challenge='5x mLD50 PR8 H1N1 (heterosubtypic)',chal_day=3,window='d2-3',cells='S06!G2:K30'),
 'S06-C':      dict(exp='E05',age='aged >=20 mo BALB/c',vaccine='bivalent H1N1+H3N2',challenge='5x mLD50 rgH5N1 (heterosubtypic)',chal_day=14,window='d14',cells='S06!M2:Q30'),
 'S06-D':      dict(exp='E06',age='aged >=20 mo BALB/c',vaccine='bivalent H1N1+H3N2',challenge='5x mLD50 rgH5N1 (heterosubtypic)',chal_day=3,window='d2-3',cells='S06!A33:E61'),
 'S06-E(r34)': dict(exp='E07',age='aged >=20 mo BALB/c',vaccine='Aichi H3N2',challenge='5x mLD50 PR8 H1N1 (heterosubtypic)',chal_day=60,window='d60',cells='S06!G33:L68'),
 'S06-F(r34)': dict(exp='E08',age='aged >=20 mo BALB/c',vaccine='bivalent H1N1+H3N2',challenge='5x mLD50 rgH5N1 (heterosubtypic)',chal_day=60,window='d60',cells='S06!M33:R68'),
 'S06-G':      dict(exp='E09',age='aged >=20 mo BALB/c',vaccine='CA09 H1N1',challenge='5x mLD50 Perth H3N2 (heterosubtypic)',chal_day=60,window='d60',cells='S06!A70:F105'),
 'S15-H':      dict(exp='E10',age='aged >=20 mo BALB/c',vaccine='bivalent / none',challenge='5x mLD50 rgH5N1',chal_day=3,window='d2-3',cells='S15!A72:D93'),
 'S06-E(r71)': dict(exp='E11',age='14 mo BALB/c (10 mo + 4 mo), +/- PR8 imprinting',vaccine='bivalent H1N1+H3N2',challenge='5x LD50 PR8 H1N1',chal_day=None,window='not stated',cells='S06!G70:K98'),
 'S06-F(r71)': dict(exp='E12',age='14 mo BALB/c (10 mo + 4 mo), +/- PR8 imprinting',vaccine='bivalent H1N1+H3N2',challenge='5x LD50 Perth H3N2',chal_day=14,window='d14',cells='S06!M70:Q98'),
 'S15-L':      dict(exp='E13',age='aged 20 mo C57BL/6',vaccine='bivalent H1N1+H3N2',challenge='not stated',chal_day=None,window='not stated',cells='S15!A102:E130'),
 'S15-N':      dict(exp='E14',age='aged 20 mo Swiss Webster (outbred)',vaccine='bivalent H1N1+H3N2',challenge='not stated',chal_day=None,window='not stated',cells='S15!A133:E161'),
 'S09-B':      dict(exp='Y01',age='young BALB/c',vaccine='Aichi H3N2',challenge='5x mLD50 PR8 H1N1',chal_day=21,window='d21',cells='S09!A11:D35'),
 'S09-D':      dict(exp='Y02',age='young BALB/c',vaccine='CA09 H1N1',challenge='5x mLD50 Perth H3N2',chal_day=21,window='d21',cells='S09!A38:D62'),
 'S09-F':      dict(exp='Y03',age='young BALB/c',vaccine='bivalent H1N1+H3N2',challenge='5x mLD50 rgH5N1',chal_day=180,window='d180',cells='S09!A65:D88'),
 'S13-E':      dict(exp='Y04',age='young BALB/c',vaccine='bivalent H1N1+H3N2',challenge='10x mLD50 CA09 H1N1 (homologous)',chal_day=14,window='d14',cells='S13!R2:V30'),
}
# canonical arm names --------------------------------------------------------------------------------------
def arm(block, g):
    g=g.replace('Naïve','Naive')
    m={'PSLN-344Y':'PSLN-344(Y)','PSLN-212Y':'PSLN-212(Y)'}
    return m.get(g,g)
s['arm']=[arm(b,g) for b,g in zip(s.block,s.group)]
s['exp']=s.block.map(lambda b: META[b]['exp'])

def cp(k,n):
    lo,hi=proportion_confint(k,n,alpha=0.05,method='beta'); return lo,hi

# exact permutation log-rank ---------------------------------------------------------------------------------
def logrank_stat(time,event,grp):
    """Return (O1-E1, V) for group==1 (standard hypergeometric variance)."""
    O_E=0.0; V=0.0
    for t in np.unique(time[event==1]):
        at=time>=t; n=at.sum(); n1=(at&(grp==1)).sum()
        dt=((time==t)&(event==1)).sum(); d1=((time==t)&(event==1)&(grp==1)).sum()
        O_E+=d1-dt*n1/n
        if n>1: V+=dt*(n1/n)*(1-n1/n)*(n-dt)/(n-1)
    return O_E,V
def logrank_exact(t1,e1,t2,e2,max_enum=400000,seed=1):
    time=np.r_[t1,t2].astype(float); event=np.r_[e1,e2].astype(int)
    n1=len(t1); N=len(time); grp=np.zeros(N,int); grp[:n1]=1
    oe,v=logrank_stat(time,event,grp)
    if v==0: return np.nan,1.0,1.0
    chi=oe*oe/v; p_asym=stats.chi2.sf(chi,1)
    ncomb=math.comb(N,n1); obs=abs(oe); cnt=0; tot=0
    if ncomb<=max_enum:
        for idx in itertools.combinations(range(N),n1):
            g=np.zeros(N,int); g[list(idx)]=1
            o,_=logrank_stat(time,event,g); tot+=1
            if abs(o)>=obs-1e-12: cnt+=1
        return chi,p_asym,cnt/tot
    rng=np.random.default_rng(seed)
    for _ in range(20000):
        g=np.zeros(N,int); g[rng.choice(N,n1,replace=False)]=1
        o,_=logrank_stat(time,event,g); tot+=1
        if abs(o)>=obs-1e-12: cnt+=1
    return chi,p_asym,(cnt+1)/(tot+1)

# ---------------------------------------------------------------------------------------------------------
# 1. per-experiment, per-arm table
rows=[]
for (b,a),x in s.groupby(['block','arm'],sort=False):
    n=len(x); dead=int((x.event==1).sum()); alive=n-dead
    lo,hi=cp(alive,n)
    dd=sorted(int(t) for t,e in zip(x.time,x.event) if e==1)
    rows.append(dict(exp=META[b]['exp'],block=b,cells=META[b]['cells'],age=META[b]['age'],vaccine=META[b]['vaccine'],
                     challenge=META[b]['challenge'],chal_day=META[b]['chal_day'],window=META[b]['window'],arm=a,
                     group_cells=f"{x.cell.iloc[0]}:{x.cell.iloc[-1]}",n=n,deaths=dead,survivors=alive,
                     surv_pct=round(100*alive/n,1),ci_lo=round(100*lo,1),ci_hi=round(100*hi,1),
                     death_days=','.join(map(str,dd)),median_death_day=(np.median(dd) if dd else np.nan),
                     rows_missing_day=int(x.time.isna().sum())))
per=pd.DataFrame(rows).sort_values(['exp','arm']).reset_index(drop=True)
per.to_csv('survival_per_experiment.csv',index=False)
print(per[['exp','block','window','arm','n','deaths','survivors','surv_pct','ci_lo','ci_hi','death_days']].to_string())

# ---------------------------------------------------------------------------------------------------------
# 2. within-experiment tests
def test(b,a1,a2):
    x1=s[(s.block==b)&(s.arm==a1)&s.time.notna()]; x2=s[(s.block==b)&(s.arm==a2)&s.time.notna()]
    if len(x1)==0 or len(x2)==0: return None
    k1=(x1.event==0).sum(); k2=(x2.event==0).sum()
    _,pf=stats.fisher_exact([[k1,len(x1)-k1],[k2,len(x2)-k2]])
    chi,pa,pe=logrank_exact(x1.time.values,x1.event.values,x2.time.values,x2.event.values)
    return dict(exp=META[b]['exp'],block=b,arm1=a1,arm2=a2,surv1=f'{k1}/{len(x1)}',surv2=f'{k2}/{len(x2)}',
                risk_diff_pct=round(100*(k1/len(x1)-k2/len(x2)),1),fisher_p=pf,logrank_chi2=chi,logrank_p_asym=pa,logrank_p_exact=pe)
contrasts=[('PSLN-344','PSLN-212'),('PSLN-344','Sham'),('PSLN-212','Sham'),('PSLN-344','PSLN-212(Y)'),('PSLN-344','CMP-204'),('PSLN-344','Untreated'),
           ('3d Vaccine+PSLN-344','3d PSLN-344'),('3d Vaccine+PSLN-344','3d Vaccine'),('3d PSLN-344','3d Vaccine'),
           ('Naive+PSLN-344','Naive+PSLN-212'),('Imprinting+PSLN-344','Imprinting+PSLN-212'),('Imprinting+PSLN-212','Naive+PSLN-212'),('Imprinting+PSLN-344','Naive+PSLN-344'),
           ('PSLN-344(Y)','PSLN-212(Y)'),('PSLN-344(Y)','Sham'),('PSLN-344(Y)','CMP-204(Y)'),('CMP-204(Y)','Sham'),('PSLN-212(Y)','Sham')]
T=[]
for b in META:
    for a1,a2 in contrasts:
        r=test(b,a1,a2)
        if r: T.append(r)
T=pd.DataFrame(T); T.to_csv('survival_tests.csv',index=False)
print('\nWithin-experiment tests (Fisher exact on survival at end of observation; exact permutation log-rank):')
print(T.to_string(float_format=lambda v:f'{v:.4g}'))

# ---------------------------------------------------------------------------------------------------------
# 3. pooled analyses (aged / middle-aged animals; each experiment is a stratum)
def strata_tables(blocks_arms):
    """blocks_arms: list of (block, arm1, arm2) -> list of 2x2 [[surv1, dead1],[surv2, dead2]]"""
    tabs=[]; lab=[]
    for b,a1,a2 in blocks_arms:
        x1=s[(s.block==b)&(s.arm==a1)]; x2=s[(s.block==b)&(s.arm==a2)]
        if len(x1)==0 or len(x2)==0: continue
        tabs.append(np.array([[(x1.event==0).sum(),(x1.event==1).sum()],[(x2.event==0).sum(),(x2.event==1).sum()]])); lab.append((b,a1,a2))
    return tabs,lab
def mh_rd(tabs):
    """Mantel-Haenszel pooled risk difference in survival with the Greenland-Robins (1985) variance.
    (Strata with 0 or 100 % in both arms contribute no variance, so this interval is optimistic; the
    Newcombe interval on the pooled proportions is reported alongside.)"""
    num=0.0; den=0.0; L=0.0
    for t in tabs:
        a,b=t[0]; c,d_=t[1]; n1=a+b; n2=c+d_; N=n1+n2
        w=n1*n2/N; num+=w*(a/n1-c/n2); den+=w
        L+=(a*b*n2**3+c*d_*n1**3)/(n1*n2*N**2)
    rd=num/den; se=math.sqrt(L)/den
    return rd,rd-1.96*se,rd+1.96*se
def newcombe(k1,n1,k2,n2):
    """Newcombe hybrid-score 95 % CI for a difference of two independent proportions."""
    from statsmodels.stats.proportion import proportion_confint as pc
    p1=k1/n1; p2=k2/n2; l1,u1=pc(k1,n1,method='wilson'); l2,u2=pc(k2,n2,method='wilson')
    d_=p1-p2
    return d_-math.sqrt((p1-l1)**2+(u2-p2)**2), d_+math.sqrt((u1-p1)**2+(p2-l2)**2)
def pooled(name,blocks_arms):
    tabs,lab=strata_tables(blocks_arms)
    k1=sum(t[0,0] for t in tabs); n1=sum(t[0].sum() for t in tabs); k2=sum(t[1,0] for t in tabs); n2=sum(t[1].sum() for t in tabs)
    informative=[t for t in tabs if t[:,0].sum()>0 and t[:,1].sum()>0]
    if informative:
        st=StratifiedTable([t+0.0 for t in tabs]); cmh=st.test_null_odds(correction=True); chi=float(cmh.statistic); p=float(stats.chi2.sf(chi,1))
    else:
        chi=np.nan; p=1.0
    rd,lo,hi=mh_rd(tabs); nlo,nhi=newcombe(k1,n1,k2,n2)
    l1,h1=cp(k1,n1); l2,h2=cp(k2,n2)
    return dict(analysis=name,strata=len(tabs),blocks=' | '.join(f'{b}' for b,_,_ in lab),
                arm1_surv=f'{k1}/{n1}',arm1_pct=round(100*k1/n1,1),arm1_ci=f'{100*l1:.0f}-{100*h1:.0f}',
                arm2_surv=f'{k2}/{n2}',arm2_pct=round(100*k2/n2,1),arm2_ci=f'{100*l2:.0f}-{100*h2:.0f}',
                MH_risk_diff_pct=round(100*rd,1),MH_rd_ci=f'{100*lo:.0f} to {100*hi:.0f}',newcombe_rd_ci=f'{100*nlo:.0f} to {100*nhi:.0f}',
                CMH_chi2=(round(chi,2) if chi==chi else np.nan),CMH_p=p,fisher_unstratified_p=stats.fisher_exact([[k1,n1-k1],[k2,n2-k2]])[1])
aged20=['S03-I','S03-J','S06-A','S06-B','S06-C','S06-D','S06-E(r34)','S06-F(r34)','S06-G','S15-L','S15-N']
P=[]
P.append(pooled('A. PSLN-344 vs PSLN-212, all >=20-mo experiments as printed',[(b,'PSLN-344','PSLN-212') for b in aged20]))
P.append(pooled('B. as A, excluding S06-C (survival table identical to S06-D)',[(b,'PSLN-344','PSLN-212') for b in aged20 if b!='S06-C']))
P.append(pooled('C. as B, also excluding S03-J (group labels disagree with its weight table S13-G)',[(b,'PSLN-344','PSLN-212') for b in aged20 if b not in('S06-C','S03-J')]))
P.append(pooled('D. PSLN-344 vs Sham (vaccine + empty liposome), >=20-mo, excl. S06-C',[(b,'PSLN-344','Sham') for b in aged20 if b!='S06-C']))
P.append(pooled('E. PSLN-212 vs Sham, >=20-mo, excl. S06-C',[(b,'PSLN-212','Sham') for b in aged20 if b!='S06-C']))
P.append(pooled('F. aged PSLN-344 vs young PSLN-212(Y), excl. S06-C',[(b,'PSLN-344','PSLN-212(Y)') for b in aged20 if b!='S06-C']))
P.append(pooled('G. 14-mo animals: PSLN-344 vs PSLN-212 (naive and imprinted strata)',[('S06-E(r71)','Naive+PSLN-344','Naive+PSLN-212'),('S06-E(r71)','Imprinting+PSLN-344','Imprinting+PSLN-212'),('S06-F(r71)','Naive+PSLN-344','Naive+PSLN-212'),('S06-F(r71)','Imprinting+PSLN-344','Imprinting+PSLN-212')]))
P.append(pooled('H. day-60 challenge only: PSLN-344 vs PSLN-212',[(b,'PSLN-344','PSLN-212') for b in ['S06-E(r34)','S06-F(r34)','S06-G']]))
P.append(pooled('I. day-60 challenge only: aged PSLN-344 vs young PSLN-212(Y)',[(b,'PSLN-344','PSLN-212(Y)') for b in ['S06-E(r34)','S06-F(r34)','S06-G']]))
P.append(pooled('J. day-60: challenged PSLN-344 vs Untreated (no vaccine, no virus) age-matched',[(b,'PSLN-344','Untreated') for b in ['S06-E(r34)','S06-F(r34)','S06-G']]))
P.append(pooled('K. young: PSLN-344(Y) vs PSLN-212(Y)',[(b,'PSLN-344(Y)','PSLN-212(Y)') for b in ['S09-B','S09-D','S09-F']]))
P=pd.DataFrame(P); P.to_csv('survival_pooled.csv',index=False)
print('\nPooled (stratified by experiment):'); print(P.drop(columns=['blocks']).to_string(float_format=lambda v:f'{v:.3g}'))

# by challenge window, PSLN-344 aged --------------------------------------------------------------------------
print('\nPSLN-344 (aged >=20 mo) by challenge window (survival tables as printed):')
W=[]
for win,blocks,armname in [('d2-3',['S03-J','S06-B','S06-D','S15-H'],None),('d14',['S03-I','S06-A','S06-C'],None),('d14 excl. S06-C',['S03-I','S06-A'],None),('d60',['S06-E(r34)','S06-F(r34)','S06-G'],None),
                           ('strain panel (timing not stated)',['S15-L','S15-N'],None)]:
    for a in ['PSLN-344','PSLN-212','Sham','PSLN-212(Y)','Untreated']:
        x=s[s.block.isin(blocks)&(s.arm.isin([a] if a!='PSLN-344' else ['PSLN-344','3d Vaccine+PSLN-344']))]
        if len(x)==0: continue
        k=(x.event==0).sum(); n=len(x); lo,hi=cp(k,n)
        W.append(dict(window=win,arm=a,blocks=','.join(blocks),surv=f'{k}/{n}',pct=round(100*k/n,1),ci=f'{100*lo:.0f}-{100*hi:.0f}'))
W=pd.DataFrame(W); W.to_csv('survival_by_window.csv',index=False); print(W.to_string())
# waning test: d14 vs d60 for PSLN-344
for lab,b14 in [('d14 incl. S06-C',['S03-I','S06-A','S06-C']),('d14 excl. S06-C',['S03-I','S06-A'])]:
    a=s[s.block.isin(b14)&(s.arm=='PSLN-344')]; b=s[s.block.isin(['S06-E(r34)','S06-F(r34)','S06-G'])&(s.arm=='PSLN-344')]
    t=[[(a.event==0).sum(),(a.event==1).sum()],[(b.event==0).sum(),(b.event==1).sum()]]
    print(f'  waning, PSLN-344 {lab} vs d60: {t}  Fisher p={stats.fisher_exact(t)[1]:.3f}')
u=s[s.arm=='Untreated']; print('  Untreated (no vaccine/no virus) deaths over 14 d: %d/%d'%((u.event==1).sum(),len(u)), ' 95%% CI %.0f-%.0f%%'%tuple(100*np.array(cp((u.event==1).sum(),len(u)))))
