import pandas as pd, numpy as np
from scipy import stats
B=pd.read_csv('/tmp/work/tidy/bodyweight.csv'); S=pd.read_csv('/tmp/work/tidy/survival.csv')
PAIR={'S15-A':'S06-A','S15-B':'S06-B','S15-C':'S06-C','S15-D':'S06-D','S15-E':'S06-E(d60)','S15-F':'S06-F(d60)','S15-G':'S06-G(d60)',
      'S15-I':'S15-H','S15-J':'S06-E(imprint)','S15-K':'S06-F(imprint)','S15-M':'S15-L','S15-O':'S15-N',
      'S09-C':'S09-B','S09-E':'S09-D','S09-G':'S09-F','S13-F':'S03-I','S13-G':'S03-J'}
rows=[]; anim=[]
for (blk,g),d in B.groupby(['block','group'],sort=False):
    if blk not in PAIR: continue
    last_day=d.day.max()
    for a,dd in d.groupby('animal'):
        dd=dd.sort_values('day'); v=dd.value.values; days=dd.day.values
        locf = len(v)>=3 and v[-1]==v[-2] and days[-1]==14
        dead = (days[-1] < 14) or locf
        # live values only (strip LOCF tail)
        k=len(v)-1
        while k>0 and v[k]==v[k-1]: k-=1
        live=v[:k+1]
        anim.append(dict(block=blk,group=g,animal=a,dead_inferred=dead,nadir=live[1:].min() if len(live)>1 else np.nan,
                         nadir_day=days[1:k+1][np.argmin(live[1:])] if len(live)>1 else np.nan, last_day=days[-1]))
A=pd.DataFrame(anim)
for (blk,g),d in A.groupby(['block','group'],sort=False):
    sb=PAIR[blk]; s=S[(S.block==sb)&(S.group==g)]
    surv_rec = f"{int((s.event==0).sum())}/{len(s)}" if len(s) else 'group absent in survival block'
    alive=d[~d.dead_inferred]
    rows.append(dict(bw_block=blk,survival_block=sb,group=g,n_weighed=len(d),survivors_by_weights=int((~d.dead_inferred).sum()),
                     survivors_by_survival_block=surv_rec,
                     nadir_survivors_mean=alive.nadir.mean() if len(alive) else np.nan,nadir_survivors_min=alive.nadir.min() if len(alive) else np.nan,
                     pct_survivors_gt15_loss=100*(alive.nadir<85).mean() if len(alive) else np.nan))
R=pd.DataFrame(rows)
R['concordant']=R.apply(lambda r: (str(r.survivors_by_weights)+'/'+str(r.n_weighed))==r.survivors_by_survival_block,axis=1)
pd.set_option('display.width',250)
print(R.round(1).to_string(index=False))
R.to_csv('/tmp/work/tables/bodyweight_vs_survival.csv',index=False)
A.to_csv('/tmp/work/tables/bodyweight_animals.csv',index=False)
# survivors' morbidity: PSLN-344 vs PSLN-212(Y) in aged day-14/day-3/day-60 blocks (clean S15-A,B,C,E,F,G)
clean=['S15-A','S15-B','S15-C','S15-E','S15-F','S15-G']
a=A[A.block.isin(clean)&(A.group=='PSLN-344')&(~A.dead_inferred)].nadir; y=A[A.block.isin(clean)&(A.group=='PSLN-212(Y)')&(~A.dead_inferred)].nadir
print(f"\nSurvivor nadir (clean aged blocks): PSLN-344 mean {a.mean():.1f}% (n={len(a)}), young PSLN-212(Y) {y.mean():.1f}% (n={len(y)}); diff {a.mean()-y.mean():.1f} pp, t-test p={stats.ttest_ind(a,y).pvalue:.4f}")
