"""Independent check: re-read the source workbook by the cell ranges cited in the proposal and recompute the numbers."""
import openpyxl, re, os, numpy as np
from openpyxl.utils import range_boundaries, get_column_letter as L
wb = openpyxl.load_workbook(os.environ.get('PSLN_XLSX', '/tmp/world/filesystem/psln_program_dataset.xlsx'), data_only=True)
md = open(os.environ.get('PSLN_MD', '/tmp/work/report/proposal.md')).read()
def rng(ref):
    sh, r = ref.split('!'); c0, r0, c1, r1 = range_boundaries(r); ws = wb[sh]
    return [[ws.cell(row=i, column=j).value for j in range(c0, c1+1)] for i in range(r0, r1+1)]
ok = True
def check(label, got, want):
    global ok
    good = (got == want)
    ok &= good
    print(('OK   ' if good else 'FAIL ') + label + f": recomputed {got} | document {want}")

# ---- Table 1a: survival rectangles (header row first; first column = days) ----
t1 = re.search(r'\*\*Table 1a.*?\n\n(.*?)\n\n', md, re.S).group(1).splitlines()[2:]
for line in t1:
    cells = [c.strip().replace('**','') for c in line.strip('|').split('|')]
    blk, desc, sham, p212, p344, young, src, note = cells
    if '!' not in src: continue
    g = rng(src); hdr = [str(x).strip() if x is not None else None for x in g[0]]
    res = {}
    for j, name in enumerate(hdr):
        if j == 0 or name is None: continue
        ev = [row[j] for row in g[1:] if row[j] is not None]
        res[name] = f"{sum(1 for e in ev if e == 0)}/{len(ev)}"
    check(f"Table 1a {blk} [{src}]", (res.get('Sham'), res.get('PSLN-212'), res.get('PSLN-344'), res.get('PSLN-212(Y)')), (sham, p212, p344, young))

# ---- Table 1b rectangles ----
def surv(src):
    g = rng(src); hdr = [str(x).strip() if x is not None else None for x in g[0]]
    return {name: f"{sum(1 for row in g[1:] if row[j] == 0)}/{sum(1 for row in g[1:] if row[j] is not None)}" for j, name in enumerate(hdr) if j and name}
print(); 
for src in ['S15!A102:E130','S15!A133:E161','S15!A72:D93','S03!G16:J46','S06!G70:K98','S06!M70:Q98','S09!A11:D35','S09!A38:D62','S09!A65:D88','S13!R2:V30']:
    print('     Table 1b', src, surv(src))
r = surv('S03!G16:J46'); check('S03-J rows per group (10 each, PSLN-344 all alive)', (r['Sham'], r['PSLN-212'], r['PSLN-344']), ('1/10','3/10','10/10'))
check('S03!G46 (day for last PSLN-344 row) is blank', wb['S03']['G46'].value, None)

# ---- Table 2: recompute from cited rectangles ----
def gm(v): v = np.array([5.0 if x == 0 else x for x in v], float); return float(np.exp(np.log(v).mean()))
def mean(v): return float(np.mean(v))
def fmt(x):
    ax = abs(x); return f"{x:,.0f}" if ax >= 100 else f"{x:.1f}" if ax >= 1 else f"{x:.2f}"
t2 = re.search(r'\*\*Table 2.*?\n\n(.*?)\n\n', md, re.S).group(1).splitlines()[2:]
doc = {}
for line in t2:
    c = [x.strip().replace('**','') for x in line.strip('|').split('|')]
    doc[c[-1]] = c
print()
def cols(src, names, stat):   # groups in columns, header row above the rectangle's first data row
    sh, r = src.split('!'); c0, r0, c1, r1 = range_boundaries(r); ws = wb[sh]
    out = {}
    for j in range(c0, c1+1):
        h = str(ws.cell(row=r0-1, column=j).value).strip()
        out[h] = stat([ws.cell(row=i, column=j).value for i in range(r0, r1+1)])
    return [fmt(out[n]) for n in names]
def rows_(src, names, stat):  # groups in rows, label in the column left of the rectangle
    sh, r = src.split('!'); c0, r0, c1, r1 = range_boundaries(r); ws = wb[sh]
    out = {}
    for i in range(r0, r1+1):
        h = str(ws.cell(row=i, column=c0-1).value).strip()
        out[h] = stat([ws.cell(row=i, column=j).value for j in range(c0, c1+1)])
    return [fmt(out[n]) for n in names]
G4 = ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']
check('T2 Ifnb1 S01!B3:F9', rows_('S01!B3:F9', G4, gm), doc['S01!B3:F9'][1:5])
ws = wb['S01']; v = [[ws.cell(row=26, column=c).value for c in range(s, s+5)] for s in (2, 7, 12, 17)]
check('T2 monocytes d4 S01!B26:U26', [fmt(mean(x)) for x in v], doc['S01!B26:U26'][1:5])
check('T2 CCR7 DC S02!A3:D7', cols('S02!A3:D7', G4, mean), doc['S02!A3:D7'][1:5])
check('T2 CD86 S02!F10:I14', cols('S02!F10:I14', G4, mean), doc['S02!F10:I14'][1:5])
check('T2 GC B S03!L17:O21', cols('S03!L17:O21', G4, mean), doc['S03!L17:O21'][1:5])
check('T2 Tfh:Tfr S04!A15:D19', cols('S04!A15:D19', G4, gm), doc['S04!A15:D19'][1:5])
check('T2 IgG H1 S03!A3:E7', cols('S03!A3:E7', G4, gm), doc['S03!A3:E7'][1:5])
check('T2 HAI H1 S03!K3:O7', cols('S03!K3:O7', G4, gm), doc['S03!K3:O7'][1:5])
check('T2 HAI H3 S03!K10:O14', cols('S03!K10:O14', G4, gm), doc['S03!K10:O14'][1:5])
check('T2 neut H1 S03!Q3:U7', cols('S03!Q3:U7', G4, gm), doc['S03!Q3:U7'][1:5])
check('T2 Ki67 S05!A19:D23', cols('S05!A19:D23', G4, mean), doc['S05!A19:D23'][1:5])
check('T2 IFNg d14 S05!A33:D37', cols('S05!A33:D37', G4, mean), doc['S05!A33:D37'][1:5])
check('T2 IFNg d60 S05!A40:D44', cols('S05!A40:D44', G4, mean), doc['S05!A40:D44'][1:5])
check('T2 TRM S05!A54:D58', cols('S05!A54:D58', G4, mean), doc['S05!A54:D58'][1:5])
# IgG2a:IgG1 recomputed from S13!A3:G7 (A-C IgG2a; E-G IgG1)
ws = wb['S13']; ratio = {}
for k, (ca, cb) in zip(['PSLN-212','PSLN-344','PSLN-212(Y)'], [(1,5),(2,6),(3,7)]):
    ratio[k] = gm([ws.cell(row=i, column=ca).value / ws.cell(row=i, column=cb).value for i in range(3, 8)])
check('T2 IgG2a:IgG1 S13!A3:G7', [f"{ratio[k]:.2f}" for k in ['PSLN-212','PSLN-344','PSLN-212(Y)']], doc['S13!A3:G7'][2:5])
# ---- specific cited cells ----
print()
check('HAI PSLN-212 aged S03!M3:M7 range', (min(x[0] for x in rng('S03!M3:M7')), max(x[0] for x in rng('S03!M3:M7'))), (40, 80))
check('HAI PSLN-344 aged S03!N3:N7 range', (min(x[0] for x in rng('S03!N3:N7')), max(x[0] for x in rng('S03!N3:N7'))), (160, 640))
ee = rng('S08!M11:O11')[0]; check('EE PSLN-344 S08!M11:O11 mean/min/max', (round(np.mean(ee),1), round(min(ee),1), round(max(ee),1)), (54.8, 49.3, 59.4))
w = rng('S08!Q23:U23')[0]; check('S08-D PSLN-344 day 4 mean (S08!Q23:U23)', round(np.mean(w),1), 96.7)
w = rng('S08!AA23:AE23')[0]; check('S08-D Vaccine day 4 mean (S08!AA23:AE23)', round(np.mean(w),1), 98.8)
w = rng('S08!Q26:U26')[0]; check('S08-D PSLN-344 day 10 mean', round(np.mean(w),1), 99.8)
w = [x for x in rng('S08!V26:Z26')[0] if x is not None]; check('S08-D PSLN-212/R848 day 10 mean, n', (round(float(np.mean(w)),2), len(w), min(w)), (90.65, 4, 84.7))
t = rng('S10!F3:I7'); check('S10-A Tnf means PBS, Sham, PSLN-344, CT', [round(np.mean([r[j] for r in t]),2) for j in range(4)], [1.0, 1.32, 1.59, 3.5])
t = rng('S10!A3:D7'); check('S10-A Ifnb1 means', [round(np.mean([r[j] for r in t]),2) for j in range(4)], [1.0, 1.17, 1.32, 5.5])
# S09-A back-transforms (row 8 = Tnf; Q-S PSLN-344; T-V young; H-J PSLN-212)  and 72-h panel (AN-AP, AQ-AS, AE-AG)
ws = wb['S09']
def g9(row, c0): return round(10**np.mean([ws.cell(row=row, column=c).value for c in range(c0, c0+3)]), 1)
from openpyxl.utils import column_index_from_string as CI
check('S09-A Tnf 16h 344/212/young', (g9(8, CI('Q')), g9(8, CI('H')), g9(8, CI('T'))), (40.5, 15.7, 13.9))
check('S09-A Tnf 72h 344/212/young', (g9(8, CI('AN')), g9(8, CI('AE')), g9(8, CI('AQ'))), (8.4, 5.2, 0.5))
check('S09-A Il6 72h 344/212/young', (g9(4, CI('AN')), g9(4, CI('AE')), g9(4, CI('AQ'))), (7.2, 1.9, 3.1))
check('S09-A Ccl2 16h 344/212/young', (round(g9(5, CI('Q'))), g9(5, CI('H')), round(g9(5, CI('T')), -1)), (590, 7.6, 1390))
check('S09-A Tnf & Il10 16h R848 combo', (round(g9(8, CI('N'))), round(g9(9, CI('N')))), (202, 179))
print('\nALL CHECKS PASSED' if ok else '\nSOME CHECKS FAILED')
