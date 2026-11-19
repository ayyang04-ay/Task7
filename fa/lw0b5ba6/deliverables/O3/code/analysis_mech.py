import pandas as pd, numpy as np, warnings
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
warnings.filterwarnings('ignore')
D = pd.read_csv('/tmp/work/tidy/continuous.csv'); D['time'] = D['time'].astype(str)
def g(blk, grp, meas=None):
    d = D[(D.block==blk)&(D.group==grp)]
    if meas: d = d[d.measurand==meas]
    return d.value.values
rows=[]
def comp(label, blk, a, b, meas=None, note=''):
    x, y = g(blk,a,meas), g(blk,b,meas)
    w = stats.ttest_ind(x,y,equal_var=False).pvalue
    mw = stats.mannwhitneyu(x,y,method='exact').pvalue
    rows.append(dict(experiment=label, block=blk, measurand=(meas or D[D.block==blk].measurand.iloc[0]), group_a=a, group_b=b, n_a=len(x), n_b=len(y),
                     mean_a=x.mean(), sd_a=x.std(ddof=1), mean_b=y.mean(), sd_b=y.std(ddof=1), ratio_a_over_b=x.mean()/y.mean(),
                     pct_reduction=100*(1-y.mean()/x.mean()), p_welch=w, p_mw_exact=mw, note=note))
comp('Surfactant-mimetic vehicle targets AECII vs free dye','S01-B','AECII/PSLN-SRB','AECII/FreeSRB', note='dye cargo (SRB), not CDN-1807')
comp('Surfactant-mimetic vehicle targets AECI vs free dye','S01-B','AECI/PSLN-SRB','AECI/FreeSRB')
comp('AECII vs AECI preference of PSLN','S01-B','AECII/PSLN-SRB','AECI/PSLN-SRB')
comp('AM uptake depends on SP-A/SP-D','S01-C','WT','SPA/D', note='liposome of PSLN-344 composition, DiD-labelled')
comp('Mn formulation reduces AECII uptake','S08-C','AECII-PSLN-SRB','AECII-PSLN-344-SRB', note='S08-C shares values with S01-B (integrity flag)')
comp('Mn formulation reduces AECI uptake','S08-C','AECI-PSLN-SRB','AECI-PSLN-344-SRB')
comp('GM-CSF add-back to PSLN-212 increases moDC','S02-G','PSLN-212+GM-CSF','PSLN-212')
comp('GM-CSF alone','S02-G','PSLN-212+GM-CSF','GM-CSF')
comp('IFNAR needed for moDC (no cDC precursors)','S02-H','WT w/o cDC','IFN w/o cDC', note='BM chimeras, PSLN-344 + bivalent vaccine')
comp('IFNAR needed for moDC (with cDC precursors)','S02-H','WT w/ cDC','IFN w/ cDC')
comp('GM-CSF rescues IFNAR-/- moDC','S02-H','GMCSF','IFN w/o cDC')
comp('GM-CSF rescue vs WT','S02-H','WT w/o cDC','GMCSF')
comp('CCR2 blockade abolishes CD8 GZMB (young)','S02-I','PSLN-344(Y)','PSLN-344(Y)+INCB3344', note='young animals')
comp('CCR2 blockade reduces monocytes','S07-B','PSLN-344','PSLN-344+INCB3344','Lung CD11b+Ly6C+ monocytes (%)')
comp('CCR2 blockade reduces Ly6C+ macrophages','S07-B','PSLN-344','PSLN-344+INCB3344','Lung Ly6C+ macrophages (%)')
comp('Gap-junction block (CBX) reduces monocyte recruitment','S11-C','CBX-','CBX+')
comp('IFNAR-/- BM reduces monocyte infiltration (young)','S12-A','WT to WT','IFNAR-/- to WT', note='n=3, young')
comp('PTX blocks antigen+ DC arrival in MLN','S02-C','PSLN-344','PTX', note='adjuvant for PTX group not stated')
comp('PTX blocks DC priming capacity (OT-I)','S02-E','PSLN-344','PTX', note='OT-I (H-2Kb) with DCs from BALB/c (H-2d) donors?')
comp('PTX blocks OT-I priming in MLN in vivo','S05-C','MLN','MLN+PTX', note='C57BL/6 recipients, OVA + PSLN-344')
comp('PTX does not affect lung OT-I proliferation','S05-C','Lung','Lung+PTX')
M = pd.DataFrame(rows)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 55)
print(M[['experiment','block','group_a','group_b','n_a','mean_a','mean_b','ratio_a_over_b','pct_reduction','p_welch','p_mw_exact']].round(4).to_string(index=False))
M.to_csv('/tmp/work/tidy/mechanistic_tests.csv', index=False)
# Tukey for S02-H
d = D[D.block=='S02-H']; print(pairwise_tukeyhsd(d.value, d.group))
d = D[D.block=='S02-G']; print(pairwise_tukeyhsd(d.value, d.group))
