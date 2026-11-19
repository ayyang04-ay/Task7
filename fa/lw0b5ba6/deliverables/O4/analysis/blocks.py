"""
Block map for psln_program_dataset.xlsx.
Every block is described by explicit cell ranges so that every derived number
can be traced back to workbook cells. Layout types:
  colgroups : header row holds group names in given columns; values in rows r0..r1 below
  rowgroups : group name in a label column; replicate values across columns c0..c1
  spans     : timepoint rows (label column), groups occupy contiguous column spans
  survival  : one row per animal; 'days' column + one indicator column per group (1=event, 0=censored)
"""
from openpyxl.utils import column_index_from_string as ci, get_column_letter as gl

XLSX = '/tmp/world/filesystem/psln_program_dataset.xlsx'

def span(a, b):
    return [gl(i) for i in range(ci(a), ci(b) + 1)]

# ---------------------------------------------------------------------------
# Continuous blocks
# ---------------------------------------------------------------------------
BLOCKS = {}

def add(bid, **kw):
    BLOCKS[bid] = kw

# ---- S01
add('S01-A_16h', sheet='S01', kind='rowgroups', label_col='A', rows=range(3, 11), cols=span('B', 'F'),
    measurand='Lung Ifnb1 mRNA (fold vs untreated), 16 h, no vaccine', unit='fold', scale='fold', time='16h')
add('S01-A_72h', sheet='S01', kind='rowgroups', label_col='G', rows=range(3, 11), cols=span('H', 'L'),
    measurand='Lung Ifnb1 mRNA (fold vs untreated), 72 h, no vaccine', unit='fold', scale='fold', time='72h')
add('S01-B', sheet='S01', kind='rowgroups', label_col='A', rows=range(14, 18), cols=span('B', 'F'),
    measurand='AEC SRB+ (%) 16 h, PSLN-SRB vs free SRB (aged)', unit='%', scale='linear', time='16h')
add('S01-C', sheet='S01', kind='rowgroups', label_col='A', rows=range(20, 22), cols=span('B', 'E'),
    measurand='Alveolar macrophage DiD+ (%) 16 h, WT vs Sftpa1/Sftpd KO', unit='%', scale='linear', time='16h')
add('S01-D', sheet='S01', kind='spans', time_col='A', rows=range(24, 29),
    groups={'Sham': span('B', 'F'), 'PSLN-212': span('G', 'K'), 'PSLN-344': span('L', 'P'), 'PSLN-212(Y)': span('Q', 'U')},
    measurand='Lung monocytes CD11b+Ly6C+ (%) d0-8', unit='%', scale='linear', time='day')
add('S01-E', sheet='S01', kind='spans', time_col='A', rows=range(30, 35),
    groups={'Sham': span('B', 'F'), 'PSLN-212': span('G', 'K'), 'PSLN-344': span('L', 'P'), 'PSLN-212(Y)': span('Q', 'U'), 'PSLN-344(Y)': span('V', 'Z')},
    measurand='Lung CD11b+ DC (%) d0-8', unit='%', scale='linear', time='day')
add('S01-F', sheet='S01', kind='spans', time_col=None, rows=[36],
    groups={'Sham': span('B', 'F'), 'PSLN-212': span('G', 'K'), 'PSLN-344': span('L', 'P'), 'PSLN-212(Y)': span('Q', 'U'), 'PSLN-344(Y)': span('V', 'Z')},
    measurand='Lung cDC1 XCR1+ (%) 72 h', unit='%', scale='linear', time='72h')
add('S01-G', sheet='S01', kind='spans', time_col=None, rows=[38],
    groups={'Sham': span('B', 'F'), 'PSLN-212': span('G', 'K'), 'PSLN-344': span('L', 'P'), 'PSLN-212(Y)': span('Q', 'U'), 'PSLN-344(Y)': span('V', 'Z')},
    measurand='Lung cDC2 CD172a+ (%) 72 h', unit='%', scale='linear', time='72h')
# ---- S02
add('S02-A', sheet='S02', kind='colgroups', header_row=2, cols=span('A', 'D'), rows=range(3, 8),
    measurand='Lung migratory CCR7+ CD11b+ DC (%) 72 h', unit='%', scale='linear', time='72h')
add('S02-B', sheet='S02', kind='colgroups', header_row=2, cols=span('F', 'I'), rows=range(3, 8),
    measurand='MLN CD11b+CD103- DC (%) 72 h', unit='%', scale='linear', time='72h')
add('S02-C', sheet='S02', kind='colgroups', header_row=2, cols=span('K', 'O'), rows=range(3, 8),
    measurand='MLN DC AF647-OVA+ (%) 36 h', unit='%', scale='linear', time='36h')
add('S02-D_CD40', sheet='S02', kind='colgroups', header_row=9, cols=span('A', 'D'), rows=range(10, 15),
    measurand='MLN CD11b+ DC CD40+ (%) d3', unit='%', scale='linear', time='d3')
add('S02-D_CD86', sheet='S02', kind='colgroups', header_row=9, cols=span('F', 'I'), rows=range(10, 15),
    measurand='MLN CD11b+ DC CD86+ (%) d3', unit='%', scale='linear', time='d3')
add('S02-E', sheet='S02', kind='colgroups', header_row=9, cols=span('K', 'O'), rows=range(10, 15),
    measurand='OT-I CFSE-dilution by sorted MLN CD11b+ DC (%)', unit='%', scale='linear', time='72h+3d')
add('S02-F', sheet='S02', kind='spans', time_col='A', rows=range(17, 20),
    groups={'PSLN-344': span('B', 'F'), 'PSLN-212': span('G', 'K'), 'Sham': span('L', 'P')},
    measurand='Lung Gm-csf (Csf2) mRNA (fold) 16/36/72 h', unit='fold', scale='fold', time='h')
add('S02-G', sheet='S02', kind='colgroups', header_row=21, cols=span('B', 'D'), rows=range(22, 27),
    measurand='Lung Ly6C+CD11c+MHC-II+ moDC-like (%) d5, GM-CSF rescue', unit='%', scale='linear', time='d5')
add('S02-H', sheet='S02', kind='colgroups', header_row=29, cols=span('B', 'F'), rows=range(30, 35),
    measurand='CD45.2+ moDC (%) d3, BM chimeras WT vs Ifnar-/-', unit='%', scale='linear', time='d3')
add('S02-I', sheet='S02', kind='colgroups', header_row=29, cols=span('H', 'I'), rows=range(30, 35),
    measurand='Lung GZMB+ CD8 (%) d5, +/- CCR2 antagonist (young)', unit='%', scale='linear', time='d5')
# ---- S03
for bid, cols, hr, rows, meas, scale in [
    ('S03-A', span('A', 'E'), 2, range(3, 8), 'Serum IgG anti-CA09 H1N1 (endpoint titre) d14', 'titer'),
    ('S03-B', span('G', 'I'), 2, range(3, 8), 'IgG2a/IgG1 ratio anti-CA09 H1N1 d14', 'ratio'),
    ('S03-C', span('K', 'O'), 2, range(3, 8), 'HAI titre anti-CA09 H1N1 d14 (LOD 1:10)', 'hai'),
    ('S03-D', span('Q', 'U'), 2, range(3, 8), 'Neutralising titre anti-CA09 H1N1 d14', 'titer'),
    ('S03-E', span('A', 'E'), 9, range(10, 15), 'Serum IgG anti-Aichi H3N2 (endpoint titre) d14', 'titer'),
    ('S03-F', span('G', 'I'), 9, range(10, 15), 'IgG2a/IgG1 ratio anti-Aichi H3N2 d14', 'ratio'),
    ('S03-G', span('K', 'O'), 9, range(10, 15), 'HAI titre anti-Aichi H3N2 d14 (LOD 1:10)', 'hai'),
    ('S03-H', span('Q', 'U'), 9, range(10, 15), 'Neutralising titre anti-Aichi H3N2 d14', 'titer')]:
    add(bid, sheet='S03', kind='colgroups', header_row=hr, cols=cols, rows=rows, measurand=meas, unit=scale, scale=scale, time='d14')
add('S03-K', sheet='S03', kind='colgroups', header_row=16, cols=span('L', 'O'), rows=range(17, 22),
    measurand='MLN GC B cells CXCR5+GL7+ (%) d7', unit='%', scale='linear', time='d7')
add('S03-L_Aicda', sheet='S03', kind='rowgroups', label_col='K', rows=range(26, 29), cols=span('L', 'N'),
    measurand='MLN B cell Aicda mRNA (fold) d5', unit='fold', scale='fold', time='d5')
add('S03-L_E47', sheet='S03', kind='rowgroups', label_col='K', rows=range(26, 29), cols=span('O', 'Q'),
    measurand='MLN B cell E47 mRNA (fold) d5', unit='fold', scale='fold', time='d5')
# ---- S04
add('S04-A_ICOSlo', sheet='S04', kind='rowgroups', label_col='A', rows=range(2, 6), cols=span('B', 'F'),
    measurand='MLN Tfh CXCR5+PD1+ ICOS-low (%) d7', unit='%', scale='linear', time='d7')
add('S04-A_ICOShi', sheet='S04', kind='rowgroups', label_col='A', rows=range(2, 6), cols=span('G', 'K'),
    measurand='MLN Tfh CXCR5+PD1+ ICOS-high (%) d7', unit='%', scale='linear', time='d7')
add('S04-B_Foxp3', sheet='S04', kind='colgroups', header_row=7, cols=span('A', 'D'), rows=range(8, 13),
    measurand='MLN Tfr Foxp3+ in CXCR5+ICOShi (%) d7', unit='%', scale='linear', time='d7')
add('S04-B_TfhTfr', sheet='S04', kind='colgroups', header_row=14, cols=span('A', 'D'), rows=range(15, 20),
    measurand='Tfh:Tfr quotient d7 (as printed)', unit='ratio', scale='ratio', time='d7')
add('S04-C', sheet='S04', kind='colgroups', header_row=21, cols=span('A', 'D'), rows=range(22, 27),
    measurand='MLN Tfr Foxp3+ (%) d30', unit='%', scale='linear', time='d30')
add('S04-D', sheet='S04', kind='colgroups', header_row=28, cols=span('A', 'D'), rows=range(29, 32),
    measurand='Lung Treg CD4+Foxp3+ (%) d7', unit='%', scale='linear', time='d7')
# ---- S05
add('S05-A', sheet='S05', kind='spans', time_col='A', rows=range(3, 6),
    groups={'PSLN-212': span('B', 'C'), 'PSLN-344': span('E', 'F'), 'PSLN-212(Y)': span('H', 'I')},
    measurand='Lung NP366-374 tetramer+ CD8 (%) d3/5/7', unit='%', scale='linear', time='day')
add('S05-B', sheet='S05', kind='spans', time_col='A', rows=range(8, 11),
    groups={'PSLN-212': span('B', 'C'), 'PSLN-344': span('E', 'F'), 'PSLN-212(Y)': span('H', 'I')},
    measurand='MLN NP366-374 tetramer+ CD8 (%) d3/5/7', unit='%', scale='linear', time='day')
add('S05-C', sheet='S05', kind='colgroups', header_row=12, cols=span('A', 'D'), rows=range(13, 16),
    measurand='OT-I proliferation (%) d4, +/- pertussis toxin', unit='%', scale='linear', time='d4')
for bid, hr, meas, t in [('S05-D', 18, 'Lung Ki-67+ CD8 (%) d3', 'd3'), ('S05-E', 25, 'Lung GZMB+ CD8 (%) d3', 'd3'),
                         ('S05-F', 32, 'MLN IFN-g+ CD8, H5N1 restim (%) d14', 'd14'),
                         ('S05-G', 39, 'MLN IFN-g+ CD8, H5N1 restim (%) d60', 'd60'),
                         ('S05-H', 46, 'MLN GZMB+ CD8 (%) d60', 'd60'),
                         ('S05-I', 53, 'Lung TRM CD69+CD103+ CD8 (%) d25', 'd25')]:
    add(bid, sheet='S05', kind='colgroups', header_row=hr, cols=span('A', 'D'), rows=range(hr + 1, hr + 6),
        measurand=meas, unit='%', scale='linear', time=t)
# ---- S07
add('S07-A', sheet='S07', kind='spans', time_col='A', rows=range(3, 8),
    groups={'PSLN-212': span('B', 'D'), 'PSLN-344': span('E', 'G')},
    measurand='Lung Ly6C+CCR2+ macrophages (x10^5 cells) d0-30', unit='x1e5', scale='linear', time='day')
add('S07-B_mono', sheet='S07', kind='colgroups', header_row=9, cols=span('B', 'C'), rows=range(10, 15),
    measurand='Lung CD11b+Ly6C+ monocytes (%) +/- INCB3344', unit='%', scale='linear', time='not stated')
add('S07-B_Ly6CMac', sheet='S07', kind='colgroups', header_row=9, cols=span('E', 'F'), rows=range(10, 15),
    measurand='Lung Ly6C+ macrophages (%) +/- INCB3344', unit='%', scale='linear', time='not stated')
add('S07-C', sheet='S07', kind='colgroups', header_row=15, cols=span('B', 'C'), rows=range(16, 21),
    measurand='Lung Treg (%) after macrophage transfer (group labels duplicated)', unit='%', scale='linear', time='d4 post transfer')
# ---- S08
add('S08-A', sheet='S08', kind='spans', time_col='A', rows=range(3, 8),
    groups={'CMP-204': span('B', 'D'), 'PSLN-212': span('E', 'G'), 'PSLN-344': span('H', 'J'), 'PSLN-344/R848': span('K', 'M')},
    measurand='Lung Ifnb1 mRNA (fold) 16 h vs dose (ug)', unit='fold', scale='fold', time='dose')
add('S08-B', sheet='S08', kind='spans', time_col=None, rows=[11],
    groups={'CMP-204': span('A', 'C'), 'PSLN-212': span('D', 'F'), 'PSLN-R848': span('G', 'I'), 'PSLN-212/R848': span('J', 'L'), 'PSLN-344': span('M', 'O')},
    measurand='Encapsulation efficiency (%)', unit='%', scale='linear', time='n/a')
add('S08-C', sheet='S08', kind='colgroups', header_row=13, cols=span('A', 'D'), rows=range(14, 19),
    measurand='AEC SRB+ (%) 16 h, PSLN-SRB vs PSLN-344-SRB', unit='%', scale='linear', time='16h')
# ---- S10
add('S10-A_Ifnb1', sheet='S10', kind='colgroups', header_row=2, cols=span('A', 'D'), rows=range(3, 8),
    measurand='CNS Ifnb1 mRNA (fold) 36 h', unit='fold', scale='fold', time='36h')
add('S10-A_Tnf', sheet='S10', kind='colgroups', header_row=2, cols=span('F', 'I'), rows=range(3, 8),
    measurand='CNS Tnf mRNA (fold) 36 h', unit='fold', scale='fold', time='36h')
add('S10-A_Isg15', sheet='S10', kind='colgroups', header_row=2, cols=span('K', 'N'), rows=range(3, 8),
    measurand='CNS Isg15 mRNA (fold) 36 h', unit='fold', scale='fold', time='36h')
# ---- S11
add('S11-A', sheet='S11', kind='spans', time_col='A', rows=range(3, 8),
    groups={'Vaccine': span('B', 'F'), 'PSLN-212': span('G', 'K'), 'PSLN-344': span('L', 'P'), 'PSLN-212(Y)': span('Q', 'U')},
    measurand='Lung alveolar macrophages (%) d0-8', unit='%', scale='linear', time='day')
add('S11-B', sheet='S11', kind='spans', time_col='A', rows=range(10, 15),
    groups={'Vaccine': span('B', 'F'), 'PSLN-212': span('G', 'K'), 'PSLN-344': span('L', 'P'), 'PSLN-212(Y)': span('Q', 'U')},
    measurand='Lung neutrophils (%) d0-8', unit='%', scale='linear', time='day')
add('S11-C', sheet='S11', kind='colgroups', header_row=16, cols=span('A', 'B'), rows=range(17, 22),
    measurand='Lung recruited monocytes (%) d3, +/- carbenoxolone', unit='%', scale='linear', time='d3')
add('S11-D', sheet='S11', kind='spans', time_col='A', rows=range(24, 29),
    groups={'Vaccine': span('B', 'F'), 'PSLN-212': span('G', 'K'), 'PSLN-344': span('L', 'P'), 'PSLN-212(Y)': span('Q', 'U')},
    measurand='Lung NK cells (%) d0-8', unit='%', scale='linear', time='day')
add('S11-E', sheet='S11', kind='colgroups', header_row=30, cols=span('A', 'D'), rows=range(31, 36),
    measurand='Lung CD206+ macrophages (%) (timepoint not stated)', unit='%', scale='linear', time='not stated')
# ---- S12
add('S12-A', sheet='S12', kind='colgroups', header_row=2, cols=span('A', 'B'), rows=range(3, 6),
    measurand='Infiltrating CD45.2+ monocytes (%) d3, WT vs Ifnar-/- BM (young)', unit='%', scale='linear', time='d3')
# ---- S13
for bid, cols, meas in [('S13-A', span('A', 'C'), 'Serum IgG2a anti-CA09 H1N1 d14'),
                        ('S13-B', span('E', 'G'), 'Serum IgG1 anti-CA09 H1N1 d14'),
                        ('S13-C', span('I', 'K'), 'Serum IgG2a anti-Aichi H3N2 d14'),
                        ('S13-D', span('M', 'O'), 'Serum IgG1 anti-Aichi H3N2 d14')]:
    add(bid, sheet='S13', kind='colgroups', header_row=2, cols=cols, rows=range(3, 8), measurand=meas, unit='titer', scale='titer', time='d14')
add('S13-H', sheet='S13', kind='colgroups', header_row=52, cols=span('A', 'D'), rows=range(53, 58),
    measurand='MLN B220+ IgG+ (%) (timepoint not stated)', unit='%', scale='linear', time='not stated')
add('S13-I', sheet='S13', kind='colgroups', header_row=52, cols=span('F', 'J'), rows=range(53, 58),
    measurand='Serum IgG anti-CA09 H1N1 d28 (boost d14)', unit='titer', scale='titer', time='d28')
add('S13-J', sheet='S13', kind='colgroups', header_row=52, cols=span('L', 'P'), rows=range(53, 58),
    measurand='Serum IgG anti-Aichi H3N2 d28 (boost d14)', unit='titer', scale='titer', time='d28')
# ---- S14
add('S14-A_H1N1', sheet='S14', kind='colgroups', header_row=2, cols=span('A', 'D'), rows=range(3, 8),
    measurand='MLN IFN-g+ CD8, CA09 H1N1 restim (%)', unit='%', scale='linear', time='not stated')
add('S14-A_H3N2', sheet='S14', kind='colgroups', header_row=2, cols=span('F', 'I'), rows=range(3, 8),
    measurand='MLN IFN-g+ CD8, Aichi H3N2 restim (%)', unit='%', scale='linear', time='not stated')

# S09-A: two panels, 7 analytes x 7 groups x 3 replicates (log10 fold)
S09A_GROUPS_P1 = {'PBS': span('B', 'D'), 'CMP-204': span('E', 'G'), 'PSLN-212': span('H', 'J'), 'PSLN-R848': span('K', 'M'),
                  'PSLN-212/R848': span('N', 'P'), 'PSLN-344': span('Q', 'S'), 'PSLN-212(Y)': span('T', 'V')}
S09A_GROUPS_P2 = {'PBS': span('Y', 'AA'), 'CMP-204': span('AB', 'AD'), 'PSLN-212': span('AE', 'AG'), 'PSLN-R848': span('AH', 'AJ'),
                  'PSLN-212/R848': span('AK', 'AM'), 'PSLN-344': span('AN', 'AP'), 'PSLN-212(Y)': span('AQ', 'AS')}
add('S09-A_panel1', sheet='S09', kind='spans', time_col='A', rows=range(3, 10), groups=S09A_GROUPS_P1,
    measurand='Lung cytokine mRNA (log10 fold), panel 1 (label: 16 h)', unit='log10 fold', scale='log10', time='analyte')
add('S09-A_panel2', sheet='S09', kind='spans', time_col='X', rows=range(3, 10), groups=S09A_GROUPS_P2,
    measurand='Lung cytokine mRNA (log10 fold), panel 2 (label: 16 h; values match S01-A 72 h)', unit='log10 fold', scale='log10', time='analyte')

# ---------------------------------------------------------------------------
# Survival blocks (days column, group indicator columns, rows)
# ---------------------------------------------------------------------------
SURV = {}
def addS(bid, sheet, days_col, header_row, group_cols, rows, desc, cohort, challenge_day=None):
    SURV[bid] = dict(sheet=sheet, days_col=days_col, header_row=header_row, group_cols=group_cols, rows=rows, desc=desc, cohort=cohort, challenge_day=challenge_day)

addS('S03-I', 'S03', 'A', 16, span('B', 'F'), range(17, 52), 'Bivalent vax; 10x mLD50 CA09 H1N1 d14 (homologous)', 'aged BALB/c', 14)
addS('S03-J', 'S03', 'G', 16, span('H', 'J'), range(17, 47), 'rgH5N1 vax; WT VN04 H5N1 d2 (homologous, rapid)', 'age not stated (default aged)', 2)
addS('S06-A', 'S06', 'A', 2, span('B', 'E'), range(3, 31), 'H3N2 vax; 5x PR8 H1N1 d14 (heterosubtypic)', 'aged BALB/c', 14)
addS('S06-B', 'S06', 'G', 2, span('H', 'K'), range(3, 31), 'H3N2 vax; 5x PR8 H1N1 d3 (heterosubtypic, rapid)', 'aged BALB/c', 3)
addS('S06-C', 'S06', 'M', 2, span('N', 'Q'), range(3, 31), 'Bivalent vax; 5x rgH5N1 d14 (heterosubtypic)', 'aged BALB/c', 14)
addS('S06-D', 'S06', 'A', 33, span('B', 'E'), range(34, 62), 'Bivalent vax; 5x rgH5N1 d3 (heterosubtypic, rapid)', 'aged BALB/c', 3)
addS('S06-E', 'S06', 'G', 33, span('H', 'L'), range(34, 69), 'H3N2 vax; 5x PR8 H1N1 d60 (heterosubtypic, durable)', 'aged BALB/c', 60)
addS('S06-F', 'S06', 'M', 33, span('N', 'R'), range(34, 69), 'Bivalent vax; 5x rgH5N1 d60 (heterosubtypic, durable)', 'aged BALB/c', 60)
addS('S06-G', 'S06', 'A', 70, span('B', 'F'), range(71, 106), 'H1N1 vax; 5x Perth H3N2 d60 (heterosubtypic, durable)', 'aged BALB/c', 60)
addS("S06-E'(r71-98,G-K)", 'S06', 'G', 70, span('H', 'K'), range(71, 99), 'Imprinting model; bivalent vax; 5x PR8 H1N1', '14-mo BALB/c (10-mo imprint)', None)
addS("S06-F'(r71-98,M-Q)", 'S06', 'M', 70, span('N', 'Q'), range(71, 99), 'Imprinting model; bivalent vax; 5x Perth H3N2 d14', '14-mo BALB/c (10-mo imprint)', 14)
addS('S09-B', 'S09', 'A', 11, span('B', 'D'), range(12, 36), 'H3N2 vax; 5x PR8 H1N1 d21', 'young BALB/c', 21)
addS('S09-D', 'S09', 'A', 38, span('B', 'D'), range(39, 63), 'H1N1 vax; 5x Perth H3N2 d21', 'young BALB/c', 21)
addS('S09-F', 'S09', 'A', 65, span('B', 'D'), range(66, 89), 'Bivalent vax; 5x rgH5N1 d180', 'young BALB/c', 180)
addS('S13-E', 'S13', 'R', 2, span('S', 'V'), range(3, 31), 'Bivalent vax; 10x CA09 H1N1 d14', 'young BALB/c', 14)
addS('S15-H', 'S15', 'A', 72, span('B', 'D'), range(73, 94), 'Vaccine and/or PSLN-344 3 d before 5x rgH5N1', 'aged BALB/c', 3)
addS('S15-L', 'S15', 'A', 102, span('B', 'E'), range(103, 131), 'Bivalent vax; challenge (aged C57BL/6)', 'aged C57BL/6 (20 mo)', None)
addS('S15-N', 'S15', 'A', 133, span('B', 'E'), range(134, 162), 'Bivalent vax; challenge (aged Swiss Webster)', 'aged Swiss Webster (20 mo)', None)

# ---------------------------------------------------------------------------
# Body-weight blocks (days column, group spans) and linkage to survival blocks
# ---------------------------------------------------------------------------
BW = {}
def addW(bid, sheet, days_col, rows, groups, linked=None, note=''):
    BW[bid] = dict(sheet=sheet, days_col=days_col, rows=rows, groups=groups, linked=linked, note=note)

addW('S08-D', 'S08', 'A', range(21, 27), {'PSLN-212(Y)': span('B', 'F'), 'CMP-204': span('G', 'K'), 'PSLN-212': span('L', 'P'),
     'PSLN-344': span('Q', 'U'), 'PSLN-212/R848': span('V', 'Z'), 'Vaccine': span('AA', 'AE')}, None, 'post-vaccination tolerability')
addW('S09-C', 'S09', 'F', range(12, 20), {'PSLN-212(Y)': span('G', 'N'), 'Sham': span('O', 'V'), 'PSLN-344(Y)': span('W', 'AD')}, 'S09-B')
addW('S09-E', 'S09', 'F', range(39, 47), {'PSLN-212(Y)': span('G', 'N'), 'Sham': span('O', 'V'), 'PSLN-344(Y)': span('W', 'AD')}, 'S09-D')
addW('S09-G', 'S09', 'F', range(66, 74), {'PSLN-212(Y)': span('G', 'N'), 'Sham': span('O', 'V'), 'PSLN-344(Y)': span('W', 'AD')}, 'S09-F')
addW('S13-F', 'S13', 'A', range(33, 41), {'PSLN-212(Y)': span('B', 'H'), 'Sham': span('I', 'O'), 'PSLN-212': span('P', 'V'),
     'PSLN-344': span('W', 'AC'), 'Naive': span('AD', 'AJ')}, 'S03-I')
addW('S13-G', 'S13', 'A', range(43, 51), {'PSLN-344': span('B', 'K'), 'Sham': span('L', 'U'), 'Naive': span('V', 'AE')}, 'S03-J')
G4 = {'PSLN-212(Y)': span('B', 'H'), 'Sham': span('I', 'O'), 'PSLN-212': span('P', 'V'), 'PSLN-344': span('W', 'AC')}
G5 = dict(G4, **{'Untreated': span('AD', 'AJ')})
addW('S15-A', 'S15', 'A', range(3, 11), G4, 'S06-A')
addW('S15-B', 'S15', 'A', range(13, 21), G4, 'S06-B')
addW('S15-C', 'S15', 'A', range(23, 31), G4, 'S06-C')
addW('S15-D', 'S15', 'A', range(33, 41), G4, 'S06-D')
addW('S15-E', 'S15', 'A', range(43, 51), G5, 'S06-E')
addW('S15-F', 'S15', 'A', range(53, 61), G5, 'S06-F')
addW('S15-G', 'S15', 'A', range(63, 71), G5, 'S06-G')
addW('S15-I', 'S15', 'H', range(72, 80), {'3d Vaccine': span('I', 'O'), '3d PSLN-344': span('P', 'V'), '3d Vaccine+PSLN-344': span('W', 'AC')}, 'S15-H')
G_IMP = {'Naive+PSLN-212': span('I', 'O'), 'Imprinting+PSLN-212': span('P', 'V'), 'Naive+PSLN-344': span('W', 'AC'), 'Imprinting+PSLN-344': span('AD', 'AJ')}
addW('S15-J', 'S15', 'H', range(83, 91), G_IMP, "S06-E'(r71-98,G-K)")
addW('S15-K', 'S15', 'H', range(93, 101), G_IMP, "S06-F'(r71-98,M-Q)")
G_M = {'PSLN-212(Y)': span('I', 'O'), 'Sham': span('P', 'V'), 'PSLN-212': span('W', 'AC'), 'PSLN-344': span('AD', 'AJ')}
addW('S15-M', 'S15', 'H', range(103, 111), G_M, 'S15-L')
addW('S15-O', 'S15', 'H', range(134, 142), G_M, 'S15-N')
