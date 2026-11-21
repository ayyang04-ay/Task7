"""
01_extract.py  --  Parse psln_program_dataset.xlsx into tidy long tables.
Every value keeps its sheet/cell coordinate so any number can be traced to source.
Outputs (CSV, /tmp/work/tidy):
  continuous.csv : block, measurand, group, time, rep, value, cell
  survival.csv   : block, group, time, event, cell
  bodyweight.csv : block, group, animal, day, value, cell
"""
import openpyxl, pandas as pd, re
from openpyxl.utils import column_index_from_string as ci, get_column_letter as gl

WB = openpyxl.load_workbook('/tmp/world/filesystem/psln_program_dataset.xlsx', data_only=True)
cont, surv, bw = [], [], []

def v(ws, r, c):
    return ws.cell(row=r, column=c).value

def add_rows_groups(sheet, block, meas, rows, label_col, val_cols, time=None):
    """groups are row labels (label_col), replicates across val_cols"""
    ws = WB[sheet]
    for r in rows:
        g = v(ws, r, ci(label_col))
        for k, c in enumerate(val_cols):
            x = v(ws, r, ci(c))
            if x is None: continue
            cont.append(dict(block=block, measurand=meas, group=str(g).strip(), time=time, rep=k+1,
                             value=float(x), cell=f"{sheet}!{c}{r}"))

def add_cols_groups(sheet, block, meas, header_row, cols, rows, time=None, groups=None):
    """groups are column headers, replicates down rows"""
    ws = WB[sheet]
    for j, c in enumerate(cols):
        g = groups[j] if groups else v(ws, header_row, ci(c))
        for k, r in enumerate(rows):
            x = v(ws, r, ci(c))
            if x is None: continue
            cont.append(dict(block=block, measurand=meas, group=str(g).strip(), time=time, rep=k+1,
                             value=float(x), cell=f"{sheet}!{c}{r}"))

def add_timecourse(sheet, block, meas, rows, time_col, group_spans, time_override=None):
    """group_spans: list of (group, first_col, last_col); one row per timepoint, replicates across columns"""
    ws = WB[sheet]
    for i, r in enumerate(rows):
        t = time_override[i] if time_override else v(ws, r, ci(time_col))
        for g, c0, c1 in group_spans:
            for k, c in enumerate(range(ci(c0), ci(c1)+1)):
                x = v(ws, r, c)
                if x is None: continue
                cont.append(dict(block=block, measurand=meas, group=g, time=t, rep=k+1,
                                 value=float(x), cell=f"{sheet}!{gl(c)}{r}"))

def add_survival(sheet, block, rows, day_col, group_cols):
    ws = WB[sheet]
    for r in rows:
        d = v(ws, r, ci(day_col))
        for g, c in group_cols:
            x = v(ws, r, ci(c))
            if x is None: continue
            surv.append(dict(block=block, group=g, time=(float(d) if d is not None else float('nan')), event=int(x),
                             cell=f"{sheet}!{c}{r}", day_cell=f"{sheet}!{day_col}{r}"))

def add_bw(sheet, block, rows, day_col, group_spans):
    ws = WB[sheet]
    for r in rows:
        d = v(ws, r, ci(day_col))
        for g, c0, c1 in group_spans:
            for k, c in enumerate(range(ci(c0), ci(c1)+1)):
                x = v(ws, r, c)
                if x is None: continue
                bw.append(dict(block=block, group=g, animal=k+1, day=float(d), value=float(x), cell=f"{sheet}!{gl(c)}{r}"))

# ---------------- S01 ----------------
add_rows_groups('S01','S01-A','Lung Ifnb1 (fold vs untreated)', range(3,11),'A',list('BCDEF'), time='16h')
add_rows_groups('S01','S01-A','Lung Ifnb1 (fold vs untreated)', range(3,11),'G',list('HIJKL'), time='72h')
add_rows_groups('S01','S01-B','SRB+ alveolar epithelial cells (%)', range(14,18),'A',list('BCDEF'), time='16h')
add_rows_groups('S01','S01-C','DiD+ alveolar macrophages (%)', range(20,22),'A',list('BCDE'), time='16h')
sp5 = [('Sham','B','F'),('PSLN-212','G','K'),('PSLN-344','L','P'),('PSLN-212(Y)','Q','U'),('PSLN-344(Y)','V','Z')]
add_timecourse('S01','S01-D','Lung monocytes CD11b+Ly6C+ (%)', range(24,29),'A', sp5[:4], time_override=[0,2,4,6,8])
add_timecourse('S01','S01-E','Lung CD11b+ DC (%)', range(30,35),'A', sp5, time_override=[0,2,4,6,8])
add_timecourse('S01','S01-F','Lung cDC1 XCR1+ (%)', [36],'A', sp5, time_override=['72h'])
add_timecourse('S01','S01-G','Lung cDC2 CD172a+ (%)', [38],'A', sp5, time_override=['72h'])
# ---------------- S02 ----------------
add_cols_groups('S02','S02-A','Lung CCR7+ migratory CD11b+ DC (%)',2,list('ABCD'),range(3,8),time='72h')
add_cols_groups('S02','S02-B','MLN CD11b+CD103- DC (%)',2,list('FGHI'),range(3,8),time='72h')
add_cols_groups('S02','S02-C','MLN DC AF647-OVA+ (%)',2,list('KLMNO'),range(3,8),time='36h')
add_cols_groups('S02','S02-D CD40','MLN CD11b+ DC CD40+ (%)',9,list('ABCD'),range(10,15),time='d3')
add_cols_groups('S02','S02-D CD86','MLN CD11b+ DC CD86+ (%)',9,list('FGHI'),range(10,15),time='d3')
add_cols_groups('S02','S02-E','OT-I CD8 proliferation with MLN DC (%)',9,list('KLMNO'),range(10,15),time='72h DC + 3d coculture')
add_timecourse('S02','S02-F','Lung Gm-csf (fold vs untreated)', range(17,20),'A',
               [('PSLN-344','B','F'),('PSLN-212','G','K'),('Sham','L','P')], time_override=['16h','36h','72h'])
add_cols_groups('S02','S02-G','Lung Ly6C+CD11c+MHCII+ moDC-like (%)',21,list('BCD'),range(22,27),time='d5')
add_cols_groups('S02','S02-H','CD45.2+ moDC (%)',29,list('BCDEF'),range(30,35),time='d3')
add_cols_groups('S02','S02-I','Lung GZMB+ CD8 (%)',29,list('HI'),range(30,35),time='d5')
# ---------------- S03 ----------------
add_cols_groups('S03','S03-A','Serum IgG anti-CA09 H1N1 (endpoint titre)',2,list('ABCDE'),range(3,8),time='d14')
add_cols_groups('S03','S03-B','IgG2a/IgG1 ratio anti-CA09 (as printed)',2,list('GHI'),range(3,8),time='d14')
add_cols_groups('S03','S03-C','HAI titre anti-CA09 H1N1',2,list('KLMNO'),range(3,8),time='d14')
add_cols_groups('S03','S03-D','Neutralising titre anti-CA09 H1N1',2,list('QRSTU'),range(3,8),time='d14')
add_cols_groups('S03','S03-E','Serum IgG anti-Aichi H3N2 (endpoint titre)',9,list('ABCDE'),range(10,15),time='d14')
add_cols_groups('S03','S03-F','IgG2a/IgG1 ratio anti-Aichi (as printed)',9,list('GHI'),range(10,15),time='d14')
add_cols_groups('S03','S03-G','HAI titre anti-Aichi H3N2',9,list('KLMNO'),range(10,15),time='d14')
add_cols_groups('S03','S03-H','Neutralising titre anti-Aichi H3N2',9,list('QRSTU'),range(10,15),time='d14')
add_survival('S03','S03-I', range(17,52),'A',[('Sham','B'),('CMP-204','C'),('PSLN-212','D'),('PSLN-344','E'),('PSLN-212(Y)','F')])
add_survival('S03','S03-J', range(17,47),'G',[('Sham','H'),('PSLN-212','I'),('PSLN-344','J')])
add_cols_groups('S03','S03-K','MLN GC B cells CXCR5+GL7+ (%)',16,list('LMNO'),range(17,22),time='d7')
add_rows_groups('S03','S03-L','MLN B-cell Aicda (fold)', range(26,29),'K',list('LMN'), time='d5')
add_rows_groups('S03','S03-L','MLN B-cell E47 (fold)', range(26,29),'K',list('OPQ'), time='d5')
# ---------------- S04 ----------------
add_rows_groups('S04','S04-A','MLN Tfh ICOS-low CXCR5+PD1+ (%)', range(2,6),'A',list('BCDEF'), time='d7')
add_rows_groups('S04','S04-A','MLN Tfh ICOS-high CXCR5+PD1+ (%)', range(2,6),'A',list('GHIJK'), time='d7')
add_cols_groups('S04','S04-B Foxp3','MLN Tfr Foxp3+ in CXCR5+ICOShi (%)',7,list('ABCD'),range(8,13),time='d7')
add_cols_groups('S04','S04-B Tfh:Tfr','Tfh:Tfr ratio (as printed)',14,list('ABCD'),range(15,20),time='d7')
add_cols_groups('S04','S04-C','MLN Tfr Foxp3+ (%)',21,list('ABCD'),range(22,27),time='d30')
add_cols_groups('S04','S04-D','Lung Treg CD4+Foxp3+ (%)',28,list('ABCD'),range(29,32),time='d7')
# ---------------- S05 ----------------
sp3 = [('PSLN-212','B','C'),('PSLN-344','E','F'),('PSLN-212(Y)','H','I')]
add_timecourse('S05','S05-A','Lung NP366 tetramer+ CD8 (%)', range(3,6),'A', sp3)
add_timecourse('S05','S05-B','MLN NP366 tetramer+ CD8 (%)', range(8,11),'A', sp3)
add_cols_groups('S05','S05-C','OT-I proliferation (%)',12,list('ABCD'),range(13,16),time='d4')
add_cols_groups('S05','S05-D','Lung Ki-67+ CD8 (%)',18,list('ABCD'),range(19,24),time='d3')
add_cols_groups('S05','S05-E','Lung GZMB+ CD8 (%)',25,list('ABCD'),range(26,31),time='d3')
add_cols_groups('S05','S05-F','MLN IFN-g+ CD8, rgH5N1 restim (%)',32,list('ABCD'),range(33,38),time='d14')
add_cols_groups('S05','S05-G','MLN IFN-g+ CD8, rgH5N1 restim (%)',39,list('ABCD'),range(40,45),time='d60')
add_cols_groups('S05','S05-H','MLN GZMB+ CD8 (%)',46,list('ABCD'),range(47,52),time='d60')
add_cols_groups('S05','S05-I','Lung TRM CD69+CD103+ CD8 (%)',53,list('ABCD'),range(54,59),time='d25')
# ---------------- S06 (survival) ----------------
g4 = ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']
add_survival('S06','S06-A', range(3,31),'A', list(zip(g4, list('BCDE'))))
add_survival('S06','S06-B', range(3,31),'G', list(zip(g4, list('HIJK'))))
add_survival('S06','S06-C', range(3,31),'M', list(zip(g4, list('NOPQ'))))
add_survival('S06','S06-D', range(34,62),'A', list(zip(g4, list('BCDE'))))
add_survival('S06','S06-E(d60)', range(34,69),'G', list(zip(g4+['Untreated'], list('HIJKL'))))
add_survival('S06','S06-F(d60)', range(34,69),'M', list(zip(g4+['Untreated'], list('NOPQR'))))
add_survival('S06','S06-G(d60)', range(71,106),'A', list(zip(g4+['Untreated'], list('BCDEF'))))
gi = ['Naive+PSLN-212','Imprinting+PSLN-212','Naive+PSLN-344','Imprinting+PSLN-344']
add_survival('S06','S06-E(imprint)', range(71,99),'G', list(zip(gi, list('HIJK'))))
add_survival('S06','S06-F(imprint)', range(71,99),'M', list(zip(gi, list('NOPQ'))))
# ---------------- S07 ----------------
add_timecourse('S07','S07-A','Lung Ly6C+CCR2+ macrophages (x10^5 cells)', range(3,8),'A',
               [('PSLN-212','B','D'),('PSLN-344','E','G')])
add_cols_groups('S07','S07-B','Lung CD11b+Ly6C+ monocytes (%)',9,list('BC'),range(10,15),time='not stated')
add_cols_groups('S07','S07-B','Lung Ly6C+ macrophages (%)',9,list('EF'),range(10,15),time='not stated')
add_cols_groups('S07','S07-C','Lung Treg after Mphi transfer (%)',15,list('BC'),range(16,21),time='d4 post-transfer',
                groups=['Ly6C-CD206+ MPhi (col B)','Ly6C-CD206+ MPhi (col C)'])
# ---------------- S08 ----------------
add_timecourse('S08','S08-A','Lung Ifnb1 16h (fold) dose-response', range(3,8),'A',
               [('CMP-204','B','D'),('PSLN-212','E','G'),('PSLN-344','H','J'),('PSLN-344/R848','K','M')])
add_timecourse('S08','S08-B','Encapsulation efficiency (%)', [11],'A',
               [('CMP-204','A','C'),('PSLN-212','D','F'),('PSLN-R848','G','I'),('PSLN-212/R848','J','L'),('PSLN-344','M','O')],
               time_override=['n/a'])
add_cols_groups('S08','S08-C','SRB+ alveolar epithelial cells (%)',13,list('ABCD'),range(14,19),time='16h')
add_bw('S08','S08-D', range(21,27),'A', [('PSLN-212(Y)','B','F'),('CMP-204','G','K'),('PSLN-212','L','P'),
        ('PSLN-344','Q','U'),('PSLN-212/R848','V','Z'),('Vaccine','AA','AE')])
# ---------------- S09 ----------------
ws = WB['S09']
p1 = [('PBS','B','D'),('CMP-204','E','G'),('PSLN-212','H','J'),('PSLN-R848','K','M'),('PSLN-212/R848','N','P'),('PSLN-344','Q','S'),('PSLN-212(Y)','T','V')]
p2 = [('PBS','Y','AA'),('CMP-204','AB','AD'),('PSLN-212','AE','AG'),('PSLN-R848','AH','AJ'),('PSLN-212/R848','AK','AM'),('PSLN-344','AN','AP'),('PSLN-212(Y)','AQ','AS')]
for r in range(3,10):
    an = ws.cell(row=r, column=1).value
    for tag, spans in (('panel1 (cols B-V)', p1), ('panel2 (cols Y-AS)', p2)):
        for g, c0, c1 in spans:
            for k, c in enumerate(range(ci(c0), ci(c1)+1)):
                x = ws.cell(row=r, column=c).value
                if x is None: continue
                cont.append(dict(block='S09-A '+tag, measurand=f'Lung {an} (log10 fold)', group=g, time='16h (as printed)', rep=k+1,
                                 value=float(x), cell=f"S09!{gl(c)}{r}"))
add_survival('S09','S09-B', range(12,36),'A', [('Sham','B'),('PSLN-344(Y)','C'),('PSLN-212(Y)','D')])
add_bw('S09','S09-C', range(12,20),'F', [('PSLN-212(Y)','G','N'),('Sham','O','V'),('PSLN-344(Y)','W','AD')])
add_survival('S09','S09-D', range(39,63),'A', [('Sham','B'),('PSLN-344(Y)','C'),('PSLN-212(Y)','D')])
add_bw('S09','S09-E', range(39,47),'F', [('PSLN-212(Y)','G','N'),('Sham','O','V'),('PSLN-344(Y)','W','AD')])
add_survival('S09','S09-F', range(66,89),'A', [('Sham','B'),('PSLN-344(Y)','C'),('PSLN-212(Y)','D')])
add_bw('S09','S09-G', range(66,74),'F', [('PSLN-212(Y)','G','N'),('Sham','O','V'),('PSLN-344(Y)','W','AD')])
# ---------------- S10 ----------------
add_cols_groups('S10','S10-A','CNS Ifnb1 (fold)',2,list('ABCD'),range(3,8),time='36h')
add_cols_groups('S10','S10-A','CNS Tnf (fold)',2,list('FGHI'),range(3,8),time='36h')
add_cols_groups('S10','S10-A','CNS Isg15 (fold)',2,list('KLMN'),range(3,8),time='36h')
# ---------------- S11 ----------------
sp11 = [('Vaccine','B','F'),('PSLN-212','G','K'),('PSLN-344','L','P'),('PSLN-212(Y)','Q','U')]
add_timecourse('S11','S11-A','Lung alveolar macrophages (%)', range(3,8),'A', sp11)
add_timecourse('S11','S11-B','Lung neutrophils (%)', range(10,15),'A', sp11)
add_cols_groups('S11','S11-C','Lung recruited monocytes (%)',16,list('AB'),range(17,22),time='d3')
add_timecourse('S11','S11-D','Lung NK cells (%)', range(24,29),'A', sp11)
add_cols_groups('S11','S11-E','Lung CD206+ macrophages (%)',30,list('ABCD'),range(31,36),time='not stated')
# ---------------- S12 ----------------
add_cols_groups('S12','S12-A','Infiltrating CD45.2+ monocytes (%)',2,list('AB'),range(3,6),time='d3')
# ---------------- S13 ----------------
add_cols_groups('S13','S13-A','Serum IgG2a anti-CA09 (titre)',2,list('ABC'),range(3,8),time='d14')
add_cols_groups('S13','S13-B','Serum IgG1 anti-CA09 (titre)',2,list('EFG'),range(3,8),time='d14')
add_cols_groups('S13','S13-C','Serum IgG2a anti-Aichi (titre)',2,list('IJK'),range(3,8),time='d14')
add_cols_groups('S13','S13-D','Serum IgG1 anti-Aichi (titre)',2,list('MNO'),range(3,8),time='d14')
add_survival('S13','S13-E', range(3,31),'R', [('Naive','S'),('Sham','T'),('CMP-204(Y)','U'),('PSLN-344(Y)','V')])
add_bw('S13','S13-F', range(33,41),'A', [('PSLN-212(Y)','B','H'),('Sham','I','O'),('PSLN-212','P','V'),('PSLN-344','W','AC'),('Naive','AD','AJ')])
add_bw('S13','S13-G', range(43,51),'A', [('PSLN-344','B','K'),('Sham','L','U'),('Naive','V','AE')])
add_cols_groups('S13','S13-H','MLN B220+ IgG+ (%)',52,list('ABCD'),range(53,58),time='not stated')
add_cols_groups('S13','S13-I','Serum IgG anti-CA09 post-boost (titre)',52,list('FGHIJ'),range(53,58),time='d28 (boost d14)')
add_cols_groups('S13','S13-J','Serum IgG anti-Aichi post-boost (titre)',52,list('LMNOP'),range(53,58),time='d28 (boost d14)')
# ---------------- S14 ----------------
add_cols_groups('S14','S14-A H1N1','MLN IFN-g+ CD8, CA09 restim (%)',2,list('ABCD'),range(3,8),time='not stated')
add_cols_groups('S14','S14-A H3N2','MLN IFN-g+ CD8, Aichi restim (%)',2,list('FGHI'),range(3,8),time='not stated')
# ---------------- S15 ----------------
s15 = [('PSLN-212(Y)','B','H'),('Sham','I','O'),('PSLN-212','P','V'),('PSLN-344','W','AC')]
s15u = s15 + [('Untreated','AD','AJ')]
add_bw('S15','S15-A', range(3,11),'A', s15)
add_bw('S15','S15-B', range(13,21),'A', s15)
add_bw('S15','S15-C', range(23,31),'A', s15)
add_bw('S15','S15-D', range(33,41),'A', s15)
add_bw('S15','S15-E', range(43,51),'A', s15u)
add_bw('S15','S15-F', range(53,61),'A', s15u)
add_bw('S15','S15-G', range(63,71),'A', s15u)
add_survival('S15','S15-H', range(73,94),'A', [('3d Vaccine','B'),('3d PSLN-344','C'),('3d Vaccine+PSLN-344','D')])
add_bw('S15','S15-I', range(72,80),'H', [('3d Vaccine','I','O'),('3d PSLN-344','P','V'),('3d Vaccine+PSLN-344','W','AC')])
si = [('Naive+PSLN-212','I','O'),('Imprinting+PSLN-212','P','V'),('Naive+PSLN-344','W','AC'),('Imprinting+PSLN-344','AD','AJ')]
add_bw('S15','S15-J', range(83,91),'H', si)
add_bw('S15','S15-K', range(93,101),'H', si)
add_survival('S15','S15-L', range(103,131),'A', list(zip(g4, list('BCDE'))))
s15s = [('PSLN-212(Y)','I','O'),('Sham','P','V'),('PSLN-212','W','AC'),('PSLN-344','AD','AJ')]
add_bw('S15','S15-M', range(103,111),'H', s15s)
add_survival('S15','S15-N', range(134,162),'A', list(zip(g4, list('BCDE'))))
add_bw('S15','S15-O', range(134,142),'H', s15s)

C = pd.DataFrame(cont); S = pd.DataFrame(surv); B = pd.DataFrame(bw)
C.to_csv('/tmp/work/tidy/continuous.csv', index=False)
S.to_csv('/tmp/work/tidy/survival.csv', index=False)
B.to_csv('/tmp/work/tidy/bodyweight.csv', index=False)
print(len(C), len(S), len(B))
