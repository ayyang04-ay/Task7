"""Sample-size / power calculations for the proposed studies, using effect sizes and variances estimated from our own data."""
import numpy as np, pandas as pd, itertools
from scipy import stats
import tidy

def fisher_power(p1, p0, n1, n0=None, alpha=0.05):
    n0 = n0 or n1
    pw = 0.0
    for a in range(n1 + 1):
        pa = stats.binom.pmf(a, n1, p1)
        if pa < 1e-12: continue
        for c in range(n0 + 1):
            pc = stats.binom.pmf(c, n0, p0)
            if pc < 1e-12: continue
            if stats.fisher_exact([[a, n1 - a], [c, n0 - c]])[1] <= alpha:
                pw += pa * pc
    return pw

print('=== (a) Survival end-point, two-sided Fisher exact, alpha 0.05')
scen = [('PSLN-344 86% vs PSLN-212 14% (flag-robust pooled acute: 18/21 vs 3/21; S06-A/B/C)', .857, .143),
        ('PSLN-344 93% vs PSLN-212 18% (as-printed pooled acute: 42/45 vs 8/45)', .933, .178),
        ('PSLN-344 86% vs 43% (if PSLN-212 really protects 3/7 as the S13-F traces imply)', .857, .43),
        ('PSLN-344 67% vs 5% at d60 (14/21 vs 1/21; S06-E/F/G)', .667, .048),
        ('PSLN-344 86% vs licensed-type comparator 50% (assumed, no data)', .857, .50),
        ('PSLN-344 86% vs comparator 60% (assumed, no data)', .857, .60)]
rows = []
for lab, p1, p0 in scen:
    r = dict(scenario=lab)
    for n in [8, 10, 12, 15, 20, 25, 30]:
        r[f'n={n}'] = round(fisher_power(p1, p0, n), 2)
    rows.append(r)
PW = pd.DataFrame(rows); pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 95)
print(PW.to_string(index=False)); PW.to_csv('../tables/T12_power_survival.csv', index=False)

print('\n=== (b) Titre end-points: pooled within-group SD of log2 titre (adjuvanted groups) from our data')
sds = {}
for b in ['S03-A', 'S03-C', 'S03-D', 'S03-E', 'S03-G', 'S03-H']:
    v = []
    for g in ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']:
        x = np.log2(np.where(tidy.vec(b, g) <= 0, 5, tidy.vec(b, g))); v.append(x.var(ddof=1))
    sds[b] = np.sqrt(np.mean(v))
print({k: round(v, 2) for k, v in sds.items()})
def n_two_sample(delta, sd, alpha=0.05, power=0.9, one_sided=False):
    for n in range(3, 500):
        df = 2 * n - 2; nc = delta / (sd * np.sqrt(2 / n))
        tcrit = stats.t.ppf(1 - (alpha if one_sided else alpha / 2), df)
        pw = 1 - stats.nct.cdf(tcrit, df, nc)
        if pw >= power: return n
for lab, sd in [('HAI (S03-C/G)', max(sds['S03-C'], sds['S03-G'])), ('Neutralising (S03-D/H)', max(sds['S03-D'], sds['S03-H'])), ('IgG ELISA (S03-A/E)', max(sds['S03-A'], sds['S03-E']))]:
    print(f'  {lab}: SD log2 = {sd:.2f}; n/group for 90% power: 4-fold difference {n_two_sample(2, sd)}, 2-fold difference {n_two_sample(1, sd)}; '
          f'non-inferiority vs young benchmark with 2-fold margin (one-sided 0.025, true ratio 1) {n_two_sample(1, sd, alpha=0.025, one_sided=True)}, '
          f'with 1.5-fold margin {n_two_sample(np.log2(1.5), sd, alpha=0.025, one_sided=True)}')

print('\n=== (c) Tolerability: body-weight nadir after immunisation (S08-D)')
v = []
for g in ['PSLN-212', 'PSLN-344', 'Vaccine', 'PSLN-212(Y)', 'CMP-204']:
    d = tidy.get('S08-D'); s = d[(d.group == g) & (d.x > 0)].groupby('rep')['value'].min(); v.append(s.var(ddof=1))
sd = np.sqrt(np.mean(v)); print(f'  pooled SD of per-animal nadir = {sd:.2f} points')
for delta in [2, 3, 5]:
    print(f'  n/group to detect a {delta}-point difference in nadir with 90% power: {n_two_sample(delta, sd)}')
# what the current n=5 could detect
for n in [5]:
    for delta in np.arange(1, 8, 0.5):
        df = 2 * n - 2; nc = delta / (sd * np.sqrt(2 / n)); pw = 1 - stats.nct.cdf(stats.t.ppf(0.975, df), df, nc)
        if pw >= 0.8:
            print(f'  with the n=5 actually used, 80% power only for differences >= {delta} points'); break

print('\n=== (d) Durability vs background mortality in aged animals')
print('  observed: PSLN-344 d60 survival 14/21 (67%) vs unchallenged untreated 17/21 (81%); challenged sham 0/21')
for n in [15, 20, 30, 40]:
    print(f'  n={n}/group: power to distinguish 67% from 93% (acute level) = {fisher_power(.667, .933, n):.2f}; 67% vs 81% (background) = {fisher_power(.667, .81, n):.2f}')
print('\n=== (e) natural attrition allowance')
print('  untreated aged animals lost over a 14-d window at ~22 months: 4/21 = 19% (95% CI 5-42) -> inflate aged-animal group sizes by >=25% for studies running past 22 months')
