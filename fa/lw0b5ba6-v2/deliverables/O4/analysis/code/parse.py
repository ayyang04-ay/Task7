"""
Parser for psln_program_dataset.xlsx.
Every extracted value carries its sheet and cell coordinate so any downstream number
can be traced back to the workbook.  Block layouts follow psln_program_annotation.pdf
(Per-block annotation) and were confirmed by direct inspection of the cells.
Output: tidy long-format tables
  values.csv   - continuous per-animal readouts
  survival.csv - one row per animal (time, event)
  bw.csv       - body-weight series (one row per animal x day)
"""
import openpyxl, re, json
import pandas as pd
from openpyxl.utils import column_index_from_string as ci, get_column_letter as gl

WB = openpyxl.load_workbook('/tmp/world/filesystem/psln_program_dataset.xlsx', data_only=True)

def cell(ws, col, row):
    return ws.cell(row=row, column=ci(col) if isinstance(col, str) else col)

def cols(a, b):
    return [gl(i) for i in range(ci(a), ci(b) + 1)]

VAL = []   # continuous
SURV = []  # survival
BW = []    # body weight

def add_val(block, sheet, group, value, coord, time=None, analyte=None, unit=None, note=None):
    VAL.append(dict(block=block, sheet=sheet, group=str(group).strip(), time=time, analyte=analyte,
                    value=value, cell=f"{sheet}!{coord}", unit=unit, note=note))

# ---------- generic layouts ----------
def header_cols_block(block, sheet, header_row, group_cols, first_row, last_row, unit=None, analyte=None, time=None):
    """groups in a header row, one column per group, replicates down the rows"""
    ws = WB[sheet]
    for c in group_cols:
        g = cell(ws, c, header_row).value
        for r in range(first_row, last_row + 1):
            v = cell(ws, c, r).value
            if v is None or isinstance(v, str):
                continue
            add_val(block, sheet, g, float(v), f"{c}{r}", time=time, analyte=analyte, unit=unit)

def row_groups_block(block, sheet, name_col, rows, val_cols, unit=None, analyte=None, time=None):
    """group name in one column, replicates across columns"""
    ws = WB[sheet]
    for r in rows:
        g = cell(ws, name_col, r).value
        for c in val_cols:
            v = cell(ws, c, r).value
            if v is None or isinstance(v, str):
                continue
            add_val(block, sheet, g, float(v), f"{c}{r}", time=time, analyte=analyte, unit=unit)

def spanned_time_block(block, sheet, header_row, spans, first_row, last_row, time_col='A', unit=None, analyte=None, time_override=None):
    """group header spans several columns (replicates); rows are timepoints"""
    ws = WB[sheet]
    for (start, end) in spans:
        g = cell(ws, start, header_row).value
        for r in range(first_row, last_row + 1):
            t = cell(ws, time_col, r).value if time_col else None
            if time_override is not None:
                t = time_override
            for c in cols(start, end):
                v = cell(ws, c, r).value
                if v is None or isinstance(v, str):
                    continue
                add_val(block, sheet, g, float(v), f"{c}{r}", time=t, analyte=analyte, unit=unit)

def survival_block(block, sheet, header_row, day_col, group_cols, first_row, last_row, obs_days=14):
    ws = WB[sheet]
    for r in range(first_row, last_row + 1):
        d = cell(ws, day_col, r).value
        for c in group_cols:
            e = cell(ws, c, r).value
            if e is None:
                continue
            g = cell(ws, c, header_row).value
            SURV.append(dict(block=block, sheet=sheet, group=str(g).strip(), day=d, event=int(e),
                             cell_day=f"{sheet}!{day_col}{r}", cell_event=f"{sheet}!{c}{r}", obs_days=obs_days))

def bw_block(block, sheet, header_row, spans, first_row, last_row, day_col):
    ws = WB[sheet]
    for (start, end) in spans:
        g = cell(ws, start, header_row).value
        for k, c in enumerate(cols(start, end)):
            for r in range(first_row, last_row + 1):
                d = cell(ws, day_col, r).value
                v = cell(ws, c, r).value
                BW.append(dict(block=block, sheet=sheet, group=str(g).strip(), animal=f"{block}:{c}", col=c,
                               day=d, value=(None if v is None else float(v)), cell=f"{sheet}!{c}{r}"))

# ================= S01 =================
row_groups_block('S01-A_16h', 'S01', 'A', range(3, 11), cols('B', 'F'), unit='fold vs untreated', analyte='Ifnb1', time='16h')
row_groups_block('S01-A_72h', 'S01', 'G', range(3, 11), cols('H', 'L'), unit='fold vs untreated', analyte='Ifnb1', time='72h')
row_groups_block('S01-B', 'S01', 'A', range(14, 18), cols('B', 'F'), unit='%SRB+', time='16h')
row_groups_block('S01-C', 'S01', 'A', range(20, 22), cols('B', 'E'), unit='%DiD+ AM', time='16h')
spanned_time_block('S01-D', 'S01', 23, [('B', 'F'), ('G', 'K'), ('L', 'P'), ('Q', 'U')], 24, 28, unit='% monocytes')
spanned_time_block('S01-E', 'S01', 29, [('B', 'F'), ('G', 'K'), ('L', 'P'), ('Q', 'U'), ('V', 'Z')], 30, 34, unit='% CD11b+ DC')
spanned_time_block('S01-F', 'S01', 35, [('B', 'F'), ('G', 'K'), ('L', 'P'), ('Q', 'U'), ('V', 'Z')], 36, 36, time_col=None, unit='% cDC1', time_override='72h')
spanned_time_block('S01-G', 'S01', 37, [('B', 'F'), ('G', 'K'), ('L', 'P'), ('Q', 'U'), ('V', 'Z')], 38, 38, time_col=None, unit='% cDC2', time_override='72h')
# ================= S02 =================
header_cols_block('S02-A', 'S02', 2, cols('A', 'D'), 3, 7, unit='% CCR7+ CD11b+ DC lung', time='72h')
header_cols_block('S02-B', 'S02', 2, cols('F', 'I'), 3, 7, unit='% CD11b+CD103- DC MLN', time='72h')
header_cols_block('S02-C', 'S02', 2, cols('K', 'O'), 3, 7, unit='% AF647-OVA+ DC MLN', time='36h')
header_cols_block('S02-D_CD40', 'S02', 9, cols('A', 'D'), 10, 14, unit='% CD40+', time='d3')
header_cols_block('S02-D_CD86', 'S02', 9, cols('F', 'I'), 10, 14, unit='% CD86+', time='d3')
header_cols_block('S02-E', 'S02', 9, cols('K', 'O'), 10, 14, unit='% OT-I proliferated', time='72h DC harvest')
spanned_time_block('S02-F', 'S02', 16, [('B', 'F'), ('G', 'K'), ('L', 'P')], 17, 19, unit='Gm-csf fold')
header_cols_block('S02-G', 'S02', 21, cols('B', 'D'), 22, 26, unit='% moDC-like', time='d5')
header_cols_block('S02-H', 'S02', 29, cols('B', 'F'), 30, 34, unit='% CD45.2+ moDC', time='d3')
header_cols_block('S02-I', 'S02', 29, cols('H', 'I'), 30, 34, unit='% GZMB+ CD8 lung', time='d5')
# ================= S03 =================
header_cols_block('S03-A', 'S03', 2, cols('A', 'E'), 3, 7, unit='IgG titre CA09', time='d14')
header_cols_block('S03-B', 'S03', 2, cols('G', 'I'), 3, 7, unit='IgG2a/IgG1 CA09', time='d14')
header_cols_block('S03-C', 'S03', 2, cols('K', 'O'), 3, 7, unit='HAI CA09', time='d14')
header_cols_block('S03-D', 'S03', 2, cols('Q', 'U'), 3, 7, unit='NT CA09', time='d14')
header_cols_block('S03-E', 'S03', 9, cols('A', 'E'), 10, 14, unit='IgG titre Aichi', time='d14')
header_cols_block('S03-F', 'S03', 9, cols('G', 'I'), 10, 14, unit='IgG2a/IgG1 Aichi', time='d14')
header_cols_block('S03-G', 'S03', 9, cols('K', 'O'), 10, 14, unit='HAI Aichi', time='d14')
header_cols_block('S03-H', 'S03', 9, cols('Q', 'U'), 10, 14, unit='NT Aichi', time='d14')
survival_block('S03-I', 'S03', 16, 'A', cols('B', 'F'), 17, 51, obs_days=14)
survival_block('S03-J', 'S03', 16, 'G', cols('H', 'J'), 17, 46, obs_days=22)
header_cols_block('S03-K', 'S03', 16, cols('L', 'O'), 17, 21, unit='% GC B', time='d7')
row_groups_block('S03-L_Aicda', 'S03', 'K', range(26, 29), cols('L', 'N'), unit='fold', analyte='Aicda', time='d5')
row_groups_block('S03-L_E47', 'S03', 'K', range(26, 29), cols('O', 'Q'), unit='fold', analyte='E47', time='d5')
# ================= S04 =================
row_groups_block('S04-A_ICOSlo', 'S04', 'A', range(2, 6), cols('B', 'F'), unit='% Tfh ICOS-lo', time='d7')
row_groups_block('S04-A_ICOShi', 'S04', 'A', range(2, 6), cols('G', 'K'), unit='% Tfh ICOS-hi', time='d7')
header_cols_block('S04-B_Foxp3', 'S04', 7, cols('A', 'D'), 8, 12, unit='% Foxp3+ in CXCR5+ICOShi (Tfr)', time='d7')
header_cols_block('S04-B_TfhTfr', 'S04', 14, cols('A', 'D'), 15, 19, unit='Tfh:Tfr', time='d7')
header_cols_block('S04-C', 'S04', 21, cols('A', 'D'), 22, 26, unit='% Tfr', time='d30')
header_cols_block('S04-D', 'S04', 28, cols('A', 'D'), 29, 31, unit='% lung Treg', time='d7')
# ================= S05 =================
spanned_time_block('S05-A', 'S05', 2, [('B', 'C'), ('E', 'F'), ('H', 'I')], 3, 5, unit='% NP366 tet+ CD8 lung')
spanned_time_block('S05-B', 'S05', 7, [('B', 'C'), ('E', 'F'), ('H', 'I')], 8, 10, unit='% NP366 tet+ CD8 MLN')
header_cols_block('S05-C', 'S05', 12, cols('A', 'D'), 13, 15, unit='% OT-I proliferated', time='d4')
header_cols_block('S05-D', 'S05', 18, cols('A', 'D'), 19, 23, unit='% Ki67+ CD8 lung', time='d3')
header_cols_block('S05-E', 'S05', 25, cols('A', 'D'), 26, 30, unit='% GZMB+ CD8 lung', time='d3')
header_cols_block('S05-F', 'S05', 32, cols('A', 'D'), 33, 37, unit='% IFNg+ CD8 MLN (rgH5N1 restim)', time='d14')
header_cols_block('S05-G', 'S05', 39, cols('A', 'D'), 40, 44, unit='% IFNg+ CD8 MLN (rgH5N1 restim)', time='d60')
header_cols_block('S05-H', 'S05', 46, cols('A', 'D'), 47, 51, unit='% GZMB+ CD8 MLN', time='d60')
header_cols_block('S05-I', 'S05', 53, cols('A', 'D'), 54, 58, unit='% lung TRM CD8', time='d25')
# ================= S06 =================
survival_block('S06-A', 'S06', 2, 'A', cols('B', 'E'), 3, 30)
survival_block('S06-B', 'S06', 2, 'G', cols('H', 'K'), 3, 30)
survival_block('S06-C', 'S06', 2, 'M', cols('N', 'Q'), 3, 30)
survival_block('S06-D', 'S06', 33, 'A', cols('B', 'E'), 34, 61)
survival_block('S06-E', 'S06', 33, 'G', cols('H', 'L'), 34, 68)
survival_block('S06-F', 'S06', 33, 'M', cols('N', 'R'), 34, 68)
survival_block('S06-G', 'S06', 70, 'A', cols('B', 'F'), 71, 105)
survival_block('S06-E2_imprint', 'S06', 70, 'G', cols('H', 'K'), 71, 98)
survival_block('S06-F2_imprint', 'S06', 70, 'M', cols('N', 'Q'), 71, 98)
# ================= S07 =================
spanned_time_block('S07-A', 'S07', 2, [('B', 'D'), ('E', 'G')], 3, 7, unit='Ly6C+CCR2+ macrophages (x10^5)')
ws = WB['S07']
for c, g, pop in [('B', 'PSLN-344', 'monocytes'), ('C', 'PSLN-344+INCB3344', 'monocytes'),
                  ('E', 'PSLN-344', 'Ly6C+ macrophages'), ('F', 'PSLN-344+INCB3344', 'Ly6C+ macrophages')]:
    for r in range(10, 15):
        add_val('S07-B', 'S07', g, float(cell(ws, c, r).value), f"{c}{r}", analyte=pop, unit='%')
for c in ['B', 'C']:
    for r in range(16, 21):
        add_val('S07-C', 'S07', f"{cell(ws, c, 15).value} [col {c}]", float(cell(ws, c, r).value), f"{c}{r}", unit='% lung Treg', time='d4 post transfer')
# ================= S08 =================
spanned_time_block('S08-A', 'S08', 2, [('B', 'D'), ('E', 'G'), ('H', 'J'), ('K', 'M')], 3, 7, unit='Ifnb1 fold (dose ug)')
ws = WB['S08']
for start, end in [('A', 'C'), ('D', 'F'), ('G', 'I'), ('J', 'L'), ('M', 'O')]:
    g = cell(ws, start, 10).value
    for c in cols(start, end):
        add_val('S08-B', 'S08', g, float(cell(ws, c, 11).value), f"{c}11", unit='% EE')
header_cols_block('S08-C', 'S08', 13, cols('A', 'D'), 14, 18, unit='%SRB+', time='16h')
bw_block('S08-D', 'S08', 20, [('B', 'F'), ('G', 'K'), ('L', 'P'), ('Q', 'U'), ('V', 'Z'), ('AA', 'AE')], 21, 26, 'A')
# ================= S09 =================
ws = WB['S09']
for (start, end) in [('B', 'D'), ('E', 'G'), ('H', 'J'), ('K', 'M'), ('N', 'P'), ('Q', 'S'), ('T', 'V')]:
    g = cell(ws, start, 2).value
    for r in range(3, 10):
        an = cell(ws, 'A', r).value
        for c in cols(start, end):
            add_val('S09-A_blk1(cols A-U)', 'S09', g, float(cell(ws, c, r).value), f"{c}{r}", analyte=an, unit='log10 fold', time='16h (label)')
for (start, end) in [('Y', 'AA'), ('AB', 'AD'), ('AE', 'AG'), ('AH', 'AJ'), ('AK', 'AM'), ('AN', 'AP'), ('AQ', 'AS')]:
    g = cell(ws, start, 2).value
    for r in range(3, 10):
        an = cell(ws, 'X', r).value
        for c in cols(start, end):
            add_val('S09-A_blk2(cols X-AS)', 'S09', g, float(cell(ws, c, r).value), f"{c}{r}", analyte=an, unit='log10 fold', time='16h (label)')
survival_block('S09-B', 'S09', 11, 'A', cols('B', 'D'), 12, 35)
bw_block('S09-C', 'S09', 11, [('G', 'N'), ('O', 'V'), ('W', 'AD')], 12, 19, 'F')
survival_block('S09-D', 'S09', 38, 'A', cols('B', 'D'), 39, 62)
bw_block('S09-E', 'S09', 38, [('G', 'N'), ('O', 'V'), ('W', 'AD')], 39, 46, 'F')
survival_block('S09-F', 'S09', 65, 'A', cols('B', 'D'), 66, 88)
bw_block('S09-G', 'S09', 65, [('G', 'N'), ('O', 'V'), ('W', 'AD')], 66, 73, 'F')
# ================= S10 =================
header_cols_block('S10-A_Ifnb1', 'S10', 2, cols('A', 'D'), 3, 7, unit='CNS fold', analyte='Ifnb1', time='36h')
header_cols_block('S10-A_Tnf', 'S10', 2, cols('F', 'I'), 3, 7, unit='CNS fold', analyte='Tnf', time='36h')
header_cols_block('S10-A_Isg15', 'S10', 2, cols('K', 'N'), 3, 7, unit='CNS fold', analyte='Isg15', time='36h')
# ================= S11 =================
spanned_time_block('S11-A', 'S11', 2, [('B', 'F'), ('G', 'K'), ('L', 'P'), ('Q', 'U')], 3, 7, unit='% alveolar macrophages')
spanned_time_block('S11-B', 'S11', 9, [('B', 'F'), ('G', 'K'), ('L', 'P'), ('Q', 'U')], 10, 14, unit='% neutrophils')
header_cols_block('S11-C', 'S11', 16, cols('A', 'B'), 17, 21, unit='% recruited monocytes', time='d3')
spanned_time_block('S11-D', 'S11', 23, [('B', 'F'), ('G', 'K'), ('L', 'P'), ('Q', 'U')], 24, 28, unit='% NK')
header_cols_block('S11-E', 'S11', 30, cols('A', 'D'), 31, 35, unit='% CD206+ macrophages', time='not stated')
# ================= S12 =================
header_cols_block('S12-A', 'S12', 2, cols('A', 'B'), 3, 5, unit='% CD45.2+ monocytes', time='d3')
# ================= S13 =================
header_cols_block('S13-A', 'S13', 2, cols('A', 'C'), 3, 7, unit='IgG2a titre CA09', time='d14')
header_cols_block('S13-B', 'S13', 2, cols('E', 'G'), 3, 7, unit='IgG1 titre CA09', time='d14')
header_cols_block('S13-C', 'S13', 2, cols('I', 'K'), 3, 7, unit='IgG2a titre Aichi', time='d14')
header_cols_block('S13-D', 'S13', 2, cols('M', 'O'), 3, 7, unit='IgG1 titre Aichi', time='d14')
survival_block('S13-E', 'S13', 2, 'R', cols('S', 'V'), 3, 30)
bw_block('S13-F', 'S13', 32, [('B', 'H'), ('I', 'O'), ('P', 'V'), ('W', 'AC'), ('AD', 'AJ')], 33, 40, 'A')
bw_block('S13-G', 'S13', 42, [('B', 'K'), ('L', 'U'), ('V', 'AE')], 43, 50, 'A')
header_cols_block('S13-H', 'S13', 52, cols('A', 'D'), 53, 57, unit='% IgG+ in B220+ MLN', time='not stated')
header_cols_block('S13-I', 'S13', 52, cols('F', 'J'), 53, 57, unit='IgG titre CA09 (boost)', time='d28')
header_cols_block('S13-J', 'S13', 52, cols('L', 'P'), 53, 57, unit='IgG titre Aichi (boost)', time='d28')
# ================= S14 =================
header_cols_block('S14-A_H1N1', 'S14', 2, cols('A', 'D'), 3, 7, unit='% IFNg+ CD8 MLN (H1N1 restim)', time='not stated')
header_cols_block('S14-A_H3N2', 'S14', 2, cols('F', 'I'), 3, 7, unit='% IFNg+ CD8 MLN (H3N2 restim)', time='not stated')
# ================= S15 =================
four = [('B', 'H'), ('I', 'O'), ('P', 'V'), ('W', 'AC')]
five = four + [('AD', 'AJ')]
bw_block('S15-A', 'S15', 2, four, 3, 10, 'A')
bw_block('S15-B', 'S15', 12, four, 13, 20, 'A')
bw_block('S15-C', 'S15', 22, four, 23, 30, 'A')
bw_block('S15-D', 'S15', 32, four, 33, 40, 'A')
bw_block('S15-E', 'S15', 42, five, 43, 50, 'A')
bw_block('S15-F', 'S15', 52, five, 53, 60, 'A')
bw_block('S15-G', 'S15', 62, five, 63, 70, 'A')
survival_block('S15-H', 'S15', 72, 'A', cols('B', 'D'), 73, 93)
bw_block('S15-I', 'S15', 71, [('I', 'O'), ('P', 'V'), ('W', 'AC')], 72, 79, 'H')
bw_block('S15-J', 'S15', 82, [('I', 'O'), ('P', 'V'), ('W', 'AC'), ('AD', 'AJ')], 83, 90, 'H')
bw_block('S15-K', 'S15', 92, [('I', 'O'), ('P', 'V'), ('W', 'AC'), ('AD', 'AJ')], 93, 100, 'H')
survival_block('S15-L', 'S15', 102, 'A', cols('B', 'E'), 103, 130)
bw_block('S15-M', 'S15', 102, [('I', 'O'), ('P', 'V'), ('W', 'AC'), ('AD', 'AJ')], 103, 110, 'H')
survival_block('S15-N', 'S15', 133, 'A', cols('B', 'E'), 134, 161)
bw_block('S15-O', 'S15', 133, [('I', 'O'), ('P', 'V'), ('W', 'AC'), ('AD', 'AJ')], 134, 141, 'H')

vals = pd.DataFrame(VAL); surv = pd.DataFrame(SURV); bw = pd.DataFrame(BW)
vals.to_csv('/tmp/work/values.csv', index=False)
surv.to_csv('/tmp/work/survival.csv', index=False)
bw.to_csv('/tmp/work/bw.csv', index=False)
print(len(vals), len(surv), len(bw))

# coverage check: every numeric cell in the workbook must be accounted for (either as value, survival day/event, bw, or header/time/dose label)
used = set(vals.cell) | set(surv.cell_day) | set(surv.cell_event) | set(bw.cell)
unused = []
for ws in WB.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, (int, float)) and f"{ws.title}!{c.coordinate}" not in used:
                unused.append(f"{ws.title}!{c.coordinate}={c.value}")
print('numeric cells not captured:', len(unused))
print(unused)
