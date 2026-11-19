"""Audit 4: blocks that can be recomputed from other blocks - do the printed labels reconcile?"""
import numpy as np, pandas as pd, itertools
from psln_blocks import df
pd.set_option('display.width',250)
def M(block):
    d=df[df.block==block]
    return {g:a.sort_values('rep').value.astype(float).values for g,a in d.groupby('group',sort=False)}

print('='*100); print('(1) IgG2a/IgG1 quotient: S03-B (H1N1) vs S13-A / S13-B ;  S03-F (H3N2) vs S13-C / S13-D')
for qb,nb,db,lab in [('S03-B','S13-A','S13-B','CA09 H1N1'),('S03-F','S13-C','S13-D','Aichi H3N2')]:
    q=M(qb); n=M(nb); d_=M(db)
    rec={g:n[g]/d_[g] for g in n}
    print(f'\n  {lab}: recomputed IgG2a/IgG1 per animal from {nb}/{db}:')
    for g in rec: print(f'     {g:12s}', np.round(rec[g],4), ' geo-mean=%.2f'%np.exp(np.log(rec[g]).mean()))
    print(f'  {qb} as printed:')
    for g in q: print(f'     {g:12s}', np.round(q[g],4), ' geo-mean=%.2f'%np.exp(np.log(q[g]).mean()))
    print('  which recomputed group does each printed column equal?')
    for g in q:
        for h in rec:
            if np.allclose(q[g],rec[h],atol=6e-4):
                print(f'     {qb} column printed as "{g}"  ==  {nb}/{db} ratio for "{h}"', '' if g==h else '  <-- LABEL DOES NOT MATCH')

print('\n'+'='*100); print('(2) Tfh:Tfr quotient S04-B vs Foxp3+ fraction S04-B')
f=M('S04-B Foxp3'); t=M('S04-B Tfh:Tfr')
for g in f:
    rec=(100-f[g])/f[g]
    print(f'   {g:12s} printed {np.round(t[g],4)}  recomputed (100-Foxp3)/Foxp3 {np.round(rec,4)}  match={np.allclose(rec,t[g],atol=6e-4)}')

print('\n'+'='*100); print('(3) S09-A (log10, n=3) vs S01-A (linear, n=5): Ifnb1 row')
d=df[(df.block.str.startswith('S09-A'))&(df.analyte=='Ifnb1')]
for blk in ['S09-A/panel1(A-V)','S09-A/panel2(X-AS)']:
    print('  ',blk,'(label printed on sheet: "S09-A 16h n=3 Log10")')
    for g,a in d[d.block==blk].groupby('group',sort=False):
        back=10**a.sort_values('rep').value.astype(float).values
        hits=[]
        for sb in ['S01-A/16h','S01-A/72h']:
            for g2,v in M(sb).items():
                if np.allclose(back, v[:3], rtol=2e-3, atol=6e-3): hits.append(f'{sb} "{g2}" first 3 of 5')
        print(f'      {g:14s} 10^x = {np.round(back,2)}   equals: {hits}')

print('\n'+'='*100); print('(4) SRB uptake: S01-B vs S08-C')
a=M('S01-B'); b=M('S08-C')
for g in a: print(f'   S01-B {g:18s}', a[g], ' mean=%.2f'%a[g].mean())
for g in b: print(f'   S08-C {g:18s}', b[g], ' mean=%.2f'%b[g].mean())

print('\n'+'='*100); print('(5) rgH5N1-restimulated vs H1N1/H3N2-restimulated IFN-g+ CD8 (S05-F vs S14-A) and other like-for-like repeats')
for blk in ['S05-F','S14-A H1N1','S14-A H3N2','S05-G','S05-E','S02-I','S01-D','S07-B/Mono','S11-C','S12-A']:
    m=M(blk) if blk!='S01-D' else {g:a.sort_values('rep').value.values for g,a in df[(df.block=='S01-D')&(df.time.isin([2,4]))].groupby(['group','time'],sort=False)}
    print('  ',blk, {str(k):np.round(np.mean(v),2) for k,v in m.items()})
