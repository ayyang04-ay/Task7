import pandas as pd, itertools, numpy as np
B=pd.read_csv('/tmp/work/tidy/bodyweight.csv')
B=B[B.day>0]
traj={}
for k,d in B.groupby(['block','group','animal']):
    traj[k]=dict(zip(d.day,d.value.round(4)))
res=[]
for a,b in itertools.combinations(traj,2):
    if a[0]==b[0] and a[1]==b[1]: continue
    ta,tb=traj[a],traj[b]
    common=[dd for dd in ta if dd in tb]
    same=[dd for dd in common if ta[dd]==tb[dd] and ta[dd]!=100.0]
    if len(same)>=3:
        res.append((a,b,len(same),len(common),same))
res.sort(key=lambda x:-x[2])
for a,b,s,c,days in res:
    print(f"{s}/{c} identical days {days}: {a} <-> {b}")
print(len(res))
