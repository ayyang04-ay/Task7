import pandas as pd, numpy as np, warnings
from scipy import stats, optimize
warnings.filterwarnings('ignore')
C = pd.read_csv('/tmp/work/tidy/continuous.csv'); C['time'] = C['time'].astype(str)
K = pd.read_csv('/tmp/work/tidy/contrasts_continuous.csv')
pd.set_option('display.width', 260); pd.set_option('display.max_rows', 300); pd.set_option('display.max_colwidth', 48)

def tr(meas, x):
    m = meas.lower(); x = np.asarray(x, float)
    if 'titre' in m:
        if 'hi titre' in m:
            x = np.where(x <= 0, 5, x)
        return np.log2(x)
    if 'fold' in m and 'log10' not in m:
        return np.log10(x)
    return x

def auc(pos, neg):
    # probability a random positive > random negative (ties 0.5); direction-agnostic reported as max(AUC,1-AUC) with sign
    pos, neg = np.asarray(pos), np.asarray(neg)
    s = sum((p > q) + 0.5 * (p == q) for p in pos for q in neg) / (len(pos) * len(neg))
    return s

# candidate biomarkers: (block, measurand, time, human-translatable analogue, stage)
cands = [
 ('S01-A', 'Lung Ifnb1 (fold vs untreated)', '16h', 'Nasal/blood type-I IFN & ISG signature (e.g. IFI27, ISG15, MX1) at 16-24 h', 'PD: target engagement (h)'),
 ('S02-F', 'Lung Gm-csf (fold vs untreated)', '36h', 'Nasal lining fluid GM-CSF (CSF2) at 24-48 h', 'PD: Mn-dependent mediator (h)'),
 ('S09-A (cols A-V; printed 16h)', 'Lung Ccl2 (log10 fold)', '16h (as printed)', 'Nasal lining fluid / serum MCP-1 (CCL2) at 16-24 h', 'PD: monocyte-recruiting chemokine (h)'),
 ('S01-D', 'Lung monocytes CD11b+Ly6C+ (%)', '4', '(no direct human analogue; nasal cytology research only)', 'Cellular: innate recruitment (d4)'),
 ('S01-F', 'Lung cDC1 (%)', '72h', '(research only)', 'Cellular: DC (72 h)'),
 ('S02-A', 'Lung migratory CCR7+ CD11b+ DC (%)', '72h', '(research only)', 'Cellular: DC migration (72 h)'),
 ('S05-E', 'Lung GZMB+ CD8 T (%)', 'd3', '(research only)', 'Cellular: early CD8 effector (d3)'),
 ('S04-A', 'MLN Tfh ICOS-high (%)', 'd7', 'Circulating Tfh (CXCR5+PD-1+ICOS+) in blood at day 7', 'Adaptive: Tfh (d7)'),
 ('S04-B Foxp3', 'MLN Tfr Foxp3+ in CXCR5+ICOShi (%)', 'd7', 'Circulating Tfr / cTfh:cTfr ratio at day 7', 'Adaptive: Tfh:Tfr balance (d7)'),
 ('S03-K', 'MLN GC B cells CXCR5+GL7+ (%)', 'd7', 'Plasmablasts in blood at day 7 (proxy)', 'Adaptive: GC (d7)'),
 ('S03-C', 'HI titre CA09 H1N1', 'd14', 'HI titre (GMT, seroconversion, seroprotection)', 'Humoral (d14)'),
 ('S03-G', 'HI titre Aichi H3N2', 'd14', 'HI titre (GMT, seroconversion, seroprotection)', 'Humoral (d14)'),
 ('S03-D', 'Neutralising titre CA09 H1N1', 'd14', 'Microneutralisation titre', 'Humoral (d14)'),
 ('S03-A', 'Serum IgG anti-CA09 H1N1 (titre)', 'd14', 'HA-specific IgG ELISA', 'Humoral (d14)'),
 ('S13-A', 'Serum IgG2a anti-CA09 (titre)', 'd14', 'Th1-associated IgG subclass profile (IgG1/IgG3 vs IgG2/IgG4 in humans; not 1:1)', 'Humoral quality (d14)'),
 ('S05-F', 'MLN IFNg+ CD8 T, H5N1 restim (%) d14', 'd14', 'IFN-g ELISpot / ICS to conserved NP/M1 peptides (PBMC)', 'Cellular: cross-reactive CD8 (d14)'),
 ('S05-G', 'MLN IFNg+ CD8 T, H5N1 restim (%) d60', 'd60', 'IFN-g ELISpot at day 60-180 (durability)', 'Cellular durability (d60)'),
 ('S05-I', 'Lung CD8 TRM CD69+CD103+ (%)', 'd25', '(nasal/airway TRM research only)', 'Mucosal memory (d25)'),
]
rows = []
for blk, meas, t, human, stage in cands:
    d = C[(C.block == blk) & (C.measurand == meas) & (C.time == t)]
    grp = lambda g: tr(meas, d[d.group == g].value.values)
    have = set(d.group)
    sham = 'Sham' if 'Sham' in have else ('PBS' if 'PBS' in have else None)
    young = 'PSLN-212(Y)' if 'PSLN-212(Y)' in have else None
    a344, a212 = grp('PSLN-344'), grp('PSLN-212')
    r = dict(stage=stage, block=blk, marker=meas, time=t, human_analogue=human)
    r['AUC_344_vs_212'] = auc(a344, a212)
    r['p_344_vs_212_welch'] = stats.ttest_ind(a344, a212, equal_var=False).pvalue
    na_, nb_ = len(a344), len(a212)
    sp_ = np.sqrt(((na_ - 1) * a344.var(ddof=1) + (nb_ - 1) * a212.var(ddof=1)) / (na_ + nb_ - 2))
    r['g_344_vs_212'] = (a344.mean() - a212.mean()) / sp_ * (1 - 3 / (4 * (na_ + nb_) - 9))   # Hedges g (small-sample corrected)
    # fraction of young response restored by PSLN-344, relative to vehicle baseline (Sham) when available else PSLN-212
    base = grp(sham) if sham else a212
    if young:
        y = grp(young)
        denom = y.mean() - base.mean()
        r['pct_young_restored'] = 100 * (a344.mean() - base.mean()) / denom if abs(denom) > 1e-9 else np.nan
        r['baseline_for_restoration'] = sham if sham else 'PSLN-212'
    # protected (344 aged + young) vs unprotected (Sham + 212 aged)
    prot = np.concatenate([a344] + ([grp(young)] if young else []))
    unprot = np.concatenate([a212] + ([grp(sham)] if sham else []))
    r['AUC_protected_vs_unprotected_arms'] = auc(prot, unprot)
    # separation: min(344) > max(212)?
    r['complete_separation_344_vs_212'] = bool(min(a344) > max(a212) or max(a344) < min(a212))
    rows.append(r)
B = pd.DataFrame(rows)
print(B[['stage', 'block', 'marker', 'time', 'AUC_344_vs_212', 'g_344_vs_212', 'p_344_vs_212_welch', 'pct_young_restored',
         'AUC_protected_vs_unprotected_arms', 'complete_separation_344_vs_212']].round(3).to_string(index=False))
B.to_csv('/tmp/work/tidy/biomarker_candidates.csv', index=False)

# ---- group-level concordance: arm means vs pooled aged survival
surv = {'Sham': 1 / 80, 'PSLN-212': 11 / 80, 'PSLN-344': 68 / 80, 'PSLN-212(Y)': 69 / 70}
print('\nGroup-level rank concordance with pooled survival (Sham<212<344<Y):')
for blk, meas, t, human, stage in cands:
    d = C[(C.block == blk) & (C.measurand == meas) & (C.time == t)]
    gm = {g: tr(meas, d[d.group == g].value.values).mean() for g in surv if g in set(d.group)}
    if len(gm) >= 3:
        order = sorted(gm, key=gm.get)
        sorder = sorted(gm, key=surv.get)
        rho = stats.spearmanr([gm[g] for g in gm], [surv[g] for g in gm]).correlation
        print(f'  {blk:30s} {meas[:45]:45s} arms={len(gm)} marker order={order} spearman={rho:+.2f}')

# ---- early PD marker vs later immunogenicity across arms (S01-A Ifnb1 16h vs HI / IgG d14)
print('\nArm-level: Ifnb1 16 h (S01-A) vs day-14 humoral readouts (S03), 5 arms incl. CMP-204')
arms = ['Sham', 'CMP-204', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']
ifn = {g: np.log10(C[(C.block == 'S01-A') & (C.time == '16h') & (C.group == g)].value).mean() for g in arms}
for blk, meas in [('S03-C', 'HI titre CA09 H1N1'), ('S03-G', 'HI titre Aichi H3N2'), ('S03-A', 'Serum IgG anti-CA09 H1N1 (titre)'),
                  ('S03-E', 'Serum IgG anti-Aichi H3N2 (titre)'), ('S03-D', 'Neutralising titre CA09 H1N1'), ('S03-H', 'Neutralising titre Aichi H3N2')]:
    y = {g: tr(meas, C[(C.block == blk) & (C.group == g)].value.values).mean() for g in arms}
    x = [ifn[g] for g in arms]; yy = [y[g] for g in arms]
    pr = stats.pearsonr(x, yy); sr = stats.spearmanr(x, yy)
    print(f'  {meas:38s} Pearson r={pr.statistic:+.2f} (p={pr.pvalue:.3f}); Spearman rho={sr.correlation:+.2f} (p={sr.pvalue:.3f})')

# ---- HI threshold look: per-animal HI distribution by arm
print('\nHI titres per arm (S03-C / S03-G):')
for blk in ['S03-C', 'S03-G']:
    d = C[C.block == blk]
    print(' ', blk, {g: sorted(d[d.group == g].value.astype(int).tolist()) for g in arms})

# ---- S08-A dose-response: Emax model with baseline 1 (fold), fit on log10 response
print('\nS08-A Ifnb1 dose-response fits (Emax model: E = 1 + Emax*D/(ED50 + D)), 16 h, aged lung')
d = C[C.block == 'S08-A']; d = d.assign(dose=d.time.astype(float))
fits = []
for g, dg in d.groupby('group'):
    D = dg.dose.values; Y = dg.value.values
    f = lambda D, Emax, ED50: 1 + Emax * D / (ED50 + D)
    try:
        p, cov = optimize.curve_fit(f, D, Y, p0=[Y.max(), 10], bounds=([0, 0.01], [1e4, 1e4]))
        se = np.sqrt(np.diag(cov))
    except Exception as e:
        p, se = [np.nan, np.nan], [np.nan, np.nan]
    m20 = Y[D == 20].mean(); m40 = Y[D == 40].mean()
    fits.append(dict(group=g, Emax=p[0], Emax_se=se[0], ED50_ug=p[1], ED50_se=se[1], mean_20ug=m20, mean_40ug=m40,
                     pct_of_40ug_at_20ug=100 * (m20 - 1) / (m40 - 1)))
F = pd.DataFrame(fits); print(F.round(2).to_string(index=False)); F.to_csv('/tmp/work/tidy/dose_response_fits.csv', index=False)
