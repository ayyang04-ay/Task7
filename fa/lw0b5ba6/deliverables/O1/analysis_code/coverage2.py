import openpyxl, pandas as pd
wb = openpyxl.load_workbook('/tmp/world/filesystem/psln_program_dataset.xlsx', data_only=True)
df = pd.read_csv('/tmp/work/tidy.csv')
parsed = set(df.cell)
axis = {'S01':['A'], 'S02':['A'], 'S03':['A','G'], 'S05':['A'], 'S06':['A','G','M'], 'S07':['A'], 'S08':['A'],
        'S09':['A','F'], 'S11':['A'], 'S13':['A','R'], 'S15':['A','H']}
from collections import defaultdict
d = defaultdict(list)
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value,(int,float)) and c.column_letter in axis.get(ws.title,[]):
                key = f'{ws.title}!{c.coordinate}'
                if key not in parsed:
                    d[(ws.title,c.column_letter)].append(c.row)
for k,v in d.items():
    # compress row ranges
    rng=[]; s=v[0]; p=v[0]
    for x in v[1:]:
        if x==p+1: p=x; continue
        rng.append((s,p)); s=p=x
    rng.append((s,p))
    print(k, rng)
