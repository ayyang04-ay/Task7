#!/usr/bin/env python
"""
05_endpoints.py -- descriptive statistics and group contrasts for every non-survival, non-weight block.
Run: micromamba run -n core python 05_endpoints.py

Scale handling
  * titres (ELISA endpoint, HAI, neutralisation)            -> analysed on log10 scale; summary = geometric mean (GMT)
      HAI values printed as 0 are below the lowest dilution tested (1:10, annotation S03-C/G) -> set to 5 (LOD/2)
  * qPCR relative expression (linear, "relative to untreated") -> analysed on log10 scale; summary = geometric mean fold
  * S09-A is already log10 (block label)                       -> analysed as is; back-transformed for display
  * percentages, counts, ratios                                -> analysed on the raw (linear) scale; summary = arithmetic mean
Tests
  * stated method: one-way ANOVA + Tukey HSD across the groups printed in the block (per factor level)
  * sensitivity: Welch t-test and exact two-sided Mann-Whitney for each contrast
Outputs: tables/T05_endpoint_descriptives.csv, tables/T06_endpoint_contrasts.csv, tables/T07_restoration_index.csv
"""
import os, itertools, warnings
import numpy as np, pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
sc = pd.read_csv(os.path.join(HERE, 'parsed', 'scalar_long.csv'), keep_default_na=False)
sc['factor'] = sc.factor.astype(str)
rng = np.random.default_rng(20261101)

TITRE = {'S03-A', 'S03-C', 'S03-D', 'S03-E', 'S03-G', 'S03-H', 'S13-A', 'S13-B', 'S13-C', 'S13-D', 'S13-I', 'S13-J'}
QPCR = {'S01-A', 'S02-F', 'S03-L', 'S08-A', 'S10-A'}
LOG10_ALREADY = {'S09-A(cols A-V)', 'S09-A(cols X-AS)'}
HAI = {'S03-C', 'S03-G'}

def scale_of(b):
    if b in TITRE: return 'log10(titre)'
    if b in QPCR: return 'log10(fold)'
    if b in LOG10_ALREADY: return 'log10(fold), as stored'
    return 'linear'

def transform(b, x):
    x = np.asarray(x, float)
    if b in HAI: x = np.where(x <= 0, 5.0, x)
    if b in TITRE or b in QPCR: return np.log10(x)
    return x

def center(b, y):
    """display-scale central value: geometric mean for log-analysed blocks, arithmetic mean otherwise"""
    if b in TITRE or b in QPCR or b in LOG10_ALREADY: return 10 ** np.mean(y)
    return np.mean(y)

desc, cons = [], []
for (b, f), d in sc.groupby(['block', 'factor'], sort=False):
    groups = list(d.group.unique())
    Y = {g: transform(b, d[d.group == g].sort_values('rep').value.values) for g in groups}
    raw = {g: d[d.group == g].sort_values('rep').value.values for g in groups}
    for g in groups:
        y, r = Y[g], raw[g]
        desc.append(dict(block=b, level=f, group=g, n=len(r), mean=np.mean(r), sd=np.std(r, ddof=1) if len(r) > 1 else np.nan,
                         sem=stats.sem(r) if len(r) > 1 else np.nan, median=np.median(r), min=np.min(r), max=np.max(r),
                         analysis_scale=scale_of(b), centre_on_analysis_scale=center(b, y),
                         values=' '.join(f'{v:g}' for v in r), cells=f"{d[d.group == g].cell.iloc[0]}..{d[d.group == g].cell.iloc[-1].split('!')[1]}"))
    if len(groups) < 2: continue
    # ANOVA + Tukey on analysis scale
    allv = np.concatenate([Y[g] for g in groups]); lab = np.concatenate([[g] * len(Y[g]) for g in groups])
    tuk = {}
    p_anova = np.nan
    try:
        if len(groups) >= 3:
            p_anova = stats.f_oneway(*[Y[g] for g in groups]).pvalue
            res = pairwise_tukeyhsd(allv, lab)
            for row in res.summary().data[1:]:
                tuk[frozenset((row[0], row[1]))] = float(row[3])
    except Exception as e:
        pass
    for g1, g0 in itertools.combinations(groups, 2):
        y1, y0 = Y[g1], Y[g0]
        try: pw = stats.ttest_ind(y1, y0, equal_var=False).pvalue
        except Exception: pw = np.nan
        try: ps = stats.ttest_ind(y1, y0, equal_var=True).pvalue
        except Exception: ps = np.nan
        try: pm = stats.mannwhitneyu(y1, y0, alternative='two-sided', method='exact').pvalue
        except Exception: pm = np.nan
        c1, c0 = center(b, y1), center(b, y0)
        cons.append(dict(block=b, level=f, group_a=g1, group_b=g0, n_a=len(y1), n_b=len(y0), centre_a=c1, centre_b=c0,
                         ratio_a_over_b=(c1 / c0 if c0 not in (0, np.nan) else np.nan), diff_a_minus_b=c1 - c0,
                         analysis_scale=scale_of(b), p_anova=p_anova, p_tukey=tuk.get(frozenset((g1, g0)), np.nan),
                         p_student_t=ps, p_welch_t=pw, p_mannwhitney_exact=pm))
T5 = pd.DataFrame(desc); T6 = pd.DataFrame(cons)
T5.to_csv(os.path.join(HERE, 'tables', 'T05_endpoint_descriptives.csv'), index=False)
T6.to_csv(os.path.join(HERE, 'tables', 'T06_endpoint_contrasts.csv'), index=False)

# ---------------- restoration index ----------------
# For blocks that contain aged+PSLN-212, aged+PSLN-344 and young+PSLN-212:
#   pct_of_young    = centre(aged 344) / centre(young 212)                        (GMT ratio for log-scale blocks)
#   deficit_closed  = (aged344 - aged212) / (young212 - aged212) on the analysis scale (log10 for titres/qPCR)
# bootstrap (10,000 resamples within group) percentile 95% CI
def norm(g):
    return g.replace('PSLN-212Y', 'PSLN-212(Y)').replace('PSLN-212(y)', 'PSLN-212(Y)')
rows = []
for (b, f), d in sc.groupby(['block', 'factor'], sort=False):
    d = d.assign(g=d.group.map(norm))
    if not {'PSLN-212', 'PSLN-344', 'PSLN-212(Y)'} <= set(d.g): continue
    a212 = transform(b, d[d.g == 'PSLN-212'].value.values); a344 = transform(b, d[d.g == 'PSLN-344'].value.values)
    y212 = transform(b, d[d.g == 'PSLN-212(Y)'].value.values)
    islog = scale_of(b) != 'linear'
    def stat(a2, a3, y2):
        m2, m3, my = np.mean(a2), np.mean(a3), np.mean(y2)
        pct = (10 ** (m3 - my) if islog else m3 / my) * 100
        closed = (m3 - m2) / (my - m2) * 100 if my != m2 else np.nan
        fold = 10 ** (m3 - m2) if islog else m3 / m2
        return pct, closed, fold
    pct, closed, fold = stat(a212, a344, y212)
    bs = np.array([stat(rng.choice(a212, len(a212)), rng.choice(a344, len(a344)), rng.choice(y212, len(y212))) for _ in range(10000)])
    lo, hi = np.nanpercentile(bs, [2.5, 97.5], axis=0)
    rows.append(dict(block=b, level=f, analysis_scale=scale_of(b),
                     aged_PSLN212=center(b, a212), aged_PSLN344=center(b, a344), young_PSLN212=center(b, y212),
                     fold_344_over_212_aged=fold, fold_ci95=f'{lo[2]:.2f}-{hi[2]:.2f}',
                     aged344_as_pct_of_young=pct, pct_ci95=f'{lo[0]:.0f}-{hi[0]:.0f}',
                     age_deficit_closed_pct=closed, closed_ci95=f'{lo[1]:.0f}-{hi[1]:.0f}',
                     n=f'{len(a212)}/{len(a344)}/{len(y212)}'))
T7 = pd.DataFrame(rows)
T7.to_csv(os.path.join(HERE, 'tables', 'T07_restoration_index.csv'), index=False)
pd.set_option('display.width', 280); pd.set_option('display.max_rows', 800); pd.set_option('display.max_colwidth', 60)
pd.options.display.float_format = '{:.4g}'.format
print(T7.to_string())
