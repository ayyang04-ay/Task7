import pandas as pd, numpy as np, warnings
from scipy import stats
warnings.filterwarnings('ignore')
vals = pd.read_csv('values_corrected.csv'); surv = pd.read_csv('survival.csv')
surv.loc[(surv.block=='S03-J') & surv.day.isna(), 'day'] = 21
pd.set_option('display.width',250)
# CMP-204 (cGAMP) vs PSLN-212 (CDN-1807) - same vehicle, different agonist
print('CMP-204 (cGAMP liposome) vs PSLN-212 (CDN-1807 liposome) and PSLN-344:')
for blk,log in [('S01-A_16h',True),('S03-A',True),('S03-E',True),('S03-C',True),('S03-G',True),('S03-D',True),('S03-H',True),('S13-I',True),('S13-J',True)]:
    d = vals[vals.block==blk]
    gmf = lambda g: 10**np.log10(d[d.g==g].value).mean()
    a = np.log10(d[d.g=='CMP-204'].value); b = np.log10(d[d.g=='PSLN-212'].value)
    print(f"  {blk:10s} CMP-204 GM={gmf('CMP-204'):8.1f}  PSLN-212 GM={gmf('PSLN-212'):8.1f}  PSLN-344 GM={gmf('PSLN-344'):8.1f}   CMP/212 ratio={10**(a.mean()-b.mean()):.2f} p={stats.ttest_ind(a,b,equal_var=False)[1]:.3f}")
# R848 combos
d = vals[vals.block=='S01-A_16h']
for g in ['PSLN-R848','PSLN-212/R848','PSLN-212','PSLN-344']:
    print(f"  S01-A 16h Ifnb1 {g:15s} GM={10**np.log10(d[d.g==g].value).mean():.1f}")
# ---- bootstrap CIs for restoration indices ----
rng = np.random.default_rng(7)
def ri_boot(block, log, time=None, B=4000):
    d = vals[vals.block==block]
    if time is not None: d = d[d.time.astype(str)==str(time)]
    y = lambda g: (np.log10(d[d.g==g].value.values) if log else d[d.g==g].value.values)
    a,b,c = y('PSLN-344'), y('PSLN-212'), y('PSLN-212(Y)')
    est = (a.mean()-b.mean())/(c.mean()-b.mean())
    bs=[]
    for _ in range(B):
        aa,bb,cc = rng.choice(a,len(a)), rng.choice(b,len(b)), rng.choice(c,len(c))
        den = cc.mean()-bb.mean()
        if abs(den)>1e-9: bs.append((aa.mean()-bb.mean())/den)
    lo,hi = np.percentile(bs,[2.5,97.5]); return est,lo,hi
# survival RI bootstrap (resample animals within experiment x arm)
exps = ['S03-I','S06-A','S06-B','S06-C','S06-E','S06-F','S06-G','S15-L','S15-N']
def surv_ri(sample=False):
    tot = {}
    for g in ['PSLN-344','PSLN-212','PSLN-212(Y)']:
        s=n=0
        for b in exps:
            e = surv[(surv.block==b)&(surv.group==g)].event.values
            if sample: e = rng.choice(e,len(e))
            s += (e==0).sum(); n += len(e)
        tot[g]=s/n
    den = tot['PSLN-212(Y)']-tot['PSLN-212']
    return (tot['PSLN-344']-tot['PSLN-212'])/den if den>0 else np.nan
est = surv_ri(); bs = [surv_ri(True) for _ in range(4000)]; bs=[x for x in bs if x==x]
print(f"\nSurvival restoration index = {est:.2f} (bootstrap 95% CI {np.percentile(bs,2.5):.2f}-{np.percentile(bs,97.5):.2f})")
rows=[('Survival (9 aged challenge expts)', est, np.percentile(bs,2.5), np.percentile(bs,97.5), 'S03-I,S06-A/B/C/E/F/G,S15-L/N')]
for lab,blk,log,t in [('Lung Ifnb1 16 h','S01-A_16h',True,None),('Lung monocytes d4','S01-D',False,4),('Lung CD11b+ DC d4','S01-E',False,4),('cDC1','S01-F',False,None),
                      ('CCR7+ migratory DC','S02-A',False,None),('MLN CD11b+ DC','S02-B',False,None),('Antigen+ DC in MLN','S02-C',False,None),('CD40 on MLN DC','S02-D_CD40',False,None),
                      ('CD86 on MLN DC','S02-D_CD86',False,None),('OT-I priming','S02-E',False,None),('GC B cells','S03-K',False,None),('ICOS-hi Tfh','S04-A_ICOShi',False,None),
                      ('Tfr d7 (inverse)','S04-B_Foxp3',False,None),('Lung Treg (inverse)','S04-D',False,None),('IgG CA09','S03-A',True,None),('IgG Aichi','S03-E',True,None),
                      ('HAI CA09','S03-C',True,None),('HAI Aichi','S03-G',True,None),('NT CA09','S03-D',True,None),('NT Aichi','S03-H',True,None),
                      ('IgG2a:IgG1 CA09 (corrected)','S03-B',True,None),('Ki-67+ CD8 d3','S05-D',False,None),('GZMB+ CD8 d3','S05-E',False,None),
                      ('IFNg+ CD8 H5N1 recall d14','S05-F',False,None),('IFNg+ CD8 H5N1 recall d60','S05-G',False,None),('Lung TRM d25','S05-I',False,None),
                      ('IFNg+ CD8 H1N1 recall','S14-A_H1N1',False,None),('IFNg+ CD8 H3N2 recall','S14-A_H3N2',False,None),('CD206+ macrophages (inverse)','S11-E',False,None)]:
    e,lo,hi = ri_boot(blk,log,t); rows.append((lab,e,lo,hi,blk))
ri = pd.DataFrame(rows, columns=['readout','restoration_index','ci_lo','ci_hi','source'])
print(ri.round(2).to_string()); ri.round(3).to_csv('/tmp/outputs/analysis/T11_restoration_index.csv', index=False)
