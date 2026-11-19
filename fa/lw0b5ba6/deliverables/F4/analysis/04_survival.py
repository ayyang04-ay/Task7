#!/usr/bin/env python
"""
04_survival.py  --  time-to-event analysis of every challenge block.
Run: micromamba run -n core python 04_survival.py

Conventions
  * group column: 1 = death (event), 0 = alive at last observation (censored)  [annotation, sheet S06 preamble]
  * log-rank = stated method (annotation p.2). Because n is 7-10 per arm we ALSO report
      - exact permutation p for the log-rank statistic (all allocations enumerated when feasible, else 200k Monte Carlo)
      - Fisher's exact test on survival at end of observation (two-sided)
  * Survival proportions carry exact Clopper-Pearson 95% CIs.
Outputs: tables/T02_survival_by_group.csv, tables/T03_survival_contrasts.csv, tables/T04_survival_pooled.csv
"""
import os, itertools, math
import numpy as np, pandas as pd
from scipy import stats
from lifelines.statistics import logrank_test, multivariate_logrank_test

HERE = os.path.dirname(os.path.abspath(__file__))
sv = pd.read_csv(os.path.join(HERE, 'parsed', 'survival_long.csv'), keep_default_na=False)
sv['day_missing'] = sv.day.astype(str) == ''
sv['day'] = pd.to_numeric(sv.day, errors='coerce')
sv['group'] = sv.group.str.replace('Naïve', 'Naive')
rng = np.random.default_rng(20261101)

META = {  # block -> design descriptors taken from the annotation PDF (page refs in proposal)
 'S03-I': dict(host='aged BALB/c', vaccine='bivalent H1N1+H3N2', challenge='10x mLD50 CA09 H1N1 (homologous)', interval='d14', obs=14),
 'S03-J': dict(host='BALB/c, age not stated in block (no (Y) label)', vaccine='rgH5N1', challenge='wild-type VN04 H5N1 (homologous, BSL-3)', interval='d2', obs=22),
 'S06-A': dict(host='aged BALB/c', vaccine='Aichi H3N2', challenge='5x mLD50 PR8 H1N1 (heterosubtypic)', interval='d14', obs=14),
 'S06-B': dict(host='aged BALB/c', vaccine='Aichi H3N2', challenge='5x mLD50 PR8 H1N1 (heterosubtypic)', interval='d3', obs=14),
 'S06-C': dict(host='aged BALB/c', vaccine='bivalent H1N1+H3N2', challenge='5x mLD50 rgH5N1 (heterosubtypic)', interval='d14', obs=14),
 'S06-D': dict(host='aged BALB/c', vaccine='bivalent H1N1+H3N2', challenge='5x mLD50 rgH5N1 (heterosubtypic)', interval='d3', obs=14),
 'S06-E': dict(host='aged BALB/c', vaccine='Aichi H3N2', challenge='5x mLD50 PR8 H1N1 (heterosubtypic)', interval='d60', obs=14),
 'S06-F': dict(host='aged BALB/c', vaccine='bivalent H1N1+H3N2', challenge='5x mLD50 rgH5N1 (heterosubtypic)', interval='d60', obs=14),
 'S06-G': dict(host='aged BALB/c', vaccine='CA09 H1N1', challenge='5x mLD50 Perth H3N2 (heterosubtypic)', interval='d60', obs=14),
 'S06-E(r71)': dict(host='BALB/c 14 mo (infected or saline at 10 mo)', vaccine='bivalent H1N1+H3N2', challenge='5x LD50 PR8 H1N1', interval='not stated', obs=14),
 'S06-F(r71)': dict(host='BALB/c 14 mo (infected or saline at 10 mo)', vaccine='bivalent H1N1+H3N2', challenge='5x LD50 Perth H3N2', interval='d14', obs=14),
 'S15-H': dict(host='aged BALB/c', vaccine='bivalent / none', challenge='5x mLD50 rgH5N1', interval='d3', obs=14),
 'S15-L': dict(host='aged C57BL/6 (20 mo)', vaccine='bivalent H1N1+H3N2', challenge='not stated in block', interval='not stated', obs=14),
 'S15-N': dict(host='aged Swiss Webster (20 mo)', vaccine='bivalent H1N1+H3N2', challenge='not stated in block', interval='not stated', obs=14),
 'S09-B': dict(host='young BALB/c', vaccine='Aichi H3N2', challenge='5x mLD50 PR8 H1N1 (heterosubtypic)', interval='d21', obs=14),
 'S09-D': dict(host='young BALB/c', vaccine='CA09 H1N1', challenge='5x mLD50 Perth H3N2 (heterosubtypic)', interval='d21', obs=14),
 'S09-F': dict(host='young BALB/c', vaccine='bivalent H1N1+H3N2', challenge='5x mLD50 rgH5N1 (heterosubtypic)', interval='d180', obs=14),
 'S13-E': dict(host='young BALB/c', vaccine='bivalent H1N1+H3N2', challenge='10x mLD50 CA09 H1N1 (homologous)', interval='d14', obs=14),
 'S08-unlabelled': dict(host='unknown', vaccine='unknown', challenge='unknown', interval='unknown', obs=14),
}

def cp(k, n, a=0.05):
    lo = 0.0 if k == 0 else stats.beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(1 - a / 2, k + 1, n - k)
    return lo, hi

def lr_stat(t, e, g):
    """signed log-rank Z (O-E)/sqrt(V) for group g==1 vs g==0"""
    t, e, g = map(np.asarray, (t, e, g))
    O = E = V = 0.0
    for tj in np.unique(t[e == 1]):
        at = t >= tj
        n = at.sum(); n1 = (at & (g == 1)).sum()
        d = ((t == tj) & (e == 1)).sum(); d1 = ((t == tj) & (e == 1) & (g == 1)).sum()
        O += d1; E += d * n1 / n
        if n > 1: V += d * (n1 / n) * (1 - n1 / n) * (n - d) / (n - 1)
    return (O - E), V

def exact_logrank(t, e, g):
    t, e, g = map(np.asarray, (t, e, g))
    oe, v = lr_stat(t, e, g)
    if v == 0: return 1.0, 'degenerate'
    obs = oe * oe / v
    n, n1 = len(g), int(g.sum())
    total = math.comb(n, n1)
    cnt = 0; tot = 0
    if total <= 250000:
        for idx in itertools.combinations(range(n), n1):
            gg = np.zeros(n, int); gg[list(idx)] = 1
            oe2, v2 = lr_stat(t, e, gg)
            s = oe2 * oe2 / v2 if v2 > 0 else 0.0
            cnt += s >= obs - 1e-12; tot += 1
        return cnt / tot, 'exact'
    for _ in range(200000):
        gg = rng.permutation(g)
        oe2, v2 = lr_stat(t, e, gg)
        s = oe2 * oe2 / v2 if v2 > 0 else 0.0
        cnt += s >= obs - 1e-12; tot += 1
    return (cnt + 1) / (tot + 1), 'MC'

def median_surv(t, e):
    # Kaplan-Meier median (inf if never reaches 0.5)
    t, e = np.asarray(t), np.asarray(e); s = 1.0
    for tj in np.unique(t[e == 1]):
        s *= 1 - ((t == tj) & (e == 1)).sum() / (t >= tj).sum()
        if s <= 0.5: return tj
    return np.inf

# ---------------- per-group table ----------------
rows = []
for (b, g), d in sv.groupby(['block', 'group'], sort=False):
    dd = d[~d.day_missing]
    n_all, n = len(d), len(dd)
    deaths = int(dd.event.sum()); surv_all = int((d.event == 0).sum())
    lo, hi = cp(surv_all, n_all)
    m = META.get(b, {})
    rows.append(dict(block=b, group=g, host=m.get('host'), vaccine=m.get('vaccine'), challenge=m.get('challenge'),
                     challenge_day_post_vacc=m.get('interval'), n_rows=n_all, n_with_day=n, deaths=deaths, survivors=surv_all,
                     survival_pct=round(100 * surv_all / n_all, 1), ci95_lo=round(100 * lo, 1), ci95_hi=round(100 * hi, 1),
                     median_days_to_death=median_surv(dd.day, dd.event), death_days=' '.join(str(int(x)) for x in sorted(dd[dd.event == 1].day)),
                     cells=f"{d.cell.iloc[0]}:{d.cell.iloc[-1].split('!')[1]}"))
T2 = pd.DataFrame(rows)
os.makedirs(os.path.join(HERE, 'tables'), exist_ok=True)
T2.to_csv(os.path.join(HERE, 'tables', 'T02_survival_by_group.csv'), index=False)

# ---------------- pairwise contrasts ----------------
def contrast(b, g1, g0):
    d = sv[(sv.block == b) & (sv.group.isin([g1, g0])) & (~sv.day_missing)]
    a, c = d[d.group == g1], d[d.group == g0]
    if len(a) == 0 or len(c) == 0: return None
    lr = logrank_test(a.day, c.day, a.event, c.event)
    pex, how = exact_logrank(d.day.values, d.event.values, (d.group == g1).astype(int).values)
    s1, n1, s0, n0 = int((a.event == 0).sum()), len(a), int((c.event == 0).sum()), len(c)
    fe = stats.fisher_exact([[s1, n1 - s1], [s0, n0 - s0]])[1]
    return dict(block=b, test_group=g1, ref_group=g0, surv_test=f'{s1}/{n1}', surv_ref=f'{s0}/{n0}',
                risk_diff_pct=round(100 * (s1 / n1 - s0 / n0), 1), logrank_chi2=round(lr.test_statistic, 2),
                p_logrank_asymptotic=lr.p_value, p_logrank_permutation=pex, perm_method=how, p_fisher_exact=fe)

pairs = []
for b in sv.block.unique():
    gs = list(sv[sv.block == b].group.unique())
    def add(g1, g0):
        if g1 in gs and g0 in gs:
            r = contrast(b, g1, g0)
            if r: pairs.append(r)
    add('PSLN-344', 'Sham'); add('PSLN-344', 'PSLN-212'); add('PSLN-344', 'CMP-204'); add('PSLN-344', 'PSLN-212(Y)')
    add('PSLN-212', 'Sham'); add('CMP-204', 'Sham'); add('PSLN-212(Y)', 'Sham'); add('PSLN-344', 'Untreated'); add('PSLN-212(Y)', 'Untreated')
    add('3d Vaccine+PSLN-344', '3d Vaccine'); add('3d Vaccine+PSLN-344', '3d PSLN-344'); add('3d PSLN-344', '3d Vaccine')
    add('Naive+PSLN-344', 'Naive+PSLN-212'); add('Imprinting+PSLN-344', 'Imprinting+PSLN-212')
    add('Imprinting+PSLN-212', 'Naive+PSLN-212'); add('Imprinting+PSLN-344', 'Naive+PSLN-344')
    add('PSLN-344Y', 'Sham'); add('PSLN-212Y', 'Sham'); add('PSLN-344Y', 'PSLN-212Y')
    add('PSLN-344(Y)', 'Sham'); add('CMP-204(Y)', 'Sham'); add('PSLN-344(Y)', 'CMP-204(Y)'); add('Sham', 'Naive'); add('PSLN-344(Y)', 'Naive')
T3 = pd.DataFrame(pairs)
T3.to_csv(os.path.join(HERE, 'tables', 'T03_survival_contrasts.csv'), index=False)

# ---------------- pooled / stratified analyses ----------------
def pooled(blocks, g1, g0, label, relabel=None):
    d = sv[sv.block.isin(blocks) & (~sv.day_missing)].copy()
    if relabel: d['group'] = d.group.replace(relabel)
    d = d[d.group.isin([g1, g0])]
    OE = V = 0.0
    for b, x in d.groupby('block'):
        oe, v = lr_stat(x.day.values, x.event.values, (x.group == g1).astype(int).values)
        OE += oe; V += v
    chi2 = OE * OE / V
    p = stats.chi2.sf(chi2, 1)
    # all rows (incl. the one record with a missing day) for the proportion
    dall = sv[sv.block.isin(blocks)].copy()
    if relabel: dall['group'] = dall.group.replace(relabel)
    a, c = dall[dall.group == g1], dall[dall.group == g0]
    s1, n1, s0, n0 = int((a.event == 0).sum()), len(a), int((c.event == 0).sum()), len(c)
    l1, h1 = cp(s1, n1); l0, h0 = cp(s0, n0)
    # Mantel-Haenszel risk difference (stratified by experiment), Greenland-Robins variance
    num = den = 0.0; vnum = 0.0
    for b in blocks:
        x = dall[dall.block == b]; xa, xc = x[x.group == g1], x[x.group == g0]
        if len(xa) == 0 or len(xc) == 0: continue
        a1, m1, a0, m0 = (xa.event == 0).sum(), len(xa), (xc.event == 0).sum(), len(xc)
        w = m1 * m0 / (m1 + m0)
        num += w * (a1 / m1 - a0 / m0); den += w
        vnum += (a1 * (m1 - a1) * m0 ** 3 + a0 * (m0 - a0) * m1 ** 3) / (m1 * m0 * (m1 + m0) ** 2)
    rd = num / den; se = math.sqrt(vnum) / den
    return dict(analysis=label, blocks=' '.join(blocks), test_group=g1, ref_group=g0, surv_test=f'{s1}/{n1}',
                surv_test_pct=round(100 * s1 / n1, 1), test_ci95=f'{100*l1:.1f}-{100*h1:.1f}',
                surv_ref=f'{s0}/{n0}', surv_ref_pct=round(100 * s0 / n0, 1), ref_ci95=f'{100*l0:.1f}-{100*h0:.1f}',
                MH_risk_diff_pct=round(100 * rd, 1), MH_rd_ci95=f'{max(-100, 100*(rd-1.96*se)):.1f} to {min(100, 100*(rd+1.96*se)):.1f}',
                stratified_logrank_chi2=round(chi2, 2), p_stratified_logrank=p)

early = ['S03-I', 'S03-J', 'S06-A', 'S06-B', 'S06-C', 'S06-D']          # aged BALB/c, challenge d2-d14 after one dose
d60 = ['S06-E', 'S06-F', 'S06-G']                                          # aged BALB/c, challenge d60
het14 = ['S06-A', 'S06-C']; d3 = ['S06-B', 'S06-D']
strains = ['S15-L', 'S15-N']
imp = ['S06-E(r71)', 'S06-F(r71)']
P = []
P.append(pooled(early, 'PSLN-344', 'Sham', 'Aged BALB/c, single dose, challenge d2-d14 (6 expts)'))
P.append(pooled(early, 'PSLN-344', 'PSLN-212', 'Aged BALB/c, single dose, challenge d2-d14 (6 expts)'))
P.append(pooled(early, 'PSLN-212', 'Sham', 'Aged BALB/c, single dose, challenge d2-d14 (6 expts)'))
noJ = ['S03-I', 'S06-A', 'S06-B', 'S06-C', 'S06-D']
P.append(pooled(noJ, 'PSLN-344', 'Sham', 'Same, excluding S03-J (age not stated in block) (5 expts)'))
P.append(pooled(noJ, 'PSLN-344', 'PSLN-212', 'Same, excluding S03-J (age not stated in block) (5 expts)'))
P.append(pooled(['S06-A', 'S06-B', 'S06-C', 'S06-D'], 'PSLN-344', 'Sham', 'Aged BALB/c heterosubtypic only, d3+d14 (4 expts)'))
P.append(pooled(['S06-A', 'S06-B', 'S06-C', 'S06-D'], 'PSLN-344', 'PSLN-212', 'Aged BALB/c heterosubtypic only, d3+d14 (4 expts)'))
P.append(pooled(['S06-B', 'S06-D'], 'PSLN-344', 'PSLN-212', 'Aged BALB/c heterosubtypic, challenge d3 only (2 expts)'))
P.append(pooled(['S06-A', 'S06-C'], 'PSLN-344', 'PSLN-212', 'Aged BALB/c heterosubtypic, challenge d14 only (2 expts)'))
P.append(pooled(['S06-A', 'S06-B', 'S06-C', 'S06-D'], 'PSLN-344', 'PSLN-212(Y)', 'Aged+344 vs young+212 benchmark, heterosubtypic d3+d14 (4 expts)'))
P.append(pooled(['S03-I', 'S06-A', 'S06-B', 'S06-C', 'S06-D'], 'PSLN-344', 'PSLN-212(Y)', 'Aged+344 vs young+212 benchmark, d3-d14 (5 expts)'))
P.append(pooled(d60, 'PSLN-344', 'Sham', 'Aged BALB/c, challenge d60 (3 expts)'))
P.append(pooled(d60, 'PSLN-344', 'PSLN-212', 'Aged BALB/c, challenge d60 (3 expts)'))
P.append(pooled(d60, 'PSLN-344', 'PSLN-212(Y)', 'Aged+344 vs young+212 benchmark, d60 (3 expts)'))
P.append(pooled(d60, 'PSLN-344', 'Untreated', 'Aged+344 challenged vs age-matched untreated UNCHALLENGED, d60 (3 expts)'))
P.append(pooled(d60, 'PSLN-212(Y)', 'Untreated', 'Young+212 challenged vs aged untreated UNCHALLENGED, d60 (3 expts)'))
P.append(pooled(strains, 'PSLN-344', 'Sham', 'Aged C57BL/6 + Swiss Webster (2 expts)'))
P.append(pooled(strains, 'PSLN-344', 'PSLN-212', 'Aged C57BL/6 + Swiss Webster (2 expts)'))
rl = {'Naive+PSLN-344': 'PSLN-344', 'Imprinting+PSLN-344': 'PSLN-344', 'Naive+PSLN-212': 'PSLN-212', 'Imprinting+PSLN-212': 'PSLN-212'}
P.append(pooled(imp, 'PSLN-344', 'PSLN-212', '14-mo BALB/c, naive or PR8-imprinted (2 expts, 4 arms each)', relabel=rl))
T4 = pd.DataFrame(P)
T4.to_csv(os.path.join(HERE, 'tables', 'T04_survival_pooled.csv'), index=False)

# d14-type vs d60 within PSLN-344 (waning?) -- Fisher on pooled counts (exploratory; different experiments)
def tot(blocks, g):
    d = sv[sv.block.isin(blocks) & (sv.group == g)]
    return int((d.event == 0).sum()), len(d)
s_e, n_e = tot(['S06-A', 'S06-B', 'S06-C', 'S06-D'], 'PSLN-344'); s_l, n_l = tot(d60, 'PSLN-344')
s_u, n_u = tot(d60, 'Untreated')
extra = [
 dict(q='PSLN-344 aged: heterosubtypic d3/d14 vs d60 (waning?)', a=f'{s_e}/{n_e}', b=f'{s_l}/{n_l}', p_fisher=stats.fisher_exact([[s_e, n_e - s_e], [s_l, n_l - s_l]])[1]),
 dict(q='d60: PSLN-344 challenged vs Untreated unchallenged (attrition ceiling)', a=f'{s_l}/{n_l}', b=f'{s_u}/{n_u}', p_fisher=stats.fisher_exact([[s_l, n_l - s_l], [s_u, n_u - s_u]])[1]),
]
lo, hi = cp(n_u - s_u, n_u)
extra.append(dict(q='Background 14-day mortality, untreated unchallenged aged mice (S06-E/F/G)', a=f'{n_u - s_u}/{n_u} deaths', b=f'95% CI {100*lo:.1f}-{100*hi:.1f}%', p_fisher=np.nan))
T4b = pd.DataFrame(extra); T4b.to_csv(os.path.join(HERE, 'tables', 'T04b_survival_extra.csv'), index=False)

# ---------------- sensitivity: resolve every survival-table / weight-table conflict AGAINST PSLN-344 ----------------
# (deaths implied by the paired body-weight table: blank-after or value frozen to the end; see 03_integrity_checks.py CHECK 6)
#   S06-D  PSLN-344 7/7 -> 5/7 (S15-D shows two frozen trajectories from d8)
#   S03-I  PSLN-212 0/7 -> 3/7 (S13-F shows three recovering animals)
#   S03-J  comparator 'PSLN-212' 3/10 -> 4/10 (S13-G middle group: four animals back to ~100 %)
#   d60:   survival tables already give the lower PSLN-344 counts (S06-E 5/7 vs 6/7 by weight; S06-G 4/7 vs 5-7/7) -> unchanged
def fisher_pool(a, b):
    return stats.fisher_exact([[a[0], a[1] - a[0]], [b[0], b[1] - b[0]]])[1]
base344 = tot(early, 'PSLN-344'); base212 = tot(early, 'PSLN-212'); basesham = tot(early, 'Sham')
worst344 = (base344[0] - 2, base344[1]); worst212 = (base212[0] + 3 + 1, base212[1])
h = tot(['S15-H'], '3d Vaccine+PSLN-344')
sens = []
for lab, a, b2, c in [('survival tables as printed', base344, base212, basesham), ('all table conflicts resolved against PSLN-344', worst344, worst212, basesham)]:
    l, u = cp(a[0], a[1]); l2, u2 = cp(b2[0], b2[1])
    sens.append(dict(scenario=lab, PSLN344=f'{a[0]}/{a[1]}', PSLN344_pct=round(100 * a[0] / a[1], 1), PSLN344_ci95=f'{100*l:.1f}-{100*u:.1f}',
                     PSLN212=f'{b2[0]}/{b2[1]}', PSLN212_pct=round(100 * b2[0] / b2[1], 1), PSLN212_ci95=f'{100*l2:.1f}-{100*u2:.1f}',
                     Sham=f'{c[0]}/{c[1]}', p_fisher_344_vs_212=fisher_pool(a, b2), p_fisher_344_vs_sham=fisher_pool(a, c)))
allearly = (base344[0] + h[0], base344[1] + h[1]); l, u = cp(*allearly)
sens.append(dict(scenario='all aged-BALB/c PSLN-344 arms challenged d2-d14 incl. S15-H (no matched Sham/212 arm there)', PSLN344=f'{allearly[0]}/{allearly[1]}',
                 PSLN344_pct=round(100 * allearly[0] / allearly[1], 1), PSLN344_ci95=f'{100*l:.1f}-{100*u:.1f}'))
T4c = pd.DataFrame(sens); T4c.to_csv(os.path.join(HERE, 'tables', 'T04c_survival_sensitivity.csv'), index=False)

pd.set_option('display.width', 280); pd.set_option('display.max_rows', 500); pd.set_option('display.max_colwidth', 70)
print(T4c.to_string()); print()
print(T2.drop(columns=['host', 'vaccine', 'challenge', 'cells']).to_string())
print(); print(T3.to_string()); print(); print(T4.drop(columns=['blocks']).to_string()); print(); print(T4b.to_string())
