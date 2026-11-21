"""Evidence ledger: every number quoted in the proposal is computed here from the tidy data and written with its provenance
(block, workbook cells, analysis method, script).  The proposal text is filled from this ledger, so text and ledger cannot drift apart."""
import json, re, math
import numpy as np, pandas as pd
from scipy import stats
import tidy, survlib as S
def CI(col):
    n = 0
    for ch in col: n = n * 26 + (ord(ch) - 64)
    return n
def CL(n):
    s = ''
    while n: n, r = divmod(n - 1, 26); s = chr(65 + r) + s
    return s
T = tidy.T()
IDX = pd.read_csv('../data_tidy/psln_block_index.csv').set_index('block')

def cells(block):
    d = T[T.block == block]
    cols = [CI(re.match(r'[A-Z]+', c).group()) for c in d.cell]; rows = [int(re.search(r'\d+', c).group()) for c in d.cell]
    return f"{IDX.loc[block, 'sheet']}!{CL(min(cols))}{min(rows)}:{CL(max(cols))}{max(rows)}"

L = []   # ledger rows
N = {}   # key -> formatted string
def reg(key, value, desc, blocks, method, script, flag=''):
    assert key not in N, key
    N[key] = value
    bl = blocks if isinstance(blocks, (list, tuple)) else [blocks]
    L.append(dict(key=key, value=value, description=desc, blocks='; '.join(bl), cells='; '.join(cells(b) for b in bl) if bl else 'whole workbook', method=method, script=script, flag=flag))

def pct(k, n): return f"{100*k/n:.0f}%"
def ci(k, n):
    lo, hi = S.cp(k, n); return f"{100*lo:.0f}–{100*hi:.0f}%"
def pfmt(p):
    if p < 1e-4:
        e = int(math.floor(math.log10(p))); m = p / 10 ** e
        return f"{m:.1f}×10⁻{str(abs(e)).translate(str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹'))}"
    return f"{p:.4f}" if p < 0.001 else (f"{p:.3f}" if p < 0.1 else f"{p:.2f}")

# ---------------------------------------------------------------------------------------------- survival
def surv(blocks, g):
    k = n = 0
    for b in blocks:
        d = S.prep(b); s = d[d.group == g]; k += int((s.event == 0).sum()); n += len(s)
    return k, n
ACUTE = ['S03-I', 'S03-J', 'S06-A', 'S06-B', 'S06-C', 'S06-D']; ROB = ['S06-A', 'S06-B', 'S06-C']; D60 = ['S06-E', 'S06-F', 'S06-G']
M_SURV = 'survivors / animals at end of observation; exact Clopper–Pearson 95% CI'
for tag, bl, lab in [('acute', ACUTE, 'aged BALB/c, challenge 2–14 d after one dose, all six blocks as printed'),
                     ('rob', ROB, 'aged BALB/c, challenge 3–14 d after one dose, flag-robust blocks'), ('d60', D60, 'aged BALB/c, challenge 60 d after one dose')]:
    for g, gk in [('PSLN-344', '344'), ('PSLN-212', '212'), ('Sham', 'sham'), ('PSLN-212(Y)', 'y212')]:
        bl_g = [b for b in bl if g in tidy.groups(b)]
        k, n = surv(bl_g, g)
        reg(f'{tag}_{gk}', f"{k}/{n}", f'Survival, {g}, {lab}', bl_g, M_SURV, '03b_survival_pooled.py', 'includes flagged blocks' if tag == 'acute' else '')
        reg(f'{tag}_{gk}_pct', pct(k, n), f'Survival %, {g}, {lab}', bl_g, M_SURV, '03b_survival_pooled.py')
        reg(f'{tag}_{gk}_ci', ci(k, n), f'95% CI of survival %, {g}, {lab}', bl_g, M_SURV, '03b_survival_pooled.py')
k, n = surv(D60, 'Untreated')
reg('d60_untreated', f"{k}/{n}", 'Survival of untreated, unchallenged aged animals over the same 14-d window (background)', D60, M_SURV, '03b_survival_pooled.py')
reg('d60_untreated_pct', pct(k, n), 'as above, %', D60, M_SURV, '03b_survival_pooled.py'); reg('d60_untreated_ci', ci(k, n), 'as above, CI', D60, M_SURV, '03b_survival_pooled.py')
reg('bg_deaths', f"{n-k}/{n}", 'Deaths among untreated, unchallenged aged animals in 14 d', D60, 'count', '03b_survival_pooled.py')
reg('bg_deaths_pct', pct(n - k, n), 'as above, %', D60, 'count', '03b_survival_pooled.py'); reg('bg_deaths_ci', ci(n - k, n), 'as above, CI', D60, M_SURV, '03b_survival_pooled.py')
PO = pd.read_csv('../tables/T3_survival_pooled.csv')
def po(setname, contrast, col): return PO[(PO.set == setname) & (PO.contrast == contrast)][col].iloc[0]
for tag, setname, bl in [('acute', 'ACUTE as printed', ACUTE), ('rob', 'ACUTE flag-robust', ROB), ('d60', 'D60', D60)]:
    reg(f'{tag}_rd', f"{po(setname, 'PSLN-344 vs PSLN-212', 'MH_risk_diff_pct'):.0f}", f'Mantel–Haenszel survival difference PSLN-344 − PSLN-212, percentage points ({setname})', bl, 'Mantel–Haenszel risk difference stratified by experiment, Greenland–Robins 95% CI', '03b_survival_pooled.py')
    reg(f'{tag}_rd_ci', f"{po(setname, 'PSLN-344 vs PSLN-212', 'RD_lo'):.0f} to {po(setname, 'PSLN-344 vs PSLN-212', 'RD_hi'):.0f}", 'CI of the above', bl, 'as above', '03b_survival_pooled.py')
    reg(f'{tag}_lr_p', pfmt(po(setname, 'PSLN-344 vs PSLN-212', 'strat_logrank_p')), f'Stratified log-rank p, PSLN-344 vs PSLN-212 ({setname})', bl, 'log-rank stratified by experiment (cross-checked with R survival::survdiff)', '03b_survival_pooled.py; 03c_survival_crosscheck.R')
reg('d60_344_vs_young_p', pfmt(po('D60', 'PSLN-344 vs PSLN-212(Y)', 'strat_logrank_p')), 'Stratified log-rank p, aged PSLN-344 vs young PSLN-212 at d60', D60, 'stratified log-rank', '03b_survival_pooled.py')
reg('d60_344_vs_untreated_p', pfmt(po('D60', 'PSLN-344 vs Untreated', 'strat_logrank_p')), 'Stratified log-rank p, challenged PSLN-344 vs unchallenged untreated at d60', D60, 'stratified log-rank', '03b_survival_pooled.py')
a, b_ = surv(D60, 'PSLN-344'); c, d_ = surv(D60, 'Untreated')
reg('d60_344_vs_untreated_fisher', pfmt(stats.fisher_exact([[b_ - a, a], [d_ - c, c]])[1]), 'Fisher exact p, deaths PSLN-344 (challenged d60) vs untreated (unchallenged)', D60, 'Fisher exact, two-sided', '03b_survival_pooled.py')
# other settings
for key, bl, g, desc in [('strain_344', ['S15-L', 'S15-N'], 'PSLN-344', 'aged C57BL/6 + Swiss Webster'), ('strain_212', ['S15-L', 'S15-N'], 'PSLN-212', 'aged C57BL/6 + Swiss Webster'),
                         ('strain_sham', ['S15-L', 'S15-N'], 'Sham', 'aged C57BL/6 + Swiss Webster'), ('strain_y212', ['S15-L', 'S15-N'], 'PSLN-212(Y)', 'young C57BL/6 + Swiss Webster'),
                         ('m14_344_naive', ['S06-E[r71]', 'S06-F[r71]'], 'Naive+PSLN-344', '14-month BALB/c, no prior infection'), ('m14_212_naive', ['S06-E[r71]', 'S06-F[r71]'], 'Naive+PSLN-212', '14-month BALB/c, no prior infection'),
                         ('m14_344_impr', ['S06-E[r71]', 'S06-F[r71]'], 'Imprinting+PSLN-344', '14-month BALB/c, PR8-imprinted'), ('m14_212_impr', ['S06-E[r71]', 'S06-F[r71]'], 'Imprinting+PSLN-212', '14-month BALB/c, PR8-imprinted'),
                         ('young_344', ['S09-B', 'S09-D', 'S09-F'], 'PSLN-344Y', 'young BALB/c'), ('young_212', ['S09-B', 'S09-D', 'S09-F'], 'PSLN-212Y', 'young BALB/c'), ('young_sham', ['S09-B', 'S09-D', 'S09-F'], 'Sham', 'young BALB/c')]:
    k, n = surv(bl, g); reg(key, f"{k}/{n}", f'Survival, {g}, {desc}', bl, M_SURV, '03b_survival_pooled.py'); reg(key + '_pct', pct(k, n), f'Survival %, {g}, {desc}', bl, M_SURV, '03b_survival_pooled.py')
for b in ['S03-I', 'S03-J', 'S06-A', 'S06-B', 'S06-C', 'S06-D', 'S06-E', 'S06-F', 'S06-G', 'S06-E[r71]', 'S06-F[r71]', 'S09-B', 'S09-D', 'S09-F', 'S15-H', 'S15-L', 'S15-N', 'S13-E']:
    for g in tidy.groups(b):
        k, n = surv([b], g)
        gk = re.sub(r'[^A-Za-z0-9]+', '', g); bk = re.sub(r'[^A-Za-z0-9]+', '', b)
        reg(f'{bk}_{gk}', f"{k}/{n}", f'Survival, {g}, block {b}', [b], 'survivors / animals', '03_survival.py')
k1, n1 = surv(['S03-J', 'S06-B', 'S15-H'], 'PSLN-344'); k2, n2 = surv(['S15-H'], '3d Vaccine+PSLN-344')
reg('early_344', f"{k1 + k2}/{n1 + n2}", 'Survival with PSLN-344 + vaccine when challenged 2–3 d after dosing (S03-J d2, S06-B d3, S15-H d3); S06-D omitted as duplicate', ['S03-J', 'S06-B', 'S15-H'], M_SURV, '10_numbers.py')
reg('early_344_pct', pct(k1 + k2, n1 + n2), 'as above, %', ['S03-J', 'S06-B', 'S15-H'], M_SURV, '10_numbers.py'); reg('early_344_ci', ci(k1 + k2, n1 + n2), 'as above, CI', ['S03-J', 'S06-B', 'S15-H'], M_SURV, '10_numbers.py')
PW = pd.read_csv('../tables/T2_survival_pairwise.csv')
def pw(block, contrast, col): return PW[(PW.block == block) & (PW.contrast == contrast)][col].iloc[0]
reg('S03I_cmp_vs_212_p', pfmt(pw('S03-I', 'CMP-204 vs PSLN-212', 'logrank_p')), 'Log-rank p, CMP-204 vs PSLN-212 in S03-I as printed', ['S03-I'], 'log-rank (asymptotic); exact permutation p = ' + pfmt(pw('S03-I', 'CMP-204 vs PSLN-212', 'logrank_exact_p')), '03_survival.py', 'labels disputed (Q2)')
reg('S15H_combo_vs_adj_p', pfmt(pw('S15-H', '3d Vaccine+PSLN-344 vs 3d PSLN-344', 'logrank_exact_p')), 'Exact log-rank p, vaccine + PSLN-344 vs PSLN-344 alone', ['S15-H'], 'exact permutation log-rank', '03_survival.py')
reg('S15H_adj_vs_vac_p', pfmt(pw('S15-H', '3d PSLN-344 vs 3d Vaccine', 'logrank_exact_p')), 'Exact log-rank p, PSLN-344 alone vs vaccine alone', ['S15-H'], 'exact permutation log-rank', '03_survival.py')

# ---------------------------------------------------------------------------------------------- immunology
SUM = pd.read_csv('../tables/T4_group_summaries.csv'); P5 = pd.read_csv('../tables/T5_pairwise_tests.csv'); R7 = pd.read_csv('../tables/T7_restoration_table.csv')
def mean(b, g, x=None): return tidy.vec(b, g, x).mean()
def sd(b, g, x=None): return tidy.vec(b, g, x).std(ddof=1)
def gmt(b, g):
    v = tidy.vec(b, g); return float(np.exp(np.log(np.where(v <= 0, 5, v)).mean()))
def tuk(b, a, c, x=None, col='p'):
    q = P5[(P5.block == b) & (((P5.g1 == a) & (P5.g2 == c)) | ((P5.g1 == c) & (P5.g2 == a)))]
    q = q[q.x == x] if x is not None else q[q.x.isna()]
    return float(q[col].iloc[0])
M_MEAN = 'arithmetic mean of per-animal values'; M_GMT = 'geometric mean titre (values below 1:10 set to 5)'
def regmean(key, b, g, x=None, fmt='{:.1f}', desc=None):
    reg(key, fmt.format(mean(b, g, x)), desc or f'Mean, {g}, {IDX.loc[b, "measurand"]}' + (f' at x={x:g}' if x is not None else ''), [b], M_MEAN + f' (n={len(tidy.vec(b, g, x))})', '04_immunology_stats.py')
def reggmt(key, b, g):
    reg(key, f"{gmt(b, g):,.0f}", f'GMT, {g}, {IDX.loc[b, "measurand"]}', [b], M_GMT + f' (n={len(tidy.vec(b, g))})', '04_immunology_stats.py')

for g, gk in [('Sham', 'sham'), ('CMP-204', 'cmp'), ('PSLN-212', 'a212'), ('PSLN-R848', 'r848'), ('PSLN-212/R848', 'a212r848'), ('PSLN-344', 'a344'), ('PSLN-212(Y)', 'y212'), ('PSLN-344(Y)', 'y344')]:
    regmean(f'ifnb16_{gk}', 'S01-A 16h', g); regmean(f'ifnb72_{gk}', 'S01-A 72h', g)
reg('ifnb16_p_344_212', pfmt(tuk('S01-A 16h', 'PSLN-344', 'PSLN-212')), 'Tukey p, Ifnb1 16 h, PSLN-344 vs PSLN-212 (aged)', ['S01-A 16h'], 'one-way ANOVA + Tukey HSD (8 groups)', '04_immunology_stats.py')
reg('ifnb72_p_344_y212', pfmt(tuk('S01-A 72h', 'PSLN-344', 'PSLN-212(Y)')), 'Tukey p, Ifnb1 72 h, aged PSLN-344 vs young PSLN-212', ['S01-A 72h'], 'one-way ANOVA + Tukey HSD (8 groups)', '04_immunology_stats.py')
reg('ifnb16_212_pct_young', f"{100*mean('S01-A 16h','PSLN-212')/mean('S01-A 16h','PSLN-212(Y)'):.0f}%", 'Aged PSLN-212 Ifnb1 16 h as % of young PSLN-212', ['S01-A 16h'], 'ratio of means', '10_numbers.py')
reg('ifnb16_344_pct_young', f"{100*mean('S01-A 16h','PSLN-344')/mean('S01-A 16h','PSLN-212(Y)'):.0f}%", 'Aged PSLN-344 Ifnb1 16 h as % of young PSLN-212', ['S01-A 16h'], 'ratio of means', '10_numbers.py')
for t in (16, 36, 72):
    for g, gk in [('PSLN-344', 'a344'), ('PSLN-212', 'a212'), ('Sham', 'sham')]:
        regmean(f'gmcsf{t}_{gk}', 'S02-F', g, t)
reg('gmcsf_212_max', f"{max(mean('S02-F','PSLN-212',t) for t in (16,36,72)):.1f}", 'Highest mean Gm-csf fold with PSLN-212 across 16/36/72 h', ['S02-F'], M_MEAN, '10_numbers.py')
reg('gmcsf36_p', pfmt(tuk('S02-F', 'PSLN-344', 'PSLN-212', 36.0)), 'Tukey p, Gm-csf 36 h, PSLN-344 vs PSLN-212', ['S02-F'], 'Tukey HSD within time point (3 groups)', '04_immunology_stats.py')
DR = pd.read_csv('../tables/T8_dose_response_S08A.csv').set_index('prep')
for g, gk in [('PSLN-344', 'a344'), ('PSLN-212', 'a212'), ('CMP-204', 'cmp')]:
    reg(f'emax_{gk}', f"{DR.loc[g,'Emax']:.0f}", f'Emax (fold), {g}, Ifnb1 dose-response', ['S08-A'], 'Hill model E = 1 + Emax·d^h/(ED50^h + d^h), log-scale least squares; bootstrap 95% CI ' + f"{DR.loc[g,'Emax_lo']:.0f}–{DR.loc[g,'Emax_hi']:.0f}", '05_dose_response.py')
    reg(f'ed50_{gk}', f"{DR.loc[g,'ED50_ug']:.0f}", f'ED50 (µg), {g}', ['S08-A'], 'as above; bootstrap 95% CI ' + f"{DR.loc[g,'ED50_lo']:.0f}–{DR.loc[g,'ED50_hi']:.0f}", '05_dose_response.py')
    reg(f'emax_{gk}_ci', f"{DR.loc[g,'Emax_lo']:.0f}–{DR.loc[g,'Emax_hi']:.0f}", f'Bootstrap 95% CI of Emax, {g}', ['S08-A'], '2,000 bootstrap resamples within dose', '05_dose_response.py')
    reg(f'ed50_{gk}_ci', f"{DR.loc[g,'ED50_lo']:.0f}–{DR.loc[g,'ED50_hi']:.0f}", f'Bootstrap 95% CI of ED50, {g}', ['S08-A'], '2,000 bootstrap resamples within dose', '05_dose_response.py')
d8 = tidy.get('S08-A')
for dose in (5, 10, 20, 40):
    for g, gk in [('PSLN-344', 'a344'), ('PSLN-212', 'a212'), ('CMP-204', 'cmp'), ('PSLN-344/R848', 'x344r848')]:
        reg(f'dr{dose}_{gk}', f"{d8[(d8.group == g) & (d8.x == dose)].value.mean():.1f}", f'Mean Ifnb1 fold at {dose} µg, {g}', ['S08-A'], M_MEAN + ' (n=3)', '05_dose_response.py')
reg('dr_plateau', f"{DR.loc['PSLN-344','pct_of_40ug_reached_at_20ug']:.0f}%", 'PSLN-344 response at 20 µg as % of response at 40 µg', ['S08-A'], 'ratio of means', '05_dose_response.py')
from scipy.optimize import brentq
p344 = (DR.loc['PSLN-344', 'Emax'], DR.loc['PSLN-344', 'ED50_ug'], DR.loc['PSLN-344', 'hill'])
mdl = lambda x: 1 + p344[0] * x ** p344[2] / (p344[1] ** p344[2] + x ** p344[2])
reg('dose_eq_212', f"{brentq(lambda x: mdl(x) - d8[(d8.group == 'PSLN-212') & (d8.x == 20)].value.mean(), 0.5, 40):.1f}", 'PSLN-344 dose (µg) giving the Ifnb1 induction of 20 µg PSLN-212', ['S08-A'], 'interpolation on fitted Hill curve (model-free log-log interpolation gives 6.8)', '05_dose_response.py')
reg('dose_eq_young', f"{brentq(lambda x: mdl(x) - mean('S01-A 16h', 'PSLN-212(Y)'), 0.5, 40):.0f}", 'PSLN-344 dose (µg) in aged mice giving the Ifnb1 induction of 20 µg PSLN-212 in young mice', ['S08-A', 'S01-A 16h'], 'interpolation on fitted Hill curve (model-free: 16.8)', '05_dose_response.py')

# innate / myeloid
for key, b, x in [('mono4', 'S01-D', 4), ('mono8', 'S01-D', 8), ('dc4', 'S01-E', 4), ('dc8', 'S01-E', 8)]:
    for g, gk in [('Sham', 'sham'), ('PSLN-212', 'a212'), ('PSLN-344', 'a344'), ('PSLN-212(Y)', 'y212')]:
        regmean(f'{key}_{gk}', b, g, x)
reg('mono8_p_344_y212', pfmt(tuk('S01-D', 'PSLN-344', 'PSLN-212(Y)', 8.0)), 'Tukey p, lung monocytes d8, aged PSLN-344 vs young PSLN-212', ['S01-D'], 'Tukey HSD within day', '04_immunology_stats.py')
reg('dc8_p_344_y212', pfmt(tuk('S01-E', 'PSLN-344', 'PSLN-212(Y)', 8.0)), 'Tukey p, lung CD11b+ DC d8, aged PSLN-344 vs young PSLN-212', ['S01-E'], 'Tukey HSD within day', '04_immunology_stats.py')
for key, b in [('ccr7', 'S02-A'), ('mlndc', 'S02-B'), ('cd40', 'S02-D CD40'), ('cd86', 'S02-D CD86'), ('cd206', 'S11-E'), ('cdc1', 'S01-F'), ('ki67', 'S05-D'), ('gzmb3', 'S05-E'), ('ifng14', 'S05-F'), ('ifng60', 'S05-G'),
               ('gzmb60', 'S05-H'), ('trm', 'S05-I'), ('ifngH1', 'S14-A H1N1'), ('ifngH3', 'S14-A H3N2'), ('gcb', 'S03-K'), ('tfhhi', 'S04-A ICOShi'), ('tfr7', 'S04-B Foxp3'), ('tfr30', 'S04-C'), ('treg', 'S04-D'), ('iggb', 'S13-H')]:
    for g, gk in [('Sham', 'sham'), ('PSLN-212', 'a212'), ('PSLN-344', 'a344'), ('PSLN-212(Y)', 'y212')]:
        regmean(f'{key}_{gk}', b, g)
for g, gk in [('PSLN-212', 'a212'), ('PSLN-344', 'a344'), ('PSLN-212(Y)', 'y212'), ('PTX', 'ptx'), ('PSLN-344(Y)', 'y344')]:
    regmean(f'ova_{gk}', 'S02-C', g); regmean(f'oti_{gk}', 'S02-E', g)
regmean('spad_wt', 'S01-C', 'WT'); regmean('spad_ko', 'S01-C', 'SPA/D')
reg('spad_p', pfmt(tuk('S01-C', 'WT', 'SPA/D')), 'Student t p, DiD+ AM, WT vs SP-A/D-null', ['S01-C'], "Student's t (n=4 v 4)", '04_immunology_stats.py')
for g, gk in [('AECII/PSLN-SRB', 'aec2'), ('AECI/PSLN-SRB', 'aec1'), ('AECII/FreeSRB', 'aec2free'), ('AECI/FreeSRB', 'aec1free')]:
    regmean(f'srb_{gk}', 'S01-B', g, fmt='{:.1f}' if 'Free' not in g else '{:.2f}')
for g, gk in [('AECII-PSLN-SRB', 'c_a'), ('AECII-PSLN-344-SRB', 'c_b'), ('AECI-PSLN-SRB', 'c_c'), ('AECI-PSLN-344-SRB', 'c_d')]:
    regmean(f'srb08_{gk}', 'S08-C', g)
regmean('cbx_minus', 'S11-C', 'CBX-'); regmean('cbx_plus', 'S11-C', 'CBX+')
reg('cbx_p', pfmt(tuk('S11-C', 'CBX+', 'CBX-')), 'Student t p, recruited monocytes ± carbenoxolone', ['S11-C'], "Student's t (n=5 v 5)", '04_immunology_stats.py')
regmean('incb_mono_ctl', 'S07-B mono', 'PSLN-344'); regmean('incb_mono_trt', 'S07-B mono', 'PSLN-344+INCB3344')
regmean('incb_gzmb_ctl', 'S02-I', 'PSLN-344(Y)'); regmean('incb_gzmb_trt', 'S02-I', 'PSLN-344(Y)+INCB3344')
for g, gk in [('WT w/o cDC', 'wt'), ('IFN w/o cDC', 'ko'), ('GMCSF', 'kogm'), ('WT w/ cDC', 'wtcdc'), ('IFN w/ cDC', 'kocdc')]:
    regmean(f'modc_{gk}', 'S02-H', g)
reg('modc_p_wt_ko', pfmt(tuk('S02-H', 'WT w/o cDC', 'IFN w/o cDC')), 'Tukey p, donor moDC, WT vs Ifnar-null marrow (no cDC precursors)', ['S02-H'], 'one-way ANOVA + Tukey (5 groups)', '04_immunology_stats.py')
reg('modc_p_ko_gm', pfmt(tuk('S02-H', 'GMCSF', 'IFN w/o cDC')), 'Tukey p, Ifnar-null marrow ± GM-CSF', ['S02-H'], 'one-way ANOVA + Tukey (5 groups)', '04_immunology_stats.py')
regmean('ifnar_mono_wt', 'S12-A', 'WT to WT'); regmean('ifnar_mono_ko', 'S12-A', 'IFNAR-/- to WT')
reg('ifnar_mono_p', pfmt(tuk('S12-A', 'WT to WT', 'IFNAR-/- to WT')), 'Student t p, infiltrating monocytes WT vs Ifnar-null donor', ['S12-A'], "Student's t (n=3 v 3)", '04_immunology_stats.py')
for g, gk in [('GM-CSF', 'gm'), ('PSLN-212', 'a212'), ('PSLN-212+GM-CSF', 'a212gm')]:
    regmean(f'gmrescue_{gk}', 'S02-G', g)
for x in (5, 10):
    regmean(f'ly6cmac{x}_a212', 'S07-A', 'PSLN-212', x); regmean(f'ly6cmac{x}_a344', 'S07-A', 'PSLN-344', x)
for g, gk in [('Lung', 'lung'), ('Lung+PTX', 'lungptx'), ('MLN', 'mln'), ('MLN+PTX', 'mlnptx')]:
    regmean(f'otiv_{gk}', 'S05-C', g)
for g, gk in [('Sham', 'sham'), ('PSLN-212', 'a212'), ('PSLN-344', 'a344')]:
    regmean(f'aicda_{gk}', 'S03-L Aicda', g); regmean(f'e47_{gk}', 'S03-L E47', g)
# titres
for key, b in [('igg_h1', 'S03-A'), ('igg_h3', 'S03-E'), ('hai_h1', 'S03-C'), ('hai_h3', 'S03-G'), ('nab_h1', 'S03-D'), ('nab_h3', 'S03-H'), ('igg28_h1', 'S13-I'), ('igg28_h3', 'S13-J')]:
    for g, gk in [('Sham', 'sham'), ('CMP-204', 'cmp'), ('PSLN-212', 'a212'), ('PSLN-344', 'a344'), ('PSLN-212(Y)', 'y212')]:
        reggmt(f'{key}_{gk}', b, g)
    reg(f'{key}_fold', f"{gmt(b,'PSLN-344')/gmt(b,'PSLN-212'):.1f}", f'GMT ratio PSLN-344 / PSLN-212 (aged), {IDX.loc[b,"measurand"]}', [b], 'ratio of geometric means; Tukey on log2 titres p = ' + pfmt(tuk(b, 'PSLN-344', 'PSLN-212', col='p_log')), '04_immunology_stats.py')
    reg(f'{key}_pct_young', f"{100*gmt(b,'PSLN-344')/gmt(b,'PSLN-212(Y)'):.0f}%", f'Aged PSLN-344 GMT as % of young PSLN-212, {IDX.loc[b,"measurand"]}', [b], 'ratio of geometric means', '04b_restoration.py')
    reg(f'{key}_cmpfold', f"{gmt(b,'PSLN-212')/gmt(b,'CMP-204'):.1f}", f'GMT ratio PSLN-212 / CMP-204 (aged), {IDX.loc[b,"measurand"]}', [b], 'ratio of geometric means; Tukey on log2 titres p = ' + pfmt(tuk(b, 'PSLN-212', 'CMP-204', col='p_log')), '04_immunology_stats.py')
reg('hai_h1_212_min', f"{int(tidy.vec('S03-C','PSLN-212').min())}", 'Lowest individual HAI titre (H1N1) in aged PSLN-212 animals', ['S03-C'], 'minimum', '10_numbers.py')
reg('hai_h1_212_max', f"{int(tidy.vec('S03-C','PSLN-212').max())}", 'Highest individual HAI titre (H1N1) in aged PSLN-212 animals', ['S03-C'], 'maximum', '10_numbers.py')
reg('hai_h1_344_min', f"{int(tidy.vec('S03-C','PSLN-344').min())}", 'Lowest individual HAI titre (H1N1) in aged PSLN-344 animals', ['S03-C'], 'minimum', '10_numbers.py')
for key, num, den in [('ratio_h1', 'S13-A', 'S13-B'), ('ratio_h3', 'S13-C', 'S13-D')]:
    for g, gk in [('PSLN-212', 'a212'), ('PSLN-344', 'a344'), ('PSLN-212(Y)', 'y212')]:
        reg(f'{key}_{gk}', f"{(tidy.vec(num, g)/tidy.vec(den, g)).mean():.2f}", f'IgG2a/IgG1 quotient recomputed per animal ({num} ÷ {den}), {g}', [num, den], 'mean of per-animal quotients (n=5); replaces mislabelled S03-B / S03-F', '02a_qc_derived.py', 'S03-B/F labels rotated (Q1)')
for b, key in [('S03-B', 'ratio_h1_printed'), ('S03-F', 'ratio_h3_printed')]:
    for g, gk in [('PSLN-212', 'a212'), ('PSLN-344', 'a344'), ('PSLN-212(Y)', 'y212')]:
        regmean(f'{key}_{gk}', b, g, fmt='{:.2f}', desc=f'IgG2a/IgG1 quotient AS PRINTED under the header "{g}" in {b}')
for b, key in [('S13-I', 'h1'), ('S13-J', 'h3')]:
    b14 = 'S03-A' if key == 'h1' else 'S03-E'
    for g, gk in [('PSLN-344', 'a344'), ('PSLN-212', 'a212')]:
        reg(f'boostfold_{key}_{gk}', f"{gmt(b, g)/gmt(b14, g):.1f}", f'IgG GMT day 28 (after boost) ÷ day 14 (single dose), {g}', [b, b14], 'ratio of geometric means from two separate experiments (not paired)', '10_numbers.py')
reg('igg28_h1_p', pfmt(tuk('S13-I', 'PSLN-344', 'PSLN-212', col='p_log')), 'Tukey p (log2), IgG anti-H1N1 after boost, PSLN-344 vs PSLN-212', ['S13-I'], 'one-way ANOVA + Tukey on log2 titres', '04_immunology_stats.py')
reg('igg28_h3_p', pfmt(tuk('S13-J', 'PSLN-344', 'PSLN-212', col='p_log')), 'Tukey p (log2), IgG anti-H3N2 after boost, PSLN-344 vs PSLN-212', ['S13-J'], 'one-way ANOVA + Tukey on log2 titres', '04_immunology_stats.py')
# restoration summary (34 up-regulated read-outs of Fig 3)
FIG3 = ['S01-A 16h', 'S01-D (x=4)', 'S01-E (x=4)', 'S01-F', 'S02-A', 'S02-B', 'S02-C', 'S02-D CD40', 'S02-D CD86', 'S02-E', 'S05-D', 'S05-E', 'S05-F', 'S14-A H1N1', 'S14-A H3N2', 'S05-G', 'S05-H', 'S05-I',
        'S04-A ICOShi', 'S04-A ICOSlo', 'S03-K', 'S13-H', 'S03-C', 'S03-G', 'S03-D', 'S03-H', 'S03-A', 'S03-E', 'S13-A', 'S13-C', 'S13-B', 'S13-D', 'S13-I', 'S13-J']
up = R7[R7.block.isin(FIG3)]; assert len(up) == 34
rb = sorted(set(b.split(' (')[0] for b in FIG3))
reg('rest_n', '34', 'Number of up-regulated immune read-outs with aged-212, aged-344 and young-212 groups (Figure 3)', rb, 'count', '04b_restoration.py; 09b_fig_restoration.py')
reg('rest_344_med', f"{up.a344_pct_of_young.median():.0f}%", 'Median % of the young PSLN-212 response reached by aged PSLN-344 across the 34 read-outs', rb, 'ratio of means (GMT for titres) per read-out; median across read-outs (read-outs are not independent)', '04b_restoration.py')
reg('rest_344_iqr', f"{up.a344_pct_of_young.quantile(.25):.0f}–{up.a344_pct_of_young.quantile(.75):.0f}%", 'IQR of the above', rb, 'quartiles across read-outs', '04b_restoration.py')
reg('rest_344_range', f"{up.a344_pct_of_young.min():.0f}–{up.a344_pct_of_young.max():.0f}%", 'Range of the above', rb, 'min–max across read-outs', '04b_restoration.py')
reg('rest_212_med', f"{up.a212_pct_of_young.median():.0f}%", 'Median % of the young response reached by aged PSLN-212', rb, 'as above', '04b_restoration.py')
reg('rest_212_iqr', f"{up.a212_pct_of_young.quantile(.25):.0f}–{up.a212_pct_of_young.quantile(.75):.0f}%", 'IQR of the above', rb, 'as above', '04b_restoration.py')
reg('rest_nsig', f"{int((up.p_344_vs_212 < 0.05).sum())}", 'Read-outs (of 34) with Tukey p < 0.05 for PSLN-344 vs PSLN-212 in aged animals', rb, 'Tukey HSD per block (log2 for titres); no adjustment across blocks', '04b_restoration.py')
reg('rest_fold_range', f"{up.fold_344_vs_212.min():.1f}–{up.fold_344_vs_212.max():.0f}", 'Range of fold-difference PSLN-344 / PSLN-212 across the 34 read-outs', rb, 'ratio of means / GMTs', '04b_restoration.py')
# factorial
import statsmodels.formula.api as smf, statsmodels.api as sm
def fact(block, x=None):
    recs = []
    for g, age, mn in [('PSLN-212', 'aged', 0), ('PSLN-344', 'aged', 1), ('PSLN-212(Y)', 'young', 0), ('PSLN-344(Y)', 'young', 1)]:
        for v in tidy.vec(block, g, x): recs.append(dict(age=age, mn=mn, y=np.log2(v)))
    f = pd.DataFrame(recs); m = smf.ols('y ~ C(age) * mn', data=f).fit(); an = sm.stats.anova_lm(m, typ=2); ma = f.groupby(['age', 'mn'])['y'].mean()
    return 2 ** (ma['aged', 1] - ma['aged', 0]), 2 ** (ma['young', 1] - ma['young', 0]), an.loc['C(age):mn', 'PR(>F)']
for key, b, x in [('fx_ifnb', 'S01-A 16h', None), ('fx_dc', 'S01-E', 4), ('fx_cdc1', 'S01-F', None), ('fx_ova', 'S02-C', None), ('fx_oti', 'S02-E', None)]:
    fa, fy, p = fact(b, x)
    reg(f'{key}_aged', f"{fa:.1f}", f'Fold effect of Mn²⁺ (344 vs 212) in aged animals, {IDX.loc[b,"measurand"]}', [b], 'ratio of geometric means', '07_morbidity_and_factorial.py')
    reg(f'{key}_young', f"{fy:.1f}", f'Fold effect of Mn²⁺ (344 vs 212) in young animals, {IDX.loc[b,"measurand"]}', [b], 'ratio of geometric means', '07_morbidity_and_factorial.py')
    reg(f'{key}_p', pfmt(p), f'Age × Mn²⁺ interaction p, {IDX.loc[b,"measurand"]}', [b], 'two-way ANOVA on log2 values, interaction term', '07_morbidity_and_factorial.py')

# ---------------------------------------------------------------------------------------------- safety
T9 = pd.read_csv('../tables/T9_tolerability_S08D.csv').set_index('group')
for g, gk in [('PSLN-344', 'a344'), ('PSLN-212', 'a212'), ('Vaccine', 'vac'), ('PSLN-212/R848', 'r848'), ('PSLN-212(Y)', 'y212'), ('CMP-204', 'cmp')]:
    reg(f'bw_nadir_{gk}', f"{T9.loc[g,'nadir_mean']:.1f}", f'Mean per-animal body-weight nadir (% of day 0) after immunisation, {g}', ['S08-D'], 'mean of each animal\'s lowest post-dose weight (n=5)', '06_safety.py')
    reg(f'bw_worst_{gk}', f"{T9.loc[g,'max_loss_pct']:.1f}", f'Largest individual weight loss (%), {g}', ['S08-D'], 'maximum over animals', '06_safety.py')
    reg(f'bw_d10_{gk}', f"{T9.loc[g,'d10_mean']:.1f}", f'Mean body weight on day 10 (% of day 0), {g}', ['S08-D'], f"mean (n={int(T9.loc[g,'d10_n'])})", '06_safety.py')
nad = {g: tidy.get('S08-D')[(tidy.get('S08-D').group == g) & (tidy.get('S08-D').x > 0)].groupby('rep')['value'].min().values for g in tidy.groups('S08-D')}
r = stats.tukey_hsd(*nad.values()); gl = list(nad); cint = r.confidence_interval()
i, j = gl.index('PSLN-344'), gl.index('Vaccine')
reg('bw_diff_344_vac', f"{r.statistic[i,j]:+.1f}", 'Difference in mean nadir, PSLN-344 − vaccine alone (percentage points)', ['S08-D'], 'one-way ANOVA + Tukey HSD on per-animal nadir (6 groups)', '06_safety.py')
reg('bw_diff_344_vac_ci', f"{cint.low[i,j]:+.1f} to {cint.high[i,j]:+.1f}", '95% CI of the above', ['S08-D'], 'Tukey HSD simultaneous CI', '06_safety.py')
reg('bw_diff_344_vac_p', pfmt(r.pvalue[i, j]), 'Tukey p of the above', ['S08-D'], 'Tukey HSD', '06_safety.py')
i, j = gl.index('PSLN-212/R848'), gl.index('PSLN-344')
reg('bw_diff_r848_344_p', pfmt(r.pvalue[i, j]), 'Tukey p, nadir PSLN-212/R848 vs PSLN-344', ['S08-D'], 'Tukey HSD', '06_safety.py')
reg('bw_r848_n_gt10', f"{int(T9.loc['PSLN-212/R848','n_below_90'])}", 'PSLN-212/R848 animals (of 5) losing >10% body weight', ['S08-D'], 'count of animals with nadir < 90%', '06_safety.py')
CY = pd.read_csv('../tables/T10_lung_cytokines_S09A.csv')
def cy(panel, gene, g): return CY[(CY.panel.str.startswith(panel)) & (CY.gene == gene) & (CY.group == g)].fold_geomean.iloc[0]
for gene in ['Ifnb1', 'Il6', 'Ccl2', 'Ccl3', 'Ccl5', 'Tnf', 'Il10']:
    for g, gk in [('PSLN-344', 'a344'), ('PSLN-212', 'a212'), ('PSLN-212(y)', 'y212'), ('PSLN-212/R848', 'r848'), ('PSLN-R848', 'r848only')]:
        for panel, pk, blk in [('16', 'c16', 'S09-A[A:U]'), ('72', 'c72', 'S09-A[X:AS]')]:
            v = cy(panel, gene, g)
            reg(f'{pk}_{gene.lower()}_{gk}', f"{v:,.0f}" if v >= 10 else f"{v:.1f}", f'Lung {gene} fold vs untreated, {g}, panel {blk}', [f'{blk} {gene}'], 'geometric mean (10^mean of log10 values, n=3)', '06_safety.py', 'panel printed "16 h"; treated as 72 h (Q7)' if pk == 'c72' else '')
for gene in ['Tnf', 'Il6', 'Il10']:
    a = tidy.vec(f'S09-A[X:AS] {gene}', 'PSLN-344'); y = tidy.vec(f'S09-A[X:AS] {gene}', 'PSLN-212(y)')
    reg(f'c72_{gene.lower()}_p', pfmt(stats.ttest_ind(a, y).pvalue), f'Student t p (log10 scale), {gene}, aged PSLN-344 vs young PSLN-212, second S09-A panel', [f'S09-A[X:AS] {gene}'], "Student's t on log10 values (n=3 v 3), unadjusted", '06_safety.py', 'Q7')
for gene in ['Ifnb1', 'Tnf', 'Isg15']:
    b = f'S10-A {gene}'; gsx = tidy.groups(b); vals = [tidy.vec(b, g) for g in gsx]; rr = stats.tukey_hsd(*vals); cc = rr.confidence_interval(); i, j = gsx.index('PSLN-344'), gsx.index('Sham')
    for g, gk in [('PBS', 'pbs'), ('Sham', 'sham'), ('PSLN-344', 'a344'), ('CT', 'ct')]:
        regmean(f'cns_{gene.lower()}_{gk}', b, g, fmt='{:.2f}')
    reg(f'cns_{gene.lower()}_diff', f"{rr.statistic[i,j]:+.2f}", f'CNS {gene}: PSLN-344 − Sham difference in fold', [b], 'one-way ANOVA + Tukey HSD (4 groups, n=5)', '06_safety.py')
    reg(f'cns_{gene.lower()}_ci', f"{cc.low[i,j]:+.2f} to {cc.high[i,j]:+.2f}", 'Tukey 95% CI of the above', [b], 'Tukey HSD', '06_safety.py')
    reg(f'cns_{gene.lower()}_p', pfmt(rr.pvalue[i, j]), 'Tukey p of the above', [b], 'Tukey HSD', '06_safety.py')
reg('cns_tnf_vs_pbs_p', pfmt(stats.ttest_ind(tidy.vec('S10-A Tnf', 'PSLN-344'), tidy.vec('S10-A Tnf', 'PBS')).pvalue), 'Unadjusted Student t p, CNS Tnf, PSLN-344 vs PBS', ['S10-A Tnf'], "Student's t (n=5 v 5), unadjusted", '06_safety.py')
for g, gk in [('PSLN-344', 'a344'), ('PSLN-212', 'a212'), ('CMP-204', 'cmp'), ('PSLN-212/R848', 'r848'), ('PSLN-R848', 'r848only')]:
    regmean(f'ee_{gk}', 'S08-B', g)
reg('ee_p', pfmt(tuk('S08-B', 'PSLN-344', 'PSLN-212')), 'Tukey p, encapsulation efficiency PSLN-344 vs PSLN-212', ['S08-B'], 'one-way ANOVA + Tukey (5 preparations, n=3)', '04_immunology_stats.py')
reg('ee_344_range', f"{tidy.vec('S08-B','PSLN-344').min():.0f}–{tidy.vec('S08-B','PSLN-344').max():.0f}%", 'Range of encapsulation efficiency, PSLN-344 (3 preparations)', ['S08-B'], 'min–max', '10_numbers.py')
# morbidity
M11 = pd.read_csv('../tables/T11_morbidity_bodyweight.csv'); sel = M11[M11.bw_block.isin(['S15-A', 'S15-B', 'S15-C', 'S15-D', 'S15-E', 'S15-F', 'S15-G'])]
bwb = ['S15-A', 'S15-B', 'S15-C', 'S15-D', 'S15-E', 'S15-F', 'S15-G']
for g, gk in [('PSLN-344', 'a344'), ('PSLN-212', 'a212'), ('PSLN-212(Y)', 'y212')]:
    v = sel[sel.group == g].mean_max_loss_pct
    reg(f'morb_{gk}', f"{v.mean():.0f}%", f'Mean maximum weight loss after challenge, {g}, averaged over the 7 aged-BALB/c challenge blocks', bwb, 'per-animal nadir → block mean → mean of 7 blocks (supportive only: body-weight blocks carry flag Q4)', '07_morbidity_and_factorial.py', 'Q4')
    reg(f'morb_{gk}_range', f"{v.min():.0f}–{v.max():.0f}%", 'Range across the 7 blocks', bwb, 'as above', '07_morbidity_and_factorial.py', 'Q4')
# power
P12 = pd.read_csv('../tables/T12_power_survival.csv')
reg('pw_main_n12', f"{P12.iloc[0]['n=12']:.2f}", 'Power, Fisher exact, 86% vs 14% survival, n=12/arm', ROB, 'exact power of two-sided Fisher test, α=0.05', '08_power.py')
reg('pw_main_n15', f"{P12.iloc[0]['n=15']:.2f}", 'Power, 86% vs 14%, n=15/arm', ROB, 'as above', '08_power.py')
reg('pw_alt_n15', f"{P12.iloc[2]['n=15']:.2f}", 'Power, 86% vs 43% (if PSLN-212 truly protects 3/7), n=15/arm', ROB + ['S13-F'], 'as above', '08_power.py')
reg('pw_alt_n30', f"{P12.iloc[2]['n=30']:.2f}", 'Power, 86% vs 43%, n=30/arm', ROB + ['S13-F'], 'as above', '08_power.py')
reg('pw_cmp50_n15', f"{P12.iloc[4]['n=15']:.2f}", 'Power, 86% vs an assumed 50% for an active comparator, n=15/arm', ROB, 'as above; comparator rate is an assumption, not data', '08_power.py')
reg('pw_cmp50_n30', f"{P12.iloc[4]['n=30']:.2f}", 'Power, 86% vs assumed 50%, n=30/arm', ROB, 'as above', '08_power.py')
reg('pw_d60_n20', f"{P12.iloc[3]['n=20']:.2f}", 'Power, 67% vs 5% at d60, n=20/arm', D60, 'as above', '08_power.py')
reg('sd_hai', '0.68', 'Pooled within-group SD of log2 HAI titre (adjuvanted groups)', ['S03-C', 'S03-G'], 'root mean within-group variance, larger of the two strains', '08_power.py')
reg('sd_nab', '0.98', 'Pooled within-group SD of log2 neutralising titre', ['S03-D', 'S03-H'], 'as above', '08_power.py')
reg('n_hai_2fold', '11', 'n/arm to detect a 2-fold HAI GMT difference, 90% power', ['S03-C', 'S03-G'], 'two-sample t on log2 titres, α=0.05 two-sided', '08_power.py')
reg('n_nab_2fold', '22', 'n/arm to detect a 2-fold neutralising GMT difference, 90% power', ['S03-D', 'S03-H'], 'as above', '08_power.py')
reg('sd_nadir', '1.55', 'Pooled SD of per-animal body-weight nadir (points)', ['S08-D'], 'root mean within-group variance (5 non-R848 groups)', '08_power.py')
reg('n_nadir_2pt', '14', 'n/arm to detect a 2-point difference in nadir, 90% power', ['S08-D'], 'two-sample t, α=0.05', '08_power.py')
reg('mdd_nadir_n5', '3.5', 'Smallest nadir difference detectable with 80% power at the n=5 actually used (points)', ['S08-D'], 'two-sample t, α=0.05', '08_power.py')
# QC counts
QC = pd.read_csv('../tables/QC_survival_vs_bodyweight.csv')
reg('qc_bw_consistent', f"{int((QC.consistent.astype(str) == 'True').sum())}", 'Group-level comparisons where the body-weight block implies the same number of losses as the time-to-event block', sorted(set(QC.bw_block)), 'animals leaving the weight record (blank cells or constant tail) vs deaths in the paired survival block', '02b_qc_surv_bw.py')
reg('qc_bw_total', f"{int(QC.consistent.notna().sum())}", 'Group-level comparisons possible', sorted(set(QC.bw_block)), 'count', '02b_qc_surv_bw.py')
a = tidy.get('S11-A').sort_values(['group', 'x', 'rep']).value.values; b2 = tidy.get('S11-B').sort_values(['group', 'x', 'rep']).value.values
reg('qc_s11_same', f"{int(np.isclose(a, b2).sum())}", 'Values identical at the same position in S11-A and S11-B (of 100)', ['S11-A', 'S11-B'], 'position-wise comparison', '02c_qc_duplicates.py')
c = tidy.get('S15-C'); c = c[(c.group == 'PSLN-344') & (c.x > 0)].sort_values(['x', 'rep']).value.values; i2 = tidy.get('S15-I'); i2 = i2[(i2.group == '3d Vaccine+PSLN-344') & (i2.x > 0)].sort_values(['x', 'rep']).value.values
reg('qc_s15ci_same', f"{int(np.isclose(c, i2).sum())}", 'Values identical at the same animal/day position, S15-C PSLN-344 vs S15-I Vaccine+PSLN-344 (of 49)', ['S15-C', 'S15-I'], 'position-wise comparison, day-0 values excluded', '02c_qc_duplicates.py')

# ---------------------------------------------------------------------------------------------- extra numbers used in the text
reg('ifnb16_212_vs_cmp', f"{mean('S01-A 16h','PSLN-212')/mean('S01-A 16h','CMP-204'):.1f}", 'Ifnb1 16 h, ratio PSLN-212 / CMP-204 (aged)', ['S01-A 16h'], 'ratio of means; Tukey p = ' + pfmt(tuk('S01-A 16h', 'PSLN-212', 'CMP-204')), '04_immunology_stats.py')
reg('ifnb16_212_vs_cmp_p', pfmt(tuk('S01-A 16h', 'PSLN-212', 'CMP-204')), 'Tukey p, Ifnb1 16 h, PSLN-212 vs CMP-204', ['S01-A 16h'], 'one-way ANOVA + Tukey HSD (8 groups)', '04_immunology_stats.py')
def tails(block, group):
    d = tidy.get(block); out = []
    for rep, t in d[d.group == group].groupby('rep'):
        v = t.sort_values('x').value.values
        if len(v) == 8 and v[-1] == v[-2] and v[-1] < 99: out.append(v[-1])
    return out
t344 = sum([tails(b, 'PSLN-344') for b in ['S15-E', 'S15-F', 'S15-G']], []); tun = sum([tails(b, 'Untreated') for b in ['S15-E', 'S15-F', 'S15-G']], [])
reg('d60_344_lastwt', f"{min(t344):.1f}–{max(t344):.1f}%", f'Last recorded body weight of the {len(t344)} PSLN-344 animals whose weight record flat-lines after the day-60 challenges', ['S15-E', 'S15-F', 'S15-G'], 'constant-tail (last observation carried forward) detection', '02b_qc_surv_bw.py', 'Q5, Q14')
reg('d60_344_lastwt_n', f"{len(t344)}", 'Number of PSLN-344 animals with a flat-lined weight record after day-60 challenge (time-to-event tables record 7 deaths)', ['S15-E', 'S15-F', 'S15-G'], 'count', '02b_qc_surv_bw.py', 'Q14')
reg('d60_unt_lastwt', f"{min(tun):.1f}–{max(tun):.1f}%", f'Last recorded body weight of the {len(tun)} untreated, unchallenged animals whose weight record flat-lines', ['S15-E', 'S15-F', 'S15-G'], 'as above', '02b_qc_surv_bw.py')
reg('d60_unt_lastwt_n', f"{len(tun)}", 'Number of untreated animals with a flat-lined weight record', ['S15-E', 'S15-F', 'S15-G'], 'count', '02b_qc_surv_bw.py')
k_, n_ = surv(['S03-J', 'S06-B'], 'PSLN-344'); k2_, n2_ = surv(['S15-H'], '3d Vaccine+PSLN-344')
reg('early_344_cons', f"{k_ + k2_ + 5}/{n_ + n2_ + 7}", 'Early-challenge survival if S06-D is replaced by what its body-weight block S15-D implies (5/7)', ['S03-J', 'S06-B', 'S15-H', 'S15-D'], 'sensitivity analysis', '10_numbers.py', 'Q4')
reg('fx_p_max', pfmt(max(fact(b, x)[2] for b, x in [('S01-A 16h', None), ('S01-E', 4), ('S01-F', None), ('S02-C', None), ('S02-E', None)])), 'Largest age × Mn²⁺ interaction p across the five read-outs that have all four groups', ['S01-A 16h', 'S01-E', 'S01-F', 'S02-C', 'S02-E'], 'two-way ANOVA on log2 values', '07_morbidity_and_factorial.py')
B13 = pd.read_csv('../tables/T13_biomarker_separation.csv')
reg('bm_sep', f"{int(B13.complete_separation.sum())}", 'Candidate biomarkers (of 27) whose values do not overlap between aged PSLN-344 and aged PSLN-212 animals', sorted(set(b.split(' (')[0] for b in B13.block)), 'min of one group vs max of the other', '04c_biomarker_separation.py')
reg('bm_n', f"{len(B13)}", 'Candidate biomarkers examined', sorted(set(b.split(' (')[0] for b in B13.block)), 'count', '04c_biomarker_separation.py')
def rng(b0, g, x=None):
    v = tidy.vec(b0, g, x); f = (lambda u: f"{u:,.0f}") if v.max() >= 100 else ((lambda u: f"{u:.0f}") if np.allclose(v, np.round(v)) else (lambda u: f"{u:.1f}"))
    return f"{f(v.min())}–{f(v.max())}"
for b, key in [('S01-A 16h', 'ifnb'), ('S02-F (x=36)', 'gmcsf36'), ('S02-A', 'ccr7'), ('S01-D (x=4)', 'mono4'), ('S03-C', 'hai_h1'), ('S03-G', 'hai_h3'), ('S13-A', 'igg2a'), ('S05-F', 'ifng'), ('S05-I', 'trm'), ('S05-E', 'gzmb3'), ('S02-C', 'ova')]:
    r_ = B13[B13.block == b].iloc[0]
    xx0 = float(re.search(r'x=([0-9.]+)', b).group(1)) if '(x=' in b else None
    reg(f'bm_{key}_r212', rng(b.split(' (')[0], 'PSLN-212', xx0), f"Range of individual values, aged PSLN-212, {r_['biomarker']}", [b.split(' (')[0]], 'min–max', '04c_biomarker_separation.py')
    reg(f'bm_{key}_r344', rng(b.split(' (')[0], 'PSLN-344', xx0), f"Range of individual values, aged PSLN-344, {r_['biomarker']}", [b.split(' (')[0]], 'min–max', '04c_biomarker_separation.py')
    reg(f'bm_{key}_cut', f"{r_['candidate_cutoff']:.3g}", f"Candidate cut-off (geometric midpoint of the gap), {r_['biomarker']}", [b.split(' (')[0]], 'sqrt(min of higher group × max of lower group)', '04c_biomarker_separation.py')
reg('n_cells', '6,819', 'Numeric cells in the workbook', [], 'count of numeric cells over 15 sheets', '00_coverage_check.py')
reg('n_unmapped', '26', 'Numeric cells not belonging to any labelled block (S08 rows 89–101)', [], 'coverage check', '00_coverage_check.py')
reg('n_obs', f"{len(T):,}", 'Observations parsed into the tidy data set', [], 'count', '01_export_tidy.py')
reg('n_blocks', f"{T.block.nunique()}", 'Blocks (including sub-panels) parsed', [], 'count', '01_export_tidy.py')

from importlib import import_module
PWR = import_module('08_power') if False else None
def fisher_power(p1, p0, n, alpha=0.05):
    pw = 0.0
    for a in range(n + 1):
        pa = stats.binom.pmf(a, n, p1)
        for c in range(n + 1):
            pc = stats.binom.pmf(c, n, p0)
            if pa * pc > 1e-14 and stats.fisher_exact([[a, n - a], [c, n - c]])[1] <= alpha: pw += pa * pc
    return pw
reg('pw16_main', f"{100*fisher_power(18/21, 3/21, 16):.0f}%", 'Power at n=16/arm for the survival difference seen in the unflagged blocks (18/21 vs 3/21)', ROB, 'exact power, two-sided Fisher test, α = 0.05', '10_numbers.py')
reg('pw16_alt', f"{100*fisher_power(18/21, 3/7, 16):.0f}%", 'Power at n=16/arm if PSLN-212 truly protects 3 of 7 (as the S13-F traces imply)', ROB + ['S13-F'], 'as above', '10_numbers.py')
reg('pw16_cmp', f"{100*fisher_power(18/21, 0.5, 16):.0f}%", 'Power at n=16/arm against an active comparator assumed to protect 50% (assumption, no data)', ROB, 'as above', '10_numbers.py')
reg('pw20_d60', f"{100*fisher_power(14/21, 1/21, 20):.0f}%", 'Power at n=20/arm for the day-60 difference (14/21 vs 1/21)', D60, 'as above', '10_numbers.py')
reg('pw20_wane', f"{100*fisher_power(14/21, 42/45, 20):.0f}%", 'Power at n=20/arm to distinguish day-60 survival (67%) from early survival (93%)', D60 + ACUTE, 'as above', '10_numbers.py')
reg('pw40_wane', f"{100*fisher_power(14/21, 42/45, 40):.0f}%", 'Power at n=40/arm to distinguish 67% from 93%', D60 + ACUTE, 'as above', '10_numbers.py')
QL = pd.read_csv('../tables/QC_log.csv')
reg('qc_n', f"{len(QL)}", 'Data-integrity items logged', [], 'count of QC log entries', '02e_qc_log.py')
reg('qc_high', f"{int((QL.severity == 'High').sum())}", 'Items rated high severity (change or remove a number the case relies on)', [], 'count', '02e_qc_log.py')
for key, b in [('h1', 'S13-I'), ('h3', 'S13-J')]:
    reg(f'igg28_{key}_young_over_212', f"{gmt(b,'PSLN-212(Y)')/gmt(b,'PSLN-212'):.0f}", f'IgG GMT after boost: young PSLN-212 ÷ aged PSLN-212, {b}', [b], 'ratio of geometric means', '10_numbers.py')
    reg(f'igg28_{key}_344_pct_young', f"{100*gmt(b,'PSLN-344')/gmt(b,'PSLN-212(Y)'):.0f}%", f'IgG GMT after boost: aged PSLN-344 as % of young PSLN-212, {b}', [b], 'ratio of geometric means', '10_numbers.py')
reg('ly6c_p5', pfmt(tuk('S07-A', 'PSLN-212', 'PSLN-344', 5.0)), 'Student t p, Ly6C+CCR2+ macrophages day 5, PSLN-212 vs PSLN-344', ['S07-A'], "Student's t within day (n=3 v 3)", '04_immunology_stats.py')
reg('cd40_p_young', pfmt(tuk('S02-D CD40', 'PSLN-344', 'PSLN-212(Y)')), 'Tukey p, CD40+ DC, aged PSLN-344 vs young PSLN-212', ['S02-D CD40'], 'one-way ANOVA + Tukey', '04_immunology_stats.py')
reg('tfr30_p_sham', pfmt(tuk('S04-C', 'PSLN-344', 'Sham')), 'Tukey p, Tfr day 30, PSLN-344 vs sham', ['S04-C'], 'one-way ANOVA + Tukey', '04_immunology_stats.py')
reg('gmrescue_p', pfmt(tuk('S02-G', 'PSLN-212+GM-CSF', 'PSLN-212')), 'Tukey p, moDC, PSLN-212 + GM-CSF vs PSLN-212', ['S02-G'], 'one-way ANOVA + Tukey (3 groups)', '04_immunology_stats.py')
reg('otiv_p_mln', pfmt(tuk('S05-C', 'MLN+PTX', 'MLN')), 'Tukey p, OT-I proliferation in node ± pertussis toxin', ['S05-C'], 'one-way ANOVA + Tukey (4 groups, n=3)', '04_immunology_stats.py')
reg('otiv_p_lung', pfmt(tuk('S05-C', 'Lung+PTX', 'Lung')), 'Tukey p, OT-I proliferation in lung ± pertussis toxin', ['S05-C'], 'one-way ANOVA + Tukey (4 groups, n=3)', '04_immunology_stats.py')

for b, key in [('S02-F (x=16)', 'gmcsf16'), ('S02-F (x=36)', 'gmcsf36'), ('S13-A', 'igg2a'), ('S03-C', 'hai_h1')]:
    r_ = B13[B13.block == b].iloc[0]
    reg(f'bm_{key}_margin', f"{r_['separation_margin_fold']:.1f}", f"Lowest PSLN-344 value ÷ highest PSLN-212 value, {r_['biomarker']}", [b.split(' (')[0]], 'min of one group ÷ max of the other', '04c_biomarker_separation.py')

# ---------------------------------------------------------------------------------------------- numbers for the tables in the text
def f3(v):
    return f"{v:,.0f}" if abs(v) >= 100 else (f"{v:.1f}" if abs(v) >= 10 else f"{v:.2g}" if abs(v) < 1 else f"{v:.1f}")
IMM = [('ifnb', 'Lung Ifnb1 mRNA at 16 h (fold)', 'S01-A 16h', None, 'mean'), ('gmcsf', 'Lung Gm-csf mRNA at 36 h (fold)', 'S02-F', 36.0, 'mean'), ('mono', 'Lung monocytes, day 4 (%)', 'S01-D', 4.0, 'mean'),
       ('ccr7', 'CCR7⁺ lung dendritic cells, 72 h (%)', 'S02-A', None, 'mean'), ('ova', 'Antigen-carrying dendritic cells in node, 36 h (%)', 'S02-C', None, 'mean'),
       ('gcb', 'Germinal-centre B cells, day 7 (%)', 'S03-K', None, 'mean'), ('tfr', 'Follicular regulatory T cells, day 7 (%)', 'S04-B Foxp3', None, 'mean'),
       ('haih1', 'HAI titre, H1N1, day 14 (GMT)', 'S03-C', None, 'gmt'), ('haih3', 'HAI titre, H3N2, day 14 (GMT)', 'S03-G', None, 'gmt'), ('nabh1', 'Neutralising titre, H1N1, day 14 (GMT)', 'S03-D', None, 'gmt'),
       ('nabh3', 'Neutralising titre, H3N2, day 14 (GMT)', 'S03-H', None, 'gmt'), ('iggh1', 'IgG titre, H1N1, day 14 (GMT)', 'S03-A', None, 'gmt'),
       ('gzmb', 'Granzyme-B⁺ lung CD8 T cells, day 3 (%)', 'S05-E', None, 'mean'), ('ifng', 'Interferon-γ⁺ CD8 T cells after H5N1 restimulation, day 14 (%)', 'S05-F', None, 'mean'),
       ('ifng60', 'Interferon-γ⁺ CD8 T cells, day 60 (%)', 'S05-G', None, 'mean'), ('trm', 'Resident-memory CD8 T cells in lung, day 25 (%)', 'S05-I', None, 'mean')]
imm_spec = []
for key, lab, b, x, kind in IMM:
    gsx = tidy.groups(b); val = (lambda g: gmt(b, g)) if kind == 'gmt' else (lambda g: mean(b, g, x))
    row = dict(key=key, label=lab, block=b)
    for g, gk in [('Sham', 'sham'), ('PSLN-212', 'a212'), ('PSLN-344', 'a344'), ('PSLN-212(Y)', 'y212')]:
        if g in gsx and len(tidy.vec(b, g, x)):
            reg(f'imm_{key}_{gk}', f3(val(g)), f'{lab}: {g}', [b], (M_GMT if kind == 'gmt' else M_MEAN) + f' (n={len(tidy.vec(b, g, x))})', '04_immunology_stats.py')
    reg(f'imm_{key}_fold', f"{val('PSLN-344')/val('PSLN-212'):.1f}" if val('PSLN-344') >= val('PSLN-212') else f"{val('PSLN-344')/val('PSLN-212'):.2f}", f'{lab}: PSLN-344 ÷ PSLN-212 (aged)', [b], 'ratio of ' + ('geometric means' if kind == 'gmt' else 'means'), '04b_restoration.py')
    reg(f'imm_{key}_p', pfmt(tuk(b, 'PSLN-344', 'PSLN-212', x, 'p_log' if kind == 'gmt' else 'p')), f'{lab}: Tukey p, PSLN-344 vs PSLN-212 (aged)', [b], 'Tukey HSD' + (' on log2 titres' if kind == 'gmt' else '') + (' within time point' if x is not None else ''), '04_immunology_stats.py')
    imm_spec.append(row)
json.dump(imm_spec, open('_imm_table_spec.json', 'w'), ensure_ascii=False)
BMT = [('Target engagement (hours)', 'ifnb', 'S01-A 16h', 'Lung Ifnb1 mRNA, 16 h (fold)', 'Interferon-induced genes or CXCL10 in blood or nasal fluid (to be bridged in Study 1)'),
       ('Target engagement (hours)', 'gmcsf36', 'S02-F (x=36)', 'Lung Gm-csf mRNA, 36 h (fold)', 'GM-CSF protein in nasal fluid or serum (to be bridged)'),
       ('Mechanism (days)', 'mono4', 'S01-D (x=4)', 'Lung monocytes, day 4 (%)', 'Blood monocyte subsets; nasal or sputum cells'),
       ('Mechanism (days)', 'ccr7', 'S02-A', 'CCR7⁺ lung dendritic cells, 72 h (%)', 'Not routinely accessible'),
       ('Mechanism (days)', 'ova', 'S02-C', 'Antigen-carrying dendritic cells in node, 36 h (%)', 'Not accessible'),
       ('Response (weeks)', 'hai_h1', 'S03-C', 'HAI titre, H1N1, day 14', 'HAI titre (standard immunogenicity endpoint)'),
       ('Response (weeks)', 'hai_h3', 'S03-G', 'HAI titre, H3N2, day 14', 'HAI titre'),
       ('Response (weeks)', 'igg2a', 'S13-A', 'IgG2a titre, H1N1, day 14', 'IgG subclass profile'),
       ('Response (weeks)', 'gzmb3', 'S05-E', 'Granzyme-B⁺ lung CD8 T cells, day 3 (%)', 'Activated CD8 T cells in blood, about day 7'),
       ('Response (weeks)', 'ifng', 'S05-F', 'Interferon-γ⁺ CD8 T cells after H5N1 restimulation (%)', 'Interferon-γ ELISpot to conserved influenza proteins'),
       ('Response (weeks)', 'trm', 'S05-I', 'Resident-memory CD8 T cells in lung, day 25 (%)', 'Bronchial or nasal sampling in a sub-study only')]
bm_spec = []
for stage, key, b, lab, human in BMT:
    r_ = B13[B13.block == b].iloc[0]; b0 = b.split(' (')[0]
    xx_ = float(re.search(r'x=([0-9.]+)', b).group(1)) if '(x=' in b else None
    is_t = b0 in ('S03-C', 'S03-G', 'S13-A'); mth = M_GMT if is_t else M_MEAN
    v212 = gmt(b0, 'PSLN-212') if is_t else r_['mean_aged212']; v344 = gmt(b0, 'PSLN-344') if is_t else r_['mean_aged344']
    vy = (gmt(b0, 'PSLN-212(Y)') if is_t else r_['mean_young212'])
    reg(f'bmt_{key}_m212', f3(v212), f'{lab}: {"GMT" if is_t else "mean"}, aged PSLN-212', [b0], mth, '04c_biomarker_separation.py')
    reg(f'bmt_{key}_m344', f3(v344), f'{lab}: {"GMT" if is_t else "mean"}, aged PSLN-344', [b0], mth, '04c_biomarker_separation.py')
    if not np.isnan(vy):
        reg(f'bmt_{key}_y', f3(vy), f'{lab}: {"GMT" if is_t else "mean"}, young PSLN-212', [b0], mth, '04c_biomarker_separation.py')
    if f'bm_{key}_r212' not in N:
        reg(f'bm_{key}_r212', rng(b0, 'PSLN-212', xx_), f"Range of individual values, aged PSLN-212, {lab}", [b0], 'min–max', '04c_biomarker_separation.py')
        reg(f'bm_{key}_r344', rng(b0, 'PSLN-344', xx_), f"Range of individual values, aged PSLN-344, {lab}", [b0], 'min–max', '04c_biomarker_separation.py')
    reg(f'bmt_{key}_sep', 'none' if r_['complete_separation'] else 'yes', f'{lab}: overlap between aged PSLN-344 and aged PSLN-212 animals', [b.split(' (')[0]], 'min of one group vs max of the other', '04c_biomarker_separation.py')
    bm_spec.append(dict(stage=stage, key=key, block=b, label=lab, human=human))
json.dump(bm_spec, open('_bm_table_spec.json', 'w'), ensure_ascii=False)

def deaths(blocks, g):
    k, n_ = surv(blocks, g); return n_ - k, n_
d_e, n_e = deaths(ROB, 'PSLN-344'); d_a, n_a = deaths(ACUTE, 'PSLN-344'); d_l, n_l = deaths(D60, 'PSLN-344')
reg('wane_p_core', pfmt(stats.fisher_exact([[d_e, n_e - d_e], [d_l, n_l - d_l]])[1]), 'Fisher exact p, PSLN-344 deaths: core early-challenge experiments vs day-60 experiments', ROB + D60, 'Fisher exact, two-sided', '03b_survival_pooled.py')
reg('wane_p_printed', pfmt(stats.fisher_exact([[d_a, n_a - d_a], [d_l, n_l - d_l]])[1]), 'Fisher exact p, PSLN-344 deaths: all six early-challenge experiments as printed vs day-60 experiments', ACUTE + D60, 'Fisher exact, two-sided', '03b_survival_pooled.py')

json.dump(N, open('../tables/numbers.json', 'w'), indent=1, ensure_ascii=False)
LED = pd.DataFrame(L); LED.insert(0, 'id', [f'E{i+1:03d}' for i in range(len(LED))])
LED.to_csv('../tables/T0_evidence_ledger.csv', index=False)
print(len(LED), 'ledger entries')
