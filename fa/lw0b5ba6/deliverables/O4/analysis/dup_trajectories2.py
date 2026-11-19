import pandas as pd, numpy as np, itertools
bw = pd.read_csv('tidy_bodyweight.csv')
bw = bw[bw.day != 0].copy()
traj = {}
for (b, c), x in bw.groupby(['block', 'col']):
    traj[(b, c, x.group.iloc[0])] = x.set_index('day').value.sort_index()
rows = []
for k1, k2 in itertools.combinations(list(traj), 2):
    s1, s2 = traj[k1], traj[k2]
    common = [d for d in s1.index.intersection(s2.index) if pd.notna(s1[d]) and pd.notna(s2[d])]
    matched_vals = set(); live_days = []; off_days = []
    for d in common:
        a, b = s1[d], s2[d]
        if abs(a - b) < 1e-6:
            matched_vals.add(round(a, 6)); live_days.append(int(d))
        else:
            nd = len(repr(float(a)).split('.')[1]) if '.' in repr(float(a)) else 0
            if nd >= 4 and abs((a - b) - round(a - b)) < 1e-6:
                off_days.append((int(d), round(a - b, 1)))
    nd = len(matched_vals)
    if nd >= 3 or (nd >= 2 and len(off_days) >= 2) or (len(off_days) >= 4):
        rows.append(dict(animal_1=f'{k1[0]}:{k1[1]} [{k1[2]}]', animal_2=f'{k2[0]}:{k2[1]} [{k2[2]}]', same_block=k1[0] == k2[0],
                         distinct_exact_values=nd, exact_days=live_days, integer_offset_days=off_days,
                         values=sorted(matched_vals)))
R = pd.DataFrame(rows).sort_values(['distinct_exact_values'], ascending=False)
pd.set_option('display.width', 320); pd.set_option('display.max_colwidth', 160); pd.set_option('display.max_rows', 200)
print(R.to_string())
R.to_csv('dup_animal_trajectories_distinct.csv', index=False)
