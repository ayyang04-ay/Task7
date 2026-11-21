import pandas as pd, numpy as np, itertools, warnings
from scipy import stats
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test, multivariate_logrank_test
warnings.filterwarnings('ignore')
pd.set_option('display.width', 300); pd.set_option('display.max_rows', 3000); pd.set_option('display.max_colwidth', 80)
S = pd.read_csv('surv_long.csv')
# the PSLN-344 row in S03-J with an event flag but no day (S03!G46 blank): base case = excluded (matches stated n=9)
S['missing_day'] = S.day.isna()

META = {
 'S03-I':      dict(age='aged', strain='BALB/c', vaccine='bivalent', challenge='10xLD50 CA09 H1N1 (matched virus)', day='d14', horizon=14),
 'S03-J':      dict(age='not stated (no (Y) label)', strain='not stated', vaccine='rgH5N1', challenge='wild-type VN04 H5N1', day='d2', horizon=21),
 'S06-A':      dict(age='aged', strain='BALB/c', vaccine='Aichi H3N2', challenge='5xLD50 PR8 H1N1 (mismatched virus)', day='d14', horizon=14),
 'S06-B':      dict(age='aged', strain='BALB/c', vaccine='Aichi H3N2', challenge='5xLD50 PR8 H1N1 (mismatched virus)', day='d3', horizon=14),
 'S06-C':      dict(age='aged', strain='BALB/c', vaccine='bivalent', challenge='5xLD50 rgH5N1 (mismatched virus)', day='d14', horizon=14),
 'S06-D':      dict(age='aged', strain='BALB/c', vaccine='bivalent', challenge='5xLD50 rgH5N1 (mismatched virus)', day='d3', horizon=14),
 'S06-E':      dict(age='aged', strain='BALB/c', vaccine='Aichi H3N2', challenge='5xLD50 PR8 H1N1 (mismatched virus)', day='d60', horizon=14),
 'S06-F':      dict(age='aged', strain='BALB/c', vaccine='bivalent', challenge='5xLD50 rgH5N1 (mismatched virus)', day='d60', horizon=14),
 'S06-G':      dict(age='aged', strain='BALB/c', vaccine='CA09 H1N1', challenge='5xLD50 Perth H3N2 (mismatched virus)', day='d60', horizon=14),
 'S06-E(r71)': dict(age='14 months at vaccination', strain='BALB/c', vaccine='bivalent', challenge='5xLD50 PR8 H1N1', day='not stated', horizon=14),
 'S06-F(r71)': dict(age='14 months at vaccination', strain='BALB/c', vaccine='bivalent', challenge='5xLD50 Perth H3N2', day='d14', horizon=14),
 'S09-B':      dict(age='young', strain='BALB/c', vaccine='Aichi H3N2', challenge='5xLD50 PR8 H1N1', day='d21', horizon=14),
 'S09-D':      dict(age='young', strain='BALB/c', vaccine='CA09 H1N1', challenge='5xLD50 Perth H3N2', day='d21', horizon=14),
 'S09-F':      dict(age='young', strain='BALB/c', vaccine='bivalent', challenge='5xLD50 rgH5N1', day='d180', horizon=14),
 'S13-E':      dict(age='young', strain='BALB/c', vaccine='bivalent', challenge='10xLD50 CA09 H1N1 (matched virus)', day='d14', horizon=14),
 'S15-H':      dict(age='aged', strain='BALB/c', vaccine='bivalent / none', challenge='5xLD50 rgH5N1', day='d3', horizon=14),
 'S15-L':      dict(age='aged (20 mo)', strain='C57BL/6', vaccine='bivalent', challenge='not stated', day='not stated', horizon=14),
 'S15-N':      dict(age='aged (20 mo)', strain='Swiss Webster', vaccine='bivalent', challenge='not stated', day='not stated', horizon=14),
}

def cp(k, n, a=0.05):
    lo = 0.0 if k == 0 else stats.beta.ppf(a/2, k, n-k+1)
    hi = 1.0 if k == n else stats.beta.ppf(1-a/2, k+1, n-k)
    return lo, hi

grp_rows=[]; pair_rows=[]
for blk, d0 in S.groupby('block', sort=False):
    d = d0[~d0.missing_day]
    for g, x in d.groupby('group', sort=False):
        n=len(x); deaths=int(x.event.sum()); surv=n-deaths
        kmf = KaplanMeierFitter().fit(x.day, x.event)
        med = kmf.median_survival_time_
        lo, hi = cp(surv, n)
        n_rows = int((d0.group==g).sum())
        grp_rows.append(dict(block=blk, **META[blk], group=g, n=n, n_rows_in_sheet=n_rows, deaths=deaths, survivors=surv, surv_pct=100*surv/n, ci_lo=100*lo, ci_hi=100*hi,
                             median_days=(np.inf if np.isinf(med) else med), death_days=sorted(x[x.event==1].day.astype(int).tolist()),
                             cells=f"{x.cell_evt.iloc[0]}:{x.cell_evt.iloc[-1].split('!')[1]}"))
    for a, b in itertools.combinations(d.group.unique(), 2):
        xa = d[d.group==a]; xb = d[d.group==b]
        lr = logrank_test(xa.day, xb.day, xa.event, xb.event)
        tab = [[int((xa.event==0).sum()), int(xa.event.sum())], [int((xb.event==0).sum()), int(xb.event.sum())]]
        fe = stats.fisher_exact(tab)[1]
        pair_rows.append(dict(block=blk, A=a, B=b, surv_A=f"{tab[0][0]}/{len(xa)}", surv_B=f"{tab[1][0]}/{len(xb)}", logrank_chi2=lr.test_statistic, p_logrank=lr.p_value, p_fisher=fe))
G = pd.DataFrame(grp_rows); P = pd.DataFrame(pair_rows)
G.to_csv('surv_groups.csv', index=False); P.to_csv('surv_pairs.csv', index=False)
print(G[['block','age','strain','vaccine','challenge','day','group','n','n_rows_in_sheet','survivors','surv_pct','ci_lo','ci_hi','median_days','death_days','cells']].round(1).to_string())
print()
key = P[((P.A.str.contains('344'))|(P.B.str.contains('344')))]
print(P.round(5).to_string())
