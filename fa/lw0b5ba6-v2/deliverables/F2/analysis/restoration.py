import numpy as np, pandas as pd
from scipy import stats
from statlib import *
pd.set_option('display.width', 300); pd.set_option('display.max_rows', 3000); pd.set_option('display.float_format', lambda x: f'{x:.4g}')
LABEL = {
 'S01-A_16h':'Lung Ifnb1 mRNA, 16 h (fold)', 'S01-A_72h':'Lung Ifnb1 mRNA, 72 h (fold)', 'S01-F':'Lung cDC1, 72 h (%)','S01-G':'Lung cDC2, 72 h (%)',
 'S02-A':'CCR7+ migratory CD11b+ DC, lung 72 h (%)','S02-B':'MLN CD11b+CD103- DC, 72 h (%)','S02-C':'Antigen(OVA-AF647)+ DC in MLN, 36 h (%)',
 'S02-D_CD40':'CD40+ MLN CD11b+ DC, d3 (%)','S02-D_CD86':'CD86+ MLN CD11b+ DC, d3 (%)','S02-E':'OT-I CD8 priming by MLN DC ex vivo (%)',
 'S03-A':'Serum IgG anti-H1N1, d14 (titre)','S03-C':'HAI anti-H1N1, d14 (titre)','S03-D':'Neutralising Ab anti-H1N1, d14 (titre)',
 'S03-E':'Serum IgG anti-H3N2, d14 (titre)','S03-G':'HAI anti-H3N2, d14 (titre)','S03-H':'Neutralising Ab anti-H3N2, d14 (titre)',
 'S03-K':'GC B cells in MLN, d7 (%)','S04-A_ICOSlo':'Tfh ICOS-low, d7 (%)','S04-A_ICOShi':'Tfh ICOS-high, d7 (%)','S04-B_Tfr':'Tfr (Foxp3+ in CXCR5+), d7 (%)',
 'S04-B_TfhTfr':'Tfh:Tfr ratio, d7','S04-C':'Tfr, d30 (%)','S04-D':'Lung Treg, d7 (%)','S05-D':'Ki-67+ lung CD8, d3 (%)','S05-E':'GZMB+ lung CD8, d3 (%)',
 'S05-F':'IFN-g+ CD8 to rgH5N1 (heterosubtypic), MLN d14 (%)','S05-G':'IFN-g+ CD8 to rgH5N1, MLN d60 (%)','S05-H':'GZMB+ CD8, MLN d60 (%)','S05-I':'Lung CD8 TRM (CD69+CD103+), d25 (%)',
 'S11-E':'CD206+ lung macrophages (%)','S13-A':'IgG2a anti-H1N1, d14 (titre)','S13-B':'IgG1 anti-H1N1, d14 (titre)','S13-C':'IgG2a anti-H3N2, d14 (titre)','S13-D':'IgG1 anti-H3N2, d14 (titre)',
 'S13-H':'IgG+ B220+ cells in MLN (%)','S13-I':'IgG anti-H1N1 after boost, d28 (titre)','S13-J':'IgG anti-H3N2 after boost, d28 (titre)','S14-A_H1N1':'IFN-g+ CD8 to H1N1, MLN (%)','S14-A_H3N2':'IFN-g+ CD8 to H3N2, MLN (%)',
}
rows=[]
for k, lab in LABEL.items():
    d = B[k]
    if not {'PSLN-212','PSLN-344','PSLN-212(Y)'} <= set(d.group.unique()): continue
    c1 = contrast(k, 'PSLN-212', 'PSLN-344'); c2 = contrast(k, 'PSLN-212(Y)', 'PSLN-344'); c3 = contrast(k, 'PSLN-212(Y)', 'PSLN-212')
    sc = scale_of(k)
    if sc=='log10':
        y = c2['gm_ref']; a = c1['gm_test']; o = c1['gm_ref']
    else:
        y = c2['mean_ref']; a = c1['mean_test']; o = c1['mean_ref']
    sham = None
    if 'Sham' in d.group.unique():
        sv_ = d[d.group=='Sham']['value'].values
        sham = (10**np.mean(np.log10(np.where(sv_>0, sv_, HAI_LOD_SUB))) if sc=='log10' else sv_.mean())
    rows.append(dict(block=k, readout=lab, scale=('geometric mean' if sc=='log10' else 'mean'), sham_aged=sham, psln212_aged=o, psln344_aged=a, young_psln212=y,
                     fold_344_vs_212=c1['fold'], fold_lo=c1['fold_lo'], fold_hi=c1['fold_hi'], p_welch_344_vs_212=c1['p_welch'], p_tukey_344_vs_212=c1['p_tukey'], p_mw_344_vs_212=c1['p_mw_exact'],
                     pct_of_young_344=100*a/y, pct_of_young_212=100*o/y, p_welch_344_vs_young=c2['p_welch'], p_tukey_344_vs_young=c2['p_tukey'],
                     closer_to_young=abs(np.log(a/y)) < abs(np.log(o/y)), n=c1['n_test'], cells_212=c1['cells_ref'], cells_344=c1['cells_test'], cells_young=c2['cells_ref']))
r = pd.DataFrame(rows); r.to_csv('restoration_index.csv', index=False)
print(r[['block','readout','sham_aged','psln212_aged','psln344_aged','young_psln212','fold_344_vs_212','p_welch_344_vs_212','p_tukey_344_vs_212','pct_of_young_212','pct_of_young_344','p_welch_344_vs_young','closer_to_young']].to_string(index=False))
print('\nreadouts:', len(r), ' PSLN-344 closer to young benchmark than PSLN-212:', int(r.closer_to_young.sum()))
print('Welch p<0.05 for 344 vs 212:', int((r.p_welch_344_vs_212<0.05).sum()), ' Tukey p<0.05:', int((r.p_tukey_344_vs_212<0.05).sum()), ' MW exact p<0.05:', int((r.p_mw_344_vs_212<0.05).sum()))
print('344 not different from young (Welch p>=0.05):', int((r.p_welch_344_vs_young>=0.05).sum()), ' of ', len(r))
print(r[r.p_welch_344_vs_212>=0.05][['block','readout','p_welch_344_vs_212']])
print('median % of young: PSLN-344', r.pct_of_young_344.median(), ' PSLN-212', r.pct_of_young_212.median())
