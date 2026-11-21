import pandas as pd, numpy as np
md=open('/tmp/outputs/PSLN_portfolio_proposal.md').read()
T='/tmp/work/tables/'
CON=pd.read_csv(T+'continuous_contrasts.csv'); CON['time']=CON['time'].astype(str)
SUM=pd.read_csv(T+'continuous_summary.csv'); SUM['time']=SUM['time'].astype(str)
SPL=pd.read_csv(T+'survival_pooled.csv'); GAP=pd.read_csv(T+'age_gap_curated.csv'); MEC=pd.read_csv(T+'mechanism_tests.csv')
CNS=pd.read_csv(T+'cns_S10A.csv'); RG=pd.read_csv(T+'reactogenicity_S08D.csv'); DR=pd.read_csv(T+'dose_response_S08A.csv'); SS=pd.read_csv(T+'sample_size_planning.csv')
def c(b,ct,t=None):
    d=CON[(CON.block==b)&(CON.contrast==ct)]
    if t is not None: d=d[d.time==str(t)]
    return d.iloc[0]
checks=[]
def chk(label, s): checks.append((label, s, s in md))
pr=SPL[SPL.analysis.str.startswith('PRIMARY')].iloc[0]
chk('HR primary', f"{pr.cox_HR:.3f} (95% CI {pr.HR_lo:.3f}–{pr.HR_hi:.3f})")
chk('RD primary', f"{100*pr.MH_RD_death:.0f} percentage points (95% CI {100*pr.RD_lo:.0f} to {100*pr.RD_hi:.0f})")
for pre in ['Sens-1','Sens-2','Sens-4']: chk(pre, f"HR {SPL[SPL.analysis.str.startswith(pre)].iloc[0].cox_HR:.3f}")
for pre in ['Challenge 14','Challenge 2-3','Heterosubtypic','Challenge 60']:
    r=SPL[SPL.analysis.str.startswith(pre)].iloc[0]; chk(pre, f"{r.surv_344} vs {r.surv_212}")
x=c('S01-A','PSLN-344 vs PSLN-212','16h'); chk('Ifnb1 344', f"{x.mean_a:.1f}-fold"); chk('Ifnb1 212', f"{x.mean_b:.1f}-fold"); chk('Ifnb1 GMR', f"GMR {x.est:.2f}, {x.lo:.2f}–{x.hi:.2f}")
chk('Ifnb1 Y', f"{SUM[(SUM.block=='S01-A')&(SUM.group=='PSLN-212(Y)')&(SUM.time=='16h')].gmean.iloc[0]:.1f}-fold")
x=c('S02-F','PSLN-344 vs PSLN-212','36h'); chk('Gm-csf', f"observed {x.est:.2f}, {x.lo:.2f}–{x.hi:.2f}")
x=c('S03-C','PSLN-344 vs PSLN-212'); chk('HAI CA09 GMR', f"observed {x.est:.1f}, {x.lo:.1f}–{x.hi:.1f}")
chk('HAI 368 vs 46', f"HAI GMT 46 vs 368")
x=c('S05-F','PSLN-344 vs PSLN-212','d14'); chk('IFNg ratio', f"observed {x.mean_a/x.mean_b:.1f}×")
med=GAP.gap_closed.median(); q1,q3=GAP.gap_closed.quantile([.25,.75]); chk('gap median', f"**{100*med:.0f}%** (IQR {100*q1:.0f}–{100*q3:.0f}%)")
m=MEC.set_index('question')
chk('AECII', f"AECII 15.8% vs AECI 3.8%"); chk('AM', f"43.1% WT vs 12.7%")
r=m.loc['Gap-junction blockade (carbenoxolone) reduces monocyte recruitment']; chk('CBX', f"{r.mean_b:.1f}% vs {r.mean_a:.1f}% (p={r.student_p:.3f})")
r=m.loc['moDC generation requires IFNAR (cDC-depleted BM)']; chk('IFNAR', f"IFNAR-KO BM moDC {r.mean_b:.1f}% vs {r.mean_a:.1f}%")
r=m.loc['CCR2 blockade abolishes lung GZMB+ CD8 (young)']; chk('INCB GZMB', f"{r.mean_a:.1f}% → {r.mean_b:.1f}%")
for meas,pv in [('CNS Ifnb1 (fold)',0.87),('CNS Tnf (fold)',0.54),('CNS Isg15 (fold)',0.96)]:
    v=CNS[(CNS.measurand==meas)&(CNS.group=='PSLN-344')].tukey_p_vs_PBS.iloc[0]; checks.append((meas, f"{v:.2f}", abs(v-pv)<0.005))
r=RG.set_index('group'); chk('nadir 344', f"{r.loc['PSLN-344','mean_nadir']:.1f}%"); chk('nadir vac', f"{r.loc['Vaccine','mean_nadir']:.1f}%"); chk('nadir R848', f"{r.loc['PSLN-212/R848','mean_nadir']:.1f}%")
d=DR.set_index('formulation'); chk('top 344', f"top {d.loc['PSLN-344','top']:.0f}×"); chk('top 212', f"{d.loc['PSLN-212','top']:.0f}×")
for _,rr in SS.iterrows():
    if rr.comparison.startswith('survival 70'): chk('n surv', '90% power for 70% vs 20%')
    if rr.comparison=='HAI NI vs benchmark, margin 1.5-fold': chk('n NI', f"{rr.n_per_arm}/arm for 90% power")
chk('d60 vs young', '14/21 aged animals vs 21/21 young (p=0.009)'); chk('bg', '(17/21 survived; p=0.48)')
chk('212 vs sham', '7/59 vs 1/59, p=0.061'); chk('nadir surv', '87.3% vs 89.8% (p=0.0035)')
chk('EE', 'current 54.8% ± 5.1'); chk('8ug', 'about 8 µg of PSLN-344')
bad=[x for x in checks if not x[2]]
print(f"{len(checks)-len(bad)}/{len(checks)} checks found in text")
for b in bad: print('MISSING:',b)
