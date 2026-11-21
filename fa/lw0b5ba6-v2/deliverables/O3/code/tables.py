from loadcsv import *
import numpy as np, pandas as pd, re
def ci(s):
    n=0
    for ch in s: n=n*26+(ord(ch)-64)
    return n
def gl(n):
    s=''
    while n: n,r=divmod(n-1,26); s=chr(65+r)+s
    return s
def rng(block, group, filt=None):
    d=DF[(DF.block==block)&(DF.group==group)]
    if filt:
        for k,v in filt.items(): d=d[d[k].astype(str)==str(v)]
    cells=d.cell.str.split('!').str[1]; sheet=d.cell.iloc[0].split('!')[0]
    cols=cells.str.extract(r'([A-Z]+)')[0].map(ci); rows=cells.str.extract(r'(\d+)')[0].astype(int)
    return f"{sheet}!{gl(cols.min())}{rows.min()}:{gl(cols.max())}{rows.max()}"
H=pd.read_csv('/tmp/work/h2h_344_vs_212.csv')
FILT={'Lung Gm-csf 16h (fold)':{'hour':'16h'},'Lung Gm-csf 36h (fold)':{'hour':'36h'},'Lung Gm-csf 72h (fold)':{'hour':'72h'},
      'Lung monocytes d4 (%)':{'day':'4'},'Lung CD11b+ DC d4 (%)':{'day':'4'}}
out=[]
for _,r in H.iterrows():
    f=FILT.get(r.readout)
    try:
        c212=rng(r.block,'PSLN-212',f); c344=rng(r.block,'PSLN-344',f)
    except Exception as e:
        c212=c344=''
    gy = 'PSLN-212(Y)' if r.block!='S05-A' else 'PSLN-212Y'
    try: cy=rng(r.block,gy,f)
    except: cy=''
    out.append(dict(domain=r.domain,readout=r.readout,block=r.block,integrity_tier=r.tier,scale=r.scale,
        sham=r.sham,aged_PSLN212=r.aged_212,aged_PSLN344=r.aged_344,young_PSLN212=r.young_212,
        effect_344_vs_212_95CI=r.effect_344_vs_212,hedges_g=r.hedges_g,p_welch=r.p_welch,p_mannwhitney_exact=r.p_mw_exact,
        p_tukey=r.p_tukey,p_holm=r.p_holm_welch,q_BH=r.q_BH_welch,restoration_pct_of_young=r.restoration_pct,
        cells_PSLN212=c212,cells_PSLN344=c344,cells_young=cy))
T=pd.DataFrame(out); T.to_csv('/tmp/outputs/tables/T1_head_to_head_PSLN344_vs_PSLN212_aged.csv',index=False)
print(T[['readout','cells_PSLN212','cells_PSLN344']].head(8).to_string())
# survival table with cells
S=pd.read_csv('/tmp/work/survival_by_study.csv')
def srng(b,g):
    d=SV[(SV.block==b)&(SV.group==g)]
    c=d.cell.str.split('!').str[1].str.split('/').str[1]; sheet=d.cell.iloc[0].split('!')[0]
    rows=c.str.extract(r'(\d+)')[0].astype(int); col=c.str.extract(r'([A-Z]+)')[0].iloc[0]
    return f"{sheet}!{col}{rows.min()}:{col}{rows.max()}"
S['cells_PSLN212']=[srng(b,'PSLN-212') for b in S.study]; S['cells_PSLN344']=[srng(b,'PSLN-344') for b in S.study]
S=S.rename(columns={'sham':'sham_deaths','aged_212':'PSLN212_deaths','aged_344':'PSLN344_deaths','young_212':'young212_deaths','tier':'integrity_tier','flag':'integrity_note'})
S.to_csv('/tmp/outputs/tables/T2_survival_by_study_aged.csv',index=False)
P=pd.read_csv('/tmp/work/survival_pooled.csv'); P.to_csv('/tmp/outputs/tables/T3_survival_pooled.csv',index=False)
pd.read_csv('/tmp/work/s09a_panel.csv').to_csv('/tmp/outputs/tables/T4_lung_cytokine_chemokine_panel_16h_S09A.csv',index=False)
print(S[['study','cells_PSLN212','cells_PSLN344']].to_string())
