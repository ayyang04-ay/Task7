import numpy as np, pandas as pd, itertools, warnings
from scipy import stats
from blocks import B, T, S, W
warnings.filterwarnings('ignore')

LOG_BLOCKS = {'S01-A_16h','S01-A_72h','S03-A','S03-C','S03-D','S03-E','S03-G','S03-H','S03-L_Aicda','S03-L_E47','S13-A','S13-B','S13-C','S13-D','S13-I','S13-J',
              'S10-A_Ifnb1','S10-A_Tnf','S10-A_Isg15','S03-B','S03-F','S04-B_TfhTfr','S08-A','S02-F'}
HAI_LOD_SUB = 5.0   # HAI "0" (= below the lowest dilution tested, 1:10) is substituted by 5 (LoD/2) for log analysis

def get(block, analyte=None):
    df = B[block] if block in B else T[block]
    if analyte is not None:
        df = df[df.analyte==analyte]
    return df

def scale_of(block):
    if block.startswith('S09-A'): return 'log10_stored'
    return 'log10' if block in LOG_BLOCKS else 'linear'

def transform(block, v):
    v = np.asarray(v, float)
    sc = scale_of(block)
    if sc == 'log10':
        v = np.where(v>0, v, HAI_LOD_SUB)
        return np.log10(v)
    return v

def cellrange(d):
    c = d['cellref'].tolist()
    return f"{c[0]}:{c[-1].split('!')[1]}" if len(c)>1 else c[0]

_TUKEY_CACHE = {}
def tukey_table(df, block, ycol='y', cache_key=None):
    if cache_key is not None and cache_key in _TUKEY_CACHE: return _TUKEY_CACHE[cache_key]
    out = _tukey_table(df, block, ycol)
    if cache_key is not None: _TUKEY_CACHE[cache_key] = out
    return out
def _tukey_table(df, block, ycol='y'):
    groups = list(df['group'].unique())
    samples = [df[df.group==g][ycol].values for g in groups]
    if len(groups) < 3: return {}
    r = stats.tukey_hsd(*samples)
    out = {}
    for i, gi in enumerate(groups):
        for j, gj in enumerate(groups):
            if i != j: out[(gi, gj)] = float(r.pvalue[i, j])
    return out

def contrast(block, ref, test, analyte=None, df=None):
    """test vs ref.  Returns dict; difference = test - ref on analysis scale; fold = test/ref (geometric if log scale, ratio of arithmetic means otherwise)"""
    d = get(block, analyte).copy() if df is None else df.copy()
    d['y'] = transform(block, d['value'].values)
    a = d[d.group==ref]; b = d[d.group==test]
    ya, yb = a['y'].values, b['y'].values
    ra, rb = a['value'].values, b['value'].values
    sc = scale_of(block)
    tk = tukey_table(d, block, cache_key=((block, analyte) if df is None else None))
    t, pw = stats.ttest_ind(yb, ya, equal_var=False)
    va, vb = ya.var(ddof=1)/len(ya), yb.var(ddof=1)/len(yb)
    se = np.sqrt(va+vb)
    dfw = (va+vb)**2/(va**2/(len(ya)-1)+vb**2/(len(yb)-1))
    tcrit = stats.t.ppf(0.975, dfw)
    diff = yb.mean()-ya.mean(); lo, hi = diff-tcrit*se, diff+tcrit*se
    try: pmw = stats.mannwhitneyu(yb, ya, alternative='two-sided', method='exact').pvalue
    except Exception: pmw = np.nan
    F, pan = stats.f_oneway(*[d[d.group==g]['y'].values for g in d.group.unique()])
    out = dict(block=block, analyte=analyte or '', scale=sc, ref=ref, test=test, n_ref=len(ya), n_test=len(yb),
               mean_ref=ra.mean(), sd_ref=ra.std(ddof=1), mean_test=rb.mean(), sd_test=rb.std(ddof=1),
               diff=diff, diff_lo=lo, diff_hi=hi, p_welch=pw, p_mw_exact=pmw, p_tukey=tk.get((ref,test), np.nan), p_anova=pan, k_groups=d.group.nunique(),
               cells_ref=cellrange(a), cells_test=cellrange(b))
    if sc.startswith('log10'):
        out.update(gm_ref=10**ya.mean(), gm_test=10**yb.mean(), fold=10**diff, fold_lo=10**lo, fold_hi=10**hi)
    else:
        out.update(gm_ref=np.nan, gm_test=np.nan, fold=rb.mean()/ra.mean() if ra.mean()!=0 else np.nan, fold_lo=np.nan, fold_hi=np.nan)
    return out

# ---------------- survival helpers ----------------
def km_surv_at(days, events, t):
    days = np.asarray(days, float); events = np.asarray(events, int)
    s = 1.0
    for u in np.unique(days[events==1]):
        if u <= t:
            s *= 1 - ((days==u)&(events==1)).sum()/ (days>=u).sum()
    return s

def logrank(d1, e1, d2, e2):
    """two-sample log-rank chi-square (1 df) and asymptotic p"""
    d = np.concatenate([d1,d2]).astype(float); e = np.concatenate([e1,e2]).astype(int); g = np.r_[np.zeros(len(d1)), np.ones(len(d2))]
    O1=E1=V=0.0
    for u in np.unique(d[e==1]):
        n = (d>=u).sum(); n1 = ((d>=u)&(g==0)).sum(); m = ((d==u)&(e==1)).sum(); m1 = ((d==u)&(e==1)&(g==0)).sum()
        O1 += m1; E1 += m*n1/n
        if n>1: V += m*(n1/n)*(1-n1/n)*(n-m)/(n-1)
    if V==0: return 0.0, 1.0, O1-E1
    chi = (O1-E1)**2/V
    return chi, float(stats.chi2.sf(chi,1)), O1-E1

def logrank_perm(d1, e1, d2, e2, nperm=20000, seed=1):
    """permutation p for the log-rank statistic (exact enumeration when feasible)"""
    from math import comb
    d = np.concatenate([d1,d2]).astype(float); e = np.concatenate([e1,e2]).astype(int)
    n1 = len(d1); n = len(d)
    obs = logrank(d1,e1,d2,e2)[0]
    idx = np.arange(n)
    if comb(n, n1) <= 20000:
        cnt=tot=0
        for c in itertools.combinations(idx, n1):
            m = np.zeros(n, bool); m[list(c)] = True
            chi = logrank(d[m], e[m], d[~m], e[~m])[0]
            tot+=1; cnt += chi >= obs-1e-12
        return cnt/tot
    rng = np.random.default_rng(seed); cnt=0
    for _ in range(nperm):
        p = rng.permutation(n); m = np.zeros(n,bool); m[p[:n1]] = True
        cnt += logrank(d[m], e[m], d[~m], e[~m])[0] >= obs-1e-12
    return (cnt+1)/(nperm+1)

def cp_ci(k, n, alpha=0.05):
    lo = stats.beta.ppf(alpha/2, k, n-k+1) if k>0 else 0.0
    hi = stats.beta.ppf(1-alpha/2, k+1, n-k) if k<n else 1.0
    return lo, hi

def surv_group(block, group):
    d = S[block]; d = d[d.group==group]
    return d
