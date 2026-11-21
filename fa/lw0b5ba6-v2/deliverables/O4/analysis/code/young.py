import pandas as pd, numpy as np
from scipy import stats
v = pd.read_csv('values_corrected.csv')
for blk,t,log,lab in [('S01-A_16h',None,True,'Ifnb1 16 h'),('S01-A_72h',None,True,'Ifnb1 72 h'),('S01-E','4',False,'CD11b+ DC d4'),('S01-F',None,False,'cDC1'),('S01-G',None,False,'cDC2'),('S02-C',None,False,'Ag+ DC in MLN'),('S02-E',None,False,'OT-I priming')]:
    d = v[v.block==blk]
    if t: d = d[d.time.astype(str)==t]
    a = d[d.g=='PSLN-344(Y)'].value; b = d[d.g=='PSLN-212(Y)'].value
    if log: a,b = np.log10(a), np.log10(b)
    p = stats.ttest_ind(a,b,equal_var=False)[1]
    eff = f"{10**(a.mean()-b.mean()):.2f}x" if log else f"{a.mean()-b.mean():+.2f} pts"
    ma = 10**a.mean() if log else a.mean(); mb = 10**b.mean() if log else b.mean()
    print(f"{lab:16s} young PSLN-344 {ma:6.2f} vs young PSLN-212 {mb:6.2f}  {eff}  p={p:.3f}  [{blk}]")
