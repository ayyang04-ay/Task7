import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
s=pd.read_csv('survival.csv'); P=pd.read_csv('surv_pairwise.csv'); pooled=pd.read_csv('pooled_survival.csv')
def km(d,e):
    d=np.asarray(d,float); e=np.asarray(e,int); ts=[0]; S=[1.0]; cur=1.0
    for tt in np.unique(d[e==1]):
        n=(d>=tt).sum(); m=((d==tt)&(e==1)).sum(); cur*=1-m/n; ts.append(tt); S.append(cur)
    ts.append(max(d.max(),14)); S.append(cur); return ts,S
colors={'Sham':'#7f7f7f','PSLN-212':'#1f77b4','PSLN-344':'#d62728','PSLN-212(Y)':'#2ca02c','CMP-204':'#bcbd22','Untreated':'#000000',
        '3d Vaccine':'#7f7f7f','3d PSLN-344':'#ff9896','3d Vaccine+PSLN-344':'#d62728'}
panels=[('S06-A','H3 vaccine → PR8 (H1N1), d14','Weights (S15-A): Sham d4 row = S15-M PSLN-212 d4 (7/7);\nPSLN-344 #2–3 reuse values found in S15-M (C57BL/6)'),('S06-B','H3 vaccine → PR8 (H1N1), d3','OK'),('S06-C','Bivalent → rgH5N1, d14','Flag: PSLN-212 deaths 5 here vs 6 implied by weights;\nS15-C PSLN-344 weights = S15-I (3-day study) d2–d12'),
        ('S06-D','Bivalent → rgH5N1, d3','VOID: cell-for-cell identical to S06-C; weights (S15-D)\nimply 2 PSLN-344 & 2 young deaths'),
        ('S06-E_r34','H3 vaccine → PR8, d60','Flag: PSLN-344 deaths 2 here vs 1 implied by weights'),('S06-F_r34','Bivalent → rgH5N1, d60','Weights (S15-F) contain values reused from S08-D'),
        ('S06-G','H1 vaccine → Perth (H3N2), d60','Flag: unchallenged aged controls 3/7 died;\nPSLN-344 deaths 3 here vs 2 implied by weights'),
        ('S03-I','Bivalent → CA09 10×LD50, d14','Flag: PSLN-212 all dead d5–6 here, but weights\n(S13-F) show all 7 alive at d8 & 3 recovering'),
        ('S03-J','rgH5N1 vaccine → wt VN04 H5N1, d2','Flag: stated n=9 vs 10 rows; 1 PSLN-344 row lacks day;\nSham deaths 9 here vs 5 implied by S13-G weights'),
        ('S15-L','C57BL/6 aged, bivalent','Young arm: 1 death here vs 0 implied by weights;\nweights (S15-M) reuse S15-A & S09-E values'),('S15-N','Swiss Webster aged, bivalent','Weights (S15-O) share values with S15-C/S15-M'),
        ('S15-H','3-day: vaccine ± PSLN-344 → rgH5N1','Weights (S15-I) of vaccine+PSLN-344 arm duplicate\nthe S15-C PSLN-344 arm on d2–d12 (40/42 values)')]
fig,axes=plt.subplots(4,3,figsize=(13,14)); axes=axes.ravel()
for ax,(blk,title,flag) in zip(axes,panels):
    d=s[s.block==blk].dropna(subset=['day'])
    for g in d.group.unique():
        x=d[d.group==g]; ts,S=km(x.day,x.event)
        n=len(s[(s.block==blk)&(s.group==g)]); surv=n-int(s[(s.block==blk)&(s.group==g)].event.sum())
        ax.step(ts,S,where='post',color=colors.get(g,'purple'),lw=2 if 'PSLN-344' in g else 1.3,label=f"{g} {surv}/{n}")
    pr=P[(P.block==blk)&(P.comparison=='PSLN-344 vs PSLN-212')]
    ptxt=f"log-rank 344 vs 212: p={pr.logrank_p.iloc[0]:.2g}" if len(pr) else ''
    if blk=='S15-H':
        pr=P[(P.block==blk)&(P.comparison=='3d Vaccine+PSLN-344 vs 3d Vaccine')]; ptxt=f"vax+344 vs vax: p={pr.logrank_p.iloc[0]:.2g}"
    ax.set_title(f"{blk}: {title}\n{ptxt}",fontsize=8.5)
    ax.set_ylim(-0.03,1.05); ax.set_xlim(0,22 if blk=='S03-J' else 14.5); ax.set_xlabel('days after challenge',fontsize=7); ax.tick_params(labelsize=7)
    ax.legend(fontsize=6.3,loc='lower left')
    if flag=='OK':
        ax.text(0.98,0.98,'No integrity flag detected',transform=ax.transAxes,ha='right',va='top',fontsize=6.2,color='#006400',bbox=dict(fc='#f0fff0',ec='#006400',lw=0.6))
    elif flag:
        ax.text(0.98,0.98,flag,transform=ax.transAxes,ha='right',va='top',fontsize=6.2,color='#b00000',bbox=dict(fc='#fff3f3',ec='#b00000',lw=0.6))
    if blk=='S06-D':
        ax.set_facecolor('#f2f2f2')
fig.suptitle('Fig. 3  Survival after lethal influenza challenge in aged mice (BALB/c unless stated), as recorded in the workbook; integrity flags in red',fontsize=10)
plt.tight_layout(rect=[0,0,1,0.97]); plt.savefig('/tmp/outputs/figures/fig3_survival_KM.png',dpi=170)

# pooled bar chart
pp=pooled[pooled.b=='PSLN-212'].copy()
lab=['Tier A: all aged blocks as printed\n(S06-D duplicate excluded; 10 blocks)','Tier A incl. duplicate S06-D\n(not recommended)','Tier B: survival & weight records agree\n(S06-A,B,F(r34), S15-L,N)','Tier C: no detectable integrity flag\n(S06-B only)','Aged BALB/c heterosubtypic only\n(S06-A,B,C,E,F,G)','Day-60 durability\n(S06-E,F (r34), S06-G)']
fig,ax=plt.subplots(figsize=(11,5.6))
y=np.arange(len(pp))
a=pp.a_surv/pp.a_n*100; b=pp.b_surv/pp.b_n*100
ax.barh(y+0.2,a,0.4,color='#d62728',label='PSLN-344 (aged)'); ax.barh(y-0.2,b,0.4,color='#1f77b4',label='PSLN-212 (aged)')
for i,(r) in enumerate(pp.itertuples()):
    ax.text(a.iloc[i]+1,i+0.2,f"{r.a_surv}/{r.a_n}",va='center',fontsize=7); ax.text(b.iloc[i]+1,i-0.2,f"{r.b_surv}/{r.b_n}",va='center',fontsize=7)
    ax.text(103,i,f"RD {100*r.rd:+.0f} pts\nstrat. log-rank p={r.slr_p:.1g}",va='center',fontsize=7)
ax.set_yticks(y); ax.set_yticklabels(lab[:len(pp)],fontsize=7.5); ax.set_xlim(0,132); ax.set_ylim(len(pp)-0.4,-1.0); ax.set_xlabel('% surviving to end of observation',fontsize=8)
ax.axvline(81,color='k',ls=':',lw=0.8); ax.text(81,-0.75,'unchallenged aged background survival 17/21 (81%)',fontsize=6.5,ha='center')
ax.legend(fontsize=7,loc='upper center',bbox_to_anchor=(0.5,-0.12),ncol=2)
ax.set_title('Fig. 4  Pooled survival, PSLN-344 vs PSLN-212 in aged mice, by data-integrity sensitivity tier\n(Mantel–Haenszel risk difference; stratified log-rank by experiment)',fontsize=9)
plt.tight_layout(); plt.subplots_adjust(left=0.24); plt.savefig('/tmp/outputs/figures/fig4_pooled_survival_tiers.png',dpi=180)
print('ok')
