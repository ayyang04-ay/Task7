"""
Block registry for psln_program_dataset.xlsx.

Every block is addressed by explicit cell ranges so each number in the proposal can be traced
back to the workbook.  Group labels are kept exactly "as printed"; interpretation flags live in
the QC log, never in the raw labels.

kinds
-----
cols : one group per column, replicate animals down the rows
rows : one group per row, replicate animals across the columns
tc   : time course / dose series - one row per time (or dose), each group owns a column span
surv : time-to-event - a 'days' column and one 0/1 flag column per group
bw   : body weight - one row per day, each group owns a column span (one column per animal)
"""
import re
import openpyxl
import pandas as pd
from openpyxl.utils import column_index_from_string as C

WB_PATH = '/tmp/world/filesystem/psln_program_dataset.xlsx'

def _span(a, b):
    return list(range(C(a), C(b) + 1))

B = []   # registry

def cols(id, sheet, rows, groups, stated_n, **meta):
    """groups: list of (label, column letter)"""
    B.append(dict(id=id, sheet=sheet, kind='cols', rows=rows, groups=groups, stated_n=stated_n, **meta))

def rows_(id, sheet, groups, colspan, stated_n, **meta):
    """groups: list of (label, row number); colspan: (first,last) letters"""
    B.append(dict(id=id, sheet=sheet, kind='rows', groups=groups, colspan=colspan, stated_n=stated_n, **meta))

def tc(id, sheet, rows, xcol, groups, stated_n, xname='day', **meta):
    """groups: list of (label, first col, last col)"""
    B.append(dict(id=id, sheet=sheet, kind='tc', rows=rows, xcol=xcol, groups=groups, stated_n=stated_n, xname=xname, **meta))

def surv(id, sheet, rows, daycol, groups, stated_n, **meta):
    """groups: list of (label, flag column letter)"""
    B.append(dict(id=id, sheet=sheet, kind='surv', rows=rows, daycol=daycol, groups=groups, stated_n=stated_n, **meta))

def bw(id, sheet, rows, xcol, groups, stated_n, **meta):
    B.append(dict(id=id, sheet=sheet, kind='bw', rows=rows, xcol=xcol, groups=groups, stated_n=stated_n, xname='day', **meta))

G4 = ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']
G5 = ['Sham', 'CMP-204', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']

# ----------------------------------------------------------------------------------- S01
g8 = ['Sham', 'CMP-204', 'PSLN-212', 'PSLN-R848', 'PSLN-212/R848', 'PSLN-344', 'PSLN-212(Y)', 'PSLN-344(Y)']
rows_('S01-A 16h', 'S01', [(g, 3 + i) for i, g in enumerate(g8)], ('B', 'F'), 5,
      measurand='Ifnb1 mRNA, total lung cells (qRT-PCR), fold vs untreated', scale='linear', time='16 h', antigen='none')
rows_('S01-A 72h', 'S01', [(g, 3 + i) for i, g in enumerate(g8)], ('H', 'L'), 5,
      measurand='Ifnb1 mRNA, total lung cells (qRT-PCR), fold vs untreated', scale='linear', time='72 h', antigen='none')
rows_('S01-B', 'S01', [('AECII/PSLN-SRB', 14), ('AECI/PSLN-SRB', 15), ('AECII/FreeSRB', 16), ('AECI/FreeSRB', 17)], ('B', 'F'), 5,
      measurand='% SRB+ alveolar epithelial cells', scale='linear %', time='16 h')
rows_('S01-C', 'S01', [('WT', 20), ('SPA/D', 21)], ('B', 'E'), 4,
      measurand='% DiD+ alveolar macrophages', scale='linear %', time='16 h')
tc('S01-D', 'S01', (24, 28), 'A', [('Sham', 'B', 'F'), ('PSLN-212', 'G', 'K'), ('PSLN-344', 'L', 'P'), ('PSLN-212(Y)', 'Q', 'U')], 5,
   measurand='% lung monocytes (CD11b+Ly6C+CD11c-Ly6G-)', scale='linear %')
tc('S01-E', 'S01', (30, 34), 'A', [('Sham', 'B', 'F'), ('PSLN-212', 'G', 'K'), ('PSLN-344', 'L', 'P'), ('PSLN-212(Y)', 'Q', 'U'), ('PSLN-344(Y)', 'V', 'Z')], 5,
   measurand='% lung CD11b+ DC (CD11c+MHC-II+CD11b+F4/80-)', scale='linear %')
for bid, r, m in [('S01-F', 36, '% lung cDC1 (XCR1+CD172a-CD11c+CD26+)'), ('S01-G', 38, '% lung cDC2 (XCR1-CD172a+CD11c+CD26+)')]:
    tc(bid, 'S01', (r, r), None, [('Sham', 'B', 'F'), ('PSLN-212', 'G', 'K'), ('PSLN-344', 'L', 'P'), ('PSLN-212(Y)', 'Q', 'U'), ('PSLN-344(Y)', 'V', 'Z')], 5,
       measurand=m, scale='linear %', time='72 h')

# ----------------------------------------------------------------------------------- S02
cols('S02-A', 'S02', (3, 7), list(zip(G4, 'ABCD')), 5, measurand='% CCR7+ of lung CD11b+ DC', time='72 h')
cols('S02-B', 'S02', (3, 7), list(zip(G4, 'FGHI')), 5, measurand='% MLN CD11b+CD103- DC', time='72 h')
gC = ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)', 'PTX', 'PSLN-344(Y)']
cols('S02-C', 'S02', (3, 7), list(zip(gC, 'KLMNO')), 5, measurand='% OVA-AF647+ MLN DC', time='36 h')
cols('S02-D CD40', 'S02', (10, 14), list(zip(G4, 'ABCD')), 5, measurand='% CD40+ of MLN CD11b+ DC', time='day 3')
cols('S02-D CD86', 'S02', (10, 14), list(zip(G4, 'FGHI')), 5, measurand='% CD86+ of MLN CD11b+ DC', time='day 3')
cols('S02-E', 'S02', (10, 14), list(zip(gC, 'KLMNO')), 5, measurand='% proliferated OT-I CD8 (CFSE dilution) after co-culture with MLN CD11b+ DC', time='DC day 3 + 3 d culture')
tc('S02-F', 'S02', (17, 19), 'A', [('PSLN-344', 'B', 'F'), ('PSLN-212', 'G', 'K'), ('Sham', 'L', 'P')], 5, xname='hour',
   measurand='Gm-csf mRNA, lung (qRT-PCR), fold vs untreated', scale='linear')
cols('S02-G', 'S02', (22, 26), list(zip(['GM-CSF', 'PSLN-212', 'PSLN-212+GM-CSF'], 'BCD')), 5, measurand='% lung Ly6C+CD11c+MHC-II+F4/80-/int (moDC)', time='day 5')
cols('S02-H', 'S02', (30, 34), list(zip(['WT w/o cDC', 'WT w/ cDC', 'IFN w/o cDC', 'IFN w/ cDC', 'GMCSF'], 'BCDEF')), 5, measurand='% CD45.2+ monocyte-derived DC', time='day 3')
cols('S02-I', 'S02', (30, 34), list(zip(['PSLN-344(Y)', 'PSLN-344(Y)+INCB3344'], 'HI')), 5, measurand='% GZMB+ lung CD8 T', time='day 5')

# ----------------------------------------------------------------------------------- S03
cols('S03-A', 'S03', (3, 7), list(zip(G5, 'ABCDE')), 5, measurand='serum IgG anti-CA09 H1N1 (endpoint titre)', time='day 14', titre=True)
g3 = ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']
cols('S03-B', 'S03', (3, 7), list(zip(g3, 'GHI')), 5, measurand='IgG2a/IgG1 quotient, anti-CA09 H1N1', time='day 14')
cols('S03-C', 'S03', (3, 7), list(zip(G5, 'KLMNO')), 5, measurand='HAI titre vs CA09 H1N1 (LLOD 10)', time='day 14', titre=True)
cols('S03-D', 'S03', (3, 7), list(zip(G5, 'QRSTU')), 5, measurand='neutralising titre vs CA09 H1N1', time='day 14', titre=True)
cols('S03-E', 'S03', (10, 14), list(zip(G5, 'ABCDE')), 5, measurand='serum IgG anti-Aichi H3N2 (endpoint titre)', time='day 14', titre=True)
cols('S03-F', 'S03', (10, 14), list(zip(g3, 'GHI')), 5, measurand='IgG2a/IgG1 quotient, anti-Aichi H3N2', time='day 14')
cols('S03-G', 'S03', (10, 14), list(zip(G5, 'KLMNO')), 5, measurand='HAI titre vs Aichi H3N2 (LLOD 10)', time='day 14', titre=True)
cols('S03-H', 'S03', (10, 14), list(zip(G5, 'QRSTU')), 5, measurand='neutralising titre vs Aichi H3N2', time='day 14', titre=True)
surv('S03-I', 'S03', (17, 51), 'A', list(zip(G5, 'BCDEF')), 7,
     model='aged BALB/c; bivalent vaccine i.n.; 10x mLD50 CA09 H1N1 at d14', obs_days=14)
surv('S03-J', 'S03', (17, 46), 'G', list(zip(['Sham', 'PSLN-212', 'PSLN-344'], 'HIJ')), 9,
     model='aged BALB/c; rgH5N1 vaccine i.n.; wild-type VN04 H5N1 at d2', obs_days=22)
cols('S03-K', 'S03', (17, 21), list(zip(G4, 'LMNO')), 5, measurand='% GC B cells (CXCR5+GL7+) in MLN', time='day 7')
rows_('S03-L Aicda', 'S03', [('Sham', 26), ('PSLN-212', 27), ('PSLN-344', 28)], ('L', 'N'), 3, measurand='Aicda mRNA, MLN B cells, fold vs untreated', time='day 5')
rows_('S03-L E47', 'S03', [('Sham', 26), ('PSLN-212', 27), ('PSLN-344', 28)], ('O', 'Q'), 3, measurand='E47 mRNA, MLN B cells, fold vs untreated', time='day 5')

# ----------------------------------------------------------------------------------- S04
rows_('S04-A ICOSlo', 'S04', [(g, 2 + i) for i, g in enumerate(G4)], ('B', 'F'), 5, measurand='% Tfh ICOS-lo (CD4+CXCR5+PD1+), MLN', time='day 7')
rows_('S04-A ICOShi', 'S04', [(g, 2 + i) for i, g in enumerate(G4)], ('G', 'K'), 5, measurand='% Tfh ICOS-hi (CD4+CXCR5+PD1+), MLN', time='day 7')
cols('S04-B Foxp3', 'S04', (8, 12), list(zip(G4, 'ABCD')), 5, measurand='% Tfr (Foxp3+ in CXCR5+ICOShi CD4), MLN', time='day 7')
cols('S04-B Tfh:Tfr', 'S04', (15, 19), list(zip(G4, 'ABCD')), 5, measurand='Tfh:Tfr quotient, MLN', time='day 7')
cols('S04-C', 'S04', (22, 26), list(zip(G4, 'ABCD')), 5, measurand='% Tfr, MLN', time='day 30')
cols('S04-D', 'S04', (29, 31), list(zip(G4, 'ABCD')), 3, measurand='% lung Treg (CD4+Foxp3+)', time='day 7')

# ----------------------------------------------------------------------------------- S05
g3y = ['PSLN-212', 'PSLN-344', 'PSLN-212Y']
tc('S05-A', 'S05', (3, 5), 'A', [('PSLN-212', 'B', 'C'), ('PSLN-344', 'E', 'F'), ('PSLN-212Y', 'H', 'I')], 3, measurand='% NP366-374 tetramer+ of lung CD8 T')
tc('S05-B', 'S05', (8, 10), 'A', [('PSLN-212', 'B', 'C'), ('PSLN-344', 'E', 'F'), ('PSLN-212Y', 'H', 'I')], 3, measurand='% NP366-374 tetramer+ of MLN CD8 T')
cols('S05-C', 'S05', (13, 15), list(zip(['Lung', 'Lung+PTX', 'MLN', 'MLN+PTX'], 'ABCD')), 3, measurand='% proliferating transferred OT-I CD8', time='day 4')
cols('S05-D', 'S05', (19, 23), list(zip(G4, 'ABCD')), 5, measurand='% Ki-67+ lung CD8 T', time='day 3')
cols('S05-E', 'S05', (26, 30), list(zip(G4, 'ABCD')), 5, measurand='% GZMB+ lung CD8 T', time='day 3')
cols('S05-F', 'S05', (33, 37), list(zip(G4, 'ABCD')), 5, measurand='% IFN-g+ CD8 T, MLN, rgH5N1 restim', time='day 14')
cols('S05-G', 'S05', (40, 44), list(zip(G4, 'ABCD')), 5, measurand='% IFN-g+ CD8 T, MLN, rgH5N1 restim', time='day 60')
cols('S05-H', 'S05', (47, 51), list(zip(G4, 'ABCD')), 5, measurand='% GZMB+ CD8 T, MLN', time='day 60')
cols('S05-I', 'S05', (54, 58), list(zip(G4, 'ABCD')), 5, measurand='% lung CD8 TRM (CD69+CD103+)', time='day 25')

# ----------------------------------------------------------------------------------- S06 (time to event)
surv('S06-A', 'S06', (3, 30), 'A', list(zip(G4, 'BCDE')), 7, model='aged BALB/c; Aichi H3N2 vaccine; 5x mLD50 PR8 H1N1 at d14', obs_days=14)
surv('S06-B', 'S06', (3, 30), 'G', list(zip(G4, 'HIJK')), 7, model='aged BALB/c; Aichi H3N2 vaccine; 5x mLD50 PR8 H1N1 at d3', obs_days=14)
surv('S06-C', 'S06', (3, 30), 'M', list(zip(G4, 'NOPQ')), 7, model='aged BALB/c; bivalent vaccine; 5x mLD50 rgH5N1 at d14', obs_days=14)
surv('S06-D', 'S06', (34, 61), 'A', list(zip(G4, 'BCDE')), 7, model='aged BALB/c; bivalent vaccine; 5x mLD50 rgH5N1 at d3', obs_days=14)
G4U = G4 + ['Untreated']
surv('S06-E', 'S06', (34, 68), 'G', list(zip(G4U, 'HIJKL')), 7, model='aged BALB/c; Aichi H3N2 vaccine; 5x mLD50 PR8 H1N1 at d60', obs_days=14)
surv('S06-F', 'S06', (34, 68), 'M', list(zip(G4U, 'NOPQR')), 7, model='aged BALB/c; bivalent vaccine; 5x mLD50 rgH5N1 at d60', obs_days=14)
surv('S06-G', 'S06', (71, 105), 'A', list(zip(G4U, 'BCDEF')), 7, model='aged BALB/c; CA09 H1N1 vaccine; 5x mLD50 Perth H3N2 at d60', obs_days=14)
gI = ['Naive+PSLN-212', 'Imprinting+PSLN-212', 'Naive+PSLN-344', 'Imprinting+PSLN-344']
surv('S06-E[r71]', 'S06', (71, 98), 'G', list(zip(gI, 'HIJK')), 7, printed_label='S06-E',
     model='BALB/c 10 mo at PR8 imprinting/saline, vaccinated 4 mo later (bivalent); 5x LD50 PR8 H1N1', obs_days=14)
surv('S06-F[r71]', 'S06', (71, 98), 'M', list(zip(gI, 'NOPQ')), 7, printed_label='S06-F',
     model='BALB/c 10 mo at PR8 imprinting/saline, vaccinated 4 mo later (bivalent); 5x LD50 Perth H3N2 at d14', obs_days=14)

# ----------------------------------------------------------------------------------- S07
tc('S07-A', 'S07', (3, 7), 'A', [('PSLN-212', 'B', 'D'), ('PSLN-344', 'E', 'G')], 3, measurand='lung Ly6C+CCR2+ macrophages (x10^5 cells)')
cols('S07-B mono', 'S07', (10, 14), list(zip(['PSLN-344', 'PSLN-344+INCB3344'], 'BC')), 5, measurand='% lung CD11b+Ly6C+ monocytes')
cols('S07-B Ly6C+Mph', 'S07', (10, 14), list(zip(['PSLN-344', 'PSLN-344+INCB3344'], 'EF')), 5, measurand='% lung Ly6C+ macrophages')
cols('S07-C', 'S07', (16, 20), [('Ly6C-CD206+ MPhi [col B]', 'B'), ('Ly6C-CD206+ MPhi [col C]', 'C')], 5, measurand='% lung Treg after macrophage transfer', time='day 4 post transfer')

# ----------------------------------------------------------------------------------- S08
tc('S08-A', 'S08', (3, 7), 'A', [('CMP-204', 'B', 'D'), ('PSLN-212', 'E', 'G'), ('PSLN-344', 'H', 'J'), ('PSLN-344/R848', 'K', 'M')], 3, xname='dose_ug',
   measurand='Ifnb1 mRNA, lung, 16 h, fold vs untreated', scale='linear')
tc('S08-B', 'S08', (11, 11), None, [('CMP-204', 'A', 'C'), ('PSLN-212', 'D', 'F'), ('PSLN-R848', 'G', 'I'), ('PSLN-212/R848', 'J', 'L'), ('PSLN-344', 'M', 'O')], 3,
   measurand='encapsulation efficiency (%)')
cols('S08-C', 'S08', (14, 18), list(zip(['AECII-PSLN-SRB', 'AECII-PSLN-344-SRB', 'AECI-PSLN-SRB', 'AECI-PSLN-344-SRB'], 'ABCD')), 5, measurand='% SRB+ alveolar epithelial cells', time='16 h')
bw('S08-D', 'S08', (21, 26), 'A', [('PSLN-212(Y)', 'B', 'F'), ('CMP-204', 'G', 'K'), ('PSLN-212', 'L', 'P'), ('PSLN-344', 'Q', 'U'), ('PSLN-212/R848', 'V', 'Z'), ('Vaccine', 'AA', 'AE')], 5,
   measurand='body weight after immunisation (% of day 0)', model='CA09 vaccine + 20 ug adjuvant i.n.; no challenge')

# ----------------------------------------------------------------------------------- S09
genes = ['Ifnb1', 'Il6', 'Ccl2', 'Ccl3', 'Ccl5', 'Tnf', 'Il10']
g7 = ['PBS', 'CMP-204', 'PSLN-212', 'PSLN-R848', 'PSLN-212/R848', 'PSLN-344', 'PSLN-212(y)']
p1 = [('B', 'D'), ('E', 'G'), ('H', 'J'), ('K', 'M'), ('N', 'P'), ('Q', 'S'), ('T', 'V')]
p2 = [('Y', 'AA'), ('AB', 'AD'), ('AE', 'AG'), ('AH', 'AJ'), ('AK', 'AM'), ('AN', 'AP'), ('AQ', 'AS')]
for i, gname in enumerate(genes):
    tc(f'S09-A[A:U] {gname}', 'S09', (3 + i, 3 + i), None, [(g, a, b) for g, (a, b) in zip(g7, p1)], 3, printed_label='S09-A 16h n=3 Log10',
       measurand=f'{gname} mRNA lung, log10 fold vs untreated', scale='log10', time='16 h (as printed)')
    tc(f'S09-A[X:AS] {gname}', 'S09', (3 + i, 3 + i), None, [(g, a, b) for g, (a, b) in zip(g7, p2)], 3, printed_label='S09-A 16h n=3 Log10',
       measurand=f'{gname} mRNA lung, log10 fold vs untreated', scale='log10', time='16 h (as printed; values match S01-A 72 h)')
gY = ['Sham', 'PSLN-344Y', 'PSLN-212Y']
bwY = [('PSLN-212Y', 'G', 'N'), ('Sham', 'O', 'V'), ('PSLN-344Y', 'W', 'AD')]
surv('S09-B', 'S09', (12, 35), 'A', list(zip(gY, 'BCD')), 8, model='young BALB/c; Aichi H3N2 vaccine; 5x mLD50 PR8 H1N1 at d21', obs_days=14)
bw('S09-C', 'S09', (12, 19), 'F', bwY, 8, pair='S09-B')
surv('S09-D', 'S09', (39, 62), 'A', list(zip(gY, 'BCD')), 8, model='young BALB/c; CA09 H1N1 vaccine; 5x mLD50 Perth H3N2 at d21', obs_days=14)
bw('S09-E', 'S09', (39, 46), 'F', bwY, 8, pair='S09-D')
surv('S09-F', 'S09', (66, 88), 'A', list(zip(gY, 'BCD')), 8, model='young BALB/c; bivalent vaccine; 5x mLD50 rgH5N1 at d180', obs_days=14)
bw('S09-G', 'S09', (66, 73), 'F', bwY, 8, pair='S09-F')

# ----------------------------------------------------------------------------------- S10
gS10 = ['PBS', 'Sham', 'PSLN-344', 'CT']
cols('S10-A Ifnb1', 'S10', (3, 7), list(zip(gS10, 'ABCD')), 5, measurand='Ifnb1 mRNA, CNS, fold vs untreated', time='36 h')
cols('S10-A Tnf', 'S10', (3, 7), list(zip(gS10, 'FGHI')), 5, measurand='Tnf mRNA, CNS, fold vs untreated', time='36 h')
cols('S10-A Isg15', 'S10', (3, 7), list(zip(gS10, 'KLMN')), 5, measurand='Isg15 mRNA, CNS, fold vs untreated', time='36 h')

# ----------------------------------------------------------------------------------- S11
gV = [('Vaccine', 'B', 'F'), ('PSLN-212', 'G', 'K'), ('PSLN-344', 'L', 'P'), ('PSLN-212(Y)', 'Q', 'U')]
tc('S11-A', 'S11', (3, 7), 'A', gV, 5, measurand='% alveolar macrophages in lung')
tc('S11-B', 'S11', (10, 14), 'A', gV, 5, measurand='% neutrophils in lung')
cols('S11-C', 'S11', (17, 21), list(zip(['CBX+', 'CBX-'], 'AB')), 5, measurand='% recruited lung monocytes (PSLN-344 + CA09 vaccine)', time='day 3')
tc('S11-D', 'S11', (24, 28), 'A', gV, 5, measurand='% NK cells in lung')
cols('S11-E', 'S11', (31, 35), list(zip(G4, 'ABCD')), 5, measurand='% CD206+ macrophages in lung', time='not stated')

# ----------------------------------------------------------------------------------- S12
cols('S12-A', 'S12', (3, 5), list(zip(['WT to WT', 'IFNAR-/- to WT'], 'AB')), 3, measurand='% infiltrating CD45.2+ monocytes', time='day 3')

# ----------------------------------------------------------------------------------- S13
cols('S13-A', 'S13', (3, 7), list(zip(g3, 'ABC')), 5, measurand='serum IgG2a anti-CA09 H1N1', time='day 14', titre=True)
cols('S13-B', 'S13', (3, 7), list(zip(g3, 'EFG')), 5, measurand='serum IgG1 anti-CA09 H1N1', time='day 14', titre=True)
cols('S13-C', 'S13', (3, 7), list(zip(g3, 'IJK')), 5, measurand='serum IgG2a anti-Aichi H3N2', time='day 14', titre=True)
cols('S13-D', 'S13', (3, 7), list(zip(g3, 'MNO')), 5, measurand='serum IgG1 anti-Aichi H3N2', time='day 14', titre=True)
surv('S13-E', 'S13', (3, 30), 'R', list(zip(['Naive', 'Sham', 'CMP-204(Y)', 'PSLN-344(Y)'], 'STUV')), 5,
     model='young BALB/c; bivalent vaccine; 10x mLD50 CA09 H1N1 at d14', obs_days=14)
bw('S13-F', 'S13', (33, 40), 'A', [('PSLN-212(Y)', 'B', 'H'), ('Sham', 'I', 'O'), ('PSLN-212', 'P', 'V'), ('PSLN-344', 'W', 'AC'), ('Naive', 'AD', 'AJ')], 7, pair='S03-I')
bw('S13-G', 'S13', (43, 50), 'A', [('PSLN-344', 'B', 'K'), ('Sham', 'L', 'U'), ('Naive', 'V', 'AE')], 10, pair='S03-J')
cols('S13-H', 'S13', (53, 57), list(zip(G4, 'ABCD')), 5, measurand='% IgG+ of MLN B220+ cells', time='not stated')
cols('S13-I', 'S13', (53, 57), list(zip(G5, 'FGHIJ')), 5, measurand='serum IgG anti-CA09 H1N1 (prime d0 + boost d14)', time='day 28', titre=True)
cols('S13-J', 'S13', (53, 57), list(zip(G5, 'LMNOP')), 5, measurand='serum IgG anti-Aichi H3N2 (prime d0 + boost d14)', time='day 28', titre=True)

# ----------------------------------------------------------------------------------- S14
cols('S14-A H1N1', 'S14', (3, 7), list(zip(G4, 'ABCD')), 5, measurand='% IFN-g+ CD8 T, MLN, CA09 H1N1 restim', time='not stated (as S05-F)')
cols('S14-A H3N2', 'S14', (3, 7), list(zip(G4, 'FGHI')), 5, measurand='% IFN-g+ CD8 T, MLN, Aichi H3N2 restim', time='not stated (as S05-F)')

# ----------------------------------------------------------------------------------- S15
bw4 = [('PSLN-212(Y)', 'B', 'H'), ('Sham', 'I', 'O'), ('PSLN-212', 'P', 'V'), ('PSLN-344', 'W', 'AC')]
bw5 = bw4 + [('Untreated', 'AD', 'AJ')]
for bid, r0, grp, pair in [('S15-A', 3, bw4, 'S06-A'), ('S15-B', 13, bw4, 'S06-B'), ('S15-C', 23, bw4, 'S06-C'), ('S15-D', 33, bw4, 'S06-D'),
                           ('S15-E', 43, bw5, 'S06-E'), ('S15-F', 53, bw5, 'S06-F'), ('S15-G', 63, bw5, 'S06-G')]:
    bw(bid, 'S15', (r0, r0 + 7), 'A', grp, 7, pair=pair)
surv('S15-H', 'S15', (73, 93), 'A', list(zip(['3d Vaccine', '3d PSLN-344', '3d Vaccine+PSLN-344'], 'BCD')), 7,
     model='aged BALB/c; vaccine alone / PSLN-344 alone / both, 3 d before 5x mLD50 rgH5N1', obs_days=14)
bw('S15-I', 'S15', (72, 79), 'H', [('3d Vaccine', 'I', 'O'), ('3d PSLN-344', 'P', 'V'), ('3d Vaccine+PSLN-344', 'W', 'AC')], 7, pair='S15-H')
bwI = [('Naive+PSLN-212', 'I', 'O'), ('Imprinting+PSLN-212', 'P', 'V'), ('Naive+PSLN-344', 'W', 'AC'), ('Imprinting+PSLN-344', 'AD', 'AJ')]
bw('S15-J', 'S15', (83, 90), 'H', bwI, 7, pair='S06-E[r71]')
bw('S15-K', 'S15', (93, 100), 'H', bwI, 7, pair='S06-F[r71]')
surv('S15-L', 'S15', (103, 130), 'A', list(zip(G4, 'BCDE')), 7, model='aged C57BL/6 (20 mo); bivalent vaccine; challenge virus/interval not stated', obs_days=14)
bwS = [('PSLN-212(Y)', 'I', 'O'), ('Sham', 'P', 'V'), ('PSLN-212', 'W', 'AC'), ('PSLN-344', 'AD', 'AJ')]
bw('S15-M', 'S15', (103, 110), 'H', bwS, 7, pair='S15-L')
surv('S15-N', 'S15', (134, 161), 'A', list(zip(G4, 'BCDE')), 7, model='aged Swiss Webster (20 mo); bivalent vaccine; challenge virus/interval not stated', obs_days=14)
bw('S15-O', 'S15', (134, 141), 'H', bwS, 7, pair='S15-N')

BLOCKS = {b['id']: b for b in B}
assert len(BLOCKS) == len(B), 'duplicate ids'

# =================================================================================== loaders
_wb = None
def wb():
    global _wb
    if _wb is None:
        _wb = openpyxl.load_workbook(WB_PATH, data_only=True)
    return _wb

def _cell(ws, r, c):
    v = ws.cell(r, c).value
    return v

def load(bid):
    """Return tidy DataFrame for one block."""
    b = BLOCKS[bid]
    ws = wb()[b['sheet']]
    out = []
    k = b['kind']
    if k == 'cols':
        r0, r1 = b['rows']
        for g, col in b['groups']:
            ci = C(col)
            for j, r in enumerate(range(r0, r1 + 1)):
                v = _cell(ws, r, ci)
                if v is not None:
                    out.append(dict(block=bid, group=g, rep=j + 1, value=float(v), cell=f"{col}{r}"))
    elif k == 'rows':
        a, z = b['colspan']
        for g, r in b['groups']:
            for j, ci in enumerate(_span(a, z)):
                v = _cell(ws, r, ci)
                if v is not None:
                    out.append(dict(block=bid, group=g, rep=j + 1, value=float(v), cell=f"{openpyxl.utils.get_column_letter(ci)}{r}"))
    elif k in ('tc', 'bw'):
        r0, r1 = b['rows']
        for r in range(r0, r1 + 1):
            x = _cell(ws, r, C(b['xcol'])) if b.get('xcol') else None
            if isinstance(x, str):
                m = re.match(r'^\s*(\d+)', x)
                x = float(m.group(1)) if m else x
            for g, a, z in b['groups']:
                for j, ci in enumerate(_span(a, z)):
                    v = _cell(ws, r, ci)
                    if v is not None:
                        out.append(dict(block=bid, group=g, rep=j + 1, x=x, value=float(v), cell=f"{openpyxl.utils.get_column_letter(ci)}{r}"))
    elif k == 'surv':
        r0, r1 = b['rows']
        dc = C(b['daycol'])
        for r in range(r0, r1 + 1):
            d = _cell(ws, r, dc)
            for g, col in b['groups']:
                f = _cell(ws, r, C(col))
                if f is not None:
                    # NB: a flag can exist without a day value (S03-J!J46) - keep it, time = NaN
                    out.append(dict(block=bid, group=g, time=(float(d) if d is not None else float('nan')),
                                    event=int(f), cell=f"{col}{r}"))
    df = pd.DataFrame(out)
    return df

def meta(bid):
    return BLOCKS[bid]

if __name__ == '__main__':
    import sys
    tot = 0
    for bid in BLOCKS:
        df = load(bid)
        tot += len(df)
        print(bid, BLOCKS[bid]['kind'], len(df), dict(df.groupby('group', sort=False).size()))
    print('total observations parsed', tot)
