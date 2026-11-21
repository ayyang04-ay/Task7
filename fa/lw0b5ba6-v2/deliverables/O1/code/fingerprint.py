import openpyxl, re, collections
from openpyxl.utils import get_column_letter as gl
wb = openpyxl.load_workbook('/tmp/world/filesystem/psln_program_dataset.xlsx', data_only=True)
occ = collections.defaultdict(list)
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            v = c.value
            if isinstance(v, float):
                s = repr(v)
                if '.' in s and len(s.split('.')[1]) >= 4:
                    occ[round(v, 6)].append(f'{ws.title}!{c.coordinate}')
rep = {k: v for k, v in occ.items() if len(v) > 1}
print('high-precision values occurring >1 time:', len(rep))
for k, v in sorted(rep.items(), key=lambda x: x[1][0]):
    print(k, v)
