import pandas as pd, numpy as np, warnings
from scipy import stats
warnings.filterwarnings('ignore')
pd.set_option('display.width', 320); pd.set_option('display.max_rows', 3000); pd.set_option('display.max_colwidth', 50)
Q = pd.read_csv('quant_long.csv'); Q['time']=Q['time'].astype(str)
Q['g'] = Q.group.replace({'PSLN-212Y':'PSLN-212(Y)','PSLN-212(y)':'PSLN-212(Y)','PSLN-344Y':'PSLN-344(Y)','PBS':'Sham*','Vaccine':'Sham*'})
LOG = {'S01-A','S02-F','S03-A','S03-C','S03-D','S03-E','S03-G','S03-H','S03-L','S08-A','S10-A','S13-A','S13-B','S13-C','S13-D','S13-I','S13-J','S04-B Tfh:Tfr'}
rows=[]
for (blk, an, t), d in Q.groupby(['block','analyte','time'], sort=False):
    if blk in ('S03-B','S03-F','S07-A','S07-C','S08-C','S11-B','S08-B','S08-A','S10-A'): continue   # mislabeled / ambiguous / not a PD marker
    gs = set(d.g)
    if not {'PSLN-212','PSLN-344'} <= gs: continue
    def tr(v):
        v = np.asarray(v, float)
        if blk == 'S09-A': return v
        if blk in ('S03-C','S03-G'): return np.log10(np.where(v==0, 5, v))
        return np.log10(v) if blk in LOG else v
    a = tr(d[d.g=='PSLN-212'].value); b = tr(d[d.g=='PSLN-344'].value)
    y = tr(d[d.g=='PSLN-212(Y)'].value) if 'PSLN-212(Y)' in gs else None
    s = tr(d[d.g.isin(['Sham','Sham*'])].value) if ({'Sham','Sham*'} & gs) else None
    sp = np.sqrt(((len(a)-1)*a.var(ddof=1)+(len(b)-1)*b.var(ddof=1))/(len(a)+len(b)-2))
    g = (b.mean()-a.mean())/sp * (1-3/(4*(len(a)+len(b))-9))
    islog = blk in LOG or blk=='S09-A'
    r = dict(block=blk, analyte=an, time=t, n=f"{len(a)}/{len(b)}", scale='log10' if islog else 'linear',
             P212=(10**a.mean() if islog else a.mean()), P344=(10**b.mean() if islog else b.mean()),
             Young=(np.nan if y is None else (10**y.mean() if islog else y.mean())), Sham=(np.nan if s is None else (10**s.mean() if islog else s.mean())),
             fold_344_v_212=(10**(b.mean()-a.mean()) if islog else b.mean()/a.mean()), hedges_g=g, p_welch=stats.ttest_ind(a,b,equal_var=False).pvalue,
             complete_separation=(b.min()>a.max()) or (b.max()<a.min()))
    if y is not None:
        r['P344_pct_of_young'] = 100*(10**(b.mean()-y.mean()) if islog else b.mean()/y.mean())
        r['P212_pct_of_young'] = 100*(10**(a.mean()-y.mean()) if islog else a.mean()/y.mean())
        if s is not None:
            # fraction of the young-vs-sham window recovered (on analysis scale)
            r['restoration_344'] = 100*(b.mean()-s.mean())/(y.mean()-s.mean()); r['restoration_212'] = 100*(a.mean()-s.mean())/(y.mean()-s.mean())
    rows.append(r)
B = pd.DataFrame(rows)
B.to_csv('biomarker_table.csv', index=False)
show = B.copy()
for c in ['P212','P344','Young','Sham','fold_344_v_212','hedges_g','P344_pct_of_young','P212_pct_of_young','restoration_344','restoration_212']:
    show[c] = show[c].map(lambda x: '' if pd.isna(x) else (f"{x:.0f}" if abs(x)>=100 else f"{x:.1f}" if abs(x)>=10 else f"{x:.2f}"))
show['p_welch'] = show.p_welch.map(lambda x: f"{x:.1e}")
print(show.to_string(index=False))
