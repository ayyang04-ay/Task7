"""06_survival.py
Time-to-event analysis of every challenge experiment.

Encoding (from the annotation): one row per animal, day column = elapsed days, group column 1/0.
Checked against the paired body-weight blocks: 1 = death/humane endpoint on that day, 0 = alive at end of observation.

Per experiment: survivors/n, exact (Clopper-Pearson) CI, Fisher exact test and exact permutation log-rank test
for the pre-specified contrasts.  Across experiments: pooled proportions and an exact stratified permutation
log-rank test (labels permuted within experiment).
Sensitivity analyses re-read the blocks whose labels or counts conflict with their paired weight blocks.
"""
import json, itertools, math, sys
import numpy as np
from scipy import stats
from math import comb

B = json.load(open('/tmp/work/parsed/parsed_blocks.json'))
RNG = np.random.default_rng(20261101)

def grp(bid, g):
    a = B[bid]['groups'][g]
    t = np.array([x['day'] if x['day'] is not None else np.nan for x in a], float)
    e = np.array([x['event'] for x in a], int)
    return t, e

def surv_n(bid, g):
    t, e = grp(bid, g)
    return int((e == 0).sum()), len(e)

def cp(k, n, a=0.05):
    lo = 0.0 if k == 0 else stats.beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(1 - a / 2, k + 1, n - k)
    return lo, hi

def logrank_OE(t, e, g):
    """O - E and variance for group g==1 (two-sample log-rank)."""
    OE = 0.0; V = 0.0
    for u in np.unique(t[e == 1]):
        at = t >= u
        n = at.sum(); n1 = (at & (g == 1)).sum()
        d = ((t == u) & (e == 1)).sum(); d1 = ((t == u) & (e == 1) & (g == 1)).sum()
        OE += d1 - d * n1 / n
        if n > 1:
            V += d * (n1 / n) * (1 - n1 / n) * (n - d) / (n - 1)
    return OE, V

def perm_logrank(strata, n_mc=200000):
    """strata: list of (t, e, g) arrays. Exact enumeration if feasible, otherwise Monte Carlo. Two-sided."""
    obs = sum(logrank_OE(t, e, g)[0] for t, e, g in strata)
    Vtot = sum(logrank_OE(t, e, g)[1] for t, e, g in strata)
    n_enum = 1
    for t, e, g in strata:
        n_enum *= comb(len(g), int(g.sum()))
    if n_enum <= 400000:
        # exact: distribution of the sum over strata via enumeration within each stratum + convolution
        dists = []
        for t, e, g in strata:
            n = len(g); k = int(g.sum()); vals = {}
            for idx in itertools.combinations(range(n), k):
                gg = np.zeros(n, int); gg[list(idx)] = 1
                v = round(logrank_OE(t, e, gg)[0], 9)
                vals[v] = vals.get(v, 0) + 1
            tot = sum(vals.values())
            dists.append({v: c / tot for v, c in vals.items()})
        conv = {0.0: 1.0}
        for d in dists:
            new = {}
            for a, pa in conv.items():
                for b, pb in d.items():
                    key = round(a + b, 9); new[key] = new.get(key, 0) + pa * pb
            conv = new
        p = sum(pr for v, pr in conv.items() if abs(v) >= abs(obs) - 1e-9)
        return obs, Vtot, min(1.0, p), 'exact'
    cnt = 0
    for _ in range(n_mc):
        s = 0.0
        for t, e, g in strata:
            s += logrank_OE(t, e, RNG.permutation(g))[0]
        cnt += abs(s) >= abs(obs) - 1e-9
    return obs, Vtot, (cnt + 1) / (n_mc + 1), f'MC {n_mc}'

def two_group(bid, g1, g0, fix=None):
    t1, e1 = grp(bid, g1); t0, e0 = grp(bid, g0)
    # one PSLN-344 row in S03-J has event=0 but no day: treat as censored at end of observation (21 d as recorded for the others)
    if np.isnan(t1).any(): t1 = np.where(np.isnan(t1), np.nanmax(t1), t1)
    if np.isnan(t0).any(): t0 = np.where(np.isnan(t0), np.nanmax(t0), t0)
    t = np.r_[t1, t0]; e = np.r_[e1, e0]; g = np.r_[np.ones(len(t1), int), np.zeros(len(t0), int)]
    return t, e, g

EXPS = [  # id, label, age class, strain, regimen descriptors
 ('S03-I',     'Homologous CA09 H1N1 10xLD50, d14 (bivalent vaccine)',      'aged',  'BALB/c'),
 ('S03-J',     'Wild-type VN04 H5N1, d2 (rgH5N1 vaccine)',                   'aged',  'BALB/c'),
 ('S06-A',     'H3N2 vaccine -> PR8 H1N1 5xLD50, d14',                       'aged',  'BALB/c'),
 ('S06-B',     'H3N2 vaccine -> PR8 H1N1 5xLD50, d3',                        'aged',  'BALB/c'),
 ('S06-C',     'Bivalent -> rgH5N1 5xLD50, d14',                             'aged',  'BALB/c'),
 ('S06-D',     'Bivalent -> rgH5N1 5xLD50, d3',                              'aged',  'BALB/c'),
 ('S06-E_r34', 'H3N2 vaccine -> PR8 H1N1 5xLD50, d60',                       'aged',  'BALB/c'),
 ('S06-F_r34', 'Bivalent -> rgH5N1 5xLD50, d60',                             'aged',  'BALB/c'),
 ('S06-G',     'H1N1 vaccine -> Perth H3N2 5xLD50, d60',                     'aged',  'BALB/c'),
 ('S15-L',     'Bivalent -> challenge virus not stated',                    'aged',  'C57BL/6'),
 ('S15-N',     'Bivalent -> challenge virus not stated',                    'aged',  'Swiss Webster'),
]

res = {'per_experiment': [], 'pooled': {}, 'other': {}}
print("=" * 120)
print("A. AGED-ANIMAL CHALLENGE EXPERIMENTS  (survivors / n at end of observation, as printed in the survival blocks)")
print("=" * 120)
hdr = f"{'block':<10}{'design':<55}{'strain':<14}{'Sham':>7}{'212':>7}{'344':>7}{'212(Y)':>8}  {'Fisher 344v212':>15}{'logrank 344v212':>17}{'Fisher 344vSham':>17}{'Fisher 344vY':>14}"
print(hdr)
tot = {k: [0, 0] for k in ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']}
strata_212 = []; strata_sham = []; strata_y = []
for bid, lab, age, strain in EXPS:
    row = {'block': bid, 'design': lab, 'strain': strain}
    cells = []
    for gname in ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']:
        if gname in B[bid]['groups']:
            s, n = surv_n(bid, gname); tot[gname][0] += s; tot[gname][1] += n
            row[gname] = (s, n); cells.append(f"{s}/{n}")
        else:
            row[gname] = None; cells.append('-')
    s3, n3 = row['PSLN-344']; s2, n2 = row['PSLN-212']; ss, ns = row['Sham']
    pf = stats.fisher_exact([[s3, n3 - s3], [s2, n2 - s2]])[1]
    pfs = stats.fisher_exact([[s3, n3 - s3], [ss, ns - ss]])[1]
    t, e, g = two_group(bid, 'PSLN-344', 'PSLN-212'); strata_212.append((t, e, g))
    _, _, plr, how = perm_logrank([(t, e, g)])
    t_, e_, g_ = two_group(bid, 'PSLN-344', 'Sham'); strata_sham.append((t_, e_, g_))
    if row['PSLN-212(Y)']:
        sy, ny = row['PSLN-212(Y)']; pfy = stats.fisher_exact([[s3, n3 - s3], [sy, ny - sy]])[1]
        strata_y.append(two_group(bid, 'PSLN-344', 'PSLN-212(Y)'))
    else:
        pfy = float('nan')
    row.update(fisher_344_v_212=pf, logrank_344_v_212=plr, fisher_344_v_sham=pfs, fisher_344_v_Y=pfy)
    res['per_experiment'].append(row)
    print(f"{bid:<10}{lab:<55}{strain:<14}{cells[0]:>7}{cells[1]:>7}{cells[2]:>7}{cells[3]:>8}  {pf:>15.4f}{plr:>17.4f}{pfs:>17.4f}{pfy:>14.3f}")

print("-" * 120)
print("POOLED (simple sum over the 11 experiments that contain all of Sham / PSLN-212 / PSLN-344):")
for k, (s, n) in tot.items():
    lo, hi = cp(s, n); print(f"   {k:<12} {s}/{n} = {100*s/n:.1f}%  (exact 95% CI {100*lo:.1f}-{100*hi:.1f}%)")
    res['pooled'][k] = dict(s=s, n=n, pct=100 * s / n, lo=100 * lo, hi=100 * hi)
for name, st in [('344 vs 212', strata_212), ('344 vs Sham', strata_sham), ('344 vs 212(Y)', strata_y)]:
    obs, V, p, how = perm_logrank(st)
    z = obs / math.sqrt(V) if V > 0 else float('nan')
    print(f"   stratified log-rank PSLN-{name}: O-E = {obs:.2f}, Z = {z:.2f}, permutation p ({how}) = {p:.2e}; asymptotic p = {2*stats.norm.sf(abs(z)):.2e}")
    res['pooled'][f'stratified_logrank_{name}'] = dict(OE=obs, Z=z, p_perm=p, how=how, p_asym=2 * stats.norm.sf(abs(z)))

# Mantel-Haenszel common risk difference for survival (344 - 212), with Sato variance
def mh_rd(tables):
    num = den = 0.0; P = Q = 0.0
    for (a, n1, c, n0) in tables:
        N = n1 + n0; w = n1 * n0 / N
        num += (a / n1 - c / n0) * w; den += w
        b = n1 - a; d = n0 - c
        P += (a * b * n0 ** 3 + c * d * n1 ** 3) / (n1 * n0 * N ** 2)   # Greenland-Robins variance components
    rd = num / den
    se = math.sqrt(P) / den
    return rd, rd - 1.96 * se, rd + 1.96 * se
tabs = [(r['PSLN-344'][0], r['PSLN-344'][1], r['PSLN-212'][0], r['PSLN-212'][1]) for r in res['per_experiment']]
rd, lo, hi = mh_rd(tabs)
print(f"   Mantel-Haenszel survival difference PSLN-344 minus PSLN-212: {100*rd:.1f} percentage points (95% CI {100*lo:.1f} to {100*hi:.1f})")
res['pooled']['MH_RD_344_minus_212'] = dict(rd=100 * rd, lo=100 * lo, hi=100 * hi)
tabs = [(r['PSLN-344'][0], r['PSLN-344'][1], r['PSLN-212(Y)'][0], r['PSLN-212(Y)'][1]) for r in res['per_experiment'] if r['PSLN-212(Y)']]
rd, lo, hi = mh_rd(tabs)
sy = sum(t[2] for t in tabs); ny = sum(t[3] for t in tabs); s3 = sum(t[0] for t in tabs); n3 = sum(t[1] for t in tabs)
print(f"   PSLN-344 (aged) vs PSLN-212(Y) (young) in the {len(tabs)} experiments with both: {s3}/{n3} vs {sy}/{ny}; MH difference {100*rd:.1f} points (95% CI {100*lo:.1f} to {100*hi:.1f})")
res['pooled']['MH_RD_344_minus_Y'] = dict(rd=100 * rd, lo=100 * lo, hi=100 * hi, s344=s3, n344=n3, sY=sy, nY=ny)

# ------------------------------------------------------------------ by challenge interval
print("\nBy interval between immunisation and challenge (aged BALB/c, PSLN-344 | PSLN-212 | Sham | PSLN-212(Y)):")
for name, ids in [('d2-d3', ['S03-J', 'S06-B', 'S06-D']), ('d14', ['S03-I', 'S06-A', 'S06-C']), ('d60', ['S06-E_r34', 'S06-F_r34', 'S06-G'])]:
    out = []
    for gname in ['PSLN-344', 'PSLN-212', 'Sham', 'PSLN-212(Y)']:
        s = sum(surv_n(b, gname)[0] for b in ids if gname in B[b]['groups']); n = sum(surv_n(b, gname)[1] for b in ids if gname in B[b]['groups'])
        lo, hi = cp(s, n); out.append(f"{gname} {s}/{n} ({100*s/n:.0f}%, {100*lo:.0f}-{100*hi:.0f})")
        res['other'][f'interval_{name}_{gname}'] = (s, n)
    print(f"   {name:<6} " + ' | '.join(out))

# ------------------------------------------------------------------ d60 and background mortality
print("\nDay-60 experiments: unchallenged, unvaccinated age-matched 'Untreated' animals (background mortality)")
u = [surv_n(b, 'Untreated') for b in ['S06-E_r34', 'S06-F_r34', 'S06-G']]
p344 = [surv_n(b, 'PSLN-344') for b in ['S06-E_r34', 'S06-F_r34', 'S06-G']]
su, nu = sum(x[0] for x in u), sum(x[1] for x in u); s3, n3 = sum(x[0] for x in p344), sum(x[1] for x in p344)
print(f"   Untreated (no virus) survivors per block {u} -> {su}/{nu} ({100*su/nu:.0f}%); deaths {nu-su}/{nu} = {100*(nu-su)/nu:.0f}% in 14 d, exact 95% CI {100*cp(nu-su, nu)[0]:.0f}-{100*cp(nu-su, nu)[1]:.0f}%")
print(f"   PSLN-344 (challenged) survivors per block {p344} -> {s3}/{n3} ({100*s3/n3:.0f}%)")
pf = stats.fisher_exact([[s3, n3 - s3], [su, nu - su]])[1]
print(f"   Fisher exact PSLN-344 challenged vs Untreated unchallenged: p = {pf:.3f}")
res['other']['d60_untreated'] = dict(s=su, n=nu, per_block=u); res['other']['d60_344'] = dict(s=s3, n=n3, per_block=p344, fisher_vs_untreated=pf)

# ------------------------------------------------------------------ other designs
print("\n" + "=" * 120)
print("B. OTHER CHALLENGE DESIGNS")
def show(bid, note=''):
    print(f"   {bid} {note}")
    out = {}
    for gname in B[bid]['order']:
        s, n = surv_n(bid, gname); t, e = grp(bid, gname)
        print(f"        {gname:<24} {s}/{n}   death days {sorted(int(x) for x in t[e == 1])}")
        out[gname] = (s, n)
    res['other'][bid] = out
    return out
o = show('S15-H', '(aged BALB/c; rgH5N1 challenge 3 d after: vaccine alone / PSLN-344 alone / vaccine + PSLN-344)')
print(f"        Fisher vaccine+344 vs 344 alone: p = {stats.fisher_exact([[6,1],[0,7]])[1]:.4f}; vs vaccine alone: p = {stats.fisher_exact([[6,1],[0,7]])[1]:.4f}")
o = show('S06-E_r71', '(14-month BALB/c, PR8-imprinted or saline; bivalent vaccine; PR8 challenge, interval not stated)')
o = show('S06-F_r71', '(14-month BALB/c, PR8-imprinted or saline; bivalent vaccine; Perth H3N2 challenge d14)')
s3 = sum(surv_n(b, g)[0] for b in ['S06-E_r71', 'S06-F_r71'] for g in ['Naïve+PSLN-344', 'Imprinting+PSLN-344'])
s2n = sum(surv_n(b, 'Naïve+PSLN-212')[0] for b in ['S06-E_r71', 'S06-F_r71']); s2i = sum(surv_n(b, 'Imprinting+PSLN-212')[0] for b in ['S06-E_r71', 'S06-F_r71'])
print(f"        pooled: PSLN-344 {s3}/28; PSLN-212 naive {s2n}/14, imprinted {s2i}/14;  Fisher 344 (28) vs 212 (28): p = {stats.fisher_exact([[s3, 28 - s3], [s2n + s2i, 28 - s2n - s2i]])[1]:.2e}")
res['other']['imprint_pooled'] = dict(s344=s3, n344=28, s212_naive=s2n, s212_imp=s2i)
print("\n   Young BALB/c:")
for b, note in [('S09-B', '(H3N2 vaccine -> PR8, d21)'), ('S09-D', '(H1N1 vaccine -> Perth H3N2, d21)'), ('S09-F', '(bivalent -> rgH5N1, d180)'), ('S13-E', '(homologous CA09 10xLD50, d14)')]:
    show(b, note)
sy3 = sum(surv_n(b, 'PSLN-344Y')[0] for b in ['S09-B', 'S09-D', 'S09-F']); sy2 = sum(surv_n(b, 'PSLN-212Y')[0] for b in ['S09-B', 'S09-D', 'S09-F'])
print(f"        young heterologous challenges pooled: PSLN-344Y {sy3}/24, PSLN-212Y {sy2}/24")
res['other']['young_pooled'] = dict(s344=sy3, s212=sy2, n=24)

# ------------------------------------------------------------------ sensitivity analyses
print("\n" + "=" * 120)
print("C. SENSITIVITY: re-reading blocks that conflict with the paired body-weight block")
# weight-block-based survivor counts (from 03_weight_vs_survival.py; 'possible' carried-forward animals counted as deaths)
WV = json.load(open('/tmp/work/parsed/weight_vs_survival.json'))
wv = {(r[0], r[2]): r for r in WV}
def weight_surv(bid, gname, worst=True):
    r = wv[(bid, gname)]
    n = r[5]; dead = r[7] if worst else r[6]
    return n - dead, n
alt = {}
for bid, lab, age, strain in EXPS:
    alt[bid] = {}
    for gname in ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']:
        if gname not in B[bid]['groups']: continue
        s, n = surv_n(bid, gname)
        if (bid, gname) in wv:
            sw_lo, nw = weight_surv(bid, gname, worst=True); sw_hi, _ = weight_surv(bid, gname, worst=False)
        else:
            sw_lo = sw_hi = None
        alt[bid][gname] = dict(surv=(s, n), weight_lo=sw_lo, weight_hi=sw_hi)
def pooled(picker, ids=None):
    out = {}
    for gname in ['PSLN-344', 'PSLN-212']:
        S = N = 0
        for bid in (ids or [e[0] for e in EXPS]):
            s, n = picker(bid, gname)
            if s is None: continue
            S += s; N += n
        out[gname] = (S, N)
    return out
def pick_printed(bid, g): return alt[bid][g]['surv']
def pick_worst(bid, g):
    """least favourable to PSLN-344: for 344 take the lower of survival-table and weight-block survivors; for 212 the higher.
       S03-I: weight block says PSLN-212 3/7. S03-J: weight block has no PSLN-212 arm -> drop the 212 comparison there."""
    s, n = alt[bid][g]['surv']; lo = alt[bid][g]['weight_lo']; hi = alt[bid][g]['weight_hi']
    if bid == 'S03-J' and g == 'PSLN-212': return None, None
    if g == 'PSLN-344': return (min(s, lo) if lo is not None else s), n
    return (max(s, hi) if hi is not None else s), n
for name, pk, ids in [('as printed, all 11 experiments', pick_printed, None),
                      ('worst case for PSLN-344 (every survival/weight conflict resolved against it; S03-J 212-arm dropped)', pick_worst, None),
                      ('as printed, excluding the two label-conflicted blocks S03-I and S03-J', pick_printed, [e[0] for e in EXPS if e[0] not in ('S03-I', 'S03-J')]),
                      ('worst case AND excluding S03-I, S03-J', pick_worst, [e[0] for e in EXPS if e[0] not in ('S03-I', 'S03-J')])]:
    o = pooled(pk, ids)
    (s3, n3), (s2, n2) = o['PSLN-344'], o['PSLN-212']
    p = stats.fisher_exact([[s3, n3 - s3], [s2, n2 - s2]])[1]
    l3, h3 = cp(s3, n3); l2, h2 = cp(s2, n2)
    print(f"   {name}:\n        PSLN-344 {s3}/{n3} = {100*s3/n3:.0f}% ({100*l3:.0f}-{100*h3:.0f})   PSLN-212 {s2}/{n2} = {100*s2/n2:.0f}% ({100*l2:.0f}-{100*h2:.0f})   Fisher p = {p:.1e}")
    res['pooled'][f'sens::{name}'] = dict(s344=s3, n344=n3, s212=s2, n212=n2, p=p)
print("\n   per-experiment detail (survival table | weight-block survivors worst..best):")
for bid in alt:
    print(f"   {bid:<10} " + ' ; '.join(f"{g}: {v['surv'][0]}/{v['surv'][1]} | {v['weight_lo']}..{v['weight_hi']}" for g, v in alt[bid].items()))
res['alt'] = alt
json.dump(res, open('/tmp/work/parsed/survival_results.json', 'w'), indent=1, default=str)

# ------------------------------------------------------------------ additional pre-specified subsets
print("\n" + "=" * 120)
print("D. SUBSETS")
def pool(ids, groups=('PSLN-344', 'PSLN-212', 'Sham', 'PSLN-212(Y)')):
    out = {}
    for gname in groups:
        s = sum(surv_n(b, gname)[0] for b in ids if gname in B[b]['groups']); n = sum(surv_n(b, gname)[1] for b in ids if gname in B[b]['groups'])
        out[gname] = (s, n)
    return out
subsets = {
 'HA-mismatched (heterosubtypic) challenges, aged BALB/c: S06-A,B,C,D,E,F,G': ['S06-A', 'S06-B', 'S06-C', 'S06-D', 'S06-E_r34', 'S06-F_r34', 'S06-G'],
 'strict subset: survival table and weight block agree for every arm, design fully annotated: S06-A, S06-B, S06-F': ['S06-A', 'S06-B', 'S06-F_r34'],
 'non-BALB/c strains: S15-L (C57BL/6), S15-N (Swiss Webster)': ['S15-L', 'S15-N'],
 'early challenge d2-d3: S03-J, S06-B, S06-D': ['S03-J', 'S06-B', 'S06-D'],
}
for name, ids in subsets.items():
    o = pool(ids)
    (s3, n3), (s2, n2) = o['PSLN-344'], o['PSLN-212']
    p = stats.fisher_exact([[s3, n3 - s3], [s2, n2 - s2]])[1]
    print(f"   {name}\n        " + ' | '.join(f"{g} {s}/{n} ({100*s/n:.0f}%; {100*cp(s,n)[0]:.0f}-{100*cp(s,n)[1]:.0f})" for g, (s, n) in o.items() if n) + f"   Fisher 344 v 212 p={p:.1e}")
    res['pooled'][f'subset::{name}'] = {g: v for g, v in o.items()} | {'p': p}
# early challenge including the S15-H combination arm
s = 22 + 6; n = 24 + 7
print(f"   early challenge incl. S15-H vaccine+PSLN-344 arm: {s}/{n} = {100*s/n:.0f}% ({100*cp(s,n)[0]:.0f}-{100*cp(s,n)[1]:.0f})")
res['pooled']['early_incl_S15H'] = (s, n)
# age effect on PSLN-212: young vs aged in the same experiments
o = pool([e[0] for e in EXPS if 'PSLN-212(Y)' in B[e[0]]['groups']])
print(f"   age effect on PSLN-212 (10 experiments with both arms): young {o['PSLN-212(Y)']} vs aged {o['PSLN-212']}")
res['pooled']['age_effect_212'] = o
json.dump(res, open('/tmp/work/parsed/survival_results.json', 'w'), indent=1, default=str)
