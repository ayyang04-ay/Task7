import numpy as np, pandas as pd
from statsmodels.stats.proportion import proportion_confint
def newcombe(x1,n1,x2,n2):
    l1,u1 = proportion_confint(x1,n1,method='wilson'); l2,u2 = proportion_confint(x2,n2,method='wilson')
    p1,p2 = x1/n1, x2/n2; d = p1-p2
    lo = d - np.sqrt((p1-l1)**2 + (u2-p2)**2); hi = d + np.sqrt((u1-p1)**2 + (p2-l2)**2)
    return d, lo, hi
R = pd.read_csv('/tmp/work/survival_pooled.csv')
out=[]
for _,r in R.iterrows():
    x1,n1 = map(int, r.surv_344.split('/')); x2,n2 = map(int, r.surv_212.split('/'))
    d,lo,hi = newcombe(x1,n1,x2,n2)
    out.append((r.analysis[:60], r.surv_344, r.surv_212, round(100*d,1), round(100*lo,1), round(100*hi,1), r.CMH_p, r.strat_logrank_p, r.MH_OR))
    R.loc[_, 'RD_newcombe_lo'] = 100*lo; R.loc[_, 'RD_newcombe_hi'] = 100*hi
R.to_csv('/tmp/work/survival_pooled.csv', index=False)
for o in out: print(o)
print()
# pooled arms pairwise
PO = pd.read_csv('/tmp/work/survival_pooled_arms.csv').set_index('group')
for a,b in [('PSLN-344','Sham'),('PSLN-212','Sham'),('PSLN-212(Y)','PSLN-344')]:
    d,lo,hi = newcombe(PO.loc[a,'survivors'],PO.loc[a,'n'],PO.loc[b,'survivors'],PO.loc[b,'n'])
    print(a,'vs',b, f"{PO.loc[a,'survivors']}/{PO.loc[a,'n']} vs {PO.loc[b,'survivors']}/{PO.loc[b,'n']}", round(100*d,1), round(100*lo,1), round(100*hi,1))
