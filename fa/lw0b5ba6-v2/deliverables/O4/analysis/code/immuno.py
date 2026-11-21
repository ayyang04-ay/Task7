import pandas as pd, numpy as np, warnings
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
warnings.filterwarnings('ignore')
vals = pd.read_csv('values.csv')
vals['group'] = vals.group.str.strip(); vals['note'] = vals['note'].astype(object)
# --- corrections documented in the audit ---
# (1) S03-B / S03-F: printed group labels are rotated relative to raw subclass titres (S13-A..D); relabel to match raw data.
rot = {'PSLN-212':'PSLN-212(Y)', 'PSLN-344':'PSLN-212', 'PSLN-212(Y)':'PSLN-344'}
m = vals.block.isin(['S03-B','S03-F'])
vals.loc[m,'group_corrected'] = vals.loc[m,'group'].map(rot)
vals['group_used'] = vals['group_corrected'].fillna(vals['group'])
# (2) HAI values of 0 are below the 1:10 lowest dilution -> impute 5 (half the LLOQ) for log analysis
hai = vals.block.isin(['S03-C','S03-G']) & (vals.value==0)
vals.loc[hai,'value'] = 5.0
vals.loc[hai,'note'] = 'HAI <10 imputed as 5'

def norm(g):
    g = g.replace('PSLN-212Y','PSLN-212(Y)').replace('PSLN-212(y)','PSLN-212(Y)')
    return g
vals['g'] = vals.group_used.map(norm)
readouts = [
 # (block, time filter, label, scale, category)
 ('S01-A_16h',None,'Lung Ifnb1 16 h (fold)','log','Innate'),
 ('S01-A_72h',None,'Lung Ifnb1 72 h (fold)','log','Innate'),
 ('S02-F','16h','Lung Gm-csf 16 h (fold)','log','Innate'),
 ('S02-F','36h','Lung Gm-csf 36 h (fold)','log','Innate'),
 ('S02-F','72h','Lung Gm-csf 72 h (fold)','log','Innate'),
 ('S01-D','4','Lung monocytes d4 (%)','lin','Innate'),
 ('S01-E','4','Lung CD11b+ DC d4 (%)','lin','Innate'),
 ('S01-F',None,'Lung cDC1 72 h (%)','lin','Innate'),
 ('S02-A',None,'Lung CCR7+ migratory CD11b+ DC 72 h (%)','lin','Antigen presentation'),
 ('S02-B',None,'MLN CD11b+CD103- DC 72 h (%)','lin','Antigen presentation'),
 ('S02-C',None,'MLN antigen+ (AF647-OVA) DC 36 h (%)','lin','Antigen presentation'),
 ('S02-D_CD40',None,'MLN CD11b+ DC CD40+ d3 (%)','lin','Antigen presentation'),
 ('S02-D_CD86',None,'MLN CD11b+ DC CD86+ d3 (%)','lin','Antigen presentation'),
 ('S02-E',None,'OT-I priming by MLN DC (%)','lin','Antigen presentation'),
 ('S03-K',None,'MLN germinal-centre B d7 (%)','lin','Humoral'),
 ('S04-A_ICOShi',None,'MLN ICOS-hi Tfh d7 (%)','lin','Humoral'),
 ('S04-B_Foxp3',None,'Tfr (Foxp3+ of CXCR5+ICOShi) d7 (%)','lin','Regulatory'),
 ('S04-C',None,'Tfr d30 (%)','lin','Regulatory'),
 ('S04-D',None,'Lung Treg d7 (%)','lin','Regulatory'),
 ('S03-A',None,'Serum IgG CA09 d14 (titre)','log','Humoral'),
 ('S03-E',None,'Serum IgG Aichi d14 (titre)','log','Humoral'),
 ('S03-C',None,'HAI CA09 d14 (titre)','log','Humoral'),
 ('S03-G',None,'HAI Aichi d14 (titre)','log','Humoral'),
 ('S03-D',None,'Neutralising Ab CA09 d14 (titre)','log','Humoral'),
 ('S03-H',None,'Neutralising Ab Aichi d14 (titre)','log','Humoral'),
 ('S13-A',None,'IgG2a CA09 d14 (titre)','log','Humoral'),
 ('S13-B',None,'IgG1 CA09 d14 (titre)','log','Humoral'),
 ('S13-C',None,'IgG2a Aichi d14 (titre)','log','Humoral'),
 ('S13-D',None,'IgG1 Aichi d14 (titre)','log','Humoral'),
 ('S03-B',None,'IgG2a:IgG1 CA09 (labels corrected)','log','Humoral'),
 ('S03-F',None,'IgG2a:IgG1 Aichi (labels corrected)','log','Humoral'),
 ('S13-I',None,'IgG CA09 d28 post-boost (titre)','log','Humoral'),
 ('S13-J',None,'IgG Aichi d28 post-boost (titre)','log','Humoral'),
 ('S13-H',None,'MLN IgG+ B220+ (%) [time not stated]','lin','Humoral'),
 ('S05-D',None,'Lung Ki-67+ CD8 d3 (%)','lin','Cellular'),
 ('S05-E',None,'Lung GZMB+ CD8 d3 (%)','lin','Cellular'),
 ('S05-F',None,'MLN IFNg+ CD8, H5N1 recall d14 (%)','lin','Cellular'),
 ('S05-G',None,'MLN IFNg+ CD8, H5N1 recall d60 (%)','lin','Cellular'),
 ('S05-H',None,'MLN GZMB+ CD8 d60 (%)','lin','Cellular'),
 ('S05-I',None,'Lung CD8 TRM d25 (%)','lin','Cellular'),
 ('S14-A_H1N1',None,'MLN IFNg+ CD8, H1N1 recall (%) [time not stated]','lin','Cellular'),
 ('S14-A_H3N2',None,'MLN IFNg+ CD8, H3N2 recall (%) [time not stated]','lin','Cellular'),
 ('S11-D','4','Lung NK d4 (%)','lin','Innate'),
 ('S11-E',None,'Lung CD206+ macrophages (%) [time not stated]','lin','Regulatory'),
]
rows=[]
for blk,tf,label,scale,cat in readouts:
    d = vals[vals.block==blk]
    if tf is not None: d = d[d.time.astype(str)==tf]
    y = np.log10(d.value) if scale=='log' else d.value
    d = d.assign(y=y)
    grp = d.groupby('g').y
    def summ(g):
        if g not in grp.groups: return (np.nan,np.nan,0)
        v = grp.get_group(g); return (v.mean(), v.std(ddof=1), len(v))
    m212,s212,n212 = summ('PSLN-212'); m344,s344,n344 = summ('PSLN-344'); my,sy,ny = summ('PSLN-212(Y)'); msh,ssh,nsh = summ('Sham')
    a = d[d.g=='PSLN-344'].y; b = d[d.g=='PSLN-212'].y
    t,p = stats.ttest_ind(a,b,equal_var=False)
    # Welch CI for difference
    se = np.sqrt(a.var(ddof=1)/len(a)+b.var(ddof=1)/len(b)); dfw = se**4/((a.var(ddof=1)/len(a))**2/(len(a)-1)+(b.var(ddof=1)/len(b))**2/(len(b)-1))
    diff = a.mean()-b.mean(); q = stats.t.ppf(0.975,dfw); lo,hi = diff-q*se, diff+q*se
    # Tukey across all groups in block (stated method)
    try:
        tk = pairwise_tukeyhsd(d.y, d.g); tdf = pd.DataFrame(tk.summary().data[1:], columns=tk.summary().data[0])
        r = tdf[((tdf.group1=='PSLN-212')&(tdf.group2=='PSLN-344'))|((tdf.group1=='PSLN-344')&(tdf.group2=='PSLN-212'))]
        ptk = float(r['p-adj'].iloc[0]) if len(r) else np.nan
    except Exception as ex:
        ptk = np.nan
    if scale=='log':
        eff = f"{10**diff:.2f}x (95% CI {10**lo:.2f}-{10**hi:.2f})"
        disp = lambda m: f"{10**m:.3g}" if m==m else ''
    else:
        eff = f"{diff:+.2f} pts (95% CI {lo:+.2f} to {hi:+.2f})"
        disp = lambda m: f"{m:.3g}" if m==m else ''
    ri = (m344-m212)/(my-m212) if (my==my and abs(my-m212)>1e-9) else np.nan
    cells = f"{d.cell.iloc[0]}..{d.cell.iloc[-1].split('!')[1]}"
    rows.append(dict(category=cat, readout=label, block=blk, scale=('geometric mean' if scale=='log' else 'arithmetic mean'),
        Sham=disp(msh), PSLN212_aged=disp(m212), PSLN344_aged=disp(m344), PSLN212_young=disp(my),
        n_per_group=f"{n212}/{n344}/{ny if ny else '-'}", effect_344_vs_212=eff, welch_p=p, tukey_p_344_vs_212=ptk,
        restoration_index=(round(ri,2) if ri==ri else None), cells=cells))
out = pd.DataFrame(rows)
out.to_csv('/tmp/outputs/analysis/T4_immunology_contrasts.csv', index=False)
pd.set_option('display.width',320); pd.set_option('display.max_colwidth',48); pd.set_option('display.max_rows',200)
print(out.drop(columns=['cells','scale']).to_string())
vals.to_csv('values_corrected.csv', index=False)
