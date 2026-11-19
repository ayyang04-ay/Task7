"""Re-runnable specific integrity checks; writes integrity_checks.csv."""
import openpyxl, math, pandas as pd, numpy as np
from blocks import XLSX
wb = openpyxl.load_workbook(XLSX, data_only=True)
rows = []
def add(i, check, result, detail):
    rows.append(dict(id=i, check=check, result=result, detail=detail))
ws = wb['S06']
c = [tuple(ws[f'{col}{r}'].value for col in 'MNOPQ') for r in range(3, 31)]
d = [tuple(ws[f'{col}{r}'].value for col in 'ABCDE') for r in range(34, 62)]
add('C2', 'S06-C (S06!M3:Q30) identical to S06-D (S06!A34:E61)', c == d, f'{sum(x == y for x, y in zip(c, d))}/28 rows identical across days + 4 group columns')
ws = wb['S09']
a = [ws.cell(row=18, column=k).value for k in range(7, 15)]; b = [ws.cell(row=18, column=k).value for k in range(23, 31)]
add('C4', 'S09-C day-12 PSLN-212Y (G18:N18) vs PSLN-344Y (W18:AD18)', a == b, f'{a} vs {b}')
s1 = wb['S01']; s8 = wb['S08']
v1 = [s1[f'{k}14'].value for k in 'BCDEF']; v2 = [s8[f'A{r}'].value for r in range(14, 19)]
v3 = [s1[f'{k}15'].value for k in 'BCDEF']; v4 = [s8[f'B{r}'].value for r in range(14, 19)]
add('C5', 'S01-B AECII/PSLN-SRB (S01!B14:F14) vs S08-C AECII-PSLN-SRB (S08!A14:A18)', len(set(v1) & set(v2)), f'shared values {sorted(set(v1) & set(v2))}')
add('C5', 'S01-B AECI/PSLN-SRB (S01!B15:F15) vs S08-C AECII-PSLN-344-SRB (S08!B14:B18)', len(set(v3) & set(v4)), f'shared values {sorted(set(v3) & set(v4))}')
# S09-A panel 2 vs S01-A 72h, PBS vs Sham
grp1 = {'PBS': 3, 'CMP-204': 4, 'PSLN-212': 5, 'PSLN-R848': 6, 'PSLN-212/R848': 7, 'PSLN-344': 8, 'PSLN-212(Y)': 9}
p2cols = {'PBS': ['Y', 'Z', 'AA'], 'CMP-204': ['AB', 'AC', 'AD'], 'PSLN-212': ['AE', 'AF', 'AG'], 'PSLN-R848': ['AH', 'AI', 'AJ'], 'PSLN-212/R848': ['AK', 'AL', 'AM'], 'PSLN-344': ['AN', 'AO', 'AP'], 'PSLN-212(Y)': ['AQ', 'AR', 'AS']}
p1cols = {'PBS': ['B', 'C', 'D'], 'CMP-204': ['E', 'F', 'G'], 'PSLN-212': ['H', 'I', 'J'], 'PSLN-R848': ['K', 'L', 'M'], 'PSLN-212/R848': ['N', 'O', 'P'], 'PSLN-344': ['Q', 'R', 'S'], 'PSLN-212(Y)': ['T', 'U', 'V']}
m72 = m16 = 0; tot = 0
for gname, r in grp1.items():
    a72 = [s1[f'{k}{r}'].value for k in 'HIJKL']; a16 = [s1[f'{k}{r}'].value for k in 'BCDEF']
    for col in p2cols[gname]:
        x = 10 ** ws[f'{col}3'].value; tot += 1
        m72 += any(abs(x - y) <= 0.011 for y in a72)
    for col in p1cols[gname]:
        x = 10 ** ws[f'{col}3'].value
        m16 += any(abs(x - y) <= 0.011 for y in a16)
add('M2', 'S09-A panel 2 Ifnb1 (S09!Y3:AS3) matches S01-A 72 h (S01!H3:L10)', f'{m72}/{tot}', 'tolerance 0.011 after 10^x')
add('M2', 'S09-A panel 1 Ifnb1 (S09!B3:V3) matches S01-A 16 h (S01!B3:F10); "PBS" compared with S01-A "Sham"', f'{m16}/{tot}', 'tolerance 0.011 after 10^x')
# S04-B derived
s4 = wb['S04']
f = [[s4.cell(row=r, column=k).value for r in range(8, 13)] for k in range(1, 5)]
q = [[s4.cell(row=r, column=k).value for r in range(15, 20)] for k in range(1, 5)]
ok = all(abs(qq - (100 - ff) / ff) < 1e-4 for fc, qc in zip(f, q) for ff, qq in zip(fc, qc))
add('m5', 'S04-B Tfh:Tfr (S04!A15:D19) equals (100-Foxp3%)/Foxp3% from S04!A8:D12', ok, '20/20 animals')
# n mismatches
s3 = wb['S03']
nJ = {g: sum(1 for r in range(17, 47) if s3.cell(row=r, column=k).value is not None) for g, k in [('Sham', 8), ('PSLN-212', 9), ('PSLN-344', 10)]}
add('m1', 'S03-J stated n (S03!G15 "n=9") vs observed per group', str(nJ), f'S03!G46 day value missing: {s3["G46"].value is None}')
s13 = wb['S13']
nE = {g: sum(1 for r in range(3, 31) if s13.cell(row=r, column=k).value is not None) for g, k in [('Naive', 19), ('Sham', 20), ('CMP-204(Y)', 21), ('PSLN-344(Y)', 22)]}
add('m1', 'S13-E stated n (S13!R1 "n=5") vs observed per group', str(nE), '')
s9 = wb['S09']
nB = sum(1 for r in range(12, 36) if s9[f'B{r}'].value is not None); nF = sum(1 for r in range(66, 89) if s9[f'B{r}'].value is not None)
add('m1', 'Sham records: S09-B (annotation says 7) and S09-F (annotation says 8)', f'S09-B={nB}, S09-F={nF}', '')
s5 = wb['S05']
add('m1', 'S05-A/B stated n=3 vs observations per group per day', '2', 'two value columns per group (e.g. S05!B3:C3)')
# untreated sentinel deaths
ws = wb['S06']
u = {'S06-E': [(ws[f'G{r}'].value, ws[f'L{r}'].value) for r in range(62, 69)], 'S06-F': [(ws[f'M{r}'].value, ws[f'R{r}'].value) for r in range(62, 69)], 'S06-G': [(ws[f'A{r}'].value, ws[f'F{r}'].value) for r in range(99, 106)]}
add('M5', 'Unchallenged aged sentinel deaths (S06!L62:L68, R62:R68, F99:F105)', sum(e for v in u.values() for _, e in v), str({k: [dd for dd, e in v if e == 1] for k, v in u.items()}))
# S07-C labels
s7 = wb['S07']
add('M6', 'S07-C group labels (S07!B15, C15)', s7['B15'].value == s7['C15'].value, f"{s7['B15'].value!r} / {s7['C15'].value!r}")
# S08 orphan region
s8 = wb['S08']
add('M7', 'S08 rows 89-101 content', 'unlabelled', str([(r, s8[f'A{r}'].value, s8[f'C{r}'].value, s8[f'D{r}'].value) for r in range(89, 102)]))
T = pd.DataFrame(rows); T.to_csv('integrity_checks.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 90)
print(T.to_string(index=False))
