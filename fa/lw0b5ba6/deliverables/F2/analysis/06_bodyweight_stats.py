#!/usr/bin/env python
"""
Step 6 - Body-weight analysis.  Dead animals are handled explicitly: blank cells and frozen (carried-forward)
tails are NOT treated as observations.  Per arm: peak weight loss per animal (nadir while alive), mean of
animals alive at each day, number alive per day.  S08-D (post-vaccination, no challenge) is the tolerability block.
Output: stats/bodyweight_by_arm.csv, stats/bodyweight_daily.csv
"""
import pandas as pd, numpy as np, os
from scipy import stats
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 2000); pd.set_option("display.max_columns", 40)
O = "/tmp/outputs/analysis/stats"
b = pd.read_csv("/tmp/outputs/analysis/tidy/bodyweight.csv", keep_default_na=False); b["value"] = pd.to_numeric(b["value"], errors="coerce"); b["day"] = b["day"].astype(float)
D = pd.read_csv("/tmp/outputs/analysis/integrity/D_bodyweight_animal_status.csv", keep_default_na=False)
D["last_real_day"] = pd.to_numeric(D["last_real_day"], errors="coerce")
m = b.merge(D[["block", "animal", "status", "last_real_day"]], on=["block", "animal"])
m["real"] = m["value"].notna() & (m["day"] <= m["last_real_day"])
real = m[m.real]
daily = real.groupby(["block", "group", "day"], sort=False)["value"].agg(n_alive="count", mean="mean", sd="std").reset_index()
daily.to_csv(f"{O}/bodyweight_daily.csv", index=False)
rows = []
for (blk, grp), g in real.groupby(["block", "group"], sort=False):
    per = g.groupby("animal")["value"].min()
    stt = D[(D.block == blk) & (D.group == grp)].set_index("animal")["status"]
    surv = [a for a in per.index if stt[a] == "complete"]
    dd = daily[(daily.block == blk) & (daily.group == grp)]
    imin = dd["mean"].idxmin()
    cells = b[(b.block == blk) & (b.group == grp)]["cell"]
    rows.append(dict(block=blk, group=grp, n=len(per), n_alive_last_day=len(surv), mean_peak_loss_all_pct=100 - per.mean(), max_individual_loss_pct=100 - per.min(),
                     mean_peak_loss_survivors_pct=(100 - per[surv].mean()) if surv else np.nan, sd_peak_loss_survivors=per[surv].std() if len(surv) > 1 else np.nan,
                     nadir_of_group_mean_pct=dd.loc[imin, "mean"], nadir_day=dd.loc[imin, "day"],
                     last_day_mean_survivors=dd[dd.day == dd.day.max()]["mean"].iloc[0] if len(dd) else np.nan,
                     cells=f"{b[(b.block==blk)]['sheet'].iloc[0]}!{cells.iloc[0]}:{cells.iloc[-1]}"))
R = pd.DataFrame(rows); R.to_csv(f"{O}/bodyweight_by_arm.csv", index=False)
print(R.to_string(index=False, float_format=lambda v: f"{v:.1f}"))

print("\nS08-D tolerability after vaccination (no challenge): per-animal peak loss, Welch t vs 'Vaccine' alone and vs PSLN-212")
q = real[real.block == "S08-D"]; per = q.groupby(["group", "animal"])["value"].min().reset_index()
for g in ["PSLN-212(Y)", "CMP-204", "PSLN-212", "PSLN-344", "PSLN-212/R848"]:
    a = 100 - per[per.group == g]["value"]; v = 100 - per[per.group == "Vaccine"]["value"]; p2 = 100 - per[per.group == "PSLN-212"]["value"]
    print(f"   {g:<14} peak loss mean {a.mean():.2f}% (sd {a.std():.2f}, max {a.max():.1f})  vs Vaccine {v.mean():.2f}%: p={stats.ttest_ind(a, v, equal_var=False).pvalue:.4f}"
          + (f" | vs PSLN-212 {p2.mean():.2f}%: p={stats.ttest_ind(a, p2, equal_var=False).pvalue:.4f}" if g != "PSLN-212" else ""))
d10 = q[q.day == 10].groupby("group")["value"].agg(["count", "mean", "min"]); print(d10.round(1).to_string())
print("\nS08-D daily means (animals with a reading)"); print(daily[daily.block == "S08-D"].pivot(index="day", columns="group", values="mean").round(1).to_string())
