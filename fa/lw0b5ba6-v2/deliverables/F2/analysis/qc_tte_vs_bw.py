import numpy as np, pandas as pd
from blocks import *
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500); pd.set_option('display.max_colwidth', 200)

# linked pairs: weight block -> TTE block  (per annotation)
LINK = {'S09-C':'S09-B','S09-E':'S09-D','S09-G':'S09-F','S13-F':'S03-I','S13-G':'S03-J',
        'S15-A':'S06-A','S15-B':'S06-B','S15-C':'S06-C','S15-D':'S06-D','S15-E':'S06-E','S15-F':'S06-F','S15-G':'S06-G',
        'S15-I':'S15-H','S15-J':'S06-E2','S15-K':'S06-F2','S15-M':'S15-L','S15-O':'S15-N'}

def infer(df):
    """per animal: last day with a value; day the value froze (LOCF signature); inferred status"""
    rows=[]
    for (g,rep), d in df.groupby(['group','rep'], sort=False):
        d = d.sort_values('day')
        days = list(d['day']); vals = list(d['value'])
        last_day = days[-1]
        # frozen run ending at the last recorded day
        k = len(vals)-1
        while k>0 and vals[k]==vals[k-1]: k-=1
        frozen_from = days[k] if k < len(vals)-1 else None
        run_len = len(vals)-1-k
        if last_day < 14:
            status = 'dead_blank'; last_real = last_day
        elif run_len >= 1 and vals[-1] < 97 and k>0:   # value frozen through d14 => carried forward
            status = 'dead_LOCF' if run_len>=2 or vals[-1] < 90 else 'ambiguous_flat'
            last_real = frozen_from
        else:
            status = 'alive'; last_real = 14
        rows.append(dict(group=g, rep=rep, last_day=last_day, frozen_from=frozen_from, run_len=run_len, d14=vals[-1] if last_day==14 else np.nan,
                         nadir=min(vals), status=status, last_real=last_real))
    return pd.DataFrame(rows)

out=[]
for wk, sk in LINK.items():
    inf = infer(W[wk])
    tte = S[sk]
    print('\n=====', wk, '(weights)  vs ', sk, '(time-to-event)')
    gw = list(inf['group'].unique()); gs = list(tte['group'].unique())
    print('  weight groups:', gw); print('  TTE groups   :', gs)
    for g in gw:
        d = inf[inf.group==g]
        n = len(d); alive = int((d.status=='alive').sum()); amb = int((d.status=='ambiguous_flat').sum())
        dead = d[d.status.str.startswith('dead')]
        lastreal = sorted(dead['last_real'].tolist())
        # matching TTE group name (normalise)
        def norm(x): return x.replace(' ','').replace('(Y)','Y').replace('Naïve','Naive').lower()
        m = [x for x in gs if norm(x)==norm(g)]
        if m:
            t = tte[tte.group==m[0]]
            tn = len(t); tdeaths = int(t.event.sum()); tdays = sorted(t[t.event==1]['day'].tolist())
            tsurv = tn - tdeaths
        else:
            tn=tdeaths=tsurv=None; tdays=None
        flag = ''
        if m and (alive+amb != tsurv or n!=tn): flag = '  <-- MISMATCH'
        if m and alive != tsurv and alive+amb == tsurv: flag = '  (ambiguous flat)'
        print(f"  {g:22s} BW: n={n} alive@d14={alive} ambiguous={amb} dead={len(dead)} last-real-weight-days={lastreal} | TTE: n={tn} survivors={tsurv} death-days={tdays}{flag}")
        out.append(dict(weight_block=wk, tte_block=sk, group=g, bw_n=n, bw_alive_d14=alive, bw_ambiguous=amb, bw_dead=len(dead), bw_last_real_days=lastreal,
                        tte_n=tn, tte_survivors=tsurv, tte_death_days=tdays, flag=flag.strip()))
    for g in gs:
        def norm(x): return x.replace(' ','').replace('(Y)','Y').replace('Naïve','Naive').lower()
        if not [x for x in gw if norm(x)==norm(g)]:
            t = tte[tte.group==g]
            print(f"  {g:22s} BW: -- no weight group of this name --           | TTE: n={len(t)} survivors={len(t)-int(t.event.sum())} death-days={sorted(t[t.event==1]['day'].tolist())}")
            out.append(dict(weight_block=wk, tte_block=sk, group=g, bw_n=None, tte_n=len(t), tte_survivors=len(t)-int(t.event.sum()), tte_death_days=sorted(t[t.event==1]['day'].tolist()), flag='group absent from weight block'))
pd.DataFrame(out).to_csv('qc_tte_vs_bodyweight.csv', index=False)
