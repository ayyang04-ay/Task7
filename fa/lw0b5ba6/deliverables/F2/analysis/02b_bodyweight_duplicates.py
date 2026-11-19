#!/usr/bin/env python
"""Step 2b - body-weight series that recur between different blocks or groups, counting real readings only
(blank and frozen tails excluded).  Output: integrity/B2_duplicate_bodyweight_trajectories_real_values.csv"""
import pandas as pd, numpy as np, itertools
b = pd.read_csv("/tmp/outputs/analysis/tidy/bodyweight.csv", keep_default_na=False); b["value"] = pd.to_numeric(b["value"], errors="coerce"); b["day"] = b["day"].astype(float)
D = pd.read_csv("/tmp/outputs/analysis/integrity/D_bodyweight_animal_status.csv", keep_default_na=False); D["last_real_day"] = pd.to_numeric(D["last_real_day"], errors="coerce")
m = b.merge(D[["block", "animal", "status", "last_real_day"]], on=["block", "animal"])
m = m[m.value.notna() & (m.day <= m.last_real_day) & (m.day > 0)]
traj = {k: dict(zip(g.day, g.value)) for k, g in m.groupby(["block", "group", "animal"], sort=False)}
keys = list(traj); rows = []
for a, bq in itertools.combinations(keys, 2):
    if a[0] == bq[0] and a[1] == bq[1]: continue
    da, db = traj[a], traj[bq]
    same = [d for d in da if d in db and abs(da[d] - db[d]) < 1e-9]
    if len(same) >= 4:
        rows.append(dict(a_block=a[0], a_group=a[1], a_animal=a[2], b_block=bq[0], b_group=bq[1], b_animal=bq[2], n_identical=len(same), n_common=len(set(da) & set(db)), days=",".join(str(int(x)) for x in same)))
R = pd.DataFrame(rows); R.to_csv("/tmp/outputs/analysis/integrity/B2_duplicate_bodyweight_trajectories_real_values.csv", index=False)
print(R.groupby(["a_block", "a_group", "b_block", "b_group"]).agg(animals=("a_animal", "count"), identical=("n_identical", "sum"), common=("n_common", "sum")).to_string())
