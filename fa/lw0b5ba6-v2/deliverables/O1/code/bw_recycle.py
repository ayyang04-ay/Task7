import pandas as pd, itertools, collections
B = pd.read_csv('/tmp/work/tidy/bw.csv')
B = B[B.day > 0]
traj = {}
for (b, g, a), d in B.groupby(['block', 'group', 'animal']):
    traj[(b, g, a)] = {day: round(v, 3) for day, v in zip(d.day, d.value)}
keys = list(traj)
pairs = []
for k1, k2 in itertools.combinations(keys, 2):
    t1, t2 = traj[k1], traj[k2]
    common = [d for d in t1 if d in t2]
    same = [d for d in common if t1[d] == t2[d]]
    # require >=3 identical days, ignoring trivially-shared LOCF plateaus within same animal
    if len(same) >= 3:
        pairs.append((k1, k2, len(same), len(common), same))
print('animal-trajectory pairs sharing >=3 identical daily weights:', len(pairs))
summ = collections.Counter()
for k1, k2, s, c, days in pairs:
    within = 'within-block' if k1[0] == k2[0] else 'cross-block'
    summ[(k1[0], k2[0])] += 1
    print(f'{within:12s} {k1} ~ {k2}: {s}/{c} days identical {days}')
print()
print('block-pair counts:')
for k, v in sorted(summ.items()):
    print(k, v)
