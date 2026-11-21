"""QC 1: do derived blocks reproduce from their parent blocks, and under which labels?"""
import numpy as np, pandas as pd, itertools
import psln_blocks as P

def vec(bid, g):
    d = P.load(bid); return d[d.group == g].sort_values('rep')['value'].values

print('=== IgG2a/IgG1 quotient: S03-B vs S13-A / S13-B (CA09 H1N1) and S03-F vs S13-C / S13-D (Aichi H3N2)')
for quo, num, den in [('S03-B', 'S13-A', 'S13-B'), ('S03-F', 'S13-C', 'S13-D')]:
    gs = ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']
    calc = {g: vec(num, g) / vec(den, g) for g in gs}
    for gq in gs:
        q = vec(quo, gq)
        match = [g for g in gs if np.allclose(calc[g], q, rtol=2e-4)]
        print(f"  {quo} column printed '{gq}': mean {q.mean():.3f}  == per-animal {num}/{den} of group {match}")
    for g in gs:
        print(f"     recomputed {num}/{den} for {g}: per-animal {np.round(calc[g],3)}  mean {calc[g].mean():.2f}  geo-mean {np.exp(np.log(calc[g]).mean()):.2f}")

print('\n=== Tfh:Tfr quotient S04-B vs Foxp3+ fraction S04-B')
for g in P.G4:
    f = vec('S04-B Foxp3', g); q = vec('S04-B Tfh:Tfr', g)
    print(f"  {g}: (100-x)/x reproduces quotient: {np.allclose((100 - f) / f, q, rtol=1e-4)}")
print('   -> the quotient is an algebraic transform of one measurement, not an independent endpoint')

print('\n=== S04-A: ICOS-lo + ICOS-hi per animal')
for g in P.G4:
    print(f"  {g}: total Tfh% = {np.round(vec('S04-A ICOSlo', g) + vec('S04-A ICOShi', g), 2)}")

print('\n=== S09-A (log10) vs S01-A (linear): which timepoint does each S09-A panel reproduce?')
m16 = P.load('S01-A 16h').groupby('group')['value'].mean(); m72 = P.load('S01-A 72h').groupby('group')['value'].mean()
name = {'PBS': None, 'CMP-204': 'CMP-204', 'PSLN-212': 'PSLN-212', 'PSLN-R848': 'PSLN-R848', 'PSLN-212/R848': 'PSLN-212/R848', 'PSLN-344': 'PSLN-344', 'PSLN-212(y)': 'PSLN-212(Y)'}
for panel in ['S09-A[A:U] Ifnb1', 'S09-A[X:AS] Ifnb1']:
    d = P.load(panel); d['lin'] = 10 ** d['value']
    mm = d.groupby('group', sort=False)['lin'].mean()
    rows = []
    for g, v in mm.items():
        if name[g]:
            rows.append((g, round(v, 2), round(m16[name[g]], 2), round(m72[name[g]], 2)))
    t = pd.DataFrame(rows, columns=['group', 'S09-A mean (10^x)', 'S01-A 16h mean', 'S01-A 72h mean'])
    r16 = np.corrcoef(np.log10(t.iloc[:, 1]), np.log10(t.iloc[:, 2]))[0, 1]; r72 = np.corrcoef(np.log10(t.iloc[:, 1]), np.log10(t.iloc[:, 3]))[0, 1]
    rm16 = np.sqrt(np.mean((np.log10(t.iloc[:, 1]) - np.log10(t.iloc[:, 2])) ** 2)); rm72 = np.sqrt(np.mean((np.log10(t.iloc[:, 1]) - np.log10(t.iloc[:, 3])) ** 2))
    print(panel); print(t.to_string(index=False)); print(f"   log-scale RMSD vs 16h = {rm16:.3f}, vs 72h = {rm72:.3f}; r vs 16h = {r16:.3f}, r vs 72h = {r72:.3f}")

print('\n=== S08-A (20 ug row) vs S01-A 16h (aged) - is the dose series in aged animals, and what is "PSLN-344/R848"?')
d = P.load('S08-A'); d20 = d[d.x == 20].groupby('group', sort=False)['value'].mean()
for g, v in d20.items():
    print(f"  S08-A 20ug {g}: {v:.1f} | S01-A 16h aged: " + ', '.join(f"{k} {m16[k]:.1f}" for k in ['CMP-204', 'PSLN-212', 'PSLN-212/R848', 'PSLN-344']) + f" | young: PSLN-212(Y) {m16['PSLN-212(Y)']:.1f}, PSLN-344(Y) {m16['PSLN-344(Y)']:.1f}")

print('\n=== S01-B vs S08-C (same tracer, dose, timepoint, aged animals)')
for g in ['AECII/PSLN-SRB', 'AECI/PSLN-SRB']:
    print('  S01-B', g, vec('S01-B', g), 'mean %.2f' % vec('S01-B', g).mean())
for g in ['AECII-PSLN-SRB', 'AECII-PSLN-344-SRB', 'AECI-PSLN-SRB', 'AECI-PSLN-344-SRB']:
    print('  S08-C', g, vec('S08-C', g), 'mean %.2f' % vec('S08-C', g).mean())

print('\n=== S09-A Ifnb1 values are a subset of S01-A values (same group, same time point)?')
import tidy as _t
nm = {'PBS': 'Sham', 'CMP-204': 'CMP-204', 'PSLN-212': 'PSLN-212', 'PSLN-R848': 'PSLN-R848', 'PSLN-212/R848': 'PSLN-212/R848', 'PSLN-344': 'PSLN-344', 'PSLN-212(y)': 'PSLN-212(Y)'}
for panel, ref in [('S09-A[A:U] Ifnb1', 'S01-A 16h'), ('S09-A[X:AS] Ifnb1', 'S01-A 72h'), ('S09-A[X:AS] Ifnb1', 'S01-A 16h')]:
    hit = tot = 0
    for g, g2 in nm.items():
        a = 10 ** vec(panel, g); b = list(vec(ref, g2))
        for v in a:
            j = [i for i, w in enumerate(b) if abs(w - v) <= 0.006 + 0.002 * abs(w)]
            tot += 1
            if j: hit += 1; b.pop(j[0])
    print(f'  {panel} vs {ref}: {hit} of {tot} values found among the S01-A animals of the same group')
