from load import *
import numpy as np, pandas as pd
from scipy.stats import poisson
tc = DF[DF['day'].notna() & DF['animal_col'].notna()].copy()
tc['day'] = pd.to_numeric(tc['day'], errors='coerce')
bw_blocks = [b for b in tc.block.unique() if 'body weight' in tc[tc.block==b].measurand.iloc[0]]
fresh = {}
for (b,g,c), d in tc[tc.block.isin(bw_blocks)].groupby(['block','group','animal_col']):
    s = d.set_index('day')['value'].sort_index()
    prev = s.shift(1)
    f = s[(s.index!=0) & ~(np.isclose(s, prev))]
    fresh[(b,g,c)] = f
keys = list(fresh); n=len(keys)
days = [2,4,6,8,10,12,14]
# per-day empirical match probability across all cross-block pairs
M = {d:[0,0] for d in days}
counts_aligned=[]; counts_shift=[]
rng = np.random.default_rng(0)
for i in range(n):
    for j in range(i+1,n):
        if keys[i][0]==keys[j][0]: continue  # cross-block only
        a,b = fresh[keys[i]], fresh[keys[j]]
        k=0
        for d in days:
            if d in a.index and d in b.index:
                M[d][1]+=1
                if abs(a[d]-b[d])<1e-9: M[d][0]+=1; k+=1
        counts_aligned.append(k)
        # misaligned control: compare a at day d with b at day d+2 (shifted)
        k2=0
        for d in days[:-1]:
            d2=d+2
            if d in a.index and d2 in b.index and abs(a[d]-b[d2])<1e-9: k2+=1
        counts_shift.append(k2)
print("n animal columns:",n)
for d in days: print(f"day {d:2d}: P(identical fresh value, cross-block pair) = {M[d][0]}/{M[d][1]} = {M[d][0]/max(M[d][1],1):.4f}")
ca = np.array(counts_aligned); cs=np.array(counts_shift)
print("\nPairs by number of identical fresh values (aligned days) vs misaligned control (day d vs d+2):")
for k in range(0,8):
    print(f"  k={k}: aligned {np.sum(ca==k):6d}   misaligned {np.sum(cs==k):6d}")
# expected count of pairs with >=k matches under independence (Poisson approx, per-pair lambda from per-day p)
p = np.mean([M[d][0]/M[d][1] for d in days])
from scipy.stats import binom
npairs = len(ca)
for k in [3,4,5,6]:
    print(f"Expected #pairs with >=%d matches by chance (binomial, 7 days, p=%.4f): %.4f ; observed aligned: %d" % (k,p,npairs*binom.sf(k-1,7,p), np.sum(ca>=k)))
