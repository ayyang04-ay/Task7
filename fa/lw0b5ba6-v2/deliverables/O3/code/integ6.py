from load import *
import numpy as np, pandas as pd
pairs = [('S03-I','S13-F'),('S03-J','S13-G'),('S06-A','S15-A'),('S06-B','S15-B'),('S06-C','S15-C'),('S06-D','S15-D'),
         ('S06-E','S15-E'),('S06-F','S15-F'),('S06-G','S15-G'),("S06-E'(imprint)",'S15-J'),("S06-F'(imprint)",'S15-K'),
         ('S09-B','S09-C'),('S09-D','S09-E'),('S09-F','S09-G'),('S15-H','S15-I'),('S15-L','S15-M'),('S15-N','S15-O')]
def norm(g): return g.replace('PSLN-212Y','PSLN-212(Y)').replace('PSLN-344Y','PSLN-344(Y)').strip()
rows=[]
for sb, wbk in pairs:
    s = SV[SV.block==sb].copy(); s['g']=s.group.map(norm)
    w = DF[DF.block==wbk].copy(); w['g']=w.group.map(norm); w['day']=pd.to_numeric(w['day'])
    for g in sorted(set(s.g)|set(w.g)):
        ss = s[s.g==g]; ww = w[w.g==g]
        n_s = len(ss); d_s = int(ss.event.sum()) if n_s else None
        # weight-apparent deaths: column missing at final day, or last >=3 values identical (frozen)
        app=0; ncol=0; alive_at={}
        for c, d in ww.groupby('animal_col'):
            ncol+=1
            t = d.set_index('day')['value'].sort_index()
            last = t.index.max()
            frozen = len(t)>=3 and np.allclose(t.iloc[-3:], t.iloc[-1])
            if last < 14 or frozen: app+=1
        # max #alive per survival at day 8 vs weights recorded at day 8 (non-missing)
        def alive(day): return int(((ss.time>day)|((ss.time>=day)&(ss.event==1))|(ss.event==0)).sum()) if n_s else None
        w8 = int((ww.day==8).sum())
        w10 = int((ww.day==10).sum())
        rows.append(dict(survival=sb, weights=wbk, group=g, n_surv=n_s, deaths_surv=d_s, n_weight_cols=ncol,
                         weight_apparent_deaths=app, at_risk_d8_surv=alive(8), weights_d8=w8, at_risk_d10_surv=alive(10), weights_d10=w10))
R = pd.DataFrame(rows)
R['flag'] = ''
R.loc[(R.n_surv==0)|(R.n_weight_cols==0),'flag'] += 'GROUP MISSING IN ONE FILE; '
m = (R.n_surv>0)&(R.n_weight_cols>0)
R.loc[m & (R.deaths_surv!=R.weight_apparent_deaths),'flag'] += 'death count mismatch; '
R.loc[m & (R.weights_d8>R.at_risk_d8_surv),'flag'] += 'more weights than survivors d8; '
R.loc[m & (R.weights_d10>R.at_risk_d10_surv),'flag'] += 'more weights than survivors d10; '
pd.set_option('display.width',250); pd.set_option('display.max_rows',200)
print(R.to_string(index=False))
R.to_csv('/tmp/work/survival_weight_reconciliation.csv',index=False)
