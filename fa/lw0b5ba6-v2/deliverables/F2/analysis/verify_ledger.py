"""Independent check: re-read the cell ranges quoted in the ledger straight from the source workbook (no use of blocks.py)
and recompute means / geometric means / survivor counts."""
import openpyxl, numpy as np, pandas as pd, re, os
wb = openpyxl.load_workbook(os.environ.get('PSLN_XLSX', '/tmp/world/filesystem/psln_program_dataset.xlsx'), data_only=True)
L = pd.read_csv('evidence_ledger.csv')
def read_range(ref):
    sheet, rng = ref.split('!')
    cells = wb[sheet][rng]
    vals = []
    if not isinstance(cells, tuple): cells = ((cells,),)
    for row in cells:
        for c in (row if isinstance(row, tuple) else (row,)):
            if isinstance(c.value, (int, float)): vals.append(float(c.value))
    return vals
ok = bad = skipped = 0; problems = []
for r in L.itertuples():
    cells = r.Cells if isinstance(r.Cells, str) else ''
    m = r.Method if isinstance(r.Method, str) else ''
    if not re.fullmatch(r'S\d\d![A-Z]+\d+:[A-Z]+\d+', cells): skipped += 1; continue
    v = read_range(cells)
    try: raw = eval(r.Raw, {'np': np, 'nan': float('nan')})
    except Exception: skipped += 1; continue
    if m == 'mean' or m.startswith('mean;') or m.startswith('mean (') or m == 'mean, SD':
        calc = np.mean(v); tgt = raw if np.isscalar(raw) else None
    elif m == 'geometric mean':
        vv = [x if x > 0 else 5.0 for x in v]; calc = float(np.exp(np.mean(np.log(vv)))); tgt = raw
    elif m == 'Count' and isinstance(raw, tuple) and len(raw) == 2:
        calc = (sum(1 for x in v if x == 0), len(v)); tgt = raw       # survivors = status 0
    else: skipped += 1; continue
    if tgt is None: skipped += 1; continue
    good = (calc == tgt) if isinstance(tgt, tuple) else abs(calc - float(tgt)) < 1e-6 * max(1, abs(float(tgt)))
    if good: ok += 1
    else: bad += 1; problems.append((r.ID, r.Key, cells, m, calc, tgt))
print('re-derived from raw cells and matched:', ok, '| mismatched:', bad, '| not of a simple re-derivable type:', skipped)
for p in problems: print('  MISMATCH', p)
