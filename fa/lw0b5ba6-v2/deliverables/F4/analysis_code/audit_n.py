import pandas as pd, numpy as np, re
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 1000); pd.set_option('display.max_colwidth', 80)
Q = pd.read_csv('quant_long.csv'); S = pd.read_csv('surv_long.csv'); W = pd.read_csv('wt_long.csv')
stated = {'S01-A':5,'S01-B':5,'S01-C':4,'S01-D':5,'S01-E':5,'S01-F':5,'S01-G':5,'S02-A':5,'S02-B':5,'S02-C':5,'S02-D CD40':5,'S02-D CD86':5,'S02-E':5,'S02-F':5,'S02-G':5,'S02-H':5,'S02-I':5,
 'S03-A':5,'S03-B':5,'S03-C':5,'S03-D':5,'S03-E':5,'S03-F':5,'S03-G':5,'S03-H':5,'S03-I':7,'S03-J':9,'S03-K':5,'S03-L':3,'S04-A':5,'S04-B Foxp3':5,'S04-B Tfh:Tfr':5,'S04-C':5,'S04-D':3,
 'S05-A':3,'S05-B':3,'S05-C':3,'S05-D':5,'S05-E':5,'S05-F':5,'S05-G':5,'S05-H':5,'S05-I':5,'S06-A':7,'S06-B':7,'S06-C':7,'S06-D':7,'S06-E':7,'S06-F':7,'S06-G':7,'S06-E(r71)':7,'S06-F(r71)':7,
 'S07-A':3,'S07-B':5,'S07-C':5,'S08-A':3,'S08-B':3,'S08-C':5,'S08-D':5,'S09-A':3,'S09-B':8,'S09-C':8,'S09-D':8,'S09-E':8,'S09-F':8,'S09-G':8,'S10-A':5,'S11-A':5,'S11-B':5,'S11-C':5,'S11-D':5,'S11-E':5,
 'S12-A':3,'S13-A':5,'S13-B':5,'S13-C':5,'S13-D':5,'S13-E':5,'S13-F':7,'S13-G':10,'S13-H':5,'S13-I':5,'S13-J':5,'S14-A H1N1':5,'S14-A H3N2':5,
 'S15-A':7,'S15-B':7,'S15-C':7,'S15-D':7,'S15-E':7,'S15-F':7,'S15-G':7,'S15-H':7,'S15-I':7,'S15-J':7,'S15-K':7,'S15-L':7,'S15-M':7,'S15-N':7,'S15-O':7}
rows=[]
g = Q.groupby(['block','analyte','time','group'], sort=False, dropna=False).size().reset_index(name='n')
for _,r in g.iterrows():
    if r.n != stated[r.block]: rows.append(('QUANT', r.block, r.analyte, r.time, r.group, stated[r.block], r.n))
g = S.groupby(['block','group'], sort=False).agg(n=('event','size'), n_day=('day','count')).reset_index()
for _,r in g.iterrows():
    if r.n != stated[r.block] or r.n_day != r.n: rows.append(('SURV', r.block, '', '', r.group, stated[r.block], f"{r.n} rows ({r.n_day} with a day value)"))
g = W[W.day==0].groupby(['block','group'], sort=False).agg(n=('value','count')).reset_index()
for _,r in g.iterrows():
    if r.n != stated[r.block]: rows.append(('WT d0', r.block, '', '', r.group, stated[r.block], r.n))
out = pd.DataFrame(rows, columns=['type','block','analyte','time','group','stated_n','observed_n'])
print(out.to_string())
out.to_csv('audit_n_mismatch.csv', index=False)
# survival n per block/group for overview
print(S.groupby(['block','group'], sort=False).agg(n=('event','size'), deaths=('event','sum')).reset_index().to_string())
