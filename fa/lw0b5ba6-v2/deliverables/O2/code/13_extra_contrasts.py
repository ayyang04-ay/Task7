import pandas as pd, numpy as np, warnings
from scipy import stats
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
warnings.filterwarnings('ignore')
CC=pd.read_csv('/tmp/work/tidy/continuous.csv'); CC["time"]=CC["time"].astype(str)
CC.loc[CC.block.isin(['S03-C','S03-G'])&(CC.value<10),'value']=5.0
out=[]
# two-way ANOVA (group x time) for time-course blocks
for blk,meas,log in [('S01-D','monocytes',False),('S01-E','CD11b+ DC',False),('S02-F','Gm-csf',True),('S07-A','Ly6C+CCR2+',False),('S11-D','NK',False)]:
    d=CC[(CC.block==blk)&(CC.measurand.str.contains(meas,regex=False))].copy()
    d['y']=np.log10(d.value) if log else d.value
    m=smf.ols('y ~ C(group)*C(time)',data=d).fit(); a=anova_lm(m,typ=2)
    out.append(dict(analysis='two-way ANOVA',block=blk,measurand=d.measurand.iloc[0],scale='log10' if log else 'linear',
                    p_group=a.loc['C(group)','PR(>F)'],p_time=a.loc['C(time)','PR(>F)'],p_interaction=a.loc['C(group):C(time)','PR(>F)']))
TW=pd.DataFrame(out); print(TW.to_string(index=False)); TW.to_csv('/tmp/work/tables/two_way_anova.csv',index=False)
# selected extra pairwise contrasts
K=pd.read_csv('/tmp/work/tables/continuous_contrasts.csv')
sel=K[K.contrast.isin(['PSLN-344(Y) vs PSLN-212(Y)','PSLN-212 vs CMP-204','PSLN-344 vs CMP-204','CMP-204 vs Sham','PSLN-212 vs Sham'])&K.excluded.isna()]
pd.set_option('display.width',220)
print(sel[['block','measurand','time','contrast','mean_a','mean_b','est','lo','hi','tukey_p','welch_p']].round(3).to_string(index=False))
# R848 comparisons in S01-A and S09-A panel1 (Tnf/Il10) and S08-A
rows=[]
def cmp(block,meas,time,a,b,log=True):
    d=CC[(CC.block==block)&(CC.measurand.str.contains(meas,regex=False))&(CC.time==time)]
    va=d[d.group==a].value.values; vb=d[d.group==b].value.values
    if block.startswith('S09-A'): va,vb=10**va,10**vb
    la,lb=(np.log10(va),np.log10(vb)) if log else (va,vb)
    grp=d.group.values; y=np.log10(10**d.value.values if block.startswith('S09-A') else d.value.values)
    tk=pairwise_tukeyhsd(y,grp); tab=pd.DataFrame(tk.summary().data[1:],columns=tk.summary().data[0])
    r=tab[((tab.group1==a)&(tab.group2==b))|((tab.group1==b)&(tab.group2==a))]
    rows.append(dict(block=block,measurand=meas,time=time,a=a,b=b,gm_a=10**la.mean(),gm_b=10**lb.mean(),GMR=10**(la.mean()-lb.mean()),tukey_p=float(r['p-adj'].iloc[0])))
cmp('S01-A','Ifnb1','16h','PSLN-212/R848','PSLN-344'); cmp('S01-A','Ifnb1','16h','PSLN-212/R848','PSLN-212'); cmp('S01-A','Ifnb1','16h','PSLN-R848','PSLN-212')
for an in ['Tnf','Il10','Il6']:
    cmp('S09-A panel1 (cols B-V)',an,'16h (as printed)','PSLN-212/R848','PSLN-344'); cmp('S09-A panel1 (cols B-V)',an,'16h (as printed)','PSLN-R848','PSLN-344')
for dose in ['10','20','40']:
    cmp('S08-A','Ifnb1',dose,'PSLN-344/R848','PSLN-344')
R=pd.DataFrame(rows); print(R.round(4).to_string(index=False)); R.to_csv('/tmp/work/tables/r848_contrasts.csv',index=False)
