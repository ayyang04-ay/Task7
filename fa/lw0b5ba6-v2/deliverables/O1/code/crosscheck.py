import pandas as pd, numpy as np
V = pd.read_csv('/tmp/work/tidy/values.csv')
g = lambda blk, grp, an=None, t=None: V[(V.block==blk)&(V.group==grp)&((V.analyte==an) if an else True)&((V.time==t) if t else True)].sort_values('animal')
print('=== A. S09-A panels vs log10(S01-A) ===')
s01 = V[V.block=='S01-A']
for panel in ['S09-A panel1[A:U]','S09-A panel2[X:AS]']:
    p = V[(V.block==panel)&(V.analyte=='Ifnb1')]
    for grp in ['PBS','CMP-204','PSLN-212','PSLN-R848','PSLN-212/R848','PSLN-344','PSLN-212(Y)']:
        vals = 10**p[p.group==grp].sort_values('animal').value.values
        src = 'Sham' if grp=='PBS' else grp
        for t in ['16h','72h']:
            ref = s01[(s01.group==src)&(s01.time==t)].value.values
            hits = sum(any(abs(v-r)<0.006 for r in ref) for v in vals)
            if hits: print(f'{panel:20s} {grp:14s} 10^values={np.round(vals,2)} match S01-A {src} {t}: {hits}/3')
print('\n=== B. IgG2a/IgG1 ratio: S03-B/F (as printed) vs S13 primary titres ===')
for (ratio_blk, g2a, g1) in [('S03-B','S13-A','S13-B'),('S03-F','S13-C','S13-D')]:
    prim = {grp: g(g2a,grp).value.values/g(g1,grp).value.values for grp in ['PSLN-212','PSLN-344','PSLN-212(Y)']}
    for grp in ['PSLN-212','PSLN-344','PSLN-212(Y)']:
        printed = g(ratio_blk, grp).value.values
        match = [k for k,v in prim.items() if np.allclose(v, printed, rtol=2e-3)]
        print(f'{ratio_blk} printed "{grp}": {np.round(printed,3)} -> equals S13 quotient of: {match}')
    for grp,v in prim.items(): print(f'   {g2a}/{g1} {grp}: {np.round(v,3)}  mean={v.mean():.2f}')
print('\n=== C. S04-B Tfh:Tfr vs (100-Foxp3)/Foxp3 ===')
for grp in ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']:
    f = g('S04-B Foxp3',grp).value.values; r = g('S04-B Tfh:Tfr',grp).value.values
    print(grp, 'max abs diff', np.abs((100-f)/f - r).max().round(6))
print('\n=== D. S01-B vs S08-C (same condition: PSLN-SRB, aged, 16h) ===')
for a,b in [('AECII/PSLN-SRB','AECII-PSLN-SRB'),('AECI/PSLN-SRB','AECI-PSLN-SRB')]:
    x = g('S01-B',a).value.values; y = g('S08-C',b).value.values
    print(a, x, 'mean', x.mean().round(2), '|', b, y, 'mean', y.mean().round(2))
print('S08-C AECII-PSLN-344-SRB', g('S08-C','AECII-PSLN-344-SRB').value.values, ' vs S01-B AECI/PSLN-SRB', g('S01-B','AECI/PSLN-SRB').value.values)
print('\n=== E. S08-A 20ug vs S01-A 16h (Ifnb1) ===')
for grp in ['CMP-204','PSLN-212','PSLN-344']:
    print(grp, 'S08-A 20ug', g('S08-A',grp,t='20ug').value.values, ' S01-A 16h', g('S01-A',grp,t='16h').value.values)
