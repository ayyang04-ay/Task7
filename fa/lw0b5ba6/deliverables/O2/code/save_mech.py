import pandas as pd, numpy as np, warnings
from scipy import stats
warnings.filterwarnings('ignore')
t=pd.read_csv('tidy.csv'); t['time']=t['time'].astype(str)
rows=[]
def grp(block,g,filt=None):
    d=t[(t.block==block)&(t.group==g)]
    if filt: d=d[d[filt[0]].astype(str)==filt[1]]
    return d.value.values, ';'.join([d.cell.iloc[0],d.cell.iloc[-1]]) if len(d) else ''
def cmp(step,label,block,a,b,filt=None,log=False):
    xa,ca=grp(block,a,filt); xb,cb=grp(block,b,filt)
    ya,yb=(np.log10(xa),np.log10(xb)) if log else (xa,xb)
    st=stats.ttest_ind(ya,yb); w=stats.ttest_ind(ya,yb,equal_var=False); mw=stats.mannwhitneyu(xa,xb)
    ma,mb=(10**ya.mean(),10**yb.mean()) if log else (xa.mean(),xb.mean())
    rows.append(dict(MoA_step=step,comparison=label,block=block,group_A=a,mean_A=ma,sd_A=xa.std(ddof=1),n_A=len(xa),cells_A=ca,group_B=b,mean_B=mb,sd_B=xb.std(ddof=1),n_B=len(xb),cells_B=cb,
                     pct_change_A_vs_B=(ma-mb)/mb*100,student_p=st.pvalue,welch_p=w.pvalue,mannwhitney_p=mw.pvalue,scale='log10' if log else 'linear'))
cmp('1 Delivery','AECII vs AECI uptake (PSLN-SRB)','S01-B','AECII/PSLN-SRB','AECI/PSLN-SRB')
cmp('1 Delivery','Liposome vs free dye in AECII','S01-B','AECII/PSLN-SRB','AECII/FreeSRB')
cmp('1 Delivery','AM uptake, WT vs Sftpa1/Sftpd KO','S01-C','WT','SPA/D')
cmp('1 Delivery','S08-C AECII: PSLN vs PSLN-344 (as printed; see F06)','S08-C','AECII-PSLN-SRB','AECII-PSLN-344-SRB')
cmp('3 Paracrine','Recruited monocytes, saline vs carbenoxolone','S11-C','CBX-','CBX+')
cmp('4 Recruitment','Monocytes, vehicle vs CCR2 antagonist','S07-B_Mono','PSLN-344','PSLN-344+INCB3344')
cmp('4 Recruitment','Ly6C+ macrophages, vehicle vs CCR2 antagonist','S07-B_Ly6C+Mphi','PSLN-344','PSLN-344+INCB3344')
cmp('4 Recruitment','Monocyte infiltration, WT vs IFNAR-/- BM (young)','S12-A','WT to WT','IFNAR-/- to WT')
cmp('5 moDC fate','moDC, WT vs IFNAR-/- BM (cDC precursors removed)','S02-H','WT w/o cDC','IFN w/o cDC')
cmp('5 moDC fate','moDC, WT vs IFNAR-/- BM (with cDC precursors)','S02-H','WT w/ cDC','IFN w/ cDC')
cmp('5 moDC fate','moDC, IFNAR-/- + GM-CSF rescue vs IFNAR-/-','S02-H','GMCSF','IFN w/o cDC')
cmp('5 moDC fate','moDC, PSLN-212 + GM-CSF vs PSLN-212','S02-G','PSLN-212+GM-CSF','PSLN-212')
cmp('5 moDC fate','moDC, PSLN-212 + GM-CSF vs GM-CSF alone','S02-G','PSLN-212+GM-CSF','GM-CSF')
for day in ['2','5','10','30']:
    cmp('5 moDC fate',f'Ly6C+CCR2+ macrophages (x1e5) day {day}, PSLN-344 vs PSLN-212','S07-A','PSLN-344','PSLN-212',filt=('time',day))
cmp('6 DC migration','Antigen+ MLN DC, PSLN-344 vs pertussis toxin','S02-C','PSLN-344','PTX')
cmp('6 DC migration','OT-I proliferation, PSLN-344 DC vs PTX DC (see F12)','S02-E','PSLN-344','PTX')
cmp('6 DC migration','OT-I proliferation in MLN, vehicle vs PTX','S05-C','MLN','MLN+PTX')
cmp('6 DC migration','OT-I proliferation in lung, vehicle vs PTX','S05-C','Lung','Lung+PTX')
cmp('7 Regulation','Lung Treg after macrophage transfer, col B vs col C (labels identical, see F10)','S07-C','colB "Ly6C-CD206+ MPhi"','colC "Ly6C-CD206+ MPhi"')
cmp('9 CD8','GZMB+ CD8 (young), vehicle vs CCR2 antagonist','S02-I','PSLN-344(Y)','PSLN-344(Y)+INCB3344')
for an in ['Ifnb1','Tnf','Isg15']:
    for a,b in [('PSLN-344','PBS'),('PSLN-344','Sham'),('CT','PBS')]:
        cmp('Safety',f'CNS {an} 36 h, {a} vs {b}',f'S10-A_{an}',a,b,log=True)
pd.DataFrame(rows).to_csv('mech_results.csv',index=False)
print(len(rows),'mechanism/safety comparisons saved')
