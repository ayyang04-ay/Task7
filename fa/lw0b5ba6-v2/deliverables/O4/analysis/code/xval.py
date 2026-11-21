import pandas as pd, numpy as np
from lifelines.statistics import logrank_test
surv = pd.read_csv('survival.csv'); surv.loc[(surv.block=='S03-J') & surv.day.isna(), 'day'] = 21
def a(b,g):
    d=surv[(surv.block==b)&(surv.group==g)]; return d.day.values, d.event.values
for b,g1,g2 in [('S03-I','PSLN-344','PSLN-212'),('S06-A','PSLN-344','PSLN-212'),('S06-G','PSLN-344','PSLN-212'),('S15-N','PSLN-344','PSLN-212'),('S06-A','PSLN-344','PSLN-212(Y)'),('S03-J','PSLN-344','PSLN-212')]:
    t1,e1=a(b,g1); t2,e2=a(b,g2)
    r=logrank_test(t1,t2,e1,e2)
    print(b,g1,'vs',g2,'chi2=%.2f p=%.6f'%(r.test_statistic,r.p_value))
