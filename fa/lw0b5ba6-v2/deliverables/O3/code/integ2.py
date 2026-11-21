from load import *
import numpy as np, pandas as pd
from scipy.stats import gmean
def v(b,g): return DF[(DF.block==b)&(DF.group==g)]['value'].values
print("Consistency of S13 subclass labels with S03 total IgG (GMTs):")
for tot, a2, a1, lab in [('S03-A','S13-A','S13-B','CA09'),('S03-E','S13-C','S13-D','Aichi')]:
    for g in ['PSLN-212','PSLN-344','PSLN-212(Y)']:
        print(f"  {lab} {g:12s} total IgG GMT={gmean(v(tot,g)):8.0f} | S13 IgG2a GMT={gmean(v(a2,g)):7.0f} IgG1 GMT={gmean(v(a1,g)):7.0f} | IgG2a/IgG1 mean={np.mean(v(a2,g)/v(a1,g)):.2f}")
