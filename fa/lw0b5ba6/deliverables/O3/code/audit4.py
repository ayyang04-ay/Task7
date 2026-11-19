import pandas as pd, numpy as np, itertools
S = pd.read_csv('/tmp/work/tidy/survival.csv'); W = pd.read_csv('/tmp/work/tidy/weights.csv'); C = pd.read_csv('/tmp/work/tidy/continuous.csv')
# 1. identical survival vectors (sorted days+events) between groups of different blocks
print('=== Identical survival vectors across blocks (non-trivial: at least one death) ===')
vec = {}
for (b, g), d in S.groupby(['block', 'group']):
    key = tuple(sorted(zip(d.days.fillna(-1), d.event)))
    vec.setdefault(key, []).append(f'{b}:{g}')
for k, v in vec.items():
    if len(v) > 1 and sum(e for _, e in k) > 0 and sum(e for _, e in k) < len(k):
        print(' ', v, k)
# 2. identical weight rows between different groups within the same weight block & day (excluding day 0 all-100)
print('\n=== Identical weight vectors (same day, different groups, >=4 identical values in same positions) ===')
for (b, d), sub in W[W.day > 0].groupby(['block', 'day']):
    groups = {g: s.sort_values('animal')['value'].values for g, s in sub.groupby('group')}
    for g1, g2 in itertools.combinations(groups, 2):
        a, c = groups[g1], groups[g2]
        n = min(len(a), len(c))
        same = np.isclose(a[:n], c[:n]).sum()
        if same >= 4:
            print(f'  {b} day {int(d)}: {g1} vs {g2}: {same}/{n} identical: {a[:n]}')
# 3. identical weight values across blocks at same group/animal/day (cross-block recycling)
print('\n=== Cross-block identical weight trajectories/values (>=3 identical non-100 values for a same-position animal) ===')
W['key'] = W.block + '|' + W.group + '|' + W.animal.astype(str)
traj = {k: s.set_index('day')['value'] for k, s in W[W.day > 0].groupby('key')}
keys = list(traj)
hits = []
for a, b in itertools.combinations(keys, 2):
    if a.split('|')[0] == b.split('|')[0]:
        continue
    ta, tb = traj[a], traj[b]
    common = ta.index.intersection(tb.index)
    same = [(int(d), ta[d]) for d in common if np.isclose(ta[d], tb[d]) and not float(ta[d]).is_integer()]
    if len(same) >= 3:
        hits.append((a, b, same))
for h in hits: print(' ', h)
print('n hits', len(hits))
