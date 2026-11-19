#!/usr/bin/env python
"""
Step 1 - Extract every data block of psln_program_dataset.xlsx into tidy (long) tables.

Every value keeps its sheet + cell address so that any number quoted in the proposal can be
traced back to the workbook.  Block geometry was transcribed by hand from the workbook and the
annotation PDF; nothing is inferred silently.  Labels are kept "as printed".

Outputs (in /tmp/outputs/analysis/tidy):
  continuous.csv   one row per measured value (block, panel, group, x, replicate, value, cell)
  survival.csv     one row per animal in time-to-event blocks (block, group, time, event, cell)
  bodyweight.csv   one row per animal x day in body-weight blocks (block, group, animal, day, value, cell)
"""
import openpyxl, csv, os, sys
from openpyxl.utils import get_column_letter as L, column_index_from_string as C

SRC = "/tmp/world/filesystem/psln_program_dataset.xlsx"
OUT = "/tmp/outputs/analysis/tidy"
os.makedirs(OUT, exist_ok=True)
wb = openpyxl.load_workbook(SRC, data_only=True)

cont, surv, bw = [], [], []

def cols(a, b):
    return [L(i) for i in range(C(a), C(b) + 1)]

def num(ws, addr):
    v = ws[addr].value
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(str(v).strip())
    except ValueError:
        return None

# ---------------------------------------------------------------- continuous helpers
def col_block(sheet, block, panel, groups, rows, x=""):
    """groups: list of (label, column).  Each column = one group, rows = replicates."""
    ws = wb[sheet]
    for g, c in groups:
        for i, r in enumerate(rows, 1):
            v = num(ws, f"{c}{r}")
            if v is not None:
                cont.append(dict(sheet=sheet, block=block, panel=panel, group=g, x=x, rep=i, value=v, cell=f"{c}{r}"))

def row_block(sheet, block, panel, group, row, columns, x=""):
    """one row, replicates across columns"""
    ws = wb[sheet]
    for i, c in enumerate(columns, 1):
        v = num(ws, f"{c}{row}")
        if v is not None:
            cont.append(dict(sheet=sheet, block=block, panel=panel, group=group, x=x, rep=i, value=v, cell=f"{c}{row}"))

def grid_block(sheet, block, panel, groups, xrows):
    """groups: list of (label, first_col, last_col); xrows: list of (x_label, row)"""
    for g, a, b in groups:
        for x, r in xrows:
            row_block(sheet, block, panel, g, r, cols(a, b), x=x)

def surv_block(sheet, block, daycol, groups, r0, r1):
    """groups: list of (label, column holding 1/0).  One row per animal."""
    ws = wb[sheet]
    for g, c in groups:
        for r in range(r0, r1 + 1):
            s = ws[f"{c}{r}"].value
            if s is None:
                continue
            t = num(ws, f"{daycol}{r}")
            surv.append(dict(sheet=sheet, block=block, group=g, time=t, event=int(s), cell=f"{daycol}{r}/{c}{r}"))

def bw_block(sheet, block, daycol, groups, r0, r1):
    """groups: list of (label, first_col, last_col); rows r0..r1 = days"""
    ws = wb[sheet]
    for g, a, b in groups:
        for k, c in enumerate(cols(a, b), 1):
            for r in range(r0, r1 + 1):
                d = num(ws, f"{daycol}{r}")
                v = num(ws, f"{c}{r}")
                bw.append(dict(sheet=sheet, block=block, group=g, animal=f"{g}#{k}", col=c, day=d,
                               value=v, cell=f"{c}{r}"))

G4 = lambda cs: list(zip(["Sham", "PSLN-212", "PSLN-344", "PSLN-212(Y)"], cs))
G5 = lambda cs: list(zip(["Sham", "CMP-204", "PSLN-212", "PSLN-344", "PSLN-212(Y)"], cs))

# =============================================================== S01
for r, g in zip(range(3, 11), ["Sham", "CMP-204", "PSLN-212", "PSLN-R848", "PSLN-212/R848", "PSLN-344", "PSLN-212(Y)", "PSLN-344(Y)"]):
    row_block("S01", "S01-A", "Ifnb1 16h", g, r, cols("B", "F"), x="16h")
    row_block("S01", "S01-A", "Ifnb1 72h", g, r, cols("H", "L"), x="72h")
for r, g in zip(range(14, 18), ["AECII/PSLN-SRB", "AECI/PSLN-SRB", "AECII/FreeSRB", "AECI/FreeSRB"]):
    row_block("S01", "S01-B", "", g, r, cols("B", "F"))
for r, g in zip((20, 21), ["WT", "SPA/D"]):
    row_block("S01", "S01-C", "", g, r, cols("B", "E"))
days5 = [("0", 0), ("2", 1), ("4", 2), ("6", 3), ("8", 4)]
grid_block("S01", "S01-D", "", [("Sham", "B", "F"), ("PSLN-212", "G", "K"), ("PSLN-344", "L", "P"), ("PSLN-212(Y)", "Q", "U")],
           [(d, 24 + i) for d, i in days5])
g5w = [("Sham", "B", "F"), ("PSLN-212", "G", "K"), ("PSLN-344", "L", "P"), ("PSLN-212(Y)", "Q", "U"), ("PSLN-344(Y)", "V", "Z")]
grid_block("S01", "S01-E", "", g5w, [(d, 30 + i) for d, i in days5])
grid_block("S01", "S01-F", "", g5w, [("72h", 36)])
grid_block("S01", "S01-G", "", g5w, [("72h", 38)])

# =============================================================== S02
col_block("S02", "S02-A", "", G4("ABCD"), range(3, 8))
col_block("S02", "S02-B", "", G4("FGHI"), range(3, 8))
g2c = list(zip(["PSLN-212", "PSLN-344", "PSLN-212(Y)", "PTX", "PSLN-344(Y)"], "KLMNO"))
col_block("S02", "S02-C", "", g2c, range(3, 8))
col_block("S02", "S02-D CD40", "", G4("ABCD"), range(10, 15))
col_block("S02", "S02-D CD86", "", G4("FGHI"), range(10, 15))
col_block("S02", "S02-E", "", g2c, range(10, 15))
grid_block("S02", "S02-F", "", [("PSLN-344", "B", "F"), ("PSLN-212", "G", "K"), ("Sham", "L", "P")],
           [("16h", 17), ("36h", 18), ("72h", 19)])
col_block("S02", "S02-G", "", list(zip(["GM-CSF", "PSLN-212", "PSLN-212+GM-CSF"], "BCD")), range(22, 27))
col_block("S02", "S02-H", "", list(zip(["WT w/o cDC", "WT w/ cDC", "IFN w/o cDC", "IFN w/ cDC", "GMCSF"], "BCDEF")), range(30, 35))
col_block("S02", "S02-I", "", list(zip(["PSLN-344(Y)", "PSLN-344(Y)+INCB3344"], "HI")), range(30, 35))

# =============================================================== S03
g3r = list(zip(["PSLN-212", "PSLN-344", "PSLN-212(Y)"], "GHI"))
col_block("S03", "S03-A", "IgG CA09 d14", G5("ABCDE"), range(3, 8))
col_block("S03", "S03-B", "IgG2a/IgG1 CA09 d14 (as printed)", g3r, range(3, 8))
col_block("S03", "S03-C", "HAI CA09 d14", G5("KLMNO"), range(3, 8))
col_block("S03", "S03-D", "NAb CA09 d14", G5("QRSTU"), range(3, 8))
col_block("S03", "S03-E", "IgG Aichi d14", G5("ABCDE"), range(10, 15))
col_block("S03", "S03-F", "IgG2a/IgG1 Aichi d14 (as printed)", g3r, range(10, 15))
col_block("S03", "S03-G", "HAI Aichi d14", G5("KLMNO"), range(10, 15))
col_block("S03", "S03-H", "NAb Aichi d14", G5("QRSTU"), range(10, 15))
surv_block("S03", "S03-I", "A", G5("BCDEF"), 17, 51)
surv_block("S03", "S03-J", "G", list(zip(["Sham", "PSLN-212", "PSLN-344"], "HIJ")), 17, 46)
col_block("S03", "S03-K", "", G4("LMNO"), range(17, 22))
for r, g in zip((26, 27, 28), ["Sham", "PSLN-212", "PSLN-344"]):
    row_block("S03", "S03-L", "Aicda", g, r, cols("L", "N"), x="Aicda")
    row_block("S03", "S03-L", "E47", g, r, cols("O", "Q"), x="E47")

# =============================================================== S04
for r, g in zip(range(2, 6), ["Sham", "PSLN-212", "PSLN-344", "PSLN-212(Y)"]):
    row_block("S04", "S04-A", "ICOS-low Tfh", g, r, cols("B", "F"), x="ICOS-")
    row_block("S04", "S04-A", "ICOS-high Tfh", g, r, cols("G", "K"), x="ICOS+")
col_block("S04", "S04-B Foxp3+ in CXCR5+", "", G4("ABCD"), range(8, 13))
col_block("S04", "S04-B Tfh:Tfr", "", G4("ABCD"), range(15, 20))
col_block("S04", "S04-C", "", G4("ABCD"), range(22, 27))
col_block("S04", "S04-D", "", G4("ABCD"), range(29, 32))

# =============================================================== S05
g5t = [("PSLN-212", "B", "C"), ("PSLN-344", "E", "F"), ("PSLN-212Y", "H", "I")]
grid_block("S05", "S05-A", "Lung", g5t, [("3", 3), ("5", 4), ("7", 5)])
grid_block("S05", "S05-B", "MLN", g5t, [("3", 8), ("5", 9), ("7", 10)])
col_block("S05", "S05-C", "", list(zip(["Lung", "Lung+PTX", "MLN", "MLN+PTX"], "ABCD")), range(13, 16))
for blk, r0 in [("S05-D", 19), ("S05-E", 26), ("S05-F", 33), ("S05-G", 40), ("S05-H", 47), ("S05-I", 54)]:
    col_block("S05", blk, "", G4("ABCD"), range(r0, r0 + 5))

# =============================================================== S06 (time to event)
surv_block("S06", "S06-A", "A", G4("BCDE"), 3, 30)
surv_block("S06", "S06-B", "G", G4("HIJK"), 3, 30)
surv_block("S06", "S06-C", "M", G4("NOPQ"), 3, 30)
surv_block("S06", "S06-D", "A", G4("BCDE"), 34, 61)
g5u = lambda cs: list(zip(["Sham", "PSLN-212", "PSLN-344", "PSLN-212(Y)", "Untreated"], cs))
surv_block("S06", "S06-E", "G", g5u("HIJKL"), 34, 68)
surv_block("S06", "S06-F", "M", g5u("NOPQR"), 34, 68)
surv_block("S06", "S06-G", "A", g5u("BCDEF"), 71, 105)
gimp = lambda cs: list(zip(["Naive+PSLN-212", "Imprinting+PSLN-212", "Naive+PSLN-344", "Imprinting+PSLN-344"], cs))
# The two blocks below are printed "S06-E" and "S06-F" a second time (rows 69-98); we suffix them.
surv_block("S06", "S06-E(2) imprinting/PR8", "G", gimp("HIJK"), 71, 98)
surv_block("S06", "S06-F(2) imprinting/Perth", "M", gimp("NOPQ"), 71, 98)

# =============================================================== S07
grid_block("S07", "S07-A", "", [("PSLN-212", "B", "D"), ("PSLN-344", "E", "G")],
           [("0", 3), ("2", 4), ("5", 5), ("10", 6), ("30", 7)])
col_block("S07", "S07-B", "CD11b+Ly6C+ monocytes", list(zip(["PSLN-344", "PSLN-344+INCB3344"], "BC")), range(10, 15), x="Mono")
col_block("S07", "S07-B", "Ly6C+ macrophages", list(zip(["PSLN-344", "PSLN-344+INCB3344"], "EF")), range(10, 15), x="Mac")
col_block("S07", "S07-C", "", [("Ly6C-CD206+ MPhi [col B]", "B"), ("Ly6C-CD206+ MPhi [col C]", "C")], range(16, 21))

# =============================================================== S08
grid_block("S08", "S08-A", "", [("CMP-204", "B", "D"), ("PSLN-212", "E", "G"), ("PSLN-344", "H", "J"), ("PSLN-344/R848", "K", "M")],
           [("1", 3), ("5", 4), ("10", 5), ("20", 6), ("40", 7)])
for g, a, b in [("CMP-204", "A", "C"), ("PSLN-212", "D", "F"), ("PSLN-R848", "G", "I"), ("PSLN-212/R848", "J", "L"), ("PSLN-344", "M", "O")]:
    row_block("S08", "S08-B", "", g, 11, cols(a, b))
col_block("S08", "S08-C", "", list(zip(["AECII-PSLN-SRB", "AECII-PSLN-344-SRB", "AECI-PSLN-SRB", "AECI-PSLN-344-SRB"], "ABCD")), range(14, 19))
bw_block("S08", "S08-D", "A", [("PSLN-212(Y)", "B", "F"), ("CMP-204", "G", "K"), ("PSLN-212", "L", "P"), ("PSLN-344", "Q", "U"),
                               ("PSLN-212/R848", "V", "Z"), ("Vaccine", "AA", "AE")], 21, 26)

# =============================================================== S09
g9 = ["PBS", "CMP-204", "PSLN-212", "PSLN-R848", "PSLN-212/R848", "PSLN-344", "PSLN-212(y)"]
p1 = [("B", "D"), ("E", "G"), ("H", "J"), ("K", "M"), ("N", "P"), ("Q", "S"), ("T", "V")]
p2 = [("Y", "AA"), ("AB", "AD"), ("AE", "AG"), ("AH", "AJ"), ("AK", "AM"), ("AN", "AP"), ("AQ", "AS")]
for r, an in zip(range(3, 10), ["Ifnb1", "Il6", "Ccl2", "Ccl3", "Ccl5", "Tnf", "Il10"]):
    for g, (a, b) in zip(g9, p1):
        row_block("S09", "S09-A", "panel1 (cols A-V, printed 16h)", g, r, cols(a, b), x=an)
    for g, (a, b) in zip(g9, p2):
        row_block("S09", "S09-A", "panel2 (cols X-AS, printed 16h)", g, r, cols(a, b), x=an)
g9s = list(zip(["Sham", "PSLN-344Y", "PSLN-212Y"], "BCD"))
g9w = [("PSLN-212Y", "G", "N"), ("Sham", "O", "V"), ("PSLN-344Y", "W", "AD")]
surv_block("S09", "S09-B", "A", g9s, 12, 35); bw_block("S09", "S09-C", "F", g9w, 12, 19)
surv_block("S09", "S09-D", "A", g9s, 39, 62); bw_block("S09", "S09-E", "F", g9w, 39, 46)
surv_block("S09", "S09-F", "A", g9s, 66, 88); bw_block("S09", "S09-G", "F", g9w, 66, 73)

# =============================================================== S10
g10 = ["PBS", "Sham", "PSLN-344", "CT"]
col_block("S10", "S10-A", "Ifnb1", list(zip(g10, "ABCD")), range(3, 8), x="Ifnb1")
col_block("S10", "S10-A", "Tnf", list(zip(g10, "FGHI")), range(3, 8), x="Tnf")
col_block("S10", "S10-A", "Isg15", list(zip(g10, "KLMN")), range(3, 8), x="Isg15")

# =============================================================== S11
g11 = [("Vaccine", "B", "F"), ("PSLN-212", "G", "K"), ("PSLN-344", "L", "P"), ("PSLN-212(Y)", "Q", "U")]
grid_block("S11", "S11-A", "", g11, [(d, 3 + i) for d, i in days5])
grid_block("S11", "S11-B", "", g11, [(d, 10 + i) for d, i in days5])
col_block("S11", "S11-C", "", list(zip(["CBX+", "CBX-"], "AB")), range(17, 22))
grid_block("S11", "S11-D", "", g11, [(d, 24 + i) for d, i in days5])
col_block("S11", "S11-E", "", G4("ABCD"), range(31, 36))

# =============================================================== S12
col_block("S12", "S12-A", "", list(zip(["WT to WT", "IFNAR-/- to WT"], "AB")), range(3, 6))

# =============================================================== S13
g3 = lambda cs: list(zip(["PSLN-212", "PSLN-344", "PSLN-212(Y)"], cs))
col_block("S13", "S13-A", "IgG2a CA09 d14", g3("ABC"), range(3, 8))
col_block("S13", "S13-B", "IgG1 CA09 d14", g3("EFG"), range(3, 8))
col_block("S13", "S13-C", "IgG2a Aichi d14", g3("IJK"), range(3, 8))
col_block("S13", "S13-D", "IgG1 Aichi d14", g3("MNO"), range(3, 8))
surv_block("S13", "S13-E", "R", list(zip(["Naive", "Sham", "CMP-204(Y)", "PSLN-344(Y)"], "STUV")), 3, 30)
bw_block("S13", "S13-F", "A", [("PSLN-212(Y)", "B", "H"), ("Sham", "I", "O"), ("PSLN-212", "P", "V"), ("PSLN-344", "W", "AC"), ("Naive", "AD", "AJ")], 33, 40)
bw_block("S13", "S13-G", "A", [("PSLN-344", "B", "K"), ("Sham", "L", "U"), ("Naive", "V", "AE")], 43, 50)
col_block("S13", "S13-H", "", G4("ABCD"), range(53, 58))
col_block("S13", "S13-I", "IgG CA09 d28 (boost d14)", G5("FGHIJ"), range(53, 58))
col_block("S13", "S13-J", "IgG Aichi d28 (boost d14)", G5("LMNOP"), range(53, 58))

# =============================================================== S14
col_block("S14", "S14-A H1N1", "", G4("ABCD"), range(3, 8))
col_block("S14", "S14-A H3N2", "", G4("FGHI"), range(3, 8))

# =============================================================== S15
g15 = [("PSLN-212(Y)", "B", "H"), ("Sham", "I", "O"), ("PSLN-212", "P", "V"), ("PSLN-344", "W", "AC")]
g15u = g15 + [("Untreated", "AD", "AJ")]
bw_block("S15", "S15-A", "A", g15, 3, 10)
bw_block("S15", "S15-B", "A", g15, 13, 20)
bw_block("S15", "S15-C", "A", g15, 23, 30)
bw_block("S15", "S15-D", "A", g15, 33, 40)
bw_block("S15", "S15-E", "A", g15u, 43, 50)
bw_block("S15", "S15-F", "A", g15u, 53, 60)
bw_block("S15", "S15-G", "A", g15u, 63, 70)
surv_block("S15", "S15-H", "A", list(zip(["3d Vaccine", "3d PSLN-344", "3d Vaccine+PSLN-344"], "BCD")), 73, 93)
bw_block("S15", "S15-I", "H", [("3d Vaccine", "I", "O"), ("3d PSLN-344", "P", "V"), ("3d Vaccine+PSLN-344", "W", "AC")], 72, 79)
gimpw = [("Naive+PSLN-212", "I", "O"), ("Imprinting+PSLN-212", "P", "V"), ("Naive+PSLN-344", "W", "AC"), ("Imprinting+PSLN-344", "AD", "AJ")]
bw_block("S15", "S15-J", "H", gimpw, 83, 90)
bw_block("S15", "S15-K", "H", gimpw, 93, 100)
g15s = list(zip(["Sham", "PSLN-212", "PSLN-344", "PSLN-212(Y)"], "BCDE"))
g15m = [("PSLN-212(Y)", "I", "O"), ("Sham", "P", "V"), ("PSLN-212", "W", "AC"), ("PSLN-344", "AD", "AJ")]
surv_block("S15", "S15-L", "A", g15s, 103, 130); bw_block("S15", "S15-M", "H", g15m, 103, 110)
surv_block("S15", "S15-N", "A", g15s, 134, 161); bw_block("S15", "S15-O", "H", g15m, 134, 141)

def dump(name, rows):
    keys = list(rows[0].keys())
    with open(os.path.join(OUT, name), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
    print(f"{name}: {len(rows)} rows")

dump("continuous.csv", cont); dump("survival.csv", surv); dump("bodyweight.csv", bw)

# ---------------------------------------------------------------- completeness audit:
# every numeric cell in the workbook must have been captured by exactly one block (or be a known axis/orphan cell)
captured = {}
for r in cont: captured.setdefault((r["sheet"], r["cell"]), []).append(r["block"])
for r in surv:
    a, b = r["cell"].split("/")
    captured.setdefault((r["sheet"], a), []).append(r["block"]); captured.setdefault((r["sheet"], b), []).append(r["block"])
for r in bw:
    if r["value"] is not None: captured.setdefault((r["sheet"], r["cell"]), []).append(r["block"])
missing, multi = [], []
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, (int, float)):
                k = (ws.title, c.coordinate)
                if k not in captured: missing.append(k)
                elif len(set(captured[k])) > 1: multi.append((k, captured[k]))
# axis cells (day / dose columns of grid & body-weight blocks) are expected to be "missing"
with open(os.path.join(OUT, "uncaptured_numeric_cells.txt"), "w") as f:
    for k in missing: f.write(f"{k[0]}!{k[1]} = {wb[k[0]][k[1]].value}\n")
print("numeric cells not captured as data (axis labels + orphan region):", len(missing))
print("cells captured by >1 block:", len(multi))
