"""Group summaries and stated-method statistics for every non-survival, non-body-weight block.

Stated methods (annotation p.2): one-way ANOVA + Tukey; two-way ANOVA + Tukey; Student's t; log-rank.
 * single-timepoint blocks, >2 groups : one-way ANOVA + Tukey HSD (on log2 for titres and fold-change qPCR as a sensitivity analysis)
 * two-group blocks                   : Student's t (Welch reported alongside)
 * time/dose series                   : two-way ANOVA (group x time) + Tukey within each time point
Titres of 0 (below the 1:10 starting dilution) are set to 5 (LLOD/2) before log transformation.
"""
import numpy as np, pandas as pd, itertools, warnings
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import tidy

def tukey(vals):
    """vals: dict group -> array.  Returns DataFrame(group1, group2, meandiff(g2-g1), lower, upper, p-adj) with exact p (scipy)."""
    gs = list(vals)
    if min(len(v) for v in vals.values()) < 2:
        return pd.DataFrame(columns=['group1', 'group2', 'meandiff', 'lower', 'upper', 'p-adj'])
    r = stats.tukey_hsd(*[np.asarray(vals[g], float) for g in gs]); ci = r.confidence_interval(0.95)
    out = []
    for i in range(len(gs)):
        for j in range(i + 1, len(gs)):
            # scipy statistic[i, j] = mean_i - mean_j ; report g2 - g1 with g1 = gs[i], g2 = gs[j]
            out.append(dict(group1=gs[i], group2=gs[j], meandiff=-r.statistic[i, j], lower=-ci.high[i, j], upper=-ci.low[i, j], **{'p-adj': r.pvalue[i, j]}))
    return pd.DataFrame(out)
warnings.filterwarnings('ignore')
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 800); pd.set_option('display.max_colwidth', 70)

T = tidy.T()
idx = pd.read_csv('../data_tidy/psln_block_index.csv').set_index('block')
TITRE = ['S03-A', 'S03-C', 'S03-D', 'S03-E', 'S03-G', 'S03-H', 'S13-A', 'S13-B', 'S13-C', 'S13-D', 'S13-I', 'S13-J']
LOGSCALE_ALREADY = [b for b in idx.index if b.startswith('S09-A')]
single = [b for b in idx.index if idx.loc[b, 'kind'] in ('cols', 'rows')] + [b for b in idx.index if idx.loc[b, 'kind'] == 'tc' and T[T.block == b]['x'].isna().all()]
series = [b for b in idx.index if idx.loc[b, 'kind'] == 'tc' and not T[T.block == b]['x'].isna().all()]

def summarise(v, titre=False):
    v = np.asarray(v, float); n = len(v)
    out = dict(n=n, mean=v.mean(), sd=v.std(ddof=1) if n > 1 else np.nan, median=np.median(v), min=v.min(), max=v.max())
    if titre:
        w = np.where(v <= 0, 5.0, v); lg = np.log(w)
        gm = np.exp(lg.mean()); se = lg.std(ddof=1) / np.sqrt(n); t = stats.t.ppf(0.975, n - 1)
        out.update(gmt=gm, gmt_lo=np.exp(lg.mean() - t * se), gmt_hi=np.exp(lg.mean() + t * se), n_below_lod=int((v <= 0).sum()))
    return out

S_rows = []; P_rows = []; A_rows = []
for b in single:
    d = T[T.block == b]
    titre = b in TITRE
    gs = list(pd.unique(d.group))
    for g in gs:
        S_rows.append(dict(block=b, x=np.nan, group=g, measurand=idx.loc[b, 'measurand'], time=idx.loc[b, 'time'], **summarise(d[d.group == g].value, titre)))
    vals = {g: d[d.group == g].value.values.astype(float) for g in gs}
    if titre:
        lvals = {g: np.log2(np.where(v <= 0, 5.0, v)) for g, v in vals.items()}
    elif b in LOGSCALE_ALREADY:
        lvals = None
    else:
        lvals = {g: np.log2(v) for g, v in vals.items()} if all((v > 0).all() for v in vals.values()) else None
    if len(gs) == 2:
        a, c = vals[gs[0]], vals[gs[1]]
        t_s = stats.ttest_ind(a, c); t_w = stats.ttest_ind(a, c, equal_var=False); mw = stats.mannwhitneyu(a, c, alternative='two-sided')
        sp = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(c) - 1) * c.var(ddof=1)) / (len(a) + len(c) - 2))
        dd = a.mean() - c.mean(); se = sp * np.sqrt(1 / len(a) + 1 / len(c)); tq = stats.t.ppf(0.975, len(a) + len(c) - 2)
        P_rows.append(dict(block=b, x=np.nan, g1=gs[0], g2=gs[1], mean1=a.mean(), mean2=c.mean(), diff=dd, diff_lo=dd - tq * se, diff_hi=dd + tq * se,
                           ratio=a.mean() / c.mean(), test='Student t', p=t_s.pvalue, p_welch=t_w.pvalue, p_mwu=mw.pvalue))
        A_rows.append(dict(block=b, test='Student t', stat=t_s.statistic, p=t_s.pvalue))
    elif len(gs) > 2:
        F = stats.f_oneway(*[vals[g] for g in gs])
        A_rows.append(dict(block=b, test='one-way ANOVA (linear)', stat=F.statistic, p=F.pvalue))
        res = tukey(vals)
        lres = None
        if lvals is not None:
            Fl = stats.f_oneway(*[lvals[g] for g in gs])
            A_rows.append(dict(block=b, test='one-way ANOVA (log2)', stat=Fl.statistic, p=Fl.pvalue))
            lres = tukey(lvals).set_index(['group1', 'group2'])
        for _, r in res.iterrows():
            g1, g2 = r['group1'], r['group2']
            row = dict(block=b, x=np.nan, g1=g2, g2=g1, mean1=vals[g2].mean(), mean2=vals[g1].mean(), diff=r['meandiff'], diff_lo=r['lower'], diff_hi=r['upper'],
                       ratio=vals[g2].mean() / vals[g1].mean() if vals[g1].mean() != 0 else np.nan, test='Tukey HSD', p=r['p-adj'])
            if lres is not None:
                lr = lres.loc[(g1, g2)]
                row.update(p_log=lr['p-adj'], gm_ratio=2 ** lr['meandiff'], gm_ratio_lo=2 ** lr['lower'], gm_ratio_hi=2 ** lr['upper'])
            P_rows.append(row)

for b in series:
    d = T[T.block == b].copy()
    gs = list(pd.unique(d.group)); xs = sorted(pd.unique(d.x))
    for x in xs:
        for g in gs:
            S_rows.append(dict(block=b, x=x, group=g, measurand=idx.loc[b, 'measurand'], time='', **summarise(d[(d.group == g) & (d.x == x)].value)))
    d['G'] = d.group.astype('category'); d['X'] = d.x.astype(str)
    m = smf.ols('value ~ C(G) * C(X)', data=d).fit()
    an = sm.stats.anova_lm(m, typ=2)
    for term in an.index[:3]:
        A_rows.append(dict(block=b, test=f'two-way ANOVA: {term}', stat=an.loc[term, 'F'], p=an.loc[term, 'PR(>F)']))
    for x in xs:
        s = d[d.x == x]
        if s.group.nunique() > 2 and s.groupby('group').size().min() >= 2:
            res = tukey({g: s[s.group == g].value.values for g in gs if (s.group == g).any()})
            for _, r in res.iterrows():
                g1, g2 = r['group1'], r['group2']
                m1 = s[s.group == g2].value.mean(); m2 = s[s.group == g1].value.mean()
                P_rows.append(dict(block=b, x=x, g1=g2, g2=g1, mean1=m1, mean2=m2, diff=r['meandiff'], diff_lo=r['lower'], diff_hi=r['upper'], ratio=m1 / m2 if m2 else np.nan,
                                   test='Tukey HSD within time', p=r['p-adj']))
        elif s.group.nunique() == 2:
            g1, g2 = gs
            a = s[s.group == g1].value.values; c = s[s.group == g2].value.values
            t_s = stats.ttest_ind(a, c)
            P_rows.append(dict(block=b, x=x, g1=g1, g2=g2, mean1=a.mean(), mean2=c.mean(), diff=a.mean() - c.mean(), ratio=a.mean() / c.mean(), test='Student t within time', p=t_s.pvalue))

SUM = pd.DataFrame(S_rows); PW = pd.DataFrame(P_rows); AN = pd.DataFrame(A_rows)
SUM.to_csv('../tables/T4_group_summaries.csv', index=False)
PW.to_csv('../tables/T5_pairwise_tests.csv', index=False)
AN.to_csv('../tables/T6_omnibus_tests.csv', index=False)
print(SUM.shape, PW.shape, AN.shape)
