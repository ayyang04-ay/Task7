#!/usr/bin/env python
"""
01_parse_workbook.py
Parse psln_program_dataset.xlsx into tidy long-format CSVs.

Every block is addressed by explicit cell ranges (sheet, header cells, data rows/cols) so that
each number in the downstream analysis can be traced back to a workbook cell.
Run with:  micromamba run -n chem python 01_parse_workbook.py
Outputs (in ./parsed/):
  scalar_long.csv   : block, sheet, panel, group, factor (day/dose/analyte/timepoint), rep, value, cell
  survival_long.csv : block, sheet, group, animal, day, event, cell
  weight_long.csv   : block, sheet, group, animal, day, value, cell
"""
import os, csv
import openpyxl
from openpyxl.utils import get_column_letter as L, column_index_from_string as CI

SRC = '/tmp/world/filesystem/psln_program_dataset.xlsx'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parsed')
os.makedirs(OUT, exist_ok=True)
wb = openpyxl.load_workbook(SRC)

scalar, surv, weight = [], [], []

def v(ws, r, c):
    return ws.cell(r, c if isinstance(c, int) else CI(c)).value

def col_block(block, sheet, hdr_row, first_col, last_col, r0, r1, panel='', factor='', groups=None):
    """Columns = groups (names on hdr_row), rows = replicates."""
    ws = wb[sheet]
    for j, c in enumerate(range(CI(first_col), CI(last_col) + 1)):
        g = groups[j] if groups else v(ws, hdr_row, c)
        rep = 0
        for r in range(r0, r1 + 1):
            x = v(ws, r, c)
            if x is None: continue
            rep += 1
            scalar.append(dict(block=block, sheet=sheet, panel=panel, group=str(g).strip(), col_index=j, factor=factor,
                               rep=rep, value=float(x), cell=f'{sheet}!{L(c)}{r}'))

def row_block(block, sheet, name_col, first_col, last_col, r0, r1, panel='', factor=''):
    """Rows = groups (names in name_col), columns = replicates."""
    ws = wb[sheet]
    for j, r in enumerate(range(r0, r1 + 1)):
        g = v(ws, r, name_col)
        rep = 0
        for c in range(CI(first_col), CI(last_col) + 1):
            x = v(ws, r, c)
            if x is None: continue
            rep += 1
            scalar.append(dict(block=block, sheet=sheet, panel=panel, group=str(g).strip(), col_index=j, factor=factor,
                               rep=rep, value=float(x), cell=f'{sheet}!{L(c)}{r}'))

def wide_block(block, sheet, hdr_row, starts, width, r0, r1, factor_col='A', panel='', factor_from_row=True):
    """Groups occupy `width` adjacent columns starting at each col in `starts` (name on hdr_row);
    each row is a level of a factor (day / dose / timepoint / analyte) given in factor_col."""
    ws = wb[sheet]
    for j, s in enumerate(starts):
        g = v(ws, hdr_row, s)
        for r in range(r0, r1 + 1):
            f = v(ws, r, factor_col) if factor_from_row else ''
            rep = 0
            for c in range(CI(s), CI(s) + width):
                x = v(ws, r, c)
                if x is None: continue
                rep += 1
                scalar.append(dict(block=block, sheet=sheet, panel=panel, group=str(g).strip(), col_index=j,
                                   factor=f if f is not None else '', rep=rep, value=float(x), cell=f'{sheet}!{L(c)}{r}'))

def surv_block(block, sheet, hdr_row, day_col, first_col, last_col, r0, r1):
    ws = wb[sheet]
    for j, c in enumerate(range(CI(first_col), CI(last_col) + 1)):
        g = v(ws, hdr_row, c) if hdr_row else f'col{L(c)}'
        k = 0
        for r in range(r0, r1 + 1):
            e = v(ws, r, c)
            if e is None: continue
            k += 1
            d = v(ws, r, day_col)
            surv.append(dict(block=block, sheet=sheet, group=str(g).strip(), col_index=j, animal=k,
                             day=(int(d) if d is not None else ''),   # blank = event flag present but no day recorded
                             event=int(e), cell=f'{sheet}!{L(c)}{r}'))

def weight_block(block, sheet, hdr_row, starts, width, r0, r1, day_col):
    ws = wb[sheet]
    for j, s in enumerate(starts):
        g = v(ws, hdr_row, s)
        for k, c in enumerate(range(CI(s), CI(s) + width)):
            for r in range(r0, r1 + 1):
                x = v(ws, r, c)
                if x is None: continue
                weight.append(dict(block=block, sheet=sheet, group=str(g).strip(), col_index=j, animal=k + 1,
                                   day=int(v(ws, r, day_col)), value=float(x), cell=f'{sheet}!{L(c)}{r}'))

# ---------------- S01 ----------------
row_block('S01-A', 'S01', 'A', 'B', 'F', 3, 10, panel='16h', factor='16h')
row_block('S01-A', 'S01', 'G', 'H', 'L', 3, 10, panel='72h', factor='72h')
row_block('S01-B', 'S01', 'A', 'B', 'F', 14, 17)
row_block('S01-C', 'S01', 'A', 'B', 'E', 20, 21)
wide_block('S01-D', 'S01', 23, ['B', 'G', 'L', 'Q'], 5, 24, 28)
wide_block('S01-E', 'S01', 29, ['B', 'G', 'L', 'Q', 'V'], 5, 30, 34)
wide_block('S01-F', 'S01', 35, ['B', 'G', 'L', 'Q', 'V'], 5, 36, 36, factor_from_row=False)
wide_block('S01-G', 'S01', 37, ['B', 'G', 'L', 'Q', 'V'], 5, 38, 38, factor_from_row=False)
# ---------------- S02 ----------------
col_block('S02-A', 'S02', 2, 'A', 'D', 3, 7)
col_block('S02-B', 'S02', 2, 'F', 'I', 3, 7)
col_block('S02-C', 'S02', 2, 'K', 'O', 3, 7)
col_block('S02-D CD40', 'S02', 9, 'A', 'D', 10, 14)
col_block('S02-D CD86', 'S02', 9, 'F', 'I', 10, 14)
col_block('S02-E', 'S02', 9, 'K', 'O', 10, 14)
wide_block('S02-F', 'S02', 16, ['B', 'G', 'L'], 5, 17, 19)
col_block('S02-G', 'S02', 21, 'B', 'D', 22, 26)
col_block('S02-H', 'S02', 29, 'B', 'F', 30, 34)
col_block('S02-I', 'S02', 29, 'H', 'I', 30, 34)
# ---------------- S03 ----------------
col_block('S03-A', 'S03', 2, 'A', 'E', 3, 7)
col_block('S03-B', 'S03', 2, 'G', 'I', 3, 7)
col_block('S03-C', 'S03', 2, 'K', 'O', 3, 7)
col_block('S03-D', 'S03', 2, 'Q', 'U', 3, 7)
col_block('S03-E', 'S03', 9, 'A', 'E', 10, 14)
col_block('S03-F', 'S03', 9, 'G', 'I', 10, 14)
col_block('S03-G', 'S03', 9, 'K', 'O', 10, 14)
col_block('S03-H', 'S03', 9, 'Q', 'U', 10, 14)
surv_block('S03-I', 'S03', 16, 'A', 'B', 'F', 17, 51)
surv_block('S03-J', 'S03', 16, 'G', 'H', 'J', 17, 46)
col_block('S03-K', 'S03', 16, 'L', 'O', 17, 21)
row_block('S03-L', 'S03', 'K', 'L', 'N', 26, 28, panel='Aicda', factor='Aicda')
row_block('S03-L', 'S03', 'K', 'O', 'Q', 26, 28, panel='E47', factor='E47')
# ---------------- S04 ----------------
row_block('S04-A', 'S04', 'A', 'B', 'F', 2, 5, panel='ICOS-', factor='ICOS-')
row_block('S04-A', 'S04', 'A', 'G', 'K', 2, 5, panel='ICOS+', factor='ICOS+')
col_block('S04-B Foxp3', 'S04', 7, 'A', 'D', 8, 12)
col_block('S04-B Tfh:Tfr', 'S04', 14, 'A', 'D', 15, 19)
col_block('S04-C', 'S04', 21, 'A', 'D', 22, 26)
col_block('S04-D', 'S04', 28, 'A', 'D', 29, 31)
# ---------------- S05 ----------------
wide_block('S05-A', 'S05', 2, ['B', 'E', 'H'], 2, 3, 5)
wide_block('S05-B', 'S05', 7, ['B', 'E', 'H'], 2, 8, 10)
col_block('S05-C', 'S05', 12, 'A', 'D', 13, 15)
col_block('S05-D', 'S05', 18, 'A', 'D', 19, 23)
col_block('S05-E', 'S05', 25, 'A', 'D', 26, 30)
col_block('S05-F', 'S05', 32, 'A', 'D', 33, 37)
col_block('S05-G', 'S05', 39, 'A', 'D', 40, 44)
col_block('S05-H', 'S05', 46, 'A', 'D', 47, 51)
col_block('S05-I', 'S05', 53, 'A', 'D', 54, 58)
# ---------------- S06 (time to event) ----------------
surv_block('S06-A', 'S06', 2, 'A', 'B', 'E', 3, 30)
surv_block('S06-B', 'S06', 2, 'G', 'H', 'K', 3, 30)
surv_block('S06-C', 'S06', 2, 'M', 'N', 'Q', 3, 30)
surv_block('S06-D', 'S06', 33, 'A', 'B', 'E', 34, 68)
surv_block('S06-E', 'S06', 33, 'G', 'H', 'L', 34, 68)          # first S06-E (rows 34-68): d60 PR8
surv_block('S06-F', 'S06', 33, 'M', 'N', 'R', 34, 68)          # first S06-F (rows 34-68): d60 rgH5N1
surv_block('S06-G', 'S06', 70, 'A', 'B', 'F', 71, 105)
surv_block('S06-E(r71)', 'S06', 70, 'G', 'H', 'K', 71, 105)    # second block labelled S06-E: imprinting / PR8
surv_block('S06-F(r71)', 'S06', 70, 'M', 'N', 'Q', 71, 105)    # second block labelled S06-F: imprinting / Perth
# ---------------- S07 ----------------
wide_block('S07-A', 'S07', 2, ['B', 'E'], 3, 3, 7)
col_block('S07-B', 'S07', 9, 'B', 'C', 10, 14, panel='CD11b+Ly6C+ monocytes', factor='CD11b+Ly6C+ monocytes')
col_block('S07-B', 'S07', 9, 'E', 'F', 10, 14, panel='Ly6C+ macrophages', factor='Ly6C+ macrophages')
col_block('S07-C', 'S07', 15, 'B', 'C', 16, 20, groups=['colB: Ly6C-CD206+ MΦ (as printed)', 'colC: Ly6C-CD206+ MΦ (as printed)'])
# ---------------- S08 ----------------
wide_block('S08-A', 'S08', 2, ['B', 'E', 'H', 'K'], 3, 3, 7)
wide_block('S08-B', 'S08', 10, ['A', 'D', 'G', 'J', 'M'], 3, 11, 11, factor_from_row=False)
col_block('S08-C', 'S08', 13, 'A', 'D', 14, 18)
weight_block('S08-D', 'S08', 20, ['B', 'G', 'L', 'Q', 'V', 'AA'], 5, 21, 26, 'A')
surv_block('S08-unlabelled', 'S08', None, 'A', 'C', 'D', 89, 101)
# ---------------- S09 ----------------
wide_block('S09-A(cols A-V)', 'S09', 2, ['B', 'E', 'H', 'K', 'N', 'Q', 'T'], 3, 3, 9, factor_col='A')
wide_block('S09-A(cols X-AS)', 'S09', 2, ['Y', 'AB', 'AE', 'AH', 'AK', 'AN', 'AQ'], 3, 3, 9, factor_col='X')
surv_block('S09-B', 'S09', 11, 'A', 'B', 'D', 12, 35)
weight_block('S09-C', 'S09', 11, ['G', 'O', 'W'], 8, 12, 19, 'F')
surv_block('S09-D', 'S09', 38, 'A', 'B', 'D', 39, 62)
weight_block('S09-E', 'S09', 38, ['G', 'O', 'W'], 8, 39, 46, 'F')
surv_block('S09-F', 'S09', 65, 'A', 'B', 'D', 66, 88)
weight_block('S09-G', 'S09', 65, ['G', 'O', 'W'], 8, 66, 73, 'F')
# ---------------- S10 ----------------
col_block('S10-A', 'S10', 2, 'A', 'D', 3, 7, panel='Ifnb1', factor='Ifnb1')
col_block('S10-A', 'S10', 2, 'F', 'I', 3, 7, panel='Tnf', factor='Tnf')
col_block('S10-A', 'S10', 2, 'K', 'N', 3, 7, panel='Isg15', factor='Isg15')
# ---------------- S11 ----------------
wide_block('S11-A', 'S11', 2, ['B', 'G', 'L', 'Q'], 5, 3, 7)
wide_block('S11-B', 'S11', 9, ['B', 'G', 'L', 'Q'], 5, 10, 14)
col_block('S11-C', 'S11', 16, 'A', 'B', 17, 21)
wide_block('S11-D', 'S11', 23, ['B', 'G', 'L', 'Q'], 5, 24, 28)
col_block('S11-E', 'S11', 30, 'A', 'D', 31, 35)
# ---------------- S12 ----------------
col_block('S12-A', 'S12', 2, 'A', 'B', 3, 5)
# ---------------- S13 ----------------
col_block('S13-A', 'S13', 2, 'A', 'C', 3, 7)
col_block('S13-B', 'S13', 2, 'E', 'G', 3, 7)
col_block('S13-C', 'S13', 2, 'I', 'K', 3, 7)
col_block('S13-D', 'S13', 2, 'M', 'O', 3, 7)
surv_block('S13-E', 'S13', 2, 'R', 'S', 'V', 3, 30)
weight_block('S13-F', 'S13', 32, ['B', 'I', 'P', 'W', 'AD'], 7, 33, 40, 'A')
weight_block('S13-G', 'S13', 42, ['B', 'L', 'V'], 10, 43, 50, 'A')
col_block('S13-H', 'S13', 52, 'A', 'D', 53, 57)
col_block('S13-I', 'S13', 52, 'F', 'J', 53, 57)
col_block('S13-J', 'S13', 52, 'L', 'P', 53, 57)
# ---------------- S14 ----------------
col_block('S14-A H1N1', 'S14', 2, 'A', 'D', 3, 7)
col_block('S14-A H3N2', 'S14', 2, 'F', 'I', 3, 7)
# ---------------- S15 ----------------
for blk, hdr in [('S15-A', 2), ('S15-B', 12), ('S15-C', 22), ('S15-D', 32)]:
    weight_block(blk, 'S15', hdr, ['B', 'I', 'P', 'W'], 7, hdr + 1, hdr + 8, 'A')
for blk, hdr in [('S15-E', 42), ('S15-F', 52), ('S15-G', 62)]:
    weight_block(blk, 'S15', hdr, ['B', 'I', 'P', 'W', 'AD'], 7, hdr + 1, hdr + 8, 'A')
surv_block('S15-H', 'S15', 72, 'A', 'B', 'D', 73, 93)
weight_block('S15-I', 'S15', 71, ['I', 'P', 'W'], 7, 72, 79, 'H')
weight_block('S15-J', 'S15', 82, ['I', 'P', 'W', 'AD'], 7, 83, 90, 'H')
weight_block('S15-K', 'S15', 92, ['I', 'P', 'W', 'AD'], 7, 93, 100, 'H')
surv_block('S15-L', 'S15', 102, 'A', 'B', 'E', 103, 130)
weight_block('S15-M', 'S15', 102, ['I', 'P', 'W', 'AD'], 7, 103, 110, 'H')
surv_block('S15-N', 'S15', 133, 'A', 'B', 'E', 134, 161)
weight_block('S15-O', 'S15', 133, ['I', 'P', 'W', 'AD'], 7, 134, 141, 'H')

def dump(rows, name):
    keys = list(rows[0].keys())
    with open(os.path.join(OUT, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
    print(name, len(rows), 'rows')

dump(scalar, 'scalar_long.csv'); dump(surv, 'survival_long.csv'); dump(weight, 'weight_long.csv')

# ---- completeness check: every numeric cell in the workbook must be captured exactly once (or be a factor/day label)
captured = {}
for coll in (scalar, surv, weight):
    for d in coll:
        captured[d['cell']] = captured.get(d['cell'], 0) + 1
dups = {k: n for k, n in captured.items() if n > 1}
print('cells captured more than once:', dups)
missed = []
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, (int, float)) and f'{ws.title}!{c.coordinate}' not in captured:
                missed.append((ws.title, c.coordinate, c.value))
import collections
bysheetcol = collections.Counter((s, ''.join(ch for ch in coord if ch.isalpha())) for s, coord, _ in missed)
print('numeric cells not captured as data (should only be day/dose factor columns):')
for k, n in sorted(bysheetcol.items()): print('   ', k, n)
