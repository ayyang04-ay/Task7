"""Independent spot-check: recompute headline numbers straight from workbook cell addresses (no block registry, no tidy file)
and compare with the evidence ledger."""
import json, math
import numpy as np, openpyxl
from scipy import stats
wb = openpyxl.load_workbook('/tmp/world/filesystem/psln_program_dataset.xlsx', data_only=True)
N = json.load(open('../tables/numbers.json'))
def col(ws, c, r0, r1): return [wb[ws][f'{c}{r}'].value for r in range(r0, r1 + 1)]
def row(ws, r, c0, c1):
    from openpyxl.utils import column_index_from_string as ci
    return [wb[ws].cell(r, c).value for c in range(ci(c0), ci(c1) + 1)]
def surv(ws, c, r0, r1):
    f = [v for v in col(ws, c, r0, r1) if v is not None]; return f"{f.count(0)}/{len(f)}"
def gmt(v): v = [5 if x <= 0 else x for x in v]; return math.exp(sum(math.log(x) for x in v) / len(v))
checks = []
def chk(key, mine, tol=None):
    led = N[key]
    ok = (str(mine) == led) if tol is None else abs(float(led.replace(',', '').replace('%', '').replace('−', '-')) - mine) <= tol
    checks.append(ok); print(f"{'OK ' if ok else 'MISMATCH'} {key:28s} ledger={led:>10s}  independent={mine if tol is None else round(mine, 3)}")
# survival, core experiments (S06-A cols B-E rows 3-30; S06-B cols H-K; S06-C cols N-Q)
def pool(cols_):
    k = n = 0
    for ws, c, r0, r1 in cols_:
        a, b = surv(ws, c, r0, r1).split('/'); k += int(a); n += int(b)
    return f"{k}/{n}"
chk('rob_344', pool([('S06', 'D', 3, 30), ('S06', 'J', 3, 30), ('S06', 'P', 3, 30)]))
chk('rob_212', pool([('S06', 'C', 3, 30), ('S06', 'I', 3, 30), ('S06', 'O', 3, 30)]))
chk('rob_sham', pool([('S06', 'B', 3, 30), ('S06', 'H', 3, 30), ('S06', 'N', 3, 30)]))
chk('acute_344', pool([('S06', 'D', 3, 30), ('S06', 'J', 3, 30), ('S06', 'P', 3, 30), ('S06', 'D', 34, 61), ('S03', 'E', 17, 51), ('S03', 'J', 17, 46)]))
chk('acute_212', pool([('S06', 'C', 3, 30), ('S06', 'I', 3, 30), ('S06', 'O', 3, 30), ('S06', 'C', 34, 61), ('S03', 'D', 17, 51), ('S03', 'I', 17, 46)]))
chk('d60_344', pool([('S06', 'J', 34, 68), ('S06', 'P', 34, 68), ('S06', 'D', 71, 105)]))
chk('d60_untreated', pool([('S06', 'L', 34, 68), ('S06', 'R', 34, 68), ('S06', 'F', 71, 105)]))
chk('young_344', pool([('S09', 'C', 12, 35), ('S09', 'C', 39, 62), ('S09', 'C', 66, 88)]))
chk('S15H_3dPSLN344', surv('S15', 'C', 73, 93)); chk('S15H_3dVaccinePSLN344', surv('S15', 'D', 73, 93))
chk('m14_344_naive', pool([('S06', 'J', 71, 98), ('S06', 'P', 71, 98)])); chk('m14_212_naive', pool([('S06', 'H', 71, 98), ('S06', 'N', 71, 98)]))
# exact CI for 18/21
lo = stats.beta.ppf(0.025, 18, 4); hi = stats.beta.ppf(0.975, 19, 3); chk('rob_344_ci', f"{100*lo:.0f}–{100*hi:.0f}%")
# titres
chk('hai_h1_a344', gmt(col('S03', 'N', 3, 7)), 0.6); chk('hai_h1_a212', gmt(col('S03', 'M', 3, 7)), 0.6)
chk('hai_h1_fold', gmt(col('S03', 'N', 3, 7)) / gmt(col('S03', 'M', 3, 7)), 0.06)
chk('nab_h1_a344', gmt(col('S03', 'T', 3, 7)), 0.6); chk('igg_h1_fold', gmt(col('S03', 'D', 3, 7)) / gmt(col('S03', 'C', 3, 7)), 0.06)
# IgG2a/IgG1 recomputed: S13 A-C (IgG2a) / E-G (IgG1)
chk('ratio_h1_a344', float(np.mean(np.array(col('S13', 'B', 3, 7)) / np.array(col('S13', 'F', 3, 7)))), 0.006)
chk('ratio_h1_a212', float(np.mean(np.array(col('S13', 'A', 3, 7)) / np.array(col('S13', 'E', 3, 7)))), 0.006)
chk('ratio_h1_printed_a344', float(np.mean(col('S03', 'H', 3, 7))), 0.006)
# innate
chk('ifnb16_a344', float(np.mean(row('S01', 8, 'B', 'F'))), 0.06); chk('ifnb16_a212', float(np.mean(row('S01', 5, 'B', 'F'))), 0.06); chk('ifnb16_y212', float(np.mean(row('S01', 9, 'B', 'F'))), 0.06)
chk('gmcsf36_a344', float(np.mean(row('S02', 18, 'B', 'F'))), 0.06); chk('mono4_a344', float(np.mean(row('S01', 26, 'L', 'P'))), 0.06)
chk('cd40_a344', float(np.mean(col('S02', 'C', 10, 14))), 0.06); chk('trm_a344', float(np.mean(col('S05', 'C', 54, 58))), 0.06)
# safety
s08 = wb['S08']
from openpyxl.utils import column_index_from_string as ci
nad = lambda c0, c1: [min(v for v in (s08.cell(r, c).value for r in range(22, 27)) if v is not None) for c in range(ci(c0), ci(c1) + 1)]
chk('bw_nadir_a344', float(np.mean(nad('Q', 'U'))), 0.06); chk('bw_worst_a344', 100 - min(nad('Q', 'U')), 0.06); chk('bw_nadir_r848', float(np.mean(nad('V', 'Z'))), 0.06)
chk('c72_tnf_a344', 10 ** float(np.mean(row('S09', 8, 'AN', 'AP'))), 0.06); chk('c16_ccl2_a344', 10 ** float(np.mean(row('S09', 5, 'Q', 'S'))), 0.6)
chk('cns_tnf_a344', float(np.mean(col('S10', 'H', 3, 7))), 0.006)
# QC counts
a = [wb['S11'].cell(r, c).value for r in range(3, 8) for c in range(2, 22)]; b = [wb['S11'].cell(r, c).value for r in range(10, 15) for c in range(2, 22)]
chk('qc_s11_same', str(sum(x == y for x, y in zip(a, b))))
same = all(wb['S06'].cell(r, c).value == wb['S06'].cell(r + 31, c - 12).value for r in range(3, 31) for c in range(13, 18))
print('S06-C (M3:Q30) identical to S06-D (A34:E61):', same); checks.append(same)
print(f"\n{sum(checks)} of {len(checks)} independent checks agree with the ledger")
