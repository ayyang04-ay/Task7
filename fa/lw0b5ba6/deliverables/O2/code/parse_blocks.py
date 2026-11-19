"""
Explicit, cell-addressed parser for psln_program_dataset.xlsx.
Every block is defined by sheet + cell ranges so that every number can be traced to a cell.
Output: /tmp/work/tidy.csv (one row per observation, with source cell) and survival.csv
"""
import openpyxl, re, json
import pandas as pd
from openpyxl.utils import column_index_from_string as ci, get_column_letter as cl

WB = openpyxl.load_workbook('/tmp/world/filesystem/psln_program_dataset.xlsx', data_only=True)
rows_out = []   # continuous / per-animal values
surv_out = []   # time-to-event
bw_out = []     # body weight trajectories (per animal)


def v(ws, col, row):
    return ws[f"{col}{row}"].value


def add(block, sheet, group, value, cell, **kw):
    if value is None:
        return
    d = dict(block=block, sheet=sheet, group=group, value=float(value), cell=f"{sheet}!{cell}")
    d.update(kw)
    rows_out.append(d)


def col_groups_rows(block, sheet, header_row, cols, rows, labels=None, **kw):
    """groups in columns (header in header_row), replicates down rows"""
    ws = WB[sheet]
    for c in cols:
        g = labels[c] if labels else v(ws, c, header_row)
        for r in rows:
            add(block, sheet, str(g).strip(), v(ws, c, r), f"{c}{r}", rep=r - rows[0] + 1, **kw)


def row_groups_cols(block, sheet, label_col, rows, cols, **kw):
    """groups in rows (label in label_col), replicates across columns"""
    ws = WB[sheet]
    for r in rows:
        g = v(ws, label_col, r)
        for i, c in enumerate(cols):
            add(block, sheet, str(g).strip(), v(ws, c, r), f"{c}{r}", rep=i + 1, **kw)


def span(a, b):
    return [cl(i) for i in range(ci(a), ci(b) + 1)]


def wide_time_block(block, sheet, header_row, time_col, rows, group_starts, width, kind='value', **kw):
    """header row holds group name at first column of each group span; time in time_col; width reps per group"""
    ws = WB[sheet]
    for gstart in group_starts:
        g = str(v(ws, gstart, header_row)).strip()
        cols = span(gstart, cl(ci(gstart) + width - 1))
        for r in rows:
            t = v(ws, time_col, r)
            for i, c in enumerate(cols):
                val = v(ws, c, r)
                if kind == 'bw':
                    if val is not None:
                        bw_out.append(dict(block=block, sheet=sheet, group=g, animal=i + 1, day=float(t), value=float(val), cell=f"{sheet}!{c}{r}"))
                else:
                    add(block, sheet, g, val, f"{c}{r}", rep=i + 1, time=str(t).strip(), **kw)


def surv_block(block, sheet, header_row, day_col, group_cols, rows, labels=None):
    ws = WB[sheet]
    for c in group_cols:
        g = labels[c] if labels else str(v(ws, c, header_row)).strip()
        for r in rows:
            st = v(ws, c, r)
            if st is None:
                continue
            d = v(ws, day_col, r)
            surv_out.append(dict(block=block, sheet=sheet, group=g, day=(None if d is None else float(d)), event=int(st), cell=f"{sheet}!{c}{r}", daycell=f"{sheet}!{day_col}{r}"))


# ---------------- S01 ----------------
row_groups_cols('S01-A_16h', 'S01', 'A', range(3, 11), span('B', 'F'), time='16h', measure='Ifnb1 fold (lung)')
row_groups_cols('S01-A_72h', 'S01', 'G', range(3, 11), span('H', 'L'), time='72h', measure='Ifnb1 fold (lung)')
row_groups_cols('S01-B', 'S01', 'A', range(14, 18), span('B', 'F'), measure='% SRB+ AEC')
row_groups_cols('S01-C', 'S01', 'A', range(20, 22), span('B', 'E'), measure='% DiD+ AM')
wide_time_block('S01-D', 'S01', 23, 'A', range(24, 29), ['B', 'G', 'L', 'Q'], 5, measure='% lung monocytes')
wide_time_block('S01-E', 'S01', 29, 'A', range(30, 35), ['B', 'G', 'L', 'Q', 'V'], 5, measure='% lung CD11b+ DC')
for blk, hr, r in [('S01-F', 35, 36), ('S01-G', 37, 38)]:
    ws = WB['S01']
    for gs in ['B', 'G', 'L', 'Q', 'V']:
        g = v(ws, gs, hr)
        for i, c in enumerate(span(gs, cl(ci(gs) + 4))):
            add(blk, 'S01', g, v(ws, c, r), f"{c}{r}", rep=i + 1, measure='% cDC1' if blk == 'S01-F' else '% cDC2')

# ---------------- S02 ----------------
col_groups_rows('S02-A', 'S02', 2, span('A', 'D'), range(3, 8), measure='% CCR7+ migratory CD11b+ DC (lung)')
col_groups_rows('S02-B', 'S02', 2, span('F', 'I'), range(3, 8), measure='% MLN CD11b+CD103- DC')
col_groups_rows('S02-C', 'S02', 2, span('K', 'O'), range(3, 8), measure='% MLN DC AF647-OVA+')
col_groups_rows('S02-D_CD40', 'S02', 9, span('A', 'D'), range(10, 15), measure='% CD40+ MLN CD11b+ DC')
col_groups_rows('S02-D_CD86', 'S02', 9, span('F', 'I'), range(10, 15), measure='% CD86+ MLN CD11b+ DC')
col_groups_rows('S02-E', 'S02', 9, span('K', 'O'), range(10, 15), measure='% OT-I proliferation')
wide_time_block('S02-F', 'S02', 16, 'A', range(17, 20), ['B', 'G', 'L'], 5, measure='Gm-csf fold (lung)')
col_groups_rows('S02-G', 'S02', 21, span('B', 'D'), range(22, 27), measure='% Ly6C+ moDC-like')
col_groups_rows('S02-H', 'S02', 29, span('B', 'F'), range(30, 35), measure='% CD45.2+ moDC')
col_groups_rows('S02-I', 'S02', 29, span('H', 'I'), range(30, 35), measure='% GZMB+ CD8 (lung)')

# ---------------- S03 ----------------
col_groups_rows('S03-A', 'S03', 2, span('A', 'E'), range(3, 8), measure='IgG CA09 titre d14')
col_groups_rows('S03-B', 'S03', 2, span('G', 'I'), range(3, 8), measure='IgG2a/IgG1 CA09 d14')
col_groups_rows('S03-C', 'S03', 2, span('K', 'O'), range(3, 8), measure='HAI CA09 d14')
col_groups_rows('S03-D', 'S03', 2, span('Q', 'U'), range(3, 8), measure='Neut CA09 d14')
col_groups_rows('S03-E', 'S03', 9, span('A', 'E'), range(10, 15), measure='IgG Aichi titre d14')
col_groups_rows('S03-F', 'S03', 9, span('G', 'I'), range(10, 15), measure='IgG2a/IgG1 Aichi d14')
col_groups_rows('S03-G', 'S03', 9, span('K', 'O'), range(10, 15), measure='HAI Aichi d14')
col_groups_rows('S03-H', 'S03', 9, span('Q', 'U'), range(10, 15), measure='Neut Aichi d14')
surv_block('S03-I', 'S03', 16, 'A', span('B', 'F'), range(17, 52))
surv_block('S03-J', 'S03', 16, 'G', span('H', 'J'), range(17, 47))
col_groups_rows('S03-K', 'S03', 16, span('L', 'O'), range(17, 22), measure='% GC B (MLN) d7')
ws = WB['S03']
for r in range(26, 29):
    g = v(ws, 'K', r)
    for i, c in enumerate(['L', 'M', 'N']):
        add('S03-L_Aicda', 'S03', g, v(ws, c, r), f"{c}{r}", rep=i + 1, measure='Aicda fold (MLN B) d5')
    for i, c in enumerate(['O', 'P', 'Q']):
        add('S03-L_E47', 'S03', g, v(ws, c, r), f"{c}{r}", rep=i + 1, measure='E47 fold (MLN B) d5')

# ---------------- S04 ----------------
row_groups_cols('S04-A_ICOSlo', 'S04', 'A', range(2, 6), span('B', 'F'), measure='% Tfh ICOS-lo')
row_groups_cols('S04-A_ICOShi', 'S04', 'A', range(2, 6), span('G', 'K'), measure='% Tfh ICOS-hi')
col_groups_rows('S04-B_Tfr', 'S04', 7, span('A', 'D'), range(8, 13), measure='% Tfr d7')
col_groups_rows('S04-B_TfhTfr', 'S04', 14, span('A', 'D'), range(15, 20), measure='Tfh:Tfr d7')
col_groups_rows('S04-C', 'S04', 21, span('A', 'D'), range(22, 27), measure='% Tfr d30')
col_groups_rows('S04-D', 'S04', 28, span('A', 'D'), range(29, 32), measure='% lung Treg d7')

# ---------------- S05 ----------------
wide_time_block('S05-A', 'S05', 2, 'A', range(3, 6), ['B', 'E', 'H'], 2, measure='% NP366 tet+ CD8 (lung)')
wide_time_block('S05-B', 'S05', 7, 'A', range(8, 11), ['B', 'E', 'H'], 2, measure='% NP366 tet+ CD8 (MLN)')
col_groups_rows('S05-C', 'S05', 12, span('A', 'D'), range(13, 16), measure='% OT-I proliferating')
col_groups_rows('S05-D', 'S05', 18, span('A', 'D'), range(19, 24), measure='% Ki67+ CD8 (lung) d3')
col_groups_rows('S05-E', 'S05', 25, span('A', 'D'), range(26, 31), measure='% GZMB+ CD8 (lung) d3')
col_groups_rows('S05-F', 'S05', 32, span('A', 'D'), range(33, 38), measure='% IFNg+ CD8 (MLN) d14, H5 restim')
col_groups_rows('S05-G', 'S05', 39, span('A', 'D'), range(40, 45), measure='% IFNg+ CD8 (MLN) d60, H5 restim')
col_groups_rows('S05-H', 'S05', 46, span('A', 'D'), range(47, 52), measure='% GZMB+ CD8 (MLN) d60')
col_groups_rows('S05-I', 'S05', 53, span('A', 'D'), range(54, 59), measure='% lung TRM CD8 d25')

# ---------------- S06 survival ----------------
surv_block('S06-A', 'S06', 2, 'A', span('B', 'E'), range(3, 31))
surv_block('S06-B', 'S06', 2, 'G', span('H', 'K'), range(3, 31))
surv_block('S06-C', 'S06', 2, 'M', span('N', 'Q'), range(3, 31))
surv_block('S06-D', 'S06', 33, 'A', span('B', 'E'), range(34, 62))
surv_block('S06-E_r34', 'S06', 33, 'G', span('H', 'L'), range(34, 69))
surv_block('S06-F_r34', 'S06', 33, 'M', span('N', 'R'), range(34, 69))
surv_block('S06-G', 'S06', 70, 'A', span('B', 'F'), range(71, 106))
surv_block('S06-E_r71', 'S06', 70, 'G', span('H', 'K'), range(71, 106))
surv_block('S06-F_r71', 'S06', 70, 'M', span('N', 'Q'), range(71, 106))

# ---------------- S07 ----------------
wide_time_block('S07-A', 'S07', 2, 'A', range(3, 8), ['B', 'E'], 3, measure='Ly6C+CCR2+ Mphi count x1e5')
ws = WB['S07']
for c, g, cell_pop in [('B', 'PSLN-344', 'Mono'), ('C', 'PSLN-344+INCB3344', 'Mono'), ('E', 'PSLN-344', 'Ly6C+Mphi'), ('F', 'PSLN-344+INCB3344', 'Ly6C+Mphi')]:
    for r in range(10, 15):
        add(f'S07-B_{cell_pop}', 'S07', g, v(ws, c, r), f"{c}{r}", rep=r - 9, measure=f'% {cell_pop}')
for c, g in [('B', 'colB "Ly6C-CD206+ MPhi"'), ('C', 'colC "Ly6C-CD206+ MPhi"')]:
    for r in range(16, 21):
        add('S07-C', 'S07', g, v(ws, c, r), f"{c}{r}", rep=r - 15, measure='% lung Treg after Mphi transfer')

# ---------------- S08 ----------------
wide_time_block('S08-A', 'S08', 2, 'A', range(3, 8), ['B', 'E', 'H', 'K'], 3, measure='Ifnb1 fold by dose (ug)')
ws = WB['S08']
for gs in ['A', 'D', 'G', 'J', 'M']:
    g = v(ws, gs, 10)
    for i, c in enumerate(span(gs, cl(ci(gs) + 2))):
        add('S08-B', 'S08', g, v(ws, c, 11), f"{c}11", rep=i + 1, measure='EE % (A260)')
col_groups_rows('S08-C', 'S08', 13, span('A', 'D'), range(14, 19), measure='% SRB+ AEC')
wide_time_block('S08-D', 'S08', 20, 'A', range(21, 27), ['B', 'G', 'L', 'Q', 'V', 'AA'], 5, kind='bw')
surv_block('S08-unlabelled', 'S08', None, 'A', ['C', 'D'], range(89, 102), labels={'C': 'unlabelled colC', 'D': 'unlabelled colD'})

# ---------------- S09 ----------------
ws = WB['S09']
for blk, starts in [('S09-A_blk1(B:V)', ['B', 'E', 'H', 'K', 'N', 'Q', 'T']), ('S09-A_blk2(Y:AS)', ['Y', 'AB', 'AE', 'AH', 'AK', 'AN', 'AQ'])]:
    for gs in starts:
        g = str(v(ws, gs, 2)).strip()
        for r in range(3, 10):
            an = v(ws, 'A', r)
            for i, c in enumerate(span(gs, cl(ci(gs) + 2))):
                add(blk, 'S09', g, v(ws, c, r), f"{c}{r}", rep=i + 1, analyte=an, measure='log10 fold')
surv_block('S09-B', 'S09', 11, 'A', span('B', 'D'), range(12, 36))
wide_time_block('S09-C', 'S09', 11, 'F', range(12, 20), ['G', 'O', 'W'], 8, kind='bw')
surv_block('S09-D', 'S09', 38, 'A', span('B', 'D'), range(39, 63))
wide_time_block('S09-E', 'S09', 38, 'F', range(39, 47), ['G', 'O', 'W'], 8, kind='bw')
surv_block('S09-F', 'S09', 65, 'A', span('B', 'D'), range(66, 89))
wide_time_block('S09-G', 'S09', 65, 'F', range(66, 74), ['G', 'O', 'W'], 8, kind='bw')

# ---------------- S10 ----------------
col_groups_rows('S10-A_Ifnb1', 'S10', 2, span('A', 'D'), range(3, 8), measure='CNS Ifnb1 fold 36h')
col_groups_rows('S10-A_Tnf', 'S10', 2, span('F', 'I'), range(3, 8), measure='CNS Tnf fold 36h')
col_groups_rows('S10-A_Isg15', 'S10', 2, span('K', 'N'), range(3, 8), measure='CNS Isg15 fold 36h')

# ---------------- S11 ----------------
wide_time_block('S11-A', 'S11', 2, 'A', range(3, 8), ['B', 'G', 'L', 'Q'], 5, measure='% alveolar macrophages')
wide_time_block('S11-B', 'S11', 9, 'A', range(10, 15), ['B', 'G', 'L', 'Q'], 5, measure='% neutrophils')
col_groups_rows('S11-C', 'S11', 16, span('A', 'B'), range(17, 22), measure='% recruited monocytes d3')
wide_time_block('S11-D', 'S11', 23, 'A', range(24, 29), ['B', 'G', 'L', 'Q'], 5, measure='% NK cells')
col_groups_rows('S11-E', 'S11', 30, span('A', 'D'), range(31, 36), measure='% CD206+ macrophages')

# ---------------- S12 ----------------
col_groups_rows('S12-A', 'S12', 2, span('A', 'B'), range(3, 6), measure='% CD45.2+ monocytes')

# ---------------- S13 ----------------
col_groups_rows('S13-A', 'S13', 2, span('A', 'C'), range(3, 8), measure='IgG2a CA09 d14')
col_groups_rows('S13-B', 'S13', 2, span('E', 'G'), range(3, 8), measure='IgG1 CA09 d14')
col_groups_rows('S13-C', 'S13', 2, span('I', 'K'), range(3, 8), measure='IgG2a Aichi d14')
col_groups_rows('S13-D', 'S13', 2, span('M', 'O'), range(3, 8), measure='IgG1 Aichi d14')
surv_block('S13-E', 'S13', 2, 'R', span('S', 'V'), range(3, 31))
wide_time_block('S13-F', 'S13', 32, 'A', range(33, 41), ['B', 'I', 'P', 'W', 'AD'], 7, kind='bw')
wide_time_block('S13-G', 'S13', 42, 'A', range(43, 51), ['B', 'L', 'V'], 10, kind='bw')
col_groups_rows('S13-H', 'S13', 52, span('A', 'D'), range(53, 58), measure='% IgG+ of B220+ MLN')
col_groups_rows('S13-I', 'S13', 52, span('F', 'J'), range(53, 58), measure='IgG CA09 d28 (boost d14)')
col_groups_rows('S13-J', 'S13', 52, span('L', 'P'), range(53, 58), measure='IgG Aichi d28 (boost d14)')

# ---------------- S14 ----------------
col_groups_rows('S14-A_H1N1', 'S14', 2, span('A', 'D'), range(3, 8), measure='% IFNg+ CD8 MLN, H1N1 restim')
col_groups_rows('S14-A_H3N2', 'S14', 2, span('F', 'I'), range(3, 8), measure='% IFNg+ CD8 MLN, H3N2 restim')

# ---------------- S15 ----------------
for blk, hr, r0 in [('S15-A', 2, 3), ('S15-B', 12, 13), ('S15-C', 22, 23), ('S15-D', 32, 33)]:
    wide_time_block(blk, 'S15', hr, 'A', range(r0, r0 + 8), ['B', 'I', 'P', 'W'], 7, kind='bw')
for blk, hr, r0 in [('S15-E', 42, 43), ('S15-F', 52, 53), ('S15-G', 62, 63)]:
    wide_time_block(blk, 'S15', hr, 'A', range(r0, r0 + 8), ['B', 'I', 'P', 'W', 'AD'], 7, kind='bw')
surv_block('S15-H', 'S15', 72, 'A', span('B', 'D'), range(73, 94))
wide_time_block('S15-I', 'S15', 71, 'H', range(72, 80), ['I', 'P', 'W'], 7, kind='bw')
wide_time_block('S15-J', 'S15', 82, 'H', range(83, 91), ['I', 'P', 'W', 'AD'], 7, kind='bw')
wide_time_block('S15-K', 'S15', 92, 'H', range(93, 101), ['I', 'P', 'W', 'AD'], 7, kind='bw')
surv_block('S15-L', 'S15', 102, 'A', span('B', 'E'), range(103, 131))
wide_time_block('S15-M', 'S15', 102, 'H', range(103, 111), ['I', 'P', 'W', 'AD'], 7, kind='bw')
surv_block('S15-N', 'S15', 133, 'A', span('B', 'E'), range(134, 162))
wide_time_block('S15-O', 'S15', 133, 'H', range(134, 142), ['I', 'P', 'W', 'AD'], 7, kind='bw')

tidy = pd.DataFrame(rows_out)
surv = pd.DataFrame(surv_out)
bw = pd.DataFrame(bw_out)
# normalise group labels (strip, unify (y)/Y variants but keep original)
def norm(g):
    g = str(g).strip().replace('Naïve', 'Naive')
    g = re.sub(r'\(y\)$', '(Y)', g)
    g = re.sub(r'^PSLN-(\d+)Y$', r'PSLN-\1(Y)', g)
    return g
for df in (tidy, surv, bw):
    df['group_raw'] = df['group']
    df['group'] = df['group'].map(norm)
tidy.to_csv('/tmp/work/tidy.csv', index=False)
surv.to_csv('/tmp/work/survival.csv', index=False)
bw.to_csv('/tmp/work/bodyweight.csv', index=False)
print('tidy', tidy.shape, 'surv', surv.shape, 'bw', bw.shape)
print(tidy.groupby('block').size().to_string())
