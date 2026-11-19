import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
t=pd.read_csv('tidy.csv'); b=pd.read_csv('bodyweight.csv'); s=pd.read_csv('survival.csv')
fig,axes=plt.subplots(2,3,figsize=(15,9.5)); axes=axes.ravel()
# (a) S11-A vs S11-B
a=t[t.block=='S11-A']; n=t[t.block=='S11-B']
m=a.merge(n,on=['group','time','rep'],suffixes=('_am','_neu')); same=np.isclose(m.value_am,m.value_neu)
ax=axes[0]
ax.scatter(m.value_am[~same],m.value_neu[~same],s=14,c='grey',label=f'different ({(~same).sum()})')
ax.scatter(m.value_am[same],m.value_neu[same],s=22,c='#d62728',label=f'identical to 0.1 ({same.sum()})')
ax.plot([10,60],[10,60],'k--',lw=0.7); ax.set_xlabel('S11-A alveolar macrophages (%)',fontsize=8); ax.set_ylabel('S11-B neutrophils (%), same group/day/replicate position',fontsize=8)
ax.set_title('(a) Two different cell populations share 35/100\nposition-matched values (chance ≈1e-46; NK control block 0–1/100)',fontsize=8.5); ax.legend(fontsize=7)
# (b) body weight reuse across experiments
ax=axes[1]
def traj(bb,g,an): d=b[(b.block==bb)&(b.group==g)&(b.animal==an)].sort_values('day'); return d.day.values,d.value.values
for (bb,g,an,c,ls,lab) in [('S09-E','PSLN-344(Y)',2,'#d62728','-','S09-E young BALB/c, PSLN-344(Y) #2 (Perth H3N2)'),('S15-M','PSLN-212(Y)',1,'k',':','S15-M young C57BL/6, PSLN-212(Y) #1'),
                           ('S09-E','PSLN-344(Y)',3,'#1f77b4','-','S09-E PSLN-344(Y) #3'),('S15-M','PSLN-212(Y)',2,'grey',':','S15-M PSLN-212(Y) #2')]:
    x,y=traj(bb,g,an); ax.plot(x,y,ls=ls,color=c,lw=2 if ls=='-' else 1.6,marker='o' if ls=='-' else 'x',ms=4,label=lab)
ax.set_xlabel('day',fontsize=8); ax.set_ylabel('% of day-0 weight',fontsize=8); ax.set_ylim(91.5,104); ax.legend(fontsize=6.2,loc='lower left')
ax.set_title('(b) Different strain, formulation & challenge virus,\nidentical 7–8-significant-digit weights on days 6–14',fontsize=8.5)
# (c) S15-A vs S15-M PSLN-344
ax=axes[2]
for (bb,an,c,ls,lab) in [('S15-A',2,'#d62728','-','S15-A aged BALB/c PSLN-344 #2'),('S15-M',2,'k',':','S15-M aged C57BL/6 PSLN-344 #2'),('S15-A',3,'#1f77b4','-','S15-A PSLN-344 #3'),('S15-M',3,'grey',':','S15-M PSLN-344 #3')]:
    x,y=traj(bb,'PSLN-344',an); ax.plot(x,y,ls=ls,color=c,lw=2 if ls=='-' else 1.6,marker='o' if ls=='-' else 'x',ms=4,label=lab)
ax.set_xlabel('day',fontsize=8); ax.legend(fontsize=6.2,loc='lower left')
ax.set_title('(c) BALB/c (S15-A) and C57BL/6 (S15-M) studies share\nidentical PSLN-344 weights (e.g., 92.42424, 89.09091, 93.63636)',fontsize=8.5)
# (d) S03-B label rotation
ax=axes[3]
groups=['PSLN-212','PSLN-344','PSLN-212(Y)']
q=[t[(t.block=='S03-B')&(t.group==g)].value.mean() for g in groups]
r=[(t[(t.block=='S13-A')&(t.group==g)].sort_values('rep').value.values/t[(t.block=='S13-B')&(t.group==g)].sort_values('rep').value.values).mean() for g in groups]
x=np.arange(3); ax.bar(x-0.18,q,0.36,color='#9467bd',label='S03-B as printed'); ax.bar(x+0.18,r,0.36,color='#2ca02c',label='recomputed from S13-A/S13-B')
ax.set_xticks(x); ax.set_xticklabels(groups,fontsize=8); ax.set_ylabel('IgG2a / IgG1 (CA09, d14)',fontsize=8); ax.legend(fontsize=7)
ax.set_title('(d) Same 15 numbers, cyclically rotated group labels\n(S03-B & S03-F vs S13-A–D): Th1-skew claim reverses',fontsize=8.5)
# (e) S03-I vs S13-F
ax=axes[4]
d=b[(b.block=='S13-F')&(b.group=='PSLN-212')]
for an,dd in d.groupby('animal'): ax.plot(dd.day,dd.value,'-o',ms=3,color='#1f77b4',alpha=0.8)
dd=s[(s.block=='S03-I')&(s.group=='PSLN-212')]
for i,dy in enumerate(sorted(dd.day)): ax.plot(dy,72+i*0.8,'x',color='#d62728')
ax.text(6.3,73,'S03-I: all 7 PSLN-212 animals\nrecorded dead on d5–6 (red ×)',fontsize=7,color='#d62728')
ax.set_ylim(70,103); ax.set_xlabel('day after challenge',fontsize=8); ax.set_ylabel('% of day-0 weight (S13-F)',fontsize=8)
ax.set_title('(e) "Same animals" (annotation): weights show all 7 alive at d8,\n4 flat-lined from d10 (carried forward), 3 recovering',fontsize=8.5)
# (f) S06-C vs S06-D identical
ax=axes[5]
def km(dv,ev):
    dv=np.asarray(dv,float); ev=np.asarray(ev,int); ts=[0]; S=[1.0]; cur=1.0
    for tt in np.unique(dv[ev==1]):
        nn=(dv>=tt).sum(); mm=((dv==tt)&(ev==1)).sum(); cur*=1-mm/nn; ts.append(tt); S.append(cur)
    ts.append(14); S.append(cur); return ts,S
for blk,ls,lw in [('S06-C','-',3),('S06-D','--',1.5)]:
    for g,c in [('Sham','grey'),('PSLN-212','#1f77b4'),('PSLN-344','#d62728')]:
        x=s[(s.block==blk)&(s.group==g)]; ts,S=km(x.day,x.event); ax.step(ts,S,where='post',ls=ls,lw=lw,color=c,label=f'{blk} {g}')
ax.legend(fontsize=6.2,ncol=2,loc='lower left'); ax.set_xlabel('days after challenge',fontsize=8); ax.set_ylabel('survival',fontsize=8)
ax.set_title('(f) S06-C (challenge d14) and S06-D (challenge d3):\n28/28 rows identical in every group',fontsize=8.5)
for ax in axes: ax.tick_params(labelsize=7)
fig.suptitle('Fig. 5  Data-integrity findings that affect pivotal claims (all values read directly from psln_program_dataset.xlsx)',fontsize=10)
plt.tight_layout(rect=[0,0,1,0.96]); plt.savefig('/tmp/outputs/figures/fig5_data_integrity_evidence.png',dpi=170); print('ok')
