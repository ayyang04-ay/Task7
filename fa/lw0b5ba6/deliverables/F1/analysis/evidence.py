"""
evidence.py -- every number quoted in the proposal is defined here, computed from the workbook cells,
and tied to (a) the cells it comes from and (b) the analysis that produced it.
The proposal template refers to these items by key; build_report.py assigns the [E#] tags.
"""
from paths import TABLES, FIGS, OUT as OUTDIR, BUILD, PANDOC
import numpy as np, pandas as pd, math, warnings
from collections import OrderedDict
from scipy import stats
import psln_blocks as pb
from stats_util import *
warnings.filterwarnings('ignore')
df = pb.tidy(); sv = df[df.kind == 'surv']
T = TABLES

RANGE = {
 'S01-A': 'S01!A2:L10', 'S01-B': 'S01!A14:F17', 'S01-C': 'S01!A20:E21', 'S01-D': 'S01!A23:U28', 'S01-E': 'S01!A29:Z34', 'S01-F': 'S01!A35:Z36', 'S01-G': 'S01!A37:Z38',
 'S02-A': 'S02!A2:D7', 'S02-B': 'S02!F2:I7', 'S02-C': 'S02!K2:O7', 'S02-D CD40': 'S02!A9:D14', 'S02-D CD86': 'S02!F9:I14', 'S02-E': 'S02!K9:O14', 'S02-F': 'S02!A16:P19',
 'S02-G': 'S02!B21:D26', 'S02-H': 'S02!B29:F34', 'S02-I': 'S02!H29:I34',
 'S03-A': 'S03!A2:E7', 'S03-B': 'S03!G2:I7', 'S03-C': 'S03!K2:O7', 'S03-D': 'S03!Q2:U7', 'S03-E': 'S03!A9:E14', 'S03-F': 'S03!G9:I14', 'S03-G': 'S03!K9:O14', 'S03-H': 'S03!Q9:U14',
 'S03-I': 'S03!A16:F51', 'S03-J': 'S03!G16:J46', 'S03-K': 'S03!L16:O21', 'S03-L': 'S03!K25:Q28',
 'S04-A': 'S04!A1:K5', 'S04-B Foxp3+': 'S04!A7:D12', 'S04-B Tfh:Tfr': 'S04!A14:D19', 'S04-C': 'S04!A21:D26', 'S04-D': 'S04!A28:D31',
 'S05-A': 'S05!A2:I5', 'S05-B': 'S05!A7:I10', 'S05-C': 'S05!A12:D15', 'S05-D': 'S05!A18:D23', 'S05-E': 'S05!A25:D30', 'S05-F': 'S05!A32:D37', 'S05-G': 'S05!A39:D44',
 'S05-H': 'S05!A46:D51', 'S05-I': 'S05!A53:D58',
 'S06-A': 'S06!A2:E30', 'S06-B': 'S06!G2:K30', 'S06-C': 'S06!M2:Q30', 'S06-D': 'S06!A33:E61', 'S06-E (rows 34-68)': 'S06!G33:L68', 'S06-F (rows 34-68)': 'S06!M33:R68',
 'S06-G': 'S06!A70:F105', 'S06-E (rows 71-105)': 'S06!G70:K98', 'S06-F (rows 71-105)': 'S06!M70:Q98',
 'S07-A': 'S07!A2:H7', 'S07-B': 'S07!B8:F14', 'S07-C': 'S07!B15:C20',
 'S08-A': 'S08!A2:M7', 'S08-B': 'S08!A10:O11', 'S08-C': 'S08!A13:D18', 'S08-D': 'S08!A20:AE26', 'S08 rows 89-101': 'S08!A89:D101',
 'S09-A (cols A-U)': 'S09!A2:V9', 'S09-A (cols X-AS)': 'S09!X2:AS9', 'S09-B': 'S09!A11:D35', 'S09-C': 'S09!F11:AD19', 'S09-D': 'S09!A38:D62', 'S09-E': 'S09!F38:AD46',
 'S09-F': 'S09!A65:D88', 'S09-G': 'S09!F65:AD73',
 'S10-A': 'S10!A2:N7', 'S11-A': 'S11!A2:U7', 'S11-B': 'S11!A9:U14', 'S11-C': 'S11!A16:B21', 'S11-D': 'S11!A23:U28', 'S11-E': 'S11!A30:D35', 'S12-A': 'S12!A2:B5',
 'S13-A': 'S13!A2:C7', 'S13-B': 'S13!E2:G7', 'S13-C': 'S13!I2:K7', 'S13-D': 'S13!M2:O7', 'S13-E': 'S13!R2:V30', 'S13-F': 'S13!A32:AJ40', 'S13-G': 'S13!A42:AE50',
 'S13-H': 'S13!A52:D57', 'S13-I': 'S13!F52:J57', 'S13-J': 'S13!L52:P57', 'S14-A H1N1': 'S14!A2:D7', 'S14-A H3N2': 'S14!F2:I7',
 'S15-A': 'S15!A2:AC10', 'S15-B': 'S15!A12:AC20', 'S15-C': 'S15!A22:AC30', 'S15-D': 'S15!A32:AC40', 'S15-E': 'S15!A42:AJ50', 'S15-F': 'S15!A52:AJ60', 'S15-G': 'S15!A62:AJ70',
 'S15-H': 'S15!A72:D93', 'S15-I': 'S15!H71:AC79', 'S15-J': 'S15!H82:AJ90', 'S15-K': 'S15!H92:AJ100', 'S15-L': 'S15!A102:E130', 'S15-M': 'S15!H102:AJ110',
 'S15-N': 'S15!A133:E161', 'S15-O': 'S15!H133:AJ141',
}
def R(*blocks):
    return '; '.join(f"{b.replace(' (rows 34-68)', ' [rows 34-68]').replace(' (rows 71-105)', ' [rows 71-105]')} ({RANGE[b]})" for b in blocks)

AGED11 = ['S03-I', 'S03-J', 'S06-A', 'S06-B', 'S06-C', 'S06-D', 'S06-E (rows 34-68)', 'S06-F (rows 34-68)', 'S06-G', 'S15-L', 'S15-N']
CLEAN8 = [b for b in AGED11 if b not in ('S03-I', 'S03-J', 'S06-D')]
D60 = ['S06-E (rows 34-68)', 'S06-F (rows 34-68)', 'S06-G']

def v(block, group, analyte=None, x=None):
    t = df[(df.block == block) & (df.group == group)]
    if analyte is not None: t = t[t.analyte.str.contains(analyte, regex=False)]
    if x is not None: t = t[t.x.astype(str) == str(x)]
    return t.sort_values('rep').value.to_numpy(float)
gmean = lambda a: float(10 ** np.mean(np.log10(np.where(np.asarray(a) <= 0, 5.0, a))))
def surv(blocks, g):
    s = n = 0
    for b in blocks:
        t = sv[(sv.block == b) & (sv.group == g)]
        s += int((t.event == 0).sum()); n += len(t)
    return s, n
def prop(s, n, ci=True, of=' of '):
    lo, hi = clopper_pearson(s, n)
    return f"{s}{of}{n} ({100*s/n:.0f}%; 95% CI {100*lo:.0f}–{100*hi:.0f}%)" if ci else f"{s}{of}{n} ({100*s/n:.0f}%)"
def pfmt(p):
    if p < 1e-4:
        e = int(math.floor(math.log10(p))); m = p / 10 ** e
        if round(m) == 10: m, e = 1, e + 1
        sup = str(e).translate(str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹'))
        return f"{m:.0f}×10{sup}"
    if p < 0.001: return f"{p:.4f}"
    if p < 0.01: return f"{p:.3f}"
    return f"{p:.2f}" if p >= 0.095 else f"{p:.3f}"
def gmr(a, b):
    la, lb = np.log10(np.where(a <= 0, 5.0, a)), np.log10(np.where(b <= 0, 5.0, b)); w = welch(la, lb)
    return 10 ** w['diff'], 10 ** w['lo'], 10 ** w['hi'], w['p']
def tukey_p(block, a, b, analyte=None, x=None, log=False):
    t = df[df.block == block]
    if analyte is not None: t = t[t.analyte.str.contains(analyte, regex=False)]
    if x is not None: t = t[t.x.astype(str) == str(x)]
    G = OrderedDict((g, (np.log10(np.where(tg.value <= 0, 5.0, tg.value)) if log else tg.value.to_numpy(float))) for g, tg in t.groupby('group', sort=False))
    _, _, tk = tukey(G)
    return tk[(a, b)][3] if (a, b) in tk else tk[(b, a)][3]

E = OrderedDict()
def ev(key, statement, data, analysis, **vals):
    assert key not in E, key
    E[key] = dict(statement=statement, data=data, analysis=analysis, vals=vals)

P7 = pd.read_csv(T + 'T7_survival_pooled.csv'); COX = pd.read_csv(T + 'T7b_stratified_cox.csv')
def p7(analysis, contrast): return P7[(P7.analysis == analysis) & (P7.contrast == contrast)].iloc[0]

# ------------------------------------------------------------------ survival: pooled
for tag, blocks, lab, an in [('clean8', CLEAN8, 'the 8 aged-animal challenge experiments that remain when the duplicated survival table (S06-C = S06-D) is counted once and the two label-conflicted tables (S03-I, S03-J) are set aside', 'excluding S06-D and label-conflicted S03-I/S03-J (8)'),
                             ('all11', AGED11, 'all 11 aged-animal challenge experiments, as printed', 'ALL aged experiments, as printed (11)')]:
    s344, s212, ssham, sy = surv(blocks, 'PSLN-344'), surv(blocks, 'PSLN-212'), surv(blocks, 'Sham'), surv(blocks, 'PSLN-212(Y)')
    r = p7(an, 'PSLN-344 vs PSLN-212')
    ev(f'{tag}', f"Survival in {lab}: PSLN-344 {prop(*s344)}; PSLN-212 {prop(*s212)}; vehicle + vaccine {prop(*ssham)}; young PSLN-212 benchmark {prop(*sy)}. "
       f"PSLN-344 vs PSLN-212: Mantel-Haenszel risk difference {r.MH_risk_diff_pct:.0f} points (95% CI {r.rd_lo:.0f} to {r.rd_hi:.0f}); stratified log-rank chi2 {r.strat_logrank_chi2:.1f}, p = {pfmt(r.p_strat_logrank)}.",
       R(*blocks), 'a06_survival_pooled.py -> T7; exact (Clopper-Pearson) CI; log-rank stratified by experiment (matches R survival::survdiff)',
       s344=prop(*s344), s212=prop(*s212), sham=prop(*ssham), young=prop(*sy), s344s=f"{s344[0]} of {s344[1]}", s212s=f"{s212[0]} of {s212[1]}", shams=f"{ssham[0]} of {ssham[1]}",
       youngs=f"{sy[0]} of {sy[1]}", pct344=f"{100*s344[0]/s344[1]:.0f}%", pct212=f"{100*s212[0]/s212[1]:.0f}%", rd=f"{r.MH_risk_diff_pct:.0f}", p=pfmt(r.p_strat_logrank))
c8 = COX[(COX.set == 'clean8') & (COX.contrast == 'PSLN-344 vs PSLN-212')].iloc[0]; c11 = COX[(COX.set == 'all11') & (COX.contrast == 'PSLN-344 vs PSLN-212')].iloc[0]
ev('hr', f"Hazard ratio for death, PSLN-344 vs PSLN-212 in aged animals (Cox model stratified by experiment): {c8.HR_death:.2f} (95% CI {c8.lo:.2f}–{c8.hi:.2f}) in the 8 unflagged experiments; "
   f"{c11.HR_death:.2f} ({c11.lo:.2f}–{c11.hi:.2f}) across all 11.", R(*AGED11), 'R survival::coxph, strata(experiment) -> T7b',
   clean8=f"hazard ratio {c8.HR_death:.2f}, 95% CI {c8.lo:.2f}–{c8.hi:.2f}", all11=f"{c11.HR_death:.2f} ({c11.lo:.2f}–{c11.hi:.2f})")
ev('breadth', "Breadth of the survival effect of PSLN-344 in aged animals: three mouse strains (BALB/c in S03/S06; C57BL/6 6 of 7 in S15-L; outbred Swiss Webster 6 of 7 in S15-N) and five challenge viruses "
   "(CA09 H1N1 S03-I 7/7; PR8 H1N1 S06-A 6/7, S06-B 5/7, S06-E 5/7; Perth H3N2 S06-G 4/7; rgH5N1 S06-C 7/7, S06-F 5/7; wild-type VN04 H5N1 S03-J 10/10).",
   R('S03-I', 'S03-J', 'S06-A', 'S06-B', 'S06-C', 'S06-E (rows 34-68)', 'S06-F (rows 34-68)', 'S06-G', 'S15-L', 'S15-N'), 'a05_survival.py -> T5 (counts per block)')
s = [surv([b], g) for b, g in [('S03-J', 'PSLN-344'), ('S06-B', 'PSLN-344'), ('S15-H', '3d Vaccine+PSLN-344')]]
tot = (sum(x[0] for x in s), sum(x[1] for x in s))
ev('rapid', f"Survival when challenge came 2–3 days after a single dose of vaccine + PSLN-344: {prop(*tot)} (S03-J wild-type H5N1 on day 2: {s[0][0]}/{s[0][1]}; S06-B PR8 on day 3: {s[1][0]}/{s[1][1]}; "
   f"S15-H rgH5N1 on day 3: {s[2][0]}/{s[2][1]}). S06-D (7/7) is not counted because its table is identical to S06-C and conflicts with its own weight block (5 of 7); including it as printed gives 28 of 31.",
   R('S03-J', 'S06-B', 'S15-H', 'S06-D'), 'a06_survival_pooled.py (rapid-protection summary); exact CI', all=prop(*tot), short=f"{tot[0]} of {tot[1]}")
def one(b, g): s_, n_ = surv([b], g); return f"{s_} of {n_}"
ev('hetero', f"Protection against subtypes absent from the vaccine (aged animals, PSLN-344; PSLN-212 in brackets): H3N2 vaccine -> PR8 H1N1 on day 14: {one('S06-A','PSLN-344')} ({one('S06-A','PSLN-212')}) and on day 3: {one('S06-B','PSLN-344')} ({one('S06-B','PSLN-212')}); "
   f"seasonal bivalent H1N1+H3N2 vaccine -> rgH5N1 on day 60: {one('S06-F (rows 34-68)','PSLN-344')} ({one('S06-F (rows 34-68)','PSLN-212')}); on day 14: {one('S06-C','PSLN-344')} ({one('S06-C','PSLN-212')}; table also printed as S06-D, defect D1); "
   f"H1N1 vaccine -> Perth H3N2 on day 60: {one('S06-G','PSLN-344')} ({one('S06-G','PSLN-212')}).",
   R('S06-A', 'S06-B', 'S06-C', 'S06-F (rows 34-68)', 'S06-G'), 'a05_survival.py -> T5', h5=one('S06-C', 'PSLN-344'), h1=one('S06-A', 'PSLN-344'), h3=one('S06-G', 'PSLN-344'), h5d60=one('S06-F (rows 34-68)', 'PSLN-344'))
s0 = surv(['S03-J'], 'PSLN-344'); t = sv[(sv.block == 'S03-J') & (sv.group == 'PSLN-344')]
ev('h5wt', f"Wild-type H5N1 challenge 2 days after one dose (S03-J): PSLN-344 {s0[0]} of {s0[1]} survived ({int(t.value.notna().sum())} records carry a day value, 1 has the survival flag but an empty day cell); "
   f"the two control arms survived {one('S03-J','Sham')} and {one('S03-J','PSLN-212')} (printed 'Sham' and 'PSLN-212'; the paired weight block S13-G labels its arms 'Naive' and 'Sham').",
   R('S03-J', 'S13-G'), 'a05_survival.py -> T5; a02_surv_vs_weight.py -> T2', n=f"{s0[0]} of {s0[1]}")

# ------------------------------------------------------------------ gap to young, durability, background
r = p7('ALL aged experiments, as printed (11)', 'PSLN-344 vs PSLN-212(Y)')
cy = COX[(COX.set == 'all11') & (COX.contrast == 'PSLN-344 vs PSLN-212(Y)')].iloc[0]
ev('gap', f"Aged PSLN-344 vs the young PSLN-212 benchmark in the 10 experiments that had both arms: {r.surv_a} ({r.pct_a:.0f}%) vs {r.surv_b} ({r.pct_b:.0f}%); "
   f"risk difference {r.MH_risk_diff_pct:.0f} points (95% CI {r.rd_lo:.0f} to {r.rd_hi:.0f}); stratified log-rank p = {pfmt(r.p_strat_logrank)}.",
   R(*[b for b in AGED11 if b != 'S03-J']), 'a06_survival_pooled.py -> T7', a=f"{r.surv_a.replace('/', ' of ')} ({r.pct_a:.0f}%)", y=f"{r.surv_b.replace('/', ' of ')} ({r.pct_b:.0f}%)",
   rd=f"{abs(r.MH_risk_diff_pct):.0f} points", p=f"p = {pfmt(r.p_strat_logrank)}")
d14, d60, unt, y60 = surv(['S03-I', 'S06-A', 'S06-C'], 'PSLN-344'), surv(D60, 'PSLN-344'), surv(D60, 'Untreated'), surv(D60, 'PSLN-212(Y)')
fis = lambda a, b: stats.fisher_exact([[a[0], a[1] - a[0]], [b[0], b[1] - b[0]]])[1]
ev('dur', f"Durability in aged animals: PSLN-344 survival {prop(*d14)} when challenged on day 14 (S03-I, S06-A, S06-C) vs {prop(*d60)} when challenged on day 60 (S06-E, S06-F, S06-G); Fisher exact p = {pfmt(fis(d14, d60))}. "
   f"Without the duplicated table S06-C: 13 of 14 vs 14 of 21, p = {pfmt(fis((13, 14), d60))}. Young benchmark at day 60: {y60[0]} of {y60[1]}.", R('S03-I', 'S06-A', 'S06-C', *D60), 'a06_survival_pooled.py -> T8',
   d14=f"{d14[0]} of {d14[1]} ({100*d14[0]/d14[1]:.0f}%)", d60=f"{d60[0]} of {d60[1]} ({100*d60[0]/d60[1]:.0f}%)", p=pfmt(fis(d14, d60)))
lo, hi = clopper_pearson(unt[1] - unt[0], unt[1])
ev('bg', f"Background mortality: {unt[1]-unt[0]} of {unt[1]} untreated, unchallenged aged controls died during the same 14-day observation windows of the day-60 experiments "
   f"(S06-E 1/7, S06-F 0/7, S06-G 3/7) = {100*(unt[1]-unt[0])/unt[1]:.0f}% (95% CI {100*lo:.0f}–{100*hi:.0f}%). PSLN-344 day-60 survival (14/21) vs these controls (17/21): Fisher p = {pfmt(fis(d60, unt))}.",
   R(*D60), 'a06_survival_pooled.py -> T8', deaths=f"{unt[1]-unt[0]} of {unt[1]}", pct=f"{100*(unt[1]-unt[0])/unt[1]:.0f}%", ci=f"{100*lo:.0f}–{100*hi:.0f}%", p=pfmt(fis(d60, unt)))

# ------------------------------------------------------------------ young animals, middle-aged, imprinting, antigen requirement
yb = ['S09-B', 'S09-D', 'S09-F']
a, b, c = surv(yb, 'PSLN-344Y'), surv(yb, 'PSLN-212Y'), surv(yb, 'Sham')
ev('young', f"Young animals (three challenge studies, S09-B, S09-D, S09-F; challenge 21–180 days after one dose): PSLN-344 {a[0]} of {a[1]} survived, PSLN-212 {b[0]} of {b[1]}, vehicle {c[0]} of {c[1]}. "
   "No survival difference between the two formulations in young animals.", R(*yb), 'a05_survival.py -> T5', a=f"{a[0]} of {a[1]}", b=f"{b[0]} of {b[1]}")
ib = ['S06-E (rows 71-105)', 'S06-F (rows 71-105)']
n212, n344, i212, i344 = surv(ib, 'Naive+PSLN-212'), surv(ib, 'Naive+PSLN-344'), surv(ib, 'Imprinting+PSLN-212'), surv(ib, 'Imprinting+PSLN-344')
ev('mid', f"Middle-aged animals (14 months at vaccination: infected or mock-infected at 10 months, vaccinated 4 months later; two challenge studies): previously uninfected animals survived {n212[0]} of {n212[1]} with PSLN-212 "
   f"and {n344[0]} of {n344[1]} with PSLN-344 (Fisher p = {pfmt(fis(n344, n212))}).", R(*ib), 'a05_survival.py -> T5/T6', a=f"{n212[0]} of {n212[1]}", b=f"{n344[0]} of {n344[1]}")
ev('imprint', f"Prior influenza exposure ('imprinting' with PR8 H1N1 four months before vaccination): PSLN-344 protected {i344[0]} of {i344[1]} previously infected and {n344[0]} of {n344[1]} previously uninfected animals; "
   f"PSLN-212 protected {i212[0]} of {i212[1]} previously infected animals (all 4 survivors in the PR8 re-challenge, 0 of 7 against Perth H3N2).", R(*ib), 'a05_survival.py -> T5',
   a=f"{i344[0]} of {i344[1]}", b=f"{n344[0]} of {n344[1]}")
h = [surv(['S15-H'], g) for g in ['3d Vaccine', '3d PSLN-344', '3d Vaccine+PSLN-344']]
ev('antigen', f"Antigen requirement (S15-H, aged, rgH5N1 challenge 3 days after dosing): vaccine alone {h[0][0]} of {h[0][1]} survived, PSLN-344 alone {h[1][0]} of {h[1][1]}, vaccine + PSLN-344 {h[2][0]} of {h[2][1]} "
   f"(Fisher p = {pfmt(fis(h[2], h[1]))} vs either single component). Adjuvant alone did not shorten survival relative to vaccine alone (median day of death 6 vs 5; log-rank exact p = 0.31).",
   R('S15-H'), 'a05_survival.py -> T5/T6', adj=f"{h[1][0]} of {h[1][1]}", vac=f"{h[0][0]} of {h[0][1]}", both=f"{h[2][0]} of {h[2][1]}")
x2 = pd.read_csv(T + 'T2_survival_vs_weight_crosscheck.csv'); w344 = b212 = 0
for blk in AGED11:
    for g in ('PSLN-344', 'PSLN-212'):
        rr = x2[(x2.surv_block == blk) & (x2.group == g)].iloc[0]
        st = int(rr.surv_n - rr.surv_deaths); sw = int(rr.wt_n - rr.wt_deaths) if rr.wt_n == rr.wt_n else st
        if g == 'PSLN-344': w344 += min(st, sw)
        else: b212 += max(st, sw)
ev('worst', f"Worst-case reading of the record: taking, for every one of the 11 experiments, the lower of (survival table, weight-implied survivors) for PSLN-344 and the higher of the two for PSLN-212 "
   f"gives {prop(w344, 80)} vs {prop(b212, 80)}; Fisher p = {pfmt(fis((w344, 80), (b212, 80)))}.", R(*AGED11) + '; paired weight blocks S13-F, S13-G, S15-A..G, S15-M, S15-O',
   'a02_surv_vs_weight.py -> T2; evidence.py', a=f"{w344} of 80", b=f"{b212} of 80", apct=f"{100*w344/80:.0f}%", bpct=f"{100*b212/80:.0f}%")
ev('s15n', "Outbred Swiss Webster (S15-N): PSLN-344 6 of 7 vs PSLN-212 2 of 7 - not significant on its own (log-rank exact p = 0.09; Fisher p = 0.10); vs vehicle 0 of 7, p = 0.003. "
   "Individual experiments have 7 animals per group; several PSLN-344 vs PSLN-212 contrasts are individually borderline, and the conclusion rests on the pooled analysis.",
   R('S15-N'), 'a05_survival.py -> T6')

# ------------------------------------------------------------------ innate / immune read-outs
i212, i344, iy, ish, icmp, i344y = [v('S01-A', g, x='16h') for g in ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)', 'Sham', 'CMP-204', 'PSLN-344(Y)']]
RI = pd.read_csv(T + 'T11_restoration_and_biomarker_triage.csv').set_index('endpoint')
ri = lambda k: RI.loc[k]
g1 = gmr(i212, iy)
ev('ifn', f"Lung Ifnb1 transcript 16 h after one 20 µg intranasal dose (fold vs untreated, mean of 5): aged PSLN-212 {i212.mean():.1f}, aged PSLN-344 {i344.mean():.1f}, young PSLN-212 {iy.mean():.1f}, young PSLN-344 {i344y.mean():.1f}, "
   f"vehicle {ish.mean():.1f}. Aged/young ratio for PSLN-212 {g1[0]:.2f} (95% CI {g1[1]:.2f}–{g1[2]:.2f}); restoration index for PSLN-344 {ri('Ifnb1 lung 16 h').restoration_index:.2f} "
   f"(bootstrap 95% CI {ri('Ifnb1 lung 16 h').RI_lo:.2f}–{ri('Ifnb1 lung 16 h').RI_hi:.2f}); Tukey p (PSLN-344 vs PSLN-212, aged) = {pfmt(tukey_p('S01-A', 'PSLN-212', 'PSLN-344', x='16h', log=True))}.",
   R('S01-A'), 'a07_point_stats.py -> T9/T10 (log scale, one-way ANOVA + Tukey); a08_restoration.py -> T11',
   a=f"{i212.mean():.1f}", m=f"{i344.mean():.1f}", y=f"{iy.mean():.1f}", my=f"{i344y.mean():.1f}", ri=f"{ri('Ifnb1 lung 16 h').restoration_index:.2f}")
g2 = gmr(i212, icmp)
ev('cdn', f"CDN-1807 vs cGAMP in the same liposome without Mn²⁺ (aged animals): lung Ifnb1 at 16 h geometric mean {gmean(i212):.1f} (PSLN-212) vs {gmean(icmp):.1f} (CMP-204), ratio {g2[0]:.1f} (95% CI {g2[1]:.1f}–{g2[2]:.1f}; "
   f"Tukey p = {pfmt(tukey_p('S01-A', 'CMP-204', 'PSLN-212', x='16h', log=True))}). HAI GMT against CA09 {gmean(v('S03-C','PSLN-212')):.0f} vs {gmean(v('S03-C','CMP-204')):.0f} (Tukey p = {pfmt(tukey_p('S03-C','CMP-204','PSLN-212',log=True))}, not significant). "
   f"Survival after CA09 challenge (S03-I, as printed): CMP-204 3 of 7, PSLN-212 0 of 7 - but the control-arm labels of S03-I are in doubt.",
   R('S01-A', 'S03-C', 'S03-I'), 'a07_point_stats.py -> T10', ratio=f"{g2[0]:.1f} times")
hc, ha = gmr(v('S03-C', 'PSLN-344'), v('S03-C', 'PSLN-212')), gmr(v('S03-G', 'PSLN-344'), v('S03-G', 'PSLN-212'))
ev('hai', f"HAI titre on day 14 (geometric mean, n = 5): anti-CA09 H1N1 vehicle {gmean(v('S03-C','Sham')):.0f}, aged PSLN-212 {gmean(v('S03-C','PSLN-212')):.0f}, aged PSLN-344 {gmean(v('S03-C','PSLN-344')):.0f}, young PSLN-212 {gmean(v('S03-C','PSLN-212(Y)')):.0f}; "
   f"anti-Aichi H3N2 {gmean(v('S03-G','Sham')):.0f}, {gmean(v('S03-G','PSLN-212')):.0f}, {gmean(v('S03-G','PSLN-344')):.0f}, {gmean(v('S03-G','PSLN-212(Y)')):.0f}. PSLN-344 / PSLN-212 ratio {hc[0]:.1f} (95% CI {hc[1]:.1f}–{hc[2]:.1f}) and {ha[0]:.1f} ({ha[1]:.1f}–{ha[2]:.1f}). "
   "Values printed as 0 (below the 1:10 starting dilution) were set to 5.", R('S03-C', 'S03-G'), 'a07_point_stats.py -> T9/T10 (log scale)',
   m=f"{gmean(v('S03-C','PSLN-344')):.0f}", a=f"{gmean(v('S03-C','PSLN-212')):.0f}", y=f"{gmean(v('S03-C','PSLN-212(Y)')):.0f}", fold=f"{hc[0]:.0f}- to {ha[0]:.0f}-fold",
   m2=f"{gmean(v('S03-G','PSLN-344')):.0f}", a2=f"{gmean(v('S03-G','PSLN-212')):.0f}")
ev('hai40', f"An HAI titre of 40 did not mark protection in aged animals: all 5 aged PSLN-212 animals reached 40 or more against CA09 (values {', '.join(f'{x:.0f}' for x in v('S03-C','PSLN-212'))}), "
   "yet the PSLN-212 group was not protected against CA09 challenge (0 of 7 in S03-I as printed; 3 of 7 if the paired weight block is right). Every animal in the two protective regimens had HAI of 160 or more.",
   R('S03-C', 'S03-I', 'S13-F'), 'a07_point_stats.py -> T9; a08 -> T11')
c344, c212, cy_, csh = [v('S05-F', g) for g in ['PSLN-344', 'PSLN-212', 'PSLN-212(Y)', 'Sham']]
ev('cd8', f"CD8 T cells making IFN-gamma on re-stimulation with rgH5N1 (a subtype not in the bivalent vaccine), lymph node, day 14 (%, mean of 5): vehicle {csh.mean():.1f}, aged PSLN-212 {c212.mean():.1f}, aged PSLN-344 {c344.mean():.1f}, "
   f"young PSLN-212 {cy_.mean():.1f}; day 60: {v('S05-G','PSLN-212').mean():.1f}, {v('S05-G','PSLN-344').mean():.1f}, {v('S05-G','PSLN-212(Y)').mean():.1f} (S05-G). PSLN-344/PSLN-212 ratio {c344.mean()/c212.mean():.1f} at day 14 "
   f"(Tukey p = {pfmt(tukey_p('S05-F','PSLN-212','PSLN-344'))}).", R('S05-F', 'S05-G'), 'a07_point_stats.py -> T9/T10',
   m=f"{c344.mean():.1f}%", a=f"{c212.mean():.1f}%", y=f"{cy_.mean():.1f}%", fold=f"{c344.mean()/c212.mean():.1f}-fold")
n_short = int((RI.p_344_vs_young < 0.05).sum())
ev('ri', f"Restoration index (RI) of PSLN-344 in aged animals = (PSLN-344 aged - PSLN-212 aged) / (PSLN-212 young - PSLN-212 aged), computed for the {len(RI)} read-outs that have all three groups: median {RI.restoration_index.median():.2f} "
   f"(range {RI.restoration_index.min():.2f}–{RI.restoration_index.max():.2f}); by domain: interferon {RI[RI.domain.str.startswith('1')].restoration_index.median():.2f}, monocyte/DC {RI[RI.domain.str.startswith('2')].restoration_index.median():.2f}, "
   f"germinal centre/Tfh {RI[RI.domain.str.startswith('3')].restoration_index.median():.2f}, antibody {RI[RI.domain.str.startswith('4')].restoration_index.median():.2f}, CD8 T cell {RI[RI.domain.str.startswith('5')].restoration_index.median():.2f}. "
   f"{n_short} of {len(RI)} read-outs remain significantly different from young (Welch p < 0.05, unadjusted).", 'every block that has vehicle, PSLN-212, PSLN-344 and young PSLN-212 groups; listed per row in T11',
   'a08_restoration.py -> T11; log scale for titres and fold-changes; bootstrap CI (10,000 resamples)', median=f"{RI.restoration_index.median():.2f}", pct=f"{100*RI.restoration_index.median():.0f}%",
   short=f"{n_short} of {len(RI)}", n=f"{len(RI)}")
cd40, cd86 = ri('DC CD40+ d3'), ri('DC CD86+ d3')
ev('costim', f"Dendritic-cell co-stimulation, lymph node day 3 (% positive, mean of 5): CD40 aged PSLN-212 {cd40.aged_PSLN212:.1f}, aged PSLN-344 {cd40.aged_PSLN344:.1f}, young PSLN-212 {cd40.young_PSLN212:.1f} "
   f"(RI {cd40.restoration_index:.2f}, 95% CI {cd40.RI_lo:.2f}–{cd40.RI_hi:.2f}); CD86 {cd86.aged_PSLN212:.1f}, {cd86.aged_PSLN344:.1f}, {cd86.young_PSLN212:.1f} (RI {cd86.restoration_index:.2f}, {cd86.RI_lo:.2f}–{cd86.RI_hi:.2f}). "
   "The lowest restoration of any read-out.", R('S02-D CD40', 'S02-D CD86'), 'a08_restoration.py -> T11',
   cd40=f"{100*cd40.restoration_index:.0f}%", cd86=f"{100*cd86.restoration_index:.0f}%", m40=f"{cd40.aged_PSLN344:.0f}%", y40=f"{cd40.young_PSLN212:.0f}%", m86=f"{cd86.aged_PSLN344:.0f}%", y86=f"{cd86.young_PSLN212:.0f}%")
NAD = pd.read_csv(T + 'T12c_weight_nadir_contrasts.csv'); ny = NAD[NAD.contrast == 'PSLN-344 vs PSLN-212(Y)']; na = NAD[NAD.contrast == 'PSLN-344 vs PSLN-212']
ev('nadir', f"Morbidity after challenge (lowest body weight per animal, % of day 0, averaged over the {len(ny)} aged-animal challenge blocks with weight records): PSLN-344 aged {ny.nadir_a.mean():.1f}%, young PSLN-212 {ny.nadir_b.mean():.1f}%, "
   f"aged PSLN-212 {na.nadir_b.mean():.1f}%. PSLN-344 animals lost more weight than the young benchmark in {int((ny['diff'] < 0).sum())} of {len(ny)} blocks (paired t across blocks p = {pfmt(stats.ttest_rel(ny.nadir_a, ny.nadir_b).pvalue)}). "
   "Weight blocks contain re-used traces (record defect D7) and are supporting evidence only.", R('S13-F', 'S15-A', 'S15-B', 'S15-C', 'S15-D', 'S15-E', 'S15-F', 'S15-G', 'S15-M', 'S15-O'),
   'a09_weights.py -> T12/T12c', m=f"{ny.nadir_a.mean():.0f}%", y=f"{ny.nadir_b.mean():.0f}%", a=f"{na.nadir_b.mean():.0f}%", k=f"{int((ny['diff'] < 0).sum())} of {len(ny)}")

# ------------------------------------------------------------------ tolerability / safety
TOL = pd.read_csv(T + 'T13_tolerability_S08D.csv').set_index('group')
wv = df[(df.block == 'S08-D')]
ev('tol', f"Body weight after intranasal immunisation without challenge (S08-D, n = 5; lowest weight per animal as % of day 0, mean): vaccine alone {TOL.loc['Vaccine','mean_nadir']:.1f}, aged PSLN-212 {TOL.loc['PSLN-212','mean_nadir']:.1f}, "
   f"aged PSLN-344 {TOL.loc['PSLN-344','mean_nadir']:.1f} (worst animal {TOL.loc['PSLN-344','worst_animal']:.1f}; group mean back to {TOL.loc['PSLN-344','mean_d10']:.1f} on day 10), CMP-204 {TOL.loc['CMP-204','mean_nadir']:.1f}, "
   f"PSLN-212/R848 {TOL.loc['PSLN-212/R848','mean_nadir']:.1f} (worst {TOL.loc['PSLN-212/R848','worst_animal']:.1f}; 4 of 5 animals have a day-10 value, mean {TOL.loc['PSLN-212/R848','mean_d10']:.1f}). "
   "PSLN-344 vs vaccine alone: difference -1.8 points (95% CI -3.7 to 0.1; Welch p = 0.06).", R('S08-D'), 'a09_weights.py -> T13',
   m=f"{100-TOL.loc['PSLN-344','mean_nadir']:.1f}%", vac=f"{100-TOL.loc['Vaccine','mean_nadir']:.1f}%", r848=f"{100-TOL.loc['PSLN-212/R848','mean_nadir']:.0f}% of body weight on average (worst animal {100-TOL.loc['PSLN-212/R848','worst_animal']:.0f}%)",
   worst=f"{100-TOL.loc['PSLN-344','worst_animal']:.1f}%")
cn = {a: {g: v('S10-A', g, a) for g in ['PBS', 'Sham', 'PSLN-344', 'CT']} for a in ['Ifnb1', 'Tnf', 'Isg15']}
gs = {a: gmr(cn[a]['PSLN-344'], cn[a]['Sham']) for a in cn}
ev('cns', "Brain ('central nervous system') transcripts 36 h after intranasal dosing of aged animals (S10-A, n = 5; fold vs untreated, mean): "
   + '; '.join(f"{a} PBS {cn[a]['PBS'].mean():.1f}, vehicle {cn[a]['Sham'].mean():.1f}, PSLN-344 {cn[a]['PSLN-344'].mean():.1f}, cholera toxin {cn[a]['CT'].mean():.1f}" for a in cn)
   + f". PSLN-344 / vehicle ratios {gs['Ifnb1'][0]:.2f}, {gs['Tnf'][0]:.2f}, {gs['Isg15'][0]:.2f} (upper 95% limits {gs['Ifnb1'][2]:.1f}, {gs['Tnf'][2]:.1f}, {gs['Isg15'][2]:.1f}; all Welch p > 0.3). "
   "Against PBS the Tnf ratio is 1.57 (unadjusted p = 0.03; Tukey p = 0.12). One time point; no histology; no manganese measurement.", R('S10-A'), 'a07_point_stats.py -> T9/T10 (log scale)',
   ct=f"{cn['Isg15']['CT'].mean():.1f}- to {cn['Ifnb1']['CT'].mean():.1f}-fold", m=f"{min(cn[a]['PSLN-344'].mean() for a in cn):.1f}- to {max(cn[a]['PSLN-344'].mean() for a in cn):.1f}-fold",
   up=f"{max(gs[a][2] for a in gs):.1f}-fold")
S9 = pd.read_csv(T + 'T9_group_summaries.csv'); s9 = S9[S9.block.str.startswith('S09-A')].copy(); s9['an'] = s9.analyte.str.split().str[0]
f9 = lambda panel, g, a: float(10 ** s9[(s9.block == panel) & (s9.group == g) & (s9.an == a)]['mean'].iloc[0])
P1, P2 = 'S09-A (cols A-U)', 'S09-A (cols X-AS)'
ev('cyto', f"Lung inflammatory transcripts (S09-A; geometric-mean fold vs untreated, n = 3). 16 h: PSLN-344 aged Il6 {f9(P1,'PSLN-344','Il6'):.0f}, Tnf {f9(P1,'PSLN-344','Tnf'):.0f}, Ccl2 {f9(P1,'PSLN-344','Ccl2'):.0f}; young PSLN-212 {f9(P1,'PSLN-212(y)','Il6'):.0f}, {f9(P1,'PSLN-212(y)','Tnf'):.0f}, {f9(P1,'PSLN-212(y)','Ccl2'):.0f}. "
   f"Second panel (printed '16h'; its Ifnb1 row reproduces the 72 h values of S01-A, so I treat it as 72 h): PSLN-344 aged Il6 {f9(P2,'PSLN-344','Il6'):.1f}, Tnf {f9(P2,'PSLN-344','Tnf'):.1f}, Ccl2 {f9(P2,'PSLN-344','Ccl2'):.0f}, Il10 {f9(P2,'PSLN-344','Il10'):.1f}; "
   f"aged PSLN-212 {f9(P2,'PSLN-212','Il6'):.1f}, {f9(P2,'PSLN-212','Tnf'):.1f}, {f9(P2,'PSLN-212','Ccl2'):.1f}, {f9(P2,'PSLN-212','Il10'):.1f}; young PSLN-212 {f9(P2,'PSLN-212(y)','Il6'):.1f}, {f9(P2,'PSLN-212(y)','Tnf'):.1f}, {f9(P2,'PSLN-212(y)','Ccl2'):.0f}, {f9(P2,'PSLN-212(y)','Il10'):.1f}; "
   f"PSLN-212/R848 {f9(P2,'PSLN-212/R848','Il6'):.0f}, {f9(P2,'PSLN-212/R848','Tnf'):.0f}, {f9(P2,'PSLN-212/R848','Ccl2'):.0f}, {f9(P2,'PSLN-212/R848','Il10'):.0f}.",
   R(P1, P2, 'S01-A'), 'a07_point_stats.py -> T9/T10; a04_crosschecks.py (panel identity)',
   h72=f"Il6 {f9(P2,'PSLN-344','Il6'):.0f}-fold, Tnf {f9(P2,'PSLN-344','Tnf'):.0f}-fold and Ccl2 {f9(P2,'PSLN-344','Ccl2'):.0f}-fold above untreated", il6=f"{f9(P2,'PSLN-344','Il6'):.0f}", tnf=f"{f9(P2,'PSLN-344','Tnf'):.0f}", ccl2=f"{f9(P2,'PSLN-344','Ccl2'):.0f}",
   tnfy=f"{f9(P2,'PSLN-212(y)','Tnf'):.1f}", tnfa=f"{f9(P2,'PSLN-212','Tnf'):.1f}")
m8 = {g: v('S01-D', g, x=8).mean() for g in ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']}; d8 = {g: v('S01-E', g, x=8).mean() for g in ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']}
i72 = {g: v('S01-A', g, x='72h').mean() for g in ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']}
ev('resol', f"Resolution of the lung response in aged PSLN-344 animals is incomplete at the last time points sampled: lung monocytes on day 8 {m8['PSLN-344']:.1f}% (vehicle {m8['Sham']:.1f}%, young PSLN-212 {m8['PSLN-212(Y)']:.1f}%; Tukey p vs young = {pfmt(tukey_p('S01-D','PSLN-344','PSLN-212(Y)',x=8))}); "
   f"CD11b+ dendritic cells on day 8 {d8['PSLN-344']:.1f}% (vehicle {d8['Sham']:.1f}%, young {d8['PSLN-212(Y)']:.1f}%); Ifnb1 at 72 h {i72['PSLN-344']:.1f}-fold (young PSLN-212 {i72['PSLN-212(Y)']:.1f}-fold). No sample later than day 8 for these read-outs.",
   R('S01-D', 'S01-E', 'S01-A'), 'a07_point_stats.py -> T9/T10', mono=f"{m8['PSLN-344']:.1f}%", veh=f"{m8['Sham']:.1f}%")

# ------------------------------------------------------------------ dose, CMC
DR = pd.read_csv(T + 'T14_dose_response_fit.csv').set_index('group'); DM = pd.read_csv(T + 'T14b_dose_response_means.csv').pivot(index='dose_ug', columns='group', values='mean_fold')
ev('dose', f"Dose-response of lung Ifnb1 at 16 h (S08-A; 1, 5, 10, 20, 40 µg; n = 3 per dose; age of animals not stated): PSLN-344 means {', '.join(f'{x:.1f}' for x in DM['PSLN-344'])}; "
   f"PSLN-212 {', '.join(f'{x:.1f}' for x in DM['PSLN-212'])}; CMP-204 {', '.join(f'{x:.1f}' for x in DM['CMP-204'])}. Hill fit: maximum effect {DR.loc['PSLN-344','Emax_fold']:.0f}-fold (95% CI {DR.loc['PSLN-344','Emax_lo']:.0f}–{DR.loc['PSLN-344','Emax_hi']:.0f}) for PSLN-344 vs "
   f"{DR.loc['PSLN-212','Emax_fold']:.0f} ({DR.loc['PSLN-212','Emax_lo']:.0f}–{DR.loc['PSLN-212','Emax_hi']:.0f}) for PSLN-212; half-maximal dose {DR.loc['PSLN-344','ED50_ug']:.0f} µg ({DR.loc['PSLN-344','ED50_lo']:.0f}–{DR.loc['PSLN-344','ED50_hi']:.0f}) vs {DR.loc['PSLN-212','ED50_ug']:.0f} µg. "
   f"Doubling the dose from 20 to 40 µg adds {100*(DM.loc[40,'PSLN-344']/DM.loc[20,'PSLN-344']-1):.0f}%. No survival, antibody or tolerability data at any dose other than 20 µg.", R('S08-A'), 'a10_dose_response.py -> T14 (least squares on log scale; bootstrap CI)',
   emax=f"{DR.loc['PSLN-344','Emax_fold']:.0f}-fold", emax212=f"{DR.loc['PSLN-212','Emax_fold']:.0f}-fold", ed50=f"{DR.loc['PSLN-344','ED50_ug']:.0f} µg", ed50b=f"{DR.loc['PSLN-212','ED50_ug']:.0f} µg", step=f"{100*(DM.loc[40,'PSLN-344']/DM.loc[20,'PSLN-344']-1):.0f}%",
   r848=f"{DM.loc[20,'PSLN-344/R848']:.0f}-fold vs {DM.loc[20,'PSLN-344']:.0f}-fold")
ee = {g: v('S08-B', g) for g in ['CMP-204', 'PSLN-212', 'PSLN-R848', 'PSLN-212/R848', 'PSLN-344']}
ev('ee', "Encapsulation efficiency (S08-B, n = 3 preparations, mean ± SD): " + ', '.join(f"{g} {a.mean():.1f} ± {a.std(ddof=1):.1f}%" for g, a in ee.items()) + ". The only formulation-quality data in the package: particle size, charge, manganese content, stability and endotoxin are described as measured but are not in the workbook.",
   R('S08-B'), 'a07_point_stats.py -> T9', m=f"{ee['PSLN-344'].mean():.0f}%")

# ------------------------------------------------------------------ mechanism links
mu = lambda b, g, a=None, x=None: v(b, g, a, x).mean()
wp = lambda a, b: stats.ttest_ind(a, b, equal_var=False).pvalue
ev('uptake', f"Vehicle function. Alveolar macrophages taking up dye-labelled liposome at 16 h: wild-type {mu('S01-C','WT'):.1f}% vs surfactant-protein A/D knock-out {mu('S01-C','SPA/D'):.1f}% (n = 4; Welch p = {pfmt(wp(v('S01-C','WT'), v('S01-C','SPA/D')))}). "
   f"Dye-positive alveolar epithelial cells after liposomal vs free dye: type II {mu('S01-B','AECII/PSLN-SRB'):.1f}% vs {mu('S01-B','AECII/FreeSRB'):.2f}%; type I {mu('S01-B','AECI/PSLN-SRB'):.1f}% vs {mu('S01-B','AECI/FreeSRB'):.2f}% (n = 5; Tukey p < 0.01 for both).",
   R('S01-C', 'S01-B'), 'a07_point_stats.py -> T9/T10', wt=f"{mu('S01-C','WT'):.0f}%", ko=f"{mu('S01-C','SPA/D'):.0f}%", aec2=f"{mu('S01-B','AECII/PSLN-SRB'):.1f}%", free=f"{mu('S01-B','AECII/FreeSRB'):.1f}%")
ev('gapj', f"Gap-junction blocker carbenoxolone before vaccine + PSLN-344: recruited lung monocytes on day 3 {mu('S11-C','CBX+'):.1f}% vs {mu('S11-C','CBX-'):.1f}% without blocker "
   f"(-{100*(1-mu('S11-C','CBX+')/mu('S11-C','CBX-')):.0f}%; n = 5; Welch p = {pfmt(wp(v('S11-C','CBX+'), v('S11-C','CBX-')))}).", R('S11-C'), 'a07_point_stats.py -> T10', cut=f"{100*(1-mu('S11-C','CBX+')/mu('S11-C','CBX-')):.0f}%")
ev('gmcsf', f"Lung Gm-csf transcript (fold vs untreated, mean of 5) at 16 / 36 / 72 h: PSLN-344 {mu('S02-F','PSLN-344',x='16h'):.1f} / {mu('S02-F','PSLN-344',x='36h'):.1f} / {mu('S02-F','PSLN-344',x='72h'):.1f}; "
   f"PSLN-212 {mu('S02-F','PSLN-212',x='16h'):.1f} / {mu('S02-F','PSLN-212',x='36h'):.1f} / {mu('S02-F','PSLN-212',x='72h'):.1f}; vehicle {mu('S02-F','Sham',x='16h'):.1f} / {mu('S02-F','Sham',x='36h'):.1f} / {mu('S02-F','Sham',x='72h'):.1f} (aged animals; Tukey p < 0.001 at each time).",
   R('S02-F'), 'a07_point_stats.py -> T9/T10 (log scale)', m16=f"{mu('S02-F','PSLN-344',x='16h'):.1f}", m36=f"{mu('S02-F','PSLN-344',x='36h'):.1f}", a16=f"{mu('S02-F','PSLN-212',x='16h'):.1f}")
ev('mono', f"Lung monocytes (% of lung cells, mean of 5) on day 4: vehicle {mu('S01-D','Sham',x=4):.1f}, aged PSLN-212 {mu('S01-D','PSLN-212',x=4):.1f}, aged PSLN-344 {mu('S01-D','PSLN-344',x=4):.1f}, young PSLN-212 {mu('S01-D','PSLN-212(Y)',x=4):.1f} "
   f"(Tukey p, PSLN-344 vs PSLN-212 = {pfmt(tukey_p('S01-D','PSLN-212','PSLN-344',x=4))}). CCR2 antagonist INCB3344 before vaccine + PSLN-344: monocytes {mu('S07-B','PSLN-344','monocytes'):.1f}% -> {mu('S07-B','PSLN-344+INCB3344','monocytes'):.1f}%, "
   f"Ly6C+ macrophages {mu('S07-B','PSLN-344','macrophages'):.1f}% -> {mu('S07-B','PSLN-344+INCB3344','macrophages'):.1f}% (n = 5; Welch p <= 0.003; time point not stated).", R('S01-D', 'S07-B'), 'a07_point_stats.py -> T9/T10',
   m=f"{mu('S01-D','PSLN-344',x=4):.0f}%", a=f"{mu('S01-D','PSLN-212',x=4):.0f}%")
a_, b_ = v('S12-A', 'WT to WT'), v('S12-A', 'IFNAR-/- to WT')
ev('modc', f"Monocyte-to-dendritic-cell conversion after vaccine + PSLN-344 (donor-derived monocyte-derived DC, %, mean of 5): wild-type marrow {mu('S02-H','WT w/o cDC'):.1f}, interferon-receptor-deficient marrow {mu('S02-H','IFN w/o cDC'):.1f} "
   f"(-{100*(1-mu('S02-H','IFN w/o cDC')/mu('S02-H','WT w/o cDC')):.0f}%; Tukey p < 0.0001), receptor-deficient marrow + GM-CSF {mu('S02-H','GMCSF'):.1f} (S02-H). In aged PSLN-212 animals GM-CSF raised monocyte-derived DC-like cells from {mu('S02-G','PSLN-212'):.1f}% to {mu('S02-G','PSLN-212+GM-CSF'):.1f}% "
   f"(Tukey p = 0.0001; S02-G). Monocyte entry itself was not clearly interferon-receptor dependent: {a_.mean():.1f}% vs {b_.mean():.1f}% (n = 3; Welch p = {pfmt(wp(a_, b_))}; S12-A).",
   R('S02-H', 'S02-G', 'S12-A'), 'a07_point_stats.py -> T9/T10', wt=f"{mu('S02-H','WT w/o cDC'):.1f}%", ko=f"{mu('S02-H','IFN w/o cDC'):.1f}%", gm=f"{mu('S02-H','GMCSF'):.1f}%")
ev('dcmig', f"Dendritic cells, aged PSLN-344 vs aged PSLN-212 (young PSLN-212 in brackets), mean of 5: lung CD11b+ DC day 4 {mu('S01-E','PSLN-344',x=4):.1f}% vs {mu('S01-E','PSLN-212',x=4):.1f}% ({mu('S01-E','PSLN-212(Y)',x=4):.1f}%); "
   f"lung cDC1 at 72 h {mu('S01-F','PSLN-344'):.1f}% vs {mu('S01-F','PSLN-212'):.1f}% ({mu('S01-F','PSLN-212(Y)'):.1f}%); CCR7+ migratory DC {mu('S02-A','PSLN-344'):.1f}% vs {mu('S02-A','PSLN-212'):.1f}% ({mu('S02-A','PSLN-212(Y)'):.1f}%); "
   f"lymph-node CD11b+ DC {mu('S02-B','PSLN-344'):.1f}% vs {mu('S02-B','PSLN-212'):.1f}% ({mu('S02-B','PSLN-212(Y)'):.1f}%); antigen-carrying DC in lymph node at 36 h {mu('S02-C','PSLN-344'):.1f}% vs {mu('S02-C','PSLN-212'):.1f}% ({mu('S02-C','PSLN-212(Y)'):.1f}%), "
   f"{mu('S02-C','PTX'):.1f}% with pertussis toxin (the adjuvant given to the PTX group is not stated). All PSLN-344 vs PSLN-212 Tukey p < 0.01.",
   R('S01-E', 'S01-F', 'S02-A', 'S02-B', 'S02-C'), 'a07_point_stats.py -> T9/T10', ccr7=f"{mu('S02-A','PSLN-344'):.0f}%", ccr7a=f"{mu('S02-A','PSLN-212'):.0f}%", ag=f"{mu('S02-C','PSLN-344'):.1f}%", aga=f"{mu('S02-C','PSLN-212'):.1f}%")
ev('xprime', f"Cross-priming capacity of lymph-node DC (proliferation of naive OT-I CD8 T cells in co-culture, %, mean of 5): aged PSLN-212 {mu('S02-E','PSLN-212'):.1f}, aged PSLN-344 {mu('S02-E','PSLN-344'):.1f}, young PSLN-212 {mu('S02-E','PSLN-212(Y)'):.1f}, "
   f"young PSLN-344 {mu('S02-E','PSLN-344(Y)'):.1f}; pertussis-toxin group {mu('S02-E','PTX'):.1f}.", R('S02-E'), 'a07_point_stats.py -> T9/T10', m=f"{mu('S02-E','PSLN-344'):.1f}%", a=f"{mu('S02-E','PSLN-212'):.1f}%", y=f"{mu('S02-E','PSLN-212(Y)'):.1f}%")
tfh = lambda g: (v('S04-A', g, 'ICOS-high') + v('S04-A', g, 'ICOS-low')).mean()
ev('gc', f"Germinal-centre response in the draining lymph node, aged PSLN-344 vs aged PSLN-212 (young PSLN-212): GC B cells day 7 {mu('S03-K','PSLN-344'):.1f}% vs {mu('S03-K','PSLN-212'):.1f}% ({mu('S03-K','PSLN-212(Y)'):.1f}%); "
   f"ICOS-high follicular helper T cells {mu('S04-A','PSLN-344','ICOS-high'):.1f}% vs {mu('S04-A','PSLN-212','ICOS-high'):.1f}% ({mu('S04-A','PSLN-212(Y)','ICOS-high'):.1f}%); follicular regulatory T cells {mu('S04-B Foxp3+','PSLN-344'):.1f}% vs {mu('S04-B Foxp3+','PSLN-212'):.1f}% ({mu('S04-B Foxp3+','PSLN-212(Y)'):.1f}%); "
   f"helper:regulatory ratio {mu('S04-B Tfh:Tfr','PSLN-344'):.1f} vs {mu('S04-B Tfh:Tfr','PSLN-212'):.1f} ({mu('S04-B Tfh:Tfr','PSLN-212(Y)'):.1f}); Aicda transcript {mu('S03-L','PSLN-344','Aicda'):.1f}- vs {mu('S03-L','PSLN-212','Aicda'):.1f}-fold (n = 3); "
   f"IgG+ B cells {mu('S13-H','PSLN-344'):.1f}% vs {mu('S13-H','PSLN-212'):.1f}% ({mu('S13-H','PSLN-212(Y)'):.1f}%). By day 30 follicular regulatory cells no longer differ: {mu('S04-C','PSLN-344'):.1f}% vs {mu('S04-C','PSLN-212'):.1f}% (vehicle {mu('S04-C','Sham'):.1f}%; young {mu('S04-C','PSLN-212(Y)'):.1f}%; Tukey p = 0.14 vs PSLN-212).",
   R('S03-K', 'S03-L', 'S04-A', 'S04-B Foxp3+', 'S04-B Tfh:Tfr', 'S04-C', 'S13-H'), 'a07_point_stats.py -> T9/T10', gcb=f"{mu('S03-K','PSLN-344'):.1f}%", gcba=f"{mu('S03-K','PSLN-212'):.1f}%",
   ratio=f"{mu('S04-B Tfh:Tfr','PSLN-344'):.1f}", ratioa=f"{mu('S04-B Tfh:Tfr','PSLN-212'):.1f}",
   tfr30m=f"{mu('S04-C','PSLN-344'):.1f}%", tfr30a=f"{mu('S04-C','PSLN-212'):.1f}%", tfr30y=f"{mu('S04-C','PSLN-212(Y)'):.1f}%", tfr30s=f"{mu('S04-C','Sham'):.1f}%", tfr7m=f"{mu('S04-B Foxp3+','PSLN-344'):.1f}%", tfr7a=f"{mu('S04-B Foxp3+','PSLN-212'):.1f}%")
rat = {g: (v('S13-A', g) / v('S13-B', g)) for g in ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']}; rat2 = {g: (v('S13-C', g) / v('S13-D', g)) for g in ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']}
ev('igratio', f"IgG2a/IgG1 ratio (a marker of a type-1-skewed antibody response) recomputed from the subclass titres in S13-A..D (mean of 5): anti-CA09 aged PSLN-212 {rat['PSLN-212'].mean():.2f}, aged PSLN-344 {rat['PSLN-344'].mean():.2f}, young PSLN-212 {rat['PSLN-212(Y)'].mean():.2f}; "
   f"anti-Aichi {rat2['PSLN-212'].mean():.2f}, {rat2['PSLN-344'].mean():.2f}, {rat2['PSLN-212(Y)'].mean():.2f}. The ratio blocks S03-B and S03-F contain exactly these 15 + 15 values but under headers rotated by one position "
   f"(as printed they would read PSLN-212 {mu('S03-B','PSLN-212'):.2f}, PSLN-344 {mu('S03-B','PSLN-344'):.2f}, young {mu('S03-B','PSLN-212(Y)'):.2f}).",
   R('S13-A', 'S13-B', 'S13-C', 'S13-D', 'S03-B', 'S03-F'), 'a04_crosschecks.py -> T4 (exact recomputation, all 30 values matched to <0.2%)', m=f"{rat['PSLN-344'].mean():.1f}", a=f"{rat['PSLN-212'].mean():.1f}", y=f"{rat['PSLN-212(Y)'].mean():.1f}",
   printed=f"{mu('S03-B','PSLN-344'):.2f}")
ev('ab', f"Antibody on day 14 after one dose, geometric mean titre (n = 5), vehicle / aged PSLN-212 / aged PSLN-344 / young PSLN-212: IgG anti-CA09 {gmean(v('S03-A','Sham')):.0f} / {gmean(v('S03-A','PSLN-212')):.0f} / {gmean(v('S03-A','PSLN-344')):.0f} / {gmean(v('S03-A','PSLN-212(Y)')):.0f}; "
   f"neutralising anti-CA09 {gmean(v('S03-D','Sham')):.0f} / {gmean(v('S03-D','PSLN-212')):.0f} / {gmean(v('S03-D','PSLN-344')):.0f} / {gmean(v('S03-D','PSLN-212(Y)')):.0f}; IgG anti-Aichi {gmean(v('S03-E','Sham')):.0f} / {gmean(v('S03-E','PSLN-212')):.0f} / {gmean(v('S03-E','PSLN-344')):.0f} / {gmean(v('S03-E','PSLN-212(Y)')):.0f}. "
   f"After a booster (day 28): IgG anti-CA09 {gmean(v('S13-I','PSLN-212')):.0f} / {gmean(v('S13-I','PSLN-344')):.0f} / {gmean(v('S13-I','PSLN-212(Y)')):.0f}; anti-Aichi {gmean(v('S13-J','PSLN-212')):.0f} / {gmean(v('S13-J','PSLN-344')):.0f} / {gmean(v('S13-J','PSLN-212(Y)')):.0f} "
   f"(aged PSLN-344 = {100*gmean(v('S13-I','PSLN-344'))/gmean(v('S13-I','PSLN-212(Y)')):.0f}% and {100*gmean(v('S13-J','PSLN-344'))/gmean(v('S13-J','PSLN-212(Y)')):.0f}% of young).",
   R('S03-A', 'S03-D', 'S03-E', 'S13-I', 'S13-J'), 'a07_point_stats.py -> T9/T10 (log scale)', igg=f"{gmean(v('S03-A','PSLN-344')):.0f}", igga=f"{gmean(v('S03-A','PSLN-212')):.0f}", iggy=f"{gmean(v('S03-A','PSLN-212(Y)')):.0f}",
   boost=f"{100*gmean(v('S13-J','PSLN-344'))/gmean(v('S13-J','PSLN-212(Y)')):.0f}–{100*gmean(v('S13-I','PSLN-344'))/gmean(v('S13-I','PSLN-212(Y)')):.0f}%")
ev('lungcd8', f"Lung CD8 T cells. Transferred OT-I cells proliferated in the lung whether or not lymph-node trafficking was blocked with pertussis toxin ({mu('S05-C','Lung'):.0f}% vs {mu('S05-C','Lung+PTX'):.0f}%), while proliferation in the lymph node fell from {mu('S05-C','MLN'):.0f}% to {mu('S05-C','MLN+PTX'):.0f}% (n = 3; S05-C). "
   f"Day 3 after vaccination, aged PSLN-344 vs aged PSLN-212 (young): Ki-67+ CD8 {mu('S05-D','PSLN-344'):.1f}% vs {mu('S05-D','PSLN-212'):.1f}% ({mu('S05-D','PSLN-212(Y)'):.1f}%); granzyme-B+ CD8 {mu('S05-E','PSLN-344'):.1f}% vs {mu('S05-E','PSLN-212'):.1f}% ({mu('S05-E','PSLN-212(Y)'):.1f}%). "
   f"Blocking CCR2 in young PSLN-344 animals cut granzyme-B+ CD8 from {mu('S02-I','PSLN-344(Y)'):.1f}% to {mu('S02-I','PSLN-344(Y)+INCB3344'):.1f}% (n = 5; Welch p = 0.0001; S02-I).",
   R('S05-C', 'S05-D', 'S05-E', 'S02-I'), 'a07_point_stats.py -> T9/T10')
ev('trm', f"Lung-resident memory CD8 T cells on day 25 (%, mean of 5): vehicle {mu('S05-I','Sham'):.1f}, aged PSLN-212 {mu('S05-I','PSLN-212'):.1f}, aged PSLN-344 {mu('S05-I','PSLN-344'):.1f}, young PSLN-212 {mu('S05-I','PSLN-212(Y)'):.1f} "
   f"(Tukey p, PSLN-344 vs PSLN-212 < 0.0001; vs young = {pfmt(tukey_p('S05-I','PSLN-344','PSLN-212(Y)'))}).", R('S05-I'), 'a07_point_stats.py -> T9/T10', m=f"{mu('S05-I','PSLN-344'):.1f}%", a=f"{mu('S05-I','PSLN-212'):.1f}%", y=f"{mu('S05-I','PSLN-212(Y)'):.1f}%")
s07c_b = mu('S07-C', 'col B (printed "Ly6C-CD206+ MPhi")'); s07c_c = mu('S07-C', 'col C (printed "Ly6C-CD206+ MPhi")')
ev('brake', f"Suppressive lung environment of aged animals: CD206+ macrophages vehicle {mu('S11-E','Sham'):.0f}%, aged PSLN-212 {mu('S11-E','PSLN-212'):.0f}%, aged PSLN-344 {mu('S11-E','PSLN-344'):.0f}%, young PSLN-212 {mu('S11-E','PSLN-212(Y)'):.0f}% (n = 5; time point not stated; S11-E); "
   f"lung regulatory T cells day 7 {mu('S04-D','Sham'):.1f}%, {mu('S04-D','PSLN-212'):.1f}%, {mu('S04-D','PSLN-344'):.1f}%, {mu('S04-D','PSLN-212(Y)'):.1f}% (n = 3; S04-D). Ly6C+CCR2+ macrophages accumulated after PSLN-212 but not PSLN-344 "
   f"({mu('S07-A','PSLN-212',x=5):.1f} vs {mu('S07-A','PSLN-344',x=5):.1f} ×10⁵ cells on day 5; n = 3; S07-A). A macrophage-transfer experiment changed lung regulatory T cells ({s07c_b:.1f}% vs {s07c_c:.1f}%) "
   "but both columns carry the same label, so the direction cannot be assigned (S07-C).", R('S11-E', 'S04-D', 'S07-A', 'S07-C'), 'a07_point_stats.py -> T9/T10', cd206=f"{mu('S11-E','PSLN-344'):.0f}%", cd206a=f"{mu('S11-E','PSLN-212'):.0f}%",
   treg=f"{mu('S04-D','PSLN-344'):.1f}%", trega=f"{mu('S04-D','PSLN-212'):.1f}%")
a1, a2 = v('S08-C', 'AECII-PSLN-SRB'), v('S08-C', 'AECII-PSLN-344-SRB'); a3, a4 = v('S08-C', 'AECI-PSLN-SRB'), v('S08-C', 'AECI-PSLN-344-SRB')
ev('aecmn', f"Does adding Mn²⁺ change delivery to the epithelium? S08-C as printed: type II cells {a1.mean():.1f}% (liposome) vs {a2.mean():.1f}% (Mn liposome); type I {a3.mean():.1f}% vs {a4.mean():.1f}% - a four- to five-fold loss. "
   f"But S01-B gives {mu('S01-B','AECI/PSLN-SRB'):.1f}% for type I cells with the same liposome, which equals S08-C column B ({a2.mean():.1f}%), not column C ({a3.mean():.1f}%). If columns B and C are transposed, the Mn liposome delivers {a3.mean():.1f}% (type II) and {a4.mean():.1f}% (type I), "
   f"i.e. no material loss. Unresolved.", R('S08-C', 'S01-B'), 'a04_crosschecks.py (section E); a07 -> T9')
ev('r848', f"Adding the TLR7/8 agonist R848 was not an improvement: PSLN-212/R848 caused {100-TOL.loc['PSLN-212/R848','mean_nadir']:.0f}% mean weight loss with one animal missing at day 10 (S08-D), Tnf {f9(P1,'PSLN-212/R848','Tnf'):.0f}-fold and Il10 {f9(P1,'PSLN-212/R848','Il10'):.0f}-fold at 16 h and still {f9(P2,'PSLN-212/R848','Tnf'):.0f}- and {f9(P2,'PSLN-212/R848','Il10'):.0f}-fold in the later panel (S09-A); "
   f"PSLN-344/R848 gave less Ifnb1 than PSLN-344 alone ({DM.loc[20,'PSLN-344/R848']:.0f}- vs {DM.loc[20,'PSLN-344']:.0f}-fold at 20 µg; S08-A; this material is not in the annotation's materials list). No efficacy data exist for either R848 combination.",
   R('S08-D', P1, P2, 'S08-A'), 'a09_weights.py -> T13; a07 -> T9; a10 -> T14b')
yy = gmr(v('S01-A', 'PSLN-344(Y)', x='16h'), v('S01-A', 'PSLN-212(Y)', x='16h'))
W12 = pd.read_csv(T + 'T12_weight_nadir_by_group.csv')
ny_ = lambda b, g: W12[(W12.block == b) & (W12.group == g)].mean_nadir.iloc[0]
ev('youngpd', f"In young animals Mn²⁺ adds little: Ifnb1 at 16 h {mu('S01-A','PSLN-344(Y)',x='16h'):.1f}- vs {mu('S01-A','PSLN-212(Y)',x='16h'):.1f}-fold (ratio {yy[0]:.2f}; Tukey p = {pfmt(tukey_p('S01-A','PSLN-212(Y)','PSLN-344(Y)',x='16h',log=True))}); "
   f"antigen-carrying DC {mu('S02-C','PSLN-344(Y)'):.1f}% vs {mu('S02-C','PSLN-212(Y)'):.1f}%; cross-priming {mu('S02-E','PSLN-344(Y)'):.1f}% vs {mu('S02-E','PSLN-212(Y)'):.1f}% (both not significant); survival 24 of 24 vs 24 of 24; "
   f"lowest body weight after challenge {ny_('S09-C','PSLN-344Y'):.1f}% vs {ny_('S09-C','PSLN-212Y'):.1f}%, {ny_('S09-E','PSLN-344Y'):.1f}% vs {ny_('S09-E','PSLN-212Y'):.1f}%, {ny_('S09-G','PSLN-344Y'):.1f}% vs {ny_('S09-G','PSLN-212Y'):.1f}% (S09-C, E, G).",
   R('S01-A', 'S02-C', 'S02-E', 'S09-B', 'S09-D', 'S09-F', 'S09-C', 'S09-E', 'S09-G'), 'a07 -> T10; a05 -> T5; a09 -> T12')

# ------------------------------------------------------------------ biomarker thresholds (regimen-level separation)
def sep(k): r_ = RI.loc[k]; return r_.weakest_protective_value, r_.strongest_nonprotective_value, r_.AUC_protective_vs_not, bool(r_.complete_separation)
bm_rows = [('Ifnb1 lung 16 h', 'fold', 0), ('Lung monocytes, peak d4', '%', 1), ('Lung CCR7+ migratory DC 72 h', '%', 1), ('GC B cells d7', '%', 1), ('Tfh:Tfr ratio d7', '', 1),
           ('HAI anti-CA09 d14', '', 0), ('HAI anti-Aichi d14', '', 0), ('IgG anti-CA09 d14', '', 0), ('IgG2a anti-CA09 d14', '', 0), ('IFNg+ CD8, rgH5N1 restim d14', '%', 1), ('IFNg+ CD8, rgH5N1 restim d60', '%', 1), ('Lung TRM CD8 d25', '%', 1)]
txt = []
for k, u, d_ in bm_rows:
    w_, s_, auc, cs = sep(k); uu = '-fold' if u == 'fold' else u; txt.append(f"{k}: lowest value in a protective regimen {w_:.{d_}f}{uu}, highest in a non-protective regimen {s_:.{d_}f}{uu}")
ev('bm', "Separation of protective regimens (aged PSLN-344, young PSLN-212) from non-protective regimens (vehicle, aged PSLN-212) at the level of individual animals - " + '; '.join(txt) +
   f". {int(RI.complete_separation.sum())} of {len(RI)} read-outs separate completely (no overlap). Biomarkers and survival were measured in different animals, so these are regimen-level thresholds, not individual correlates of protection.",
   'blocks listed per row in T11', 'a08_restoration.py -> T11 (columns for the weakest protective value, the strongest non-protective value and the AUC)',
   ifn=f"≥ {sep('Ifnb1 lung 16 h')[0]:.0f}-fold against ≤ {sep('Ifnb1 lung 16 h')[1]:.0f}-fold", hai=f"≥ {sep('HAI anti-CA09 d14')[0]:.0f} against ≤ {sep('HAI anti-CA09 d14')[1]:.0f}",
   cd8=f"≥ {sep('IFNg+ CD8, rgH5N1 restim d14')[0]:.1f}% against ≤ {sep('IFNg+ CD8, rgH5N1 restim d14')[1]:.1f}%", mono=f"≥ {sep('Lung monocytes, peak d4')[0]:.0f}% against ≤ {sep('Lung monocytes, peak d4')[1]:.0f}%",
   gcb=f"≥ {sep('GC B cells d7')[0]:.1f}% against ≤ {sep('GC B cells d7')[1]:.1f}%", trm=f"≥ {sep('Lung TRM CD8 d25')[0]:.1f}% against ≤ {sep('Lung TRM CD8 d25')[1]:.1f}%",
   igg=f"≥ {sep('IgG anti-CA09 d14')[0]:.0f} against ≤ {sep('IgG anti-CA09 d14')[1]:.0f}", ccr7=f"≥ {sep('Lung CCR7+ migratory DC 72 h')[0]:.0f}% against ≤ {sep('Lung CCR7+ migratory DC 72 h')[1]:.0f}%",
   tfh=f"≥ {sep('Tfh:Tfr ratio d7')[0]:.1f} against ≤ {sep('Tfh:Tfr ratio d7')[1]:.1f}", nsep=f"{int(RI.complete_separation.sum())} of {len(RI)}")
gm16 = v('S02-F', 'PSLN-344', x='16h'); gm16a = v('S02-F', 'PSLN-212', x='16h')
ev('bmgm', f"Gm-csf at 16 h separates aged PSLN-344 (lowest animal {gm16.min():.1f}-fold) from aged PSLN-212 (highest animal {gm16a.max():.1f}-fold); no young group in this block.", R('S02-F'), 'evidence.py (min/max of cells)',
   t=f"≥ {gm16.min():.1f}-fold against ≤ {gm16a.max():.1f}-fold")

# ------------------------------------------------------------------ power
PW = pd.read_csv(T + 'T16_power_sample_size.csv')
pw = lambda scen, tgt: int(PW[(PW.scenario.str.startswith(scen)) & (PW.target_power == tgt)].n_per_group.iloc[0])
hist = PW[PW.scenario.str.startswith('historical')]
ev('power', f"Sample size (two-sided Fisher exact test, alpha 0.05): to detect 75% vs 25% survival needs {pw('Conservative', 0.8)} per group for 80% power and {pw('Conservative', 0.9)} for 90%; the observed 84% vs 12% needs {pw('Observed', 0.9)} for 90%; "
   f"80% vs 40% (an attribution arm) needs {pw('Attribution arm (e.g.', 0.8)}; a day-14 vs day-60 difference of 93% vs 67% needs {pw('Durability', 0.8)}. With 24 per group the power for 75% vs 25% is {100*fisher_power(0.75, 0.25, 24):.0f}% and for 80% vs 40% is {100*fisher_power(0.8, 0.4, 24):.0f}%. "
   f"The historical design (7 per group) had {100*hist.achieved_power.iloc[0]:.0f}% power for the observed effect and {100*hist.achieved_power.iloc[3]:.0f}% for the durability difference.",
   'planning values taken from T7 (pooled survival) and T8 (durability)', 'a12_power.py -> T16 (exact enumeration of binomial outcomes)',
   n90=f"{pw('Conservative', 0.9)}", p24=f"{100*fisher_power(0.75, 0.25, 24):.0f}%", attr=f"{pw('Attribution arm (e.g.', 0.8)}", p24attr=f"{100*fisher_power(0.8, 0.4, 24):.0f}%", dur=f"{pw('Durability', 0.8)}",
   hist=f"{100*hist.achieved_power.iloc[0]:.0f}%", histdur=f"{100*hist.achieved_power.iloc[3]:.0f}%")
lo20, hi20 = clopper_pearson(4, 20)
ev('bgn', f"Precision of a background-mortality estimate: if 19% of unchallenged aged controls die, a group of 7 gives a 95% CI of 0–58% (1/7) and a group of 20 gives {100*lo20:.0f}–{100*hi20:.0f}% (4/20).", 'T8 (observed 4/21)', 'a12_power.py; exact CI',
   ci20=f"{100*lo20:.0f}–{100*hi20:.0f}%")
ev('design', "Design facts taken from the annotation file (page 1 and block entries): BALB/c animals were female and the sex of the C57BL/6 and Swiss Webster animals is not stated; aged = 20 months or older (BALB/c), 20 months (C57BL/6, Swiss Webster); young = 7–8 weeks; vaccines were whole virus inactivated with 0.02% formalin; every challenge study used a single intranasal dose of 20 µg adjuvant; "
   "groups were 5 animals (most immune read-outs), 3 (some) or 7–10 (challenge studies). The file contains no statement of randomisation or blinding, no virus-titre data, no histopathology, no pharmacokinetics, no manganese measurement and no species other than mouse.",
   'annotation PDF, pages 1–2 (Animals; Viruses and vaccines; Routes and doses; Stated statistical methods) and per-block entries; workbook sheet inventory', 'a01_counts.py -> T1 (observation counts for all 102 blocks)')
ev('counts', "Challenge studies in the file: 12 in aged animals (S03-I, S03-J, S06-A, -B, -C, -D, -E, -F, -G, S15-H, S15-L, S15-N), 2 in 14-month-old animals (S06-E and S06-F, rows 71-105), 4 in young animals (S09-B, S09-D, S09-F, S13-E).",
   'all time-to-event blocks (Appendix D)', 'a05_survival.py -> T5')
