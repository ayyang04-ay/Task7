import pandas as pd, numpy as np
from scipy import stats
exec(open('survstats.py').read().split("meta = {")[0])   # reuse functions + surv loading
def counts(b,g, override=None):
    t,e = arr(b,g); n=len(t); s=int((e==0).sum())
    if override and (b,g) in override: s = override[(b,g)]
    return s,n
def mh_rd(strata):
    # strata: list of (s1,n1,s0,n0); Mantel-Haenszel risk difference (survival) with Greenland-Robins (1985) variance
    num=den=0.0; var_num=0.0
    for s1,n1,s0,n0 in strata:
        N=n1+n0; w=n1*n0/N
        num += (s1*n0 - s0*n1)/N; den += w
        # Sato (1989) variance component
    rd = num/den
    # Greenland-Robins variance
    P=Q=0.0
    for s1,n1,s0,n0 in strata:
        N=n1+n0
        P += (n1**2*s0 - n0**2*s1 + n1*n0*(n0-n1)/2)/N**2
        Q += (s1*(n0-s0) + s0*(n1-s1))/(2*N)
    var = (rd*P + Q)/den**2
    se = np.sqrt(var); return rd, rd-1.96*se, rd+1.96*se
def analyse(name, exps, g1='PSLN-344', g0='PSLN-212', override=None, note=''):
    strata=[]; lr=[]
    for b in exps:
        if isinstance(b,tuple): b,gg1,gg0 = b
        else: gg1,gg0 = g1,g0
        s1,n1 = counts(b,gg1,override); s0,n0 = counts(b,gg0,override)
        strata.append((s1,n1,s0,n0))
        t1,e1 = arr(b,gg1); t0,e0 = arr(b,gg0)
        if override and (b,gg0) in override:   # reconstruct e0 with extra survivors (censor latest deaths)
            k = override[(b,gg0)] - int((e0==0).sum())
            if k>0:
                idx = np.argsort(-t0*(e0==1))[:k]; e0=e0.copy(); t0=t0.copy(); e0[idx]=0; t0[idx]=14
        lr.append((t1,e1,t0,e0))
    S1=sum(x[0] for x in strata); N1=sum(x[1] for x in strata); S0=sum(x[2] for x in strata); N0=sum(x[3] for x in strata)
    rd,lo,hi = mh_rd(strata)
    chi,p,O,E = strat_lr(lr)
    return dict(analysis=name, experiments=len(exps), arm1=f"{S1}/{N1} ({100*S1/N1:.0f}%)", arm0=f"{S0}/{N0} ({100*S0/N0:.0f}%)",
                MH_risk_diff_pct=f"{100*rd:.0f} (95% CI {100*lo:.0f} to {100*hi:.0f})", strat_logrank_chi2=round(chi,1), p=f"{p:.1e}", note=note)
aged_all = ['S03-I','S03-J','S06-A','S06-B','S06-C','S06-D','S06-E','S06-F','S06-G','S15-L','S15-N']
dedup = [x for x in aged_all if x!='S06-D']
restricted = ['S06-A','S06-B','S06-F','S15-L','S15-N']
# conservative reconciliation: where BW-inferred deaths disagree, take the count LESS favourable to PSLN-344 / MORE favourable to PSLN-212
ov = {('S03-I','PSLN-212'):3, ('S06-E','PSLN-212'):1}
consv = [x for x in dedup if x!='S03-J']
res=[]
res.append(analyse('A. All aged challenge experiments as recorded (PSLN-344 vs PSLN-212)', aged_all))
res.append(analyse('B. De-duplicated (S06-D removed: exact copy of S06-C)', dedup))
res.append(analyse('C. B + BW-reconciled worst case for PSLN-344; S03-J removed', consv, override=ov, note='PSLN-212 survivors raised: S03-I 0->3, S06-E 0->1 (per S13-F/S15-E body-weight records)'))
res.append(analyse('D. Restricted: only experiments whose 344/212 survival agrees with body-weight records', restricted))
res.append(analyse('E. 14-month animals (imprinting study), both strata', [('S06-E2_imprint','Naive+PSLN-344','Naive+PSLN-212'),('S06-E2_imprint','Imprinting+PSLN-344','Imprinting+PSLN-212'),('S06-F2_imprint','Naive+PSLN-344','Naive+PSLN-212'),('S06-F2_imprint','Imprinting+PSLN-344','Imprinting+PSLN-212')]))
res.append(analyse('F. PSLN-344 vs Sham, aged, de-duplicated', dedup, g0='Sham'))
ywith = [x for x in dedup if x not in ('S03-J',)]
res.append(analyse('G. Aged PSLN-344 vs YOUNG PSLN-212 (age-gap closure), de-duplicated', ywith, g0='PSLN-212(Y)'))
res.append(analyse('H. Aged PSLN-212 vs Sham, de-duplicated', dedup, g1='PSLN-212', g0='Sham'))
res.append(analyse('I. Aged PSLN-212 vs YOUNG PSLN-212 (age deficit), same 9 expts as G', ywith, g1='PSLN-212', g0='PSLN-212(Y)'))
out = pd.DataFrame(res)
pd.set_option('display.width',300); pd.set_option('display.max_colwidth',90)
print(out.to_string())
out.to_csv('/tmp/outputs/analysis/T3_pooled_survival.csv', index=False)
# restoration index
S = lambda exps,g: sum(counts(b,g)[0] for b in exps)/sum(counts(b,g)[1] for b in exps)
s344=S(ywith,'PSLN-344'); s212=S(ywith,'PSLN-212'); sy=S(ywith,'PSLN-212(Y)')
print(f"\nRestoration index (survival), {len(ywith)} expts: (aged344 {s344:.3f} - aged212 {s212:.3f}) / (young212 {sy:.3f} - aged212) = {(s344-s212)/(sy-s212):.2f}")
