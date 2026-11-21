"""Per-block descriptive statistics and the stated tests (one-way ANOVA + Tukey), plus robustness tests.
Scale handling:
  - titers and qPCR fold-changes are analyzed on log10 scale (geometric means); percentages on the linear scale.
  - HAI '0' (= below the lowest dilution tested, 1:10) is set to 5 for geometric means (sensitivity: 1 and 10).
  - S09-A is already log10.
"""
import pandas as pd, numpy as np, itertools, warnings
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
warnings.filterwarnings('ignore')
pd.set_option('display.width', 300); pd.set_option('display.max_rows', 3000); pd.set_option('display.max_colwidth', 70)
Q = pd.read_csv('quant_long.csv')
Q['time'] = Q['time'].astype(str)

LOG_BLOCKS = {'S01-A','S02-F','S03-A','S03-C','S03-D','S03-E','S03-G','S03-H','S03-L','S08-A','S10-A','S13-A','S13-B','S13-C','S13-D','S13-I','S13-J','S03-B','S03-F','S04-B Tfh:Tfr','S07-A'}
ALREADY_LOG = {'S09-A'}
HAI = {'S03-C','S03-G'}

def cellrange(d):
    c = d.sort_values('rep').cell.tolist()
    return c[0] if len(c)==1 else f"{c[0]}:{c[-1].split('!')[1]}"

desc_rows=[]; pair_rows=[]; anova_rows=[]
for (blk, an, t), d in Q.groupby(['block','analyte','time'], sort=False):
    logscale = blk in LOG_BLOCKS
    d = d.copy()
    if blk in HAI: d['v_an'] = np.log10(d.value.replace(0, 5.0))
    elif logscale: d['v_an'] = np.log10(d.value)
    else: d['v_an'] = d.value
    groups = list(d.group.unique())
    for g in groups:
        x = d[d.group==g]
        v = x.value.values; va = x.v_an.values
        row = dict(block=blk, analyte=an, time=t, group=g, n=len(v), mean=v.mean(), sd=v.std(ddof=1) if len(v)>1 else np.nan, median=np.median(v), min=v.min(), max=v.max(), cells=cellrange(x))
        if blk in ALREADY_LOG:
            row['geomean'] = 10**v.mean()   # back-transformed fold change
        elif logscale:
            row['geomean'] = 10**va.mean()
        else: row['geomean'] = np.nan
        desc_rows.append(row)
    if len(groups) >= 2 and all((d.group==g).sum() >= 2 for g in groups):
        arrs = [d[d.group==g].v_an.values for g in groups]
        if len(groups) > 2:
            F, p = stats.f_oneway(*arrs)
            anova_rows.append(dict(block=blk, analyte=an, time=t, scale='log10' if (logscale or blk in ALREADY_LOG) else 'linear', k=len(groups), F=F, p_anova=p, p_kruskal=stats.kruskal(*arrs).pvalue))
            tk = pairwise_tukeyhsd(d.v_an.values, d.group.values)
            tkd = {(a,b):(pv, md, lo, hi) for a,b,md,pv,lo,hi,_ in tk.summary().data[1:]}
        else:
            tkd = {}
        for a, b in itertools.combinations(groups, 2):
            xa = d[d.group==a].v_an.values; xb = d[d.group==b].v_an.values
            tt = stats.ttest_ind(xb, xa, equal_var=False)
            st = stats.ttest_ind(xb, xa, equal_var=True)
            try: mw = stats.mannwhitneyu(xb, xa, alternative='two-sided', method='exact').pvalue
            except Exception: mw = np.nan
            diff = xb.mean() - xa.mean()
            # Welch CI
            se = np.sqrt(xa.var(ddof=1)/len(xa) + xb.var(ddof=1)/len(xb))
            dfw = se**4 / ((xa.var(ddof=1)/len(xa))**2/(len(xa)-1) + (xb.var(ddof=1)/len(xb))**2/(len(xb)-1)) if se>0 else np.nan
            tcrit = stats.t.ppf(0.975, dfw) if se>0 else np.nan
            lo, hi = diff - tcrit*se, diff + tcrit*se
            ptk = np.nan
            if (a,b) in tkd: ptk = tkd[(a,b)][0]
            elif (b,a) in tkd: ptk = tkd[(b,a)][0]
            islog = logscale or blk in ALREADY_LOG
            pair_rows.append(dict(block=blk, analyte=an, time=t, A=a, B=b, nA=len(xa), nB=len(xb), scale='log10' if islog else 'linear',
                                  effect=(10**diff if islog else diff), ci_lo=(10**lo if islog else lo), ci_hi=(10**hi if islog else hi),
                                  effect_type=('ratio B/A (geometric)' if islog else 'difference B-A'),
                                  p_tukey=ptk, p_welch=tt.pvalue, p_student=st.pvalue, p_mwu_exact=mw))
D = pd.DataFrame(desc_rows); P = pd.DataFrame(pair_rows); A = pd.DataFrame(anova_rows)
D.to_csv('desc_stats.csv', index=False); P.to_csv('pairwise_stats.csv', index=False); A.to_csv('anova_stats.csv', index=False)
print(D.shape, P.shape, A.shape)
