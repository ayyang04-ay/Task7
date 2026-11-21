import openpyxl, numpy as np
ws = openpyxl.load_workbook('/tmp/world/filesystem/psln_program_dataset.xlsx', data_only=True)
def col(sh, c, r0, r1): return np.array([ws[sh][f'{c}{r}'].value for r in range(r0, r1 + 1)], float)
def row(sh, r, c0, c1):
    from openpyxl.utils import column_index_from_string as ci, get_column_letter as gl
    return np.array([ws[sh][f'{gl(i)}{r}'].value for i in range(ci(c0), ci(c1) + 1)], float)
gm = lambda v: 2 ** np.mean(np.log2(np.where(v <= 0, 5, v)))
checks = {
 'HAI CA09 GMT 344/212/Y': [round(gm(col('S03', c, 3, 7))) for c in 'NMO'],
 'HAI Aichi GMT 344/212/Y': [round(gm(col('S03', c, 10, 14))) for c in 'NMO'],
 'IgG CA09 GMT 344/212/Y/sham': [round(gm(col('S03', c, 3, 7))) for c in 'DCEA'],
 'Ifnb1 16h GM 344/212/Y': [round(gm(row('S01', r, 'B', 'F')), 1) for r in (8, 5, 9)],
 'Monocytes d4 mean 344/212/Y': [round(row('S01', 26, a, b).mean(), 1) for a, b in (('L', 'P'), ('G', 'K'), ('Q', 'U'))],
 'Lung TRM mean 344/212/Y': [round(col('S05', c, 54, 58).mean(), 2) for c in 'CBD'],
 'Gm-csf 36h GM 344/212': [round(gm(row('S02', 18, a, b)), 2) for a, b in (('B', 'F'), ('G', 'K'))],
}
for k, v in checks.items(): print(k, v)
# survival pooled from raw cells: count 0s (survivors) per arm column in each block
def surv(sh, daycol, r0, r1, c):
    e = [ws[sh][f'{c}{r}'].value for r in range(r0, r1 + 1)]; e = [x for x in e if x is not None]
    return sum(1 for x in e if x == 0), len(e)
blocks = {  # (sheet, r0, r1, {arm: col})
 'S03-I': ('S03', 17, 51, {'sham': 'B', '212': 'D', '344': 'E', 'Y': 'F'}), 'S03-J': ('S03', 17, 46, {'sham': 'H', '212': 'I', '344': 'J'}),
 'S06-A': ('S06', 3, 30, {'sham': 'B', '212': 'C', '344': 'D', 'Y': 'E'}), 'S06-B': ('S06', 3, 30, {'sham': 'H', '212': 'I', '344': 'J', 'Y': 'K'}),
 'S06-C': ('S06', 3, 30, {'sham': 'N', '212': 'O', '344': 'P', 'Y': 'Q'}), 'S06-E': ('S06', 34, 68, {'sham': 'H', '212': 'I', '344': 'J', 'Y': 'K'}),
 'S06-F': ('S06', 34, 68, {'sham': 'N', '212': 'O', '344': 'P', 'Y': 'Q'}), 'S06-G': ('S06', 71, 105, {'sham': 'B', '212': 'C', '344': 'D', 'Y': 'E'}),
 'S15-L': ('S15', 103, 130, {'sham': 'B', '212': 'C', '344': 'D', 'Y': 'E'}), 'S15-N': ('S15', 134, 161, {'sham': 'B', '212': 'C', '344': 'D', 'Y': 'E'})}
tot = {}
for b, (sh, r0, r1, arms) in blocks.items():
    for a, c in arms.items():
        s, n = surv(sh, None, r0, r1, c); tot.setdefault(a, [0, 0]); tot[a][0] += s; tot[a][1] += n
print('pooled aged arms (raw cells):', {a: f'{s}/{n}' for a, (s, n) in tot.items()})
imp = [surv('S06', None, 71, 98, c) for c in 'HIJKNOPQ']
print('imprint arms (212n,212i,344n,344i, x2):', imp)
