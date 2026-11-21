"""Candidate biomarkers: does each read-out separate aged PSLN-344 from aged PSLN-212 animal-by-animal, and does it rank the four
groups in the same order as survival (sham < aged-212 < aged-344 <= young-212)?  Hypothesis-generating only: n = 3-5 per group and
every assay is terminal, so no animal has both a biomarker value and a challenge outcome."""
import numpy as np, pandas as pd
from scipy import stats
import tidy
idx = pd.read_csv('../data_tidy/psln_block_index.csv').set_index('block')
cands = [('S01-A 16h', None, 'Lung Ifnb1 mRNA, 16 h (fold)', 'PD / target engagement', 'up'), ('S02-F', 16, 'Lung Gm-csf mRNA, 16 h (fold)', 'PD / target engagement', 'up'), ('S02-F', 36, 'Lung Gm-csf mRNA, 36 h (fold)', 'PD / target engagement', 'up'),
         ('S01-D', 4, '% lung monocytes, day 4', 'Mechanism: recruitment', 'up'), ('S01-E', 4, '% lung CD11b+ DC, day 4', 'Mechanism: moDC', 'up'), ('S01-F', None, '% lung cDC1, 72 h', 'Mechanism: DC', 'up'),
         ('S02-A', None, '% CCR7+ of lung CD11b+ DC, 72 h', 'Mechanism: DC migration', 'up'), ('S02-C', None, '% antigen+ MLN DC, 36 h', 'Mechanism: antigen transport', 'up'),
         ('S02-D CD40', None, '% CD40+ MLN DC, day 3', 'Mechanism: DC activation', 'up'), ('S02-D CD86', None, '% CD86+ MLN DC, day 3', 'Mechanism: DC activation', 'up'),
         ('S11-E', None, '% CD206+ lung macrophages', 'Mechanism: suppressive milieu', 'down'), ('S04-B Foxp3', None, '% Tfr of CXCR5+ CD4, day 7', 'Mechanism: suppressive milieu', 'down'), ('S04-D', None, '% lung Treg, day 7', 'Mechanism: suppressive milieu', 'down'),
         ('S05-D', None, '% Ki-67+ lung CD8, day 3', 'Early cellular response', 'up'), ('S05-E', None, '% GZMB+ lung CD8, day 3', 'Early cellular response', 'up'),
         ('S04-A ICOShi', None, '% ICOS-hi Tfh, day 7', 'Humoral precursor', 'up'), ('S03-K', None, '% GC B cells, day 7', 'Humoral precursor', 'up'),
         ('S03-C', None, 'HAI titre H1N1, day 14', 'Immunogenicity', 'up'), ('S03-G', None, 'HAI titre H3N2, day 14', 'Immunogenicity', 'up'), ('S03-D', None, 'Neutralising titre H1N1, day 14', 'Immunogenicity', 'up'), ('S03-H', None, 'Neutralising titre H3N2, day 14', 'Immunogenicity', 'up'),
         ('S03-A', None, 'IgG titre H1N1, day 14', 'Immunogenicity', 'up'), ('S13-A', None, 'IgG2a titre H1N1, day 14', 'Immunogenicity (Th1-type)', 'up'),
         ('S05-F', None, '% IFN-γ+ CD8 (rgH5N1 restim), day 14', 'Cross-reactive T cells', 'up'), ('S14-A H1N1', None, '% IFN-γ+ CD8 (H1N1 restim)', 'Cross-reactive T cells', 'up'), ('S05-I', None, '% lung CD8 TRM, day 25', 'Tissue memory', 'up'), ('S05-G', None, '% IFN-γ+ CD8, day 60', 'Memory', 'up')]
rows = []
for b, x, lab, role, direction in cands:
    g = {k: tidy.vec(b, k, x) for k in tidy.groups(b)}
    a, c = g['PSLN-344'], g['PSLN-212']
    sham = g.get('Sham', g.get('Vaccine')); yk = next((k for k in ['PSLN-212(Y)', 'PSLN-212Y'] if k in g), None); y = g.get(yk) if yk else None
    if direction == 'up':
        sep = a.min() > c.max(); thr = np.sqrt(a.min() * c.max()) if sep else np.nan; gap = a.min() / c.max()
    else:
        sep = a.max() < c.min(); thr = np.sqrt(a.max() * c.min()) if sep else np.nan; gap = c.min() / a.max()
    means = [v.mean() for v in [sham, c, a, y] if v is not None]
    mono = all(np.diff(means) > 0) if direction == 'up' else all(np.diff(means) < 0)
    u = stats.mannwhitneyu(a, c, alternative='two-sided').pvalue
    rows.append(dict(block=b + (f' (x={x:g})' if x is not None else ''), biomarker=lab, role=role, n_per_group=len(a), mean_sham=sham.mean() if sham is not None else np.nan, mean_aged212=c.mean(), mean_aged344=a.mean(),
                     mean_young212=y.mean() if y is not None else np.nan, fold_344_vs_212=a.mean() / c.mean(), range_aged212=f'{c.min():g}–{c.max():g}', range_aged344=f'{a.min():g}–{a.max():g}',
                     complete_separation=bool(sep), separation_margin_fold=gap, candidate_cutoff=thr, ranks_like_survival=bool(mono), mwu_p=u))
B = pd.DataFrame(rows); B.to_csv('../tables/T13_biomarker_separation.csv', index=False)
pd.set_option('display.width', 260); pd.set_option('display.max_colwidth', 45)
print(B[['block', 'biomarker', 'n_per_group', 'mean_aged212', 'mean_aged344', 'mean_young212', 'fold_344_vs_212', 'range_aged212', 'range_aged344', 'complete_separation', 'separation_margin_fold', 'candidate_cutoff', 'ranks_like_survival']].round(2).to_string(index=False))
print('complete separation:', B.complete_separation.sum(), 'of', len(B))
