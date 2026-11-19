import pandas as pd, numpy as np, itertools
W = pd.read_csv('/tmp/work/tidy/weights.csv')
W['key'] = W.block + '|' + W.group + '|a' + W.animal.astype(str)
traj = {k: s.set_index('day')['value'] for k, s in W[W.day > 0].groupby('key')}
hits = []
for a, b in itertools.combinations(traj, 2):
    if a.split('|')[0] == b.split('|')[0]:
        continue
    ta, tb = traj[a], traj[b]
    common = ta.index.intersection(tb.index)
    same = [(int(d), float(ta[d])) for d in common if np.isclose(ta[d], tb[d])]
    distinct = len(set(round(x, 6) for _, x in same))
    if distinct >= 3:
        hits.append(dict(a=a, b=b, n_same_days=len(same), n_distinct=distinct,
                         days=[d for d, _ in same], values=[round(x, 3) for _, x in same]))
H = pd.DataFrame(hits)
H['block_pair'] = H.a.str.split('|').str[0] + ' ~ ' + H.b.str.split('|').str[0]
H['grp_pair'] = H.a.str.split('|').str[1] + ' ~ ' + H.b.str.split('|').str[1]
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 110); pd.set_option('display.max_rows', 200)
print(H.sort_values(['block_pair', 'a'])[['a', 'b', 'n_same_days', 'n_distinct', 'days', 'values']].to_string(index=False))
print()
print(H.groupby(['block_pair', 'grp_pair']).agg(animals=('a', 'size'), same_vals=('n_same_days', 'sum')).to_string())
H.to_csv('/tmp/work/tidy/audit_weight_recycling.csv', index=False)
# chance baseline: pairs of trajectories from different blocks, fraction with >=3 distinct shared values
n_pairs = sum(1 for a, b in itertools.combinations(traj, 2) if a.split('|')[0] != b.split('|')[0])
print('\ncross-block trajectory pairs tested:', n_pairs, ' flagged:', len(H))
