"""
Pooled / stratified survival analyses across challenge experiments in AGED animals, with sensitivity analyses
for the integrity findings (duplicate block S06-D; label conflicts S03-I, S03-J; weight-implied deaths).
"""
from paths import TABLES, FIGS, OUT as OUTDIR, BUILD, PANDOC
import pandas as pd, numpy as np, math
from scipy import stats
import psln_blocks as pb
from stats_util import *
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 3000); pd.set_option('display.max_colwidth', 120)
df = pb.tidy(); sv = df[df.kind == 'surv']
END = lambda blk: 21 if blk == 'S03-J' else 14
def get(blk, g):
    t = sv[(sv.block == blk) & (sv.group == g)]
    return (t.value.fillna(END(blk)).to_numpy(float), t.event.to_numpy(int)) if len(t) else None

# long-format export for the R cross-check and the stratified Cox model (a06c_cox.R)
_x = sv[['block', 'group', 'value', 'event']].rename(columns={'value': 'day'}).copy()
_x.loc[(_x.block == 'S03-J') & _x.day.isna(), 'day'] = 21
_x.to_csv(TABLES + 'surv_long.csv', index=False)

AGED = ['S03-I', 'S03-J', 'S06-A', 'S06-B', 'S06-C', 'S06-D', 'S06-E (rows 34-68)', 'S06-F (rows 34-68)', 'S06-G', 'S15-L', 'S15-N']
TIMING = {'S03-I': 'd14', 'S03-J': 'd2-3', 'S06-A': 'd14', 'S06-B': 'd2-3', 'S06-C': 'd14', 'S06-D': 'd2-3',
          'S06-E (rows 34-68)': 'd60', 'S06-F (rows 34-68)': 'd60', 'S06-G': 'd60', 'S15-L': 'other strain (timing n.s.)', 'S15-N': 'other strain (timing n.s.)'}

def pooled(blocks, a, b, label):
    strata = []; tabs = []; sa = na = sb = nb = 0
    for blk in blocks:
        A, B = get(blk, a), get(blk, b)
        if A is None or B is None: continue
        strata.append((A[0], A[1], B[0], B[1]))
        ka, kb = int((A[1] == 0).sum()), int((B[1] == 0).sum())
        tabs.append((ka, len(A[1]), kb, len(B[1])))
        sa += ka; na += len(A[1]); sb += kb; nb += len(B[1])
    if not strata: return None
    slr = stratified_logrank(strata)
    rd, lo, hi = mh_risk_difference(tabs)
    cmh = cmh_test(tabs)
    ca = clopper_pearson(sa, na); cb = clopper_pearson(sb, nb)
    return dict(analysis=label, contrast=f'{a} vs {b}', k_experiments=len(strata),
                surv_a=f'{sa}/{na}', pct_a=100 * sa / na, a_lo=100 * ca[0], a_hi=100 * ca[1],
                surv_b=f'{sb}/{nb}', pct_b=100 * sb / nb, b_lo=100 * cb[0], b_hi=100 * cb[1],
                MH_risk_diff_pct=100 * rd, rd_lo=100 * lo, rd_hi=100 * hi, strat_logrank_chi2=slr['chi2'], p_strat_logrank=slr['p'], p_CMH=cmh[1])

rows = []
for a, b in [('PSLN-344', 'PSLN-212'), ('PSLN-344', 'Sham'), ('PSLN-344', 'PSLN-212(Y)'), ('PSLN-212', 'Sham'), ('PSLN-212', 'PSLN-212(Y)')]:
    rows.append(pooled(AGED, a, b, 'ALL aged experiments, as printed (11)'))
    rows.append(pooled([x for x in AGED if x != 'S06-D'], a, b, 'excluding S06-D (duplicate of S06-C) (10)'))
    rows.append(pooled([x for x in AGED if x not in ('S06-D', 'S03-I', 'S03-J')], a, b, 'excluding S06-D and label-conflicted S03-I/S03-J (8)'))
    rows.append(pooled([x for x in AGED if x not in ('S06-C', 'S06-D', 'S03-I', 'S03-J')], a, b, 'excluding both copies S06-C/S06-D and S03-I/S03-J (7)'))
    for tm in ['d2-3', 'd14', 'd60', 'other strain (timing n.s.)']:
        rows.append(pooled([x for x in AGED if TIMING[x] == tm], a, b, f'timing {tm}, as printed'))
    rows.append(pooled([x for x in AGED if TIMING[x] == 'd2-3' and x != 'S06-D'], a, b, 'timing d2-3 excluding S06-D'))
P = pd.DataFrame([r for r in rows if r])
P.to_csv(TABLES + 'T7_survival_pooled.csv', index=False)
print(P.round(4).to_string())

# ---- durability: PSLN-344 d14 vs d60, and vs unchallenged untreated aged controls
print('\n--- durability / background mortality ---')
def count(blocks, g):
    s = n = 0
    for blk in blocks:
        A = get(blk, g)
        if A is not None: s += int((A[1] == 0).sum()); n += len(A[1])
    return s, n
d14 = count(['S03-I', 'S06-A', 'S06-C'], 'PSLN-344'); d60 = count(['S06-E (rows 34-68)', 'S06-F (rows 34-68)', 'S06-G'], 'PSLN-344')
d14het = count(['S06-A', 'S06-C'], 'PSLN-344')
unt = count(['S06-E (rows 34-68)', 'S06-F (rows 34-68)', 'S06-G'], 'Untreated')
y60 = count(['S06-E (rows 34-68)', 'S06-F (rows 34-68)', 'S06-G'], 'PSLN-212(Y)')
p212_60 = count(['S06-E (rows 34-68)', 'S06-F (rows 34-68)', 'S06-G'], 'PSLN-212')
dur = []
def fis(a, b): return stats.fisher_exact([[a[0], a[1] - a[0]], [b[0], b[1] - b[0]]])[1]
for lab, x in [('PSLN-344 aged, d14 challenges (S03-I, S06-A, S06-C)', d14), ('PSLN-344 aged, d14 heterosubtypic only (S06-A, S06-C)', d14het),
               ('PSLN-344 aged, d60 challenges (S06-E, S06-F, S06-G)', d60),
               ('Untreated UNCHALLENGED aged, same 14-d window at d60 (S06-E/F/G)', unt), ('PSLN-212(Y) young, d60', y60), ('PSLN-212 aged, d60', p212_60)]:
    lo, hi = clopper_pearson(*x); dur.append(dict(group=lab, survivors=x[0], n=x[1], pct=100 * x[0] / x[1], lo=100 * lo, hi=100 * hi))
D = pd.DataFrame(dur); print(D.round(1).to_string())
tests = [('PSLN-344 d14 (all 3) vs d60', fis(d14, d60)), ('PSLN-344 d14 heterosubtypic vs d60', fis(d14het, d60)),
         ('PSLN-344 d60 vs Untreated unchallenged d60', fis(d60, unt)), ('PSLN-344 d60 vs PSLN-212(Y) d60', fis(d60, y60)),
         ('PSLN-344 d60 vs PSLN-212 aged d60', fis(d60, p212_60))]
for t in tests: print(f'Fisher exact  {t[0]}: p = {t[1]:.4f}')
D.to_csv(TABLES + 'T8_durability_background.csv', index=False)
pd.DataFrame(tests, columns=['comparison', 'p_fisher']).to_csv(TABLES + 'T8b_durability_tests.csv', index=False)

# stratified logrank PSLN-344 vs untreated at d60
st = [(*get(b, 'PSLN-344'), *get(b, 'Untreated')) for b in ['S06-E (rows 34-68)', 'S06-F (rows 34-68)', 'S06-G']]
print('stratified log-rank PSLN-344 (challenged) vs Untreated (unchallenged) at d60:', stratified_logrank(st))

# ---- rapid protection summary incl. S15-H and S03-J
print('\n--- rapid protection (challenge 2-3 d after a single dose), PSLN-344 + antigen ---')
rap = [('S03-J', 'PSLN-344'), ('S06-B', 'PSLN-344'), ('S06-D', 'PSLN-344'), ('S15-H', '3d Vaccine+PSLN-344')]
s = n = 0
for blk, g in rap:
    A = get(blk, g); k = int((A[1] == 0).sum()); print(blk, g, f'{k}/{len(A[1])}'); s += k; n += len(A[1])
print('pooled', s, n, clopper_pearson(s, n))
s2 = s - 7; n2 = n - 7
print('pooled excluding S06-D', s2, n2, clopper_pearson(s2, n2))

# ---- sensitivity: weight-implied death counts (T2) instead of survival-table counts
x = pd.read_csv(TABLES + 'T2_survival_vs_weight_crosscheck.csv')
print('\n--- sensitivity: survivors implied by body-weight traces (aged experiments) ---')
for g in ['PSLN-344', 'PSLN-212', 'PSLN-212(Y)', 'Sham']:
    t = x[(x.group == g) & x.surv_block.isin(AGED) & x.wt_n.notna()]
    tb = x[(x.group == g) & x.surv_block.isin(AGED) & x.surv_n.notna() & x.wt_n.notna()]
    print(g, 'by weights:', int((t.wt_n - t.wt_deaths).sum()), '/', int(t.wt_n.sum()), '| same blocks by survival tables:', int((tb.surv_n - tb.surv_deaths).sum()), '/', int(tb.surv_n.sum()))
