from loadcsv import *
import numpy as np, pandas as pd
from scipy import stats
def ci(s):
    n=0
    for ch in s: n=n*26+(ord(ch)-64)
    return n
def gl(n):
    s=''
    while n: n,r=divmod(n-1,26); s=chr(65+r)+s
    return s
def cells(b,g,filt=None):
    d=DF[(DF.block==b)&(DF.group==g)]
    if filt:
        for k,v in filt.items(): d=d[d[k].astype(str)==str(v)]
    c=d.cell.str.split('!').str[1]; sh=d.cell.iloc[0].split('!')[0]
    cols=c.str.extract(r'([A-Z]+)')[0].map(ci); rows=c.str.extract(r'(\d+)')[0].astype(int)
    return f"{sh}!{gl(cols.min())}{rows.min()}:{gl(cols.max())}{rows.max()}", d.value.values.astype(float)
E=[('Targeting','SP-A/D-dependent AM uptake','S01-C','WT','SPA/D',None),
   ('Targeting','AECII uptake vs free dye','S01-B','AECII/FreeSRB','AECII/PSLN-SRB',None),
   ('Innate propagation','Gap-junction blockade (CBX) of monocyte recruitment','S11-C','CBX-','CBX+',None),
   ('Monocyte recruitment','CCR2 antagonist INCB3344: monocytes','S07-B_mono','PSLN-344','PSLN-344+INCB3344',None),
   ('Monocyte recruitment','CCR2 antagonist INCB3344: Ly6C+ macrophages','S07-B_mac','PSLN-344','PSLN-344+INCB3344',None),
   ('Monocyte recruitment','CCR2 antagonist INCB3344: lung GZMB+ CD8 (young)','S02-I','PSLN-344(Y)','PSLN-344(Y)+INCB3344',None),
   ('moDC differentiation','IFNAR-KO marrow, cDC precursors removed','S02-H','WT w/o cDC','IFN w/o cDC',None),
   ('moDC differentiation','IFNAR-KO marrow, cDC precursors retained','S02-H','WT w/ cDC','IFN w/ cDC',None),
   ('moDC differentiation','GM-CSF rescue of IFNAR-KO (w/o cDC)','S02-H','IFN w/o cDC','GMCSF',None),
   ('moDC differentiation','GM-CSF added to PSLN-212','S02-G','PSLN-212','PSLN-212+GM-CSF',None),
   ('moDC differentiation','IFNAR-KO -> WT monocyte infiltration (young, n=3)','S12-A','WT to WT','IFNAR-/- to WT',None),
   ('Monocyte fate','Ly6C+CCR2+ macrophages d5 (x1e5), PSLN-212 vs PSLN-344','S07-A','PSLN-212','PSLN-344',{'day':'5'}),
   ('Monocyte fate','Ly6C+CCR2+ macrophages d10 (x1e5), PSLN-212 vs PSLN-344','S07-A','PSLN-212','PSLN-344',{'day':'10'}),
   ('DC migration','PTX: antigen+ MLN DC (aged PSLN-344)','S02-C','PSLN-344','PTX',None),
   ('DC migration','PTX: MLN DC -> OT-I priming (aged PSLN-344)','S02-E','PSLN-344','PTX',None),
   ('DC migration','PTX: OT-I proliferation in MLN in vivo','S05-C','MLN','MLN+PTX',None),
   ('DC migration','PTX: OT-I proliferation in lung in vivo','S05-C','Lung','Lung+PTX',None)]
rows=[]
for dom,lab,b,g1,g2,f in E:
    c1,x1=cells(b,g1,f); c2,x2=cells(b,g2,f)
    t=stats.ttest_ind(x2,x1,equal_var=False); mw=stats.mannwhitneyu(x2,x1,method='exact')
    rows.append(dict(step=dom,experiment=lab,block=b,control_group=g1,test_group=g2,n=f"{len(x1)},{len(x2)}",
        mean_control=round(x1.mean(),3),mean_test=round(x2.mean(),3),pct_change=round((x2.mean()/x1.mean()-1)*100,1),
        p_welch=t.pvalue,p_mannwhitney_exact=mw.pvalue,cells_control=c1,cells_test=c2))
pd.DataFrame(rows).to_csv('/tmp/outputs/tables/T5_moa_interventions.csv',index=False)
print(pd.DataFrame(rows)[['experiment','mean_control','mean_test','pct_change','p_welch','cells_control','cells_test']].to_string(index=False))
