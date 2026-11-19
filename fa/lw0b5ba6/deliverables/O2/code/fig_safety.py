import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
b=pd.read_csv('bodyweight.csv'); t=pd.read_csv('tidy.csv')
fig,axes=plt.subplots(1,3,figsize=(15,4.6))
ax=axes[0]; d=b[b.block=='S08-D']
cols={'Vaccine':'grey','PSLN-212':'#1f77b4','PSLN-344':'#d62728','CMP-204':'#bcbd22','PSLN-212/R848':'#9467bd','PSLN-212(Y)':'#2ca02c'}
for g,c in cols.items():
    x=d[d.group==g].groupby('day').value; m=x.mean(); sd=x.std(); n=x.count()
    ax.errorbar(m.index,m.values,yerr=sd.values,color=c,marker='o',ms=3,capsize=2,lw=2 if g=='PSLN-344' else 1.2,label=g+(' (1 animal missing d10)' if g=='PSLN-212/R848' else ''))
ax.set_xlabel('days after intranasal vaccination (no challenge)',fontsize=8); ax.set_ylabel('% of day-0 weight, mean ± SD (n=5)',fontsize=8)
ax.set_title('(a) Reactogenicity proxy [S08-D]: PSLN-344 nadir 96.4±1.5%\nvs vaccine alone 98.2±1.1% (p=0.065); R848 combo 90.0±5.0%',fontsize=8.5); ax.legend(fontsize=6.5)
ax=axes[1]
an=['Ifnb1','Tnf','Isg15']; gs=['PBS','Sham','PSLN-344','CT']; gc=['#bbbbbb','#7f7f7f','#d62728','#8c564b']
for i,a in enumerate(an):
    for j,g in enumerate(gs):
        v=t[(t.block==f'S10-A_{a}')&(t.group==g)].value
        lv=np.log10(v); gmv=10**lv.mean(); lo=gmv-10**(lv.mean()-lv.std(ddof=1)); hi=10**(lv.mean()+lv.std(ddof=1))-gmv
        ax.bar(i+j*0.2-0.3,gmv,0.2,yerr=[[lo],[hi]],color=gc[j],capsize=2,label=g if i==0 else None)
        ax.plot(np.full(len(v),i+j*0.2-0.3),v,'k.',ms=3)
ax.set_xticks(range(3)); ax.set_xticklabels([f'CNS {a}' for a in an],fontsize=8); ax.set_ylabel('fold vs untreated (36 h); geometric mean × / ÷ geometric SD',fontsize=8); ax.set_ylim(0,10)
ax.set_title('(b) CNS innate activation 36 h after intranasal dose [S10-A]\nPSLN-344 vs PBS: Tukey (log) p=0.50 / 0.12 / 0.77; cholera toxin ↑',fontsize=8.5); ax.legend(fontsize=7)
ax.text(0.02,0.97,'Tnf: PSLN-344 1.54× vs PBS 0.98× (geometric)\n(unadjusted p=0.031; Tukey p=0.12)\nBlock is declared "mean ± SD" in annotation\nbut holds 5 values/group — verify',transform=ax.transAxes,va='top',fontsize=6.5,color='#b00000')
ax=axes[2]
an=['Ifnb1','Il6','Tnf','Ccl2','Il10']
p1=[];p2=[]
for a in an:
    for blk,store in [('S09-A_blk1(B:V)',p1),('S09-A_blk2(Y:AS)',p2)]:
        store.append([10**t[(t.block==blk)&(t.group==g)&(t.analyte==a)].value.mean() for g in ['PSLN-344','PSLN-212(Y)','PSLN-212/R848']])
p1=np.array(p1); p2=np.array(p2); x=np.arange(len(an))
for j,(g,c) in enumerate([('PSLN-344 aged','#d62728'),('PSLN-212 young','#2ca02c'),('PSLN-212/R848 aged','#9467bd')]):
    ax.bar(x+j*0.27-0.27,p1[:,j],0.13,color=c,label=f'{g}, 16 h')
    ax.bar(x+j*0.27-0.27+0.13,p2[:,j],0.13,color=c,alpha=0.4,hatch='//',label=f'{g}, 2nd panel')
ax.set_yscale('log'); ax.set_xticks(x); ax.set_xticklabels(an,fontsize=8); ax.set_ylabel('fold vs PBS (geometric mean, n=3)',fontsize=8)
ax.set_title('(c) Lung cytokines [S09-A]: 2nd panel is labelled "16 h" but matches\nS01-A 72 h values (r=0.999) → PSLN-344 Il6/Tnf/Ccl2 still 7–27× at ~72 h',fontsize=8.5)
ax.legend(fontsize=5.8,ncol=2)
for a in axes: a.tick_params(labelsize=7)
fig.suptitle('Fig. 7  Tolerability and safety-relevant readouts available in the dataset (all exploratory, single experiments)',fontsize=10)
plt.tight_layout(rect=[0,0,1,0.93]); plt.savefig('/tmp/outputs/figures/fig7_safety_readouts.png',dpi=170); print('ok')
