import pandas as pd, numpy as np, warnings
from scipy import stats
warnings.filterwarnings('ignore')
s=pd.read_csv('survival.csv')
def logrank(d1,e1,d2,e2):
    d1,e1,d2,e2=map(np.asarray,(d1,e1,d2,e2))
    times=np.unique(np.concatenate([d1[e1==1],d2[e2==1]]))
    O1=E1=V=0.0
    for tt in times:
        n1=(d1>=tt).sum(); n2=(d2>=tt).sum(); n=n1+n2
        m1=((d1==tt)&(e1==1)).sum(); m2=((d2==tt)&(e2==1)).sum(); m=m1+m2
        if n==0: continue
        O1+=m1; E1+=m*n1/n
        if n>1: V+=m*(n1/n)*(n2/n)*(n-m)/(n-1)
    chi=(O1-E1)**2/V if V>0 else 0.0
    return chi, stats.chi2.sf(chi,1), O1, E1, V
def km_median(d,e):
    d=np.asarray(d); e=np.asarray(e); S=1.0
    for tt in np.unique(d[e==1]):
        n=(d>=tt).sum(); m=((d==tt)&(e==1)).sum(); S*=1-m/n
        if S<=0.5: return tt
    return np.inf
rows=[]
s2=s.dropna(subset=['day'])
for blk,dB in s.groupby('block'):
    gs=dB.group.unique()
    for g in gs:
        x=dB[dB.group==g]; xd=x.dropna(subset=['day'])
        rows.append(dict(block=blk,group=g,n=len(x),deaths=int(x.event.sum()),survivors=int(len(x)-x.event.sum()),
                         surv_pct=100*(1-x.event.mean()),median=km_median(xd.day,xd.event),missing_day=int(x.day.isna().sum())))
S=pd.DataFrame(rows)
pd.set_option('display.width',250); pd.set_option('display.max_rows',300)
print(S.to_string(index=False))
S.to_csv('surv_summary.csv',index=False)
print("\n=== pairwise log-rank and Fisher exact ===")
pairs=[('PSLN-344','PSLN-212'),('PSLN-344','Sham'),('PSLN-212','Sham'),('PSLN-344','PSLN-212(Y)'),('PSLN-344','CMP-204'),('CMP-204','PSLN-212'),
       ('Naive+PSLN-344','Naive+PSLN-212'),('Imprinting+PSLN-344','Imprinting+PSLN-212'),('Imprinting+PSLN-212','Naive+PSLN-212'),
       ('3d Vaccine+PSLN-344','3d Vaccine'),('3d Vaccine+PSLN-344','3d PSLN-344'),('PSLN-344(Y)','Sham'),('PSLN-212(Y)','Sham'),('PSLN-344(Y)','PSLN-212(Y)'),('CMP-204(Y)','Sham'),
       ('PSLN-344','Untreated')]
P=[]
for blk,dB in s2.groupby('block'):
    for a,b in pairs:
        if a in dB.group.values and b in dB.group.values:
            A=dB[dB.group==a]; B=dB[dB.group==b]
            chi,p,O,E,V=logrank(A.day,A.event,B.day,B.event)
            # Fisher on survival at end (use full s incl. missing day)
            Af=s[(s.block==blk)&(s.group==a)]; Bf=s[(s.block==blk)&(s.group==b)]
            tab=[[int(len(Af)-Af.event.sum()),int(Af.event.sum())],[int(len(Bf)-Bf.event.sum()),int(Bf.event.sum())]]
            fp=stats.fisher_exact(tab)[1]
            P.append(dict(block=blk,comparison=f'{a} vs {b}',a_surv=f'{tab[0][0]}/{sum(tab[0])}',b_surv=f'{tab[1][0]}/{sum(tab[1])}',logrank_chi2=round(chi,2),logrank_p=p,fisher_p=fp))
P=pd.DataFrame(P); print(P.to_string(index=False)); P.to_csv('surv_pairwise.csv',index=False)
