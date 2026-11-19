import numpy as np, pandas as pd
from scipy import stats
from statsmodels.stats.power import TTestIndPower
def exact_power_fisher(p1, p2, n, alpha=0.05):
    # exact power: sum over all outcomes (a,b) of P(a)P(b) * 1[Fisher two-sided p < alpha]
    pa = stats.binom.pmf(np.arange(n + 1), n, p1); pb = stats.binom.pmf(np.arange(n + 1), n, p2)
    pw = 0.0
    for a in range(n + 1):
        for b in range(n + 1):
            if pa[a] * pb[b] < 1e-12: continue
            if stats.fisher_exact([[a, n - a], [b, n - b]])[1] < alpha:
                pw += pa[a] * pb[b]
    return pw
def n_for(p1, p2, target=0.8):
    for n in range(4, 80):
        pw = exact_power_fisher(p1, p2, n)
        if pw >= target: return n, pw
bg = 4 / 21
rows = []
for lab, p1, p2 in [('PSLN-344 vs PSLN-212, observed pooled 85% vs 14%', .85, .14), ('PSLN-344 vs PSLN-212, conservative 70% vs 20%', .70, .20),
                    ('PSLN-344 vs Mn-only liposome, assumed 75% vs 30%', .75, .30), ('PSLN-344 vs IM benchmark, assumed 75% vs 40%', .75, .40)]:
    n, pw = n_for(p1, p2)
    rows.append(dict(endpoint='14-day survival (Fisher exact, two-sided alpha 0.05, exact power >= 80%)', scenario=lab, n_per_arm=n,
                     exact_power=round(pw, 3), n_per_arm_after_background_mortality=int(np.ceil(n / (1 - bg)))))
C = pd.read_csv('/tmp/work/tidy/continuous.csv'); sds = []
for b in ['S03-C', 'S03-G']:
    for g in ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']:
        x = np.log2(np.clip(C[(C.block == b) & (C.group == g)].value.values, 5, None)); sds.append(x.std(ddof=1))
sd = np.sqrt(np.mean(np.square(sds))); tp = TTestIndPower()
for fold in [4, 2, 1.5]:
    d = np.log2(fold) / sd
    rows.append(dict(endpoint=f'HI GMT ratio (two-sample t on log2; pooled SD {sd:.2f} from S03-C/G)', scenario=f'{fold}x', n_per_arm=int(np.ceil(tp.solve_power(effect_size=d, alpha=0.05, power=0.8))),
                     exact_power=0.8, n_per_arm_after_background_mortality=None))
R = pd.DataFrame(rows); R.to_csv('/tmp/work/tidy/sample_size.csv', index=False)
print(R.to_string(index=False)); print('background 14-d mortality used: 4/21 =', round(bg, 3))
