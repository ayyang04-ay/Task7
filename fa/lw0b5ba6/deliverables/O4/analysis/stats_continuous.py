import pandas as pd, numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from blocks import BLOCKS

c = pd.read_csv('tidy_continuous.csv')
c['level'] = c['level'].fillna('').astype(str)
# S07-C: both columns carry the same printed label -> keep column identity
m = c.block == 'S07-C'
c.loc[m, 'group'] = c.loc[m, 'cell'].str.extract(r'!([A-Z]+)\d+')[0].map({'B': 'colB "Ly6C-CD206+ MΦ"', 'C': 'colC "Ly6C-CD206+ MΦ"'})

LOG_SCALES = {'titer', 'hai', 'fold', 'ratio', 'log10'}
def to_analysis(v, scale):
    v = np.asarray(v, float)
    if scale == 'hai':
        v = np.where(v <= 0, 5.0, v)           # <1:10 (recorded as 0) -> 5 (half the lowest dilution)
        return np.log2(v)
    if scale in ('titer', 'fold', 'ratio'):
        return np.log2(v)
    if scale == 'log10':
        return v * np.log2(10)                 # convert log10 to log2 units
    return v

def hedges_g(a, b):
    na, nb = len(a), len(b)
    if na < 2 or nb < 2: return np.nan
    sp = np.sqrt(((na - 1) * np.var(a, ddof=1) + (nb - 1) * np.var(b, ddof=1)) / (na + nb - 2))
    if sp == 0: return np.nan
    d = (np.mean(a) - np.mean(b)) / sp
    J = 1 - 3 / (4 * (na + nb) - 9)
    return d * J

def welch(a, b):
    if len(a) < 2 or len(b) < 2: return np.nan, (np.nan, np.nan)
    t = stats.ttest_ind(a, b, equal_var=False)
    # CI for difference in means (Welch)
    va, vb = np.var(a, ddof=1) / len(a), np.var(b, ddof=1) / len(b)
    se = np.sqrt(va + vb)
    if se == 0: return np.nan, (np.nan, np.nan)
    df = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))
    q = stats.t.ppf(0.975, df)
    d = np.mean(a) - np.mean(b)
    return t.pvalue, (d - q * se, d + q * se)

summ, contr, tuk = [], [], []
CONTRASTS = [('PSLN-344', 'PSLN-212', 'Mn effect in aged (PSLN-344 vs PSLN-212, aged)'),
             ('PSLN-344', 'Sham', 'Adjuvant vs vehicle (PSLN-344 vs Sham, aged)'),
             ('PSLN-344', 'Vaccine', 'Adjuvant vs vaccine alone (aged)'),
             ('PSLN-344', 'PBS', 'PSLN-344 vs PBS'),
             ('PSLN-344', 'PSLN-212(Y)', 'Aged PSLN-344 vs young PSLN-212 (benchmark)'),
             ('PSLN-212', 'PSLN-212(Y)', 'Age deficit with PSLN-212 (aged vs young)'),
             ('PSLN-344(Y)', 'PSLN-212(Y)', 'Mn effect in young'),
             ('PSLN-344', 'CMP-204', 'PSLN-344 vs cGAMP benchmark (CMP-204), aged'),
             ('PSLN-344', 'CT', 'PSLN-344 vs cholera toxin'),
             ('PSLN-344', 'PSLN-212/R848', 'PSLN-344 vs CDN+R848 combination')]
for (blk, lvl), d in c.groupby(['block', 'level'], sort=False):
    scale = BLOCKS[blk]['scale']
    groups = {g: x.value.values for g, x in d.groupby('group', sort=False)}
    cells = {g: f"{x.cell.iloc[0]}:{x.cell.iloc[-1].split('!')[1]}" for g, x in d.groupby('group', sort=False)}
    for g, v in groups.items():
        a = to_analysis(v, scale)
        row = dict(block=blk, level=lvl, measurand=BLOCKS[blk]['measurand'], scale=scale, group=g, n=len(v),
                   mean=np.mean(v), sd=np.std(v, ddof=1) if len(v) > 1 else np.nan, median=np.median(v),
                   min=np.min(v), max=np.max(v), cells=cells[g])
        if scale in ('titer', 'hai', 'fold', 'ratio'):
            row['geo_mean'] = 2 ** np.mean(a)
            se = np.std(a, ddof=1) / np.sqrt(len(a)) if len(a) > 1 else np.nan
            tq = stats.t.ppf(0.975, len(a) - 1) if len(a) > 1 else np.nan
            row['geo_mean_95CI'] = f"{2 ** (np.mean(a) - tq * se):.3g}-{2 ** (np.mean(a) + tq * se):.3g}" if len(a) > 1 else ''
        if scale == 'log10':
            row['geo_mean'] = 10 ** np.mean(v)
        if scale == 'hai':
            row['n_ge_40'] = int((np.asarray(v) >= 40).sum())
        summ.append(row)
    for g1, g2, lab in CONTRASTS:
        if g1 in groups and g2 in groups:
            a1, a2 = to_analysis(groups[g1], scale), to_analysis(groups[g2], scale)
            p, ci = welch(a1, a2)
            diff = np.mean(a1) - np.mean(a2)
            if scale in LOG_SCALES:
                eff = 2 ** diff; eff_ci = (2 ** ci[0], 2 ** ci[1]); etype = 'fold (geometric)'
            else:
                eff = diff; eff_ci = ci; etype = 'difference (percentage points or units)'
            contr.append(dict(block=blk, level=lvl, measurand=BLOCKS[blk]['measurand'], contrast=lab, g1=g1, g2=g2,
                              n1=len(a1), n2=len(a2), mean1=np.mean(groups[g1]), mean2=np.mean(groups[g2]),
                              effect=eff, effect_type=etype, ci_low=eff_ci[0], ci_high=eff_ci[1],
                              hedges_g=hedges_g(a1, a2), p_welch=p,
                              p_mwu=stats.mannwhitneyu(a1, a2, alternative='two-sided').pvalue if len(a1) > 1 and len(a2) > 1 else np.nan))
    # restoration index: fraction of the age gap (PSLN-212 aged -> PSLN-212(Y)) closed by PSLN-344 (aged)
    if all(k in groups for k in ('PSLN-344', 'PSLN-212', 'PSLN-212(Y)')):
        m344, m212, mY = [np.mean(to_analysis(groups[k], scale)) for k in ('PSLN-344', 'PSLN-212', 'PSLN-212(Y)')]
        ri = (m344 - m212) / (mY - m212) if (mY - m212) != 0 else np.nan
        contr.append(dict(block=blk, level=lvl, measurand=BLOCKS[blk]['measurand'], contrast='Restoration index (fraction of aged-vs-young gap closed by PSLN-344; analysis scale)',
                          g1='PSLN-344', g2='PSLN-212 -> PSLN-212(Y)', effect=ri, effect_type='fraction'))
    # Tukey HSD (stated method) on analysis scale
    if len(groups) >= 3 and all(len(v) >= 2 for v in groups.values()):
        vals = np.concatenate([to_analysis(v, scale) for v in groups.values()])
        labs = np.concatenate([[g] * len(v) for g, v in groups.items()])
        try:
            res = pairwise_tukeyhsd(vals, labs)
            tb = pd.DataFrame(res.summary().data[1:], columns=res.summary().data[0])
            tb.insert(0, 'level', lvl); tb.insert(0, 'block', blk)
            tuk.append(tb)
        except Exception as e:
            print('tukey fail', blk, lvl, e)

S = pd.DataFrame(summ); C = pd.DataFrame(contr); T = pd.concat(tuk)
# FDR across all primary Mn-effect contrasts and across all contrasts
mask = C.p_welch.notna()
C.loc[mask, 'q_BH_all_contrasts'] = multipletests(C.loc[mask, 'p_welch'], method='fdr_bh')[1]
S.to_csv('block_group_summary.csv', index=False)
C.to_csv('block_contrasts.csv', index=False)
T.to_csv('block_tukey_hsd.csv', index=False)
pd.set_option('display.width', 320); pd.set_option('display.max_rows', 500); pd.set_option('display.max_colwidth', 60)
key = C[C.contrast.str.startswith('Mn effect in aged')][['block', 'level', 'measurand', 'mean1', 'mean2', 'effect', 'effect_type', 'ci_low', 'ci_high', 'hedges_g', 'p_welch', 'q_BH_all_contrasts']]
print(key.to_string())
print()
ri = C[C.contrast.str.startswith('Restoration')][['block', 'level', 'measurand', 'effect']]
print(ri.to_string())
