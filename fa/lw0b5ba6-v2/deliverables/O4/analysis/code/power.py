import numpy as np, pandas as pd
from scipy import stats
vals = pd.read_csv('values_corrected.csv')
def fisher_power(p1,p0,n,alpha=0.05):
    # exact power: sum over outcomes of P(x1)P(x0) * 1[fisher p<alpha]
    from scipy.stats import binom, fisher_exact
    pw=0.0
    x = np.arange(n+1); b1 = binom.pmf(x,n,p1); b0 = binom.pmf(x,n,p0)
    for i in x:
        for j in x:
            if b1[i]*b0[j] < 1e-12: continue
            if fisher_exact([[i,n-i],[j,n-j]])[1] < alpha: pw += b1[i]*b0[j]
    return pw
scen = [('Observed, pooled de-duplicated (T3 set B)',0.84,0.12),('Conservative, BW-reconciled (T3 set C)',0.81,0.16),
        ('Lower 95% bound of set-C risk difference (53 pts)',0.69,0.16),('Sceptical: effect halved',0.50,0.16)]
rows=[]
for lab,p1,p0 in scen:
    for n in [7,10,12,15,20,25,30]:
        rows.append(dict(scenario=lab, p_PSLN344=p1, p_PSLN212=p0, n_per_arm=n, power=round(fisher_power(p1,p0,n),3)))
pw = pd.DataFrame(rows)
print(pw.pivot_table(index='scenario', columns='n_per_arm', values='power').round(2).to_string())
pw.to_csv('/tmp/outputs/analysis/T12_power_survival.csv', index=False)
# immunogenicity: pooled within-group SD of log10 HAI / IgG / IFNg+CD8 (%) from aged groups
def sd_pooled(block, log=True, groups=('PSLN-212','PSLN-344')):
    d = vals[(vals.block==block)&(vals.g.isin(groups))]
    y = np.log10(d.value) if log else d.value
    d = d.assign(y=y); s = d.groupby('g').y.agg(['var','count'])
    return np.sqrt(((s['var']*(s['count']-1)).sum())/((s['count']-1).sum()))
for blk,lab,log,delta in [('S03-C','HAI CA09 (log10)',True,np.log10(4)),('S03-A','IgG CA09 (log10)',True,np.log10(4)),('S05-F','IFNg+ CD8 % (H5N1 recall)',False,2.0)]:
    sd = sd_pooled(blk,log)
    # n per arm for two-sided t-test, alpha .05, power .9
    from statsmodels.stats.power import TTestIndPower
    n = TTestIndPower().solve_power(effect_size=delta/sd, alpha=0.05, power=0.9)
    print(f'{lab}: pooled within-group SD = {sd:.3f}; detect {"4-fold" if log else "+2.0 pts"} difference with 90% power -> n = {np.ceil(n):.0f}/arm')
