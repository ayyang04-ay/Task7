import pandas as pd, numpy as np
from scipy import stats
from statsmodels.duration.survfunc import survdiff
from statsmodels.stats.contingency_tables import StratifiedTable
from statsmodels.stats.proportion import proportion_confint

s = pd.read_csv('tidy_survival.csv')
# one PSLN-344 animal in S03-J has no day value (S03!G46 blank, J46=0): it is censored; use end of follow-up (21)
miss = s.days.isna()
print('rows with missing day value:', s[miss][['block', 'group', 'cell_days', 'cell_event']].to_dict('records'))
s.loc[miss, 'days'] = s.loc[miss].block.map({'S03-J': 21})

def logrank(d1, d2):
    t = np.r_[d1.days, d2.days]; e = np.r_[d1.event, d2.event]; g = np.r_[np.zeros(len(d1)), np.ones(len(d2))]
    if e.sum() == 0: return np.nan
    try:
        chi2, p = survdiff(t, e, g)
        return p
    except Exception:
        return np.nan

def median_surv(d):
    # KM median
    times = np.sort(d.days.unique()); S = 1.0; n = len(d)
    for tt in times:
        at_risk = (d.days >= tt).sum(); ev = ((d.days == tt) & (d.event == 1)).sum()
        if at_risk > 0: S *= (1 - ev / at_risk)
        if S <= 0.5: return tt
    return np.nan  # not reached

rows = []
COMP = [('PSLN-344', 'PSLN-212'), ('PSLN-344', 'Sham'), ('PSLN-212', 'Sham'), ('PSLN-344', 'PSLN-212(Y)'), ('PSLN-344', 'Untreated'),
        ('PSLN-344(Y)', 'PSLN-212(Y)'), ('PSLN-344(Y)', 'Sham'), ('PSLN-344(Y)', 'Naive'), ('CMP-204(Y)', 'Sham'), ('CMP-204', 'Sham'),
        ('PSLN-344', 'CMP-204'), ('Naive+PSLN-344', 'Naive+PSLN-212'), ('Imprinting+PSLN-344', 'Imprinting+PSLN-212'),
        ('Imprinting+PSLN-344', 'Naive+PSLN-344'), ('Imprinting+PSLN-212', 'Naive+PSLN-212'),
        ('3d Vaccine+PSLN-344', '3d Vaccine'), ('3d Vaccine+PSLN-344', '3d PSLN-344'), ('3d PSLN-344', '3d Vaccine')]
for b, d in s.groupby('block', sort=False):
    G = {g: x for g, x in d.groupby('group', sort=False)}
    for g, x in G.items():
        n = len(x); surv = int((x.event == 0).sum())
        lo, hi = proportion_confint(surv, n, method='beta')
        rows.append(dict(block=b, kind='group', g1=g, n1=n, surv1=surv, frac1=surv / n, ci_low=lo, ci_high=hi, median_days=median_surv(x),
                         desc=x.desc.iloc[0], cohort=x.cohort.iloc[0]))
    for g1, g2 in COMP:
        if g1 in G and g2 in G:
            a, c = G[g1], G[g2]
            s1, s2 = int((a.event == 0).sum()), int((c.event == 0).sum())
            fisher = stats.fisher_exact([[s1, len(a) - s1], [s2, len(c) - s2]])[1]
            rows.append(dict(block=b, kind='comparison', g1=g1, g2=g2, n1=len(a), surv1=s1, n2=len(c), surv2=s2,
                             diff_pct_points=100 * (s1 / len(a) - s2 / len(c)), p_logrank=logrank(a, c), p_fisher=fisher,
                             desc=a.desc.iloc[0], cohort=a.cohort.iloc[0]))
R = pd.DataFrame(rows)
R.to_csv('survival_tests.csv', index=False)
pd.set_option('display.width', 260); pd.set_option('display.max_rows', 300); pd.set_option('display.max_colwidth', 60)
print(R[R.kind == 'comparison'][['block', 'g1', 'g2', 'surv1', 'n1', 'surv2', 'n2', 'diff_pct_points', 'p_logrank', 'p_fisher']].to_string(index=False))
