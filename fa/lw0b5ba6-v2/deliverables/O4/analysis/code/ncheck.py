import pandas as pd, re
vals = pd.read_csv('values.csv'); surv = pd.read_csv('survival.csv'); bw = pd.read_csv('bw.csv')
stated = {
 'S01-A_16h':5,'S01-A_72h':5,'S01-B':5,'S01-C':4,'S01-D':5,'S01-E':5,'S01-F':5,'S01-G':5,
 'S02-A':5,'S02-B':5,'S02-C':5,'S02-D_CD40':5,'S02-D_CD86':5,'S02-E':5,'S02-F':5,'S02-G':5,'S02-H':5,'S02-I':5,
 'S03-A':5,'S03-B':5,'S03-C':5,'S03-D':5,'S03-E':5,'S03-F':5,'S03-G':5,'S03-H':5,'S03-K':5,'S03-L_Aicda':3,'S03-L_E47':3,
 'S04-A_ICOSlo':5,'S04-A_ICOShi':5,'S04-B_Foxp3':5,'S04-B_TfhTfr':5,'S04-C':5,'S04-D':3,
 'S05-A':3,'S05-B':3,'S05-C':3,'S05-D':5,'S05-E':5,'S05-F':5,'S05-G':5,'S05-H':5,'S05-I':5,
 'S07-A':3,'S07-B':5,'S07-C':5,'S08-A':3,'S08-B':3,'S08-C':5,'S09-A_blk1(cols A-U)':3,'S09-A_blk2(cols X-AS)':3,
 'S10-A_Ifnb1':5,'S10-A_Tnf':5,'S10-A_Isg15':5,'S11-A':5,'S11-B':5,'S11-C':5,'S11-D':5,'S11-E':5,'S12-A':3,
 'S13-A':5,'S13-B':5,'S13-C':5,'S13-D':5,'S13-H':5,'S13-I':5,'S13-J':5,'S14-A_H1N1':5,'S14-A_H3N2':5}
rows=[]
for b,n in stated.items():
    d = vals[vals.block==b]
    keys = ['group','time','analyte']
    g = d.groupby([k for k in keys], dropna=False).size().reset_index(name='obs')
    for _,r in g.iterrows():
        if r.obs!=n:
            rows.append((b,r.group,r.time,r.analyte,n,r.obs))
print('CONTINUOUS BLOCKS with obs != stated n:')
for r in rows: print('  ',r)
print()
stated_s = {'S03-I':7,'S03-J':9,'S06-A':7,'S06-B':7,'S06-C':7,'S06-D':7,'S06-E':7,'S06-F':7,'S06-G':7,'S06-E2_imprint':7,'S06-F2_imprint':7,
            'S09-B':8,'S09-D':8,'S09-F':8,'S13-E':5,'S15-H':7,'S15-L':7,'S15-N':7}
print('SURVIVAL: n per group, deaths, survivors; missing day values')
for b,n in stated_s.items():
    d = surv[surv.block==b]
    for g,dd in d.groupby('group', sort=False):
        flag = '' if len(dd)==n else f'  <-- stated n={n}'
        miss = dd.day.isna().sum()
        print(f'  {b:16s} {g:22s} N={len(dd):2d} deaths={int(dd.event.sum()):2d} surv={int((dd.event==0).sum()):2d} missing_day={miss}{flag}')
