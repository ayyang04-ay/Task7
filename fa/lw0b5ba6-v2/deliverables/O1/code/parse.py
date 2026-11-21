"""Parse every block of psln_program_dataset.xlsx into tidy tables with cell provenance.

Outputs (in /tmp/work/tidy):
  values.csv : scalar per-animal measurements   (block, sheet, analyte, group, time, animal, value, cell)
  tte.csv    : time-to-event rows                (block, sheet, group, animal, time, event, cell_time, cell_event)
  bw.csv     : body-weight trajectories          (block, sheet, group, animal, day, value, cell)
Block coordinates were transcribed from a full cell dump and cross-checked against the annotation PDF.
"""
import openpyxl, os, re
import pandas as pd
from openpyxl.utils import column_index_from_string as ci, get_column_letter as gl

WB = openpyxl.load_workbook('/tmp/world/filesystem/psln_program_dataset.xlsx', data_only=True)
OUT = '/tmp/work/tidy'; os.makedirs(OUT, exist_ok=True)
vals, tte, bw = [], [], []

def cell(ws, col, row):
    return ws.cell(row, ci(col) if isinstance(col, str) else col)

def span(a, b):
    return [gl(i) for i in range(ci(a), ci(b) + 1)]

def norm(g):
    return re.sub(r'\s+', ' ', str(g)).strip().replace('Naïve', 'Naive')

# ---------- generic readers ----------
def rows_groups(sheet, block, rows, labcol, c0, c1, analyte='', time=''):
    """groups in rows (label column), animals across columns"""
    ws = WB[sheet]
    for r in rows:
        g = cell(ws, labcol, r).value
        for k, c in enumerate(span(c0, c1)):
            v = cell(ws, c, r).value
            if v is None: continue
            vals.append(dict(block=block, sheet=sheet, analyte=analyte, group=norm(g), time=time,
                             animal=k + 1, value=float(v), cell=f'{sheet}!{c}{r}'))

def cols_groups(sheet, block, hdr_row, cols, r0, r1, analyte='', time='', labels=None):
    """groups in columns (header row), animals down rows"""
    ws = WB[sheet]
    for j, c in enumerate(cols):
        g = labels[j] if labels else cell(ws, c, hdr_row).value
        for k, r in enumerate(range(r0, r1 + 1)):
            v = cell(ws, c, r).value
            if v is None: continue
            vals.append(dict(block=block, sheet=sheet, analyte=analyte, group=norm(g), time=time,
                             animal=k + 1, value=float(v), cell=f'{sheet}!{c}{r}'))

def timecourse(sheet, block, rows, timecol, spans, analyte='', time_fmt=str):
    """rows = timepoints; spans = list of (group, c0, c1)"""
    ws = WB[sheet]
    for r in rows:
        t = cell(ws, timecol, r).value
        for g, c0, c1 in spans:
            for k, c in enumerate(span(c0, c1)):
                v = cell(ws, c, r).value
                if v is None: continue
                vals.append(dict(block=block, sheet=sheet, analyte=analyte, group=norm(g), time=time_fmt(t),
                                 animal=k + 1, value=float(v), cell=f'{sheet}!{c}{r}'))

def tte_block(sheet, block, daycol, r0, r1, groupcols, hdr_row):
    ws = WB[sheet]
    for c in groupcols:
        g = norm(cell(ws, c, hdr_row).value)
        k = 0
        for r in range(r0, r1 + 1):
            e = cell(ws, c, r).value
            if e is None: continue
            k += 1
            d = cell(ws, daycol, r).value
            tte.append(dict(block=block, sheet=sheet, group=g, animal=k,
                            time=(float(d) if d is not None else None), event=int(e),
                            cell_time=f'{sheet}!{daycol}{r}', cell_event=f'{sheet}!{c}{r}'))

def bw_block(sheet, block, rows, daycol, spans):
    ws = WB[sheet]
    for r in rows:
        d = cell(ws, daycol, r).value
        for g, c0, c1 in spans:
            for k, c in enumerate(span(c0, c1)):
                v = cell(ws, c, r).value
                if v is None: continue
                bw.append(dict(block=block, sheet=sheet, group=norm(g), animal=k + 1, day=float(d),
                               value=float(v), cell=f'{sheet}!{c}{r}'))

# ---------- S01 ----------
rows_groups('S01', 'S01-A', range(3, 11), 'A', 'B', 'F', analyte='Ifnb1', time='16h')
rows_groups('S01', 'S01-A', range(3, 11), 'G', 'H', 'L', analyte='Ifnb1', time='72h')
rows_groups('S01', 'S01-B', range(14, 18), 'A', 'B', 'F', analyte='SRB+ AEC')
rows_groups('S01', 'S01-C', range(20, 22), 'A', 'B', 'E', analyte='DiD+ AM')
sp4 = [('Sham', 'B', 'F'), ('PSLN-212', 'G', 'K'), ('PSLN-344', 'L', 'P'), ('PSLN-212(Y)', 'Q', 'U')]
sp5 = sp4 + [('PSLN-344(Y)', 'V', 'Z')]
timecourse('S01', 'S01-D', range(24, 29), 'A', sp4, analyte='Lung monocytes', time_fmt=lambda t: f'd{t}')
timecourse('S01', 'S01-E', range(30, 35), 'A', sp5, analyte='Lung CD11b+ DC', time_fmt=lambda t: f'd{t}')
timecourse('S01', 'S01-F', [36], 'A', sp5, analyte='Lung cDC1', time_fmt=lambda t: '72h')
timecourse('S01', 'S01-G', [38], 'A', sp5, analyte='Lung cDC2', time_fmt=lambda t: '72h')

# ---------- S02 ----------
cols_groups('S02', 'S02-A', 2, span('A', 'D'), 3, 7, analyte='CCR7+ migratory CD11b+ DC (lung)', time='72h')
cols_groups('S02', 'S02-B', 2, span('F', 'I'), 3, 7, analyte='MLN CD11b+CD103- DC', time='72h')
cols_groups('S02', 'S02-C', 2, span('K', 'O'), 3, 7, analyte='MLN AF647-OVA+ DC', time='36h')
cols_groups('S02', 'S02-D CD40', 9, span('A', 'D'), 10, 14, analyte='CD40+ of MLN CD11b+ DC', time='d3')
cols_groups('S02', 'S02-D CD86', 9, span('F', 'I'), 10, 14, analyte='CD86+ of MLN CD11b+ DC', time='d3')
cols_groups('S02', 'S02-E', 9, span('K', 'O'), 10, 14, analyte='OT-I proliferation (DC co-culture)', time='72h+3d')
timecourse('S02', 'S02-F', range(17, 20), 'A', [('PSLN-344', 'B', 'F'), ('PSLN-212', 'G', 'K'), ('Sham', 'L', 'P')],
           analyte='Gm-csf (lung)')
cols_groups('S02', 'S02-G', 21, span('B', 'D'), 22, 26, analyte='Lung Ly6C+CD11c+MHCII+ (moDC-like)', time='d5')
cols_groups('S02', 'S02-H', 29, span('B', 'F'), 30, 34, analyte='CD45.2+ moDC', time='d3')
cols_groups('S02', 'S02-I', 29, span('H', 'I'), 30, 34, analyte='Lung GZMB+ CD8', time='d5')

# ---------- S03 ----------
cols_groups('S03', 'S03-A', 2, span('A', 'E'), 3, 7, analyte='IgG CA09 H1N1', time='d14')
cols_groups('S03', 'S03-B', 2, span('G', 'I'), 3, 7, analyte='IgG2a/IgG1 CA09 H1N1 (as printed)', time='d14')
cols_groups('S03', 'S03-C', 2, span('K', 'O'), 3, 7, analyte='HAI CA09 H1N1', time='d14')
cols_groups('S03', 'S03-D', 2, span('Q', 'U'), 3, 7, analyte='Neut CA09 H1N1', time='d14')
cols_groups('S03', 'S03-E', 9, span('A', 'E'), 10, 14, analyte='IgG Aichi H3N2', time='d14')
cols_groups('S03', 'S03-F', 9, span('G', 'I'), 10, 14, analyte='IgG2a/IgG1 Aichi H3N2 (as printed)', time='d14')
cols_groups('S03', 'S03-G', 9, span('K', 'O'), 10, 14, analyte='HAI Aichi H3N2', time='d14')
cols_groups('S03', 'S03-H', 9, span('Q', 'U'), 10, 14, analyte='Neut Aichi H3N2', time='d14')
tte_block('S03', 'S03-I', 'A', 17, 51, span('B', 'F'), 16)
tte_block('S03', 'S03-J', 'G', 17, 46, span('H', 'J'), 16)
cols_groups('S03', 'S03-K', 16, span('L', 'O'), 17, 21, analyte='MLN GC B cells', time='d7')
rows_groups('S03', 'S03-L', range(26, 29), 'K', 'L', 'N', analyte='Aicda', time='d5')
rows_groups('S03', 'S03-L', range(26, 29), 'K', 'O', 'Q', analyte='E47', time='d5')

# ---------- S04 ----------
rows_groups('S04', 'S04-A', range(2, 6), 'A', 'B', 'F', analyte='Tfh ICOS-lo', time='d7')
rows_groups('S04', 'S04-A', range(2, 6), 'A', 'G', 'K', analyte='Tfh ICOS-hi', time='d7')
cols_groups('S04', 'S04-B Foxp3', 7, span('A', 'D'), 8, 12, analyte='Tfr (Foxp3+ of CXCR5+ICOShi)', time='d7')
cols_groups('S04', 'S04-B Tfh:Tfr', 14, span('A', 'D'), 15, 19, analyte='Tfh:Tfr', time='d7')
cols_groups('S04', 'S04-C', 21, span('A', 'D'), 22, 26, analyte='Tfr (Foxp3+ of CXCR5+ICOShi)', time='d30')
cols_groups('S04', 'S04-D', 28, span('A', 'D'), 29, 31, analyte='Lung Treg', time='d7')

# ---------- S05 ----------
timecourse('S05', 'S05-A', range(3, 6), 'A', [('PSLN-212', 'B', 'D'), ('PSLN-344', 'E', 'G'), ('PSLN-212(Y)', 'H', 'I')],
           analyte='Lung NP366 tetramer+ CD8', time_fmt=lambda t: f'd{t}')
timecourse('S05', 'S05-B', range(8, 11), 'A', [('PSLN-212', 'B', 'D'), ('PSLN-344', 'E', 'G'), ('PSLN-212(Y)', 'H', 'I')],
           analyte='MLN NP366 tetramer+ CD8', time_fmt=lambda t: f'd{t}')
cols_groups('S05', 'S05-C', 12, span('A', 'D'), 13, 15, analyte='OT-I proliferation in vivo', time='d4')
cols_groups('S05', 'S05-D', 18, span('A', 'D'), 19, 23, analyte='Lung Ki-67+ CD8', time='d3')
cols_groups('S05', 'S05-E', 25, span('A', 'D'), 26, 30, analyte='Lung GZMB+ CD8', time='d3')
cols_groups('S05', 'S05-F', 32, span('A', 'D'), 33, 37, analyte='MLN IFNg+ CD8 (rgH5N1 restim)', time='d14')
cols_groups('S05', 'S05-G', 39, span('A', 'D'), 40, 44, analyte='MLN IFNg+ CD8 (rgH5N1 restim)', time='d60')
cols_groups('S05', 'S05-H', 46, span('A', 'D'), 47, 51, analyte='MLN GZMB+ CD8', time='d60')
cols_groups('S05', 'S05-I', 53, span('A', 'D'), 54, 58, analyte='Lung TRM CD8', time='d25')

# ---------- S06 ----------
tte_block('S06', 'S06-A', 'A', 3, 30, span('B', 'E'), 2)
tte_block('S06', 'S06-B', 'G', 3, 30, span('H', 'K'), 2)
tte_block('S06', 'S06-C', 'M', 3, 30, span('N', 'Q'), 2)
tte_block('S06', 'S06-D', 'A', 34, 68, span('B', 'E'), 33)
tte_block('S06', 'S06-E', 'G', 34, 68, span('H', 'L'), 33)
tte_block('S06', 'S06-F', 'M', 34, 68, span('N', 'R'), 33)
tte_block('S06', 'S06-G', 'A', 71, 105, span('B', 'F'), 70)
tte_block('S06', 'S06-E[imprint]', 'G', 71, 105, span('H', 'K'), 70)   # printed label 'S06-E' (duplicate)
tte_block('S06', 'S06-F[imprint]', 'M', 71, 105, span('N', 'Q'), 70)   # printed label 'S06-F' (duplicate)

# ---------- S07 ----------
timecourse('S07', 'S07-A', range(3, 8), 'A', [('PSLN-212', 'B', 'D'), ('PSLN-344', 'E', 'G')],
           analyte='Lung Ly6C+CCR2+ macrophages (x1e5)', time_fmt=lambda t: f'd{t}')
cols_groups('S07', 'S07-B', 9, ['B', 'C'], 10, 14, analyte='Lung CD11b+Ly6C+ monocytes')
cols_groups('S07', 'S07-B', 9, ['E', 'F'], 10, 14, analyte='Lung Ly6C+ macrophages')
cols_groups('S07', 'S07-C', 15, ['B', 'C'], 16, 20, analyte='Lung Treg after MPhi transfer', time='d4 post-transfer',
            labels=['Ly6C-CD206+ MPhi [col B]', 'Ly6C-CD206+ MPhi [col C]'])

# ---------- S08 ----------
timecourse('S08', 'S08-A', range(3, 8), 'A', [('CMP-204', 'B', 'D'), ('PSLN-212', 'E', 'G'), ('PSLN-344', 'H', 'J'),
                                              ('PSLN-344/R848', 'K', 'M')], analyte='Ifnb1 dose-response 16h',
           time_fmt=lambda t: f'{t}ug')
timecourse('S08', 'S08-B', [11], 'A', [('CMP-204', 'A', 'C'), ('PSLN-212', 'D', 'F'), ('PSLN-R848', 'G', 'I'),
                                       ('PSLN-212/R848', 'J', 'L'), ('PSLN-344', 'M', 'O')],
           analyte='Encapsulation efficiency', time_fmt=lambda t: '')
cols_groups('S08', 'S08-C', 13, span('A', 'D'), 14, 18, analyte='SRB+ AEC', time='16h')
bw_block('S08', 'S08-D', range(21, 27), 'A', [('PSLN-212(Y)', 'B', 'F'), ('CMP-204', 'G', 'K'), ('PSLN-212', 'L', 'P'),
                                              ('PSLN-344', 'Q', 'U'), ('PSLN-212/R848', 'V', 'Z'), ('Vaccine', 'AA', 'AE')])

# ---------- S09 ----------
p1 = [('PBS', 'B', 'D'), ('CMP-204', 'E', 'G'), ('PSLN-212', 'H', 'J'), ('PSLN-R848', 'K', 'M'),
      ('PSLN-212/R848', 'N', 'P'), ('PSLN-344', 'Q', 'S'), ('PSLN-212(Y)', 'T', 'V')]
p2 = [('PBS', 'Y', 'AA'), ('CMP-204', 'AB', 'AD'), ('PSLN-212', 'AE', 'AG'), ('PSLN-R848', 'AH', 'AJ'),
      ('PSLN-212/R848', 'AK', 'AM'), ('PSLN-344', 'AN', 'AP'), ('PSLN-212(Y)', 'AQ', 'AS')]
ws9 = WB['S09']
for r in range(3, 10):
    a1 = ws9.cell(r, 1).value; a2 = ws9.cell(r, ci('X')).value
    for panel, spans, an in [('panel1[A:U]', p1, a1), ('panel2[X:AS]', p2, a2)]:
        for g, c0, c1 in spans:
            for k, c in enumerate(span(c0, c1)):
                v = cell(ws9, c, r).value
                if v is None: continue
                vals.append(dict(block='S09-A ' + panel, sheet='S09', analyte=an, group=norm(g), time='16h (as printed)',
                                 animal=k + 1, value=float(v), cell=f'S09!{c}{r}'))
tte_block('S09', 'S09-B', 'A', 12, 35, span('B', 'D'), 11)
bw_block('S09', 'S09-C', range(12, 20), 'F', [('PSLN-212(Y)', 'G', 'N'), ('Sham', 'O', 'V'), ('PSLN-344(Y)', 'W', 'AD')])
tte_block('S09', 'S09-D', 'A', 39, 62, span('B', 'D'), 38)
bw_block('S09', 'S09-E', range(39, 47), 'F', [('PSLN-212(Y)', 'G', 'N'), ('Sham', 'O', 'V'), ('PSLN-344(Y)', 'W', 'AD')])
tte_block('S09', 'S09-F', 'A', 66, 88, span('B', 'D'), 65)
bw_block('S09', 'S09-G', range(66, 74), 'F', [('PSLN-212(Y)', 'G', 'N'), ('Sham', 'O', 'V'), ('PSLN-344(Y)', 'W', 'AD')])

# ---------- S10 ----------
cols_groups('S10', 'S10-A', 2, span('A', 'D'), 3, 7, analyte='CNS Ifnb1', time='36h')
cols_groups('S10', 'S10-A', 2, span('F', 'I'), 3, 7, analyte='CNS Tnf', time='36h')
cols_groups('S10', 'S10-A', 2, span('K', 'N'), 3, 7, analyte='CNS Isg15', time='36h')

# ---------- S11 ----------
sp11 = [('Vaccine', 'B', 'F'), ('PSLN-212', 'G', 'K'), ('PSLN-344', 'L', 'P'), ('PSLN-212(Y)', 'Q', 'U')]
timecourse('S11', 'S11-A', range(3, 8), 'A', sp11, analyte='Lung alveolar macrophages', time_fmt=lambda t: f'd{t}')
timecourse('S11', 'S11-B', range(10, 15), 'A', sp11, analyte='Lung neutrophils', time_fmt=lambda t: f'd{t}')
cols_groups('S11', 'S11-C', 16, ['A', 'B'], 17, 21, analyte='Lung recruited monocytes', time='d3')
timecourse('S11', 'S11-D', range(24, 29), 'A', sp11, analyte='Lung NK cells', time_fmt=lambda t: f'd{t}')
cols_groups('S11', 'S11-E', 30, span('A', 'D'), 31, 35, analyte='Lung CD206+ macrophages', time='not stated')

# ---------- S12 ----------
cols_groups('S12', 'S12-A', 2, ['A', 'B'], 3, 5, analyte='Infiltrating CD45.2+ monocytes', time='d3')

# ---------- S13 ----------
cols_groups('S13', 'S13-A', 2, span('A', 'C'), 3, 7, analyte='IgG2a CA09 H1N1', time='d14')
cols_groups('S13', 'S13-B', 2, span('E', 'G'), 3, 7, analyte='IgG1 CA09 H1N1', time='d14')
cols_groups('S13', 'S13-C', 2, span('I', 'K'), 3, 7, analyte='IgG2a Aichi H3N2', time='d14')
cols_groups('S13', 'S13-D', 2, span('M', 'O'), 3, 7, analyte='IgG1 Aichi H3N2', time='d14')
tte_block('S13', 'S13-E', 'R', 3, 30, span('S', 'V'), 2)
bw_block('S13', 'S13-F', range(33, 41), 'A', [('PSLN-212(Y)', 'B', 'H'), ('Sham', 'I', 'O'), ('PSLN-212', 'P', 'V'),
                                              ('PSLN-344', 'W', 'AC'), ('Naive', 'AD', 'AJ')])
bw_block('S13', 'S13-G', range(43, 51), 'A', [('PSLN-344', 'B', 'K'), ('Sham', 'L', 'U'), ('Naive', 'V', 'AE')])
cols_groups('S13', 'S13-H', 52, span('A', 'D'), 53, 57, analyte='MLN IgG+ of B220+', time='not stated')
cols_groups('S13', 'S13-I', 52, span('F', 'J'), 53, 57, analyte='IgG CA09 H1N1 post-boost', time='d28')
cols_groups('S13', 'S13-J', 52, span('L', 'P'), 53, 57, analyte='IgG Aichi H3N2 post-boost', time='d28')

# ---------- S14 ----------
cols_groups('S14', 'S14-A H1N1', 2, span('A', 'D'), 3, 7, analyte='MLN IFNg+ CD8 (H1N1 restim)', time='not stated')
cols_groups('S14', 'S14-A H3N2', 2, span('F', 'I'), 3, 7, analyte='MLN IFNg+ CD8 (H3N2 restim)', time='not stated')

# ---------- S15 ----------
sp15 = [('PSLN-212(Y)', 'B', 'H'), ('Sham', 'I', 'O'), ('PSLN-212', 'P', 'V'), ('PSLN-344', 'W', 'AC')]
sp15u = sp15 + [('Untreated', 'AD', 'AJ')]
for blk, r0, spn in [('S15-A', 3, sp15), ('S15-B', 13, sp15), ('S15-C', 23, sp15), ('S15-D', 33, sp15),
                     ('S15-E', 43, sp15u), ('S15-F', 53, sp15u), ('S15-G', 63, sp15u)]:
    bw_block('S15', blk, range(r0, r0 + 8), 'A', spn)
tte_block('S15', 'S15-H', 'A', 73, 100, span('B', 'D'), 72)
bw_block('S15', 'S15-I', range(72, 80), 'H', [('3d Vaccine', 'I', 'O'), ('3d PSLN-344', 'P', 'V'),
                                             ('3d Vaccine+PSLN-344', 'W', 'AC')])
spjk = [('Naive+PSLN-212', 'I', 'O'), ('Imprinting+PSLN-212', 'P', 'V'), ('Naive+PSLN-344', 'W', 'AC'),
        ('Imprinting+PSLN-344', 'AD', 'AJ')]
bw_block('S15', 'S15-J', range(83, 91), 'H', spjk)
bw_block('S15', 'S15-K', range(93, 101), 'H', spjk)
tte_block('S15', 'S15-L', 'A', 103, 130, span('B', 'E'), 102)
spmo = [('PSLN-212(Y)', 'I', 'O'), ('Sham', 'P', 'V'), ('PSLN-212', 'W', 'AC'), ('PSLN-344', 'AD', 'AJ')]
bw_block('S15', 'S15-M', range(103, 111), 'H', spmo)
tte_block('S15', 'S15-N', 'A', 134, 161, span('B', 'E'), 133)
bw_block('S15', 'S15-O', range(134, 142), 'H', spmo)

# ---------- S08 unlabeled region ----------
ws8 = WB['S08']
unl = [(f'S08!{c}{r}', ws8[f'{c}{r}'].value) for r in range(89, 102) for c in 'ABCD' if ws8[f'{c}{r}'].value is not None]

V = pd.DataFrame(vals); T = pd.DataFrame(tte); B = pd.DataFrame(bw)
V.to_csv(f'{OUT}/values.csv', index=False); T.to_csv(f'{OUT}/tte.csv', index=False); B.to_csv(f'{OUT}/bw.csv', index=False)
pd.DataFrame(unl, columns=['cell', 'value']).to_csv(f'{OUT}/s08_unlabeled.csv', index=False)
print('values', V.shape, 'tte', T.shape, 'bw', B.shape, 'unlabeled', len(unl))
print(V.groupby('block').size().to_string())
print(T.groupby(['block', 'group']).size().to_string())
