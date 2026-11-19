"""Recomputation cross-checks between blocks that should be arithmetically linked."""
from paths import TABLES, FIGS, OUT as OUTDIR, BUILD, PANDOC
import pandas as pd, numpy as np, itertools, psln_blocks as pb
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 3000)
df = pb.tidy()
def vals(block, group, analyte=None, x=None):
    t = df[(df.block == block) & (df.group == group)]
    if analyte is not None: t = t[t.analyte.str.contains(analyte, regex=False)]
    if x is not None: t = t[t.x.astype(str) == str(x)]
    return t.sort_values('rep').value.to_numpy(float)

out = []
print('=== A. S03-B / S03-F (IgG2a/IgG1 ratio) recomputed from S13-A..D subclass titres ===')
for ratio_blk, g2a_blk, g1_blk, strain in [('S03-B', 'S13-A', 'S13-B', 'CA09 H1N1'), ('S03-F', 'S13-C', 'S13-D', 'Aichi H3N2')]:
    comp = {g: vals(g2a_blk, g) / vals(g1_blk, g) for g in ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']}
    printed = {g: vals(ratio_blk, g) for g in ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']}
    for gp, pv in printed.items():
        match = [gc for gc, cv in comp.items() if np.allclose(cv, pv, rtol=2e-3)]
        print(f'{ratio_blk} ({strain}) column printed as {gp:12s}: values {np.round(pv,3)}  == {g2a_blk}/{g1_blk} computed for group: {match}')
        out.append(dict(check='IgG2a/IgG1 ratio vs subclass titres', block=ratio_blk, printed_label=gp, matches_computed_group=';'.join(match),
                        printed_mean=pv.mean(), note=''))
    for gc, cv in comp.items():
        print(f'    computed {g2a_blk}/{g1_blk} {gc:12s}: {np.round(cv,3)}  mean {cv.mean():.2f}')

print('\n=== B. S04-B Tfh:Tfr vs S04-B Foxp3+ (is ratio = (100-Tfr)/Tfr ?) and vs S04-A Tfh ===')
for g in ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']:
    tfr = vals('S04-B Foxp3+', g); ratio = vals('S04-B Tfh:Tfr', g)
    lo = vals('S04-A', g, 'ICOS-low'); hi = vals('S04-A', g, 'ICOS-high')
    print(f'{g:12s} Tfr {tfr}  ratio {np.round(ratio,3)}  (100-Tfr)/Tfr {np.round((100-tfr)/tfr,3)}  match={np.allclose(ratio,(100-tfr)/tfr,rtol=2e-3)}'
          f' | S04-A ICOS-lo+hi sums {np.round(lo+hi,2)}')

print('\n=== C. S09-A Ifnb1 rows vs S01-A (10**log10 values vs linear fold) ===')
s01 = {(g, h): vals('S01-A', g, x=h) for g in ['Sham', 'CMP-204', 'PSLN-212', 'PSLN-R848', 'PSLN-212/R848', 'PSLN-344', 'PSLN-212(Y)'] for h in ['16h', '72h']}
for blk in ['S09-A (cols A-U)', 'S09-A (cols X-AS)']:
    for g in ['PBS', 'CMP-204', 'PSLN-212', 'PSLN-R848', 'PSLN-212/R848', 'PSLN-344', 'PSLN-212(y)']:
        v = 10 ** vals(blk, g, 'Ifnb1')
        hits = []
        for (g1, h), ref in s01.items():
            n = sum(any(abs(a - b) / b < 0.006 for b in ref) for a in v)
            if n >= 2: hits.append(f'{g1}@{h} ({n}/3 values)')
        print(f'{blk:18s} {g:14s} 10^x = {np.round(v,2)}  -> matches S01-A: {hits}')
        out.append(dict(check='S09-A Ifnb1 vs S01-A', block=blk, printed_label=g, matches_computed_group=';'.join(hits), printed_mean=v.mean(), note=''))

print('\n=== D. S08-A 20 ug row vs S01-A 16 h (same dose, same readout) ===')
for g in ['CMP-204', 'PSLN-212', 'PSLN-344']:
    a = vals('S08-A', g, x=20); b16 = vals('S01-A', g, x='16h')
    by = vals('S01-A', g.replace('PSLN-212', 'PSLN-212(Y)').replace('PSLN-344', 'PSLN-344(Y)'), x='16h') if g != 'CMP-204' else None
    print(f'{g:10s} S08-A@20ug {a} mean {a.mean():.1f} | S01-A aged 16h mean {b16.mean():.1f}' + (f' | S01-A young 16h mean {by.mean():.1f}' if by is not None else ''))

print('\n=== E. S01-B vs S08-C (SRB uptake; same measurand for PSLN-SRB in aged animals at 16 h) ===')
for g in ['AECII/PSLN-SRB', 'AECI/PSLN-SRB', 'AECII/FreeSRB', 'AECI/FreeSRB']:
    v = vals('S01-B', g); print(f'S01-B {g:20s} {v} mean {v.mean():.2f}')
for g in ['AECII-PSLN-SRB', 'AECII-PSLN-344-SRB', 'AECI-PSLN-SRB', 'AECI-PSLN-344-SRB']:
    v = vals('S08-C', g); print(f'S08-C {g:20s} {v} mean {v.mean():.2f}')

print('\n=== F. S14-A / S05-F / S05-G (IFNg+ CD8, same immunisation) group means ===')
for blk in ['S05-F', 'S05-G', 'S14-A H1N1', 'S14-A H3N2']:
    print(blk, {g: round(vals(blk, g).mean(), 2) for g in ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']})

print('\n=== G. S11-A vs S11-B value identity ===')
a = df[df.block == 'S11-A'].copy(); b = df[df.block == 'S11-B'].copy()
a['pos'] = a.cell.str.replace(r'\d+$', '', regex=True) + '@' + a.x.astype(str); b['pos'] = b.cell.str.replace(r'\d+$', '', regex=True) + '@' + b.x.astype(str)
m = a.merge(b, on=['group', 'x', 'rep'], suffixes=('_A', '_B'))
m['same'] = m.value_A == m.value_B
print('identical values at the same group/day/animal position:', int(m.same.sum()), 'of', len(m))
print(m.groupby(['group', 'rep']).same.sum().unstack())
pd.DataFrame(out).to_csv(TABLES + 'T4_label_crosschecks.csv', index=False)
