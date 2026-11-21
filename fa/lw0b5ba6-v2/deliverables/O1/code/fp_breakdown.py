import openpyxl, collections, re
wb = openpyxl.load_workbook('/tmp/world/filesystem/psln_program_dataset.xlsx', data_only=True)
occ = collections.defaultdict(list)
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            v = c.value
            if isinstance(v, float):
                s = repr(v)
                if '.' in s and len(s.split('.')[1]) >= 4:
                    occ[round(v, 6)].append((ws.title, c.coordinate))
rep = {k: v for k, v in occ.items() if len(v) > 1}
cat = collections.Counter()
for k, v in rep.items():
    sheets = {s for s, _ in v}
    if sheets == {'S04'}: cat['derived (S04 Tfh:Tfr from identical Foxp3 values)'] += 1
    elif sheets == {'S09'} and all(re.match(r'[A-Z]+([3-9])$', c) for _, c in v): cat['within S09-A cytokine panel'] += 1
    else: cat['body-weight values shared across experiments/arms'] += 1
print(len(rep), dict(cat))
