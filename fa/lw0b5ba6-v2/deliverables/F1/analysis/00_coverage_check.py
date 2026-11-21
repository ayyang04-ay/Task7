"""Verify that every numeric cell of the workbook is accounted for by the block registry."""
import openpyxl, numbers
from openpyxl.utils import get_column_letter as L, column_index_from_string as C
import psln_blocks as P

wb = P.wb()
used = {s: set() for s in wb.sheetnames}
for bid, b in P.BLOCKS.items():
    df = P.load(bid)
    for c in df['cell']:
        used[b['sheet']].add(c)
    # x / day columns
    if b['kind'] in ('tc', 'bw') and b.get('xcol'):
        for r in range(b['rows'][0], b['rows'][1] + 1):
            used[b['sheet']].add(f"{b['xcol']}{r}")
    if b['kind'] == 'surv':
        for r in range(b['rows'][0], b['rows'][1] + 1):
            used[b['sheet']].add(f"{b['daycol']}{r}")
tot = 0; unused = {}
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, numbers.Number):
                tot += 1
                if c.coordinate not in used[ws.title]:
                    unused.setdefault(ws.title, []).append((c.coordinate, c.value))
print('numeric cells in workbook:', tot)
for s, lst in unused.items():
    print(s, len(lst), lst)
