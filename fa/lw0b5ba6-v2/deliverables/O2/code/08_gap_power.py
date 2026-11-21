import pandas as pd, numpy as np
from scipy import stats
from statsmodels.stats.power import TTestIndPower, NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize
G=pd.read_csv('/tmp/work/tables/age_gap_closure.csv')
C=pd.read_csv('/tmp/work/tidy/continuous.csv'); C['time']=C['time'].astype(str)
C.loc[C.block.isin(['S03-C','S03-G'])&(C.value<10),'value']=5.0
CUR=[ # (block, time, measurand-substring, stage, short label)
('S01-A','16h','Ifnb1','1 Innate sensing','Lung Ifnb1 16 h'),
('S09-A panel1 (cols B-V)','16h (as printed)','Il6','1 Innate sensing','Lung Il6 16 h*'),
('S09-A panel1 (cols B-V)','16h (as printed)','Ccl2','1 Innate sensing','Lung Ccl2 16 h*'),
('S09-A panel1 (cols B-V)','16h (as printed)','Ccl3','1 Innate sensing','Lung Ccl3 16 h*'),
('S09-A panel1 (cols B-V)','16h (as printed)','Ccl5','1 Innate sensing','Lung Ccl5 16 h*'),
('S01-D','4','monocytes','2 Myeloid recruitment','Lung Ly6C+ monocytes d4 (peak)'),
('S01-E','4','CD11b+ DC','2 Myeloid recruitment','Lung CD11b+ DC d4 (peak)'),
('S11-E','not stated','CD206','2 Myeloid recruitment','Lung CD206+ macrophages (decrease)'),
('S01-F','72h','cDC1','3 DC migration & priming','Lung cDC1 72 h'),
('S01-G','72h','cDC2','3 DC migration & priming','Lung cDC2 72 h (decrease)'),
('S02-A','72h','CCR7','3 DC migration & priming','CCR7+ migratory DC'),
('S02-B','72h','MLN CD11b','3 DC migration & priming','MLN CD11b+ DC'),
('S02-C','36h','AF647','3 DC migration & priming','Antigen+ DC in MLN'),
('S02-D CD40','d3','CD40','3 DC migration & priming','MLN DC CD40+'),
('S02-D CD86','d3','CD86','3 DC migration & priming','MLN DC CD86+'),
('S02-E','72h DC + 3d coculture','OT-I','3 DC migration & priming','DC priming of OT-I CD8'),
('S04-A','d7','ICOS-high','4 Tfh / germinal centre','Tfh ICOS-high d7'),
('S04-B Foxp3','d7','Tfr','4 Tfh / germinal centre','Tfr d7 (decrease)'),
('S04-C','d30','Tfr','4 Tfh / germinal centre','Tfr d30 (decrease)'),
('S04-D','d7','Treg','4 Tfh / germinal centre','Lung Treg d7 (decrease)'),
('S03-K','d7','GC B','4 Tfh / germinal centre','GC B cells d7'),
('S13-H','not stated','IgG+','4 Tfh / germinal centre','IgG+ B cells (MLN)'),
('S03-A','d14','IgG','5 Antibody','IgG anti-CA09 d14'),
('S03-E','d14','IgG','5 Antibody','IgG anti-Aichi d14'),
('S03-C','d14','HAI','5 Antibody','HAI anti-CA09 d14'),
('S03-G','d14','HAI','5 Antibody','HAI anti-Aichi d14'),
('S03-D','d14','Neutralising','5 Antibody','Neut anti-CA09 d14'),
('S03-H','d14','Neutralising','5 Antibody','Neut anti-Aichi d14'),
('S13-A','d14','IgG2a','5 Antibody','IgG2a anti-CA09 d14'),
('S13-C','d14','IgG2a','5 Antibody','IgG2a anti-Aichi d14'),
('S13-I','d28 (boost d14)','IgG','5 Antibody','IgG anti-CA09 d28 post-boost'),
('S13-J','d28 (boost d14)','IgG','5 Antibody','IgG anti-Aichi d28 post-boost'),
('S05-D','d3','Ki-67','6 CD8 T cells','Lung Ki-67+ CD8 d3'),
('S05-E','d3','GZMB','6 CD8 T cells','Lung GZMB+ CD8 d3'),
('S05-F','d14','IFN-g','6 CD8 T cells','IFN-g+ CD8 d14 (H5 restim)'),
('S14-A H1N1','not stated','IFN-g','6 CD8 T cells','IFN-g+ CD8 (H1 restim)'),
('S14-A H3N2','not stated','IFN-g','6 CD8 T cells','IFN-g+ CD8 (H3 restim)'),
('S05-I','d25','TRM','6 CD8 T cells','Lung TRM d25'),
('S05-G','d60','IFN-g','7 Memory (d60)','IFN-g+ CD8 d60'),
('S05-H','d60','GZMB','7 Memory (d60)','GZMB+ CD8 d60'),
]
rows=[]
for blk,t,sub,stage,lab in CUR:
    r=G[(G.block==blk)&(G.time.astype(str)==t)&(G.measurand.str.contains(sub,regex=False))]
    assert len(r)==1,(blk,t,sub,len(r))
    r=r.iloc[0]; rows.append(dict(stage=stage,readout=lab,block=blk,time=t,gap_closed=r.gap_closed,lo=r.lo,hi=r.hi,m212=r.m212,m344=r.m344,mY=r.mY,scale=r.scale))
Q=pd.DataFrame(rows); Q.to_csv('/tmp/work/tables/age_gap_curated.csv',index=False)
print(Q.round(3).to_string(index=False))
print("CURATED n=",len(Q)," median=",round(Q.gap_closed.median(),3)," IQR=",Q.gap_closed.quantile([.25,.75]).round(3).tolist(),
      " >=50%:",int((Q.gap_closed>=.5).sum()),"/",len(Q))
print(Q.groupby('stage').gap_closed.median().round(2))

# ------- power / sample size (planning) -------
print("\n=== planning variances from our data")
def sdlog(block,groups,base=2,time=None):
    d=C[(C.block==block)&C.group.isin(groups)]
    if time is not None: d=d[d.time==time]
    assert d.groupby('group').time.nunique().max()==1, 'mixed timepoints'
    f=np.log2 if base==2 else np.log10
    s=[f(dd.value).std(ddof=1) for _,dd in d.groupby('group')]
    return np.sqrt(np.mean(np.square(s)))
sd_hai=np.mean([sdlog('S03-C',['PSLN-212','PSLN-344','PSLN-212(Y)']),sdlog('S03-G',['PSLN-212','PSLN-344','PSLN-212(Y)'])])
sd_ifn=sdlog('S01-A',['PSLN-212','PSLN-344','PSLN-212(Y)'],base=2,time='16h')
sd_igg=np.mean([sdlog('S03-A',['PSLN-212','PSLN-344','PSLN-212(Y)']),sdlog('S03-E',['PSLN-212','PSLN-344','PSLN-212(Y)'])])
print(f"pooled within-group SD: log2 HAI={sd_hai:.2f}; log2 Ifnb1(16h)={sd_ifn:.2f}; log2 IgG={sd_igg:.2f}")
tp=TTestIndPower()
out=[]
# (a) Mn-only vs PSLN-344: detect 2-fold difference in Ifnb1 (log2 diff=1) and HAI (log2 diff=1), two-sided alpha .05, power .9
for name,sd in [('Ifnb1 16h, 2-fold',sd_ifn),('HAI d14, 2-fold',sd_hai),('IgG d14, 2-fold',sd_igg)]:
    n=tp.solve_power(effect_size=1/sd,alpha=0.05,power=0.9,alternative='two-sided'); out.append((name,'superiority 2-fold, 90% power, a=.05',int(np.ceil(n))))
# (b) Non-inferiority of IN PSLN-344 vs IM benchmark on HAI GMT: margin 2-fold (log2=1), true ratio 1, one-sided alpha .025, power .9
n=tp.solve_power(effect_size=1/sd_hai,alpha=0.05,power=0.9,alternative='larger'); out.append(('HAI NI vs benchmark, margin 2-fold','one-sided a=.025, 90% power, true GMR=1',int(np.ceil(n))))
# tighter margin 1.5-fold
n=tp.solve_power(effect_size=np.log2(1.5)/sd_hai,alpha=0.05,power=0.9,alternative='larger'); out.append(('HAI NI vs benchmark, margin 1.5-fold','one-sided a=.025, 90% power, true GMR=1',int(np.ceil(n))))
# (c) survival: replicate PSLN-344 vs PSLN-212 with shrunken planning values 70% vs 20%; and 80% vs 40% (vs a stronger comparator)
def fisher_power(p1,p2,n,sims=4000,rng=np.random.default_rng(1)):
    a=rng.binomial(n,p1,sims); b=rng.binomial(n,p2,sims)
    return np.mean([stats.fisher_exact([[x,n-x],[y,n-y]])[1]<0.05 for x,y in zip(a,b)])
for p1,p2 in [(0.70,0.20),(0.80,0.40),(0.67,0.95)]:
    for n in range(6,61):
        if fisher_power(p1,p2,n)>=0.9: out.append((f'survival {int(p1*100)}% vs {int(p2*100)}%','Fisher two-sided a=.05, 90% power (simulated)',n)); break
P=pd.DataFrame(out,columns=['comparison','assumptions','n_per_arm']); print(P.to_string(index=False))
P.to_csv('/tmp/work/tables/sample_size_planning.csv',index=False)
pd.DataFrame([dict(sd_log2_HAI=sd_hai,sd_log2_Ifnb1_16h=sd_ifn,sd_log2_IgG=sd_igg)]).to_csv('/tmp/work/tables/planning_variances.csv',index=False)
