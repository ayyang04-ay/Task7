import pandas as pd, numpy as np
pd.set_option('display.width', 330); pd.set_option('display.max_rows', 3000); pd.set_option('display.max_colwidth', 46)
D = pd.read_csv('desc_stats.csv'); P = pd.read_csv('pairwise_stats.csv')
D['time']=D['time'].astype(str); P['time']=P['time'].astype(str)
norm = {'PSLN-212Y':'PSLN-212(Y)','PSLN-212(y)':'PSLN-212(Y)','PSLN-344Y':'PSLN-344(Y)','PBS':'PBS','Vaccine':'Vaccine'}
D['g'] = D.group.replace(norm); P['A2']=P.A.replace(norm); P['B2']=P.B.replace(norm)
rows=[]
for (blk, an, t), d in D.groupby(['block','analyte','time'], sort=False):
    use_gm = d.geomean.notna().all()
    val = (d.set_index('g').geomean if use_gm else d.set_index('g')['mean'])
    r = dict(block=blk, analyte=an, time=t, stat=('GM' if use_gm else 'mean'))
    for g in ['Sham','PBS','Vaccine','CMP-204','PSLN-212','PSLN-344','PSLN-212(Y)','PSLN-344(Y)']:
        r[g] = val.get(g, np.nan)
    p = P[(P.block==blk)&(P.analyte==an)&(P.time==t)]
    def pair(a,b):
        x = p[((p.A2==a)&(p.B2==b))]
        if len(x): return x.iloc[0].effect, x.iloc[0].ci_lo, x.iloc[0].ci_hi, x.iloc[0].p_tukey, x.iloc[0].p_welch, x.iloc[0].p_mwu_exact, x.iloc[0].effect_type
        x = p[((p.A2==b)&(p.B2==a))]
        if len(x):
            e=x.iloc[0]
            if e.scale=='log10': return 1/e.effect, 1/e.ci_hi, 1/e.ci_lo, e.p_tukey, e.p_welch, e.p_mwu_exact, e.effect_type
            return -e.effect, -e.ci_hi, -e.ci_lo, e.p_tukey, e.p_welch, e.p_mwu_exact, e.effect_type
        return (np.nan,)*6+('',)
    e = pair('PSLN-212','PSLN-344'); r.update({'344v212_eff':e[0],'344v212_lo':e[1],'344v212_hi':e[2],'344v212_pTukey':e[3],'344v212_pWelch':e[4],'344v212_pMWU':e[5],'eff_type':e[6]})
    e = pair('PSLN-212(Y)','PSLN-344'); r.update({'344vYoung_eff':e[0],'344vYoung_lo':e[1],'344vYoung_hi':e[2],'344vYoung_pTukey':e[3],'344vYoung_pWelch':e[4]})
    e = pair('PSLN-212(Y)','PSLN-212'); r.update({'212vYoung_eff':e[0],'212vYoung_pTukey':e[3],'212vYoung_pWelch':e[4]})
    e = pair('Sham','PSLN-212'); r.update({'212vSham_eff':e[0],'212vSham_pTukey':e[3],'212vSham_pWelch':e[4]})
    e = pair('Sham','PSLN-344'); r.update({'344vSham_eff':e[0],'344vSham_pTukey':e[3],'344vSham_pWelch':e[4]})
    rows.append(r)
SC = pd.DataFrame(rows)
SC.to_csv('scorecard.csv', index=False)
show = SC[SC['PSLN-344'].notna() & SC['PSLN-212'].notna()].copy()
def f(x):
    if pd.isna(x): return ''
    ax=abs(x)
    if ax>=1000: return f"{x:.0f}"
    if ax>=100: return f"{x:.0f}"
    if ax>=10: return f"{x:.1f}"
    return f"{x:.2f}"
def pf(x):
    if pd.isna(x): return ''
    return f"{x:.1e}" if x<0.001 else f"{x:.3f}"
out = pd.DataFrame({'block':show.block,'analyte':show.analyte.str.slice(0,44),'t':show.time,'st':show.stat,
  'Sham':show['Sham'].fillna(show['PBS']).fillna(show['Vaccine']).map(f),'CMP204':show['CMP-204'].map(f),'P212':show['PSLN-212'].map(f),'P344':show['PSLN-344'].map(f),'Y212':show['PSLN-212(Y)'].map(f),'Y344':show['PSLN-344(Y)'].map(f),
  '344v212':show['344v212_eff'].map(f),'CI':show.apply(lambda r: f"[{f(r['344v212_lo'])},{f(r['344v212_hi'])}]",axis=1),'pTuk':show['344v212_pTukey'].map(pf),'pWel':show['344v212_pWelch'].map(pf),'pMWU':show['344v212_pMWU'].map(pf),
  '344vY':show['344vYoung_eff'].map(f),'pTukY':show['344vYoung_pTukey'].map(pf),'212vY':show['212vYoung_eff'].map(f),'pTuk212Y':show['212vYoung_pTukey'].map(pf),'212vSham_p':show['212vSham_pTukey'].map(pf)})
print(out.to_string(index=False))
