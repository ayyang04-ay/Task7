import pandas as pd, numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportion_confint
B = pd.read_csv('/tmp/work/tidy/bw.csv'); T = pd.read_csv('/tmp/work/tidy/tte.csv'); V = pd.read_csv('/tmp/work/tidy/values.csv')
# 1. S15-I combination arm vs S15-C PSLN-344
a = B[(B.block=='S15-C')&(B.group=='PSLN-344')&(B.day>0)].pivot(index='day',columns='animal',values='value')
b = B[(B.block=='S15-I')&(B.group=='3d Vaccine+PSLN-344')&(B.day>0)].pivot(index='day',columns='animal',values='value')
eq = (a.round(3)==b.round(3))
print('S15-I combo vs S15-C PSLN-344 identical cells by day:\n', eq.sum(axis=1).to_string(), '\n total', int(eq.values.sum()), 'of', eq.size)
print('days 2-12 identical:', int(eq.loc[2:12].values.sum()), 'of', eq.loc[2:12].size)
# 2. background mortality in unchallenged aged controls
u = T[T.group=='Untreated']; s=int((u.event==1).sum()); n=len(u)
lo,hi = proportion_confint(s,n,method='beta'); print(f'\nUntreated (unchallenged) aged deaths: {s}/{n} = {100*s/n:.0f}% (95% CI {100*lo:.0f}-{100*hi:.0f}%)', u[u.event==1][['block','time','cell_time']].values.tolist())
ub = B[(B.group=='Untreated')]
for blk,d in ub.groupby('block'):
    piv = d.pivot(index='animal',columns='day',values='value'); flat = piv[(piv[14.0]==piv[12.0])&(piv[12.0]==piv[10.0])]
    print(blk,'flat-lined untreated animals (weight at flat-line):', flat[14.0].tolist())
# 3. CDN-1807 (PSLN-212) vs cGAMP (CMP-204) in aged
def gm(v): v=np.where(v<=0,5,v); return 2**np.mean(np.log2(v))
for blk,an in [('S03-A','IgG CA09 H1N1'),('S03-C','HAI CA09 H1N1'),('S03-D','Neut CA09 H1N1'),('S03-E','IgG Aichi H3N2'),('S03-G','HAI Aichi H3N2'),('S03-H','Neut Aichi H3N2'),('S13-I','IgG CA09 H1N1 post-boost'),('S13-J','IgG Aichi H3N2 post-boost')]:
    x = V[(V.block==blk)&(V.group=='PSLN-212')].value.values; y = V[(V.block==blk)&(V.group=='CMP-204')].value.values; z=V[(V.block==blk)&(V.group=='PSLN-344')].value.values
    p = stats.ttest_ind(np.log2(np.where(x<=0,5,x)),np.log2(np.where(y<=0,5,y)),equal_var=False).pvalue
    print(f'{blk} {an}: GMT PSLN-212 {gm(x):.0f} vs CMP-204 {gm(y):.0f} (ratio {gm(x)/gm(y):.1f}, p={p:.3f}); PSLN-344 {gm(z):.0f}')
# 4. PSLN-212 vs sham in aged (is PSLN-212 active at all?)
for blk in ['S03-A','S03-C','S03-E','S03-G','S03-K','S05-F','S05-I']:
    x = V[(V.block==blk)&(V.group=='PSLN-212')].value.values; y = V[(V.block==blk)&(V.group=='Sham')].value.values
    print(blk, 'PSLN-212 mean', round(x.mean(),2), 'Sham mean', round(y.mean(),2), 'p', round(stats.ttest_ind(x,y,equal_var=False).pvalue,4))
# 5. S08-D missing animal
d = B[(B.block=='S08-D')&(B.group=='PSLN-212/R848')].pivot(index='animal',columns='day',values='value'); print('\nS08-D PSLN-212/R848:\n', d.to_string())
