"""
Descriptive statistics and contrasts for every one-value-per-animal block and every time-course block.
 - linear-scale endpoints: mean, SD; one-way ANOVA + Tukey HSD (the method stated in the annotation); Welch 95% CI; exact Mann-Whitney
 - titre / fold-change endpoints: analysed on log10 scale; geometric mean and geometric-mean ratio (GMR) with 95% CI
   (HAI values printed as 0 are below the 1:10 starting dilution and are set to 5 for the log analysis)
Outputs: T9_group_summaries.csv, T10_pairwise_contrasts.csv
"""
from paths import TABLES, FIGS, OUT as OUTDIR, BUILD, PANDOC
import pandas as pd, numpy as np, math, itertools, warnings
from scipy import stats
import psln_blocks as pb
from stats_util import *
warnings.filterwarnings('ignore')
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 4000); pd.set_option('display.max_colwidth', 80)
df = pb.tidy()
pt = df[df.kind.isin(['point', 'series'])].copy()
pt['xk'] = pt.x.map(lambda v: '' if v is None or (isinstance(v, float) and v != v) else str(v))

LOGSCALE = lambda an: any(k in an for k in ['(titre)', '(fold', 'fold)', '(ratio)', 'Tfh:Tfr ratio'])
ALREADY_LOG = lambda an: 'log10' in an

summ = []; cont = []
for (blk, an, xk), t in pt.groupby(['block', 'analyte', 'xk'], sort=False):
    groups = {g: tg.sort_values('rep').value.to_numpy(float) for g, tg in t.groupby('group', sort=False)}
    cells = {g: f"{tg.cell.iloc[0]}:{tg.cell.iloc[-1].split('!')[1]}" for g, tg in t.groupby('group', sort=False)}
    logsc = LOGSCALE(an) and not ALREADY_LOG(an)
    for g, v in groups.items():
        rec = dict(block=blk, analyte=an, x=xk, group=g, n=len(v), mean=v.mean(), sd=v.std(ddof=1) if len(v) > 1 else np.nan,
                   median=np.median(v), min=v.min(), max=v.max(), cells=cells[g])
        if logsc or ALREADY_LOG(an):
            lv = np.log10(np.where(v <= 0, 5.0, v)) if logsc else v
            rec['geo_mean'] = 10 ** lv.mean()
            if len(v) > 1:
                se = lv.std(ddof=1) / math.sqrt(len(v)); tc = stats.t.ppf(0.975, len(v) - 1)
                rec['geo_lo'] = 10 ** (lv.mean() - tc * se); rec['geo_hi'] = 10 ** (lv.mean() + tc * se)
        summ.append(rec)
    if len(groups) < 2 or min(len(v) for v in groups.values()) < 2:
        continue
    tr = (lambda v: np.log10(np.where(v <= 0, 5.0, v))) if logsc else (lambda v: v)
    G = {g: tr(v) for g, v in groups.items()}
    try:
        F, pA, tk = tukey(G) if len(G) >= 3 else (np.nan, np.nan, {})
    except Exception:
        F, pA, tk = np.nan, np.nan, {}
    for a, b in itertools.combinations(G, 2):
        w = welch(G[a], G[b])
        rec = dict(block=blk, analyte=an, x=xk, a=a, b=b, n_a=len(G[a]), n_b=len(G[b]), scale='log10' if (logsc or ALREADY_LOG(an)) else 'linear',
                   mean_a=groups[a].mean(), mean_b=groups[b].mean(), diff=w['diff'], diff_lo=w['lo'], diff_hi=w['hi'], p_welch=w['p'],
                   p_mwu_exact=mwu_exact(groups[a], groups[b]), hedges_g=hedges_g(G[a], G[b]), anova_F=F, anova_p=pA,
                   p_tukey=tk.get((a, b), (None, None, None, np.nan))[3] if tk else np.nan)
        if logsc or ALREADY_LOG(an):
            rec.update(GMR=10 ** w['diff'], GMR_lo=10 ** w['lo'], GMR_hi=10 ** w['hi'])
        else:
            rec.update(ratio_of_means=groups[a].mean() / groups[b].mean() if groups[b].mean() != 0 else np.nan)
        cont.append(rec)
S = pd.DataFrame(summ); Cn = pd.DataFrame(cont)
S.to_csv(TABLES + 'T9_group_summaries.csv', index=False)
Cn.to_csv(TABLES + 'T10_pairwise_contrasts.csv', index=False)
print(len(S), 'group summaries;', len(Cn), 'pairwise contrasts')
