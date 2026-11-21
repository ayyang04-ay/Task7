import numpy as np, pandas as pd
from scipy import stats
from statlib import *
from statsmodels.stats.contingency_tables import StratifiedTable
pd.set_option('display.width', 300); pd.set_option('display.max_rows', 3000); pd.set_option('display.float_format', lambda x: f'{x:.4g}')

def strat_logrank(pairs):
    """pairs: list of (d1,e1,d2,e2) per stratum -> stratified log-rank"""
    OE=0; V=0
    for d1,e1,d2,e2 in pairs:
        d = np.concatenate([d1,d2]).astype(float); e = np.concatenate([e1,e2]).astype(int); g = np.r_[np.zeros(len(d1)), np.ones(len(d2))]
        for u in np.unique(d[e==1]):
            n = (d>=u).sum(); n1 = ((d>=u)&(g==0)).sum(); m = ((d==u)&(e==1)).sum(); m1 = ((d==u)&(e==1)&(g==0)).sum()
            OE += m1 - m*n1/n
            if n>1: V += m*(n1/n)*(1-n1/n)*(n-m)/(n-1)
    chi = OE**2/V
    return chi, stats.chi2.sf(chi,1)

def pooled(strata, label, override=None):
    """strata: list of (block, g344, g212). override: dict (block, group) -> survivors (for sensitivity)"""
    tabs=[]; pairs=[]; rows=[]
    for blk, ga, gb in strata:
        df = S[blk]; mx = df['day'].max()
        a = df[df.group==ga]; b = df[df.group==gb]
        sa, na = int((a.event==0).sum()), len(a); sb, nb = int((b.event==0).sum()), len(b)
        if override:
            sa = override.get((blk,ga), sa); sb = override.get((blk,gb), sb)
        tabs.append(np.array([[sa, na-sa],[sb, nb-sb]]))
        pairs.append((a['day'].fillna(mx).values, a['event'].values, b['day'].fillna(mx).values, b['event'].values))
        rows.append((blk, ga, f'{sa}/{na}', gb, f'{sb}/{nb}'))
    SA = sum(t[0,0] for t in tabs); NA = sum(t[0].sum() for t in tabs); SB = sum(t[1,0] for t in tabs); NB = sum(t[1].sum() for t in tabs)
    loA, hiA = cp_ci(SA, NA); loB, hiB = cp_ci(SB, NB)
    st = StratifiedTable(tabs)
    cmh = st.test_null_odds(correction=True)
    # Mantel-Haenszel risk difference with Greenland-Robins variance
    num = sum((t[0,0]*t[1].sum() - t[1,0]*t[0].sum())/t.sum() for t in tabs); den = sum(t[0].sum()*t[1].sum()/t.sum() for t in tabs)
    rd = num/den
    var = sum((t[0,0]*t[0,1]*t[1].sum()**3 + t[1,0]*t[1,1]*t[0].sum()**3)/(t[0].sum()*t[1].sum()*t.sum()**2) for t in tabs)
    se = np.sqrt(var)/den
    chi, p_slr = (np.nan, np.nan) if override else strat_logrank(pairs)
    res = dict(set=label, n_strata=len(tabs), surv_344=f'{SA}/{NA}', pct_344=100*SA/NA, ci344=f'{100*loA:.0f}-{100*hiA:.0f}', surv_212=f'{SB}/{NB}', pct_212=100*SB/NB, ci212=f'{100*loB:.0f}-{100*hiB:.0f}',
               MH_risk_diff=100*rd, rd_lo=100*(rd-1.96*se), rd_hi=100*(rd+1.96*se), MH_OR=st.oddsratio_pooled, cmh_chi2=cmh.statistic, p_cmh=cmh.pvalue, strat_logrank_chi2=chi, p_strat_logrank=p_slr)
    return res, rows

A = [('S03-I','PSLN-344','PSLN-212'),('S03-J','PSLN-344','PSLN-212'),('S06-A','PSLN-344','PSLN-212'),('S06-B','PSLN-344','PSLN-212'),('S06-C','PSLN-344','PSLN-212'),
     ('S06-D','PSLN-344','PSLN-212'),('S06-E','PSLN-344','PSLN-212'),('S06-F','PSLN-344','PSLN-212'),('S06-G','PSLN-344','PSLN-212')]
Bset = [x for x in A if x[0] not in ('S03-I','S03-J','S06-C')]
Cset = A + [('S15-L','PSLN-344','PSLN-212'),('S15-N','PSLN-344','PSLN-212'),('S06-E2','Naïve+PSLN-344','Naïve+PSLN-212'),('S06-E2','Imprinting+PSLN-344','Imprinting+PSLN-212'),
            ('S06-F2','Naïve+PSLN-344','Naïve+PSLN-212'),('S06-F2','Imprinting+PSLN-344','Imprinting+PSLN-212')]
Dset = [x for x in Cset if x[0] not in ('S03-I','S03-J','S06-C')]
# worst case for PSLN-344 / best case for PSLN-212 using body-weight-inferred survivors where they disagree with the time-to-event block
worst = {('S06-D','PSLN-344'):5, ('S03-I','PSLN-212'):3, ('S06-E','PSLN-212'):1, ('S03-J','PSLN-212'):5}
out=[]; detail={}
for lab, st_, ov in [('A: aged BALB/c, all 9 blocks as printed', A, None),
                     ('B: aged BALB/c, conservative (drop S03-I, S03-J, S06-C)', Bset, None),
                     ('C: all strains/ages, as printed (15 strata)', Cset, None),
                     ('D: all strains/ages, conservative (drop S03-I, S03-J, S06-C)', Dset, None),
                     ('E: set A with worst-case body-weight-inferred counts', A, worst),
                     ('F: set B with worst-case body-weight-inferred counts', Bset, worst)]:
    r, rows = pooled(st_, lab, ov); out.append(r); detail[lab]=rows
o = pd.DataFrame(out); o.to_csv('stats_survival_pooled.csv', index=False)
print(o.T.to_string())
for k,v in detail.items():
    print('\n', k)
    for r in v: print('   ', r)
