"""03_weight_vs_survival.py
Reconcile each time-to-event block with the body-weight block said to come from the same animals.

Weight blocks encode animals that left the study in two different ways:
  (a) blank cells after the last weighing, and
  (b) the last value repeated unchanged to day 14 (carried forward).
Both are treated here as 'no longer observed'.  An animal is called a non-survivor in the weight block if
  - its series goes blank before day 14, or
  - its final value is repeated unchanged over >=2 trailing weighings (>= 3 identical final cells
    is labelled 'firm'; exactly 2 identical final cells is labelled 'possible').
"""
import json, itertools
B = json.load(open('/tmp/work/parsed/parsed_blocks.json'))

PAIRS = [  # (survival block, weight block, {survival label -> weight label})
 ('S03-I', 'S13-F', None), ('S03-J', 'S13-G', None),
 ('S06-A', 'S15-A', None), ('S06-B', 'S15-B', None), ('S06-C', 'S15-C', None), ('S06-D', 'S15-D', None),
 ('S06-E_r34', 'S15-E', None), ('S06-F_r34', 'S15-F', None), ('S06-G', 'S15-G', None),
 ('S06-E_r71', 'S15-J', None), ('S06-F_r71', 'S15-K', None),
 ('S09-B', 'S09-C', None), ('S09-D', 'S09-E', None), ('S09-F', 'S09-G', None),
 ('S15-H', 'S15-I', None), ('S15-L', 'S15-M', None), ('S15-N', 'S15-O', None)]

def norm(s):
    return s.replace('ï', 'i').replace(' ', '').replace('(Y)', 'Y').lower()

def animal_series(wb, g):
    d = wb['groups'][g]; times = wb['times']
    n = len(d[times[0]])
    return [[d[t][i] for t in times] for i in range(n)], [int(float(t)) for t in times]

def classify(series, days):
    """return (status, last_real_day, nadir, final) for one animal"""
    vals = series
    present = [i for i, v in enumerate(vals) if v is not None]
    last = present[-1]
    nadir = min(v for v in vals if v is not None)
    if days[last] < days[-1]:
        return 'blank', days[last], nadir, vals[last]
    # trailing run of identical values
    run = 1
    while last - run >= 0 and vals[last - run] is not None and vals[last - run] == vals[last]:
        run += 1
    if run >= 3:
        return 'carried-fwd(firm)', days[last - run + 1], nadir, vals[last]
    if run == 2 and vals[last] < 90:
        return 'carried-fwd(possible)', days[last - 1], nadir, vals[last]
    return 'alive', days[last], nadir, vals[last]

out = []
for sb, wbk, _ in PAIRS:
    S, W = B[sb], B[wbk]
    print('=' * 110)
    print(f"{sb}  <->  {wbk}     survival groups: {S['order']}   |  weight groups: {W['order']}")
    smap = {norm(g): g for g in S['order']}; wmap = {norm(g): g for g in W['order']}
    only_s = [smap[k] for k in smap if k not in wmap]; only_w = [wmap[k] for k in wmap if k not in smap]
    if only_s or only_w:
        print(f"   !! GROUP LISTS DIFFER: only in survival block {only_s}; only in weight block {only_w}")
    for k in list(dict.fromkeys(list(smap) + list(wmap))):
        line = f"   {(smap.get(k) or wmap.get(k)):<24}"
        s_dead = s_n = None
        if k in smap:
            a = S['groups'][smap[k]]
            s_n = len(a); s_dead = sum(1 for x in a if x['event'] == 1)
            ddays = sorted(x['day'] for x in a if x['event'] == 1)
            line += f" survival: {s_n - s_dead}/{s_n} alive; death days {ddays}"
        else:
            line += " survival: (no such group)"
        if k in wmap:
            ser, days = animal_series(W, wmap[k])
            cl = [classify(s, days) for s in ser]
            firm = [c for c in cl if c[0] in ('blank', 'carried-fwd(firm)')]
            poss = [c for c in cl if c[0] == 'carried-fwd(possible)']
            alive = [c for c in cl if c[0] == 'alive']
            lastdays = sorted(c[1] for c in firm)
            line += f"\n   {'':<24} weight:   {len(alive)}/{len(cl)} with real series to d14; lost n={len(firm)} (last real weighing days {lastdays})"
            if poss:
                line += f"; +{len(poss)} possible (2 identical final cells, last real day {[c[1] for c in poss]})"
            w_dead_lo, w_dead_hi = len(firm), len(firm) + len(poss)
            enc = sorted(set(c[0] for c in firm + poss))
            line += f"  encoding: {enc}" if enc else ""
            if s_dead is not None:
                flag = 'OK' if (w_dead_lo <= s_dead <= w_dead_hi and s_n == len(cl)) else 'MISMATCH'
                line += f"\n   {'':<24} --> {flag}: survival block deaths {s_dead}/{s_n} vs weight block losses {w_dead_lo}" + (f"-{w_dead_hi}" if poss else "") + f"/{len(cl)}"
                out.append((sb, wbk, smap[k], s_n, s_dead, len(cl), w_dead_lo, w_dead_hi, flag))
        else:
            line += "\n" + ' ' * 28 + "weight:   (no such group)"
        print(line)
json.dump(out, open('/tmp/work/parsed/weight_vs_survival.json', 'w'), indent=1)
print('\nSUMMARY of mismatches:')
for r in out:
    if r[-1] != 'OK': print('  ', r)
