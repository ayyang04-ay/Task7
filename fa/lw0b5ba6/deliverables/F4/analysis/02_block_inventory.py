#!/usr/bin/env python
"""
02_block_inventory.py
Inventory of every block: groups as printed, observations per group, stated n (from the block label),
and mismatch flags. Run: micromamba run -n core python 02_block_inventory.py
"""
import pandas as pd, numpy as np, re, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parsed')
sc = pd.read_csv(os.path.join(P, 'scalar_long.csv'), keep_default_na=False)
sv = pd.read_csv(os.path.join(P, 'survival_long.csv'), keep_default_na=False)
wt = pd.read_csv(os.path.join(P, 'weight_long.csv'), keep_default_na=False)

stated_n = {  # from block labels in the workbook (cell text), e.g. "S01-A n=5"
 'S01-A':5,'S01-B':5,'S01-C':4,'S01-D':5,'S01-E':5,'S01-F':5,'S01-G':5,
 'S02-A':5,'S02-B':5,'S02-C':5,'S02-D CD40':5,'S02-D CD86':5,'S02-E':5,'S02-F':5,'S02-G':5,'S02-H':5,'S02-I':5,
 'S03-A':5,'S03-B':5,'S03-C':5,'S03-D':5,'S03-E':5,'S03-F':5,'S03-G':5,'S03-H':5,'S03-I':7,'S03-J':9,'S03-K':5,'S03-L':3,
 'S04-A':5,'S04-B Foxp3':5,'S04-B Tfh:Tfr':5,'S04-C':5,'S04-D':3,
 'S05-A':3,'S05-B':3,'S05-C':3,'S05-D':5,'S05-E':5,'S05-F':5,'S05-G':5,'S05-H':5,'S05-I':5,
 'S06-A':7,'S06-B':7,'S06-C':7,'S06-D':7,'S06-E':7,'S06-F':7,'S06-G':7,'S06-E(r71)':7,'S06-F(r71)':7,
 'S07-A':3,'S07-B':5,'S07-C':5,
 'S08-A':3,'S08-B':3,'S08-C':5,'S08-D':5,'S08-unlabelled':None,
 'S09-A(cols A-V)':3,'S09-A(cols X-AS)':3,'S09-B':8,'S09-C':8,'S09-D':8,'S09-E':8,'S09-F':8,'S09-G':8,
 'S10-A':5,'S11-A':5,'S11-B':5,'S11-C':5,'S11-D':5,'S11-E':5,'S12-A':3,
 'S13-A':5,'S13-B':5,'S13-C':5,'S13-D':5,'S13-E':5,'S13-F':7,'S13-G':10,'S13-H':5,'S13-I':5,'S13-J':5,
 'S14-A H1N1':5,'S14-A H3N2':5,
 'S15-A':7,'S15-B':7,'S15-C':7,'S15-D':7,'S15-E':7,'S15-F':7,'S15-G':7,'S15-H':7,'S15-I':7,'S15-J':7,'S15-K':7,
 'S15-L':7,'S15-M':7,'S15-N':7,'S15-O':7}

rows = []
for b, d in sc.groupby('block', sort=False):
    cnt = d.groupby(['group', 'factor'], sort=False).size()
    per_group = d.groupby('group', sort=False).apply(lambda x: sorted(set(x.groupby('factor').size())), include_groups=False)
    rows.append(dict(block=b, kind='scalar', groups='; '.join(per_group.index), n_obs_per_group_per_level='; '.join(str(x) for x in per_group.values),
                     stated_n=stated_n.get(b), n_min=cnt.min(), n_max=cnt.max()))
for b, d in sv.groupby('block', sort=False):
    cnt = d.groupby('group', sort=False).size()
    rows.append(dict(block=b, kind='time-to-event', groups='; '.join(cnt.index), n_obs_per_group_per_level='; '.join(str(x) for x in cnt.values),
                     stated_n=stated_n.get(b), n_min=cnt.min(), n_max=cnt.max()))
for b, d in wt.groupby('block', sort=False):
    cnt0 = d[d.day == 0].groupby('group', sort=False).size()
    rows.append(dict(block=b, kind='body weight', groups='; '.join(cnt0.index), n_obs_per_group_per_level='; '.join(str(x) for x in cnt0.values) + ' (day 0)',
                     stated_n=stated_n.get(b), n_min=cnt0.min(), n_max=cnt0.max()))
inv = pd.DataFrame(rows)
inv['n_mismatch'] = [(r.stated_n is None) or (r.n_min != r.stated_n) or (r.n_max != r.stated_n) for r in inv.itertuples()]
inv.to_csv(os.path.join(P, '..', 'tables', 'T00_block_inventory.csv'), index=False) if os.path.isdir(os.path.join(P, '..', 'tables')) else None
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 90); pd.set_option('display.max_rows', 500)
print(inv.to_string())
print('\nBlocks where stated n != observations:')
print(inv[inv.n_mismatch][['block', 'kind', 'stated_n', 'n_obs_per_group_per_level', 'groups']].to_string())
