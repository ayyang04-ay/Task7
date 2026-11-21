exec(open('pooled.py').read().split("aged_all = ")[0])
ywith = ['S03-I','S06-A','S06-B','S06-C','S06-E','S06-F','S06-G','S15-L','S15-N']
r = analyse('aged PSLN-212 vs young PSLN-212', ywith, g1='PSLN-212', g0='PSLN-212(Y)')
print(r)
import numpy as np, pandas as pd
v = pd.read_csv('values_corrected.csv')
a = v[(v.block=='S03-A')&(v.g=='PSLN-344')].value; b = v[(v.block=='S13-I')&(v.g=='PSLN-344')].value
print('boost ratio PSLN-344 CA09 IgG d28/d14 GM:', 10**(np.log10(b).mean()-np.log10(a).mean()))
