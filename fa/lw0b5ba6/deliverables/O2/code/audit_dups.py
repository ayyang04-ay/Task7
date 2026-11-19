import pandas as pd, numpy as np, itertools
t=pd.read_csv('tidy.csv'); s=pd.read_csv('survival.csv'); b=pd.read_csv('bodyweight.csv')
pd.set_option('display.width',250); pd.set_option('display.max_rows',500); pd.set_option('display.max_colwidth',60)

print("=== 1. Identical survival vectors (sorted day/event multiset) across blocks ===")
sv = s.groupby(['block','group']).apply(lambda d: tuple(sorted(zip(d.day.fillna(-1), d.event)))).reset_index(name='vec')
dup = sv.groupby('vec').filter(lambda d: d.block.nunique()>1)
for vec, d in dup.groupby('vec'):
    if all(e==0 for _,e in vec): 
        continue  # all-censored vectors are trivially identical
    print(list(zip(d.block,d.group)), vec)
# whole-block identity
blk = sv.groupby('block').apply(lambda d: tuple(sorted(zip(d.group,d.vec)))).reset_index(name='bvec')
for v_, d in blk.groupby('bvec'):
    if len(d)>1: print("WHOLE BLOCK IDENTICAL:", list(d.block))

print("\n=== 2. Continuous data: identical runs of >=3 consecutive replicate values between different block/group ===")
t['key']=t.block+'|'+t.group+'|'+t.get('time',pd.Series(['']*len(t))).fillna('').astype(str)+'|'+t.get('analyte',pd.Series(['']*len(t))).fillna('').astype(str)
vecs = {k: list(d.sort_values('rep').value.round(6)) for k,d in t.groupby('key')}
cells = {k: list(d.sort_values('rep').cell) for k,d in t.groupby('key')}
keys=list(vecs)
hits=[]
for a,bk in itertools.combinations(keys,2):
    va,vb=vecs[a],vecs[bk]
    # count shared values (multiset intersection) excluding trivial values like 0/100/10/14
    common=[x for x in set(va)&set(vb) if x not in (0,100,10,14,1)]
    if len(common)>=2:
        hits.append((a,bk,len(common),sorted(common)))
for h in sorted(hits,key=lambda x:-x[2]):
    print(h)
