import pandas as pd, numpy as np
rng = np.random.default_rng(20261101)
V = pd.read_csv('/tmp/work/tidy/values.csv'); V['time']=V.time.fillna('')
H = pd.read_csv('/tmp/work/h2h.csv'); H = H[H.excluded.isna() & H.restoration_index.notna()]
LAYER = {
 ('S01-A','16h'):'1 Innate cytokine (16-36h)', ('S09-A panel1[A:U]','Ccl2'):'1 Innate cytokine (16-36h)',('S09-A panel1[A:U]','Ccl3'):'1 Innate cytokine (16-36h)',
 ('S09-A panel1[A:U]','Ccl5'):'1 Innate cytokine (16-36h)',('S09-A panel1[A:U]','Il6'):'1 Innate cytokine (16-36h)',
 ('S01-D','d4'):'2 Myeloid recruitment & DC (d3-4)',('S01-E','d4'):'2 Myeloid recruitment & DC (d3-4)',('S01-F','72h'):'2 Myeloid recruitment & DC (d3-4)',
 ('S01-G','72h'):'2 Myeloid recruitment & DC (d3-4)',('S02-A','72h'):'2 Myeloid recruitment & DC (d3-4)',('S02-B','72h'):'2 Myeloid recruitment & DC (d3-4)',
 ('S02-C','36h'):'2 Myeloid recruitment & DC (d3-4)',
 ('S02-D CD40','d3'):'3 DC co-stimulation (d3)',('S02-D CD86','d3'):'3 DC co-stimulation (d3)',
 ('S02-E','72h+3d'):'4 CD8 priming/effector (d3)',('S05-D','d3'):'4 CD8 priming/effector (d3)',('S05-E','d3'):'4 CD8 priming/effector (d3)',
 ('S04-A','Tfh ICOS-hi'):'5 Tfh/GC/regulation (d7)',('S04-A','Tfh ICOS-lo'):'5 Tfh/GC/regulation (d7)',('S03-K','d7'):'5 Tfh/GC/regulation (d7)',
 ('S04-B Foxp3','d7'):'5 Tfh/GC/regulation (d7)',('S04-D','d7'):'5 Tfh/GC/regulation (d7)',('S13-H',''):'5 Tfh/GC/regulation (d7)',
 ('S03-A','d14'):'6 Antibody (d14)',('S03-C','d14'):'6 Antibody (d14)',('S03-D','d14'):'6 Antibody (d14)',('S03-E','d14'):'6 Antibody (d14)',
 ('S03-G','d14'):'6 Antibody (d14)',('S03-H','d14'):'6 Antibody (d14)',('S13-A','d14'):'6 Antibody (d14)',('S13-B','d14'):'6 Antibody (d14)',
 ('S13-C','d14'):'6 Antibody (d14)',('S13-D','d14'):'6 Antibody (d14)',
 ('S13-I','d28'):'7 Antibody post-boost (d28)',('S13-J','d28'):'7 Antibody post-boost (d28)',
 ('S05-F','d14'):'8 CD8 memory (d14-60)',('S05-G','d60'):'8 CD8 memory (d14-60)',('S05-H','d60'):'8 CD8 memory (d14-60)',('S05-I','d25'):'8 CD8 memory (d14-60)',
 ('S14-A H1N1',''):'8 CD8 memory (d14-60)',('S14-A H3N2',''):'8 CD8 memory (d14-60)',('S04-C','d30'):'5 Tfh/GC/regulation (d7)',
}
def layer(r):
    for (b,k),L in LAYER.items():
        if r.block==b and (k in (r.time if isinstance(r.time,str) else '') or k in r.analyte or (k=='' )): return L
    return None
LOGK = ('IgG','HAI','Neut','Ifnb1','post-boost')
def tr(blk,an,x):
    if blk.startswith('S09-A'): return x
    if any(k in an for k in LOGK): return np.log2(np.where(x<=0,5,x))
    return x
rows=[]
for _,r in H.iterrows():
    L = layer(r)
    if L is None: continue
    t = r.time if isinstance(r.time,str) else ''
    d = V[(V.block==r.block)&(V.analyte==r.analyte)&(V.time==t)]
    a = tr(r.block,r.analyte,d[d.group=='PSLN-344'].value.values); b = tr(r.block,r.analyte,d[d.group=='PSLN-212'].value.values)
    y = tr(r.block,r.analyte,d[d.group=='PSLN-212(Y)'].value.values)
    bs=[]
    for _ in range(4000):
        aa,bb,yy = rng.choice(a,len(a)),rng.choice(b,len(b)),rng.choice(y,len(y))
        gap = yy.mean()-bb.mean()
        if abs(gap)>1e-9: bs.append((aa.mean()-bb.mean())/gap)
    lo,hi = np.percentile(bs,[2.5,97.5])
    rows.append(dict(layer=L, block=r.block, analyte=r.analyte, time=t, RI=r.restoration_index, RI_lo=lo, RI_hi=hi, p_344_vs_Y=r.p_344_vs_Y))
R = pd.DataFrame(rows).sort_values(['layer','block'])
R.to_csv('/tmp/work/restoration_index.csv', index=False)
pd.set_option('display.width',200)
print(R.round(2).to_string(index=False))
print()
S = R.groupby('layer').RI.agg(['count','median','min','max']).round(2); print(S)
S.to_csv('/tmp/work/restoration_by_layer.csv')
