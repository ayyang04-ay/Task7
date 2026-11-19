#!/usr/bin/env python
"""
05b_curated_restoration.py -- curated "restoration" table used for Figure 2 and the MoA section.
Run: micromamba run -n core python 05b_curated_restoration.py   (after 04_survival.py and 05_endpoints.py)

For each endpoint measured in aged+PSLN-212, aged+PSLN-344 and young+PSLN-212 animals:
  aged212_pct_of_young, aged344_pct_of_young  (ratio of geometric means for titres / qPCR, ratio of arithmetic means otherwise)
  markers where LOWER is the young phenotype (Tfr, Treg, CD206+ macrophages) are inverted (young / aged) so that 100% always = young level
  bootstrap 95% CI (10,000 within-group resamples) for the PSLN-344 value; Welch t / exact Mann-Whitney p for 344 vs 212 (aged)
Integrity-driven choices (see Appendix A of the proposal):
  * IgG2a:IgG1 is RECOMPUTED from S13-A..D; S03-B / S03-F as printed are not used (column headers rotated)
  * S11-A / S11-B (duplicated values), S07-C (duplicate labels), S08-C (header conflict) are not used
  * S05-A/B (n = 2 per group/time-point, contradictory conditions) are not used
Output: tables/T07_restoration_index_curated.csv
"""
import os, numpy as np, pandas as pd
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(HERE, 'tables')
sc = pd.read_csv(os.path.join(HERE, 'parsed', 'scalar_long.csv'), keep_default_na=False); sc['factor'] = sc.factor.astype(str)
sv = pd.read_csv(os.path.join(HERE, 'parsed', 'survival_long.csv'), keep_default_na=False)
rng = np.random.default_rng(20261101)
LOGB = {'S01-A', 'S03-A', 'S03-C', 'S03-D', 'S03-E', 'S03-G', 'S03-H', 'S13-A', 'S13-B', 'S13-C', 'S13-D', 'S13-I', 'S13-J'}
HAI = {'S03-C', 'S03-G'}

def vals(block, level, group):
    d = sc[(sc.block == block) & (sc.group == group)]
    if level is not None: d = d[d.factor == level]
    v = d.sort_values('rep').value.values.astype(float)
    if block in HAI: v = np.where(v <= 0, 5.0, v)
    return v

spec = [  # step, label, block, level, inverse
 ('1 Innate sensing', 'Lung Ifnb1 mRNA, 16 h', 'S01-A', '16h', False),
 ('2 Monocyte -> DC', 'Lung monocytes, day 4', 'S01-D', '4', False),
 ('2 Monocyte -> DC', 'Lung CD11b+ DC, day 4', 'S01-E', '4', False),
 ('2 Monocyte -> DC', 'Lung cDC1, 72 h', 'S01-F', None, False),
 ('2 Monocyte -> DC', 'CCR7+ migratory CD11b+ DC (lung), 72 h', 'S02-A', None, False),
 ('2 Monocyte -> DC', 'CD11b+ DC in draining node, 72 h', 'S02-B', None, False),
 ('2 Monocyte -> DC', 'Antigen-carrying DC in draining node, 36 h', 'S02-C', None, False),
 ('2 Monocyte -> DC', 'CD40+ of node CD11b+ DC, day 3', 'S02-D CD40', None, False),
 ('2 Monocyte -> DC', 'CD86+ of node CD11b+ DC, day 3', 'S02-D CD86', None, False),
 ('2 Monocyte -> DC', 'Ex vivo CD8 cross-priming by node DC', 'S02-E', None, False),
 ('3 Regulatory brake (inverted)', 'Follicular regulatory T (Foxp3+), day 7', 'S04-B Foxp3', None, True),
 ('3 Regulatory brake (inverted)', 'Follicular regulatory T, day 30', 'S04-C', None, True),
 ('3 Regulatory brake (inverted)', 'Lung Treg, day 7 (n=3)', 'S04-D', None, True),
 ('3 Regulatory brake (inverted)', 'CD206+ lung macrophages', 'S11-E', None, True),
 ('4 Germinal centre / antibody', 'ICOS+ Tfh, day 7', 'S04-A', 'ICOS+', False),
 ('4 Germinal centre / antibody', 'Tfh:Tfr ratio, day 7', 'S04-B Tfh:Tfr', None, False),
 ('4 Germinal centre / antibody', 'Germinal-centre B cells, day 7', 'S03-K', None, False),
 ('4 Germinal centre / antibody', 'IgG+ B cells in node', 'S13-H', None, False),
 ('4 Germinal centre / antibody', 'Serum IgG anti-H1N1, day 14 (GMT)', 'S03-A', None, False),
 ('4 Germinal centre / antibody', 'Serum IgG anti-H3N2, day 14 (GMT)', 'S03-E', None, False),
 ('4 Germinal centre / antibody', 'HAI anti-H1N1, day 14 (GMT)', 'S03-C', None, False),
 ('4 Germinal centre / antibody', 'HAI anti-H3N2, day 14 (GMT)', 'S03-G', None, False),
 ('4 Germinal centre / antibody', 'Neutralising anti-H1N1, day 14 (GMT)', 'S03-D', None, False),
 ('4 Germinal centre / antibody', 'Neutralising anti-H3N2, day 14 (GMT)', 'S03-H', None, False),
 ('4 Germinal centre / antibody', 'IgG2a anti-H1N1 (GMT)', 'S13-A', None, False),
 ('4 Germinal centre / antibody', 'IgG1 anti-H1N1 (GMT)', 'S13-B', None, False),
 ('4 Germinal centre / antibody', 'IgG anti-H1N1 after boost, day 28 (GMT)', 'S13-I', None, False),
 ('4 Germinal centre / antibody', 'IgG anti-H3N2 after boost, day 28 (GMT)', 'S13-J', None, False),
 ('5 CD8 T cells', 'Lung Ki-67+ CD8, day 3', 'S05-D', None, False),
 ('5 CD8 T cells', 'Lung GZMB+ CD8, day 3', 'S05-E', None, False),
 ('5 CD8 T cells', 'IFN-g+ CD8 vs rgH5N1 (cross-reactive), day 14', 'S05-F', None, False),
 ('5 CD8 T cells', 'IFN-g+ CD8 vs rgH5N1, day 60', 'S05-G', None, False),
 ('5 CD8 T cells', 'GZMB+ CD8 vs rgH5N1, day 60', 'S05-H', None, False),
 ('5 CD8 T cells', 'IFN-g+ CD8 vs H1N1', 'S14-A H1N1', None, False),
 ('5 CD8 T cells', 'IFN-g+ CD8 vs H3N2', 'S14-A H3N2', None, False),
 ('5 CD8 T cells', 'Lung resident-memory CD8, day 25', 'S05-I', None, False),
]
rows = []
for step, label, b, lvl, inv in spec:
    a2, a3, y2 = vals(b, lvl, 'PSLN-212'), vals(b, lvl, 'PSLN-344'), vals(b, lvl, 'PSLN-212(Y)')
    islog = b in LOGB
    tr = (lambda v: np.log10(v)) if islog else (lambda v: v)
    def pct(a, y):
        if islog: r = 10 ** (np.mean(np.log10(a)) - np.mean(np.log10(y)))
        else: r = np.mean(a) / np.mean(y)
        return 100 * (1 / r if inv else r)
    p2, p3 = pct(a2, y2), pct(a3, y2)
    bs = np.array([pct(rng.choice(a3, len(a3)), rng.choice(y2, len(y2))) for _ in range(10000)]); lo, hi = np.percentile(bs, [2.5, 97.5])
    cen = (lambda v: 10 ** np.mean(np.log10(v))) if islog else np.mean
    rows.append(dict(step=step, label=label, block=b, level=lvl or '', inverted=inv, scale='geometric mean' if islog else 'mean',
                     aged212=cen(a2), aged344=cen(a3), young212=cen(y2), n=f'{len(a2)}/{len(a3)}/{len(y2)}',
                     fold_344_vs_212_aged=cen(a3) / cen(a2), aged212_pct_of_young=p2, aged344_pct_of_young=p3, pct_lo=lo, pct_hi=hi,
                     p_welch_344_vs_212=stats.ttest_ind(tr(a3), tr(a2), equal_var=False).pvalue,
                     p_mwu_344_vs_212=stats.mannwhitneyu(a3, a2, method='exact').pvalue,
                     p_welch_344_vs_young=stats.ttest_ind(tr(a3), tr(y2), equal_var=False).pvalue,
                     all_344_above_all_212=bool((a3.min() > a2.max()) if not inv else (a3.max() < a2.min()))))
# recomputed IgG2a:IgG1 (S13-A/S13-B and S13-C/S13-D)
for lab, nb, db in [('IgG2a:IgG1 anti-H1N1 (recomputed S13-A/S13-B)', 'S13-A', 'S13-B'), ('IgG2a:IgG1 anti-H3N2 (recomputed S13-C/S13-D)', 'S13-C', 'S13-D')]:
    r = {g: vals(nb, None, g) / vals(db, None, g) for g in ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']}
    a2, a3, y2 = r['PSLN-212'], r['PSLN-344'], r['PSLN-212(Y)']
    bs = np.array([100 * np.mean(rng.choice(a3, 5)) / np.mean(rng.choice(y2, 5)) for _ in range(10000)]); lo, hi = np.percentile(bs, [2.5, 97.5])
    rows.append(dict(step='4 Germinal centre / antibody', label=lab, block=f'{nb}/{db}', level='', inverted=False, scale='mean of per-animal ratios',
                     aged212=a2.mean(), aged344=a3.mean(), young212=y2.mean(), n='5/5/5', fold_344_vs_212_aged=a3.mean() / a2.mean(),
                     aged212_pct_of_young=100 * a2.mean() / y2.mean(), aged344_pct_of_young=100 * a3.mean() / y2.mean(), pct_lo=lo, pct_hi=hi,
                     p_welch_344_vs_212=stats.ttest_ind(a3, a2, equal_var=False).pvalue, p_mwu_344_vs_212=stats.mannwhitneyu(a3, a2, method='exact').pvalue,
                     p_welch_344_vs_young=stats.ttest_ind(a3, y2, equal_var=False).pvalue, all_344_above_all_212=bool(a3.min() > a2.max())))
# survival rows (pooled, survival tables as printed)
def tot(blocks, g):
    d = sv[sv.block.isin(blocks) & (sv.group == g)]; return int((d.event == 0).sum()), len(d)
for lab, blocks in [('Survival, heterosubtypic challenge d3/d14 (4 expts pooled)', ['S06-A', 'S06-B', 'S06-C', 'S06-D']),
                    ('Survival, heterosubtypic challenge d60 (3 expts pooled)', ['S06-E', 'S06-F', 'S06-G'])]:
    (s2, n2), (s3, n3), (sy, ny) = tot(blocks, 'PSLN-212'), tot(blocks, 'PSLN-344'), tot(blocks, 'PSLN-212(Y)')
    lo = stats.beta.ppf(0.025, s3, n3 - s3 + 1) if s3 else 0; hi = stats.beta.ppf(0.975, s3 + 1, n3 - s3) if s3 < n3 else 1
    rows.append(dict(step='6 Protection', label=lab, block='+'.join(blocks), level='', inverted=False, scale='proportion surviving',
                     aged212=s2 / n2, aged344=s3 / n3, young212=sy / ny, n=f'{n2}/{n3}/{ny}', fold_344_vs_212_aged=(s3 / n3) / (s2 / n2) if s2 else np.nan,
                     aged212_pct_of_young=100 * (s2 / n2) / (sy / ny), aged344_pct_of_young=100 * (s3 / n3) / (sy / ny), pct_lo=100 * lo, pct_hi=100 * hi,
                     p_welch_344_vs_212=np.nan, p_mwu_344_vs_212=stats.fisher_exact([[s3, n3 - s3], [s2, n2 - s2]])[1], p_welch_344_vs_young=np.nan,
                     all_344_above_all_212=np.nan))
order = {s: i for i, s in enumerate(['1 Innate sensing', '2 Monocyte -> DC', '3 Regulatory brake (inverted)', '4 Germinal centre / antibody', '5 CD8 T cells', '6 Protection'])}
out = pd.DataFrame(rows); out['o'] = out.step.map(order); out = out.sort_values('o', kind='stable').drop(columns='o')
out.to_csv(os.path.join(T, 'T07_restoration_index_curated.csv'), index=False)
pd.set_option('display.width', 260); pd.set_option('display.max_rows', 200); pd.set_option('display.max_colwidth', 50); pd.options.display.float_format = '{:.3g}'.format
print(out.drop(columns=['step', 'scale', 'level', 'inverted']).to_string())
x = out[~out.step.str.startswith('6')]
print('\nendpoints:', len(x), '| 344 > 212 with exact MWU p<0.05:', int((x.p_mwu_344_vs_212 < 0.05).sum()), '| complete separation of all animals:', int(x.all_344_above_all_212.sum()))
print('median aged212 % of young:', round(x.aged212_pct_of_young.median(), 1), '| median aged344 % of young:', round(x.aged344_pct_of_young.median(), 1),
      '| range 344:', round(x.aged344_pct_of_young.min(), 1), '-', round(x.aged344_pct_of_young.max(), 1))
