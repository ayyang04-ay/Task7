import pandas as pd, numpy as np
from scipy import stats
R=pd.read_csv('continuous_results.csv')
k='PSLN-344 vs PSLN-212'
R=R[~R[f'{k}|welch_p'].isna()].copy()
flagged={'S11-A','S11-B','S03-B','S03-F','S08-C','S09-A_blk2(Y:AS)','S05-A','S05-B','S02-E','S10-A_Ifnb1','S10-A_Tnf','S10-A_Isg15'}
R['flagged']=R.block.isin(flagged)
R['dir_fav']=np.where(R.readout.str.contains('Tfr|Treg|cDC2|CD206'), -1, 1)  # expected direction
eff=np.where(R['transform']=='log', np.log10(R[f'{k}|ratio'].fillna(1)), R[f'{k}|diff'].fillna(0))
eff=np.where(R.readout.str.contains('log10 fold'), np.log10(R[f'{k}|ratio']), eff)
R['fav']=np.sign(eff)==R.dir_fav
R['sig_tukey']=R[f'{k}|tukey_p']<0.05
R['sig_welch']=R[f'{k}|welch_p']<0.05
efficacy=R[~R.readout.str.startswith('CNS')]
for lab,d in [('all efficacy readouts',efficacy),('excluding integrity-flagged blocks',efficacy[~efficacy.flagged])]:
    print(f"{lab}: n={len(d)}; favourable direction {d.fav.sum()}; significant & favourable (Welch) {(d.fav&d.sig_welch).sum()}; (Tukey, where >2 groups) {(d.fav&d.sig_tukey).sum()}")
print(efficacy[~(efficacy.fav&efficacy.sig_welch)][['readout','block',f'{k}|welch_p',f'{k}|tukey_p','fav']].to_string(index=False))

# terminal digit check on 2-dp values (flow/qPCR) - last digit uniformity
t=pd.read_csv('tidy.csv')
vals=t.value[(t.value*100%1==0)&(t.value*10%1!=0)]   # exactly 2 decimals, non-zero 2nd decimal
ld=(np.round(vals*100)%10).astype(int)
obs=np.bincount(ld,minlength=10)[1:]   # digits 1..9 (0 excluded by construction)
chi=stats.chisquare(obs)
print("\nterminal digit (2nd decimal, digits 1-9) counts:",obs.tolist()," chi2 p=%.3f"%chi.pvalue)

# ---- sample size for replication (two-sided alpha 0.05, power 0.9), Fisher/arcsine approx & log-rank (Schoenfeld)
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize
for p1,p2,lab in [(0.80,0.11,'Tier B observed (80% vs 11%)'),(0.60,0.15,'conservative: half the observed gap (~60% vs ~15%)'),(0.50,0.20,'very conservative (50% vs 20%)')]:
    es=proportion_effectsize(p1,p2); n=NormalIndPower().solve_power(es,alpha=0.05,power=0.9,ratio=1)
    # Schoenfeld log-rank: events needed = 4*(z_a+z_b)^2 / (log HR)^2 ; HR from exponential approx of survival at fixed time
    hr=np.log(p1)/np.log(p2)  # S1=exp(-l1 t) => HR=l1/l2
    z=stats.norm.ppf(0.975)+stats.norm.ppf(0.9); events=4*z**2/np.log(hr)**2
    pe=( (1-p1)+(1-p2) )/2; n_lr=events/pe/2
    print(f"{lab}: arcsine-approx n/arm={np.ceil(n):.0f}; log-rank (Schoenfeld) HR={hr:.2f}, events={events:.0f}, n/arm={np.ceil(n_lr):.0f}")
