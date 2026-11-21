"""Collect every number quoted in the proposal narrative into a ledger (value + source block/cells + analysis file)."""
import pandas as pd, numpy as np, json
from statsmodels.stats.proportion import proportion_confint
from scipy import stats
W = '/tmp/work/'
H = pd.read_csv(W + 'h2h.csv'); S = pd.read_csv(W + 'survival_by_group.csv'); P = pd.read_csv(W + 'survival_pooled.csv')
PO = pd.read_csv(W + 'survival_pooled_arms.csv').set_index('group'); LOO = pd.read_csv(W + 'survival_loo.csv')
PW = pd.read_csv(W + 'survival_pairwise.csv'); M = pd.read_csv(W + 'moa_contrasts.csv'); R = pd.read_csv(W + 'restoration_index.csv')
E = pd.read_csv(W + 'dose_response.csv').set_index('group'); RX = pd.read_csv(W + 'reactogenicity_s08d.csv').set_index('group')
T = pd.read_csv(W + 'tidy/tte.csv'); V = pd.read_csv(W + 'tidy/values.csv'); V['time'] = V.time.fillna('')
L = []
def add(key, value, meaning, blocks, analysis, cells=''):
    L.append(dict(key=key, value=value, meaning=meaning, source_blocks=blocks, source_cells=cells, analysis=analysis))
    return value
def h(blk, an, t):
    return H[(H.block == blk) & (H.analyte == an) & (H.time == t)].iloc[0]
def newc(x1, n1, x2, n2):
    l1, u1 = proportion_confint(x1, n1, method='wilson'); l2, u2 = proportion_confint(x2, n2, method='wilson')
    p1, p2 = x1 / n1, x2 / n2; d = p1 - p2
    return 100 * d, 100 * (d - np.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)), 100 * (d + np.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2))
F = {}
# ---- pooled aged arms
for g, k in [('Sham', 'sham'), ('PSLN-212', 'p212'), ('PSLN-344', 'p344'), ('PSLN-212(Y)', 'young')]:
    r = PO.loc[g]
    F[f'arm_{k}'] = add(f'arm_{k}', f"{int(r.survivors)}/{int(r.n)} ({r.pct:.0f}%)", f'Pooled survival, {g}, aged experiments',
                        r.blocks, 'survival.py -> survival_pooled_arms.csv')
    F[f'arm_{k}_ci'] = add(f'arm_{k}_ci', f"{r.lo:.0f}-{r.hi:.0f}%", f'Clopper-Pearson 95% CI, {g}', r.blocks, 'survival_pooled_arms.csv')
d, lo, hi = newc(61, 73, 62, 63)
F['p344_vs_young'] = add('p344_vs_young', f'{d:.0f} pp ({lo:.0f} to {hi:.0f})', 'Aged PSLN-344 minus young PSLN-212 pooled survival (Newcombe CI)', 'same as arms', 'newcombe.py')
a = P.iloc[0]
F['h2h_344'] = add('h2h_344', a.surv_344, 'Head-to-head survivors PSLN-344 (14 strata incl. 14-month imprinting)', 'S03-I,J; S06-A,B,C,E,F,G; S06-E/F[imprint]; S15-L,N', 'survival.py')
F['h2h_212'] = add('h2h_212', a.surv_212, 'Head-to-head survivors PSLN-212', 'as above', 'survival.py')
F['h2h_pct344'] = add('h2h_pct344', f'{a.pct_344:.0f}%', '', 'as above', 'survival.py'); F['h2h_pct212'] = add('h2h_pct212', f'{a.pct_212:.0f}%', '', 'as above', 'survival.py')
F['h2h_rd'] = add('h2h_rd', f'{a.MH_RD_pp:.0f}', 'Mantel-Haenszel risk difference (pp); equals crude (balanced arms)', 'as above', 'survival.py / newcombe.py')
F['h2h_rd_ci'] = add('h2h_rd_ci', f'{a.RD_newcombe_lo:.0f}-{a.RD_newcombe_hi:.0f}', 'Newcombe 95% CI (pp)', 'as above', 'newcombe.py')
F['h2h_hr'] = add('h2h_hr', '0.076 (0.043-0.134)', 'Stratified Cox hazard ratio PSLN-344 vs PSLN-212', 'as above', 'strat.R (R survival 3.8-3)')
F['h2h_chi2'] = add('h2h_chi2', '117', 'Stratified log-rank chi-square (1 df), p<2e-16', 'as above', 'strat.R')
F['h2h_strata'] = add('h2h_strata', '14/14', 'Strata with point estimate favouring PSLN-344', 'as above', 'survival.py')
b = P.iloc[1]; c = P.iloc[2]
F['sensB'] = add('sensB', f'{b.MH_RD_pp:.0f} pp ({b.RD_newcombe_lo:.0f}-{b.RD_newcombe_hi:.0f})', 'Sensitivity B: excluding body-weight-conflict experiments', 'S06-A,B,F + imprint strata', 'survival.py')
F['sensC'] = add('sensC', f'{c.MH_RD_pp:.0f} pp ({c.RD_newcombe_lo:.0f}-{c.RD_newcombe_hi:.0f})', 'Sensitivity C: worst case for PSLN-344', 'all strata + S06-D (S15-D counts)', 'survival.py')
F['sensC_counts'] = add('sensC_counts', f'{c.surv_344} vs {c.surv_212}', 'Worst-case survivor counts', '', 'survival.py')
F['loo_range'] = add('loo_range', f'{LOO.MH_RD_pp.min():.0f}-{LOO.MH_RD_pp.max():.0f} pp', 'Leave-one-experiment-out range of the difference', '', 'survival_loo.csv')
# durability / rapid / imprint / young
dd = P[P.analysis.str.startswith('E.')].iloc[0]
F['d60_344'] = add('d60_344', dd.surv_344, 'Day-60 challenges, PSLN-344', 'S06-E,F,G', 'survival.py'); F['d60_212'] = add('d60_212', dd.surv_212, 'Day-60 challenges, PSLN-212', 'S06-E,F,G', 'survival.py')
yy = T[T.block.isin(['S06-E', 'S06-F', 'S06-G']) & (T.group == 'PSLN-212(Y)')]
F['d60_young'] = add('d60_young', f"{int((yy.event == 0).sum())}/{len(yy)}", 'Day-60 challenges, young PSLN-212', 'S06-E,F,G', 'survival_by_group.csv')
F['d14_vs_d60'] = add('d14_vs_d60', '13/14 vs 10/14 (Fisher p=0.33)', 'PSLN-344 matched designs, challenge d14 (S06-A,C) vs d60 (S06-E,F)', 'S06-A,C,E,F', 'biomarkers.py')
rr = P[P.analysis.str.startswith('F.')].iloc[0]
F['rapid'] = add('rapid', f'{rr.surv_344} vs {rr.surv_212}', 'Rapid-onset challenges (d2-3), PSLN-344 vs PSLN-212', 'S03-J, S06-B', 'survival.py')
def sv(blk, g):
    s = S[(S.block == blk) & (S.group == g)].iloc[0]; return f"{int(s.survivors)}/{int(s.n)}"
for blk in ['S03-I', 'S03-J', 'S06-A', 'S06-B', 'S06-C', 'S06-E', 'S06-F', 'S06-G', 'S15-L', 'S15-N']:
    for g, k in [('Sham', 'sham'), ('PSLN-212', '212'), ('PSLN-344', '344'), ('PSLN-212(Y)', 'Y'), ('CMP-204', 'cmp'), ('Untreated', 'untr')]:
        if ((S.block == blk) & (S.group == g)).any():
            F[f'{blk}_{k}'] = add(f'{blk}_{k}', sv(blk, g), f'Survivors {g}', blk, 'survival_by_group.csv',
                                  S[(S.block == blk) & (S.group == g)].cells.iloc[0])
for blk in ['S06-E[imprint]', 'S06-F[imprint]']:
    for g in ['Naive+PSLN-212', 'Naive+PSLN-344', 'Imprinting+PSLN-212', 'Imprinting+PSLN-344']:
        k = f"{blk[:5]}imp_{g.replace('+PSLN-', '')}"
        F[k] = add(k, sv(blk, g), f'Survivors {g}', blk, 'survival_by_group.csv', S[(S.block == blk) & (S.group == g)].cells.iloc[0])
for blk in ['S09-B', 'S09-D', 'S09-F', 'S13-E']:
    for g in ['Sham', 'PSLN-212(Y)', 'PSLN-344(Y)', 'CMP-204(Y)', 'Naive']:
        if ((S.block == blk) & (S.group == g)).any():
            k = f"{blk}_{g.replace('PSLN-', '').replace('(Y)', 'Y').replace('CMP-204', 'cmp')}"
            F[k] = add(k, sv(blk, g), f'Survivors {g} (young)', blk, 'survival_by_group.csv')
for g, k in [('3d Vaccine', 'vac'), ('3d PSLN-344', 'adj'), ('3d Vaccine+PSLN-344', 'combo')]:
    F[f'S15H_{k}'] = add(f'S15H_{k}', sv('S15-H', g), f'Survivors {g}', 'S15-H', 'survival_by_group.csv')
u = T[T.group == 'Untreated']; s = int((u.event == 1).sum()); n = len(u); lo, hi = proportion_confint(s, n, method='beta')
F['untreated_deaths'] = add('untreated_deaths', f'{s}/{n} ({100 * s / n:.0f}%; 95% CI {100 * lo:.0f}-{100 * hi:.0f}%)', 'Deaths in unvaccinated, unchallenged aged controls',
                            'S06-E, S06-G', 'extra_checks.py', 'S06!G62, S06!A99:A101')
# ---- endpoint counts
Hf = H[H.excluded.isna()]; sig = Hf[Hf.q_BH < 0.05]
F['n_endpoints'] = add('n_endpoints', str(len(Hf)), 'Independent post-treatment endpoints with both aged arms', 'all', 'h2h.py')
F['n_sig'] = add('n_sig', str(len(sig)), 'Endpoints differing at BH-FDR<5%', 'all', 'h2h.py')
sepn = 0
for _, hh in sig.iterrows():
    tt_ = hh.time if isinstance(hh.time, str) else ''
    dd_ = V[(V.block == hh.block) & (V.analyte == hh.analyte) & (V.time == tt_)]
    a_ = dd_[dd_.group == 'PSLN-344'].value.values; b_ = dd_[dd_.group == 'PSLN-212'].value.values
    sepn += int(a_.min() > b_.max() or a_.max() < b_.min())
F['n_sep'] = add('n_sep', f'{sepn}/{len(sig)}', 'Significant endpoints with complete separation of per-animal values', 'all', 'facts.py')
F['n_sig_young'] = add('n_sig_young', f"{int((sig.restoration_index > 0).sum())}/{int(sig.restoration_index.notna().sum())}", 'Significant endpoints with young benchmark that moved toward young', 'all', 'h2h.py')
# ---- key endpoints
def grab(key, blk, an, t, fmt, what):
    x = h(blk, an, t)
    F[key + '_344'] = add(key + '_344', fmt(x.summary344), f'{what}: PSLN-344', blk, 'h2h.csv')
    F[key + '_212'] = add(key + '_212', fmt(x.summary212), f'{what}: PSLN-212', blk, 'h2h.csv')
    if not pd.isna(x.summaryY): F[key + '_Y'] = add(key + '_Y', fmt(x.summaryY), f'{what}: young PSLN-212', blk, 'h2h.csv')
    if not pd.isna(x.summarySham): F[key + '_sham'] = add(key + '_sham', fmt(x.summarySham), f'{what}: sham', blk, 'h2h.csv')
    eff = f'{x.est:.1f}x ({x.lo:.1f}-{x.hi:.1f})' if x.scale != 'linear %' else f'{x.est:+.1f} pp ({x.lo:+.1f} to {x.hi:+.1f})'
    F[key + '_eff'] = add(key + '_eff', eff, f'{what}: effect 344 vs 212 (95% CI)', blk, 'h2h.csv')
    if not pd.isna(x.restoration_index): F[key + '_ri'] = add(key + '_ri', f'{x.restoration_index:.2f}', f'{what}: restoration index', blk, 'h2h.csv')
t0 = lambda v: f'{v:,.0f}'; t1 = lambda v: f'{v:.1f}'
grab('ifnb', 'S01-A', 'Ifnb1', '16h', t1, 'Lung Ifnb1 16 h fold')
grab('gmcsf', 'S02-F', 'Gm-csf (lung)', '36h', t1, 'Lung Gm-csf 36 h fold')
grab('mono', 'S01-D', 'Lung monocytes', 'd4', t1, 'Lung monocytes d4 %')
grab('ccr7', 'S02-A', 'CCR7+ migratory CD11b+ DC (lung)', '72h', t1, 'CCR7+ migratory DC %')
grab('cd86', 'S02-D CD86', 'CD86+ of MLN CD11b+ DC', 'd3', t1, 'CD86+ MLN DC %')
grab('cd40', 'S02-D CD40', 'CD40+ of MLN CD11b+ DC', 'd3', t1, 'CD40+ MLN DC %')
grab('oti', 'S02-E', 'OT-I proliferation (DC co-culture)', '72h+3d', t1, 'OT-I priming %')
grab('tfh', 'S04-A', 'Tfh ICOS-hi', 'd7', t1, 'ICOS-hi Tfh %')
grab('tfr', 'S04-B Foxp3', 'Tfr (Foxp3+ of CXCR5+ICOShi)', 'd7', t1, 'Tfr %')
grab('gc', 'S03-K', 'MLN GC B cells', 'd7', t1, 'GC B %')
grab('igg', 'S03-A', 'IgG CA09 H1N1', 'd14', t0, 'IgG CA09 GMT')
grab('hai1', 'S03-C', 'HAI CA09 H1N1', 'd14', t0, 'HAI CA09 GMT')
grab('hai3', 'S03-G', 'HAI Aichi H3N2', 'd14', t0, 'HAI Aichi GMT')
grab('neut1', 'S03-D', 'Neut CA09 H1N1', 'd14', t0, 'Neut CA09 GMT')
grab('boost1', 'S13-I', 'IgG CA09 H1N1 post-boost', 'd28', t0, 'Post-boost IgG CA09 GMT')
grab('boost3', 'S13-J', 'IgG Aichi H3N2 post-boost', 'd28', t0, 'Post-boost IgG Aichi GMT')
grab('ifng14', 'S05-F', 'MLN IFNg+ CD8 (rgH5N1 restim)', 'd14', t1, 'IFNg+ CD8 d14 %')
grab('ifng60', 'S05-G', 'MLN IFNg+ CD8 (rgH5N1 restim)', 'd60', t1, 'IFNg+ CD8 d60 %')
grab('trm', 'S05-I', 'Lung TRM CD8', 'd25', t1, 'Lung TRM %')
grab('gzmb3', 'S05-E', 'Lung GZMB+ CD8', 'd3', t1, 'Lung GZMB+ CD8 d3 %')
grab('cd206', 'S11-E', 'Lung CD206+ macrophages', 'not stated', t1, 'CD206+ macrophages %')
grab('ly6c5', 'S07-A', 'Lung Ly6C+CCR2+ macrophages (x1e5)', 'd5', t1, 'Ly6C+CCR2+ macrophages d5 (x1e5)')
# S09-A cytokines (panel1 = 16 h; panel2 = 72 h)
for an in ['Ccl2', 'Ccl3', 'Ccl5', 'Il6', 'Tnf', 'Il10']:
    grab(f'{an.lower()}16', 'S09-A panel1[A:U]', an, '16h (as printed)', t1, f'{an} 16 h fold')
    grab(f'{an.lower()}72', 'S09-A panel2[X:AS]', an, '16h (as printed)', t1, f'{an} 72 h fold (panel printed 16h)')
x = h('S09-A panel2[X:AS]', 'Tnf', '16h (as printed)'); F['tnf72_p_vsY'] = add('tnf72_p_vsY', f'{x.p_344_vs_Y:.3f}', 'Tnf 72 h PSLN-344 vs young p', 'S09-A panel2', 'h2h.csv')
x = h('S09-A panel2[X:AS]', 'Il10', '16h (as printed)'); F['il1072_p_vsY'] = add('il1072_p_vsY', f'{x.p_344_vs_Y:.3f}', 'Il10 72 h PSLN-344 vs young p', 'S09-A panel2', 'h2h.csv')
# IgG2a/IgG1 ratios from primary S13 titres
def ratio(a, b, g):
    x = V[(V.block == a) & (V.group == g)].sort_values('animal').value.values; y = V[(V.block == b) & (V.group == g)].sort_values('animal').value.values
    return (x / y).mean()
for g, k in [('PSLN-212', '212'), ('PSLN-344', '344'), ('PSLN-212(Y)', 'Y')]:
    F[f'th1_h1_{k}'] = add(f'th1_h1_{k}', f"{ratio('S13-A', 'S13-B', g):.2f}", f'IgG2a/IgG1 H1N1 {g} (from primary titres)', 'S13-A/S13-B', 'crosscheck.py')
    F[f'th1_h3_{k}'] = add(f'th1_h3_{k}', f"{ratio('S13-C', 'S13-D', g):.2f}", f'IgG2a/IgG1 H3N2 {g}', 'S13-C/S13-D', 'crosscheck.py')
# dose response
F['emax344'] = add('emax344', f"{E.loc['PSLN-344', 'Emax']:.0f}", 'Emax Ifnb1 fold (fit), PSLN-344', 'S08-A', 'moa.py -> dose_response.csv')
F['emax212'] = add('emax212', f"{E.loc['PSLN-212', 'Emax']:.0f}", 'Emax PSLN-212', 'S08-A', 'dose_response.csv')
F['ed50_344'] = add('ed50_344', f"{E.loc['PSLN-344', 'ED50_ug']:.1f}", 'ED50 ug PSLN-344', 'S08-A', 'dose_response.csv')
F['ed50_212'] = add('ed50_212', f"{E.loc['PSLN-212', 'ED50_ug']:.1f}", 'ED50 ug PSLN-212', 'S08-A', 'dose_response.csv')
F['emax_r848'] = add('emax_r848', f"{E.loc['PSLN-344/R848', 'Emax']:.0f}", 'Emax PSLN-344/R848', 'S08-A', 'dose_response.csv')
F['dose_sparing'] = add('dose_sparing', 'about 3-fold dose-sparing: PSLN-344 at 6.7–7.3 µg matches PSLN-212 at 20 µg', 'Dose-sparing, Emax fit (7.3 ug) and linear interpolation (6.7 ug)', 'S08-A', 'moa.py')
dr = V[V.block == 'S08-A'].copy(); m = dr[dr.group == 'PSLN-344'].groupby('time').value.mean()
F['ifnb_10_vs_20'] = add('ifnb_10_vs_20', f"{100 * m['10ug'] / m['20ug']:.0f}%", 'PSLN-344 Ifnb1 at 10 ug as % of 20 ug response', 'S08-A', 'facts.py')
F['plateau'] = add('plateau', f"{100 * (E.loc['PSLN-344', 'plateau_ratio_40_20'] - 1):.0f}%", 'Gain from 20 to 40 ug for PSLN-344', 'S08-A', 'dose_response.csv')
# MoA contrasts
def mc(label_start):
    r = M[M.label.str.startswith(label_start)].iloc[0]; return r
for key, lab in [('spad', 'Delivery: SP-A/D'), ('cbx', 'Gap-junction'), ('ifnar', 'Type I IFN: IFNAR-/- BM (no cDC)'), ('gmrescue', 'GM-CSF rescue: IFNAR-/- BM + GM-CSF vs IFNAR-/- BM'),
                 ('gmgof', 'GM-CSF gain-of-function'), ('ccr2mono', 'CCR2: INCB3344 vs vehicle, lung monocytes'), ('ccr2mac', 'CCR2: INCB3344 vs vehicle, Ly6C+'),
                 ('ccr2cd8', 'CCR2: INCB3344 vs vehicle, lung GZMB'), ('ptxdc', 'Migration: PTX vs PSLN-344, antigen+'), ('ptxoti', 'Migration: PTX vs PSLN-344, OT-I'),
                 ('ptxmln', 'Migration: PTX in vivo, OT-I proliferation in MLN'), ('ptxlung', 'Migration: PTX in vivo, OT-I proliferation in lung'),
                 ('ifnarmono', 'Type I IFN: IFNAR-/- vs WT BM: infiltrating'), ('young_ifnb', 'Young: PSLN-344(Y) vs PSLN-212(Y), Ifnb1'),
                 ('cns_ifnb', 'CNS Ifnb1: PSLN-344 vs Sham'), ('cns_tnf', 'CNS Tnf: PSLN-344 vs Sham'), ('cns_isg', 'CNS Isg15: PSLN-344 vs Sham'),
                 ('ct_ifnb', 'CNS Ifnb1: CT vs Sham'), ('cmp_ifnb', 'cGAMP (CMP-204) vs PSLN-212'), ('r848_ifnb', 'PSLN-212/R848 vs PSLN-344'), ('ee', 'Encapsulation efficiency')]:
    r = mc(lab)
    pv = 'p<0.001' if r.p_welch < 0.001 else f'p={r.p_welch:.3f}'
    F[key] = add(key, f"{r.meanB:.1f} → {r.meanA:.1f}, {r['pct_change']:+.0f}%, {pv}", r.label, r.block, 'moa.py -> moa_contrasts.csv')
# reactogenicity
F['nadir_344'] = add('nadir_344', f"{RX.loc['PSLN-344', 'mean_nadir']:.1f}%", 'Mean post-vaccination weight nadir PSLN-344', 'S08-D', 'moa.py -> reactogenicity_s08d.csv')
F['nadir_212'] = add('nadir_212', f"{RX.loc['PSLN-212', 'mean_nadir']:.1f}%", 'PSLN-212', 'S08-D', 'reactogenicity_s08d.csv')
F['nadir_vac'] = add('nadir_vac', f"{RX.loc['Vaccine', 'mean_nadir']:.1f}%", 'Vaccine only', 'S08-D', 'reactogenicity_s08d.csv')
F['nadir_r848'] = add('nadir_r848', f"{RX.loc['PSLN-212/R848', 'mean_nadir']:.1f}%", 'Mean post-vaccination weight nadir PSLN-212/R848', 'S08-D', 'reactogenicity_s08d.csv')
F['maxloss_r848'] = add('maxloss_r848', f"{RX.loc['PSLN-212/R848', 'max_loss_pct']:.0f}%", 'Maximum individual weight loss PSLN-212/R848', 'S08-D', 'reactogenicity_s08d.csv')
F['nadir_p'] = add('nadir_p', 'p=0.56', 'Welch test on weight nadir, PSLN-344 vs PSLN-212', 'S08-D', 'moa.py')
F['nadir_p_r848'] = add('nadir_p_r848', 'p=0.043', 'Welch test on weight nadir, PSLN-212/R848 vs PSLN-344', 'S08-D', 'moa.py')
# restoration layers
RL = pd.read_csv(W + 'restoration_by_layer.csv').set_index('layer')
for lay, k in [('1 Innate cytokine (16-36h)', 'ri_innate'), ('2 Myeloid recruitment & DC (d3-4)', 'ri_myeloid'), ('3 DC co-stimulation (d3)', 'ri_costim'),
               ('6 Antibody (d14)', 'ri_ab'), ('7 Antibody post-boost (d28)', 'ri_boost'), ('8 CD8 memory (d14-60)', 'ri_cd8mem')]:
    F[k] = add(k, f"{RL.loc[lay, 'median']:.2f}", f'Median restoration index: {lay}', 'see restoration_index.csv', 'restoration.py')
# HAI threshold
F['hai160'] = add('hai160', 'PSLN-344 5/5, young 5/5, PSLN-212 0/5, CMP-204 0/5, Sham 0/5', 'Animals with HAI >= 1:160 (CA09)', 'S03-C', 'biomarkers.py')
ds = T[T.block.isin(['S06-E', 'S06-F', 'S06-G']) & (T.group == 'Sham')]
F['d60_sham'] = add('d60_sham', f"{int((ds.event == 0).sum())}/{len(ds)}", 'Day-60 challenges, sham', 'S06-E,F,G', 'survival_by_group.csv')
F['fp_total'] = add('fp_total', '39', 'High-precision (>=4 decimal) values occurring more than once in the workbook', 'all sheets', 'fingerprint.py / fp_breakdown.py')
F['fp_bw'] = add('fp_bw', '33', 'Of which: body-weight values shared between different experiments or arms', 'S08, S09, S13, S15', 'fp_breakdown.py')
F['s15i_copy'] = add('s15i_copy', '40 of 42', 'S15-I combination-arm weights identical to S15-C PSLN-344 (days 2-12)', 'S15-I, S15-C', 'extra_checks.py')
F['ledger_n'] = str(len(L) + 1)
def gmv(blk, g):
    v = V[(V.block == blk) & (V.group == g)].value.values; v = np.where(v <= 0, 5, v); return 2 ** np.mean(np.log2(v))
r212, r344 = [], []
for blk in ['S03-A', 'S03-C', 'S03-D', 'S03-E', 'S03-G', 'S03-H']:
    c = gmv(blk, 'CMP-204'); r212.append(gmv(blk, 'PSLN-212') / c); r344.append(gmv(blk, 'PSLN-344') / c)
F['cmp_vs212'] = add('cmp_vs212', f'{min(r212):.1f}-{max(r212):.1f}x', 'GMT ratio PSLN-212/CMP-204 across six d14 titre endpoints', 'S03-A,C,D,E,G,H', 'facts.py')
F['cmp_vs344'] = add('cmp_vs344', f'{min(r344):.0f}-{max(r344):.0f}x', 'GMT ratio PSLN-344/CMP-204 across six d14 titre endpoints', 'S03-A,C,D,E,G,H', 'facts.py')
json.dump(F, open(W + 'facts.json', 'w'), indent=1)
pd.DataFrame(L).to_csv(W + 'evidence_ledger.csv', index=False)
print(len(L), 'ledger entries'); print(json.dumps({k: F[k] for k in list(F)[:40]}, indent=0))
