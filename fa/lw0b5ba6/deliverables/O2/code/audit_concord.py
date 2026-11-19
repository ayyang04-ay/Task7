import pandas as pd, numpy as np
s=pd.read_csv('survival.csv'); b=pd.read_csv('bodyweight.csv')
pd.set_option('display.width',250); pd.set_option('display.max_rows',500)
def bw_fate(d):
    """d: one animal's bw records sorted by day. returns (status, day) status in alive/died_missing/died_LOCF"""
    d=d.sort_values('day'); days=list(d.day); vals=list(d.value)
    last=max(days)
    if last<14: return ('gone', last)            # record stops -> died/removed after 'last'
    # LOCF: identical values for final >=2 recorded timepoints and not recovered
    k=1
    while k<len(vals) and abs(vals[-1-k]-vals[-1])<1e-9: k+=1
    if k>=2 and vals[-1]<97:
        return ('LOCF', days[-k])                 # plateau starts here
    return ('alive', 14)
pairs=[('S03-I','S13-F','annotation: S13-F = animals of S03-I'),('S03-J','S13-G','annotation: S13-G = animals of S03-J'),
       ('S06-A','S15-A','same design'),('S06-B','S15-B','same design'),('S06-C','S15-C','same design'),('S06-D','S15-D','same design'),
       ('S06-E_r34','S15-E','same design'),('S06-F_r34','S15-F','same design'),('S06-G','S15-G','same design'),
       ('S15-H','S15-I','annotation: S15-I = animals of S15-H'),('S06-E_r71','S15-J','same design'),('S06-F_r71','S15-K','same design'),
       ('S15-L','S15-M','annotation: S15-M = animals of S15-L'),('S15-N','S15-O','annotation: S15-O = animals of S15-N'),
       ('S09-B','S09-C','annotation: S09-C = animals of S09-B'),('S09-D','S09-E','annotation'),('S09-F','S09-G','annotation')]
rows=[]
for sb,bb,link in pairs:
    ss=s[s.block==sb]; bw=b[b.block==bb]
    groups=sorted(set(ss.group)|set(bw.group))
    for g in groups:
        sg=ss[ss.group==g]; bg=bw[bw.group==g]
        n_s=len(sg); dead_s=int(sg.event.sum()) if n_s else None
        fates=[bw_fate(d) for _,d in bg.groupby('animal')] if len(bg) else []
        n_b=len(fates); gone=sum(f[0]=='gone' for f in fates); locf=sum(f[0]=='LOCF' for f in fates)
        death_days_s=sorted(sg[sg.event==1].day.tolist()) if n_s else None
        rows.append(dict(surv=sb,bw=bb,link=link,group=g,n_surv=n_s,deaths_surv=dead_s,surv_death_days=death_days_s,
                         n_bw=n_b,bw_record_stops=gone,bw_LOCF_plateau=locf,bw_implied_deaths=gone+locf,
                         bw_fates=sorted([(f[0],f[1]) for f in fates if f[0]!='alive'])))
r=pd.DataFrame(rows)
r['match']=r.apply(lambda x: (x.deaths_surv==x.bw_implied_deaths) if (x.n_surv and x.n_bw) else None,axis=1)
print(r[['surv','bw','group','n_surv','deaths_surv','n_bw','bw_record_stops','bw_LOCF_plateau','bw_implied_deaths','match']].to_string(index=False))
r.to_csv('concordance.csv',index=False)
print()
print(r[r.match==False][['surv','bw','group','surv_death_days','bw_fates']].to_string(index=False))
