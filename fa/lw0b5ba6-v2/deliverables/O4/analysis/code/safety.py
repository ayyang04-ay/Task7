import pandas as pd, numpy as np, warnings
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
warnings.filterwarnings('ignore')
vals = pd.read_csv('values_corrected.csv'); bw = pd.read_csv('bw.csv')
pd.set_option('display.width',250)
# ---- 1. S09-A block-2 timepoint: compare log10 Ifnb1 group means with S01-A 16h and 72h ----
def gm(block, an='Ifnb1', log=False):
    d = vals[vals.block==block]
    if 'analyte' in d and an: d = d[(d.analyte==an)|(d.analyte.isna())]
    y = d.value if log else np.log10(d.value)
    return d.assign(y=y).groupby('g').y.mean()
b1 = gm('S09-A_blk1(cols A-U)', log=True); b2 = gm('S09-A_blk2(cols X-AS)', log=True)
a16 = gm('S01-A_16h'); a72 = gm('S01-A_72h')
a16.index = a16.index.str.replace('Sham','PBS'); a72.index = a72.index.str.replace('Sham','PBS')
common = [g for g in b1.index if g in a16.index and g!='PBS']
tab = pd.DataFrame({'S09A_blk1':b1[common],'S09A_blk2':b2[common],'S01A_16h':a16[common],'S01A_72h':a72[common]})
print('log10 Ifnb1 group means (PBS/Sham excluded):'); print(tab.round(2))
for x in ['S09A_blk1','S09A_blk2']:
    for y in ['S01A_16h','S01A_72h']:
        r = np.corrcoef(tab[x],tab[y])[0,1]; mad = (tab[x]-tab[y]).abs().mean()
        print(f'  {x} vs {y}: r={r:.2f}, mean |diff| = {mad:.2f} log10')
tab.to_csv('/tmp/outputs/analysis/T5_S09A_timepoint_check.csv')
# ---- 2. lung cytokines at 16 h (block 1, label-consistent) PSLN-344 vs PSLN-212 ----
d = vals[vals.block=='S09-A_blk1(cols A-U)']
rows=[]
for an in ['Ifnb1','Il6','Ccl2','Ccl3','Ccl5','Tnf','Il10']:
    x = d[(d.analyte==an)]
    g = x.groupby('g').value
    a = g.get_group('PSLN-344'); b = g.get_group('PSLN-212'); y = g.get_group('PSLN-212(Y)'); p0 = g.get_group('PBS'); r8 = g.get_group('PSLN-212/R848')
    t,p = stats.ttest_ind(a,b,equal_var=False)
    rows.append(dict(analyte=an, PBS=10**p0.mean(), PSLN212=10**b.mean(), PSLN344=10**a.mean(), PSLN212_young=10**y.mean(), PSLN212_R848=10**r8.mean(),
                     ratio_344_vs_212=10**(a.mean()-b.mean()), welch_p=p, ratio_344aged_vs_212young=10**(a.mean()-y.mean()),
                     cells=f"{x.cell.iloc[0]}..{x.cell.iloc[-1].split('!')[1]}"))
cyt = pd.DataFrame(rows); print('\nLung transcripts 16 h (S09-A block 1; fold vs untreated, geometric means, n=3):'); print(cyt.round(3).to_string())
cyt.to_csv('/tmp/outputs/analysis/T6_lung_cytokines_16h.csv', index=False)
# ---- 3. CNS transcripts S10-A ----
rows=[]
for blk,an in [('S10-A_Ifnb1','Ifnb1'),('S10-A_Tnf','Tnf'),('S10-A_Isg15','Isg15')]:
    x = vals[vals.block==blk]; g = x.groupby('g').value
    tk = pairwise_tukeyhsd(x.value, x.g); tdf = pd.DataFrame(tk.summary().data[1:], columns=tk.summary().data[0])
    def tp(a,b):
        r = tdf[((tdf.group1==a)&(tdf.group2==b))|((tdf.group1==b)&(tdf.group2==a))]; return float(r['p-adj'].iloc[0])
    a = g.get_group('PSLN-344'); s = g.get_group('Sham'); pb = g.get_group('PBS'); ct = g.get_group('CT')
    rows.append(dict(analyte=an, PBS=f"{pb.mean():.2f}±{pb.std():.2f}", Sham=f"{s.mean():.2f}±{s.std():.2f}", PSLN344=f"{a.mean():.2f}±{a.std():.2f}", CT=f"{ct.mean():.2f}±{ct.std():.2f}",
                     tukey_p_344_vs_sham=tp('PSLN-344','Sham'), tukey_p_344_vs_PBS=tp('PSLN-344','PBS'), tukey_p_CT_vs_sham=tp('CT','Sham'),
                     welch_p_344_vs_sham=stats.ttest_ind(a,s,equal_var=False)[1], cells=f"{x.cell.iloc[0]}..{x.cell.iloc[-1].split('!')[1]}"))
cns = pd.DataFrame(rows); print('\nCNS transcripts 36 h (S10-A; mean±SD, n=5):'); print(cns.to_string())
cns.to_csv('/tmp/outputs/analysis/T7_CNS_transcripts.csv', index=False)
# ---- 4. post-vaccination weight S08-D ----
b = bw[bw.block=='S08-D'].copy()
piv = b.pivot_table(index='day', columns='group', values='value', aggfunc='mean')
nad = b.groupby(['group','animal']).value.min().groupby('group').agg(['mean','min'])
cnt = b.dropna(subset=['value']).groupby(['group','day']).animal.nunique().unstack(0)
print('\nS08-D post-vaccination body weight (% of day 0), group means by day:'); print(piv.round(1).to_string())
print('\nper-group nadir (mean of per-animal minima; worst animal):'); print(nad.round(1))
print('\nanimals with a recorded weight by day:'); print(cnt.to_string())
# stats on nadir
na = b.groupby(['group','animal']).value.min().reset_index()
tk = pairwise_tukeyhsd(na.value, na.group); print(tk.summary())
piv.round(2).to_csv('/tmp/outputs/analysis/T8_postvaccination_bodyweight.csv')
