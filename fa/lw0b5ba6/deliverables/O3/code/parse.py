"""
Parse psln_program_dataset.xlsx into tidy tables using explicit, hand-verified cell coordinates.
Every value keeps its source cell so that every downstream number can be traced back to the workbook.

Outputs (in /tmp/work/tidy/):
  continuous.csv : sheet, block, measurand, group, time, rep, value, cell
  survival.csv   : sheet, block, group, animal, days, event, cell_days, cell_event
  weights.csv    : sheet, block, group, animal, day, value, cell
"""
import openpyxl, pandas as pd, os
from openpyxl.utils import column_index_from_string as ci, get_column_letter as gl

WB = '/tmp/world/filesystem/psln_program_dataset.xlsx'
OUT = '/tmp/work/tidy'
os.makedirs(OUT, exist_ok=True)
wb = openpyxl.load_workbook(WB, data_only=True)

cont, surv, wts = [], [], []

def v(ws, col, row):
    return ws.cell(row=row, column=ci(col) if isinstance(col, str) else col).value

def cols(a, b):
    return [gl(i) for i in range(ci(a), ci(b) + 1)]

# ---------- generic helpers ----------
def rowgroups(sheet, block, meas, label_col, first_val_col, last_val_col, rows, time=None):
    """groups in rows: label in label_col, replicates across columns"""
    ws = wb[sheet]
    for r in rows:
        g = v(ws, label_col, r)
        for k, c in enumerate(cols(first_val_col, last_val_col)):
            x = v(ws, c, r)
            if x is None:
                continue
            cont.append(dict(sheet=sheet, block=block, measurand=meas, group=str(g).strip(), time=time,
                             rep=k + 1, value=float(x), cell=f'{c}{r}'))

def colgroups(sheet, block, meas, header_row, group_cols, rows, time=None):
    """groups in columns: header label in header_row, replicates down rows"""
    ws = wb[sheet]
    for c in group_cols:
        g = v(ws, c, header_row)
        for k, r in enumerate(rows):
            x = v(ws, c, r)
            if x is None:
                continue
            cont.append(dict(sheet=sheet, block=block, measurand=meas, group=str(g).strip(), time=time,
                             rep=k + 1, value=float(x), cell=f'{c}{r}'))

def spangroups(sheet, block, meas, header_row, spans, rows, time_col='A', time_override=None):
    """groups spanning several columns (replicates across columns), time down rows"""
    ws = wb[sheet]
    for (c0, c1) in spans:
        g = v(ws, c0, header_row)
        for r in rows:
            t = time_override if time_override is not None else v(ws, time_col, r)
            for k, c in enumerate(cols(c0, c1)):
                x = v(ws, c, r)
                if x is None:
                    continue
                cont.append(dict(sheet=sheet, block=block, measurand=meas, group=str(g).strip(), time=t,
                                 rep=k + 1, value=float(x), cell=f'{c}{r}'))

def survblock(sheet, block, days_col, header_row, group_cols, rows):
    ws = wb[sheet]
    for c in group_cols:
        g = str(v(ws, c, header_row)).strip()
        a = 0
        for r in rows:
            e = v(ws, c, r)
            if e is None:
                continue
            a += 1
            d = v(ws, days_col, r)
            surv.append(dict(sheet=sheet, block=block, group=g, animal=a,
                             days=(float(d) if d is not None else None), event=int(e),
                             cell_days=f'{days_col}{r}', cell_event=f'{c}{r}'))

def weightblock(sheet, block, header_row, spans, rows, day_col):
    ws = wb[sheet]
    for (c0, c1) in spans:
        g = str(v(ws, c0, header_row)).strip()
        for k, c in enumerate(cols(c0, c1)):
            for r in rows:
                x = v(ws, c, r)
                if x is None:
                    continue
                wts.append(dict(sheet=sheet, block=block, group=g, animal=k + 1,
                                day=float(v(ws, day_col, r)), value=float(x), cell=f'{c}{r}'))

# ================= S01 =================
rowgroups('S01', 'S01-A', 'Lung Ifnb1 (fold vs untreated)', 'A', 'B', 'F', range(3, 11), time='16h')
rowgroups('S01', 'S01-A', 'Lung Ifnb1 (fold vs untreated)', 'G', 'H', 'L', range(3, 11), time='72h')
rowgroups('S01', 'S01-B', 'SRB+ alveolar epithelial cells (%)', 'A', 'B', 'F', range(14, 18), time='16h')
rowgroups('S01', 'S01-C', 'DiD+ alveolar macrophages (%)', 'A', 'B', 'E', range(20, 22), time='16h')
spangroups('S01', 'S01-D', 'Lung monocytes CD11b+Ly6C+ (%)', 23,
           [('B', 'F'), ('G', 'K'), ('L', 'P'), ('Q', 'U')], range(24, 29))
spangroups('S01', 'S01-E', 'Lung CD11b+ DC (%)', 29,
           [('B', 'F'), ('G', 'K'), ('L', 'P'), ('Q', 'U'), ('V', 'Z')], range(30, 35))
spangroups('S01', 'S01-F', 'Lung cDC1 (%)', 35,
           [('B', 'F'), ('G', 'K'), ('L', 'P'), ('Q', 'U'), ('V', 'Z')], [36], time_override='72h')
spangroups('S01', 'S01-G', 'Lung cDC2 (%)', 37,
           [('B', 'F'), ('G', 'K'), ('L', 'P'), ('Q', 'U'), ('V', 'Z')], [38], time_override='72h')

# ================= S02 =================
colgroups('S02', 'S02-A', 'Lung migratory CCR7+ CD11b+ DC (%)', 2, cols('A', 'D'), range(3, 8), '72h')
colgroups('S02', 'S02-B', 'MLN CD11b+CD103- DC (%)', 2, cols('F', 'I'), range(3, 8), '72h')
colgroups('S02', 'S02-C', 'MLN DC AF647-OVA+ (%)', 2, cols('K', 'O'), range(3, 8), '36h')
colgroups('S02', 'S02-D CD40', 'MLN CD11b+ DC CD40+ (%)', 9, cols('A', 'D'), range(10, 15), 'd3')
colgroups('S02', 'S02-D CD86', 'MLN CD11b+ DC CD86+ (%)', 9, cols('F', 'I'), range(10, 15), 'd3')
colgroups('S02', 'S02-E', 'OT-I proliferation with MLN CD11b+ DC (%)', 9, cols('K', 'O'), range(10, 15), '72h+3d')
spangroups('S02', 'S02-F', 'Lung Gm-csf (fold vs untreated)', 16, [('B', 'F'), ('G', 'K'), ('L', 'P')], range(17, 20))
colgroups('S02', 'S02-G', 'Lung Ly6C+ moDC-like cells (%)', 21, cols('B', 'D'), range(22, 27), 'd5')
colgroups('S02', 'S02-H', 'CD45.2+ moDC (%)', 29, cols('B', 'F'), range(30, 35), 'd3')
colgroups('S02', 'S02-I', 'Lung GZMB+ CD8 T (%)', 29, cols('H', 'I'), range(30, 35), 'd5')

# ================= S03 =================
colgroups('S03', 'S03-A', 'Serum IgG anti-CA09 H1N1 (titre)', 2, cols('A', 'E'), range(3, 8), 'd14')
colgroups('S03', 'S03-B', 'IgG2a/IgG1 anti-CA09 (ratio, as printed)', 2, cols('G', 'I'), range(3, 8), 'd14')
colgroups('S03', 'S03-C', 'HI titre CA09 H1N1', 2, cols('K', 'O'), range(3, 8), 'd14')
colgroups('S03', 'S03-D', 'Neutralising titre CA09 H1N1', 2, cols('Q', 'U'), range(3, 8), 'd14')
colgroups('S03', 'S03-E', 'Serum IgG anti-Aichi H3N2 (titre)', 9, cols('A', 'E'), range(10, 15), 'd14')
colgroups('S03', 'S03-F', 'IgG2a/IgG1 anti-Aichi (ratio, as printed)', 9, cols('G', 'I'), range(10, 15), 'd14')
colgroups('S03', 'S03-G', 'HI titre Aichi H3N2', 9, cols('K', 'O'), range(10, 15), 'd14')
colgroups('S03', 'S03-H', 'Neutralising titre Aichi H3N2', 9, cols('Q', 'U'), range(10, 15), 'd14')
survblock('S03', 'S03-I', 'A', 16, cols('B', 'F'), range(17, 52))
survblock('S03', 'S03-J', 'G', 16, cols('H', 'J'), range(17, 47))
colgroups('S03', 'S03-K', 'MLN GC B cells CXCR5+GL7+ (%)', 16, cols('L', 'O'), range(17, 22), 'd7')
rowgroups('S03', 'S03-L', 'MLN B cell Aicda (fold)', 'K', 'L', 'N', range(26, 29), 'd5')
rowgroups('S03', 'S03-L', 'MLN B cell E47 (fold)', 'K', 'O', 'Q', range(26, 29), 'd5')

# ================= S04 =================
rowgroups('S04', 'S04-A', 'MLN Tfh ICOS-low (%)', 'A', 'B', 'F', range(2, 6), 'd7')
rowgroups('S04', 'S04-A', 'MLN Tfh ICOS-high (%)', 'A', 'G', 'K', range(2, 6), 'd7')
colgroups('S04', 'S04-B Foxp3', 'MLN Tfr Foxp3+ in CXCR5+ICOShi (%)', 7, cols('A', 'D'), range(8, 13), 'd7')
colgroups('S04', 'S04-B Tfh:Tfr', 'Tfh:Tfr ratio (as printed)', 14, cols('A', 'D'), range(15, 20), 'd7')
colgroups('S04', 'S04-C', 'MLN Tfr (%) day 30', 21, cols('A', 'D'), range(22, 27), 'd30')
colgroups('S04', 'S04-D', 'Lung Treg CD4+Foxp3+ (%)', 28, cols('A', 'D'), range(29, 32), 'd7')

# ================= S05 =================
spangroups('S05', 'S05-A', 'Lung NP366 tetramer+ CD8 (%)', 2, [('B', 'C'), ('E', 'F'), ('H', 'I')], range(3, 6))
spangroups('S05', 'S05-B', 'MLN NP366 tetramer+ CD8 (%)', 7, [('B', 'C'), ('E', 'F'), ('H', 'I')], range(8, 11))
colgroups('S05', 'S05-C', 'OT-I proliferation in vivo (%)', 12, cols('A', 'D'), range(13, 16), 'd4')
colgroups('S05', 'S05-D', 'Lung Ki-67+ CD8 T (%)', 18, cols('A', 'D'), range(19, 24), 'd3')
colgroups('S05', 'S05-E', 'Lung GZMB+ CD8 T (%)', 25, cols('A', 'D'), range(26, 31), 'd3')
colgroups('S05', 'S05-F', 'MLN IFNg+ CD8 T, H5N1 restim (%) d14', 32, cols('A', 'D'), range(33, 38), 'd14')
colgroups('S05', 'S05-G', 'MLN IFNg+ CD8 T, H5N1 restim (%) d60', 39, cols('A', 'D'), range(40, 45), 'd60')
colgroups('S05', 'S05-H', 'MLN GZMB+ CD8 T (%) d60', 46, cols('A', 'D'), range(47, 52), 'd60')
colgroups('S05', 'S05-I', 'Lung CD8 TRM CD69+CD103+ (%)', 53, cols('A', 'D'), range(54, 59), 'd25')

# ================= S06 =================
survblock('S06', 'S06-A', 'A', 2, cols('B', 'E'), range(3, 31))
survblock('S06', 'S06-B', 'G', 2, cols('H', 'K'), range(3, 31))
survblock('S06', 'S06-C', 'M', 2, cols('N', 'Q'), range(3, 31))
survblock('S06', 'S06-D', 'A', 33, cols('B', 'E'), range(34, 69))
survblock('S06', 'S06-E', 'G', 33, cols('H', 'L'), range(34, 69))
survblock('S06', 'S06-F', 'M', 33, cols('N', 'R'), range(34, 69))
survblock('S06', 'S06-G', 'A', 70, cols('B', 'F'), range(71, 106))
survblock('S06', 'S06-E(rows71-105; imprinting)', 'G', 70, cols('H', 'K'), range(71, 106))
survblock('S06', 'S06-F(rows71-105; imprinting)', 'M', 70, cols('N', 'Q'), range(71, 106))

# ================= S07 =================
spangroups('S07', 'S07-A', 'Lung Ly6C+CCR2+ macrophages (x10^5 cells)', 2, [('B', 'D'), ('E', 'G')], range(3, 8))
ws = wb['S07']
for c, g, m in [('B', 'PSLN-344', 'Lung CD11b+Ly6C+ monocytes (%)'), ('C', 'PSLN-344+INCB3344', 'Lung CD11b+Ly6C+ monocytes (%)'),
                ('E', 'PSLN-344', 'Lung Ly6C+ macrophages (%)'), ('F', 'PSLN-344+INCB3344', 'Lung Ly6C+ macrophages (%)')]:
    for k, r in enumerate(range(10, 15)):
        cont.append(dict(sheet='S07', block='S07-B', measurand=m, group=g, time=None, rep=k + 1,
                         value=float(v(ws, c, r)), cell=f'{c}{r}'))
for c, g in [('B', 'Ly6C-CD206+ MPhi [col B, label duplicated]'), ('C', 'Ly6C-CD206+ MPhi [col C, label duplicated]')]:
    for k, r in enumerate(range(16, 21)):
        cont.append(dict(sheet='S07', block='S07-C', measurand='Lung Treg after macrophage transfer (%)', group=g,
                         time='d4 post-transfer', rep=k + 1, value=float(v(ws, c, r)), cell=f'{c}{r}'))

# ================= S08 =================
spangroups('S08', 'S08-A', 'Lung Ifnb1 dose-response (fold)', 2, [('B', 'D'), ('E', 'G'), ('H', 'J'), ('K', 'M')], range(3, 8))
spangroups('S08', 'S08-B', 'Encapsulation efficiency (%)', 10, [('A', 'C'), ('D', 'F'), ('G', 'I'), ('J', 'L'), ('M', 'O')], [11], time_override='n/a')
colgroups('S08', 'S08-C', 'SRB+ alveolar epithelial cells (%)', 13, cols('A', 'D'), range(14, 19), '16h')
weightblock('S08', 'S08-D', 20, [('B', 'F'), ('G', 'K'), ('L', 'P'), ('Q', 'U'), ('V', 'Z'), ('AA', 'AE')], range(21, 27), 'A')

# ================= S09 =================
ws = wb['S09']
for (blk_label, spans, t) in [
    ('S09-A (cols A-V; printed 16h)', [('B', 'D'), ('E', 'G'), ('H', 'J'), ('K', 'M'), ('N', 'P'), ('Q', 'S'), ('T', 'V')], '16h (as printed)'),
    ('S09-A (cols X-AS; printed 16h)', [('Y', 'AA'), ('AB', 'AD'), ('AE', 'AG'), ('AH', 'AJ'), ('AK', 'AM'), ('AN', 'AP'), ('AQ', 'AS')], '16h (as printed)')]:
    label_col = 'A' if spans[0][0] == 'B' else 'X'
    for (c0, c1) in spans:
        g = str(v(ws, c0, 2)).strip()
        for r in range(3, 10):
            analyte = v(ws, label_col, r)
            for k, c in enumerate(cols(c0, c1)):
                x = v(ws, c, r)
                cont.append(dict(sheet='S09', block=blk_label, measurand=f'Lung {analyte} (log10 fold)', group=g,
                                 time=t, rep=k + 1, value=float(x), cell=f'{c}{r}'))
survblock('S09', 'S09-B', 'A', 11, cols('B', 'D'), range(12, 36))
weightblock('S09', 'S09-C', 11, [('G', 'N'), ('O', 'V'), ('W', 'AD')], range(12, 20), 'F')
survblock('S09', 'S09-D', 'A', 38, cols('B', 'D'), range(39, 63))
weightblock('S09', 'S09-E', 38, [('G', 'N'), ('O', 'V'), ('W', 'AD')], range(39, 47), 'F')
survblock('S09', 'S09-F', 'A', 65, cols('B', 'D'), range(66, 89))
weightblock('S09', 'S09-G', 65, [('G', 'N'), ('O', 'V'), ('W', 'AD')], range(66, 74), 'F')

# ================= S10 =================
colgroups('S10', 'S10-A', 'CNS Ifnb1 (fold)', 2, cols('A', 'D'), range(3, 8), '36h')
colgroups('S10', 'S10-A', 'CNS Tnf (fold)', 2, cols('F', 'I'), range(3, 8), '36h')
colgroups('S10', 'S10-A', 'CNS Isg15 (fold)', 2, cols('K', 'N'), range(3, 8), '36h')

# ================= S11 =================
spangroups('S11', 'S11-A', 'Lung alveolar macrophages (%)', 2, [('B', 'F'), ('G', 'K'), ('L', 'P'), ('Q', 'U')], range(3, 8))
spangroups('S11', 'S11-B', 'Lung neutrophils (%)', 9, [('B', 'F'), ('G', 'K'), ('L', 'P'), ('Q', 'U')], range(10, 15))
colgroups('S11', 'S11-C', 'Lung recruited monocytes (%)', 16, cols('A', 'B'), range(17, 22), 'd3')
spangroups('S11', 'S11-D', 'Lung NK cells (%)', 23, [('B', 'F'), ('G', 'K'), ('L', 'P'), ('Q', 'U')], range(24, 29))
colgroups('S11', 'S11-E', 'Lung CD206+ macrophages (%)', 30, cols('A', 'D'), range(31, 36), 'not stated')

# ================= S12 =================
colgroups('S12', 'S12-A', 'Infiltrating CD45.2+ monocytes (%)', 2, cols('A', 'B'), range(3, 6), 'd3')

# ================= S13 =================
colgroups('S13', 'S13-A', 'Serum IgG2a anti-CA09 (titre)', 2, cols('A', 'C'), range(3, 8), 'd14')
colgroups('S13', 'S13-B', 'Serum IgG1 anti-CA09 (titre)', 2, cols('E', 'G'), range(3, 8), 'd14')
colgroups('S13', 'S13-C', 'Serum IgG2a anti-Aichi (titre)', 2, cols('I', 'K'), range(3, 8), 'd14')
colgroups('S13', 'S13-D', 'Serum IgG1 anti-Aichi (titre)', 2, cols('M', 'O'), range(3, 8), 'd14')
survblock('S13', 'S13-E', 'R', 2, cols('S', 'V'), range(3, 31))
weightblock('S13', 'S13-F', 32, [('B', 'H'), ('I', 'O'), ('P', 'V'), ('W', 'AC'), ('AD', 'AJ')], range(33, 41), 'A')
weightblock('S13', 'S13-G', 42, [('B', 'K'), ('L', 'U'), ('V', 'AE')], range(43, 51), 'A')
colgroups('S13', 'S13-H', 'MLN B220+ IgG+ (%)', 52, cols('A', 'D'), range(53, 58), 'not stated')
colgroups('S13', 'S13-I', 'Serum IgG anti-CA09 d28 post-boost (titre)', 52, cols('F', 'J'), range(53, 58), 'd28')
colgroups('S13', 'S13-J', 'Serum IgG anti-Aichi d28 post-boost (titre)', 52, cols('L', 'P'), range(53, 58), 'd28')

# ================= S14 =================
colgroups('S14', 'S14-A H1N1', 'MLN IFNg+ CD8 T, H1N1 restim (%)', 2, cols('A', 'D'), range(3, 8), 'not stated')
colgroups('S14', 'S14-A H3N2', 'MLN IFNg+ CD8 T, H3N2 restim (%)', 2, cols('F', 'I'), range(3, 8), 'not stated')

# ================= S15 =================
four = [('B', 'H'), ('I', 'O'), ('P', 'V'), ('W', 'AC')]
five = four + [('AD', 'AJ')]
weightblock('S15', 'S15-A', 2, four, range(3, 11), 'A')
weightblock('S15', 'S15-B', 12, four, range(13, 21), 'A')
weightblock('S15', 'S15-C', 22, four, range(23, 31), 'A')
weightblock('S15', 'S15-D', 32, four, range(33, 41), 'A')
weightblock('S15', 'S15-E', 42, five, range(43, 51), 'A')
weightblock('S15', 'S15-F', 52, five, range(53, 61), 'A')
weightblock('S15', 'S15-G', 62, five, range(63, 71), 'A')
survblock('S15', 'S15-H', 'A', 72, cols('B', 'D'), range(73, 94))
weightblock('S15', 'S15-I', 71, [('I', 'O'), ('P', 'V'), ('W', 'AC')], range(72, 80), 'H')
weightblock('S15', 'S15-J', 82, [('I', 'O'), ('P', 'V'), ('W', 'AC'), ('AD', 'AJ')], range(83, 91), 'H')
weightblock('S15', 'S15-K', 92, [('I', 'O'), ('P', 'V'), ('W', 'AC'), ('AD', 'AJ')], range(93, 101), 'H')
survblock('S15', 'S15-L', 'A', 102, cols('B', 'E'), range(103, 131))
weightblock('S15', 'S15-M', 102, [('I', 'O'), ('P', 'V'), ('W', 'AC'), ('AD', 'AJ')], range(103, 111), 'H')
survblock('S15', 'S15-N', 'A', 133, cols('B', 'E'), range(134, 162))
weightblock('S15', 'S15-O', 133, [('I', 'O'), ('P', 'V'), ('W', 'AC'), ('AD', 'AJ')], range(134, 142), 'H')

C = pd.DataFrame(cont); S = pd.DataFrame(surv); W = pd.DataFrame(wts)
# normalise group labels (strip, unify Naive / young suffixes) but keep printed label too
def norm(g):
    g = g.replace('Naïve', 'Naive').strip()
    g = g.replace('PSLN-212Y', 'PSLN-212(Y)').replace('PSLN-344Y', 'PSLN-344(Y)').replace('PSLN-212(y)', 'PSLN-212(Y)')
    return g
for D in (C, S, W):
    D['group_printed'] = D['group']
    D['group'] = D['group'].map(norm)
C.to_csv(f'{OUT}/continuous.csv', index=False)
S.to_csv(f'{OUT}/survival.csv', index=False)
W.to_csv(f'{OUT}/weights.csv', index=False)
print('continuous', C.shape, 'blocks', C.block.nunique())
print('survival', S.shape, 'blocks', S.block.nunique())
print('weights', W.shape, 'blocks', W.block.nunique())
print(C.groupby(['block', 'measurand', 'group', 'time'], dropna=False).size().to_string())
