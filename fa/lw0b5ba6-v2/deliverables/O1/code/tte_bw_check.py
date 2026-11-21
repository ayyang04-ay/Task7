import pandas as pd, itertools, numpy as np
T = pd.read_csv('/tmp/work/tidy/tte.csv'); B = pd.read_csv('/tmp/work/tidy/bw.csv')
def gnorm(g): return g.replace('PSLN-212Y','PSLN-212(Y)').replace('PSLN-344Y','PSLN-344(Y)')
T['group'] = T.group.map(gnorm); B['group'] = B.group.map(gnorm)
print('=== group-level identical TTE vectors across blocks (excluding all-censored arms) ===')
tv = {(b,g): tuple(sorted(zip(d.time.fillna(-1), d.event))) for (b,g), d in T.groupby(['block','group'])}
for k1,k2 in itertools.combinations(tv,2):
    if k1[0]==k2[0]: continue
    if tv[k1]==tv[k2] and sum(e for _,e in tv[k1])>0:
        print('identical arm:', k1, k2, tv[k1])

print('\n=== BW vs TTE reconciliation ===')
mapping = {'S15-A':'S06-A','S15-B':'S06-B','S15-C':'S06-C','S15-D':'S06-D','S15-E':'S06-E','S15-F':'S06-F','S15-G':'S06-G',
           'S15-I':'S15-H','S15-J':'S06-E[imprint]','S15-K':'S06-F[imprint]','S15-M':'S15-L','S15-O':'S15-N',
           'S09-C':'S09-B','S09-E':'S09-D','S09-G':'S09-F','S13-F':'S03-I','S13-G':'S03-J'}
rows=[]
for bwb, tb in mapping.items():
    bb = B[B.block==bwb]; tt = T[T.block==tb]
    for g in sorted(set(bb.group)|set(tt.group)):
        d = bb[bb.group==g]
        n_bw = d.animal.nunique()
        surv_bw = None; locf = 0; blank=0
        if n_bw:
            s=0
            for a, da in d.groupby('animal'):
                da = da.sort_values('day')
                vals = dict(zip(da.day, da.value))
                if 14 not in vals:
                    blank += 1; continue
                if vals.get(12) == vals.get(14) and vals.get(10) == vals.get(12):
                    locf += 1; continue
                s += 1
            surv_bw = s
        dt = tt[tt.group==g]
        surv_tte = int((dt.event==0).sum()) if len(dt) else None
        rows.append(dict(bw_block=bwb, tte_block=tb, group=g, n_bw=n_bw, n_tte=len(dt), surv_bw=surv_bw,
                         dead_blank=blank, dead_locf=locf, surv_tte=surv_tte,
                         match=(surv_bw==surv_tte) if (surv_bw is not None and surv_tte is not None) else 'group missing in one block'))
R = pd.DataFrame(rows); print(R.to_string())
R.to_csv('/tmp/work/bw_vs_tte.csv', index=False)
