import numpy as np, pandas as pd
from scipy import stats
rng = np.random.default_rng(7)
c = pd.read_csv('tidy_continuous.csv')
def v(b, g):
    x = c[(c.block == b) & (c.group == g)].value.values.astype(float)
    return x
out = []
# observed log2 SDs
for b, lab in [('S03-C', 'HAI H1N1'), ('S03-G', 'HAI H3N2'), ('S03-A', 'IgG H1N1'), ('S03-E', 'IgG H3N2')]:
    a = np.log2(np.where(v(b, 'PSLN-344') <= 0, 5, v(b, 'PSLN-344'))); p = np.log2(np.where(v(b, 'PSLN-212') <= 0, 5, v(b, 'PSLN-212')))
    sd = np.sqrt((a.var(ddof=1) + p.var(ddof=1)) / 2)
    obs = 2 ** (a.mean() - p.mean())
    thr = 2 ** (np.log2(obs) / 2)   # half the observed effect on log scale
    # n per group for 90% power to detect the threshold effect (two-sided alpha 0.05, t-test), inflate SD x1.5 for realism
    for infl in [1.0, 1.5]:
        s = sd * infl; d = np.log2(thr) / s
        n = 2
        while True:
            df = 2 * n - 2; nc = d * np.sqrt(n / 2); tcrit = stats.t.ppf(0.975, df)
            pw = 1 - stats.nct.cdf(tcrit, df, nc) + stats.nct.cdf(-tcrit, df, nc)
            if pw >= 0.9 or n > 200: break
            n += 1
        out.append(dict(endpoint=lab, observed_fold=round(obs, 2), pooled_log2_SD=round(sd, 2), SD_inflation=infl, threshold_fold_half_log_effect=round(thr, 2), n_per_group_90pct_power=n))
P = pd.DataFrame(out); print(P.to_string(index=False)); P.to_csv('design_power_continuous.csv', index=False)

# survival: Fisher exact power by simulation for assumed rates
def fisher_power(p1, p0, n, sims=4000):
    hits = 0
    for _ in range(sims):
        a = rng.binomial(n, p1); c0 = rng.binomial(n, p0)
        if stats.fisher_exact([[a, n - a], [c0, n - c0]])[1] < 0.05: hits += 1
    return hits / sims
rows = []
for p1, p0, lab in [(0.84, 0.13, 'observed pooled (S06-D removed)'), (0.70, 0.20, 'conservative: 50-pt difference'), (0.60, 0.25, 'half the observed difference (~35 pts)')]:
    for n in [8, 10, 12, 15, 18, 20, 25]:
        rows.append(dict(scenario=lab, p_PSLN344=p1, p_PSLN212=p0, n_per_group=n, power=fisher_power(p1, p0, n)))
S = pd.DataFrame(rows); print(S.pivot(index='n_per_group', columns='scenario', values='power').round(2).to_string())
S.to_csv('design_power_survival.csv', index=False)
