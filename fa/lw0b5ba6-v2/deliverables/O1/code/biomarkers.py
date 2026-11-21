import pandas as pd, numpy as np
from scipy import stats
V = pd.read_csv('/tmp/work/tidy/values.csv'); V['time']=V.time.fillna('')
T = pd.read_csv('/tmp/work/tidy/tte.csv')
def vals(blk, grp, an=None, t=None):
    d = V[(V.block==blk)&(V.group==grp)]
    if an: d=d[d.analyte==an]
    if t is not None: d=d[d.time==t]
    return d.sort_values('animal').value.values
cands = [ # (tier, marker, block, analyte, time, human analogue / matrix)
 ('T1 PD (16-36 h)','Ifnb1 (lung)','S01-A','Ifnb1','16h','IFN-beta / ISG score (blood); CXCL10, IFN-lambda in nasal lining fluid'),
 ('T1 PD (16-36 h)','Ccl2 (lung)','S09-A panel1[A:U]','Ccl2','16h (as printed)','CCL2/MCP-1 in nasal lining fluid & serum'),
 ('T1 PD (16-36 h)','Il6 (lung)','S09-A panel1[A:U]','Il6','16h (as printed)','IL-6 (nasal, serum) - also reactogenicity marker'),
 ('T1 PD (16-36 h)','Gm-csf (lung, 36 h)','S02-F','Gm-csf (lung)','36h','GM-CSF in nasal lining fluid'),
 ('T1 PD (16-36 h)','Tnf (lung, 72 h) [safety]','S09-A panel2[X:AS]','Tnf','16h (as printed)','TNF/IL-10 persistence = reactogenicity flag'),
 ('T2 cellular (d3-7)','Lung monocytes d4','S01-D','Lung monocytes','d4','nasal brush/curettage myeloid cells (research only)'),
 ('T2 cellular (d3-7)','CCR7+ migratory DC 72 h','S02-A','CCR7+ migratory CD11b+ DC (lung)','72h','not accessible; mechanistic only'),
 ('T2 cellular (d3-7)','ICOS-hi Tfh d7 (MLN)','S04-A','Tfh ICOS-hi','d7','circulating Tfh (ICOS+PD-1+CXCR5+CXCR3+) d7 blood'),
 ('T2 cellular (d3-7)','Tfr d7 (MLN)','S04-B Foxp3','Tfr (Foxp3+ of CXCR5+ICOShi)','d7','circulating Tfr / cTfh:cTfr ratio d7 blood'),
 ('T2 cellular (d3-7)','GC B cells d7 (MLN)','S03-K','MLN GC B cells','d7','plasmablasts d7 blood (surrogate)'),
 ('T2 cellular (d3-7)','Ki-67+ CD8 lung d3','S05-D','Lung Ki-67+ CD8','d3','activated CD38+HLA-DR+ CD8 d7-10 blood'),
 ('T3 efficacy surrogate (d14-28)','HAI CA09 d14','S03-C','HAI CA09 H1N1','d14','HAI GMT, seroconversion, % >= threshold'),
 ('T3 efficacy surrogate (d14-28)','HAI Aichi d14','S03-G','HAI Aichi H3N2','d14','HAI GMT'),
 ('T3 efficacy surrogate (d14-28)','Neut CA09 d14','S03-D','Neut CA09 H1N1','d14','microneutralisation GMT'),
 ('T3 efficacy surrogate (d14-28)','IgG2a CA09 d14 (Th1)','S13-A','IgG2a CA09 H1N1','d14','IgG subclass (IgG1/IgG3) + Th1 cytokines'),
 ('T3 efficacy surrogate (d14-28)','IFNg+ CD8 d14 (rgH5N1 restim)','S05-F','MLN IFNg+ CD8 (rgH5N1 restim)','d14','IFN-gamma ELISpot, conserved NP/M1 peptides'),
 ('T4 durability (d25-60)','Lung TRM CD8 d25','S05-I','Lung TRM CD8','d25','nasal TRM (CD69+CD103+) by nasal brushing'),
 ('T4 durability (d25-60)','IFNg+ CD8 d60','S05-G','MLN IFNg+ CD8 (rgH5N1 restim)','d60','IFN-gamma ELISpot month 3-6'),
 ('T4 durability (d25-60)','GZMB+ CD8 d60','S05-H','MLN GZMB+ CD8','d60','granzyme B+ CD8 (blood)'),
]
LOGK=('IgG','HAI','Neut','Ifnb1','Gm-csf')
rows=[]
for tier,mk,blk,an,t,hum in cands:
    a,b = vals(blk,'PSLN-344',an,t), vals(blk,'PSLN-212',an,t)
    y = vals(blk,'PSLN-212(Y)',an,t); s = vals(blk,'Sham',an,t)
    if len(s)==0: s = vals(blk,'PBS',an,t)
    U = stats.mannwhitneyu(a,b,alternative='two-sided').statistic; auc = U/(len(a)*len(b))
    sep = (a.min()>b.max()) or (a.max()<b.min())
    lg = any(k in an for k in LOGK) and not blk.startswith('S09')
    f = (lambda v: 2**np.mean(np.log2(np.where(v<=0,5,v)))) if lg else ((lambda v: 10**np.mean(v)) if blk.startswith('S09') else np.mean)
    rows.append(dict(tier=tier, marker=mk, source=f'{blk} ({t})', n=f'{len(a)}v{len(b)}', sham=f(s) if len(s) else np.nan, PSLN212=f(b), PSLN344=f(a),
                     young212=f(y) if len(y) else np.nan, AUC_344_vs_212=max(auc,1-auc), complete_separation=sep, human_analogue=hum))
Bm = pd.DataFrame(rows); Bm.to_csv('/tmp/work/biomarker_table.csv', index=False)
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',60)
print(Bm.round(2).to_string(index=False))

print('\n=== HAI threshold vs survival (group level, homologous CA09: S03-C titres, S03-I survival; different animals) ===')
groups=['Sham','CMP-204','PSLN-212','PSLN-344','PSLN-212(Y)']
for g in groups:
    h = vals('S03-C',g,'HAI CA09 H1N1','d14'); hh=np.where(h<=0,5,h)
    d = T[(T.block=='S03-I')&(T.group==g)]
    print(f"{g:12s} HAI={list(h.astype(int))} GMT={2**np.mean(np.log2(hh)):.0f} >=40:{(h>=40).sum()}/5 >=160:{(h>=160).sum()}/5 | survival {int((d.event==0).sum())}/{len(d)}")
print('\n=== T-cell markers vs heterosubtypic survival (group level) ===')
for g in ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']:
    d14 = T[T.block.isin(['S06-A','S06-C'])&(T.group==g)]; d60 = T[T.block.isin(['S06-E','S06-F','S06-G'])&(T.group==g)]
    print(f"{g:12s} TRM d25={vals('S05-I',g).mean():.2f} IFNg d14={vals('S05-F',g).mean():.2f} IFNg d60={vals('S05-G',g).mean():.2f} | "
          f"hetero surv d14 (S06-A,C) {int((d14.event==0).sum())}/{len(d14)}; d60 (S06-E,F,G) {int((d60.event==0).sum())}/{len(d60)}")
# durability test: matched designs d14 vs d60 for PSLN-344
a = T[T.block.isin(['S06-A','S06-C'])&(T.group=='PSLN-344')]; b = T[T.block.isin(['S06-E','S06-F'])&(T.group=='PSLN-344')]
sa, sb = int((a.event==0).sum()), int((b.event==0).sum())
print('PSLN-344 matched designs d14 (S06-A,C) vs d60 (S06-E,F):', f'{sa}/{len(a)} vs {sb}/{len(b)}', 'Fisher p =', round(stats.fisher_exact([[sa,len(a)-sa],[sb,len(b)-sb]])[1],3))
