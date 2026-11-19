"""
Structured parser for psln_program_dataset.xlsx.

Every block is declared with explicit cell ranges so that each number used downstream
can be traced to (sheet, block, cell).  A coverage check at the bottom proves that every
numeric cell in the workbook is assigned to exactly one declared block (or to the one
declared orphan region in S08).
"""
import openpyxl
from openpyxl.utils import column_index_from_string as c2i, get_column_letter as i2c
import pandas as pd

XLSX = '/tmp/world/filesystem/psln_program_dataset.xlsx'
wb = openpyxl.load_workbook(XLSX)

def colrange(a, b):
    return [i2c(i) for i in range(c2i(a), c2i(b) + 1)]

records = []      # tidy: one row per numeric observation
used = set()      # (sheet, coordinate) consumed

def add(sheet, block, kind, group, cell, value, **kw):
    rec = dict(sheet=sheet, block=block, kind=kind, group=group, cell=cell, value=value)
    rec.update(kw)
    records.append(rec)
    used.add((sheet, cell))

def mark(sheet, cell):
    used.add((sheet, cell))

# ---------- generic readers -------------------------------------------------------------
def read_cols(sheet, block, header_row, cols, rows, kind='scalar', label_override=None, **kw):
    """Groups are columns (header in header_row); replicates run down rows."""
    ws = wb[sheet]
    for j, col in enumerate(cols):
        g = ws[f'{col}{header_row}'].value if label_override is None else label_override[j]
        mark(sheet, f'{col}{header_row}')
        for rep, r in enumerate(rows, 1):
            v = ws[f'{col}{r}'].value
            if v is not None:
                add(sheet, block, kind, str(g).strip(), f'{col}{r}', v, rep=rep, col_order=j, **kw)

def read_rows(sheet, block, label_col, rows, cols, kind='scalar', **kw):
    """Groups are rows (label in label_col); replicates run across cols."""
    ws = wb[sheet]
    for j, r in enumerate(rows):
        g = ws[f'{label_col}{r}'].value
        mark(sheet, f'{label_col}{r}')
        for rep, col in enumerate(cols, 1):
            v = ws[f'{col}{r}'].value
            if v is not None:
                add(sheet, block, kind, str(g).strip(), f'{col}{r}', v, rep=rep, col_order=j, **kw)

def read_wide(sheet, block, header_row, group_spans, time_col, rows, kind='timecourse', time_name='day', **kw):
    """Wide time-course: each group spans several columns (one per animal); rows are timepoints."""
    ws = wb[sheet]
    for j, (hdr_col, a, b) in enumerate(group_spans):
        g = ws[f'{hdr_col}{header_row}'].value
        mark(sheet, f'{hdr_col}{header_row}')
        for r in rows:
            t = ws[f'{time_col}{r}'].value
            mark(sheet, f'{time_col}{r}')
            for rep, col in enumerate(colrange(a, b), 1):
                v = ws[f'{col}{r}'].value
                if v is not None:
                    add(sheet, block, kind, str(g).strip(), f'{col}{r}', v, rep=rep, col_order=j, time=t, **kw)

def read_surv(sheet, block, header_row, day_col, group_cols, rows, **kw):
    """Survival: one row per animal; day in day_col; 1/0 flag sits in the animal's group column."""
    ws = wb[sheet]
    mark(sheet, f'{day_col}{header_row}')
    groups = {}
    for j, col in enumerate(group_cols):
        groups[col] = (str(ws[f'{col}{header_row}'].value).strip(), j)
        mark(sheet, f'{col}{header_row}')
    for r in rows:
        d = ws[f'{day_col}{r}'].value
        flags = [(col, ws[f'{col}{r}'].value) for col in group_cols if ws[f'{col}{r}'].value is not None]
        if d is None and not flags:
            continue
        if d is not None:
            mark(sheet, f'{day_col}{r}')
        if len(flags) != 1:
            # malformed row: keep it, flagged
            add(sheet, block, 'survival', 'MALFORMED', f'{day_col}{r}', d, event=None, time=d, malformed=True, **kw)
            for col, _ in flags: mark(sheet, f'{col}{r}')
            continue
        col, ev = flags[0]
        add(sheet, block, 'survival', groups[col][0], f'{col}{r}', ev, event=ev, time=d,
            day_cell=f'{day_col}{r}', col_order=groups[col][1], malformed=(d is None), **kw)

# ======================================== S01 ==========================================
S='S01'; mark(S,'A1'); mark(S,'A2'); mark(S,'G2')
read_rows(S,'S01-A/16h','A',range(3,11),colrange('B','F'), analyte='Ifnb1', time='16h')
read_rows(S,'S01-A/72h','G',range(3,11),colrange('H','L'), analyte='Ifnb1', time='72h')
mark(S,'A13'); read_rows(S,'S01-B','A',range(14,18),colrange('B','F'))
mark(S,'A19'); read_rows(S,'S01-C','A',range(20,22),colrange('B','E'))
mark(S,'A23'); read_wide(S,'S01-D',23,[('B','B','F'),('G','G','K'),('L','L','P'),('Q','Q','U')],'A',range(24,29))
mark(S,'A29'); read_wide(S,'S01-E',29,[('B','B','F'),('G','G','K'),('L','L','P'),('Q','Q','U'),('V','V','Z')],'A',range(30,35))
mark(S,'A35')
for blk,hr,r in [('S01-F',35,36),('S01-G',37,38)]:
    mark(S,f'A{hr}')
    ws=wb[S]
    for j,(h,a,b) in enumerate([('B','B','F'),('G','G','K'),('L','L','P'),('Q','Q','U'),('V','V','Z')]):
        g=ws[f'{h}{hr}'].value; mark(S,f'{h}{hr}')
        for rep,col in enumerate(colrange(a,b),1):
            v=ws[f'{col}{r}'].value
            if v is not None: add(S,blk,'scalar',str(g).strip(),f'{col}{r}',v,rep=rep,col_order=j)

# ======================================== S02 ==========================================
S='S02'
for c in ['A1','F1','K1','A8','F8','K8','A15','A20','A28','G28']: mark(S,c)
read_cols(S,'S02-A',2,colrange('A','D'),range(3,8))
read_cols(S,'S02-B',2,colrange('F','I'),range(3,8))
read_cols(S,'S02-C',2,colrange('K','O'),range(3,8))
read_cols(S,'S02-D CD40',9,colrange('A','D'),range(10,15))
read_cols(S,'S02-D CD86',9,colrange('F','I'),range(10,15))
read_cols(S,'S02-E',9,colrange('K','O'),range(10,15))
read_wide(S,'S02-F',16,[('B','B','F'),('G','G','K'),('L','L','P')],'A',range(17,20),time_name='hours')
read_cols(S,'S02-G',21,colrange('B','D'),range(22,27))
read_cols(S,'S02-H',29,colrange('B','F'),range(30,35))
read_cols(S,'S02-I',29,colrange('H','I'),range(30,35))

# ======================================== S03 ==========================================
S='S03'
for c in ['A1','G1','K1','Q1','A8','G8','K8','Q8','A15','G15','K15','K25','L25','O25']: mark(S,c)
read_cols(S,'S03-A',2,colrange('A','E'),range(3,8))
read_cols(S,'S03-B',2,colrange('G','I'),range(3,8))
read_cols(S,'S03-C',2,colrange('K','O'),range(3,8))
read_cols(S,'S03-D',2,colrange('Q','U'),range(3,8))
read_cols(S,'S03-E',9,colrange('A','E'),range(10,15))
read_cols(S,'S03-F',9,colrange('G','I'),range(10,15))
read_cols(S,'S03-G',9,colrange('K','O'),range(10,15))
read_cols(S,'S03-H',9,colrange('Q','U'),range(10,15))
read_surv(S,'S03-I',16,'A',colrange('B','F'),range(17,52))
read_surv(S,'S03-J',16,'G',colrange('H','J'),range(17,47))
read_cols(S,'S03-K',16,colrange('L','O'),range(17,22))
read_rows(S,'S03-L/Aicda','K',range(26,29),colrange('L','N'),analyte='Aicda')
read_rows(S,'S03-L/E47','K',range(26,29),colrange('O','Q'),analyte='E47')

# ======================================== S04 ==========================================
S='S04'
for c in ['A1','B1','G1','A6','A13','A20','A27']: mark(S,c)
read_rows(S,'S04-A/ICOSlo','A',range(2,6),colrange('B','F'),analyte='ICOS-low Tfh')
read_rows(S,'S04-A/ICOShi','A',range(2,6),colrange('G','K'),analyte='ICOS-high Tfh')
read_cols(S,'S04-B Foxp3',7,colrange('A','D'),range(8,13))
read_cols(S,'S04-B Tfh:Tfr',14,colrange('A','D'),range(15,20))
read_cols(S,'S04-C',21,colrange('A','D'),range(22,27))
read_cols(S,'S04-D',28,colrange('A','D'),range(29,32))

# ======================================== S05 ==========================================
S='S05'
for c in ['A1','A2','A6','A7','A11','A17','A24','A31','A38','A45','A52']: mark(S,c)
read_wide(S,'S05-A',2,[('B','B','C'),('E','E','F'),('H','H','I')],'A',range(3,6))
read_wide(S,'S05-B',7,[('B','B','C'),('E','E','F'),('H','H','I')],'A',range(8,11))
read_cols(S,'S05-C',12,colrange('A','D'),range(13,16))
read_cols(S,'S05-D',18,colrange('A','D'),range(19,24))
read_cols(S,'S05-E',25,colrange('A','D'),range(26,31))
read_cols(S,'S05-F',32,colrange('A','D'),range(33,38))
read_cols(S,'S05-G',39,colrange('A','D'),range(40,45))
read_cols(S,'S05-H',46,colrange('A','D'),range(47,52))
read_cols(S,'S05-I',53,colrange('A','D'),range(54,59))

# ======================================== S06 ==========================================
S='S06'
for c in ['A1','G1','M1','A32','G32','M32','A69','G69','M69']: mark(S,c)
read_surv(S,'S06-A',2,'A',colrange('B','E'),range(3,31))
read_surv(S,'S06-B',2,'G',colrange('H','K'),range(3,31))
read_surv(S,'S06-C',2,'M',colrange('N','Q'),range(3,31))
read_surv(S,'S06-D',33,'A',colrange('B','E'),range(34,62))
read_surv(S,'S06-E(r34)',33,'G',colrange('H','L'),range(34,69))
read_surv(S,'S06-F(r34)',33,'M',colrange('N','R'),range(34,69))
read_surv(S,'S06-G',70,'A',colrange('B','F'),range(71,106))
read_surv(S,'S06-E(r71)',70,'G',colrange('H','K'),range(71,99))
read_surv(S,'S06-F(r71)',70,'M',colrange('N','Q'),range(71,99))

# ======================================== S07 ==========================================
S='S07'
for c in ['A1','A2','A8','B8','E8','A15']+[f'H{r}' for r in range(3,8)]: mark(S,c)
read_wide(S,'S07-A',2,[('B','B','D'),('E','E','G')],'A',range(3,8))
read_cols(S,'S07-B/Mono',9,colrange('B','C'),range(10,15),analyte='CD11b+Ly6C+ monocytes')
read_cols(S,'S07-B/Ly6C+Mac',9,colrange('E','F'),range(10,15),analyte='Ly6C+ macrophages')
read_cols(S,'S07-C',15,colrange('B','C'),range(16,21),label_override=['Ly6C-CD206+ MΦ [col B]','Ly6C-CD206+ MΦ [col C]'])

# ======================================== S08 ==========================================
S='S08'
for c in ['A1','A2','A9','A12','A19']: mark(S,c)
read_wide(S,'S08-A',2,[('B','B','D'),('E','E','G'),('H','H','J'),('K','K','M')],'A',range(3,8),time_name='dose_ug')
ws=wb[S]
for j,(h,a,b) in enumerate([('A','A','C'),('D','D','F'),('G','G','I'),('J','J','L'),('M','M','O')]):
    g=ws[f'{h}10'].value; mark(S,f'{h}10')
    for rep,col in enumerate(colrange(a,b),1):
        add(S,'S08-B','scalar',str(g).strip(),f'{col}11',ws[f'{col}11'].value,rep=rep,col_order=j)
read_cols(S,'S08-C',13,colrange('A','D'),range(14,19))
read_wide(S,'S08-D',20,[('B','B','F'),('G','G','K'),('L','L','P'),('Q','Q','U'),('V','V','Z'),('AA','AA','AE')],'A',range(21,27),kind='weight')
# orphan region rows 89-101 (no label, no header)
for r in range(89,102):
    mark(S,f'A{r}')
    for col in ['C','D']:
        v=ws[f'{col}{r}'].value
        if v is not None:
            add(S,'S08-ORPHAN(r89-101)','orphan',f'unlabelled col {col}',f'{col}{r}',v,time=ws[f'A{r}'].value)

# ======================================== S09 ==========================================
S='S09'
for c in ['A1','X1','A10','E10','A37','F37','A64','F64']: mark(S,c)
ws=wb[S]
p1=[('B','B','D'),('E','E','G'),('H','H','J'),('K','K','M'),('N','N','P'),('Q','Q','S'),('T','T','V')]
p2=[('Y','Y','AA'),('AB','AB','AD'),('AE','AE','AG'),('AH','AH','AJ'),('AK','AK','AM'),('AN','AN','AP'),('AQ','AQ','AS')]
for blk,spans,lab in [('S09-A/panel1(A-V)',p1,'A'),('S09-A/panel2(X-AS)',p2,'X')]:
    for j,(h,a,b) in enumerate(spans):
        g=ws[f'{h}2'].value; mark(S,f'{h}2')
        for r in range(3,10):
            an=ws[f'{lab}{r}'].value; mark(S,f'{lab}{r}')
            for rep,col in enumerate(colrange(a,b),1):
                add(S,blk,'scalar_log10',str(g).strip(),f'{col}{r}',ws[f'{col}{r}'].value,rep=rep,col_order=j,analyte=an)
read_surv(S,'S09-B',11,'A',colrange('B','D'),range(12,36))
read_wide(S,'S09-C',11,[('G','G','N'),('O','O','V'),('W','W','AD')],'F',range(12,20),kind='weight'); mark(S,'F11')
read_surv(S,'S09-D',38,'A',colrange('B','D'),range(39,63))
read_wide(S,'S09-E',38,[('G','G','N'),('O','O','V'),('W','W','AD')],'F',range(39,47),kind='weight'); mark(S,'F38')
read_surv(S,'S09-F',65,'A',colrange('B','D'),range(66,89))
read_wide(S,'S09-G',65,[('G','G','N'),('O','O','V'),('W','W','AD')],'F',range(66,74),kind='weight'); mark(S,'F65')

# ======================================== S10 ==========================================
S='S10'
for c in ['A1','E1','J1']: mark(S,c)
read_cols(S,'S10-A/Ifnb1',2,colrange('A','D'),range(3,8),analyte='Ifnb1')
read_cols(S,'S10-A/Tnf',2,colrange('F','I'),range(3,8),analyte='Tnf')
read_cols(S,'S10-A/Isg15',2,colrange('K','N'),range(3,8),analyte='Isg15')

# ======================================== S11 ==========================================
S='S11'
for c in ['A1','A2','A8','A9','A15','A22','A23','A29']: mark(S,c)
sp=[('B','B','F'),('G','G','K'),('L','L','P'),('Q','Q','U')]
read_wide(S,'S11-A',2,sp,'A',range(3,8))
read_wide(S,'S11-B',9,sp,'A',range(10,15))
read_cols(S,'S11-C',16,colrange('A','B'),range(17,22))
read_wide(S,'S11-D',23,sp,'A',range(24,29))
read_cols(S,'S11-E',30,colrange('A','D'),range(31,36))

# ======================================== S12 ==========================================
S='S12'; mark(S,'A1')
read_cols(S,'S12-A',2,colrange('A','B'),range(3,6))

# ======================================== S13 ==========================================
S='S13'
for c in ['A1','E1','I1','M1','R1','A31','A32','A42','A51','E51','K51']: mark(S,c)
read_cols(S,'S13-A',2,colrange('A','C'),range(3,8))
read_cols(S,'S13-B',2,colrange('E','G'),range(3,8))
read_cols(S,'S13-C',2,colrange('I','K'),range(3,8))
read_cols(S,'S13-D',2,colrange('M','O'),range(3,8))
read_surv(S,'S13-E',2,'R',colrange('S','V'),range(3,31))
read_wide(S,'S13-F',32,[('B','B','H'),('I','I','O'),('P','P','V'),('W','W','AC'),('AD','AD','AJ')],'A',range(33,41),kind='weight')
read_wide(S,'S13-G',42,[('B','B','K'),('L','L','U'),('V','V','AE')],'A',range(43,51),kind='weight')
read_cols(S,'S13-H',52,colrange('A','D'),range(53,58))
read_cols(S,'S13-I',52,colrange('F','J'),range(53,58))
read_cols(S,'S13-J',52,colrange('L','P'),range(53,58))

# ======================================== S14 ==========================================
S='S14'
for c in ['A1','E1']: mark(S,c)
read_cols(S,'S14-A H1N1',2,colrange('A','D'),range(3,8))
read_cols(S,'S14-A H3N2',2,colrange('F','I'),range(3,8))

# ======================================== S15 ==========================================
S='S15'
for c in ['A1','A2','A11','A12','A21','A22','A31','A32','A41','A42','A51','A52','A61','A62','A71','G71','H71',
          'G81','H82','G91','H92','A101','G101','H102','A132','G132','H133']: mark(S,c)
sp4=[('B','B','H'),('I','I','O'),('P','P','V'),('W','W','AC')]
sp5=sp4+[('AD','AD','AJ')]
read_wide(S,'S15-A',2,sp4,'A',range(3,11),kind='weight')
read_wide(S,'S15-B',12,sp4,'A',range(13,21),kind='weight')
read_wide(S,'S15-C',22,sp4,'A',range(23,31),kind='weight')
read_wide(S,'S15-D',32,sp4,'A',range(33,41),kind='weight')
read_wide(S,'S15-E',42,sp5,'A',range(43,51),kind='weight')
read_wide(S,'S15-F',52,sp5,'A',range(53,61),kind='weight')
read_wide(S,'S15-G',62,sp5,'A',range(63,71),kind='weight')
read_surv(S,'S15-H',72,'A',colrange('B','D'),range(73,94))
read_wide(S,'S15-I',71,[('I','I','O'),('P','P','V'),('W','W','AC')],'H',range(72,80),kind='weight')
spJ=[('I','I','O'),('P','P','V'),('W','W','AC'),('AD','AD','AJ')]
read_wide(S,'S15-J',82,spJ,'H',range(83,91),kind='weight')
read_wide(S,'S15-K',92,spJ,'H',range(93,101),kind='weight')
read_surv(S,'S15-L',102,'A',colrange('B','E'),range(103,131))
read_wide(S,'S15-M',102,spJ,'H',range(103,111),kind='weight')
read_surv(S,'S15-N',133,'A',colrange('B','E'),range(134,162))
read_wide(S,'S15-O',133,spJ,'H',range(134,142),kind='weight')

df = pd.DataFrame(records)

def coverage_report():
    """Every non-empty cell in the workbook must be consumed by a declared block."""
    missing = []
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if c.value is not None and (ws.title, c.coordinate) not in used:
                    missing.append((ws.title, c.coordinate, c.value))
    dup = df[df.duplicated(['sheet', 'cell'], keep=False)]
    return missing, dup

if __name__ == '__main__':
    missing, dup = coverage_report()
    print('observations parsed:', len(df))
    print('unassigned non-empty cells:', len(missing)); print(missing[:60])
    print('cells assigned twice:', len(dup))
    df.to_csv('tidy_all_observations.csv', index=False)
    print(df.groupby(['sheet','block','kind']).size().to_string())
