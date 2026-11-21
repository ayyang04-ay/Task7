import numpy as np, pandas as pd, itertools
from scipy import stats
import statsmodels.api as sm, statsmodels.formula.api as smf
from blocks import *
from statlib import LOG_BLOCKS
pd.set_option('display.width', 300); pd.set_option('display.max_rows', 3000); pd.set_option('display.float_format', lambda x: f'{x:.4g}')
rows=[]; an=[]
for k, df in T.items():
    tcol = [c for c in df.columns if c in ('day','time','dose_ug')][0]
    d = df.copy(); d['t'] = d[tcol].astype(str)
    d['y'] = np.log10(d['value']) if k in LOG_BLOCKS else d['value']
    d = d.rename(columns={'group':'grp'})
    m = smf.ols('y ~ C(grp)*C(t)', data=d).fit()
    a = sm.stats.anova_lm(m, typ=2)
    an.append(dict(block=k, scale='log10' if k in LOG_BLOCKS else 'linear', p_group=a.loc['C(grp)','PR(>F)'], p_time=a.loc['C(t)','PR(>F)'], p_interaction=a.loc['C(grp):C(t)','PR(>F)'],
                   F_group=a.loc['C(grp)','F'], F_inter=a.loc['C(grp):C(t)','F'], df_resid=int(m.df_resid)))
    # Tukey across all group x time cells (two-way ANOVA with post hoc Tukey, as stated) - family = all cells
    d['cell'] = d['grp'] + ' @ ' + d['t']
    cells = list(d['cell'].unique())
    tk = stats.tukey_hsd(*[d[d.cell==c]['y'].values for c in cells])
    for t in d['t'].unique():
        gs = list(d[d.t==t]['grp'].unique())
        # within-timepoint Tukey as well
        tkw = stats.tukey_hsd(*[d[(d.t==t)&(d.grp==g)]['y'].values for g in gs]) if len(gs)>=3 else None
        for g1,g2 in itertools.combinations(gs,2):
            x = d[(d.t==t)&(d.grp==g1)]; y = d[(d.t==t)&(d.grp==g2)]
            i, j = cells.index(f'{g1} @ {t}'), cells.index(f'{g2} @ {t}')
            pw = stats.ttest_ind(x['y'], y['y'], equal_var=False).pvalue
            rows.append(dict(block=k, time=t, g1=g1, g2=g2, n1=len(x), n2=len(y), mean1=x['value'].mean(), sd1=x['value'].std(ddof=1), mean2=y['value'].mean(), sd2=y['value'].std(ddof=1),
                             ratio_2_over_1=y['value'].mean()/x['value'].mean(), p_tukey_allcells=tk.pvalue[i,j],
                             p_tukey_within_time=(tkw.pvalue[gs.index(g1), gs.index(g2)] if tkw is not None else np.nan), p_welch=pw,
                             cells1=f"{x['cellref'].iloc[0]}:{x['cellref'].iloc[-1].split('!')[1]}", cells2=f"{y['cellref'].iloc[0]}:{y['cellref'].iloc[-1].split('!')[1]}"))
r = pd.DataFrame(rows); r.to_csv('stats_timecourse_pairwise.csv', index=False)
a = pd.DataFrame(an); a.to_csv('stats_timecourse_anova.csv', index=False)
print(a.to_string(index=False))
sel = r[((r.g1=='PSLN-212')&(r.g2=='PSLN-344'))|((r.g1=='PSLN-344')&(r.g2=='PSLN-212'))|((r.g1=='PSLN-344')&(r.g2=='PSLN-212(Y)'))|((r.g1=='PSLN-344')&(r.g2=='PSLN-212Y'))|((r.g1=='Vaccine')&(r.g2=='PSLN-344'))|((r.g1=='Sham')&(r.g2=='PSLN-344'))|((r.g1=='PSLN-344')&(r.g2=='Sham'))|((r.g1=='PSLN-212(Y)')&(r.g2=='PSLN-344(Y)'))]
print(sel.drop(columns=['cells1','cells2']).to_string(index=False))
