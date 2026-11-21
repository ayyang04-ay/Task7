"""Time-to-event analysis of every survival block (per-group table T1 and pairwise tests T2).  Helpers live in survlib.py."""
from survlib import *

# --------------------------------------------------------------------------- per-group table
rows = []
for b in SURV:
    d = prep(b)
    for g in pd.unique(d.group):
        s = d[d.group == g]; n = len(s); k = int(s.event.sum())
        lo, hi = cp(n - k, n)
        dt = sorted(s[s.event == 1].time.astype(int).tolist())
        med = np.median(s.time) if k > n / 2 else np.nan    # KM median reached only if >50% died
        rows.append(dict(block=b, group=g, n=n, deaths=k, survivors=n - k, surv_pct=100 * (n - k) / n, ci_lo=100 * lo, ci_hi=100 * hi,
                         death_days=' '.join(map(str, dt)), median_days_to_death=(float(np.median(dt)) if dt else np.nan),
                         km_median=med, n_time_missing=int(s.time_missing.sum())))
G = pd.DataFrame(rows)
G.to_csv('../tables/T1_survival_by_group.csv', index=False)
print(G[['block', 'group', 'n', 'deaths', 'survivors', 'surv_pct', 'ci_lo', 'ci_hi', 'death_days', 'n_time_missing']].round(1).to_string(index=False))

# --------------------------------------------------------------------------- pairwise tests
def pair(b, g1, g0):
    d = prep(b); s = d[d.group.isin([g1, g0])]
    if s.group.nunique() < 2:
        return None
    grp = (s.group == g1).astype(int).values
    a = s[s.group == g1]; c = s[s.group == g0]
    lr = logrank_test(a.time, c.time, a.event, c.event)
    pex = lr_exact(s.time.values, s.event.values, grp)
    tab = [[int((a.event == 0).sum()), int(a.event.sum())], [int((c.event == 0).sum()), int(c.event.sum())]]
    pf = stats.fisher_exact(tab)[1]
    return dict(block=b, contrast=f'{g1} vs {g0}', surv_1=f"{tab[0][0]}/{len(a)}", surv_0=f"{tab[1][0]}/{len(c)}",
                risk_diff_pct=100 * (tab[0][0] / len(a) - tab[1][0] / len(c)),
                logrank_chi2=lr.test_statistic, logrank_p=lr.p_value, logrank_exact_p=pex, fisher_p=pf)

contrasts = []
for b in SURV:
    gs = tidy.groups(b)
    want = [('PSLN-344', 'Sham'), ('PSLN-344', 'PSLN-212'), ('PSLN-212', 'Sham'), ('PSLN-344', 'PSLN-212(Y)'), ('PSLN-212(Y)', 'PSLN-212'),
            ('CMP-204', 'Sham'), ('PSLN-344', 'CMP-204'), ('CMP-204', 'PSLN-212'), ('PSLN-344', 'Untreated'), ('PSLN-212', 'Untreated'),
            ('Naive+PSLN-344', 'Naive+PSLN-212'), ('Imprinting+PSLN-344', 'Imprinting+PSLN-212'), ('Imprinting+PSLN-212', 'Naive+PSLN-212'),
            ('Imprinting+PSLN-344', 'Naive+PSLN-344'),
            ('PSLN-344Y', 'Sham'), ('PSLN-212Y', 'Sham'), ('PSLN-344Y', 'PSLN-212Y'),
            ('PSLN-344(Y)', 'Sham'), ('CMP-204(Y)', 'Sham'), ('PSLN-344(Y)', 'Naive'), ('Sham', 'Naive'), ('PSLN-344(Y)', 'CMP-204(Y)'),
            ('3d Vaccine+PSLN-344', '3d Vaccine'), ('3d Vaccine+PSLN-344', '3d PSLN-344'), ('3d PSLN-344', '3d Vaccine')]
    for g1, g0 in want:
        if g1 in gs and g0 in gs:
            contrasts.append(pair(b, g1, g0))
Cn = pd.DataFrame(contrasts)
Cn.to_csv('../tables/T2_survival_pairwise.csv', index=False)
print()
print(Cn.round(4).to_string(index=False))
