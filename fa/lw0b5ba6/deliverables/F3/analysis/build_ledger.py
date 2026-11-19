"""
Evidence ledger.  Every number used in the proposal is (re)computed here DIRECTLY from the cited workbook cells
(independently of the tidy parser), checked against the analysis outputs, and written to ledger.json / ledger.csv.
If a recomputed value disagrees with the analysis CSV the script stops.
"""
import json, math, re, numpy as np, pandas as pd, openpyxl
from openpyxl.utils import range_boundaries, get_column_letter
from scipy import stats
from statsmodels.stats.proportion import proportion_confint
wb=openpyxl.load_workbook('/tmp/world/filesystem/psln_program_dataset.xlsx')

def raw(ref):
    """'S03!D3:D7' -> list of numeric cell values (blanks skipped). Several ranges may be joined with ';'."""
    out=[]
    for part in ref.split(';'):
        part=part.strip(); sh,rng=part.split('!')
        if ':' not in rng: rng=rng+':'+rng
        c1,r1,c2,r2=range_boundaries(rng)
        for r in range(r1,r2+1):
            for c in range(c1,c2+1):
                v=wb[sh].cell(r,c).value
                if isinstance(v,(int,float)): out.append(float(v))
    return out
def mean(ref): return float(np.mean(raw(ref)))
def sd(ref): return float(np.std(raw(ref),ddof=1))
def gmean(ref,floor=None):
    v=np.array(raw(ref)); 
    if floor is not None: v=np.where(v<=0,floor,v)
    return float(np.exp(np.log(v).mean()))
def gmean_log10(ref): return float(10**np.mean(raw(ref)))      # cells already hold log10 values (S09-A)
def surv(ref):
    v=raw(ref); return int(sum(1 for x in v if x==0)), len(v)
def cp(k,n):
    lo,hi=proportion_confint(k,n,method='beta'); return 100*lo,100*hi
def welch(a,b,log=None):
    a=np.array(raw(a) if isinstance(a,str) else a); b=np.array(raw(b) if isinstance(b,str) else b)
    if log=='log10': a,b=np.log10(a),np.log10(b)
    if log=='log2': a,b=np.log2(np.where(a<=0,5,a)),np.log2(np.where(b<=0,5,b))
    t=stats.ttest_ind(a,b,equal_var=False); d=a.mean()-b.mean()
    se=math.sqrt(a.var(ddof=1)/len(a)+b.var(ddof=1)/len(b)); df=se**4/((a.var(ddof=1)/len(a))**2/(len(a)-1)+(b.var(ddof=1)/len(b))**2/(len(b)-1)); h=stats.t.ppf(.975,df)*se
    if log: base=10 if log=='log10' else 2; return dict(est=base**d,lo=base**(d-h),hi=base**(d+h),p=float(t.pvalue))
    return dict(est=d,lo=d-h,hi=d+h,p=float(t.pvalue))
def pf(p):
    if p<0.0001: 
        e=int(math.floor(math.log10(p))); m=p/10**e
        return f'{m:.1f}e{e}'
    if p<0.001: return f'{p:.4f}'
    if p<0.01: return f'{p:.3f}'
    return f'{p:.2f}' if p>=0.095 else f'{p:.3f}'

per=pd.read_csv('survival_per_experiment.csv'); pooled=pd.read_csv('survival_pooled.csv'); tests=pd.read_csv('survival_tests.csv')
imm=pd.read_csv('immunology_descriptives.csv'); con=pd.read_csv('immunology_contrasts.csv'); ri=pd.read_csv('immunology_restoration_index.csv')
tcd=pd.read_csv('timecourse_descriptives.csv'); tcc=pd.read_csv('timecourse_contrasts.csv')
F={}; L=[]
def add(id_,section,statement,cells,analysis,method=''):
    L.append(dict(id=id_,section=section,statement=statement,cells=cells,analysis=analysis,method=method))
def C(block,g1,g2):   # contrast row from analysis_02
    r=con[(con.block==block)&(con.g1==g1)&(con.g2==g2)]
    assert len(r)==1,(block,g1,g2); return r.iloc[0]
def cells(block,group):
    r=imm[(imm.block==block)&(imm.group==group)]; assert len(r)==1,(block,group); return r.cells.iloc[0]
def chk(a,b,tol=1e-6): assert abs(a-b)<=tol*max(1,abs(b)),(a,b)

# ======================================================================================================
# SURVIVAL
AGED=['S03-I','S03-J','S06-A','S06-B','S06-D','S06-E(r34)','S06-F(r34)','S06-G','S15-L','S15-N']      # S06-C excluded (identical to S06-D)
sheet_of={'S03-I':'S03','S03-J':'S03','S06-A':'S06','S06-B':'S06','S06-C':'S06','S06-D':'S06','S06-E(r34)':'S06','S06-F(r34)':'S06','S06-G':'S06','S06-E(r71)':'S06','S06-F(r71)':'S06',
          'S15-H':'S15','S15-L':'S15','S15-N':'S15','S09-B':'S09','S09-D':'S09','S09-F':'S09','S13-E':'S13'}
def arm_ref(block,arm):
    r=per[(per.block==block)&(per.arm==arm)]
    if len(r)==0: return None
    return f"{sheet_of[block]}!{r.group_cells.iloc[0]}"
def pool(blocks,arm):
    refs=[arm_ref(b,arm) for b in blocks]; refs=[r for r in refs if r]
    k=n=0
    for r in refs:
        a,b=surv(r); k+=a; n+=b
    return k,n,'; '.join(refs)
for arm,key in [('PSLN-344','p344'),('PSLN-212','p212'),('Sham','psham'),('PSLN-212(Y)','pyoung')]:
    k,n,refs=pool(AGED,arm); lo,hi=cp(k,n); F[key]=dict(k=k,n=n,pct=100*k/n,lo=lo,hi=hi,refs=refs)
row=pooled[pooled.analysis.str.startswith('B.')].iloc[0]
assert row.arm1_surv==f"{F['p344']['k']}/{F['p344']['n']}" and row.arm2_surv==f"{F['p212']['k']}/{F['p212']['n']}"
F['rd']=dict(rd=row.MH_risk_diff_pct,newcombe=row.newcombe_rd_ci,mh=row.MH_rd_ci,chi2=row.CMH_chi2,p=row.CMH_p)
for key,id_,name in [('p344','L01','vaccine + PSLN-344'),('p212','L02','vaccine + PSLN-212 (same drug and liposome, no manganese)'),('psham','L03','vaccine + empty liposome ("Sham")'),('pyoung','L04','')]:
    f=F[key]; scope=('Survival of young animals given PSLN-212 in the nine aged-animal experiments that include a young arm (S03-J has none; S06-C excluded)' if key=='pyoung' else f'Pooled survival of aged (20 months or more) animals after lethal challenge, {name}, ten experiments (S06-C excluded)')
    add(id_,'Survival',f"{scope}: {f['k']}/{f['n']} ({f['pct']:.1f}%; exact 95% CI {f['lo']:.0f}-{f['hi']:.0f}%).",
                 f['refs'],'analysis_01_survival.py -> survival_per_experiment.csv, survival_pooled.csv (row B)','Count of animals flagged 0 (alive at end of observation) over all animals listed; Clopper-Pearson interval.')
add('L05','Survival',f"Difference in pooled survival, PSLN-344 minus PSLN-212: {F['rd']['rd']:.0f} percentage points (Newcombe 95% CI {F['rd']['newcombe']}; Mantel-Haenszel {F['rd']['mh']}); Cochran-Mantel-Haenszel chi2 {F['rd']['chi2']:.1f}, p = {pf(F['rd']['p'])}. Within single experiments the exact log-rank p ranges from {tests[(tests.arm1=='PSLN-344')&(tests.arm2=='PSLN-212')&tests.block.isin(AGED)].logrank_p_exact.min():.4f} to {tests[(tests.arm1=='PSLN-344')&(tests.arm2=='PSLN-212')&tests.block.isin(AGED)].logrank_p_exact.max():.3f}.",
    F['p344']['refs']+' | '+F['p212']['refs'],'analysis_01_survival.py -> survival_pooled.csv (row B), survival_tests.csv','Experiments are strata. Per-experiment p: exact permutation log-rank (all allocations enumerated).')
sens=pd.read_csv('survival_sensitivity.csv')
a=sens[sens.scenario.str.startswith('ADVERSE BOUND excl. S06-C: fewest')].iloc[0]; b=sens[sens.scenario.str.startswith('ADVERSE BOUND excl. S06-C: most')].iloc[0]; cfp=sens[sens.scenario.str.startswith('ADVERSE BOUND: PSLN-344 vs')].iloc[0]
F['adverse']=dict(a=a.surv,apct=a.pct,b=b.surv,bpct=b.pct,p=cfp.fisher_p)
add('L06','Survival',f"Adverse-bound sensitivity (for each experiment take the larger PSLN-344 death count and the smaller PSLN-212 death count from either the survival table or its body-weight table): {a.surv} ({a.pct:.0f}%) vs {b.surv} ({b.pct:.0f}%); Fisher p = {pf(cfp.fisher_p)}.",
    'survival blocks as L01/L02 plus weight blocks S13-F, S13-G, S15-A, S15-B, S15-D, S15-E, S15-F, S15-G, S15-M, S15-O','audit_02_survival_vs_weight.py -> weights_decoded_per_animal.csv; analysis_07 -> survival_sensitivity.csv, survival_table_vs_weight_by_arm.csv','Weight tables decoded as described in audit_02 (blank = gone; terminal constant run = gone).')
STRICT=['S06-A','S06-B','S06-D','S06-E(r34)','S06-F(r34)','S06-G']
F['strict']={a:pool(STRICT,a)[:2] for a in ['PSLN-344','PSLN-212']}
add('L06b','Survival',f"Strictest subset: the six aged BALB/c experiments with neither a duplicated table, a group-label conflict nor reused animal trajectories in the PSLN-344 arm (S06-A, S06-B, S06-D, S06-E, S06-F, S06-G): PSLN-344 {F['strict']['PSLN-344'][0]}/{F['strict']['PSLN-344'][1]} vs PSLN-212 {F['strict']['PSLN-212'][0]}/{F['strict']['PSLN-212'][1]}; Fisher p = {pf(stats.fisher_exact([[F['strict']['PSLN-344'][0],F['strict']['PSLN-344'][1]-F['strict']['PSLN-344'][0]],[F['strict']['PSLN-212'][0],F['strict']['PSLN-212'][1]-F['strict']['PSLN-212'][0]]])[1])}. These are the same six experiments as the different-subtype set (L09b).",
    pool(STRICT,'PSLN-344')[2]+' | '+pool(STRICT,'PSLN-212')[2],'build_ledger.py (counts from survival_per_experiment.csv)')
w=sens[(sens.source=='implied by body-weight tables')&(sens.scenario.str.startswith('excluding S06-C'))]
F['wt344']=w[w.arm=='PSLN-344'].surv.iloc[0]; F['wt212']=w[w.arm=='PSLN-212'].surv.iloc[0]
add('L07','Survival',f"Survival implied by the body-weight tables alone (same ten experiments): PSLN-344 {F['wt344']}; PSLN-212 {F['wt212']} (S03-J cannot be mapped because its weight table S13-G carries different group labels).",
    'S13!B33:AJ40; S13!B43:AE50; S15!B3:AC10; S15!B13:AC20; S15!B33:AC40; S15!B43:AJ50; S15!B53:AJ60; S15!B63:AJ70; S15!I103:AJ110; S15!I134:AJ141','audit_02 -> weights_decoded_per_animal.csv; analysis_07 -> survival_sensitivity.csv')
# windows
def win(blocks,arm,extra=None):
    refs=[arm_ref(b,arm) for b in blocks]; refs=[r for r in refs if r]
    if extra: refs+=extra
    k=n=0
    for r in refs:
        a_,b_=surv(r); k+=a_; n+=b_
    return dict(k=k,n=n,pct=100*k/n,lo=cp(k,n)[0],hi=cp(k,n)[1],refs='; '.join(refs))
early=['S03-J','S06-B','S06-D']
F['early344']=win(early,'PSLN-344',[arm_ref('S15-H','3d Vaccine+PSLN-344')]); F['early212']=win(early,'PSLN-212'); F['earlysham']=win(early,'Sham')
add('L08','Survival',f"Challenge 2-3 days after a single dose (S03-J, S06-B, S06-D, S15-H): PSLN-344 {F['early344']['k']}/{F['early344']['n']} ({F['early344']['pct']:.0f}%; CI {F['early344']['lo']:.0f}-{F['early344']['hi']:.0f}%); PSLN-212 {F['early212']['k']}/{F['early212']['n']}; Sham {F['earlysham']['k']}/{F['earlysham']['n']}.",
    F['early344']['refs']+' | '+F['early212']['refs']+' | '+F['earlysham']['refs'],'analysis_01 -> survival_by_window.csv')
F['d14_344']=win(['S03-I','S06-A'],'PSLN-344'); F['d14_212']=win(['S03-I','S06-A'],'PSLN-212')
add('L09','Survival',f"Challenge at day 14 (S03-I, S06-A; S06-C excluded): PSLN-344 {F['d14_344']['k']}/{F['d14_344']['n']}; PSLN-212 {F['d14_212']['k']}/{F['d14_212']['n']}.",F['d14_344']['refs']+' | '+F['d14_212']['refs'],'analysis_01 -> survival_by_window.csv')
late=['S06-E(r34)','S06-F(r34)','S06-G']
for arm,key in [('PSLN-344','d60_344'),('PSLN-212','d60_212'),('Sham','d60_sham'),('PSLN-212(Y)','d60_y'),('Untreated','d60_un')]: F[key]=win(late,arm)
add('L10','Survival',f"Challenge at day 60 (S06-E, S06-F, S06-G at rows 34-105): PSLN-344 {F['d60_344']['k']}/{F['d60_344']['n']} ({F['d60_344']['pct']:.0f}%; CI {F['d60_344']['lo']:.0f}-{F['d60_344']['hi']:.0f}%); PSLN-212 {F['d60_212']['k']}/{F['d60_212']['n']}; Sham {F['d60_sham']['k']}/{F['d60_sham']['n']}; young PSLN-212 {F['d60_y']['k']}/{F['d60_y']['n']}; untreated, unchallenged age-matched animals {F['d60_un']['k']}/{F['d60_un']['n']} ({F['d60_un']['pct']:.0f}%).",
    ' | '.join(F[k]['refs'] for k in ['d60_344','d60_212','d60_sham','d60_y','d60_un']),'analysis_01 -> survival_by_window.csv, survival_pooled.csv (rows H, I, J)')
k1=F['early344']['k']+F['d14_344']['k']; n1=F['early344']['n']+F['d14_344']['n']
pw=stats.fisher_exact([[k1,n1-k1],[F['d60_344']['k'],F['d60_344']['n']-F['d60_344']['k']]])[1]
pu=stats.fisher_exact([[F['d60_344']['k'],F['d60_344']['n']-F['d60_344']['k']],[F['d60_un']['k'],F['d60_un']['n']-F['d60_un']['k']]])[1]
py=stats.fisher_exact([[F['d60_344']['k'],F['d60_344']['n']-F['d60_344']['k']],[F['d60_y']['k'],F['d60_y']['n']-F['d60_y']['k']]])[1]
F['wane']=dict(k1=k1,n1=n1,p=pw,p_untreated=pu,p_young=py)
add('L11','Survival',f"Durability: PSLN-344 survival when challenged within 14 days {k1}/{n1} ({100*k1/n1:.0f}%) vs at day 60 {F['d60_344']['k']}/{F['d60_344']['n']} ({F['d60_344']['pct']:.0f}%), Fisher p = {pf(pw)}; day-60 PSLN-344 vs young PSLN-212, p = {pf(py)}; day-60 PSLN-344 vs untreated unchallenged, p = {pf(pu)}.",
    F['early344']['refs']+'; '+F['d14_344']['refs']+' | '+F['d60_344']['refs']+' | '+F['d60_un']['refs'],'build_ledger.py (Fisher exact on the counts of L08-L10)')
F['h5']={a:dict(zip(['k','n'],surv(arm_ref('S03-J',a)))) for a in ['PSLN-344','PSLN-212','Sham']}
add('L12','Survival',f"Wild-type VN04 H5N1 challenge 2 days after one dose of rgH5N1 vaccine (S03-J): PSLN-344 {F['h5']['PSLN-344']['k']}/{F['h5']['PSLN-344']['n']} alive (one of these rows, J46, has no day recorded; block label says n=9); PSLN-212 {F['h5']['PSLN-212']['k']}/{F['h5']['PSLN-212']['n']}; Sham {F['h5']['Sham']['k']}/{F['h5']['Sham']['n']}. The paired weight table S13-G labels its three groups PSLN-344, Sham, Naive.",
    'S03!G17:J46; S13!B43:AE50','analysis_01 -> survival_per_experiment.csv; audit_02')
F['homo']={a:dict(zip(['k','n'],surv(arm_ref('S03-I',a)))) for a in ['PSLN-344','PSLN-212','Sham','CMP-204','PSLN-212(Y)']}
add('L13','Survival',f"Homologous 10x mLD50 CA09 H1N1 challenge at day 14 (S03-I): PSLN-344 {F['homo']['PSLN-344']['k']}/7; PSLN-212 {F['homo']['PSLN-212']['k']}/7; CMP-204 {F['homo']['CMP-204']['k']}/7; Sham {F['homo']['Sham']['k']}/7; young PSLN-212 {F['homo']['PSLN-212(Y)']['k']}/7. The paired weight table S13-F shows 3 of 7 'PSLN-212' animals recovering, has a Naive group and no CMP-204 group.",
    'S03!A17:F51; S13!B33:AJ40','analysis_01; audit_02 -> audit_02_survival_vs_weight.csv')
F['b6']={a:surv(arm_ref('S15-L',a)) for a in ['PSLN-344','PSLN-212','Sham','PSLN-212(Y)']}; F['sw']={a:surv(arm_ref('S15-N',a)) for a in ['PSLN-344','PSLN-212','Sham','PSLN-212(Y)']}
add('L14','Survival',f"Other genetic backgrounds, 20-month animals: C57BL/6 (S15-L) PSLN-344 {F['b6']['PSLN-344'][0]}/7 vs PSLN-212 {F['b6']['PSLN-212'][0]}/7 vs Sham {F['b6']['Sham'][0]}/7; outbred Swiss Webster (S15-N) {F['sw']['PSLN-344'][0]}/7 vs {F['sw']['PSLN-212'][0]}/7 vs {F['sw']['Sham'][0]}/7. Challenge virus, dose and day are not stated for these two blocks.",
    'S15!A103:E130; S15!A134:E161','analysis_01 -> survival_per_experiment.csv, survival_tests.csv')
im={}
for b in ['S06-E(r71)','S06-F(r71)']:
    for a in ['Naive+PSLN-212','Imprinting+PSLN-212','Naive+PSLN-344','Imprinting+PSLN-344']: im[(b,a)]=surv(arm_ref(b,a))
F['mid344']=(sum(v[0] for k,v in im.items() if '344' in k[1]),28); F['mid212']=(sum(v[0] for k,v in im.items() if '212' in k[1]),28)
F['imp344']=(sum(v[0] for k,v in im.items() if k[1]=='Imprinting+PSLN-344'),14); F['nai344']=(sum(v[0] for k,v in im.items() if k[1]=='Naive+PSLN-344'),14)
F['nai212']=(sum(v[0] for k,v in im.items() if k[1]=='Naive+PSLN-212'),14); F['imp212_pr8']=im[('S06-E(r71)','Imprinting+PSLN-212')]; F['imp212_perth']=im[('S06-F(r71)','Imprinting+PSLN-212')]
rowG=pooled[pooled.analysis.str.startswith('G.')].iloc[0]; assert rowG.arm1_surv==f"{F['mid344'][0]}/28"
add('L15','Survival',f"14-month animals (10 months + 4 months after PR8 or saline; blocks at S06 rows 69-98, labelled S06-E and S06-F a second time): PSLN-344 {F['mid344'][0]}/28 vs PSLN-212 {F['mid212'][0]}/28 (CMH p = {pf(rowG.CMH_p)}). PSLN-344: previously infected {F['imp344'][0]}/14, infection-naive {F['nai344'][0]}/14. PSLN-212 in naive 14-month animals {F['nai212'][0]}/14; previously infected {F['imp212_pr8'][0]}/7 against PR8 (the imprinting virus) and {F['imp212_perth'][0]}/7 against Perth H3N2.",
    'S06!G70:K98; S06!M70:Q98','analysis_01 -> survival_per_experiment.csv, survival_pooled.csv (row G)')
F['ag']={a:surv(arm_ref('S15-H',a)) for a in ['3d Vaccine','3d PSLN-344','3d Vaccine+PSLN-344']}
t=tests[(tests.block=='S15-H')&(tests.arm1=='3d Vaccine+PSLN-344')&(tests.arm2=='3d PSLN-344')].iloc[0]; t2=tests[(tests.block=='S15-H')&(tests.arm1=='3d PSLN-344')&(tests.arm2=='3d Vaccine')].iloc[0]
add('L16','Survival',f"Antigen requirement (S15-H; dosed 3 days before 5x mLD50 rgH5N1): vaccine alone {F['ag']['3d Vaccine'][0]}/7; PSLN-344 alone {F['ag']['3d PSLN-344'][0]}/7; vaccine + PSLN-344 {F['ag']['3d Vaccine+PSLN-344'][0]}/7 (combination vs PSLN-344 alone: Fisher p = {pf(t.fisher_p)}, exact log-rank p = {pf(t.logrank_p_exact)}; PSLN-344 alone vs vaccine alone: exact log-rank p = {pf(t2.logrank_p_exact)}).",
    'S15!A73:D93','analysis_01 -> survival_tests.csv')
y={b:{a:surv(arm_ref(b,a)) for a in ['PSLN-344(Y)','PSLN-212(Y)','Sham']} for b in ['S09-B','S09-D','S09-F']}
F['y344']=(sum(y[b]['PSLN-344(Y)'][0] for b in y),sum(y[b]['PSLN-344(Y)'][1] for b in y)); F['y212']=(sum(y[b]['PSLN-212(Y)'][0] for b in y),sum(y[b]['PSLN-212(Y)'][1] for b in y)); F['ysham']=(sum(y[b]['Sham'][0] for b in y),sum(y[b]['Sham'][1] for b in y))
F['y13']={a:surv(arm_ref('S13-E',a)) for a in ['PSLN-344(Y)','CMP-204(Y)','Sham','Naive']}
add('L17','Survival',f"Young animals: PSLN-344 {F['y344'][0]}/{F['y344'][1]} vs PSLN-212 {F['y212'][0]}/{F['y212'][1]} vs Sham {F['ysham'][0]}/{F['ysham'][1]} across S09-B (H3N2 vaccine, PR8 at day 21), S09-D (H1N1 vaccine, Perth H3N2 at day 21) and S09-F (bivalent vaccine, rgH5N1 at day 180). Homologous challenge S13-E: PSLN-344 {F['y13']['PSLN-344(Y)'][0]}/7, CMP-204 {F['y13']['CMP-204(Y)'][0]}/7, Sham {F['y13']['Sham'][0]}/7, Naive {F['y13']['Naive'][0]}/7.",
    'S09!A12:D35; S09!A39:D62; S09!A66:D88; S13!R3:V30','analysis_01 -> survival_per_experiment.csv, survival_pooled.csv (row K)')
un=F['d60_un']; F['un_dead']=(un['n']-un['k'],un['n'],cp(un['n']-un['k'],un['n']))
add('L18','Survival',f"Background mortality: {F['un_dead'][0]}/{F['un_dead'][1]} untreated, unchallenged 20-month animals died during the three 14-day observation windows (exact 95% CI {F['un_dead'][2][0]:.0f}-{F['un_dead'][2][1]:.0f}%): 1/7 in S06-E, 0/7 in S06-F, 3/7 in S06-G.",un['refs'],'analysis_01 -> survival_per_experiment.csv')
mor=pd.read_csv('challenge_morbidity.csv'); wd=pd.read_csv('weights_decoded_per_animal.csv')
a_blocks=['S13-F','S13-G','S15-A','S15-B','S15-D','S15-E','S15-F','S15-G','S15-M','S15-O']
m344=mor[mor.weight_block.isin(a_blocks)&(mor.group=='PSLN-344')].mean_nadir_survivors; my=mor[mor.weight_block.isin(a_blocks)&(mor.group=='PSLN-212(Y)')].mean_nadir_survivors
F['nadir344']=(m344.min(),m344.max()); F['nadiry']=(my.min(),my.max())
mt=pd.read_csv('challenge_morbidity_tests.csv'); mt=mt[mt.weight_block.isin(a_blocks)&(mt.g1=='PSLN-344')&(mt.g2=='PSLN-212(Y)')]
F['nadirdiff']=(mt['diff'].mean(),len(mt),int((mt['diff']<0).sum()))
add('L19','Survival',f"Morbidity in survivors: lowest body weight actually measured after challenge averaged {F['nadir344'][0]:.1f}-{F['nadir344'][1]:.1f}% of baseline across the ten aged PSLN-344 groups, vs {F['nadiry'][0]:.1f}-{F['nadiry'][1]:.1f}% in young PSLN-212 groups; PSLN-344 survivors lost more weight than young survivors in {F['nadirdiff'][2]} of {F['nadirdiff'][1]} paired experiments (mean difference {F['nadirdiff'][0]:.1f} points).",
    'S13!B33:AC40; S13!B43:K50; S15!B3:AC10; S15!B13:AC20; S15!B33:AC40; S15!B43:AC50; S15!B53:AC60; S15!B63:AC70; S15!I103:AJ110; S15!I134:AJ141','analysis_05_challenge_morbidity.py -> challenge_morbidity.csv, challenge_morbidity_tests.csv','Per-animal nadir over real observations only (carried-forward values of dead animals removed).')
dec=wd[(wd.block.isin(['S15-E','S15-F','S15-G']))&(wd['mode']!='survivor')]
d344=dec[dec.group=='PSLN-344'].last_value; dun=dec[dec.group=='Untreated'].last_value
F['term']=(d344.min(),d344.max(),len(d344),dun.min(),dun.max(),len(dun))
add('L20','Survival',f"Day-60 experiments: the {len(d344)} PSLN-344 animals that leave the weight tables do so at {d344.min():.1f}-{d344.max():.1f}% of baseline weight; the {len(dun)} untreated, unchallenged animals that leave do so at {dun.min():.1f}-{dun.max():.1f}%.",
    'S15!W43:AC50; S15!W53:AC60; S15!W63:AC70; S15!AD43:AJ50; S15!AD53:AJ60; S15!AD63:AJ70','audit_02 -> weights_decoded_per_animal.csv')

HET=['S06-A','S06-B','S06-D','S06-E(r34)','S06-F(r34)','S06-G']
F['het']={a:pool(HET,a)[:2] for a in ['PSLN-344','PSLN-212','Sham','PSLN-212(Y)']}
add('L09b','Survival',f"Experiments in which the challenge virus is of a different subtype from the vaccine (S06-A, S06-B: H3N2 vaccine, PR8 H1N1 challenge; S06-D, S06-F: H1N1+H3N2 vaccine, rgH5N1 challenge; S06-E: H3N2 vaccine, PR8 challenge; S06-G: H1N1 vaccine, Perth H3N2 challenge): PSLN-344 {F['het']['PSLN-344'][0]}/{F['het']['PSLN-344'][1]} ({100*F['het']['PSLN-344'][0]/F['het']['PSLN-344'][1]:.0f}%); PSLN-212 {F['het']['PSLN-212'][0]}/{F['het']['PSLN-212'][1]}; Sham {F['het']['Sham'][0]}/{F['het']['Sham'][1]}; young PSLN-212 {F['het']['PSLN-212(Y)'][0]}/{F['het']['PSLN-212(Y)'][1]}.",
    pool(HET,'PSLN-344')[2]+' | '+pool(HET,'PSLN-212')[2],'analysis_01 -> survival_per_experiment.csv')
rowE=pooled[pooled.analysis.str.startswith('E.')].iloc[0]; F['p212_vs_sham']=dict(rd=rowE.MH_risk_diff_pct,p=rowE.CMH_p)
add('L02b','Survival',f"PSLN-212 vs vaccine + empty liposome in aged animals: {rowE.arm1_surv} vs {rowE.arm2_surv}; difference {rowE.MH_risk_diff_pct:.0f} points (Newcombe 95% CI {rowE.newcombe_rd_ci}); CMH p = {pf(rowE.CMH_p)}.",F['p212']['refs']+' | '+F['psham']['refs'],'analysis_01 -> survival_pooled.csv (row E)')
rowF=pooled[pooled.analysis.str.startswith('F.')].iloc[0]; F['p344_vs_young']=dict(rd=rowF.MH_risk_diff_pct,ci=rowF.newcombe_rd_ci,p=rowF.CMH_p,a=rowF.arm1_surv,b=rowF.arm2_surv)
add('L04b','Survival',f"Aged PSLN-344 vs young PSLN-212 in the nine experiments that contain both: {rowF.arm1_surv} vs {rowF.arm2_surv}; difference {rowF.MH_risk_diff_pct:.0f} points (Newcombe 95% CI {rowF.newcombe_rd_ci}); CMH p = {pf(rowF.CMH_p)}.",'as L01 and L04 without S03-J','analysis_01 -> survival_pooled.csv (row F)')
# ======================================================================================================
# IMMUNOLOGY (aged PSLN-344 vs aged PSLN-212; young PSLN-212 as benchmark)
def trio(key,id_,block,label,scale,unit='%',fmt='{:.1f}',extra='',groups=('PSLN-344','PSLN-212','PSLN-212(Y)'),section='Immunology'):
    g344,g212,gy=groups
    fn={'linear':mean,'log10':gmean,'log2':(lambda r: gmean(r,floor=5))}[scale]
    v=[fn(cells(block,g)) for g in (g344,g212,gy)]
    for g,val in zip((g344,g212,gy),v): chk(val,float(imm[(imm.block==block)&(imm.group==g)].centre_on_test_scale.iloc[0]),1e-6)
    c=C(block,g344,g212); cw=welch(cells(block,g344),cells(block,g212),None if scale=='linear' else scale); chk(cw['p'],c.welch_p,1e-6); chk(cw['est'],c.effect,1e-6)
    r=ri[ri.block==block]; rest=float(r.restoration_pct.iloc[0]) if len(r) else float('nan')
    F[key]=dict(a=v[0],b=v[1],y=v[2],eff=c.effect,lo=c.ci95_lo,hi=c.ci95_hi,p=c.welch_p,tukey=c.tukey_p,rest=rest,n=int(c.n1))
    effs=(f"difference {c.effect:.1f} points (95% CI {c.ci95_lo:.1f} to {c.ci95_hi:.1f})" if scale=='linear' else f"ratio {c.effect:.1f} (95% CI {c.ci95_lo:.1f}-{c.ci95_hi:.1f})")
    stat='mean' if scale=='linear' else 'geometric mean'
    add(id_,section,f"{label}: aged PSLN-344 {fmt.format(v[0])}{unit} vs aged PSLN-212 {fmt.format(v[1])}{unit} (young PSLN-212 {fmt.format(v[2])}{unit}); {effs}; Welch p = {pf(c.welch_p)}, Tukey p = {pf(c.tukey_p)}; n = {int(c.n1)} per group." + (f" Share of the age gap closed: {rest:.0f}%." if rest==rest else '')+extra,
        '; '.join(cells(block,g) for g in (g344,g212,gy)),'analysis_02_immunology.py -> immunology_descriptives.csv, immunology_contrasts.csv, immunology_restoration_index.csv',f"{stat}; tests on the {scale} scale; Tukey from one-way ANOVA over all groups in the block.")
trio('ifnb16','L21','S01-A/16h','Lung Ifnb1 mRNA 16 h after adjuvant alone (fold vs untreated)','log10',unit='x',fmt='{:.1f}')
trio('ifnb72','L22','S01-A/72h','Lung Ifnb1 mRNA at 72 h (fold vs untreated)','log10',unit='x',fmt='{:.1f}')
# Gm-csf
g={}
for grp,rows in [('PSLN-344','B{r}:F{r}'),('PSLN-212','G{r}:K{r}'),('Sham','L{r}:P{r}')]:
    for t,r in [(16,17),(36,18),(72,19)]: g[(grp,t)]=gmean('S02!'+rows.format(r=r))
for (grp,t),val in g.items(): chk(val,float(tcd[(tcd.block=='S02-F')&(tcd.group==grp)&(tcd.time==t)].geo_mean.iloc[0]),1e-6)
F['gmcsf']=g; cc=tcc[(tcc.block=='S02-F')&(tcc.g1=='PSLN-344')&(tcc.g2=='PSLN-212')].set_index('time')
add('L23','Immunology',f"Lung Gm-csf mRNA (geometric-mean fold vs untreated) at 16 / 36 / 72 h after vaccination: PSLN-344 {g[('PSLN-344',16)]:.1f} / {g[('PSLN-344',36)]:.1f} / {g[('PSLN-344',72)]:.1f}; PSLN-212 {g[('PSLN-212',16)]:.1f} / {g[('PSLN-212',36)]:.1f} / {g[('PSLN-212',72)]:.1f}; Sham {g[('Sham',16)]:.1f} / {g[('Sham',36)]:.1f} / {g[('Sham',72)]:.1f}. Ratio PSLN-344/PSLN-212 {cc.loc[16].estimate:.1f}, {cc.loc[36].estimate:.1f}, {cc.loc[72].estimate:.1f} (Holm-adjusted Welch p = {pf(cc.loc[16].holm_p_within_block_pair)}, {pf(cc.loc[36].holm_p_within_block_pair)}, {pf(cc.loc[72].holm_p_within_block_pair)}); n = 5. No young group in this block.",
    'S02!B17:P19','analysis_03_timecourses.py -> timecourse_descriptives.csv, timecourse_contrasts.csv','log10 scale; two-way ANOVA group x time also reported in timecourse_anova.csv.')
def tcfact(key,id_,block,label,day,rowcells,unit='%'):
    v={k:mean(r) for k,r in rowcells.items()}
    for k,val in v.items(): chk(val,float(tcd[(tcd.block==block)&(tcd.group==k)&(tcd.time==day)]['mean'].iloc[0]),1e-6)
    c=tcc[(tcc.block==block)&(tcc.g1=='PSLN-344')&(tcc.g2=='PSLN-212')&(tcc.time==day)].iloc[0]
    F[key]=dict(v=v,p=c.welch_p,holm=c.holm_p_within_block_pair)
    add(id_,'Immunology',f"{label}, day {day}: PSLN-344 {v['PSLN-344']:.1f}{unit} vs PSLN-212 {v['PSLN-212']:.1f}{unit} (Sham {v['Sham']:.1f}{unit}; young PSLN-212 {v['PSLN-212(Y)']:.1f}{unit}); Welch p = {pf(c.welch_p)} (Holm across the five days {pf(c.holm_p_within_block_pair)}); n = 5 per group and day.",
        '; '.join(rowcells.values()),'analysis_03_timecourses.py -> timecourse_descriptives.csv, timecourse_contrasts.csv, timecourse_anova.csv','Terminal sampling; two-way ANOVA interaction p in timecourse_anova.csv.')
tcfact('mono','L24','S01-D','Lung monocytes (CD11b+Ly6C+CD11c-Ly6G-)',4,{'PSLN-344':'S01!L26:P26','PSLN-212':'S01!G26:K26','Sham':'S01!B26:F26','PSLN-212(Y)':'S01!Q26:U26'})
tcfact('cd11bdc','L25','S01-E','Lung CD11b+ dendritic cells',4,{'PSLN-344':'S01!L32:P32','PSLN-212':'S01!G32:K32','Sham':'S01!B32:F32','PSLN-212(Y)':'S01!Q32:U32'})
F['mono8']=dict(a=mean('S01!L28:P28'),b=mean('S01!G28:K28'),s=mean('S01!B28:F28'),y=mean('S01!Q28:U28'))
trio('cdc1','L26','S01-F','Lung cDC1 at 72 h','linear')
trio('migdc','L27','S02-A','Lung CCR7+ migratory CD11b+ dendritic cells at 72 h','linear')
trio('ovadc','L28','S02-C','Antigen (OVA-AF647)-positive dendritic cells in mediastinal lymph node at 36 h','linear',extra=f" Pertussis-toxin group: {mean('S02!N3:N7'):.1f}% (S02!N3:N7; the annotation does not say which adjuvant this group received).")
F['ptx_ova']=mean('S02!N3:N7')
trio('cd40','L29a','S02-D CD40','CD40+ of lymph-node CD11b+ dendritic cells, day 3','linear')
trio('cd86','L29b','S02-D CD86','CD86+ of lymph-node CD11b+ dendritic cells, day 3','linear')
trio('prime','L30','S02-E','Ex vivo proliferation of OT-I CD8 T cells driven by sorted lymph-node CD11b+ dendritic cells','linear')
trio('ki67','L31','S05-D','Lung Ki-67+ CD8 T cells, day 3','linear')
trio('gzmb','L32','S05-E','Lung GZMB+ CD8 T cells, day 3','linear')
trio('ifng14','L33a','S05-F','IFN-g+ CD8 T cells in lymph node after rgH5N1 restimulation, day 14 (animals vaccinated with H1N1+H3N2)','linear',fmt='{:.2f}')
trio('ifng60','L33b','S05-G','IFN-g+ CD8 T cells in lymph node after rgH5N1 restimulation, day 60','linear',fmt='{:.2f}')
trio('trm','L34','S05-I','Lung resident-memory CD8 T cells (CD69+CD103+), day 25','linear',fmt='{:.2f}',extra=' Strain and age of these animals are not stated unambiguously (vaccinated "as in S05-A", whose conditions are internally inconsistent).')
trio('tfh','L35a','S04-A/ICOShi','ICOS-high T follicular helper cells in lymph node, day 7','linear')
trio('tfr','L35b','S04-B Foxp3','T follicular regulatory cells (Foxp3+ of CXCR5+ICOShi CD4) in lymph node, day 7','linear')
trio('tfhtfr','L35c','S04-B Tfh:Tfr','Tfh:Tfr quotient, day 7','log10',unit='')
trio('tfr30','L35d','S04-C','T follicular regulatory cells at day 30','linear',extra=f" Sham {mean('S04!A22:A26'):.1f}%.")
F['tfr30sham']=mean('S04!A22:A26')
trio('gcb','L36','S03-K','Germinal-centre B cells in lymph node, day 7','linear')
for an,key,id_ in [('Aicda','aicda','L37a'),('E47','e47','L37b')]:
    b=f'S03-L/{an}'; a_,b_,s_=gmean(cells(b,'PSLN-344')),gmean(cells(b,'PSLN-212')),gmean(cells(b,'Sham')); c=C(b,'PSLN-344','PSLN-212')
    F[key]=dict(a=a_,b=b_,s=s_,eff=c.effect,p=c.welch_p)
    add(id_,'Immunology',f"{an} mRNA in lymph-node B cells, day 5 (geometric-mean fold vs untreated): PSLN-344 {a_:.1f} vs PSLN-212 {b_:.1f} (Sham {s_:.1f}); ratio {c.effect:.1f} (95% CI {c.ci95_lo:.1f}-{c.ci95_hi:.1f}), Welch p = {pf(c.welch_p)}; n = 3; no young group.",
        '; '.join(cells(b,g_) for g_ in ['PSLN-344','PSLN-212','Sham']),'analysis_02 -> immunology_descriptives.csv, immunology_contrasts.csv','log10 scale')
trio('igg_h1','L38a','S03-A','Serum IgG to CA09 H1N1, day 14 (geometric mean titre)','log2',unit='',fmt='{:,.0f}')
trio('igg_h3','L38b','S03-E','Serum IgG to Aichi H3N2, day 14 (geometric mean titre)','log2',unit='',fmt='{:,.0f}')
trio('hai_h1','L39a','S03-C','HAI titre to CA09 H1N1, day 14 (geometric mean)','log2',unit='',fmt='{:.0f}')
trio('hai_h3','L39b','S03-G','HAI titre to Aichi H3N2, day 14 (geometric mean)','log2',unit='',fmt='{:.0f}')
trio('nt_h1','L40a','S03-D','Neutralising titre to CA09 H1N1, day 14 (geometric mean)','log2',unit='',fmt='{:,.0f}')
trio('nt_h3','L40b','S03-H','Neutralising titre to Aichi H3N2, day 14 (geometric mean)','log2',unit='',fmt='{:,.0f}')
# IgG2a/IgG1 recomputed
for key,id_,nb,db,cols,qb,qcols,lab in [('ratio_h1','L41a','S13-A','S13-B',(('B','F'),('A','E'),('C','G')),'S03-B','S03!G3:I7','CA09 H1N1'),('ratio_h3','L41b','S13-C','S13-D',(('J','N'),('I','M'),('K','O')),'S03-F','S03!G10:I14','Aichi H3N2')]:
    vals=[]
    for num,den in cols:
        n_=np.array(raw(f'S13!{num}3:{num}7')); d_=np.array(raw(f'S13!{den}3:{den}7')); vals.append(n_/d_)
    g344,g212,gy=[float(np.exp(np.log(v).mean())) for v in vals]
    blk=[b for b in imm.block.unique() if b.startswith('IgG2a/IgG1') and (('H1N1' in b)==(lab=='CA09 H1N1'))][0]
    chk(g344,float(imm[(imm.block==blk)&(imm.group=='PSLN-344')].centre_on_test_scale.iloc[0])); c=C(blk,'PSLN-344','PSLN-212')
    pr={g_:gmean(cells(qb,g_)) for g_ in ['PSLN-212','PSLN-344','PSLN-212(Y)']}
    F[key]=dict(a=g344,b=g212,y=gy,eff=c.effect,lo=c.ci95_lo,hi=c.ci95_hi,p=c.welch_p,printed=pr)
    add(id_,'Immunology',f"IgG2a/IgG1 quotient to {lab}, recomputed per animal from the subclass titres: PSLN-344 {g344:.2f} vs PSLN-212 {g212:.2f} (young {gy:.2f}); ratio {c.effect:.1f} (95% CI {c.ci95_lo:.1f}-{c.ci95_hi:.1f}), Welch p = {pf(c.welch_p)}. The printed quotient block {qb} shows {pr['PSLN-344']:.2f} under 'PSLN-344', {pr['PSLN-212']:.2f} under 'PSLN-212' and {pr['PSLN-212(Y)']:.2f} under 'PSLN-212(Y)': its three columns equal the recomputed young, aged-PSLN-212 and PSLN-344 quotients respectively, i.e. the headers are rotated by one position.",
        f"S13!{cols[0][0]}3:{cols[0][0]}7 / S13!{cols[0][1]}3:{cols[0][1]}7; S13!{cols[1][0]}3:{cols[1][0]}7 / S13!{cols[1][1]}3:{cols[1][1]}7; S13!{cols[2][0]}3:{cols[2][0]}7 / S13!{cols[2][1]}3:{cols[2][1]}7; printed block {qcols}",
        'audit_04_derived_checks.py; analysis_02 -> immunology_contrasts.csv (RECOMPUTED rows)','geometric mean of per-animal quotients; log10 scale')
trio('boost_h1','L42a','S13-I','Serum IgG to CA09 H1N1 at day 28 after a day-14 boost (geometric mean titre)','log2',unit='',fmt='{:,.0f}')
trio('boost_h3','L42b','S13-J','Serum IgG to Aichi H3N2 at day 28 after a day-14 boost (geometric mean titre)','log2',unit='',fmt='{:,.0f}')
FIG3=['S01-A/16h','S01-F','S02-A','S02-C','S02-D CD40','S02-D CD86','S02-E','S04-A/ICOShi','S04-B Foxp3','S03-K','S03-A','S03-C','S03-D','S03-G','S03-H','IgG2a/IgG1 anti-H1N1 RECOMPUTED from S13-A / S13-B','S05-D','S05-E','S05-F','S05-G','S05-I']
rr=ri[ri.block.isin(FIG3)].restoration_pct; assert len(rr)==len(FIG3)
F['rest']=dict(n=len(rr),median=float(rr.median()),min=float(rr.min()),max=float(rr.max()),ge55=int((rr>=55).sum()),low=ri[ri.block.isin(FIG3)&(ri.restoration_pct<55)][['block','restoration_pct']].values.tolist())
add('L43','Immunology',f"Share of the age gap closed (0% = aged PSLN-212, 100% = young PSLN-212) across {len(rr)} read-outs spanning innate, dendritic-cell, follicular, antibody and CD8 responses: median {rr.median():.0f}%, range {rr.min():.0f}-{rr.max():.0f}%; {int((rr>=55).sum())} of {len(rr)} are at or above 55%. Below: CD40 {F['cd40']['rest']:.0f}%, CD86 {F['cd86']['rest']:.0f}%, lung GZMB+ CD8 {F['gzmb']['rest']:.0f}%.",
    'blocks S01-A, S01-F, S02-A, S02-C, S02-D, S02-E, S03-A, S03-C, S03-D, S03-G, S03-H, S03-K, S04-A, S04-B, S05-D..G, S05-I, S13-A/B (cells in L21-L41)','analysis_02 -> immunology_restoration_index.csv; figure 3','(mean344 - mean212)/(meanYoung - mean212) on the test scale; bootstrap CIs in the CSV.')
h344=raw('S03!N3:N7')+raw('S03!N10:N14'); h212=raw('S03!M3:M7')+raw('S03!M10:M14'); hy=raw('S03!O3:O7')+raw('S03!O10:O14')
F['hai160']=dict(a=sum(v>=160 for v in h344),an=len(h344),b40=sum(v>=40 for v in h212),bn=len(h212),bmax=max(h212),amin=min(h344),ymin=min(hy))
add('L44','Immunology',f"HAI distribution: all {len(h344)} PSLN-344 sera (two strains) are >= {min(h344):.0f}; {sum(v>=40 for v in h212)} of {len(h212)} PSLN-212 sera reach the conventional 1:40 level and none exceeds {max(h212):.0f}; lowest young-PSLN-212 titre {min(hy):.0f}.",'S03!M3:O7; S03!M10:O14','build_ledger.py (counts); analysis_07 -> biomarker_separation.csv')

# ======================================================================================================
# MECHANISM - interventions
def two(key,id_,block,g1,g2,label,section='Mechanism',extra='',scale='linear'):
    a_,b_=mean(cells(block,g1)),mean(cells(block,g2)); c=con[(con.block==block)&(((con.g1==g1)&(con.g2==g2))|((con.g1==g2)&(con.g2==g1)))].iloc[0]
    F[key]=dict(a=a_,b=b_,p=c.welch_p,mw=c.mannwhitney_exact_p,n=int(c.n1))
    add(id_,section,f"{label}: {a_:.1f}% vs {b_:.1f}%; Welch p = {pf(c.welch_p)} (exact Mann-Whitney p = {pf(c.mannwhitney_exact_p)}); n = {int(c.n1)} per group.{extra}",f"{cells(block,g1)}; {cells(block,g2)}",'analysis_02 -> immunology_descriptives.csv, immunology_contrasts.csv','arithmetic means of percentages')
two('spad','L45','S01-C','WT','SPA/D','DiD-liposome-positive alveolar macrophages 16 h after dosing, wild type vs Sftpa1/Sftpd double knockout (young)')
two('srb2','L46a','S01-B','AECII/PSLN-SRB','AECII/FreeSRB','Dye-positive type-II alveolar epithelial cells 16 h after liposomal vs free sulforhodamine B (aged)')
two('srb1','L46b','S01-B','AECI/PSLN-SRB','AECI/FreeSRB','Dye-positive type-I alveolar epithelial cells, liposomal vs free dye (aged)')
two('cbx','L47','S11-C','CBX-','CBX+','Recruited lung monocytes on day 3 after PSLN-344 + vaccine, without vs with carbenoxolone pre-treatment')
two('ccr2mono','L48a','S07-B/Mono','PSLN-344','PSLN-344+INCB3344','Lung CD11b+Ly6C+ monocytes after PSLN-344 + vaccine, without vs with CCR2 antagonist (time point not stated)')
two('ccr2mac','L48b','S07-B/Ly6C+Mac','PSLN-344','PSLN-344+INCB3344','Lung Ly6C+ macrophages, without vs with CCR2 antagonist (time point not stated)')
two('ccr2cd8','L48c','S02-I','PSLN-344(Y)','PSLN-344(Y)+INCB3344','Lung GZMB+ CD8 T cells on day 5 in YOUNG animals given PSLN-344 + vaccine, without vs with CCR2 antagonist')
two('ifnar','L49a','S02-H','WT w/o cDC','IFN w/o cDC','Donor-derived monocyte-derived dendritic cells in lung on day 3, wild-type vs Ifnar-knockout marrow (cDC precursors removed)')
two('ifnar_gm','L49b','S02-H','GMCSF','IFN w/o cDC','Same read-out, Ifnar-knockout marrow with vs without intratracheal rGM-CSF',extra=f" Wild-type reference {mean(cells('S02-H','WT w/o cDC')):.1f}%.")
two('ifnar_rec','L49c','S12-A','WT to WT','IFNAR-/- to WT','Donor monocytes infiltrating lung on day 3, wild-type vs Ifnar-knockout marrow (young recipients)',extra=' Only three animals per group; a difference of this size cannot be excluded or confirmed.')
two('gmrescue','L50','S02-G','PSLN-212+GM-CSF','PSLN-212','Lung Ly6C+CD11c+MHC-II+ cells on day 5, PSLN-212 + vaccine with vs without intranasal rGM-CSF',extra=f" rGM-CSF with vaccine but no adjuvant: {mean(cells('S02-G','GM-CSF')):.1f}%.")
F['gmalone']=mean(cells('S02-G','GM-CSF'))
two('ptx_mln','L51a','S05-C','MLN','MLN+PTX','Proliferating OT-I CD8 T cells in lymph node on day 4 after OVA + PSLN-344, without vs with pertussis toxin')
two('ptx_lung','L51b','S05-C','Lung','Lung+PTX','Proliferating OT-I CD8 T cells in lung on day 4, without vs with pertussis toxin')
m5={'PSLN-344':gmean('S07!E5:G5'),'PSLN-212':gmean('S07!B5:D5')}; c5=tcc[(tcc.block=='S07-A')&(tcc.time==5)&(tcc.g1=='PSLN-344')&(tcc.g2=='PSLN-212')].iloc[0]
F['ccr2mac_tc']=dict(a=mean('S07!E5:G5'),b=mean('S07!B5:D5'),ratio=c5.estimate,p=c5.welch_p,d10a=mean('S07!E6:G6'),d10b=mean('S07!B6:D6'))
add('L52a','Mechanism',f"Lung Ly6C+CCR2+ macrophages on day 5 as printed (x10^5 cells, mean): PSLN-344 {F['ccr2mac_tc']['a']:.1f} vs PSLN-212 {F['ccr2mac_tc']['b']:.1f}, i.e. {F['ccr2mac_tc']['b']/F['ccr2mac_tc']['a']:.1f}-fold fewer with PSLN-344; ratio of geometric means {c5.estimate:.2f}, Welch p = {pf(c5.welch_p)}; day 10: {F['ccr2mac_tc']['d10a']:.1f} vs {F['ccr2mac_tc']['d10b']:.1f}; n = 3 per group and day. Not used for the mechanism: the direction sits oddly with the larger monocyte influx (L24), the higher Ccl2 signal (L61) and S07-B (L48b), and the sheet contains a mislabelled block (L54).",'S07!B2:G7','analysis_03 -> timecourse_descriptives.csv, timecourse_contrasts.csv','log10 scale for the test')
trio('cd206','L52b','S11-E','CD206+ lung macrophages (time point not stated)','linear',section='Mechanism',extra=f" Sham {mean(cells('S11-E','Sham')):.1f}%.")
trio('treg','L53','S04-D','Lung regulatory T cells (CD4+Foxp3+), day 7','linear',fmt='{:.2f}',section='Mechanism')
F['s07c']=(mean('S07!B16:B20'),mean('S07!C16:C20'))
add('L54','Mechanism',f"Lung regulatory T cells 4 days after transfer of sorted donor macrophages (S07-C): {F['s07c'][0]:.1f}% (column B) vs {F['s07c'][1]:.1f}% (column C). Both columns are headed 'Ly6C-CD206+', so the subset that induces more regulatory T cells cannot be identified.",'S07!B15:C20','analysis_02 -> immunology_descriptives.csv')

# young / alternatives -------------------------------------------------------------------------------------
def yy(block,scale='linear'):
    fn=gmean if scale!='linear' else mean
    return fn(cells(block,'PSLN-344(Y)')),fn(cells(block,'PSLN-212(Y)')),C(block,'PSLN-344(Y)','PSLN-212(Y)')
a1=yy('S01-A/16h','log10'); a2=yy('S01-F'); a3=yy('S02-C'); a4=yy('S02-E')
F['young']=dict(ifnb=(a1[0],a1[1],a1[2].effect,a1[2].welch_p,a1[2].tukey_p),cdc1=(a2[0],a2[1],a2[2].welch_p),ova=(a3[0],a3[1],a3[2].welch_p),prime=(a4[0],a4[1],a4[2].welch_p))
add('L55','Differentiation',f"Young animals, PSLN-344 vs PSLN-212: Ifnb1 at 16 h {a1[0]:.1f}x vs {a1[1]:.1f}x (ratio {a1[2].effect:.2f}, Welch p = {pf(a1[2].welch_p)}, Tukey p = {pf(a1[2].tukey_p)}); cDC1 {a2[0]:.1f}% vs {a2[1]:.1f}% (p = {pf(a2[2].welch_p)}); antigen+ DC in lymph node {a3[0]:.1f}% vs {a3[1]:.1f}% (p = {pf(a3[2].welch_p)}); ex vivo CD8 priming {a4[0]:.1f}% vs {a4[1]:.1f}% (p = {pf(a4[2].welch_p)}).",
    f"{cells('S01-A/16h','PSLN-344(Y)')}; {cells('S01-A/16h','PSLN-212(Y)')}; {cells('S01-F','PSLN-344(Y)')}; {cells('S01-F','PSLN-212(Y)')}; {cells('S02-C','PSLN-344(Y)')}; {cells('S02-C','PSLN-212(Y)')}; {cells('S02-E','PSLN-344(Y)')}; {cells('S02-E','PSLN-212(Y)')}",'analysis_02 -> immunology_contrasts.csv')
ia=pd.read_csv('age_by_manganese_interaction.csv').set_index('block')
# independent recomputation of the increments from raw cells
chk(ia.loc['S01-A/16h','increment_aged'],gmean('S01!B8:F8')/gmean('S01!B5:F5')); chk(ia.loc['S01-A/16h','increment_young'],gmean('S01!B10:F10')/gmean('S01!B9:F9'))
chk(ia.loc['S02-C','increment_aged'],mean('S02!L3:L7')-mean('S02!K3:K7')); chk(ia.loc['S02-C','increment_young'],mean('S02!O3:O7')-mean('S02!M3:M7'))
F['ageint']={b:dict(a=ia.loc[b,'increment_aged'],y=ia.loc[b,'increment_young'],p=ia.loc[b,'p_interaction']) for b in ia.index}
add('L55b','Differentiation',f"Manganese adds more in aged than in young animals (two-way ANOVA, age x formulation; n = 5 per cell). Ifnb1 at 16 h: {ia.loc['S01-A/16h','increment_aged']:.2f}-fold in aged vs {ia.loc['S01-A/16h','increment_young']:.2f}-fold in young, interaction p = {pf(ia.loc['S01-A/16h','p_interaction'])}. Lung cDC1: +{ia.loc['S01-F','increment_aged']:.1f} vs +{ia.loc['S01-F','increment_young']:.1f} points, p = {pf(ia.loc['S01-F','p_interaction'])}. Antigen-bearing dendritic cells in lymph node: +{ia.loc['S02-C','increment_aged']:.1f} vs +{ia.loc['S02-C','increment_young']:.1f} points, p = {pf(ia.loc['S02-C','p_interaction'])}. Ex vivo CD8 priming: +{ia.loc['S02-E','increment_aged']:.1f} vs +{ia.loc['S02-E','increment_young']:.1f} points, p = {pf(ia.loc['S02-E','p_interaction'])}. Survival in young animals is already {F['y212'][0]}/{F['y212'][1]} without manganese, so it cannot show an advantage.",
    'S01!B5:F5; S01!B8:F10; S01!G36:Z36; S02!K3:M7; S02!O3:O7; S02!K10:M14; S02!O10:O14','analysis_08_age_by_manganese.py -> age_by_manganese_interaction.csv','Interaction term of a two-way ANOVA on the scale used for each read-out (log10 for Ifnb1).')
mtt=pd.read_csv('challenge_morbidity_tests.csv'); r=mtt[mtt.weight_block=='S09-G'].iloc[0]
F['y180']=dict(n1=r.nadir1_survivors,n2=r.nadir2_survivors,p=r.welch_p,d1=r.d14_1,d2=r.d14_2,pd=r.d14_p)
add('L56','Differentiation',f"Young animals challenged 180 days after vaccination (S09-G): lowest weight {r.nadir1_survivors:.1f}% with PSLN-344 vs {r.nadir2_survivors:.1f}% with PSLN-212 (Welch p = {pf(r.welch_p)}); day-14 weight {r.d14_1:.1f}% vs {r.d14_2:.1f}% (p = {pf(r.d14_p)}); n = 8. Two of the three young weight tables share whole-animal trajectories (see data-quality register).",'S09!G66:AD73','analysis_05 -> challenge_morbidity_tests.csv')
cm=dict(ifnb=gmean(cells('S01-A/16h','CMP-204')),igg=gmean(cells('S03-A','CMP-204')),hai=gmean(cells('S03-C','CMP-204')),nt=gmean(cells('S03-D','CMP-204')))
c1=C('S01-A/16h','PSLN-212','CMP-204'); c2=C('S03-A','PSLN-212','CMP-204'); cm.update(r_ifnb=c1.effect,p_ifnb=c1.welch_p,r_igg=c2.effect,p_igg=c2.welch_p); F['cmp']=cm
add('L57','Alternatives',f"cGAMP payload (CMP-204) in aged animals: Ifnb1 at 16 h {cm['ifnb']:.1f}x (PSLN-212 {F['ifnb16']['b']:.1f}x; PSLN-344 {F['ifnb16']['a']:.1f}x); IgG {cm['igg']:.0f}, HAI {cm['hai']:.0f}, neutralising {cm['nt']:.0f} (geometric means, CA09 H1N1); survival after homologous challenge {F['homo']['CMP-204']['k']}/7 (S03-I). CDN-1807 vs cGAMP in the same manganese-free liposome (PSLN-212 vs CMP-204): Ifnb1 ratio {c1.effect:.2f} (95% CI {c1.ci95_lo:.2f}-{c1.ci95_hi:.2f}), Welch p = {pf(c1.welch_p)}; IgG ratio {c2.effect:.2f} ({c2.ci95_lo:.2f}-{c2.ci95_hi:.2f}), p = {pf(c2.welch_p)}. No block combines cGAMP with manganese.",
    f"{cells('S01-A/16h','CMP-204')}; {cells('S01-A/16h','PSLN-212')}; {cells('S03-A','CMP-204')}; {cells('S03-A','PSLN-212')}; {cells('S03-C','CMP-204')}; {cells('S03-D','CMP-204')}; S03!C24:C30",'analysis_02 -> immunology_descriptives.csv, immunology_contrasts.csv; analysis_01')
sw=pd.read_csv('safety_weight_after_vaccination.csv').set_index('group'); swt=pd.read_csv('safety_weight_after_vaccination_tests.csv').set_index('contrast')
cy=pd.read_csv('safety_cytokines.csv'); cyt=pd.read_csv('safety_cytokines_tests.csv')
def cyv(panel,an,g): 
    r=cy[(cy.panel.str.startswith(panel))&(cy.analyte==an)&(cy.group==g)].iloc[0]; v=gmean_log10('S09!'+r.cells.split('!')[1]); chk(v,r.geo_fold); return v
def cyp(panel,an,g1,g2):
    r=cyt[(cyt.panel.str.startswith(panel))&(cyt.analyte==an)&(cyt.g1==g1)&(cyt.g2==g2)].iloc[0]; return r.fold_ratio,r.welch_p
dr=pd.read_csv('dose_response_fit.csv').set_index('group'); dd=pd.read_csv('dose_response_by_dose.csv')
F['r848']=dict(nadir=sw.loc['PSLN-212/R848','mean_nadir'],n10=int(sw.loc['PSLN-212/R848','n_loss_ge10pct']),nd10=int(sw.loc['PSLN-212/R848','n_day10']),d10=sw.loc['PSLN-212/R848','mean_d10'],
               il10=cyv('16 h','Il10','PSLN-212/R848'),tnf=cyv('16 h','Tnf','PSLN-212/R848'),il10_344=cyv('16 h','Il10','PSLN-344'),
               d20=float(dd[(dd.group=='PSLN-344/R848')&(dd.dose_ug==20)]['mean'].iloc[0]),d20_344=float(dd[(dd.group=='PSLN-344')&(dd.dose_ug==20)]['mean'].iloc[0]),
               ifnb_212r=gmean(cells('S01-A/16h','PSLN-212/R848')))
chk(F['r848']['nadir'],np.mean([min(raw(f'S08!{c}22:{c}26')) for c in 'VWXYZ']))
add('L58','Alternatives',f"Adding the TLR7/8 agonist R848: PSLN-212/R848 gives a mean weight nadir of {F['r848']['nadir']:.1f}% after vaccination, {F['r848']['n10']} of 5 animals lose >= 10%, group mean still {F['r848']['d10']:.1f}% on day 10 with only {F['r848']['nd10']} of 5 animals recorded (S08-D); lung Il10 {F['r848']['il10']:.0f}x and Tnf {F['r848']['tnf']:.0f}x at 16 h vs {F['r848']['il10_344']:.1f}x Il10 for PSLN-344 (S09-A); Ifnb1 at 16 h: PSLN-212/R848 {F['r848']['ifnb_212r']:.1f}x vs {F['ifnb16']['a']:.1f}x for PSLN-344 (S01-A); a preparation labelled PSLN-344/R848 gives {F['r848']['d20']:.1f}x at 20 ug vs {F['r848']['d20_344']:.1f}x for PSLN-344 (S08-A; this preparation is not defined in the annotation).",
    'S08!V21:Z26; S09!N8:P9; S09!Q9:S9; S01!B7:F7; S01!B8:F8; S08!K6:M6; S08!H6:J6','analysis_04_safety.py -> safety_weight_after_vaccination.csv, safety_cytokines.csv; analysis_06 -> dose_response_by_dose.csv')
p=dr.loc['PSLN-344']; q=dr.loc['PSLN-212']
d20=mean('S08!H6:J6'); d40=mean('S08!H7:J7'); w2040=welch('S08!H7:J7','S08!H6:J6','log10')
F['dose']=dict(emax=p.Emax_fold,elo=p.Emax_lo,ehi=p.Emax_hi,ed50=p.ED50_ug,dlo=p.ED50_lo,dhi=p.ED50_hi,emax212=q.Emax_fold,e212lo=q.Emax_lo,e212hi=q.Emax_hi,ed50_212=q.ED50_ug,d20=d20,d40=d40,p2040=w2040['p'],d5=mean('S08!H4:J4'),d10=mean('S08!H5:J5'),d1=mean('S08!H3:J3'),eq=6.6,d20_212=mean('S08!E6:G6'))
add('L59','Dose',f"Dose-response of lung Ifnb1 at 16 h (S08-A; n = 3 per dose; age of animals not stated): PSLN-344 {F['dose']['d1']:.1f} / {F['dose']['d5']:.1f} / {F['dose']['d10']:.1f} / {d20:.1f} / {d40:.1f}-fold at 1 / 5 / 10 / 20 / 40 ug; fitted Emax {p.Emax_fold:.0f}-fold (95% CI {p.Emax_lo:.0f}-{p.Emax_hi:.0f}) and ED50 {p.ED50_ug:.0f} ug ({p.ED50_lo:.0f}-{p.ED50_hi:.0f}); PSLN-212 Emax {q.Emax_fold:.0f}-fold ({q.Emax_lo:.0f}-{q.Emax_hi:.0f}), ED50 {q.ED50_ug:.0f} ug. 40 vs 20 ug: ratio {d40/d20:.2f}, Welch p = {pf(w2040['p'])}. A PSLN-344 dose of about 6.6 ug is predicted to match the 20-ug PSLN-212 response ({F['dose']['d20_212']:.1f}-fold).",
    'S08!B3:M7','analysis_06_dose_response.py -> dose_response_fit.csv, dose_response_by_dose.csv','Emax model fitted on log10 scale; parametric-bootstrap CIs')
# safety ---------------------------------------------------------------------------------------------------
nad344=[min(raw(f'S08!{c}22:{c}26')) for c in 'QRSTU']; nadv=[min(raw(f'S08!{c}22:{c}26')) for c in ['AA','AB','AC','AD','AE']]
chk(np.mean(nad344),sw.loc['PSLN-344','mean_nadir']); t=swt.loc['PSLN-344 vs Vaccine']
F['react']=dict(nadir=np.mean(nad344),worst=min(nad344),d10=mean('S08!Q26:U26'),d8=mean('S08!Q25:U25'),vac=np.mean(nadv),diff=t['diff'],lo=t.ci_lo,hi=t.ci_hi,p=t.welch_p,n212=sw.loc['PSLN-212','mean_nadir'],ny=sw.loc['PSLN-212(Y)','mean_nadir'],cmp=sw.loc['CMP-204','mean_nadir'])
add('L60','Safety',f"Body weight after intranasal vaccination without challenge (S08-D, n = 5): PSLN-344 mean nadir {F['react']['nadir']:.1f}% of baseline (worst animal {F['react']['worst']:.1f}%), {F['react']['d8']:.1f}% on day 8 and {F['react']['d10']:.1f}% on day 10; vaccine alone {F['react']['vac']:.1f}%; difference {t['diff']:.1f} points (95% CI {t.ci_lo:.1f} to {t.ci_hi:.1f}), Welch p = {pf(t.welch_p)}. PSLN-212 aged {F['react']['n212']:.1f}%, PSLN-212 young {F['react']['ny']:.1f}%, CMP-204 {F['react']['cmp']:.1f}%.",
    'S08!B21:AE26','analysis_04_safety.py -> safety_weight_after_vaccination.csv, safety_weight_after_vaccination_tests.csv','Per-animal nadir over days 2-10')
c16={an:(cyv('16 h',an,'PSLN-344'),cyv('16 h',an,'PSLN-212'),cyv('16 h',an,'PSLN-212(y)')) for an in ['Ifnb1','Il6','Tnf','Il10','Ccl2','Ccl3','Ccl5']}
c72={an:(cyv('72 h',an,'PSLN-344'),cyv('72 h',an,'PSLN-212'),cyv('72 h',an,'PSLN-212(y)')) for an in ['Ifnb1','Il6','Tnf','Il10','Ccl2','Ccl3','Ccl5']}
F['c16']=c16; F['c72']=c72
F['c16y']={an:cyp('16 h',an,'PSLN-344','PSLN-212(y)') for an in ['Il6','Tnf','Il10','Ccl2']}; F['c72y']={an:cyp('72 h',an,'PSLN-344','PSLN-212(y)') for an in ['Il6','Tnf','Il10']}; F['c72a']={an:cyp('72 h',an,'PSLN-344','PSLN-212') for an in ['Il6','Tnf','Il10']}
add('L61','Safety',f"Lung cytokine mRNA 16 h after adjuvant alone (S09-A, columns A-V; stored as log10; geometric-mean fold vs untreated; n = 3): aged PSLN-344 Il6 {c16['Il6'][0]:.0f}x, Tnf {c16['Tnf'][0]:.0f}x, Ccl2 {c16['Ccl2'][0]:.0f}x (aged PSLN-212 Ccl2 {c16['Ccl2'][1]:.1f}x, a {c16['Ccl2'][0]/c16['Ccl2'][1]:.0f}-fold difference), Il10 {c16['Il10'][0]:.1f}x. Relative to young PSLN-212: Il6 {F['c16y']['Il6'][0]:.2f}-fold (p = {pf(F['c16y']['Il6'][1])}), Ccl2 {F['c16y']['Ccl2'][0]:.2f}-fold (p = {pf(F['c16y']['Ccl2'][1])}), Tnf {F['c16y']['Tnf'][0]:.1f}-fold (p = {pf(F['c16y']['Tnf'][1])}), Il10 {F['c16y']['Il10'][0]:.1f}-fold (p = {pf(F['c16y']['Il10'][1])}).",
    'S09!B3:V9','analysis_04_safety.py -> safety_cytokines.csv, safety_cytokines_tests.csv','values are log10 in the workbook; back-transformed; Welch tests on the stored scale')
add('L62','Safety',f"Lung cytokine mRNA at 72 h (S09-A, columns X-AS; printed '16h' but its Ifnb1 row reproduces the 72-h values of S01-A): aged PSLN-344 Tnf {c72['Tnf'][0]:.1f}x, Il6 {c72['Il6'][0]:.1f}x, Il10 {c72['Il10'][0]:.1f}x, Ccl2 {c72['Ccl2'][0]:.0f}x; aged PSLN-212 Tnf {c72['Tnf'][1]:.1f}x, Il6 {c72['Il6'][1]:.1f}x, Il10 {c72['Il10'][1]:.1f}x; young PSLN-212 Tnf {c72['Tnf'][2]:.1f}x, Il6 {c72['Il6'][2]:.1f}x, Il10 {c72['Il10'][2]:.1f}x. PSLN-344 vs young: Tnf {F['c72y']['Tnf'][0]:.0f}-fold (p = {pf(F['c72y']['Tnf'][1])}), Il6 {F['c72y']['Il6'][0]:.1f}-fold (p = {pf(F['c72y']['Il6'][1])}); PSLN-344 vs aged PSLN-212: Tnf {F['c72a']['Tnf'][0]:.1f}-fold (p = {pf(F['c72a']['Tnf'][1])}), Il6 {F['c72a']['Il6'][0]:.1f}-fold (p = {pf(F['c72a']['Il6'][1])}). n = 3.",
    'S09!Y3:AS9; cross-check S01!H3:L10','analysis_04_safety.py -> safety_cytokines.csv; audit_04_derived_checks.py (panel identity)')
cn=pd.read_csv('safety_cns_tests.csv')
def cnr(an,g1,g2): r=cn[(cn.analyte==an)&(cn.g1==g1)&(cn.g2==g2)].iloc[0]; return r.ratio,r.ci_lo,r.ci_hi,r.welch_p
F['cns']={(an,g2):cnr(an,'PSLN-344',g2) for an in ['Ifnb1','Tnf','Isg15'] for g2 in ['PBS','Sham']}; F['cns_ct']={an:cnr(an,'CT','PBS') for an in ['Ifnb1','Tnf','Isg15']}; F['cns_ct344']=cnr('Tnf','CT','PSLN-344')
chk(F['cns'][('Tnf','PBS')][0],gmean('S10!H3:H7')/gmean('S10!F3:F7'))
s_=F['cns']
add('L63','Safety',f"CNS transcripts 36 h after intranasal dosing (S10-A, n = 5; ratio of geometric means): PSLN-344 vs buffer - Ifnb1 {s_[('Ifnb1','PBS')][0]:.2f} (95% CI {s_[('Ifnb1','PBS')][1]:.2f}-{s_[('Ifnb1','PBS')][2]:.2f}), Tnf {s_[('Tnf','PBS')][0]:.2f} ({s_[('Tnf','PBS')][1]:.2f}-{s_[('Tnf','PBS')][2]:.2f}; Welch p = {pf(s_[('Tnf','PBS')][3])}, not adjusted for the six comparisons), Isg15 {s_[('Isg15','PBS')][0]:.2f} ({s_[('Isg15','PBS')][1]:.2f}-{s_[('Isg15','PBS')][2]:.2f}); PSLN-344 vs vaccine + empty liposome - {s_[('Ifnb1','Sham')][0]:.2f}, {s_[('Tnf','Sham')][0]:.2f} (CI {s_[('Tnf','Sham')][1]:.2f}-{s_[('Tnf','Sham')][2]:.2f}), {s_[('Isg15','Sham')][0]:.2f}; cholera toxin vs buffer - {F['cns_ct']['Ifnb1'][0]:.1f}, {F['cns_ct']['Tnf'][0]:.1f}, {F['cns_ct']['Isg15'][0]:.1f}. 'Buffer' is the group printed as PBS; under the annotation's general rule it received buffer alone, although the block description lists only vaccine-containing conditions.",
    'S10!A3:N7','analysis_04_safety.py -> safety_cns.csv, safety_cns_tests.csv','log10 scale; Welch intervals')
ee=raw('S08!M11:O11'); F['ee']=dict(mean=np.mean(ee),min=min(ee),max=max(ee),cv=100*np.std(ee,ddof=1)/np.mean(ee),p212=mean('S08!D11:F11'),cmp=mean('S08!A11:C11'))
add('L64','CMC',f"Encapsulation efficiency (S08-B, three preparations each): PSLN-344 {np.mean(ee):.1f}% (range {min(ee):.1f}-{max(ee):.1f}%; CV {F['ee']['cv']:.0f}%); PSLN-212 {F['ee']['p212']:.1f}%; CMP-204 {F['ee']['cmp']:.1f}%. The method is stated as absorbance of CDN-1807 at 260 nm, yet values are also reported for PSLN-R848, which contains no CDN-1807. Particle size, zeta potential, morphology and stability are described in the annotation but no such data are in the workbook.",
    'S08!A10:O11','analysis_02 -> immunology_descriptives.csv (block S08-B)')
pw_=pd.read_csv('power_table.csv')
def npg(lbl,t): return int(pw_[(pw_.comparison.str.startswith(lbl))&(pw_.target_power==t)].n_per_group.iloc[0])
F['power']=dict(obs=npg('PSLN-344 vs PSLN-212 in aged',0.9),cons=npg('Conservative planning',0.9),act50=npg('PSLN-344 vs an active comparator achieving 50%',0.9),act50_80=npg('PSLN-344 vs an active comparator achieving 50%',0.8),act60=npg('PSLN-344 vs an active comparator achieving 60%',0.8),hai2=npg('HAI / neutralising titre: detect a 2-fold',0.9),hai4=npg('HAI / neutralising titre: detect a 4-fold',0.9),d60=npg('Day-60 durability',0.9))
add('L65','Planning',f"Animals per group for 90% power (two-sided alpha 0.05, Fisher exact): {F['power']['obs']} at the observed 84% vs 12%; {F['power']['cons']} if the true rates are 70% vs 15%; {F['power']['act50']} against a comparator that achieves 50% ({F['power']['act50_80']} for 80% power); {F['power']['d60']} for the day-60 contrast (67% vs 5%). For titres (pooled within-group SD 0.80 log2 from S03-C/D/G/H): {F['power']['hai2']} per group to detect a 2-fold difference, {F['power']['hai4']} for 4-fold.",
    'S03!K3:O7; S03!Q3:U7; S03!K10:O14; S03!Q10:U14 (SD); survival counts as L01-L02, L10','analysis_07_sensitivity_biomarkers_power.py -> power_table.csv','exact enumeration of the binomial outcomes; t-test power for titres')

bs=pd.read_csv('biomarker_separation.csv'); nsep=int(bs.complete_separation.sum())
def sepv(b): r=bs[bs.block==b].iloc[0]; return r.unprotected_extreme,r.protected_extreme
F['sep']=dict(n=len(bs),nsep=nsep,hai=sepv('S03-C'),ifng=sepv('S05-F'),ifnb=sepv('S01-A/16h'),mig=sepv('S02-A'),tfh=sepv('S04-B Tfh:Tfr'),trm=sepv('S05-I'),ki=sepv('S05-D'))
add('L66','Biomarkers',f"Separation of the two protected groups (aged PSLN-344, young PSLN-212) from the two unprotected groups (aged PSLN-212, Sham), animal by animal: complete in {nsep} of {len(bs)} single-time-point read-outs that contain all four groups. Examples (highest unprotected value / lowest protected value): HAI to H1N1 {F['sep']['hai'][0]:.0f} / {F['sep']['hai'][1]:.0f}; IFN-g+ CD8 at day 14 {F['sep']['ifng'][0]:.2f}% / {F['sep']['ifng'][1]:.2f}%; Ifnb1 at 16 h {F['sep']['ifnb'][0]:.1f}x / {F['sep']['ifnb'][1]:.1f}x; CCR7+ migratory DC {F['sep']['mig'][0]:.1f}% / {F['sep']['mig'][1]:.1f}%; Tfh:Tfr {F['sep']['tfh'][0]:.1f} / {F['sep']['tfh'][1]:.1f}; lung resident-memory CD8 {F['sep']['trm'][0]:.2f}% / {F['sep']['trm'][1]:.2f}%.",
    'all four-group scalar blocks (cells listed in immunology_descriptives.csv)','analysis_07 -> biomarker_separation.csv','Group-level only: survival and biomarkers were measured in different animals.')
fam=con[(con.g1=='PSLN-344')&(con.g2=='PSLN-212')&~con.block.isin(['S03-B','S03-F','S08-B'])]
F['mult']=dict(n=len(fam),raw05=int((fam.welch_p<0.05).sum()),bh05=int((multipletests_bh(fam.welch_p)<0.05).sum()) if False else None)
from statsmodels.stats.multitest import multipletests
F['mult']=dict(n=len(fam),raw05=int((fam.welch_p<0.05).sum()),bh05=int((multipletests(fam.welch_p,method='fdr_bh')[1]<0.05).sum()),holm05=int((multipletests(fam.welch_p,method='holm')[1]<0.05).sum()),ns=fam[fam.welch_p>=0.05].block.tolist())
add('L67','Statistics',f"Multiplicity: of {len(fam)} single-time-point contrasts between aged PSLN-344 and aged PSLN-212 (printed quotient blocks and encapsulation efficiency excluded), {F['mult']['raw05']} have Welch p < 0.05, {F['mult']['bh05']} remain below 0.05 after Benjamini-Hochberg adjustment and {F['mult']['holm05']} after Holm adjustment. Not significant: {', '.join(F['mult']['ns'])}. With five animals per group the smallest attainable exact rank-test p is 0.008.",
    'all blocks containing both groups (cells in immunology_descriptives.csv)','analysis_02 -> immunology_contrasts.csv; build_ledger.py')
# ======================================================================================================
# DATA QUALITY
a1=pd.read_csv('audit_01_stated_vs_observed_n.csv'); bad=a1[~a1.match]
F['nmis']=bad[['block','label','observed_n_by_group']].values.tolist()
add('Q01','Data quality',f"Stated n differs from the observations present in {len(bad)} blocks: S03-J (label n=9; 10 rows per group, one PSLN-344 row without a day), S05-A and S05-B (label n=3; 2 values per group and day), S09-F (label n=8; Sham has 7 rows - the annotation attributes this shortfall to S09-B, whose Sham column has 8), S13-E (label n=5; 7 rows per group).",
    'S03!G15:J46; S05!A1:I10; S09!A64:D88; S09!A10:D35; S13!R1:V30','audit_01_n_and_labels.py -> audit_01_stated_vs_observed_n.csv')
a2=pd.read_csv('audit_02_survival_vs_weight.csv'); F['a2']=a2.status.value_counts().to_dict()
dc=a2[a2.status=='DEATH COUNT DIFFERS']
F['a2list']=[(r.surv_block,r.weight_block,r.group,int(r.surv_n-r.surv_deaths),int(r.wt_n-r.wt_exits)) for r in dc.itertuples()]
add('Q02','Data quality',f"Survival tables vs the body-weight tables recorded for the same animals ({len(a2)} arm-level comparisons over 17 experiments): {F['a2'].get('agree',0)} agree in count and, within a two-day tolerance, in timing; {sum(v for k,v in F['a2'].items() if k.startswith('count agrees'))} agree in count but not in timing; {F['a2'].get('DEATH COUNT DIFFERS',0)} differ in the number of deaths, 1 differs in the number of animals (S09-F/S09-G Sham, 7 vs 8) and 4 group labels exist in only one of the two tables (S03-I/S13-F: CMP-204 vs Naive; S03-J/S13-G: PSLN-212 vs Naive). Death-count differences (survivors per table / per weights): "+'; '.join(f"{s}/{w_} {g} {a_}/7 vs {b_}/7" if 'S03-J' not in s else f"{s}/{w_} {g} {a_}/10 vs {b_}/10" for s,w_,g,a_,b_ in F['a2list'])+'.',
    'all survival blocks and all body-weight blocks on S03, S06, S09, S13, S15','audit_02_survival_vs_weight.py -> audit_02_survival_vs_weight.csv, weights_decoded_per_animal.csv')
ov=pd.read_csv('audit_03a_duplicate_vectors.csv')
F['s15c_i']=int(sum(1 for d_ in [2,4,6,8,10,12] for c_ in ['W','X','Y','Z','AA','AB','AC'] if wb['S15'][f'{c_}{23+d_//2}'].value==wb['S15'][f'{c_}{72+d_//2}'].value))
s6c=[(wb['S06'].cell(r,13).value,[wb['S06'].cell(r,c).value for c in range(14,18)]) for r in range(3,31)]; s6d=[(wb['S06'].cell(r,1).value,[wb['S06'].cell(r,c).value for c in range(2,6)]) for r in range(34,62)]
assert s6c==s6d
add('Q03','Data quality',f"S06-C (bivalent vaccine, rgH5N1 at day 14) is identical to S06-D (same, day 3) in every one of its 28 rows: same day and same group flag for all four arms. The paired weight block S15-C implies 1/7 PSLN-212 survivors rather than 2/7, and its PSLN-344 columns for days 2-12 repeat the 'Vaccine + PSLN-344' columns of S15-I in {F['s15c_i']} of 42 cells. The day-14 rgH5N1 experiment therefore has no independent record and is excluded from all pooled figures.",
    'S06!M3:Q30 vs S06!A34:E61; S15!W24:AC29 vs S15!W73:AC78','audit_03_duplicates.py -> audit_03a_duplicate_vectors.csv; audit_02')
scr=pd.read_csv('audit_05_group_order_screen.csv'); out_=scr[~scr.inside_0_1].block.tolist(); assert sorted(out_)==['S01-A/72h','S03-B','S03-F']
F['screen']=dict(n=len(scr),inside=int(scr.inside_0_1.sum()))
add('Q04','Data quality',f"The printed IgG2a/IgG1 blocks S03-B and S03-F do not match their own source titres (S13-A to S13-D) under the printed headers; they match exactly when the headers are rotated (see L41). Read as printed they would show PSLN-344 as the most IgG1-skewed group; recomputed, PSLN-344 is IgG2a-skewed like young animals. A screen of all {len(scr)} single-time-point blocks that contain aged PSLN-212, aged PSLN-344 and young PSLN-212 finds the PSLN-344 mean between the other two in {int(scr.inside_0_1.sum())}; the exceptions are these two blocks and the 72-h interferon block (S01-A), where aged animals on PSLN-344 are simply slower to return to baseline.",'S03!G2:I7; S03!G9:I14; S13!A2:O7','audit_04_derived_checks.py; audit_05_group_order_screen.py -> audit_05_group_order_screen.csv')
add('Q05','Data quality',"S09-A holds two panels both labelled '16h'. After back-transformation the Ifnb1 row of the second panel (columns X-AS) reproduces the 72-h values of S01-A for all seven groups, and the first panel reproduces the 16-h values (three of the five S01-A animals in each case). The second panel is treated as 72 h. The same control animals are called 'Sham' in S01-A and 'PBS' in S09-A.",'S09!A1:AS9; S01!A3:L10','audit_04_derived_checks.py')
add('Q06','Data quality',f"Epithelial delivery of PSLN-344: S08-C as printed gives {mean('S08!B14:B18'):.1f}% dye-positive type-II cells for PSLN-344 vs {mean('S08!A14:A18'):.1f}% for the Mn-free liposome, and {mean('S08!C14:C18'):.1f}% type-I cells for the Mn-free liposome, whereas S01-B gives {mean('S01!B15:F15'):.1f}% type-I cells for the same Mn-free liposome. Columns A and B of S08-C share five exact values with the type-II and type-I columns of S01-B. The block is consistent with S01-B only if its headers are permuted; it is not used.",'S08!A13:D18; S01!A14:F17','audit_04_derived_checks.py')
add('Q07','Data quality',"S11-A (alveolar macrophages) and S11-B (neutrophils) share 35 of 100 values in identical positions, including entire animal columns (S11!G3:G7 = G10:G14, L3:M7 = L10:M14, Q3:R7 = Q10:R14). They cannot both be independent measurements of different cell types; neither is used for inference, so the dataset contains no usable neutrophil read-out.",'S11!B3:U7 vs S11!B10:U14','audit_03_duplicates.py -> audit_03c_positional_overlap.csv; audit_03d_overlap_detail.py')
wv=pd.read_csv('tidy_all_observations.csv'); wv=wv[wv.kind=='weight']; nd=int(sum(1 for v in wv.value if len(repr(float(v)).split('.')[1])>1))
F['wt_dec']=(nd,len(wv))
add('Q08','Data quality',f"Body-weight tables reuse values across experiments: identical 8-animal rows for two different groups on day 12 of S09-C; whole-animal trajectories repeated between S09-E and S09-G, and between the PSLN-344 decedent of S15-A, S15-M and S15-O (85.1% carried forward from day 6 in all three strains); S15-A Sham day 4 equals S15-M PSLN-212 day 4 for all seven animals. {nd} of {len(wv)} weight cells carry more than one decimal, and the same four-digit fractions (e.g. .4231, .8791, .4744) recur with different integer parts in up to six blocks. These tables need to be regenerated from balance records.",
    'S09!G18:AD18; S09!N40:N46 vs S09!N67:N73; S15!AA3:AA10, S15!AH103:AH110, S15!AH134:AH141; S15!I5:O5 vs S15!W105:AC105','audit_03_duplicates.py; audit_03d_overlap_detail.py')
add('Q09','Data quality',"Labels that prevent interpretation: S07-C (both groups headed 'Ly6C-CD206+'); two different experiments are each labelled S06-E and S06-F; S08 rows 89-101 hold 13 unlabelled values; 'PSLN-344/R848' in S08-A is not a defined material; the pertussis-toxin group of S02-C/S02-E has no stated adjuvant; challenge virus, dose and day are not stated for S15-L/S15-N, nor the challenge dose for S03-J; time points are not stated for S07-B, S11-E, S13-H, S14-A. S05-A/S05-B list two incompatible immunisation conditions and use an H-2Db tetramer although the default strain is BALB/c.",
    'S07!B15:C15; S06!G32, M32, G69, M69; S08!A89:D101; S08!K2; annotation PDF pp. 3-19','audit_01_n_and_labels.py; psln_blocks.py (coverage check); annotation')
add('Q11','Data quality',f"S07-A (Ly6C+CCR2+ macrophage time-course) is internally plausible but its direction is unconfirmed: as printed PSLN-344 has {F['ccr2mac_tc']['b']/F['ccr2mac_tc']['a']:.1f}-fold fewer such cells than PSLN-212 on day 5, although PSLN-344 draws in about twice as many monocytes (S01-D), induces {c16['Ccl2'][0]/c16['Ccl2'][1]:.0f}-fold more Ccl2 (S09-A) and its lungs contain {F['ccr2mac']['a']:.0f}% Ly6C+ macrophages in S07-B. No other block allows a cross-check, and S07-C on the same sheet is mislabelled. The block is reported but not used.",'S07!B2:G7; S01!G26:P26; S09!H5:J5; S09!Q5:S5; S07!E10:E14','analysis_03 -> timecourse_descriptives.csv; build_ledger.py')
add('Q10','Data quality',"File dates: the workbook was last modified on 3 September 2026 and the annotation PDF created on 15 September 2026 (document properties). Nothing in either file is dated later.",'docProps/core.xml of the workbook; PDF metadata','inspection')

# ---- programmatic checks behind the data-quality statements ------------------------------------------------
def rowvals(ref): return [round(v,4) for v in raw(ref)]
for key in ['ratio_h1','ratio_h3']:                                   # Q04: header rotation
    f=F[key]; assert abs(f['printed']['PSLN-212']-f['y'])<0.01 and abs(f['printed']['PSLN-344']-f['b'])<0.01 and abs(f['printed']['PSLN-212(Y)']-f['a'])<0.01
back=lambda ref:[round(10**v,2) for v in raw(ref)]
assert back('S09!AN3:AP3')==[round(v,2) for v in raw('S01!H8:J8')]      # Q05: second S09-A panel = S01-A 72 h (PSLN-344)
assert back('S09!Y3:AA3')==[round(v,2) for v in raw('S01!H3:J3')]       #      ... and the control group
assert back('S09!B3:D3')==[round(v,2) for v in raw('S01!B3:D3')]        #      first panel = S01-A 16 h (control)
assert len(set(rowvals('S08!A14:A18'))&set(rowvals('S01!B14:F14')))+len(set(rowvals('S08!B14:B18'))&set(rowvals('S01!B15:F15')))==5   # Q06
ov=pd.read_csv('audit_03c_positional_overlap.csv'); r_=ov[(ov.block1=='S11-A')&(ov.block2=='S11-B')].iloc[0]; assert (r_.comparable_cells,r_.identical_cells)==(100,35)   # Q07
assert rowvals('S09!G18:N18')==rowvals('S09!W18:AD18')                  # Q08: S09-C day 12, two groups identical
assert rowvals('S09!N40:N46')==rowvals('S09!N67:N73')                   #      S09-E vs S09-G animal trajectory
assert set(rowvals('S15!AA6:AA10'))=={85.1} and set(rowvals('S15!AH106:AH110'))=={85.1} and set(rowvals('S15!AH137:AH141'))=={85.1}
assert rowvals('S15!I5:O5')==rowvals('S15!W105:AC105')                  #      S15-A Sham day 4 = S15-M PSLN-212 day 4
assert len(pd.read_csv('audit_01_stated_vs_observed_n.csv').query('match==False'))==5                                   # Q01
def _clean(o):
    if isinstance(o,dict): return {('|'.join(map(str,k)) if isinstance(k,tuple) else str(k)):_clean(v) for k,v in o.items()}
    if isinstance(o,(list,tuple,set)): return [_clean(v) for v in o]
    if hasattr(o,'item'): return o.item()
    if isinstance(o,float) and o!=o: return None
    return o
json.dump(dict(F=_clean(F),L=L),open('ledger.json','w'),indent=1)
import pickle; pickle.dump(dict(F=F,L=L),open('ledger.pkl','wb'))
pd.DataFrame(L).to_csv('ledger.csv',index=False)
print(len(L),'ledger entries written; all cross-checks passed')
for e in L: print(e['id'],'|',e['statement'][:230])
