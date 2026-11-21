import openpyxl, sys
from openpyxl.utils import get_column_letter
wb = openpyxl.load_workbook('/tmp/world/filesystem/psln_program_dataset.xlsx', data_only=False)
sheet = sys.argv[1]
ws = wb[sheet]
for row in ws.iter_rows():
    cells = [(c.coordinate, c.value) for c in row if c.value is not None]
    if cells:
        print(' | '.join(f'{k}={v!r}' for k,v in cells))
# comments
for row in ws.iter_rows():
    for c in row:
        if c.comment:
            print('COMMENT', c.coordinate, c.comment.text)
