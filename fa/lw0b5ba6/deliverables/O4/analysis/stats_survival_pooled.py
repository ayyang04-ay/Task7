import pandas as pd, numpy as np
from scipy.stats import hypergeom
from statsmodels.stats.proportion import proportion_confint

sc = pd.read_csv('survival_counts.csv')
def cnt(block, group):
    r = sc[(sc.block == block) & (sc.group == group)].iloc[0]
    return int(r.survivors), int(r.n)

# strata: (label, block, treated group, control group)
STRATA = [('S03-I homologous H1N1 d14', 'S03-I', 'PSLN-344', 'PSLN-212'),
          ('S03-J WT H5N1 d2 (age not stated)', 'S03-J', 'PSLN-344', 'PSLN-212'),
          ('S06-A PR8 d14', 'S06-A', 'PSLN-344', 'PSLN-212'),
          ('S06-B PR8 d3', 'S06-B', 'PSLN-344', 'PSLN-212'),
          ('S06-C rgH5N1 d14', 'S06-C', 'PSLN-344', 'PSLN-212'),
          ('S06-D rgH5N1 d3', 'S06-D', 'PSLN-344', 'PSLN-212'),
          ('S06-E PR8 d60', 'S06-E', 'PSLN-344', 'PSLN-212'),
          ('S06-F rgH5N1 d60', 'S06-F', 'PSLN-344', 'PSLN-212'),
          ('S06-G Perth H3N2 d60', 'S06-G', 'PSLN-344', 'PSLN-212'),
          ("S06-E' naive (14 mo) PR8", "S06-E'(r71-98,G-K)", 'Naive+PSLN-344', 'Naive+PSLN-212'),
          ("S06-E' imprinted (14 mo) PR8", "S06-E'(r71-98,G-K)", 'Imprinting+PSLN-344', 'Imprinting+PSLN-212'),
          ("S06-F' naive (14 mo) Perth", "S06-F'(r71-98,M-Q)", 'Naive+PSLN-344', 'Naive+PSLN-212'),
          ("S06-F' imprinted (14 mo) Perth", "S06-F'(r71-98,M-Q)", 'Imprinting+PSLN-344', 'Imprinting+PSLN-212'),
          ('S15-L aged C57BL/6', 'S15-L', 'PSLN-344', 'PSLN-212'),
          ('S15-N aged Swiss Webster', 'S15-N', 'PSLN-344', 'PSLN-212')]

# weight-implied survivor counts where the linked body-weight block disagrees with the survival record
# (from bw_vs_survival_reconciliation.csv; 'alive' + 'flatline=2' counted as alive = most lenient reading)
WEIGHT_IMPLIED = {('S06-C', 'PSLN-212'): 1, ('S06-D', 'PSLN-344'): 5, ('S06-E', 'PSLN-212'): 1, ('S06-E', 'PSLN-344'): 6,
                  ('S06-G', 'PSLN-344'): 7, ('S03-I', 'PSLN-212'): 3, ('S15-L', 'PSLN-212(Y)'): 7}
# integrity status of each stratum (see integrity register)
FLAG = {'S03-I': 'major', 'S03-J': 'major', 'S06-A': 'major', 'S06-B': 'none detected', 'S06-C': 'critical', 'S06-D': 'critical',
        'S06-E': 'minor', 'S06-F': 'moderate', 'S06-G': 'major', "S06-E'(r71-98,G-K)": 'moderate', "S06-F'(r71-98,M-Q)": 'moderate',
        'S15-L': 'critical', 'S15-N': 'major'}

def exact_stratified(tables):
    """Exact conditional (stratified) test: T = sum of treated survivors; null = independent hypergeometrics."""
    dist = np.array([1.0]); lo_total = 0; obs = 0
    for (a, n1, c, n0) in tables:
        K = a + c; N = n1 + n0
        lo = max(0, K - n0); hi = min(K, n1)
        pm = np.array([hypergeom.pmf(k, N, K, n1) for k in range(lo, hi + 1)])
        dist = np.convolve(dist, pm); lo_total += lo; obs += a
    idx = obs - lo_total
    return dist[idx:].sum()

def run(name, strata, mode='recorded'):
    tabs = []; rows = []
    for lab, blk, t, c in strata:
        a, n1 = cnt(blk, t); cc, n0 = cnt(blk, c)
        if mode == 'worst':
            a = min(a, WEIGHT_IMPLIED.get((blk, t), a)); cc = max(cc, WEIGHT_IMPLIED.get((blk, c), cc))
        tabs.append((a, n1, cc, n0)); rows.append((lab, a, n1, cc, n0))
    A = sum(r[1] for r in rows); N1 = sum(r[2] for r in rows); Cc = sum(r[3] for r in rows); N0 = sum(r[4] for r in rows)
    w = [(n1 * n0 / (n1 + n0)) for (_, a, n1, cc, n0) in rows]
    rd = sum(wi * (a / n1 - cc / n0) for wi, (_, a, n1, cc, n0) in zip(w, rows)) / sum(w)
    p = exact_stratified(tabs)
    l1, h1 = proportion_confint(A, N1, method='beta'); l0, h0 = proportion_confint(Cc, N0, method='beta')
    return dict(analysis=name, strata=len(rows), PSLN344_surv=f'{A}/{N1}', PSLN344_pct=100 * A / N1, PSLN344_CI=f'{100*l1:.0f}-{100*h1:.0f}%',
                PSLN212_surv=f'{Cc}/{N0}', PSLN212_pct=100 * Cc / N0, PSLN212_CI=f'{100*l0:.0f}-{100*h0:.0f}%',
                MH_risk_difference_pct_points=100 * rd, exact_stratified_p_one_sided=p)

out = []
out.append(run('A. All aged/middle-aged strata as recorded', STRATA))
out.append(run('B. As recorded, S06-D removed (exact duplicate of S06-C)', [s for s in STRATA if s[1] != 'S06-D']))
out.append(run('C. Worst case: S06-D removed + weight-implied counts least favourable to PSLN-344', [s for s in STRATA if s[1] != 'S06-D'], mode='worst'))
out.append(run('D. Strictly >=20-month strata only (excl. S03-J age unstated, S06-E/F\' 14-mo), S06-D removed, worst case',
               [s for s in STRATA if s[1] not in ('S06-D', 'S03-J', "S06-E'(r71-98,G-K)", "S06-F'(r71-98,M-Q)")], mode='worst'))
out.append(run('E. Strata with no critical/major integrity flag only (S06-B, S06-E, S06-F, S06-E\', S06-F\')',
               [s for s in STRATA if FLAG[s[1]] in ('none detected', 'minor', 'moderate')], mode='worst'))
out.append(run('F. Single stratum with no integrity flag detected (S06-B)', [s for s in STRATA if s[1] == 'S06-B']))
O = pd.DataFrame(out)
pd.set_option('display.width', 260); pd.set_option('display.max_colwidth', 110)
print(O.to_string(index=False))
O.to_csv('survival_pooled_sensitivity.csv', index=False)

# per-stratum table with flags
rows = []
for lab, blk, t, c in STRATA:
    a, n1 = cnt(blk, t); cc, n0 = cnt(blk, c)
    rows.append(dict(stratum=lab, block=blk, PSLN344=f'{a}/{n1}', PSLN212=f'{cc}/{n0}', integrity_flag=FLAG[blk],
                     weight_implied_PSLN344=WEIGHT_IMPLIED.get((blk, t), ''), weight_implied_PSLN212=WEIGHT_IMPLIED.get((blk, c), '')))
pd.DataFrame(rows).to_csv('survival_strata_flags.csv', index=False)
print(pd.DataFrame(rows).to_string(index=False))

# background mortality in unchallenged aged controls
bg = sc[sc.group == 'Untreated']
d = int(bg.deaths.sum()); n = int(bg.n.sum()); lo, hi = proportion_confint(d, n, method='beta')
print(f'\nBackground 14-day mortality, untreated unchallenged aged (S06-E/F/G): {d}/{n} = {100*d/n:.1f}% (95% CI {100*lo:.1f}-{100*hi:.1f}%)')
