"""
Parse psln_program_dataset.xlsx into a tidy long table with exact cell provenance.
Every block is specified explicitly (sheet, ranges, group labels) and the group
labels are VERIFIED against the header cells in the workbook, so any mismatch fails loudly.
Run in the `chem` env (openpyxl available).
"""
import openpyxl, re, json, sys
import pandas as pd
from openpyxl.utils import column_index_from_string as ci, get_column_letter as cl

WB = '/tmp/world/filesystem/psln_program_dataset.xlsx'
wb = openpyxl.load_workbook(WB, data_only=True)

rows_out = []
checks = []

def cell(ws, col, row):
    return ws[f'{col}{row}'].value

def norm(s):
    if s is None: return None
    return re.sub(r'\s+', ' ', str(s)).strip().replace('ï','i').replace('Naïve', 'Naive')

def age_of(group, default):
    g = group.replace(' ', '')
    if re.search(r'\((Y|y)\)$', g) or re.search(r'[0-9]Y$', g):
        return 'young'
    return default

def add(block, sheet, group, value, coord, meta, rep, age, time=None, event=None):
    rows_out.append(dict(block=block, sheet=sheet, group=group, age=age, value=value,
                         cell=f'{sheet}!{coord}', rep=rep, time=time, event=event, **meta))

def verify(ws, sheet, block, coord, expected):
    got = norm(ws[coord].value)
    ok = (got == norm(expected))
    checks.append(dict(block=block, cell=f'{sheet}!{coord}', expected=expected, found=got, ok=ok))
    if not ok:
        print(f'HEADER MISMATCH {block} {sheet}!{coord}: expected {expected!r} found {got!r}')

# ---------- block type handlers ----------
def cols_block(sheet, block, header_row, groups, rows, meta, default_age='aged', time=None):
    """groups: list of (group_label, column). values in `rows` below."""
    ws = wb[sheet]
    for g, c in groups:
        verify(ws, sheet, block, f'{c}{header_row}', g)
        for i, r in enumerate(rows):
            v = cell(ws, c, r)
            if v is None: continue
            add(block, sheet, norm(g), float(v), f'{c}{r}', meta, i+1, age_of(norm(g), default_age), time=time)

def rows_block(sheet, block, label_col, groups, cols, meta, default_age='aged', time=None):
    """groups: list of (group_label,row); values across `cols`."""
    ws = wb[sheet]
    for g, r in groups:
        verify(ws, sheet, block, f'{label_col}{r}', g)
        for i, c in enumerate(cols):
            v = cell(ws, c, r)
            if v is None: continue
            add(block, sheet, norm(g), float(v), f'{c}{r}', meta, i+1, age_of(norm(g), default_age), time=time)

def span(a, b):
    return [cl(i) for i in range(ci(a), ci(b)+1)]

def time_block(sheet, block, header_row, groups, time_col, time_rows, meta, default_age='aged', header_cells=None):
    """groups: list of (label, first_col, last_col) ; time in time_col rows."""
    ws = wb[sheet]
    for g, c1, c2 in groups:
        verify(ws, sheet, block, f'{c1}{header_row}', g)
        for r in time_rows:
            t = cell(ws, time_col, r)
            for i, c in enumerate(span(c1, c2)):
                v = cell(ws, c, r)
                if v is None: continue
                add(block, sheet, norm(g), float(v), f'{c}{r}', meta, i+1, age_of(norm(g), default_age), time=float(t))

def surv_block(sheet, block, header_row, day_col, groups, row_range, meta, default_age='aged'):
    ws = wb[sheet]
    r1, r2 = row_range
    for g, c in groups:
        verify(ws, sheet, block, f'{c}{header_row}', g)
        rep = 0
        for r in range(r1, r2+1):
            e = cell(ws, c, r)
            if e is None: continue
            rep += 1
            d = cell(ws, day_col, r)
            add(block, sheet, norm(g), None if d is None else float(d), f'{c}{r}', meta, rep,
                age_of(norm(g), default_age), time=None if d is None else float(d), event=int(e))

def M(measurand, unit, timepoint, **kw):
    d = dict(measurand=measurand, unit=unit, timepoint=timepoint)
    d.update(kw); return d

# =================== S01 ===================
g8 = ['Sham','CMP-204','PSLN-212','PSLN-R848','PSLN-212/R848','PSLN-344','PSLN-212(Y)','PSLN-344(Y)']
rows_block('S01','S01-A_16h','A', [(g,3+i) for i,g in enumerate(g8)], span('B','F'),
           M('Ifnb1 mRNA, total lung cells (qRT-PCR)','fold vs untreated','16 h post-dose, no vaccine'))
rows_block('S01','S01-A_72h','G', [(g,3+i) for i,g in enumerate(g8)], span('H','L'),
           M('Ifnb1 mRNA, total lung cells (qRT-PCR)','fold vs untreated','72 h post-dose, no vaccine'))
rows_block('S01','S01-B','A', [('AECII/PSLN-SRB',14),('AECI/PSLN-SRB',15),('AECII/FreeSRB',16),('AECI/FreeSRB',17)], span('B','F'),
           M('SRB+ alveolar epithelial cells (gating PDPN+EpCAM+ / MHC-II+EpCAM+)','%','16 h'))
rows_block('S01','S01-C','A', [('WT',20),('SPA/D',21)], span('B','E'),
           M('DiD+ alveolar macrophages (PSLN-344-composition liposome)','%','16 h'))
gD = [('Sham','B','F'),('PSLN-212','G','K'),('PSLN-344','L','P'),('PSLN-212(Y)','Q','U')]
time_block('S01','S01-D',23, gD, 'A', range(24,29), M('Lung monocytes CD11b+Ly6C+CD11c-Ly6G-','%','days 0-8 post-immunisation (CA09)'))
gE = gD + [('PSLN-344(Y)','V','Z')]
time_block('S01','S01-E',29, gE, 'A', range(30,35), M('Lung CD11b+ DC','%','days 0-8 post-immunisation (CA09)'))
ws = wb['S01']
for blk, hr, vr, meas in [('S01-F',35,36,'Lung cDC1 XCR1+CD172a-'),('S01-G',37,38,'Lung cDC2 XCR1-CD172a+')]:
    for g,c1,c2 in gE:
        verify(ws,'S01',blk,f'{c1}{hr}',g)
        for i,c in enumerate(span(c1,c2)):
            v = cell(ws,c,vr)
            if v is None: continue
            add(blk,'S01',g,float(v),f'{c}{vr}',M(meas,'%','72 h post-immunisation (bivalent)'),i+1,age_of(g,'aged'))

# =================== S02 ===================
r = range(3,8)
cols_block('S02','S02-A',2,[('Sham','A'),('PSLN-212','B'),('PSLN-344','C'),('PSLN-212(Y)','D')], r, M('Lung CCR7+ migratory CD11b+ DC','%','72 h (CA09)'))
cols_block('S02','S02-B',2,[('Sham','F'),('PSLN-212','G'),('PSLN-344','H'),('PSLN-212(Y)','I')], r, M('MLN CD11b+CD103- DC','%','72 h (CA09)'))
cols_block('S02','S02-C',2,[('PSLN-212','K'),('PSLN-344','L'),('PSLN-212(Y)','M'),('PTX','N'),('PSLN-344(Y)','O')], r, M('MLN AF647-OVA+ DC','%','36 h (OVA)'))
r = range(10,15)
cols_block('S02','S02-D_CD40',9,[('Sham','A'),('PSLN-212','B'),('PSLN-344','C'),('PSLN-212(Y)','D')], r, M('CD40+ of MLN CD11b+ DC','%','day 3 (CA09)'))
cols_block('S02','S02-D_CD86',9,[('Sham','F'),('PSLN-212','G'),('PSLN-344','H'),('PSLN-212(Y)','I')], r, M('CD86+ of MLN CD11b+ DC','%','day 3 (CA09)'))
cols_block('S02','S02-E',9,[('PSLN-212','K'),('PSLN-344','L'),('PSLN-212(Y)','M'),('PTX','N'),('PSLN-344(Y)','O')], r, M('OT-I CFSE-dilution after co-culture with MLN CD11b+ DC','%','DC harvest 72 h; read day 3'))
ws = wb['S02']
for g,c1,c2 in [('PSLN-344','B','F'),('PSLN-212','G','K'),('Sham','L','P')]:
    verify(ws,'S02','S02-F',f'{c1}16',g)
    for rr,t in [(17,16),(18,36),(19,72)]:
        verify(ws,'S02','S02-F',f'A{rr}',f'{t}h')
        for i,c in enumerate(span(c1,c2)):
            add('S02-F','S02',g,float(cell(ws,c,rr)),f'{c}{rr}',M('Gm-csf mRNA, lung','fold vs untreated','16/36/72 h (bivalent)'),i+1,'aged',time=float(t))
cols_block('S02','S02-G',21,[('GM-CSF','B'),('PSLN-212','C'),('PSLN-212+GM-CSF','D')], range(22,27), M('Lung Ly6C+CD11c+MHC-II+F4/80-int (moDC-like)','%','day 5'), default_age='unstated')
cols_block('S02','S02-H',29,[('WT w/o cDC','B'),('WT w/ cDC','C'),('IFN w/o cDC','D'),('IFN w/ cDC','E'),('GMCSF','F')], range(30,35), M('CD45.2+ moDC (BM chimera, PSLN-344)','%','day 3'), default_age='unstated')
cols_block('S02','S02-I',29,[('PSLN-344(Y)','H'),('PSLN-344(Y)+INCB3344','I')], range(30,35), M('Lung GZMB+ CD8 T cells (+/- CCR2 antagonist)','%','day 5'), default_age='young')

# =================== S03 ===================
g5 = ['Sham','CMP-204','PSLN-212','PSLN-344','PSLN-212(Y)']
def g5cols(cols): return list(zip(g5, cols))
cols_block('S03','S03-A',2,g5cols(['A','B','C','D','E']), range(3,8), M('Serum IgG anti-CA09 (ELISA)','reciprocal endpoint titre','day 14'))
cols_block('S03','S03-B',2,[('PSLN-212','G'),('PSLN-344','H'),('PSLN-212(Y)','I')], range(3,8), M('IgG2a/IgG1 ratio anti-CA09 (as printed)','ratio','day 14'))
cols_block('S03','S03-C',2,g5cols(['K','L','M','N','O']), range(3,8), M('HAI titre anti-CA09','reciprocal titre (LoD 10)','day 14'))
cols_block('S03','S03-D',2,g5cols(['Q','R','S','T','U']), range(3,8), M('Neutralising titre anti-CA09','reciprocal titre','day 14'))
cols_block('S03','S03-E',9,g5cols(['A','B','C','D','E']), range(10,15), M('Serum IgG anti-Aichi H3N2 (ELISA)','reciprocal endpoint titre','day 14'))
cols_block('S03','S03-F',9,[('PSLN-212','G'),('PSLN-344','H'),('PSLN-212(Y)','I')], range(10,15), M('IgG2a/IgG1 ratio anti-Aichi (as printed)','ratio','day 14'))
cols_block('S03','S03-G',9,g5cols(['K','L','M','N','O']), range(10,15), M('HAI titre anti-Aichi H3N2','reciprocal titre (LoD 10)','day 14'))
cols_block('S03','S03-H',9,g5cols(['Q','R','S','T','U']), range(10,15), M('Neutralising titre anti-Aichi H3N2','reciprocal titre','day 14'))
surv_block('S03','S03-I',16,'A', g5cols(['B','C','D','E','F']), (17,51), M('Survival, 10xmLD50 CA09 H1N1 (homologous) at d14','event','14 d obs', exp='S03-I'))
surv_block('S03','S03-J',16,'G', [('Sham','H'),('PSLN-212','I'),('PSLN-344','J')], (17,46), M('Survival, WT VN04 H5N1 at d2 after rgH5N1 vaccine','event','22 d obs', exp='S03-J'))
cols_block('S03','S03-K',16,[('Sham','L'),('PSLN-212','M'),('PSLN-344','N'),('PSLN-212(Y)','O')], range(17,22), M('MLN GC B cells CXCR5+GL7+','%','day 7'))
ws = wb['S03']
verify(ws,'S03','S03-L','L25','Aicda'); verify(ws,'S03','S03-L','O25','E47')
for g,rr in [('Sham',26),('PSLN-212',27),('PSLN-344',28)]:
    verify(ws,'S03','S03-L',f'K{rr}',g)
    for blk,cs in [('S03-L_Aicda',['L','M','N']),('S03-L_E47',['O','P','Q'])]:
        for i,c in enumerate(cs):
            add(blk,'S03',g,float(cell(ws,c,rr)),f'{c}{rr}',M(f'{blk.split("_")[1]} mRNA, MLN B cells','fold vs untreated','day 5'),i+1,'aged')

# =================== S04 ===================
ws = wb['S04']
verify(ws,'S04','S04-A','B1','ICOS-CXCR5+PD1+'); verify(ws,'S04','S04-A','G1','ICOS+CXCR5+PD1+')
for g,rr in [('Sham',2),('PSLN-212',3),('PSLN-344',4),('PSLN-212(Y)',5)]:
    verify(ws,'S04','S04-A',f'A{rr}',g)
    for blk,cs in [('S04-A_ICOSlo',span('B','F')),('S04-A_ICOShi',span('G','K'))]:
        for i,c in enumerate(cs):
            add(blk,'S04',g,float(cell(ws,c,rr)),f'{c}{rr}',M(f'MLN Tfh CD4+CXCR5+PD1+ {blk.split("_")[1]}','%','day 7'),i+1,age_of(g,'aged'))
g4 = [('Sham','A'),('PSLN-212','B'),('PSLN-344','C'),('PSLN-212(Y)','D')]
cols_block('S04','S04-B_Foxp3',7,g4, range(8,13), M('MLN Tfr Foxp3+ in CXCR5+ICOShi','%','day 7'))
cols_block('S04','S04-B_TfhTfr',14,g4, range(15,20), M('Tfh:Tfr quotient (as printed)','ratio','day 7'))
cols_block('S04','S04-C',21,g4, range(22,27), M('MLN Tfr Foxp3+','%','day 30'))
cols_block('S04','S04-D',28,g4, range(29,32), M('Lung Treg CD4+Foxp3+','%','day 7'))

# =================== S05 ===================
ws = wb['S05']
for blk, hr, rws, meas in [('S05-A',2,range(3,6),'Lung NP366 tetramer+ CD8'),('S05-B',7,range(8,11),'MLN NP366 tetramer+ CD8')]:
    for g,c1,c2 in [('PSLN-212','B','C'),('PSLN-344','E','F'),('PSLN-212Y','H','I')]:
        verify(ws,'S05',blk,f'{c1}{hr}',g)
        for rr in rws:
            for i,c in enumerate([c1,c2]):
                add(blk,'S05',g,float(cell(ws,c,rr)),f'{c}{rr}',M(meas,'%','days 3/5/7'),i+1,age_of(g,'aged'),time=float(cell(ws,'A',rr)))
cols_block('S05','S05-C',12,[('Lung','A'),('Lung+PTX','B'),('MLN','C'),('MLN+PTX','D')], range(13,16), M('OT-I proliferation (CFSE) +/- pertussis toxin','%','day 4'), default_age='unstated')
for blk,hr,r1,meas,tp in [('S05-D',18,19,'Lung Ki-67+ CD8','day 3'),('S05-E',25,26,'Lung GZMB+ CD8','day 3'),
                          ('S05-F',32,33,'MLN IFN-g+ CD8 (rgH5N1 restim)','day 14'),('S05-G',39,40,'MLN IFN-g+ CD8 (rgH5N1 restim)','day 60'),
                          ('S05-H',46,47,'MLN GZMB+ CD8','day 60'),('S05-I',53,54,'Lung TRM CD8 CD69+CD103+','day 25')]:
    cols_block('S05',blk,hr,g4, range(r1,r1+5), M(meas,'%',tp))

# =================== S06 ===================
g4s = ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']
surv_block('S06','S06-A',2,'A', list(zip(g4s,['B','C','D','E'])), (3,30), M('Survival: Aichi H3N2 vacc -> 5x PR8 H1N1 at d14','event','14 d', exp='S06-A'))
surv_block('S06','S06-B',2,'G', list(zip(g4s,['H','I','J','K'])), (3,30), M('Survival: Aichi H3N2 vacc -> 5x PR8 H1N1 at d3','event','14 d', exp='S06-B'))
surv_block('S06','S06-C',2,'M', list(zip(g4s,['N','O','P','Q'])), (3,30), M('Survival: bivalent -> 5x rgH5N1 at d14','event','14 d', exp='S06-C'))
surv_block('S06','S06-D',33,'A', list(zip(g4s,['B','C','D','E'])), (34,61), M('Survival: bivalent -> 5x rgH5N1 at d3','event','14 d', exp='S06-D'))
surv_block('S06','S06-E',33,'G', list(zip(g4s+['Untreated'],['H','I','J','K','L'])), (34,68), M('Survival: Aichi H3N2 vacc -> 5x PR8 H1N1 at d60','event','14 d', exp='S06-E'))
surv_block('S06','S06-F',33,'M', list(zip(g4s+['Untreated'],['N','O','P','Q','R'])), (34,68), M('Survival: bivalent -> 5x rgH5N1 at d60','event','14 d', exp='S06-F'))
surv_block('S06','S06-G',70,'A', list(zip(g4s+['Untreated'],['B','C','D','E','F'])), (71,105), M('Survival: CA09 vacc -> 5x Perth H3N2 at d60','event','14 d', exp='S06-G'))
gi = ['Naive+PSLN-212','Imprinting+PSLN-212','Naive+PSLN-344','Imprinting+PSLN-344']
surv_block('S06','S06-E2_imprint',70,'G', list(zip(gi,['H','I','J','K'])), (71,98), M('Survival: imprinting (14 mo) bivalent -> 5x PR8 H1N1','event','14 d', exp='S06-E2'), default_age='14mo')
surv_block('S06','S06-F2_imprint',70,'M', list(zip(gi,['N','O','P','Q'])), (71,98), M('Survival: imprinting (14 mo) bivalent -> 5x Perth H3N2 at d14','event','14 d', exp='S06-F2'), default_age='14mo')

# =================== S07 ===================
ws = wb['S07']
for g,c1,c2 in [('PSLN-212','B','D'),('PSLN-344','E','G')]:
    verify(ws,'S07','S07-A',f'{c1}2',g)
    for rr in range(3,8):
        for i,c in enumerate(span(c1,c2)):
            add('S07-A','S07',g,float(cell(ws,c,rr)),f'{c}{rr}',M('Lung Ly6C+CCR2+ macrophages','cells x10^5','days 0-30'),i+1,'aged',time=float(cell(ws,'A',rr)))
verify(ws,'S07','S07-B','B8','CD11b+Ly6C+ Monocytes'); verify(ws,'S07','S07-B','E8','Ly6C+ Mφ')
for blk,cols in [('S07-B_Mono',[('PSLN-344','B'),('PSLN-344+INCB3344','C')]),('S07-B_Ly6CMac',[('PSLN-344','E'),('PSLN-344+INCB3344','F')])]:
    cols_block('S07',blk,9,cols, range(10,15), M(blk,'%','not stated'), default_age='unstated')
# S07-C: both headers identical -> keep as printed with column suffix
for g,c in [('Ly6C-CD206+ MΦ','B'),('Ly6C-CD206+ MΦ','C')]:
    verify(ws,'S07','S07-C',f'{c}15',g)
    for i,rr in enumerate(range(16,21)):
        add('S07-C','S07',f'{g} [col {c}]',float(cell(ws,c,rr)),f'{c}{rr}',M('Lung Treg after macrophage transfer','%','day 4 post-transfer'),i+1,'aged')

# =================== S08 ===================
ws = wb['S08']
for g,c1,c2 in [('CMP-204','B','D'),('PSLN-212','E','G'),('PSLN-344','H','J'),('PSLN-344/R848','K','M')]:
    verify(ws,'S08','S08-A',f'{c1}2',g)
    for rr in range(3,8):
        for i,c in enumerate(span(c1,c2)):
            add('S08-A','S08',g,float(cell(ws,c,rr)),f'{c}{rr}',M('Ifnb1 mRNA lung, dose-response','fold vs untreated','16 h'),i+1,'unstated',time=float(cell(ws,'A',rr)))
for g,c1,c2 in [('CMP-204','A','C'),('PSLN-212','D','F'),('PSLN-R848','G','I'),('PSLN-212/R848','J','L'),('PSLN-344','M','O')]:
    verify(ws,'S08','S08-B',f'{c1}10',g)
    for i,c in enumerate(span(c1,c2)):
        add('S08-B','S08',g,float(cell(ws,c,11)),f'{c}11',M('Encapsulation efficiency (A260)','%','n/a'),i+1,'n/a')
cols_block('S08','S08-C',13,[('AECII-PSLN-SRB','A'),('AECII-PSLN-344-SRB','B'),('AECI-PSLN-SRB','C'),('AECI-PSLN-344-SRB','D')], range(14,19), M('SRB+ AEC (gating PDPN/MHC-II within EpCAM+)','%','16 h'))
gw = [('PSLN-212(Y)','B','F'),('CMP-204','G','K'),('PSLN-212','L','P'),('PSLN-344','Q','U'),('PSLN-212/R848','V','Z'),('Vaccine','AA','AE')]
time_block('S08','S08-D',20, gw, 'A', range(21,27), M('Body weight after vaccination (reactogenicity)','% of d0','days 0-10 post-vaccination'))
# unlabeled region rows 89-101
for rr in range(89,102):
    for c in ['C','D']:
        v = cell(ws,c,rr)
        if v is not None:
            add('S08-UNLABELLED','S08',f'col {c}',float(cell(ws,'A',rr)),f'{c}{rr}',M('unlabelled','unknown','unknown'),rr,'unknown',time=float(cell(ws,'A',rr)),event=int(v))

# =================== S09 ===================
ws = wb['S09']
an = ['Ifnb1','Il6','Ccl2','Ccl3','Ccl5','Tnf','Il10']
p1 = [('PBS','B'),('CMP-204','E'),('PSLN-212','H'),('PSLN-R848','K'),('PSLN-212/R848','N'),('PSLN-344','Q'),('PSLN-212(y)','T')]
p2 = [('PBS','Y'),('CMP-204','AB'),('PSLN-212','AE'),('PSLN-R848','AH'),('PSLN-212/R848','AK'),('PSLN-344','AN'),('PSLN-212(y)','AQ')]
for blk, panel, labcol in [('S09-A_panel1_A-U',p1,'A'),('S09-A_panel2_X-AS',p2,'X')]:
    for g,c1 in panel:
        verify(ws,'S09',blk,f'{c1}2',g)
        for k,a in enumerate(an):
            rr = 3+k
            verify(ws,'S09',blk,f'{labcol}{rr}',a)
            for i in range(3):
                c = cl(ci(c1)+i)
                add(blk,'S09',g,float(cell(ws,c,rr)),f'{c}{rr}',M(f'{a} mRNA lung','log10 fold vs untreated','labelled 16 h', analyte=a),i+1,age_of(g,'aged'))
gS9 = [('Sham','B'),('PSLN-344Y','C'),('PSLN-212Y','D')]
surv_block('S09','S09-B',11,'A', gS9, (12,35), M('Survival young: Aichi vacc -> 5x PR8 at d21','event','14 d', exp='S09-B'), default_age='young')
surv_block('S09','S09-D',38,'A', gS9, (39,62), M('Survival young: CA09 vacc -> 5x Perth H3N2 at d21','event','14 d', exp='S09-D'), default_age='young')
surv_block('S09','S09-F',65,'A', gS9, (66,88), M('Survival young: bivalent -> 5x rgH5N1 at d180','event','14 d', exp='S09-F'), default_age='young')
gw9 = [('PSLN-212Y','G','N'),('Sham','O','V'),('PSLN-344Y','W','AD')]
time_block('S09','S09-C',11, gw9,'F', range(12,20), M('Body weight young after PR8 challenge','% of d0','days 0-14', exp='S09-B'), default_age='young')
time_block('S09','S09-E',38, gw9,'F', range(39,47), M('Body weight young after Perth challenge','% of d0','days 0-14', exp='S09-D'), default_age='young')
time_block('S09','S09-G',65, gw9,'F', range(66,74), M('Body weight young after rgH5N1 d180 challenge','% of d0','days 0-14', exp='S09-F'), default_age='young')

# =================== S10 ===================
ws = wb['S10']
for blk, cols in [('S10-A_Ifnb1',[('PBS','A'),('Sham','B'),('PSLN-344','C'),('CT','D')]),
                  ('S10-A_Tnf',[('PBS','F'),('Sham','G'),('PSLN-344','H'),('CT','I')]),
                  ('S10-A_Isg15',[('PBS','K'),('Sham','L'),('PSLN-344','M'),('CT','N')])]:
    cols_block('S10',blk,2,cols, range(3,8), M(f'CNS {blk.split("_")[1]} mRNA','fold vs untreated','36 h'))

# =================== S11 ===================
g11 = [('Vaccine','B','F'),('PSLN-212','G','K'),('PSLN-344','L','P'),('PSLN-212(Y)','Q','U')]
time_block('S11','S11-A',2, g11,'A', range(3,8), M('Lung alveolar macrophages','%','days 0-8 (CA09)'))
time_block('S11','S11-B',9, g11,'A', range(10,15), M('Lung neutrophils','%','days 0-8 (CA09)'))
cols_block('S11','S11-C',16,[('CBX+','A'),('CBX-','B')], range(17,22), M('Lung recruited monocytes +/- carbenoxolone (PSLN-344)','%','day 3'))
time_block('S11','S11-D',23, g11,'A', range(24,29), M('Lung NK cells','%','days 0-8 (CA09)'))
cols_block('S11','S11-E',30,g4, range(31,36), M('Lung CD206+ macrophages','%','not stated'))

# =================== S12 ===================
cols_block('S12','S12-A',2,[('WT to WT','A'),('IFNAR-/- to WT','B')], range(3,6), M('Infiltrating CD45.2+ CD11b+Ly6C+ monocytes (BM chimera, PSLN-344)','%','day 3'), default_age='young')

# =================== S13 ===================
cols_block('S13','S13-A',2,[('PSLN-212','A'),('PSLN-344','B'),('PSLN-212(Y)','C')], range(3,8), M('Serum IgG2a anti-CA09','reciprocal endpoint titre','day 14'))
cols_block('S13','S13-B',2,[('PSLN-212','E'),('PSLN-344','F'),('PSLN-212(Y)','G')], range(3,8), M('Serum IgG1 anti-CA09','reciprocal endpoint titre','day 14'))
cols_block('S13','S13-C',2,[('PSLN-212','I'),('PSLN-344','J'),('PSLN-212(Y)','K')], range(3,8), M('Serum IgG2a anti-Aichi','reciprocal endpoint titre','day 14'))
cols_block('S13','S13-D',2,[('PSLN-212','M'),('PSLN-344','N'),('PSLN-212(Y)','O')], range(3,8), M('Serum IgG1 anti-Aichi','reciprocal endpoint titre','day 14'))
surv_block('S13','S13-E',2,'R', [('Naive','S'),('Sham','T'),('CMP-204(Y)','U'),('PSLN-344(Y)','V')], (3,30), M('Survival young: 10x CA09 at d14','event','14 d', exp='S13-E'), default_age='young')
gw13 = [('PSLN-212(Y)','B','H'),('Sham','I','O'),('PSLN-212','P','V'),('PSLN-344','W','AC'),('Naive','AD','AJ')]
time_block('S13','S13-F',32, gw13,'A', range(33,41), M('Body weight (stated: animals of S03-I)','% of d0','days 0-14', exp='S03-I'))
gw13g = [('PSLN-344','B','K'),('Sham','L','U'),('Naive','V','AE')]
time_block('S13','S13-G',42, gw13g,'A', range(43,51), M('Body weight (stated: animals of S03-J)','% of d0','days 0-14', exp='S03-J'))
cols_block('S13','S13-H',52,g4, range(53,58), M('IgG+ of MLN B220+ cells','%','not stated'))
cols_block('S13','S13-I',52,[('Sham','F'),('CMP-204','G'),('PSLN-212','H'),('PSLN-344','I'),('PSLN-212(Y)','J')], range(53,58), M('Serum IgG anti-CA09 after boost','reciprocal endpoint titre','day 28 (boost d14)'))
cols_block('S13','S13-J',52,[('Sham','L'),('CMP-204','M'),('PSLN-212','N'),('PSLN-344','O'),('PSLN-212(Y)','P')], range(53,58), M('Serum IgG anti-Aichi after boost','reciprocal endpoint titre','day 28 (boost d14)'))

# =================== S14 ===================
cols_block('S14','S14-A_H1N1',2,g4, range(3,8), M('MLN IFN-g+ CD8 (CA09 restim)','%','not stated'))
cols_block('S14','S14-A_H3N2',2,[('Sham','F'),('PSLN-212','G'),('PSLN-344','H'),('PSLN-212(Y)','I')], range(3,8), M('MLN IFN-g+ CD8 (Aichi restim)','%','not stated'))

# =================== S15 ===================
gw15 = [('PSLN-212(Y)','B','H'),('Sham','I','O'),('PSLN-212','P','V'),('PSLN-344','W','AC')]
gw15u = gw15 + [('Untreated','AD','AJ')]
for blk, hr, r1, gg, exp in [('S15-A',2,3,gw15,'S06-A'),('S15-B',12,13,gw15,'S06-B'),('S15-C',22,23,gw15,'S06-C'),('S15-D',32,33,gw15,'S06-D'),
                         ('S15-E',42,43,gw15u,'S06-E'),('S15-F',52,53,gw15u,'S06-F'),('S15-G',62,63,gw15u,'S06-G')]:
    time_block('S15',blk,hr, gg,'A', range(r1,r1+8), M(f'Body weight after challenge ({exp})','% of d0','days 0-14', exp=exp))
surv_block('S15','S15-H',72,'A', [('3d Vaccine','B'),('3d PSLN-344','C'),('3d Vaccine+PSLN-344','D')], (73,93), M('Survival: vaccine/PSLN-344/both 3 d before 5x VN04 rgH5N1','event','14 d', exp='S15-H'))
time_block('S15','S15-I',71, [('3d Vaccine','I','O'),('3d PSLN-344','P','V'),('3d Vaccine+PSLN-344','W','AC')],'H', range(72,80), M('Body weight (animals of S15-H)','% of d0','days 0-14', exp='S15-H'))
gwi = [('Naive+PSLN-212','I','O'),('Imprinting+PSLN-212','P','V'),('Naive+PSLN-344','W','AC'),('Imprinting+PSLN-344','AD','AJ')]
time_block('S15','S15-J',82, gwi,'H', range(83,91), M('Body weight imprinting PR8 (animals of S06-E2)','% of d0','days 0-14', exp='S06-E2'), default_age='14mo')
time_block('S15','S15-K',92, gwi,'H', range(93,101), M('Body weight imprinting Perth (animals of S06-F2)','% of d0','days 0-14', exp='S06-F2'), default_age='14mo')
surv_block('S15','S15-L',102,'A', list(zip(g4s,['B','C','D','E'])), (103,130), M('Survival C57BL/6 aged (challenge not stated)','event','14 d', exp='S15-L'))
gwm = [('PSLN-212(Y)','I','O'),('Sham','P','V'),('PSLN-212','W','AC'),('PSLN-344','AD','AJ')]
time_block('S15','S15-M',102, gwm,'H', range(103,111), M('Body weight C57BL/6 (animals of S15-L)','% of d0','days 0-14', exp='S15-L'))
surv_block('S15','S15-N',133,'A', list(zip(g4s,['B','C','D','E'])), (134,161), M('Survival Swiss Webster aged (challenge not stated)','event','14 d', exp='S15-N'))
time_block('S15','S15-O',133, gwm,'H', range(134,142), M('Body weight Swiss Webster (animals of S15-N)','% of d0','days 0-14', exp='S15-N'))

df = pd.DataFrame(rows_out)
df.to_csv('/tmp/work/tidy.csv', index=False)
pd.DataFrame(checks).to_csv('/tmp/work/header_checks.csv', index=False)
print('rows', len(df), 'blocks', df.block.nunique(), 'header checks', len(checks), 'failed', sum(not c['ok'] for c in checks))
