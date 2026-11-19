import pandas as pd, numpy as np, itertools
bw = pd.read_csv('tidy_bodyweight.csv')
bw = bw[bw.value.notna() & (bw.day != 0)].copy()
bw['ndec'] = bw.value.apply(lambda v: len(repr(float(v)).split('.')[1]) if '.' in repr(float(v)) else 0)
hp = bw[bw.ndec >= 5].copy()
hp['key'] = hp.value.round(6)
rows = []
for k, x in hp.groupby('key'):
    if len(x) >= 2:
        # only count if different animals (not the same animal carried forward)
        ids = set(zip(x.block, x.col))
        if len(ids) >= 2:
            rows.append(dict(value=k, n=len(x), where='; '.join(f"{b}:{c}{'' if True else ''}(group {g}, day {int(d)}) [{cell}]" for b, c, g, d, cell in zip(x.block, x.col, x.group, x.day, x.cell))))
R = pd.DataFrame(rows)
pd.set_option('display.width', 300); pd.set_option('display.max_colwidth', 250)
print(R.to_string())
R.to_csv('dup_exact_highprecision_bw.csv', index=False)

# Position-matched comparison S11-A vs S11-B
cont = pd.read_csv('tidy_continuous.csv')
a = cont[cont.block == 'S11-A'].copy(); b = cont[cont.block == 'S11-B'].copy()
a['pos'] = a.groupby(['group', 'level']).cumcount(); b['pos'] = b.groupby(['group', 'level']).cumcount()
m = a.merge(b, on=['group', 'level', 'pos'], suffixes=('_AM', '_Neut'))
m['match'] = np.isclose(m.value_AM, m.value_Neut)
print('\nS11-A (alveolar macrophages) vs S11-B (neutrophils): position-matched identical values:', int(m.match.sum()), 'of', len(m))
print(m.groupby(['group', 'pos']).match.sum().unstack())
m.to_csv('dup_S11A_vs_S11B_positionwise.csv', index=False)
# permutation-style chance estimate: shuffle positions within the whole block
rng = np.random.default_rng(1)
vals_b = m.value_Neut.values.copy(); cnt = []
for _ in range(20000):
    rng.shuffle(vals_b); cnt.append(np.isclose(m.value_AM.values, vals_b).sum())
cnt = np.array(cnt)
print('chance expectation (random re-pairing of the 100 neutrophil values):', cnt.mean().round(2), ' max in 20000 permutations:', cnt.max(), ' P(>=observed)~', (cnt >= m.match.sum()).mean())

# S01-B vs S08-C
for ga, gb in [('AECII/PSLN-SRB', 'AECII-PSLN-SRB'), ('AECI/PSLN-SRB', 'AECII-PSLN-344-SRB'), ('AECI/PSLN-SRB', 'AECI-PSLN-SRB')]:
    va = cont[(cont.block == 'S01-B') & (cont.group == ga)].value.tolist()
    vb = cont[(cont.block == 'S08-C') & (cont.group == gb)].value.tolist()
    print(f'S01-B {ga} {va}  vs  S08-C {gb} {vb}  shared: {sorted(set(va) & set(vb))}')
