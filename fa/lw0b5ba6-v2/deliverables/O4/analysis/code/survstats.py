import pandas as pd, numpy as np
from scipy import stats
surv = pd.read_csv('survival.csv')
# S03-J: one PSLN-344 animal has no day value (J46) but event=0 -> censored; observation ran to 22 d, censor at 21 like others
surv.loc[(surv.block=='S03-J') & surv.day.isna(), 'day'] = 21
surv['group'] = surv.group.str.replace('Naïve','Naive')

def logrank(t1,e1,t2,e2):
    t = np.r_[t1,t2]; e = np.r_[e1,e2]; g = np.r_[np.zeros(len(t1)),np.ones(len(t2))]
    times = np.unique(t[e==1]); O1=E1=V=0.0
    for u in times:
        atrisk = t>=u; n = atrisk.sum(); n1 = (atrisk & (g==0)).sum()
        d = ((t==u)&(e==1)).sum(); d1 = ((t==u)&(e==1)&(g==0)).sum()
        O1 += d1; E1 += d*n1/n
        if n>1: V += d*(n1/n)*(1-n1/n)*(n-d)/(n-1)
    return O1,E1,V
def lr_test(t1,e1,t2,e2):
    O,E,V = logrank(t1,e1,t2,e2)
    if V==0: return np.nan, 1.0
    chi = (O-E)**2/V; return chi, stats.chi2.sf(chi,1)
def strat_lr(strata):
    O=E=V=0.0
    for (t1,e1,t2,e2) in strata:
        o,ee,v = logrank(t1,e1,t2,e2); O+=o; E+=ee; V+=v
    chi=(O-E)**2/V; return chi, stats.chi2.sf(chi,1), O, E
def cp(k,n,a=0.05):
    lo = stats.beta.ppf(a/2,k,n-k+1) if k>0 else 0.0
    hi = stats.beta.ppf(1-a/2,k+1,n-k) if k<n else 1.0
    return lo,hi
def arr(b,g):
    d = surv[(surv.block==b)&(surv.group==g)]; return d.day.values.astype(float), d.event.values.astype(int)

meta = {  # experiment descriptions (from annotation)
 'S03-I':('aged BALB/c','bivalent (CA09+Aichi)','10x mLD50 CA09 H1N1 (homologous)','d14',14),
 'S03-J':('aged BALB/c (no (Y) label)','rgH5N1 vaccine','wild-type VN04 H5N1 (BSL-3)','d2',22),
 'S06-A':('aged BALB/c','Aichi H3N2','5x mLD50 PR8 H1N1 (heterosubtypic)','d14',14),
 'S06-B':('aged BALB/c','Aichi H3N2','5x mLD50 PR8 H1N1 (heterosubtypic)','d3',14),
 'S06-C':('aged BALB/c','bivalent','5x mLD50 rgH5N1 (heterosubtypic)','d14',14),
 'S06-D':('aged BALB/c','bivalent','5x mLD50 rgH5N1 (heterosubtypic)','d3',14),
 'S06-E':('aged BALB/c','Aichi H3N2','5x mLD50 PR8 H1N1 (heterosubtypic)','d60',14),
 'S06-F':('aged BALB/c','bivalent','5x mLD50 rgH5N1 (heterosubtypic)','d60',14),
 'S06-G':('aged BALB/c','CA09 H1N1','5x mLD50 Perth H3N2 (heterosubtypic)','d60',14),
 'S06-E2_imprint':('14-mo BALB/c, +/- PR8 imprinting','bivalent','5x LD50 PR8 H1N1','not stated',14),
 'S06-F2_imprint':('14-mo BALB/c, +/- PR8 imprinting','bivalent','5x LD50 Perth H3N2 (heterosubtypic)','d14',14),
 'S15-H':('aged BALB/c','bivalent / PSLN-344 alone / both','5x mLD50 VN04 rgH5N1','d3',14),
 'S15-L':('aged C57BL/6 (20 mo)','bivalent','not stated','not stated',14),
 'S15-N':('aged Swiss Webster (20 mo)','bivalent','not stated','not stated',14),
 'S09-B':('young BALB/c','Aichi H3N2','5x mLD50 PR8 H1N1','d21',14),
 'S09-D':('young BALB/c','CA09 H1N1','5x mLD50 Perth H3N2','d21',14),
 'S09-F':('young BALB/c','bivalent','5x mLD50 VN04 rgH5N1','d180',14),
 'S13-E':('young BALB/c','bivalent','10x mLD50 CA09 H1N1','d14',14),
}
rows=[]
for b,(pop,vac,chal,when,obs) in meta.items():
    d = surv[surv.block==b]
    for g in dict.fromkeys(d.group):
        t,e = arr(b,g); n=len(t); s=int((e==0).sum()); lo,hi = cp(s,n)
        rows.append(dict(experiment=b, population=pop, vaccine=vac, challenge=chal, challenge_day=when, group=g, n=n,
                         survivors=s, pct_survival=round(100*s/n,1), ci95=f"{100*lo:.0f}-{100*hi:.0f}%",
                         median_death_day=(np.median(t[e==1]) if (e==1).any() else np.nan),
                         cells=f"{d[d.group==g].cell_event.iloc[0]}:{d[d.group==g].cell_event.iloc[-1].split('!')[1]}"))
per = pd.DataFrame(rows)
# pairwise tests
def pair(b,g1,g2):
    t1,e1 = arr(b,g1); t2,e2 = arr(b,g2)
    chi,p = lr_test(t1,e1,t2,e2)
    s1,s2 = int((e1==0).sum()), int((e2==0).sum())
    fp = stats.fisher_exact([[s1,len(t1)-s1],[s2,len(t2)-s2]])[1]
    return dict(experiment=b, comparison=f"{g1} vs {g2}", surv1=f"{s1}/{len(t1)}", surv2=f"{s2}/{len(t2)}",
                diff_pct=round(100*(s1/len(t1)-s2/len(t2)),1), logrank_chi2=round(chi,2) if chi==chi else None, logrank_p=p, fisher_p=fp)
pr=[]
for b in ['S03-I','S03-J','S06-A','S06-B','S06-C','S06-D','S06-E','S06-F','S06-G','S15-L','S15-N']:
    pr.append(pair(b,'PSLN-344','PSLN-212'))
    pr.append(pair(b,'PSLN-344','Sham'))
    if 'PSLN-212(Y)' in set(surv[surv.block==b].group): pr.append(pair(b,'PSLN-344','PSLN-212(Y)'))
pr.append(pair('S03-I','PSLN-344','CMP-204'))
pr.append(pair('S03-I','PSLN-212','Sham'))
for b in ['S06-E2_imprint','S06-F2_imprint']:
    pr.append(pair(b,'Naive+PSLN-344','Naive+PSLN-212')); pr.append(pair(b,'Imprinting+PSLN-344','Imprinting+PSLN-212'))
pr.append(pair('S15-H','3d Vaccine+PSLN-344','3d Vaccine')); pr.append(pair('S15-H','3d Vaccine+PSLN-344','3d PSLN-344'))
for b in ['S09-B','S09-D','S09-F']:
    pr.append(pair(b,'PSLN-344Y','PSLN-212Y')); pr.append(pair(b,'PSLN-344Y','Sham'))
pr.append(pair('S13-E','PSLN-344(Y)','Sham')); pr.append(pair('S13-E','PSLN-344(Y)','CMP-204(Y)'))
pairs = pd.DataFrame(pr)
per.to_csv('/tmp/outputs/analysis/T1_survival_by_group.csv', index=False)
pairs.to_csv('/tmp/outputs/analysis/T2_survival_pairwise_tests.csv', index=False)
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',60)
print(per[['experiment','population','challenge','challenge_day','group','survivors','n','pct_survival','ci95','median_death_day']].to_string())
print(pairs.to_string())
