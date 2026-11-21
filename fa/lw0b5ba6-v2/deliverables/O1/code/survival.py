"""Survival analysis: per experiment (log-rank, Fisher exact, exact CIs) and pooled stratified analyses
for aged PSLN-344 vs aged PSLN-212, with sensitivity sets addressing the data-integrity findings."""
import pandas as pd, numpy as np
from scipy import stats
from lifelines.statistics import logrank_test
from statsmodels.stats.contingency_tables import StratifiedTable
from statsmodels.stats.proportion import proportion_confint

T = pd.read_csv('/tmp/work/tidy/tte.csv')
T['group'] = T.group.str.replace('PSLN-212Y', 'PSLN-212(Y)').str.replace('PSLN-344Y', 'PSLN-344(Y)')
# S03-J PSLN-344 animal 10: event=0 but day missing (S03!G46). Observation ran 22 d; all other censored rows = 21.
T.loc[(T.block == 'S03-J') & T.time.isna(), 'time'] = 21.0

META = {  # block: (population, vaccine -> challenge, challenge day post-vax, relation)
    'S03-I': ('aged BALB/c', 'bivalent -> CA09 H1N1 10xLD50', 14, 'homologous'),
    'S03-J': ('BALB/c (age not stated; no (Y) label)', 'rgH5N1 -> wt VN04 H5N1', 2, 'homologous H5, rapid'),
    'S06-A': ('aged BALB/c', 'Aichi H3N2 -> PR8 H1N1', 14, 'heterosubtypic'),
    'S06-B': ('aged BALB/c', 'Aichi H3N2 -> PR8 H1N1', 3, 'heterosubtypic, rapid'),
    'S06-C': ('aged BALB/c', 'bivalent -> rgH5N1', 14, 'heterosubtypic'),
    'S06-D': ('aged BALB/c', 'bivalent -> rgH5N1', 3, 'heterosubtypic, rapid [DUPLICATE of S06-C]'),
    'S06-E': ('aged BALB/c', 'Aichi H3N2 -> PR8 H1N1', 60, 'heterosubtypic, durability'),
    'S06-F': ('aged BALB/c', 'bivalent -> rgH5N1', 60, 'heterosubtypic, durability'),
    'S06-G': ('aged BALB/c', 'CA09 H1N1 -> Perth H3N2', 60, 'heterosubtypic, durability'),
    'S06-E[imprint]': ('14-mo BALB/c (+/- PR8 imprinting)', 'bivalent -> PR8 H1N1', None, 'imprinting'),
    'S06-F[imprint]': ('14-mo BALB/c (+/- PR8 imprinting)', 'bivalent -> Perth H3N2', 14, 'imprinting'),
    'S15-L': ('aged C57BL/6', 'bivalent -> (challenge not stated)', None, 'strain generality'),
    'S15-N': ('aged Swiss Webster', 'bivalent -> (challenge not stated)', None, 'strain generality'),
    'S15-H': ('aged BALB/c', 'bivalent +/- PSLN-344 -> VN04 rgH5N1', 3, 'antigen requirement'),
    'S09-B': ('young BALB/c', 'Aichi H3N2 -> PR8 H1N1', 21, 'young'),
    'S09-D': ('young BALB/c', 'CA09 H1N1 -> Perth H3N2', 21, 'young'),
    'S09-F': ('young BALB/c', 'bivalent -> VN04 rgH5N1', 180, 'young, durability'),
    'S13-E': ('young BALB/c', 'bivalent -> CA09 H1N1 10xLD50', 14, 'young'),
}

def cp(k, n):
    lo, hi = proportion_confint(k, n, alpha=0.05, method='beta'); return lo, hi

rows = []
for blk, d in T.groupby('block'):
    grp = {g: dd for g, dd in d.groupby('group')}
    for g, dd in grp.items():
        n = len(dd); s = int((dd.event == 0).sum()); lo, hi = cp(s, n)
        md = dd[dd.event == 1].time.median() if (dd.event == 1).any() else np.nan
        rows.append(dict(block=blk, population=META.get(blk, ('',))[0], design=META.get(blk, ('', ''))[1],
                         group=g, n=n, survivors=s, pct=100 * s / n, ci_lo=100 * lo, ci_hi=100 * hi,
                         median_death_day_among_deaths=md,
                         cells=f"{dd.cell_event.iloc[0]}:{dd.cell_event.iloc[-1]}"))
S = pd.DataFrame(rows)
S.to_csv('/tmp/work/survival_by_group.csv', index=False)

pairs = [('PSLN-344', 'PSLN-212'), ('PSLN-344', 'Sham'), ('PSLN-212', 'Sham'), ('PSLN-344', 'PSLN-212(Y)'),
         ('Naive+PSLN-344', 'Naive+PSLN-212'), ('Imprinting+PSLN-344', 'Imprinting+PSLN-212'),
         ('PSLN-344(Y)', 'PSLN-212(Y)'), ('PSLN-344(Y)', 'Sham'), ('PSLN-212(Y)', 'Sham'),
         ('3d Vaccine+PSLN-344', '3d Vaccine'), ('3d Vaccine+PSLN-344', '3d PSLN-344'), ('PSLN-344(Y)', 'CMP-204(Y)'),
         ('CMP-204', 'Sham'), ('PSLN-344', 'CMP-204')]
prow = []
for blk, d in T.groupby('block'):
    for a, b in pairs:
        da, db = d[d.group == a], d[d.group == b]
        if len(da) == 0 or len(db) == 0: continue
        lr = logrank_test(da.time, db.time, da.event, db.event)
        sa, sb = int((da.event == 0).sum()), int((db.event == 0).sum())
        fe = stats.fisher_exact([[sa, len(da) - sa], [sb, len(db) - sb]])
        prow.append(dict(block=blk, A=a, B=b, surv_A=f'{sa}/{len(da)}', surv_B=f'{sb}/{len(db)}',
                         diff_pp=100 * (sa / len(da) - sb / len(db)), p_logrank=lr.p_value, p_fisher=fe[1]))
P = pd.DataFrame(prow)
P.to_csv('/tmp/work/survival_pairwise.csv', index=False)

# ---------- pooled aged PSLN-344 vs PSLN-212 ----------
strata_all = [('S03-I', 'PSLN-344', 'PSLN-212'), ('S03-J', 'PSLN-344', 'PSLN-212'), ('S06-A', 'PSLN-344', 'PSLN-212'),
              ('S06-B', 'PSLN-344', 'PSLN-212'), ('S06-C', 'PSLN-344', 'PSLN-212'), ('S06-E', 'PSLN-344', 'PSLN-212'),
              ('S06-F', 'PSLN-344', 'PSLN-212'), ('S06-G', 'PSLN-344', 'PSLN-212'),
              ('S06-E[imprint]', 'Naive+PSLN-344', 'Naive+PSLN-212'), ('S06-E[imprint]', 'Imprinting+PSLN-344', 'Imprinting+PSLN-212'),
              ('S06-F[imprint]', 'Naive+PSLN-344', 'Naive+PSLN-212'), ('S06-F[imprint]', 'Imprinting+PSLN-344', 'Imprinting+PSLN-212'),
              ('S15-L', 'PSLN-344', 'PSLN-212'), ('S15-N', 'PSLN-344', 'PSLN-212')]

def table(blk, a, b, override=None):
    d = T[T.block == blk]
    sa = int((d[d.group == a].event == 0).sum()); na = (d.group == a).sum()
    sb = int((d[d.group == b].event == 0).sum()); nb = (d.group == b).sum()
    if override and (blk, a) in override: sa = override[(blk, a)]
    if override and (blk, b) in override: sb = override[(blk, b)]
    return sa, na, sb, nb

def strat_logrank(strata):
    O = E = Vv = 0
    for blk, a, b in strata:
        d = T[T.block == blk]; da = d[d.group == a]; db = d[d.group == b]
        times = sorted(set(pd.concat([da, db]).query('event==1').time))
        for t in times:
            na = (da.time >= t).sum(); nb = (db.time >= t).sum(); n = na + nb
            oa = ((da.time == t) & (da.event == 1)).sum(); o = oa + ((db.time == t) & (db.event == 1)).sum()
            if n < 2: continue
            e = o * na / n; v = o * (na / n) * (1 - na / n) * (n - o) / (n - 1)
            O += oa; E += e; Vv += v
    chi = (O - E) ** 2 / Vv; return O, E, chi, stats.chi2.sf(chi, 1)

def mh_rd(tabs):
    # Mantel-Haenszel risk difference (survival) with Greenland-Robins/Sato variance
    num = den = 0; var_num = 0
    for sa, na, sb, nb in tabs:
        N = na + nb; w = na * nb / N
        pa, pb = sa / na, sb / nb
        num += w * (pa - pb); den += w
    rd = num / den
    # Sato (1989) variance
    P_ = Q_ = 0
    for sa, na, sb, nb in tabs:
        N = na + nb
        P_ += (nb ** 2 * sa - na ** 2 * sb + na * nb * (nb - na) / 2) / N ** 2
        Q_ += (sa * (nb - sb) + sb * (na - sa)) / (2 * N)
    var = (rd * P_ + Q_) / den ** 2
    se = np.sqrt(var); return rd, rd - 1.96 * se, rd + 1.96 * se

def summarize(name, strata, override=None):
    tabs = [table(*s, override=override) for s in strata]
    tot = np.array(tabs).sum(0)
    rd, lo, hi = mh_rd(tabs)
    st = StratifiedTable([np.array([[sa, na - sa], [sb, nb - sb]]) for sa, na, sb, nb in tabs], shift_zeros=True)
    cmh = st.test_null_odds(correction=True)
    O, E, chi, p_lr = strat_logrank(strata)
    n_favour = sum(1 for sa, na, sb, nb in tabs if sa / na > sb / nb); n_tie = sum(1 for sa, na, sb, nb in tabs if sa / na == sb / nb)
    sign_p = stats.binomtest(n_favour, len(tabs) - n_tie, 0.5).pvalue if len(tabs) - n_tie > 0 else np.nan
    return dict(analysis=name, strata=len(tabs), surv_344=f'{tot[0]}/{tot[1]}', pct_344=100 * tot[0] / tot[1],
                surv_212=f'{tot[2]}/{tot[3]}', pct_212=100 * tot[2] / tot[3], MH_RD_pp=100 * rd, RD_lo=100 * lo, RD_hi=100 * hi,
                MH_OR=st.oddsratio_pooled, CMH_p=cmh.pvalue, strat_logrank_chi2=chi, strat_logrank_p=p_lr,
                strata_favouring_344=f'{n_favour}/{len(tabs)} (ties {n_tie})', sign_test_p=sign_p,
                breslow_day_p=st.test_equal_odds().pvalue)

res = [summarize('A. As recorded (S06-D excluded as exact duplicate of S06-C)', strata_all)]
conflict = {'S03-I', 'S03-J', 'S06-C', 'S06-E', 'S06-G', 'S15-L', 'S15-N'}
res.append(summarize('B. Excluding experiments whose survival record conflicts with the body-weight record',
                     [s for s in strata_all if s[0] not in conflict]))
# C: worst case for PSLN-344: where body-weight implies different counts, take whichever is less favourable to 344
worst = {('S03-I', 'PSLN-212'): 3, ('S06-C', 'PSLN-212'): 2, ('S06-E', 'PSLN-212'): 1, ('S06-E', 'PSLN-344'): 5,
         ('S15-L', 'PSLN-212'): 1, ('S15-N', 'PSLN-212'): 3, ('S06-G', 'PSLN-344'): 4}
strata_c = strata_all + [('S06-D', 'PSLN-344', 'PSLN-212')]
worst_c = dict(worst); worst_c[('S06-D', 'PSLN-344')] = 5; worst_c[('S06-D', 'PSLN-212')] = 3  # BW-implied S15-D counts
rc = summarize('C. Worst case for PSLN-344 (BW-implied counts where less favourable; S06-D re-entered with S15-D BW counts)',
               strata_c, override=worst_c)
rc['strat_logrank_p'] = np.nan; rc['strat_logrank_chi2'] = np.nan  # log-rank not defined for count overrides
res.append(rc)
res.append(summarize('D. Aged BALB/c S06 series only (S06-A,B,C,E,F,G; challenge d3, d14 or d60)',
                     [s for s in strata_all if s[0] in ('S06-A', 'S06-B', 'S06-C', 'S06-E', 'S06-F', 'S06-G')]))
res.append(summarize('E. Durability only (challenge at day 60: S06-E,F,G)', [s for s in strata_all if s[0] in ('S06-E', 'S06-F', 'S06-G')]))
res.append(summarize('F. Rapid onset (challenge day 2-3: S03-J, S06-B)', [s for s in strata_all if s[0] in ('S03-J', 'S06-B')]))
# leave-one-out on A
loo = []
for s in sorted(set(x[0] for x in strata_all)):
    r = summarize(f'LOO drop {s}', [x for x in strata_all if x[0] != s]); loo.append(r)
R = pd.DataFrame(res); L = pd.DataFrame(loo)
R.to_csv('/tmp/work/survival_pooled.csv', index=False); L.to_csv('/tmp/work/survival_loo.csv', index=False)

# pooled aged arms vs sham and young benchmark (as recorded, S06-D excluded)
aged_blocks = ['S03-I', 'S03-J', 'S06-A', 'S06-B', 'S06-C', 'S06-E', 'S06-F', 'S06-G', 'S15-L', 'S15-N']
pool = []
for g in ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)', 'CMP-204']:
    d = T[T.block.isin(aged_blocks) & (T.group == g)]
    if len(d):
        s = int((d.event == 0).sum()); n = len(d); lo, hi = cp(s, n)
        pool.append(dict(group=g, blocks=','.join(sorted(d.block.unique())), survivors=s, n=n, pct=100 * s / n, lo=100 * lo, hi=100 * hi))
PO = pd.DataFrame(pool); PO.to_csv('/tmp/work/survival_pooled_arms.csv', index=False)

pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30); pd.set_option('display.max_colwidth', 60)
print(S.round(1).to_string(index=False)); print()
print(P.round(4).to_string(index=False)); print()
print(R.round(4).T.to_string()); print()
print(L[['analysis', 'surv_344', 'surv_212', 'MH_RD_pp', 'RD_lo', 'RD_hi', 'CMH_p', 'strat_logrank_p']].round(4).to_string(index=False)); print()
print(PO.round(1).to_string(index=False))
