import pandas as pd, numpy as np, itertools
from scipy.stats import binom
df = pd.read_csv('/tmp/work/tidy.csv')

def locf_flag(s):
    """mark values that equal the previous timepoint value for the same animal (carried forward)"""
    s = s.sort_values('time').copy()
    s['locf'] = s.value.eq(s.value.shift(1)) & s.time.gt(0)
    return s

# ---------------- WEIGHTS ----------------
w = df[(df.unit=='% of d0')].copy()
w = w.groupby(['block','group','rep'], group_keys=False).apply(locf_flag)
w = w[(w.time>0) & (~w.locf)]      # drop day0 (=100 by definition) and carried-forward repeats
w['hp'] = w.value.apply(lambda x: round(x,1)!=x)
w['frac'] = (w.value % 1).round(4)
mats = {k: s for k,s in w.groupby(['block','group'])}
keys = list(mats)
tot_off=0; tot_off_m=0; tot_off_hp=0; tot_off_hp_m=0
pairs=[]
for A,B in itertools.combinations(keys,2):
    if A==B: continue
    a, b = mats[A], mats[B]
    m = a.merge(b, on='time', suffixes=('_a','_b'))
    if m.empty: continue
    diag = m[m.rep_a==m.rep_b]; off = m[m.rep_a!=m.rep_b]
    k_exact = int((diag.value_a==diag.value_b).sum())
    hpd = diag[diag.hp_a & diag.hp_b]
    k_shift = int(((hpd.frac_a==hpd.frac_b) & (hpd.value_a!=hpd.value_b)).sum())
    tot_off += len(off); tot_off_m += int((off.value_a==off.value_b).sum())
    hpo = off[off.hp_a & off.hp_b]
    tot_off_hp += len(hpo); tot_off_hp_m += int((hpo.frac_a==hpo.frac_b).sum())
    pairs.append(dict(A=A,B=B,n_aligned=len(diag),n_aligned_hp=len(hpd),k_exact=k_exact,k_shift=k_shift,
                      cells='; '.join((diag[(diag.value_a==diag.value_b)].cell_a + '=' + diag[(diag.value_a==diag.value_b)].cell_b).tolist()[:10]),
                      shift_cells='; '.join((hpd[(hpd.frac_a==hpd.frac_b)&(hpd.value_a!=hpd.value_b)].cell_a+'~'+hpd[(hpd.frac_a==hpd.frac_b)&(hpd.value_a!=hpd.value_b)].cell_b).tolist()[:10])))
p0 = tot_off_m/tot_off; p0hp = (tot_off_hp_m+1)/(tot_off_hp+1)
print(f'chance exact-match rate (weights, same day, different animal position): {p0:.5f}  ; chance frac-match rate for high-precision values: {p0hp:.5f}')
P = pd.DataFrame(pairs)
P['p_exact'] = binom.sf(P.k_exact-1, P.n_aligned, p0)
P['p_shift'] = binom.sf(P.k_shift-1, P.n_aligned_hp.clip(lower=1), p0hp)
P['p_min'] = P[['p_exact','p_shift']].min(axis=1)
ntests = len(P)*2
P['bonferroni_sig'] = P.p_min < 0.05/ntests
sig = P[P.bonferroni_sig].sort_values('p_min')
pd.set_option('display.width',320); pd.set_option('display.max_colwidth',160)
print('weight block-group pairs tested:', len(P), ' significant (Bonferroni):', len(sig))
print(sig[['A','B','n_aligned','k_exact','n_aligned_hp','k_shift','p_exact','p_shift']].to_string())
sig.to_csv('/tmp/work/weight_copy_sig.csv', index=False)
P.to_csv('/tmp/work/weight_copy_all.csv', index=False)
