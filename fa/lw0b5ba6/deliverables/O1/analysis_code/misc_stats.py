import pandas as pd, numpy as np, warnings
warnings.filterwarnings('ignore')
from scipy.optimize import curve_fit
from scipy import stats
import statsmodels.formula.api as smf
import statsmodels.api as sm
df = pd.read_csv('/tmp/work/tidy.csv')
out = {}
# ---- S08-A dose-response: Emax model on linear fold (Ifnb1), per formulation
d = df[df.block=='S08-A']
def emax(dose, e0, emax_, ed50): return e0 + emax_*dose/(ed50+dose)
rows=[]
for g,s in d.groupby('group'):
    try:
        p,cov = curve_fit(emax, s.time.values, s.value.values, p0=[1, s.value.max(), 10], maxfev=20000)
        se = np.sqrt(np.diag(cov))
        pred = emax(s.time.values,*p); r2 = 1-((s.value-pred)**2).sum()/((s.value-s.value.mean())**2).sum()
        m20 = s[s.time==20].value.mean(); m40 = s[s.time==40].value.mean()
        rows.append(dict(group=g, E0=p[0], Emax=p[1], ED50_ug=p[2], ED50_se=se[2], R2=r2, mean_20ug=m20, mean_40ug=m40,
                         pct_of_fitted_max_at_20ug=100*(emax(20,*p)-p[0])/p[1], gain_40_vs_20_pct=100*(m40/m20-1)))
    except Exception as e:
        rows.append(dict(group=g, error=str(e)))
DR = pd.DataFrame(rows); print(DR.round(2).to_string()); DR.to_csv('/tmp/work/dose_response.csv',index=False)
# ---- two-way ANOVA for time-course blocks (aged PSLN-212 vs PSLN-344), linear scale
rows=[]
for b in ['S01-D','S01-E','S07-A','S02-F']:
    s = df[(df.block==b)&(df.group.isin(['PSLN-212','PSLN-344']))].copy()
    if b=='S02-F': s['value']=np.log10(s.value)
    s['t']=s.time.astype(str)
    m = smf.ols('value ~ C(group)*C(t)', data=s).fit()
    a = sm.stats.anova_lm(m, typ=2)
    rows.append(dict(block=b, p_group=a.loc['C(group)','PR(>F)'], p_time=a.loc['C(t)','PR(>F)'], p_interaction=a.loc['C(group):C(t)','PR(>F)']))
TW = pd.DataFrame(rows); print(TW.to_string()); TW.to_csv('/tmp/work/twoway_anova.csv',index=False)
# ---- S08-D reactogenicity: per-animal nadir over days 2-10
w = df[df.block=='S08-D']
nad = w[w.time>0].groupby(['group','rep']).value.min().reset_index()
nd = w[w.time>0].loc[w[w.time>0].groupby(['group','rep']).value.idxmin()][['group','rep','time']]
nad = nad.merge(nd, on=['group','rep'])
R = nad.groupby('group').agg(n=('value','size'), mean_nadir=('value','mean'), sd=('value','std'), min_nadir=('value','min'), mean_nadir_day=('time','mean')).reset_index()
ref = nad[nad.group=='Vaccine'].value.values
R['welch_p_vs_vaccine'] = [stats.ttest_ind(nad[nad.group==g].value.values, ref, equal_var=False).pvalue if g!='Vaccine' else np.nan for g in R.group]
R['mean_loss_pct'] = 100-R.mean_nadir
n10 = w[w.time==10].groupby('group').size()
R['n_day10'] = R.group.map(n10)
print(R.round(3).to_string()); R.to_csv('/tmp/work/reactogenicity.csv',index=False)
# day-10 missing animal in PSLN-212/R848
print(w[(w.group=='PSLN-212/R848')].pivot(index='time',columns='rep',values='value'))
