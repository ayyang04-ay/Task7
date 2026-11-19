import pandas as pd, numpy as np
from blocks import BW
bw = pd.read_csv('tidy_bodyweight.csv')
sc = pd.read_csv('survival_counts.csv')

def classify(series_days, vals):
    """Return status of an animal from its weight trajectory.
    blank_after: first day with missing value (animal disappears) ;
    flat_run: length of trailing run of identical values ending at last day."""
    v = list(vals)
    days = list(series_days)
    # first missing
    first_missing = None
    for d, x in zip(days, v):
        if x is None or (isinstance(x, float) and np.isnan(x)):
            first_missing = d; break
    if first_missing is not None:
        return 'disappears', first_missing, None
    run = 1
    for i in range(len(v) - 1, 0, -1):
        if abs(v[i] - v[i - 1]) < 1e-9:
            run += 1
        else:
            break
    if run >= 3:
        return 'flatline>=3', days[len(v) - run], v[-1]
    if run == 2:
        return 'flatline=2', days[len(v) - run], v[-1]
    return 'alive', None, v[-1]

rows = []
for bid, w in BW.items():
    d = bw[bw.block == bid]
    for g, cols in w['groups'].items():
        dd = d[d.group == d[d.col.isin(cols)].group.iloc[0]] if len(d[d.col.isin(cols)]) else None
        statuses = []
        for c in cols:
            a = d[d.col == c].sort_values('day')
            st, when, last = classify(a.day.tolist(), a.value.tolist())
            statuses.append((c, st, when, last))
        n = len(cols)
        n_dis = sum(s[1] == 'disappears' for s in statuses)
        n_f3 = sum(s[1] == 'flatline>=3' for s in statuses)
        n_f2 = sum(s[1] == 'flatline=2' for s in statuses)
        n_alive = sum(s[1] == 'alive' for s in statuses)
        linked = w['linked']
        gnorm = g.replace('Naïve', 'Naive')
        surv = None
        if linked:
            m = sc[(sc.block == linked)]
            # map group names
            gg = gnorm.replace('PSLN-212Y', 'PSLN-212(Y)').replace('PSLN-344Y', 'PSLN-344(Y)')
            mm = m[m.group == gg]
            if len(mm):
                surv = f"{int(mm.survivors.iloc[0])}/{int(mm.n.iloc[0])} (deaths d{mm.death_days.iloc[0]})"
            else:
                surv = 'GROUP NOT IN SURVIVAL BLOCK'
        rows.append(dict(bw_block=bid, group=g, n_weight_cols=n, alive_by_weights=n_alive, disappear=n_dis,
                         flat3=n_f3, flat2=n_f2, implied_survivors_strict=n_alive + n_f2,
                         implied_survivors_loose=n_alive, linked_survival=linked, survival_record=surv,
                         detail='; '.join(f"{c}:{st}{'@d'+str(int(wn)) if wn is not None else ''}" for c, st, wn, _ in statuses if st != 'alive')))
out = pd.DataFrame(rows)
pd.set_option('display.width', 300); pd.set_option('display.max_colwidth', 120)
print(out.to_string())
out.to_csv('bw_vs_survival_reconciliation.csv', index=False)
