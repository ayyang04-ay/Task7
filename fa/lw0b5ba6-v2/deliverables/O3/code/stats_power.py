from loadcsv import *
import numpy as np, pandas as pd
from scipy import stats
from statsmodels.stats.power import TTestIndPower
import warnings; warnings.filterwarnings('ignore')
rng=np.random.default_rng(1)
def fisher_power(p1,p2,n,alpha=0.05,sims=4000):
    x1=rng.binomial(n,p1,sims); x2=rng.binomial(n,p2,sims)
    return np.mean([stats.fisher_exact([[a,n-a],[b,n-b]])[1]<alpha for a,b in zip(x1,x2)])
def n_for(p1,p2,target=0.9):
    for n in range(4,80):
        if fisher_power(p1,p2,n)>=target: return n
    return '>80'
print("== Survival: mortality inputs from our data ==")
sv=SV.copy()
S06=['S06-A','S06-B','S06-C','S06-E','S06-F','S06-G']
for g in ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']:
    x=sv[(sv.block.isin(S06))&(sv.group==g)]; print(f"  {g:12s} S06 series mortality {x.event.sum()}/{len(x)} = {x.event.mean():.2f}")
x=sv[(sv.block.isin(S06))]
y=x[x.group=='PSLN-212(Y)']; c=x[x.group=='PSLN-344']
print(f"  aged PSLN-344 vs young PSLN-212 (S06 series): Fisher p={stats.fisher_exact([[c.event.sum(),len(c)-c.event.sum()],[y.event.sum(),len(y)-y.event.sum()]])[1]:.4f}")
print("\n== n/arm for 90% power (Fisher exact, 2-sided alpha .05), PSLN-344 mortality assumed 0.29 (most conservative pooled estimate) ==")
for comp_mort,label in [(0.94,'PSLN-212 (conservative pooled 33/35)'),(0.90,'PSLN-212 (S06 pooled 38/42)'),(0.70,'benchmark comparator, if 70%'),(0.60,'benchmark, if 60%'),(0.50,'benchmark, if 50%')]:
    print(f"   vs {label:38s}: n/arm = {n_for(comp_mort,0.29)}")
print("   (replication of effect at HALF the observed size, 0.94 -> 0.62): n/arm =", n_for(0.94,0.62))
print("\n== Antibody endpoints: within-group SD (log2) from aged groups ==")
def sdlog(b,g,hai=False):
    x=DF[(DF.block==b)&(DF.group==g)].value.values.astype(float)
    if hai: x=np.where(x<10,5,x)
    return np.std(np.log2(x),ddof=1)
sds={}
for b,hai in [('S03-C',True),('S03-G',True),('S03-D',False),('S03-H',False),('S03-A',False),('S03-E',False)]:
    s=[sdlog(b,g,hai) for g in ['PSLN-212','PSLN-344','PSLN-212(Y)']]
    sds[b]=np.sqrt(np.mean(np.square(s))); print(f"   {b}: pooled SD log2 = {sds[b]:.2f}  (212 {s[0]:.2f}, 344 {s[1]:.2f}, Y {s[2]:.2f})")
sd=max(sds['S03-C'],sds['S03-G'])
pw=TTestIndPower()
for fold in [2,1.5]:
    es=np.log2(fold)/sd
    print(f"   HAI: detect {fold}x GMT difference (SD {sd:.2f} log2): n/arm = {int(np.ceil(pw.solve_power(es,alpha=0.05,power=0.9)))} (90% power)")
# non-inferiority of aged PSLN-344 vs young benchmark (margin 1.5x GMT ratio) assuming true ratio 1
es=np.log2(1.5)/sd
print(f"   HAI non-inferiority vs young benchmark, margin 1.5x, true ratio 1.0, 1-sided .025: n/arm = {int(np.ceil(pw.solve_power(es,alpha=0.05,power=0.9)))}")
print("\n== Group-level association: HAI GMT (d14) vs survival after homologous challenge (S03-C vs S03-I; different animals) ==")
for g in ['Sham','CMP-204','PSLN-212','PSLN-344','PSLN-212(Y)']:
    h=DF[(DF.block=='S03-C')&(DF.group==g)].value.values.astype(float); h=np.where(h<10,5,h)
    m=DF[(DF.block=='S03-D')&(DF.group==g)].value.values.astype(float)
    s=sv[(sv.block=='S03-I')&(sv.group==g)]
    print(f"   {g:12s} HAI GMT {stats.gmean(h):6.1f} (n>=40: {(h>=40).sum()}/5, >=160: {(h>=160).sum()}/5)  MN GMT {stats.gmean(m):7.0f}   survival {len(s)-s.event.sum()}/{len(s)}")
print("\n== CMP-204 (cGAMP) vs PSLN-212 (CDN-1807), aged ==")
for b,lab,log in [('S01-A_16h','Ifnb1 16h',1),('S03-A','IgG CA09',1),('S03-E','IgG Aichi',1),('S03-C','HAI CA09',1),('S03-G','HAI Aichi',1),('S03-D','Neut CA09',1),('S03-H','Neut Aichi',1),('S13-I','IgG CA09 post-boost',1)]:
    a=DF[(DF.block==b)&(DF.group=='CMP-204')].value.values.astype(float); c=DF[(DF.block==b)&(DF.group=='PSLN-212')].value.values.astype(float)
    if 'HAI' in lab: a=np.where(a<10,5,a); c=np.where(c<10,5,c)
    t=stats.ttest_ind(np.log2(c),np.log2(a),equal_var=False)
    print(f"   {lab:20s} CMP-204 GM {stats.gmean(a):7.1f} | PSLN-212 GM {stats.gmean(c):7.1f} | ratio {stats.gmean(c)/stats.gmean(a):.2f}x  p={t.pvalue:.3g}")
s=sv[(sv.block=='S03-I')]; a=s[s.group=='CMP-204']; c=s[s.group=='PSLN-212']
print(f"   S03-I survival CMP-204 {len(a)-a.event.sum()}/7 vs PSLN-212 {len(c)-c.event.sum()}/7, Fisher p={stats.fisher_exact([[a.event.sum(),7-a.event.sum()],[c.event.sum(),7-c.event.sum()]])[1]:.2f}")
