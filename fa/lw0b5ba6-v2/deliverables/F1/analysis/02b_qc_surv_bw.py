"""QC 2: do the body-weight blocks agree with the time-to-event blocks they are said to describe?

For each body-weight trajectory we infer 'removed from study' when either
  (a) the cells go blank after some day, or
  (b) the trajectory has a constant tail (>=2 identical final values), i.e. last observation carried forward.
Rule (b) is validated on the 'Untreated' groups (S15-E/G), whose flat-line days reproduce the S06-E/G death days.
"""
import numpy as np, pandas as pd
import psln_blocks as P

DAYS = [0, 2, 4, 6, 8, 10, 12, 14]

def traj(bid):
    d = P.load(bid)
    out = {}
    for (g, rep), s in d.groupby(['group', 'rep'], sort=False):
        out[(g, rep)] = s.set_index('x')['value'].reindex(DAYS)
    return out

def infer(s):
    """return (status, last_informative_day, last_value) ; status in alive/blank/flat"""
    v = s.dropna()
    last_day = v.index[-1]
    if last_day < 14:
        return 'blank', last_day, v.iloc[-1]
    # constant tail
    vals = v.values
    k = 1
    while k < len(vals) and vals[-k - 1] == vals[-1]:
        k += 1
    if k >= 2 and vals[-1] < 99.0:      # tail of >=2 identical values (exclude trivial 100/100)
        first_flat_day = v.index[len(vals) - k]
        return 'flat', first_flat_day, vals[-1]
    return 'alive', 14, vals[-1]

rows = []
for bid, b in P.BLOCKS.items():
    if b['kind'] != 'bw' or not b.get('pair'):
        continue
    sv = P.load(b['pair'])
    tj = traj(bid)
    groups_bw = [g for g, *_ in b['groups']]
    groups_sv = list(sv['group'].unique())
    for g in groups_bw:
        st = [infer(s) for (gg, rep), s in tj.items() if gg == g]
        n = len(st)
        n_blank = sum(x[0] == 'blank' for x in st); n_flat = sum(x[0] == 'flat' for x in st)
        bw_removed_days = sorted([x[1] for x in st if x[0] != 'alive'])
        flat_vals = [round(x[2], 1) for x in st if x[0] == 'flat']
        # matching survival group (tolerant to label variants)
        if g in groups_sv:
            s = sv[sv.group == g]
            deaths = int(s.event.sum()); ns = len(s); dd = sorted(s[s.event == 1].time.astype(int).tolist())
        else:
            deaths = None; ns = None; dd = None
        rows.append(dict(bw_block=bid, surv_block=b['pair'], group=g, n_bw=n, bw_blank=n_blank, bw_flat_tail=n_flat,
                         bw_removed_total=n_blank + n_flat, bw_last_day_before_removal=bw_removed_days, flat_tail_values=flat_vals,
                         n_surv=ns, surv_deaths=deaths, surv_death_days=dd,
                         consistent=(None if deaths is None else (deaths == n_blank + n_flat and ns == n))))
    for g in groups_sv:
        if g not in groups_bw:
            s = sv[sv.group == g]
            rows.append(dict(bw_block=bid, surv_block=b['pair'], group=g + ' [no body-weight columns]', n_bw=None, n_surv=len(s),
                             surv_deaths=int(s.event.sum()), surv_death_days=sorted(s[s.event == 1].time.astype(int).tolist()), consistent=None))
qc = pd.DataFrame(rows)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 60); pd.set_option('display.max_rows', 500)
print(qc.to_string(index=False))
qc.to_csv('../tables/QC_survival_vs_bodyweight.csv', index=False)
print('\nconsistent:', qc.consistent.value_counts(dropna=False).to_dict())
