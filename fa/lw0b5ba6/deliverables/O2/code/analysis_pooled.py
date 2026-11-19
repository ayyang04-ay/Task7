import pandas as pd, numpy as np
from scipy import stats
from statsmodels.stats.contingency_tables import StratifiedTable
s=pd.read_csv('survival.csv')
def strat_logrank(blocks,a,b):
    O=E=V=0.0
    for blk in blocks:
        d=s[(s.block==blk)].dropna(subset=['day'])
        A=d[d.group==a]; B=d[d.group==b]
        d1,e1,d2,e2=A.day.values,A.event.values,B.day.values,B.event.values
        for tt in np.unique(np.concatenate([d1[e1==1],d2[e2==1]])):
            n1=(d1>=tt).sum(); n2=(d2>=tt).sum(); n=n1+n2; m=((d1==tt)&(e1==1)).sum()+((d2==tt)&(e2==1)).sum()
            O+=((d1==tt)&(e1==1)).sum(); E+=m*n1/n
            if n>1: V+=m*(n1/n)*(n2/n)*(n-m)/(n-1)
    chi=(O-E)**2/V; return chi, stats.chi2.sf(chi,1), O, E
def pooled(blocks,a,b,label):
    tabs=[]; sa=na=sb=nb=0
    for blk in blocks:
        A=s[(s.block==blk)&(s.group==a)]; B=s[(s.block==blk)&(s.group==b)]
        x=[[len(A)-A.event.sum(), A.event.sum()],[len(B)-B.event.sum(), B.event.sum()]]
        tabs.append(np.array(x,float)+0.5)   # Haldane correction for zero cells in OR
        sa+=len(A)-A.event.sum(); na+=len(A); sb+=len(B)-B.event.sum(); nb+=len(B)
    st=StratifiedTable(tabs)
    cmh=st.test_null_odds(correction=True)
    chi,p,O,E=strat_logrank(blocks,a,b)
    # risk difference (pooled, Mantel-Haenszel weights)
    num=den=0
    for blk in blocks:
        A=s[(s.block==blk)&(s.group==a)]; B=s[(s.block==blk)&(s.group==b)]
        n1,n2=len(A),len(B); p1=1-A.event.mean(); p2=1-B.event.mean(); w=n1*n2/(n1+n2)
        num+=w*(p1-p2); den+=w
    print(f"{label:70s} {a} {sa}/{na} ({100*sa/na:.0f}%) vs {b} {sb}/{nb} ({100*sb/nb:.0f}%) | MH risk diff {100*num/den:+.0f} pts | CMH p={cmh.pvalue:.2g} | stratified log-rank chi2={chi:.1f} p={p:.2g} (O={O:.0f},E={E:.1f})")
    return dict(label=label,a=a,b=b,a_surv=sa,a_n=na,b_surv=sb,b_n=nb,rd=num/den,cmh_p=cmh.pvalue,slr_p=p)
out=[]
tierA=['S03-I','S03-J','S06-A','S06-B','S06-C','S06-E_r34','S06-F_r34','S06-G','S15-L','S15-N']
tierB=['S06-A','S06-B','S06-F_r34','S15-L','S15-N']
tierC=['S06-B']
hetero=['S06-A','S06-B','S06-C','S06-E_r34','S06-F_r34','S06-G']  # BALB/c aged heterosubtypic only
for lab,bl in [('Tier A: all aged challenge blocks as printed (S06-D duplicate excluded)',tierA),
               ('Tier A + S06-D (as printed, incl. duplicate) -- NOT recommended',tierA+['S06-D']),
               ('Tier B: blocks whose body-weight companion agrees on deaths in both arms',tierB),
               ('Tier C: blocks with no detectable integrity flag',tierC),
               ('Aged BALB/c heterosubtypic challenges only (S06-A,B,C,E,F,G)',hetero),
               ('Day-60 durability challenges (S06-E_r34, S06-F_r34, S06-G)',['S06-E_r34','S06-F_r34','S06-G'])]:
    out.append(pooled(bl,'PSLN-344','PSLN-212',lab))
for lab,bl in [('Tier A vs Sham',tierA),('Tier B vs Sham',tierB)]:
    out.append(pooled(bl,'PSLN-344','Sham',lab))
for lab,bl in [('Tier A: PSLN-344 (aged) vs PSLN-212(Y) young benchmark',tierA[:2]+tierA[2:])]:
    bl2=[b for b in bl if 'PSLN-212(Y)' in s[s.block==b].group.values]
    out.append(pooled(bl2,'PSLN-344','PSLN-212(Y)',lab+' '+str(bl2)))
print()
# imprinting
out.append(pooled(['S06-E_r71','S06-F_r71'],'Naive+PSLN-344','Naive+PSLN-212','14-mo mice, naive: PSLN-344 vs PSLN-212'))
out.append(pooled(['S06-E_r71','S06-F_r71'],'Imprinting+PSLN-344','Imprinting+PSLN-212','14-mo mice, imprinted: PSLN-344 vs PSLN-212'))
pd.DataFrame(out).to_csv('pooled_survival.csv',index=False)
