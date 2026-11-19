import pandas as pd, numpy as np, warnings
from scipy import stats
from statsmodels.duration.survfunc import survdiff, SurvfuncRight
from statsmodels.stats.contingency_tables import StratifiedTable
warnings.filterwarnings('ignore')
S = pd.read_csv('/tmp/work/tidy/survival.csv')
# S03-J PSLN-344 animal 10 has no time value; it is censored (event 0) -> assign end of observation (21 d) for analysis,
# and flag. (Sensitivity: drop it.)
S['days_imputed'] = S['days'].isna()
S.loc[S.days.isna(), 'days'] = 21.0

meta = {
 'S03-I': dict(model='aged BALB/c', vaccine='bivalent', challenge='10x mLD50 CA09 H1N1 (homologous)', day=14, ctype='homologous'),
 'S03-J': dict(model='aged BALB/c (age not stated in block)', vaccine='rgH5N1', challenge='wild-type VN04 H5N1', day=2, ctype='homologous H5, early'),
 'S06-A': dict(model='aged BALB/c', vaccine='Aichi H3N2', challenge='5x PR8 H1N1', day=14, ctype='heterosubtypic'),
 'S06-B': dict(model='aged BALB/c', vaccine='Aichi H3N2', challenge='5x PR8 H1N1', day=3, ctype='heterosubtypic, early'),
 'S06-C': dict(model='aged BALB/c', vaccine='bivalent', challenge='5x rgH5N1', day=14, ctype='heterosubtypic (H5)'),
 'S06-D': dict(model='aged BALB/c', vaccine='bivalent', challenge='5x rgH5N1', day=3, ctype='heterosubtypic (H5), early'),
 'S06-E': dict(model='aged BALB/c', vaccine='Aichi H3N2', challenge='5x PR8 H1N1', day=60, ctype='heterosubtypic, durable'),
 'S06-F': dict(model='aged BALB/c', vaccine='bivalent', challenge='5x rgH5N1', day=60, ctype='heterosubtypic (H5), durable'),
 'S06-G': dict(model='aged BALB/c', vaccine='CA09 H1N1', challenge='5x Perth H3N2', day=60, ctype='heterosubtypic, durable'),
 'S06-E(rows71-105; imprinting)': dict(model='14-mo BALB/c, +/- prior PR8 infection', vaccine='bivalent', challenge='5x PR8 H1N1', day=None, ctype='imprinting'),
 'S06-F(rows71-105; imprinting)': dict(model='14-mo BALB/c, +/- prior PR8 infection', vaccine='bivalent', challenge='5x Perth H3N2', day=14, ctype='imprinting'),
 'S09-B': dict(model='young BALB/c', vaccine='Aichi H3N2', challenge='5x PR8 H1N1', day=21, ctype='heterosubtypic'),
 'S09-D': dict(model='young BALB/c', vaccine='CA09 H1N1', challenge='5x Perth H3N2', day=21, ctype='heterosubtypic'),
 'S09-F': dict(model='young BALB/c', vaccine='bivalent', challenge='5x VN04 rgH5N1', day=180, ctype='heterosubtypic (H5), durable'),
 'S13-E': dict(model='young BALB/c', vaccine='bivalent', challenge='10x CA09 H1N1', day=14, ctype='homologous'),
 'S15-H': dict(model='aged BALB/c', vaccine='bivalent / none', challenge='5x VN04 rgH5N1', day=3, ctype='rapid onset / antigen-free control'),
 'S15-L': dict(model='aged C57BL/6 (20 mo)', vaccine='bivalent', challenge='NOT STATED', day=None, ctype='strain generality'),
 'S15-N': dict(model='aged Swiss Webster (20 mo)', vaccine='bivalent', challenge='NOT STATED', day=None, ctype='strain generality'),
}

def logrank(d, a, b):
    x = d[d.group.isin([a, b])]
    if x.event.sum() == 0:
        return np.nan
    st, p = survdiff(x.days.values, x.event.values, (x.group == a).astype(int).values)
    return p

rows, pw = [], []
for blk, d in S.groupby('block', sort=False):
    for g, dg in d.groupby('group', sort=False):
        n, dead = len(dg), int(dg.event.sum())
        sf = SurvfuncRight(dg.days.values, dg.event.values)
        # median survival (first time surv <= 0.5)
        med = np.nan
        if dead > 0:
            s = pd.Series(sf.surv_prob, index=sf.surv_times)
            below = s[s <= 0.5]
            med = below.index[0] if len(below) else np.nan
        lo, hi = stats.beta.ppf(0.025, n - dead, dead + 1) if n - dead > 0 else 0.0, stats.beta.ppf(0.975, n - dead + 1, dead) if dead > 0 else 1.0
        rows.append(dict(block=blk, **meta.get(blk, {}), group=g, n=n, deaths=dead, survivors=n - dead,
                         survival_pct=100 * (n - dead) / n, surv_95lo=100 * lo, surv_95hi=100 * hi, median_survival_days=med,
                         death_days=sorted(dg.loc[dg.event == 1, 'days'].astype(int).tolist())))
    groups = list(dict.fromkeys(d.group))
    for a in groups:
        for b in groups:
            if a >= b:
                continue
            x = d[d.group.isin([a, b])]
            ta = [[int((x[x.group == a].event == 0).sum()), int(x[x.group == a].event.sum())],
                  [int((x[x.group == b].event == 0).sum()), int(x[x.group == b].event.sum())]]
            pf = stats.fisher_exact(ta)[1]
            pw.append(dict(block=blk, group_a=a, group_b=b, surv_a=f'{ta[0][0]}/{sum(ta[0])}', surv_b=f'{ta[1][0]}/{sum(ta[1])}',
                           p_logrank=logrank(d, a, b), p_fisher=pf))
R = pd.DataFrame(rows); P = pd.DataFrame(pw)
R.to_csv('/tmp/work/tidy/summary_survival.csv', index=False); P.to_csv('/tmp/work/tidy/pairwise_survival.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500); pd.set_option('display.max_colwidth', 40)
print(R[['block', 'model', 'challenge', 'day', 'group', 'n', 'deaths', 'survival_pct', 'surv_95lo', 'surv_95hi', 'median_survival_days', 'death_days']].round(1).to_string(index=False))
print()
key = P[(P.group_a.str.contains('344') | P.group_b.str.contains('344'))]
print(key.round(5).to_string(index=False))
