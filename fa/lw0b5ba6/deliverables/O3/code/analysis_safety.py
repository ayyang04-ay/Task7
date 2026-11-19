import pandas as pd, numpy as np
from scipy import stats
W = pd.read_csv('/tmp/work/tidy/weights.csv'); K = pd.read_csv('/tmp/work/tidy/contrasts_continuous.csv'); C = pd.read_csv('/tmp/work/tidy/continuous.csv')
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 300)
# --- S08-D reactogenicity: nadir (days 2-10) and day-10 weight per animal
d = W[W.block == 'S08-D']
per = d[d.day > 0].groupby(['group', 'animal']).agg(nadir=('value', 'min'), nadir_day=('value', lambda x: d.loc[x.idxmin(), 'day']),
                                                    last_day=('day', 'max'), last=('value', 'last')).reset_index()
summ = per.groupby('group').agg(n=('nadir', 'size'), nadir_mean=('nadir', 'mean'), nadir_sd=('nadir', 'std'), nadir_min=('nadir', 'min'),
                                max_loss_pct=('nadir', lambda x: 100 - x.min()), n_lost_ge10pct=('nadir', lambda x: int((x <= 90).sum())),
                                missing_d10=('last_day', lambda x: int((x < 10).sum())))
print('S08-D post-vaccination body weight (percent of day 0); nadir over days 2-10'); print(summ.round(2))
ref = per[per.group == 'Vaccine'].nadir.values
for g in ['PSLN-344', 'PSLN-212', 'CMP-204', 'PSLN-212/R848', 'PSLN-212(Y)']:
    x = per[per.group == g].nadir.values
    print(f'  nadir {g} vs Vaccine alone: diff {x.mean()-ref.mean():+.2f} pts; Welch p={stats.ttest_ind(x, ref, equal_var=False).pvalue:.4f}; MW p={stats.mannwhitneyu(x, ref, method="exact").pvalue:.4f}')
x = per[per.group == 'PSLN-212/R848'].nadir.values; y = per[per.group == 'PSLN-344'].nadir.values
print(f'  nadir PSLN-212/R848 vs PSLN-344: diff {x.mean()-y.mean():+.2f}; Welch p={stats.ttest_ind(x, y, equal_var=False).pvalue:.4f}')
# day-by-day means
print(d.groupby(['group', 'day']).value.mean().unstack().round(1))
per.to_csv('/tmp/work/tidy/safety_S08D_nadir.csv', index=False)

# --- S10-A CNS
print('\nS10-A CNS transcripts (fold vs untreated), 36 h')
k = K[K.block == 'S10-A']
print(k[['measurand', 'contrast', 'mean_a', 'mean_b', 'effect', 'p_welch', 'p_mannwhitney_exact', 'p_tukey']].round(4).to_string(index=False))
for m in ['CNS Ifnb1 (fold)', 'CNS Tnf (fold)', 'CNS Isg15 (fold)']:
    g = C[(C.block == 'S10-A') & (C.measurand == m)].groupby('group').value.agg(['mean', 'std']).round(2)
    print(m, g.to_dict('index'))
