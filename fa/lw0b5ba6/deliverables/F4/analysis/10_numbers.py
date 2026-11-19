#!/usr/bin/env python
"""
10_numbers.py -- registry of every number quoted in the proposal.
Each entry: key, value (as printed in the proposal), source block(s), analysis table / script that produces it.
Run: micromamba run -n core python 10_numbers.py      (after scripts 01-07)
Output: tables/T10_numbers_cited.csv  and  tables/T10_numbers_cited.json (read by 11_build_proposal.py)
"""
import os, json, numpy as np, pandas as pd
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(HERE, 'tables'); P = os.path.join(HERE, 'parsed')
rd = lambda f, **k: pd.read_csv(os.path.join(T, f), **k)
D = rd('T05_endpoint_descriptives.csv', keep_default_na=False); D['level'] = D.level.astype(str)
C = rd('T06_endpoint_contrasts.csv', keep_default_na=False, na_values=['']); C['level'] = C.level.fillna('').astype(str)
S2 = rd('T02_survival_by_group.csv'); S3 = rd('T03_survival_contrasts.csv'); S4 = rd('T04_survival_pooled.csv'); S4b = rd('T04b_survival_extra.csv'); S4c = rd('T04c_survival_sensitivity.csv')
R = rd('T07_restoration_index_curated.csv'); DR = rd('T08e_S08A_dose_response.csv').set_index('group')
W = rd('T08a_S08D_postvaccination_weight.csv').set_index('group'); WT = rd('T08a2_S08D_tukey_nadir.csv')
CY = rd('T08b_S09A_cytokines.csv'); CNS = rd('T08d_S10A_CNS.csv'); PW = rd('T11_power.csv')
IV = rd('T01d_integrity_survival_vs_weight.csv'); TR = rd('T01f_integrity_weight_trajectory_reuse.csv'); FRc = rd('T01g_integrity_weight_fraction_reuse.csv')
S11 = rd('T01c_integrity_S11A_vs_S11B.csv'); Y = rd('T09b_young_344_vs_212.csv', keep_default_na=False); Y['level'] = Y.level.astype(str)
NAD = rd('T09a_postchallenge_nadir_survivors.csv')
N = {}; REG = []
def put(key, value, source, analysis, note=''):
    N[key] = value; REG.append(dict(key=key, value=value, source_blocks=source, analysis=analysis, note=note))
def mean(block, group, level=''):
    return float(D[(D.block == block) & (D.group == group) & (D.level == str(level))]['mean'].iloc[0])
def gm(block, group, level=''):
    return float(D[(D.block == block) & (D.group == group) & (D.level == str(level))].centre_on_analysis_scale.iloc[0])
def sd(block, group, level=''):
    return float(D[(D.block == block) & (D.group == group) & (D.level == str(level))]['sd'].iloc[0])
def con(block, a, b, level='', col='p_welch_t'):
    x = C[(C.block == block) & (C.level == str(level)) & (((C.group_a == a) & (C.group_b == b)) | ((C.group_a == b) & (C.group_b == a)))]
    return float(x[col].iloc[0])
def fmt_p(p):
    """p-value with its operator, as printed in the proposal ('= 0.003', '< 0.0001'); exact values stay in the T tables"""
    if p < 1e-4: return '< 0.0001'
    if p < 0.001: return f'= {p:.4f}'
    if p < 0.01: return f'= {p:.3f}'
    return f'= {p:.2f}' if p >= 0.095 else (f'= {p:.3f}' if round(p, 3) != round(p, 2) else f'= {p:.2f}')
def pooled(analysis_prefix, test, ref):
    x = S4[S4.analysis.str.startswith(analysis_prefix) & (S4.test_group == test) & (S4.ref_group == ref)]
    assert len(x) == 1, (analysis_prefix, test, ref, len(x)); return x.iloc[0]
def sg(block, group):
    r = S2[(S2.block == block) & (S2.group == group)].iloc[0]; return f'{int(r.survivors)}/{int(r.n_rows)}'

# ------------------------------------------------------------------ survival
a = pooled('Aged BALB/c, single dose', 'PSLN-344', 'PSLN-212'); b = pooled('Aged BALB/c, single dose', 'PSLN-344', 'Sham')
src = 'S03-I S03-J S06-A S06-B S06-C S06-D'
put('early_344', a.surv_test, src, 'T04 (04_survival.py)'); put('early_344_pct', f'{a.surv_test_pct:.0f}', src, 'T04'); put('early_344_ci', '–'.join(f'{float(v):.0f}' for v in a.test_ci95.split('-')), src, 'T04 exact Clopper-Pearson')
put('early_212', a.surv_ref, src, 'T04'); put('early_212_pct', f'{a.surv_ref_pct:.0f}', src, 'T04'); put('early_sham', b.surv_ref, src, 'T04'); put('early_sham_pct', f'{b.surv_ref_pct:.0f}', src, 'T04')
put('early_p_212', fmt_p(a.p_stratified_logrank), src, 'T04 log-rank stratified by experiment'); put('early_p_sham', fmt_p(b.p_stratified_logrank), src, 'T04')
put('early_rd_212', f'{a.MH_risk_diff_pct:.0f}', src, 'T04 Mantel-Haenszel risk difference'); put('early_rd_212_ci', a.MH_rd_ci95.replace(' to ', '–'), src, 'T04')
w = S4c.iloc[1]; put('worst_344', w.PSLN344, src + ' + S13-F S13-G S15-D', 'T04c sensitivity'); put('worst_344_pct', f'{w.PSLN344_pct:.0f}', src, 'T04c'); put('worst_212', w.PSLN212, src, 'T04c'); put('worst_212_pct', f'{w.PSLN212_pct:.0f}', src, 'T04c')
put('worst_p', fmt_p(w.p_fisher_344_vs_212), src, 'T04c Fisher exact')
x = pooled('Same, excluding S03-J', 'PSLN-344', 'PSLN-212'); x2 = pooled('Same, excluding S03-J', 'PSLN-344', 'Sham')
put('noJ_344', x.surv_test, 'S03-I S06-A..D', 'T04'); put('noJ_212', x.surv_ref, 'S03-I S06-A..D', 'T04'); put('noJ_sham', x2.surv_ref, 'S03-I S06-A..D', 'T04')
put('all_early_344', S4c.iloc[2].PSLN344, src + ' S15-H', 'T04c'); put('all_early_344_pct', f'{S4c.iloc[2].PSLN344_pct:.0f}', src + ' S15-H', 'T04c')
h = pooled('Aged BALB/c heterosubtypic only', 'PSLN-344', 'PSLN-212')
put('het_344', h.surv_test, 'S06-A..D', 'T04'); put('het_344_pct', f'{h.surv_test_pct:.0f}', 'S06-A..D', 'T04'); put('het_212', h.surv_ref, 'S06-A..D', 'T04')
d3 = pooled('Aged BALB/c heterosubtypic, challenge d3', 'PSLN-344', 'PSLN-212'); put('d3_344', d3.surv_test, 'S06-B S06-D', 'T04'); put('d3_212', d3.surv_ref, 'S06-B S06-D', 'T04')
for k, blk, g in [('h_combo', 'S15-H', '3d Vaccine+PSLN-344'), ('h_adj', 'S15-H', '3d PSLN-344'), ('h_vac', 'S15-H', '3d Vaccine'),
                  ('j_344', 'S03-J', 'PSLN-344'), ('j_sham', 'S03-J', 'Sham'), ('j_212', 'S03-J', 'PSLN-212'),
                  ('i_344', 'S03-I', 'PSLN-344'), ('i_sham', 'S03-I', 'Sham'), ('i_212', 'S03-I', 'PSLN-212'), ('i_cmp', 'S03-I', 'CMP-204'), ('i_y', 'S03-I', 'PSLN-212(Y)'),
                  ('a_344', 'S06-A', 'PSLN-344'), ('b_344', 'S06-B', 'PSLN-344'), ('c_344', 'S06-C', 'PSLN-344'), ('d_344', 'S06-D', 'PSLN-344'),
                  ('e_344', 'S06-E', 'PSLN-344'), ('f_344', 'S06-F', 'PSLN-344'), ('g_344', 'S06-G', 'PSLN-344'),
                  ('e_unt', 'S06-E', 'Untreated'), ('f_unt', 'S06-F', 'Untreated'), ('g_unt', 'S06-G', 'Untreated'),
                  ('l_344', 'S15-L', 'PSLN-344'), ('n_344', 'S15-N', 'PSLN-344'), ('l_y', 'S15-L', 'PSLN-212(Y)'),
                  ('imp_pr8_n212', 'S06-E(r71)', 'Naive+PSLN-212'), ('imp_pr8_i212', 'S06-E(r71)', 'Imprinting+PSLN-212'), ('imp_pr8_n344', 'S06-E(r71)', 'Naive+PSLN-344'), ('imp_pr8_i344', 'S06-E(r71)', 'Imprinting+PSLN-344'),
                  ('imp_per_n212', 'S06-F(r71)', 'Naive+PSLN-212'), ('imp_per_i212', 'S06-F(r71)', 'Imprinting+PSLN-212'), ('imp_per_n344', 'S06-F(r71)', 'Naive+PSLN-344'), ('imp_per_i344', 'S06-F(r71)', 'Imprinting+PSLN-344'),
                  ('yb_344', 'S09-B', 'PSLN-344Y'), ('yb_212', 'S09-B', 'PSLN-212Y'), ('yf_344', 'S09-F', 'PSLN-344Y'), ('yf_212', 'S09-F', 'PSLN-212Y'), ('yf_sham', 'S09-F', 'Sham'),
                  ('ye_cmp', 'S13-E', 'CMP-204(Y)'), ('ye_344', 'S13-E', 'PSLN-344(Y)'), ('ye_sham', 'S13-E', 'Sham')]:
    put(k, sg(blk, g), blk, 'T02 (04_survival.py)')
d = pooled('Aged BALB/c, challenge d60', 'PSLN-344', 'PSLN-212'); d_s = pooled('Aged BALB/c, challenge d60', 'PSLN-344', 'Sham'); d_u = pooled('Aged+344 challenged vs age-matched untreated', 'PSLN-344', 'Untreated')
d_y = pooled('Aged+344 vs young+212 benchmark, d60', 'PSLN-344', 'PSLN-212(Y)')
src60 = 'S06-E S06-F S06-G'
put('d60_344', d.surv_test, src60, 'T04'); put('d60_344_pct', f'{d.surv_test_pct:.0f}', src60, 'T04'); put('d60_344_ci', '–'.join(f'{float(v):.0f}' for v in d.test_ci95.split('-')), src60, 'T04'); put('d60_212', d.surv_ref, src60, 'T04'); put('d60_sham', d_s.surv_ref, src60, 'T04')
put('d60_p_212', fmt_p(d.p_stratified_logrank), src60, 'T04'); put('d60_unt', d_u.surv_ref, src60, 'T04'); put('d60_unt_pct', f'{d_u.surv_ref_pct:.0f}', src60, 'T04'); put('d60_y', d_y.surv_ref, src60, 'T04'); put('d60_p_y', fmt_p(d_y.p_stratified_logrank), src60, 'T04')
put('d60_p_unt', fmt_p(S4b.iloc[1].p_fisher), src60, 'T04b Fisher exact'); put('bg_deaths', S4b.iloc[2].a.replace(' deaths', ''), src60, 'T04b'); put('bg_ci', '–'.join(f'{float(v):.0f}' for v in S4b.iloc[2].b.replace('95% CI ', '').replace('%', '').split('-')) + '%', src60, 'T04b')
put('bg_pct', f"{100 * 4 / 21:.0f}", src60, 'T04b')
put('wane_p', fmt_p(S4b.iloc[0].p_fisher), 'S06-A..G', 'T04b Fisher exact (25/28 vs 14/21)')
yb = pooled('Aged+344 vs young+212 benchmark, d3-d14', 'PSLN-344', 'PSLN-212(Y)'); put('yb5_344', yb.surv_test, 'S03-I S06-A..D', 'T04'); put('yb5_y', yb.surv_ref, 'S03-I S06-A..D', 'T04')
st = pooled('Aged C57BL/6 + Swiss Webster', 'PSLN-344', 'PSLN-212'); st2 = pooled('Aged C57BL/6 + Swiss Webster', 'PSLN-344', 'Sham')
put('str_344', st.surv_test, 'S15-L S15-N', 'T04'); put('str_212', st.surv_ref, 'S15-L S15-N', 'T04'); put('str_sham', st2.surv_ref, 'S15-L S15-N', 'T04')
im = pooled('14-mo BALB/c', 'PSLN-344', 'PSLN-212'); put('imp_344', im.surv_test, 'S06-E(r71) S06-F(r71)', 'T04'); put('imp_212', im.surv_ref, 'S06-E(r71) S06-F(r71)', 'T04'); put('imp_p', fmt_p(im.p_stratified_logrank), 'S06-E(r71) S06-F(r71)', 'T04')
x = S3[(S3.test_group == 'PSLN-344') & (S3.ref_group == 'Sham')]; put('n_expt_sham', str(len(x)), 'S03-I/J S06-A..G S15-L/N', 'T03'); put('max_p_sham', f'{x.p_logrank_permutation.max():.3f}', 'same', 'T03 exact permutation log-rank (largest of the 11 p-values)')
x = S3[(S3.test_group == 'PSLN-344') & (S3.ref_group == 'PSLN-212')]; put('n_expt_212_sig', str(int((x.p_logrank_permutation < 0.05).sum())), 'same', 'T03'); put('n_expt_212', str(len(x)), 'same', 'T03')
put('p_212_ns', fmt_p(x.p_logrank_permutation.max()), 'S15-N', 'T03')

# ------------------------------------------------------------------ immunology (restoration)
x = R[~R.step.str.startswith('6')]
put('n_endpoints', str(len(x)), 'see T07', 'T07 (05b_curated_restoration.py)'); put('n_sig', str(int((x.p_mwu_344_vs_212 < 0.05).sum())), 'see T07', 'T07 exact Mann-Whitney'); put('n_sep', str(int(x.all_344_above_all_212.sum())), 'see T07', 'T07')
put('med_344', f'{x.aged344_pct_of_young.median():.0f}', 'see T07', 'T07'); put('med_212', f'{x.aged212_pct_of_young.median():.0f}', 'see T07', 'T07')
put('rng_344_lo', f'{x.aged344_pct_of_young.min():.0f}', 'see T07', 'T07'); put('rng_344_hi', f'{x.aged344_pct_of_young.max():.0f}', 'see T07', 'T07')
Rb = R.set_index('block')
def r(block, col): return float(Rb.loc[block, col])
for k, blk in [('hai1', 'S03-C'), ('hai3', 'S03-G'), ('igg1', 'S03-A'), ('igg3', 'S03-E'), ('nt1', 'S03-D'), ('nt3', 'S03-H')]:
    put(k + '_344', f"{r(blk, 'aged344'):,.0f}", blk, 'T07 geometric mean'); put(k + '_212', f"{r(blk, 'aged212'):,.0f}", blk, 'T07'); put(k + '_y', f"{r(blk, 'young212'):,.0f}", blk, 'T07')
    put(k + '_fold', f"{r(blk, 'fold_344_vs_212_aged'):.1f}", blk, 'T07'); put(k + '_pct', f"{r(blk, 'aged344_pct_of_young'):.0f}", blk, 'T07')
for k, blk in [('ratio1', 'S13-A/S13-B'), ('ratio3', 'S13-C/S13-D')]:
    put(k + '_344', f"{r(blk, 'aged344'):.1f}", blk.replace('/', ' '), 'T07 recomputed per animal'); put(k + '_212', f"{r(blk, 'aged212'):.1f}", blk.replace('/', ' '), 'T07'); put(k + '_y', f"{r(blk, 'young212'):.1f}", blk.replace('/', ' '), 'T07')
put('ratio1_printed_344', f"{mean('S03-B', 'PSLN-344'):.1f}", 'S03-B', 'T05 / T01a (as printed, not used)')
for k, blk in [('gcb', 'S03-K'), ('ifng14', 'S05-F'), ('ifng60', 'S05-G'), ('trm', 'S05-I'), ('cd40', 'S02-D CD40'), ('cd86', 'S02-D CD86'), ('ccr7', 'S02-A'), ('agdc', 'S02-C'), ('xprime', 'S02-E'),
               ('tfr7', 'S04-B Foxp3'), ('tfr30', 'S04-C'), ('treg', 'S04-D'), ('cd206', 'S11-E'), ('ki67', 'S05-D'), ('gzmb', 'S05-E'), ('tfh', 'S04-A'), ('iggb', 'S13-H'), ('cdc1', 'S01-F'), ('mlndc', 'S02-B')]:
    put(k + '_344', f"{r(blk, 'aged344'):.1f}", blk, 'T07 mean'); put(k + '_212', f"{r(blk, 'aged212'):.1f}", blk, 'T07'); put(k + '_y', f"{r(blk, 'young212'):.1f}", blk, 'T07')
    put(k + '_pct', f"{r(blk, 'aged344_pct_of_young'):.0f}", blk, 'T07'); put(k + '_fold', f"{r(blk, 'fold_344_vs_212_aged'):.1f}", blk, 'T07')
for k, blk in [('boost1', 'S13-I'), ('boost3', 'S13-J')]:
    put(k + '_344', f"{r(blk, 'aged344'):,.0f}", blk, 'T07 geometric mean'); put(k + '_pct', f"{r(blk, 'aged344_pct_of_young'):.0f}", blk, 'T07'); put(k + '_fold', f"{r(blk, 'fold_344_vs_212_aged'):.1f}", blk, 'T07')
put('tfr30_p', fmt_p(r('S04-C', 'p_welch_344_vs_212')), 'S04-C', 'T07 Welch t')
put('tfr7_p', fmt_p(r('S04-B Foxp3', 'p_welch_344_vs_212')), 'S04-B', 'T07 Welch t')

# ------------------------------------------------------------------ innate / MoA
for k, g in [('ifn_344', 'PSLN-344'), ('ifn_212', 'PSLN-212'), ('ifn_y', 'PSLN-212(Y)'), ('ifn_cmp', 'CMP-204'), ('ifn_r848', 'PSLN-R848'), ('ifn_combo', 'PSLN-212/R848'), ('ifn_344y', 'PSLN-344(Y)')]:
    put(k, f"{gm('S01-A', g, '16h'):.1f}" if g in ('CMP-204', 'PSLN-R848') else f"{gm('S01-A', g, '16h'):.0f}", 'S01-A (16 h)', 'T05 geometric mean')
put('ifn_fold', f"{gm('S01-A', 'PSLN-344', '16h') / gm('S01-A', 'PSLN-212', '16h'):.1f}", 'S01-A', 'T05/T07'); put('ifn_p', fmt_p(con('S01-A', 'PSLN-344', 'PSLN-212', '16h', 'p_welch_t')), 'S01-A', 'T06 Welch t on log10')
put('ifn72_344', f"{gm('S01-A', 'PSLN-344', '72h'):.1f}", 'S01-A (72 h)', 'T05'); put('ifn72_y', f"{gm('S01-A', 'PSLN-212(Y)', '72h'):.1f}", 'S01-A (72 h)', 'T05')
for tp in ['16h', '36h', '72h']:
    put(f'gm_344_{tp}', f"{gm('S02-F', 'PSLN-344', tp):.1f}", f'S02-F ({tp})', 'T05 geometric mean'); put(f'gm_212_{tp}', f"{gm('S02-F', 'PSLN-212', tp):.1f}", f'S02-F ({tp})', 'T05')
put('gm_212_max', f"{max(gm('S02-F', 'PSLN-212', t) for t in ['16h', '36h', '72h']):.1f}", 'S02-F', 'T05')
put('mono_344', f"{mean('S01-D', 'PSLN-344', 4):.1f}", 'S01-D day 4', 'T05'); put('mono_212', f"{mean('S01-D', 'PSLN-212', 4):.1f}", 'S01-D day 4', 'T05'); put('mono_y', f"{mean('S01-D', 'PSLN-212(Y)', 4):.1f}", 'S01-D day 4', 'T05')
put('dc_344', f"{mean('S01-E', 'PSLN-344', 4):.1f}", 'S01-E day 4', 'T05'); put('dc_212', f"{mean('S01-E', 'PSLN-212', 4):.1f}", 'S01-E day 4', 'T05'); put('dc_y', f"{mean('S01-E', 'PSLN-212(Y)', 4):.1f}", 'S01-E day 4', 'T05')
put('ccr2_mono_a', f"{mean('S07-B', 'PSLN-344', 'CD11b+Ly6C+ monocytes'):.1f}", 'S07-B', 'T05'); put('ccr2_mono_b', f"{mean('S07-B', 'PSLN-344+INCB3344', 'CD11b+Ly6C+ monocytes'):.1f}", 'S07-B', 'T05')
put('ccr2_mono_red', f"{100 * (1 - mean('S07-B', 'PSLN-344+INCB3344', 'CD11b+Ly6C+ monocytes') / mean('S07-B', 'PSLN-344', 'CD11b+Ly6C+ monocytes')):.0f}", 'S07-B', 'T05')
put('ccr2_cd8_a', f"{mean('S02-I', 'PSLN-344(Y)'):.1f}", 'S02-I', 'T05'); put('ccr2_cd8_b', f"{mean('S02-I', 'PSLN-344(Y)+INCB3344'):.1f}", 'S02-I', 'T05')
for k, g in [('h_wt', 'WT w/o cDC'), ('h_ko', 'IFN w/o cDC'), ('h_gm', 'GMCSF'), ('h_wtc', 'WT w/ cDC'), ('h_koc', 'IFN w/ cDC')]: put(k, f"{mean('S02-H', g):.1f}", 'S02-H', 'T05')
put('h_p_ko', fmt_p(con('S02-H', 'WT w/o cDC', 'IFN w/o cDC', '', 'p_welch_t')), 'S02-H', 'T06 Welch t')
put('ccr2_p', fmt_p(con('S07-B', 'PSLN-344', 'PSLN-344+INCB3344', 'CD11b+Ly6C+ monocytes', 'p_welch_t')), 'S07-B', 'T06 Welch t')
put('gm36_p', fmt_p(con('S02-F', 'PSLN-344', 'PSLN-212', '36h', 'p_welch_t')), 'S02-F', 'T06 Welch t on log10')
put('am_p', fmt_p(con('S01-C', 'WT', 'SPA/D', '', 'p_welch_t')), 'S01-C', 'T06 Welch t')
put('s15l_344', sg('S15-L', 'PSLN-344'), 'S15-L', 'T02'); put('s15l_sham', sg('S15-L', 'Sham'), 'S15-L', 'T02'); put('h_p_gm', fmt_p(con('S02-H', 'IFN w/o cDC', 'GMCSF', '', 'p_welch_t')), 'S02-H', 'T06 Welch t')
put('g_212', f"{mean('S02-G', 'PSLN-212'):.1f}", 'S02-G', 'T05'); put('g_212gm', f"{mean('S02-G', 'PSLN-212+GM-CSF'):.1f}", 'S02-G', 'T05'); put('g_gm', f"{mean('S02-G', 'GM-CSF'):.1f}", 'S02-G', 'T05')
put('mac_212', f"{mean('S07-A', 'PSLN-212', 5):.1f}", 'S07-A day 5', 'T05'); put('mac_344', f"{mean('S07-A', 'PSLN-344', 5):.1f}", 'S07-A day 5', 'T05')
put('am_wt', f"{mean('S01-C', 'WT'):.0f}", 'S01-C', 'T05'); put('am_ko', f"{mean('S01-C', 'SPA/D'):.0f}", 'S01-C', 'T05')
put('aec2_np', f"{mean('S01-B', 'AECII/PSLN-SRB'):.1f}", 'S01-B', 'T05'); put('aec2_free', f"{mean('S01-B', 'AECII/FreeSRB'):.1f}", 'S01-B', 'T05'); put('aec1_np', f"{mean('S01-B', 'AECI/PSLN-SRB'):.1f}", 'S01-B', 'T05')
put('aec1_s08c', f"{mean('S08-C', 'AECI-PSLN-SRB'):.1f}", 'S08-C', 'T05 (as printed; conflicts with S01-B)')
put('cbx_minus', f"{mean('S11-C', 'CBX-'):.1f}", 'S11-C', 'T05'); put('cbx_plus', f"{mean('S11-C', 'CBX+'):.1f}", 'S11-C', 'T05')
put('ptx_lung', f"{mean('S05-C', 'Lung'):.0f}", 'S05-C', 'T05'); put('ptx_lung_ptx', f"{mean('S05-C', 'Lung+PTX'):.0f}", 'S05-C', 'T05'); put('ptx_mln', f"{mean('S05-C', 'MLN'):.0f}", 'S05-C', 'T05'); put('ptx_mln_ptx', f"{mean('S05-C', 'MLN+PTX'):.0f}", 'S05-C', 'T05')
put('s12_wt', f"{mean('S12-A', 'WT to WT'):.1f}", 'S12-A', 'T05'); put('s12_ko', f"{mean('S12-A', 'IFNAR-/- to WT'):.1f}", 'S12-A', 'T05'); put('s12_p', fmt_p(con('S12-A', 'WT to WT', 'IFNAR-/- to WT')), 'S12-A', 'T06 Welch t')
put('aid_344', f"{gm('S03-L', 'PSLN-344', 'Aicda'):.0f}", 'S03-L', 'T05 geometric mean'); put('aid_212', f"{gm('S03-L', 'PSLN-212', 'Aicda'):.1f}", 'S03-L', 'T05')
# young
yy = Y.set_index(['block', 'level'])
put('y_ifn_ratio', f"{yy.loc[('S01-A', '16h'), 'ratio']:.2f}", 'S01-A (16 h)', 'T09b'); put('y_ifn_p', fmt_p(yy.loc[('S01-A', '16h'), 'p_welch']), 'S01-A', 'T09b Welch t')
dn = Y[~Y.block.isin(['S01-A'])]; dn = dn[~((dn.block == 'S01-E') & (dn.level.isin(['0', '2'])))]
put('y_down_lo', f"{dn.ratio.min():.2f}", 'S01-E S01-F S01-G S02-C S02-E', 'T09b'); put('y_down_hi', f"{dn.ratio.max():.2f}", 'same', 'T09b'); put('y_down_nsig', str(int((dn.p_mwu < 0.05).sum())), 'same', 'T09b exact Mann-Whitney'); put('y_down_n', str(len(dn)), 'same', 'T09b')

# ------------------------------------------------------------------ safety / dose
put('wl_344', f"{W.loc['PSLN-344', 'mean_max_loss_pct']:.1f}", 'S08-D', 'T08a'); put('wl_344_worst', f"{100 - W.loc['PSLN-344', 'worst_animal_nadir']:.1f}", 'S08-D', 'T08a'); put('wl_vac', f"{W.loc['Vaccine', 'mean_max_loss_pct']:.1f}", 'S08-D', 'T08a')
put('wl_344_d10', f"{W.loc['PSLN-344', 'mean_day10']:.1f}", 'S08-D', 'T08a'); put('wl_combo', f"{W.loc['PSLN-212/R848', 'mean_max_loss_pct']:.1f}", 'S08-D', 'T08a'); put('wl_combo_n10', str(int(W.loc['PSLN-212/R848', 'animals_losing_ge10pct'])), 'S08-D', 'T08a')
put('wl_combo_d10', f"{W.loc['PSLN-212/R848', 'mean_day10']:.1f}", 'S08-D', 'T08a')
tk = WT[((WT.group1 == 'PSLN-344') & (WT.group2 == 'Vaccine')) | ((WT.group1 == 'Vaccine') & (WT.group2 == 'PSLN-344'))]; put('wl_p', fmt_p(float(tk['p-adj'].iloc[0])), 'S08-D', 'T08a2 Tukey on per-animal nadir')
def cy(panel_start, analyte, group): return float(CY[CY.panel.str.startswith(panel_start) & (CY.analyte == analyte) & (CY.group == group)].geo_fold.iloc[0])
for a_ in ['Tnf', 'Il6', 'Il10', 'Ccl2', 'Ifnb1']:
    for g, kg in [('PSLN-344', '344'), ('PSLN-212', '212'), ('PSLN-212(y)', 'y'), ('PSLN-212/R848', 'combo')]:
        v16, v72 = cy('16 h', a_, g), cy('72 h', a_, g)
        put(f'cy16_{a_}_{kg}', f'{v16:.0f}' if v16 >= 10 else f'{v16:.1f}', 'S09-A (cols A-V)', 'T08b geometric mean'); put(f'cy72_{a_}_{kg}', f'{v72:.0f}' if v72 >= 10 else (f'{v72:.1f}' if v72 >= 1 else f'{v72:.2f}'), 'S09-A (cols X-AS)', 'T08b')
cn = CNS.set_index(['analyte', 'a', 'b'])
for a_ in ['Ifnb1', 'Tnf', 'Isg15']:
    put(f'cns_{a_}', f"{cn.loc[(a_, 'PSLN-344', 'PBS'), 'ratio']:.2f}", 'S10-A', 'T08d'); put(f'cns_{a_}_p', fmt_p(cn.loc[(a_, 'PSLN-344', 'PBS'), 'p_welch']), 'S10-A', 'T08d Welch t'); put(f'cns_{a_}_ct', f"{cn.loc[(a_, 'CT', 'PBS'), 'ratio']:.1f}", 'S10-A', 'T08d')
put('cns_Tnf_tukey', fmt_p(cn.loc[('Tnf', 'PSLN-344', 'PBS'), 'p_tukey']), 'S10-A', 'T08d Tukey'); put('cns_Tnf_ci', f"{abs(round(cn.loc[('Tnf', 'PSLN-344', 'PBS'), 'diff_ci95_lo'], 2)):.2f} to {cn.loc[('Tnf', 'PSLN-344', 'PBS'), 'diff_ci95_hi']:.2f}", 'S10-A', 'T08d Welch 95% CI of difference (lower bound -0.0006 printed as 0.00)')
put('cns_Tnf_diff', f"{cn.loc[('Tnf', 'PSLN-344', 'PBS'), 'diff']:.2f}", 'S10-A', 'T08d')
put('cns_Tnf_sham', f"{cn.loc[('Tnf', 'Sham', 'PBS'), 'ratio']:.2f}", 'S10-A', 'T08d')
put('emax_344', f"{DR.loc['PSLN-344', 'Emax_fold']:.0f}", 'S08-A', 'T08e Hill fit'); put('emax_344_ci', DR.loc['PSLN-344', 'Emax_ci'].replace('-', '–'), 'S08-A', 'T08e bootstrap'); put('emax_212', f"{DR.loc['PSLN-212', 'Emax_fold']:.0f}", 'S08-A', 'T08e')
put('ed50_344', f"{DR.loc['PSLN-344', 'ED50_ug']:.0f}", 'S08-A', 'T08e'); put('ed50_344_ci', DR.loc['PSLN-344', 'ED50_ci'].replace('-', '–'), 'S08-A', 'T08e'); put('ed50_212', f"{DR.loc['PSLN-212', 'ED50_ug']:.0f}", 'S08-A', 'T08e')
for dose in ['5', '10', '20']: put(f'pct40_{dose}', f"{DR.loc['PSLN-344', f'pct_of_40ug_at_{dose}ug']:.0f}", 'S08-A', 'T08e observed means')
put('obs20_344', f"{DR.loc['PSLN-344', 'obs_20ug']:.0f}", 'S08-A', 'T08e'); put('obs40_212', f"{DR.loc['PSLN-212', 'obs_40ug']:.0f}", 'S08-A (40 ug)', 'T08e observed mean'); put('obs10_344', f"{DR.loc['PSLN-344', 'obs_10ug']:.0f}", 'S08-A (10 ug)', 'T08e observed mean'); put('obs40_344', f"{DR.loc['PSLN-344', 'obs_40ug']:.0f}", 'S08-A', 'T08e')
put('ee_344', f"{mean('S08-B', 'PSLN-344'):.1f}", 'S08-B', 'T05'); put('ee_344_sd', f"{sd('S08-B', 'PSLN-344'):.1f}", 'S08-B', 'T05'); put('ee_212', f"{mean('S08-B', 'PSLN-212'):.1f}", 'S08-B', 'T05')
aged = ['S13-F', 'S13-G', 'S15-A', 'S15-B', 'S15-C', 'S15-D', 'S15-E', 'S15-F', 'S15-G', 'S15-M', 'S15-O']
for g, kg in [('PSLN-344', '344'), ('PSLN-212(Y)', 'y')]:
    x = NAD[NAD.weight_block.isin(aged) & (NAD.group == g)]
    put(f'nad_{kg}', f"{(x.mean_max_loss_pct * x.n_survivors_by_weight).sum() / x.n_survivors_by_weight.sum():.0f}", ' '.join(aged), 'T09a survivors only'); put(f'nad_{kg}_n', str(int(x.n_survivors_by_weight.sum())), 'same', 'T09a'); put(f'nad_{kg}_ge10', str(int(x.n_losing_ge10pct.sum())), 'same', 'T09a')

# ------------------------------------------------------------------ integrity
comp = IV[~IV.verdict.str.startswith('group present')]
put('iv_total', str(len(comp)), 'all paired survival/weight blocks', 'T01d (03_integrity_checks.py CHECK 6)'); put('iv_agree', str(int((comp.verdict == 'agree').sum())), 'same', 'T01d'); put('iv_dis', str(int((comp.verdict == 'DISAGREE').sum())), 'same', 'T01d')
put('iv_amb', str(int((comp.verdict == 'agree if ambiguous=dead').sum())), 'same', 'T01d')
put('s11_same', str(int(S11.same.sum())), 'S11-A S11-B', 'T01c'); put('s11_tot', str(len(S11)), 'S11-A S11-B', 'T01c')
put('traj_pairs', str(len(TR)), 'S08-D S09-E S09-G S15-A/C/F/I/J/M', 'T01f (CHECK 7)'); put('traj_blockpairs', str(TR.groupby(['a_block', 'a_group', 'b_block', 'b_group']).ngroups), 'same', 'T01f')
hp_total = int(FRc.n_cells.sum()); hp_shared = int(FRc[FRc.n_blocks >= 2].n_cells.sum())
put('frac_total', str(hp_total), 'weight blocks', 'T01g (CHECK 8)'); put('frac_shared', str(hp_shared), 'weight blocks', 'T01g'); put('frac_pct', f'{100 * hp_shared / hp_total:.0f}', 'weight blocks', 'T01g')

put('cns_Tnf_p2', f"= {cn.loc[('Tnf', 'PSLN-344', 'PBS'), 'p_welch']:.2f}", 'S10-A', 'T08d Welch t')
put('boost1_base', f"{r('S03-A', 'aged344'):,.0f}", 'S03-A', 'T07 geometric mean')
put('n_aged_arms', str(6 * 18), 'design', '6 aged arms x 18')
TD = rd('T01h_integrity_terminal_digits.csv')
put('td_n2', f"{int(TD.n.iloc[1]):,}", 'all blocks recorded to 2 decimals', 'T01h (CHECK 10)'); put('td_chi2', f"{TD.chi2.iloc[1]:.0f}", 'same', 'T01h chi-square, 9 d.f.')
put('td_nw', f"{int(TD.n.iloc[2]):,}", 'weight blocks', 'T01h'); put('td_chiw', f"{TD.chi2.iloc[2]:.0f}", 'weight blocks', 'T01h chi-square, 9 d.f.')
YW = rd('T09c_young_postchallenge_weight.csv').set_index(['block', 'measure'])
put('s09g_344', f"{YW.loc[('S09-G', 'day14'), 'young344']:.1f}", 'S09-G (day 14 after challenge)', 'T09c mean of per-animal values'); put('s09g_212', f"{YW.loc[('S09-G', 'day14'), 'young212']:.1f}", 'S09-G', 'T09c')
put('s09g_p', fmt_p(YW.loc[('S09-G', 'day14'), 'p_welch']), 'S09-G', 'T09c Welch t')
put('mono8_344', f"{mean('S01-D', 'PSLN-344', 8):.1f}", 'S01-D (day 8)', 'T05'); put('mono8_y', f"{mean('S01-D', 'PSLN-212(Y)', 8):.1f}", 'S01-D (day 8)', 'T05'); put('mono0_344', f"{mean('S01-D', 'PSLN-344', 0):.1f}", 'S01-D (day 0)', 'T05')
put('mono8_p', fmt_p(con('S01-D', 'PSLN-344', 'PSLN-212(Y)', 8, 'p_welch_t')), 'S01-D (day 8)', 'T06 Welch t')
# ------------------------------------------------------------------ power
def pw(scen, n): return float(PW[(PW.scenario == scen) & (PW.n_per_arm == n)].power.iloc[0])
put('pw18', f"{100 * pw('conservative (85% vs 30%)', 18):.0f}", 'design', 'T11 exact Fisher power'); put('pw7', f"{100 * pw('conservative (85% vs 30%)', 7):.0f}", 'design', 'T11'); put('pw7_obs', f"{100 * pw('observed pooled effect (92% vs 18%)', 7):.0f}", 'design', 'T11')
put('pw12_obs', f"{100 * pw('observed pooled effect (92% vs 18%)', 12):.0f}", 'design', 'T11')
put('n_hai4', str(int(PW[(PW.scenario == '4-fold difference') & (PW.power == 0.9)].n_per_arm.iloc[0])), 'S03-C/D/G/H SDs', 'T11 t-test on log10 titres')

pd.DataFrame(REG).to_csv(os.path.join(T, 'T10_numbers_cited.csv'), index=False)
json.dump(N, open(os.path.join(T, 'T10_numbers_cited.json'), 'w'), indent=1, ensure_ascii=False)
print(len(N), 'numbers registered')
for k in ['early_344', 'early_344_ci', 'early_p_212', 'early_p_sham', 'worst_344', 'worst_p', 'd60_344', 'd60_p_unt', 'bg_ci', 'med_344', 'med_212', 'hai1_344', 'hai1_fold', 'ratio1_344', 'ifn_p', 'wl_p', 'cns_Tnf', 'cns_Tnf_p', 'cns_Tnf_ci',
          'emax_344_ci', 'iv_total', 'iv_dis', 'traj_pairs', 'traj_blockpairs', 'frac_shared', 'frac_total', 'pw18', 'n_hai4', 'y_down_lo', 'y_down_hi', 'y_down_nsig', 'y_down_n', 'nad_344', 'nad_344_n', 'nad_344_ge10', 'max_p_sham', 'imp_p', 'h_p_ko', 'h_p_gm']:
    print(f'  {k:18s} {N[k]}')
