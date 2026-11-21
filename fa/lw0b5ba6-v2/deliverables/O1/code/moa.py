"""Mechanism-of-action interventions (loss/gain of function), young-animal comparisons, dose-response, safety."""
import pandas as pd, numpy as np
from scipy import stats, optimize
V = pd.read_csv('/tmp/work/tidy/values.csv'); V['time'] = V.time.fillna('')
B = pd.read_csv('/tmp/work/tidy/bw.csv')

def get(blk, grp, an=None, t=None):
    d = V[(V.block == blk) & (V.group == grp)]
    if an: d = d[d.analyte == an]
    if t is not None: d = d[d.time == t]
    return d.sort_values('animal').value.values

def contrast(label, blk, a, b, an=None, t=None, log=False, note=''):
    x, y = get(blk, a, an, t), get(blk, b, an, t)
    tx, ty = (np.log2(x), np.log2(y)) if log else (x, y)
    p = stats.ttest_ind(tx, ty, equal_var=False).pvalue
    pm = stats.mannwhitneyu(tx, ty, alternative='two-sided', method='exact').pvalue
    m = lambda v: (2 ** np.mean(np.log2(v))) if log else np.mean(v)
    eff = (m(x) / m(y)) if log else (np.mean(x) - np.mean(y))
    return dict(label=label, block=blk, A=a, B=b, nA=len(x), nB=len(y), meanA=m(x), sdA=np.std(x, ddof=1), meanB=m(y),
                sdB=np.std(y, ddof=1), pct_change=100 * (m(x) - m(y)) / m(y), effect=eff, p_welch=p, p_mwu=pm, note=note)

rows = [
    contrast('Delivery: SP-A/D knockout reduces AM uptake of PSLN-344-composition liposomes', 'S01-C', 'SPA/D', 'WT', an='DiD+ AM'),
    contrast('Delivery: liposome vs free SRB, AECII uptake', 'S01-B', 'AECII/PSLN-SRB', 'AECII/FreeSRB', an='SRB+ AEC'),
    contrast('Delivery: liposome vs free SRB, AECI uptake', 'S01-B', 'AECI/PSLN-SRB', 'AECI/FreeSRB', an='SRB+ AEC'),
    contrast('Delivery (low confidence): Mn-PSLN vs PSLN, AECII uptake', 'S08-C', 'AECII-PSLN-344-SRB', 'AECII-PSLN-SRB', an='SRB+ AEC',
             note='S08-C overlaps S01-B; AECI values inconsistent with S01-B'),
    contrast('Gap-junction: carbenoxolone reduces recruited monocytes (PSLN-344)', 'S11-C', 'CBX+', 'CBX-'),
    contrast('Type I IFN: IFNAR-/- BM (no cDC) vs WT BM (no cDC): moDC', 'S02-H', 'IFN w/o cDC', 'WT w/o cDC'),
    contrast('Type I IFN: IFNAR-/- BM (+cDC) vs WT BM (+cDC): moDC', 'S02-H', 'IFN w/ cDC', 'WT w/ cDC'),
    contrast('GM-CSF rescue: IFNAR-/- BM + GM-CSF vs IFNAR-/- BM: moDC', 'S02-H', 'GMCSF', 'IFN w/o cDC'),
    contrast('GM-CSF rescue vs WT: IFNAR-/- BM + GM-CSF vs WT BM (no cDC)', 'S02-H', 'GMCSF', 'WT w/o cDC'),
    contrast('GM-CSF gain-of-function: PSLN-212 + GM-CSF vs PSLN-212 (moDC-like)', 'S02-G', 'PSLN-212+GM-CSF', 'PSLN-212'),
    contrast('GM-CSF alone (no STING agonist) vs PSLN-212', 'S02-G', 'GM-CSF', 'PSLN-212'),
    contrast('Type I IFN: IFNAR-/- vs WT BM: infiltrating monocytes (young)', 'S12-A', 'IFNAR-/- to WT', 'WT to WT'),
    contrast('CCR2: INCB3344 vs vehicle, lung monocytes (PSLN-344)', 'S07-B', 'PSLN-344+INCB3344', 'PSLN-344', an='Lung CD11b+Ly6C+ monocytes'),
    contrast('CCR2: INCB3344 vs vehicle, Ly6C+ macrophages (PSLN-344)', 'S07-B', 'PSLN-344+INCB3344', 'PSLN-344', an='Lung Ly6C+ macrophages'),
    contrast('CCR2: INCB3344 vs vehicle, lung GZMB+ CD8 (young, PSLN-344)', 'S02-I', 'PSLN-344(Y)+INCB3344', 'PSLN-344(Y)'),
    contrast('Migration: PTX vs PSLN-344, antigen+ DC in MLN', 'S02-C', 'PTX', 'PSLN-344', note='PTX group adjuvant not stated'),
    contrast('Migration: PTX vs PSLN-344, OT-I proliferation (MLN DC co-culture)', 'S02-E', 'PTX', 'PSLN-344', note='PTX group adjuvant not stated'),
    contrast('Migration: PTX in vivo, OT-I proliferation in MLN', 'S05-C', 'MLN+PTX', 'MLN'),
    contrast('Migration: PTX in vivo, OT-I proliferation in lung (local priming)', 'S05-C', 'Lung+PTX', 'Lung'),
    # young-animal effect of Mn
    contrast('Young: PSLN-344(Y) vs PSLN-212(Y), Ifnb1 16h', 'S01-A', 'PSLN-344(Y)', 'PSLN-212(Y)', t='16h', log=True),
    contrast('Young: PSLN-344(Y) vs PSLN-212(Y), lung CD11b+ DC d4', 'S01-E', 'PSLN-344(Y)', 'PSLN-212(Y)', t='d4'),
    contrast('Young: PSLN-344(Y) vs PSLN-212(Y), cDC1 72h', 'S01-F', 'PSLN-344(Y)', 'PSLN-212(Y)'),
    contrast('Young: PSLN-344(Y) vs PSLN-212(Y), antigen+ MLN DC', 'S02-C', 'PSLN-344(Y)', 'PSLN-212(Y)'),
    contrast('Young: PSLN-344(Y) vs PSLN-212(Y), OT-I proliferation', 'S02-E', 'PSLN-344(Y)', 'PSLN-212(Y)'),
    # aged PSLN-344 vs young benchmark on function
    contrast('Aged PSLN-344 vs young PSLN-212: OT-I proliferation', 'S02-E', 'PSLN-344', 'PSLN-212(Y)'),
    # CNS safety
    contrast('CNS Ifnb1: PSLN-344 vs Sham', 'S10-A', 'PSLN-344', 'Sham', an='CNS Ifnb1', log=True),
    contrast('CNS Tnf: PSLN-344 vs Sham', 'S10-A', 'PSLN-344', 'Sham', an='CNS Tnf', log=True),
    contrast('CNS Isg15: PSLN-344 vs Sham', 'S10-A', 'PSLN-344', 'Sham', an='CNS Isg15', log=True),
    contrast('CNS Ifnb1: CT vs Sham (assay positive control)', 'S10-A', 'CT', 'Sham', an='CNS Ifnb1', log=True),
    contrast('CNS Tnf: CT vs Sham', 'S10-A', 'CT', 'Sham', an='CNS Tnf', log=True),
    contrast('CNS Isg15: CT vs Sham', 'S10-A', 'CT', 'Sham', an='CNS Isg15', log=True),
    # other comparators
    contrast('cGAMP (CMP-204) vs PSLN-212: Ifnb1 16h', 'S01-A', 'CMP-204', 'PSLN-212', t='16h', log=True),
    contrast('PSLN-212/R848 vs PSLN-344: Ifnb1 16h', 'S01-A', 'PSLN-212/R848', 'PSLN-344', t='16h', log=True),
    contrast('CMP-204 vs PSLN-344: HAI CA09 d14', 'S03-C', 'CMP-204', 'PSLN-344', log=False),
    contrast('Encapsulation efficiency PSLN-344 vs PSLN-212', 'S08-B', 'PSLN-344', 'PSLN-212'),
]
M = pd.DataFrame(rows)
M.to_csv('/tmp/work/moa_contrasts.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 20); pd.set_option('display.max_colwidth', 70)
print(M[['label', 'nA', 'nB', 'meanA', 'meanB', 'pct_change', 'effect', 'p_welch', 'p_mwu']].round(4).to_string(index=False))

# ---------- dose-response (S08-A): Emax model on linear fold-change ----------
print('\n=== S08-A dose-response (Ifnb1 fold, 16h) ===')
dr = V[V.block == 'S08-A'].copy(); dr['dose'] = dr.time.str.replace('ug', '').astype(float)
emax_rows = []
def emax(d, e0, em, ed50, h): return e0 + em * d ** h / (ed50 ** h + d ** h)
for g, d in dr.groupby('group'):
    x, y = d.dose.values, d.value.values
    try:
        popt, pcov = optimize.curve_fit(emax, x, y, p0=[1, y.max(), 10, 1.5], bounds=([0, 0, 0.1, 0.3], [5, 500, 200, 6]), maxfev=20000)
        se = np.sqrt(np.diag(pcov))
    except Exception as e:
        popt, se = [np.nan] * 4, [np.nan] * 4
    means = d.groupby('dose').value.mean()
    emax_rows.append(dict(group=g, E0=popt[0], Emax=popt[1], ED50_ug=popt[2], ED50_se=se[2], hill=popt[3], mean_at_20=means[20], mean_at_40=means[40],
                          plateau_ratio_40_20=means[40] / means[20]))
E = pd.DataFrame(emax_rows); print(E.round(3).to_string(index=False))
# dose-sparing: dose of PSLN-344 giving the PSLN-212 20 ug mean response (interpolate on fitted curve)
p344 = E.set_index('group').loc['PSLN-344']; target = E.set_index('group').loc['PSLN-212', 'mean_at_20']
f = lambda dd: emax(dd, p344.E0, p344.Emax, p344.ED50_ug, p344.hill) - target
d_eq = optimize.brentq(f, 0.1, 40)
m344 = dr[dr.group == 'PSLN-344'].groupby('dose').value.mean(); m212 = dr[dr.group == 'PSLN-212'].groupby('dose').value.mean()
print(f'PSLN-212 mean at 20ug = {target:.2f}; PSLN-344 dose giving same response (Emax fit) = {d_eq:.1f} ug -> dose-sparing {20 / d_eq:.1f}x')
# model-free: linear interpolation between observed PSLN-344 means
xs, ys = m344.index.values, m344.values
d_lin = np.interp(target, ys, xs)
print(f'Model-free linear interpolation on PSLN-344 dose means: {d_lin:.1f} ug -> dose-sparing {20 / d_lin:.1f}x')
print('means by dose (344):', m344.round(2).to_dict(), '(212):', m212.round(2).to_dict())
E.to_csv('/tmp/work/dose_response.csv', index=False)

# ---------- reactogenicity: S08-D body weight after vaccination (no challenge) ----------
print('\n=== S08-D post-vaccination weight (reactogenicity) ===')
d = B[B.block == 'S08-D']
rows = []
for g, dd in d.groupby('group'):
    piv = dd.pivot(index='animal', columns='day', values='value')
    nadir = piv.min(axis=1)
    rows.append(dict(group=g, n_d0=piv[0.0].notna().sum(), n_d10=piv[10.0].notna().sum(), mean_nadir=nadir.mean(), sd_nadir=nadir.std(),
                     max_loss_pct=100 - nadir.min(), mean_d8=piv[8.0].mean(), mean_d10=piv[10.0].mean()))
R = pd.DataFrame(rows); print(R.round(2).to_string(index=False))
nad = {g: dd.pivot(index='animal', columns='day', values='value').min(axis=1).values for g, dd in d.groupby('group')}
for a, b in [('PSLN-344', 'Vaccine'), ('PSLN-344', 'PSLN-212'), ('PSLN-212/R848', 'Vaccine'), ('PSLN-212/R848', 'PSLN-344')]:
    print(a, 'vs', b, 'nadir diff', round(nad[a].mean() - nad[b].mean(), 2), 'p', round(stats.ttest_ind(nad[a], nad[b], equal_var=False).pvalue, 4))
R.to_csv('/tmp/work/reactogenicity_s08d.csv', index=False)
