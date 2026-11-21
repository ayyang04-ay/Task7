from loadcsv import *
import numpy as np, pandas as pd
from scipy import stats
d = DF[DF.block=='S09-A_blk1'].copy()   # 16h (verified against S01-A 16h)
d72 = DF[DF.block=='S09-A_blk2'].copy() # labelled 16h; verified = 72h
groups=['PBS','CMP-204','PSLN-212','PSLN-R848','PSLN-212/R848','PSLN-344','PSLN-212(y)']
rows=[]
for an in ['Ifnb1','Il6','Ccl2','Ccl3','Ccl5','Tnf','Il10']:
    r={'analyte':an}
    for g in groups:
        x=d[(d.analyte==an)&(d.group==g)].value.values
        r[g]=f"{10**x.mean():.1f}"
    a=d[(d.analyte==an)&(d.group=='PSLN-212')].value.values; c=d[(d.analyte==an)&(d.group=='PSLN-344')].value.values
    y=d[(d.analyte==an)&(d.group=='PSLN-212(y)')].value.values; s=d[(d.analyte==an)&(d.group=='PBS')].value.values
    t=stats.ttest_ind(c,a,equal_var=False)
    r['344/212 fold']=f"{10**(c.mean()-a.mean()):.1f}x"; r['p (Welch, log)']=f"{t.pvalue:.2g}"
    r['restoration vs young']=f"{(c.mean()-s.mean())/(y.mean()-s.mean())*100:.0f}%"
    a7=d72[(d72.analyte==an)&(d72.group=='PSLN-212')].value.values; c7=d72[(d72.analyte==an)&(d72.group=='PSLN-344')].value.values; y7=d72[(d72.analyte==an)&(d72.group=='PSLN-212(y)')].value.values
    r['72h: 212 / 344 / young']=f"{10**a7.mean():.1f} / {10**c7.mean():.1f} / {10**y7.mean():.1f}"
    rows.append(r)
R=pd.DataFrame(rows); pd.set_option('display.width',300)
print("S09-A lung transcript panel, 16h (geometric mean fold vs untreated; n=3):"); print(R.to_string(index=False))
R.to_csv('/tmp/work/s09a_panel.csv',index=False)
# R848 signature: Tnf & Il10 vs IFN
print("\nR848 arms: Tnf/Il10 vs Ifnb1 (16h):")
for g in ['PSLN-R848','PSLN-212/R848','PSLN-344','PSLN-212(y)']:
    f=lambda an: 10**d[(d.analyte==an)&(d.group==g)].value.mean()
    print(f"  {g:14s} Ifnb1 {f('Ifnb1'):6.1f}  Tnf {f('Tnf'):6.1f}  Il10 {f('Il10'):6.1f}  Tnf/Ifnb1 ratio {f('Tnf')/f('Ifnb1'):.2f}")
