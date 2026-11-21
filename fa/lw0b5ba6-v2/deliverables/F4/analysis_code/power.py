import numpy as np, pandas as pd
from scipy import stats
from itertools import product
Q = pd.read_csv('quant_long.csv')
def fisher_power(p1, p2, n, alpha=0.05):
    """exact power of two-sided Fisher test, equal n per arm"""
    pw = 0
    k = np.arange(n+1)
    pm1 = stats.binom.pmf(k, n, p1); pm2 = stats.binom.pmf(k, n, p2)
    for a in range(n+1):
        for b in range(n+1):
            if pm1[a]*pm2[b] < 1e-12: continue
            p = stats.fisher_exact([[a, n-a],[b, n-b]])[1]
            if p < alpha: pw += pm1[a]*pm2[b]
    return pw
print("Fisher exact power (two-sided alpha 0.05), survival p1 vs p2, n per arm")
for p1, p2 in [(0.80,0.10),(0.80,0.20),(0.80,0.30),(0.80,0.40),(0.80,0.50),(0.85,0.30)]:
    out=[]
    for n in [7,8,10,12,14,15,16,18,20,24]:
        out.append((n, round(fisher_power(p1,p2,n),2)))
    need = next((n for n,pw in out if pw>=0.8), None)
    print(f"  {p1:.2f} vs {p2:.2f}: ", out, " -> n for >=80% power:", need)
# SD of log10 titers within groups (our data)
print("\nwithin-group SD of log10 titers (our data):")
for blk in ['S03-A','S03-C','S03-D','S03-E','S03-G','S03-H']:
    d = Q[(Q.block==blk)&(Q.group.isin(['PSLN-344','PSLN-212(Y)','PSLN-212']))]
    sds = d.groupby('group').value.apply(lambda v: np.log10(v.replace(0,5)).std(ddof=1)).round(3).to_dict()
    print(' ', blk, sds)
def n_ttest(delta, sd, alpha=0.05, power=0.8):
    from scipy.stats import nct, t
    for n in range(3, 500):
        df = 2*n-2; ncp = delta/(sd*np.sqrt(2/n)); tc = t.ppf(1-alpha/2, df)
        pw = 1 - nct.cdf(tc, df, ncp) + nct.cdf(-tc, df, ncp)
        if pw >= power: return n
print("\nn per arm to detect fold-difference in GMT (log10 SD=0.30):", {f"{f}x": n_ttest(np.log10(f), 0.30) for f in [1.5,2,3,4]})
print("n per arm to detect fold-difference in GMT (log10 SD=0.25):", {f"{f}x": n_ttest(np.log10(f), 0.25) for f in [1.5,2,3,4]})
print("n per arm to detect difference in max weight loss (SD 3.7 pts):", {f"{d} pts": n_ttest(d, 3.7) for d in [3,4,5,6]})
# upper bound implications of 0 events in small groups ("rule of three")
for n in [5,7,10,21,49,56]:
    print(f"0 events in n={n}: one-sided 95% upper bound on event rate = {100*(1-0.05**(1/n)):.0f}%")
