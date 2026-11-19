import pandas as pd, numpy as np, warnings
from scipy import stats
from statsmodels.duration.survfunc import survdiff
from statsmodels.stats.contingency_tables import StratifiedTable
warnings.filterwarnings('ignore')
S = pd.read_csv('/tmp/work/tidy/survival.csv')
S.loc[S.days.isna(), 'days'] = 21.0
aged_exps = ['S03-I', 'S03-J', 'S06-A', 'S06-B', 'S06-C', 'S06-D', 'S06-E', 'S06-F', 'S06-G', 'S15-L', 'S15-N']
flagged = {'S03-I': 'survival contradicts paired weights S13-F (PSLN-212 7/7 dead vs 4/7); group sets differ',
           'S03-J': 'stated n 9 vs 10 observed; PSLN-344 animal without time value; paired weights S13-G contradict',
           'S06-C': 'PSLN-212 survival vector identical to S06-D',
           'S06-D': 'PSLN-212 vector identical to S06-C; paired weights S15-D imply 2 PSLN-344 deaths (0 recorded)',
           'S06-G': '3/7 unchallenged Untreated controls died (background mortality = PSLN-344 outcome)',
           'S15-L': 'challenge virus not stated; companion weights (S15-M) recycled from S09-E / S15-A',
           'S15-N': 'challenge virus not stated'}
clean = [e for e in aged_exps if e not in flagged]

# weight-inferred deaths (from audit_survival_vs_weight.csv) for scenario C / D
A = pd.read_csv('/tmp/work/tidy/audit_survival_vs_weight.csv')
A['block'] = A.pair.str.split(' <-> ').str[0]
wdeaths = {(r.block, r.group): int(r.deaths_w) for r in A.itertuples() if not np.isnan(r.n_w) and not np.isnan(r.n_s)}

def counts(exps, a, b, mode='recorded'):
    tabs = []
    for e in exps:
        d = S[S.block == e]
        if a not in set(d.group) or b not in set(d.group):
            continue
        row = []
        for g in (a, b):
            n = int((d.group == g).sum()); dead = int(d[d.group == g].event.sum())
            if mode == 'weights' and (e, g) in wdeaths:
                dead = wdeaths[(e, g)]
            if mode == 'worst_for_344':
                w = wdeaths.get((e, g), dead)
                dead = max(dead, w) if '344' in g else min(dead, w)
            row.append((n, dead))
        tabs.append((e, row))
    return tabs

def pooled(exps, a, b, mode='recorded'):
    tabs = counts(exps, a, b, mode)
    if not tabs:
        return None
    na = sum(r[0][0] for _, r in tabs); da = sum(r[0][1] for _, r in tabs)
    nb = sum(r[1][0] for _, r in tabs); db = sum(r[1][1] for _, r in tabs)
    # Mantel-Haenszel risk difference (survival) with Greenland-Robins weights
    num = den = 0.0
    for _, ((n1, d1), (n0, d0)) in tabs:
        N = n1 + n0
        num += ((n1 - d1) * n0 - (n0 - d0) * n1) / N
        den += n1 * n0 / N
    rd = num / den
    # CMH test (survivor vs dead x arm, stratified)
    st = [np.array([[n1 - d1, d1], [n0 - d0, d0]]) for _, ((n1, d1), (n0, d0)) in tabs]
    try:
        _t = StratifiedTable(st).test_null_odds(correction=True)
        cmh = _t.pvalue; cmh_chi2 = _t.statistic
        import mpmath
        cmh_exactp = float(mpmath.gammainc(0.5, cmh_chi2 / 2, mpmath.inf, regularized=True))
    except Exception:
        cmh, cmh_chi2, cmh_exactp = np.nan, np.nan, np.nan
    # stratified log-rank on recorded times (only meaningful for 'recorded' mode)
    slr = slr_chi2 = np.nan
    if mode == 'recorded':
        x = S[S.block.isin([e for e, _ in tabs]) & S.group.isin([a, b])]
        slr_chi2 = survdiff(x.days.values, x.event.values, (x.group == a).astype(int).values, strata=x.block.values)[0]
        import mpmath
        slr = float(mpmath.gammainc(0.5, slr_chi2 / 2, mpmath.inf, regularized=True))
    return dict(comparison=f'{a} vs {b}', scenario=mode, experiments=len(tabs), exp_list=', '.join(e for e, _ in tabs),
                surv_a=f'{na - da}/{na} ({100 * (na - da) / na:.0f}%)', surv_b=f'{nb - db}/{nb} ({100 * (nb - db) / nb:.0f}%)',
                MH_risk_difference_pct=100 * rd, CMH_chi2=cmh_chi2, p_CMH=cmh_exactp, stratified_logrank_chi2=slr_chi2, p_stratified_logrank=slr)

out = []
for a, b in [('PSLN-344', 'Sham'), ('PSLN-344', 'PSLN-212'), ('PSLN-212', 'Sham'), ('PSLN-212(Y)', 'PSLN-344')]:
    out.append(pooled(aged_exps, a, b, 'recorded') | {'set': 'All aged experiments (11)'})
    out.append(pooled(clean, a, b, 'recorded') | {'set': 'Excluding integrity-flagged experiments'})
    out.append(pooled(aged_exps, a, b, 'weights') | {'set': 'All aged; weight-inferred deaths where paired weights exist'})
    out.append(pooled(aged_exps, a, b, 'worst_for_344') | {'set': 'All aged; worst case for PSLN-344 (max deaths for 344, min for comparator)'})
O = pd.DataFrame(out)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 90)
print(O[['comparison', 'set', 'experiments', 'surv_a', 'surv_b', 'MH_risk_difference_pct', 'CMH_chi2', 'p_CMH', 'stratified_logrank_chi2', 'p_stratified_logrank']].to_string(index=False))
O.to_csv('/tmp/work/tidy/pooled_survival.csv', index=False)
print('\nclean set:', clean)
pd.DataFrame([dict(experiment=k, reason=v) for k, v in flagged.items()]).to_csv('/tmp/work/tidy/flagged_experiments.csv', index=False)

# background mortality in unchallenged aged controls
u = S[S.group == 'Untreated']
print('\nUnchallenged aged controls: deaths', int(u.event.sum()), 'of', len(u), '; per block', u.groupby('block').event.sum().to_dict())
