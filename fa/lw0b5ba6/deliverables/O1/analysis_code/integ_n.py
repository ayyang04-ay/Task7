import pandas as pd, numpy as np
df = pd.read_csv('/tmp/work/tidy.csv')
stated = {'S01-A_16h':5,'S01-A_72h':5,'S01-B':5,'S01-C':4,'S01-D':5,'S01-E':5,'S01-F':5,'S01-G':5,
 'S02-A':5,'S02-B':5,'S02-C':5,'S02-D_CD40':5,'S02-D_CD86':5,'S02-E':5,'S02-F':5,'S02-G':5,'S02-H':5,'S02-I':5,
 'S03-A':5,'S03-B':5,'S03-C':5,'S03-D':5,'S03-E':5,'S03-F':5,'S03-G':5,'S03-H':5,'S03-I':7,'S03-J':9,'S03-K':5,'S03-L_Aicda':3,'S03-L_E47':3,
 'S04-A_ICOSlo':5,'S04-A_ICOShi':5,'S04-B_Foxp3':5,'S04-B_TfhTfr':5,'S04-C':5,'S04-D':3,
 'S05-A':3,'S05-B':3,'S05-C':3,'S05-D':5,'S05-E':5,'S05-F':5,'S05-G':5,'S05-H':5,'S05-I':5,
 'S06-A':7,'S06-B':7,'S06-C':7,'S06-D':7,'S06-E':7,'S06-F':7,'S06-G':7,'S06-E2_imprint':7,'S06-F2_imprint':7,
 'S07-A':3,'S07-B_Mono':5,'S07-B_Ly6CMac':5,'S07-C':5,'S08-A':3,'S08-B':3,'S08-C':5,'S08-D':5,
 'S09-A_panel1_A-U':3,'S09-A_panel2_X-AS':3,'S09-B':8,'S09-C':8,'S09-D':8,'S09-E':8,'S09-F':8,'S09-G':8,
 'S10-A_Ifnb1':5,'S10-A_Tnf':5,'S10-A_Isg15':5,'S11-A':5,'S11-B':5,'S11-C':5,'S11-D':5,'S11-E':5,'S12-A':3,
 'S13-A':5,'S13-B':5,'S13-C':5,'S13-D':5,'S13-E':5,'S13-F':7,'S13-G':10,'S13-H':5,'S13-I':5,'S13-J':5,'S14-A_H1N1':5,'S14-A_H3N2':5,
 'S15-A':7,'S15-B':7,'S15-C':7,'S15-D':7,'S15-E':7,'S15-F':7,'S15-G':7,'S15-H':7,'S15-I':7,'S15-J':7,'S15-K':7,'S15-L':7,'S15-M':7,'S15-N':7,'S15-O':7}
out=[]
for (b,g),sub in df.groupby(['block','group'],sort=False):
    if b=='S08-UNLABELLED': continue
    if sub.time.notna().any() and sub.event.isna().all():
        # time-resolved: n at first timepoint (baseline) and min over time
        per_t = sub.groupby('time').size()
        n_obs = int(per_t.iloc[0]); n_min=int(per_t.min())
    else:
        n_obs = len(sub); n_min=n_obs
    s = stated.get(b)
    if b.startswith('S09-A'): n_obs = int(sub.groupby('analyte').size().iloc[0]); n_min=n_obs
    out.append(dict(block=b,group=g,stated_n=s,observed_n=n_obs,min_n_over_time=n_min,match=(s==n_obs)))
o = pd.DataFrame(out)
o.to_csv('/tmp/work/n_check.csv',index=False)
print(o[~o.match].to_string())
