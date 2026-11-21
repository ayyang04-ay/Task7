"""spotcheck_direct_cells.py - reads headline cells straight from the workbook, without the parser,
and prints the same summary numbers that the proposal quotes (survivors per arm, HAI geometric means, Ifnb1, IgG2a:IgG1)."""
import openpyxl, numpy as np
wb = openpyxl.load_workbook('/tmp/world/filesystem/psln_program_dataset.xlsx', data_only=True)
def col(ws, c, r0, r1): return [ws[f'{c}{r}'].value for r in range(r0, r1 + 1)]
gm = lambda v: float(np.exp(np.mean(np.log(v))))
def surv(ws, c, r0, r1):
    v = [x for x in col(ws, c, r0, r1) if x is not None]; return f"{v.count(0)}/{len(v)}"
s3, s6, s15, s1, s13 = wb['S03'], wb['S06'], wb['S15'], wb['S01'], wb['S13']
print('Survivors / animals (event code 0 / rows), groups as printed')
for name, ws, hr, cols, r0, r1 in [('S03-I', s3, 16, 'BCDEF', 17, 51), ('S03-J', s3, 16, 'HIJ', 17, 51), ('S06-A', s6, 2, 'BCDE', 3, 30), ('S06-B', s6, 2, 'HIJK', 3, 30), ('S06-C', s6, 2, 'NOPQ', 3, 30),
                                   ('S06-D', s6, 33, 'BCDE', 34, 68), ('S06-E rows 34-68', s6, 33, 'HIJKL', 34, 68), ('S06-F rows 34-68', s6, 33, 'NOPQR', 34, 68), ('S06-G', s6, 70, 'BCDEF', 71, 105),
                                   ('S06-E rows 71-98', s6, 70, 'HIJK', 71, 105), ('S06-F rows 71-98', s6, 70, 'NOPQ', 71, 105), ('S15-H', s15, 72, 'BCD', 73, 100), ('S15-L', s15, 102, 'BCDE', 103, 131), ('S15-N', s15, 133, 'BCDE', 134, 161)]:
    print(f"  {name:<18}", ', '.join(f"{ws[f'{c}{hr}'].value}: {surv(ws, c, r0, r1)}" for c in cols))
print('HAI geometric mean titers, day 14 (columns M, N, O = PSLN-212, PSLN-344, PSLN-212(Y))')
print('  H1N1 [S03-C]:', [round(gm(col(s3, c, 3, 7))) for c in 'MNO'], ' H3N2 [S03-G]:', [round(gm(col(s3, c, 10, 14))) for c in 'MNO'])
print('Ifnb1 fold, geometric mean [S01-A], 16 h | 72 h')
for r in range(3, 11):
    print(f"  {s1[f'A{r}'].value:<14} {gm([s1[f'{c}{r}'].value for c in 'BCDEF']):5.1f} | {gm([s1[f'{c}{r}'].value for c in 'HIJKL']):4.1f}")
print('IgG2a:IgG1, H1N1, recomputed per animal from S13-A / S13-B, and as printed in S03-B')
for g, a, b in [('PSLN-212', 'A', 'E'), ('PSLN-344', 'B', 'F'), ('PSLN-212(Y)', 'C', 'G')]:
    print(f"  {g:<12} raw headers {s13[f'{a}2'].value} / {s13[f'{b}2'].value}: {gm([x / y for x, y in zip(col(s13, a, 3, 7), col(s13, b, 3, 7))]):.2f}")
print('  S03-B printed headers', [s3[f'{c}2'].value for c in 'GHI'], '->', [round(gm(col(s3, c, 3, 7)), 2) for c in 'GHI'])
