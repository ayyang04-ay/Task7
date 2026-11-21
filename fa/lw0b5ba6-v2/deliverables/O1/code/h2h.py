"""Head-to-head statistics for every continuous endpoint.
Primary contrast: aged PSLN-344 vs aged PSLN-212.  Benchmarks: young PSLN-212(Y) and aged Sham.
Scale: titres / qPCR fold / cell counts -> log2 (geometric means, GMR); S09-A already log10;
percentages -> raw scale (difference + ratio of means).  Tests: Welch t (primary), exact Mann-Whitney (sensitivity).
Multiplicity: Benjamini-Hochberg across all primary contrasts.
Restoration index (RI) = (344 - 212) / (Y - 212) on the analysis scale: fraction of the young-vs-aged gap closed.
"""
import pandas as pd, numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests

V = pd.read_csv('/tmp/work/tidy/values.csv')
V['group'] = V.group.str.replace('PSLN-212Y', 'PSLN-212(Y)').str.replace('PSLN-344Y', 'PSLN-344(Y)')
V['time'] = V['time'].fillna('')

LOG = ('IgG', 'HAI', 'Neut', 'Ifnb1', 'Gm-csf', 'Aicda', 'E47', 'CNS', 'x1e5', 'post-boost')
def scale_of(block, analyte):
    if block.startswith('S09-A'): return 'log10 (as stored)'
    if block in ('S03-B', 'S03-F'): return 'excluded'
    if any(k in analyte for k in LOG): return 'log2'
    return 'linear %'

# Endpoints to exclude from the decision table (with reason) -- see integrity audit
EXCLUDE = {
    'S03-B': 'group labels rotated vs primary S13-A/B titres; ratio recomputed from S13',
    'S03-F': 'group labels rotated vs primary S13-C/D titres; ratio recomputed from S13',
    'S04-B Tfh:Tfr': 'derived: equals (100-Foxp3%)/Foxp3% of S04-B Foxp3 -> not independent',
    'S11-A': 'first two animals of every group/day identical to S11-B (AM vs neutrophils) -> compromised',
    'S11-B': 'see S11-A',
    'S07-C': 'both columns labelled Ly6C-CD206+; cannot assign groups',
    'S05-A': 'n=2/group; conditions contradictory (OVA vs bivalent); NP366-374 is H-2Db-restricted but BALB/c are H-2d',
    'S05-B': 'as S05-A',
}

def hedges_g(a, b):
    na, nb = len(a), len(b)
    sp = np.sqrt(((na - 1) * np.var(a, ddof=1) + (nb - 1) * np.var(b, ddof=1)) / (na + nb - 2))
    d = (np.mean(a) - np.mean(b)) / sp if sp > 0 else np.nan
    return d * (1 - 3 / (4 * (na + nb) - 9))

def transform(x, sc, analyte):
    x = np.asarray(x, float)
    if sc == 'log2':
        if 'HAI' in analyte: x = np.where(x <= 0, 5.0, x)  # below LOD (1:10) -> 5
        return np.log2(x)
    return x

rows = []
for (blk, an, t), d in V.groupby(['block', 'analyte', 'time']):
    groups = set(d.group)
    if not {'PSLN-212', 'PSLN-344'} <= groups: continue
    sc = scale_of(blk, an)
    a = d[d.group == 'PSLN-344'].value.values; b = d[d.group == 'PSLN-212'].value.values
    ta, tb = transform(a, sc, an), transform(b, sc, an)
    r = dict(block=blk, analyte=an, time=t, scale=sc, n344=len(a), n212=len(b))
    if sc == 'log2':
        r['summary344'] = 2 ** ta.mean(); r['summary212'] = 2 ** tb.mean(); r['stat'] = 'geo-mean'
    elif sc.startswith('log10'):
        r['summary344'] = 10 ** ta.mean(); r['summary212'] = 10 ** tb.mean(); r['stat'] = 'geo-mean fold'
    else:
        r['summary344'] = ta.mean(); r['summary212'] = tb.mean(); r['stat'] = 'mean %'
    r['sd344'] = ta.std(ddof=1); r['sd212'] = tb.std(ddof=1)
    tt = stats.ttest_ind(ta, tb, equal_var=False)
    # CI for difference on analysis scale (Welch)
    se = np.sqrt(ta.var(ddof=1) / len(ta) + tb.var(ddof=1) / len(tb))
    dfw = se ** 4 / ((ta.var(ddof=1) / len(ta)) ** 2 / (len(ta) - 1) + (tb.var(ddof=1) / len(tb)) ** 2 / (len(tb) - 1)) if se > 0 else np.nan
    diff = ta.mean() - tb.mean(); q = stats.t.ppf(0.975, dfw) if se > 0 else np.nan
    lo, hi = diff - q * se, diff + q * se
    if sc == 'log2':
        r['effect'] = 'GMR 344/212'; r['est'] = 2 ** diff; r['lo'] = 2 ** lo; r['hi'] = 2 ** hi
    elif sc.startswith('log10'):
        r['effect'] = 'fold ratio 344/212'; r['est'] = 10 ** diff; r['lo'] = 10 ** lo; r['hi'] = 10 ** hi
    else:
        r['effect'] = 'mean diff (pp) 344-212'; r['est'] = diff; r['lo'] = lo; r['hi'] = hi
        r['ratio'] = ta.mean() / tb.mean() if tb.mean() != 0 else np.nan
    r['p_welch'] = tt.pvalue
    r['p_mwu'] = stats.mannwhitneyu(ta, tb, alternative='two-sided', method='exact').pvalue
    r['hedges_g'] = hedges_g(ta, tb)
    # benchmarks
    for bg, key in [('PSLN-212(Y)', 'Y'), ('Sham', 'Sham'), ('PBS', 'Sham'), ('Vaccine', 'Sham'), ('PSLN-344(Y)', 'Y344')]:
        if bg in groups and f'summary{key}' not in r:
            x = transform(d[d.group == bg].value.values, sc, an)
            r[f'summary{key}'] = (2 ** x.mean() if sc == 'log2' else 10 ** x.mean() if sc.startswith('log10') else x.mean())
            r[f'_mean_t_{key}'] = x.mean()
    if '_mean_t_Y' in r:
        gap = r['_mean_t_Y'] - tb.mean()
        r['restoration_index'] = (ta.mean() - tb.mean()) / gap if abs(gap) > 1e-9 else np.nan
        ty = transform(d[d.group == 'PSLN-212(Y)'].value.values, sc, an)
        r['p_344_vs_Y'] = stats.ttest_ind(ta, ty, equal_var=False).pvalue
    r['excluded'] = EXCLUDE.get(blk, '')
    if blk == 'S08-B': r['excluded'] = 'formulation attribute, not an immune endpoint (reported separately)'
    if blk.startswith('S09-A') and an.startswith('Ifnb1'): r['excluded'] = 'not independent: same animals as S01-A Ifnb1 (see M3)'
    if t == 'd0' and not r['excluded']: r['excluded'] = 'baseline (day 0, pre-immunisation) balance check'
    rows.append(r)

H = pd.DataFrame(rows)
H = H.drop(columns=[c for c in H.columns if c.startswith('_')])
inc = H.excluded == ''
H.loc[inc, 'q_BH'] = multipletests(H.loc[inc, 'p_welch'], method='fdr_bh')[1]
H = H.sort_values(['excluded', 'block', 'analyte', 'time'], na_position='first')
H.to_csv('/tmp/work/h2h.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40); pd.set_option('display.max_rows', 200)
cols = ['block', 'analyte', 'time', 'scale', 'n344', 'n212', 'summary344', 'summary212', 'summaryY', 'summarySham',
        'effect', 'est', 'lo', 'hi', 'p_welch', 'p_mwu', 'q_BH', 'hedges_g', 'restoration_index', 'p_344_vs_Y']
print(H[inc][cols].round(4).to_string(index=False))
print('\nExcluded:'); print(H[~inc][['block', 'analyte', 'time', 'excluded']].to_string(index=False))
print('\nIncluded endpoints:', inc.sum(), ' favour 344 (q<0.05):', ((H.q_BH < 0.05) & (H.est > (1 if 1 else 0))).sum())
