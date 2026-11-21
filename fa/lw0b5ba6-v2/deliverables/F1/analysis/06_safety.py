"""Safety / tolerability read-outs available in the dataset.
 (1) S08-D body weight after immunisation (no challenge)
 (2) S09-A lung cytokine/chemokine transcripts at 16 h and (second panel; values match the S01-A 72 h panel) 72 h
 (3) S10-A CNS transcripts at 36 h with cholera toxin as positive control
 (4) persistence of innate activation (S01-A 72 h, S01-D/E day 8)
"""
import numpy as np, pandas as pd
from scipy import stats
import tidy
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500)

print('=== (1) S08-D body weight after immunisation, % of day 0')
d = tidy.get('S08-D')
m = d.pivot_table(index='x', columns='group', values='value', aggfunc='mean')[tidy.groups('S08-D')]
n = d.pivot_table(index='x', columns='group', values='value', aggfunc='count')[tidy.groups('S08-D')]
print(m.round(1).to_string()); print('n per day:'); print(n.to_string())
rows = []
for g in tidy.groups('S08-D'):
    s = d[d.group == g]
    per = s[s.x > 0].groupby('rep')['value'].min()
    day_of_nadir = s[s.x > 0].loc[s[s.x > 0].groupby('rep')['value'].idxmin(), 'x']
    d10 = s[s.x == 10]['value']
    rows.append(dict(group=g, n=per.size, nadir_mean=per.mean(), nadir_sd=per.std(ddof=1), worst_animal=per.min(), max_loss_pct=100 - per.min(),
                     modal_nadir_day=day_of_nadir.mode().iloc[0], d10_mean=d10.mean(), d10_n=d10.size, n_below_95=int((per < 95).sum()), n_below_90=int((per < 90).sum())))
N = pd.DataFrame(rows); print(N.round(2).to_string(index=False)); N.to_csv('../tables/T9_tolerability_S08D.csv', index=False)
nad = {g: d[(d.group == g) & (d.x > 0)].groupby('rep')['value'].min().values for g in tidy.groups('S08-D')}
r = stats.tukey_hsd(*nad.values()); gs = list(nad)
print('one-way ANOVA on per-animal nadir: F=%.2f p=%.2g' % stats.f_oneway(*nad.values()))
for a, b in [('PSLN-344', 'Vaccine'), ('PSLN-344', 'PSLN-212'), ('PSLN-212', 'Vaccine'), ('PSLN-212/R848', 'Vaccine'), ('PSLN-212/R848', 'PSLN-344'), ('PSLN-212(Y)', 'Vaccine'), ('CMP-204', 'Vaccine')]:
    i, j = gs.index(a), gs.index(b); ci = r.confidence_interval()
    print(f'  nadir {a} - {b}: {r.statistic[i, j]:+.2f} points (95% CI {ci.low[i, j]:+.2f} to {ci.high[i, j]:+.2f}), Tukey p = {r.pvalue[i, j]:.3g}')
# day-10 recovery
for g in ['PSLN-344', 'PSLN-212/R848']:
    print(' ', g, 'day-10 values:', d[(d.group == g) & (d.x == 10)].value.values)
print('  PSLN-212/R848 animal with no day-10 record (rep 2): trajectory', d[(d.group == 'PSLN-212/R848') & (d.rep == 2)].sort_values('x').value.values)

print('\n=== (2) S09-A lung transcripts, log10 fold vs untreated -> fold (geometric mean of n=3)')
genes = ['Ifnb1', 'Il6', 'Ccl2', 'Ccl3', 'Ccl5', 'Tnf', 'Il10']
out = []
for panel, tp in [('S09-A[A:U]', '16 h'), ('S09-A[X:AS]', '72 h (label says 16 h)')]:
    for gname in genes:
        s = tidy.get(f'{panel} {gname}')
        for g in tidy.groups(f'{panel} {gname}'):
            v = s[s.group == g].value.values
            out.append(dict(panel=tp, gene=gname, group=g, log10_mean=v.mean(), log10_sd=v.std(ddof=1), fold_geomean=10 ** v.mean()))
CY = pd.DataFrame(out)
CY.to_csv('../tables/T10_lung_cytokines_S09A.csv', index=False)
for tp in CY.panel.unique():
    print(tp); print(CY[CY.panel == tp].pivot(index='gene', columns='group', values='fold_geomean').loc[genes, ['PBS', 'CMP-204', 'PSLN-212', 'PSLN-R848', 'PSLN-212/R848', 'PSLN-344', 'PSLN-212(y)']].round(1).to_string())
# aged 344 vs young 212 (tolerability benchmark = what young animals experience with the Mn-free product) and vs aged 212
print('contrasts on log10 scale (Student t, n=3 v 3):')
for panel, tp in [('S09-A[A:U]', '16 h'), ('S09-A[X:AS]', '72 h*')]:
    for gname in genes:
        a = tidy.vec(f'{panel} {gname}', 'PSLN-344'); y = tidy.vec(f'{panel} {gname}', 'PSLN-212(y)'); o = tidy.vec(f'{panel} {gname}', 'PSLN-212'); rr = tidy.vec(f'{panel} {gname}', 'PSLN-212/R848')
        print(f'  {tp:6s} {gname:6s} 344/young212 = {10**(a.mean()-y.mean()):6.2f}x (p={stats.ttest_ind(a, y).pvalue:.3f}) | 344/aged212 = {10**(a.mean()-o.mean()):6.2f}x (p={stats.ttest_ind(a, o).pvalue:.3f}) | 212+R848/344 = {10**(rr.mean()-a.mean()):6.2f}x (p={stats.ttest_ind(rr, a).pvalue:.3f})')

print('\n=== (3) S10-A CNS transcripts at 36 h (mean, SD; ANOVA + Tukey)')
for gene in ['Ifnb1', 'Tnf', 'Isg15']:
    b = f'S10-A {gene}'; gs = tidy.groups(b); vals = [tidy.vec(b, g) for g in gs]
    F = stats.f_oneway(*vals); r = stats.tukey_hsd(*vals); ci = r.confidence_interval()
    print(gene, ' '.join(f'{g} {v.mean():.2f}±{v.std(ddof=1):.2f}' for g, v in zip(gs, vals)), f'| ANOVA p={F.pvalue:.2g}')
    for a, c in [('PSLN-344', 'Sham'), ('PSLN-344', 'PBS'), ('CT', 'PBS'), ('CT', 'PSLN-344'), ('Sham', 'PBS')]:
        i, j = gs.index(a), gs.index(c)
        print(f'     {a} - {c}: {r.statistic[i, j]:+.2f} (95% CI {ci.low[i, j]:+.2f} to {ci.high[i, j]:+.2f}), Tukey p = {r.pvalue[i, j]:.3g}; unadjusted t p = {stats.ttest_ind(vals[i], vals[j]).pvalue:.3g}')

print('\n=== (4) persistence of innate activation')
for b, x, lab in [('S01-A 72h', None, 'Ifnb1 72 h'), ('S01-D', 8, 'lung monocytes d8'), ('S01-E', 8, 'lung CD11b+ DC d8')]:
    gs = [g for g in tidy.groups(b)]
    vals = {g: tidy.vec(b, g, x) for g in gs}
    print(lab, {g: round(v.mean(), 2) for g, v in vals.items()})
