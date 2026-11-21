import pandas as pd, numpy as np, warnings
from scipy import stats
warnings.filterwarnings('ignore')
pd.set_option('display.width', 300); pd.set_option('display.max_rows', 3000)
A = pd.read_csv('wt_animal_status.csv')
A['g'] = A.group.replace({'PSLN-212Y':'PSLN-212(Y)','PSLN-344Y':'PSLN-344(Y)'})
A['maxloss'] = 100 - A.nadir
# challenge blocks, aged BALB/c core
core = ['S13-F','S15-A','S15-B','S15-C','S15-D','S15-E','S15-F','S15-G']
t = A[A.block.isin(core)].groupby(['block','g'], sort=False).agg(n=('maxloss','size'), maxloss_all=('maxloss','mean'),
       maxloss_surv=('maxloss', lambda s: s[A.loc[s.index,'status']=='alive'].mean()), n_surv=('status', lambda s: (s=='alive').sum())).reset_index()
print(t.round(1).to_string())
# pooled among survivors: PSLN-344 aged vs PSLN-212(Y)
surv = A[A.block.isin(core) & (A.status=='alive')]
for g in ['PSLN-344','PSLN-212(Y)','PSLN-212']:
    x = surv[surv.g==g].maxloss
    print(g, 'survivors n=', len(x), 'mean max weight loss %.1f (SD %.1f), median %.1f' % (x.mean(), x.std(), x.median()))
a = surv[surv.g=='PSLN-344'].maxloss; b = surv[surv.g=='PSLN-212(Y)'].maxloss
print('PSLN-344 aged survivors vs young PSLN-212 survivors: diff %.1f pts, Welch p=%.2e, MWU p=%.2e' % (a.mean()-b.mean(), stats.ttest_ind(a,b,equal_var=False).pvalue, stats.mannwhitneyu(a,b).pvalue))
# heterosubtypic only (exclude S13-F)
s2 = surv[surv.block!='S13-F']
a = s2[s2.g=='PSLN-344'].maxloss; b = s2[s2.g=='PSLN-212(Y)'].maxloss
print('heterosubtypic only: PSLN-344 %.1f (n=%d) vs young %.1f (n=%d), p=%.2e' % (a.mean(), len(a), b.mean(), len(b), stats.ttest_ind(a,b,equal_var=False).pvalue))
s3 = surv[surv.block=='S13-F']
print('homologous (S13-F): PSLN-344 %.1f vs young %.1f' % (s3[s3.g=='PSLN-344'].maxloss.mean(), s3[s3.g=='PSLN-212(Y)'].maxloss.mean()))
# all animals (incl. non-survivors) max loss
al = A[A.block.isin(core)]
print(al.groupby('g').maxloss.agg(['mean','std','count']).round(1))
# young head-to-head S09
y = A[A.block.isin(['S09-C','S09-E','S09-G'])]
print(y.groupby(['block','g'], sort=False).maxloss.agg(['mean','std','count']).round(1))
a = y[y.g=='PSLN-344(Y)'].maxloss; b = y[y.g=='PSLN-212(Y)'].maxloss
print('young 344Y vs 212Y pooled max loss: %.1f vs %.1f, Welch p=%.3f' % (a.mean(), b.mean(), stats.ttest_ind(a,b,equal_var=False).pvalue))
# day-14 recovery in S09-G (d180 challenge): final weights
W = pd.read_csv('wt_long.csv')
for blk in ['S09-C','S09-E','S09-G']:
    f = W[(W.block==blk)&(W.day==14)].groupby('group').value.mean().round(1).to_dict()
    print(blk, 'day14 mean weight', f)
x = W[(W.block=='S09-G')&(W.day==14)]
print('S09-G d14: 344Y vs 212Y Welch p=', stats.ttest_ind(x[x.group=='PSLN-344Y'].value, x[x.group=='PSLN-212Y'].value, equal_var=False).pvalue)
# WT H5N1 S13-G
g = A[A.block=='S13-G']
print(g.groupby('g').agg(n=('maxloss','size'), maxloss=('maxloss','mean'), alive=('status', lambda s:(s=='alive').sum())).round(1))
# S15-H/I
g = A[A.block=='S15-I']; print(g.groupby('g').agg(n=('maxloss','size'), maxloss=('maxloss','mean'), alive=('status', lambda s:(s=='alive').sum())).round(1))
