"""
Analysis 5 - post-challenge body weight (morbidity), using only real observations.
Dead animals are NOT averaged: BLANK cells are missing and LOCF runs (see audit_02) are truncated at the first
value of the run.  Per-animal nadir is therefore the lowest weight actually measured.
Outputs: challenge_morbidity.csv, challenge_morbidity_tests.csv, weight_naive_vs_decoded_means.csv
"""
import numpy as np, pandas as pd
from scipy import stats
from audit_02_survival_vs_weight import decode_weights, pairs
from psln_blocks import df
pd.set_option('display.width',260); pd.set_option('display.max_rows',900)
f=lambda v:f'{v:.3g}'
rows=[]; tests=[]; naive=[]
for sb,wb_,desc in pairs:
    w=decode_weights(wb_)
    for g,a in w.groupby('group',sort=False):
        surv=a[a['mode']=='survivor']
        rows.append(dict(weight_block=wb_,survival_block=sb,design=desc,group=g,n=len(a),exits=int((a['mode']!='survivor').sum()),
                         mean_nadir_all=a.nadir.mean(),sd_nadir_all=a.nadir.std(ddof=1),
                         mean_nadir_survivors=surv.nadir.mean() if len(surv) else np.nan,worst_survivor_nadir=surv.nadir.min() if len(surv) else np.nan,
                         median_nadir_day_survivors=surv.nadir_day.median() if len(surv) else np.nan,
                         mean_day14_survivors=surv.day14.mean() if len(surv) else np.nan,n_survivors_below_95_at_d14=int((surv.day14<95).sum()) if len(surv) else 0))
    G={g:a for g,a in w.groupby('group',sort=False)}
    for g1,g2 in [('PSLN-344','PSLN-212(Y)'),('PSLN-344Y','PSLN-212Y'),('PSLN-344','Sham'),('3d Vaccine+PSLN-344','3d Vaccine')]:
        if g1 in G and g2 in G:
            a=G[g1][G[g1]['mode']=='survivor']; b=G[g2][G[g2]['mode']=='survivor']
            if len(a)>1 and len(b)>1:
                t=stats.ttest_ind(a.nadir,b.nadir,equal_var=False)
                tests.append(dict(weight_block=wb_,g1=g1,g2=g2,nadir1_survivors=a.nadir.mean(),nadir2_survivors=b.nadir.mean(),diff=a.nadir.mean()-b.nadir.mean(),welch_p=t.pvalue,n1=len(a),n2=len(b),
                                  d14_1=a.day14.mean(),d14_2=b.day14.mean(),d14_p=stats.ttest_ind(a.day14,b.day14,equal_var=False).pvalue))
    # what a naive column-mean would give at day 14 versus survivors only
    x=df[(df.block==wb_)]
    for g,a in x.groupby('group',sort=False):
        last=a[a.time==a.time.max()].value
        ww=w[w.group==g]
        naive.append(dict(weight_block=wb_,group=g,naive_day14_mean_of_printed_cells=last.mean() if len(last) else np.nan,n_cells_at_d14=len(last),
                          survivors_only_day14_mean=ww[ww['mode']=='survivor'].day14.mean(),n_survivors=int((ww['mode']=='survivor').sum()),n_LOCF_cells_included_in_naive=int((ww['mode']=='LOCF').sum())))
R=pd.DataFrame(rows); T=pd.DataFrame(tests); N=pd.DataFrame(naive)
R.to_csv('challenge_morbidity.csv',index=False); T.to_csv('challenge_morbidity_tests.csv',index=False); N.to_csv('weight_naive_vs_decoded_means.csv',index=False)
print(R.drop(columns=['design','survival_block']).to_string(float_format=f)); print(); print(T.to_string(float_format=f)); print()
print(N[N.n_LOCF_cells_included_in_naive>0].to_string(float_format=f))
