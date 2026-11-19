import pandas as pd, numpy as np
rng = np.random.default_rng(1)
df = pd.read_csv('/tmp/work/tidy.csv')
s = df[df.event.notna() & (df.block!='S08-UNLABELLED')]
aged_blocks = ['S06-A','S06-B','S06-C','S06-D','S06-E','S06-F','S06-G','S15-L','S15-N']
for grp, excl in [('PSLN-212',['S06-C','S06-D']),('Sham',['S06-C','S06-D'])]:
    pool = s[(s.group==grp)&(s.block.isin(aged_blocks))&(~s.block.isin(excl))]
    outcomes = list(zip(pool.time, pool.event))
    target = sorted(zip(s[(s.block=='S06-C')&(s.group==grp)].time, s[(s.block=='S06-C')&(s.group==grp)].event))
    N=200000; hits=0; any_identical=0
    for _ in range(N):
        a = sorted([outcomes[i] for i in rng.integers(0,len(outcomes),7)])
        b = sorted([outcomes[i] for i in rng.integers(0,len(outcomes),7)])
        if a==b: any_identical+=1
    print(f'{grp}: pooled outcomes from {pool.block.nunique()} other aged blocks (n={len(pool)}); P(two independent groups of 7 have identical outcome multisets) ~ {any_identical/N:.4f}')
