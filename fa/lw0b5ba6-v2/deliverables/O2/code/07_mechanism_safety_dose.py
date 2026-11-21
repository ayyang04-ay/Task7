"""07_mechanism_safety_dose.py -- mechanistic intervention tests, S08-A dose-response fits, S10-A CNS, S08-D reactogenicity."""
import pandas as pd, numpy as np, warnings
from scipy import stats
from scipy.optimize import curve_fit
from statsmodels.stats.multicomp import pairwise_tukeyhsd
warnings.filterwarnings('ignore')
rng=np.random.default_rng(7)
C=pd.read_csv('/tmp/work/tidy/continuous.csv'); C['time']=C['time'].astype(str)
B=pd.read_csv('/tmp/work/tidy/bodyweight.csv')
def vals(block,group,meas=None,time=None):
    d=C[(C.block==block)&(C.group==group)]
    if meas: d=d[d.measurand==meas]
    if time is not None: d=d[d.time==str(time)]
    return d.sort_values('rep').value.values, (f"{d.cell.iloc[0]}..{d.cell.iloc[-1]}" if len(d) else '')
rows=[]
def t2(block,a,b,meas=None,label='',log=False,time=None):
    va,ca=vals(block,a,meas,time); vb,cb=vals(block,b,meas,time)
    xa,xb=(np.log10(va),np.log10(vb)) if log else (va,vb)
    st=stats.ttest_ind(xa,xb)            # Student's t (stated method)
    wl=stats.ttest_ind(xa,xb,equal_var=False)
    try: mw=stats.mannwhitneyu(va,vb,method='exact').pvalue
    except: mw=np.nan
    rows.append(dict(block=block,question=label,group_a=a,mean_a=va.mean(),sd_a=va.std(ddof=1),n_a=len(va),
                     group_b=b,mean_b=vb.mean(),sd_b=vb.std(ddof=1),n_b=len(vb),ratio=va.mean()/vb.mean(),
                     student_p=st.pvalue,welch_p=wl.pvalue,mw_p=mw,cells_a=ca,cells_b=cb))
t2('S01-B','AECII/PSLN-SRB','AECI/PSLN-SRB',label='PSLN tropism: type II vs type I alveolar epithelium')
t2('S01-B','AECII/PSLN-SRB','AECII/FreeSRB',label='Liposome vs free dye uptake by AECII')
t2('S01-C','WT','SPA/D',label='Alveolar-macrophage uptake depends on SP-A/SP-D')
t2('S11-C','CBX-','CBX+',label='Gap-junction blockade (carbenoxolone) reduces monocyte recruitment')
t2('S12-A','WT to WT','IFNAR-/- to WT',label='Monocyte infiltration with IFNAR-/- bone marrow')
t2('S02-H','WT w/o cDC','IFN w/o cDC',label='moDC generation requires IFNAR (cDC-depleted BM)')
t2('S02-H','WT w/ cDC','IFN w/ cDC',label='moDC generation requires IFNAR (cDC-replete BM)')
t2('S02-H','GMCSF','IFN w/o cDC',label='GM-CSF partially rescues IFNAR-/- moDC')
t2('S02-H','WT w/o cDC','GMCSF',label='GM-CSF rescue vs WT')
t2('S02-G','PSLN-212+GM-CSF','PSLN-212',label='Adding GM-CSF to PSLN-212 (no Mn) raises moDC-like cells')
t2('S02-G','PSLN-212','GM-CSF',label='PSLN-212 vs GM-CSF alone')
t2('S02-I','PSLN-344(Y)','PSLN-344(Y)+INCB3344',label='CCR2 blockade abolishes lung GZMB+ CD8 (young)')
t2('S07-B','PSLN-344','PSLN-344+INCB3344','Lung CD11b+Ly6C+ monocytes (%)',label='CCR2 blockade reduces monocytes (aged)')
t2('S07-B','PSLN-344','PSLN-344+INCB3344','Lung Ly6C+ macrophages (%)',label='CCR2 blockade reduces Ly6C+ macrophages (aged)')
t2('S05-C','MLN','MLN+PTX',label='Pertussis toxin blocks OT-I priming in MLN')
t2('S05-C','Lung','Lung+PTX',label='Pertussis toxin does not block OT-I proliferation in lung')
t2('S02-C','PSLN-344','PTX',label='Antigen+ DC in MLN: PSLN-344 vs PTX arm')
t2('S02-E','PSLN-344','PTX',label='OT-I priming by MLN DC: PSLN-344 vs PTX arm')
t2('S08-C','AECII-PSLN-SRB','AECII-PSLN-344-SRB',label='Epithelial uptake PSLN vs PSLN-344 (AECII) [DI-09]')
t2('S08-C','AECI-PSLN-SRB','AECI-PSLN-344-SRB',label='Epithelial uptake PSLN vs PSLN-344 (AECI) [DI-09]')
M=pd.DataFrame(rows); M.to_csv('/tmp/work/tables/mechanism_tests.csv',index=False)
pd.set_option('display.width',250)
print(M[['block','question','mean_a','mean_b','ratio','student_p','mw_p']].round(4).to_string(index=False))

# ---- S10-A CNS (reported as mean +/- SD per annotation) ----
cns=[]
for meas in ['CNS Ifnb1 (fold)','CNS Tnf (fold)','CNS Isg15 (fold)']:
    d=C[(C.block=='S10-A')&(C.measurand==meas)]
    tk=pairwise_tukeyhsd(d.value,d.group); tab=pd.DataFrame(tk.summary().data[1:],columns=tk.summary().data[0])
    an=stats.f_oneway(*[g.value.values for _,g in d.groupby('group')])
    for g,dd in d.groupby('group',sort=False):
        def padj(x,y):
            r=tab[((tab.group1==x)&(tab.group2==y))|((tab.group1==y)&(tab.group2==x))]
            return float(r['p-adj'].iloc[0]) if len(r) else np.nan
        cns.append(dict(measurand=meas,group=g,n=len(dd),mean=dd.value.mean(),sd=dd.value.std(ddof=1),
                        tukey_p_vs_PBS=padj(g,'PBS') if g!='PBS' else np.nan, tukey_p_vs_Sham=padj(g,'Sham') if g!='Sham' else np.nan,
                        anova_p=an.pvalue,cells=f"{dd.cell.iloc[0]}..{dd.cell.iloc[-1]}"))
CN=pd.DataFrame(cns); CN.to_csv('/tmp/work/tables/cns_S10A.csv',index=False); print(CN.round(4).to_string(index=False))

# ---- S08-A dose response: Emax/Hill fits on group data ----
def hill(D,E0,Emax,ED50,h): return E0+Emax*D**h/(ED50**h+D**h)
dr=[]; fits={}
for g in ['CMP-204','PSLN-212','PSLN-344','PSLN-344/R848']:
    d=C[(C.block=='S08-A')&(C.group==g)]; D=d.time.astype(float).values; Y=d.value.values
    p0=[1,Y.max(),10,1.5]
    try:
        popt,_=curve_fit(hill,D,Y,p0=p0,bounds=([0,0,0.1,0.3],[5,500,200,6]),maxfev=20000)
    except Exception as e: popt=[np.nan]*4
    # bootstrap within dose
    bs=[]
    for _ in range(1000):
        idx=np.concatenate([rng.choice(np.where(D==dd)[0],3) for dd in np.unique(D)])
        try:
            pb,_=curve_fit(hill,D[idx],Y[idx],p0=popt,bounds=([0,0,0.1,0.3],[5,500,200,6]),maxfev=20000); bs.append(pb)
        except: pass
    bs=np.array(bs); fits[g]=popt
    means={dd:Y[D==dd].mean() for dd in np.unique(D)}
    dr.append(dict(formulation=g,E0=popt[0],Emax=popt[1],Emax_lo=np.percentile(bs[:,1],2.5),Emax_hi=np.percentile(bs[:,1],97.5),
                   top=popt[0]+popt[1],ED50=popt[2],ED50_lo=np.percentile(bs[:,2],2.5),ED50_hi=np.percentile(bs[:,2],97.5),hill=popt[3],
                   **{f'mean_{int(k)}ug':v for k,v in means.items()}))
DR=pd.DataFrame(dr)
# dose of PSLN-344 matching PSLN-212 response at 40 ug (from fitted curve)
target=DR.set_index('formulation').loc['PSLN-212','mean_40ug']
E0,Em,ED,h=fits['PSLN-344']
x=(target-E0)/Em; d_match=ED*(x/(1-x))**(1/h)
DR['note']=''; DR.loc[DR.formulation=='PSLN-344','note']=f"PSLN-344 dose matching PSLN-212 @40ug ({target:.1f}-fold): {d_match:.1f} ug (fitted)"
DR.to_csv('/tmp/work/tables/dose_response_S08A.csv',index=False); print(DR.round(2).to_string(index=False))

# ---- S08-D reactogenicity (post-vaccination body weight, no challenge) ----
d=B[B.block=='S08-D']
nad=d[d.day>0].groupby(['group','animal']).value.min().reset_index()
rg=[]
for g,dd in nad.groupby('group',sort=False):
    last=d[(d.group==g)&(d.day==10)]
    rg.append(dict(group=g,n=len(dd),mean_nadir=dd.value.mean(),sd=dd.value.std(ddof=1),min_nadir=dd.value.min(),
                   n_gt10pct_loss=int((dd.value<90).sum()),n_present_d10=len(last)))
RG=pd.DataFrame(rg)
tk=pairwise_tukeyhsd(nad.value,nad.group); tab=pd.DataFrame(tk.summary().data[1:],columns=tk.summary().data[0])
RG['tukey_p_vs_Vaccine']=[float(tab[((tab.group1==g)&(tab.group2=='Vaccine'))|((tab.group2==g)&(tab.group1=='Vaccine'))]['p-adj'].iloc[0]) if g!='Vaccine' else np.nan for g in RG.group]
RG.to_csv('/tmp/work/tables/reactogenicity_S08D.csv',index=False); print(RG.round(3).to_string(index=False))
