import openpyxl, numpy as np
wb = openpyxl.load_workbook('/tmp/world/filesystem/psln_program_dataset.xlsx', data_only=True)
def rng(ws, a):
    return [c.value for row in wb[ws][a] for c in row if c.value is not None]
gm = lambda v: float(np.exp(np.mean(np.log(v))))
print('S03-A PSLN-344 GMT', round(gm(rng('S03','D3:D7'))), ' PSLN-212', round(gm(rng('S03','C3:C7'))), ' young', round(gm(rng('S03','E3:E7'))))
print('S01-A 16h PSLN-344 GM', round(gm(rng('S01','B8:F8')),1), ' PSLN-212', round(gm(rng('S01','B5:F5')),1), ' 212Y', round(gm(rng('S01','B9:F9')),1))
hai = lambda v: gm([5 if x<10 else x for x in v])
print('S03-C HAI PSLN-344', round(hai(rng('S03','N3:N7'))), ' PSLN-212', round(hai(rng('S03','M3:M7'))), ' Sham', round(hai(rng('S03','K3:K7')),1))
# pooled survival counts from S06 + S15-L/N directly
ws = wb['S06']
def surv(ws, daycol, gcol, r1, r2):
    ev = [ws[f'{gcol}{r}'].value for r in range(r1,r2+1) if ws[f'{gcol}{r}'].value is not None]
    return sum(1 for e in ev if e==0), len(ev)
tot = {'Sham':[0,0],'PSLN-212':[0,0],'PSLN-344':[0,0],'PSLN-212(Y)':[0,0]}
layout = [('S06','A','BCDE',3,30),('S06','G','HIJK',3,30),('S06','M','NOPQ',3,30),('S06','A','BCDE',34,61),('S06','G','HIJK',34,68),('S06','M','NOPQ',34,68),('S06','A','BCDE',71,105),('S15','A','BCDE',103,130),('S15','A','BCDE',134,161)]
for sh, d, cols, r1, r2 in layout:
    for g, col in zip(tot, cols):
        s, n = surv(wb[sh], d, col, r1, r2); tot[g][0]+=s; tot[g][1]+=n
print('pooled survivors/total', tot)
print('S05-I means', [round(np.mean(rng('S05',f'{c}54:{c}58')),2) for c in 'ABCD'])
print('S02-D CD40 means', [round(np.mean(rng('S02',f'{c}10:{c}14')),2) for c in 'ABCD'])
