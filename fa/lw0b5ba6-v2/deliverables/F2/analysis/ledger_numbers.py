"""Every number used in the proposal is computed here from the workbook and registered in the evidence ledger."""
import numpy as np, pandas as pd
from scipy import stats
from statlib import *
from blocks import *

LEDGER = []
N = {}
def reg(key, value, text, desc, blocks, cells, method):
    """value: raw numeric (or tuple); text: formatted string used in the document"""
    eid = f'E{len(LEDGER)+1:03d}'
    LEDGER.append(dict(ID=eid, Key=key, Value_as_cited=text, Description=desc, Source_blocks=blocks, Cells=cells, Method=method, Raw=str(value)))
    N[key] = text
    return text

def cells_of(block, group=None, analyte=None, day=None, kind=None):
    for D in (B, T, S, W):
        if block in D:
            d = D[block]; break
    if group is not None: d = d[d.group==group]
    if analyte is not None: d = d[d.analyte==analyte]
    if day is not None:
        col = [c for c in d.columns if c in ('day','time','dose_ug')][0]
        d = d[d[col].astype(str)==str(day)]
    c = d['cellref'].tolist()
    return f"{c[0]}:{c[-1].split('!')[1]}"

def sv(block, group):
    d = S[block]; d = d[d.group==group]; return int((d.event==0).sum()), len(d)
def pool(items):
    s = sum(sv(b,g)[0] for b,g in items); n = sum(sv(b,g)[1] for b,g in items); return s, n
def pct(s, n): return f'{s}/{n} ({100*s/n:.0f}%)'
def ci(s, n):
    lo, hi = cp_ci(s, n); return f'{100*lo:.0f}–{100*hi:.0f}%'

# ---------------------------------------------------------------- survival
A_blocks = ['S03-I','S03-J','S06-A','S06-B','S06-C','S06-D','S06-E','S06-F','S06-G']
B_blocks = ['S06-A','S06-B','S06-D','S06-E','S06-F','S06-G']
cellsA = 'S03!A17:F51; S03!G17:J46; S06!A3:Q30; S06!A34:R68; S06!A71:F105'
for g, key in [('PSLN-344','344'),('PSLN-212','212'),('Sham','sham')]:
    s, n = pool([(b,g) for b in A_blocks])
    reg(f'survA_{key}', (s,n), pct(s,n), f'Pooled 14-day survival, aged BALB/c, vaccine + {g}, nine challenge experiments as printed', ', '.join(A_blocks), cellsA, 'Sum of survivors / animals; event column 0 = alive at end of observation')
    reg(f'survA_{key}_ci', (s,n), ci(s,n), f'Exact (Clopper-Pearson) 95% CI for the pooled proportion, {g}', ', '.join(A_blocks), cellsA, 'Clopper-Pearson')
    s, n = pool([(b,g) for b in B_blocks])
    reg(f'survB_{key}', (s,n), pct(s,n), f'Pooled survival, aged BALB/c, {g}, conservative set (S03-I, S03-J, S06-C removed for unresolved flags Q03/Q10/Q11)', ', '.join(B_blocks), 'S06!A3:K30; S06!A34:R68; S06!A71:F105', 'Sum of survivors / animals')
    reg(f'survB_{key}_ci', (s,n), ci(s,n), f'Exact 95% CI, conservative set, {g}', ', '.join(B_blocks), '', 'Clopper-Pearson')
s, n = pool([(b,'PSLN-212(Y)') for b in A_blocks if b!='S03-J'])
reg('survA_young', (s,n), pct(s,n), 'Pooled survival, young mice given vaccine + PSLN-212, the eight of nine experiments that include this arm', 'S03-I, S06-A..G', '', 'Sum')
pooled = pd.read_csv('stats_survival_pooled.csv')
def prow(prefix): return pooled[pooled['set'].str.startswith(prefix)].iloc[0]
rA, rB, rE, rF = prow('A:'), prow('B:'), prow('E:'), prow('F:')
reg('survF_344', rF.surv_344, f"{rF.surv_344} ({rF.pct_344:.0f}%)", 'Worst case for PSLN-344: conservative set, with body-weight-inferred survivor counts wherever they are less favourable to PSLN-344 or more favourable to PSLN-212', 'S06-A,B,D,E,F,G + S15-A..G', 'see qc_tte_vs_bodyweight', 'Counts replaced: S06-D PSLN-344 7->5; S06-E PSLN-212 0->1')
reg('survF_212', rF.surv_212, f"{rF.surv_212} ({rF.pct_212:.0f}%)", 'Worst case, PSLN-212', 'as above', '', 'as above')
reg('rd_A', rA.MH_risk_diff, f"{rA.MH_risk_diff:.0f}", 'Mantel-Haenszel survival difference (percentage points), PSLN-344 minus PSLN-212, set A', ', '.join(A_blocks), cellsA, 'Mantel-Haenszel risk difference stratified by experiment')
reg('p_slr_A', rA.p_strat_logrank, f"p = {rA.p_strat_logrank:.0e}".replace('e-','×10⁻').replace('⁻18','⁻¹⁸'), 'Stratified log-rank test, PSLN-344 vs PSLN-212, set A (chi-square %.1f, 1 df)' % rA.strat_logrank_chi2, ', '.join(A_blocks), cellsA, 'Log-rank stratified by experiment; verified against R survival::survdiff')
reg('p_slr_B', rB.p_strat_logrank, f"p = {rB.p_strat_logrank:.0e}", 'Stratified log-rank, conservative set B (chi-square %.1f)' % rB.strat_logrank_chi2, ', '.join(B_blocks), '', 'as above')
# Cox HR from R (written by check_lr.R to cox_hr.csv)
_cox = pd.read_csv('cox_hr.csv').set_index('set')
for _s, _blocks, _cells in [('A', A_blocks, cellsA), ('B', B_blocks, '')]:
    _r = _cox.loc[_s]
    assert abs(_r.strat_logrank_chisq - (rA if _s=='A' else rB).strat_logrank_chi2) < 0.01, 'R and Python stratified log-rank disagree'
    reg(f'hr_{_s}', (float(_r.hr), float(_r.hr_lo), float(_r.hr_hi)), f'{_r.hr:.2f} (95% CI {_r.hr_lo:.2f}–{_r.hr_hi:.2f})',
        f'Hazard ratio for death, PSLN-344 vs PSLN-212, Cox model stratified by experiment, set {_s}', ', '.join(_blocks), _cells, 'R survival::coxph with strata(block); script check_lr.R; stratified log-rank chi-square identical in R and Python')
# heterosubtypic only
het = ['S06-A','S06-B','S06-C','S06-D','S06-E','S06-F','S06-G']
s,n = pool([(b,'PSLN-344') for b in het]); reg('het_344', (s,n), pct(s,n), 'Aged BALB/c, challenge virus of a different subtype from the vaccine (as printed), PSLN-344', ', '.join(het), 'S06!A3:Q30; S06!A34:R68; S06!A71:F105', 'Sum')
s,n = pool([(b,'PSLN-212') for b in het]); reg('het_212', (s,n), pct(s,n), 'Same, PSLN-212', ', '.join(het), '', 'Sum')
# timing
early = [('S03-J','PSLN-344'),('S06-B','PSLN-344'),('S06-D','PSLN-344'),('S15-H','3d Vaccine+PSLN-344')]
d14 = [('S03-I','PSLN-344'),('S06-A','PSLN-344'),('S06-C','PSLN-344')]
d60 = [('S06-E','PSLN-344'),('S06-F','PSLN-344'),('S06-G','PSLN-344')]
unt = [('S06-E','Untreated'),('S06-F','Untreated'),('S06-G','Untreated')]
s_e,n_e = pool(early); reg('early_344', (s_e,n_e), pct(s_e,n_e), 'PSLN-344 + vaccine, aged BALB/c, challenged 2-3 days after the single dose', 'S03-J, S06-B, S06-D, S15-H', 'S03!J37:J46; S06!J17:J23; S06!D48:D54; S15!D87:D93', 'Sum')
s_14,n_14 = pool(d14); reg('d14_344', (s_14,n_14), pct(s_14,n_14), 'PSLN-344, aged BALB/c, challenged at day 14', 'S03-I, S06-A, S06-C', 'S03!E38:E44; S06!D17:D23; S06!P17:P23', 'Sum')
s_60,n_60 = pool(d60); reg('d60_344', (s_60,n_60), pct(s_60,n_60), 'PSLN-344, aged BALB/c, challenged at day 60', 'S06-E, S06-F, S06-G', 'S06!J48:J54; S06!P48:P54; S06!D85:D91', 'Sum')
s_u,n_u = pool(unt); reg('unt', (s_u,n_u), pct(s_u,n_u), 'Unvaccinated, unchallenged aged controls alive at day 14 of the day-60 cohorts', 'S06-E, S06-F, S06-G (Untreated)', 'S06!L62:L68; S06!R62:R68; S06!F99:F105', 'Sum')
reg('unt_deaths', (n_u-s_u, n_u), f'{n_u-s_u}/{n_u}', 'Deaths among unvaccinated, unchallenged aged controls', 'S06-E/F/G Untreated', '', 'Sum')
s_y60,n_y60 = pool([(b,'PSLN-212(Y)') for b in ['S06-E','S06-F','S06-G']]); reg('d60_young', (s_y60,n_y60), pct(s_y60,n_y60), 'Young benchmark, day-60 challenge', 'S06-E/F/G', '', 'Sum')
p = stats.fisher_exact([[s_14,n_14-s_14],[s_60,n_60-s_60]])[1]; reg('p_d14_d60', p, f'p = {p:.3f}', 'Fisher exact test, PSLN-344 survival day-14 vs day-60 challenge', 'S03-I, S06-A, S06-C vs S06-E..G', '', 'Fisher exact, two-sided')
p = stats.fisher_exact([[s_60,n_60-s_60],[s_u,n_u-s_u]])[1]; reg('p_d60_unt', p, f'p = {p:.2f}', 'Fisher exact test, PSLN-344 day-60 survival vs unchallenged untreated controls', 'S06-E..G', '', 'Fisher exact, two-sided')
s,n = pool([(b,'PSLN-212') for b in ['S06-E','S06-F','S06-G']]); reg('d60_212', (s,n), pct(s,n), 'PSLN-212 aged, day-60 challenge', 'S06-E/F/G', '', 'Sum')
# S15-H
for g,k in [('3d Vaccine','h_vac'),('3d PSLN-344','h_adj'),('3d Vaccine+PSLN-344','h_both')]:
    s,n = sv('S15-H', g); reg(k, (s,n), f'{s}/{n}', f'Survival, aged BALB/c, "{g}", rgH5N1 challenge 3 days later', 'S15-H', cells_of('S15-H', g), 'Count')
# young
for g,k in [('PSLN-344Y','y344'),('PSLN-212Y','y212'),('Sham','ysham')]:
    s,n = pool([(b,g) for b in ['S09-B','S09-D','S09-F']]); reg(k, (s,n), f'{s}/{n}', f'Young BALB/c, pooled survival, {g}, three challenge experiments (day 21, 21, 180)', 'S09-B, S09-D, S09-F', 'S09!A12:D35; S09!A39:D62; S09!A66:D88', 'Sum')
for g,k in [('PSLN-344(Y)','e344'),('CMP-204(Y)','ecmp'),('Sham','esham'),('Naïve','enaive')]:
    s,n = sv('S13-E', g); reg('s13e_'+k, (s,n), f'{s}/{n}', f'Young BALB/c, matched H1N1 challenge, {g}', 'S13-E', cells_of('S13-E', g), 'Count')
# strains, 14 months
for b,k in [('S15-L','b6'),('S15-N','sw')]:
    for g,kk in [('PSLN-344','344'),('PSLN-212','212'),('Sham','sham'),('PSLN-212(Y)','young')]:
        s,n = sv(b,g); reg(f'{k}_{kk}', (s,n), f'{s}/{n}', f'{b} survival, {g}', b, cells_of(b,g), 'Count')
s344 = sum(sv(b,p+'PSLN-344')[0] for b in ['S06-E2','S06-F2'] for p in ['Naïve+','Imprinting+']); s212 = sum(sv(b,p+'PSLN-212')[0] for b in ['S06-E2','S06-F2'] for p in ['Naïve+','Imprinting+'])
reg('m14_344', (s344,28), pct(s344,28), '14-month-old BALB/c (with or without prior PR8 infection), PSLN-344, four groups pooled', 'S06-E2, S06-F2 (second blocks labelled S06-E / S06-F)', 'S06!J85:K98; S06!P85:Q98', 'Sum')
reg('m14_212', (s212,28), pct(s212,28), 'Same, PSLN-212', 'S06-E2, S06-F2', 'S06!H71:I84; S06!N71:O84', 'Sum')
for b,p,k in [('S06-E2','Imprinting+','imp_pr8'),('S06-F2','Imprinting+','imp_perth'),('S06-E2','Naïve+','nai_pr8'),('S06-F2','Naïve+','nai_perth')]:
    for g in ['PSLN-344','PSLN-212']:
        s,n = sv(b,p+g); reg(f'{k}_{g[-3:]}', (s,n), f'{s}/{n}', f'{b} {p}{g}', b, cells_of(b,p+g), 'Count')
# individual blocks cited
for b in A_blocks:
    for g,k in [('PSLN-344','344'),('PSLN-212','212'),('Sham','sham')]:
        s,n = sv(b,g); reg(f'{b}_{k}', (s,n), f'{s}/{n}', f'{b} survival, {g}', b, cells_of(b,g), 'Count')
s,n = sv('S03-I','CMP-204'); reg('S03-I_cmp', (s,n), f'{s}/{n}', 'S03-I survival, CMP-204 (cGAMP liposome), aged', 'S03-I', cells_of('S03-I','CMP-204'), 'Count')

# power
def fisher_power(p1, p2, n, alpha=0.05):
    pw = 0.0
    for a in range(n+1):
        pa = stats.binom.pmf(a, n, p1)
        for b in range(n+1):
            pb = stats.binom.pmf(b, n, p2)
            if pa*pb < 1e-14: continue
            if stats.fisher_exact([[a, n-a],[b, n-b]])[1] <= alpha: pw += pa*pb
    return pw
def n_for(p1,p2,target=0.9):
    for n in range(4,90):
        if fisher_power(p1,p2,n) >= target: return n
reg('power_n7', fisher_power(0.85,0.14,7), f'{100*fisher_power(0.85,0.14,7):.0f}%', 'Power of a single n=7 per arm experiment to detect 85% vs 14% survival (Fisher exact, two-sided 5%)', 'design calculation', '', 'Exact enumeration of binomial outcomes')
reg('n_worst', n_for(0.71,0.12), f'{n_for(0.71,0.12)}', 'Animals per arm for 90% power, 71% vs 12% survival (worst-case estimates)', 'design calculation', '', 'Exact Fisher power')
reg('n_soc', n_for(0.80,0.40), f'{n_for(0.80,0.40)}', 'Animals per arm for 90% power, 80% vs 40% survival (assumed benchmark effect)', 'design calculation', '', 'Exact Fisher power')

# ---------------------------------------------------------------- immunology contrasts
def C(block, ref, test, analyte=None): return contrast(block, ref, test, analyte)
def fmt(x, nd=1): return f'{x:,.{nd}f}'
def reg_pair(key, block, desc, nd=1, geometric=False, unit='', ref='PSLN-212', test='PSLN-344', young='PSLN-212(Y)', sham='Sham'):
    c = C(block, ref, test)
    a = c['gm_test'] if geometric else c['mean_test']; o = c['gm_ref'] if geometric else c['mean_ref']
    how = 'geometric mean' if geometric else 'mean'
    reg(key+'_344', a, fmt(a,nd)+unit, f'{desc}: {test}, {how} (n={c["n_test"]})', block, c['cells_test'], how)
    reg(key+'_212', o, fmt(o,nd)+unit, f'{desc}: {ref}, {how} (n={c["n_ref"]})', block, c['cells_ref'], how)
    fold = c['fold']
    reg(key+'_fold', fold, f'{fold:.1f}×' if fold<100 else f'{fold:.0f}×', f'{desc}: ratio {test}/{ref} ({"ratio of geometric means" if c["scale"].startswith("log") else "ratio of means"}); Welch p={c["p_welch"]:.2g}; Tukey p={c["p_tukey"]:.2g}', block, c['cells_ref']+'; '+c['cells_test'], 'Welch t-test (log10 scale for titres/fold values); one-way ANOVA + Tukey across all groups of the block')
    if c['scale'].startswith('log') and not np.isnan(c['fold_lo']):
        reg(key+'_foldci', (c['fold_lo'],c['fold_hi']), f'{c["fold_lo"]:.1f}–{c["fold_hi"]:.1f}', f'{desc}: 95% CI of the ratio', block, '', 'Welch interval on log10 scale')
    d = get(block)
    if young in d.group.unique():
        cy = C(block, young, test); y = cy['gm_ref'] if geometric else cy['mean_ref']
        reg(key+'_young', y, fmt(y,nd)+unit, f'{desc}: young benchmark ({young}), {how}', block, cy['cells_ref'], how)
        reg(key+'_pctyoung', 100*a/y, f'{100*a/y:.0f}%', f'{desc}: {test} as % of young benchmark; Welch p vs young = {cy["p_welch"]:.2g}', block, '', 'ratio')
    if sham in d.group.unique():
        cs = C(block, sham, test); s_ = cs['gm_ref'] if geometric else cs['mean_ref']
        reg(key+'_sham', s_, fmt(s_,nd)+unit, f'{desc}: {sham}, {how}', block, cs['cells_ref'], how)
    return c

reg_pair('ifn16', 'S01-A_16h', 'Lung Ifnb1 mRNA 16 h after dosing, fold over untreated', 1)
c = C('S01-A_16h','Sham','CMP-204'); reg('ifn16_cmp', c['mean_test'], fmt(c['mean_test'],1), 'Lung Ifnb1 16 h, CMP-204 (cGAMP liposome), aged, mean', 'S01-A', c['cells_test'], 'mean')
c = C('S01-A_16h','PSLN-212(Y)','PSLN-344(Y)'); reg('ifn16_y344', c['mean_test'], fmt(c['mean_test'],1), 'Lung Ifnb1 16 h, PSLN-344 in young mice, mean', 'S01-A', c['cells_test'], 'mean')
reg('ifn16_yfold', c['fold'], f'{c["fold"]:.1f}×', f'Ifnb1 16 h, young mice: PSLN-344/PSLN-212 ratio of geometric means; Welch p={c["p_welch"]:.2g}, Tukey p={c["p_tukey"]:.2g}', 'S01-A', c['cells_ref']+'; '+c['cells_test'], 'Welch t-test on log10; Tukey')
for g,k in [('PSLN-212/R848','r848'),('PSLN-R848','r848only')]:
    c = C('S01-A_16h','Sham',g); reg('ifn16_'+k, c['mean_test'], fmt(c['mean_test'],1), f'Lung Ifnb1 16 h, {g}, aged', 'S01-A', c['cells_test'], 'mean')
    c = C('S01-A_72h','Sham',g); reg('ifn72_'+k, c['mean_test'], fmt(c['mean_test'],1), f'Lung Ifnb1 72 h, {g}, aged', 'S01-A', c['cells_test'], 'mean')
reg_pair('ifn72', 'S01-A_72h', 'Lung Ifnb1 mRNA 72 h after dosing, fold', 1)
# dose response
dr = pd.read_csv('dose_response_S08A.csv').set_index('group')
for g,k in [('PSLN-344','344'),('PSLN-212','212'),('CMP-204','cmp')]:
    reg(f'emax_{k}', dr.loc[g,'Emax_fold'], f'{dr.loc[g,"Emax_fold"]:.0f}×', f'Fitted plateau (Emax) of Ifnb1 induction, {g} (SE {dr.loc[g,"Emax_se"]:.1f})', 'S08-A', cells_of('S08-A', g), 'Three-parameter Hill fit, fold = 1 + Emax*D^h/(ED50^h + D^h), least squares on individual values (n=3 x 5 doses)')
    reg(f'ed50_{k}', dr.loc[g,'ED50_ug'], f'{dr.loc[g,"ED50_ug"]:.0f} µg', f'Fitted ED50, {g} (SE {dr.loc[g,"ED50_se"]:.1f})', 'S08-A', cells_of('S08-A', g), 'Hill fit')
reg('d20_40', dr.loc['PSLN-344','ratio_20_over_40'], f'{100*dr.loc["PSLN-344","ratio_20_over_40"]:.0f}%', 'PSLN-344: mean Ifnb1 at 20 µg as % of 40 µg', 'S08-A', 'S08!H6:J7', 'ratio of means')
for dose in (10,20,40):
    for g,k in [('PSLN-344','344'),('PSLN-212','212')]:
        v = T['S08-A']; v = v[(v.group==g)&(v.dose_ug==dose)]['value'].mean(); reg(f'dr_{k}_{dose}', v, f'{v:.1f}', f'Ifnb1 fold at {dose} µg, {g}, mean of 3', 'S08-A', cells_of('S08-A', g, day=dose), 'mean')
g = T['S08-A']; v = g[(g.group=='PSLN-344/R848')&(g.dose_ug==20)]['value'].mean(); reg('dr_344r848_20', v, f'{v:.1f}', 'Ifnb1 fold at 20 µg, PSLN-344/R848', 'S08-A', cells_of('S08-A','PSLN-344/R848',day=20), 'mean')
# GM-CSF
d = T['S02-F']
for t in ['16h','36h','72h']:
    for g,k in [('PSLN-344','344'),('PSLN-212','212'),('Sham','sham')]:
        v = d[(d.group==g)&(d.time==t)]['value']; reg(f'gm_{k}_{t}', v.mean(), f'{v.mean():.1f}', f'Lung Gm-csf mRNA fold, {t}, {g}, mean (n={len(v)})', 'S02-F', cells_of('S02-F', g, day=t), 'mean')
tc = pd.read_csv('stats_timecourse_pairwise.csv')
def tcp(block, time, g1, g2):
    r = tc[(tc.block==block)&(tc.time.astype(str)==str(time))&(((tc.g1==g1)&(tc.g2==g2))|((tc.g1==g2)&(tc.g2==g1)))].iloc[0]; return r
r = tcp('S02-F','36h','PSLN-344','PSLN-212'); reg('gm_p36', r.p_welch, f'p = {r.p_welch:.0e}', 'Gm-csf 36 h, PSLN-344 vs PSLN-212, Welch t-test on log10 (two-way ANOVA Tukey p = %.1e)' % r.p_tukey_allcells, 'S02-F', '', 'Welch; two-way ANOVA + Tukey')
# Ccl2 and cytokines (S09-A)
for side, tlab in [('S09-A_left','16h'),('S09-A_right','72h')]:
    for an in ['Ifnb1','Il6','Tnf','Ccl2','Ccl3','Ccl5','Il10']:
        for g,k in [('PSLN-344','344'),('PSLN-212','212'),('PSLN-212(y)','young'),('PSLN-212/R848','r848')]:
            c = C(side, 'PBS', g, analyte=an)
            f = 10**c['diff']; lo, hi = 10**c['diff_lo'], 10**c['diff_hi']
            reg(f'cyt_{an}_{k}_{tlab}', f, (f'{f:,.0f}×' if f>=10 else f'{f:.1f}×'), f'Lung {an} mRNA, {tlab} panel of S09-A ({"right panel, printed 16h, identified as 72 h, flag Q02" if tlab=="72h" else "left panel"}), {g}: geometric-mean fold over control (95% CI {lo:.1f}-{hi:.1f}; n=3)', 'S09-A', c['cells_test'], '10^(mean log10 difference vs control); Welch CI')
# cells
d = T['S01-D']
for g,k in [('PSLN-344','344'),('PSLN-212','212'),('Sham','sham'),('PSLN-212(Y)','young')]:
    v = d[(d.group==g)&(d.day=='4')]['value']; reg(f'mono4_{k}', v.mean(), f'{v.mean():.1f}%', f'Lung monocytes day 4, {g}, mean (n=5)', 'S01-D', cells_of('S01-D', g, day='4'), 'mean')
    v = d[(d.group==g)&(d.day=='8')]['value']; reg(f'mono8_{k}', v.mean(), f'{v.mean():.1f}%', f'Lung monocytes day 8, {g}, mean (n=5)', 'S01-D', cells_of('S01-D', g, day='8'), 'mean')
d = T['S01-E']
for g,k in [('PSLN-344','344'),('PSLN-212','212'),('Sham','sham'),('PSLN-212(Y)','young'),('PSLN-344(Y)','y344')]:
    v = d[(d.group==g)&(d.day=='4')]['value']; reg(f'dc4_{k}', v.mean(), f'{v.mean():.1f}%', f'Lung CD11b+ dendritic cells day 4, {g}, mean (n=5)', 'S01-E', cells_of('S01-E', g, day='4'), 'mean')
d = T['S07-A']
for g,k in [('PSLN-344','344'),('PSLN-212','212')]:
    for day in (5,10):
        v = d[(d.group==g)&(d.day==day)]['value']; reg(f'mac{day}_{k}', v.mean(), f'{v.mean():.1f}', f'Lung Ly6C+CCR2+ macrophages, day {day}, {g}, x10^5 cells, mean (n=3)', 'S07-A', cells_of('S07-A', g, day=day), 'mean')
def reg_two(key, block, g_ref, g_test, desc, nd=1, unit='%'):
    c = C(block, g_ref, g_test)
    reg(key+'_a', c['mean_ref'], fmt(c['mean_ref'],nd)+unit, f'{desc}: {g_ref}, mean (n={c["n_ref"]})', block, c['cells_ref'], 'mean')
    reg(key+'_b', c['mean_test'], fmt(c['mean_test'],nd)+unit, f'{desc}: {g_test}, mean (n={c["n_test"]}); Welch p={c["p_welch"]:.2g}', block, c['cells_test'], 'mean; Welch t-test')
    return c
reg_two('spad', 'S01-C', 'WT', 'SPA/D', 'Dye-positive alveolar macrophages 16 h after DiD-liposome')
reg_two('srb2', 'S01-B', 'AECII/FreeSRB', 'AECII/PSLN-SRB', 'Dye-positive type II alveolar epithelial cells')
reg_two('srb1', 'S01-B', 'AECI/FreeSRB', 'AECI/PSLN-SRB', 'Dye-positive type I alveolar epithelial cells')
reg_two('cbx', 'S11-C', 'CBX-', 'CBX+', 'Recruited lung monocytes day 3, PSLN-344, without / with carbenoxolone')
reg_two('gmres', 'S02-G', 'PSLN-212', 'PSLN-212+GM-CSF', 'Lung Ly6C+CD11c+MHC-II+ cells day 5')
c = C('S02-G','PSLN-212','GM-CSF'); reg('gmres_alone', c['mean_test'], fmt(c['mean_test'],1)+'%', 'Same read-out, GM-CSF without adjuvant', 'S02-G', c['cells_test'], 'mean')
reg_two('ifnar', 'S02-H', 'WT w/o cDC', 'IFN w/o cDC', 'Donor-derived monocyte-derived DC day 3, PSLN-344: wild-type vs Ifnar-knockout marrow (pre-cDC removed)')
c = C('S02-H','WT w/o cDC','GMCSF'); reg('ifnar_gm', c['mean_test'], fmt(c['mean_test'],1)+'%', 'Same, Ifnar-knockout marrow + GM-CSF intratracheally', 'S02-H', c['cells_test'], 'mean')
reg_two('ccr2mono', 'S07-B_mono', 'PSLN-344', 'PSLN-344+INCB3344', 'Lung CD11b+Ly6C+ monocytes, PSLN-344 without / with CCR2 antagonist')
reg_two('ccr2mac', 'S07-B_Ly6CMac', 'PSLN-344', 'PSLN-344+INCB3344', 'Lung Ly6C+ macrophages, PSLN-344 without / with CCR2 antagonist')
reg_two('ccr2gzmb', 'S02-I', 'PSLN-344(Y)', 'PSLN-344(Y)+INCB3344', 'Lung granzyme B+ CD8 T cells day 5, young mice, PSLN-344 without / with CCR2 antagonist')
reg_two('s12', 'S12-A', 'WT to WT', 'IFNAR-/- to WT', 'Infiltrating donor monocytes day 3, young mice')
reg_two('ptx_lung', 'S05-C', 'Lung', 'Lung+PTX', 'Proliferating OT-I CD8 T cells in lung day 4, without / with pertussis toxin')
reg_two('ptx_mln', 'S05-C', 'MLN', 'MLN+PTX', 'Proliferating OT-I CD8 T cells in lymph node day 4, without / with pertussis toxin')
c = C('S02-C','PSLN-344','PTX'); reg('ptx_dc', c['mean_test'], fmt(c['mean_test'],1)+'%', 'Antigen-positive DC in lymph node, pertussis-toxin group', 'S02-C', c['cells_test'], 'mean')
reg_pair('migdc', 'S02-A', 'CCR7+ migratory CD11b+ DC in lung, 72 h', 1, unit='%')
reg_pair('agdc', 'S02-C', 'Antigen (OVA-AF647)-positive DC in lymph node, 36 h', 1, unit='%')
reg_pair('cd40', 'S02-D_CD40', 'CD40+ lymph-node CD11b+ DC, day 3', 1, unit='%')
reg_pair('cd86', 'S02-D_CD86', 'CD86+ lymph-node CD11b+ DC, day 3', 1, unit='%')
reg_pair('prime', 'S02-E', 'OT-I CD8 proliferation driven by lymph-node DC ex vivo', 1, unit='%')
reg_pair('gcb', 'S03-K', 'Germinal-centre B cells in lymph node, day 7', 1, unit='%')
reg_pair('tfhhi', 'S04-A_ICOShi', 'ICOS-high follicular helper T cells, day 7', 1, unit='%')
reg_pair('tfr', 'S04-B_Tfr', 'Follicular regulatory T cells (Foxp3+ in CXCR5+), day 7', 1, unit='%')
reg_pair('tfhtfr', 'S04-B_TfhTfr', 'Tfh:Tfr ratio, day 7', 1)
c = C('S04-B_TfhTfr','PSLN-212','PSLN-344'); reg('tfhtfr_344m', c['mean_test'], f'{c["mean_test"]:.1f}', 'Tfh:Tfr ratio day 7, PSLN-344, arithmetic mean', 'S04-B Tfh:Tfr', c['cells_test'], 'mean'); reg('tfhtfr_212m', c['mean_ref'], f'{c["mean_ref"]:.1f}', 'Tfh:Tfr ratio day 7, PSLN-212, arithmetic mean', 'S04-B Tfh:Tfr', c['cells_ref'], 'mean')
reg_pair('tfr30', 'S04-C', 'Follicular regulatory T cells, day 30', 1, unit='%')
reg_pair('treg', 'S04-D', 'Lung regulatory T cells, day 7 (n=3)', 1, unit='%')
reg_pair('cd206', 'S11-E', 'CD206+ lung macrophages', 0, unit='%')
reg_pair('igg_h1', 'S03-A', 'Serum IgG to H1N1, day 14, reciprocal titre', 0, geometric=True)
reg_pair('igg_h3', 'S03-E', 'Serum IgG to H3N2, day 14, reciprocal titre', 0, geometric=True)
reg_pair('hai_h1', 'S03-C', 'HAI titre to H1N1, day 14', 0, geometric=True)
reg_pair('hai_h3', 'S03-G', 'HAI titre to H3N2, day 14', 0, geometric=True)
reg_pair('mn_h1', 'S03-D', 'Neutralising titre to H1N1, day 14', 0, geometric=True)
reg_pair('mn_h3', 'S03-H', 'Neutralising titre to H3N2, day 14', 0, geometric=True)
reg_pair('igg2a_h1', 'S13-A', 'IgG2a to H1N1, day 14', 0, geometric=True)
reg_pair('igg1_h1', 'S13-B', 'IgG1 to H1N1, day 14', 0, geometric=True)
reg_pair('boost_h1', 'S13-I', 'IgG to H1N1, day 28 after boost at day 14', 0, geometric=True)
reg_pair('boost_h3', 'S13-J', 'IgG to H3N2, day 28 after boost at day 14', 0, geometric=True)
reg_pair('ki67', 'S05-D', 'Ki-67+ lung CD8 T cells, day 3', 1, unit='%')
reg_pair('gzmb', 'S05-E', 'Granzyme B+ lung CD8 T cells, day 3', 1, unit='%')
reg_pair('ifng14', 'S05-F', 'IFN-gamma+ CD8 T cells after restimulation with rgH5N1 antigen, day 14', 1, unit='%')
reg_pair('ifng60', 'S05-G', 'IFN-gamma+ CD8 T cells after restimulation with rgH5N1 antigen, day 60', 1, unit='%')
reg_pair('gzmb60', 'S05-H', 'Granzyme B+ CD8 T cells, lymph node day 60', 1, unit='%')
reg_pair('trm', 'S05-I', 'Lung resident-memory CD8 T cells (CD69+CD103+), day 25', 1, unit='%')
reg_pair('ifng_h1', 'S14-A_H1N1', 'IFN-gamma+ CD8 T cells after restimulation with H1N1 antigen', 1, unit='%')
reg_pair('ifng_h3', 'S14-A_H3N2', 'IFN-gamma+ CD8 T cells after restimulation with H3N2 antigen', 1, unit='%')
reg_pair('aicda', 'S03-L_Aicda', 'Aicda mRNA in lymph-node B cells, day 5 (n=3)', 1, geometric=False)
# HAI seroprotection counts
for blk,k in [('S03-C','h1'),('S03-G','h3')]:
    d = B[blk]
    for g,kk in [('PSLN-344','344'),('PSLN-212','212'),('CMP-204','cmp'),('Sham','sham')]:
        v = d[d.group==g]['value']; reg(f'hai40_{k}_{kk}', int((v>=40).sum()), f'{int((v>=40).sum())}/{len(v)}', f'Animals with HAI titre >= 40, {g}', blk, cells_of(blk,g), 'Count')
    c = C(blk,'Sham','CMP-204'); reg(f'hai_{k}_cmp', c['gm_test'], f'{c["gm_test"]:.0f}', f'HAI geometric mean titre, CMP-204', blk, c['cells_test'], 'geometric mean')
# IgG2a/IgG1 recomputed
for num,den,k,lab in [('S13-A','S13-B','h1','H1N1'),('S13-C','S13-D','h3','H3N2')]:
    for g,kk in [('PSLN-344','344'),('PSLN-212','212'),('PSLN-212(Y)','young')]:
        r = B[num][B[num].group==g]['value'].values / B[den][B[den].group==g]['value'].values
        reg(f'ratio_{k}_{kk}', r.mean(), f'{r.mean():.2f}', f'IgG2a/IgG1 quotient to {lab}, {g}, mean of per-animal quotients recomputed from subclass titres (not from the mislabelled quotient block; flag Q01)', f'{num}, {den}', cells_of(num,g)+' / '+cells_of(den,g), 'per-animal quotient, mean')
    a = B[num][B[num].group=='PSLN-344']['value'].values / B[den][B[den].group=='PSLN-344']['value'].values
    b = B[num][B[num].group=='PSLN-212']['value'].values / B[den][B[den].group=='PSLN-212']['value'].values
    p = stats.ttest_ind(np.log10(a), np.log10(b), equal_var=False).pvalue
    reg(f'ratio_{k}_p', p, f'p = {p:.3f}', f'IgG2a/IgG1 to {lab}, PSLN-344 vs PSLN-212, Welch t-test on log10 of recomputed quotients', f'{num}, {den}', '', 'Welch')
for k, blk in [('h1','S03-B'),('h3','S03-F')]:
    v = B[blk][B[blk].group=='PSLN-344']['value'].mean(); reg(f'ratio_{k}_printed344', v, f'{v:.2f}', f'IgG2a/IgG1 quotient as printed under the header "PSLN-344" in {blk} (header rotated, flag Q01)', blk, cells_of(blk,'PSLN-344'), 'mean')

# restoration summary
ri = pd.read_csv('restoration_index.csv')
reg('ri_n', len(ri), f'{len(ri)}', 'Number of single-time-point immunology read-outs that include PSLN-212 aged, PSLN-344 aged and the young benchmark', '; '.join(ri.block), '', 'see restoration_index.csv')
reg('ri_closer', int(ri.closer_to_young.sum()), f'{int(ri.closer_to_young.sum())}', 'Read-outs in which PSLN-344 is closer to the young benchmark than PSLN-212 (on the ratio scale)', 'as above', '', '|log(aged/young)| comparison')
reg('ri_sig', int((ri.p_welch_344_vs_212<0.05).sum()), f'{int((ri.p_welch_344_vs_212<0.05).sum())}', 'Read-outs with Welch p<0.05 for PSLN-344 vs PSLN-212', 'as above', '', 'Welch t-test per read-out (log10 for titres/fold values); not adjusted across read-outs')
reg('ri_med344', ri.pct_of_young_344.median(), f'{ri.pct_of_young_344.median():.0f}%', 'Median across read-outs of PSLN-344 (aged) as % of young benchmark', 'as above', '', 'median of ratios')
reg('ri_med212', ri.pct_of_young_212.median(), f'{ri.pct_of_young_212.median():.0f}%', 'Median across read-outs of PSLN-212 (aged) as % of young benchmark', 'as above', '', 'median of ratios')
reg('ri_ns_young', int((ri.p_welch_344_vs_young>=0.05).sum()), f'{int((ri.p_welch_344_vs_young>=0.05).sum())}', 'Read-outs in which PSLN-344 (aged) does not differ from the young benchmark at Welch p<0.05 (n=5 per group; low power)', 'as above', '', 'Welch')

# ---------------------------------------------------------------- safety
nad = pd.read_csv('safety_S08D_nadir.csv')
for g,k in [('PSLN-344','344'),('PSLN-212','212'),('Vaccine','vac'),('PSLN-212/R848','r848'),('CMP-204','cmp')]:
    x = nad[nad.group==g]['max_loss_pct']
    reg(f'wl_{k}', x.mean(), f'{x.mean():.1f}%', f'Mean of per-animal maximum weight loss over 10 days after immunisation, {g} (n=5)', 'S08-D', cells_of('S08-D', g), 'per-animal minimum of % day-0 weight, days 2-10')
    reg(f'wl_{k}_worst', x.max(), f'{x.max():.1f}%', f'Largest individual weight loss after immunisation, {g}', 'S08-D', cells_of('S08-D', g), 'max')
d = W['S08-D']
for g,k in [('PSLN-344','344'),('PSLN-212/R848','r848'),('Vaccine','vac')]:
    v = d[(d.group==g)&(d.day==10)]['value']; reg(f'wd10_{k}', v.mean(), f'{v.mean():.1f}%', f'Mean weight at day 10 after immunisation, {g} (n={len(v)})', 'S08-D', cells_of('S08-D', g, day=10), 'mean')
a = nad[nad.group=='PSLN-344']['max_loss_pct']; b = nad[nad.group=='Vaccine']['max_loss_pct']; p = stats.ttest_ind(a,b,equal_var=False).pvalue
reg('wl_p', p, f'p = {p:.2f}', 'Maximum weight loss after immunisation, PSLN-344 vs vaccine alone, Welch t-test (Tukey p = 0.86)', 'S08-D', '', 'Welch')
for an in ['Ifnb1','Tnf','Isg15']:
    c = C(f'S10-A_{an}','PBS','PSLN-344'); reg(f'cns_{an}_344', c['fold'], f'{c["fold"]:.1f}×', f'CNS {an} mRNA 36 h after dosing, PSLN-344 vs buffer: ratio of geometric means (95% CI {c["fold_lo"]:.2f}-{c["fold_hi"]:.2f}); Tukey p={c["p_tukey"]:.2f}; Welch p={c["p_welch"]:.2f}', 'S10-A', c['cells_ref']+'; '+c['cells_test'], 'Welch on log10; ANOVA + Tukey')
    reg(f'cns_{an}_344ci', (c['fold_lo'],c['fold_hi']), f'{c["fold_lo"]:.1f}–{c["fold_hi"]:.1f}', f'95% CI of the above', 'S10-A', '', 'Welch')
    c = C(f'S10-A_{an}','PBS','CT'); reg(f'cns_{an}_ct', c['fold'], f'{c["fold"]:.1f}×', f'CNS {an}, cholera toxin vs buffer: ratio of geometric means', 'S10-A', c['cells_test'], 'as above')
bwc = pd.read_csv('bw_challenge_nadir.csv')
x = bwc[(bwc.group=='PSLN-344')&(bwc.block.isin(['S15-A','S15-B','S15-D','S15-E','S15-F','S15-G']))]['mean_max_loss']
reg('morb_344', (x.min(), x.max()), f'{x.min():.0f}–{x.max():.0f}%', 'Range across six mismatched-virus experiments of the group mean of maximum weight loss after challenge, PSLN-344 aged (all 7 animals per group; S15-C excluded, flag Q05)', 'S15-A, B, D, E, F, G', 'S15!W3:AC70', 'per-animal minimum weight, group mean')
x = bwc[(bwc.group=='PSLN-212(Y)')&(bwc.block.isin(['S15-A','S15-B','S15-D','S15-E','S15-F','S15-G']))]['mean_max_loss']
reg('morb_young', (x.min(), x.max()), f'{x.min():.0f}–{x.max():.0f}%', 'Same, young benchmark', 'S15-A, B, D, E, F, G', 'S15!B3:H70', 'as above')
x = bwc[(bwc.group=='PSLN-212')&(bwc.block.isin(['S15-A','S15-B','S15-D','S15-E','S15-F','S15-G']))]['mean_max_loss']
reg('morb_212', (x.min(), x.max()), f'{x.min():.0f}–{x.max():.0f}%', 'Same, PSLN-212 aged', 'S15-A, B, D, E, F, G', 'S15!P3:V70', 'as above')
x = bwc[(bwc.group=='PSLN-344')&(bwc.block=='S13-F')]['mean_max_loss'].iloc[0]; reg('morb_344_hom', x, f'{x:.1f}%', 'Mean maximum weight loss after matched H1N1 challenge, PSLN-344 aged', 'S13-F', 'S13!W33:AC40', 'as above')
# CMC
for g,k in [('PSLN-344','344'),('PSLN-212','212'),('CMP-204','cmp')]:
    v = B['S08-B'][B['S08-B'].group==g]['value']; reg(f'ee_{k}', v.mean(), f'{v.mean():.1f}% (SD {v.std(ddof=1):.1f}, n=3)', f'Encapsulation efficiency, {g}', 'S08-B', cells_of('S08-B', g), 'mean, SD')
c = C('S08-B','PSLN-212','PSLN-344'); reg('ee_p', c['p_welch'], f'p = {c["p_welch"]:.2f}', 'Encapsulation efficiency, PSLN-344 vs PSLN-212, Welch t-test', 'S08-B', '', 'Welch')
# QC counts
q = pd.read_csv('qc_log.csv'); reg('qc_n', len(q), f'{len(q)}', 'Number of data-quality flags raised', 'all', '', 'see qc_log.csv / Appendix A'); reg('qc_high', int((q.Severity=='High').sum()), f'{int((q.Severity=="High").sum())}', 'Flags rated High', 'all', '', 'see qc_log.csv')
nn, coords = count_all_numeric_cells(); reg('cells_total', nn, f'{nn:,}', 'Numeric cells in the workbook', 'all 15 sheets', '', 'openpyxl count')


# ---------------------------------------------------------------- extra entries added for the text
def frozen_last(block, group):
    d = W[block]; d = d[d.group==group]; out=[]
    for rep, x in d.groupby('rep'):
        x = x.sort_values('day'); v = list(x['value']); days = list(x['day'])
        if days[-1] == 14 and len(v) >= 3 and v[-1] == v[-2] == v[-3] :
            out.append(v[-1])
        elif days[-1] == 14 and len(v) >= 2 and v[-1] == v[-2] and v[-1] < 90:
            out.append(v[-1])
    return out
fl = sum([frozen_last(b,'PSLN-344') for b in ['S15-E','S15-F','S15-G']], [])
reg('d60_deathwt_344', fl, f'{min(fl):.0f}–{max(fl):.0f}%', f'Last recorded body weight (frozen trace) of PSLN-344 animals that died after day-60 challenge, percent of day 0; n={len(fl)} animals', 'S15-E, S15-F, S15-G', 'S15!W43:AC70', 'weight value carried forward to day 14')
fu = sum([frozen_last(b,'Untreated') for b in ['S15-E','S15-F','S15-G']], [])
reg('unt_deathwt', fu, f'{min(fu):.0f}–{max(fu):.0f}%', f'Last recorded body weight (frozen trace) of unvaccinated, unchallenged aged controls that died; n={len(fu)} animals', 'S15-E, S15-G', 'S15!AD43:AJ70', 'weight value carried forward to day 14')
# number of head-to-head survival comparisons in which PSLN-344 is ahead
pairs = [(b,'PSLN-344','PSLN-212') for b in A_blocks+['S15-L','S15-N']] + [(b,p+'PSLN-344',p+'PSLN-212') for b in ['S06-E2','S06-F2'] for p in ['Naïve+','Imprinting+']]
ahead = sum(1 for b,g1,g2 in pairs if sv(b,g1)[0]/sv(b,g1)[1] > sv(b,g2)[0]/sv(b,g2)[1])
reg('h2h_ahead', (ahead, len(pairs)), f'{ahead} of {len(pairs)}', 'Head-to-head survival comparisons (aged BALB/c x9, aged C57BL/6, aged Swiss Webster, 14-month BALB/c x4) in which PSLN-344 has the higher survival fraction', 'S03-I/J, S06-A..G, S15-L, S15-N, S06-E2, S06-F2', '', 'count')
# survival difference CI for sets (Newcombe not needed; MH RD with Greenland-Robins variance)
def mh_rd(strata, override=None):
    num=den=var=0
    for blk, ga, gb in strata:
        a, n1 = sv(blk, ga); b, n0 = sv(blk, gb)
        if override: a = override.get((blk,ga), a); b = override.get((blk,gb), b)
        Nn = n1+n0; num += (a*n0 - b*n1)/Nn; den += n1*n0/Nn
        var += (a*(n1-a)*n0**3 + b*(n0-b)*n1**3)/(n1*n0*Nn**2)
    rd = num/den; se = np.sqrt(var)/den
    return rd, rd-1.96*se, rd+1.96*se
for key, st, ov in [('A', [(b,'PSLN-344','PSLN-212') for b in A_blocks], None), ('B', [(b,'PSLN-344','PSLN-212') for b in B_blocks], None),
                    ('F', [(b,'PSLN-344','PSLN-212') for b in B_blocks], {('S06-D','PSLN-344'):5, ('S06-E','PSLN-212'):1})]:
    rd, lo, hi = mh_rd(st, ov)
    reg(f'rdci_{key}', (rd,lo,hi), f'{100*rd:.0f} points (95% CI {100*lo:.0f}–{100*hi:.0f})', f'Mantel-Haenszel difference in survival, PSLN-344 minus PSLN-212, set {key}, stratified by experiment', 'see set definition', '', 'Mantel-Haenszel risk difference, Greenland-Robins variance')
# all strains/ages set C
rC = prow('C:')
reg('survC_344', rC.surv_344, f"{rC.surv_344} ({rC.pct_344:.0f}%)", 'All head-to-head experiments as printed (aged BALB/c x9, C57BL/6, Swiss Webster, 14-month x4), PSLN-344', 'S03-I/J, S06-A..G, S15-L/N, S06-E2/F2', '', 'Sum')
reg('survC_212', rC.surv_212, f"{rC.surv_212} ({rC.pct_212:.0f}%)", 'Same, PSLN-212', 'as above', '', 'Sum')
# monocytes day 8 etc already registered; CD40/CD86 % of young registered via reg_pair
# HAI >= 40 in PSLN-212 aged and survival
# S13-F PSLN-212 survivors by weights
inf = pd.read_csv('qc_tte_vs_bodyweight.csv')
r_ = inf[(inf.weight_block=='S13-F')&(inf.group=='PSLN-212')].iloc[0]
reg('s13f_212_bw', (int(r_.bw_alive_d14), int(r_.bw_n)), f'{int(r_.bw_alive_d14)}/{int(r_.bw_n)}', 'PSLN-212 aged animals alive at day 14 according to the weight traces of the matched-H1N1 challenge (flag Q10/Q11)', 'S13-F', 'S13!P33:V40', 'traces not frozen/blank at day 14')
r_ = inf[(inf.weight_block=='S15-D')&(inf.group=='PSLN-344')].iloc[0]
reg('s15d_344_bw', (int(r_.bw_alive_d14), int(r_.bw_n)), f'{int(r_.bw_alive_d14)}/{int(r_.bw_n)}', 'PSLN-344 aged animals alive at day 14 according to the weight traces of the day-3 rgH5N1 challenge (survival block says 7/7; flag Q10)', 'S15-D', 'S15!W33:AC40', 'traces not frozen at day 14')
# TTE vs BW mismatch count
mm = inf[inf.flag.fillna('').str.contains('MISMATCH')]
reg('qc_mismatch_n', len(mm), f'{len(mm)}', 'Groups in which the survival block and the linked weight block imply different survivor counts or animal numbers', '; '.join(f'{a}/{b} {g}' for a,b,g in zip(mm.tte_block, mm.weight_block, mm.group)), '', 'see qc_tte_vs_bodyweight.csv')
# young-mouse comparisons
for blk,k,lab in [('S01-F','cdc1','Lung cDC1 72 h'),('S02-C','agdc','Antigen-positive DC in lymph node'),('S02-E','prime','OT-I priming ex vivo')]:
    c = C(blk,'PSLN-212(Y)','PSLN-344(Y)')
    reg(f'y_{k}', (c['mean_ref'],c['mean_test']), f'{c["mean_test"]:.1f}% vs {c["mean_ref"]:.1f}%', f'{lab}, young mice: PSLN-344 vs PSLN-212, means (n=5); Welch p={c["p_welch"]:.2f}', blk, c['cells_test']+'; '+c['cells_ref'], 'mean; Welch')
d = T['S01-E']; a = d[(d.group=='PSLN-344(Y)')&(d.day=='4')]['value']; b = d[(d.group=='PSLN-212(Y)')&(d.day=='4')]['value']
reg('y_dc4', (b.mean(), a.mean()), f'{a.mean():.1f}% vs {b.mean():.1f}%', 'Lung CD11b+ DC day 4, young mice: PSLN-344 vs PSLN-212; Welch p=%.2f' % stats.ttest_ind(a,b,equal_var=False).pvalue, 'S01-E', cells_of('S01-E','PSLN-344(Y)',day='4')+'; '+cells_of('S01-E','PSLN-212(Y)',day='4'), 'mean; Welch')
bw = pd.read_csv('bw_challenge_nadir.csv')
for blk,k in [('S09-C','pr8'),('S09-E','perth'),('S09-G','h5')]:
    a = bw[(bw.block==blk)&(bw.group=='PSLN-344Y')].iloc[0].mean_max_loss; b = bw[(bw.block==blk)&(bw.group=='PSLN-212Y')].iloc[0].mean_max_loss
    reg(f'y_wl_{k}', (a,b), f'{a:.1f}% vs {b:.1f}%', f'Young mice, mean maximum weight loss after challenge, PSLN-344 vs PSLN-212 (n=8)', blk, '', 'per-animal minimum, group mean')
# CMP-204 vs PSLN-212 aged
c = C('S01-A_16h','CMP-204','PSLN-212'); reg('cdn_vs_cgamp', c['fold'], f'{c["fold"]:.1f}×', f'Ifnb1 16 h, aged: PSLN-212 (CDN-1807) over CMP-204 (cGAMP), ratio of geometric means; Welch p={c["p_welch"]:.1g}', 'S01-A', c['cells_ref']+'; '+c['cells_test'], 'Welch on log10')
# S01-C etc fold
c = C('S01-B','AECII/FreeSRB','AECII/PSLN-SRB'); reg('srb2_fold', c['fold'], f'{c["fold"]:.0f}×', 'Type II epithelial cells: liposomal dye over free dye, ratio of means', 'S01-B', '', 'ratio')
# S07-C
a = B['S07-C']; m = a.groupby('group')['value'].mean().tolist(); reg('s07c', m, f'{m[0]:.1f}% vs {m[1]:.1f}%', 'Lung Treg after transfer of two macrophage subsets whose column labels are identical (flag Q13)', 'S07-C', 'S07!B16:C20', 'mean')
# sci formatting fix
sup = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
def sci(p):
    m, e = f'{p:.0e}'.split('e'); return f'{m}×10{str(int(e)).translate(sup)}'
N['p_slr_A'] = 'p = ' + sci(rA.p_strat_logrank); N['p_slr_B'] = 'p = ' + sci(rB.p_strat_logrank)
for row in LEDGER:
    if row['Key'] in ('p_slr_A','p_slr_B'): row['Value_as_cited'] = N[row['Key']]
rd_F = prow('F:')
# ---- late additions used in tables
reg('p_cmh_F', rd_F.p_cmh, 'p = ' + sci(rd_F.p_cmh), 'Cochran-Mantel-Haenszel test, worst-case set F', 'S06-A,B,D,E,F,G with weight-inferred counts', '', 'CMH with continuity correction (statsmodels StratifiedTable)')
_st = [(b,'PSLN-344','PSLN-212') for b in A_blocks+['S15-L','S15-N']] + [(b,p+'PSLN-344',p+'PSLN-212') for b in ['S06-E2','S06-F2'] for p in ['Naïve+','Imprinting+']]
rd, lo, hi = mh_rd(_st)
reg('rdci_C', (rd,lo,hi), f'{100*rd:.0f} points (95% CI {100*lo:.0f}–{100*hi:.0f})', 'Mantel-Haenszel difference in survival, all 15 head-to-head strata', 'S03-I/J, S06-A..G, S15-L/N, S06-E2/F2', '', 'Mantel-Haenszel risk difference, Greenland-Robins variance')
c = C('S01-A_16h','PSLN-212(Y)','PSLN-344(Y)')
reg('ifn16_y_p', (c['p_welch'], c['p_tukey']), f'p = {c["p_welch"]:.3f} Welch, {c["p_tukey"]:.2f} after Tukey', 'Ifnb1 16 h, young mice, PSLN-344 vs PSLN-212: p-values', 'S01-A', '', 'Welch on log10; one-way ANOVA + Tukey over 8 groups')

# ---- restoration medians restricted to read-outs where aged PSLN-212 falls short of the young benchmark
_def = ri[(ri.pct_of_young_212 < 100) & (ri.block != 'S01-A_72h')]
reg('ri_def_n', len(_def), f'{len(_def)}', 'Read-outs in which aged mice given PSLN-212 are below the young benchmark (deficits)', '; '.join(_def.block), '', 'count')
reg('ri_def_med344', _def.pct_of_young_344.median(), f'{_def.pct_of_young_344.median():.0f}%', 'Median of PSLN-344 (aged) as % of young benchmark across the deficit read-outs', 'as above', '', 'median of ratios of (geometric) means')
reg('ri_def_med212', _def.pct_of_young_212.median(), f'{_def.pct_of_young_212.median():.0f}%', 'Median of PSLN-212 (aged) as % of young benchmark across the deficit read-outs', 'as above', '', 'median of ratios of (geometric) means')
_pw = fisher_power(0.80, 0.40, 32); reg('power_32', _pw, f'{100*_pw:.0f}%', 'Power with 32 per arm for 80% vs 40% survival (Fisher exact, two-sided 5%)', 'design calculation', '', 'Exact enumeration')
_pw = fisher_power(0.71, 0.12, 16); reg('power_16', _pw, f'{100*_pw:.0f}%', 'Power with 16 per arm for 71% vs 12% survival (Fisher exact, two-sided 5%)', 'design calculation', '', 'Exact enumeration')



# ---- young mice, day-180 challenge: recovery is slower with PSLN-344 (S09-G)
_g = W['S09-G']
_a = _g[(_g.group=='PSLN-344Y')&(_g.day==14)]['value']; _b = _g[(_g.group=='PSLN-212Y')&(_g.day==14)]['value']
reg('y180_d14_344', _a.mean(), f'{_a.mean():.1f}%', 'Young mice challenged 180 days after dosing: body weight 14 days after challenge, PSLN-344 (n=8), % of day 0', 'S09-G', cells_of('S09-G','PSLN-344Y',day=14), 'mean')
reg('y180_d14_212', _b.mean(), f'{_b.mean():.1f}%', 'Same, PSLN-212 (n=8)', 'S09-G', cells_of('S09-G','PSLN-212Y',day=14), 'mean')
_p = stats.ttest_ind(_a, _b, equal_var=False).pvalue; _pm = stats.mannwhitneyu(_a, _b, alternative='two-sided', method='exact').pvalue
reg('y180_d14_p', (_p, _pm), f'p = {_p:.3f}', f'Day-14 weight after day-180 challenge, PSLN-344 vs PSLN-212 in young mice: Welch t-test (exact Mann-Whitney p = {_pm:.3f})', 'S09-G', '', 'Welch; Mann-Whitney exact')
_na = _g[(_g.group=='PSLN-344Y')&(_g.day>0)].groupby('rep')['value'].min(); _nb = _g[(_g.group=='PSLN-212Y')&(_g.day>0)].groupby('rep')['value'].min()
_pn = stats.ttest_ind(_na, _nb, equal_var=False).pvalue
reg('y180_nadir', (_na.mean(), _nb.mean(), _pn), f'{100-_na.mean():.1f}% against {100-_nb.mean():.1f}%, p = {_pn:.2f}', 'Young mice, day-180 challenge: mean largest weight loss, PSLN-344 vs PSLN-212 (Welch)', 'S09-G', 'S09!G67:AD73', 'per-animal minimum; Welch')
# 72 h cytokines PSLN-344 vs PSLN-212 (aged)
for an in ['Il6','Ccl2','Tnf']:
    c = C('S09-A_right','PSLN-212','PSLN-344', analyte=an)
    reg(f'cyt72_ratio_{an}', 10**c['diff'], f'{10**c["diff"]:.1f}×', f'Lung {an} at 72 h (right panel of S09-A): PSLN-344 over PSLN-212, ratio of geometric means; Welch p={c["p_welch"]:.2f}; n=3', 'S09-A', c['cells_ref']+'; '+c['cells_test'], '10^(difference of mean log10); Welch')

# ---- cell accounting for the Methods appendix
_nn, _coords = count_all_numeric_cells()
_used = set()
for _D in (B, T, S, W):
    for _df in _D.values(): _used |= set(_df['cellref'])
_rest = _coords - _used
_orph = {c for c in _rest if c.startswith('S08!') and int(''.join(ch for ch in c.split('!')[1] if ch.isdigit())) >= 89}
reg('cells_data', len(_used), f'{len(_used):,}', 'Numeric cells parsed as data values', 'all sheets', '', 'blocks.py')
reg('cells_axis', len(_rest) - len(_orph), f'{len(_rest)-len(_orph):,}', 'Numeric cells that are axis values (days, hours, doses)', 'all sheets', '', 'blocks.py')
reg('cells_orphan', len(_orph), f'{len(_orph)}', 'Numeric cells in the unlabelled region of sheet S08 (rows 89-101)', 'S08', 'S08!A89:D101', 'blocks.py')

# ---- single-experiment tests, PSLN-344 vs PSLN-212, nine aged BALB/c experiments
_pw = pd.read_csv('stats_survival_pairwise.csv')
_sel = _pw[_pw.block.isin(A_blocks) & (((_pw.g1=='PSLN-212')&(_pw.g2=='PSLN-344'))|((_pw.g1=='PSLN-344')&(_pw.g2=='PSLN-212')))]
assert len(_sel) == 9
reg('single_lr_sig', int((_sel.p_logrank_perm < 0.05).sum()), f'{int((_sel.p_logrank_perm < 0.05).sum())} of 9', f'Aged BALB/c experiments in which PSLN-344 vs PSLN-212 reaches p<0.05 by permutation log-rank test (range of p {_sel.p_logrank_perm.min():.4f}-{_sel.p_logrank_perm.max():.3f})', ', '.join(A_blocks), cellsA, 'Log-rank statistic, exact permutation p')
reg('single_lr_max', float(_sel.p_logrank_perm.max()), f'{_sel.p_logrank_perm.max():.3f}', 'Largest permutation log-rank p among the nine experiments', ', '.join(A_blocks), '', 'as above')
reg('single_fisher_sig', int((_sel.p_fisher < 0.05).sum()), f'{int((_sel.p_fisher < 0.05).sum())} of 9', 'Aged BALB/c experiments in which PSLN-344 vs PSLN-212 reaches p<0.05 by Fisher exact test on survivor counts', ', '.join(A_blocks), cellsA, 'Fisher exact, two-sided')

# ---- design calculation: probability of meeting the Study 1 go rule (E vs D: >= 40 points overall with 32 per arm, same direction in each sex)
def go_prob(pE, pD, n_sex=16, sims=400000, seed=7):
    rng = np.random.default_rng(seed)
    eF = rng.binomial(n_sex, pE, sims); eM = rng.binomial(n_sex, pE, sims); dF = rng.binomial(n_sex, pD, sims); dM = rng.binomial(n_sex, pD, sims)
    return float((((eF+eM) - (dF+dM) >= 0.40*2*n_sex) & (eF > dF) & (eM > dM)).mean())
_g1 = go_prob(0.71, 0.12); _g2 = go_prob(0.40, 0.20)
reg('go_prob_worst', _g1, f'{100*_g1:.0f}%', 'Probability that Study 1 meets its go rule for E vs D if the true survival rates are the worst-case estimates (71% vs 12%)', 'design calculation', '', 'Simulation, 400,000 draws, 16 per sex per arm')
reg('go_prob_20pt', _g2, f'{100*_g2:.0f}%', 'Probability that Study 1 meets its go rule for E vs D if the true difference is only 20 points (40% vs 20%)', 'design calculation', '', 'Simulation, 400,000 draws, 16 per sex per arm')

if __name__ == '__main__':
    L = pd.DataFrame(LEDGER); L.to_csv('evidence_ledger.csv', index=False); print(len(L), 'ledger rows written to evidence_ledger.csv')
