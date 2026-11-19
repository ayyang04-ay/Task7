#!/usr/bin/env python
"""
12_independent_check.py -- independent re-derivation of headline numbers straight from workbook cells
(no use of the parsed CSVs or of scripts 02-11). Run: micromamba run -n chem python 12_independent_check.py
"""
import openpyxl, math, json, os
from statistics import mean
wb = openpyxl.load_workbook('/tmp/world/filesystem/psln_program_dataset.xlsx')
HERE = os.path.dirname(os.path.abspath(__file__))
N = json.load(open(os.path.join(HERE, 'tables', 'T10_numbers_cited.json')))
def col(ws, c, r0, r1): return [ws[f'{c}{r}'].value for r in range(r0, r1 + 1) if ws[f'{c}{r}'].value is not None]
def surv(sheet, c, r0, r1):
    v = col(wb[sheet], c, r0, r1); return v.count(0), len(v)
def gmean(v): return 10 ** mean(math.log10(x) for x in v)
ok = True
def check(name, got, expect):
    global ok
    flag = 'OK ' if str(got) == str(expect) else 'MISMATCH'
    if flag != 'OK ': ok = False
    print(f'{flag} {name:58s} independent={got}   proposal={expect}')

# pooled early survival: S03-I (E=344, B=sham, D=212), S03-J (J,H,I), S06-A (D,B,C), S06-B (J,H,I), S06-C (P,N,O), S06-D (D,B,C rows 34-61)
blocks = [('S03', 'E', 'B', 'D', 17, 51), ('S03', 'J', 'H', 'I', 17, 46), ('S06', 'D', 'B', 'C', 3, 30), ('S06', 'J', 'H', 'I', 3, 30), ('S06', 'P', 'N', 'O', 3, 30), ('S06', 'D', 'B', 'C', 34, 61)]
tot = {'344': [0, 0], 'sham': [0, 0], '212': [0, 0]}
for sh, c344, cs, c212, r0, r1 in blocks:
    for k, c in [('344', c344), ('sham', cs), ('212', c212)]:
        s, n = surv(sh, c, r0, r1); tot[k][0] += s; tot[k][1] += n
check('pooled d2-14 survival PSLN-344', f"{tot['344'][0]}/{tot['344'][1]}", N['early_344'])
check('pooled d2-14 survival Sham', f"{tot['sham'][0]}/{tot['sham'][1]}", N['early_sham'])
check('pooled d2-14 survival PSLN-212', f"{tot['212'][0]}/{tot['212'][1]}", N['early_212'])
d60 = [('S06', 'J', 'H', 'I', 'L', 34, 68), ('S06', 'P', 'N', 'O', 'R', 34, 68), ('S06', 'D', 'B', 'C', 'F', 71, 105)]
t = {'344': [0, 0], 'sham': [0, 0], '212': [0, 0], 'unt': [0, 0]}
for sh, c344, cs, c212, cu, r0, r1 in d60:
    for k, c in [('344', c344), ('sham', cs), ('212', c212), ('unt', cu)]:
        s, n = surv(sh, c, r0, r1); t[k][0] += s; t[k][1] += n
check('d60 survival PSLN-344', f"{t['344'][0]}/{t['344'][1]}", N['d60_344']); check('d60 survival PSLN-212', f"{t['212'][0]}/{t['212'][1]}", N['d60_212'])
check('d60 unchallenged untreated survivors', f"{t['unt'][0]}/{t['unt'][1]}", N['d60_unt']); check('d60 unchallenged deaths', f"{t['unt'][1]-t['unt'][0]}/{t['unt'][1]}", N['bg_deaths'])
check('S15-H vaccine+344 / 344 alone / vaccine alone', '%d/%d %d/%d %d/%d' % (*surv('S15', 'D', 73, 93), *surv('S15', 'C', 73, 93), *surv('S15', 'B', 73, 93)), f"{N['h_combo']} {N['h_adj']} {N['h_vac']}")
s1 = [surv('S15', 'D', 103, 130), surv('S15', 'D', 134, 161)]; check('aged C57BL/6 + Swiss Webster PSLN-344', f'{s1[0][0]+s1[1][0]}/{s1[0][1]+s1[1][1]}', N['str_344'])
imp = [surv('S06', c, 71, 98) for c in 'JKPQ']; check('14-month mice PSLN-344 (4 arms)', f'{sum(a for a, _ in imp)}/{sum(b for _, b in imp)}', N['imp_344'])
imp = [surv('S06', c, 71, 98) for c in 'HINO']; check('14-month mice PSLN-212 (4 arms)', f'{sum(a for a, _ in imp)}/{sum(b for _, b in imp)}', N['imp_212'])
ws = wb['S03']
hai = lambda c, r0, r1: [x if x > 0 else 5 for x in col(ws, c, r0, r1)]
check('HAI GMT H1N1 aged 344', f"{gmean(hai('N', 3, 7)):,.0f}", N['hai1_344']); check('HAI GMT H1N1 aged 212', f"{gmean(hai('M', 3, 7)):,.0f}", N['hai1_212'])
check('HAI GMT H3N2 aged 344', f"{gmean(hai('N', 10, 14)):,.0f}", N['hai3_344']); check('HAI GMT H3N2 aged 212', f"{gmean(hai('M', 10, 14)):,.0f}", N['hai3_212'])
check('IgG GMT H1N1 aged 344', f"{gmean(col(ws, 'D', 3, 7)):,.0f}", N['igg1_344']); check('neutralising GMT H1N1 aged 344', f"{gmean(col(ws, 'T', 3, 7)):,.0f}", N['nt1_344'])
w13 = wb['S13']; ratio = lambda a, b: mean(x / y for x, y in zip(col(w13, a, 3, 7), col(w13, b, 3, 7)))
check('IgG2a:IgG1 recomputed aged 344 (S13-A col B / S13-B col F)', f"{ratio('B', 'F'):.1f}", N['ratio1_344']); check('IgG2a:IgG1 recomputed aged 212', f"{ratio('A', 'E'):.1f}", N['ratio1_212'])
check('IgG2a:IgG1 S03-B as printed under PSLN-344', f"{mean(col(ws, 'H', 3, 7)):.1f}", N['ratio1_printed_344'])
w1 = wb['S01']; row = lambda r, c0, c1: [w1.cell(r, c).value for c in range(c0, c1 + 1)]
check('Ifnb1 16h geometric mean aged 344', f"{gmean(row(8, 2, 6)):.0f}", N['ifn_344']); check('Ifnb1 16h geometric mean aged 212', f"{gmean(row(5, 2, 6)):.0f}", N['ifn_212'])
check('Ifnb1 16h geometric mean young 212', f"{gmean(row(9, 2, 6)):.0f}", N['ifn_y'])
w2 = wb['S02']; check('Gm-csf 36h geometric mean 344', f"{gmean([w2.cell(18, c).value for c in range(2, 7)]):.1f}", N['gm_344_36h'])
check('S02-H Ifnar-null w/o cDC mean', f"{mean(col(w2, 'D', 30, 34)):.1f}", N['h_ko']); check('S02-H WT w/o cDC mean', f"{mean(col(w2, 'B', 30, 34)):.1f}", N['h_wt'])
w10 = wb['S10']; check('CNS Tnf PSLN-344 / PBS', f"{mean(col(w10, 'H', 3, 7)) / mean(col(w10, 'F', 3, 7)):.2f}", N['cns_Tnf'])
w8 = wb['S08']
def nadir(c0):
    out = []
    for c in range(c0, c0 + 5):
        v = [w8.cell(r, c).value for r in range(22, 27) if w8.cell(r, c).value is not None]; out.append(min(v))
    return out
check('S08-D mean max weight loss PSLN-344 (cols Q-U)', f"{100 - mean(nadir(17)):.1f}", N['wl_344']); check('S08-D mean max weight loss vaccine (cols AA-AE)', f"{100 - mean(nadir(27)):.1f}", N['wl_vac'])
check('S08-D mean max weight loss PSLN-212/R848 (cols V-Z)', f"{100 - mean(nadir(22)):.1f}", N['wl_combo'])
w9 = wb['S09']; tn = [w9.cell(8, c).value for c in range(40, 43)]; check('S09-A 2nd panel Tnf PSLN-344 geometric fold (cols AN-AP)', f"{10 ** mean(tn):.1f}", N['cy72_Tnf_344'])
w11 = wb['S11']; same = sum(1 for r in range(3, 8) for c in range(2, 22) if w11.cell(r, c).value == w11.cell(r + 7, c).value); check('S11-A vs S11-B identical cells', same, N['s11_same'])
print('\nALL CHECKS PASSED' if ok else '\nSOME CHECKS FAILED')
