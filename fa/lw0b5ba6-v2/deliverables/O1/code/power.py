import numpy as np, pandas as pd
from scipy import stats
from functools import lru_cache
V = pd.read_csv('/tmp/work/tidy/values.csv')
def fisher_power(p1, p2, n, alpha=0.05):
    # exact power: enumerate outcomes
    pw = 0.0
    pm1 = stats.binom.pmf(np.arange(n+1), n, p1); pm2 = stats.binom.pmf(np.arange(n+1), n, p2)
    for x1 in range(n+1):
        for x2 in range(n+1):
            if pm1[x1]*pm2[x2] < 1e-12: continue
            p = stats.fisher_exact([[x1, n-x1],[x2, n-x2]])[1]
            if p < alpha: pw += pm1[x1]*pm2[x2]
    return pw
def n_for(p1,p2,target):
    for n in range(4,80):
        if fisher_power(p1,p2,n) >= target: return n
print('Survival (Fisher exact, two-sided alpha 0.05):')
for p1,p2,lab in [(0.84,0.13,'PSLN-344 vs PSLN-212 (pooled observed 84% vs 13%)'),(0.63,0.20,'worst-case observed (63% vs 20%)'),
                  (0.80,0.40,'PSLN-344 vs SOC analogue, assumed 80% vs 40%'),(0.80,0.50,'assumed 80% vs 50%')]:
    print(f'  {lab}: n/arm for 80% power = {n_for(p1,p2,0.8)}, 90% power = {n_for(p1,p2,0.9)}')
# pooled within-group SD of log2 HAI and log2 IgG from aged PSLN-344/PSLN-212 and young groups
sds={}
for blk in ['S03-C','S03-G','S03-A','S03-E','S03-D','S03-H']:
    d = V[(V.block==blk)&(V.group.isin(['PSLN-344','PSLN-212','PSLN-212(Y)']))].copy()
    d['l']=np.log2(d.value.clip(lower=5))
    ss = d.groupby('group').l.var(ddof=1); n = d.groupby('group').size()
    sds[blk]=np.sqrt(((n-1)*ss).sum()/(n-1).sum())
print('pooled within-group SD (log2):', {k: round(v,2) for k,v in sds.items()})
sd = max(sds['S03-C'], sds['S03-G'])
for fold in [2, 4]:
    d = np.log2(fold)
    for pw in [0.8, 0.9]:
        for n in range(3,100):
            df = 2*n-2; ncp = d/(sd*np.sqrt(2/n)); tcrit = stats.t.ppf(0.975, df)
            if 1 - stats.nct.cdf(tcrit, df, ncp) >= pw: break
        print(f'HAI: detect {fold}-fold GMT difference (SD log2={sd:.2f}) power {pw}: n/arm = {n}')
# Mn tissue level design assumption
for cv in [0.3, 0.5]:
    s = np.sqrt(np.log(1+cv**2)); d = np.log(1.5)
    for n in range(3,100):
        df=2*n-2; ncp=d/(s*np.sqrt(2/n)); 
        if 1-stats.nct.cdf(stats.t.ppf(0.975,df),df,ncp)>=0.8: break
    print(f'Mn (ICP-MS) olfactory bulb: detect 1.5-fold increase, assumed CV {int(cv*100)}%, 80% power: n/group = {n}')
