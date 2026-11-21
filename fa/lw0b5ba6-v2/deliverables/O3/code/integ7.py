from load import *
import numpy as np, pandas as pd, itertools
# ---- identical survival outcomes across blocks (group-level multisets) ----
sig = {}
for (b,g), d in SV.groupby(['block','group']):
    sig[(b,g)] = tuple(sorted(zip(d.time.fillna(-1), d.event)))
print("Group survival records that are IDENTICAL across different experiments (excluding all-censored-at-14 groups):")
for (k1,s1),(k2,s2) in itertools.combinations(sig.items(),2):
    if k1[0]!=k2[0] and s1==s2 and any(e==1 for _,e in s1):
        print(f"  {k1[0]}:{k1[1]}  ==  {k2[0]}:{k2[1]}   {[(int(t),e) for t,e in s1]}")
print("\nWhole-block comparison S06-C vs S06-D (row-by-row):")
a = SV[SV.block=='S06-C'][['group','time','event']].reset_index(drop=True)
b = SV[SV.block=='S06-D'][['group','time','event']].reset_index(drop=True)
print("  identical row-for-row:", a.equals(b))
# ---- refined reconciliation: fresh weights recorded AFTER the survival-recorded death ----
pairs = [('S03-I','S13-F'),('S03-J','S13-G'),('S06-A','S15-A'),('S06-B','S15-B'),('S06-C','S15-C'),('S06-D','S15-D'),
         ('S06-E','S15-E'),('S06-F','S15-F'),('S06-G','S15-G'),("S06-E'(imprint)",'S15-J'),("S06-F'(imprint)",'S15-K'),
         ('S09-B','S09-C'),('S09-D','S09-E'),('S09-F','S09-G'),('S15-H','S15-I'),('S15-L','S15-M'),('S15-N','S15-O')]
def norm(g): return g.replace('PSLN-212Y','PSLN-212(Y)').replace('PSLN-344Y','PSLN-344(Y)').strip()
rows=[]
for sb, wbk in pairs:
    s = SV[SV.block==sb].copy(); s['g']=s.group.map(norm)
    w = DF[DF.block==wbk].copy(); w['g']=w.group.map(norm); w['day']=pd.to_numeric(w['day'])
    for g in sorted(set(s.g)|set(w.g)):
        ss=s[s.g==g]; ww=w[w.g==g]
        if len(ss)==0 or len(ww)==0:
            rows.append(dict(pair=f'{sb}/{wbk}',group=g,issue='group present in only one file',surv_deaths=(int(ss.event.sum()) if len(ss) else None),
                             weight_deaths=None)); continue
        # weight-derived deaths: missing at d14 or >=2 identical trailing values (frozen)
        wd=[]; fresh_by_day={}
        for c,d in ww.groupby('animal_col'):
            t=d.set_index('day')['value'].sort_index()
            prev=t.shift(1); fr=t[~np.isclose(t,prev)]
            for day in fr.index: fresh_by_day[day]=fresh_by_day.get(day,0)+1
            if t.index.max()<14: wd.append(int(t.index.max()))
            elif len(t)>=2 and np.isclose(t.iloc[-1],t.iloc[-2]):
                # find first day of frozen run
                k=len(t)-1
                while k>0 and np.isclose(t.iloc[k-1],t.iloc[-1]): k-=1
                wd.append(int(t.index[k]))
        sd = sorted(ss[ss.event==1].time.astype(int).tolist())
        # fresh weights at day d must be <= number alive entering day d (alive = not dead before d)
        viol=[]
        for day,nf in sorted(fresh_by_day.items()):
            if day==0: continue
            alive = int(((ss.event==0)|(ss.time>=day)).sum())
            if nf>alive: viol.append(f'd{int(day)}:{nf}>{alive}')
        rows.append(dict(pair=f'{sb}/{wbk}',group=g,surv_deaths=len(sd),weight_deaths=len(wd),surv_death_days=sd,weight_last_real_day=sorted(wd),
                         fresh_weights_exceed_alive=';'.join(viol),
                         issue=('death count differs; ' if len(sd)!=len(wd) else '')+('fresh weights after recorded deaths' if viol else '')))
R=pd.DataFrame(rows)
pd.set_option('display.width',250); pd.set_option('display.max_rows',200); pd.set_option('display.max_colwidth',60)
print(R[R.issue!=''].to_string(index=False))
R.to_csv('/tmp/work/survival_weight_reconciliation_refined.csv',index=False)
print('\nGroups checked:',len(R),' with issues:',(R.issue!='').sum())
