import pandas as pd, numpy as np, itertools
df = pd.read_csv('/tmp/work/tidy.csv')
s = df[df.event.notna() & (df.block!='S08-UNLABELLED')]
vec = {}
for (b,g),x in s.groupby(['block','group']):
    v = tuple(sorted(zip(x.time.fillna(-1), x.event.astype(int))))
    vec[(b,g)] = v
print('Non-trivial identical survival vectors (>=3 deaths, not all on same day):')
for A,B in itertools.combinations(vec,2):
    va, vb = vec[A], vec[B]
    deaths = [t for t,e in va if e==1]
    if va==vb and len(deaths)>=3 and len(set(deaths))>=3:
        print(A, B, va)
