import pandas as pd, numpy as np, warnings
warnings.filterwarnings('ignore')
from scipy import stats
rng = np.random.default_rng(7)
df = pd.read_csv('/tmp/work/tidy.csv')
S = pd.read_csv('/tmp/work/summary_stats.csv')
# ---------- (a) Hedges g PSLN-344 vs PSLN-212 (aged) per readout, on analysis scale
LOG = set(S[S.scale=='log10'].block)
EXCL = {'S11-A','S11-B','S03-B','S03-F','S05-A','S05-B','S07-C','S09-A_panel2_X-AS','S04-B_TfhTfr'}   # integrity tier C / relabel
rows=[]
x = df[df.event.isna() & (df.unit!='% of d0')]
for (b,t,a),sub in x.assign(tk=x.time.fillna(-1), an=x.analyte.fillna('')).groupby(['block','tk','an']):
    if b in EXCL: continue
    g = set(sub.group)
    if not {'PSLN-212','PSLN-344'} <= g: continue
    v1 = sub[sub.group=='PSLN-344'].value.values; v0 = sub[sub.group=='PSLN-212'].value.values
    if b in LOG: v1,v0 = np.log10(np.clip(v1,5,None) if b in ('S03-C','S03-G') else v1), np.log10(np.clip(v0,5,None) if b in ('S03-C','S03-G') else v0)
    n1,n0=len(v1),len(v0)
    sp = np.sqrt(((n1-1)*v1.var(ddof=1)+(n0-1)*v0.var(ddof=1))/(n1+n0-2))
    gg = (v1.mean()-v0.mean())/sp*(1-3/(4*(n1+n0)-9))
    rows.append(dict(block=b, time=(None if t==-1 else t), analyte=a, measurand=sub.measurand.iloc[0], n=f'{n1}/{n0}', hedges_g=gg))
H = pd.DataFrame(rows).sort_values('hedges_g', key=lambda s: -s.abs())
print(H.head(30).round(2).to_string())
H.to_csv('/tmp/work/hedges_g.csv', index=False)
# ---------- (b) stratified bootstrap CI for pooled survival risk difference
s = df[df.event.notna() & (df.block!='S08-UNLABELLED')]
def boot_rd(blocks, g1, g2, B=20000):
    data = {b:(s[(s.block==b)&(s.group==g1)].event.values, s[(s.block==b)&(s.group==g2)].event.values) for b in blocks}
    def rd(d):
        num=den=0
        for e1,e2 in d.values():
            n1,n2=len(e1),len(e2); N=n1+n2
            num += ((1-e1).sum()*n2 - (1-e2).sum()*n1)/N; den += n1*n2/N
        return num/den
    est = rd(data); bs=[]
    for _ in range(B):
        d = {b:(rng.choice(e1,len(e1)), rng.choice(e2,len(e2))) for b,(e1,e2) in data.items()}
        bs.append(rd(d))
    return est, np.percentile(bs,[2.5,97.5])
allb = ['S06-A','S06-B','S06-C','S06-D','S06-E','S06-F','S06-G','S15-L','S15-N']
clean = ['S06-A','S06-B','S06-E','S06-F']
for bl,lab in [(allb,'all 9'),(clean,'clean 4')]:
    for g1,g2 in [('PSLN-344','PSLN-212'),('PSLN-344','Sham'),('PSLN-344','PSLN-212(Y)')]:
        e,(lo,hi) = boot_rd(bl,g1,g2)
        print(f'MH risk difference {lab}: {g1} vs {g2}: {100*e:.1f} pct-pts (95% bootstrap CI {100*lo:.1f} to {100*hi:.1f})')
# ---------- (c) durability: PSLN-344 survival by challenge timing
t = {'d3':['S06-B','S06-D'],'d14':['S06-A','S06-C'],'d60':['S06-E','S06-F','S06-G']}
cnt = {k:( int((s[(s.block.isin(v))&(s.group=='PSLN-344')].event==0).sum()), int(len(s[(s.block.isin(v))&(s.group=='PSLN-344')])) ) for k,v in t.items()}
print('PSLN-344 survival by timing', cnt)
print('d14 vs d60 Fisher p:', stats.fisher_exact([[cnt['d14'][0],cnt['d14'][1]-cnt['d14'][0]],[cnt['d60'][0],cnt['d60'][1]-cnt['d60'][0]]])[1])
cy = {k:( int((s[(s.block.isin(v))&(s.group=='PSLN-212(Y)')].event==0).sum()), int(len(s[(s.block.isin(v))&(s.group=='PSLN-212(Y)')])) ) for k,v in t.items()}
print('PSLN-212(Y) by timing', cy)
# ---------- (d) power for replication study (Fisher exact, two-sided alpha 0.05)
def power(p1,p2,n,sims=4000):
    hits=0
    for _ in range(sims):
        a=rng.binomial(n,p1); b=rng.binomial(n,p2)
        if stats.fisher_exact([[a,n-a],[b,n-b]])[1]<0.05: hits+=1
    return hits/sims
print('\nPower (Fisher, alpha=0.05) PSLN-344 vs PSLN-212 under observed and conservative effects:')
for p1,p2,lab in [(0.81,0.13,'pooled observed (51/63 vs 8/63)'),(0.75,0.07,'clean-blocks observed (21/28 vs 2/28)'),(0.60,0.20,'conservative (halved gap)'),(0.67,0.05,'d60 durability observed')]:
    res = {n: power(p1,p2,n) for n in [7,10,12,15,20,25]}
    print(lab, {k:round(v,2) for k,v in res.items()})
