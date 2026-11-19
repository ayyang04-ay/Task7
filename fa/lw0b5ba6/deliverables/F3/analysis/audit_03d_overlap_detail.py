import numpy as np, pandas as pd, itertools, collections
from psln_blocks import df
pd.set_option('display.width',250); pd.set_option('display.max_rows',500)
def overlap(b1,b2):
    a=df[df.block==b1]; b=df[df.block==b2]
    ka={(r.col_order,r.rep,r.time):(r.value,r.cell,r.group) for r in a.itertuples() if r.value!=100}
    kb={(r.col_order,r.rep,r.time):(r.value,r.cell,r.group) for r in b.itertuples() if r.value!=100}
    out=[]
    for k in sorted(set(ka)&set(kb), key=lambda x:(x[0],x[1],float(x[2]))):
        if round(ka[k][0],4)==round(kb[k][0],4):
            out.append((k[2],ka[k][2],ka[k][1],kb[k][2],kb[k][1],ka[k][0]))
    return out
for b1,b2 in [('S11-A','S11-B'),('S15-A','S15-M'),('S15-M','S15-O'),('S15-C','S15-M'),('S09-E','S09-G'),('S15-A','S15-O'),('S15-A','S15-B'),('S09-E','S15-C')]:
    o=overlap(b1,b2)
    print(f'\n=== {b1} vs {b2}: {len(o)} identical cells in identical positions')
    for x in o: print('   t=%s  %s %s  ==  %s %s   value=%s'%x)
