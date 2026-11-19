import openpyxl, pandas as pd
wb = openpyxl.load_workbook('/tmp/world/filesystem/psln_program_dataset.xlsx', data_only=True)
df = pd.read_csv('/tmp/work/tidy.csv')
parsed = set(df.cell)
# axis columns (days / dose / time) per sheet
axis = {'S01':['A'], 'S02':['A'], 'S03':['A','G'], 'S05':['A'], 'S06':['A','G','M'], 'S07':['A'], 'S08':['A'],
        'S09':['A','F'], 'S11':['A'], 'S13':['A','R'], 'S15':['A','H']}
leftover = []
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value,(int,float)) and not isinstance(c.value,bool):
                key = f'{ws.title}!{c.coordinate}'
                if key in parsed: continue
                if c.column_letter in axis.get(ws.title, []): continue
                leftover.append((key, c.value))
print(len(leftover)); print(leftover[:50])
