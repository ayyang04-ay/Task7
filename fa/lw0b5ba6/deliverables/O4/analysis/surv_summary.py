import pandas as pd
s = pd.read_csv('tidy_survival.csv')
out = []
for (b, g), d in s.groupby(['block', 'group'], sort=False):
    n = len(d); dead = int(d.event.sum()); alive = n - dead
    missing_days = int(d.days.isna().sum())
    death_days = sorted(d.loc[d.event == 1, 'days'].dropna().astype(int).tolist())
    out.append(dict(block=b, group=g, n=n, deaths=dead, survivors=alive, surv_frac=f'{alive}/{n}', death_days=death_days,
                    max_followup=d.days.max(), missing_day_values=missing_days, cohort=d.cohort.iloc[0]))
o = pd.DataFrame(out)
pd.set_option('display.width', 250)
print(o.to_string())
o.to_csv('survival_counts.csv', index=False)
