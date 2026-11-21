from load import *
import numpy as np, pandas as pd
from scipy import stats
def v(b,g,**kw):
    d = DF[(DF.block==b)&(DF.group==g)]
    for k,x in kw.items(): d = d[d[k]==x]
    return d.value.values
print("S09-A Ifnb1 (log10 fold) -> fold, both blocks labelled '16h', vs S01-A 16h and 72h (linear fold):")
gm = {'PSLN-212':'PSLN-212','PSLN-344':'PSLN-344','PSLN-212(y)':'PSLN-212(Y)','CMP-204':'CMP-204','PSLN-R848':'PSLN-R848','PSLN-212/R848':'PSLN-212/R848'}
rows=[]
for g9,g1 in gm.items():
    b1 = 10**v('S09-A_blk1',g9,analyte='Ifnb1'); b2 = 10**v('S09-A_blk2',g9,analyte='Ifnb1')
    a16 = v('S01-A_16h',g1); a72 = v('S01-A_72h',g1)
    rows.append(dict(group=g1, S09A_blk1_geo=stats.gmean(b1), S09A_blk2_geo=stats.gmean(b2), S01A_16h_geo=stats.gmean(a16), S01A_72h_geo=stats.gmean(a72)))
R=pd.DataFrame(rows).round(2); print(R.to_string(index=False))
x=np.log10(R.S09A_blk2_geo); print("\ncorr(log blk2, log S01-A 72h) r=%.3f ; corr(log blk2, log S01-A 16h) r=%.3f" % (np.corrcoef(x,np.log10(R.S01A_72h_geo))[0,1], np.corrcoef(x,np.log10(R.S01A_16h_geo))[0,1]))
x=np.log10(R.S09A_blk1_geo); print("corr(log blk1, log S01-A 16h) r=%.3f ; corr(log blk1, log S01-A 72h) r=%.3f" % (np.corrcoef(x,np.log10(R.S01A_16h_geo))[0,1], np.corrcoef(x,np.log10(R.S01A_72h_geo))[0,1]))
print("\nS01-B vs S08-C (alveolar epithelial SRB uptake, %):")
for b,g in [('S01-B','AECII/PSLN-SRB'),('S01-B','AECI/PSLN-SRB'),('S01-B','AECII/FreeSRB'),('S01-B','AECI/FreeSRB'),
            ('S08-C','AECII-PSLN-SRB'),('S08-C','AECII-PSLN-344-SRB'),('S08-C','AECI-PSLN-SRB'),('S08-C','AECI-PSLN-344-SRB')]:
    x=v(b,g); print(f"  {b} {g:22s} mean={x.mean():5.2f}  values={list(x)}")
print("\nS09-C day-12 weights, PSLN-212Y vs PSLN-344Y:")
d=DF[(DF.block=='S09-C')&(DF.day==12)]
print('  212Y:',list(d[d.group=='PSLN-212Y'].value)); print('  344Y:',list(d[d.group=='PSLN-344Y'].value))
