"""
S08-A dose-response of lung Ifnb1 (16 h) : 1, 5, 10, 20, 40 ug per animal, n = 3 per dose.
Hill model on the log scale with baseline fixed at 1 (values are fold vs untreated):
     fold(d) = 1 + (Emax - 1) * d^h / (ED50^h + d^h)
Parametric fit (least squares on log10 fold) + bootstrap CI (resampling animals within dose).
"""
from paths import TABLES, FIGS, OUT as OUTDIR, BUILD, PANDOC
import pandas as pd, numpy as np, warnings
from scipy.optimize import least_squares
import psln_blocks as pb
warnings.filterwarnings('ignore')
pd.set_option('display.width', 250)
df = pb.tidy(); d = df[df.block == 'S08-A'].copy(); d['dose'] = d.x.astype(float)
rng = np.random.default_rng(20261101)

def model(p, dose):
    emax, ed50, h = p
    return 1 + (emax - 1) * dose ** h / (ed50 ** h + dose ** h)
def fit(dose, y):
    best = None
    for e0 in (y.max(), 1.5 * y.max()):
        for ed in (5, 10, 20):
            for h0 in (1, 2, 3):
                r = least_squares(lambda p: np.log10(model(p, dose)) - np.log10(y), x0=[e0, ed, h0], bounds=([1.01, 0.5, 0.3], [500, 200, 8]))
                if best is None or r.cost < best.cost: best = r
    return best.x, best.cost

rows = []; means = []
for g, t in d.groupby('group', sort=False):
    dose = t.dose.to_numpy(); y = t.value.to_numpy()
    p, cost = fit(dose, y)
    bs = []
    for _ in range(600):
        idx = np.concatenate([rng.choice(np.where(dose == dd)[0], 3) for dd in np.unique(dose)])
        try:
            pb_, _ = fit(dose[idx], y[idx]); bs.append(pb_)
        except Exception: pass
    bs = np.array(bs)
    lo = np.percentile(bs, 2.5, axis=0); hi = np.percentile(bs, 97.5, axis=0)
    rows.append(dict(group=g, Emax_fold=p[0], Emax_lo=lo[0], Emax_hi=hi[0], ED50_ug=p[1], ED50_lo=lo[1], ED50_hi=hi[1], hill=p[2], hill_lo=lo[2], hill_hi=hi[2],
                     pred_20ug=model(p, 20), frac_of_Emax_at_20ug=(model(p, 20) - 1) / (p[0] - 1)))
    m = t.groupby('dose').value.agg(['mean', 'std', 'count'])
    for dd, r in m.iterrows(): means.append(dict(group=g, dose_ug=dd, mean_fold=r['mean'], sd=r['std'], n=int(r['count'])))
F = pd.DataFrame(rows); M = pd.DataFrame(means)
print(M.pivot(index='dose_ug', columns='group', values='mean_fold').round(2))
print(F.round(2).to_string())
F.to_csv(TABLES + 'T14_dose_response_fit.csv', index=False); M.to_csv(TABLES + 'T14b_dose_response_means.csv', index=False)
# model-free statements
pv = M.pivot(index='dose_ug', columns='group', values='mean_fold')
print('\nPSLN-344 / PSLN-212 ratio of mean Ifnb1 by dose:'); print((pv['PSLN-344'] / pv['PSLN-212']).round(2))
print('PSLN-344 step 20->40 ug: x', round(pv.loc[40, 'PSLN-344'] / pv.loc[20, 'PSLN-344'], 2), '; 10->20 ug: x', round(pv.loc[20, 'PSLN-344'] / pv.loc[10, 'PSLN-344'], 2))
print('PSLN-344 at 10 ug', round(pv.loc[10, 'PSLN-344'], 1), 'vs PSLN-212 at 40 ug', round(pv.loc[40, 'PSLN-212'], 1))
# dose of PSLN-344 giving the same Ifnb1 as PSLN-212 at 20 ug (inverse prediction from the fitted curve)
from scipy.optimize import brentq
p344 = F[F.group == 'PSLN-344'].iloc[0]; target = pv.loc[20, 'PSLN-212']
dose_eq = brentq(lambda x: model([p344.Emax_fold, p344.ED50_ug, p344.hill], x) - target, 0.5, 40)
print('PSLN-344 dose matching PSLN-212@20ug (', round(target, 1), 'fold):', round(dose_eq, 1), 'ug')
