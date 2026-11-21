"""04_duplicate_scan.py
Scan for numeric sequences that recur between blocks / groups that should be independent.
Each group in each block is flattened to an ordered vector (row-major for time-course blocks).
For every pair of vectors we count position-wise identical non-trivial values (value != 100, and
not a small integer code) and also the longest identical run when the two vectors are aligned at any offset.
"""
import json, itertools
B = json.load(open('/tmp/work/parsed/parsed_blocks.json'))

vecs = {}   # (block, group, sub) -> list of values (None kept)
for bid, b in B.items():
    k = b['kind']
    if k in ('columns', 'rows'):
        for g in b['order']:
            vecs[(bid, g, '')] = list(b['groups'][g])
    elif k in ('wide_time', 'wide_analyte'):
        for g in b['order']:
            for t, vs in b['groups'][g].items():
                vecs[(bid, g, t)] = list(vs)

def nontrivial(v):
    return v is not None and v != 100 and not (float(v).is_integer() and abs(v) <= 20)

# 1) same-position matches between vectors of equal length
hits = []
keys = list(vecs)
for a, b_ in itertools.combinations(keys, 2):
    va, vb = vecs[a], vecs[b_]
    if len(va) != len(vb) or len(va) < 2:
        continue
    same = [i for i, (x, y) in enumerate(zip(va, vb)) if nontrivial(x) and x == y]
    nn = sum(1 for x in va if nontrivial(x))
    if len(same) >= 2:
        hits.append((len(same), nn, a, b_, same))
hits.sort(key=lambda h: (-h[0], h[2]))
print('=== position-wise identical values between two groups/timepoints (>=2 identical, non-trivial) ===')
for n, nn, a, b_, same in hits:
    print(f"{n}/{len(vecs[a])} identical  {a}  vs  {b_}   positions {same}   values {[vecs[a][i] for i in same]}")

# 2) aggregate by block pair / group pair
from collections import defaultdict
agg = defaultdict(lambda: [0, 0])
for n, nn, a, b_, same in hits:
    agg[(a[0], a[1], b_[0], b_[1])][0] += n
    agg[(a[0], a[1], b_[0], b_[1])][1] += 1
print('\n=== aggregated over timepoints ===')
for k, (n, m) in sorted(agg.items(), key=lambda kv: -kv[1][0]):
    print(f"{n:>3} identical cells across {m} row(s):  {k[0]} [{k[1]}]  ==  {k[2]} [{k[3]}]")

# 3) any-order multiset overlap between static groups (catches re-ordered copies), >=3 shared distinct non-trivial values
print('\n=== shared distinct values regardless of position (static blocks; >=3 shared) ===')
stat = {k: v for k, v in vecs.items() if k[2] == ''}
for a, b_ in itertools.combinations(list(stat), 2):
    sa = {x for x in stat[a] if nontrivial(x)}; sb = {x for x in stat[b_] if nontrivial(x)}
    sh = sa & sb
    if len(sh) >= 3:
        print(f"{len(sh)} shared: {a[:2]} vs {b_[:2]}: {sorted(sh)}")
