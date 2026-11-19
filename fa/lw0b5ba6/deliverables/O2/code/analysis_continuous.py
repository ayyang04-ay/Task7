import pandas as pd, numpy as np, warnings
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
warnings.filterwarnings('ignore')
t = pd.read_csv('/tmp/work/tidy.csv')
t['time'] = t['time'].astype(str)

# readout specs: (label, block, filter(time/analyte), transform, floor_for_log, note)
SPECS = [
 # ---- innate / PD ----
 ('Ifnb1 lung 16h (fold)', 'S01-A_16h', None, 'log', None, ''),
 ('Ifnb1 lung 72h (fold)', 'S01-A_72h', None, 'log', None, ''),
 ('Ifnb1 lung 16h, 20ug dose arm of dose-response (fold)', 'S08-A', ('time', '20'), 'log', None, 'n=3'),
 ('Gm-csf lung 16h (fold)', 'S02-F', ('time', '16h'), 'log', None, ''),
 ('Gm-csf lung 36h (fold)', 'S02-F', ('time', '36h'), 'log', None, ''),
 ('Gm-csf lung 72h (fold)', 'S02-F', ('time', '72h'), 'log', None, ''),
 ('Ccl2 lung 16h (log10 fold)', 'S09-A_blk1(B:V)', ('analyte', 'Ccl2'), 'lin', None, 'already log10'),
 ('Il6 lung 16h (log10 fold)', 'S09-A_blk1(B:V)', ('analyte', 'Il6'), 'lin', None, 'already log10'),
 ('Tnf lung 16h (log10 fold)', 'S09-A_blk1(B:V)', ('analyte', 'Tnf'), 'lin', None, 'already log10'),
 ('Ccl3 lung 16h (log10 fold)', 'S09-A_blk1(B:V)', ('analyte', 'Ccl3'), 'lin', None, 'already log10'),
 ('Ccl5 lung 16h (log10 fold)', 'S09-A_blk1(B:V)', ('analyte', 'Ccl5'), 'lin', None, 'already log10'),
 ('Il10 lung 16h (log10 fold)', 'S09-A_blk1(B:V)', ('analyte', 'Il10'), 'lin', None, 'already log10'),
 ('Ifnb1 lung (log10) S09-A 2nd panel [labelled 16h]', 'S09-A_blk2(Y:AS)', ('analyte', 'Ifnb1'), 'lin', None, 'label conflict'),
 # ---- myeloid ----
 ('Lung monocytes d4 (%)', 'S01-D', ('time', '4'), 'lin', None, ''),
 ('Lung CD11b+ DC d4 (%)', 'S01-E', ('time', '4'), 'lin', None, ''),
 ('Lung cDC1 72h (%)', 'S01-F', None, 'lin', None, ''),
 ('Lung cDC2 72h (%)', 'S01-G', None, 'lin', None, ''),
 ('CCR7+ migratory CD11b+ DC 72h (%)', 'S02-A', None, 'lin', None, ''),
 ('MLN CD11b+CD103- DC 72h (%)', 'S02-B', None, 'lin', None, ''),
 ('MLN DC antigen(AF647-OVA)+ 36h (%)', 'S02-C', None, 'lin', None, ''),
 ('MLN CD11b+ DC CD40+ d3 (%)', 'S02-D_CD40', None, 'lin', None, ''),
 ('MLN CD11b+ DC CD86+ d3 (%)', 'S02-D_CD86', None, 'lin', None, ''),
 ('OT-I proliferation with MLN DC (%)', 'S02-E', None, 'lin', None, 'MHC caveat'),
 ('CD206+ lung macrophages (%)', 'S11-E', None, 'lin', None, 'timepoint not stated'),
 # ---- T follicular / B ----
 ('GC B cells MLN d7 (%)', 'S03-K', None, 'lin', None, ''),
 ('Aicda MLN B d5 (fold)', 'S03-L_Aicda', None, 'log', None, 'n=3'),
 ('E47 MLN B d5 (fold)', 'S03-L_E47', None, 'log', None, 'n=3'),
 ('ICOS-hi Tfh MLN d7 (%)', 'S04-A_ICOShi', None, 'lin', None, ''),
 ('ICOS-lo Tfh MLN d7 (%)', 'S04-A_ICOSlo', None, 'lin', None, ''),
 ('Tfr (Foxp3+ of CXCR5+ICOShi) d7 (%)', 'S04-B_Tfr', None, 'lin', None, ''),
 ('Tfr d30 (%)', 'S04-C', None, 'lin', None, ''),
 ('Lung Treg d7 (%)', 'S04-D', None, 'lin', None, 'n=3'),
 ('IgG+ of B220+ MLN (%)', 'S13-H', None, 'lin', None, 'timepoint not stated'),
 # ---- humoral ----
 ('IgG anti-CA09 d14 (titre)', 'S03-A', None, 'log', None, ''),
 ('HAI anti-CA09 d14 (titre)', 'S03-C', None, 'log', 5, 'LOD 1:10; <LOD set to 5'),
 ('Neut anti-CA09 d14 (titre)', 'S03-D', None, 'log', None, ''),
 ('IgG anti-Aichi d14 (titre)', 'S03-E', None, 'log', None, ''),
 ('HAI anti-Aichi d14 (titre)', 'S03-G', None, 'log', 5, 'LOD 1:10; <LOD set to 5'),
 ('Neut anti-Aichi d14 (titre)', 'S03-H', None, 'log', None, ''),
 ('IgG2a anti-CA09 d14 (titre)', 'S13-A', None, 'log', None, ''),
 ('IgG1 anti-CA09 d14 (titre)', 'S13-B', None, 'log', None, ''),
 ('IgG2a anti-Aichi d14 (titre)', 'S13-C', None, 'log', None, ''),
 ('IgG1 anti-Aichi d14 (titre)', 'S13-D', None, 'log', None, ''),
 ('IgG anti-CA09 d28 post-boost (titre)', 'S13-I', None, 'log', None, ''),
 ('IgG anti-Aichi d28 post-boost (titre)', 'S13-J', None, 'log', None, ''),
 # ---- CD8 ----
 ('Ki-67+ CD8 lung d3 (%)', 'S05-D', None, 'lin', None, ''),
 ('GZMB+ CD8 lung d3 (%)', 'S05-E', None, 'lin', None, ''),
 ('IFNg+ CD8 MLN d14, H5 restim (%)', 'S05-F', None, 'lin', None, ''),
 ('IFNg+ CD8 MLN d60, H5 restim (%)', 'S05-G', None, 'lin', None, ''),
 ('GZMB+ CD8 MLN d60 (%)', 'S05-H', None, 'lin', None, ''),
 ('Lung TRM CD8 d25 (%)', 'S05-I', None, 'lin', None, ''),
 ('IFNg+ CD8 MLN, H1N1 restim (%)', 'S14-A_H1N1', None, 'lin', None, 'timepoint not stated'),
 ('IFNg+ CD8 MLN, H3N2 restim (%)', 'S14-A_H3N2', None, 'lin', None, 'timepoint not stated'),
 # ---- safety-relevant ----
 ('CNS Ifnb1 36h (fold)', 'S10-A_Ifnb1', None, 'log', None, 'block declared mean+SD'),
 ('CNS Tnf 36h (fold)', 'S10-A_Tnf', None, 'log', None, 'block declared mean+SD'),
 ('CNS Isg15 36h (fold)', 'S10-A_Isg15', None, 'log', None, 'block declared mean+SD'),
]


def get(block, filt):
    d = t[t.block == block]
    if filt:
        k, val = filt
        d = d[d[k].astype(str) == val]
    return d


def tr(x, how, floor):
    x = np.asarray(x, float)
    if how == 'log':
        if floor is not None:
            x = np.where(x <= 0, floor, x)
        return np.log10(x)
    return x


def summarize(x, how):
    if how == 'log':
        lx = x
        m = lx.mean(); se = lx.std(ddof=1) / np.sqrt(len(lx))
        tc = stats.t.ppf(.975, len(lx) - 1)
        return 10 ** m, 10 ** (m - tc * se), 10 ** (m + tc * se)
    m = x.mean(); se = x.std(ddof=1) / np.sqrt(len(x)); tc = stats.t.ppf(.975, len(x) - 1)
    return m, m - tc * se, m + tc * se


def hedges_g(a, b):
    na, nb = len(a), len(b)
    sp = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    d = (a.mean() - b.mean()) / sp if sp > 0 else np.nan
    J = 1 - 3 / (4 * (na + nb) - 9)
    return d * J


rows = []
for label, block, filt, how, floor, note in SPECS:
    d = get(block, filt).copy()
    d['y'] = tr(d.value, how, floor)
    groups = d.group.unique().tolist()
    res = dict(readout=label, block=block, transform=how, note=note)
    for g in groups:
        x = d[d.group == g].y.values
        c, lo, hi = summarize(x, how)
        res[f'{g}|n'] = len(x); res[f'{g}|center'] = c; res[f'{g}|lo'] = lo; res[f'{g}|hi'] = hi
    # ANOVA + Tukey over all groups in block (stated method)
    if len(groups) > 2:
        f, p = stats.f_oneway(*[d[d.group == g].y.values for g in groups])
        res['anova_p'] = p
        tk = pairwise_tukeyhsd(d.y.values, d.group.values)
        tkdf = pd.DataFrame(tk._results_table.data[1:], columns=tk._results_table.data[0])
        def tkp(a, b):
            r = tkdf[((tkdf.group1 == a) & (tkdf.group2 == b)) | ((tkdf.group1 == b) & (tkdf.group2 == a))]
            return float(r['p-adj'].iloc[0]) if len(r) else np.nan
    else:
        tkp = lambda a, b: np.nan
    for a, b in [('PSLN-344', 'PSLN-212'), ('PSLN-344', 'Sham'), ('PSLN-344', 'PSLN-212(Y)'), ('PSLN-344', 'CMP-204'), ('PSLN-212', 'Sham'), ('PSLN-344(Y)', 'PSLN-212(Y)')]:
        if a in groups and b in groups:
            xa = d[d.group == a].y.values; xb = d[d.group == b].y.values
            w = stats.ttest_ind(xa, xb, equal_var=False)
            mw = stats.mannwhitneyu(xa, xb, alternative='two-sided')
            diff = xa.mean() - xb.mean()
            # CI of difference (Welch)
            se = np.sqrt(xa.var(ddof=1) / len(xa) + xb.var(ddof=1) / len(xb))
            dfw = se ** 4 / ((xa.var(ddof=1) / len(xa)) ** 2 / (len(xa) - 1) + (xb.var(ddof=1) / len(xb)) ** 2 / (len(xb) - 1))
            tc = stats.t.ppf(.975, dfw)
            key = f'{a} vs {b}'
            if how == 'log' or 'log10' in label:
                res[f'{key}|ratio'] = 10 ** diff; res[f'{key}|ratio_lo'] = 10 ** (diff - tc * se); res[f'{key}|ratio_hi'] = 10 ** (diff + tc * se)
            else:
                res[f'{key}|diff'] = diff; res[f'{key}|diff_lo'] = diff - tc * se; res[f'{key}|diff_hi'] = diff + tc * se
            res[f'{key}|welch_p'] = w.pvalue; res[f'{key}|mw_p'] = mw.pvalue
            res[f'{key}|tukey_p'] = tkp(a, b); res[f'{key}|hedges_g'] = hedges_g(xa, xb)
    # restoration index on analysis scale: (344 - 212)/(212Y - 212)
    if all(g in groups for g in ['PSLN-344', 'PSLN-212', 'PSLN-212(Y)']):
        m = {g: d[d.group == g].y.mean() for g in ['PSLN-344', 'PSLN-212', 'PSLN-212(Y)']}
        den = m['PSLN-212(Y)'] - m['PSLN-212']
        res['restoration_index'] = (m['PSLN-344'] - m['PSLN-212']) / den if abs(den) > 1e-9 else np.nan
    rows.append(res)

R = pd.DataFrame(rows)
R.to_csv('/tmp/work/continuous_results.csv', index=False)

# compact print
def fmt(v, how):
    if pd.isna(v): return ''
    return f'{v:,.3g}'
out = []
for _, r in R.iterrows():
    line = dict(readout=r.readout, block=r.block)
    for g in ['Sham', 'CMP-204', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)', 'PSLN-344(Y)', 'Vaccine']:
        if f'{g}|center' in r and not pd.isna(r.get(f'{g}|center')):
            line[g] = f"{r[f'{g}|center']:.3g}"
    k = 'PSLN-344 vs PSLN-212'
    if f'{k}|ratio' in r and not pd.isna(r.get(f'{k}|ratio')):
        line['344v212'] = f"x{r[f'{k}|ratio']:.2f} [{r[f'{k}|ratio_lo']:.2f},{r[f'{k}|ratio_hi']:.2f}]"
    elif f'{k}|diff' in r and not pd.isna(r.get(f'{k}|diff')):
        line['344v212'] = f"{r[f'{k}|diff']:+.2f} [{r[f'{k}|diff_lo']:+.2f},{r[f'{k}|diff_hi']:+.2f}]"
    if f'{k}|welch_p' in r and not pd.isna(r.get(f'{k}|welch_p')):
        line['p_welch'] = f"{r[f'{k}|welch_p']:.2g}"; line['p_tukey'] = f"{r.get(f'{k}|tukey_p', np.nan):.2g}"; line['g'] = f"{r[f'{k}|hedges_g']:.1f}"
    if 'restoration_index' in r and not pd.isna(r.get('restoration_index')):
        line['RI'] = f"{r['restoration_index']:.2f}"
    out.append(line)
pd.set_option('display.width', 300); pd.set_option('display.max_columns', 30); pd.set_option('display.max_colwidth', 45)
print(pd.DataFrame(out).fillna('').to_string(index=False))
