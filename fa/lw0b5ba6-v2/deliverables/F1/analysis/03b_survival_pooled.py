"""Pooled / stratified survival summaries with flag-sensitivity.

Evidence sets (aged BALB/c >=20 mo, single i.n. dose):
  ACUTE  : challenge 2-14 d after immunisation  -> S03-I, S03-J, S06-A, S06-B, S06-C, S06-D
  D60    : challenge 60 d after immunisation    -> S06-E, S06-F, S06-G
Sensitivity sets:
  'as printed'      : every block, labels as printed
  'flag-robust'     : drop S06-D (cell-for-cell duplicate of S06-C), S03-I and S03-J (group identity contradicted by paired
                      body-weight blocks S13-F / S13-G)
"""
import numpy as np, pandas as pd, itertools, math
from scipy import stats
import tidy
import survlib as S

def pooled(blocks, g1, g0, label):
    OE = V = 0.0; k1 = n1 = k0 = n0 = 0; strata = []
    for b in blocks:
        d = S.prep(b); s = d[d.group.isin([g1, g0])]
        grp = (s.group == g1).astype(int).values
        oe, v = S.lr_stat(s.time.values, s.event.values, grp)
        OE += oe; V += v
        a = s[s.group == g1]; c = s[s.group == g0]
        k1 += int((a.event == 0).sum()); n1 += len(a); k0 += int((c.event == 0).sum()); n0 += len(c)
        strata.append((int((a.event == 0).sum()), len(a), int((c.event == 0).sum()), len(c)))
    chi2 = OE ** 2 / V if V > 0 else np.nan
    p = stats.chi2.sf(chi2, 1) if V > 0 else np.nan
    # Mantel-Haenszel risk difference (survival) with Sato variance -> Greenland-Robins
    num = sum(a * n0_ / (n1_ + n0_) - c * n1_ / (n1_ + n0_) for a, n1_, c, n0_ in strata)
    den = sum(n1_ * n0_ / (n1_ + n0_) for a, n1_, c, n0_ in strata)
    rd = num / den
    # Greenland-Robins variance of MH RD
    P_ = sum((n1_ ** 2 * c - n0_ ** 2 * a + n1_ * n0_ * (n0_ - n1_) / 2) / (n1_ + n0_) ** 2 for a, n1_, c, n0_ in strata)
    Q_ = sum((a * (n0_ - c) + c * (n1_ - a)) / (2 * (n1_ + n0_)) for a, n1_, c, n0_ in strata)
    var = (rd * P_ + Q_) / den ** 2
    se = math.sqrt(max(var, 0))
    lo1, hi1 = S.cp(k1, n1); lo0, hi0 = S.cp(k0, n0)
    return dict(set=label, contrast=f'{g1} vs {g0}', blocks='+'.join(blocks), surv_1=f'{k1}/{n1}', pct_1=100 * k1 / n1, ci1=f'{100*lo1:.0f}-{100*hi1:.0f}',
                surv_0=f'{k0}/{n0}', pct_0=100 * k0 / n0, ci0=f'{100*lo0:.0f}-{100*hi0:.0f}',
                MH_risk_diff_pct=100 * rd, RD_lo=100 * (rd - 1.96 * se), RD_hi=100 * (rd + 1.96 * se),
                strat_logrank_chi2=chi2, strat_logrank_p=p)

ACUTE = ['S03-I', 'S03-J', 'S06-A', 'S06-B', 'S06-C', 'S06-D']
ACUTE_ROBUST = ['S06-A', 'S06-B', 'S06-C']
D60 = ['S06-E', 'S06-F', 'S06-G']
out = []
for label, bl in [('ACUTE as printed', ACUTE), ('ACUTE flag-robust', ACUTE_ROBUST), ('D60', D60), ('ALL aged BALB/c as printed', ACUTE + D60), ('ALL aged BALB/c flag-robust', ACUTE_ROBUST + D60)]:
    for g1, g0 in [('PSLN-344', 'Sham'), ('PSLN-344', 'PSLN-212'), ('PSLN-212', 'Sham')]:
        out.append(pooled(bl, g1, g0, label))
    bl_y = [b for b in bl if b != 'S03-J']      # no young arm in S03-J
    out.append(pooled(bl_y, 'PSLN-344', 'PSLN-212(Y)', label))
out.append(pooled(D60, 'PSLN-344', 'Untreated', 'D60'))
out.append(pooled(D60, 'PSLN-212', 'Untreated', 'D60'))
out.append(pooled(['S15-L', 'S15-N'], 'PSLN-344', 'PSLN-212', 'Other strains (C57BL/6, Swiss Webster)'))
out.append(pooled(['S15-L', 'S15-N'], 'PSLN-344', 'Sham', 'Other strains (C57BL/6, Swiss Webster)'))
out.append(pooled(['S15-L', 'S15-N'], 'PSLN-344', 'PSLN-212(Y)', 'Other strains (C57BL/6, Swiss Webster)'))
out.append(pooled(['S06-E[r71]', 'S06-F[r71]'], 'Naive+PSLN-344', 'Naive+PSLN-212', '14-month BALB/c, no prior infection'))
out.append(pooled(['S06-E[r71]', 'S06-F[r71]'], 'Imprinting+PSLN-344', 'Imprinting+PSLN-212', '14-month BALB/c, PR8-imprinted'))
out.append(pooled(['S06-E[r71]', 'S06-F[r71]'], 'Imprinting+PSLN-344', 'Naive+PSLN-344', '14-month BALB/c'))
out.append(pooled(['S09-B', 'S09-D', 'S09-F'], 'PSLN-344Y', 'PSLN-212Y', 'Young BALB/c'))
out.append(pooled(['S09-B', 'S09-D', 'S09-F'], 'PSLN-344Y', 'Sham', 'Young BALB/c'))
PO = pd.DataFrame(out)
pd.set_option('display.width', 260); pd.set_option('display.max_colwidth', 45)
print(PO.round(4).to_string(index=False))
PO.to_csv('../tables/T3_survival_pooled.csv', index=False)

# ------------------------------------------------------------------ early (2-3 d) vs 14 d vs 60 d for PSLN-344
print('\nPSLN-344 survival by vaccination-to-challenge interval (aged BALB/c):')
for lab, bl in [('2-3 d', ['S03-J', 'S06-B', 'S06-D', 'S15-H']), ('2-3 d, flag-robust (S06-B + S15-H)', ['S06-B', 'S15-H']),
                ('14 d', ['S03-I', 'S06-A', 'S06-C']), ('14 d, flag-robust (S06-A + S06-C)', ['S06-A', 'S06-C']), ('60 d', D60)]:
    k = n = 0
    for b in bl:
        d = S.prep(b); g = 'PSLN-344' if 'PSLN-344' in set(d.group) else '3d Vaccine+PSLN-344'
        s = d[d.group == g]; k += int((s.event == 0).sum()); n += len(s)
    lo, hi = S.cp(k, n); print(f'  {lab}: {k}/{n} = {100*k/n:.0f}% (95% CI {100*lo:.0f}-{100*hi:.0f})  blocks {bl}')

# natural mortality: untreated aged, no challenge
k = n = 0
for b in D60:
    d = S.prep(b); s = d[d.group == 'Untreated']; k += int(s.event.sum()); n += len(s)
lo, hi = S.cp(k, n); print(f'\nUntreated, unchallenged aged animals dying within the 14-d window: {k}/{n} = {100*k/n:.0f}% (95% CI {100*lo:.0f}-{100*hi:.0f})')
k2 = n2 = 0
for b in D60:
    d = S.prep(b); s = d[d.group == 'PSLN-344']; k2 += int(s.event.sum()); n2 += len(s)
print(f'PSLN-344, challenged at d60: deaths {k2}/{n2}; Fisher vs untreated p = {stats.fisher_exact([[k2, n2-k2],[k, n-k]])[1]:.3f}')
# 60-d PSLN-344 vs acute PSLN-344 (waning?)
for lab, bl in [('as printed', ACUTE), ('flag-robust', ACUTE_ROBUST)]:
    ka = na = 0
    for b in bl:
        d = S.prep(b); s = d[d.group == 'PSLN-344']; ka += int(s.event.sum()); na += len(s)
    print(f'PSLN-344 deaths acute ({lab}) {ka}/{na} vs d60 {k2}/{n2}: Fisher p = {stats.fisher_exact([[ka, na-ka],[k2, n2-k2]])[1]:.4f}')
