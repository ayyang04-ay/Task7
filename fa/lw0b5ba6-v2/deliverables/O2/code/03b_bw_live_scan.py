import pandas as pd, itertools, numpy as np
B=pd.read_csv('/tmp/work/tidy/bodyweight.csv')
def live_traj(d):
    d=d.sort_values('day'); days=d.day.tolist(); vals=d.value.round(4).tolist()
    # strip LOCF tail: trailing run of identical values (keep first of run)
    k=len(vals)-1
    while k>0 and vals[k]==vals[k-1]: k-=1
    return {dd:v for dd,v in zip(days[:k+1],vals[:k+1]) if dd>0}
traj={k:live_traj(d) for k,d in B.groupby(['block','group','animal'])}
# null: chance match rate for same-day live values between animals in *different* blocks
pairs=0; matches=0
rows=[]
for a,b in itertools.combinations(traj,2):
    if a[0]==b[0]: continue
    ta,tb=traj[a],traj[b]
    common=[dd for dd in ta if dd in tb]
    same=[dd for dd in common if ta[dd]==tb[dd]]
    pairs+=len(common); matches+=len(same)
    if len(same)>=3: rows.append(dict(a=f"{a[0]} {a[1]} #{a[2]}", b=f"{b[0]} {b[1]} #{b[2]}", n_same=len(same), n_common=len(common), days=same))
print(f"per-day chance match rate between different-block animals: {matches}/{pairs} = {matches/pairs:.4f}")
R=pd.DataFrame(rows).sort_values('n_same',ascending=False)
pd.set_option('display.width',200); pd.set_option('display.max_colwidth',80)
print(R.to_string(index=False))
# summarise by block pair
R['pa']=R.a.str.split(' ').str[0]; R['pb']=R.b.str.split(' ').str[0]
print(R.groupby(['pa','pb']).size())
R.to_csv('/tmp/work/tidy/bw_duplicate_trajectories.csv',index=False)
