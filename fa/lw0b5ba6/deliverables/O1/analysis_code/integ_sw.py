import pandas as pd, numpy as np
df = pd.read_csv('/tmp/work/tidy.csv')
pairs = {'S06-A':'S15-A','S06-B':'S15-B','S06-C':'S15-C','S06-D':'S15-D','S06-E':'S15-E','S06-F':'S15-F','S06-G':'S15-G',
         'S06-E2_imprint':'S15-J','S06-F2_imprint':'S15-K','S15-H':'S15-I','S15-L':'S15-M','S15-N':'S15-O',
         'S09-B':'S09-C','S09-D':'S09-E','S09-F':'S09-G','S03-I':'S13-F','S03-J':'S13-G'}
def norm(g): return g.replace('Y','(Y)').replace('((Y))','(Y)') if g.endswith('Y') and not g.endswith('(Y)') else g
def weight_fate(sub):
    """per animal: last 'fresh' day and classification"""
    out=[]
    for rep, a in sub.groupby('rep'):
        a = a.sort_values('time')
        days = a.time.values; vals = a.value.values
        maxday = 14.0
        if days.max() < maxday:    # blank after some day
            out.append(('dead_blank', days.max())); continue
        # LOCF: final value repeated >=2 consecutive steps to the end
        run = 1
        for i in range(len(vals)-1,0,-1):
            if vals[i]==vals[i-1]: run+=1
            else: break
        if run>=3:
            out.append(('dead_locf', days[len(vals)-run]))
        else:
            out.append(('alive', maxday))
    return out
rows=[]
for sb, wb_ in pairs.items():
    s = df[df.block==sb]; w = df[df.block==wb_]
    for g in sorted(set(s.group)|set(w.group)):
        sg = s[s.group==g]; wg = w[w.group==g]
        if sg.empty:
            # try Y-suffix variants
            alt = [x for x in s.group.unique() if x.replace('(Y)','Y')==g.replace('(Y)','Y')]
            sg = s[s.group.isin(alt)]
        if wg.empty:
            alt = [x for x in w.group.unique() if x.replace('(Y)','Y')==g.replace('(Y)','Y')]
            wg = w[w.group.isin(alt)]
        if g.endswith('Y') and not g.endswith('(Y)') and not sg.empty and not wg.empty and g not in w.group.values: continue
        n_s = len(sg); d_s = int(sg.event.sum()) if n_s else None
        fates = weight_fate(wg) if not wg.empty else []
        n_w = len(fates); d_w = sum(f[0]!='alive' for f in fates)
        sd = sorted(sg[sg.event==1].time.tolist()) if n_s else []
        wd = sorted([f[1] for f in fates if f[0]!='alive'])
        rows.append(dict(survival_block=sb, weight_block=wb_, group=g, n_surv=n_s, deaths_surv=d_s, n_weight=n_w, deaths_weight=d_w,
                         surv_death_days=sd, weight_last_fresh_day=wd, locf_used=any(f[0]=='dead_locf' for f in fates),
                         blank_used=any(f[0]=='dead_blank' for f in fates)))
R = pd.DataFrame(rows).drop_duplicates(subset=['survival_block','group'])
R['n_match'] = R.n_surv==R.n_weight
R['deaths_match'] = R.deaths_surv==R.deaths_weight
pd.set_option('display.width',320); pd.set_option('display.max_colwidth',60)
print(R.to_string())
R.to_csv('/tmp/work/surv_weight_concordance.csv',index=False)
