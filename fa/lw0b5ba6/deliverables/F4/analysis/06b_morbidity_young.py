#!/usr/bin/env python
"""
06b_morbidity_young.py
 (1) post-challenge morbidity: per-animal body-weight nadir in animals that SURVIVE (weight tables; supporting evidence only,
     because several weight tables carry integrity flags - see 03_integrity_checks.py CHECK 6-8)
 (2) does Mn add anything in YOUNG hosts?  PSLN-344(Y) vs PSLN-212(Y) wherever both were measured
Run: micromamba run -n core python 06b_morbidity_young.py    Outputs: tables/T09a_*.csv, T09b_*.csv
"""
import os, numpy as np, pandas as pd
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, 'parsed'); T = os.path.join(HERE, 'tables')
wt = pd.read_csv(f'{P}/weight_long.csv', keep_default_na=False); st = pd.read_csv(f'{T}/T01e_weight_animal_status.csv', keep_default_na=False)
sc = pd.read_csv(f'{P}/scalar_long.csv', keep_default_na=False); sc['factor'] = sc.factor.astype(str)
sv = pd.read_csv(f'{P}/survival_long.csv', keep_default_na=False)
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 300); pd.options.display.float_format = '{:.4g}'.format

rows = []
for (b, g), x in wt[wt.day > 0].groupby(['block', 'group'], sort=False):
    if b == 'S08-D': continue
    s = st[(st.weight_block == b) & (st.group == g)].set_index('animal')
    nad = []
    for a, y in x.groupby('animal'):
        if a in s.index and s.loc[a, 'status'] == 'alive': nad.append(y.value.min())
    if nad:
        rows.append(dict(weight_block=b, group=g, n_survivors_by_weight=len(nad), mean_nadir=np.mean(nad), worst_nadir=np.min(nad), mean_max_loss_pct=100 - np.mean(nad),
                         n_losing_ge10pct=int(sum(v <= 90 for v in nad)), n_losing_ge15pct=int(sum(v <= 85 for v in nad))))
t = pd.DataFrame(rows); t.to_csv(f'{T}/T09a_postchallenge_nadir_survivors.csv', index=False)
aged = ['S13-F', 'S13-G', 'S15-A', 'S15-B', 'S15-C', 'S15-D', 'S15-E', 'S15-F', 'S15-G', 'S15-M', 'S15-O']
print(t[t.weight_block.isin(aged) & t.group.isin(['PSLN-344', 'PSLN-212(Y)'])].to_string())
for g in ['PSLN-344', 'PSLN-212(Y)']:
    x = t[t.weight_block.isin(aged) & (t.group == g)]
    print(g, 'survivors', int(x.n_survivors_by_weight.sum()), 'weighted mean max loss %', round(float((x.mean_max_loss_pct * x.n_survivors_by_weight).sum() / x.n_survivors_by_weight.sum()), 1),
          '| >=10% loss:', int(x.n_losing_ge10pct.sum()), '| >=15% loss:', int(x.n_losing_ge15pct.sum()))

rows = []
def norm(g): return g.replace('PSLN-212Y', 'PSLN-212(Y)').replace('PSLN-344Y', 'PSLN-344(Y)')
LOG = {'S01-A'}
for (b, f), d in sc.groupby(['block', 'factor'], sort=False):
    d = d.assign(g=d.group.map(norm))
    if {'PSLN-212(Y)', 'PSLN-344(Y)'} <= set(d.g):
        a, c = d[d.g == 'PSLN-344(Y)'].value.values, d[d.g == 'PSLN-212(Y)'].value.values
        if b in LOG: ca, cc = 10 ** np.mean(np.log10(a)), 10 ** np.mean(np.log10(c)); pa, pc = np.log10(a), np.log10(c)
        else: ca, cc = a.mean(), c.mean(); pa, pc = a, c
        rows.append(dict(block=b, level=f, young344=ca, young212=cc, ratio=ca / cc, p_welch=stats.ttest_ind(pa, pc, equal_var=False).pvalue,
                         p_mwu=stats.mannwhitneyu(a, c, method='exact').pvalue, n=f'{len(a)}/{len(c)}'))
y = pd.DataFrame(rows); y.to_csv(f'{T}/T09b_young_344_vs_212.csv', index=False); print(y.to_string())
for b in ['S09-B', 'S09-D', 'S09-F', 'S13-E']:
    x = sv[sv.block == b]; print(b, {g: f"{int((z.event == 0).sum())}/{len(z)}" for g, z in x.groupby('group', sort=False)})

# (3) young hosts: post-challenge body weight, PSLN-344 vs PSLN-212 (S09-C day-21 PR8, S09-E day-21 Perth, S09-G day-180 rgH5N1)
rows = []
for b in ['S09-C', 'S09-E', 'S09-G']:
    d = wt[(wt.block == b) & wt.group.isin(['PSLN-212Y', 'PSLN-344Y'])]
    per = d[d.day > 0].groupby(['group', 'animal']).value.agg(nadir='min', day14='last').reset_index()
    for col in ['nadir', 'day14']:
        a = per[per.group == 'PSLN-344Y'][col]; c = per[per.group == 'PSLN-212Y'][col]
        rows.append(dict(block=b, measure=col, young344=a.mean(), young212=c.mean(), diff=a.mean() - c.mean(), n=f'{len(a)}/{len(c)}',
                         p_welch=stats.ttest_ind(a, c, equal_var=False).pvalue, p_mwu=stats.mannwhitneyu(a, c, method='exact' if len(set(a) | set(c)) == len(a) + len(c) else 'auto').pvalue))
t9c = pd.DataFrame(rows); t9c.to_csv(f'{T}/T09c_young_postchallenge_weight.csv', index=False); print(t9c.to_string())
