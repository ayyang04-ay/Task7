import pandas as pd, numpy as np
v = pd.read_csv('values.csv')
def norm(g): return g.replace('PSLN-212(y)','PSLN-212(Y)').replace('PBS','Sham')
for blk, ref in [('S09-A_blk1(cols A-U)','S01-A_16h'),('S09-A_blk2(cols X-AS)','S01-A_72h')]:
    a = v[(v.block==blk)&(v.analyte=='Ifnb1')]; r = v[v.block==ref]
    tot=match=0
    for g in a.group.unique():
        la = a[a.group==g]; lr = r[r.group==norm(g)]
        for _,x in la.iterrows():
            tot+=1
            hit = lr[np.isclose(np.log10(lr.value), x.value, atol=6e-4)]
            if len(hit): match+=1
            print(f"   {blk[:8]} {g:14s} {x.cell:8s} log10={x.value:.5f} -> 10^={10**x.value:7.2f}  match in {ref}: {list(hit.cell)}")
    print(f' {blk}: {match}/{tot} Ifnb1 values equal log10 of a {ref} value\n')
# S04-B Tfh:Tfr derivation
f = v[v.block=='S04-B_Foxp3'].reset_index(drop=True); t = v[v.block=='S04-B_TfhTfr'].reset_index(drop=True)
print('S04-B Tfh:Tfr == (100 - Foxp3%)/Foxp3% ?', np.allclose((100-f.value)/f.value, t.value, atol=1e-5))
# S03-B/F vs S13 subclass titres
for rb, a2, g1 in [('S03-B','S13-A','S13-B'),('S03-F','S13-C','S13-D')]:
    R = v[v.block==rb]; A = v[v.block==a2]; G = v[v.block==g1]
    for g in ['PSLN-212','PSLN-344','PSLN-212(Y)']:
        ratio = A[A.group==g].value.values / G[G.group==g].value.values
        for pg in ['PSLN-212','PSLN-344','PSLN-212(Y)']:
            if np.allclose(np.round(ratio,5), np.round(R[R.group==pg].value.values,5), atol=2e-5):
                print(f'  {rb}: raw {a2}/{g1} ratio for "{g}" == printed {rb} column labelled "{pg}"')
