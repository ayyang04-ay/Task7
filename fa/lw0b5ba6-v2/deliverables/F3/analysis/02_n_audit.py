"""02_n_audit.py  -- stated n (label in workbook) vs. observations actually present, per block and group."""
import json
B = json.load(open('/tmp/work/parsed/parsed_blocks.json'))
rows = []
for bid, b in B.items():
    k = b['kind']
    if k in ('columns', 'rows'):
        for g in b['order']:
            rows.append((bid, g, b['stated_n'], str(len(b['groups'][g]))))
    elif k in ('wide_time', 'wide_analyte'):
        for g in b['order']:
            ns = [sum(1 for x in v if x is not None) for v in b['groups'][g].values()]
            rows.append((bid, g, b['stated_n'], '/'.join(map(str, ns))))
    elif k == 'survival':
        for g in b['order']:
            a = b['groups'][g]
            nd = sum(1 for x in a if x['event'] == 1); nc = sum(1 for x in a if x['event'] == 0)
            miss = sum(1 for x in a if x['day'] is None)
            rows.append((bid, g, b['stated_n'], f"{len(a)} (died {nd}, alive at end {nc}" + (f", MISSING DAY VALUE in {miss} row" if miss else "") + ")"))
import csv
with open('/tmp/work/parsed/n_audit.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['block', 'group', 'stated_n', 'observed']); w.writerows(rows)
cur = None
for r in rows:
    if r[0] != cur:
        cur = r[0]; print(f"\n{cur}  [stated n={r[2]}]")
    print(f"    {r[1]:<28} {r[3]}")
