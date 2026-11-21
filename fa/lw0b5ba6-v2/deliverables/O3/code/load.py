"""Provenance-preserving parser for psln_program_dataset.xlsx.
Every observation keeps sheet + cell address so any number can be traced."""
import openpyxl, re
import pandas as pd, numpy as np
from openpyxl.utils import get_column_letter, column_index_from_string as cidx

XL = '/tmp/world/filesystem/psln_program_dataset.xlsx'
wb = openpyxl.load_workbook(XL, data_only=True)

def cell(sheet, ref):
    return wb[sheet][ref].value

def colL(i):  # 1-based -> letter
    return get_column_letter(i)

def rows_in_cols(sheet, cols, r0, r1):
    """Return list of (value, cellref) for given column letters and row range inclusive (non-empty only)"""
    ws = wb[sheet]; out=[]
    for c in cols:
        for r in range(r0, r1+1):
            v = ws[f'{c}{r}'].value
            if v is not None and not isinstance(v,str):
                out.append((float(v), f'{c}{r}'))
    return out

REC = []  # tidy records
def add(block, sheet, group, value, ref, **kw):
    d = dict(block=block, sheet=sheet, group=group, value=value, cell=f'{sheet}!{ref}')
    d.update(kw); REC.append(d)

# ---------- group in column header, values down the column ----------
def col_block(block, sheet, header_row, cols, r0, r1, **kw):
    ws = wb[sheet]
    for c in cols:
        g = ws[f'{c}{header_row}'].value
        g = str(g).strip()
        for r in range(r0, r1+1):
            v = ws[f'{c}{r}'].value
            if v is None or isinstance(v,str): continue
            add(block, sheet, g, float(v), f'{c}{r}', **kw)

# ---------- group label in column A (or given col), values across the row ----------
def row_block(block, sheet, label_col, rows, c0, c1, **kw):
    ws = wb[sheet]
    for r in rows:
        g = str(ws[f'{label_col}{r}'].value).strip()
        for ci in range(cidx(c0), cidx(c1)+1):
            v = ws[f'{colL(ci)}{r}'].value
            if v is None or isinstance(v,str): continue
            add(block, sheet, g, float(v), f'{colL(ci)}{r}', **kw)

# ---------- time rows x merged group headers ----------
def time_group_block(block, sheet, header_row, groups, rows, time_col='A', time_name='time', **kw):
    """groups: list of (label_cell_col, first_col, last_col)"""
    ws = wb[sheet]
    for (hc, c0, c1) in groups:
        g = str(ws[f'{hc}{header_row}'].value).strip()
        for r in rows:
            t = ws[f'{time_col}{r}'].value
            for ci in range(cidx(c0), cidx(c1)+1):
                v = ws[f'{colL(ci)}{r}'].value
                if v is None or isinstance(v,str): continue
                add(block, sheet, g, float(v), f'{colL(ci)}{r}', **{time_name: t}, animal_col=colL(ci), **kw)

# =================== S01 ===================
row_block('S01-A_16h','S01','A',range(3,11),'B','F', measurand='Ifnb1 lung fold (16h)')
row_block('S01-A_72h','S01','G',range(3,11),'H','L', measurand='Ifnb1 lung fold (72h)')
row_block('S01-B','S01','A',range(14,18),'B','F', measurand='%SRB+ AEC')
row_block('S01-C','S01','A',range(20,22),'B','E', measurand='%DiD+ AM')
time_group_block('S01-D','S01',23,[('B','B','F'),('G','G','K'),('L','L','P'),('Q','Q','U')],range(24,29),time_name='day', measurand='lung monocytes %')
time_group_block('S01-E','S01',29,[('B','B','F'),('G','G','K'),('L','L','P'),('Q','Q','U'),('V','V','Z')],range(30,35),time_name='day', measurand='lung CD11b+ DC %')
time_group_block('S01-F','S01',35,[('B','B','F'),('G','G','K'),('L','L','P'),('Q','Q','U'),('V','V','Z')],[36], time_col='A', measurand='lung cDC1 % (72h)')
time_group_block('S01-G','S01',37,[('B','B','F'),('G','G','K'),('L','L','P'),('Q','Q','U'),('V','V','AA')],[38], time_col='A', measurand='lung cDC2 % (72h)')
# =================== S02 ===================
col_block('S02-A','S02',2,list('ABCD'),3,7, measurand='lung CCR7+ migratory CD11b+ DC % (72h)')
col_block('S02-B','S02',2,list('FGHI'),3,7, measurand='MLN CD11b+CD103- DC % (72h)')
col_block('S02-C','S02',2,list('KLMNO'),3,7, measurand='MLN AF647-OVA+ DC % (36h)')
col_block('S02-D_CD40','S02',9,list('ABCD'),10,14, measurand='MLN CD11b+ DC CD40+ % (d3)')
col_block('S02-D_CD86','S02',9,list('FGHI'),10,14, measurand='MLN CD11b+ DC CD86+ % (d3)')
col_block('S02-E','S02',9,list('KLMNO'),10,14, measurand='OT-I proliferation % (DC co-culture)')
time_group_block('S02-F','S02',16,[('B','B','F'),('G','G','K'),('L','L','P')],range(17,20),time_name='hour', measurand='Gm-csf lung fold')
col_block('S02-G','S02',21,list('BCD'),22,26, measurand='lung Ly6C+ moDC-like % (d5)')
col_block('S02-H','S02',29,list('BCDEF'),30,34, measurand='CD45.2+ moDC % (d3)')
col_block('S02-I','S02',29,list('HI'),30,34, measurand='lung GZMB+ CD8 % (d5)')
# =================== S03 ===================
col_block('S03-A','S03',2,list('ABCDE'),3,7, measurand='serum IgG CA09 (d14)')
col_block('S03-B','S03',2,list('GHI'),3,7, measurand='IgG2a/IgG1 CA09 (d14) [as printed]')
col_block('S03-C','S03',2,list('KLMNO'),3,7, measurand='HAI CA09 (d14)')
col_block('S03-D','S03',2,list('QRSTU'),3,7, measurand='Neut CA09 (d14)')
col_block('S03-E','S03',9,list('ABCDE'),10,14, measurand='serum IgG Aichi (d14)')
col_block('S03-F','S03',9,list('GHI'),10,14, measurand='IgG2a/IgG1 Aichi (d14) [as printed]')
col_block('S03-G','S03',9,list('KLMNO'),10,14, measurand='HAI Aichi (d14)')
col_block('S03-H','S03',9,list('QRSTU'),10,14, measurand='Neut Aichi (d14)')
col_block('S03-K','S03',16,list('LMNO'),17,21, measurand='MLN GC B % (d7)')
row_block('S03-L_Aicda','S03','K',range(26,29),'L','N', measurand='Aicda MLN B fold (d5)')
row_block('S03-L_E47','S03','K',range(26,29),'O','Q', measurand='E47 MLN B fold (d5)')
# =================== S04 ===================
row_block('S04-A_ICOSlo','S04','A',range(2,6),'B','F', measurand='Tfh ICOS-lo % (d7)')
row_block('S04-A_ICOShi','S04','A',range(2,6),'G','K', measurand='Tfh ICOS-hi % (d7)')
col_block('S04-B_Tfr','S04',7,list('ABCD'),8,12, measurand='Tfr Foxp3+ in CXCR5+ICOShi % (d7)')
col_block('S04-B_TfhTfr','S04',14,list('ABCD'),15,19, measurand='Tfh:Tfr ratio (d7)')
col_block('S04-C','S04',21,list('ABCD'),22,26, measurand='Tfr % (d30)')
col_block('S04-D','S04',28,list('ABCD'),29,31, measurand='lung Treg % (d7)')
# =================== S05 ===================
time_group_block('S05-A','S05',2,[('B','B','C'),('E','E','F'),('H','H','I')],range(3,6),time_name='day', measurand='lung NP366 tet+ CD8 %')
time_group_block('S05-B','S05',7,[('B','B','C'),('E','E','F'),('H','H','I')],range(8,11),time_name='day', measurand='MLN NP366 tet+ CD8 %')
col_block('S05-C','S05',12,list('ABCD'),13,15, measurand='OT-I proliferation in vivo % (d4)')
col_block('S05-D','S05',18,list('ABCD'),19,23, measurand='lung Ki67+ CD8 % (d3)')
col_block('S05-E','S05',25,list('ABCD'),26,30, measurand='lung GZMB+ CD8 % (d3)')
col_block('S05-F','S05',32,list('ABCD'),33,37, measurand='MLN IFNg+ CD8 % (d14, rgH5N1 restim)')
col_block('S05-G','S05',39,list('ABCD'),40,44, measurand='MLN IFNg+ CD8 % (d60, rgH5N1 restim)')
col_block('S05-H','S05',46,list('ABCD'),47,51, measurand='MLN GZMB+ CD8 % (d60)')
col_block('S05-I','S05',53,list('ABCD'),54,58, measurand='lung CD8 TRM % (d25)')
# =================== S07 ===================
time_group_block('S07-A','S07',2,[('B','B','D'),('E','E','G')],range(3,8),time_name='day', measurand='lung Ly6C+CCR2+ macrophages (x1e5)')
col_block('S07-B_mono','S07',9,list('BC'),10,14, measurand='lung CD11b+Ly6C+ monocytes %')
col_block('S07-B_mac','S07',9,list('EF'),10,14, measurand='lung Ly6C+ macrophages %')
col_block('S07-C','S07',15,list('BC'),16,20, measurand='lung Treg % after MPhi transfer')
# =================== S08 ===================
time_group_block('S08-A','S08',2,[('B','B','D'),('E','E','G'),('H','H','J'),('K','K','M')],range(3,8),time_name='dose_ug', measurand='Ifnb1 lung fold (16h) dose-response')
time_group_block('S08-B','S08',10,[('A','A','C'),('D','D','F'),('G','G','I'),('J','J','L'),('M','M','O')],[11], time_col='A', measurand='encapsulation efficiency %')
col_block('S08-C','S08',13,list('ABCD'),14,18, measurand='%SRB+ AEC (S08-C gating)')
time_group_block('S08-D','S08',20,[('B','B','F'),('G','G','K'),('L','L','P'),('Q','Q','U'),('V','V','Z'),('AA','AA','AE')],range(21,27),time_name='day', measurand='body weight % post-vaccination')
# =================== S09 ===================
ws = wb['S09']
for blockname, c0 in [('S09-A_blk1','B'),('S09-A_blk2','Y')]:
    gcols = [(colL(cidx(c0)+3*k)) for k in range(7)]
    for r in range(3,10):
        analyte = ws[f'{"A" if c0=="B" else "X"}{r}'].value
        for gc in gcols:
            g = str(ws[f'{gc}2'].value).strip()
            for ci in range(cidx(gc), cidx(gc)+3):
                v = ws[f'{colL(ci)}{r}'].value
                if v is None: continue
                add(blockname,'S09',g,float(v),f'{colL(ci)}{r}', analyte=analyte, measurand='log10 fold lung transcript (label: 16h)')
time_group_block('S09-C','S09',11,[('G','G','N'),('O','O','V'),('W','W','AD')],range(12,20),time_col='F',time_name='day', measurand='body weight % post-challenge')
time_group_block('S09-E','S09',38,[('G','G','N'),('O','O','V'),('W','W','AD')],range(39,47),time_col='F',time_name='day', measurand='body weight % post-challenge')
time_group_block('S09-G','S09',65,[('G','G','N'),('O','O','V'),('W','W','AD')],range(66,74),time_col='F',time_name='day', measurand='body weight % post-challenge')
# =================== S10 ===================
col_block('S10-A_Ifnb1','S10',2,list('ABCD'),3,7, measurand='CNS Ifnb1 fold (36h)')
col_block('S10-A_Tnf','S10',2,list('FGHI'),3,7, measurand='CNS Tnf fold (36h)')
col_block('S10-A_Isg15','S10',2,list('KLMN'),3,7, measurand='CNS Isg15 fold (36h)')
# =================== S11 ===================
time_group_block('S11-A','S11',2,[('B','B','F'),('G','G','K'),('L','L','P'),('Q','Q','U')],range(3,8),time_name='day', measurand='lung alveolar macrophages %')
time_group_block('S11-B','S11',9,[('B','B','F'),('G','G','K'),('L','L','P'),('Q','Q','U')],range(10,15),time_name='day', measurand='lung neutrophils %')
col_block('S11-C','S11',16,list('AB'),17,21, measurand='lung recruited monocytes % (d3)')
time_group_block('S11-D','S11',23,[('B','B','F'),('G','G','K'),('L','L','P'),('Q','Q','U')],range(24,29),time_name='day', measurand='lung NK %')
col_block('S11-E','S11',30,list('ABCD'),31,35, measurand='lung CD206+ macrophages %')
# =================== S12-S14 ===================
col_block('S12-A','S12',2,list('AB'),3,5, measurand='CD45.2+ CD11b+Ly6C+ monocytes % (d3)')
col_block('S13-A','S13',2,list('ABC'),3,7, measurand='IgG2a CA09 (d14)')
col_block('S13-B','S13',2,list('EFG'),3,7, measurand='IgG1 CA09 (d14)')
col_block('S13-C','S13',2,list('IJK'),3,7, measurand='IgG2a Aichi (d14)')
col_block('S13-D','S13',2,list('MNO'),3,7, measurand='IgG1 Aichi (d14)')
time_group_block('S13-F','S13',32,[('B','B','H'),('I','I','O'),('P','P','V'),('W','W','AC'),('AD','AD','AJ')],range(33,41),time_name='day', measurand='body weight % post-challenge')
time_group_block('S13-G','S13',42,[('B','B','K'),('L','L','U'),('V','V','AE')],range(43,51),time_name='day', measurand='body weight % post-challenge')
col_block('S13-H','S13',52,list('ABCD'),53,57, measurand='MLN IgG+ of B220+ %')
col_block('S13-I','S13',52,list('FGHIJ'),53,57, measurand='serum IgG CA09 (d28, boosted d14)')
col_block('S13-J','S13',52,list('LMNOP'),53,57, measurand='serum IgG Aichi (d28, boosted d14)')
col_block('S14-A_H1N1','S14',2,list('ABCD'),3,7, measurand='MLN IFNg+ CD8 % (CA09 restim)')
col_block('S14-A_H3N2','S14',2,list('FGHI'),3,7, measurand='MLN IFNg+ CD8 % (Aichi restim)')
# =================== S15 body weights ===================
bw_std = [('B','B','H'),('I','I','O'),('P','P','V'),('W','W','AC')]
bw_5 = bw_std+[('AD','AD','AJ')]
for name,hr,r0 in [('S15-A',2,3),('S15-B',12,13),('S15-C',22,23),('S15-D',32,33)]:
    time_group_block(name,'S15',hr,bw_std,range(r0,r0+8),time_name='day', measurand='body weight % post-challenge')
for name,hr,r0 in [('S15-E',42,43),('S15-F',52,53),('S15-G',62,63)]:
    time_group_block(name,'S15',hr,bw_5,range(r0,r0+8),time_name='day', measurand='body weight % post-challenge')
time_group_block('S15-I','S15',71,[('I','I','O'),('P','P','V'),('W','W','AC')],range(72,80),time_col='H',time_name='day', measurand='body weight % post-challenge')
time_group_block('S15-J','S15',82,[('I','I','O'),('P','P','V'),('W','W','AC'),('AD','AD','AJ')],range(83,91),time_col='H',time_name='day', measurand='body weight % post-challenge')
time_group_block('S15-K','S15',92,[('I','I','O'),('P','P','V'),('W','W','AC'),('AD','AD','AJ')],range(93,101),time_col='H',time_name='day', measurand='body weight % post-challenge')
time_group_block('S15-M','S15',102,[('I','I','O'),('P','P','V'),('W','W','AC'),('AD','AD','AJ')],range(103,111),time_col='H',time_name='day', measurand='body weight % post-challenge')
time_group_block('S15-O','S15',133,[('I','I','O'),('P','P','V'),('W','W','AC'),('AD','AD','AJ')],range(134,142),time_col='H',time_name='day', measurand='body weight % post-challenge')

DF = pd.DataFrame(REC)

# =================== survival ===================
SURV = []
def surv_block(block, sheet, header_row, time_col, group_cols, r0, r1, **kw):
    ws = wb[sheet]
    for r in range(r0, r1+1):
        t = ws[f'{time_col}{r}'].value
        for gc in group_cols:
            e = ws[f'{gc}{r}'].value
            if e is None or isinstance(e,str): continue
            g = str(ws[f'{gc}{header_row}'].value).strip()
            SURV.append(dict(block=block, group=g, time=(float(t) if t is not None else np.nan), event=int(e),
                             cell=f'{sheet}!{time_col}{r}/{gc}{r}', **kw))
surv_block('S03-I','S03',16,'A',list('BCDEF'),17,51, model='aged BALB/c; CA09 mono vaccine; 10x mLD50 CA09 H1N1 d14 (homologous)')
surv_block('S03-J','S03',16,'G',list('HIJ'),17,46, model='aged BALB/c; rgH5N1 vaccine; wt VN04 H5N1 d2 (BSL-3)')
surv_block('S06-A','S06',2,'A',list('BCDE'),3,30, model='aged BALB/c; Aichi H3N2 vaccine; 5x PR8 H1N1 d14 (heterosubtypic)')
surv_block('S06-B','S06',2,'G',list('HIJK'),3,30, model='aged BALB/c; Aichi H3N2 vaccine; 5x PR8 H1N1 d3 (heterosubtypic, early)')
surv_block('S06-C','S06',2,'M',list('NOPQ'),3,30, model='aged BALB/c; bivalent vaccine; 5x rgH5N1 d14 (heterosubtypic)')
surv_block('S06-D','S06',33,'A',list('BCDE'),34,61, model='aged BALB/c; bivalent vaccine; 5x rgH5N1 d3 (heterosubtypic, early)')
surv_block('S06-E','S06',33,'G',list('HIJKL'),34,68, model='aged BALB/c; Aichi H3N2 vaccine; 5x PR8 H1N1 d60 (durability)')
surv_block('S06-F','S06',33,'M',list('NOPQR'),34,68, model='aged BALB/c; bivalent vaccine; 5x rgH5N1 d60 (durability)')
surv_block('S06-G','S06',70,'A',list('BCDEF'),71,105, model='aged BALB/c; CA09 H1N1 vaccine; 5x Perth H3N2 d60 (heterosubtypic, durability)')
surv_block("S06-E'(imprint)",'S06',70,'G',list('HIJK'),71,98, model='14-mo BALB/c +/- PR8 imprinting; bivalent; 5x PR8')
surv_block("S06-F'(imprint)",'S06',70,'M',list('NOPQ'),71,98, model='14-mo BALB/c +/- PR8 imprinting; bivalent; 5x Perth H3N2 d14')
surv_block('S09-B','S09',11,'A',list('BCD'),12,35, model='young BALB/c; Aichi H3N2 vaccine; 5x PR8 H1N1 d21')
surv_block('S09-D','S09',38,'A',list('BCD'),39,62, model='young BALB/c; CA09 vaccine; 5x Perth H3N2 d21')
surv_block('S09-F','S09',65,'A',list('BCD'),66,88, model='young BALB/c; bivalent; 5x rgH5N1 d180')
surv_block('S13-E','S13',2,'R',list('STUV'),3,30, model='young BALB/c; CA09 vaccine; 10x CA09 d14')
surv_block('S15-H','S15',72,'A',list('BCD'),73,93, model='aged BALB/c; vaccine vs PSLN-344 alone vs combo; rgH5N1 d3')
surv_block('S15-L','S15',102,'A',list('BCDE'),103,130, model='aged C57BL/6 (20 mo); bivalent; challenge not stated')
surv_block('S15-N','S15',133,'A',list('BCDE'),134,161, model='aged Swiss Webster (20 mo); bivalent; challenge not stated')
SV = pd.DataFrame(SURV)

def norm_group(g):
    g = g.replace('Naïve','Naive').strip()
    return g
DF['group'] = DF['group'].map(norm_group); SV['group']=SV['group'].map(norm_group)
