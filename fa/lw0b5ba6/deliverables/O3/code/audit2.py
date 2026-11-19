import pandas as pd, numpy as np, itertools
C = pd.read_csv('/tmp/work/tidy/continuous.csv')
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500)

def vals(block, group, meas=None, time=None):
    d = C[(C.block == block) & (C.group == group)]
    if meas is not None:
        d = d[d.measurand == meas]
    if time is not None:
        d = d[d.time.astype(str) == str(time)]
    return d.sort_values('rep')['value'].values, d.sort_values('rep')['cell'].values

out = []
# ---------- A. S11-A vs S11-B positional identity ----------
a = C[C.block == 'S11-A'].set_index(['group', 'time', 'rep'])['value']
b = C[C.block == 'S11-B'].set_index(['group', 'time', 'rep'])['value']
j = pd.concat([a.rename('AM'), b.rename('Neut')], axis=1).dropna()
j['identical'] = np.isclose(j.AM, j.Neut)
print('S11-A (alveolar macrophage %) vs S11-B (neutrophil %) same animal position identical:',
      int(j.identical.sum()), 'of', len(j), f'({100*j.identical.mean():.0f}%)')
print(j.groupby(level=[0])['identical'].agg(['sum', 'size']))
print(j.groupby(level=[2])['identical'].agg(['sum', 'size']))
# control comparison: S11-A vs S11-D (NK), S11-B vs S11-D
d = C[C.block == 'S11-D'].set_index(['group', 'time', 'rep'])['value']
for nm, x, y in [('S11-A vs S11-D', a, d), ('S11-B vs S11-D', b, d)]:
    jj = pd.concat([x, y], axis=1).dropna()
    print(nm, 'identical:', int(np.isclose(jj.iloc[:, 0], jj.iloc[:, 1]).sum()), 'of', len(jj))
# how unusual? permutation-style null: compare S11-A against S11-B with rep positions shuffled within group/time
rng = np.random.default_rng(1)
null = []
jj = j.reset_index()
for it in range(2000):
    cnt = 0
    for (g, t), sub in jj.groupby(['group', 'time']):
        perm = rng.permutation(sub.Neut.values)
        cnt += np.isclose(sub.AM.values, perm).sum()
    null.append(cnt)
print('Null (within group/time shuffled) identical count: mean %.2f, 99.9th pct %.1f, max %d' %
      (np.mean(null), np.percentile(null, 99.9), np.max(null)))
# baseline day0 plausibility: AM and neutrophil day-0 means
print(j.reset_index().query('time==0').groupby('group')[['AM', 'Neut']].mean())

# ---------- B. S01-B vs S08-C ----------
print('\nS01-B vs S08-C shared values:')
for g1 in ['AECII/PSLN-SRB', 'AECI/PSLN-SRB']:
    v1, c1 = vals('S01-B', g1)
    for g2 in ['AECII-PSLN-SRB', 'AECII-PSLN-344-SRB', 'AECI-PSLN-SRB', 'AECI-PSLN-344-SRB']:
        v2, c2 = vals('S08-C', g2)
        sh = [(x, c1[i], c2[list(np.isclose(v2, x)).index(True)]) for i, x in enumerate(v1) if np.isclose(v2, x).any()]
        if sh:
            print(f'  S01-B {g1} {list(v1)}  <->  S08-C {g2} {list(v2)} : shared {sh}')

# ---------- C. S03-B/F (printed ratios) vs S13-A..D subclass titres ----------
print('\nS03-B / S03-F printed ratios vs quotients computed from S13 subclass titres:')
for (rb, a2, a1) in [('S03-B', 'S13-A', 'S13-B'), ('S03-F', 'S13-C', 'S13-D')]:
    for gq in ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']:
        q = vals(a2, gq)[0] / vals(a1, gq)[0]
        for gr in ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']:
            r = vals(rb, gr)[0]
            if np.allclose(q, r, rtol=1e-5):
                print(f'  {rb} printed "{gr}" == {a2}/{a1} quotient of "{gq}"  values={np.round(r,3)}')

# ---------- D. S04-B Tfh:Tfr vs Foxp3 ----------
print('\nS04-B Tfh:Tfr vs (100-Foxp3)/Foxp3:')
for g in ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']:
    f = vals('S04-B Foxp3', g)[0]; r = vals('S04-B Tfh:Tfr', g)[0]
    print(f'  {g}: max abs diff = {np.max(np.abs((100-f)/f - r)):.2e}')

# ---------- E. S09-A vs log10(S01-A) ----------
print('\nS09-A Ifnb1 (log10) vs log10 of S01-A Ifnb1:')
for blk in ['S09-A (cols A-V; printed 16h)', 'S09-A (cols X-AS; printed 16h)']:
    for g9, g1 in [('PBS', 'Sham'), ('CMP-204', 'CMP-204'), ('PSLN-212', 'PSLN-212'), ('PSLN-R848', 'PSLN-R848'),
                   ('PSLN-212/R848', 'PSLN-212/R848'), ('PSLN-344', 'PSLN-344'), ('PSLN-212(Y)', 'PSLN-212(Y)')]:
        x9, c9 = vals(blk, g9, meas='Lung Ifnb1 (log10 fold)')
        for t in ['16h', '72h']:
            x1, c1 = vals('S01-A', g1, time=t)
            l1 = np.round(np.log10(x1), 2)
            m = [(round(10**x, 2), c1[list(np.isclose(l1, round(x, 2), atol=0.006)).index(True)])
                 for x in x9 if np.isclose(l1, round(x, 2), atol=0.006).any()]
            if len(m) >= 2:
                print(f'  {blk[:22]} {g9:14s} matches S01-A {g1} {t}: {m}')
