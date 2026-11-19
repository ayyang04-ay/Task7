"""Build the evidence register (E-items) directly from analysis outputs so every number in the
proposal is traceable to workbook cells + a named statistical test."""
import pandas as pd, numpy as np, json
S  = pd.read_csv('/tmp/work/summary_stats.csv')
C  = pd.read_csv('/tmp/work/contrasts.csv')
SV = pd.read_csv('/tmp/work/surv_summary.csv')
SC = pd.read_csv('/tmp/work/surv_contrasts.csv')
SP = pd.read_csv('/tmp/work/surv_pooled.csv')
RI = pd.read_csv('/tmp/work/restoration_index.csv')
DR = pd.read_csv('/tmp/work/dose_response.csv')
RX = pd.read_csv('/tmp/work/reactogenicity.csv')
TI = pd.read_csv('/tmp/work/evidence_tiers.csv').set_index('block').tier.to_dict()
tidy = pd.read_csv('/tmp/work/tidy.csv')

def fp(p):
    if p is None or (isinstance(p,float) and np.isnan(p)): return 'n/a'
    if p < 1e-3: return f'p={p:.1e}'
    return f'p={p:.3f}' if p < 0.1 else f'p={p:.2f}'
def g(block, group, time=None, analyte=None):
    q = S[(S.block==block)&(S.group==group)]
    if time is not None: q = q[q.time==time]
    if analyte is not None: q = q[q.analyte==analyte]
    assert len(q)==1, (block,group,time,analyte,len(q))
    return q.iloc[0]
def c(block, g1, g2, time=None, analyte=None):
    q = C[(C.block==block)&(C.g1==g1)&(C.g2==g2)]
    if time is not None: q = q[q.time==time]
    if analyte is not None: q = q[q.analyte==analyte]
    assert len(q)==1, (block,g1,g2,time,analyte,len(q))
    return q.iloc[0]
def sv(block, group):
    q = SV[(SV.block==block)&(SV.group==group)].iloc[0]; return q
def sc(block,g1,g2):
    q = SC[(SC.block==block)&(SC.g1==g1)&(SC.g2==g2)].iloc[0]; return q
def ri(block, time=None):
    q = RI[(RI.block==block)]
    q = q[q.time.isna()] if time is None else q[q.time==time]
    return q.iloc[0]
def fmt(x, d=1):
    if abs(x) >= 1000: return f'{x:,.0f}'
    return f'{x:.{d}f}'

E = []
def add(eid, area, claim, value, blocks, cells, method, tier=None):
    if tier is None: tier = '/'.join(sorted(set(TI.get(b.strip(),'?') for b in blocks.split(','))))
    E.append(dict(id=eid, area=area, claim=claim, value=value, blocks=blocks, cells=cells, method=method, tier=tier))

# ---------------- SURVIVAL ----------------
P = lambda lab,g1,g2: SP[(SP.analysis.str.startswith(lab))&(SP.g1==g1)&(SP.g2==g2)].iloc[0]
p1 = P('All aged','PSLN-344','PSLN-212'); p2 = P('All aged','PSLN-344','Sham'); p3 = P('All aged','PSLN-344','PSLN-212(Y)'); p4 = P('Sensitivity','PSLN-344','PSLN-212')
add('E1','Efficacy','Pooled heterosubtypic/other lethal challenge, aged mice, 9 four-arm experiments: PSLN-344 vs PSLN-212',
    f'Survival PSLN-344 {p1.surv_g1} vs PSLN-212 {p1.surv_g2}; Sham 0/63 (0%); young PSLN-212 62/63 (98%). MH risk difference +68.3 pts (95% bootstrap CI 55.6 to 79.4); stratified log-rank chi2={p1.strat_logrank_chi2}, {fp(p1.strat_logrank_p)}',
    'S06-A,S06-B,S06-C,S06-D,S06-E,S06-F,S06-G,S15-L,S15-N','S06!A3:R105; S15!A103:E161','Mantel-Haenszel risk difference (stratified bootstrap CI, 20,000 resamples); stratified log-rank')
add('E2','Efficacy','Same pool: PSLN-344 vs vehicle (Sham)',
    f'{p2.surv_g1} vs {p2.surv_g2}; MH risk difference +81.0 pts (95% CI 71.4 to 88.9); stratified log-rank {fp(p2.strat_logrank_p)}',
    'S06-A,S06-B,S06-C,S06-D,S06-E,S06-F,S06-G,S15-L,S15-N','as E1','as E1')
add('E3','Efficacy','Same pool: aged PSLN-344 vs young PSLN-212 benchmark (restoration is incomplete)',
    f'{p3.surv_g1} vs {p3.surv_g2}; MH risk difference -17.5 pts (95% CI -27.0 to -7.9); stratified log-rank {fp(p3.strat_logrank_p)}',
    'S06-A,S06-B,S06-C,S06-D,S06-E,S06-F,S06-G,S15-L,S15-N','as E1','as E1')
add('E4','Efficacy','Sensitivity: only experiments with no survival-side integrity flag (S06-A, B, E, F)',
    f'PSLN-344 {p4.surv_g1} vs PSLN-212 {p4.surv_g2}; MH risk difference +67.9 pts (95% CI 50.0 to 85.7); stratified log-rank {fp(p4.strat_logrank_p)}',
    'S06-A,S06-B,S06-E,S06-F','S06!A3:K30; S06!G34:R68','as E1')
d3 = P('Challenge at d3','PSLN-344','PSLN-212'); d14 = P('Challenge at d14','PSLN-344','PSLN-212'); d60 = P('Challenge at d60','PSLN-344','PSLN-212')
add('E5','Efficacy','Speed of onset: challenge 3 days after a single dose (S06-B, S06-D)',
    f'PSLN-344 {d3.surv_g1} vs PSLN-212 {d3.surv_g2} vs Sham 0/14; stratified log-rank {fp(d3.strat_logrank_p)}',
    'S06-B,S06-D','S06!G3:K30; S06!A34:E61','stratified log-rank')
h1 = sc('S15-H','3d Vaccine+PSLN-344','3d Vaccine'); h2 = sc('S15-H','3d Vaccine+PSLN-344','3d PSLN-344')
add('E6','Efficacy','Adjuvant, not standalone: vaccine, PSLN-344 alone, or both, 3 d before VN04 rgH5N1 (S15-H)',
    f'Vaccine+PSLN-344 6/7 vs vaccine alone 0/7 (log-rank {fp(h1.logrank_p)}) vs PSLN-344 alone 0/7 (log-rank {fp(h2.logrank_p)})',
    'S15-H','S15!A73:D93','log-rank; Fisher exact')
j1 = sc('S03-J','PSLN-344','PSLN-212'); j2 = sc('S03-J','PSLN-344','Sham')
add('E7','Efficacy','Wild-type VN04 H5N1 (BSL-3), challenge 2 d after single rgH5N1 dose (S03-J)',
    f'PSLN-344 10/10 vs PSLN-212 3/10 (log-rank {fp(j1.logrank_p)}) vs Sham 1/10 (log-rank {fp(j2.logrank_p)}). Caveat: stated n=9; one PSLN-344 record lacks a day value',
    'S03-J','S03!G17:J46','log-rank; Fisher exact')
add('E8','Efficacy','Durability: challenge at day 60 (S06-E, F, G) vs day 14 (S06-A, C)',
    f'PSLN-344 d60 {d60.surv_g1} vs PSLN-212 {d60.surv_g2} (stratified log-rank {fp(d60.strat_logrank_p)}); young PSLN-212 d60 21/21 (100%). PSLN-344 d14 {d14.surv_g1}; d14 vs d60 Fisher p=0.11',
    'S06-A,S06-C,S06-E,S06-F,S06-G','S06!A3:E30; S06!M3:Q30; S06!G34:R68; S06!A71:F105','stratified log-rank; Fisher exact')
l1 = sc('S15-L','PSLN-344','PSLN-212'); n1 = sc('S15-N','PSLN-344','PSLN-212'); n2 = sc('S15-N','PSLN-344','Sham')
add('E9','Efficacy','Genetic background: aged C57BL/6 (S15-L) and Swiss Webster (S15-N)',
    f'C57BL/6: PSLN-344 6/7 vs PSLN-212 0/7 vs Sham 0/7 (log-rank vs PSLN-212 {fp(l1.logrank_p)}); Swiss Webster: 6/7 vs 2/7 vs 0/7 (vs PSLN-212 {fp(n1.logrank_p)}; vs Sham {fp(n2.logrank_p)}). Challenge virus/timing not stated',
    'S15-L,S15-N','S15!A103:E130; S15!A134:E161','log-rank')
i1 = sc('S06-E2_imprint','Naive+PSLN-344','Naive+PSLN-212'); i2 = sc('S06-F2_imprint','Imprinting+PSLN-344','Imprinting+PSLN-212')
add('E10','Efficacy','Prior influenza exposure ("imprinting"), 14-month mice (S06-E2, S06-F2)',
    f'PR8 challenge: PSLN-344 6/7 (naive) and 6/7 (imprinted) vs PSLN-212 0/7 and 4/7. Perth H3N2 challenge: PSLN-344 6/7 and 6/7 vs PSLN-212 0/7 and 0/7 (imprinted 344 vs 212 log-rank {fp(i2.logrank_p)})',
    'S06-E2_imprint,S06-F2_imprint','S06!G70:Q98','log-rank')
add('E11','Efficacy','Young mice: no differentiation between formulations (ceiling)',
    'PSLN-344Y 8/8 = PSLN-212Y 8/8 in each of S09-B, S09-D, S09-F (d180 challenge); Sham 0/8, 0/8, 0/7. S13-E: CMP-204(Y) 7/7 = PSLN-344(Y) 7/7 vs Sham 1/7',
    'S09-B,S09-D,S09-F,S13-E','S09!A12:D88; S13!R3:V30','descriptive; log-rank vs Sham p<=0.0016')
i3 = sc('S03-I','PSLN-212','CMP-204')
add('E12','Efficacy','Homologous 10x CA09 challenge, aged (S03-I); internally inconsistent',
    f'PSLN-344 7/7, young PSLN-212 7/7, CMP-204 3/7, PSLN-212 0/7, Sham 0/7. PSLN-212 does worse than the cGAMP comparator (log-rank {fp(i3.logrank_p)}) despite higher titres (E35, E36); paired weights (S13-F) contradict it',
    'S03-I','S03!A17:F51','log-rank')

# ---------------- TARGET ENGAGEMENT ----------------
a344 = g('S01-A_16h','PSLN-344'); a212 = g('S01-A_16h','PSLN-212'); ay = g('S01-A_16h','PSLN-212(Y)'); asham = g('S01-A_16h','Sham'); acmp=g('S01-A_16h','CMP-204')
ca = c('S01-A_16h','PSLN-344','PSLN-212'); cy = c('S01-A_16h','PSLN-344','PSLN-212(Y)'); cc_ = c('S01-A_16h','PSLN-344','CMP-204')
add('E13','Target engagement','Lung Ifnb1 16 h after intranasal dose (no vaccine), aged vs young (S01-A)',
    f'Geometric mean fold: aged PSLN-344 {a344.center:.1f} vs aged PSLN-212 {a212.center:.1f} (ratio {ca.effect:.2f}, {fp(ca.welch_p)}) vs young PSLN-212 {ay.center:.1f} (ratio {cy.effect:.2f}, {fp(cy.welch_p)}); Sham {asham.center:.2f}; CMP-204 {acmp.center:.1f} (PSLN-344/CMP-204 {cc_.effect:.1f}x, {fp(cc_.welch_p)}). Restoration index {ri("S01-A_16h").RI:.2f} (95% CI {ri("S01-A_16h").RI_lo:.2f} to {ri("S01-A_16h").RI_hi:.2f})',
    'S01-A_16h', f'{a344.cells}; {a212.cells}; {ay.cells}', 'Welch t-test on log10; bootstrap restoration index')
dr = DR.set_index('group')
m = tidy[tidy.block=='S08-A'].groupby(['group','time']).value.mean()
add('E14','Target engagement','Dose-response, lung Ifnb1 at 16 h (S08-A, n=3/dose)',
    f'PSLN-344: {m["PSLN-344"][1]:.1f}/{m["PSLN-344"][5]:.1f}/{m["PSLN-344"][10]:.1f}/{m["PSLN-344"][20]:.1f}/{m["PSLN-344"][40]:.1f}-fold at 1/5/10/20/40 ug; PSLN-212 max {m["PSLN-212"][40]:.1f} at 40 ug. PSLN-344 at 10 ug exceeds PSLN-212 at 40 ug (>=4x dose-sparing). 20->40 ug adds only +{dr.loc["PSLN-344","gain_40_vs_20_pct"]:.1f}%',
    'S08-A','S08!A3:M7','descriptive; Emax fit (ED50 imprecise, SE ~50%)')
b72 = c('S01-A_72h','PSLN-344','PSLN-212')
add('E15','Target engagement','Transience: lung Ifnb1 at 72 h (S01-A)',
    f'aged PSLN-344 {g("S01-A_72h","PSLN-344").center:.1f} vs PSLN-212 {g("S01-A_72h","PSLN-212").center:.1f}-fold (ratio {b72.effect:.2f}, {fp(b72.welch_p)})',
    'S01-A_72h','S01!H3:L10','Welch t-test on log10')
ck = {a: c('S09-A_panel1_A-U','PSLN-344','PSLN-212',analyte=a) for a in ['Ccl2','Ccl3','Il6','Ccl5','Tnf','Il10','Ifnb1']}
add('E16','Innate amplification','Lung cytokine/chemokine transcripts at 16 h, PSLN-344 vs PSLN-212 (S09-A panel 1, n=3; log10 data)',
    '; '.join(f'{a} {10**ck[a].effect:.1f}x ({fp(ck[a].welch_p)})' for a in ['Ccl2','Ccl3','Ccl5','Il6','Tnf','Il10']),
    'S09-A_panel1_A-U','S09!B3:V9','Welch t-test on log10 values')
f16 = c('S02-F','PSLN-344','PSLN-212',time=16.0); f36 = c('S02-F','PSLN-344','PSLN-212',time=36.0); f72 = c('S02-F','PSLN-344','PSLN-212',time=72.0)
add('E17','Innate amplification','Lung Gm-csf after vaccination (S02-F)',
    f'PSLN-344 vs PSLN-212: {f16.effect:.1f}x at 16 h ({fp(f16.welch_p)}), {f36.effect:.1f}x at 36 h ({fp(f36.welch_p)}), {f72.effect:.1f}x at 72 h ({fp(f72.welch_p)}); PSLN-344 vs Sham {c("S02-F","PSLN-344","Sham",time=36.0).effect:.1f}x at 36 h',
    'S02-F','S02!B17:P19','Welch t-test on log10')
# ---------------- MYELOID ----------------
md = {k: g('S01-D',k,time=4.0).center for k in ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']}
cd4 = c('S01-D','PSLN-344','PSLN-212',time=4.0)
add('E18','Myeloid','Lung monocytes at day 4 (S01-D)',
    f'PSLN-344 {md["PSLN-344"]:.1f}% vs PSLN-212 {md["PSLN-212"]:.1f}% ({fp(cd4.welch_p)}) vs Sham {md["Sham"]:.1f}% vs young {md["PSLN-212(Y)"]:.1f}%; group x time interaction p=4.5e-07 (two-way ANOVA)',
    'S01-D','S01!B26:U26','Welch t-test; two-way ANOVA')
m1 = c('S07-B_Mono','PSLN-344+INCB3344','PSLN-344'); m2 = c('S07-B_Ly6CMac','PSLN-344+INCB3344','PSLN-344')
add('E19','Myeloid','CCR2 dependence (INCB3344) after PSLN-344 (S07-B)',
    f'monocytes {g("S07-B_Mono","PSLN-344").center:.1f}% -> {g("S07-B_Mono","PSLN-344+INCB3344").center:.1f}% ({fp(m1.welch_p)}); Ly6C+ macrophages {g("S07-B_Ly6CMac","PSLN-344").center:.1f}% -> {g("S07-B_Ly6CMac","PSLN-344+INCB3344").center:.1f}% ({fp(m2.welch_p)}). Timepoint not stated',
    'S07-B_Mono,S07-B_Ly6CMac','S07!B10:F14','Welch t-test')
cb = c('S11-C','CBX+','CBX-')
add('E20','Myeloid','Gap-junction blockade (carbenoxolone) before PSLN-344 vaccination (S11-C)',
    f'recruited monocytes {g("S11-C","CBX-").center:.1f}% -> {g("S11-C","CBX+").center:.1f}% ({fp(cb.welch_p)})',
    'S11-C','S11!A17:B21','Welch t-test')
ifn = c('S12-A','IFNAR-/- to WT','WT to WT')
add('E21','Myeloid','IFNAR dependence of monocyte infiltration (S12-A, young, n=3) - NOT established',
    f'IFNAR-/- BM {g("S12-A","IFNAR-/- to WT").center:.1f}% vs WT BM {g("S12-A","WT to WT").center:.1f}% ({fp(ifn.welch_p)})',
    'S12-A','S12!A3:B5','Welch t-test')
h1_ = c('S02-H','IFN w/o cDC','WT w/o cDC'); h2_ = c('S02-H','GMCSF','IFN w/o cDC')
add('E22','Myeloid','moDC differentiation needs IFNAR and is rescued by GM-CSF (S02-H, BM chimeras, PSLN-344)',
    f'moDC from IFNAR-/- BM {g("S02-H","IFN w/o cDC").center:.1f}% vs WT {g("S02-H","WT w/o cDC").center:.1f}% ({fp(h1_.welch_p)}); + GM-CSF {g("S02-H","GMCSF").center:.1f}% ({fp(h2_.welch_p)} vs IFNAR-/-)',
    'S02-H','S02!B30:F34','Welch t-test')
gg = c('S02-G','PSLN-212+GM-CSF','PSLN-212')
add('E23','Myeloid','GM-CSF supplementation converts the PSLN-212 response toward moDC (S02-G)',
    f'Ly6C+CD11c+MHC-II+ cells {g("S02-G","PSLN-212+GM-CSF").center:.1f}% vs PSLN-212 {g("S02-G","PSLN-212").center:.1f}% ({fp(gg.welch_p)}) vs GM-CSF alone {g("S02-G","GM-CSF").center:.1f}%',
    'S02-G','S02!B22:D26','Welch t-test')
s7 = c('S07-A','PSLN-344','PSLN-212',time=5.0); s7b = c('S07-A','PSLN-344','PSLN-212',time=10.0)
add('E24','Myeloid','Inflammatory Ly6C+CCR2+ macrophages accumulate with PSLN-212, not PSLN-344 (S07-A, n=3)',
    f'day 5: PSLN-212 {g("S07-A","PSLN-212",time=5.0).center:.1f} vs PSLN-344 {g("S07-A","PSLN-344",time=5.0).center:.1f} x10^5 cells ({fp(s7.welch_p)}); day 10: {g("S07-A","PSLN-212",time=10.0).center:.1f} vs {g("S07-A","PSLN-344",time=10.0).center:.1f} ({fp(s7b.welch_p)})',
    'S07-A','S07!B3:G7','Welch t-test; two-way ANOVA interaction p=8.6e-05')
# ---------------- DC ----------------
e4 = c('S01-E','PSLN-344','PSLN-212',time=4.0)
add('E25','Dendritic cells','Lung CD11b+ DC, day 4 (S01-E)',
    f'PSLN-344 {g("S01-E","PSLN-344",time=4.0).center:.1f}% vs PSLN-212 {g("S01-E","PSLN-212",time=4.0).center:.1f}% (Welch {fp(e4.welch_p)}; Mann-Whitney {fp(e4.mannwhitney_p)}) vs young {g("S01-E","PSLN-212(Y)",time=4.0).center:.1f}%',
    'S01-E','S01!B32:Z32','Welch; Mann-Whitney')
f1 = c('S01-F','PSLN-344','PSLN-212')
add('E26','Dendritic cells','Lung cDC1 (XCR1+), 72 h (S01-F)',
    f'PSLN-344 {g("S01-F","PSLN-344").center:.1f}% vs PSLN-212 {g("S01-F","PSLN-212").center:.1f}% ({fp(f1.welch_p)}) vs young {g("S01-F","PSLN-212(Y)").center:.1f}%; Sham {g("S01-F","Sham").center:.1f}%',
    'S01-F','S01!B36:Z36','Welch')
a2 = c('S02-A','PSLN-344','PSLN-212')
add('E27','Dendritic cells','CCR7+ migratory CD11b+ DC in lung, 72 h (S02-A)',
    f'PSLN-344 {g("S02-A","PSLN-344").center:.1f}% vs PSLN-212 {g("S02-A","PSLN-212").center:.1f}% ({fp(a2.welch_p)}) vs young {g("S02-A","PSLN-212(Y)").center:.1f}%; Sham {g("S02-A","Sham").center:.1f}%',
    'S02-A','S02!A3:D7','Welch')
c2 = c('S02-C','PSLN-344','PSLN-212'); c2p = c('S02-C','PTX','PSLN-344')
add('E28','Dendritic cells','Antigen-bearing DC in MLN at 36 h (S02-C)',
    f'PSLN-344 {g("S02-C","PSLN-344").center:.1f}% vs PSLN-212 {g("S02-C","PSLN-212").center:.1f}% ({fp(c2.welch_p)}); pertussis toxin {g("S02-C","PTX").center:.1f}% ({fp(c2p.welch_p)} vs PSLN-344); young {g("S02-C","PSLN-212(Y)").center:.1f}%',
    'S02-C','S02!K3:O7','Welch')
d40 = c('S02-D_CD40','PSLN-344','PSLN-212'); d86 = c('S02-D_CD86','PSLN-344','PSLN-212')
add('E29','Dendritic cells','Costimulatory maturation of MLN CD11b+ DC, day 3 (S02-D) - the largest residual gap',
    f'CD40+: PSLN-344 {g("S02-D_CD40","PSLN-344").center:.1f}% vs PSLN-212 {g("S02-D_CD40","PSLN-212").center:.1f}% ({fp(d40.welch_p)}) vs young {g("S02-D_CD40","PSLN-212(Y)").center:.1f}% (RI {ri("S02-D_CD40").RI:.2f}, 95% CI {ri("S02-D_CD40").RI_lo:.2f}-{ri("S02-D_CD40").RI_hi:.2f}); CD86+: {g("S02-D_CD86","PSLN-344").center:.1f}% vs {g("S02-D_CD86","PSLN-212").center:.1f}% ({fp(d86.welch_p)}) vs young {g("S02-D_CD86","PSLN-212(Y)").center:.1f}% (RI {ri("S02-D_CD86").RI:.2f})',
    'S02-D_CD40,S02-D_CD86','S02!A10:I14','Welch; bootstrap RI')
e2 = c('S02-E','PSLN-344','PSLN-212')
add('E30','Dendritic cells','Ex vivo OT-I priming by MLN CD11b+ DC (S02-E)',
    f'PSLN-344 {g("S02-E","PSLN-344").center:.1f}% vs PSLN-212 {g("S02-E","PSLN-212").center:.1f}% ({fp(e2.welch_p)}) vs young {g("S02-E","PSLN-212(Y)").center:.1f}%; PTX {g("S02-E","PTX").center:.1f}%',
    'S02-E','S02!K10:O14','Welch')
# ---------------- B/Tfh/regulatory ----------------
t1 = c('S04-A_ICOShi','PSLN-344','PSLN-212'); t2 = c('S04-B_Foxp3','PSLN-344','PSLN-212'); k3 = c('S03-K','PSLN-344','PSLN-212')
add('E31','Germinal centre','Tfh (CXCR5+PD1+ICOS-hi), day 7 (S04-A)',
    f'PSLN-344 {g("S04-A_ICOShi","PSLN-344").center:.1f}% vs PSLN-212 {g("S04-A_ICOShi","PSLN-212").center:.1f}% ({fp(t1.welch_p)}) vs young {g("S04-A_ICOShi","PSLN-212(Y)").center:.1f}%; Sham {g("S04-A_ICOShi","Sham").center:.2f}%',
    'S04-A_ICOShi','S04!G2:K5','Welch')
add('E32','Germinal centre','Tfr (Foxp3+ of CXCR5+ICOS-hi), day 7 (S04-B)',
    f'PSLN-344 {g("S04-B_Foxp3","PSLN-344").center:.1f}% vs PSLN-212 {g("S04-B_Foxp3","PSLN-212").center:.1f}% ({fp(t2.welch_p)}) vs young {g("S04-B_Foxp3","PSLN-212(Y)").center:.1f}%; day 30 (S04-C): {g("S04-C","PSLN-344").center:.1f}% vs {g("S04-C","PSLN-212").center:.1f}% ({fp(c("S04-C","PSLN-344","PSLN-212").welch_p)}). The "Tfh:Tfr" block is derived from these values',
    'S04-B_Foxp3,S04-C','S04!A8:D12; S04!A22:D26','Welch')
add('E33','Germinal centre','GC B cells (CXCR5+GL7+), MLN day 7 (S03-K); Aicda/E47 (S03-L, n=3)',
    f'GC B {g("S03-K","PSLN-344").center:.1f}% vs {g("S03-K","PSLN-212").center:.1f}% ({fp(k3.welch_p)}) vs young {g("S03-K","PSLN-212(Y)").center:.1f}%; Aicda {c("S03-L_Aicda","PSLN-344","PSLN-212").effect:.1f}x ({fp(c("S03-L_Aicda","PSLN-344","PSLN-212").welch_p)}), E47 {c("S03-L_E47","PSLN-344","PSLN-212").effect:.1f}x ({fp(c("S03-L_E47","PSLN-344","PSLN-212").welch_p)})',
    'S03-K,S03-L_Aicda','S03!L17:O21; S03!L26:Q28','Welch (log10 for qPCR)')
tr = c('S04-D','PSLN-344','PSLN-212'); cd2 = c('S11-E','PSLN-344','PSLN-212')
add('E34','Regulatory','Lung Treg day 7 (S04-D, n=3) and lung CD206+ macrophages (S11-E, timepoint not stated)',
    f'Treg {g("S04-D","PSLN-344").center:.1f}% vs PSLN-212 {g("S04-D","PSLN-212").center:.1f}% ({fp(tr.welch_p)}), young {g("S04-D","PSLN-212(Y)").center:.1f}%; CD206+ macrophages {g("S11-E","PSLN-344").center:.1f}% vs {g("S11-E","PSLN-212").center:.1f}% ({fp(cd2.welch_p)}), Sham {g("S11-E","Sham").center:.1f}%, young {g("S11-E","PSLN-212(Y)").center:.1f}%',
    'S04-D,S11-E','S04!A29:D31; S11!A31:D35','Welch')
# ---------------- ANTIBODY ----------------
def titre_line(b):
    x344=g(b,'PSLN-344'); x212=g(b,'PSLN-212'); xy=g(b,'PSLN-212(Y)'); xs=g(b,'Sham')
    cc1 = c(b,'PSLN-344','PSLN-212')
    s = f'GMT PSLN-344 {fmt(x344.center,0)} vs PSLN-212 {fmt(x212.center,0)} ({cc1.effect:.1f}x, {fp(cc1.welch_p)}) vs young {fmt(xy.center,0)}; Sham {fmt(xs.center,0)}'
    try:
        xc=g(b,'CMP-204'); s += f'; CMP-204 {fmt(xc.center,0)}'
    except AssertionError: pass
    return s
add('E35','Antibody','Serum IgG anti-CA09 H1N1, day 14 (S03-A)', titre_line('S03-A'),'S03-A','S03!A3:E7','Welch t-test on log10 titres')
add('E36','Antibody','HAI anti-CA09, day 14 (S03-C; values <10 set to 5)', titre_line('S03-C'),'S03-C','S03!K3:O7','Welch t-test on log10 titres')
add('E37','Antibody','Neutralising titre anti-CA09, day 14 (S03-D)', titre_line('S03-D'),'S03-D','S03!Q3:U7','Welch t-test on log10 titres')
add('E38','Antibody','Aichi H3N2: IgG (S03-E), HAI (S03-G), neutralising (S03-H), day 14',
    'IgG ' + titre_line('S03-E') + ' | HAI ' + titre_line('S03-G') + ' | Neut ' + titre_line('S03-H'),'S03-E,S03-G,S03-H','S03!A10:U14','Welch t-test on log10 titres')
r1 = c('S13-AB_ratio_CA09','PSLN-344','PSLN-212'); r2 = c('S13-CD_ratio_Aichi','PSLN-344','PSLN-212')
add('E39','Antibody','IgG2a/IgG1 (Th1 skew) recomputed from primary subclass titres (S13-A..D) - replaces mislabelled S03-B/F',
    f'CA09: PSLN-344 {g("S13-AB_ratio_CA09","PSLN-344").center:.2f} vs PSLN-212 {g("S13-AB_ratio_CA09","PSLN-212").center:.2f} ({r1.effect:.1f}x, {fp(r1.welch_p)}) vs young {g("S13-AB_ratio_CA09","PSLN-212(Y)").center:.2f}; Aichi: {g("S13-CD_ratio_Aichi","PSLN-344").center:.2f} vs {g("S13-CD_ratio_Aichi","PSLN-212").center:.2f} ({r2.effect:.1f}x, {fp(r2.welch_p)}) vs young {g("S13-CD_ratio_Aichi","PSLN-212(Y)").center:.2f}',
    'S13-A,S13-B,S13-C,S13-D','S13!A3:O7','Welch on log10 of per-animal ratio')
add('E40','Antibody','After boost (day 28; S13-I, S13-J)',
    'CA09 IgG ' + titre_line('S13-I') + ' | Aichi IgG ' + titre_line('S13-J'),'S13-I,S13-J','S13!F53:P57','Welch t-test on log10 titres')
# ---------------- CD8 ----------------
def pct_line(b):
    x344=g(b,'PSLN-344'); x212=g(b,'PSLN-212'); xy=g(b,'PSLN-212(Y)'); xs=g(b,'Sham'); cc1=c(b,'PSLN-344','PSLN-212')
    return f'{x344.center:.1f}% vs PSLN-212 {x212.center:.1f}% ({fp(cc1.welch_p)}) vs young {xy.center:.1f}%; Sham {xs.center:.1f}%'
add('E41','CD8 T cells','Lung CD8 proliferation (Ki-67+, S05-D) and cytotoxic (GZMB+, S05-E), day 3',
    'Ki-67+ ' + pct_line('S05-D') + ' | GZMB+ ' + pct_line('S05-E') + f' (GZMB RI {ri("S05-E").RI:.2f})','S05-D,S05-E','S05!A19:D30','Welch')
add('E42','CD8 T cells','Cross-reactive (rgH5N1-restimulated) IFN-g+ CD8 in MLN: day 14 (S05-F) and day 60 (S05-G); GZMB+ day 60 (S05-H)',
    'd14 ' + pct_line('S05-F') + ' | d60 ' + pct_line('S05-G') + ' | GZMB d60 ' + pct_line('S05-H'),'S05-F,S05-G,S05-H','S05!A33:D51','Welch')
add('E43','CD8 T cells','Lung resident-memory CD8 (CD69+CD103+), day 25 (S05-I)',
    pct_line('S05-I') + f' (RI {ri("S05-I").RI:.2f}, 95% CI {ri("S05-I").RI_lo:.2f}-{ri("S05-I").RI_hi:.2f})','S05-I','S05!A54:D58','Welch; bootstrap RI', tier='B')
add('E44','CD8 T cells','IFN-g+ CD8 after CA09 or Aichi restimulation (S14-A; timepoint not stated)',
    'H1N1 ' + pct_line('S14-A_H1N1') + ' | H3N2 ' + pct_line('S14-A_H3N2'),'S14-A_H1N1,S14-A_H3N2','S14!A3:I7','Welch')
i2_ = c('S02-I','PSLN-344(Y)+INCB3344','PSLN-344(Y)'); pt = c('S05-C','MLN+PTX','MLN'); pl = c('S05-C','Lung+PTX','Lung')
add('E45','CD8 T cells','CCR2 blockade abolishes lung GZMB+ CD8 (S02-I, young); PTX blocks MLN but not lung OT-I proliferation (S05-C, n=3)',
    f'GZMB+ CD8 {g("S02-I","PSLN-344(Y)").center:.1f}% -> {g("S02-I","PSLN-344(Y)+INCB3344").center:.1f}% ({fp(i2_.welch_p)}); OT-I MLN {g("S05-C","MLN").center:.1f}% -> {g("S05-C","MLN+PTX").center:.1f}% ({fp(pt.welch_p)}); lung {g("S05-C","Lung").center:.1f}% vs {g("S05-C","Lung+PTX").center:.1f}% ({fp(pl.welch_p)})',
    'S02-I,S05-C','S02!H30:I34; S05!A13:D15','Welch')
# ---------------- DELIVERY ----------------
sp = c('S01-C','SPA/D','WT'); b2 = c('S01-B','AECII/PSLN-SRB','AECII/FreeSRB'); s8 = c('S08-C','AECII-PSLN-344-SRB','AECII-PSLN-SRB'); s8b = c('S08-C','AECI-PSLN-344-SRB','AECI-PSLN-SRB')
add('E46','Delivery','Alveolar macrophage uptake depends on surfactant proteins A/D (S01-C, n=4)',
    f'DiD+ AM: WT {g("S01-C","WT").center:.1f}% vs Sftpa1-/-Sftpd-/- {g("S01-C","SPA/D").center:.1f}% ({fp(sp.welch_p)})','S01-C','S01!B20:E21','Welch')
add('E47','Delivery','Epithelial uptake: liposome vs free dye (S01-B) and Mn2+ formulation vs non-Mn liposome (S08-C)',
    f'AECII SRB+: PSLN-SRB {g("S01-B","AECII/PSLN-SRB").center:.1f}% vs free SRB {g("S01-B","AECII/FreeSRB").center:.2f}% ({fp(b2.welch_p)}); PSLN-344-SRB {g("S08-C","AECII-PSLN-344-SRB").center:.1f}% vs PSLN-SRB {g("S08-C","AECII-PSLN-SRB").center:.1f}% ({fp(s8.welch_p)}); AECI {g("S08-C","AECI-PSLN-344-SRB").center:.1f}% vs {g("S08-C","AECI-PSLN-SRB").center:.1f}% ({fp(s8b.welch_p)})',
    'S01-B,S08-C','S01!B14:F17; S08!A14:D18','Welch')
# ---------------- SAFETY / CMC ----------------
cn = {a: (c(f'S10-A_{a}','PSLN-344','PBS'), c(f'S10-A_{a}','CT','PBS'), c(f'S10-A_{a}','PSLN-344','Sham')) for a in ['Ifnb1','Tnf','Isg15']}
add('E48','Safety','CNS transcripts 36 h after intranasal vaccine +/- PSLN-344 or cholera toxin (S10-A, aged, n=5)',
    '; '.join(f'{a}: PSLN-344 {cn[a][0].effect:.2f}x PBS ({fp(cn[a][0].welch_p)}), CT {cn[a][1].effect:.1f}x ({fp(cn[a][1].welch_p)}), PSLN-344 vs Sham {fp(cn[a][2].welch_p)}' for a in cn),
    'S10-A_Ifnb1,S10-A_Tnf,S10-A_Isg15','S10!A3:N7','Welch on log10; no multiplicity adjustment')
rx = RX.set_index('group')
add('E49','Safety','Reactogenicity: body-weight nadir after vaccination, no challenge (S08-D, n=5)',
    f'Vaccine alone {rx.loc["Vaccine","mean_nadir"]:.1f}%; PSLN-344 {rx.loc["PSLN-344","mean_nadir"]:.1f}% (p={rx.loc["PSLN-344","welch_p_vs_vaccine"]:.3f} vs vaccine); PSLN-212 {rx.loc["PSLN-212","mean_nadir"]:.1f}%; PSLN-212/R848 {rx.loc["PSLN-212/R848","mean_nadir"]:.1f}% (p={rx.loc["PSLN-212/R848","welch_p_vs_vaccine"]:.3f}), 4/5 animals at day 10',
    'S08-D','S08!B21:AE26','per-animal nadir days 2-10; Welch vs vaccine')
ee = tidy[tidy.block=='S08-B'].groupby('group').value.agg(['mean','std'])
add('E50','CMC','Encapsulation efficiency by A260 (S08-B, n=3)',
    '; '.join(f'{k} {v["mean"]:.1f}% (SD {v["std"]:.1f})' for k,v in ee.iterrows()),'S08-B','S08!A11:O11','descriptive')
r8 = {a: c('S09-A_panel1_A-U','PSLN-212/R848','PSLN-212',analyte=a) for a in ['Tnf','Il10','Il6']}
add('E51','Ruled out','R848 combinations: weaker or more inflammatory',
    f'Ifnb1 16 h (S01-A): PSLN-R848 {g("S01-A_16h","PSLN-R848").center:.1f}x, PSLN-212/R848 {g("S01-A_16h","PSLN-212/R848").center:.1f}x vs PSLN-344 {a344.center:.1f}x; S08-A at 20 ug: PSLN-344/R848 {m["PSLN-344/R848"][20]:.1f} vs PSLN-344 {m["PSLN-344"][20]:.1f}; PSLN-212/R848 vs PSLN-212 lung Tnf {10**r8["Tnf"].effect:.0f}x ({fp(r8["Tnf"].welch_p)}), Il10 {10**r8["Il10"].effect:.0f}x ({fp(r8["Il10"].welch_p)}); weight nadir {rx.loc["PSLN-212/R848","mean_nadir"]:.1f}% with 1 animal lost (E49)',
    'S01-A_16h,S08-A,S09-A_panel1_A-U,S08-D','S01!B3:F10; S08!K3:M7; S09!H3:P9','Welch')
cm = c('S03-A','PSLN-344','CMP-204'); cm2 = c('S03-C','PSLN-344','CMP-204')
add('E52','Ruled out','cGAMP comparator (CMP-204, prior-art analogue) vs PSLN-344, aged',
    f'IgG anti-CA09 {cm.effect:.0f}x lower than PSLN-344 ({fp(cm.welch_p)}); HAI {cm2.effect:.0f}x lower ({fp(cm2.welch_p)}); Ifnb1 {cc_.effect:.1f}x lower (E13); survival S03-I 3/7 vs 7/7 (Tier B)',
    'S03-A,S03-C,S01-A_16h,S03-I','S03!A3:O7','Welch on log10')


sh = g('S01-A_16h','Sham'); v1 = c('S10-A_Ifnb1','Sham','PBS'); v2 = c('S10-A_Tnf','Sham','PBS'); v3 = c('S10-A_Isg15','Sham','PBS')
add('E53','Vehicle','The vehicle (empty PSLN, "Sham") is inert, as a vehicle should be',
    f'Lung Ifnb1 16 h: Sham {sh.center:.2f}-fold (95% CI {sh.ci_lo:.2f}-{sh.ci_hi:.2f}) vs untreated; CNS Sham vs PBS: Ifnb1 {v1.effect:.2f}x ({fp(v1.welch_p)}), Tnf {v2.effect:.2f}x ({fp(v2.welch_p)}), Isg15 {v3.effect:.2f}x ({fp(v3.welch_p)}); vaccine + vehicle 0/63 survival in aged mice (E2)',
    'S01-A_16h,S10-A_Ifnb1','S01!B3:F3; S10!A3:N7','geometric mean with t-CI on log10; Welch on log10')

add('E54','Efficacy','Per-experiment consistency across the 9 aged four-arm experiments',
    'PSLN-344 beat vehicle (log-rank p<0.05) in 9/9 and PSLN-212 in 8/9 experiments (exception S15-N, p=0.056). PSLN-212 never significantly increased end-of-study survival over vehicle in any experiment (Fisher p>=0.46 in all 9), although it delayed death in 5/9 (log-rank p<0.05)',
    'S06-A,S06-B,S06-C,S06-D,S06-E,S06-F,S06-G,S15-L,S15-N','as E1','per-experiment log-rank and Fisher exact')

H = pd.read_csv('/tmp/work/hedges_g.csv'); H['absg']=H.hedges_g.abs(); H=H.sort_values('absg',ascending=False).reset_index(drop=True)
def hl(r):
    t = '' if pd.isna(r.time) else (f' {int(r.time)} h' if r.block=='S02-F' else (f' {int(r.time)} ug' if r.block=='S08-A' else f' d{int(r.time)}'))
    a = '' if (pd.isna(r.analyte) or r.analyte=='') else f' {r.analyte}'
    return f'{r.block}{a}{t} g={r.hedges_g:.2f} (n={r.n})'
add('E55','Biomarkers','Standardised effect size (Hedges g), PSLN-344 vs PSLN-212 (aged), across all Tier A/B readouts',
    f'{len(H)} readout-timepoints ranked; top 6: ' + '; '.join(hl(r) for r in H.head(6).itertuples()) + '. Full ranking in workbook sheet Hedges_g',
    'all Tier A/B blocks with both groups','see workbook','Hedges g (bias-corrected), log10 scale for titres/fold-changes', tier='A/B')
add('E56','Study design','Simulated power of a two-arm survival comparison (Fisher exact, two-sided alpha=0.05, 4,000 simulations/scenario)',
    'Observed effect (81% vs 13%): n=7/arm 0.61, n=10 0.80, n=12 0.93, n=15 0.96. If the true difference is 40 pts (60% vs 20%): n=15 0.45, n=20 0.64, n=25 0.80. The historical n=7 design therefore had ~61% power per experiment at the observed effect',
    'S06-A,S06-B,S06-E,S06-F','derived from E1/E4 rates','Monte Carlo simulation', tier='A')

EV = pd.DataFrame(E)
EV.to_csv('/tmp/work/evidence_register.csv', index=False)
with open('/tmp/work/evidence_register.json','w') as f: json.dump(E, f, indent=1)
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',400)
for e in E: print(e['id'], '|', e['tier'], '|', e['claim'], '\n    ', e['value'])
