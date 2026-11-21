import pandas as pd, numpy as np, itertools
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 2000); pd.set_option('display.max_colwidth', 120)
Q = pd.read_csv('quant_long.csv')
def vec(block, analyte=None, group=None, time=None):
    d = Q[Q.block==block]
    if analyte is not None: d = d[d.analyte.str.startswith(analyte)]
    if group is not None: d = d[d.group==group]
    if time is not None: d = d[d.time.astype(str)==str(time)]
    return d.sort_values('rep').value.values

print("=== 1. S09-A (log10) Ifnb1 back-transformed vs S01-A (linear) ===")
map_groups = {'PBS':'Sham','CMP-204':'CMP-204','PSLN-212':'PSLN-212','PSLN-R848':'PSLN-R848','PSLN-212/R848':'PSLN-212/R848','PSLN-344':'PSLN-344','PSLN-212(y)':'PSLN-212(Y)'}
for panel in ['panel1(A-U)','panel2(X-AS)']:
    for g9, g1 in map_groups.items():
        v9 = 10**vec('S09-A', 'Ifnb1', g9, panel)
        for t in ['16h','72h']:
            v1 = vec('S01-A', None, g1, t)
            match = [any(abs(x-y) < 0.006 for y in v1) for x in v9]
            if sum(match) >= 2:
                print(f"S09-A {panel} {g9:14s} 10^x = {np.round(v9,2)}  matches S01-A {t} '{g1}' {v1}  -> {sum(match)}/3 values")

print("\n=== 2. IgG2a/IgG1 ratio: recomputed from S13 raw titers vs S03-B / S03-F as labeled ===")
for (rb, a2, a1, virus) in [('S03-B','S13-A','S13-B','CA09 H1N1'), ('S03-F','S13-C','S13-D','Aichi H3N2')]:
    rec = {g: vec(a2, None, g)/vec(a1, None, g) for g in ['PSLN-212','PSLN-344','PSLN-212(Y)']}
    for glab in ['PSLN-212','PSLN-344','PSLN-212(Y)']:
        printed = vec(rb, None, glab)
        which = [g for g, r in rec.items() if np.allclose(r, printed, rtol=1e-4)]
        print(f"{rb} ({virus}) column labeled {glab:12s}: {np.round(printed,3)}  == recomputed ratio of group {which}")
    for g, r in rec.items():
        print(f"    recomputed {a2}/{a1} {g:12s}: {np.round(r,3)}  mean={r.mean():.2f} geomean={np.exp(np.log(r).mean()):.2f}")

print("\n=== 3. Tfh:Tfr (S04-B) vs (100-Tfr)/Tfr ===")
for g in ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']:
    tfr = vec('S04-B Foxp3', None, g); ratio = vec('S04-B Tfh:Tfr', None, g)
    print(g, np.allclose((100-tfr)/tfr, ratio, rtol=1e-4), np.round(ratio,2))

print("\n=== 4. S04-A: ICOS-lo + ICOS-hi totals ===")
for g in ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']:
    lo = vec('S04-A','Tfh ICOS-lo', g); hi = vec('S04-A','Tfh ICOS-hi', g)
    print(g, 'total Tfh%:', np.round(lo+hi,2), ' ICOS-hi fraction:', np.round(hi/(lo+hi),3))

print("\n=== 5. S08-C vs S01-B ===")
for g in ['AECII/PSLN-SRB','AECI/PSLN-SRB','AECII/FreeSRB','AECI/FreeSRB']:
    print('S01-B', g, vec('S01-B', None, g), 'mean', vec('S01-B', None, g).mean().round(2))
for g in ['AECII-PSLN-SRB','AECII-PSLN-344-SRB','AECI-PSLN-SRB','AECI-PSLN-344-SRB']:
    print('S08-C', g, vec('S08-C', None, g), 'mean', vec('S08-C', None, g).mean().round(2))

print("\n=== 6. S08-A 20ug vs S01-A 16h ===")
for g in ['CMP-204','PSLN-212','PSLN-344','PSLN-344/R848']:
    print('S08-A', g, {int(float(t)): np.round(vec('S08-A', None, g, t),2).tolist() for t in ['1','5','10','20','40']})
