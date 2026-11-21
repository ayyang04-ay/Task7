from loadcsv import *
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig,axs=plt.subplots(2,3,figsize=(18,11))
# (a) S03-B label rotation
ax=axs[0,0]
def v(b,g): return DF[(DF.block==b)&(DF.group==g)].value.values
G=['PSLN-212','PSLN-344','PSLN-212(Y)']
printed=[v('S03-B',g).mean() for g in G]
raw=[(v('S13-A',g)/v('S13-B',g)).mean() for g in G]
x=np.arange(3); ax.bar(x-0.2,printed,0.4,label='S03-B as printed',color='#bdbdbd'); ax.bar(x+0.2,raw,0.4,label='recomputed from S13-A/S13-B raw IgG2a & IgG1 titres',color='#2171b5')
ax.set_xticks(x); ax.set_xticklabels(G); ax.set_ylabel('IgG2a/IgG1 (CA09, d14)'); ax.axhline(1,color='k',lw=.6,ls=':')
ax.set_title('A. S03-B/S03-F group labels are rotated\n(printed "PSLN-344" = S13 PSLN-212 exactly; printed would wrongly imply Th2 skew)',fontsize=9); ax.legend(fontsize=8)
# (b) S06-C vs S06-D identical
ax=axs[0,1]; ax.axis('off')
c=SV[SV.block=='S06-C']; d=SV[SV.block=='S06-D']
lines=["B. S06-C (rgH5N1 challenge day 14) vs S06-D (day 3)","   group         S06-C (day,event)            S06-D (day,event)"]
for g in ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']:
    a=list(zip(c[c.group==g].time.astype(int),c[c.group==g].event)); b=list(zip(d[d.group==g].time.astype(int),d[d.group==g].event))
    fa=' '.join(f"{t}{'x' if e else 'c'}" for t,e in a); fb=' '.join(f"{t}{'x' if e else 'c'}" for t,e in b)
    lines.append(f"   {g:12s} {fa:30s} {fb}")
lines+=["","   28/28 rows identical (x = died, c = censored).","   S15-D weights (said to be S06-D animals) show frozen","   weights consistent with 2 PSLN-344 and 2 young deaths,","   which S06-D does not record.  -> S06-D excluded."]
ax.text(0,1,'\n'.join(lines),va='top',family='monospace',fontsize=8.5)
# (c) S15-C PSLN-344 vs S15-I 3d Vaccine+PSLN-344 weight curves
ax=axs[0,2]
for blk,g,ls,lab in [('S15-C','PSLN-344','-','S15-C PSLN-344 (bivalent, rgH5N1 d14)'),('S15-I','3d Vaccine+PSLN-344','--','S15-I Vaccine+PSLN-344 (3-day study)')]:
    dd=DF[(DF.block==blk)&(DF.group==g)].copy(); dd['day']=dd.day.astype(float)
    for i,(cc,z) in enumerate(dd.groupby('animal_col')):
        z=z.sort_values('day'); ax.plot(z.day,z.value,ls,color=plt.cm.tab10(i),lw=2 if ls=='-' else 1.2,label=(lab if i==0 else None),alpha=.8)
ax.set_xlabel('day'); ax.set_ylabel('% body weight'); ax.legend(fontsize=7,loc='lower left')
ax.set_title('C. Two different experiments, same animals\' weights:\n6 of 7 columns identical on 6 consecutive days (colour = column)',fontsize=9)
# (d) S11-A vs S11-B
ax=axs[1,0]
a=DF[DF.block=='S11-A'].copy(); b=DF[DF.block=='S11-B'].copy()
a['pos']=a.cell.str.extract(r'!([A-Z]+)')[0]+a['day'].astype(str); b['pos']=b.cell.str.extract(r'!([A-Z]+)')[0]+b['day'].astype(str)
m=a.merge(b,on='pos'); same=np.isclose(m.value_x,m.value_y)
ax.scatter(m.value_x[~same],m.value_y[~same],s=14,color='grey',label=f'different ({(~same).sum()})'); ax.scatter(m.value_x[same],m.value_y[same],s=22,color='#cb181d',label=f'identical ({same.sum()}/100)')
ax.plot([10,60],[10,60],'k:',lw=.7); ax.set_xlabel('S11-A alveolar macrophages (%)'); ax.set_ylabel('S11-B neutrophils (%), same cell position'); ax.legend(fontsize=8)
ax.set_title('D. S11-B "neutrophils" duplicates S11-A "alveolar macrophages"\n(first 2 animals of every group identical at all 5 timepoints)',fontsize=9)
# (e) observed vs expected identical fresh weights
ax=axs[1,1]
k=np.arange(0,8); obs=[121806,4107,135,8,3,6,7,2]; mis=[124017,2016,40,1,0,0,0,0]
from scipy.stats import binom
exp=[len(obs) and 126074*binom.pmf(i,7,0.0085) for i in k]
ax.bar(k-0.27,obs,0.27,label='observed, same day aligned',color='#cb181d'); ax.bar(k,mis,0.27,label='control: days misaligned by 2',color='#969696'); ax.bar(k+0.27,exp,0.27,label='binomial expectation',color='#fdd49e')
ax.set_yscale('log'); ax.set_ylim(5e-5,3e5); ax.set_xlabel('identical non-repeated body-weight values shared by a pair of animals from different experiments'); ax.set_ylabel('number of animal pairs')
ax.set_title('E. Cross-experiment duplication of body weights is not chance\n>=4 shared values: 18 pairs observed vs 0.02 expected',fontsize=9); ax.legend(fontsize=8)
# (f) decimal reuse example
ax=axs[1,2]; ax.axis('off')
j=DF[(DF.block=='S15-J')&(DF.animal_col=='AD')].copy(); j['d']=j.day.astype(float); j=j.sort_values('d'); mm=DF[(DF.block=='S15-M')&(DF.animal_col=='AD')].copy(); mm['d']=mm.day.astype(float); mm=mm.sort_values('d')
lines=["F. Same decimals, edited integers (8-digit fractions)","   day  S15-J Imprinting+PSLN-344  S15-M PSLN-344 (C57BL/6)"]
for (_,r1),(_,r2) in zip(j.iterrows(),mm.iterrows()):
    lines.append(f"   {int(float(r1.day)):3d}  {r1.value:>14}            {r2.value:>14}")
lines+=["","   Fractional parts match on days 2-12 (6 of 7 post-baseline","   days) while integer parts differ by 1-5. For two real animals,","   even with identical baseline weights, this is ~(1/159)^6 likely.","   The same pattern links S15-A, S15-F, S15-J, S15-M and S08-D","   (tables/T7_bodyweight_duplication_pairs.csv; register A1)."]
ax.text(0,1,'\n'.join(lines),va='top',family='monospace',fontsize=8.5)
plt.tight_layout(); plt.savefig('/tmp/outputs/figures/Fig5_data_integrity_exhibits.png',dpi=150); print('ok')
