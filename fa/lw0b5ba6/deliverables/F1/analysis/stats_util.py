"""Small, dependency-light statistics helpers used by all analysis scripts."""
import itertools, math
import numpy as np
from scipy import stats

def clopper_pearson(k, n, alpha=0.05):
    lo = 0.0 if k == 0 else stats.beta.ppf(alpha / 2, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(1 - alpha / 2, k + 1, n - k)
    return lo, hi

def wilson(k, n, alpha=0.05):
    if n == 0: return (float('nan'), float('nan'))
    z = stats.norm.ppf(1 - alpha / 2); p = k / n
    den = 1 + z * z / n; cen = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0, cen - half), min(1, cen + half)

def logrank_oe(times, events, groups):
    """returns (O1-E1, V) for group==1 vs group==0 (two-sample log-rank, hypergeometric variance)"""
    times = np.asarray(times, float); events = np.asarray(events, int); groups = np.asarray(groups, int)
    oe = 0.0; var = 0.0
    for t in np.unique(times[events == 1]):
        at_risk = times >= t
        n = at_risk.sum(); n1 = (at_risk & (groups == 1)).sum()
        d = ((times == t) & (events == 1)).sum(); d1 = ((times == t) & (events == 1) & (groups == 1)).sum()
        oe += d1 - d * n1 / n
        if n > 1:
            var += d * (n1 / n) * (1 - n1 / n) * (n - d) / (n - 1)
    return oe, var

def logrank_test(t1, e1, t0, e0, exact=True, max_enum=400000):
    """two-sided log-rank; returns dict(chi2, p_asym, p_exact, z)   group1 = first sample"""
    times = list(t1) + list(t0); events = list(e1) + list(e0)
    n1, n = len(t1), len(t1) + len(t0)
    g = np.array([1] * n1 + [0] * (n - n1))
    oe, var = logrank_oe(times, events, g)
    if var == 0:
        return dict(chi2=0.0, z=0.0, p_asym=1.0, p_exact=1.0, oe=oe, var=var)
    chi2 = oe * oe / var
    p_asym = stats.chi2.sf(chi2, 1)
    p_exact = None
    if exact:
        ncomb = math.comb(n, n1)
        if ncomb <= max_enum:
            cnt = 0; tot = 0
            obs = abs(oe) - 1e-9
            for idx in itertools.combinations(range(n), n1):
                gg = np.zeros(n, int); gg[list(idx)] = 1
                o, _ = logrank_oe(times, events, gg)
                tot += 1
                if abs(o) >= obs: cnt += 1
            p_exact = cnt / tot
        else:
            rng = np.random.default_rng(20261101); B = 200000; cnt = 0
            obs = abs(oe) - 1e-9
            for _ in range(B):
                gg = rng.permutation(g)
                o, _ = logrank_oe(times, events, gg)
                if abs(o) >= obs: cnt += 1
            p_exact = (cnt + 1) / (B + 1)
    return dict(chi2=chi2, z=oe / math.sqrt(var), p_asym=p_asym, p_exact=p_exact, oe=oe, var=var)

def stratified_logrank(strata):
    """strata: list of (t1,e1,t0,e0). returns chi2, p"""
    OE = 0; V = 0
    for t1, e1, t0, e0 in strata:
        g = np.array([1] * len(t1) + [0] * len(t0))
        oe, var = logrank_oe(list(t1) + list(t0), list(e1) + list(e0), g)
        OE += oe; V += var
    chi2 = OE * OE / V if V > 0 else 0.0
    return dict(chi2=chi2, p=stats.chi2.sf(chi2, 1), z=OE / math.sqrt(V) if V > 0 else 0.0)

def km_median(times, events):
    times = np.asarray(times, float); events = np.asarray(events, int)
    s = 1.0
    for t in np.unique(times[events == 1]):
        n = (times >= t).sum(); d = ((times == t) & (events == 1)).sum()
        s *= 1 - d / n
        if s <= 0.5: return t
    return float('inf')

def mh_risk_difference(tables):
    """Mantel-Haenszel pooled risk difference (Greenland-Robins variance).
    tables: list of (a, n1, c, n0): a events (here: survivors) of n1 in group1, c of n0 in group0"""
    num = 0; den = 0; P = 0; Q = 0
    for a, n1, c, n0 in tables:
        N = n1 + n0
        num += (a * n0 - c * n1) / N
        den += n1 * n0 / N
        b = n1 - a; d = n0 - c
        P += (a * b * n0 ** 3 + c * d * n1 ** 3) / (n1 * n0 * N ** 2) if n1 > 0 and n0 > 0 else 0
    rd = num / den
    # Sato variance (simplified robust form)
    var = 0
    for a, n1, c, n0 in tables:
        N = n1 + n0; b = n1 - a; d = n0 - c
        var += ((a * b * n0 ** 3 + c * d * n1 ** 3) / (n1 * n0 * N ** 2))
    se = math.sqrt(var) / den
    return rd, rd - 1.96 * se, rd + 1.96 * se

def cmh_test(tables):
    """Cochran-Mantel-Haenszel test (no continuity correction) for 2x2xK; tables as (a, n1, c, n0)"""
    A = 0; E = 0; V = 0
    for a, n1, c, n0 in tables:
        N = n1 + n0; m1 = a + c
        A += a; E += n1 * m1 / N
        if N > 1:
            V += n1 * n0 * m1 * (N - m1) / (N * N * (N - 1))
    chi2 = (A - E) ** 2 / V if V > 0 else 0.0
    return chi2, stats.chi2.sf(chi2, 1)

def hedges_g(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    na, nb = len(a), len(b)
    sp = math.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    if sp == 0: return float('nan')
    d = (a.mean() - b.mean()) / sp
    return d * (1 - 3 / (4 * (na + nb) - 9))

def welch(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    t, p = stats.ttest_ind(a, b, equal_var=False)
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    dfw = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1)) if (va + vb) > 0 else float('nan')
    diff = a.mean() - b.mean(); se = math.sqrt(va + vb)
    tcrit = stats.t.ppf(0.975, dfw) if dfw == dfw else float('nan')
    return dict(diff=diff, lo=diff - tcrit * se, hi=diff + tcrit * se, t=t, p=p, df=dfw)

def mwu_exact(a, b):
    try:
        return stats.mannwhitneyu(a, b, alternative='two-sided', method='exact').pvalue
    except Exception:
        return stats.mannwhitneyu(a, b, alternative='two-sided').pvalue

def tukey(groups: dict):
    """one-way ANOVA + Tukey HSD.  groups {label: values}. returns (F, p_anova, {(a,b): (diff, lo, hi, p)})"""
    labels = list(groups); arrs = [np.asarray(groups[l], float) for l in labels]
    F, p = stats.f_oneway(*arrs)
    res = stats.tukey_hsd(*arrs)
    ci = res.confidence_interval(0.95)
    out = {}
    for i, a in enumerate(labels):
        for j, b in enumerate(labels):
            if i < j:
                out[(a, b)] = (arrs[i].mean() - arrs[j].mean(), ci.low[i, j], ci.high[i, j], res.pvalue[i, j])
    return F, p, out

def fisher_power(p1, p0, n1, n0=None, alpha=0.05):
    """exact power of the two-sided Fisher exact test by enumeration of all binomial outcomes"""
    n0 = n0 or n1
    pw = 0.0
    pm1 = stats.binom.pmf(np.arange(n1 + 1), n1, p1); pm0 = stats.binom.pmf(np.arange(n0 + 1), n0, p0)
    for a in range(n1 + 1):
        if pm1[a] < 1e-12: continue
        for c in range(n0 + 1):
            if pm0[c] < 1e-12: continue
            if stats.fisher_exact([[a, n1 - a], [c, n0 - c]])[1] <= alpha:
                pw += pm1[a] * pm0[c]
    return pw
