from loadcsv import *
import numpy as np, pandas as pd
from scipy import stats
from scipy.optimize import curve_fit
import warnings; warnings.filterwarnings('ignore')
def v(b,g,**kw):
    d = DF[(DF.block==b)&(DF.group==g)]
    for k,x in kw.items(): d=d[d[k].astype(str)==str(x)]
    return d.value.values.astype(float)
def comp(label,b,g1,g2,log=False,**kw):
    a=v(b,g1,**kw); c=v(b,g2,**kw)
    ta,tc=(np.log2(a),np.log2(c)) if log else (a,c)
    t=stats.ttest_ind(tc,ta,equal_var=False); mw=stats.mannwhitneyu(c,a,method='exact')
    if log: eff=f"GM {2**ta.mean():.3g} -> {2**tc.mean():.3g} ({2**(tc.mean()-ta.mean()):.2f}x)"
    else: eff=f"{a.mean():.3g} -> {c.mean():.3g} ({(c.mean()/a.mean()-1)*100:+.0f}%)"
    print(f"  {label:62s} [{b}] {g1} vs {g2}: {eff}; Welch p={t.pvalue:.2g}; MW exact p={mw.pvalue:.3g}; n={len(a)},{len(c)}")
print("== Uptake / targeting ==")
comp('AECII SRB+ : free SRB vs PSLN-SRB (aged)','S01-B','AECII/FreeSRB','AECII/PSLN-SRB')
comp('AECI SRB+  : free SRB vs PSLN-SRB (aged)','S01-B','AECI/FreeSRB','AECI/PSLN-SRB')
comp('AM DiD+ : WT vs Sftpa1/Sftpd KO (SP-A/D-dependent uptake)','S01-C','WT','SPA/D')
print("== Innate → monocyte/moDC axis (causal tests) ==")
comp('GM-CSF sufficiency: PSLN-212 vs PSLN-212+GM-CSF (moDC-like d5)','S02-G','PSLN-212','PSLN-212+GM-CSF')
comp('GM-CSF alone vs PSLN-212 (moDC-like d5)','S02-G','GM-CSF','PSLN-212')
comp('IFNAR dependence (no cDC precursors): WT vs IFNAR-KO BM','S02-H','WT w/o cDC','IFN w/o cDC')
comp('IFNAR dependence (with cDC precursors): WT vs IFNAR-KO BM','S02-H','WT w/ cDC','IFN w/ cDC')
comp('GM-CSF rescue of IFNAR-KO (no cDC): IFN w/o cDC vs GMCSF','S02-H','IFN w/o cDC','GMCSF')
comp('IFNAR-KO BM → monocyte infiltration (young, n=3)','S12-A','WT to WT','IFNAR-/- to WT')
comp('CCR2 blockade (INCB3344): lung CD11b+Ly6C+ monocytes','S07-B_mono','PSLN-344','PSLN-344+INCB3344')
comp('CCR2 blockade (INCB3344): lung Ly6C+ macrophages','S07-B_mac','PSLN-344','PSLN-344+INCB3344')
comp('CCR2 blockade (INCB3344): lung GZMB+ CD8 d5 (young)','S02-I','PSLN-344(Y)','PSLN-344(Y)+INCB3344')
comp('Gap-junction blockade (CBX): recruited monocytes d3 (aged)','S11-C','CBX-','CBX+')
print("== Ly6C+CCR2+ macrophage kinetics (S07-A, x1e5 cells), PSLN-212 vs PSLN-344 ==")
for d in [0,2,5,10,30]:
    a=v('S07-A','PSLN-212',day=d); c=v('S07-A','PSLN-344',day=d)
    print(f"   day {d:2d}: PSLN-212 {a.mean():5.2f}  PSLN-344 {c.mean():5.2f}   Welch p={stats.ttest_ind(c,a,equal_var=False).pvalue:.2g}")
print("== Antigen transport / priming: pertussis toxin (Gi-GPCR, e.g. CCR7) ==")
comp('PTX: MLN antigen+ DC (PSLN-344 aged vs PTX)','S02-C','PSLN-344','PTX')
comp('PTX: DC→OT-I priming (PSLN-344 aged vs PTX)','S02-E','PSLN-344','PTX')
comp('PTX: OT-I proliferation in MLN in vivo','S05-C','MLN','MLN+PTX')
comp('PTX: OT-I proliferation in lung in vivo','S05-C','Lung','Lung+PTX')
print("== Young: does Mn add anything? PSLN-212(Y) vs PSLN-344(Y) ==")
comp('Ifnb1 16h','S01-A_16h','PSLN-212(Y)','PSLN-344(Y)',log=True)
comp('Ifnb1 72h','S01-A_72h','PSLN-212(Y)','PSLN-344(Y)',log=True)
comp('Lung cDC1','S01-F','PSLN-212(Y)','PSLN-344(Y)')
comp('MLN antigen+ DC','S02-C','PSLN-212(Y)','PSLN-344(Y)')
comp('DC→OT-I priming','S02-E','PSLN-212(Y)','PSLN-344(Y)')
comp('Lung CD11b+ DC d4','S01-E','PSLN-212(Y)','PSLN-344(Y)',day='4')
print("== Aged PSLN-344 vs YOUNG PSLN-212 (is restoration complete?) ==")
for b,lab,log in [('S01-A_16h','Ifnb1 16h',True),('S03-A','IgG CA09',True),('S03-C','HAI CA09',True),('S03-G','HAI Aichi',True),('S03-D','Neut CA09',True),
                  ('S03-K','GC B',False),('S04-A_ICOShi','Tfh',False),('S02-D_CD40','DC CD40',False),('S02-D_CD86','DC CD86',False),('S05-I','TRM',False),('S05-F','IFNg CD8 d14',False)]:
    comp(lab,b,'PSLN-212(Y)','PSLN-344',log=log)
