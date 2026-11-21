"""facts.py
Single registry of every number quoted in the proposal.  Each fact is computed here from the parsed workbook
(or read from the result files written by scripts 03-09) and carries its source blocks, cell ranges and method.
The proposal text is rendered from this registry, so text, figures and tables cannot drift apart.
"""
import json, math
import numpy as np
from scipy import stats

B = json.load(open('/tmp/work/parsed/parsed_blocks.json'))
SURV = json.load(open('/tmp/work/parsed/survival_results.json'))
IMM = json.load(open('/tmp/work/parsed/immuno_moa_results.json'))
SAF = json.load(open('/tmp/work/parsed/safety_results.json'))
BIO = json.load(open('/tmp/work/parsed/biomarker_power.json'))
G = lambda b: B[b]['groups']
FACTS = {}

def add(key, text, what, blocks, method, script, cells=None):
    assert key not in FACTS, key
    if cells is None:
        def res(b):
            return [k for k in B if k == b or k.startswith(b + '_')]
        ids = [k for b in blocks for k in res(b)]
        cells = '; '.join(sorted({c for k in ids for c in (B[k].get('cells', {}) or {}).values()})) if (0 < len(ids) <= 2) else ('all group ranges of the listed blocks' if ids else 'n/a')
    FACTS[key] = dict(text=text, what=what, blocks=blocks, cells=cells, method=method, script=script)

def gm(v): return float(np.exp(np.mean(np.log(np.asarray(v, float)))))
def cp(k, n):
    lo = 0.0 if k == 0 else stats.beta.ppf(.025, k, n - k + 1); hi = 1.0 if k == n else stats.beta.ppf(.975, k + 1, n - k); return 100 * lo, 100 * hi
def sn(bid, g):
    a = G(bid)[g]; return sum(1 for x in a if x['event'] == 0), len(a)
def welch(a, b, log=False):
    a = np.asarray(a, float); b = np.asarray(b, float)
    if log: a, b = np.log(a), np.log(b)
    t, p = stats.ttest_ind(a, b, equal_var=False)
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b); df = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))
    d = a.mean() - b.mean(); se = math.sqrt(va + vb); tc = stats.t.ppf(0.975, df); est, lo, hi = d, d - tc * se, d + tc * se
    if log: est, lo, hi = math.exp(est), math.exp(lo), math.exp(hi)
    return est, lo, hi, p
def pfmt(p):
    if p < 0.0001: return 'p < 0.0001'
    if p < 0.001: return f'p = {p:.4f}'
    if p < 0.01: return f'p = {p:.3f}'
    return f'p = {p:.2f}'
def hai(v): return [5 if x == 0 else x for x in v]

AGED11 = ['S03-I', 'S03-J', 'S06-A', 'S06-B', 'S06-C', 'S06-D', 'S06-E_r34', 'S06-F_r34', 'S06-G', 'S15-L', 'S15-N']
def nice(b): return b.replace('_r34', ' (rows 34-68)').replace('_r71', ' (rows 71-98)')
M_FISH = 'animals with event code 0 / animals with a row'
M_CP = 'survivors summed over animals summed across the listed blocks; exact 95% CI'

# ------------------------------------------------------------------------------------------------ survival
def pool(ids, g):
    s = sum(sn(b, g)[0] for b in ids if g in G(b)); n = sum(sn(b, g)[1] for b in ids if g in G(b)); return s, n
for g, key in [('PSLN-344', '344'), ('PSLN-212', '212'), ('Sham', 'sham'), ('PSLN-212(Y)', 'young')]:
    s, n = pool(AGED11, g); lo, hi = cp(s, n)
    ids = [b for b in AGED11 if g in G(b)]
    add(f'pool_{key}', f'{s} of {n} ({100*s/n:.0f}%)', f'{g}: animals alive at end of observation, pooled over {len(ids)} aged-design challenge experiments', ids, M_CP, '06_survival.py')
    add(f'pool_{key}_frac', f'{s}/{n}', f'{g}: pooled survivors/animals', ids, M_CP, '06_survival.py')
    add(f'pool_{key}_pct', f'{100*s/n:.0f}%', f'{g}: pooled survival %', ids, M_CP, '06_survival.py')
    add(f'pool_{key}_ci', f'{lo:.0f}-{hi:.0f}%', f'{g}: exact 95% CI of pooled survival', ids, M_CP, '06_survival.py')
rd = SURV['pooled']['MH_RD_344_minus_212']
add('mh_rd', f"{rd['rd']:.0f} percentage points (95% CI {rd['lo']:.0f} to {rd['hi']:.0f})", 'Mantel-Haenszel survival difference PSLN-344 minus PSLN-212, stratified by experiment', AGED11,
    'Mantel-Haenszel risk difference with Greenland-Robins variance, 11 strata', '06_survival.py')
sl = SURV['pooled']['stratified_logrank_344 vs 212']
add('strat_lr', 'p < 0.00001', 'stratified log-rank test PSLN-344 vs PSLN-212 (time to death), labels permuted within experiment',
    AGED11, f"permutation test, 200,000 within-experiment relabellings; observed O-E = {sl['OE']:.1f}, Z = {sl['Z']:.1f}", '06_survival.py')
pe = SURV['per_experiment']
nsig = sum(1 for r in pe if r['fisher_344_v_212'] < 0.05)
add('n_exp_sig', f'{nsig} of 11', 'experiments in which PSLN-344 vs PSLN-212 reaches p < 0.05 on its own', AGED11, 'two-sided Fisher exact test per experiment', '06_survival.py')
add('n_exp_dir', '11 of 11', 'experiments in which PSLN-344 has more survivors than PSLN-212', AGED11, 'direct count', '06_survival.py')
for r in pe:
    bid = r['block']; s3, n3 = r['PSLN-344']; s2, n2 = r['PSLN-212']; ss, ns = r['Sham']
    add(f'surv_{bid}_344', f'{s3}/{n3}', f'{nice(bid)} PSLN-344 survivors', [bid], M_FISH, '06_survival.py', cells=B[bid]['cells']['PSLN-344'])
    add(f'surv_{bid}_212', f'{s2}/{n2}', f'{nice(bid)} PSLN-212 survivors', [bid], M_FISH, '06_survival.py', cells=B[bid]['cells']['PSLN-212'])
    add(f'surv_{bid}_sham', f'{ss}/{ns}', f'{nice(bid)} Sham survivors', [bid], M_FISH, '06_survival.py', cells=B[bid]['cells']['Sham'])
    add(f'surv_{bid}_p', pfmt(r['fisher_344_v_212']), f'{nice(bid)} PSLN-344 vs PSLN-212', [bid], 'two-sided Fisher exact test', '06_survival.py')
    if r['PSLN-212(Y)']:
        add(f'surv_{bid}_young', f"{r['PSLN-212(Y)'][0]}/{r['PSLN-212(Y)'][1]}", f'{nice(bid)} PSLN-212(Y) survivors', [bid], M_FISH, '06_survival.py', cells=B[bid]['cells']['PSLN-212(Y)'])
s, n = sn('S03-I', 'CMP-204'); add('surv_S03-I_cmp', f'{s}/{n}', 'S03-I CMP-204 survivors', ['S03-I'], M_FISH, '06_survival.py', cells=B['S03-I']['cells']['CMP-204'])
# sensitivity
for name, key in [('worst case for PSLN-344 (every survival/weight conflict resolved against it; S03-J 212-arm dropped)', 'worst'),
                  ('as printed, excluding the two label-conflicted blocks S03-I and S03-J', 'excl'), ('worst case AND excluding S03-I, S03-J', 'worst_excl')]:
    d = SURV['pooled'][f'sens::{name}']
    add(f'sens_{key}_344', f"{d['s344']} of {d['n344']} ({100*d['s344']/d['n344']:.0f}%)", f'PSLN-344 pooled survival, sensitivity: {name}', AGED11 + ['S13-F', 'S13-G', 'S15-A..G', 'S15-M', 'S15-O'],
        'for each arm take the less favorable (PSLN-344) or more favorable (PSLN-212) of the survival-table count and the count implied by the paired weight block', '06_survival.py + 03_weight_vs_survival.py', cells='survival and paired weight blocks')
    add(f'sens_{key}_212', f"{d['s212']} of {d['n212']} ({100*d['s212']/d['n212']:.0f}%)", f'PSLN-212 pooled survival, sensitivity: {name}', AGED11 + ['S13-F', 'S13-G', 'S15-A..G', 'S15-M', 'S15-O'],
        'as above', '06_survival.py + 03_weight_vs_survival.py', cells='survival and paired weight blocks')
for name, key, ids in [('mismatched-strain challenges in aged BALB/c (S06-A to S06-G)', 'het', ['S06-A', 'S06-B', 'S06-C', 'S06-D', 'S06-E_r34', 'S06-F_r34', 'S06-G']),
                       ('the three experiments whose survival and weight tables agree for every arm (S06-A, S06-B, S06-F)', 'strict', ['S06-A', 'S06-B', 'S06-F_r34']),
                       ('C57BL/6 and Swiss Webster (S15-L, S15-N)', 'strains', ['S15-L', 'S15-N']),
                       ('challenge 2-3 days after dosing (S03-J, S06-B, S06-D)', 'early', ['S03-J', 'S06-B', 'S06-D']),
                       ('challenge 14 days after dosing (S03-I, S06-A, S06-C)', 'd14', ['S03-I', 'S06-A', 'S06-C']),
                       ('challenge 60 days after dosing (S06-E, S06-F, S06-G)', 'd60', ['S06-E_r34', 'S06-F_r34', 'S06-G'])]:
    for g, gk in [('PSLN-344', '344'), ('PSLN-212', '212'), ('Sham', 'sham'), ('PSLN-212(Y)', 'young')]:
        s, n = pool(ids, g)
        if n:
            lo, hi = cp(s, n)
            add(f'{key}_{gk}', f'{s} of {n} ({100*s/n:.0f}%)', f'{g} survival; {name}', ids, M_CP, '06_survival.py')
            add(f'{key}_{gk}_frac', f'{s}/{n}', f'{g} survivors / animals; {name}', ids, M_CP, '06_survival.py')
            add(f'{key}_{gk}_ci', f'{lo:.0f}-{hi:.0f}%', f'{g} exact 95% CI; {name}', ids, M_CP, '06_survival.py')
su, nu = pool(['S06-E_r34', 'S06-F_r34', 'S06-G'], 'Untreated'); lo, hi = cp(nu - su, nu)
add('untreated_surv', f'{su} of {nu} ({100*su/nu:.0f}%)', 'Untreated (no vaccine, no adjuvant, no virus) age-matched animals alive after the same 14-day window, day-60 experiments', ['S06-E_r34', 'S06-F_r34', 'S06-G'], M_CP, '06_survival.py')
add('untreated_dead', f'{nu-su} of {nu} ({100*(nu-su)/nu:.0f}%; exact 95% CI {lo:.0f}-{hi:.0f}%)', 'background deaths in unchallenged aged animals over 14 days', ['S06-E_r34', 'S06-F_r34', 'S06-G'], M_CP, '06_survival.py')
add('untreated_dead_frac', f'{nu-su}/{nu}', 'background deaths in unchallenged aged animals', ['S06-E_r34', 'S06-F_r34', 'S06-G'], 'direct count', '06_survival.py')
s3, n3 = pool(['S06-E_r34', 'S06-F_r34', 'S06-G'], 'PSLN-344')
add('d60_vs_untreated_p', pfmt(stats.fisher_exact([[s3, n3 - s3], [su, nu - su]])[1]), 'day-60: PSLN-344 challenged vs Untreated unchallenged', ['S06-E_r34', 'S06-F_r34', 'S06-G'], 'two-sided Fisher exact test on pooled counts', '06_survival.py')
d = SURV['pooled']['MH_RD_344_minus_Y']
add('aged344_vs_young', f"{d['s344']}/{d['n344']} vs {d['sY']}/{d['nY']}", 'PSLN-344 aged vs PSLN-212 young, the 10 experiments with both arms', [b for b in AGED11 if b != 'S03-J'], M_CP, '06_survival.py')
add('aged344_vs_young_rd', f"{abs(d['rd']):.0f} points lower (95% CI {abs(d['hi']):.0f} to {abs(d['lo']):.0f})", 'Mantel-Haenszel survival difference, PSLN-344 aged minus PSLN-212 young', [b for b in AGED11 if b != 'S03-J'], 'Mantel-Haenszel risk difference', '06_survival.py')
s2a, n2a = pool([b for b in AGED11 if b != 'S03-J'], 'PSLN-212')
add('age_effect_212', f'{s2a}/{n2a}', 'PSLN-212 in aged animals, the 10 experiments that also have the young arm', [b for b in AGED11 if b != 'S03-J'], M_CP, '06_survival.py')
# S15-H
for g, k in [('3d Vaccine', 'vac'), ('3d PSLN-344', 'adj'), ('3d Vaccine+PSLN-344', 'both')]:
    s, n = sn('S15-H', g); add(f's15h_{k}', f'{s}/{n}', f'S15-H {g} survivors', ['S15-H'], M_FISH, '06_survival.py', cells=B['S15-H']['cells'][g])
add('s15h_p', pfmt(stats.fisher_exact([[6, 1], [0, 7]])[1]), 'S15-H vaccine + PSLN-344 vs either component alone', ['S15-H'], 'two-sided Fisher exact test', '06_survival.py')
add('early_incl_s15h', '28 of 31 (90%)', 'PSLN-344 + vaccine, challenge 2-3 days after dosing, including the S15-H combination arm', ['S03-J', 'S06-B', 'S06-D', 'S15-H'], M_CP, '06_survival.py')
# imprinting
for bid, k in [('S06-E_r71', 'pr8'), ('S06-F_r71', 'perth')]:
    for g, gk in [('Naïve+PSLN-212', 'n212'), ('Imprinting+PSLN-212', 'i212'), ('Naïve+PSLN-344', 'n344'), ('Imprinting+PSLN-344', 'i344')]:
        s, n = sn(bid, g); add(f'imp_{k}_{gk}', f'{s}/{n}', f'{nice(bid)} {g} survivors', [bid], M_FISH, '06_survival.py', cells=B[bid]['cells'][g])
i = SURV['other']['imprint_pooled']
add('imp_344', f"{i['s344']} of 28 ({100*i['s344']/28:.0f}%)", 'PSLN-344, 14-month animals (imprinted and not), both challenges', ['S06-E_r71', 'S06-F_r71'], M_CP, '06_survival.py')
add('imp_212_naive', f"{i['s212_naive']}/14", 'PSLN-212, 14-month non-imprinted animals, both challenges', ['S06-E_r71', 'S06-F_r71'], M_CP, '06_survival.py')
add('imp_212_imp', f"{i['s212_imp']}/14", 'PSLN-212, 14-month imprinted animals, both challenges', ['S06-E_r71', 'S06-F_r71'], M_CP, '06_survival.py')
add('imp_344_imp', f"{sn('S06-E_r71','Imprinting+PSLN-344')[0] + sn('S06-F_r71','Imprinting+PSLN-344')[0]}/14", 'PSLN-344, imprinted animals, both challenges', ['S06-E_r71', 'S06-F_r71'], M_CP, '06_survival.py')
add('imp_344_naive', f"{sn('S06-E_r71','Naïve+PSLN-344')[0] + sn('S06-F_r71','Naïve+PSLN-344')[0]}/14", 'PSLN-344, 14-month non-imprinted animals, both challenges', ['S06-E_r71', 'S06-F_r71'], M_CP, '06_survival.py')
# young
y3 = sum(sn(b, 'PSLN-344Y')[0] for b in ['S09-B', 'S09-D', 'S09-F']); y2 = sum(sn(b, 'PSLN-212Y')[0] for b in ['S09-B', 'S09-D', 'S09-F'])
add('young_344', f'{y3}/24', 'young BALB/c, PSLN-344: survivors over three mismatched-strain challenges (day 21, 21, 180)', ['S09-B', 'S09-D', 'S09-F'], M_CP, '06_survival.py')
add('young_212', f'{y2}/24', 'young BALB/c, PSLN-212: same three experiments', ['S09-B', 'S09-D', 'S09-F'], M_CP, '06_survival.py')
ysh = sum(sn(b, 'Sham')[0] for b in ['S09-B', 'S09-D', 'S09-F']); nsh = sum(sn(b, 'Sham')[1] for b in ['S09-B', 'S09-D', 'S09-F'])
add('young_sham', f'{ysh}/{nsh}', 'young BALB/c, Sham: same three experiments', ['S09-B', 'S09-D', 'S09-F'], M_CP, '06_survival.py')
for g, k in [('CMP-204(Y)', 'cmp'), ('PSLN-344(Y)', '344'), ('Sham', 'sham'), ('Naïve', 'naive')]:
    s, n = sn('S13-E', g); add(f's13e_{k}', f'{s}/{n}', f'S13-E {g} survivors (young, matched challenge)', ['S13-E'], M_FISH, '06_survival.py', cells=B['S13-E']['cells'][g])
# death timing
def ddays(g): return sorted(x['day'] for b in AGED11 if g in G(b) for x in G(b)[g] if x['event'] == 1)
for g, k in [('Sham', 'sham'), ('PSLN-212', '212'), ('PSLN-344', '344')]:
    add(f'death_med_{k}', f'day {np.median(ddays(g)):.0f}', f'median day of death among {g} animals that died (n = {len(ddays(g))})', AGED11, 'median of death days, 11 experiments', '06_survival.py')
add('power_n7_big', f"{100*BIO['power']['existing_n7_85v14']:.0f}%", 'power of the existing 7-per-arm design to detect 85% vs 14% survival', [], 'exact power of two-sided Fisher test, alpha 0.05', '09_biomarkers_power.py', cells='n/a (design calculation)')
add('power_n7_mid', f"{100*BIO['power']['existing_n7_85v50']:.0f}%", 'power of 7 per arm to detect 85% vs 50% survival', [], 'exact power of two-sided Fisher test, alpha 0.05', '09_biomarkers_power.py', cells='n/a (design calculation)')

# ------------------------------------------------------------------------------------------------ serology
SER = [('S03-C', 'hai_h1', 'HAI, H1N1, day 14', True), ('S03-G', 'hai_h3', 'HAI, H3N2, day 14', True), ('S03-A', 'igg_h1', 'IgG, H1N1, day 14', False), ('S03-E', 'igg_h3', 'IgG, H3N2, day 14', False),
       ('S03-D', 'nt_h1', 'neutralizing titer, H1N1, day 14', False), ('S03-H', 'nt_h3', 'neutralizing titer, H3N2, day 14', False),
       ('S13-I', 'boost_h1', 'IgG, H1N1, day 28 after boost on day 14', False), ('S13-J', 'boost_h3', 'IgG, H3N2, day 28 after boost on day 14', False)]
M_GMT = 'geometric mean titer (HAI recorded as 0 set to 5); ratio and 95% CI by Welch t-test on log titers'
for bid, key, name, ishai in SER:
    g = {k: (hai(v) if ishai else v) for k, v in G(bid).items()}
    for grp, gk in [('Sham', 'sham'), ('CMP-204', 'cmp'), ('PSLN-212', '212'), ('PSLN-344', '344'), ('PSLN-212(Y)', 'young')]:
        add(f'{key}_{gk}', f'{gm(g[grp]):,.0f}', f'{name}: GMT {grp}', [bid], M_GMT, '07_immunogenicity_moa.py', cells=B[bid]['cells'][grp])
    est, lo, hi, p = welch(g['PSLN-344'], g['PSLN-212'], log=True)
    add(f'{key}_gmr', f'{est:.1f}-fold (95% CI {lo:.1f}-{hi:.1f})', f'{name}: GMT ratio PSLN-344 / PSLN-212 (aged)', [bid], M_GMT, '07_immunogenicity_moa.py')
    add(f'{key}_gmr_short', f'{est:.1f}-fold', f'{name}: GMT ratio PSLN-344 / PSLN-212 (aged)', [bid], M_GMT, '07_immunogenicity_moa.py')
    est, lo, hi, p = welch(g['PSLN-344'], g['PSLN-212(Y)'], log=True)
    add(f'{key}_vs_young', f'{est:.2f} (95% CI {lo:.2f}-{hi:.2f})', f'{name}: GMT ratio PSLN-344 aged / PSLN-212 young', [bid], M_GMT, '07_immunogenicity_moa.py')
    add(f'{key}_vs_young_pct', f'{100*est:.0f}%', f'{name}: PSLN-344 aged GMT as % of young benchmark', [bid], M_GMT, '07_immunogenicity_moa.py')
    est, lo, hi, p = welch(g['PSLN-212'], g['CMP-204'], log=True)
    add(f'{key}_212_vs_cmp', f'{est:.1f}-fold (95% CI {lo:.1f}-{hi:.1f})', f'{name}: GMT ratio PSLN-212 / CMP-204 (aged)', [bid], M_GMT, '07_immunogenicity_moa.py')
for bid, key in [('S03-C', 'h1'), ('S03-G', 'h3')]:
    for grp, gk in [('PSLN-212', '212'), ('PSLN-344', '344'), ('CMP-204', 'cmp'), ('Sham', 'sham')]:
        v = G(bid)[grp]; add(f'hai40_{key}_{gk}', f'{sum(1 for x in v if x >= 40)}/{len(v)}', f'{bid} {grp}: animals with HAI >= 40', [bid], 'direct count', '07_immunogenicity_moa.py', cells=B[bid]['cells'][grp])
v344 = G('S03-C')['PSLN-344'] + G('S03-G')['PSLN-344']; v212 = G('S03-C')['PSLN-212'] + G('S03-G')['PSLN-212']; vy = G('S03-C')['PSLN-212(Y)'] + G('S03-G')['PSLN-212(Y)']
add('hai_min_344', f'{min(v344)}', 'lowest individual HAI titer among PSLN-344 aged animals (both strains, 10 values)', ['S03-C', 'S03-G'], 'minimum', '09_biomarkers_power.py', cells='S03!N3:N7; S03!N10:N14')
add('hai_max_212', f'{max(v212)}', 'highest individual HAI titer among PSLN-212 aged animals (both strains, 10 values)', ['S03-C', 'S03-G'], 'maximum', '09_biomarkers_power.py', cells='S03!M3:M7; S03!M10:M14')
add('hai_min_young', f'{min(vy)}', 'lowest individual HAI titer among young PSLN-212 animals', ['S03-C', 'S03-G'], 'minimum', '09_biomarkers_power.py', cells='S03!O3:O7; S03!O10:O14')
M_SUB = 'per-animal IgG2a titer / IgG1 titer from the raw subclass blocks, geometric mean; not taken from S03-B or S03-F'
for num, den, key, pr in [('S13-A', 'S13-B', 'h1', 'S03-B'), ('S13-C', 'S13-D', 'h3', 'S03-F')]:
    q = {k: [a / b for a, b in zip(G(num)[k], G(den)[k])] for k in B[num]['order']}
    for grp, gk in [('PSLN-212', '212'), ('PSLN-344', '344'), ('PSLN-212(Y)', 'young')]:
        add(f'sub_{key}_{gk}', f'{gm(q[grp]):.2f}', f'IgG2a:IgG1 ratio ({"H1N1" if key == "h1" else "H3N2"}), {grp}, recomputed from raw titers', [num, den], M_SUB, '05_derived_value_checks.py / 07_immunogenicity_moa.py',
            cells=B[num]['cells'][grp] + ' / ' + B[den]['cells'][grp])
        add(f'sub_{key}_{gk}_printed', f'{gm(G(pr)[grp]):.2f}', f'IgG2a:IgG1 ratio as printed under the column header "{grp}" in {pr}', [pr], 'geometric mean of the printed column', '05_derived_value_checks.py', cells=B[pr]['cells'][grp])
    est, lo, hi, p = welch(q['PSLN-344'], q['PSLN-212'], log=True)
    add(f'sub_{key}_ratio', f'{est:.1f}-fold (95% CI {lo:.1f}-{hi:.1f})', f'IgG2a:IgG1 ratio, PSLN-344 / PSLN-212, {key}', [num, den], M_SUB, '07_immunogenicity_moa.py')
for bid, key in [('S13-A', 'igg2a_h1'), ('S13-B', 'igg1_h1')]:
    for grp, gk in [('PSLN-212', '212'), ('PSLN-344', '344'), ('PSLN-212(Y)', 'young')]:
        add(f'{key}_{gk}', f'{gm(G(bid)[grp]):,.0f}', f'{B[bid]["measurand"].replace("titre", "titer")}: GMT {grp}', [bid], 'geometric mean', '07_immunogenicity_moa.py', cells=B[bid]['cells'][grp])

# ------------------------------------------------------------------------------------------------ innate
M_GF = 'geometric mean fold-change; ratio and 95% CI by Welch t-test on log values'
for bid, tk in [('S01-A_16h', '16'), ('S01-A_72h', '72')]:
    g = G(bid)
    for grp, gk in [('Sham', 'sham'), ('CMP-204', 'cmp'), ('PSLN-212', '212'), ('PSLN-344', '344'), ('PSLN-212(Y)', 'young'), ('PSLN-344(Y)', '344y'), ('PSLN-212/R848', 'r848combo'), ('PSLN-R848', 'r848')]:
        add(f'ifn{tk}_{gk}', f'{gm(g[grp]):.1f}', f'Ifnb1 fold, {tk} h, {grp}', ['S01-A'], M_GF, '07_immunogenicity_moa.py', cells=B[bid]['cells'][grp])
    for a, b_, k in [('PSLN-344', 'PSLN-212', '344v212'), ('PSLN-344', 'PSLN-212(Y)', '344vY'), ('PSLN-212', 'PSLN-212(Y)', '212vY'), ('PSLN-212', 'CMP-204', '212vcmp'), ('PSLN-344(Y)', 'PSLN-212(Y)', '344YvY')]:
        est, lo, hi, p = welch(g[a], g[b_], log=True)
        add(f'ifn{tk}_{k}', f'{est:.2f} (95% CI {lo:.2f}-{hi:.2f})', f'Ifnb1 {tk} h: ratio {a} / {b_}', ['S01-A'], M_GF, '07_immunogenicity_moa.py', cells=f"{B[bid]['cells'][a]}; {B[bid]['cells'][b_]}")
        add(f'ifn{tk}_{k}_s', f'{est:.1f}-fold', f'Ifnb1 {tk} h: ratio {a} / {b_}', ['S01-A'], M_GF, '07_immunogenicity_moa.py', cells=f"{B[bid]['cells'][a]}; {B[bid]['cells'][b_]}")
d = IMM['S08-A']
for grp, gk in [('PSLN-344', '344'), ('PSLN-212', '212'), ('CMP-204', 'cmp'), ('PSLN-344/R848', '344r848')]:
    for dose in ['1', '5', '10', '20', '40']:
        add(f'dose_{gk}_{dose}', f'{d[grp][dose]:.1f}', f'Ifnb1 fold at 16 h, {grp}, {dose} µg', ['S08-A'], 'geometric mean, n = 3', '07_immunogenicity_moa.py', cells=B['S08-A']['cells'][grp])
add('dose_344_pct', f"{100*d['PSLN-344']['20']/d['PSLN-344']['40']:.0f}%", 'PSLN-344 response at 20 µg as % of its 40 µg response', ['S08-A'], 'ratio of geometric means', '07_immunogenicity_moa.py', cells=B['S08-A']['cells']['PSLN-344'])
add('dose_344_ed50', f"{d['hill_PSLN-344']['ed50']:.0f} µg", 'dose giving half-maximal Ifnb1 induction, PSLN-344', ['S08-A'], f"three-parameter Hill fit to 15 animals (Emax {d['hill_PSLN-344']['top']:.0f}-fold, SE of ED50 {d['hill_PSLN-344']['se'][1]:.1f} µg)", '07_immunogenicity_moa.py', cells=B['S08-A']['cells']['PSLN-344'])
add('dose_ratio_20', f"{d['PSLN-344']['20']/d['PSLN-212']['20']:.1f}-fold", 'Ifnb1 at 20 µg: PSLN-344 / PSLN-212 in the dose-response block', ['S08-A'], 'ratio of geometric means', '07_immunogenicity_moa.py')
b = B['S02-F']
for t in b['times']:
    for grp, gk in [('PSLN-344', '344'), ('PSLN-212', '212'), ('Sham', 'sham')]:
        add(f'gmcsf_{t}_{gk}', f"{gm(b['groups'][grp][t]):.1f}", f'Gm-csf fold, {t}, {grp}', ['S02-F'], 'geometric mean, n = 5', '07_immunogenicity_moa.py', cells=b['cells'][grp])
for grp, gk in [('PSLN-344', '344'), ('PSLN-212', '212'), ('CMP-204', 'cmp'), ('PSLN-212/R848', 'r848combo'), ('PSLN-R848', 'r848')]:
    v = G('S08-B')[grp]; add(f'ee_{gk}', f'{np.mean(v):.1f}% (SD {np.std(v, ddof=1):.1f})', f'encapsulation efficiency, {grp}, n = 3 preparations', ['S08-B'], 'mean and SD', '07_immunogenicity_moa.py', cells=B['S08-B']['cells'][grp])

# ------------------------------------------------------------------------------------------------ cellular (static four-arm blocks)
CELL = [('S02-A', 'ccr7', 'CCR7+ of lung CD11b+ DC, 72 h'), ('S02-B', 'mlndc', 'CD11b+ DC in lymph node, 72 h'), ('S02-C', 'ova', 'antigen-carrying DC in lymph node, 36 h'),
        ('S02-D_CD40', 'cd40', 'CD40+ of lymph-node CD11b+ DC, day 3'), ('S02-D_CD86', 'cd86', 'CD86+ of lymph-node CD11b+ DC, day 3'), ('S02-E', 'oti', 'CD8 (OT-I) proliferation driven by lymph-node DC'),
        ('S03-K', 'gc', 'germinal-center B cells, day 7'), ('S04-A_ICOShi', 'tfh', 'ICOS-high Tfh, day 7'), ('S04-B_Foxp3', 'tfr', 'Tfr share of CXCR5+ICOShi CD4, day 7'), ('S04-C', 'tfr30', 'Tfr share, day 30'),
        ('S04-D', 'treg', 'lung regulatory T cells, day 7'), ('S05-D', 'ki67', 'Ki-67+ lung CD8, day 3'), ('S05-E', 'gzmb', 'granzyme B+ lung CD8, day 3'),
        ('S05-F', 'ifng14', 'H5N1-cross-reactive IFN-g+ CD8, day 14'), ('S05-G', 'ifng60', 'H5N1-cross-reactive IFN-g+ CD8, day 60'), ('S05-H', 'gzmb60', 'granzyme B+ CD8 in lymph node, day 60'),
        ('S05-I', 'trm', 'lung resident-memory CD8, day 25'), ('S14-A_H1N1', 'ifng_h1', 'IFN-g+ CD8, H1N1 restimulation'), ('S14-A_H3N2', 'ifng_h3', 'IFN-g+ CD8, H3N2 restimulation'),
        ('S13-H', 'iggb', 'IgG+ of lymph-node B cells'), ('S11-E', 'cd206', 'CD206+ lung macrophages'), ('S01-F', 'cdc1', 'cDC1 share of lung cDC, 72 h')]
for bid, key, name in CELL:
    g = G(bid)
    for grp, gk in [('Sham', 'sham'), ('PSLN-212', '212'), ('PSLN-344', '344'), ('PSLN-212(Y)', 'young')]:
        if grp in g:
            add(f'{key}_{gk}', f'{np.mean(g[grp]):.1f}%', f'{name}: mean {grp} (n = {len(g[grp])})', [bid.split('_')[0] if bid.startswith('S02-D') or bid.startswith('S04') or bid.startswith('S14') else bid], 'arithmetic mean', '07_immunogenicity_moa.py', cells=B[bid]['cells'][grp])
    add(f'{key}_pct_young', f"{100*np.mean(g['PSLN-344'])/np.mean(g['PSLN-212(Y)']):.0f}%", f'{name}: PSLN-344 aged mean as % of young benchmark', [bid], 'ratio of means', '07_immunogenicity_moa.py')
    est, lo, hi, p = welch(g['PSLN-344'], g['PSLN-212'])
    add(f'{key}_p', pfmt(p), f'{name}: PSLN-344 vs PSLN-212 (aged)', [bid], 'Welch t-test, two-sided', '07_immunogenicity_moa.py')
holm = IMM['holm_344_v_212']
add('holm_n', f'{len(holm)}', 'number of PSLN-344 vs PSLN-212 contrasts (aged animals) in the multiplicity family', ['serology and cellular blocks'], 'count', '07_immunogenicity_moa.py', cells='see sheet Cellular_mechanism')
add('holm_sig', f'{sum(1 for v in holm.values() if v < 0.05)}', 'contrasts that stay below 0.05 after Holm adjustment', ['serology and cellular blocks'], 'Holm step-down on Welch p-values', '07_immunogenicity_moa.py', cells='see sheet Cellular_mechanism')
# time-courses
for bid, key, name in [('S01-D', 'mono', 'lung monocytes, day 4'), ('S01-E', 'cd11bdc', 'lung CD11b+ DC, day 4')]:
    for grp, gk in [('Sham', 'sham'), ('PSLN-212', '212'), ('PSLN-344', '344'), ('PSLN-212(Y)', 'young')]:
        add(f'{key}_{gk}', f"{np.mean(G(bid)[grp]['4']):.1f}%", f'{name}: mean {grp} (n = 5)', [bid], 'arithmetic mean of the day-4 row', '07_immunogenicity_moa.py', cells=B[bid]['cells'][grp])
for grp, gk in [('PSLN-212', '212'), ('PSLN-344', '344')]:
    add(f'mac_{gk}', f"{np.mean(G('S07-A')[grp]['5']):.1f}", f'lung Ly6C+CCR2+ macrophages, day 5, x10^5 cells, {grp} (n = 3)', ['S07-A'], 'arithmetic mean of the day-5 row', '07_immunogenicity_moa.py', cells=B['S07-A']['cells'][grp])
    add(f'mac10_{gk}', f"{np.mean(G('S07-A')[grp]['10']):.1f}", f'lung Ly6C+CCR2+ macrophages, day 10, x10^5 cells, {grp} (n = 3)', ['S07-A'], 'arithmetic mean of the day-10 row', '07_immunogenicity_moa.py', cells=B['S07-A']['cells'][grp])
# interventions
INT = [('S01-C', 'WT', 'SPA/D', 'did'), ('S01-B', 'AECII/PSLN-SRB', 'AECII/FreeSRB', 'srb2'), ('S01-B', 'AECI/PSLN-SRB', 'AECI/FreeSRB', 'srb1'), ('S11-C', 'CBX-', 'CBX+', 'cbx'),
       ('S07-B_mono', 'PSLN-344', 'PSLN-344+INCB3344', 'incb_mono'), ('S07-B_mac', 'PSLN-344', 'PSLN-344+INCB3344', 'incb_mac'), ('S02-I', 'PSLN-344(Y)', 'PSLN-344(Y)+INCB3344', 'incb_gzmb'),
       ('S02-H', 'WT w/o cDC', 'IFN w/o cDC', 'ifnar'), ('S02-H', 'GMCSF', 'IFN w/o cDC', 'gmcsf_rescue'), ('S12-A', 'WT to WT', 'IFNAR-/- to WT', 'ifnar_mono'),
       ('S02-G', 'PSLN-212+GM-CSF', 'PSLN-212', 'gmcsf_add'), ('S02-E', 'PSLN-344', 'PTX', 'ptx_oti'), ('S05-C', 'MLN', 'MLN+PTX', 'ptx_mln'), ('S05-C', 'Lung', 'Lung+PTX', 'ptx_lung')]
for bid, a, b_, key in INT:
    g = G(bid); est, lo, hi, p = welch(g[a], g[b_])
    add(f'int_{key}_a', f'{np.mean(g[a]):.1f}%', f'{bid} {a}: mean (n = {len(g[a])})', [bid.split('_')[0]], 'arithmetic mean', '07_immunogenicity_moa.py', cells=B[bid]['cells'][a])
    add(f'int_{key}_b', f'{np.mean(g[b_]):.1f}%', f'{bid} {b_}: mean (n = {len(g[b_])})', [bid.split('_')[0]], 'arithmetic mean', '07_immunogenicity_moa.py', cells=B[bid]['cells'][b_])
    add(f'int_{key}_p', pfmt(p), f'{bid} {a} vs {b_}', [bid.split('_')[0]], 'Welch t-test, two-sided', '07_immunogenicity_moa.py')
for an, bid in [('aicda', 'S03-L_Aicda'), ('e47', 'S03-L_E47')]:
    for grp, gk in [('PSLN-212', '212'), ('PSLN-344', '344')]:
        add(f'{an}_{gk}', f'{gm(G(bid)[grp]):.1f}', f'{an} transcript fold in lymph-node B cells, day 5, {grp} (n = 3)', ['S03-L'], 'geometric mean', '07_immunogenicity_moa.py', cells=B[bid]['cells'][grp])
g = G('S07-C'); ks = list(g)
add('s07c_b', f'{np.mean(g[ks[0]]):.1f}%', 'S07-C column B (label "Ly6C-CD206+ MΦ"): lung Treg after macrophage transfer', ['S07-C'], 'arithmetic mean', '07_immunogenicity_moa.py', cells=B['S07-C']['cells'][ks[0]])
add('s07c_c', f'{np.mean(g[ks[1]]):.1f}%', 'S07-C column C (same printed label): lung Treg after macrophage transfer', ['S07-C'], 'arithmetic mean', '07_immunogenicity_moa.py', cells=B['S07-C']['cells'][ks[1]])
# SRB two readings
gc_ = G('S08-C'); kk = list(gc_)
for i, k in enumerate(kk):
    add(f's08c_col{i+1}', f'{np.mean(gc_[k]):.1f}%', f'S08-C column {"ABCD"[i]} (printed header "{k}"): mean', ['S08-C'], 'arithmetic mean', '05_derived_value_checks.py', cells=B['S08-C']['cells'][k])
add('s01b_aec1', f"{np.mean(G('S01-B')['AECI/PSLN-SRB']):.1f}%", 'S01-B AECI/PSLN-SRB mean', ['S01-B'], 'arithmetic mean', '05_derived_value_checks.py', cells=B['S01-B']['cells']['AECI/PSLN-SRB'])
add('s01b_aec2', f"{np.mean(G('S01-B')['AECII/PSLN-SRB']):.1f}%", 'S01-B AECII/PSLN-SRB mean', ['S01-B'], 'arithmetic mean', '05_derived_value_checks.py', cells=B['S01-B']['cells']['AECII/PSLN-SRB'])

# ------------------------------------------------------------------------------------------------ tolerability
s = SAF['S08-D']
for grp, gk in [('PSLN-344', '344'), ('PSLN-212', '212'), ('Vaccine', 'vac'), ('PSLN-212/R848', 'r848combo'), ('PSLN-212(Y)', 'young'), ('CMP-204', 'cmp')]:
    add(f'bw_nadir_{gk}', f"{s[grp]['nadir_mean']:.1f}%", f'body weight after dosing, lowest group mean ({grp}, day {s[grp]["nadir_day"]})', ['S08-D'], 'mean of animals with a value on that day', '08_safety_tolerability.py', cells=B['S08-D']['cells'][grp])
    add(f'bw_d10_{gk}', f"{s[grp]['d10_mean']:.1f}%", f'body weight on day 10 after dosing, {grp}', ['S08-D'], 'mean of animals with a value', '08_safety_tolerability.py', cells=B['S08-D']['cells'][grp])
    add(f'bw_lt90_{gk}', f"{s[grp]['animals_below_90']}/5", f'{grp}: animals that fell below 90% of starting weight', ['S08-D'], 'per-animal minimum', '08_safety_tolerability.py', cells=B['S08-D']['cells'][grp])
    add(f'bw_lt95_{gk}', f"{s[grp]['animals_below_95']}/5", f'{grp}: animals that fell below 95% of starting weight', ['S08-D'], 'per-animal minimum', '08_safety_tolerability.py', cells=B['S08-D']['cells'][grp])
add('bw_344_vs_vac_d6', f"{abs(s['d6_344_minus_vaccine'][0]):.1f} points", 'PSLN-344 minus vaccine-alone body weight, day 6 (largest gap)', ['S08-D'], f"difference of means; Welch {pfmt(s['d6_344_minus_vaccine'][1])}", '08_safety_tolerability.py')
for pid, pk in [('S09-A_panel1', 'c16'), ('S09-A_panel2', 'c72')]:
    for an in ['Ifnb1', 'Il6', 'Ccl2', 'Ccl3', 'Ccl5', 'Tnf', 'Il10']:
        for grp, gk in [('PSLN-344', '344'), ('PSLN-212', '212'), ('PSLN-212(y)', 'young'), ('PSLN-212/R848', 'r848combo'), ('PSLN-R848', 'r848'), ('CMP-204', 'cmp')]:
            v = SAF[pid][an][grp]
            add(f'{pk}_{an.lower()}_{gk}', (f'{v:,.0f}' if v >= 10 else f'{v:.1f}'), f'{an} fold vs untreated, {grp}, {"first" if pk=="c16" else "second"} S09-A panel', ['S09-A'], '10^(mean of log10 values), n = 3', '08_safety_tolerability.py', cells=B[pid]['cells'][grp])
for an in ['Ifnb1', 'Tnf', 'Isg15']:
    d = SAF[f'S10-A_{an}']
    add(f'cns_{an.lower()}_344', f"{d['r344_pbs'][0]:.2f}-fold (95% CI {d['r344_pbs'][1]:.2f}-{d['r344_pbs'][2]:.2f})", f'CNS {an}: PSLN-344 / buffer', ['S10-A'], 'ratio of geometric means, Welch on log values', '08_safety_tolerability.py')
    add(f'cns_{an.lower()}_344_sham', f"{d['r344_sham'][0]:.2f}-fold", f'CNS {an}: PSLN-344 / vaccine + empty liposome ({pfmt(d["r344_sham"][1])})', ['S10-A'], 'ratio of geometric means', '08_safety_tolerability.py')
    add(f'cns_{an.lower()}_ct', f"{d['rCT_pbs'][0]:.1f}-fold", f'CNS {an}: cholera toxin / buffer', ['S10-A'], 'ratio of geometric means', '08_safety_tolerability.py')
    add(f'cns_{an.lower()}_hi', f"{d['r344_pbs'][2]:.1f}-fold", f'CNS {an}: upper 95% bound of PSLN-344 / buffer', ['S10-A'], 'Welch CI on log values', '08_safety_tolerability.py')
for g_, k in [('PSLN-344', '344'), ('PSLN-212(Y)', 'young')]:
    d = SAF[f'pooled_nadir_{g_}']
    add(f'nadir_{k}', f"{100-d['mean_nadir']:.0f}%", f'mean peak weight loss after challenge among {g_} survivors (n = {d["n"]}, 10 blocks)', ['S13-F', 'S15-A', 'S15-B', 'S15-C', 'S15-D', 'S15-E', 'S15-F', 'S15-G', 'S15-M', 'S15-O'],
        'per-animal minimum weight, carried-forward and blank cells removed; mean over survivors', '08_safety_tolerability.py')
b = B['S09-G']
for t in ['12', '14']:
    a = b['groups']['PSLN-344Y'][t]; c = b['groups']['PSLN-212Y'][t]
    add(f'young_d180_bw{t}', f'{np.mean(a):.1f}% vs {np.mean(c):.1f}%', f'young animals challenged 180 days after dosing: body weight on day {t} post-challenge, PSLN-344 vs PSLN-212', ['S09-G'], f'means, n = 8; Welch {pfmt(stats.ttest_ind(a, c, equal_var=False)[1])}', 'facts.py')

# ------------------------------------------------------------------------------------------------ integrity
tot = same = r1 = r2 = 0
for grp in B['S11-A']['order']:
    for t in B['S11-A']['times']:
        a = G('S11-A')[grp][t]; b_ = G('S11-B')[grp][t]; tot += 5; same += sum(x == y for x, y in zip(a, b_)); r1 += a[0] == b_[0]; r2 += a[1] == b_[1]
add('s11_same', f'{same} of {tot}', 'cells identical between S11-A (alveolar macrophages) and S11-B (neutrophils)', ['S11-A', 'S11-B'], 'position-wise comparison', '05_derived_value_checks.py')
add('s11_rep1', f'{r1} of 20', 'group-by-time cells in which the first replicate of S11-B equals that of S11-A', ['S11-A', 'S11-B'], 'position-wise comparison', '05_derived_value_checks.py')
add('s11_rep2', f'{r2} of 20', 'group-by-time cells in which the second replicate of S11-B equals that of S11-A', ['S11-A', 'S11-B'], 'position-wise comparison', '05_derived_value_checks.py')
a = B['S15-C']['groups']['PSLN-344']; c = B['S15-I']['groups']['3d Vaccine+PSLN-344']
same = sum(x == y for t in ['2', '4', '6', '8', '10', '12'] for x, y in zip(a[t], c[t]))
add('dup_s15c_s15i', f'{same} of 42', 'body-weight cells (days 2-12, 7 animals) identical between S15-C PSLN-344 and S15-I Vaccine+PSLN-344', ['S15-C', 'S15-I'], 'position-wise comparison', '04_duplicate_scan.py / 04b_weight_trajectory_dups.py')
a = B['S09-C']['groups']['PSLN-212Y']['12']; c = B['S09-C']['groups']['PSLN-344Y']['12']
add('dup_s09c', f'{sum(x == y for x, y in zip(a, c))} of 8', 'day-12 body weights identical between PSLN-212Y and PSLN-344Y in S09-C', ['S09-C'], 'position-wise comparison', '04_duplicate_scan.py')
add('rms_p2_72', '0.011', 'RMS difference (log10) between the second S09-A panel Ifnb1 group means and the S01-A 72 h group means', ['S09-A', 'S01-A'], 'root-mean-square difference of log10 group geometric means over 7 groups', '05_derived_value_checks.py')
add('rms_p2_16', '0.88', 'same, against the S01-A 16 h group means', ['S09-A', 'S01-A'], 'as above', '05_derived_value_checks.py')
add('n_numeric', '6,819', 'numeric cells in the workbook, each assigned to a block or an axis', ['all sheets'], 'parser completeness check', '01_parse_workbook.py', cells='all')
add('n_blocks', '108', 'data blocks parsed from the workbook (multi-panel blocks counted per panel)', ['all sheets'], 'count of parsed blocks', '01_parse_workbook.py', cells='all')

# ------------------------------------------------------------------------------------------------ power
P = BIO['power']
add('n_rep', f"{P['conservative replication: 78% vs 19% (worst-case sensitivity)']['n90']}", 'animals per arm for 90% power, survival 78% vs 19%', [], 'exact power, two-sided Fisher test, alpha 0.05', '09_biomarkers_power.py', cells='n/a (design calculation)')
add('n_attr40', f"{P['attribution: PSLN-344 85% vs Mn-only control assumed 40%']['n90']}", 'animals per arm for 90% power, survival 85% vs 40%', [], 'exact power, two-sided Fisher test, alpha 0.05', '09_biomarkers_power.py', cells='n/a (design calculation)')
add('n_attr50', f"{P['attribution: PSLN-344 85% vs Mn-only control assumed 50%']['n90']}", 'animals per arm for 90% power, survival 85% vs 50%', [], 'exact power, two-sided Fisher test, alpha 0.05', '09_biomarkers_power.py', cells='n/a (design calculation)')
add('n_hai2', f"{P['HAI superiority, detect 2-fold GMR']['n']}", 'animals per arm for 90% power to detect a 2-fold HAI GMT ratio', ['S03-C', 'S03-G'], f"two-sample t-test on log2 titers, pooled within-group SD {P['sd_hai_log2']:.2f} log2", '09_biomarkers_power.py', cells='S03!L3:O7; S03!L10:O14')
add('n_hai3', f"{P['HAI superiority, detect 3-fold GMR']['n']}", 'animals per arm for 90% power to detect a 3-fold HAI GMT ratio', ['S03-C', 'S03-G'], 'as above', '09_biomarkers_power.py', cells='S03!L3:O7; S03!L10:O14')
add('n_ni', f"{P['NI true 0.76']}", 'animals per arm for 90% power to show HAI non-inferiority (margin 0.5) if the true ratio is 0.76', ['S03-C', 'S03-G'], 'one-sided 0.025 non-inferiority t-test on log2 titers', '09_biomarkers_power.py', cells='S03!L3:O7; S03!L10:O14')
add('sd_hai', f"{P['sd_hai_log2']:.2f}", 'pooled within-group SD of log2 HAI titer', ['S03-C', 'S03-G'], 'root mean square of group SDs (four adjuvanted arms, two strains)', '09_biomarkers_power.py', cells='S03!L3:O7; S03!L10:O14')

# ------------------------------------------------------------------------------------------------ extra facts used in the text
def _fisher_power(p1, p2, n, alpha=0.05):
    pw = 0.0
    for a in range(n + 1):
        pa = stats.binom.pmf(a, n, p1)
        for c in range(n + 1):
            pc = stats.binom.pmf(c, n, p2)
            if pa * pc > 1e-12 and stats.fisher_exact([[a, n - a], [c, n - c]])[1] <= alpha: pw += pa * pc
    return pw
add('power_n17_attr', f"{100*_fisher_power(0.85, 0.40, 17):.0f}%", 'power of 17 per arm to detect 85% vs 40% survival', [], 'exact power, two-sided Fisher test, alpha 0.05', 'facts.py', cells='n/a (design calculation)')
add('power_n17_rep', f"{100*_fisher_power(0.78, 0.19, 17):.0f}%", 'power of 17 per arm to detect 78% vs 19% survival', [], 'exact power, two-sided Fisher test, alpha 0.05', 'facts.py', cells='n/a (design calculation)')
# weight-block readings of the two label-conflicted experiments
def _traj(bid, g):
    b = B[bid]; n = len(b['groups'][g][b['times'][0]])
    return [[b['groups'][g][t][i] for t in b['times']] for i in range(n)]
t = _traj('S13-F', 'PSLN-212'); rec = sum(1 for s in t if s[-1] is not None and s[-1] >= 95 and s[-1] != s[-2])
flat = sum(1 for s in t if s[-1] == s[-2] == s[-3])
add('s13f_212_recover', f'{rec} of {len(t)}', 'S13-F (body weight, "animals of S03-I"): PSLN-212 animals back to at least 95% of starting weight on day 14', ['S13-F'], 'count of animals with a changing series ending at 95% or more', '03_weight_vs_survival.py', cells=B['S13-F']['cells']['PSLN-212'])
add('s13f_212_flat', f'{flat} of {len(t)}', 'S13-F PSLN-212 animals whose last value is repeated unchanged from day 10 to day 14 (78-80%)', ['S13-F'], 'count of series with three identical final cells', '03_weight_vs_survival.py', cells=B['S13-F']['cells']['PSLN-212'])
t = _traj('S13-G', 'Sham'); rec = sum(1 for s in t if s[-1] >= 95)
add('s13g_sham_recover', f'{rec} of {len(t)}', 'S13-G (body weight, "animals of S03-J"): animals in the arm labeled Sham back to at least 95% on day 14', ['S13-G'], 'count', '03_weight_vs_survival.py', cells=B['S13-G']['cells']['Sham'])
t = _traj('S13-G', 'Naïve'); rec = sum(1 for s in t if s[-1] >= 95)
add('s13g_naive_recover', f'{rec} of {len(t)}', 'S13-G: animals in the arm labeled Naive back to at least 95% on day 14', ['S13-G'], 'count', '03_weight_vs_survival.py', cells=B['S13-G']['cells']['Naïve'])
add('fisher_7v3', pfmt(stats.fisher_exact([[7, 0], [3, 4]])[1]), 'S03-I under the weight-table reading: PSLN-344 7/7 vs PSLN-212 3/7', ['S03-I', 'S13-F'], 'two-sided Fisher exact test', 'facts.py', cells='n/a')
# ranges for prose
add('ab_fold_lo', f"{min(welch(G(b)['PSLN-344'] if 'C' not in b and 'G' not in b else hai(G(b)['PSLN-344']), G(b)['PSLN-212'], log=True)[0] for b in ['S03-A','S03-E','S03-C','S03-G','S03-D','S03-H']):.0f}",
    'smallest GMT ratio PSLN-344 / PSLN-212 across IgG, HAI and neutralizing titers (two strains)', ['S03-A', 'S03-C', 'S03-D', 'S03-E', 'S03-G', 'S03-H'], 'minimum of six ratios', '07_immunogenicity_moa.py')
add('ab_fold_hi', f"{max(welch(G(b)['PSLN-344'], G(b)['PSLN-212'], log=True)[0] for b in ['S03-A','S03-E','S03-C','S03-G','S03-D','S03-H']):.0f}",
    'largest GMT ratio PSLN-344 / PSLN-212 across IgG, HAI and neutralizing titers (two strains)', ['S03-A', 'S03-C', 'S03-D', 'S03-E', 'S03-G', 'S03-H'], 'maximum of six ratios', '07_immunogenicity_moa.py')

_uv = [x for bid in ['S15-E', 'S15-F', 'S15-G'] for t, v in B[bid]['groups']['Untreated'].items() if t != '0' for x in v if x is not None]
add('untreated_bw_range', f'{min(_uv):.0f}-{max(_uv):.0f}%', 'range of body weights recorded for Untreated (unchallenged) animals, days 2-14', ['S15-E', 'S15-F', 'S15-G'], 'minimum and maximum of all cells', 'facts.py')

# gap closed (restoration) summary - values written by 12_fig3_restoration.py
_R = json.load(open('/tmp/work/parsed/restoration.json'))
_rv = {r[0]: r[4] for r in _R}
_main = [v for k, v in _rv.items() if v >= 50]
add('gap_main_range', f'{min(_main):.0f}-{max(_main):.0f}%', 'range of "gap closed" across the readouts where PSLN-344 closes at least half of the aged-to-young gap', ['blocks listed in Figure 3'],
    '(PSLN-344 aged - PSLN-212 aged) / (PSLN-212 young - PSLN-212 aged); log scale for titers, ratios, fold-changes', '12_fig3_restoration.py', cells='see Figure 3 and sheet Cellular_mechanism')
add('gap_n_main', f'{len(_main)} of {len(_rv)}', 'readouts in Figure 3 on which PSLN-344 closes at least half of the aged-to-young gap', ['blocks listed in Figure 3'], 'count', '12_fig3_restoration.py', cells='see Figure 3')
for k, lab in [('gap_cd40', 'CD40+ lymph-node DC, day 3  [S02-D]'), ('gap_cd86', 'CD86+ lymph-node DC, day 3  [S02-D]'), ('gap_gzmb', 'Granzyme B+ lung CD8, day 3  [S05-E]'), ('gap_ifn', 'Ifnb1 mRNA, lung, 16 h  [S01-A]'), ('gap_surv', 'Survival, 10 challenge experiments with all three arms')]:
    add(k, f'{_rv[lab]:.0f}%', f'gap closed: {lab}', ['S02-D' if 'S02-D' in lab else ('S05-E' if 'S05-E' in lab else ('S01-A' if 'S01-A' in lab else 'S06-A'))], 'as above', '12_fig3_restoration.py', cells='see Figure 3')
for g_, k in [('PSLN-344Y', '344'), ('PSLN-212Y', '212')]:
    s_, n_ = sn('S09-F', g_); add(f'young_d180_{k}', f'{s_}/{n_}', f'S09-F young {g_}: survivors, challenge 180 days after dosing', ['S09-F'], M_FISH, '06_survival.py', cells=B['S09-F']['cells'][g_])
for grp, gk in [('PSLN-212', '212'), ('PSLN-344', '344'), ('PSLN-212(Y)', 'young')]:
    v = G('S03-C')[grp] + G('S03-G')[grp]
    add(f'hai160_{gk}', f'{sum(1 for x in v if x >= 160)}/{len(v)}', f'{grp}: HAI values at or above 160 (H1N1 and H3N2 combined)', ['S03-C', 'S03-G'], 'direct count', '09_biomarkers_power.py',
        cells=B['S03-C']['cells'][grp] + '; ' + B['S03-G']['cells'][grp])
add('n_disc', '20', 'discrepancies in the integrity log', ['see Section 9'], 'count of log entries', 'integrity_log.py', cells='n/a')
add('n_disc_high', '6', 'discrepancies ranked High', ['see Section 9'], 'count of log entries ranked High', 'integrity_log.py', cells='n/a')

for g_, k in [('PSLN-344Y', '344'), ('PSLN-212Y', '212')]:
    v = B['S09-G']['groups'][g_]['14']
    add(f'bw180_{k}', f'{np.mean(v):.1f}%', f'young {g_}: mean body weight 14 days after a challenge given 180 days after dosing (n = {len(v)})', ['S09-G'], 'arithmetic mean of the day-14 row', 'facts.py', cells=B['S09-G']['cells'][g_])

_r = [welch(hai(G(b)['PSLN-212']) if b in ('S03-C', 'S03-G') else G(b)['PSLN-212'], hai(G(b)['CMP-204']) if b in ('S03-C', 'S03-G') else G(b)['CMP-204'], log=True)[0] for b in ['S03-A', 'S03-E', 'S03-C', 'S03-G', 'S03-D', 'S03-H']]
add('n_ab_2fold', f'{sum(1 for x in _r if x >= 1.9)} of {len(_r)}', 'antibody readouts (IgG, HAI, neutralizing titer; two strains) on which PSLN-212 is about 2-fold above the cGAMP liposome CMP-204 in aged mice', ['S03-A', 'S03-C', 'S03-D', 'S03-E', 'S03-G', 'S03-H'],
    'count of GMT ratios PSLN-212 / CMP-204 of at least 1.9 (ratios: ' + ', '.join(f'{x:.1f}' for x in _r) + ')', '07_immunogenicity_moa.py')
_cs = [SAF[f'S10-A_{an}']['r344_sham'][0] for an in ['Ifnb1', 'Tnf', 'Isg15']]
add('cns_sham_max', f'{max(_cs):.1f}-fold', 'largest ratio PSLN-344 / vaccine + empty liposome across the three brain transcripts', ['S10-A'], 'maximum of three ratios of geometric means (' + ', '.join(f'{x:.2f}' for x in _cs) + ')', '08_safety_tolerability.py')
_ct = [SAF[f'S10-A_{an}']['rCT_pbs'][0] for an in ['Ifnb1', 'Tnf', 'Isg15']]
add('cns_ct_range', f'{min(_ct):.1f}- to {max(_ct):.1f}-fold', 'range of cholera toxin / buffer across the three brain transcripts', ['S10-A'], 'ratios of geometric means', '08_safety_tolerability.py')

if __name__ == '__main__':
    print(len(FACTS), 'facts')
    for k, v in list(FACTS.items()):
        print(f"{k:<28} {v['text']:<42} | {v['what'][:90]}")

