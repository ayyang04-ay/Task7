import pandas as pd, numpy as np, itertools
bw = pd.read_csv('tidy_bodyweight.csv')
bw = bw[bw.day != 0].copy()
traj = {}
for (b, c), x in bw.groupby(['block', 'col']):
    s = x.set_index('day').value
    traj[(b, c, x.group.iloc[0])] = s
rows = []
keys = list(traj)
for k1, k2 in itertools.combinations(keys, 2):
    s1, s2 = traj[k1], traj[k2]
    common = s1.index.intersection(s2.index)
    exact = 0; intoff = 0; days_exact = []; days_off = []
    for d in common:
        a, b = s1[d], s2[d]
        if pd.isna(a) or pd.isna(b):
            continue
        if abs(a - b) < 1e-6:
            # ignore if it is just a carried-forward constant shared by chance? keep
            exact += 1; days_exact.append(int(d))
        else:
            diff = a - b
            # same fractional part with integer (or 0.1-multiple) offset, only meaningful for >=4 decimal values
            da = len(repr(float(a)).split('.')[1]) if '.' in repr(float(a)) else 0
            if da >= 4 and abs(diff - round(diff)) < 1e-6:
                intoff += 1; days_off.append((int(d), round(diff, 4)))
    if exact >= 3 or (exact + intoff) >= 4:
        rows.append(dict(animal_1=f'{k1[0]} col {k1[1]} ({k1[2]})', animal_2=f'{k2[0]} col {k2[1]} ({k2[2]})',
                         same_block=(k1[0] == k2[0]), days_exact=days_exact, days_integer_offset=days_off,
                         n_exact=exact, n_int_offset=intoff))
R = pd.DataFrame(rows).sort_values(['same_block', 'n_exact'], ascending=[True, False])
pd.set_option('display.width', 320); pd.set_option('display.max_colwidth', 200); pd.set_option('display.max_rows', 200)
print(R.to_string())
R.to_csv('dup_animal_trajectories.csv', index=False)
