import pandas as pd, numpy as np, itertools, warnings
warnings.filterwarnings('ignore')
from lifelines.statistics import logrank_test
from lifelines import KaplanMeierFitter
from scipy.stats import fisher_exact, chi2
from statsmodels.stats.proportion import proportion_confint
from statsmodels.stats.contingency_tables import StratifiedTable

df = pd.read_csv('/tmp/work/tidy.csv')
s = df[df.event.notna() & (df.block!='S08-UNLABELLED')].copy()
s['event'] = s.event.astype(int)

META = {  # experiment descriptors (from annotation)
 'S03-I': ('aged BALB/c','bivalent','10x CA09 H1N1 (homologous)','d14','integrity: conflicts with S13-F weights; CMP-204>PSLN-212 paradox'),
 'S03-J': ('aged BALB/c (age not stated)','rgH5N1','WT VN04 H5N1, BSL-3 (homologous HA)','d2','integrity: stated n=9 vs 10 obs; 1 PSLN-344 row lacks day value; conflicts with S13-G'),
 'S06-A': ('aged BALB/c','Aichi H3N2','5x PR8 H1N1 (heterosubtypic)','d14',''),
 'S06-B': ('aged BALB/c','Aichi H3N2','5x PR8 H1N1 (heterosubtypic)','d3',''),
 'S06-C': ('aged BALB/c','bivalent H1+H3','5x rgH5N1 (heterosubtypic)','d14','PSLN-212 & Sham outcome vectors identical to S06-D'),
 'S06-D': ('aged BALB/c','bivalent H1+H3','5x rgH5N1 (heterosubtypic)','d3','identical vectors to S06-C; S15-D weights imply 2 unrecorded deaths each in PSLN-344 & PSLN-212(Y)'),
 'S06-E': ('aged BALB/c','Aichi H3N2','5x PR8 H1N1 (heterosubtypic)','d60','Untreated (unchallenged) 1/7 died'),
 'S06-F': ('aged BALB/c','bivalent H1+H3','5x rgH5N1 (heterosubtypic)','d60',''),
 'S06-G': ('aged BALB/c','CA09 H1N1','5x Perth H3N2 (heterosubtypic)','d60','Untreated (unchallenged) 3/7 died; PSLN-344 deaths not reflected in S15-G weights'),
 'S06-E2_imprint': ('14-mo BALB/c, +/- prior PR8 infection','bivalent','5x PR8 H1N1','not stated','label duplicated (S06-E) on sheet'),
 'S06-F2_imprint': ('14-mo BALB/c, +/- prior PR8 infection','bivalent','5x Perth H3N2 (heterosubtypic)','d14','label duplicated (S06-F) on sheet'),
 'S15-H': ('aged BALB/c','bivalent +/- PSLN-344','5x VN04 rgH5N1','d3','S15-I weights for combo group copy S15-C'),
 'S15-L': ('aged C57BL/6 (20 mo)','bivalent','not stated','not stated','challenge virus/timing not stated'),
 'S15-N': ('aged Swiss Webster (20 mo)','bivalent','not stated','not stated','challenge virus/timing not stated'),
 'S09-B': ('young BALB/c','Aichi H3N2','5x PR8 H1N1 (heterosubtypic)','d21','annotation n error (Sham)'),
 'S09-D': ('young BALB/c','CA09 H1N1','5x Perth H3N2 (heterosubtypic)','d21',''),
 'S09-F': ('young BALB/c','bivalent','5x VN04 rgH5N1','d180','Sham 7 obs vs stated 8; weights have 8 Sham'),
 'S13-E': ('young BALB/c','bivalent','10x CA09 H1N1 (homologous)','d14','stated n=5 vs 7 obs'),
}

rows=[]
for b, sub in s.groupby('block', sort=False):
    for g, x in sub.groupby('group', sort=False):
        x = x.dropna(subset=['time'])
        n = len(sub[sub.group==g]); n_t = len(x)
        d = int(sub[sub.group==g].event.sum())
        surv = n - d
        lo, hi = proportion_confint(surv, n, method='wilson')
        kmf = KaplanMeierFitter().fit(x.time, x.event)
        med = kmf.median_survival_time_
        rows.append(dict(block=b, group=g, n=n, deaths=d, survivors=surv, pct_survival=round(100*surv/n,1),
                         ci95=f'{100*lo:.0f}-{100*hi:.0f}%', median_survival_days=(None if np.isinf(med) else med),
                         n_with_time=n_t, cells=f"{x.cell.iloc[0]}..{x.cell.iloc[-1]}"))
S = pd.DataFrame(rows)

def lr(b, g1, g2):
    a = s[(s.block==b)&(s.group==g1)].dropna(subset=['time']); c = s[(s.block==b)&(s.group==g2)].dropna(subset=['time'])
    if a.empty or c.empty: return None
    r = logrank_test(a.time, c.time, a.event, c.event)
    # Fisher on end-of-study survival
    A = s[(s.block==b)&(s.group==g1)]; C = s[(s.block==b)&(s.group==g2)]
    t = [[int((A.event==0).sum()), int(A.event.sum())],[int((C.event==0).sum()), int(C.event.sum())]]
    fe = fisher_exact(t)[1]
    return dict(block=b, g1=g1, g2=g2, surv_g1=f'{t[0][0]}/{sum(t[0])}', surv_g2=f'{t[1][0]}/{sum(t[1])}',
                logrank_p=r.p_value, fisher_p=fe)

C=[]
contr = [('PSLN-344','Sham'),('PSLN-344','PSLN-212'),('PSLN-344','PSLN-212(Y)'),('PSLN-212','Sham'),('PSLN-212(Y)','Sham'),
         ('CMP-204','Sham'),('PSLN-212','CMP-204'),('PSLN-344','CMP-204'),('PSLN-344','Untreated'),('Sham','Untreated'),
         ('Naive+PSLN-344','Naive+PSLN-212'),('Imprinting+PSLN-344','Imprinting+PSLN-212'),('Imprinting+PSLN-212','Naive+PSLN-212'),('Imprinting+PSLN-344','Naive+PSLN-344'),
         ('3d Vaccine+PSLN-344','3d Vaccine'),('3d Vaccine+PSLN-344','3d PSLN-344'),('3d PSLN-344','3d Vaccine'),
         ('PSLN-344Y','Sham'),('PSLN-212Y','Sham'),('PSLN-344Y','PSLN-212Y'),('PSLN-344(Y)','Sham'),('CMP-204(Y)','Sham'),('Sham','Naive'),('PSLN-344(Y)','CMP-204(Y)')]
for b in s.block.unique():
    gs = set(s[s.block==b].group)
    for g1,g2 in contr:
        if g1 in gs and g2 in gs:
            r = lr(b,g1,g2)
            if r: C.append(r)
C = pd.DataFrame(C)

# ---------- pooled analyses (aged, heterosubtypic, same-design blocks) ----------
def pooled(blocks, g1, g2, label):
    tables=[]; tot1=[0,0]; tot2=[0,0]
    for b in blocks:
        A = s[(s.block==b)&(s.group==g1)]; B_ = s[(s.block==b)&(s.group==g2)]
        if A.empty or B_.empty: continue
        t = np.array([[ (A.event==0).sum(), A.event.sum()],[ (B_.event==0).sum(), B_.event.sum()]], dtype=float)
        tables.append(t); tot1[0]+=t[0,0]; tot1[1]+=t[0].sum(); tot2[0]+=t[1,0]; tot2[1]+=t[1].sum()
    st = StratifiedTable([t+0.0 for t in tables])
    cmh = st.test_null_odds(correction=True)
    # Mantel-Haenszel risk difference (survival proportion)
    num=0; den=0
    for t in tables:
        n1=t[0].sum(); n2=t[1].sum(); N=n1+n2
        num += (t[0,0]*n2 - t[1,0]*n1)/N; den += n1*n2/N
    rd = num/den
    # stratified log-rank: sum over strata of (O-E) and V
    O_E=0; V=0
    for b in blocks:
        A = s[(s.block==b)&(s.group==g1)].dropna(subset=['time']); B_ = s[(s.block==b)&(s.group==g2)].dropna(subset=['time'])
        if A.empty or B_.empty: continue
        d = pd.concat([A.assign(grp=1),B_.assign(grp=0)])
        for t_ in sorted(d[d.event==1].time.unique()):
            at = d[d.time>=t_]; n=len(at); n1=(at.grp==1).sum()
            dd = d[(d.time==t_)&(d.event==1)]; dt=len(dd); d1=(dd.grp==1).sum()
            if n<2: continue
            e1 = dt*n1/n; v = dt*(n1/n)*(1-n1/n)*(n-dt)/(n-1)
            O_E += d1-e1; V += v
    chi = O_E**2/V if V>0 else np.nan
    return dict(analysis=label, g1=g1, g2=g2, n_strata=len(tables), surv_g1=f'{int(tot1[0])}/{int(tot1[1])} ({100*tot1[0]/tot1[1]:.0f}%)',
                surv_g2=f'{int(tot2[0])}/{int(tot2[1])} ({100*tot2[0]/tot2[1]:.0f}%)', MH_risk_diff_pct=round(100*rd,1),
                MH_OR_survival=round(st.oddsratio_pooled,1), CMH_p=cmh.pvalue, strat_logrank_chi2=round(chi,1), strat_logrank_p=chi2.sf(chi,1))

hetero_aged_all = ['S06-A','S06-B','S06-C','S06-D','S06-E','S06-F','S06-G','S15-L','S15-N']
hetero_aged_clean = ['S06-A','S06-B','S06-E','S06-F']       # excludes blocks with any survival-side integrity flag
P=[]
for blocks,lab in [(hetero_aged_all,'All aged 4-arm challenge blocks (S06-A..G, S15-L, S15-N)'),
                   (hetero_aged_clean,'Sensitivity: only blocks with no survival-side flag (S06-A,B,E,F)'),
                   (['S06-A','S06-C'],'Challenge at d14 (S06-A,C)'),(['S06-B','S06-D'],'Challenge at d3 (S06-B,D)'),
                   (['S06-E','S06-F','S06-G'],'Challenge at d60 (S06-E,F,G)'),(['S15-L','S15-N'],'Other strains (S15-L C57BL/6, S15-N Swiss Webster)')]:
    for g1,g2 in [('PSLN-344','Sham'),('PSLN-344','PSLN-212'),('PSLN-212','Sham'),('PSLN-344','PSLN-212(Y)')]:
        try: P.append(pooled(blocks,g1,g2,lab))
        except Exception as e: print('fail',lab,g1,g2,e)
P = pd.DataFrame(P)

pd.set_option('display.width',320); pd.set_option('display.max_colwidth',80)
print(S.to_string())
print(C.to_string())
print(P.to_string())
S.to_csv('/tmp/work/surv_summary.csv',index=False); C.to_csv('/tmp/work/surv_contrasts.csv',index=False); P.to_csv('/tmp/work/surv_pooled.csv',index=False)
pd.DataFrame([(k,)+v for k,v in META.items()], columns=['block','animals','vaccine','challenge','challenge_timing','flags']).to_csv('/tmp/work/surv_meta.csv',index=False)
