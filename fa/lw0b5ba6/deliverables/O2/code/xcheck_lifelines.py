import pandas as pd, numpy as np
from lifelines.statistics import logrank_test
s=pd.read_csv('survival.csv').dropna(subset=['day'])
p=pd.read_csv('surv_pairwise.csv')
maxdiff=0
for _,r in p.iterrows():
    a,b=r.comparison.split(' vs ')
    A=s[(s.block==r.block)&(s.group==a)]; B=s[(s.block==r.block)&(s.group==b)]
    lr=logrank_test(A.day,B.day,A.event,B.event)
    maxdiff=max(maxdiff,abs(lr.p_value-r.logrank_p))
print("max |p_mine - p_lifelines| =",maxdiff)
