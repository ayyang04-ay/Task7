"""
Survival analysis of every time-to-event block, as printed.
Per group: n, deaths, survivors, % survival with exact (Clopper-Pearson) 95% CI, median time to death.
Contrasts: log-rank (asymptotic + exact permutation) and Fisher exact on end-of-study survival.
"""
from paths import TABLES, FIGS, OUT as OUTDIR, BUILD, PANDOC
import pandas as pd, numpy as np, math
from scipy import stats
import psln_blocks as pb
from stats_util import *
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 3000); pd.set_option('display.max_colwidth', 120)
df = pb.tidy()
sv = df[df.kind == 'surv'].copy()

META = {   # block -> description (from the annotation PDF)
 'S03-I': dict(strain='BALB/c aged', vaccine='bivalent (CA09 H1N1 + Aichi H3N2)', challenge='10x mLD50 CA09 H1N1', day='d14', match='homologous', obs=14),
 'S03-J': dict(strain='BALB/c aged (age not restated)', vaccine='rgH5N1, single dose', challenge='wild-type VN04 H5N1', day='d2', match='homologous subtype (rapid)', obs=22),
 'S06-A': dict(strain='BALB/c aged', vaccine='Aichi H3N2', challenge='5x mLD50 PR8 H1N1', day='d14', match='heterosubtypic', obs=14),
 'S06-B': dict(strain='BALB/c aged', vaccine='Aichi H3N2', challenge='5x mLD50 PR8 H1N1', day='d3', match='heterosubtypic (rapid)', obs=14),
 'S06-C': dict(strain='BALB/c aged', vaccine='bivalent', challenge='5x mLD50 rgH5N1', day='d14', match='heterosubtypic', obs=14),
 'S06-D': dict(strain='BALB/c aged', vaccine='bivalent', challenge='5x mLD50 rgH5N1', day='d3', match='heterosubtypic (rapid)', obs=14),
 'S06-E (rows 34-68)': dict(strain='BALB/c aged', vaccine='Aichi H3N2', challenge='5x mLD50 PR8 H1N1', day='d60', match='heterosubtypic (durability)', obs=14),
 'S06-F (rows 34-68)': dict(strain='BALB/c aged', vaccine='bivalent', challenge='5x mLD50 rgH5N1', day='d60', match='heterosubtypic (durability)', obs=14),
 'S06-G': dict(strain='BALB/c aged', vaccine='CA09 H1N1', challenge='5x mLD50 Perth H3N2', day='d60', match='heterosubtypic (durability)', obs=14),
 'S06-E (rows 71-105)': dict(strain='BALB/c 14 mo (10 mo + 4 mo)', vaccine='bivalent', challenge='5x LD50 PR8 H1N1', day='not stated', match='imprinting study', obs=14),
 'S06-F (rows 71-105)': dict(strain='BALB/c 14 mo (10 mo + 4 mo)', vaccine='bivalent', challenge='5x LD50 Perth H3N2', day='d14', match='imprinting study', obs=14),
 'S09-B': dict(strain='BALB/c young', vaccine='Aichi H3N2', challenge='5x mLD50 PR8 H1N1', day='d21', match='heterosubtypic', obs=14),
 'S09-D': dict(strain='BALB/c young', vaccine='CA09 H1N1', challenge='5x mLD50 Perth H3N2', day='d21', match='heterosubtypic', obs=14),
 'S09-F': dict(strain='BALB/c young', vaccine='bivalent', challenge='5x mLD50 VN04 rgH5N1', day='d180', match='heterosubtypic (durability)', obs=14),
 'S13-E': dict(strain='BALB/c young', vaccine='bivalent', challenge='10x mLD50 CA09 H1N1', day='d14', match='homologous', obs=14),
 'S15-H': dict(strain='BALB/c aged', vaccine='bivalent / none', challenge='5x mLD50 VN04 rgH5N1', day='d3', match='adjuvant-alone control', obs=14),
 'S15-L': dict(strain='C57BL/6 aged 20 mo', vaccine='bivalent', challenge='not stated', day='not stated', match='second strain', obs=14),
 'S15-N': dict(strain='Swiss Webster aged 20 mo (outbred)', vaccine='bivalent', challenge='not stated', day='not stated', match='third strain', obs=14),
}

rows = []
for (blk, g), t in sv.groupby(['block', 'group'], sort=False):
    if blk not in META: continue
    obs_end = META[blk]['obs']
    tt = t.value.fillna(21 if blk == 'S03-J' else obs_end)   # S03-J PSLN-344 animal 10: flag present, day cell empty -> censored at end
    n = len(t); d = int((t.event == 1).sum()); s = n - d
    lo, hi = clopper_pearson(s, n)
    rows.append(dict(block=blk, **{k: META[blk][k] for k in ['strain', 'vaccine', 'challenge', 'day', 'match']}, group=g, n=n, deaths=d, survivors=s,
                     surv_pct=100 * s / n, ci_lo=100 * lo, ci_hi=100 * hi, median_days_to_death=km_median(tt, t.event),
                     death_days=sorted(t[t.event == 1].value.tolist()), cells=f"{t.cell.iloc[0]} .. {t.cell.iloc[-1]}",
                     note='; '.join(x for x in t.note.dropna().unique())))
S = pd.DataFrame(rows)
S.to_csv(TABLES + 'T5_survival_by_block.csv', index=False)
print(S[['block', 'day', 'challenge', 'group', 'n', 'deaths', 'survivors', 'surv_pct', 'ci_lo', 'ci_hi', 'median_days_to_death']].round(1).to_string())

def get(blk, g):
    t = sv[(sv.block == blk) & (sv.group == g)]
    if len(t) == 0: return None
    end = 21 if blk == 'S03-J' else META[blk]['obs']
    return t.value.fillna(end).to_numpy(float), t.event.to_numpy(int)

CONTRASTS = [('PSLN-344', 'Sham'), ('PSLN-344', 'PSLN-212'), ('PSLN-344', 'PSLN-212(Y)'), ('PSLN-212', 'Sham'), ('PSLN-212', 'PSLN-212(Y)'),
             ('PSLN-344', 'CMP-204'), ('CMP-204', 'PSLN-212'), ('PSLN-344', 'Untreated'),
             ('Naive+PSLN-344', 'Naive+PSLN-212'), ('Imprinting+PSLN-344', 'Imprinting+PSLN-212'), ('Imprinting+PSLN-212', 'Naive+PSLN-212'),
             ('Imprinting+PSLN-344', 'Naive+PSLN-344'),
             ('3d Vaccine+PSLN-344', '3d Vaccine'), ('3d Vaccine+PSLN-344', '3d PSLN-344'), ('3d PSLN-344', '3d Vaccine'),
             ('PSLN-344Y', 'PSLN-212Y'), ('PSLN-344Y', 'Sham'), ('PSLN-212Y', 'Sham'), ('PSLN-344(Y)', 'Sham'), ('CMP-204(Y)', 'Sham'), ('Sham', 'Naive'),
             ('PSLN-344(Y)', 'CMP-204(Y)')]
crow = []
for blk in META:
    for a, b in CONTRASTS:
        A, B = get(blk, a), get(blk, b)
        if A is None or B is None: continue
        lr = logrank_test(A[0], A[1], B[0], B[1])
        sa, sb = int((A[1] == 0).sum()), int((B[1] == 0).sum())
        fis = stats.fisher_exact([[sa, len(A[1]) - sa], [sb, len(B[1]) - sb]])[1]
        crow.append(dict(block=blk, contrast=f'{a} vs {b}', surv_a=f'{sa}/{len(A[1])}', surv_b=f'{sb}/{len(B[1])}',
                         risk_diff_pct=100 * (sa / len(A[1]) - sb / len(B[1])), logrank_chi2=lr['chi2'], p_logrank_asym=lr['p_asym'],
                         p_logrank_exact=lr['p_exact'], p_fisher=fis))
Cn = pd.DataFrame(crow)
Cn.to_csv(TABLES + 'T6_survival_contrasts.csv', index=False)
print()
print(Cn.round(4).to_string())
