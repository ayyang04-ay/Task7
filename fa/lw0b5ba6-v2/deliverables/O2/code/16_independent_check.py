"""16_independent_check.py -- recompute headline numbers directly from raw cells (no tidy pipeline) + alternative Cox implementation."""
import openpyxl, numpy as np
wb = openpyxl.load_workbook('/tmp/world/filesystem/psln_program_dataset.xlsx', data_only=True)
def col(ws, c, r0, r1): return [ws[f"{c}{r}"].value for r in range(r0, r1+1)]
def rowv(ws, r, cols): return [ws[f"{c}{r}"].value for c in cols]
# 1. survival counts straight from cells: (sheet, daycol, groupcol, r0, r1)
spec = {'S03-I': ('S03', {'PSLN-344': 'E', 'PSLN-212': 'D', 'Sham': 'B'}, 17, 51), 'S03-J': ('S03', {'PSLN-344': 'J', 'PSLN-212': 'I', 'Sham': 'H'}, 17, 46),
        'S06-A': ('S06', {'PSLN-344': 'D', 'PSLN-212': 'C', 'Sham': 'B'}, 3, 30), 'S06-B': ('S06', {'PSLN-344': 'J', 'PSLN-212': 'I', 'Sham': 'H'}, 3, 30),
        'S06-C': ('S06', {'PSLN-344': 'P', 'PSLN-212': 'O', 'Sham': 'N'}, 3, 30), 'S06-E(d60)': ('S06', {'PSLN-344': 'J', 'PSLN-212': 'I', 'Sham': 'H'}, 34, 68),
        'S06-F(d60)': ('S06', {'PSLN-344': 'P', 'PSLN-212': 'O', 'Sham': 'N'}, 34, 68), 'S06-G(d60)': ('S06', {'PSLN-344': 'D', 'PSLN-212': 'C', 'Sham': 'B'}, 71, 105)}
tot = {}
for blk, (sh, cols, r0, r1) in spec.items():
    ws = wb[sh]
    for g, c in cols.items():
        v = [x for x in col(ws, c, r0, r1) if x is not None]
        n, dead = len(v), sum(v); tot.setdefault(g, [0, 0]); tot[g][0] += n - dead; tot[g][1] += n
print('raw-cell pooled survivors/n:', tot)
# 2. Ifnb1 16 h geometric means (S01 rows 5,8,9 cols B-F)
ws = wb['S01']
gm = lambda v: float(np.exp(np.mean(np.log(v))))
for lab, r in [('PSLN-212', 5), ('PSLN-344', 8), ('PSLN-212(Y)', 9), ('CMP-204', 4)]:
    print('Ifnb1 16h', lab, round(gm(rowv(ws, r, 'BCDEF')), 2))
# 3. HAI GMT (S03 cols M,N,O rows 3-7 CA09; rows 10-14 Aichi)
ws = wb['S03']
for lab, c in [('PSLN-212', 'M'), ('PSLN-344', 'N'), ('PSLN-212(Y)', 'O')]:
    print('HAI CA09', lab, round(gm(col(ws, c, 3, 7)), 1), '| Aichi', round(gm(col(ws, c, 10, 14)), 1))
# 4. alternative Cox (statsmodels PHReg, stratified) on raw-cell data
import pandas as pd
from statsmodels.duration.hazard_regression import PHReg
rows = []
for blk, (sh, cols, r0, r1) in spec.items():
    ws = wb[sh]; dcol = {'S03-I': 'A', 'S03-J': 'G', 'S06-A': 'A', 'S06-B': 'G', 'S06-C': 'M', 'S06-E(d60)': 'G', 'S06-F(d60)': 'M', 'S06-G(d60)': 'A'}[blk]
    for g in ['PSLN-344', 'PSLN-212']:
        for r in range(r0, r1+1):
            e = ws[f"{cols[g]}{r}"].value
            if e is None: continue
            t = ws[f"{dcol}{r}"].value; t = 21 if t is None else t
            rows.append(dict(block=blk, trt=int(g == 'PSLN-344'), time=float(t), event=int(e)))
d = pd.DataFrame(rows)
m = PHReg(d.time, d[['trt']], status=d.event, strata=d.block, ties='breslow').fit()
print('statsmodels PHReg stratified HR', float(np.exp(m.params[0])), 'CI', np.exp(m.conf_int()[0]))
m2 = PHReg(d.time, d[['trt']], status=d.event, strata=d.block, ties='efron').fit()
print('efron HR', float(np.exp(m2.params[0])), 'CI', np.exp(m2.conf_int()[0]))
