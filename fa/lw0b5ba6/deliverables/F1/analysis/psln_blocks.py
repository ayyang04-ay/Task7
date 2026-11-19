"""
psln_blocks.py  --  explicit, hand-checked map of every data block in
psln_program_dataset.xlsx to its cell ranges.

Nothing is inferred silently: each group in each block is tied to a cell range
"as printed" in the workbook.  Where I later argue that a printed label is wrong,
the relabelling is done in the analysis scripts (and flagged), never here.

Tidy output columns:
  sheet, block, kind, analyte, group, x (day / hour / dose or None), rep, value, cell
kind: 'point' (one value per animal), 'series' (value per animal per timepoint),
      'surv'  (time-to-event: value = day, event = 1/0), 'weight' (body-weight series)
"""
from paths import TABLES, FIGS, OUT as OUTDIR, BUILD, PANDOC
import openpyxl
from openpyxl.utils import get_column_letter as L, column_index_from_string as C

from paths import XLSX
_wb = openpyxl.load_workbook(XLSX, data_only=True)

def cell(sheet, ref):
    return _wb[sheet][ref].value

def cols(c0, c1):
    return [L(i) for i in range(C(c0), C(c1) + 1)]

ROWS = []   # tidy records

def add(sheet, block, kind, analyte, group, x, rep, value, ref, event=None, note=None):
    ROWS.append(dict(sheet=sheet, block=block, kind=kind, analyte=analyte, group=group,
                     x=x, rep=rep, value=value, event=event, cell=f'{sheet}!{ref}', note=note))

def row_block(sheet, block, analyte, row, groups, x=None, kind='point'):
    """groups: {label: (col0, col1)} all on a single row"""
    for g, (c0, c1) in groups.items():
        for i, c in enumerate(cols(c0, c1)):
            v = cell(sheet, f'{c}{row}')
            if v is not None:
                add(sheet, block, kind, analyte, g, x, i + 1, v, f'{c}{row}')

def col_block(sheet, block, analyte, r0, r1, groups, x=None, kind='point'):
    """groups: {label: col}; one animal per row"""
    for g, c in groups.items():
        for i, r in enumerate(range(r0, r1 + 1)):
            v = cell(sheet, f'{c}{r}')
            if v is not None:
                add(sheet, block, kind, analyte, g, x, i + 1, v, f'{c}{r}')

def series_block(sheet, block, analyte, r0, r1, xcol, groups, kind='series'):
    """rows = timepoints (x in xcol), groups: {label: (col0, col1)}; animals across columns"""
    for r in range(r0, r1 + 1):
        x = cell(sheet, f'{xcol}{r}')
        for g, (c0, c1) in groups.items():
            for i, c in enumerate(cols(c0, c1)):
                v = cell(sheet, f'{c}{r}')
                if v is not None:
                    add(sheet, block, kind, analyte, g, x, i + 1, v, f'{c}{r}')

def surv_block(sheet, block, r0, r1, daycol, groups, analyte='time to event'):
    """one animal per row; day in daycol; group column holds 1 (event) / 0 (censored)"""
    for g, c in groups.items():
        i = 0
        for r in range(r0, r1 + 1):
            e = cell(sheet, f'{c}{r}')
            if e is not None:
                i += 1
                d = cell(sheet, f'{daycol}{r}')
                add(sheet, block, 'surv', analyte, g, None, i, d, f'{daycol}{r}/{c}{r}', event=e,
                    note=None if d is not None else 'event flag present but day cell empty')

# ------------------------------------------------------------------ S01
for hrs, (c0, c1) in {'16h': ('B', 'F'), '72h': ('H', 'L')}.items():
    for r in range(3, 11):
        g = cell('S01', f'A{r}')
        row_block('S01', 'S01-A', f'Ifnb1 lung {hrs} (fold vs untreated)', r, {g: (c0, c1)}, x=hrs)
for r in range(14, 18):
    row_block('S01', 'S01-B', 'SRB+ alveolar epithelial cells (%)', r, {cell('S01', f'A{r}'): ('B', 'F')})
for r in (20, 21):
    row_block('S01', 'S01-C', 'DiD+ alveolar macrophages (%)', r, {cell('S01', f'A{r}'): ('B', 'E')})
series_block('S01', 'S01-D', 'lung monocytes CD11b+Ly6C+ (%)', 24, 28, 'A',
             {'Sham': ('B', 'F'), 'PSLN-212': ('G', 'K'), 'PSLN-344': ('L', 'P'), 'PSLN-212(Y)': ('Q', 'U')})
series_block('S01', 'S01-E', 'lung CD11b+ DC (%)', 30, 34, 'A',
             {'Sham': ('B', 'F'), 'PSLN-212': ('G', 'K'), 'PSLN-344': ('L', 'P'), 'PSLN-212(Y)': ('Q', 'U'),
              'PSLN-344(Y)': ('V', 'Z')})
g5 = {'Sham': ('B', 'F'), 'PSLN-212': ('G', 'K'), 'PSLN-344': ('L', 'P'), 'PSLN-212(Y)': ('Q', 'U'),
      'PSLN-344(Y)': ('V', 'Z')}
row_block('S01', 'S01-F', 'lung cDC1 XCR1+ (%) 72h', 36, g5)
row_block('S01', 'S01-G', 'lung cDC2 CD172a+ (%) 72h', 38, g5)

# ------------------------------------------------------------------ S02
g4 = {'Sham': 'A', 'PSLN-212': 'B', 'PSLN-344': 'C', 'PSLN-212(Y)': 'D'}
g4F = {'Sham': 'F', 'PSLN-212': 'G', 'PSLN-344': 'H', 'PSLN-212(Y)': 'I'}
g5K = {'PSLN-212': 'K', 'PSLN-344': 'L', 'PSLN-212(Y)': 'M', 'PTX': 'N', 'PSLN-344(Y)': 'O'}
col_block('S02', 'S02-A', 'lung CCR7+ migratory CD11b+ DC (%) 72h', 3, 7, g4)
col_block('S02', 'S02-B', 'MLN CD11b+CD103- DC (%) 72h', 3, 7, g4F)
col_block('S02', 'S02-C', 'MLN OVA-AF647+ DC (%) 36h', 3, 7, g5K)
col_block('S02', 'S02-D CD40', 'CD40+ of MLN CD11b+ DC (%) d3', 10, 14, g4)
col_block('S02', 'S02-D CD86', 'CD86+ of MLN CD11b+ DC (%) d3', 10, 14, g4F)
col_block('S02', 'S02-E', 'OT-I proliferation with MLN CD11b+ DC (%)', 10, 14, g5K)
series_block('S02', 'S02-F', 'Gm-csf lung (fold vs untreated)', 17, 19, 'A',
             {'PSLN-344': ('B', 'F'), 'PSLN-212': ('G', 'K'), 'Sham': ('L', 'P')})
col_block('S02', 'S02-G', 'lung Ly6C+CD11c+MHC-II+ (moDC-like) (%) d5', 22, 26,
          {'GM-CSF': 'B', 'PSLN-212': 'C', 'PSLN-212+GM-CSF': 'D'})
col_block('S02', 'S02-H', 'CD45.2+ moDC (%) d3', 30, 34,
          {'WT w/o cDC': 'B', 'WT w/ cDC': 'C', 'IFN w/o cDC': 'D', 'IFN w/ cDC': 'E', 'GMCSF': 'F'})
col_block('S02', 'S02-I', 'lung GZMB+ CD8 T (%) d5', 30, 34, {'PSLN-344(Y)': 'H', 'PSLN-344(Y)+INCB3344': 'I'})

# ------------------------------------------------------------------ S03
g5A = {'Sham': 'A', 'CMP-204': 'B', 'PSLN-212': 'C', 'PSLN-344': 'D', 'PSLN-212(Y)': 'E'}
g3G = {'PSLN-212': 'G', 'PSLN-344': 'H', 'PSLN-212(Y)': 'I'}
g5K_ = {'Sham': 'K', 'CMP-204': 'L', 'PSLN-212': 'M', 'PSLN-344': 'N', 'PSLN-212(Y)': 'O'}
g5Q = {'Sham': 'Q', 'CMP-204': 'R', 'PSLN-212': 'S', 'PSLN-344': 'T', 'PSLN-212(Y)': 'U'}
col_block('S03', 'S03-A', 'serum IgG anti-CA09 H1N1 d14 (titre)', 3, 7, g5A)
col_block('S03', 'S03-B', 'IgG2a/IgG1 anti-CA09 H1N1 d14 (ratio)', 3, 7, g3G)
col_block('S03', 'S03-C', 'HAI anti-CA09 H1N1 d14 (titre)', 3, 7, g5K_)
col_block('S03', 'S03-D', 'neutralising anti-CA09 H1N1 d14 (titre)', 3, 7, g5Q)
col_block('S03', 'S03-E', 'serum IgG anti-Aichi H3N2 d14 (titre)', 10, 14, g5A)
col_block('S03', 'S03-F', 'IgG2a/IgG1 anti-Aichi H3N2 d14 (ratio)', 10, 14, g3G)
col_block('S03', 'S03-G', 'HAI anti-Aichi H3N2 d14 (titre)', 10, 14, g5K_)
col_block('S03', 'S03-H', 'neutralising anti-Aichi H3N2 d14 (titre)', 10, 14, g5Q)
surv_block('S03', 'S03-I', 17, 51, 'A', {'Sham': 'B', 'CMP-204': 'C', 'PSLN-212': 'D', 'PSLN-344': 'E', 'PSLN-212(Y)': 'F'})
surv_block('S03', 'S03-J', 17, 46, 'G', {'Sham': 'H', 'PSLN-212': 'I', 'PSLN-344': 'J'})
col_block('S03', 'S03-K', 'MLN GC B cells CXCR5+GL7+ (%) d7', 17, 21,
          {'Sham': 'L', 'PSLN-212': 'M', 'PSLN-344': 'N', 'PSLN-212(Y)': 'O'})
for r in (26, 27, 28):
    g = cell('S03', f'K{r}')
    row_block('S03', 'S03-L', 'Aicda MLN B cells d5 (fold)', r, {g: ('L', 'N')})
    row_block('S03', 'S03-L', 'E47 MLN B cells d5 (fold)', r, {g: ('O', 'Q')})

# ------------------------------------------------------------------ S04
for r in range(2, 6):
    g = cell('S04', f'A{r}')
    row_block('S04', 'S04-A', 'Tfh ICOS-low CXCR5+PD1+ (%) d7', r, {g: ('B', 'F')})
    row_block('S04', 'S04-A', 'Tfh ICOS-high CXCR5+PD1+ (%) d7', r, {g: ('G', 'K')})
col_block('S04', 'S04-B Foxp3+', 'Tfr Foxp3+ in CXCR5+ (%) d7', 8, 12, g4)
col_block('S04', 'S04-B Tfh:Tfr', 'Tfh:Tfr ratio d7', 15, 19, g4)
col_block('S04', 'S04-C', 'Tfr (%) d30', 22, 26, g4)
col_block('S04', 'S04-D', 'lung Treg CD4+Foxp3+ (%) d7', 29, 31, g4)

# ------------------------------------------------------------------ S05
g3T = {'PSLN-212': ('B', 'C'), 'PSLN-344': ('E', 'F'), 'PSLN-212Y': ('H', 'I')}
series_block('S05', 'S05-A', 'NP366-374 tetramer+ of CD8 T, lung (%)', 3, 5, 'A', g3T)
series_block('S05', 'S05-B', 'NP366-374 tetramer+ of CD8 T, MLN (%)', 8, 10, 'A', g3T)
col_block('S05', 'S05-C', 'proliferating OT-I (%) d4', 13, 15, {'Lung': 'A', 'Lung+PTX': 'B', 'MLN': 'C', 'MLN+PTX': 'D'})
col_block('S05', 'S05-D', 'lung Ki-67+ CD8 T (%) d3', 19, 23, g4)
col_block('S05', 'S05-E', 'lung GZMB+ CD8 T (%) d3', 26, 30, g4)
col_block('S05', 'S05-F', 'MLN IFNg+ CD8 T, rgH5N1 restim (%) d14', 33, 37, g4)
col_block('S05', 'S05-G', 'MLN IFNg+ CD8 T, rgH5N1 restim (%) d60', 40, 44, g4)
col_block('S05', 'S05-H', 'MLN GZMB+ CD8 T (%) d60', 47, 51, g4)
col_block('S05', 'S05-I', 'lung TRM CD69+CD103+ CD8 (%) d25', 54, 58, g4)

# ------------------------------------------------------------------ S06  (all time-to-event)
s4 = lambda a: dict(zip(['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)'], a))
s5 = lambda a: dict(zip(['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)', 'Untreated'], a))
imp = lambda a: dict(zip(['Naive+PSLN-212', 'Imprinting+PSLN-212', 'Naive+PSLN-344', 'Imprinting+PSLN-344'], a))
surv_block('S06', 'S06-A', 3, 30, 'A', s4('BCDE'))
surv_block('S06', 'S06-B', 3, 30, 'G', s4('HIJK'))
surv_block('S06', 'S06-C', 3, 30, 'M', s4('NOPQ'))
surv_block('S06', 'S06-D', 34, 61, 'A', s4('BCDE'))
surv_block('S06', 'S06-E (rows 34-68)', 34, 68, 'G', s5('HIJKL'))
surv_block('S06', 'S06-F (rows 34-68)', 34, 68, 'M', s5('NOPQR'))
surv_block('S06', 'S06-G', 71, 105, 'A', s5('BCDEF'))
surv_block('S06', 'S06-E (rows 71-105)', 71, 98, 'G', imp('HIJK'))
surv_block('S06', 'S06-F (rows 71-105)', 71, 98, 'M', imp('NOPQ'))

# ------------------------------------------------------------------ S07
series_block('S07', 'S07-A', 'lung Ly6C+CCR2+ macrophages (x1e5 cells)', 3, 7, 'A',
             {'PSLN-212': ('B', 'D'), 'PSLN-344': ('E', 'G')})
col_block('S07', 'S07-B', 'lung CD11b+Ly6C+ monocytes (%)', 10, 14, {'PSLN-344': 'B', 'PSLN-344+INCB3344': 'C'})
col_block('S07', 'S07-B', 'lung Ly6C+ macrophages (%)', 10, 14, {'PSLN-344': 'E', 'PSLN-344+INCB3344': 'F'})
col_block('S07', 'S07-C', 'lung Treg (%) d4 after MPhi transfer', 16, 20,
          {'col B (printed "Ly6C-CD206+ MPhi")': 'B', 'col C (printed "Ly6C-CD206+ MPhi")': 'C'})

# ------------------------------------------------------------------ S08
series_block('S08', 'S08-A', 'Ifnb1 lung 16h (fold) dose-response', 3, 7, 'A',
             {'CMP-204': ('B', 'D'), 'PSLN-212': ('E', 'G'), 'PSLN-344': ('H', 'J'), 'PSLN-344/R848': ('K', 'M')})
row_block('S08', 'S08-B', 'encapsulation efficiency (%)', 11,
          {'CMP-204': ('A', 'C'), 'PSLN-212': ('D', 'F'), 'PSLN-R848': ('G', 'I'), 'PSLN-212/R848': ('J', 'L'),
           'PSLN-344': ('M', 'O')})
col_block('S08', 'S08-C', 'SRB+ alveolar epithelial cells (%) 16h', 14, 18,
          {'AECII-PSLN-SRB': 'A', 'AECII-PSLN-344-SRB': 'B', 'AECI-PSLN-SRB': 'C', 'AECI-PSLN-344-SRB': 'D'})
series_block('S08', 'S08-D', 'body weight after immunisation (% d0)', 21, 26, 'A',
             {'PSLN-212(Y)': ('B', 'F'), 'CMP-204': ('G', 'K'), 'PSLN-212': ('L', 'P'), 'PSLN-344': ('Q', 'U'),
              'PSLN-212/R848': ('V', 'Z'), 'Vaccine': ('AA', 'AE')}, kind='weight')
surv_block('S08', 'S08 rows 89-101 (UNLABELLED)', 89, 101, 'A', {'col C (no label)': 'C', 'col D (no label)': 'D'},
           analyte='unlabelled region')

# ------------------------------------------------------------------ S09
analytes = {3: 'Ifnb1', 4: 'Il6', 5: 'Ccl2', 6: 'Ccl3', 7: 'Ccl5', 8: 'Tnf', 9: 'Il10'}
p1 = {'PBS': ('B', 'D'), 'CMP-204': ('E', 'G'), 'PSLN-212': ('H', 'J'), 'PSLN-R848': ('K', 'M'),
      'PSLN-212/R848': ('N', 'P'), 'PSLN-344': ('Q', 'S'), 'PSLN-212(y)': ('T', 'V')}
p2 = {'PBS': ('Y', 'AA'), 'CMP-204': ('AB', 'AD'), 'PSLN-212': ('AE', 'AG'), 'PSLN-R848': ('AH', 'AJ'),
      'PSLN-212/R848': ('AK', 'AM'), 'PSLN-344': ('AN', 'AP'), 'PSLN-212(y)': ('AQ', 'AS')}
for r, a in analytes.items():
    row_block('S09', 'S09-A (cols A-U)', f'{a} lung log10 fold', r, p1, x='panel1 (printed 16h)')
    row_block('S09', 'S09-A (cols X-AS)', f'{a} lung log10 fold', r, p2, x='panel2 (printed 16h)')
y3 = {'Sham': 'B', 'PSLN-344Y': 'C', 'PSLN-212Y': 'D'}
w3 = {'PSLN-212Y': ('G', 'N'), 'Sham': ('O', 'V'), 'PSLN-344Y': ('W', 'AD')}
surv_block('S09', 'S09-B', 12, 35, 'A', y3)
series_block('S09', 'S09-C', 'body weight (% d0)', 12, 19, 'F', w3, kind='weight')
surv_block('S09', 'S09-D', 39, 62, 'A', y3)
series_block('S09', 'S09-E', 'body weight (% d0)', 39, 46, 'F', w3, kind='weight')
surv_block('S09', 'S09-F', 66, 88, 'A', y3)
series_block('S09', 'S09-G', 'body weight (% d0)', 66, 73, 'F', w3, kind='weight')

# ------------------------------------------------------------------ S10
col_block('S10', 'S10-A', 'CNS Ifnb1 36h (fold)', 3, 7, {'PBS': 'A', 'Sham': 'B', 'PSLN-344': 'C', 'CT': 'D'})
col_block('S10', 'S10-A', 'CNS Tnf 36h (fold)', 3, 7, {'PBS': 'F', 'Sham': 'G', 'PSLN-344': 'H', 'CT': 'I'})
col_block('S10', 'S10-A', 'CNS Isg15 36h (fold)', 3, 7, {'PBS': 'K', 'Sham': 'L', 'PSLN-344': 'M', 'CT': 'N'})

# ------------------------------------------------------------------ S11
v4 = {'Vaccine': ('B', 'F'), 'PSLN-212': ('G', 'K'), 'PSLN-344': ('L', 'P'), 'PSLN-212(Y)': ('Q', 'U')}
series_block('S11', 'S11-A', 'lung alveolar macrophages (%)', 3, 7, 'A', v4)
series_block('S11', 'S11-B', 'lung neutrophils (%)', 10, 14, 'A', v4)
col_block('S11', 'S11-C', 'recruited lung monocytes (%) d3', 17, 21, {'CBX+': 'A', 'CBX-': 'B'})
series_block('S11', 'S11-D', 'lung NK cells (%)', 24, 28, 'A', v4)
col_block('S11', 'S11-E', 'lung CD206+ macrophages (%)', 31, 35, g4)

# ------------------------------------------------------------------ S12
col_block('S12', 'S12-A', 'infiltrating CD45.2+ monocytes (%) d3', 3, 5, {'WT to WT': 'A', 'IFNAR-/- to WT': 'B'})

# ------------------------------------------------------------------ S13
col_block('S13', 'S13-A', 'serum IgG2a anti-CA09 d14 (titre)', 3, 7, {'PSLN-212': 'A', 'PSLN-344': 'B', 'PSLN-212(Y)': 'C'})
col_block('S13', 'S13-B', 'serum IgG1 anti-CA09 d14 (titre)', 3, 7, {'PSLN-212': 'E', 'PSLN-344': 'F', 'PSLN-212(Y)': 'G'})
col_block('S13', 'S13-C', 'serum IgG2a anti-Aichi d14 (titre)', 3, 7, {'PSLN-212': 'I', 'PSLN-344': 'J', 'PSLN-212(Y)': 'K'})
col_block('S13', 'S13-D', 'serum IgG1 anti-Aichi d14 (titre)', 3, 7, {'PSLN-212': 'M', 'PSLN-344': 'N', 'PSLN-212(Y)': 'O'})
surv_block('S13', 'S13-E', 3, 30, 'R', {'Naive': 'S', 'Sham': 'T', 'CMP-204(Y)': 'U', 'PSLN-344(Y)': 'V'})
series_block('S13', 'S13-F', 'body weight (% d0)', 33, 40, 'A',
             {'PSLN-212(Y)': ('B', 'H'), 'Sham': ('I', 'O'), 'PSLN-212': ('P', 'V'), 'PSLN-344': ('W', 'AC'),
              'Naive': ('AD', 'AJ')}, kind='weight')
series_block('S13', 'S13-G', 'body weight (% d0)', 43, 50, 'A',
             {'PSLN-344': ('B', 'K'), 'Sham': ('L', 'U'), 'Naive': ('V', 'AE')}, kind='weight')
col_block('S13', 'S13-H', 'IgG+ of MLN B220+ cells (%)', 53, 57, g4)
col_block('S13', 'S13-I', 'serum IgG anti-CA09 d28 post-boost (titre)', 53, 57,
          {'Sham': 'F', 'CMP-204': 'G', 'PSLN-212': 'H', 'PSLN-344': 'I', 'PSLN-212(Y)': 'J'})
col_block('S13', 'S13-J', 'serum IgG anti-Aichi d28 post-boost (titre)', 53, 57,
          {'Sham': 'L', 'CMP-204': 'M', 'PSLN-212': 'N', 'PSLN-344': 'O', 'PSLN-212(Y)': 'P'})

# ------------------------------------------------------------------ S14
col_block('S14', 'S14-A H1N1', 'MLN IFNg+ CD8 T, CA09 H1N1 restim (%)', 3, 7, g4)
col_block('S14', 'S14-A H3N2', 'MLN IFNg+ CD8 T, Aichi H3N2 restim (%)', 3, 7, g4F)

# ------------------------------------------------------------------ S15
w4 = {'PSLN-212(Y)': ('B', 'H'), 'Sham': ('I', 'O'), 'PSLN-212': ('P', 'V'), 'PSLN-344': ('W', 'AC')}
w5 = dict(w4); w5['Untreated'] = ('AD', 'AJ')
for blk, r0 in [('S15-A', 3), ('S15-B', 13), ('S15-C', 23), ('S15-D', 33)]:
    series_block('S15', blk, 'body weight (% d0)', r0, r0 + 7, 'A', w4, kind='weight')
for blk, r0 in [('S15-E', 43), ('S15-F', 53), ('S15-G', 63)]:
    series_block('S15', blk, 'body weight (% d0)', r0, r0 + 7, 'A', w5, kind='weight')
surv_block('S15', 'S15-H', 73, 93, 'A', {'3d Vaccine': 'B', '3d PSLN-344': 'C', '3d Vaccine+PSLN-344': 'D'})
series_block('S15', 'S15-I', 'body weight (% d0)', 72, 79, 'H',
             {'3d Vaccine': ('I', 'O'), '3d PSLN-344': ('P', 'V'), '3d Vaccine+PSLN-344': ('W', 'AC')}, kind='weight')
wi = {'Naive+PSLN-212': ('I', 'O'), 'Imprinting+PSLN-212': ('P', 'V'), 'Naive+PSLN-344': ('W', 'AC'),
      'Imprinting+PSLN-344': ('AD', 'AJ')}
series_block('S15', 'S15-J', 'body weight (% d0)', 83, 90, 'H', wi, kind='weight')
series_block('S15', 'S15-K', 'body weight (% d0)', 93, 100, 'H', wi, kind='weight')
surv_block('S15', 'S15-L', 103, 130, 'A', s4('BCDE'))
wm = {'PSLN-212(Y)': ('I', 'O'), 'Sham': ('P', 'V'), 'PSLN-212': ('W', 'AC'), 'PSLN-344': ('AD', 'AJ')}
series_block('S15', 'S15-M', 'body weight (% d0)', 103, 110, 'H', wm, kind='weight')
surv_block('S15', 'S15-N', 134, 161, 'A', s4('BCDE'))
series_block('S15', 'S15-O', 'body weight (% d0)', 134, 141, 'H', wm, kind='weight')

def tidy():
    import pandas as pd
    return pd.DataFrame(ROWS)

def all_numeric_cells():
    """every numeric cell in the workbook: {(sheet, ref): value}"""
    out = {}
    for ws in _wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, (int, float)) and not isinstance(c.value, bool):
                    out[(ws.title, c.coordinate)] = c.value
    return out

if __name__ == '__main__':
    import pandas as pd
    df = tidy()
    df.to_csv(TABLES + 'T0_tidy_all_observations.csv', index=False)
    print(len(df), 'observations in', df.block.nunique(), 'blocks')
    # coverage check: every numeric cell must be either a mapped value, a mapped day/x, or explained
    used = set()
    for r in ROWS:
        sh, ref = r['cell'].split('!')
        for p in ref.split('/'):
            used.add((sh, p))
    allc = all_numeric_cells()
    unused = sorted(k for k in allc if k not in used)
    print('numeric cells total', len(allc), 'mapped as values', len(used & set(allc)), 'not mapped', len(unused))
    import collections
    by = collections.defaultdict(list)
    for sh, ref in unused:
        by[sh].append(ref)
    for sh, refs in by.items():
        print(sh, len(refs), refs[:60])
