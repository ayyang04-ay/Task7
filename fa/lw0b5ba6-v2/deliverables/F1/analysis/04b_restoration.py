"""Restoration table: for every read-out that has Sham / PSLN-212 / PSLN-344 (aged) and PSLN-212(Y) (young benchmark)
   fold(344 vs 212, aged), % of young benchmark reached by 344 and by 212, and the Tukey p-values of the three key contrasts."""
import numpy as np, pandas as pd
pd.set_option('display.width', 280); pd.set_option('display.max_rows', 900); pd.set_option('display.max_colwidth', 70)
S = pd.read_csv('../tables/T4_group_summaries.csv'); P = pd.read_csv('../tables/T5_pairwise_tests.csv')

def pv(block, a, b, x=None, col='p'):
    q = P[(P.block == block) & (((P.g1 == a) & (P.g2 == b)) | ((P.g1 == b) & (P.g2 == a)))]
    if x is not None:
        q = q[q.x == x]
    else:
        q = q[q.x.isna()]
    if q.empty or col not in q or q[col].isna().all():
        return np.nan
    return float(q[col].iloc[0])

rows = []
def add(block, x=None, label=None, ynames=('PSLN-212(Y)', 'PSLN-212Y', 'PSLN-212(y)')):
    s = S[S.block == block]
    s = s[s.x == x] if x is not None else s[s.x.isna()]
    g = s.set_index('group')
    yn = next((y for y in ynames if y in g.index), None)
    use_gmt = 'gmt' in g and g['gmt'].notna().any()
    val = (lambda k: g.loc[k, 'gmt'] if use_gmt else g.loc[k, 'mean']) if True else None
    r = dict(block=block + (f' (x={x:g})' if x is not None else ''), readout=label or g['measurand'].iloc[0], stat='GMT' if use_gmt else 'mean', n=int(g['n'].iloc[0]))
    for k, nm in [('Sham', 'sham'), ('Vaccine', 'sham'), ('PSLN-212', 'a212'), ('PSLN-344', 'a344'), (yn, 'y212'), ('PSLN-344(Y)', 'y344')]:
        if k in g.index:
            r[nm] = val(k)
    if 'a212' in r and 'a344' in r:
        r['fold_344_vs_212'] = r['a344'] / r['a212']
    if 'y212' in r:
        if 'a344' in r: r['a344_pct_of_young'] = 100 * r['a344'] / r['y212']
        if 'a212' in r: r['a212_pct_of_young'] = 100 * r['a212'] / r['y212']
    pcol = 'p_log' if use_gmt else 'p'
    r['p_344_vs_212'] = pv(block, 'PSLN-344', 'PSLN-212', x, pcol)
    if yn: r['p_344_vs_young'] = pv(block, 'PSLN-344', yn, x, pcol)
    shamname = 'Sham' if 'Sham' in g.index else ('Vaccine' if 'Vaccine' in g.index else None)
    if shamname:
        r['p_212_vs_sham'] = pv(block, 'PSLN-212', shamname, x, pcol)
        r['p_344_vs_sham'] = pv(block, 'PSLN-344', shamname, x, pcol)
    r['p_scale'] = 'Tukey on log2 titres' if use_gmt else 'Tukey (linear)'
    rows.append(r)

for b, lab in [('S01-A 16h', 'Ifnb1 lung 16 h (fold)'), ('S01-A 72h', 'Ifnb1 lung 72 h (fold)')]:
    add(b, label=lab)
add('S02-F', 16, 'Gm-csf lung 16 h (fold)'); add('S02-F', 36, 'Gm-csf lung 36 h (fold)'); add('S02-F', 72, 'Gm-csf lung 72 h (fold)')
add('S01-D', 4, '% lung monocytes d4'); add('S01-D', 8, '% lung monocytes d8')
add('S01-E', 4, '% lung CD11b+ DC d4'); add('S01-E', 8, '% lung CD11b+ DC d8')
add('S01-F', label='% lung cDC1 72 h'); add('S01-G', label='% lung cDC2 72 h')
add('S02-A', label='% CCR7+ lung CD11b+ DC 72 h'); add('S02-B', label='% MLN CD11b+CD103- DC 72 h'); add('S02-C', label='% OVA+ MLN DC 36 h')
add('S02-D CD40', label='% CD40+ MLN CD11b+ DC d3'); add('S02-D CD86', label='% CD86+ MLN CD11b+ DC d3'); add('S02-E', label='OT-I proliferation by MLN DC (%)')
add('S11-E', label='% CD206+ lung macrophages')
add('S05-D', label='% Ki-67+ lung CD8 d3'); add('S05-E', label='% GZMB+ lung CD8 d3')
add('S05-F', label='% IFN-g+ CD8 MLN d14 (rgH5N1 restim)'); add('S14-A H1N1', label='% IFN-g+ CD8 MLN (H1N1 restim)'); add('S14-A H3N2', label='% IFN-g+ CD8 MLN (H3N2 restim)')
add('S05-G', label='% IFN-g+ CD8 MLN d60'); add('S05-H', label='% GZMB+ CD8 MLN d60'); add('S05-I', label='% lung CD8 TRM d25')
add('S03-K', label='% GC B cells MLN d7'); add('S04-A ICOShi', label='% Tfh ICOS-hi MLN d7'); add('S04-A ICOSlo', label='% Tfh ICOS-lo MLN d7')
add('S04-B Foxp3', label='% Tfr (Foxp3+ of CXCR5+) d7'); add('S04-C', label='% Tfr d30'); add('S04-D', label='% lung Treg d7'); add('S13-H', label='% IgG+ MLN B cells')
add('S03-A', label='IgG anti-H1N1 d14'); add('S03-E', label='IgG anti-H3N2 d14'); add('S03-C', label='HAI H1N1 d14'); add('S03-G', label='HAI H3N2 d14')
add('S03-D', label='Neutralising H1N1 d14'); add('S03-H', label='Neutralising H3N2 d14')
add('S13-A', label='IgG2a anti-H1N1 d14'); add('S13-B', label='IgG1 anti-H1N1 d14'); add('S13-C', label='IgG2a anti-H3N2 d14'); add('S13-D', label='IgG1 anti-H3N2 d14')
add('S13-I', label='IgG anti-H1N1 d28 (boost d14)'); add('S13-J', label='IgG anti-H3N2 d28 (boost d14)')
R = pd.DataFrame(rows)
R.to_csv('../tables/T7_restoration_table.csv', index=False)
show = R[['block', 'readout', 'stat', 'n', 'sham', 'a212', 'a344', 'y212', 'fold_344_vs_212', 'a212_pct_of_young', 'a344_pct_of_young', 'p_344_vs_212', 'p_344_vs_young', 'p_212_vs_sham']]
print(show.to_string(index=False, float_format=lambda v: (f'{v:.1e}' if (abs(v) < 1e-3 and v != 0) else f'{v:.3g}')))
up = R[~R.readout.str.contains('Tfr|Treg|CD206|cDC2|72 h \(fold\)')]
print('\nmedian %% of young benchmark reached (up-regulated read-outs): PSLN-344 %.0f%% (IQR %.0f-%.0f), PSLN-212 %.0f%% (IQR %.0f-%.0f), n read-outs = %d' % (
    up.a344_pct_of_young.median(), up.a344_pct_of_young.quantile(.25), up.a344_pct_of_young.quantile(.75),
    up.a212_pct_of_young.median(), up.a212_pct_of_young.quantile(.25), up.a212_pct_of_young.quantile(.75), up.a344_pct_of_young.notna().sum()))
