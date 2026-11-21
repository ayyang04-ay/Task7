"""Dose-response of lung Ifnb1 induction at 16 h (S08-A).  Model: E(d) = 1 + Emax * d^h / (ED50^h + d^h)  (baseline fold = 1).
Fitted on the log scale (qPCR fold changes are multiplicative).  Bootstrap CIs by resampling animals within dose."""
import numpy as np, pandas as pd
from scipy.optimize import least_squares, brentq
import tidy
rng = np.random.default_rng(7)
d = tidy.get('S08-A')
def model(p, x):
    emax, ed50, h = p
    return 1 + emax * x ** h / (ed50 ** h + x ** h)
def fit(x, y, p0=(20, 10, 2)):
    f = lambda p: np.log(model(p, x)) - np.log(y)
    r = least_squares(f, p0, bounds=([0.1, 0.5, 0.5], [500, 200, 8]))
    return r.x
rows = []
fits = {}
for g in tidy.groups('S08-A'):
    s = d[d.group == g]; x = s.x.values.astype(float); y = s.value.values
    p = fit(x, y); fits[g] = p
    boots = []
    for _ in range(2000):
        idx = np.concatenate([rng.choice(np.where(x == dv)[0], size=(x == dv).sum(), replace=True) for dv in np.unique(x)])
        try:
            boots.append(fit(x[idx], y[idx], p0=p))
        except Exception:
            pass
    boots = np.array(boots)
    lo, hi = np.percentile(boots, [2.5, 97.5], axis=0)
    m = s.groupby('x')['value'].mean()
    rows.append(dict(prep=g, Emax=p[0], Emax_lo=lo[0], Emax_hi=hi[0], ED50_ug=p[1], ED50_lo=lo[1], ED50_hi=hi[1], hill=p[2],
                     fold_20ug=m[20.0], fold_40ug=m[40.0], pct_of_40ug_reached_at_20ug=100 * m[20.0] / m[40.0]))
R = pd.DataFrame(rows)
pd.set_option('display.width', 200)
print(R.round(2).to_string(index=False))
R.to_csv('../tables/T8_dose_response_S08A.csv', index=False)
# dose of PSLN-344 matching reference responses
p344 = fits['PSLN-344']
def dose_for(target):
    return brentq(lambda x: model(p344, x) - target, 0.5, 40)
ref = {'PSLN-212 @20 ug (S08-A mean)': d[(d.group == 'PSLN-212') & (d.x == 20)].value.mean(),
       'PSLN-212 @40 ug (S08-A mean)': d[(d.group == 'PSLN-212') & (d.x == 40)].value.mean(),
       'CMP-204 @20 ug (S08-A mean)': d[(d.group == 'CMP-204') & (d.x == 20)].value.mean(),
       'young PSLN-212 @20 ug (S01-A 16h mean)': tidy.vec('S01-A 16h', 'PSLN-212(Y)').mean()}
for k, v in ref.items():
    print(f'PSLN-344 dose giving the same Ifnb1 induction as {k} = {v:.1f}-fold: {dose_for(v):.1f} ug (model interpolation)')
# observed-means interpolation as a model-free check (log-linear between tested doses)
m = d[d.group == 'PSLN-344'].groupby('x')['value'].mean()
for k, v in ref.items():
    xs = m.index.values; ys = m.values
    print(f'   model-free (log-log interpolation of observed means) for {v:.1f}-fold: {np.exp(np.interp(np.log(v), np.log(ys), np.log(xs))):.1f} ug')
