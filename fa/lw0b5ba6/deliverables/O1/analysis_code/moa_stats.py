import pandas as pd, numpy as np, warnings
warnings.filterwarnings('ignore')
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multitest import multipletests
rng = np.random.default_rng(20261101)

df = pd.read_csv('/tmp/work/tidy.csv')
x = df[df.event.isna() & (df.unit!='% of d0') & (df.block!='S08-UNLABELLED')].copy()

# ---------- analysis scale ----------
LOG_BLOCKS = {'S01-A_16h','S01-A_72h','S02-F','S03-L_Aicda','S03-L_E47','S08-A','S10-A_Ifnb1','S10-A_Tnf','S10-A_Isg15',
              'S03-A','S03-E','S13-A','S13-B','S13-C','S13-D','S13-I','S13-J','S03-C','S03-D','S03-G','S03-H','S03-B','S03-F','S04-B_TfhTfr'}
HAI_LOD = {'S03-C':10,'S03-G':10}
def transform(block, v):
    v = np.asarray(v, dtype=float)
    if block in HAI_LOD:
        v = np.where(v < HAI_LOD[block], HAI_LOD[block]/2, v)   # below LoD -> half LoD
    if block in LOG_BLOCKS:
        return np.log10(v)
    return v
def back(block, m):
    return 10**m if block in LOG_BLOCKS else m

# ---------- corrected IgG2a/IgG1 from primary titres (S13) ----------
def vals(b,g): return df[(df.block==b)&(df.group==g)].sort_values('rep').value.values
extra=[]
for blk, a, b_ in [('S13-AB_ratio_CA09','S13-A','S13-B'),('S13-CD_ratio_Aichi','S13-C','S13-D')]:
    for g in ['PSLN-212','PSLN-344','PSLN-212(Y)']:
        r = vals(a,g)/vals(b_,g)
        for i,v in enumerate(r):
            extra.append(dict(block=blk, sheet='S13', group=g, age=('young' if '(Y)' in g else 'aged'), value=v,
                              cell=f'{a}/{b_} rep{i+1}', rep=i+1, time=np.nan, event=np.nan,
                              measurand=f'IgG2a/IgG1 recomputed from {a}/{b_} titres', unit='ratio', timepoint='day 14'))
x = pd.concat([x, pd.DataFrame(extra)], ignore_index=True)
LOG_BLOCKS |= {'S13-AB_ratio_CA09','S13-CD_ratio_Aichi'}

x['tkey'] = x.time.fillna(-1)
x['an'] = x['analyte'].fillna('')
summ=[]; contr=[]; tuk=[]; ri=[]
KEY = [('PSLN-344','PSLN-212'),('PSLN-344','Sham'),('PSLN-344','PSLN-212(Y)'),('PSLN-212','Sham'),('PSLN-212(Y)','PSLN-212'),
       ('PSLN-344','CMP-204'),('PSLN-212','CMP-204'),('PSLN-344','Vaccine'),('PSLN-212','Vaccine'),('PSLN-344','PBS'),('CT','PBS'),('PSLN-344','CT'),
       ('Sham','PBS'),('PSLN-344(Y)','PSLN-212(Y)'),('PSLN-212(y)','PSLN-212'),('PSLN-212/R848','PSLN-212'),('PSLN-344','PSLN-212/R848'),
       ('PSLN-344(Y)','PSLN-344'),('PTX','PSLN-344'),('PTX','PSLN-212(Y)'),('PSLN-344','PSLN-344/R848'),
       ('CBX+','CBX-'),('PSLN-344+INCB3344','PSLN-344'),('PSLN-344(Y)+INCB3344','PSLN-344(Y)'),('IFNAR-/- to WT','WT to WT'),
       ('PSLN-212+GM-CSF','PSLN-212'),('PSLN-212+GM-CSF','GM-CSF'),('IFN w/o cDC','WT w/o cDC'),('GMCSF','IFN w/o cDC'),('IFN w/ cDC','WT w/ cDC'),
       ('Lung+PTX','Lung'),('MLN+PTX','MLN'),('SPA/D','WT'),('AECII/PSLN-SRB','AECII/FreeSRB'),('AECI/PSLN-SRB','AECI/FreeSRB'),
       ('AECII-PSLN-344-SRB','AECII-PSLN-SRB'),('AECI-PSLN-344-SRB','AECI-PSLN-SRB'),('Ly6C-CD206+ MΦ [col C]','Ly6C-CD206+ MΦ [col B]')]
for (b,t,a), sub in x.groupby(['block','tkey','an'], sort=False):
    groups = list(dict.fromkeys(sub.group))
    tv = {g: transform(b, sub[sub.group==g].value.values) for g in groups}
    raw = {g: sub[sub.group==g].value.values for g in groups}
    for g in groups:
        v = tv[g]; n=len(v)
        m = v.mean(); sd = v.std(ddof=1) if n>1 else np.nan
        tcrit = stats.t.ppf(0.975, n-1) if n>1 else np.nan
        summ.append(dict(block=b, time=(None if t==-1 else t), analyte=a, group=g, n=n, raw_mean=raw[g].mean(), raw_sd=raw[g].std(ddof=1) if n>1 else np.nan,
                         raw_median=np.median(raw[g]), center=back(b,m), center_type=('geometric mean' if b in LOG_BLOCKS else 'mean'),
                         ci_lo=back(b, m - tcrit*sd/np.sqrt(n)) if n>1 else np.nan, ci_hi=back(b, m + tcrit*sd/np.sqrt(n)) if n>1 else np.nan,
                         scale=('log10' if b in LOG_BLOCKS else 'linear'), cells=f"{sub[sub.group==g].cell.iloc[0]}..{sub[sub.group==g].cell.iloc[-1]}",
                         measurand=sub.measurand.iloc[0], unit=sub.unit.iloc[0], timepoint=sub.timepoint.iloc[0]))
    # Tukey
    if len(groups)>=3 and all(len(tv[g])>=2 for g in groups):
        allv = np.concatenate([tv[g] for g in groups]); lab = np.concatenate([[g]*len(tv[g]) for g in groups])
        try:
            F = stats.f_oneway(*[tv[g] for g in groups])
            th = pairwise_tukeyhsd(allv, lab)
            res = pd.DataFrame(th._results_table.data[1:], columns=th._results_table.data[0])
            for _,r in res.iterrows():
                tuk.append(dict(block=b, time=(None if t==-1 else t), analyte=a, g1=r['group1'], g2=r['group2'], meandiff_scale=r['meandiff'], p_tukey=r['p-adj'], anova_F=F.statistic, anova_p=F.pvalue))
        except Exception as e:
            pass
    # key contrasts
    cc=[]
    for g1,g2 in KEY:
        if g1 in tv and g2 in tv and len(tv[g1])>=2 and len(tv[g2])>=2:
            w = stats.ttest_ind(tv[g1], tv[g2], equal_var=False)
            mw = stats.mannwhitneyu(raw[g1], raw[g2], alternative='two-sided')
            d = tv[g1].mean()-tv[g2].mean()
            eff = (10**d) if b in LOG_BLOCKS else d
            ratio_lin = raw[g1].mean()/raw[g2].mean() if raw[g2].mean()!=0 else np.nan
            cc.append(dict(block=b, time=(None if t==-1 else t), analyte=a, g1=g1, g2=g2, n1=len(tv[g1]), n2=len(tv[g2]),
                           effect=eff, effect_type=('ratio of geometric means' if b in LOG_BLOCKS else 'difference of means (units)'),
                           ratio_of_means=ratio_lin, welch_p=w.pvalue, mannwhitney_p=mw.pvalue))
    if cc:
        ps = [c['welch_p'] for c in cc]
        adj = multipletests(ps, method='holm')[1]
        for c,pa in zip(cc,adj): c['welch_p_holm_within_block']=pa
        contr.extend(cc)
    # restoration index
    if all(g in tv for g in ['PSLN-212','PSLN-344','PSLN-212(Y)']):
        a212, a344, y = tv['PSLN-212'], tv['PSLN-344'], tv['PSLN-212(Y)']
        def R(a212,a344,y):
            den = y.mean()-a212.mean()
            return (a344.mean()-a212.mean())/den if abs(den)>1e-12 else np.nan
        est = R(a212,a344,y)
        boots=[]
        for _ in range(5000):
            bb = R(rng.choice(a212,len(a212)), rng.choice(a344,len(a344)), rng.choice(y,len(y)))
            if np.isfinite(bb): boots.append(bb)
        lo,hi = np.percentile(boots,[2.5,97.5]) if boots else (np.nan,np.nan)
        gap_p = stats.ttest_ind(y, a212, equal_var=False).pvalue
        ri.append(dict(block=b, time=(None if t==-1 else t), analyte=a, RI=est, RI_lo=lo, RI_hi=hi, aged_young_gap_p=gap_p,
                       m212=back(b,a212.mean()), m344=back(b,a344.mean()), m212Y=back(b,y.mean()), scale=('log10' if b in LOG_BLOCKS else 'linear'),
                       measurand=sub.measurand.iloc[0]))

S = pd.DataFrame(summ); C = pd.DataFrame(contr); T = pd.DataFrame(tuk); RI = pd.DataFrame(ri)
S.to_csv('/tmp/work/summary_stats.csv',index=False); C.to_csv('/tmp/work/contrasts.csv',index=False)
T.to_csv('/tmp/work/tukey.csv',index=False); RI.to_csv('/tmp/work/restoration_index.csv',index=False)
pd.set_option('display.width',320); pd.set_option('display.max_colwidth',50); pd.set_option('display.max_rows',500)
print(RI[['block','time','analyte','m212','m344','m212Y','RI','RI_lo','RI_hi','aged_young_gap_p']].round(3).to_string())
