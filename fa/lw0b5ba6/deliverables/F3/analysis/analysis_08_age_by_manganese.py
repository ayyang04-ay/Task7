"""
Analysis 8 - does manganese add more in aged than in young animals?
Five single-time-point blocks contain the full 2 x 2 (aged/young x PSLN-212/PSLN-344): S01-A/16h, S01-A/72h, S01-F, S01-G,
S02-C, S02-E.  Two-way ANOVA (age x formulation) on the scale used elsewhere; the interaction term is the test.
Output: age_by_manganese_interaction.csv
"""
import numpy as np, pandas as pd, warnings
import statsmodels.api as sm, statsmodels.formula.api as smf
warnings.filterwarnings('ignore')
d=pd.read_csv('tidy_all_observations.csv'); d['group']=d.group.str.strip()
rows=[]
for blk,scale,lab in [('S01-A/16h','log10','Lung Ifnb1, 16 h'),('S01-A/72h','log10','Lung Ifnb1, 72 h'),('S01-F','linear','Lung cDC1, 72 h'),('S01-G','linear','Lung cDC2, 72 h'),
                      ('S02-C','linear','Antigen+ DC in lymph node, 36 h'),('S02-E','linear','Ex vivo CD8 priming by lymph-node DC')]:
    x=d[(d.block==blk)&d.group.isin(['PSLN-212','PSLN-344','PSLN-212(Y)','PSLN-344(Y)'])].copy()
    x['age']=np.where(x.group.str.endswith('(Y)'),'young','aged'); x['mn']=np.where(x.group.str.contains('344'),'Mn','none')
    x['y']=np.log10(x.value) if scale=='log10' else x.value
    m=smf.ols('y ~ C(age)*C(mn)',data=x).fit(); an=sm.stats.anova_lm(m,typ=2)
    g=x.groupby(['age','mn']).y.mean()
    ia=g[('aged','Mn')]-g[('aged','none')]; iy=g[('young','Mn')]-g[('young','none')]
    if scale=='log10': inc_a,inc_y,unit=10**ia,10**iy,'fold'
    else: inc_a,inc_y,unit=ia,iy,'points'
    rows.append(dict(block=blk,readout=lab,scale=scale,n_per_cell=int(x.groupby('group').size().min()),increment_aged=inc_a,increment_young=inc_y,unit=unit,
                     p_interaction=an.loc['C(age):C(mn)','PR(>F)'],p_age=an.loc['C(age)','PR(>F)'],p_manganese=an.loc['C(mn)','PR(>F)'],
                     cells='; '.join(f"{gg}: {x[x.group==gg].sheet.iloc[0]}!{x[x.group==gg].cell.iloc[0]}:{x[x.group==gg].cell.iloc[-1]}" for gg in ['PSLN-212','PSLN-344','PSLN-212(Y)','PSLN-344(Y)'])))
R=pd.DataFrame(rows); R.to_csv('age_by_manganese_interaction.csv',index=False)
pd.set_option('display.width',250); print(R.drop(columns=['cells']).to_string(float_format=lambda v:f'{v:.3g}'))
