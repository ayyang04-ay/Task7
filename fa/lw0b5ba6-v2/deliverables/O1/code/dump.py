import openpyxl, sys
from openpyxl.utils import get_column_letter
wb = openpyxl.load_workbook('psln_program_dataset.xlsx', data_only=False)
sheets = sys.argv[1:] if len(sys.argv)>1 else wb.sheetnames
for name in sheets:
    ws = wb[name]
    print('#'*20, name, ws.dimensions)
    for row in ws.iter_rows():
        cells = [(c.coordinate, c.value) for c in row if c.value is not None]
        if cells:
            print(' | '.join(f'{k}={v!r}' for k,v in cells))
