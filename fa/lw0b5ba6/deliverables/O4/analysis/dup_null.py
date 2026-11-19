"""Chance benchmark for exact matches between animal weight trajectories.
Only 'live' values are used (value differs from that animal's previous reading) so carried-forward
constants of dead animals are not counted. Per-day collision probabilities are estimated empirically
from all live values recorded on that day across every body-weight block."""
import pandas as pd, numpy as np, itertools, collections
bw = pd.read_csv('tidy_bodyweight.csv')
bw = bw[(bw.day != 0) & bw.value.notna()].sort_values(['block', 'col', 'day'])
bw['prev'] = bw.groupby(['block', 'col']).value.shift(1)
bw['live'] = bw.prev.isna() | (np.abs(bw.value - bw.prev) > 1e-9)
live = bw[bw.live].copy()
live['v'] = live.value.round(6)
# per-day collision probability
q = {}
for d, x in live.groupby('day'):
    c = collections.Counter(x.v); N = len(x)
    q[d] = sum(k * (k - 1) for k in c.values()) / (N * (N - 1))
print('per-day chance that two random live readings coincide exactly:', {int(k): round(v, 4) for k, v in q.items()})
traj = {k: dict(zip(x.day, x.v)) for k, x in live.groupby(['block', 'col'])}
keys = list(traj)
obs = collections.Counter(); exp = collections.Counter(); pairs = 0
from itertools import combinations
def poisson_binom_tail(ps, k):
    # P(at least k successes)
    dist = np.zeros(len(ps) + 1); dist[0] = 1
    for p in ps:
        dist[1:] = dist[1:] * (1 - p) + dist[:-1] * p; dist[0] *= (1 - p)
    return dist[k:].sum()
rows = []
for a, b in combinations(keys, 2):
    if a[0] == b[0]:
        continue  # cross-experiment pairs only
    common = set(traj[a]) & set(traj[b])
    if not common:
        continue
    pairs += 1
    m = sum(traj[a][d] == traj[b][d] for d in common)
    obs[m] += 1
    ps = [q[d] for d in common]
    for k in range(1, 8):
        exp[k] += poisson_binom_tail(ps, k)
print('cross-experiment animal pairs compared:', pairs)
print('k  observed_pairs_with>=k_live_matches  expected_by_chance')
tab = []
for k in range(1, 8):
    o = sum(v for m, v in obs.items() if m >= k)
    tab.append((k, o, exp[k])); print(k, o, round(exp[k], 4))
pd.DataFrame(tab, columns=['k_live_exact_matches', 'observed_pairs', 'expected_pairs_by_chance']).to_csv('dup_chance_benchmark.csv', index=False)
