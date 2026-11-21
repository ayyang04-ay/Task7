"""
Cell-explicit parser for psln_program_dataset.xlsx.
Every value is carried with its sheet + cell address so each number in the report can be traced.
Output: tidy long tables
  QUANT : sheet, block, analyte, group, time, rep, value, cell
  SURV  : sheet, block, group, rep, day, event, cell_day, cell_evt
  WT    : sheet, block, group, animal, day, value, cell
"""
import openpyxl, re, json, os
import pandas as pd, numpy as np
from openpyxl.utils import get_column_letter as L, column_index_from_string as C

XLSX = os.environ.get('PSLN_XLSX', '/tmp/world/filesystem/psln_program_dataset.xlsx')   # source workbook
wb = openpyxl.load_workbook(XLSX, data_only=True)

def cv(ws, col, row):
    """cell value by (col letter or index, row)"""
    if isinstance(col, str): col = C(col)
    return ws.cell(row=row, column=col).value

def addr(col, row):
    if isinstance(col, int): col = L(col)
    return f"{col}{row}"

quant = []   # continuous per-animal measurements
surv = []    # time-to-event rows
wt = []      # body weights

def q(sheet, block, analyte, group, time, vals_cells):
    for i, (v, a) in enumerate(vals_cells):
        if v is None: continue
        quant.append(dict(sheet=sheet, block=block, analyte=analyte, group=str(group).strip(), time=time, rep=i+1, value=float(v), cell=f"{sheet}!{a}"))

def cols_block(sheet, block, analyte, hdr_row, first_col, last_col, r0, r1, time=None, groups=None):
    """one group per column; header in hdr_row"""
    ws = wb[sheet]
    for ci in range(C(first_col), C(last_col)+1):
        g = cv(ws, ci, hdr_row) if groups is None else groups[ci-C(first_col)]
        vc = [(cv(ws, ci, r), addr(ci, r)) for r in range(r0, r1+1)]
        q(sheet, block, analyte, g, time, vc)

def rows_block(sheet, block, analyte, label_col, first_col, last_col, r0, r1, time=None):
    """one group per row; label in label_col"""
    ws = wb[sheet]
    for r in range(r0, r1+1):
        g = cv(ws, label_col, r)
        vc = [(cv(ws, ci, r), addr(ci, r)) for ci in range(C(first_col), C(last_col)+1)]
        q(sheet, block, analyte, g, time, vc)

def timecourse(sheet, block, analyte, hdr_row, group_starts, width, time_col, r0, r1, fixed_time=None):
    """groups are merged headers spanning `width` columns starting at each col in group_starts; one row per timepoint"""
    ws = wb[sheet]
    for gs in group_starts:
        g = cv(ws, gs, hdr_row)
        for r in range(r0, r1+1):
            t = fixed_time if fixed_time is not None else cv(ws, time_col, r)
            vc = [(cv(ws, ci, r), addr(ci, r)) for ci in range(C(gs), C(gs)+width)]
            q(sheet, block, analyte, g, t, vc)

def survival(sheet, block, day_col, first_g, last_g, hdr_row, r0, r1):
    ws = wb[sheet]
    for ci in range(C(first_g), C(last_g)+1):
        g = str(cv(ws, ci, hdr_row)).strip()
        k = 0
        for r in range(r0, r1+1):
            e = cv(ws, ci, r)
            if e is None: continue
            k += 1
            d = cv(ws, day_col, r)
            surv.append(dict(sheet=sheet, block=block, group=g, rep=k, day=(None if d is None else float(d)), event=int(e),
                             cell_day=f"{sheet}!{addr(day_col, r)}", cell_evt=f"{sheet}!{addr(ci, r)}"))

def weights(sheet, block, hdr_row, group_starts, width, day_col, r0, r1):
    ws = wb[sheet]
    for gs in group_starts:
        g = str(cv(ws, gs, hdr_row)).strip()
        for k, ci in enumerate(range(C(gs), C(gs)+width)):
            for r in range(r0, r1+1):
                v = cv(ws, ci, r)
                d = cv(ws, day_col, r)
                wt.append(dict(sheet=sheet, block=block, group=g, animal=k+1, col=L(ci), day=float(d), value=(np.nan if v is None else float(v)), cell=f"{sheet}!{addr(ci, r)}"))

# ---------------- S01 ----------------
rows_block('S01', 'S01-A', 'Ifnb1 lung (fold vs untreated)', 'A', 'B', 'F', 3, 10, time='16h')
rows_block('S01', 'S01-A', 'Ifnb1 lung (fold vs untreated)', 'G', 'H', 'L', 3, 10, time='72h')
rows_block('S01', 'S01-B', 'SRB+ AEC (%)', 'A', 'B', 'F', 14, 17, time='16h')
rows_block('S01', 'S01-C', 'DiD+ alveolar macrophages (%)', 'A', 'B', 'E', 20, 21, time='16h')
timecourse('S01', 'S01-D', 'lung monocytes (%)', 23, ['B','G','L','Q'], 5, 'A', 24, 28)
timecourse('S01', 'S01-E', 'lung CD11b+ DC (%)', 29, ['B','G','L','Q','V'], 5, 'A', 30, 34)
timecourse('S01', 'S01-F', 'lung cDC1 (%)', 35, ['B','G','L','Q','V'], 5, 'A', 36, 36, fixed_time='72h')
timecourse('S01', 'S01-G', 'lung cDC2 (%)', 37, ['B','G','L','Q','V'], 5, 'A', 38, 38, fixed_time='72h')
# ---------------- S02 ----------------
cols_block('S02', 'S02-A', 'lung CCR7+ CD11b+ DC (%)', 2, 'A', 'D', 3, 7, time='72h')
cols_block('S02', 'S02-B', 'MLN CD11b+CD103- DC (%)', 2, 'F', 'I', 3, 7, time='72h')
cols_block('S02', 'S02-C', 'MLN OVA-AF647+ DC (%)', 2, 'K', 'O', 3, 7, time='36h')
cols_block('S02', 'S02-D CD40', 'CD40+ of MLN CD11b+ DC (%)', 9, 'A', 'D', 10, 14, time='d3')
cols_block('S02', 'S02-D CD86', 'CD86+ of MLN CD11b+ DC (%)', 9, 'F', 'I', 10, 14, time='d3')
cols_block('S02', 'S02-E', 'OT-I proliferation ex vivo (%)', 9, 'K', 'O', 10, 14, time='72h')
timecourse('S02', 'S02-F', 'Gm-csf lung (fold)', 16, ['B','G','L'], 5, 'A', 17, 19)
cols_block('S02', 'S02-G', 'lung Ly6C+ moDC-like (%)', 21, 'B', 'D', 22, 26, time='d5')
cols_block('S02', 'S02-H', 'CD45.2+ moDC (%)', 29, 'B', 'F', 30, 34, time='d3')
cols_block('S02', 'S02-I', 'lung GZMB+ CD8 T (%)', 29, 'H', 'I', 30, 34, time='d5')
# ---------------- S03 ----------------
cols_block('S03', 'S03-A', 'serum IgG anti-CA09 H1N1 (titer)', 2, 'A', 'E', 3, 7, time='d14')
cols_block('S03', 'S03-B', 'IgG2a/IgG1 anti-CA09 (ratio)', 2, 'G', 'I', 3, 7, time='d14')
cols_block('S03', 'S03-C', 'HAI anti-CA09 H1N1 (titer)', 2, 'K', 'O', 3, 7, time='d14')
cols_block('S03', 'S03-D', 'neutralizing anti-CA09 H1N1 (titer)', 2, 'Q', 'U', 3, 7, time='d14')
cols_block('S03', 'S03-E', 'serum IgG anti-Aichi H3N2 (titer)', 9, 'A', 'E', 10, 14, time='d14')
cols_block('S03', 'S03-F', 'IgG2a/IgG1 anti-Aichi (ratio)', 9, 'G', 'I', 10, 14, time='d14')
cols_block('S03', 'S03-G', 'HAI anti-Aichi H3N2 (titer)', 9, 'K', 'O', 10, 14, time='d14')
cols_block('S03', 'S03-H', 'neutralizing anti-Aichi H3N2 (titer)', 9, 'Q', 'U', 10, 14, time='d14')
survival('S03', 'S03-I', 'A', 'B', 'F', 16, 17, 51)
survival('S03', 'S03-J', 'G', 'H', 'J', 16, 17, 46)
cols_block('S03', 'S03-K', 'MLN GC B cells (%)', 16, 'L', 'O', 17, 21, time='d7')
rows_block('S03', 'S03-L', 'Aicda MLN B (fold)', 'K', 'L', 'N', 26, 28, time='d5')
rows_block('S03', 'S03-L', 'E47 MLN B (fold)', 'K', 'O', 'Q', 26, 28, time='d5')
# ---------------- S04 ----------------
rows_block('S04', 'S04-A', 'Tfh ICOS-lo (%)', 'A', 'B', 'F', 2, 5, time='d7')
rows_block('S04', 'S04-A', 'Tfh ICOS-hi (%)', 'A', 'G', 'K', 2, 5, time='d7')
cols_block('S04', 'S04-B Foxp3', 'Tfr (Foxp3+ of CXCR5+ICOShi) (%)', 7, 'A', 'D', 8, 12, time='d7')
cols_block('S04', 'S04-B Tfh:Tfr', 'Tfh:Tfr ratio', 14, 'A', 'D', 15, 19, time='d7')
cols_block('S04', 'S04-C', 'Tfr (%)', 21, 'A', 'D', 22, 26, time='d30')
cols_block('S04', 'S04-D', 'lung Treg (%)', 28, 'A', 'D', 29, 31, time='d7')
# ---------------- S05 ----------------
timecourse('S05', 'S05-A', 'lung NP366 tetramer+ CD8 (%)', 2, ['B','E','H'], 2, 'A', 3, 5)
timecourse('S05', 'S05-B', 'MLN NP366 tetramer+ CD8 (%)', 7, ['B','E','H'], 2, 'A', 8, 10)
cols_block('S05', 'S05-C', 'OT-I proliferation in vivo (%)', 12, 'A', 'D', 13, 15, time='d4')
cols_block('S05', 'S05-D', 'lung Ki67+ CD8 (%)', 18, 'A', 'D', 19, 23, time='d3')
cols_block('S05', 'S05-E', 'lung GZMB+ CD8 (%)', 25, 'A', 'D', 26, 30, time='d3')
cols_block('S05', 'S05-F', 'MLN IFNg+ CD8, rgH5N1 restim (%)', 32, 'A', 'D', 33, 37, time='d14')
cols_block('S05', 'S05-G', 'MLN IFNg+ CD8, rgH5N1 restim (%)', 39, 'A', 'D', 40, 44, time='d60')
cols_block('S05', 'S05-H', 'MLN GZMB+ CD8 (%)', 46, 'A', 'D', 47, 51, time='d60')
cols_block('S05', 'S05-I', 'lung CD8 TRM (%)', 53, 'A', 'D', 54, 58, time='d25')
# ---------------- S06 ----------------
survival('S06', 'S06-A', 'A', 'B', 'E', 2, 3, 30)
survival('S06', 'S06-B', 'G', 'H', 'K', 2, 3, 30)
survival('S06', 'S06-C', 'M', 'N', 'Q', 2, 3, 30)
survival('S06', 'S06-D', 'A', 'B', 'E', 33, 34, 61)
survival('S06', 'S06-E', 'G', 'H', 'L', 33, 34, 68)
survival('S06', 'S06-F', 'M', 'N', 'R', 33, 34, 68)
survival('S06', 'S06-G', 'A', 'B', 'F', 70, 71, 105)
survival('S06', 'S06-E(r71)', 'G', 'H', 'K', 70, 71, 98)   # imprinting, PR8 challenge (labeled S06-E a second time)
survival('S06', 'S06-F(r71)', 'M', 'N', 'Q', 70, 71, 98)   # imprinting, Perth challenge (labeled S06-F a second time)
# ---------------- S07 ----------------
timecourse('S07', 'S07-A', 'lung Ly6C+CCR2+ macrophages (x1e5)', 2, ['B','E'], 3, 'A', 3, 7)
cols_block('S07', 'S07-B', 'lung CD11b+Ly6C+ monocytes (%)', 9, 'B', 'C', 10, 14)
cols_block('S07', 'S07-B', 'lung Ly6C+ macrophages (%)', 9, 'E', 'F', 10, 14)
cols_block('S07', 'S07-C', 'lung Treg after Mphi transfer (%)', 15, 'B', 'C', 16, 20, groups=['col B: "Ly6C-CD206+ MPhi"', 'col C: "Ly6C-CD206+ MPhi"'])
# ---------------- S08 ----------------
timecourse('S08', 'S08-A', 'Ifnb1 lung dose-response (fold)', 2, ['B','E','H','K'], 3, 'A', 3, 7)
timecourse('S08', 'S08-B', 'encapsulation efficiency (%)', 10, ['A','D','G','J','M'], 3, 'A', 11, 11, fixed_time='na')
cols_block('S08', 'S08-C', 'SRB+ AEC (%)', 13, 'A', 'D', 14, 18, time='16h')
weights('S08', 'S08-D', 20, ['B','G','L','Q','V','AA'], 5, 'A', 21, 26)
# ---------------- S09 ----------------
ws = wb['S09']
for (hdr_starts, lab_col, panel) in [(['B','E','H','K','N','Q','T'], 'A', 'panel1(A-U)'), (['Y','AB','AE','AH','AK','AN','AQ'], 'X', 'panel2(X-AS)')]:
    for gs in hdr_starts:
        g = cv(ws, gs, 2)
        for r in range(3, 10):
            an = cv(ws, lab_col, r)
            vc = [(cv(ws, ci, r), addr(ci, r)) for ci in range(C(gs), C(gs)+3)]
            q('S09', 'S09-A', f'{an} (log10 fold)', g, panel, vc)
survival('S09', 'S09-B', 'A', 'B', 'D', 11, 12, 35)
weights('S09', 'S09-C', 11, ['G','O','W'], 8, 'F', 12, 19)
survival('S09', 'S09-D', 'A', 'B', 'D', 38, 39, 62)
weights('S09', 'S09-E', 38, ['G','O','W'], 8, 'F', 39, 46)
survival('S09', 'S09-F', 'A', 'B', 'D', 65, 66, 88)
weights('S09', 'S09-G', 65, ['G','O','W'], 8, 'F', 66, 73)
# ---------------- S10 ----------------
cols_block('S10', 'S10-A', 'CNS Ifnb1 (fold)', 2, 'A', 'D', 3, 7, time='36h')
cols_block('S10', 'S10-A', 'CNS Tnf (fold)', 2, 'F', 'I', 3, 7, time='36h')
cols_block('S10', 'S10-A', 'CNS Isg15 (fold)', 2, 'K', 'N', 3, 7, time='36h')
# ---------------- S11 ----------------
timecourse('S11', 'S11-A', 'lung alveolar macrophages (%)', 2, ['B','G','L','Q'], 5, 'A', 3, 7)
timecourse('S11', 'S11-B', 'lung neutrophils (%)', 9, ['B','G','L','Q'], 5, 'A', 10, 14)
cols_block('S11', 'S11-C', 'recruited lung monocytes (%)', 16, 'A', 'B', 17, 21, time='d3')
timecourse('S11', 'S11-D', 'lung NK cells (%)', 23, ['B','G','L','Q'], 5, 'A', 24, 28)
cols_block('S11', 'S11-E', 'lung CD206+ macrophages (%)', 30, 'A', 'D', 31, 35)
# ---------------- S12 ----------------
cols_block('S12', 'S12-A', 'infiltrating CD45.2+ monocytes (%)', 2, 'A', 'B', 3, 5, time='d3')
# ---------------- S13 ----------------
cols_block('S13', 'S13-A', 'IgG2a anti-CA09 (titer)', 2, 'A', 'C', 3, 7, time='d14')
cols_block('S13', 'S13-B', 'IgG1 anti-CA09 (titer)', 2, 'E', 'G', 3, 7, time='d14')
cols_block('S13', 'S13-C', 'IgG2a anti-Aichi (titer)', 2, 'I', 'K', 3, 7, time='d14')
cols_block('S13', 'S13-D', 'IgG1 anti-Aichi (titer)', 2, 'M', 'O', 3, 7, time='d14')
survival('S13', 'S13-E', 'R', 'S', 'V', 2, 3, 30)
weights('S13', 'S13-F', 32, ['B','I','P','W','AD'], 7, 'A', 33, 40)
weights('S13', 'S13-G', 42, ['B','L','V'], 10, 'A', 43, 50)
cols_block('S13', 'S13-H', 'IgG+ of MLN B220+ (%)', 52, 'A', 'D', 53, 57)
cols_block('S13', 'S13-I', 'serum IgG anti-CA09, d28 post-boost (titer)', 52, 'F', 'J', 53, 57, time='d28')
cols_block('S13', 'S13-J', 'serum IgG anti-Aichi, d28 post-boost (titer)', 52, 'L', 'P', 53, 57, time='d28')
# ---------------- S14 ----------------
cols_block('S14', 'S14-A H1N1', 'MLN IFNg+ CD8, CA09 restim (%)', 2, 'A', 'D', 3, 7)
cols_block('S14', 'S14-A H3N2', 'MLN IFNg+ CD8, Aichi restim (%)', 2, 'F', 'I', 3, 7)
# ---------------- S15 ----------------
for blk, hr, five in [('S15-A', 2, False), ('S15-B', 12, False), ('S15-C', 22, False), ('S15-D', 32, False), ('S15-E', 42, True), ('S15-F', 52, True), ('S15-G', 62, True)]:
    gs = ['B','I','P','W'] + (['AD'] if five else [])
    weights('S15', blk, hr, gs, 7, 'A', hr+1, hr+8)
survival('S15', 'S15-H', 'A', 'B', 'D', 72, 73, 93)
weights('S15', 'S15-I', 71, ['I','P','W'], 7, 'H', 72, 79)
weights('S15', 'S15-J', 82, ['I','P','W','AD'], 7, 'H', 83, 90)
weights('S15', 'S15-K', 92, ['I','P','W','AD'], 7, 'H', 93, 100)
survival('S15', 'S15-L', 'A', 'B', 'E', 102, 103, 130)
weights('S15', 'S15-M', 102, ['I','P','W','AD'], 7, 'H', 103, 110)
survival('S15', 'S15-N', 'A', 'B', 'E', 133, 134, 161)
weights('S15', 'S15-O', 133, ['I','P','W','AD'], 7, 'H', 134, 141)

QUANT = pd.DataFrame(quant)
SURV = pd.DataFrame(surv)
WT = pd.DataFrame(wt)

if __name__ == '__main__':
    QUANT.to_csv('quant_long.csv', index=False)
    SURV.to_csv('surv_long.csv', index=False)
    WT.to_csv('wt_long.csv', index=False)
    print(QUANT.shape, SURV.shape, WT.shape)
    # completeness check: count numeric cells in workbook vs captured
    captured = set(QUANT.cell) | set(SURV.cell_evt) | set(SURV.cell_day.dropna()) | set(WT.dropna(subset=['value']).cell)
    allnum = {}
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, (int, float)) and not isinstance(c.value, bool):
                    allnum[f"{ws.title}!{c.coordinate}"] = c.value
    missing = sorted(set(allnum) - captured, key=lambda s: (s.split('!')[0], C(re.match(r'[A-Z]+', s.split('!')[1]).group()), int(re.search(r'\d+', s.split('!')[1]).group())))
    print("numeric cells in workbook:", len(allnum), "captured:", len(captured & set(allnum)), "not captured:", len(missing))
    # show not captured grouped by sheet
    from collections import defaultdict
    d = defaultdict(list)
    for m in missing: d[m.split('!')[0]].append(m.split('!')[1])
    for k, v in d.items(): print(k, len(v), v[:80])
