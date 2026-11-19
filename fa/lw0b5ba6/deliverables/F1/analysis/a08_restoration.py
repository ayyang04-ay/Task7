"""
(1) Restoration index: how far does PSLN-344 move AGED animals from the aged PSLN-212 level towards the YOUNG PSLN-212 benchmark?
       RI = (m344 - m212) / (mY - m212)      0 = no better than PSLN-212 in aged; 1 = equal to the young benchmark
    computed on log10 scale for titres / fold-changes / ratios, linear for percentages; 95% CI by bootstrap (animals resampled within group).
(2) Biomarker triage: does the readout separate regimens that protect (aged PSLN-344, young PSLN-212) from regimens that do not
    (Sham/vaccine-only, aged PSLN-212)?  ROC AUC at the animal level + the largest non-protective value / smallest protective value.
    NOTE: biomarkers and survival were measured in different animals, so this is regimen-level separation, not an individual correlate.
"""
from paths import TABLES, FIGS, OUT as OUTDIR, BUILD, PANDOC
import pandas as pd, numpy as np, math, warnings
from scipy import stats
import psln_blocks as pb
warnings.filterwarnings('ignore')
pd.set_option('display.width', 300); pd.set_option('display.max_rows', 4000); pd.set_option('display.max_colwidth', 60)
df = pb.tidy()
rng = np.random.default_rng(20261101)

def vals(block, group, analyte=None, x=None):
    t = df[(df.block == block) & (df.group == group)]
    if analyte is not None: t = t[t.analyte.str.contains(analyte, regex=False)]
    if x is not None: t = t[t.x.astype(str) == str(x)]
    return t.sort_values('rep').value.to_numpy(float)

# endpoint list: (domain, label, block, analyte filter, x, scale, direction[+1 higher=young-like], accessible matrix)
E = [
 ('1 Innate sensing',      'Ifnb1 lung 16 h',                       'S01-A', 'Ifnb1 lung 16h', '16h', 'log', 'lung tissue (clin. analogue: nasal/BAL ISG, serum CXCL10)'),
 ('2 Monocyte/DC',         'Lung monocytes, peak d4',               'S01-D', None, 4, 'lin', 'lung'),
 ('2 Monocyte/DC',         'Lung CD11b+ DC, peak d4',               'S01-E', None, 4, 'lin', 'lung'),
 ('2 Monocyte/DC',         'Lung cDC1 72 h',                        'S01-F', None, None, 'lin', 'lung'),
 ('2 Monocyte/DC',         'Lung cDC2 72 h (falls in young)',       'S01-G', None, None, 'lin', 'lung'),
 ('2 Monocyte/DC',         'Lung CCR7+ migratory DC 72 h',          'S02-A', None, None, 'lin', 'lung'),
 ('2 Monocyte/DC',         'MLN CD11b+ DC 72 h',                    'S02-B', None, None, 'lin', 'lymph node'),
 ('2 Monocyte/DC',         'MLN antigen(OVA)+ DC 36 h',             'S02-C', None, None, 'lin', 'lymph node'),
 ('2 Monocyte/DC',         'DC CD40+ d3',                           'S02-D CD40', None, None, 'lin', 'lymph node'),
 ('2 Monocyte/DC',         'DC CD86+ d3',                           'S02-D CD86', None, None, 'lin', 'lymph node'),
 ('2 Monocyte/DC',         'DC cross-priming of OT-I',              'S02-E', None, None, 'lin', 'ex vivo'),
 ('3 GC / Tfh',            'GC B cells d7',                         'S03-K', None, None, 'lin', 'lymph node'),
 ('3 GC / Tfh',            'Tfh ICOS-high d7',                      'S04-A', 'ICOS-high', None, 'lin', 'lymph node (clin.: circulating Tfh)'),
 ('3 GC / Tfh',            'Tfh ICOS-low d7',                       'S04-A', 'ICOS-low', None, 'lin', 'lymph node'),
 ('3 GC / Tfh',            'Tfr d7 (lower = young-like)',           'S04-B Foxp3+', None, None, 'lin', 'lymph node'),
 ('3 GC / Tfh',            'Tfh:Tfr ratio d7',                      'S04-B Tfh:Tfr', None, None, 'log', 'lymph node'),
 ('3 GC / Tfh',            'Tfr d30 (lower = young-like)',          'S04-C', None, None, 'lin', 'lymph node'),
 ('3 GC / Tfh',            'IgG+ B cells in MLN',                   'S13-H', None, None, 'lin', 'lymph node'),
 ('4 Antibody',            'IgG anti-CA09 d14',                     'S03-A', None, None, 'log', 'serum'),
 ('4 Antibody',            'IgG anti-Aichi d14',                    'S03-E', None, None, 'log', 'serum'),
 ('4 Antibody',            'HAI anti-CA09 d14',                     'S03-C', None, None, 'log', 'serum'),
 ('4 Antibody',            'HAI anti-Aichi d14',                    'S03-G', None, None, 'log', 'serum'),
 ('4 Antibody',            'Neutralising anti-CA09 d14',            'S03-D', None, None, 'log', 'serum'),
 ('4 Antibody',            'Neutralising anti-Aichi d14',           'S03-H', None, None, 'log', 'serum'),
 ('4 Antibody',            'IgG2a anti-CA09 d14',                   'S13-A', None, None, 'log', 'serum'),
 ('4 Antibody',            'IgG1 anti-CA09 d14',                    'S13-B', None, None, 'log', 'serum'),
 ('4 Antibody',            'IgG2a anti-Aichi d14',                  'S13-C', None, None, 'log', 'serum'),
 ('4 Antibody',            'IgG1 anti-Aichi d14',                   'S13-D', None, None, 'log', 'serum'),
 ('4 Antibody',            'IgG anti-CA09 d28 post-boost',          'S13-I', None, None, 'log', 'serum'),
 ('4 Antibody',            'IgG anti-Aichi d28 post-boost',         'S13-J', None, None, 'log', 'serum'),
 ('5 CD8 T cell',          'Lung Ki-67+ CD8 d3',                    'S05-D', None, None, 'lin', 'lung'),
 ('5 CD8 T cell',          'Lung GZMB+ CD8 d3',                     'S05-E', None, None, 'lin', 'lung'),
 ('5 CD8 T cell',          'IFNg+ CD8, rgH5N1 restim d14',          'S05-F', None, None, 'lin', 'lymph node (clin.: PBMC ELISpot)'),
 ('5 CD8 T cell',          'IFNg+ CD8, rgH5N1 restim d60',          'S05-G', None, None, 'lin', 'lymph node (clin.: PBMC ELISpot)'),
 ('5 CD8 T cell',          'MLN GZMB+ CD8 d60',                     'S05-H', None, None, 'lin', 'lymph node'),
 ('5 CD8 T cell',          'Lung TRM CD8 d25',                      'S05-I', None, None, 'lin', 'lung'),
 ('5 CD8 T cell',          'IFNg+ CD8, CA09 restim',                'S14-A H1N1', None, None, 'lin', 'lymph node (clin.: PBMC ELISpot)'),
 ('5 CD8 T cell',          'IFNg+ CD8, Aichi restim',               'S14-A H3N2', None, None, 'lin', 'lymph node (clin.: PBMC ELISpot)'),
 ('6 Regulatory milieu',   'Lung CD206+ macrophages (lower = young-like)', 'S11-E', None, None, 'lin', 'lung'),
 ('6 Regulatory milieu',   'Lung Treg d7 (lower = young-like)',     'S04-D', None, None, 'lin', 'lung'),
]
rows = []
for dom, lab, blk, an, x, sc, matrix in E:
    a = vals(blk, 'PSLN-212', an, x); m = vals(blk, 'PSLN-344', an, x); y = vals(blk, 'PSLN-212(Y)', an, x)
    c = vals(blk, 'Sham', an, x)
    if len(c) == 0: c = vals(blk, 'Vaccine', an, x)
    tr = (lambda v: np.log10(np.where(v <= 0, 5.0, v))) if sc == 'log' else (lambda v: v)
    A, M, Y = tr(a), tr(m), tr(y)
    ri = (M.mean() - A.mean()) / (Y.mean() - A.mean())
    bs = []
    for _ in range(10000):
        aa = rng.choice(A, len(A)); mm = rng.choice(M, len(M)); yy = rng.choice(Y, len(Y))
        den = yy.mean() - aa.mean()
        if abs(den) > 1e-12: bs.append((mm.mean() - aa.mean()) / den)
    lo, hi = np.percentile(bs, [2.5, 97.5])
    # gap to young: Welch test PSLN-344 vs Y
    p_gap = stats.ttest_ind(M, Y, equal_var=False).pvalue
    p_mn = stats.ttest_ind(M, A, equal_var=False).pvalue
    # separation protected (M, Y) vs unprotected (A, C)
    prot = np.concatenate([M, Y]); unprot = np.concatenate([A, tr(c)]) if len(c) else A
    sign = 1 if Y.mean() > A.mean() else -1
    U = stats.mannwhitneyu(sign * prot, sign * unprot, alternative='greater').statistic
    auc = U / (len(prot) * len(unprot))
    inv = (lambda v: 10 ** v) if sc == 'log' else (lambda v: v)
    worst_prot = inv(min(sign * prot) * sign); best_unprot = inv(max(sign * unprot) * sign)
    fmt = (lambda v: 10 ** v.mean()) if sc == 'log' else (lambda v: v.mean())
    rows.append(dict(domain=dom, endpoint=lab, block=blk, scale='geometric mean' if sc == 'log' else 'mean',
                     sham_or_vaccine=fmt(tr(c)) if len(c) else np.nan, aged_PSLN212=fmt(A), aged_PSLN344=fmt(M), young_PSLN212=fmt(Y),
                     n=f'{len(a)}/{len(m)}/{len(y)}', fold_344_vs_212=(10 ** (M.mean() - A.mean())) if sc == 'log' else m.mean() / a.mean(),
                     p_344_vs_212=p_mn, pct_of_young=100 * ((10 ** (M.mean() - Y.mean())) if sc == 'log' else m.mean() / y.mean()), p_344_vs_young=p_gap,
                     restoration_index=ri, RI_lo=lo, RI_hi=hi, AUC_protective_vs_not=auc,
                     complete_separation=bool(min(sign * prot) > max(sign * unprot)),
                     weakest_protective_value=worst_prot, strongest_nonprotective_value=best_unprot, matrix=matrix))
R = pd.DataFrame(rows)
R.to_csv(TABLES + 'T11_restoration_and_biomarker_triage.csv', index=False)
print(R[['domain', 'endpoint', 'block', 'sham_or_vaccine', 'aged_PSLN212', 'aged_PSLN344', 'young_PSLN212', 'fold_344_vs_212', 'p_344_vs_212', 'pct_of_young', 'p_344_vs_young',
         'restoration_index', 'RI_lo', 'RI_hi']].round(3).to_string())
print()
print(R[['endpoint', 'block', 'AUC_protective_vs_not', 'complete_separation', 'weakest_protective_value', 'strongest_nonprotective_value', 'matrix']].round(3).to_string())
print('\nRestoration index by domain (median, range):')
print(R.groupby('domain').restoration_index.agg(['median', 'min', 'max', 'count']).round(2))
print('overall median RI', R.restoration_index.median().round(3), ' n endpoints', len(R), '; endpoints where PSLN-344 aged is still significantly below/above young (p<0.05):', int((R.p_344_vs_young < 0.05).sum()))
