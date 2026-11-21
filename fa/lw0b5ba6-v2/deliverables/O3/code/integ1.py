from load import *
import numpy as np, pandas as pd
ws = wb
def vals(block, group):
    return DF[(DF.block==block)&(DF.group==group)].sort_values('cell')['value'].values
def vals_cells(block, group):
    d = DF[(DF.block==block)&(DF.group==group)]
    return d['value'].values, d['cell'].values
print("=== CHECK 1: S04-B Tfh:Tfr vs S04-B Foxp3+ (is ratio = (100-Tfr)/Tfr ?)")
for g in ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']:
    tfr,_ = vals_cells('S04-B_Tfr',g); rat,_ = vals_cells('S04-B_TfhTfr',g)
    print(f"  {g:12s} max|ratio-(100-Tfr)/Tfr| = {np.max(np.abs(rat-(100-tfr)/tfr)):.2e}")

print("\n=== CHECK 2: S03-B / S03-F quotient vs S13-A/B and S13-C/D raw subclass titres")
for qb, a2, a1 in [('S03-B','S13-A','S13-B'),('S03-F','S13-C','S13-D')]:
    print(' ', qb)
    for gq in ['PSLN-212','PSLN-344','PSLN-212(Y)']:
        q,_ = vals_cells(qb,gq)
        row=[]
        for gs in ['PSLN-212','PSLN-344','PSLN-212(Y)']:
            r = vals_cells(a2,gs)[0]/vals_cells(a1,gs)[0]
            row.append(f"vs S13 {gs}: max|diff|={np.max(np.abs(q-r)):.4f}")
        print(f"    printed '{gq}':  "+' ; '.join(row))
