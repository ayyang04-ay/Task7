import pandas as pd, numpy as np
from scipy.optimize import curve_fit
from scipy import stats
c = pd.read_csv('tidy_continuous.csv'); c['level'] = c.level.fillna('').astype(str)
bw = pd.read_csv('tidy_bodyweight.csv')
out = {}
# ---- S08-D post-vaccination body weight (tolerability)
d = bw[(bw.block == 'S08-D')]
rows = []
for g, x in d.groupby('group', sort=False):
    per_animal_min = x.groupby('col').value.min()
    day_means = x.groupby('day').value.mean()
    rows.append(dict(group=g, n_animals=x.col.nunique(), mean_of_animal_nadirs=per_animal_min.mean(), lowest_animal_nadir=per_animal_min.min(),
                     nadir_day_of_group_mean=int(day_means.idxmin()), group_mean_at_nadir=day_means.min(),
                     n_missing_day10=int(x[(x.day == 10)].value.isna().sum())))
T = pd.DataFrame(rows); print('S08-D post-vaccination weights'); print(T.round(2).to_string(index=False)); T.to_csv('safety_S08D_bodyweight.csv', index=False)
# ---- S10-A CNS transcripts
rows = []
for an in ['Ifnb1', 'Tnf', 'Isg15']:
    x = c[c.block == f'S10-A_{an}']
    g = {k: v.value.values for k, v in x.groupby('group')}
    for ref in ['PBS', 'Sham']:
        for tst in ['PSLN-344', 'CT']:
            a, b = np.log2(g[tst]), np.log2(g[ref])
            p = stats.ttest_ind(a, b, equal_var=False).pvalue
            rows.append(dict(analyte=an, test=tst, reference=ref, mean_test=g[tst].mean(), mean_ref=g[ref].mean(),
                             geo_fold=2 ** (a.mean() - b.mean()), p_welch_log=p))
T = pd.DataFrame(rows); print('\nS10-A CNS 36 h'); print(T.round(4).to_string(index=False)); T.to_csv('safety_S10A_CNS.csv', index=False)
# ---- S08-A dose response, Emax fit
x = c[c.block == 'S08-A'].copy(); x['dose'] = x.level.astype(float)
def emax(D, E0, Emax, ED50, h): return E0 + Emax * D ** h / (ED50 ** h + D ** h)
rows = []
for g, y in x.groupby('group', sort=False):
    try:
        p, cov = curve_fit(emax, y.dose, y.value, p0=[1, y.value.max(), 10, 1.5], bounds=([0, 0, 0.1, 0.3], [5, 500, 200, 6]), maxfev=20000)
        se = np.sqrt(np.diag(cov))
        rows.append(dict(group=g, E0=p[0], Emax=p[1], ED50_ug=p[2], ED50_se=se[2], hill=p[3],
                         mean_at_20ug=y[y.dose == 20].value.mean(), mean_at_40ug=y[y.dose == 40].value.mean(), mean_at_10ug=y[y.dose == 10].value.mean(), mean_at_5ug=y[y.dose == 5].value.mean()))
    except Exception as e:
        print('fit fail', g, e)
T = pd.DataFrame(rows); print('\nS08-A Emax fits'); print(T.round(2).to_string(index=False)); T.to_csv('dose_response_S08A_emax.csv', index=False)
# dose of PSLN-344 giving the same Ifnb1 as PSLN-212 at 20 and 40 ug
p344 = T[T.group == 'PSLN-344'].iloc[0]
for target_g in ['PSLN-212']:
    for dd in [20, 40]:
        target = x[(x.group == target_g) & (x.dose == dd)].value.mean()
        # invert Emax
        E0, Em, ED50, h = p344.E0, p344.Emax, p344.ED50_ug, p344.hill
        f = (target - E0) / Em
        Deq = ED50 * (f / (1 - f)) ** (1 / h)
        print(f'PSLN-344 dose matching {target_g} at {dd} ug (Ifnb1 {target:.1f}x): {Deq:.1f} ug  -> dose-sparing ~{dd/Deq:.1f}x')
# ---- S08-B encapsulation
e = c[c.block == 'S08-B']
print('\nS08-B encapsulation efficiency (%)')
print(e.groupby('group', sort=False).value.agg(['count', 'mean', 'std', 'min', 'max']).round(2).to_string())
p = stats.ttest_ind(e[e.group == 'PSLN-344'].value, e[e.group == 'PSLN-212'].value, equal_var=False).pvalue
print('PSLN-344 vs PSLN-212 EE p(Welch)=', round(p, 3))
