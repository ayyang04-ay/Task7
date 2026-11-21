"""Weight-derived animal status.
Rule (conservative, stated in report):
  - blank cells after the last recorded weight  -> animal removed (dead/euthanized) after that day
  - a trailing run of identical values through the last day is treated as last-observation-carried-forward (animal removed after the first day of the run) when
        run length >= 3, OR run length == 2 and the carried value is <= 90 % of baseline
    (two identical consecutive readings near baseline are treated as coincidence, animal alive)
"""
import pandas as pd, numpy as np
W = pd.read_csv('wt_long.csv')
def animal_status(df):
    df = df.sort_values('day'); days = df.day.values; v = df.value.values
    obs = ~np.isnan(v); last = np.where(obs)[0][-1]
    if days[last] < days[-1]:
        return dict(last_live_day=days[last], status='blank', nadir=np.nanmin(v[:last+1]), final=np.nan, carried=np.nan)
    k = last
    while k > 1 and obs[k-1] and v[k-1] == v[k]: k -= 1
    run = last - k + 1
    if (run >= 3) or (run == 2 and v[last] <= 90):
        return dict(last_live_day=days[k], status='LOCF', nadir=np.nanmin(v[:k+1]), final=np.nan, carried=v[last])
    return dict(last_live_day=days[last], status='alive', nadir=np.nanmin(v), final=v[last], carried=np.nan)
rows=[]
for (blk, grp, an), d in W.groupby(['block','group','animal'], sort=False):
    r = animal_status(d); r.update(block=blk, group=grp, animal=an, col=d.col.iloc[0]); rows.append(r)
A = pd.DataFrame(rows)
A.to_csv('wt_animal_status.csv', index=False)
def lastlive(s): return sorted(int(x) for x in s)
G = A.groupby(['block','group'], sort=False).apply(lambda x: pd.Series(dict(
      n=len(x), alive_d_end=int((x.status=='alive').sum()), removed_blank=int((x.status=='blank').sum()), removed_locf=int((x.status=='LOCF').sum()),
      last_live_days_removed=lastlive(x[x.status!='alive'].last_live_day), mean_nadir_all=x.nadir.mean(),
      mean_nadir_survivors=x[x.status=='alive'].nadir.mean() if (x.status=='alive').any() else np.nan,
      mean_final_survivors=x[x.status=='alive'].final.mean() if (x.status=='alive').any() else np.nan,
      carried_values=[round(c,1) for c in x[x.status=='LOCF'].carried]))).reset_index()
G.to_csv('wt_group_status.csv', index=False)
if __name__ == '__main__':
    pd.set_option('display.width', 300); pd.set_option('display.max_rows', 500); pd.set_option('display.max_colwidth', 60)
    print(G.round(1).to_string())
