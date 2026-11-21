"""16_evidence_workbook.py - writes PSLN_evidence_tables.xlsx: every number quoted in the proposal with its source,
plus the per-block statistics, the integrity log and the sample-size calculations.
Run in the 'chem' environment (xlsxwriter):  micromamba run -n chem python 16_evidence_workbook.py"""
import json, math, itertools, csv, collections
import numpy as np
from scipy import stats
import xlsxwriter
from facts import FACTS, B, G, AGED11, sn, cp, gm, welch, hai
from integrity_log import LOG, DESIGN_LIMITS

USED = json.load(open('/tmp/work/parsed/facts_used.json'))
SURV = json.load(open('/tmp/work/parsed/survival_results.json'))
IMM = json.load(open('/tmp/work/parsed/immuno_moa_results.json'))
SAF = json.load(open('/tmp/work/parsed/safety_results.json'))
BIO = json.load(open('/tmp/work/parsed/biomarker_power.json'))
WV = json.load(open('/tmp/work/parsed/weight_vs_survival.json'))
OUT = '/tmp/outputs/PSLN_evidence_tables.xlsx'
wb = xlsxwriter.Workbook(OUT)
import datetime as _dt
wb.set_properties({'title': 'PSLN program - evidence tables behind the portfolio proposal', 'subject': 'Source and calculation for every number quoted', 'created': _dt.datetime(2026, 11, 1, 12, 0)})
H = wb.add_format({'bold': True, 'bg_color': '#DCE6F1', 'border': 1, 'text_wrap': True, 'valign': 'top'})
T = wb.add_format({'text_wrap': True, 'valign': 'top'})
N2 = wb.add_format({'num_format': '0.00', 'valign': 'top'}); N1 = wb.add_format({'num_format': '0.0', 'valign': 'top'}); N0 = wb.add_format({'num_format': '#,##0', 'valign': 'top'})
P = wb.add_format({'num_format': '0.0000', 'valign': 'top'}); TITLE = wb.add_format({'bold': True, 'font_size': 14}); B_ = wb.add_format({'bold': True})
def sheet(name, headers, rows, widths, note=None):
    ws = wb.add_worksheet(name); r0 = 0
    if note:
        ws.write(0, 0, note, wb.add_format({'italic': True, 'text_wrap': False})); r0 = 2
    for j, h in enumerate(headers): ws.write(r0, j, h, H)
    for i, row in enumerate(rows, r0 + 1):
        for j, v in enumerate(row):
            if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))): ws.write_blank(i, j, None, T)
            elif isinstance(v, (int, np.integer)): ws.write_number(i, j, int(v), T)
            elif isinstance(v, (float, np.floating)):
                ws.write_number(i, j, float(v), P if (headers[j].lower().startswith('p ') or headers[j].lower().startswith('p(') or 'p-value' in headers[j].lower() or headers[j].lower().startswith('holm')) else N2)
            else: ws.write_string(i, j, str(v), T)
    for j, w in enumerate(widths): ws.set_column(j, j, w)
    ws.freeze_panes(r0 + 1, 0); ws.autofilter(r0, 0, r0 + len(rows), len(headers) - 1)
    return ws
def nice(b): return b.replace('_r34', ' (rows 34-68)').replace('_r71', ' (rows 71-98)').replace('_16h', ' (16 h)').replace('_72h', ' (72 h)').replace('_panel1', ' (first panel)').replace('_panel2', ' (second panel)')

# ---------------------------------------------------------------- README
ws = wb.add_worksheet('README'); ws.set_column(0, 0, 28); ws.set_column(1, 1, 120)
ws.write(0, 0, 'PSLN program - evidence tables behind the portfolio proposal (1 November 2026)', TITLE)
readme = [
 ('Purpose', 'Lets a reader trace every number quoted in PSLN_portfolio_proposal.docx back to workbook cells and to the calculation that produced it.'),
 ('Data analyzed', 'psln_program_dataset.xlsx (last saved 3 September 2026) and psln_program_annotation.pdf (15 September 2026). Nothing was relabeled, imputed or excluded as an outlier.'),
 ('Block IDs', 'As printed in the workbook (S01-A ... S15-O). Two labels are used twice on sheet S06; they are distinguished here by row range. Multi-panel blocks carry a suffix (for example S01-A (16 h)).'),
 ('Numbers_cited', 'Every number quoted in the proposal, in order of first appearance: value, meaning, source blocks, source cells, method, script.'),
 ('Survival', 'Every time-to-event block: animals, survivors, death days, exact 95% CI, and the count implied by the paired body-weight block.'),
 ('Survival_pooled', 'Pooled and stratified analyses, subsets and sensitivity analyses.'),
 ('Serology', 'Geometric mean titers with 95% CI for every titer block, and the contrasts between groups.'),
 ('Cellular_mechanism', 'Group means, contrasts PSLN-344 vs PSLN-212 in aged animals, multiplicity-adjusted p-values and percent of young benchmark.'),
 ('Gap_closed', 'The values plotted in Figure 3: share of the aged-to-young gap closed by PSLN-344, per readout.'),
 ('Interventions', 'Knock-out, inhibitor, antagonist and rescue experiments.'),
 ('Tolerability', 'Body weight after dosing (S08-D), lung cytokines (S09-A, back-transformed from log10), brain transcripts (S10-A).'),
 ('Integrity_log', 'The 20 discrepancies: evidence, why each matters, how it was handled here, what the audit should close.'),
 ('N_audit', 'Stated n against the number of values present, per block and group.'),
 ('Repeated_sequences', 'Body-weight trajectories that share three or more identical time-matched values with an animal in a different block or group.'),
 ('Sample_size', 'Power calculations behind the group sizes proposed for the next studies.'),
 ('Conventions', 'Titers and fold-changes are summarized as geometric means and compared on the log scale. HAI recorded as 0 was set to 5. Survival = event code 0 at end of observation. '
                 'Exact 95% CIs are Clopper-Pearson. p-values are two-sided and unadjusted unless the column says Holm.'),
 ('Reproducing', 'Scripts 01 to 16 in the folder "analysis" regenerate every table and figure from the two source files; see analysis/README.md.'),
]
for i, (a, b_) in enumerate(readme, 2):
    ws.write(i, 0, a, B_); ws.write(i, 1, b_, T)

# ---------------------------------------------------------------- Numbers_cited
rows = []
for i, k in enumerate(USED, 1):
    f = FACTS[k]
    rows.append([i, f['text'], f['what'], ', '.join(nice(b) for b in f['blocks']) if f['blocks'] else 'design calculation', f['cells'], f['method'], f['script'], k])
sheet('Numbers_cited', ['No.', 'Number as quoted', 'What it is', 'Source blocks', 'Source cells', 'How computed', 'Script', 'Registry key'], rows, [5, 26, 60, 40, 60, 60, 34, 22])

# ---------------------------------------------------------------- Survival
PAIR = {'S03-I': 'S13-F', 'S03-J': 'S13-G', 'S06-A': 'S15-A', 'S06-B': 'S15-B', 'S06-C': 'S15-C', 'S06-D': 'S15-D', 'S06-E_r34': 'S15-E', 'S06-F_r34': 'S15-F', 'S06-G': 'S15-G',
        'S06-E_r71': 'S15-J', 'S06-F_r71': 'S15-K', 'S09-B': 'S09-C', 'S09-D': 'S09-E', 'S09-F': 'S09-G', 'S15-H': 'S15-I', 'S15-L': 'S15-M', 'S15-N': 'S15-O', 'S13-E': None}
wv = {(r[0], r[2]): r for r in WV}
rows = []
for bid, b in B.items():
    if b['kind'] != 'survival': continue
    for g in b['order']:
        a = b['groups'][g]; n = len(a); s = sum(1 for x in a if x['event'] == 0); lo, hi = cp(s, n)
        dd = sorted(x['day'] for x in a if x['event'] == 1)
        pf = plr = None
        if g == 'PSLN-344' and 'PSLN-212' in b['groups']:
            s2, n2 = sn(bid, 'PSLN-212'); pf = float(stats.fisher_exact([[s, n - s], [s2, n2 - s2]])[1])
            pe = [r for r in SURV['per_experiment'] if r['block'] == bid]
            plr = float(pe[0]['logrank_344_v_212']) if pe else None
        w = wv.get((bid, g)); wtxt = None; flag = None
        if w:
            lo_s, hi_s = w[5] - w[7], w[5] - w[6]
            wtxt = f"{lo_s}/{w[5]}" if lo_s == hi_s else f"{lo_s} to {hi_s} of {w[5]}"; flag = 'agree' if w[8] == 'OK' else 'DIFFER'
        miss = sum(1 for x in a if x['day'] is None)
        rows.append([nice(bid), b.get('vaccine', ''), b.get('challenge', ''), b.get('challenge_day'), b.get('strain', ''), g, b['stated_n'], n, s, n - s, 100 * s / n, lo, hi, ', '.join(str(int(d)) for d in dd),
                     pf, plr, PAIR.get(bid) or '', wtxt, flag, b['cells'][g], ('one row has no day value' if miss else '')])
sheet('Survival', ['Block', 'Vaccine', 'Challenge', 'Challenge day after dose', 'Animals', 'Group as printed', 'Stated n', 'Rows', 'Alive at end', 'Died', '% alive', 'Exact 95% CI low', 'Exact 95% CI high', 'Days of death',
                   'p (Fisher) vs PSLN-212', 'p (exact log-rank) vs PSLN-212', 'Paired weight block', 'Alive per weight block', 'Survival vs weight table', 'Cells', 'Note'], rows,
      [16, 26, 24, 10, 22, 20, 7, 6, 7, 6, 8, 8, 8, 22, 11, 11, 10, 12, 10, 30, 20])

# ---------------------------------------------------------------- Survival_pooled
rows = []
def add_pool(label, ids, groups=('PSLN-344', 'PSLN-212', 'Sham', 'PSLN-212(Y)')):
    for g in groups:
        s = sum(sn(b, g)[0] for b in ids if g in G(b)); n = sum(sn(b, g)[1] for b in ids if g in G(b))
        if n:
            lo, hi = cp(s, n); rows.append([label, ', '.join(nice(b) for b in ids), g, s, n, 100 * s / n, lo, hi, ''])
add_pool('All 11 aged challenge experiments (Figure 1)', AGED11)
add_pool('Challenge 2-3 days after dosing', ['S03-J', 'S06-B', 'S06-D']); add_pool('Challenge 14 days after dosing', ['S03-I', 'S06-A', 'S06-C']); add_pool('Challenge 60 days after dosing', ['S06-E_r34', 'S06-F_r34', 'S06-G'])
add_pool('Mismatched-strain challenges, aged BALB/c', ['S06-A', 'S06-B', 'S06-C', 'S06-D', 'S06-E_r34', 'S06-F_r34', 'S06-G']); add_pool('C57BL/6 and Swiss Webster', ['S15-L', 'S15-N'])
add_pool('Strict subset (survival and weight tables agree for every arm; design fully recorded)', ['S06-A', 'S06-B', 'S06-F_r34'])
add_pool('Unchallenged age-matched animals, day-60 blocks', ['S06-E_r34', 'S06-F_r34', 'S06-G'], groups=('Untreated',))
add_pool('Young BALB/c, mismatched-strain challenges', ['S09-B', 'S09-D', 'S09-F'], groups=('PSLN-344Y', 'PSLN-212Y', 'Sham'))
add_pool('14-month animals with or without prior infection', ['S06-E_r71', 'S06-F_r71'], groups=('Naïve+PSLN-344', 'Imprinting+PSLN-344', 'Naïve+PSLN-212', 'Imprinting+PSLN-212'))
for name, key in [('Sensitivity: as printed, all 11', 'as printed, all 11 experiments'), ('Sensitivity: worst case for PSLN-344 (each survival/weight conflict resolved against it; S03-J PSLN-212 arm dropped)', 'worst case for PSLN-344 (every survival/weight conflict resolved against it; S03-J 212-arm dropped)'),
                  ('Sensitivity: as printed, excluding S03-I and S03-J', 'as printed, excluding the two label-conflicted blocks S03-I and S03-J'), ('Sensitivity: worst case and excluding S03-I, S03-J', 'worst case AND excluding S03-I, S03-J')]:
    d = SURV['pooled'][f'sens::{key}']
    for g, s, n in [('PSLN-344', d['s344'], d['n344']), ('PSLN-212', d['s212'], d['n212'])]:
        lo, hi = cp(s, n); rows.append([name, 'Figure 1 blocks and paired weight blocks', g, s, n, 100 * s / n, lo, hi, f"Fisher p (344 vs 212) = {d['p']:.1e}"])
d = SURV['pooled']
rows.append(['Stratified tests, PSLN-344 vs PSLN-212, 11 experiments', 'Figure 1 blocks', '', None, None, None, None, None,
             f"Mantel-Haenszel survival difference {d['MH_RD_344_minus_212']['rd']:.1f} points (95% CI {d['MH_RD_344_minus_212']['lo']:.1f} to {d['MH_RD_344_minus_212']['hi']:.1f}); "
             f"stratified log-rank Z = {d['stratified_logrank_344 vs 212']['Z']:.2f}, permutation p = {d['stratified_logrank_344 vs 212']['p_perm']:.1e} (200,000 within-experiment permutations)"])
rows.append(['Stratified tests, PSLN-344 aged vs PSLN-212 young, 10 experiments', 'Figure 1 blocks except S03-J', '', None, None, None, None, None,
             f"Mantel-Haenszel survival difference {d['MH_RD_344_minus_Y']['rd']:.1f} points (95% CI {d['MH_RD_344_minus_Y']['lo']:.1f} to {d['MH_RD_344_minus_Y']['hi']:.1f}); "
             f"stratified log-rank permutation p = {d['stratified_logrank_344 vs 212(Y)']['p_perm']:.1e}"])
sheet('Survival_pooled', ['Analysis', 'Blocks', 'Group', 'Alive', 'Animals', '% alive', 'Exact 95% CI low', 'Exact 95% CI high', 'Test / note'], rows, [58, 50, 20, 7, 8, 8, 9, 9, 90])

# ---------------------------------------------------------------- Serology
TITRE = ['S03-A', 'S03-E', 'S03-C', 'S03-G', 'S03-D', 'S03-H', 'S13-I', 'S13-J', 'S13-A', 'S13-B', 'S13-C', 'S13-D']
rows = []
for bid in TITRE:
    o = IMM[bid]
    for g, d in o['groups'].items():
        rows.append([bid, o['name'], 'group', g, d['n'], ', '.join(str(x) for x in d['raw']), d['gmt'], d['lo'], d['hi'], None, None, B[bid]['cells'][g]])
    for k, d in o.items():
        if k.startswith('GMR '):
            rows.append([bid, o['name'], 'contrast', k.replace('GMR ', ''), None, '', d['gmr'], d['lo'], d['hi'], d['p_welch'], d['p_mwu'], ''])
for virus, num, den in [('H1N1', 'S13-A', 'S13-B'), ('H3N2', 'S13-C', 'S13-D')]:
    o = IMM[f'IgG2a:IgG1 {virus}']
    for g in ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']:
        rows.append([f'{num}/{den}', f'IgG2a:IgG1 ratio {virus}, recomputed per animal from raw titers', 'group', g, 5, ', '.join(f'{x:.3f}' for x in o[g]['vals']), o[g]['gm'], None, None, None, None, f"{B[num]['cells'][g]} / {B[den]['cells'][g]}"])
    rows.append([f'{num}/{den}', f'IgG2a:IgG1 ratio {virus}', 'contrast', 'PSLN-344/PSLN-212', None, '', o['ratio_344_212']['est'], o['ratio_344_212']['lo'], o['ratio_344_212']['hi'], o['ratio_344_212']['p'], None, ''])
    pr = 'S03-B' if virus == 'H1N1' else 'S03-F'
    for g in B[pr]['order']:
        rows.append([pr, f'IgG2a:IgG1 ratio {virus} AS PRINTED (column labels rotated; not used)', 'group', g + ' (printed header)', 5, ', '.join(f'{x:.3f}' for x in G(pr)[g]), gm(G(pr)[g]), None, None, None, None, B[pr]['cells'][g]])
sheet('Serology', ['Block', 'Measure', 'Row type', 'Group or contrast', 'n', 'Individual values', 'GMT or ratio', '95% CI low', '95% CI high', 'p (Welch, log scale)', 'p (exact Mann-Whitney)', 'Cells'], rows,
      [12, 46, 9, 26, 4, 40, 12, 10, 10, 12, 12, 22], note='GMT = geometric mean titer. Contrast rows give the ratio of geometric means (first group / second group).')

# ---------------------------------------------------------------- Cellular_mechanism
R = {r[0]: r for r in json.load(open('/tmp/work/parsed/restoration.json'))}
holm = IMM['holm_344_v_212']
rows = []
for bid, o in IMM.items():
    if not isinstance(o, dict) or 'groups' not in o or bid in TITRE: continue
    if bid not in B or B[bid]['kind'] not in ('columns', 'rows'): continue
    if 'diff_344_212' not in o: continue
    g = o['groups']
    def mget(k, f): return g[k][f] if k in g else None
    rows.append([nice(bid), o['name'], mget('Sham', 'mean'), mget('Sham', 'sd'), mget('PSLN-212', 'mean'), mget('PSLN-212', 'sd'), mget('PSLN-344', 'mean'), mget('PSLN-344', 'sd'), mget('PSLN-212(Y)', 'mean'), mget('PSLN-212(Y)', 'sd'),
                 g['PSLN-344']['n'], o['diff_344_212'], o['lo'], o['hi'], o['p_welch'], o['p_mwu'], holm.get(bid), o['pct_of_young'],
                 '; '.join(f"{k}: {v}" for k, v in B[bid]['cells'].items() if k in ('PSLN-212', 'PSLN-344', 'PSLN-212(Y)'))])
sheet('Cellular_mechanism', ['Block', 'Readout', 'Sham mean', 'Sham SD', 'PSLN-212 aged mean', 'SD', 'PSLN-344 aged mean', 'SD', 'PSLN-212 young mean', 'SD', 'n per group', 'Difference 344 - 212', '95% CI low', '95% CI high',
                             'p (Welch)', 'p (exact Mann-Whitney)', 'Holm-adjusted p (family of 37)', 'PSLN-344 as % of young', 'Cells'], rows, [12, 44, 8, 7, 9, 7, 9, 7, 9, 7, 6, 10, 9, 9, 10, 10, 11, 10, 60],
      note='Percentages from flow cytometry unless the readout says otherwise. The Holm family is the 37 PSLN-344 vs PSLN-212 contrasts in aged animals (these rows plus the titer blocks).')
ws = wb.add_worksheet('Gap_closed')
for j, h in enumerate(['Readout [block]', 'PSLN-212 aged', 'PSLN-344 aged', 'PSLN-212 young', 'Gap closed (%)']): ws.write(0, j, h, H)
for i, r in enumerate(json.load(open('/tmp/work/parsed/restoration.json')), 1):
    ws.write_string(i, 0, r[0], T)
    for j in (1, 2, 3): ws.write_number(i, j, r[j], N2)
    ws.write_number(i, 4, r[4], N1)
ws.set_column(0, 0, 58); ws.set_column(1, 4, 16)
ws.write(27, 0, 'Gap closed = (PSLN-344 aged - PSLN-212 aged) / (PSLN-212 young - PSLN-212 aged); log scale for titers, ratios and fold-changes; linear for percentages. Values are those plotted in Figure 3.', T)

# ---------------------------------------------------------------- Interventions
rows = []
for k, o in IMM.items():
    if '::' in k:
        bid, rest = k.split('::'); a, b_ = rest.split(' vs ')
        rows.append([nice(bid), o['label'], a, o['a'], b_, o['b'], o['est'], o['lo'], o['hi'], o['p'], o['p_mwu'], f"{o['n'][0]}, {o['n'][1]}"])
rows.append(['S07-C', 'macrophage transfer -> lung regulatory T cells; BOTH ARMS CARRY THE SAME PRINTED LABEL, direction cannot be assigned', 'column B', IMM['S07-C']['colB'], 'column C', IMM['S07-C']['colC'], IMM['S07-C']['colB'] - IMM['S07-C']['colC'], None, None, IMM['S07-C']['p'], None, '5, 5'])
sheet('Interventions', ['Block', 'What the experiment tests', 'Arm 1', 'Mean 1', 'Arm 2', 'Mean 2', 'Difference', '95% CI low', '95% CI high', 'p (Welch)', 'p (exact Mann-Whitney)', 'n'], rows, [12, 70, 22, 8, 26, 8, 10, 9, 9, 10, 10, 7])

# ---------------------------------------------------------------- Tolerability
ws = wb.add_worksheet('Tolerability'); ws.set_column(0, 0, 34); ws.set_column(1, 12, 13)
ws.write(0, 0, 'S08-D  Body weight after dosing, no challenge (% of day 0; mean of animals with a value)', B_)
days = B['S08-D']['times']
for j, h in enumerate(['Group'] + [f'day {d}' for d in days] + ['n on day 10', 'animals < 95%', 'animals < 90%']): ws.write(1, j, h, H)
for i, g in enumerate(B['S08-D']['order'], 2):
    d = SAF['S08-D'][g]; ws.write_string(i, 0, g, T)
    for j, t in enumerate(days, 1): ws.write_number(i, j, d['mean_by_day'][t], N1)
    ws.write_number(i, len(days) + 1, d['n_by_day']['10'], T); ws.write_string(i, len(days) + 2, f"{d['animals_below_95']}/5", T); ws.write_string(i, len(days) + 3, f"{d['animals_below_90']}/5", T)
r0 = 10
for pid, lab in [('S09-A_panel1', 'S09-A first panel (columns A-U): lung transcripts 16 h after adjuvant alone, fold vs untreated (10^mean log10, n = 3)'),
                 ('S09-A_panel2', 'S09-A second panel (columns X-AS): printed "16h"; Ifnb1 matches the 72 h data of S01-A (see Integrity_log D5)')]:
    ws.write(r0, 0, lab, B_); grp = B[pid]['order']
    for j, h in enumerate(['Transcript'] + grp): ws.write(r0 + 1, j, h, H)
    for i, an in enumerate(B[pid]['analytes'], r0 + 2):
        ws.write_string(i, 0, an, T)
        for j, g in enumerate(grp, 1): ws.write_number(i, j, SAF[pid][an][g], N1)
    r0 += 11
ws.write(r0, 0, 'S10-A  Brain transcripts 36 h after intranasal dosing (fold vs untreated, n = 5)', B_)
for j, h in enumerate(['Transcript', 'Buffer mean', 'Vaccine + empty liposome mean', 'Vaccine + PSLN-344 mean', 'Vaccine + cholera toxin mean', 'PSLN-344 / buffer', '95% CI low', '95% CI high', 'p', 'PSLN-344 / empty liposome', 'p', 'cholera toxin / buffer', 'p']): ws.write(r0 + 1, j, h, H)
for i, an in enumerate(['Ifnb1', 'Tnf', 'Isg15'], r0 + 2):
    d = SAF[f'S10-A_{an}']; ws.write_string(i, 0, an, T)
    for j, k in enumerate(['PBS', 'Sham', 'PSLN-344', 'CT'], 1): ws.write_number(i, j, d['means'][k], N2)
    for j, v in enumerate(list(d['r344_pbs'][:3]), 5): ws.write_number(i, j, v, N2)
    ws.write_number(i, 8, d['r344_pbs'][3], P); ws.write_number(i, 9, d['r344_sham'][0], N2); ws.write_number(i, 10, d['r344_sham'][1], P); ws.write_number(i, 11, d['rCT_pbs'][0], N2); ws.write_number(i, 12, d['rCT_pbs'][1], P)

# ---------------------------------------------------------------- Integrity_log
rows = [[e['id'], e['rank'], e['blocks'], e['title'], e['finding'], e['face'], e['handling'], e['audit']] for e in LOG]
ws = sheet('Integrity_log', ['ID', 'Rank', 'Blocks', 'Discrepancy', 'Evidence', 'Why it matters', 'How handled in this analysis', 'What the audit should close'], rows, [5, 8, 26, 38, 90, 60, 60, 46])
r = len(rows) + 3
ws.write(r, 3, 'Limits of the dataset that are not errors', B_)
for i, x in enumerate(DESIGN_LIMITS, r + 1): ws.write(i, 3, x, T)

# ---------------------------------------------------------------- N_audit
rows = list(csv.reader(open('/tmp/work/parsed/n_audit.csv')))[1:]
rows2 = []
for b_, g, sn_, obs in rows:
    nums = [int(x) for x in __import__('re').findall(r'^\d+|(?<=/)\d+', obs)] if obs else []
    first = int(__import__('re').match(r'\d+', obs).group(0))
    flag = '' if str(first) == str(sn_) else 'stated n differs from values present'
    if 'MISSING' in obs: flag = (flag + '; ' if flag else '') + 'row without a day value'
    rows2.append([nice(b_), g, int(sn_) if sn_ not in ('', 'None') else None, obs, flag])
sheet('N_audit', ['Block', 'Group as printed', 'Stated n', 'Values present (per time point where applicable)', 'Flag'], rows2, [22, 28, 9, 50, 40],
      note='For time-course and body-weight blocks the counts are per time point; counts that fall over time in body-weight blocks reflect animals leaving the study (blank cells).')

# ---------------------------------------------------------------- Repeated_sequences
Wb = [k for k, b in B.items() if b['kind'] == 'wide_time' and 'body weight' in b.get('measurand', '')]
animals = {}
for bid in Wb:
    b = B[bid]
    for g in b['order']:
        n = len(b['groups'][g][b['times'][0]])
        for i in range(n): animals[(bid, g, i)] = {int(float(t)): b['groups'][g][t][i] for t in b['times']}
def informative(tr):
    out = {}; prev = None
    for d in sorted(tr):
        v = tr[d]
        if d == 0 or v is None: prev = v; continue
        if v == prev: continue
        out[d] = v; prev = v
    return out
inf = {k: informative(v) for k, v in animals.items()}
rows = []
for a, b_ in itertools.combinations(list(inf), 2):
    if a[:2] == b_[:2]: continue
    same = [d for d in inf[a] if d in inf[b_] and inf[a][d] == inf[b_][d]]
    if len(same) >= 3:
        rows.append([a[0], a[1], a[2] + 1, b_[0], b_[1], b_[2] + 1, len(same), min(len(inf[a]), len(inf[b_])), ', '.join(str(d) for d in same), ', '.join(str(inf[a][d]) for d in same)])
rows.sort(key=lambda r: (-r[6], r[0]))
sheet('Repeated_sequences', ['Block 1', 'Group 1', 'Animal (column position)', 'Block 2', 'Group 2', 'Animal (column position)', 'Identical time-matched values', 'Informative values available', 'Days', 'Values'], rows, [9, 22, 10, 9, 22, 10, 10, 10, 24, 60],
      note='Body-weight blocks only. Day 0 (always 100) and carried-forward repeats within an animal are ignored. Also: S11-A and S11-B share 35 of 100 cells (see Integrity_log D7).')

# ---------------------------------------------------------------- Sample_size
rows = []
for k, v in BIO['power'].items():
    if isinstance(v, dict) and 'n80' in v: rows.append(['Survival, two-sided Fisher exact, alpha 0.05', k, v['n80'], v['n90']])
for k in ['HAI superiority, detect 4-fold GMR', 'HAI superiority, detect 3-fold GMR', 'HAI superiority, detect 2-fold GMR']:
    rows.append([f"HAI titer, t-test on log2, SD {BIO['power']['sd_hai_log2']:.2f}", k.replace('HAI superiority, d', 'D'), None, BIO['power'][f'HAI {k.replace("HAI ", "")}']['n']])
rows.append(['HAI non-inferiority, margin ratio 0.5, one-sided 0.025', 'true ratio 0.87', None, BIO['power']['NI true 0.87']]); rows.append(['HAI non-inferiority, margin ratio 0.5, one-sided 0.025', 'true ratio 0.76', None, BIO['power']['NI true 0.76']])
rows.append(['Existing design, 7 per arm', 'power for 85% vs 14% survival', None, None]); rows[-1][2] = f"{100*BIO['power']['existing_n7_85v14']:.0f}% power"
rows.append(['Existing design, 7 per arm', 'power for 85% vs 50% survival', f"{100*BIO['power']['existing_n7_85v50']:.0f}% power", None])
rows.append(['Proposed design, 17 per arm', 'power for 78% vs 19% survival', FACTS['power_n17_rep']['text'] + ' power', None]); rows.append(['Proposed design, 17 per arm', 'power for 85% vs 40% survival', FACTS['power_n17_attr']['text'] + ' power', None])
sheet('Sample_size', ['Endpoint and test', 'Scenario', 'n per arm for 80% power (or power)', 'n per arm for 90% power'], rows, [52, 70, 20, 16])
wb.close()
print('written', OUT)
