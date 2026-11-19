import pandas as pd, numpy as np
t=pd.read_csv('tidy.csv')
def vec(b,g,**kw):
    d=t[(t.block==b)&(t.group==g)]
    for k,v in kw.items(): d=d[d[k].astype(str)==v]
    return d.sort_values('rep').value.values, list(d.sort_values('rep').cell)
print("=== S03-B / S03-F (IgG2a/IgG1 quotient) vs recomputation from S13-A..D ===")
for qb,num,den in [('S03-B','S13-A','S13-B'),('S03-F','S13-C','S13-D')]:
    for g13 in ['PSLN-212','PSLN-344','PSLN-212(Y)']:
        a,_=vec(num,g13); b,_=vec(den,g13); ratio=a/b
        for gq in ['PSLN-212','PSLN-344','PSLN-212(Y)']:
            q,c=vec(qb,gq)
            if np.allclose(q,ratio,atol=1e-4):
                print(f"  {qb} column labelled '{gq}' ({c[0]}..{c[-1]}) == {num}/{den} ratio for '{g13}'   mean ratio {ratio.mean():.2f}")
print("\n=== S04-B Tfh:Tfr vs (100 - Tfr%)/Tfr% ===")
for g in ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']:
    tfr,_=vec('S04-B_Tfr',g); q,_=vec('S04-B_TfhTfr',g)
    print(f"  {g:12s} reported {np.round(q,3)}  recomputed {(np.round((100-tfr)/tfr,3))}  match={np.allclose(q,(100-tfr)/tfr,atol=1e-4)}")
print("\n=== S09-A second panel (labelled 16h) vs S01-A 16h and 72h (Ifnb1) ===")
rows=[]
for g in ['CMP-204','PSLN-212','PSLN-R848','PSLN-212/R848','PSLN-344','PSLN-212(Y)']:
    p1,_=vec('S09-A_blk1(B:V)',g,analyte='Ifnb1'); p2,_=vec('S09-A_blk2(Y:AS)',g,analyte='Ifnb1')
    a16,_=vec('S01-A_16h',g); a72,_=vec('S01-A_72h',g)
    rows.append(dict(group=g,S09A_panel1_fold=10**p1.mean(),S09A_panel2_fold=10**p2.mean(),S01A_16h_gm=np.exp(np.log(a16).mean()),S01A_72h_gm=np.exp(np.log(a72).mean())))
r=pd.DataFrame(rows); print(r.round(2).to_string(index=False))
for c1 in ['S09A_panel1_fold','S09A_panel2_fold']:
    for c2 in ['S01A_16h_gm','S01A_72h_gm']:
        x=np.log10(r[c1]); y=np.log10(r[c2])
        print(f"  {c1} vs {c2}: Pearson r(log)={np.corrcoef(x,y)[0,1]:.3f}; mean |log10 diff|={np.mean(np.abs(x-y)):.3f}")
