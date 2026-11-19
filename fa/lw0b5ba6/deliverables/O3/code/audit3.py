import pandas as pd, numpy as np
S = pd.read_csv('/tmp/work/tidy/survival.csv')
W = pd.read_csv('/tmp/work/tidy/weights.csv')
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500); pd.set_option('display.max_colwidth', 120)

pairs = [('S03-I', 'S13-F'), ('S03-J', 'S13-G'), ('S06-A', 'S15-A'), ('S06-B', 'S15-B'), ('S06-C', 'S15-C'),
         ('S06-D', 'S15-D'), ('S06-E', 'S15-E'), ('S06-F', 'S15-F'), ('S06-G', 'S15-G'),
         ('S06-E(rows71-105; imprinting)', 'S15-J'), ('S06-F(rows71-105; imprinting)', 'S15-K'),
         ('S09-B', 'S09-C'), ('S09-D', 'S09-E'), ('S09-F', 'S09-G'), ('S15-H', 'S15-I'), ('S15-L', 'S15-M'),
         ('S15-N', 'S15-O')]

def classify(traj):
    """traj: Series day->value for one animal (NaN = missing). Return (status, inferred_death_day)."""
    t = traj.dropna()
    days_all = sorted(traj.index)
    last_day = t.index.max()
    if last_day < max(days_all):                       # trajectory stops -> removed (dead)
        return 'stops', last_day
    # trailing plateau of identical values (carried forward)
    vals = t.values
    k = 1
    while k < len(vals) and np.isclose(vals[-1 - k], vals[-1]):
        k += 1
    if (k >= 3) or (k >= 2 and vals[-1] < 90):
        return 'plateau(LOCF)', t.index[len(vals) - k]
    if vals[-1] >= 90:
        return 'recovered', None
    return 'alive<90 at end', None

rows = []
for sb, wb in pairs:
    s = S[S.block == sb]; w = W[W.block == wb]
    sg = s.groupby('group').agg(n_s=('event', 'size'), deaths_s=('event', 'sum'),
                                death_days=('days', lambda x: sorted(x[s.loc[x.index, 'event'] == 1].astype(int).tolist())))
    res = []
    for (g, a), tr in w.groupby(['group', 'animal']):
        traj = tr.set_index('day')['value'].reindex(sorted(w.day.unique()))
        st, dd = classify(traj)
        res.append(dict(group=g, animal=a, status=st, dday=dd))
    R = pd.DataFrame(res)
    wg = R.groupby('group').agg(n_w=('animal', 'size'),
                                stops=('status', lambda x: (x == 'stops').sum()),
                                locf=('status', lambda x: (x == 'plateau(LOCF)').sum()),
                                recovered=('status', lambda x: (x == 'recovered').sum()),
                                low_alive=('status', lambda x: (x == 'alive<90 at end').sum()),
                                w_death_days=('dday', lambda x: sorted([int(v) for v in x.dropna()])))
    m = sg.join(wg, how='outer')
    m['deaths_w'] = m['stops'].fillna(0) + m['locf'].fillna(0)
    m.insert(0, 'pair', f'{sb} <-> {wb}')
    rows.append(m.reset_index())
M = pd.concat(rows)
M['consistent_deaths'] = M['deaths_s'] == M['deaths_w']
print(M[['pair', 'group', 'n_s', 'deaths_s', 'death_days', 'n_w', 'deaths_w', 'stops', 'locf', 'recovered', 'low_alive',
         'w_death_days', 'consistent_deaths']].to_string(index=False))
M.to_csv('/tmp/work/tidy/audit_survival_vs_weight.csv', index=False)

# number of weight records per day vs number alive per survival data (for groups where weights stop rather than LOCF)
print('\n=== per-day: weights recorded vs animals alive at start of that day (alive = days > d-1 or censored) ===')
for sb, wb in pairs:
    s = S[S.block == sb]; w = W[W.block == wb]
    for g in sorted(set(s.group) & set(w.group)):
        ss = s[s.group == g]
        line = []
        for d in sorted(w.day.unique()):
            alive = int(((ss.days >= d) | (ss.event == 0)).sum())   # animals not yet dead before day d
            nrec = int(w[(w.group == g) & (w.day == d)].shape[0])
            line.append(f'd{int(d)}:{nrec}/{alive}')
        flag = any(int(x.split(':')[1].split('/')[0]) > int(x.split('/')[1]) for x in line)
        print(f'{sb:32s} {g:22s} {"INCONSISTENT " if flag else "ok           "} ' + ' '.join(line))
