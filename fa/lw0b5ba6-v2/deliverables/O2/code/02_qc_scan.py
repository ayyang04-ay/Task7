"""02_qc_scan.py -- systematic integrity scan of the tidy data."""
import pandas as pd, numpy as np, itertools
C=pd.read_csv('/tmp/work/tidy/continuous.csv'); S=pd.read_csv('/tmp/work/tidy/survival.csv'); B=pd.read_csv('/tmp/work/tidy/bodyweight.csv')
C['time']=C['time'].astype(str)
out=[]
# 1) positional identical replicate values between different (block/measurand/time/group) vectors
vecs={}
for k,d in C.groupby(['block','measurand','time','group'],sort=False):
    vecs[k]=d.sort_values('rep')['value'].round(6).tolist()
keys=list(vecs)
print("=== (1) vectors sharing >=2 identical values at the same replicate position (different block/measurand/time)")
for a,b in itertools.combinations(keys,2):
    va,vb=vecs[a],vecs[b]
    n=min(len(va),len(vb))
    if n<3: continue
    same=sum(1 for i in range(n) if va[i]==vb[i] and va[i] not in (0.0,100.0))
    if same>=2 and (a[0],a[1],a[2])!=(b[0],b[1],b[2]):
        print(f"  {same}/{n} same: {a} <-> {b}")
# 1b) within same block+measurand+time: different groups sharing values
print("\n=== (1b) identical values across different groups within a block/timepoint")
for a,b in itertools.combinations(keys,2):
    if (a[0],a[1],a[2])==(b[0],b[1],b[2]):
        va,vb=vecs[a],vecs[b]; n=min(len(va),len(vb))
        same=sum(1 for i in range(n) if va[i]==vb[i])
        if same>=2: print(f"  {same}/{n}: {a} <-> {b}")
# 2) survival: identical (time,event) multisets between different blocks
print("\n=== (2) survival group vectors identical across blocks")
sv={}
for k,d in S.groupby(['block','group'],sort=False):
    sv[k]=tuple(sorted(zip(d.time.fillna(-1),d.event)))
for a,b in itertools.combinations(sv,2):
    if a[0]!=b[0] and sv[a]==sv[b] and any(e==1 for _,e in sv[a]):
        print(f"  identical with events: {a} <-> {b}: {sv[a]}")
# whole-block identity
blocks=S.block.unique()
for a,b in itertools.combinations(blocks,2):
    ga=S[S.block==a].groupby('group').apply(lambda d: tuple(sorted(zip(d.time.fillna(-1),d.event))))
    gb=S[S.block==b].groupby('group').apply(lambda d: tuple(sorted(zip(d.time.fillna(-1),d.event))))
    if set(ga.index)==set(gb.index) and all(ga[g]==gb[g] for g in ga.index):
        print(f"  WHOLE BLOCK IDENTICAL: {a} == {b}")
# 3) body weight: identical day-rows across groups
print("\n=== (3) body weight: identical day-vectors between groups/blocks (excluding day 0)")
bv={}
for k,d in B[B.day>0].groupby(['block','group','day'],sort=False):
    bv[k]=tuple(d.sort_values('animal').value.round(4))
for a,b in itertools.combinations(bv,2):
    if len(bv[a])>=4 and bv[a]==bv[b]:
        print(f"  {a} == {b}: {bv[a]}")
# partial: >=4 identical per-animal positions
for a,b in itertools.combinations(bv,2):
    va,vb=bv[a],bv[b]; n=min(len(va),len(vb))
    same=sum(1 for i in range(n) if va[i]==vb[i])
    if same>=3 and va!=vb and not (a[0]==b[0] and a[1]==b[1]):
        print(f"  partial {same}/{n}: {a} <-> {b}")
