import numpy as np, pandas as pd, itertools
from scipy import stats
from statlib import *
pd.set_option('display.width', 300); pd.set_option('display.max_rows', 3000); pd.set_option('display.float_format', lambda x: f'{x:.4g}')

DESIGN = {  # block: (strain/age, vaccine, challenge, interval)
 'S03-I': ('BALB/c aged (>=20 mo)', 'bivalent H1N1+H3N2', '10x mLD50 CA09 H1N1 (homologous)', 'd14'),
 'S03-J': ('BALB/c aged (>=20 mo) [age not restated in block]', 'rgH5N1, single dose', 'wild-type VN04 H5N1 (homologous subtype)', 'd2'),
 'S06-A': ('BALB/c aged', 'Aichi H3N2', '5x mLD50 PR8 H1N1 (heterosubtypic)', 'd14'),
 'S06-B': ('BALB/c aged', 'Aichi H3N2', '5x mLD50 PR8 H1N1 (heterosubtypic)', 'd3'),
 'S06-C': ('BALB/c aged', 'bivalent H1N1+H3N2', '5x mLD50 rgH5N1 (heterosubtypic)', 'd14'),
 'S06-D': ('BALB/c aged', 'bivalent H1N1+H3N2', '5x mLD50 rgH5N1 (heterosubtypic)', 'd3'),
 'S06-E': ('BALB/c aged', 'Aichi H3N2', '5x mLD50 PR8 H1N1 (heterosubtypic)', 'd60'),
 'S06-F': ('BALB/c aged', 'bivalent H1N1+H3N2', '5x mLD50 rgH5N1 (heterosubtypic)', 'd60'),
 'S06-G': ('BALB/c aged', 'CA09 H1N1', '5x mLD50 Perth H3N2 (heterosubtypic)', 'd60'),
 'S06-E2': ('BALB/c 14 mo (10 mo + 4 mo), +/- prior PR8 infection', 'bivalent H1N1+H3N2', '5x LD50 PR8 H1N1', 'interval not stated'),
 'S06-F2': ('BALB/c 14 mo (10 mo + 4 mo), +/- prior PR8 infection', 'bivalent H1N1+H3N2', '5x LD50 Perth H3N2', 'd14'),
 'S09-B': ('BALB/c young', 'Aichi H3N2', '5x mLD50 PR8 H1N1', 'd21'),
 'S09-D': ('BALB/c young', 'CA09 H1N1', '5x mLD50 Perth H3N2', 'd21'),
 'S09-F': ('BALB/c young', 'bivalent H1N1+H3N2', '5x mLD50 VN04 rgH5N1', 'd180'),
 'S13-E': ('BALB/c young', 'bivalent H1N1+H3N2', '10x mLD50 CA09 H1N1', 'd14'),
 'S15-H': ('BALB/c aged', 'bivalent / none', '5x mLD50 VN04 rgH5N1', 'd3'),
 'S15-L': ('C57BL/6 aged 20 mo (young for (Y))', 'bivalent H1N1+H3N2', 'challenge virus not stated', 'not stated'),
 'S15-N': ('Swiss Webster aged 20 mo (young for (Y))', 'bivalent H1N1+H3N2', 'challenge virus not stated', 'not stated'),
}
rows=[]
for k, df in S.items():
    for g, d in df.groupby('group', sort=False):
        n=len(d); deaths=int(d.event.sum()); surv=n-deaths
        lo,hi = cp_ci(surv,n)
        dd = sorted(d[d.event==1]['day'].tolist())
        end = d['day'].max()
        # median survival (KM) : smallest t with S(t)<=0.5
        med = np.nan
        dv = d['day'].fillna(d['day'].max()).values; ev = d['event'].values
        for u in sorted(set(dv[ev==1])):
            if km_surv_at(dv, ev, u) <= 0.5: med=u; break
        cells = d['cellref'].tolist()
        rows.append(dict(block=k, model=DESIGN[k][0], vaccine=DESIGN[k][1], challenge=DESIGN[k][2], interval=DESIGN[k][3], group=g, n=n, deaths=deaths, survivors=surv,
                         surv_pct=100*surv/n, ci_lo=100*lo, ci_hi=100*hi, death_days=','.join(str(int(x)) for x in dd), median_surv_d=med, obs_end_d=end,
                         missing_day=int(d['day'].isna().sum()), cells=f"{cells[0]}:{cells[-1].split('!')[1]}"))
sv = pd.DataFrame(rows); sv.to_csv('stats_survival_groups.csv', index=False)
print(sv[['block','group','n','survivors','surv_pct','ci_lo','ci_hi','death_days','median_surv_d','cells']].to_string(index=False))

# pairwise tests within block
prs=[]
for k, df in S.items():
    gs = list(df.group.unique())
    for g1, g2 in itertools.combinations(gs, 2):
        a = df[df.group==g1]; b = df[df.group==g2]
        mx = df['day'].max()
        d1 = a['day'].fillna(mx).values; e1 = a['event'].values; d2 = b['day'].fillna(mx).values; e2 = b['event'].values
        chi, p, _ = logrank(d1,e1,d2,e2)
        pperm = logrank_perm(d1,e1,d2,e2)
        s1 = (e1==0).sum(); s2 = (e2==0).sum()
        _, pf = stats.fisher_exact([[s1, len(e1)-s1],[s2, len(e2)-s2]])
        prs.append(dict(block=k, g1=g1, g2=g2, surv1=f'{s1}/{len(e1)}', surv2=f'{s2}/{len(e2)}', logrank_chi2=chi, p_logrank=p, p_logrank_perm=pperm, p_fisher=pf))
pr = pd.DataFrame(prs); pr.to_csv('stats_survival_pairwise.csv', index=False)
print(pr.to_string(index=False))
