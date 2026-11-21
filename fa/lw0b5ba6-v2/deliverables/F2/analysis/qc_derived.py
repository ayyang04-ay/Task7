import numpy as np, pandas as pd, itertools
from blocks import *
pd.set_option('display.width', 300); pd.set_option('display.float_format', lambda x: f'{x:.5g}')
# 1. S04-B Tfh:Tfr vs Foxp3+ fraction
a = B['S04-B_Tfr'].copy(); b = B['S04-B_TfhTfr'].copy()
a['pred'] = (100-a['value'])/a['value']
print('S04-B: does Tfh:Tfr == (100 - Foxp3%)/Foxp3% ?')
for g in a.group.unique():
    pa = a[a.group==g]['pred'].round(4).tolist(); pb = b[b.group==g]['value'].round(4).tolist()
    print(f'  {g:12s} predicted {pa}\n               printed   {pb}   match_same_order={np.allclose(pa,pb,atol=2e-3)}  match_as_multiset={sorted(np.round(pa,3))==sorted(np.round(pb,3))}')
# any cross-group matches?
allpred = {(g,i):v for g in a.group.unique() for i,v in enumerate(a[a.group==g]['pred'])}
for g in b.group.unique():
    for i,v in enumerate(b[b.group==g]['value']):
        m = [k for k,p in allpred.items() if abs(p-v)<2e-3]
        if (g,i) not in m: print('   printed', g, i, round(v,4), 'matches predicted from', m)

# 2. IgG2a/IgG1 quotient S03-B vs S13-A / S13-B ; S03-F vs S13-C / S13-D
def ratio_check(q, num, den):
    Q = B[q]; N = B[num]; D = B[den]
    print(f'\n{q} (printed quotient) vs {num}/{den} (recomputed from subclass titres)')
    rec = {}
    for g in N.group.unique():
        rec[g] = (N[N.group==g]['value'].values / D[D.group==g]['value'].values)
        print(f'  recomputed {g:12s}: {np.round(rec[g],4)}  mean={rec[g].mean():.3f}  gmean={np.exp(np.log(rec[g]).mean()):.3f}')
    for g in Q.group.unique():
        v = Q[Q.group==g]['value'].values
        hit = [h for h, r in rec.items() if np.allclose(r, v, atol=2e-3)]
        print(f'  printed    {g:12s}: {np.round(v,4)}  mean={v.mean():.3f}   == recomputed column of: {hit}')
ratio_check('S03-B','S13-A','S13-B')
ratio_check('S03-F','S13-C','S13-D')

# 3. total IgG (S03-A/E) ordering vs subclass sums
for tot, g2a, g1 in [('S03-A','S13-A','S13-B'),('S03-E','S13-C','S13-D')]:
    print(f'\n{tot} total IgG GMT vs sum of subclass means ({g2a}+{g1})')
    for g in ['PSLN-212','PSLN-344','PSLN-212(Y)']:
        t = B[tot]; print(f"  {g:12s} total IgG mean={t[t.group==g]['value'].mean():9.0f}   IgG2a mean={B[g2a][B[g2a].group==g]['value'].mean():8.1f}  IgG1 mean={B[g1][B[g1].group==g]['value'].mean():8.1f}")

# 4. S01-B vs S08-C
print('\nS01-B vs S08-C (SRB+ alveolar epithelial cells)')
for k in ['S01-B','S08-C']:
    for g in B[k].group.unique():
        print(f"  {k} {g:22s} {B[k][B[k].group==g]['value'].tolist()}")
# 5. S04-A: sums
lo = B['S04-A_ICOSlo']; hi = B['S04-A_ICOShi']
print('\nS04-A total Tfh (ICOSlo+ICOShi) and ICOShi fraction')
for g in lo.group.unique():
    s = lo[lo.group==g]['value'].values + hi[hi.group==g]['value'].values
    f = hi[hi.group==g]['value'].values / s
    print(f'  {g:12s} total={np.round(s,3)} mean={s.mean():.2f}   ICOShi fraction={np.round(f,3)} mean={f.mean():.3f}')
