import pandas as pd, numpy as np, itertools, warnings
from scipy import stats
from lifelines.statistics import logrank_test
warnings.filterwarnings('ignore')
pd.set_option('display.width', 300); pd.set_option('display.max_rows', 3000); pd.set_option('display.max_colwidth', 80)
S = pd.read_csv('surv_long.csv'); S = S[S.day.notna()]
G = pd.read_csv('surv_groups.csv'); WG = pd.read_csv('wt_group_status.csv')

pairs = {'S03-I':'S13-F','S03-J':'S13-G','S06-A':'S15-A','S06-B':'S15-B','S06-C':'S15-C','S06-D':'S15-D','S06-E':'S15-E','S06-F':'S15-F','S06-G':'S15-G',
         'S06-E(r71)':'S15-J','S06-F(r71)':'S15-K','S09-B':'S09-C','S09-D':'S09-E','S09-F':'S09-G','S15-H':'S15-I','S15-L':'S15-M','S15-N':'S15-O'}
norm = lambda g: g.replace('Naïve','Naive').strip()
rows=[]
for sb, wb_ in pairs.items():
    gs = G[G.block==sb]
    for _, r in gs.iterrows():
        w = WG[(WG.block==wb_) & (WG.group.map(norm)==norm(r.group))]
        rows.append(dict(surv_block=sb, wt_block=wb_, group=r.group, table=f"{r.survivors}/{r.n}", table_death_days=r.death_days,
                         weights=(f"{int(w.alive_d_end.iloc[0])}/{int(w.n.iloc[0])}" if len(w) else 'group absent'),
                         wt_last_live_days=(w.last_live_days_removed.iloc[0] if len(w) else ''),
                         concordant=(len(w)>0 and int(w.alive_d_end.iloc[0])==r.survivors and int(w.n.iloc[0])==r.n)))
    # groups only in weights
    for _, w in WG[WG.block==wb_].iterrows():
        if norm(w.group) not in set(gs.group.map(norm)):
            rows.append(dict(surv_block=sb, wt_block=wb_, group=w.group, table='group absent', table_death_days='', weights=f"{w.alive_d_end}/{w.n}", wt_last_live_days=w.last_live_days_removed, concordant=False))
CON = pd.DataFrame(rows); CON.to_csv('surv_vs_weights.csv', index=False)
print(CON.to_string())

# ---------------- pooled analyses ----------------
def cp(k, n, a=0.05):
    lo = 0.0 if k == 0 else stats.beta.ppf(a/2, k, n-k+1)
    hi = 1.0 if k == n else stats.beta.ppf(1-a/2, k+1, n-k)
    return lo, hi

def strat_logrank(blocks, ga, gb):
    """stratified (by block) log-rank: sum O-E and V over strata"""
    OE = 0; V = 0
    for b in blocks:
        d = S[(S.block==b) & (S.group.isin([ga, gb]))]
        times = sorted(d[d.event==1].day.unique())
        for t in times:
            at = d[d.day >= t]
            n = len(at); n1 = (at.group==ga).sum()
            dd = ((d.day==t) & (d.event==1)).sum(); d1 = ((d.day==t) & (d.event==1) & (d.group==ga)).sum()
            if n > 1:
                OE += d1 - dd*n1/n
                V += dd*(n1/n)*(1-n1/n)*(n-dd)/(n-1)
    chi2 = OE**2/V if V>0 else np.nan
    return chi2, stats.chi2.sf(chi2, 1)

def mh_rd(blocks, ga, gb, counts):
    """Mantel-Haenszel risk difference (survival proportion gb - ga... we compute ga - gb) with Greenland-Robins variance; counts[(block, group)] = (survivors, n)"""
    num=0; den=0; P=0; Qv=0
    for b in blocks:
        a, n1 = counts[(b, ga)]; c, n0 = counts[(b, gb)]
        N = n1+n0; w = n1*n0/N
        num += (a*n0 - c*n1)/N; den += w
        P += (a*(n1-a)*n0**3 + c*(n0-c)*n1**3)/(n1*n0*N**2)
    rd = num/den; se = np.sqrt(P)/den
    return rd, rd-1.96*se, rd+1.96*se

def pooled(blocks, label, source='table', groups=('Sham','PSLN-212','PSLN-344','PSLN-212(Y)')):
    counts = {}
    out = {}
    for g in groups:
        k = n = 0
        for b in blocks:
            if source == 'table':
                r = G[(G.block==b)&(G.group==g)]
                if len(r)==0: continue
                kk, nn = int(r.survivors.iloc[0]), int(r.n.iloc[0])
            else:
                r = WG[(WG.block==pairs[b])&(WG.group==g)]
                if len(r)==0: continue
                kk, nn = int(r.alive_d_end.iloc[0]), int(r.n.iloc[0])
            counts[(b,g)] = (kk, nn); k += kk; n += nn
        if n: out[g] = (k, n, *cp(k, n))
    print(f"\n--- {label} [{source}] blocks={blocks}")
    for g,(k,n,lo,hi) in out.items(): print(f"   {g:12s} {k}/{n} = {100*k/n:.0f}%  (95% CI {100*lo:.0f}-{100*hi:.0f}%)")
    res = dict(label=label, source=source, blocks=','.join(blocks))
    for g,(k,n,lo,hi) in out.items(): res[g] = f"{k}/{n}"; res[g+'_pct'] = 100*k/n; res[g+'_lo']=100*lo; res[g+'_hi']=100*hi
    for ga, gb in [('PSLN-344','PSLN-212'), ('PSLN-344','Sham'), ('PSLN-212','Sham'), ('PSLN-344','PSLN-212(Y)')]:
        if ga in out and gb in out:
            tab = [[out[ga][0], out[ga][1]-out[ga][0]], [out[gb][0], out[gb][1]-out[gb][0]]]
            pf = stats.fisher_exact(tab)[1]
            bl = [b for b in blocks if (b,ga) in counts and (b,gb) in counts]
            rd, lo, hi = mh_rd(bl, ga, gb, counts)
            s = f"   {ga} vs {gb}: pooled Fisher p={pf:.2e}; MH risk difference (survival) = {100*rd:.0f} pts (95% CI {100*lo:.0f} to {100*hi:.0f})"
            res[f'{ga} vs {gb} fisher_p'] = pf; res[f'{ga} vs {gb} MH_RD'] = 100*rd; res[f'{ga} vs {gb} MH_lo'] = 100*lo; res[f'{ga} vs {gb} MH_hi'] = 100*hi
            if source == 'table':
                chi2, p = strat_logrank(bl, ga, gb)
                s += f"; stratified log-rank chi2={chi2:.1f}, p={p:.1e}"
                res[f'{ga} vs {gb} strat_logrank_chi2'] = chi2; res[f'{ga} vs {gb} strat_logrank_p'] = p
            print(s)
    return res

allres=[]
core8 = ['S03-I','S06-A','S06-B','S06-C','S06-D','S06-E','S06-F','S06-G']
core7 = [b for b in core8 if b != 'S06-D']
allres.append(pooled(core8, 'Aged BALB/c, single dose, all 8 blocks as printed'))
allres.append(pooled(core7, 'Aged BALB/c, single dose, excluding S06-D (row-for-row duplicate of S06-C)'))
allres.append(pooled(core8, 'Aged BALB/c, single dose, all 8 blocks', source='weights'))
allres.append(pooled(core7, 'Aged BALB/c, excl. S06-D', source='weights'))
allres.append(pooled(['S06-B','S06-D'], 'Aged BALB/c, challenge d3 (S06-B, S06-D)'))
allres.append(pooled(['S06-B','S06-D'], 'Aged BALB/c, challenge d3 (S15-B, S15-D)', source='weights'))
allres.append(pooled(['S03-I','S06-A','S06-C'], 'Aged BALB/c, challenge d14'))
allres.append(pooled(['S03-I','S06-A','S06-C'], 'Aged BALB/c, challenge d14', source='weights'))
allres.append(pooled(['S06-E','S06-F','S06-G'], 'Aged BALB/c, challenge d60', groups=('Sham','PSLN-212','PSLN-344','PSLN-212(Y)','Untreated')))
allres.append(pooled(['S06-E','S06-F','S06-G'], 'Aged BALB/c, challenge d60', source='weights', groups=('Sham','PSLN-212','PSLN-344','PSLN-212(Y)','Untreated')))
allres.append(pooled(['S15-L','S15-N'], 'Other strains aged 20 mo (C57BL/6, Swiss Webster)'))
allres.append(pooled(core7+['S15-L','S15-N'], 'All aged, 3 strains, excl. S06-D'))
allres.append(pooled(core7+['S15-L','S15-N','S03-J'], 'All aged, 3 strains, excl. S06-D, incl. WT H5N1 (S03-J; age not stated)'))
pd.DataFrame(allres).to_csv('pooled_survival.csv', index=False)

# day-14 vs day-60 within PSLN-344 (tables), and PSLN-344 d60 vs Untreated (unchallenged)
print("\nPSLN-344 d14 (S03-I,S06-A,S06-C) 20/21 vs d60 (S06-E,F,G) 14/21: Fisher p =", stats.fisher_exact([[20,1],[14,7]])[1])
print("PSLN-344 d3+d14 excl S06-D (S03-I,S06-A,S06-B,S06-C) 25/28 vs d60 14/21: Fisher p =", stats.fisher_exact([[25,3],[14,7]])[1])
print("PSLN-344 d60 challenged 14/21 vs Untreated unchallenged 17/21: Fisher p =", stats.fisher_exact([[14,7],[17,4]])[1])
print("weights: PSLN-344 d60 16/21 vs Untreated 17/21: Fisher p =", stats.fisher_exact([[16,5],[17,4]])[1])
print("Untreated 17/21 CI:", [round(100*x) for x in cp(17,21)], " deaths 4/21 CI:", [round(100*x) for x in cp(4,21)])
# young
print("\nYoung head-to-head (S09-B,D,F): PSLN-344Y 24/24, PSLN-212Y 24/24, Sham 0/23; CI for 24/24:", [round(100*x) for x in cp(24,24)])
