import pandas as pd, numpy as np, warnings
from scipy import stats, optimize
warnings.filterwarnings('ignore')
vals = pd.read_csv('values_corrected.csv')
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',70)
def grp(block, g, time=None, analyte=None):
    d = vals[(vals.block==block)&(vals.group==g)]
    if time is not None: d = d[d.time.astype(str)==str(time)]
    if analyte is not None: d = d[d.analyte==analyte]
    return d
rows=[]
def contrast(label, block, g1, g0, time=None, analyte=None, log=False, interp=''):
    a = grp(block,g1,time,analyte); b = grp(block,g0,time,analyte)
    x = np.log10(a.value) if log else a.value; y = np.log10(b.value) if log else b.value
    t,p = stats.ttest_ind(x,y,equal_var=False)
    if log: eff = f"{10**(x.mean()-y.mean()):.2f}x"
    else: eff = f"{x.mean()-y.mean():+.2f} ({100*(x.mean()/y.mean()-1):+.0f}%)"
    rows.append(dict(experiment=label, block=block, arm=f"{g1} (n={len(a)})", comparator=f"{g0} (n={len(b)})",
                     arm_mean=round(a.value.mean(),3), comp_mean=round(b.value.mean(),3), effect=eff, welch_p=p, interpretation=interp,
                     cells=f"{a.cell.iloc[0]}..{a.cell.iloc[-1].split('!')[1]} vs {b.cell.iloc[0]}..{b.cell.iloc[-1].split('!')[1]}"))
contrast('Surfactant-mimetic carrier drives AECII uptake','S01-B','AECII/PSLN-SRB','AECII/FreeSRB', interp='liposome vs free dye, AECII')
contrast('Surfactant-mimetic carrier drives AECI uptake','S01-B','AECI/PSLN-SRB','AECI/FreeSRB', interp='liposome vs free dye, AECI')
contrast('AECII > AECI uptake of PSLN','S01-B','AECII/PSLN-SRB','AECI/PSLN-SRB')
contrast('AM uptake requires SP-A/SP-D','S01-C','WT','SPA/D', interp='Sftpa1-/-Sftpd-/- vs WT, DiD+ AM')
contrast('Mn2+ particle: AECII uptake','S08-C','AECII-PSLN-344-SRB','AECII-PSLN-SRB', interp='Mn particle vs Mn-free particle')
contrast('Mn2+ particle: AECI uptake','S08-C','AECI-PSLN-344-SRB','AECI-PSLN-SRB')
contrast('GM-CSF rescues PSLN-212 in aged','S02-G','PSLN-212+GM-CSF','PSLN-212', interp='Ly6C+CD11c+MHC-II+ moDC-like, d5')
contrast('GM-CSF alone','S02-G','GM-CSF','PSLN-212')
contrast('moDC differentiation needs IFNAR (no cDC precursors)','S02-H','WT w/o cDC','IFN w/o cDC', interp='WT vs Ifnar-/- BM, CD135+ removed')
contrast('moDC differentiation needs IFNAR (with cDC precursors)','S02-H','WT w/ cDC','IFN w/ cDC')
contrast('GM-CSF partially rescues Ifnar-/-','S02-H','GMCSF','IFN w/o cDC')
contrast('GM-CSF rescue vs WT','S02-H','GMCSF','WT w/o cDC')
contrast('Monocyte recruitment only partly IFNAR-dependent','S12-A','WT to WT','IFNAR-/- to WT', interp='young recipients, n=3')
contrast('CCR2 blockade: lung monocytes','S07-B','PSLN-344+INCB3344','PSLN-344', analyte='monocytes')
contrast('CCR2 blockade: Ly6C+ macrophages','S07-B','PSLN-344+INCB3344','PSLN-344', analyte='Ly6C+ macrophages')
contrast('CCR2 blockade: lung GZMB+ CD8 (young)','S02-I','PSLN-344(Y)+INCB3344','PSLN-344(Y)')
contrast('Gap-junction blockade (CBX): recruited monocytes','S11-C','CBX+','CBX-')
contrast('PTX (Gi/CCR7) blocks MLN priming of OT-I','S05-C','MLN+PTX','MLN', interp='PSLN-344 + OVA, C57BL/6')
contrast('PTX does not block lung OT-I proliferation','S05-C','Lung+PTX','Lung')
contrast('PTX blocks antigen+ DC arrival in MLN','S02-C','PTX','PSLN-344', interp='adjuvant/age of PTX group not stated')
contrast('PTX blocks MLN-DC priming of OT-I','S02-E','PTX','PSLN-344')
contrast('Aicda (class switch) d5','S03-L_Aicda','PSLN-344','PSLN-212', log=True)
contrast('E47 d5','S03-L_E47','PSLN-344','PSLN-212', log=True)
contrast('Lung Ly6C+CCR2+ macrophages d5 (x10^5)','S07-A','PSLN-344','PSLN-212', time=5)
contrast('Lung Ly6C+CCR2+ macrophages d10 (x10^5)','S07-A','PSLN-344','PSLN-212', time=10)
contrast('Lung Ly6C+CCR2+ macrophages d30 (x10^5)','S07-A','PSLN-344','PSLN-212', time=30)
contrast('Encapsulation efficiency','S08-B','PSLN-344','PSLN-212')
contrast('Macrophage transfer -> lung Treg (columns identically labelled)','S07-C','Ly6C-CD206+ MΦ [col B]','Ly6C-CD206+ MΦ [col C]', interp='UNINTERPRETABLE: both columns carry the same label')
m = pd.DataFrame(rows); print(m.drop(columns=['cells']).to_string()); m.to_csv('/tmp/outputs/analysis/T9_mechanism_perturbations.csv', index=False)

# ---- dose response (S08-A): Hill/Emax fit per formulation ----
d = vals[vals.block=='S08-A'].copy(); d['dose']=d.time.astype(float)
def hill(x, e0, emax, ec50, h): return e0 + emax*x**h/(ec50**h + x**h)
fits=[]
for g in ['CMP-204','PSLN-212','PSLN-344','PSLN-344/R848']:
    x = d[d.group==g]
    try:
        p,cov = optimize.curve_fit(hill, x.dose, x.value, p0=[1, x.value.max(), 10, 1.5], bounds=([0,0,0.1,0.3],[5,500,200,6]), maxfev=20000)
        se = np.sqrt(np.diag(cov))
    except Exception as ex:
        p = [np.nan]*4; se=[np.nan]*4
    means = x.groupby('dose').value.mean()
    fits.append(dict(formulation=g, **{f'mean@{int(k)}ug':round(v,1) for k,v in means.items()}, Emax_fit=round(p[0]+p[1],1), EC50_ug=f"{p[2]:.1f} (SE {se[2]:.1f})", hill=round(p[3],2)))
f = pd.DataFrame(fits); print('\nS08-A Ifnb1 dose-response (fold vs untreated, 16 h, n=3/dose):'); print(f.to_string())
f.to_csv('/tmp/outputs/analysis/T10_dose_response.csv', index=False)
# dose of PSLN-344 that matches PSLN-212 at 20 ug (interpolation on fitted curve)
x344 = d[d.group=='PSLN-344']; p344,_ = optimize.curve_fit(hill, x344.dose, x344.value, p0=[1,50,10,1.5], bounds=([0,0,0.1,0.3],[5,500,200,6]), maxfev=20000)
target = d[(d.group=='PSLN-212')&(d.dose==20)].value.mean()
dose_eq = optimize.brentq(lambda z: hill(z,*p344)-target, 0.5, 40)
print(f'PSLN-212 @20ug mean = {target:.1f}; PSLN-344 dose giving same Ifnb1 = {dose_eq:.1f} ug -> potency ratio ~{20/dose_eq:.1f}x')
