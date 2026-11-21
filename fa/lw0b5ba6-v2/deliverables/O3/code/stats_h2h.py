from load import *
import numpy as np, pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multitest import multipletests
import warnings; warnings.filterwarnings('ignore')

# (block, label, scale, time filter dict, group names for sham/212/344/Y, integrity tier, domain)
# tier: A = no integrity flag; B = flagged but corrected/resolvable via cross-reference; C = unreliable (excluded from primary)
SPEC = [
 # ---- innate activation ----
 ('S01-A_16h','Lung Ifnb1 16h (fold)','log',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Innate'),
 ('S01-A_72h','Lung Ifnb1 72h (fold)','log',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Innate'),
 ('S02-F','Lung Gm-csf 16h (fold)','log',{'hour':'16h'},'Sham','PSLN-212','PSLN-344',None,'A','Innate'),
 ('S02-F','Lung Gm-csf 36h (fold)','log',{'hour':'36h'},'Sham','PSLN-212','PSLN-344',None,'A','Innate'),
 ('S02-F','Lung Gm-csf 72h (fold)','log',{'hour':'72h'},'Sham','PSLN-212','PSLN-344',None,'A','Innate'),
 # ---- myeloid / DC ----
 ('S01-D','Lung monocytes d4 (%)','lin',{'day':'4'},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Myeloid/DC'),
 ('S01-E','Lung CD11b+ DC d4 (%)','lin',{'day':'4'},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Myeloid/DC'),
 ('S01-F','Lung cDC1 72h (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Myeloid/DC'),
 ('S02-A','Lung CCR7+ migratory DC 72h (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Myeloid/DC'),
 ('S02-B','MLN CD11b+CD103- DC 72h (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Myeloid/DC'),
 ('S02-C','MLN antigen+ (OVA-AF647) DC 36h (%)','lin',{},None,'PSLN-212','PSLN-344','PSLN-212(Y)','A','Myeloid/DC'),
 ('S02-D_CD40','MLN DC CD40+ d3 (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Myeloid/DC'),
 ('S02-D_CD86','MLN DC CD86+ d3 (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Myeloid/DC'),
 ('S02-E','DC->OT-I proliferation ex vivo (%)','lin',{},None,'PSLN-212','PSLN-344','PSLN-212(Y)','A','Myeloid/DC'),
 ('S11-E','Lung CD206+ macrophages (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Myeloid/DC'),
 # ---- Tfh / GC / B ----
 ('S04-A_ICOShi','MLN Tfh ICOS-hi d7 (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Tfh/GC'),
 ('S04-B_Tfr','MLN Tfr Foxp3+ d7 (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Tfh/GC'),
 ('S04-C','MLN Tfr d30 (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Tfh/GC'),
 ('S04-D','Lung Treg d7 (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Tfh/GC'),
 ('S03-K','MLN GC B cells d7 (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Tfh/GC'),
 ('S03-L_Aicda','MLN B Aicda d5 (fold)','log',{},'Sham','PSLN-212','PSLN-344',None,'A','Tfh/GC'),
 ('S03-L_E47','MLN B E47 d5 (fold)','log',{},'Sham','PSLN-212','PSLN-344',None,'A','Tfh/GC'),
 ('S13-H','MLN IgG+ B220+ (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Tfh/GC'),
 # ---- humoral ----
 ('S03-A','Serum IgG CA09 d14 (titre)','log',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Humoral'),
 ('S03-E','Serum IgG Aichi d14 (titre)','log',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Humoral'),
 ('S03-C','HAI CA09 d14 (titre)','loghai',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Humoral'),
 ('S03-G','HAI Aichi d14 (titre)','loghai',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Humoral'),
 ('S03-D','Neutralising CA09 d14 (titre)','log',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Humoral'),
 ('S03-H','Neutralising Aichi d14 (titre)','log',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Humoral'),
 ('S13-A','IgG2a CA09 d14 (titre)','log',{},None,'PSLN-212','PSLN-344','PSLN-212(Y)','A','Humoral'),
 ('S13-C','IgG2a Aichi d14 (titre)','log',{},None,'PSLN-212','PSLN-344','PSLN-212(Y)','A','Humoral'),
 ('S13-B','IgG1 CA09 d14 (titre)','log',{},None,'PSLN-212','PSLN-344','PSLN-212(Y)','A','Humoral'),
 ('S13-D','IgG1 Aichi d14 (titre)','log',{},None,'PSLN-212','PSLN-344','PSLN-212(Y)','A','Humoral'),
 ('S13-I','Serum IgG CA09 d28 post-boost (titre)','log',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Humoral'),
 ('S13-J','Serum IgG Aichi d28 post-boost (titre)','log',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','Humoral'),
 # ---- CD8 T cell ----
 ('S05-D','Lung Ki-67+ CD8 d3 (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','CD8 T cell'),
 ('S05-E','Lung GZMB+ CD8 d3 (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','CD8 T cell'),
 ('S05-F','MLN IFNg+ CD8 d14, H5 restim (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','CD8 T cell'),
 ('S05-G','MLN IFNg+ CD8 d60, H5 restim (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','CD8 T cell'),
 ('S05-H','MLN GZMB+ CD8 d60 (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','CD8 T cell'),
 ('S05-I','Lung CD8 TRM d25 (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','CD8 T cell'),
 ('S14-A_H1N1','MLN IFNg+ CD8, CA09 restim (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','CD8 T cell'),
 ('S14-A_H3N2','MLN IFNg+ CD8, Aichi restim (%)','lin',{},'Sham','PSLN-212','PSLN-344','PSLN-212(Y)','A','CD8 T cell'),
 # ---- flagged (tier C) shown for completeness ----
 ('S11-A','Lung alveolar macrophages d4 (%) [S11-A/B duplication]','lin',{'day':4},'Vaccine','PSLN-212','PSLN-344','PSLN-212(Y)','C','Myeloid/DC'),
 ('S11-B','Lung neutrophils d4 (%) [S11-A/B duplication]','lin',{'day':4},'Vaccine','PSLN-212','PSLN-344','PSLN-212(Y)','C','Myeloid/DC'),
 ('S05-A','Lung NP366 tet+ CD8 d7 (%) [n=2; H-2Db tetramer]','lin',{'day':7},None,'PSLN-212','PSLN-344','PSLN-212Y','C','CD8 T cell'),
]

def get(block, group, filt):
    d = DF[(DF.block==block)&(DF.group==group)]
    for k,x in filt.items():
        d = d[d[k].astype(str)==str(x)]
    return d.value.values.astype(float), d.cell.tolist()

def tr(x, scale):
    if scale=='log': return np.log2(x)
    if scale=='loghai': return np.log2(np.where(x<10,5,x))   # <1:10 -> 5 (half LOD)
    return x

rows=[]
for blk,label,scale,filt,gS,g2,g4,gY,tier,dom in SPEC:
    x2,c2 = get(blk,g2,filt); x4,c4 = get(blk,g4,filt)
    t2, t4 = tr(x2,scale), tr(x4,scale)
    # Welch on transformed scale
    tt = stats.ttest_ind(t4,t2,equal_var=False)
    dfw = tt.df
    diff = t4.mean()-t2.mean()
    se = np.sqrt(t4.var(ddof=1)/len(t4)+t2.var(ddof=1)/len(t2))
    q = stats.t.ppf(0.975,dfw)
    lo,hi = diff-q*se, diff+q*se
    mw = stats.mannwhitneyu(x4,x2,alternative='two-sided',method='exact')
    # Tukey across all available groups (stated method)
    groups=[g for g in [gS,g2,g4,gY] if g]
    allv=[];alll=[]
    for g in groups:
        xv,_=get(blk,g,filt); allv+=list(tr(xv,scale)); alll+=[g]*len(xv)
    tk = pairwise_tukeyhsd(np.array(allv),np.array(alll))
    tkdf = pd.DataFrame(tk._results_table.data[1:],columns=tk._results_table.data[0])
    sel = tkdf[((tkdf.group1==g2)&(tkdf.group2==g4))|((tkdf.group1==g4)&(tkdf.group2==g2))]
    p_tukey = float(sel['p-adj'].iloc[0])
    # effect expression
    if scale in ('log','loghai'):
        eff = f"{2**diff:.1f}x ({2**lo:.1f}-{2**hi:.1f})"
        m2 = f"{2**t2.mean():.3g}"; m4=f"{2**t4.mean():.3g}"
    else:
        eff = f"{diff:+.2f} pts ({lo:+.2f} to {hi:+.2f})"
        m2=f"{t2.mean():.3g}"; m4=f"{t4.mean():.3g}"
    # restoration index vs young, on transformed scale
    ri = np.nan; mS=mY=''
    if gY:
        xY,_=get(blk,gY,filt); tY=tr(xY,scale)
        mY = f"{(2**tY.mean() if scale!='lin' else tY.mean()):.3g}"
        if gS:
            xS,_=get(blk,gS,filt); tS=tr(xS,scale); mS=f"{(2**tS.mean() if scale!='lin' else tS.mean()):.3g}"
            base=tS.mean()
        else:
            base=t2.mean()  # no sham: use aged PSLN-212 as floor
        ri = (t4.mean()-base)/(tY.mean()-base)*100 if tY.mean()!=base else np.nan
    elif gS:
        xS,_=get(blk,gS,filt); tS=tr(xS,scale); mS=f"{(2**tS.mean() if scale!='lin' else tS.mean()):.3g}"
    # Hedges g
    sp = np.sqrt(((len(t4)-1)*t4.var(ddof=1)+(len(t2)-1)*t2.var(ddof=1))/(len(t4)+len(t2)-2))
    g_h = diff/sp*(1-3/(4*(len(t4)+len(t2))-9))
    cells = f"{c2[0].split('!')[0]}!{c2[0].split('!')[1]}..;{c4[0].split('!')[1]}.."
    rows.append(dict(domain=dom, block=blk, readout=label, tier=tier, n212=len(x2), n344=len(x4),
                     sham=mS, aged_212=m2, aged_344=m4, young_212=mY, effect_344_vs_212=eff, hedges_g=round(g_h,2),
                     p_welch=tt.pvalue, p_mw_exact=mw.pvalue, p_tukey=p_tukey, restoration_pct=ri,
                     direction=('344>212' if diff>0 else '344<212'), scale=('GM (log2)' if scale!='lin' else 'mean')))
R = pd.DataFrame(rows)
prim = R.tier!='C'
R.loc[prim,'p_holm_welch'] = multipletests(R.loc[prim,'p_welch'],method='holm')[1]
R.loc[prim,'q_BH_welch'] = multipletests(R.loc[prim,'p_welch'],method='fdr_bh')[1]
pd.set_option('display.width',300); pd.set_option('display.max_rows',200); pd.set_option('display.max_colwidth',48)
show = R.copy()
for c in ['p_welch','p_mw_exact','p_tukey','p_holm_welch','q_BH_welch']: show[c]=show[c].map(lambda p: '' if pd.isna(p) else (f'{p:.1e}' if p<0.001 else f'{p:.3f}'))
show['restoration_pct']=show['restoration_pct'].map(lambda x: '' if pd.isna(x) else f'{x:.0f}%')
print(show[['domain','block','readout','tier','sham','aged_212','aged_344','young_212','effect_344_vs_212','hedges_g','p_welch','p_mw_exact','p_tukey','p_holm_welch','restoration_pct']].to_string(index=False))
R.to_csv('/tmp/work/h2h_344_vs_212.csv',index=False)
print('\nTier A/B readouts:',prim.sum(),' 344>212:',((R.direction=='344>212')&prim).sum(),
      ' Holm<0.05:',(R.loc[prim,'p_holm_welch']<0.05).sum(), ' BH q<0.05:',(R.loc[prim,'q_BH_welch']<0.05).sum())
