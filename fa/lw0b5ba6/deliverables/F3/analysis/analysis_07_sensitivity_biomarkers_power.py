"""
Analysis 7
 (a) survival sensitivity: replace each survival table by the outcome implied by its paired body-weight table;
     and a deliberately adverse bound (most PSLN-344 deaths / fewest PSLN-212 deaths from either source)
 (b) biomarker separation between protected arms (aged PSLN-344, young PSLN-212) and unprotected arms (aged PSLN-212, Sham)
 (c) sample sizes for the proposed confirmatory studies (exact Fisher power)
Outputs: survival_sensitivity.csv, biomarker_separation.csv, power_table.csv
"""
import numpy as np, pandas as pd, math, itertools
from scipy import stats
from statsmodels.stats.proportion import proportion_confint
pd.set_option('display.width',260); pd.set_option('display.max_rows',900); pd.set_option('display.max_colwidth',70)
f=lambda v:f'{v:.3g}'
per=pd.read_csv('survival_per_experiment.csv'); w=pd.read_csv('weights_decoded_per_animal.csv'); d=pd.read_csv('tidy_all_observations.csv')

# ---------- (a) ------------------------------------------------------------------------------------------
aged=['S03-I','S03-J','S06-A','S06-B','S06-C','S06-D','S06-E(r34)','S06-F(r34)','S06-G','S15-L','S15-N']
rows=[]
for b in aged:
    for arm in ['PSLN-344','PSLN-212','Sham','PSLN-212(Y)']:
        p=per[(per.block==b)&(per.arm==arm)]
        ww=w[(w.paired_survival_block==b)&(w.group.str.strip()==arm)]
        rows.append(dict(block=b,arm=arm,table_n=(int(p.n.iloc[0]) if len(p) else np.nan),table_surv=(int(p.survivors.iloc[0]) if len(p) else np.nan),
                         weight_n=(len(ww) if len(ww) else np.nan),weight_surv=(int((ww['mode']=='survivor').sum()) if len(ww) else np.nan)))
S=pd.DataFrame(rows)
S['agree']=S.table_surv==S.weight_surv
S.to_csv('survival_table_vs_weight_by_arm.csv',index=False)
print(S.to_string())
def tot(col_s,col_n,arm,blocks):
    x=S[(S.arm==arm)&S.block.isin(blocks)&S[col_n].notna()]
    k=int(x[col_s].sum()); n=int(x[col_n].sum()); lo,hi=proportion_confint(k,n,method='beta'); return k,n,100*k/n,100*lo,100*hi
out=[]
for name,blocks in [('all 11 blocks',aged),('excluding S06-C',[b for b in aged if b!='S06-C']),('excluding S06-C, S03-I, S03-J (the three with label/duplication problems)',[b for b in aged if b not in('S06-C','S03-I','S03-J')])]:
    for arm in ['PSLN-344','PSLN-212','Sham','PSLN-212(Y)']:
        k,n,p,lo,hi=tot('table_surv','table_n',arm,blocks); out.append(dict(scenario=name,source='survival tables as printed',arm=arm,surv=f'{k}/{n}',pct=p,lo=lo,hi=hi))
        if arm in('PSLN-212','Sham'):
            bl=[b for b in blocks if b!='S03-J']      # S13-G carries different group labels; cannot be mapped
            k,n,p,lo,hi=tot('weight_surv','weight_n',arm,bl); out.append(dict(scenario=name+' (weight tables; S03-J/S13-G comparator arms unmapped)',source='implied by body-weight tables',arm=arm,surv=f'{k}/{n}',pct=p,lo=lo,hi=hi))
        else:
            k,n,p,lo,hi=tot('weight_surv','weight_n',arm,blocks); out.append(dict(scenario=name,source='implied by body-weight tables',arm=arm,surv=f'{k}/{n}',pct=p,lo=lo,hi=hi))
# adverse bound
x=S[S.block.isin([b for b in aged if b!='S06-C'])]
a=x[x.arm=='PSLN-344']; k=int(np.minimum(a.table_surv,a.weight_surv.fillna(a.table_surv)).sum()); n=int(a.table_n.sum()); lo,hi=proportion_confint(k,n,method='beta')
out.append(dict(scenario='ADVERSE BOUND excl. S06-C: fewest PSLN-344 survivors from either source',source='min(table, weights)',arm='PSLN-344',surv=f'{k}/{n}',pct=100*k/n,lo=100*lo,hi=100*hi))
a=x[x.arm=='PSLN-212'].copy(); a.loc[a.block=='S03-J','weight_surv']=5   # if S13-G "Sham" (5 alive at d14) is in fact the PSLN-212 arm
k2=int(np.maximum(a.table_surv,a.weight_surv.fillna(a.table_surv)).sum()); n2=int(a.table_n.sum()); lo,hi=proportion_confint(k2,n2,method='beta')
out.append(dict(scenario='ADVERSE BOUND excl. S06-C: most PSLN-212 survivors from either source',source='max(table, weights)',arm='PSLN-212',surv=f'{k2}/{n2}',pct=100*k2/n2,lo=100*lo,hi=100*hi))
p=stats.fisher_exact([[k,n-k],[k2,n2-k2]])[1]
out.append(dict(scenario='ADVERSE BOUND: PSLN-344 vs PSLN-212 (unstratified Fisher)',source='',arm='',surv=f'{k}/{n} vs {k2}/{n2}',pct=100*(k/n-k2/n2),lo=np.nan,hi=np.nan,fisher_p=p))
O=pd.DataFrame(out); O.to_csv('survival_sensitivity.csv',index=False); print(); print(O.to_string(float_format=f))

# ---------- (b) ------------------------------------------------------------------------------------------
imm=pd.read_csv('immunology_descriptives.csv')
rows=[]
for blk,a in imm.groupby('block',sort=False):
    gs=set(a.group)
    if not {'PSLN-212','PSLN-344','PSLN-212(Y)','Sham'}<=gs: continue
    vals={g:np.array([float(v) for v in a[a.group==g]['values'].iloc[0].split()]) for g in ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']}
    prot=np.r_[vals['PSLN-344'],vals['PSLN-212(Y)']]; unprot=np.r_[vals['Sham'],vals['PSLN-212']]
    u=stats.mannwhitneyu(prot,unprot).statistic/(len(prot)*len(unprot)); auc=max(u,1-u); higher=u>=0.5
    if higher: gap_lo=unprot.max(); gap_hi=prot.min(); sep=gap_hi>gap_lo
    else: gap_lo=prot.max(); gap_hi=unprot.min(); sep=gap_hi>gap_lo
    # aged-only: PSLN-344 vs PSLN-212
    u2=stats.mannwhitneyu(vals['PSLN-344'],vals['PSLN-212']).statistic/(len(vals['PSLN-344'])*len(vals['PSLN-212'])); auc2=max(u2,1-u2)
    rows.append(dict(block=blk,measurand=a.measurand.iloc[0],direction=('higher in protected' if higher else 'lower in protected'),
                     AUC_protected_vs_unprotected=auc,complete_separation=sep,
                     unprotected_extreme=(unprot.max() if higher else unprot.min()),protected_extreme=(prot.min() if higher else prot.max()),
                     AUC_aged344_vs_aged212=auc2,n_per_group=len(vals['PSLN-344'])))
Bm=pd.DataFrame(rows); Bm.to_csv('biomarker_separation.csv',index=False); print(); print(Bm.to_string(float_format=f))

# ---------- (c) ------------------------------------------------------------------------------------------
def fisher_power(p1,p2,n,alpha=0.05):
    pw=0.0
    for k1 in range(n+1):
        a=stats.binom.pmf(k1,n,p1)
        if a<1e-12: continue
        for k2 in range(n+1):
            b=stats.binom.pmf(k2,n,p2)
            if b<1e-12: continue
            if stats.fisher_exact([[k1,n-k1],[k2,n-k2]])[1]<alpha: pw+=a*b
    return pw
def n_for(p1,p2,target=0.9):
    for n in range(4,200):
        if fisher_power(p1,p2,n)>=target: return n,fisher_power(p1,p2,n)
    return None,None
rows=[]
for lab,p1,p2 in [('PSLN-344 vs PSLN-212 in aged mice (observed 84% vs 12%)',0.84,0.12),
                  ('PSLN-344 vs an active comparator achieving 50% survival',0.84,0.50),
                  ('PSLN-344 vs an active comparator achieving 60% survival',0.84,0.60),
                  ('Day-60 durability: PSLN-344 (observed 67%) vs PSLN-212 (5%)',0.67,0.05),
                  ('Lower dose retaining efficacy: detect a drop from 84% to 50%',0.84,0.50),
                  ('Conservative planning: true PSLN-344 survival 70% vs comparator 15%',0.70,0.15)]:
    for tg in (0.8,0.9):
        n,pw=n_for(p1,p2,tg); rows.append(dict(comparison=lab,p1=p1,p2=p2,target_power=tg,n_per_group=n,achieved_power=pw))
# continuous: log2 titre, SD from data
im=pd.read_csv('tidy_all_observations.csv')
sds=[]
for blk in ['S03-C','S03-G','S03-D','S03-H']:
    for g in ['PSLN-212','PSLN-344','PSLN-212(Y)']:
        v=im[(im.block==blk)&(im.group==g)].value.values; sds.append(np.log2(v).std(ddof=1))
sd=float(np.sqrt(np.mean(np.square(sds))))
from statsmodels.stats.power import TTestIndPower
for fold in (2,4):
    for tg in (0.8,0.9):
        n=TTestIndPower().solve_power(effect_size=np.log2(fold)/sd,alpha=0.05,power=tg)
        rows.append(dict(comparison=f'HAI / neutralising titre: detect a {fold}-fold GMT difference (pooled within-group SD {sd:.2f} log2, from S03-C/D/G/H)',p1=np.nan,p2=np.nan,target_power=tg,n_per_group=math.ceil(n),achieved_power=tg))
P=pd.DataFrame(rows); P.to_csv('power_table.csv',index=False); print(); print(P.to_string(float_format=f))
