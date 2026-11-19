import pandas as pd, numpy as np, warnings
from scipy import stats
import statsmodels.formula.api as smf, statsmodels.api as sm
warnings.filterwarnings('ignore')
C = pd.read_csv('/tmp/work/tidy/continuous.csv'); C['time'] = C['time'].astype(str)
Sm = pd.read_csv('/tmp/work/tidy/summary_continuous.csv'); Sm['time'] = Sm['time'].astype(str)
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 300); pd.set_option('display.max_colwidth', 45)
def center(r):  # natural-scale central value: GM for log-analysed, mean otherwise
    return r['geo_mean'] if r['scale'] in ('log2', 'log10') else r['mean']
Sm['center'] = Sm.apply(center, axis=1)
key = [('S01-A','16h'),('S02-F','36h'),('S01-D','4'),('S01-E','4'),('S01-F','72h'),('S02-A','72h'),('S02-B','72h'),('S02-C','36h'),
       ('S02-D CD40','d3'),('S02-D CD86','d3'),('S02-E','72h+3d'),('S05-D','d3'),('S05-E','d3'),('S04-A','d7'),('S04-B Foxp3','d7'),
       ('S03-K','d7'),('S03-L','d5'),('S13-H','not stated'),('S03-A','d14'),('S03-C','d14'),('S03-D','d14'),('S03-E','d14'),('S03-G','d14'),('S03-H','d14'),
       ('S13-A','d14'),('S13-B','d14'),('S13-C','d14'),('S13-D','d14'),('S13-I','d28'),('S13-J','d28'),('S05-F','d14'),('S14-A H1N1','not stated'),
       ('S14-A H3N2','not stated'),('S05-G','d60'),('S05-H','d60'),('S05-I','d25'),('S04-C','d30'),('S04-D','d7'),('S11-E','not stated')]
rows=[]
for blk,t in key:
    d = Sm[(Sm.block==blk)&(Sm.time==t)]
    for meas, dm in d.groupby('measurand'):
        g = dm.set_index('group')['center']
        base = g.get('Sham', np.nan)
        rows.append(dict(block=blk, measurand=meas, time=t, vehicle=g.get('Sham',np.nan), PSLN212=g.get('PSLN-212',np.nan), PSLN344=g.get('PSLN-344',np.nan),
                         young212=g.get('PSLN-212(Y)',np.nan), CMP204=g.get('CMP-204',np.nan),
                         fold_344_vs_vehicle=g.get('PSLN-344',np.nan)/base if base==base else np.nan,
                         fold_344_vs_212=g.get('PSLN-344',np.nan)/g.get('PSLN-212',np.nan),
                         aged344_as_pct_of_young=100*g.get('PSLN-344',np.nan)/g.get('PSLN-212(Y)',np.nan)))
R = pd.DataFrame(rows); print(R.round(2).to_string(index=False)); R.to_csv('/tmp/work/tidy/key_endpoints_ratios.csv', index=False)

print('\n=== payload: CMP-204 (cGAMP) vs PSLN-212 (CDN-1807), both without Mn ===')
K = pd.read_csv('/tmp/work/tidy/contrasts_continuous.csv')
k = K[K.contrast=='PSLN-212 vs CMP-204']
print(k[['block','measurand','time','mean_a','mean_b','effect','effect_type','p_welch','p_mannwhitney_exact','p_tukey']].round(4).to_string(index=False))

print('\n=== S08-B encapsulation efficiency ===')
e = C[C.block=='S08-B'].groupby('group').value.agg(['mean','std','min','max','count']).round(2); print(e)
a = C[(C.block=='S08-B')&(C.group=='PSLN-344')].value; b = C[(C.block=='S08-B')&(C.group=='PSLN-212')].value
print('PSLN-344 vs PSLN-212 EE: Welch p=%.3f' % stats.ttest_ind(a,b,equal_var=False).pvalue)
allv = [C[(C.block=='S08-B')&(C.group==g)].value.values for g in C[C.block=='S08-B'].group.unique()]
print('one-way ANOVA across formulations: p=%.3f' % stats.f_oneway(*allv).pvalue)

# two-way ANOVA is in analysis_twoway.py
