"""
Continuous endpoints: group summaries + key contrasts.
Scale rules (pre-specified before looking at p-values):
  - antibody titres (IgG, IgG1, IgG2a, HI, neutralising): log2 scale; HI values of 0 (< LOD 1:10) set to 5 (half LOD)
  - qPCR fold changes reported on linear scale: log10 scale
  - S09-A already log10
  - percentages / cell counts / ratios from flow: linear (stated methods), with Mann-Whitney as robustness check
Tests: one-way ANOVA + Tukey HSD (stated methods) across all groups in the block/timepoint;
       Welch t-test for each pre-specified pairwise contrast; exact Mann-Whitney U as robustness;
       Hedges g on the analysis scale.
"""
import pandas as pd, numpy as np, warnings
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
warnings.filterwarnings('ignore')
C = pd.read_csv('/tmp/work/tidy/continuous.csv')

def scale_of(meas, block):
    m = meas.lower()
    if 'titre' in m:
        return 'log2'
    if '(fold' in m or 'fold vs' in m or 'dose-response (fold' in m:
        return 'log10'
    if 'log10 fold' in m:
        return 'log10 (as stored)'
    return 'linear'

def transform(x, sc, meas):
    x = np.asarray(x, float)
    if sc == 'log2':
        x = np.where(x <= 0, 5.0, x) if 'HI' in meas else x
        return np.log2(x)
    if sc == 'log10':
        return np.log10(x)
    return x

def hedges_g(a, b):
    na, nb = len(a), len(b)
    sp = np.sqrt(((na - 1) * np.var(a, ddof=1) + (nb - 1) * np.var(b, ddof=1)) / (na + nb - 2))
    if sp == 0:
        return np.nan
    d = (np.mean(a) - np.mean(b)) / sp
    J = 1 - 3 / (4 * (na + nb) - 9)
    return d * J

rows, contrasts = [], []
C['time'] = C['time'].astype(str)
for (blk, meas, t), d in C.groupby(['block', 'measurand', 'time'], sort=False):
    sc = scale_of(meas, blk)
    groups = list(dict.fromkeys(d.sort_values('cell').group))  # order of appearance
    gvals = {g: d[d.group == g]['value'].values for g in dict.fromkeys(d.group)}
    tvals = {g: transform(v, sc, meas) for g, v in gvals.items()}
    for g, v in gvals.items():
        tv = tvals[g]
        r = dict(block=blk, measurand=meas, time=t, group=g, n=len(v), mean=np.mean(v), sd=np.std(v, ddof=1) if len(v) > 1 else np.nan,
                 sem=(np.std(v, ddof=1) / np.sqrt(len(v))) if len(v) > 1 else np.nan, median=np.median(v), min=np.min(v), max=np.max(v),
                 scale=sc)
        if sc == 'log2':
            r['geo_mean'] = 2 ** np.mean(tv)
            if len(v) > 1:
                half = stats.t.ppf(0.975, len(v) - 1) * np.std(tv, ddof=1) / np.sqrt(len(v))
                r['gm_95lo'], r['gm_95hi'] = 2 ** (np.mean(tv) - half), 2 ** (np.mean(tv) + half)
        elif sc == 'log10':
            r['geo_mean'] = 10 ** np.mean(tv)
            if len(v) > 1:
                half = stats.t.ppf(0.975, len(v) - 1) * np.std(tv, ddof=1) / np.sqrt(len(v))
                r['gm_95lo'], r['gm_95hi'] = 10 ** (np.mean(tv) - half), 10 ** (np.mean(tv) + half)
        elif len(v) > 1:
            half = stats.t.ppf(0.975, len(v) - 1) * np.std(v, ddof=1) / np.sqrt(len(v))
            r['mean_95lo'], r['mean_95hi'] = np.mean(v) - half, np.mean(v) + half
        rows.append(r)
    # omnibus ANOVA + Tukey across all groups (if >=3 groups and n>=2 each)
    tuk = {}
    if len(tvals) >= 3 and all(len(v) >= 2 for v in tvals.values()):
        F, pF = stats.f_oneway(*tvals.values())
        allv = np.concatenate(list(tvals.values())); lab = np.concatenate([[g] * len(v) for g, v in tvals.items()])
        try:
            th = pairwise_tukeyhsd(allv, lab)
            tt = pd.DataFrame(th.summary().data[1:], columns=th.summary().data[0])
            for _, rr in tt.iterrows():
                tuk[(rr['group1'], rr['group2'])] = rr['p-adj']; tuk[(rr['group2'], rr['group1'])] = rr['p-adj']
        except Exception as e:
            pass
    else:
        F, pF = np.nan, np.nan
    # pre-specified contrasts
    def young_of(g):
        return {'PSLN-212': 'PSLN-212(Y)', 'PSLN-344': 'PSLN-344(Y)'}.get(g)
    pairs = [('PSLN-344', 'Sham'), ('PSLN-344', 'PSLN-212'), ('PSLN-344', 'PSLN-212(Y)'), ('PSLN-212', 'Sham'),
             ('PSLN-212', 'CMP-204'), ('PSLN-344', 'CMP-204'), ('CMP-204', 'Sham'), ('PSLN-344', 'Vaccine'), ('PSLN-212', 'Vaccine'),
             ('PSLN-344(Y)', 'PSLN-212(Y)'), ('PSLN-344', 'PSLN-344(Y)'), ('PSLN-344', 'PBS'), ('PSLN-212', 'PBS'),
             ('CT', 'PBS'), ('PSLN-344', 'Sham'), ('Sham', 'PBS'), ('PSLN-212/R848', 'PSLN-212'), ('PSLN-344', 'PSLN-212/R848'),
             ('PSLN-344', 'PSLN-344/R848')]
    seen = set()
    for a, b in pairs:
        if (a, b) in seen or a not in tvals or b not in tvals:
            continue
        seen.add((a, b))
        ta, tb = tvals[a], tvals[b]
        if len(ta) < 2 or len(tb) < 2:
            continue
        w = stats.ttest_ind(ta, tb, equal_var=False)
        s = stats.ttest_ind(ta, tb, equal_var=True)
        try:
            mw = stats.mannwhitneyu(gvals[a], gvals[b], alternative='two-sided', method='exact')
            pmw = mw.pvalue
        except Exception:
            pmw = np.nan
        diff = np.mean(ta) - np.mean(tb)
        if sc == 'log2':
            eff, efflab = 2 ** diff, 'GM ratio'
        elif sc.startswith('log10'):
            eff, efflab = 10 ** diff, 'GM fold ratio'
        else:
            eff, efflab = diff, 'mean difference'
        contrasts.append(dict(block=blk, measurand=meas, time=t, contrast=f'{a} vs {b}', scale=sc, n_a=len(ta), n_b=len(tb),
                              mean_a=np.mean(gvals[a]), mean_b=np.mean(gvals[b]), effect=eff, effect_type=efflab,
                              hedges_g=hedges_g(ta, tb), p_welch=w.pvalue, p_student=s.pvalue, p_mannwhitney_exact=pmw,
                              p_tukey=tuk.get((a, b), np.nan), anova_F=F, anova_p=pF))
    # fraction of young response restored (aged PSLN-344 vs Sham/vehicle baseline and young reference)
S_ = pd.DataFrame(rows); K = pd.DataFrame(contrasts)
S_.to_csv('/tmp/work/tidy/summary_continuous.csv', index=False)
K.to_csv('/tmp/work/tidy/contrasts_continuous.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 1000); pd.set_option('display.max_colwidth', 50)
print(S_[['block', 'measurand', 'time', 'group', 'n', 'mean', 'sd', 'geo_mean']].round(3).to_string(index=False))
