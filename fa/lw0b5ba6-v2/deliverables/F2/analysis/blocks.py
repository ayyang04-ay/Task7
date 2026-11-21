"""
Structured parser for psln_program_dataset.xlsx.
Every block is addressed by explicit sheet/row/column coordinates so that each number used downstream
can be traced back to a cell range.
"""
import openpyxl, os
from openpyxl.utils import get_column_letter as gcl, column_index_from_string as cidx
import pandas as pd, numpy as np

XLSX = os.environ.get('PSLN_XLSX', '/tmp/world/filesystem/psln_program_dataset.xlsx')   # source workbook
wb = openpyxl.load_workbook(XLSX, data_only=True)

def cell(ws, col, row):
    return wb[ws][f'{col}{row}'].value

def colrange(c1, c2):
    return [gcl(i) for i in range(cidx(c1), cidx(c2)+1)]

# ---------- generic readers ----------
def read_cols(ws, header_row, cols, r1, r2, block, rename=None):
    """one group per column; replicate animals down rows"""
    out = []
    for c in colrange(*cols):
        g = cell(ws, c, header_row)
        if g is None: continue
        g = str(g).strip()
        for r in range(r1, r2+1):
            v = cell(ws, c, r)
            if v is None: continue
            out.append(dict(block=block, sheet=ws, group=g, rep=r-r1+1, value=float(v), cellref=f'{ws}!{c}{r}'))
    return pd.DataFrame(out)

def read_rows(ws, label_col, valcols, r1, r2, block):
    """one group per row; replicate animals across columns"""
    out = []
    for r in range(r1, r2+1):
        g = cell(ws, label_col, r)
        if g is None: continue
        g = str(g).strip()
        for i, c in enumerate(colrange(*valcols)):
            v = cell(ws, c, r)
            if v is None: continue
            out.append(dict(block=block, sheet=ws, group=g, rep=i+1, value=float(v), cellref=f'{ws}!{c}{r}'))
    return pd.DataFrame(out)

def read_wide_time(ws, header_row, time_col, groups, r1, r2, block, timename='day'):
    """groups: list of (first_col,last_col) each holding replicate animals; header label in first col of header_row
       rows r1..r2 are timepoints with the time value in time_col"""
    out = []
    for (c1, c2) in groups:
        g = str(cell(ws, c1, header_row)).strip()
        for i, c in enumerate(colrange(c1, c2)):
            for r in range(r1, r2+1):
                t = cell(ws, time_col, r)
                v = cell(ws, c, r)
                if v is None: continue
                out.append(dict(block=block, sheet=ws, group=g, rep=i+1, time=t, value=float(v), cellref=f'{ws}!{c}{r}'))
    df = pd.DataFrame(out)
    df = df.rename(columns={'time': timename})
    return df

def read_tte(ws, header_row, day_col, gcols, r1, r2, block):
    out = []
    for c in colrange(*gcols):
        g = cell(ws, c, header_row)
        if g is None: continue
        g = str(g).strip()
        for r in range(r1, r2+1):
            e = cell(ws, c, r)
            if e is None: continue
            d = cell(ws, day_col, r)
            out.append(dict(block=block, sheet=ws, group=g, day=(float(d) if d is not None else np.nan), event=int(e), cellref=f'{ws}!{c}{r}'))
    return pd.DataFrame(out)

B = {}   # endpoint blocks (single-timepoint): DataFrame(block, group, rep, value)
T = {}   # time-course blocks: DataFrame(block, group, rep, day/time, value)
S = {}   # time-to-event blocks: DataFrame(block, group, day, event)
W = {}   # body-weight blocks
META = {}

def meta(block, **kw):
    META[block] = kw

# ================= S01 =================
B['S01-A_16h'] = read_rows('S01', 'A', ('B','F'), 3, 10, 'S01-A_16h')
B['S01-A_72h'] = read_rows('S01', 'G', ('H','L'), 3, 10, 'S01-A_72h')
B['S01-B'] = read_rows('S01', 'A', ('B','F'), 14, 17, 'S01-B')
B['S01-C'] = read_rows('S01', 'A', ('B','E'), 20, 21, 'S01-C')
T['S01-D'] = read_wide_time('S01', 23, 'A', [('B','F'),('G','K'),('L','P'),('Q','U')], 24, 28, 'S01-D')
T['S01-E'] = read_wide_time('S01', 29, 'A', [('B','F'),('G','K'),('L','P'),('Q','U'),('V','Z')], 30, 34, 'S01-E')
def read_merged_row(ws, header_row, groups, r, block):
    out=[]
    for (c1,c2) in groups:
        g=str(cell(ws,c1,header_row)).strip()
        for i,c in enumerate(colrange(c1,c2)):
            v=cell(ws,c,r)
            if v is None: continue
            out.append(dict(block=block, sheet=ws, group=g, rep=i+1, value=float(v), cellref=f'{ws}!{c}{r}'))
    return pd.DataFrame(out)
B['S01-F'] = read_merged_row('S01', 35, [('B','F'),('G','K'),('L','P'),('Q','U'),('V','Z')], 36, 'S01-F')
B['S01-G'] = read_merged_row('S01', 37, [('B','F'),('G','K'),('L','P'),('Q','U'),('V','Z')], 38, 'S01-G')

# ================= S02 =================
B['S02-A'] = read_cols('S02', 2, ('A','D'), 3, 7, 'S02-A')
B['S02-B'] = read_cols('S02', 2, ('F','I'), 3, 7, 'S02-B')
B['S02-C'] = read_cols('S02', 2, ('K','O'), 3, 7, 'S02-C')
B['S02-D_CD40'] = read_cols('S02', 9, ('A','D'), 10, 14, 'S02-D_CD40')
B['S02-D_CD86'] = read_cols('S02', 9, ('F','I'), 10, 14, 'S02-D_CD86')
B['S02-E'] = read_cols('S02', 9, ('K','O'), 10, 14, 'S02-E')
T['S02-F'] = read_wide_time('S02', 16, 'A', [('B','F'),('G','K'),('L','P')], 17, 19, 'S02-F', timename='time')
B['S02-G'] = read_cols('S02', 21, ('B','D'), 22, 26, 'S02-G')
B['S02-H'] = read_cols('S02', 29, ('B','F'), 30, 34, 'S02-H')
B['S02-I'] = read_cols('S02', 29, ('H','I'), 30, 34, 'S02-I')

# ================= S03 =================
B['S03-A'] = read_cols('S03', 2, ('A','E'), 3, 7, 'S03-A')
B['S03-B'] = read_cols('S03', 2, ('G','I'), 3, 7, 'S03-B')
B['S03-C'] = read_cols('S03', 2, ('K','O'), 3, 7, 'S03-C')
B['S03-D'] = read_cols('S03', 2, ('Q','U'), 3, 7, 'S03-D')
B['S03-E'] = read_cols('S03', 9, ('A','E'), 10, 14, 'S03-E')
B['S03-F'] = read_cols('S03', 9, ('G','I'), 10, 14, 'S03-F')
B['S03-G'] = read_cols('S03', 9, ('K','O'), 10, 14, 'S03-G')
B['S03-H'] = read_cols('S03', 9, ('Q','U'), 10, 14, 'S03-H')
S['S03-I'] = read_tte('S03', 16, 'A', ('B','F'), 17, 51, 'S03-I')
S['S03-J'] = read_tte('S03', 16, 'G', ('H','J'), 17, 46, 'S03-J')
B['S03-K'] = read_cols('S03', 16, ('L','O'), 17, 21, 'S03-K')
B['S03-L_Aicda'] = read_rows('S03', 'K', ('L','N'), 26, 28, 'S03-L_Aicda')
B['S03-L_E47'] = read_rows('S03', 'K', ('O','Q'), 26, 28, 'S03-L_E47')

# ================= S04 =================
B['S04-A_ICOSlo'] = read_rows('S04', 'A', ('B','F'), 2, 5, 'S04-A_ICOSlo')
B['S04-A_ICOShi'] = read_rows('S04', 'A', ('G','K'), 2, 5, 'S04-A_ICOShi')
B['S04-B_Tfr'] = read_cols('S04', 7, ('A','D'), 8, 12, 'S04-B_Tfr')
B['S04-B_TfhTfr'] = read_cols('S04', 14, ('A','D'), 15, 19, 'S04-B_TfhTfr')
B['S04-C'] = read_cols('S04', 21, ('A','D'), 22, 26, 'S04-C')
B['S04-D'] = read_cols('S04', 28, ('A','D'), 29, 31, 'S04-D')

# ================= S05 =================
T['S05-A'] = read_wide_time('S05', 2, 'A', [('B','C'),('E','F'),('H','I')], 3, 5, 'S05-A')
T['S05-B'] = read_wide_time('S05', 7, 'A', [('B','C'),('E','F'),('H','I')], 8, 10, 'S05-B')
B['S05-C'] = read_cols('S05', 12, ('A','D'), 13, 15, 'S05-C')
B['S05-D'] = read_cols('S05', 18, ('A','D'), 19, 23, 'S05-D')
B['S05-E'] = read_cols('S05', 25, ('A','D'), 26, 30, 'S05-E')
B['S05-F'] = read_cols('S05', 32, ('A','D'), 33, 37, 'S05-F')
B['S05-G'] = read_cols('S05', 39, ('A','D'), 40, 44, 'S05-G')
B['S05-H'] = read_cols('S05', 46, ('A','D'), 47, 51, 'S05-H')
B['S05-I'] = read_cols('S05', 53, ('A','D'), 54, 58, 'S05-I')

# ================= S06 =================
S['S06-A'] = read_tte('S06', 2, 'A', ('B','E'), 3, 30, 'S06-A')
S['S06-B'] = read_tte('S06', 2, 'G', ('H','K'), 3, 30, 'S06-B')
S['S06-C'] = read_tte('S06', 2, 'M', ('N','Q'), 3, 30, 'S06-C')
S['S06-D'] = read_tte('S06', 33, 'A', ('B','E'), 34, 61, 'S06-D')
S['S06-E'] = read_tte('S06', 33, 'G', ('H','L'), 34, 68, 'S06-E')
S['S06-F'] = read_tte('S06', 33, 'M', ('N','R'), 34, 68, 'S06-F')
S['S06-G'] = read_tte('S06', 70, 'A', ('B','F'), 71, 105, 'S06-G')
S['S06-E2'] = read_tte('S06', 70, 'G', ('H','K'), 71, 98, 'S06-E2')   # second block labelled "S06-E" (rows 69-98, cols G-K): imprinting, PR8
S['S06-F2'] = read_tte('S06', 70, 'M', ('N','Q'), 71, 98, 'S06-F2')   # second block labelled "S06-F" (rows 69-98, cols M-Q): imprinting, Perth

# ================= S07 =================
T['S07-A'] = read_wide_time('S07', 2, 'A', [('B','D'),('E','G')], 3, 7, 'S07-A')
def read_cols_labelrow(ws, header_row, cols, r1, r2, block, prefix=''):
    df = read_cols(ws, header_row, cols, r1, r2, block)
    return df
B['S07-B_mono'] = read_cols('S07', 9, ('B','C'), 10, 14, 'S07-B_mono')
B['S07-B_Ly6CMac'] = read_cols('S07', 9, ('E','F'), 10, 14, 'S07-B_Ly6CMac')
# S07-C has two identically-labelled columns -> keep column letter in the group name
_d=[]
for c in ['B','C']:
    for r in range(16,21):
        _d.append(dict(block='S07-C', sheet='S07', group=f"{cell('S07',c,15)} [col {c}]", rep=r-15, value=float(cell('S07',c,r)), cellref=f'S07!{c}{r}'))
B['S07-C'] = pd.DataFrame(_d)

# ================= S08 =================
T['S08-A'] = read_wide_time('S08', 2, 'A', [('B','D'),('E','G'),('H','J'),('K','M')], 3, 7, 'S08-A', timename='dose_ug')
B['S08-B'] = read_merged_row('S08', 10, [('A','C'),('D','F'),('G','I'),('J','L'),('M','O')], 11, 'S08-B')
B['S08-C'] = read_cols('S08', 13, ('A','D'), 14, 18, 'S08-C')
W['S08-D'] = read_wide_time('S08', 20, 'A', [('B','F'),('G','K'),('L','P'),('Q','U'),('V','Z'),('AA','AE')], 21, 26, 'S08-D')

# ================= S09 =================
def read_s09a(c1, c2, block):
    out=[]
    cols = colrange(c1,c2)
    for gi in range(7):
        gc = cols[gi*3:(gi+1)*3]
        g = str(cell('S09', gc[0], 2)).strip()
        for r in range(3,10):
            an = cell('S09', 'A', r)
            for i,c in enumerate(gc):
                v = cell('S09', c, r)
                if v is None: continue
                out.append(dict(block=block, sheet='S09', analyte=an, group=g, rep=i+1, value=float(v), cellref=f'S09!{c}{r}'))
    return pd.DataFrame(out)
B['S09-A_left'] = read_s09a('B','V','S09-A_left')     # columns B..V  (printed "16h")
B['S09-A_right'] = read_s09a('Y','AS','S09-A_right')  # columns Y..AS (printed "16h")
S['S09-B'] = read_tte('S09', 11, 'A', ('B','D'), 12, 35, 'S09-B')
W['S09-C'] = read_wide_time('S09', 11, 'F', [('G','N'),('O','V'),('W','AD')], 12, 19, 'S09-C')
S['S09-D'] = read_tte('S09', 38, 'A', ('B','D'), 39, 62, 'S09-D')
W['S09-E'] = read_wide_time('S09', 38, 'F', [('G','N'),('O','V'),('W','AD')], 39, 46, 'S09-E')
S['S09-F'] = read_tte('S09', 65, 'A', ('B','D'), 66, 88, 'S09-F')
W['S09-G'] = read_wide_time('S09', 65, 'F', [('G','N'),('O','V'),('W','AD')], 66, 73, 'S09-G')

# ================= S10 =================
B['S10-A_Ifnb1'] = read_cols('S10', 2, ('A','D'), 3, 7, 'S10-A_Ifnb1')
B['S10-A_Tnf'] = read_cols('S10', 2, ('F','I'), 3, 7, 'S10-A_Tnf')
B['S10-A_Isg15'] = read_cols('S10', 2, ('K','N'), 3, 7, 'S10-A_Isg15')

# ================= S11 =================
G4 = [('B','F'),('G','K'),('L','P'),('Q','U')]
T['S11-A'] = read_wide_time('S11', 2, 'A', G4, 3, 7, 'S11-A')
T['S11-B'] = read_wide_time('S11', 9, 'A', G4, 10, 14, 'S11-B')
B['S11-C'] = read_cols('S11', 16, ('A','B'), 17, 21, 'S11-C')
T['S11-D'] = read_wide_time('S11', 23, 'A', G4, 24, 28, 'S11-D')
B['S11-E'] = read_cols('S11', 30, ('A','D'), 31, 35, 'S11-E')

# ================= S12 =================
B['S12-A'] = read_cols('S12', 2, ('A','B'), 3, 5, 'S12-A')

# ================= S13 =================
B['S13-A'] = read_cols('S13', 2, ('A','C'), 3, 7, 'S13-A')
B['S13-B'] = read_cols('S13', 2, ('E','G'), 3, 7, 'S13-B')
B['S13-C'] = read_cols('S13', 2, ('I','K'), 3, 7, 'S13-C')
B['S13-D'] = read_cols('S13', 2, ('M','O'), 3, 7, 'S13-D')
S['S13-E'] = read_tte('S13', 2, 'R', ('S','V'), 3, 30, 'S13-E')
W['S13-F'] = read_wide_time('S13', 32, 'A', [('B','H'),('I','O'),('P','V'),('W','AC'),('AD','AJ')], 33, 40, 'S13-F')
W['S13-G'] = read_wide_time('S13', 42, 'A', [('B','K'),('L','U'),('V','AE')], 43, 50, 'S13-G')
B['S13-H'] = read_cols('S13', 52, ('A','D'), 53, 57, 'S13-H')
B['S13-I'] = read_cols('S13', 52, ('F','J'), 53, 57, 'S13-I')
B['S13-J'] = read_cols('S13', 52, ('L','P'), 53, 57, 'S13-J')

# ================= S14 =================
B['S14-A_H1N1'] = read_cols('S14', 2, ('A','D'), 3, 7, 'S14-A_H1N1')
B['S14-A_H3N2'] = read_cols('S14', 2, ('F','I'), 3, 7, 'S14-A_H3N2')

# ================= S15 =================
G4w = [('B','H'),('I','O'),('P','V'),('W','AC')]
G5w = G4w + [('AD','AJ')]
W['S15-A'] = read_wide_time('S15', 2, 'A', G4w, 3, 10, 'S15-A')
W['S15-B'] = read_wide_time('S15', 12, 'A', G4w, 13, 20, 'S15-B')
W['S15-C'] = read_wide_time('S15', 22, 'A', G4w, 23, 30, 'S15-C')
W['S15-D'] = read_wide_time('S15', 32, 'A', G4w, 33, 40, 'S15-D')
W['S15-E'] = read_wide_time('S15', 42, 'A', G5w, 43, 50, 'S15-E')
W['S15-F'] = read_wide_time('S15', 52, 'A', G5w, 53, 60, 'S15-F')
W['S15-G'] = read_wide_time('S15', 62, 'A', G5w, 63, 70, 'S15-G')
S['S15-H'] = read_tte('S15', 72, 'A', ('B','D'), 73, 93, 'S15-H')
W['S15-I'] = read_wide_time('S15', 71, 'H', [('I','O'),('P','V'),('W','AC')], 72, 79, 'S15-I')
G4x = [('I','O'),('P','V'),('W','AC'),('AD','AJ')]
W['S15-J'] = read_wide_time('S15', 82, 'H', G4x, 83, 90, 'S15-J')
W['S15-K'] = read_wide_time('S15', 92, 'H', G4x, 93, 100, 'S15-K')
S['S15-L'] = read_tte('S15', 102, 'A', ('B','E'), 103, 130, 'S15-L')
W['S15-M'] = read_wide_time('S15', 102, 'H', G4x, 103, 110, 'S15-M')
S['S15-N'] = read_tte('S15', 133, 'A', ('B','E'), 134, 161, 'S15-N')
W['S15-O'] = read_wide_time('S15', 133, 'H', G4x, 134, 141, 'S15-O')

ALL = dict(B=B, T=T, S=S, W=W)

def count_all_numeric_cells():
    n=0; coords=set()
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value,(int,float)) and not isinstance(c.value,bool):
                    n+=1; coords.add(f'{ws.title}!{c.coordinate}')
    return n, coords

if __name__ == '__main__':
    n, coords = count_all_numeric_cells()
    used=set()
    for kind,d in ALL.items():
        for k,df in d.items():
            used |= set(df['cellref'])
            if kind in ('B',):
                print(kind, k, df.groupby('group', sort=False).size().to_dict())
            elif kind=='S':
                print(kind, k, df.groupby('group', sort=False).agg(n=('event','size'), deaths=('event','sum'), missing_day=('day', lambda x: int(x.isna().sum()))).to_dict('index'))
            else:
                tcol = [c for c in df.columns if c in ('day','time','dose_ug')][0]
                print(kind, k, df.groupby(['group'], sort=False).size().to_dict(), 'times', sorted(df[tcol].unique(), key=lambda x: str(x)))
    print('numeric cells total', n, 'captured as data values', len(used))
    rest = sorted(coords-used)
    print('not captured (should be axis values / orphan region):', len(rest))
    # summarise not captured by sheet & column
    from collections import Counter
    print(Counter([(x.split('!')[0], ''.join(ch for ch in x.split('!')[1] if ch.isalpha())) for x in rest]))
