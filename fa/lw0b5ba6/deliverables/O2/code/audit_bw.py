import pandas as pd, numpy as np, itertools
b=pd.read_csv('bodyweight.csv')
b=b[b.day>0].copy()
b['hp']=b.value.apply(lambda x: abs(round(x,1)-x)>1e-6)   # more than 1 decimal place => computed from raw weights
print("high-precision (>1 dp) bw values:",b.hp.sum(),"of",len(b))
print(b[b.hp].groupby(['block','group']).size().to_string())
# 1) exact identical high-precision values in different block/group/animal
hp=b[b.hp].copy(); hp['r']=hp.value.round(5)
ex=hp.groupby('r').filter(lambda d: len(d.drop_duplicates(['block','group','animal']))>1)
print("\n=== exact identical high-precision values across different animals ===")
for r,d in ex.groupby('r'):
    print(r, list(zip(d.block,d.group,d.animal,d.day,d.cell)))
# 2) offset copies: same fractional part after removing multiples of 0.1
hp['frac']=((hp.value*10)%1).round(4)   # fractional part below 0.1 resolution
hp=hp[(hp.frac>0.0005)&(hp.frac<0.9995)]
print("\n=== shared sub-0.1 fractional signature across different animals (offset copies) ===")
n=0
for f,d in hp.groupby('frac'):
    dd=d.drop_duplicates(['block','group','animal','day'])
    if dd[['block','group','animal']].drop_duplicates().shape[0]>1:
        n+=1
        print(f, list(zip(dd.block,dd.group,dd.animal,dd.day,dd.value.round(5),dd.cell)))
print("n signatures shared:",n)
