"""04b_weight_trajectory_dups.py
Animal-level check of the body-weight blocks: does one animal's trajectory re-appear in another block or group?
For each pair of animals from different (block, group) we count time-matched identical values (excluding day 0 = 100
and excluding carried-forward tails within the same animal).  Also reports recurring fractional parts.
"""
import json, itertools, collections
B = json.load(open('/tmp/work/parsed/parsed_blocks.json'))
W = [k for k, b in B.items() if b['kind'] == 'wide_time' and 'body weight' in b.get('measurand', '')]
animals = {}
for bid in W:
    b = B[bid]
    for g in b['order']:
        n = len(b['groups'][g][b['times'][0]])
        for i in range(n):
            traj = {int(float(t)): b['groups'][g][t][i] for t in b['times']}
            animals[(bid, g, i)] = traj

def informative(traj):
    """drop day 0 and the carried-forward tail (repeat of previous value)"""
    out = {}; prev = None
    for d in sorted(traj):
        v = traj[d]
        if d == 0 or v is None: prev = v; continue
        if v == prev: continue
        out[d] = v; prev = v
    return out

inf = {k: informative(v) for k, v in animals.items()}
pairs = []
for a, b_ in itertools.combinations(list(inf), 2):
    if a[:2] == b_[:2]: continue
    same = [d for d in inf[a] if d in inf[b_] and inf[a][d] == inf[b_][d]]
    if len(same) >= 3:
        pairs.append((len(same), min(len(inf[a]), len(inf[b_])), a, b_, same))
pairs.sort(key=lambda p: -p[0])
print(f"weight blocks: {len(W)}; animals: {len(animals)}")
print("animal trajectories sharing >=3 time-matched identical values with an animal in a different block/group:")
agg = collections.defaultdict(list)
for n, m, a, b_, same in pairs:
    agg[(a[0], a[1], b_[0], b_[1])].append((a[2], b_[2], n, m, same))
for k, v in sorted(agg.items(), key=lambda kv: -sum(x[2] for x in kv[1])):
    tot = sum(x[2] for x in v)
    print(f"\n{k[0]} [{k[1]}]  vs  {k[2]} [{k[3]}]: {len(v)} animal pair(s), {tot} identical cells")
    for a_i, b_i, n, m, same in v:
        print(f"      animal #{a_i+1} vs #{b_i+1}: {n} identical of {m} informative cells, days {same}")

# recurring fractional parts (values with >2 decimals)
frac = collections.defaultdict(set)
for k, tr in animals.items():
    for d, v in tr.items():
        if v is not None and abs(v * 10 - round(v * 10)) > 1e-6:
            frac[round(v - int(v), 4)].add((k[0], k[1]))
print("\nrecurring non-1-decimal fractional parts appearing in >=3 different block/group combinations:")
for f, s in sorted(frac.items(), key=lambda kv: -len(kv[1])):
    if len(s) >= 3:
        print(f"   .{str(f)[2:]:<6} in {len(s)} block/groups: {sorted(s)}")
