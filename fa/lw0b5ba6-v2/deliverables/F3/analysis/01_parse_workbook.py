"""
01_parse_workbook.py
Parse psln_program_dataset.xlsx into explicit, cell-addressed blocks.

Every block is defined by hand from the printed layout (header row, label cells, value
ranges) so that each number can be traced back to a sheet / cell range.
Nothing is cleaned, imputed or relabelled here: values and labels are taken "as printed".

Output: parsed_blocks.json  (dict: block_id -> metadata + per-group values)
Run with:  micromamba run -n chem python 01_parse_workbook.py
"""
import json, sys, re
import openpyxl
from openpyxl.utils import get_column_letter as L, column_index_from_string as CI

SRC = '/tmp/world/filesystem/psln_program_dataset.xlsx'
OUT = '/tmp/work/parsed/parsed_blocks.json'
wb = openpyxl.load_workbook(SRC, data_only=True)

def cell(ws, col, row):
    return ws[f'{col}{row}'].value

def colrange(c0, c1):
    return [L(i) for i in range(CI(c0), CI(c1) + 1)]

blocks = {}

def add(block_id, **kw):
    assert block_id not in blocks, block_id
    blocks[block_id] = kw

# ---------------------------------------------------------------- helpers
def columns_block(sheet, block_id, label_row, cols, r0, r1, stated_n=None, **meta):
    """One group per column, replicates down rows r0..r1. cols = list of column letters."""
    ws = wb[sheet]
    groups, cells = {}, {}
    order = []
    for c in cols:
        lab = cell(ws, c, label_row)
        lab = str(lab).strip() if lab is not None else f'(blank {c}{label_row})'
        key = lab
        k = 2
        while key in groups:          # duplicate printed label -> keep both, mark position
            key = f'{lab} [col {c}]'
            k += 1
        vals = [cell(ws, c, r) for r in range(r0, r1 + 1)]
        groups[key] = [v for v in vals if v is not None]
        cells[key] = f'{sheet}!{c}{r0}:{c}{r1}'
        order.append(key)
    add(block_id, sheet=sheet, kind='columns', order=order, groups=groups, cells=cells,
        stated_n=stated_n, **meta)

def rows_block(sheet, block_id, label_col, c0, c1, r0, r1, stated_n=None, **meta):
    """One group per row (label in label_col), replicates across c0..c1."""
    ws = wb[sheet]
    groups, cells, order = {}, {}, []
    for r in range(r0, r1 + 1):
        lab = str(cell(ws, label_col, r)).strip()
        vals = [cell(ws, c, r) for c in colrange(c0, c1)]
        groups[lab] = [v for v in vals if v is not None]
        cells[lab] = f'{sheet}!{c0}{r}:{c1}{r}'
        order.append(lab)
    add(block_id, sheet=sheet, kind='rows', order=order, groups=groups, cells=cells,
        stated_n=stated_n, **meta)

def wide_time_block(sheet, block_id, header_row, time_col, spans, r0, r1, stated_n=None, **meta):
    """Time in rows (time_col), each group spans several replicate columns.
    spans = list of (first_col, last_col); group label is read from first_col at header_row.
    Stored as groups[label] = {time: [values-with-None-for-blank]} so blanks are preserved."""
    ws = wb[sheet]
    groups, cells, order = {}, {}, []
    times = [cell(ws, time_col, r) for r in range(r0, r1 + 1)]
    for (c0, c1) in spans:
        lab = str(cell(ws, c0, header_row)).strip()
        d = {}
        for r, t in zip(range(r0, r1 + 1), times):
            d[str(t)] = [cell(ws, c, r) for c in colrange(c0, c1)]
        groups[lab] = d
        cells[lab] = f'{sheet}!{c0}{r0}:{c1}{r1}'
        order.append(lab)
    add(block_id, sheet=sheet, kind='wide_time', order=order, groups=groups, cells=cells,
        times=[str(t) for t in times], stated_n=stated_n, **meta)

def survival_block(sheet, block_id, header_row, day_col, group_cols, r0, r1, stated_n=None, **meta):
    """Long-format time-to-event: one row per animal; day in day_col; the animal's group column holds 1/0."""
    ws = wb[sheet]
    labels = {c: str(cell(ws, c, header_row)).strip() for c in group_cols}
    groups = {lab: [] for lab in labels.values()}
    order = list(labels.values())
    rowsrec = []
    for r in range(r0, r1 + 1):
        day = cell(ws, day_col, r)
        flags = {c: cell(ws, c, r) for c in group_cols}
        present = [c for c, v in flags.items() if v is not None]
        if day is None and not present:
            continue
        assert len(present) == 1, (block_id, r, flags)
        c = present[0]
        groups[labels[c]].append({'row': r, 'day': day, 'event': flags[c]})
    cells = {lab: f'{sheet}!{day_col}{r0}:{day_col}{r1} + {c}{r0}:{c}{r1}' for c, lab in labels.items()}
    add(block_id, sheet=sheet, kind='survival', order=order, groups=groups, cells=cells,
        stated_n=stated_n, **meta)

# ================================================================ S01
rows_block('S01', 'S01-A_16h', 'A', 'B', 'F', 3, 10, 5, measurand='Ifnb1 mRNA, total lung, fold vs untreated (linear)', time='16 h', vaccine='none')
rows_block('S01', 'S01-A_72h', 'G', 'H', 'L', 3, 10, 5, measurand='Ifnb1 mRNA, total lung, fold vs untreated (linear)', time='72 h', vaccine='none')
rows_block('S01', 'S01-B', 'A', 'B', 'F', 14, 17, 5, measurand='% SRB+ alveolar epithelial cells', time='16 h')
rows_block('S01', 'S01-C', 'A', 'B', 'E', 20, 21, 4, measurand='% DiD+ alveolar macrophages', time='16 h')
wide_time_block('S01', 'S01-D', 23, 'A', [('B','F'),('G','K'),('L','P'),('Q','U')], 24, 28, 5, measurand='% lung monocytes (CD11b+Ly6C+)', vaccine='CA09 H1N1')
wide_time_block('S01', 'S01-E', 29, 'A', [('B','F'),('G','K'),('L','P'),('Q','U'),('V','Z')], 30, 34, 5, measurand='% lung CD11b+ DC', vaccine='CA09 H1N1')
for bid, hr, vr, meas in [('S01-F', 35, 36, '% lung cDC1 (XCR1+CD172a-)'), ('S01-G', 37, 38, '% lung cDC2 (XCR1-CD172a+)')]:
    ws = wb['S01']; groups = {}; cells = {}; order = []
    for c0, c1 in [('B','F'),('G','K'),('L','P'),('Q','U'),('V','Z')]:
        lab = str(cell(ws, c0, hr)).strip()
        groups[lab] = [cell(ws, c, vr) for c in colrange(c0, c1) if cell(ws, c, vr) is not None]
        cells[lab] = f'S01!{c0}{vr}:{c1}{vr}'; order.append(lab)
    add(bid, sheet='S01', kind='rows', order=order, groups=groups, cells=cells, stated_n=5, measurand=meas, time='72 h', vaccine='bivalent')

# ================================================================ S02
columns_block('S02', 'S02-A', 2, list('ABCD'), 3, 7, 5, measurand='% CCR7+ of lung CD11b+ DC', time='72 h', vaccine='CA09 H1N1')
columns_block('S02', 'S02-B', 2, list('FGHI'), 3, 7, 5, measurand='% MLN CD11b+CD103- DC', time='72 h', vaccine='CA09 H1N1')
columns_block('S02', 'S02-C', 2, list('KLMNO'), 3, 7, 5, measurand='% OVA-AF647+ MLN DC', time='36 h', vaccine='OVA-AF647')
columns_block('S02', 'S02-D_CD40', 9, list('ABCD'), 10, 14, 5, measurand='% CD40+ of MLN CD11b+ DC', time='d3', vaccine='CA09 H1N1')
columns_block('S02', 'S02-D_CD86', 9, list('FGHI'), 10, 14, 5, measurand='% CD86+ of MLN CD11b+ DC', time='d3', vaccine='CA09 H1N1')
columns_block('S02', 'S02-E', 9, list('KLMNO'), 10, 14, 5, measurand='% proliferated OT-I (ex vivo MLN CD11b+ DC co-culture)', time='DC d3, read d3', vaccine='OVA')
wide_time_block('S02', 'S02-F', 16, 'A', [('B','F'),('G','K'),('L','P')], 17, 19, 5, measurand='Gm-csf mRNA lung, fold vs untreated (linear)', vaccine='bivalent')
columns_block('S02', 'S02-G', 21, list('BCD'), 22, 26, 5, measurand='% lung Ly6C+CD11c+MHC-II+ F4/80-/int (moDC)', time='d5', vaccine='bivalent')
columns_block('S02', 'S02-H', 29, list('BCDEF'), 30, 34, 5, measurand='% CD45.2+ monocyte-derived DC', time='d3', vaccine='bivalent + PSLN-344')
columns_block('S02', 'S02-I', 29, list('HI'), 30, 34, 5, measurand='% lung GZMB+ CD8 T', time='d5', vaccine='bivalent + PSLN-344')

# ================================================================ S03
for bid, cols, hr, r0, meas in [
    ('S03-A', list('ABCDE'), 2, 3, 'serum IgG anti-CA09 H1N1 (endpoint titre)'),
    ('S03-B', list('GHI'),   2, 3, 'IgG2a/IgG1 quotient, CA09 H1N1'),
    ('S03-C', list('KLMNO'), 2, 3, 'HAI titre, CA09 H1N1 (LLOQ 10)'),
    ('S03-D', list('QRSTU'), 2, 3, 'neutralising titre, CA09 H1N1'),
    ('S03-E', list('ABCDE'), 9, 10, 'serum IgG anti-Aichi H3N2 (endpoint titre)'),
    ('S03-F', list('GHI'),   9, 10, 'IgG2a/IgG1 quotient, Aichi H3N2'),
    ('S03-G', list('KLMNO'), 9, 10, 'HAI titre, Aichi H3N2 (LLOQ 10)'),
    ('S03-H', list('QRSTU'), 9, 10, 'neutralising titre, Aichi H3N2')]:
    columns_block('S03', bid, hr, cols, r0, r0 + 4, 5, measurand=meas, time='d14', vaccine='bivalent')
survival_block('S03', 'S03-I', 16, 'A', list('BCDEF'), 17, 51, 7, vaccine='(as S03-A: bivalent)', challenge='10x mLD50 CA09 H1N1', challenge_day=14, obs_days=14, strain='BALB/c aged')
survival_block('S03', 'S03-J', 16, 'G', list('HIJ'), 17, 46, 9, vaccine='rgH5N1', challenge='wild-type VN04 H5N1', challenge_day=2, obs_days=22, strain='BALB/c aged')
columns_block('S03', 'S03-K', 16, list('LMNO'), 17, 21, 5, measurand='% GC B (CXCR5+GL7+) in MLN', time='d7', vaccine='bivalent')
rows_block('S03', 'S03-L_Aicda', 'K', 'L', 'N', 26, 28, 3, measurand='Aicda mRNA MLN B cells, fold (linear)', time='d5', vaccine='bivalent')
rows_block('S03', 'S03-L_E47', 'K', 'O', 'Q', 26, 28, 3, measurand='E47 mRNA MLN B cells, fold (linear)', time='d5', vaccine='bivalent')

# ================================================================ S04
rows_block('S04', 'S04-A_ICOSlo', 'A', 'B', 'F', 2, 5, 5, measurand='% Tfh ICOS-lo (CD4+CXCR5+PD1+)', time='d7', vaccine='bivalent')
rows_block('S04', 'S04-A_ICOShi', 'A', 'G', 'K', 2, 5, 5, measurand='% Tfh ICOS-hi (CD4+CXCR5+PD1+)', time='d7', vaccine='bivalent')
columns_block('S04', 'S04-B_Foxp3', 7, list('ABCD'), 8, 12, 5, measurand='% Tfr (Foxp3+ in CXCR5+ICOShi CD4)', time='d7', vaccine='bivalent')
columns_block('S04', 'S04-B_TfhTfr', 14, list('ABCD'), 15, 19, 5, measurand='Tfh:Tfr quotient', time='d7', vaccine='bivalent')
columns_block('S04', 'S04-C', 21, list('ABCD'), 22, 26, 5, measurand='% Tfr (Foxp3+ in CXCR5+ICOShi CD4)', time='d30', vaccine='bivalent')
columns_block('S04', 'S04-D', 28, list('ABCD'), 29, 31, 3, measurand='% lung Treg (CD4+Foxp3+)', time='d7', vaccine='bivalent')

# ================================================================ S05
wide_time_block('S05', 'S05-A', 2, 'A', [('B','C'),('E','F'),('H','I')], 3, 5, 3, measurand='% NP366-374 tetramer+ of lung CD8 T')
wide_time_block('S05', 'S05-B', 7, 'A', [('B','C'),('E','F'),('H','I')], 8, 10, 3, measurand='% NP366-374 tetramer+ of MLN CD8 T')
columns_block('S05', 'S05-C', 12, list('ABCD'), 13, 15, 3, measurand='% proliferating OT-I (in vivo)', time='d4', vaccine='OVA + PSLN-344')
for bid, hr, meas, tm in [('S05-D', 18, '% Ki-67+ lung CD8 T', 'd3'), ('S05-E', 25, '% GZMB+ lung CD8 T', 'd3'),
                          ('S05-F', 32, '% IFN-g+ CD8 T in MLN, rgH5N1 restim', 'd14'), ('S05-G', 39, '% IFN-g+ CD8 T in MLN, rgH5N1 restim', 'd60'),
                          ('S05-H', 46, '% GZMB+ CD8 T in MLN', 'd60'), ('S05-I', 53, '% lung CD8 TRM (CD69+CD103+)', 'd25')]:
    columns_block('S05', bid, hr, list('ABCD'), hr + 1, hr + 5, 5, measurand=meas, time=tm, vaccine='bivalent')

# ================================================================ S06 (all time-to-event)
survival_block('S06', 'S06-A', 2, 'A', list('BCDE'), 3, 30, 7, vaccine='Aichi H3N2', challenge='5x mLD50 PR8 H1N1', challenge_day=14, obs_days=14, strain='BALB/c aged')
survival_block('S06', 'S06-B', 2, 'G', list('HIJK'), 3, 30, 7, vaccine='Aichi H3N2', challenge='5x mLD50 PR8 H1N1', challenge_day=3, obs_days=14, strain='BALB/c aged')
survival_block('S06', 'S06-C', 2, 'M', list('NOPQ'), 3, 30, 7, vaccine='bivalent', challenge='5x mLD50 rgH5N1', challenge_day=14, obs_days=14, strain='BALB/c aged')
survival_block('S06', 'S06-D', 33, 'A', list('BCDE'), 34, 61, 7, vaccine='bivalent', challenge='5x mLD50 rgH5N1', challenge_day=3, obs_days=14, strain='BALB/c aged')
survival_block('S06', 'S06-E_r34', 33, 'G', list('HIJKL'), 34, 68, 7, vaccine='Aichi H3N2', challenge='5x mLD50 PR8 H1N1', challenge_day=60, obs_days=14, strain='BALB/c aged')
survival_block('S06', 'S06-F_r34', 33, 'M', list('NOPQR'), 34, 68, 7, vaccine='bivalent', challenge='5x mLD50 rgH5N1', challenge_day=60, obs_days=14, strain='BALB/c aged')
survival_block('S06', 'S06-G', 70, 'A', list('BCDEF'), 71, 105, 7, vaccine='CA09 H1N1', challenge='5x mLD50 Perth H3N2', challenge_day=60, obs_days=14, strain='BALB/c aged')
survival_block('S06', 'S06-E_r71', 70, 'G', list('HIJK'), 71, 98, 7, vaccine='bivalent (after PR8 imprinting or saline at 10 mo)', challenge='5x LD50 PR8 H1N1', challenge_day=None, obs_days=14, strain='BALB/c 14 mo at vaccination')
survival_block('S06', 'S06-F_r71', 70, 'M', list('NOPQ'), 71, 98, 7, vaccine='bivalent (after PR8 imprinting or saline at 10 mo)', challenge='5x LD50 Perth H3N2', challenge_day=14, obs_days=14, strain='BALB/c 14 mo at vaccination')

# ================================================================ S07
wide_time_block('S07', 'S07-A', 2, 'A', [('B','D'),('E','G')], 3, 7, 3, measurand='lung Ly6C+CCR2+ macrophages, count x10^5', vaccine='bivalent')
columns_block('S07', 'S07-B_mono', 9, list('BC'), 10, 14, 5, measurand='% lung CD11b+Ly6C+ monocytes', vaccine='bivalent + PSLN-344')
columns_block('S07', 'S07-B_mac', 9, list('EF'), 10, 14, 5, measurand='% lung Ly6C+ macrophages', vaccine='bivalent + PSLN-344')
columns_block('S07', 'S07-C', 15, list('BC'), 16, 20, 5, measurand='% lung Treg after macrophage transfer', time='d4 after transfer')

# ================================================================ S08
wide_time_block('S08', 'S08-A', 2, 'A', [('B','D'),('E','G'),('H','J'),('K','M')], 3, 7, 3, measurand='Ifnb1 mRNA lung 16 h, fold (linear), by dose ug', vaccine='none')
ws = wb['S08']; groups = {}; cells = {}; order = []
for c0, c1 in [('A','C'),('D','F'),('G','I'),('J','L'),('M','O')]:
    lab = str(cell(ws, c0, 10)).strip(); groups[lab] = [cell(ws, c, 11) for c in colrange(c0, c1)]
    cells[lab] = f'S08!{c0}11:{c1}11'; order.append(lab)
add('S08-B', sheet='S08', kind='rows', order=order, groups=groups, cells=cells, stated_n=3, measurand='encapsulation efficiency %')
columns_block('S08', 'S08-C', 13, list('ABCD'), 14, 18, 5, measurand='% SRB+ alveolar epithelial cells', time='16 h')
wide_time_block('S08', 'S08-D', 20, 'A', [('B','F'),('G','K'),('L','P'),('Q','U'),('V','Z'),('AA','AE')], 21, 26, 5, measurand='body weight % of d0 after immunisation', vaccine='CA09 H1N1')
orph = {f'{c}{r}': cell(ws, c, r) for r in range(89, 102) for c in 'ABCD' if cell(ws, c, r) is not None}
add('S08-orphan_r89-101', sheet='S08', kind='orphan', cells_raw=orph, stated_n=None, measurand='NOT STATED (unlabelled region)')

# ================================================================ S09
ws = wb['S09']
for bid, lab_col, spans in [('S09-A_panel1', 'A', [('B','D'),('E','G'),('H','J'),('K','M'),('N','P'),('Q','S'),('T','V')]),
                            ('S09-A_panel2', 'X', [('Y','AA'),('AB','AD'),('AE','AG'),('AH','AJ'),('AK','AM'),('AN','AP'),('AQ','AS')])]:
    groups = {}; cells = {}; order = []
    for c0, c1 in spans:
        lab = str(cell(ws, c0, 2)).strip(); d = {}
        for r in range(3, 10):
            d[str(cell(ws, lab_col, r))] = [cell(ws, c, r) for c in colrange(c0, c1)]
        groups[lab] = d; cells[lab] = f'S09!{c0}3:{c1}9'; order.append(lab)
    add(bid, sheet='S09', kind='wide_analyte', order=order, groups=groups, cells=cells, stated_n=3,
        analytes=[str(cell(ws, lab_col, r)) for r in range(3, 10)],
        printed_label=str(cell(ws, 'A' if lab_col == 'A' else 'X', 1)),
        measurand='lung cytokine mRNA, log10 fold vs untreated', vaccine='none')
w3 = [('G','N'),('O','V'),('W','AD')]
survival_block('S09', 'S09-B', 11, 'A', list('BCD'), 12, 35, 8, vaccine='Aichi H3N2', challenge='5x mLD50 PR8 H1N1', challenge_day=21, obs_days=14, strain='BALB/c young')
wide_time_block('S09', 'S09-C', 11, 'F', w3, 12, 19, 8, measurand='body weight % of d0 after challenge')
survival_block('S09', 'S09-D', 38, 'A', list('BCD'), 39, 62, 8, vaccine='CA09 H1N1', challenge='5x mLD50 Perth H3N2', challenge_day=21, obs_days=14, strain='BALB/c young')
wide_time_block('S09', 'S09-E', 38, 'F', w3, 39, 46, 8, measurand='body weight % of d0 after challenge')
survival_block('S09', 'S09-F', 65, 'A', list('BCD'), 66, 88, 8, vaccine='bivalent', challenge='5x mLD50 VN04 rgH5N1', challenge_day=180, obs_days=14, strain='BALB/c young')
wide_time_block('S09', 'S09-G', 65, 'F', w3, 66, 73, 8, measurand='body weight % of d0 after challenge')

# ================================================================ S10
columns_block('S10', 'S10-A_Ifnb1', 2, list('ABCD'), 3, 7, 5, measurand='CNS Ifnb1 mRNA fold (linear)', time='36 h', vaccine='bivalent')
columns_block('S10', 'S10-A_Tnf', 2, list('FGHI'), 3, 7, 5, measurand='CNS Tnf mRNA fold (linear)', time='36 h', vaccine='bivalent')
columns_block('S10', 'S10-A_Isg15', 2, list('KLMN'), 3, 7, 5, measurand='CNS Isg15 mRNA fold (linear)', time='36 h', vaccine='bivalent')

# ================================================================ S11
s4 = [('B','F'),('G','K'),('L','P'),('Q','U')]
wide_time_block('S11', 'S11-A', 2, 'A', s4, 3, 7, 5, measurand='% alveolar macrophages in lung', vaccine='CA09 H1N1')
wide_time_block('S11', 'S11-B', 9, 'A', s4, 10, 14, 5, measurand='% neutrophils in lung', vaccine='CA09 H1N1')
columns_block('S11', 'S11-C', 16, list('AB'), 17, 21, 5, measurand='% recruited monocytes in lung', time='d3', vaccine='CA09 H1N1 + PSLN-344')
wide_time_block('S11', 'S11-D', 23, 'A', s4, 24, 28, 5, measurand='% NK cells in lung', vaccine='CA09 H1N1')
columns_block('S11', 'S11-E', 30, list('ABCD'), 31, 35, 5, measurand='% CD206+ macrophages in lung', vaccine='CA09 H1N1')

# ================================================================ S12
columns_block('S12', 'S12-A', 2, list('AB'), 3, 5, 3, measurand='% infiltrating CD45.2+ CD11b+Ly6C+ monocytes', time='d3', vaccine='bivalent + PSLN-344')

# ================================================================ S13
columns_block('S13', 'S13-A', 2, list('ABC'), 3, 7, 5, measurand='serum IgG2a anti-CA09 H1N1 titre', time='d14', vaccine='bivalent')
columns_block('S13', 'S13-B', 2, list('EFG'), 3, 7, 5, measurand='serum IgG1 anti-CA09 H1N1 titre', time='d14', vaccine='bivalent')
columns_block('S13', 'S13-C', 2, list('IJK'), 3, 7, 5, measurand='serum IgG2a anti-Aichi H3N2 titre', time='d14', vaccine='bivalent')
columns_block('S13', 'S13-D', 2, list('MNO'), 3, 7, 5, measurand='serum IgG1 anti-Aichi H3N2 titre', time='d14', vaccine='bivalent')
survival_block('S13', 'S13-E', 2, 'R', list('STUV'), 3, 30, 5, vaccine='(as S03-I)', challenge='10x mLD50 CA09 H1N1', challenge_day=14, obs_days=14, strain='BALB/c young')
wide_time_block('S13', 'S13-F', 32, 'A', [('B','H'),('I','O'),('P','V'),('W','AC'),('AD','AJ')], 33, 40, 7, measurand='body weight % of d0 after challenge (animals of S03-I)')
wide_time_block('S13', 'S13-G', 42, 'A', [('B','K'),('L','U'),('V','AE')], 43, 50, 10, measurand='body weight % of d0 after challenge (animals of S03-J)')
columns_block('S13', 'S13-H', 52, list('ABCD'), 53, 57, 5, measurand='% IgG+ of MLN B220+ cells', vaccine='bivalent')
columns_block('S13', 'S13-I', 52, list('FGHIJ'), 53, 57, 5, measurand='serum IgG anti-CA09 H1N1 titre', time='d28 (boost d14)', vaccine='bivalent x2')
columns_block('S13', 'S13-J', 52, list('LMNOP'), 53, 57, 5, measurand='serum IgG anti-Aichi H3N2 titre', time='d28 (boost d14)', vaccine='bivalent x2')

# ================================================================ S14
columns_block('S14', 'S14-A_H1N1', 2, list('ABCD'), 3, 7, 5, measurand='% IFN-g+ CD8 T in MLN, CA09 H1N1 restim', vaccine='bivalent')
columns_block('S14', 'S14-A_H3N2', 2, list('FGHI'), 3, 7, 5, measurand='% IFN-g+ CD8 T in MLN, Aichi H3N2 restim', vaccine='bivalent')

# ================================================================ S15
g4 = [('B','H'),('I','O'),('P','V'),('W','AC')]
g5 = g4 + [('AD','AJ')]
for bid, hr, spans in [('S15-A', 2, g4), ('S15-B', 12, g4), ('S15-C', 22, g4), ('S15-D', 32, g4),
                       ('S15-E', 42, g5), ('S15-F', 52, g5), ('S15-G', 62, g5)]:
    wide_time_block('S15', bid, hr, 'A', spans, hr + 1, hr + 8, 7, measurand='body weight % of d0 after challenge')
survival_block('S15', 'S15-H', 72, 'A', list('BCD'), 73, 93, 7, vaccine='bivalent alone / PSLN-344 alone / both', challenge='5x mLD50 VN04 rgH5N1', challenge_day=3, obs_days=14, strain='BALB/c aged')
wide_time_block('S15', 'S15-I', 71, 'H', [('I','O'),('P','V'),('W','AC')], 72, 79, 7, measurand='body weight % of d0 after challenge (animals of S15-H)')
s4b = [('I','O'),('P','V'),('W','AC'),('AD','AJ')]
wide_time_block('S15', 'S15-J', 82, 'H', s4b, 83, 90, 7, measurand='body weight % of d0 after challenge (imprinting, PR8)')
wide_time_block('S15', 'S15-K', 92, 'H', s4b, 93, 100, 7, measurand='body weight % of d0 after challenge (imprinting, Perth)')
survival_block('S15', 'S15-L', 102, 'A', list('BCDE'), 103, 130, 7, vaccine='bivalent', challenge='NOT STATED', challenge_day=None, obs_days=14, strain='C57BL/6 aged (20 mo)')
wide_time_block('S15', 'S15-M', 102, 'H', s4b, 103, 110, 7, measurand='body weight % of d0 after challenge (animals of S15-L)')
survival_block('S15', 'S15-N', 133, 'A', list('BCDE'), 134, 161, 7, vaccine='bivalent', challenge='NOT STATED', challenge_day=None, obs_days=14, strain='Swiss Webster aged (20 mo)')
wide_time_block('S15', 'S15-O', 133, 'H', s4b, 134, 141, 7, measurand='body weight % of d0 after challenge (animals of S15-N)')

# ---------------------------------------------------------------- completeness check:
# every numeric cell in the workbook must belong to exactly one parsed block (or be a time/dose axis cell)
json.dump(blocks, open(OUT, 'w'), indent=1, default=str)
print('blocks parsed:', len(blocks))

tot_numeric = 0
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, (int, float)):
                tot_numeric += 1
print('numeric cells in workbook:', tot_numeric)

def count_vals(b):
    k = b['kind']; n = 0
    if k in ('columns', 'rows'):
        n = sum(len(v) for v in b['groups'].values())
    elif k in ('wide_time', 'wide_analyte'):
        n = sum(sum(1 for x in vs if x is not None) for g in b['groups'].values() for vs in g.values())
    elif k == 'survival':
        n = sum((1 if a['day'] is not None else 0) + 1 for g in b['groups'].values() for a in g)
    elif k == 'orphan':
        n = len(b['cells_raw'])
    return n
val_cells = sum(count_vals(b) for b in blocks.values())
axis_cells = 0
for bid, b in blocks.items():
    if b['kind'] == 'wide_time':
        axis_cells += sum(1 for t in b['times'] if re.fullmatch(r'-?\d+(\.\d+)?', t) and bid not in ('S01-D', 'S01-E'))
print('value cells captured:', val_cells, '| numeric axis cells (days/dose):', axis_cells, '| sum:', val_cells + axis_cells)
