import pandas as pd, numpy as np, warnings
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
warnings.filterwarnings('ignore')
t=pd.read_csv('tidy.csv'); t['time']=t['time'].astype(str)
def grp(block, g, filt=None):
    d=t[(t.block==block)&(t.group==g)]
    if filt: d=d[d[filt[0]].astype(str)==filt[1]]
    return d.value.values
def cmp(block,a,b,filt=None,log=False,label=''):
    xa,xb=grp(block,a,filt),grp(block,b,filt)
    ya,yb=(np.log10(xa),np.log10(xb)) if log else (xa,xb)
    w=stats.ttest_ind(ya,yb,equal_var=False); st=stats.ttest_ind(ya,yb)
    mw=stats.mannwhitneyu(xa,xb)
    ma,mb=(10**ya.mean(),10**yb.mean()) if log else (xa.mean(),xb.mean())
    sa,sb=xa.std(ddof=1),xb.std(ddof=1)
    chg=(ma-mb)/mb*100
    print(f"{label:60s} {block:12s} {a:>22s} {ma:8.3g}±{sa:.2g} (n={len(xa)}) vs {b:>22s} {mb:8.3g}±{sb:.2g} (n={len(xb)})  change {chg:+.0f}%  Student p={st.pvalue:.2g} Welch p={w.pvalue:.2g} MW p={mw.pvalue:.2g}")
print("=== Uptake / targeting ===")
cmp('S01-B','AECII/PSLN-SRB','AECI/PSLN-SRB',label='AECII vs AECI uptake of PSLN-SRB')
cmp('S01-B','AECII/PSLN-SRB','AECII/FreeSRB',label='PSLN vs free SRB in AECII')
cmp('S01-C','WT','SPA/D',label='AM uptake WT vs Sftpa1/Sftpd KO')
cmp('S08-C','AECII-PSLN-SRB','AECII-PSLN-344-SRB',label='S08-C AECII: PSLN vs PSLN-344 (as printed)')
cmp('S08-C','AECI-PSLN-SRB','AECI-PSLN-344-SRB',label='S08-C AECI: PSLN vs PSLN-344 (as printed)')
cmp('S08-C','AECII-PSLN-SRB','AECI-PSLN-SRB',label='S08-C PSLN: AECII vs AECI (as printed)')
print("=== Gap junction / monocyte recruitment ===")
cmp('S11-C','CBX-','CBX+',label='Recruited monocytes: CBX- vs CBX+ (gap-junction block)')
cmp('S07-B_Mono','PSLN-344','PSLN-344+INCB3344',label='Monocytes: vehicle vs CCR2 antagonist')
cmp('S07-B_Ly6C+Mphi','PSLN-344','PSLN-344+INCB3344',label='Ly6C+ Mphi: vehicle vs CCR2 antagonist')
cmp('S02-I','PSLN-344(Y)','PSLN-344(Y)+INCB3344',label='GZMB+ CD8: vehicle vs CCR2 antagonist (young)')
cmp('S12-A','WT to WT','IFNAR-/- to WT',label='CD45.2 monocyte infiltration WT vs IFNAR-/- BM')
print("=== moDC differentiation: GM-CSF / IFNAR ===")
cmp('S02-G','PSLN-212+GM-CSF','PSLN-212',label='Ly6C+ moDC: PSLN-212 + GM-CSF vs PSLN-212')
cmp('S02-G','PSLN-212+GM-CSF','GM-CSF',label='Ly6C+ moDC: PSLN-212 + GM-CSF vs GM-CSF alone')
cmp('S02-H','WT w/o cDC','IFN w/o cDC',label='moDC: WT vs IFNAR-KO BM (cDC precursors removed)')
cmp('S02-H','WT w/ cDC','IFN w/ cDC',label='moDC: WT vs IFNAR-KO BM (with cDC precursors)')
cmp('S02-H','GMCSF','IFN w/o cDC',label='moDC: IFNAR-KO + GM-CSF rescue vs IFNAR-KO')
cmp('S02-H','WT w/o cDC','GMCSF',label='moDC: WT vs IFNAR-KO+GM-CSF rescue')
print("=== DC migration blockade ===")
cmp('S02-C','PSLN-344','PTX',label='Ag+ MLN DC: PSLN-344 vs PTX')
cmp('S02-E','PSLN-344','PTX',label='OT-I proliferation: PSLN-344 DC vs PTX DC')
cmp('S05-C','MLN','MLN+PTX',label='OT-I proliferation in MLN: PBS vs PTX')
cmp('S05-C','Lung','Lung+PTX',label='OT-I proliferation in lung: PBS vs PTX')
print("=== Macrophage transfer ===")
cmp('S07-C','colB "Ly6C-CD206+ MPhi"','colC "Ly6C-CD206+ MPhi"',label='Lung Treg after transfer: col B vs col C (labels identical)')
print("=== S07-A Ly6C+CCR2+ macrophage counts by day ===")
for day in ['0','2','5','10','30']:
    cmp('S07-A','PSLN-344','PSLN-212',filt=('time',day),label=f'Ly6C+CCR2+ Mphi x1e5 day {day}')
print("=== CNS (S10-A) ===")
for an in ['Ifnb1','Tnf','Isg15']:
    blk=f'S10-A_{an}'
    for a,b in [('PSLN-344','PBS'),('PSLN-344','Sham'),('CT','PBS'),('CT','PSLN-344')]:
        cmp(blk,a,b,log=True,label=f'CNS {an}')
    d=t[t.block==blk]; f,p=stats.f_oneway(*[d[d.group==g].value for g in d.group.unique()])
    tk=pairwise_tukeyhsd(d.value.values,d.group.values); print(tk.summary())
print("=== S08-A dose response (Ifnb1 16h) ===")
d=t[t.block=='S08-A']
piv=d.groupby(['group','time']).value.agg(['mean','std','count']).unstack('group')
print(piv.round(2).to_string())
print("=== S08-B Encapsulation efficiency ===")
d=t[t.block=='S08-B']; print(d.groupby('group').value.agg(['mean','std','min','max','count']).round(1))
