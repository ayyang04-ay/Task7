"""Recompute every headline number cited in the proposal directly from the analysis tables and record where it comes from."""
import pandas as pd, numpy as np
T = '/tmp/work/tidy'
Sm = pd.read_csv(f'{T}/summary_continuous.csv'); Sm['time'] = Sm['time'].astype(str)
K = pd.read_csv(f'{T}/contrasts_continuous.csv'); K['time'] = K['time'].astype(str)
R = pd.read_csv(f'{T}/summary_survival.csv'); P = pd.read_csv(f'{T}/pairwise_survival.csv')
Pool = pd.read_csv(f'{T}/pooled_survival.csv'); B = pd.read_csv(f'{T}/biomarker_candidates.csv')
M = pd.read_csv(f'{T}/mechanistic_tests.csv'); D = pd.read_csv(f'{T}/dose_response_fits.csv'); N = pd.read_csv(f'{T}/safety_S08D_nadir.csv')
rows = []
def add(section, claim, value, block, sheet, method):
    rows.append(dict(proposal_section=section, claim=claim, value=value, source_block=block, workbook_sheet=sheet, method=method))
def cen(block, group, time=None, meas=None):
    d = Sm[(Sm.block == block) & (Sm.group == group)]
    if time is not None: d = d[d.time == str(time)]
    if meas is not None: d = d[d.measurand == meas]
    r = d.iloc[0]
    return r.geo_mean if r.scale in ('log2', 'log10') else r['mean']
def con(block, contrast, time=None, meas=None):
    d = K[(K.block == block) & (K.contrast == contrast)]
    if time is not None: d = d[d.time == str(time)]
    if meas is not None: d = d[d.measurand == meas]
    return d.iloc[0]
# pooled survival
for sc, lab in [('All aged experiments (11)', 'as recorded'), ('Excluding integrity-flagged experiments', 'excluding 7 flagged'),
                ('All aged; weight-inferred deaths where paired weights exist', 'weight-inferred'),
                ('All aged; worst case for PSLN-344 (max deaths for 344, min for comparator)', 'worst case')]:
    a = Pool[(Pool.comparison == 'PSLN-344 vs PSLN-212') & (Pool.set == sc)].iloc[0]
    v = Pool[(Pool.comparison == 'PSLN-344 vs Sham') & (Pool.set == sc)].iloc[0]
    add('1, 3.2', f'Pooled aged survival, {lab}: PSLN-344 / PSLN-212 / vehicle', f'{a.surv_a} / {a.surv_b} / {v.surv_b}',
        a.exp_list, 'Pooled_survival_scenarios', 'sum over experiments')
    add('1, 3.2', f'MH risk difference PSLN-344 vs PSLN-212, {lab}', f'{a.MH_risk_difference_pct:+.1f} points; CMH p={a.p_CMH:.1e}',
        a.exp_list, 'Pooled_survival_scenarios', 'Mantel-Haenszel RD; CMH test (continuity-corrected)')
a = Pool[(Pool.comparison == 'PSLN-344 vs PSLN-212') & (Pool.set == 'All aged experiments (11)')].iloc[0]
add('1, 3.2', 'Stratified log-rank PSLN-344 vs PSLN-212', f'chi2={a.stratified_logrank_chi2:.1f}, p={a.p_stratified_logrank:.1e}', a.exp_list, 'Pooled_survival_scenarios', 'log-rank stratified by experiment')
a = Pool[(Pool.comparison == 'PSLN-344 vs Sham') & (Pool.set == 'All aged experiments (11)')].iloc[0]
add('3.2', 'Stratified log-rank PSLN-344 vs vehicle', f'chi2={a.stratified_logrank_chi2:.1f}, p={a.p_stratified_logrank:.1e}', a.exp_list, 'Pooled_survival_scenarios', 'log-rank stratified by experiment')
a = Pool[(Pool.comparison == 'PSLN-212(Y) vs PSLN-344') & (Pool.set == 'All aged experiments (11)')].iloc[0]
add('3.2, 9', 'Young PSLN-212 vs aged PSLN-344 pooled survival', f'{a.surv_a} vs {a.surv_b}; RD {a.MH_risk_difference_pct:.1f}; CMH p={a.p_CMH:.4f}', a.exp_list, 'Pooled_survival_scenarios', 'MH RD; CMH')
a = Pool[(Pool.comparison == 'PSLN-212 vs Sham')]
for sc in ['All aged experiments (11)', 'Excluding integrity-flagged experiments']:
    x = a[a.set == sc].iloc[0]
    add('9', f'PSLN-212 vs vehicle ({sc})', f'{x.surv_a} vs {x.surv_b}; RD {x.MH_risk_difference_pct:.1f}; CMH p={x.p_CMH:.3f}', x.exp_list, 'Pooled_survival_scenarios', 'MH RD; CMH')
# per-experiment survival
for b_ in ['S03-I', 'S03-J', 'S06-A', 'S06-B', 'S06-C', 'S06-D', 'S06-E', 'S06-F', 'S06-G', 'S15-L', 'S15-N', 'S15-H', 'S09-B', 'S09-D', 'S09-F', 'S13-E',
           'S06-E(rows71-105; imprinting)', 'S06-F(rows71-105; imprinting)']:
    d = R[R.block == b_]
    add('3.2', f'Survival by arm, {b_}', '; '.join(f'{r.group} {int(r.survivors)}/{int(r.n)}' for r in d.itertuples()), b_, 'Survival_all_arms', 'end-of-observation survivors/n')
u = R[R.group == 'Untreated']
add('4 (I-06)', 'Unchallenged aged controls dying within 14 d', f'{int(u.deaths.sum())}/{int(u.n.sum())}', 'S06-E, S06-F, S06-G', 'Survival_all_arms', 'count')
# immunogenicity table
for blk, meas, t, lab in [('S03-C', None, 'd14', 'HI H1N1 GMT'), ('S03-G', None, 'd14', 'HI H3N2 GMT'), ('S03-D', None, 'd14', 'Neut H1N1 GMT'),
                          ('S03-H', None, 'd14', 'Neut H3N2 GMT'), ('S03-A', None, 'd14', 'IgG H1N1 GMT'), ('S13-J', None, 'd28', 'IgG H3N2 d28 GMT'),
                          ('S04-A', 'MLN Tfh ICOS-high (%)', 'd7', 'Tfh ICOS-high %'), ('S03-K', None, 'd7', 'GC B %'), ('S05-F', None, 'd14', 'IFNg+ CD8 d14 %'),
                          ('S05-G', None, 'd60', 'IFNg+ CD8 d60 %'), ('S05-I', None, 'd25', 'Lung TRM %'), ('S01-A', None, '16h', 'Ifnb1 16h fold'),
                          ('S02-F', None, '36h', 'Gm-csf 36h fold'), ('S01-D', None, '4', 'Monocytes d4 %'), ('S02-A', None, '72h', 'CCR7+ migratory DC %'),
                          ('S02-C', None, '36h', 'Antigen+ MLN DC %'), ('S02-E', None, '72h+3d', 'OT-I proliferation %'), ('S04-B Foxp3', None, 'd7', 'Tfr %'),
                          ('S05-E', None, 'd3', 'GZMB+ CD8 d3 %'), ('S11-E', None, 'not stated', 'CD206+ macrophages %')]:
    vals = []
    for g in ['Sham', 'CMP-204', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)', 'PTX']:
        try: vals.append(f'{g} {cen(blk, g, t, meas):.3g}')
        except Exception: pass
    c = None
    try: c = con(blk, 'PSLN-344 vs PSLN-212', t, meas)
    except Exception: pass
    extra = f' | 344 vs 212: {c.effect:.2f} ({c.effect_type}), Welch p={c.p_welch:.2g}, Tukey p={c.p_tukey:.2g}' if c is not None else ''
    add('3.3, 5, 6', lab, '; '.join(vals) + extra, blk, 'Continuous_summary / Continuous_contrasts', 'GM for log-analysed endpoints, mean otherwise; Welch t on analysis scale')
# % of young
F = pd.read_csv(f'{T}/forest_344_vs_212.csv')
for r in F.itertuples():
    add('3.3 (Figure 3)', f'Aged PSLN-344 as % of young: {r.label}', f'{r.pct_young:.0f}% ; ratio 344/212 {r.ratio:.2f} (95% CI {r.lo:.2f}-{r.hi:.2f})', r.block, 'Forest_344_vs_212', 'ratio of geometric means')
# IgG2a/IgG1 from S13
C = pd.read_csv(f'{T}/continuous.csv')
def v(bk, g): return C[(C.block == bk) & (C.group == g)].sort_values('rep').value.values
for x2, x1, lab in [('S13-A', 'S13-B', 'H1N1'), ('S13-C', 'S13-D', 'H3N2')]:
    add('3.3', f'IgG2a/IgG1 {lab} (recomputed from S13)', '; '.join(f'{g} {np.exp(np.mean(np.log(v(x2, g) / v(x1, g)))):.2f}' for g in ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']),
        f'{x2}/{x1}', 'Tidy_continuous', 'geometric mean of per-animal quotients')
# mechanistic
for r in M.itertuples():
    add('5', r.experiment, f'{r.group_a} {r.mean_a:.3g} vs {r.group_b} {r.mean_b:.3g}; Welch p={r.p_welch:.2g}; MW p={r.p_mw_exact:.2g}', r.block, 'Mechanistic_tests', 'Welch t; exact Mann-Whitney')
# dose response and EE
for r in D.itertuples():
    add('3.3, 2 (G2), 9', f'Ifnb1 dose-response {r.group}', f'Emax {r.Emax:.1f} ± {r.Emax_se:.1f}; 20 ug={r.mean_20ug:.1f}x, 40 ug={r.mean_40ug:.1f}x; 20 ug = {r.pct_of_40ug_at_20ug:.0f}% of 40-ug response',
        'S08-A', 'Dose_response_fits', 'Emax model fit (baseline 1)')
ee = C[C.block == 'S08-B'].groupby('group').value.agg(['mean', 'std'])
add('3.1, 2 (CMC)', 'Encapsulation efficiency', '; '.join(f'{g} {r["mean"]:.1f} ± {r["std"]:.1f}%' for g, r in ee.iterrows()), 'S08-B', 'Tidy_continuous', 'mean ± SD (n=3)')
# safety
ns = N.groupby('group').nadir.agg(['mean', 'std', 'min'])
add('3.4', 'Post-vaccination weight nadir (% of day 0)', '; '.join(f'{g} {r["mean"]:.1f} ± {r["std"]:.1f} (min {r["min"]:.1f})' for g, r in ns.iterrows()), 'S08-D', 'Safety_S08D_nadir', 'per-animal minimum over days 2-10')
for meas in ['CNS Ifnb1 (fold)', 'CNS Tnf (fold)', 'CNS Isg15 (fold)']:
    c1 = K[(K.block == 'S10-A') & (K.measurand == meas) & (K.contrast == 'PSLN-344 vs PBS')].iloc[0]
    c2 = K[(K.block == 'S10-A') & (K.measurand == meas) & (K.contrast == 'CT vs PBS')].iloc[0]
    add('3.4', f'{meas}: PSLN-344 and CT vs PBS', f'PSLN-344 {c1.effect:.2f}x (Welch p={c1.p_welch:.3f}, Tukey p={c1.p_tukey:.2f}); CT {c2.effect:.2f}x (p={c2.p_welch:.1g})', 'S10-A', 'Continuous_contrasts', 'GM fold ratio on log10 scale')
# biomarkers
for r in B.itertuples():
    add('6', f'Biomarker {r.marker} ({r.time})', f'AUC 344 vs 212 = {r.AUC_344_vs_212:.2f}; Hedges g = {r.g_344_vs_212:.2f}; % young restored = {r.pct_young_restored:.0f}', r.block, 'Biomarker_candidates', 'animal-level AUC; Hedges g on analysis scale')
for bk in ['S03-C', 'S03-G']:
    d = C[C.block == bk]
    add('6', f'HI titres >=160 and >=40 by arm ({bk})', '; '.join(f'{g}: >=160 {int((d[d.group == g].value >= 160).sum())}/5, >=40 {int((d[d.group == g].value >= 40).sum())}/5'
                                                            for g in ['Sham', 'CMP-204', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']), bk, 'Tidy_continuous', 'counts')
# integrity numbers
A = pd.read_csv(f'{T}/audit_s11.csv')
add('4 (I-02)', 'S11-A vs S11-B identical animal-level values', f'{int(A.identical.sum())}/{len(A)}', 'S11-A, S11-B', 'Audit_S11A_vs_S11B', 'exact equality per animal slot')
Wr = pd.read_csv(f'{T}/audit_weight_recycling.csv')
add('4 (I-01)', 'Cross-block weight trajectory pairs sharing >=3 distinct values', f'{len(Wr)}', 'S09, S13, S15', 'Weight_recycling_pairs', 'trajectory matching')
x = Wr[Wr.block_pair == 'S15-C ~ S15-I']
add('4 (I-01)', 'S15-C PSLN-344 vs S15-I Vaccine+PSLN-344 identical day-2-12 values', f'{int(x.n_same_days.sum())} of 42 (7 animals)', 'S15-C, S15-I', 'Weight_recycling_pairs', 'trajectory matching')
Ss = pd.read_csv(f'{T}/sample_size.csv')
for r in Ss.itertuples():
    add('2 (G1)', f'Sample size: {r.scenario}', f'n={r.n_per_arm}/arm; after background mortality {r.n_per_arm_after_background_mortality}', 'derived', 'Sample_size', r.endpoint)
I = pd.DataFrame(rows)
I.to_csv(f'{T}/citation_index.csv', index=False)
print(len(I), 'entries'); print(I.head(12).to_string())
