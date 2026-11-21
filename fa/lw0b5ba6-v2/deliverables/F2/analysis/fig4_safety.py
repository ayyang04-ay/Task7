import numpy as np, pandas as pd
from figstyle import *
from blocks import *
plt.rcParams.update({'axes.labelsize':7.2,'xtick.labelsize':7,'ytick.labelsize':7})
fig = plt.figure(figsize=(7.3, 5.7))
gs = fig.add_gridspec(2, 2, height_ratios=[1,1.02], hspace=0.46, wspace=0.30, left=0.105, right=0.985, top=0.955, bottom=0.085)
# (a) weight after immunisation
ax = fig.add_subplot(gs[0,0]); d = W['S08-D']
lab = {'Vaccine':'Vaccine alone','PSLN-212':'PSLN-212','PSLN-344':'PSLN-344','CMP-204':'CMP-204 (cGAMP)','PSLN-212/R848':'PSLN-212/R848'}
for g in ['Vaccine','CMP-204','PSLN-212','PSLN-344','PSLN-212/R848']:
    x = d[d.group==g].groupby('day')['value'].agg(['mean','std'])
    ax.errorbar(x.index, x['mean'], yerr=x['std'], color=COL[g], marker='o', ms=3, lw=1.3, capsize=2, label=lab[g], zorder=3 if g=='PSLN-344' else 2)
ax.axhline(100, color='#999', lw=0.6, ls=':'); ax.set_xlabel('Days after intranasal immunisation'); ax.set_ylabel('Body weight, % of day 0\n(mean ± SD, aged mice, n=5)')
ax.set_title('a  Weight after dosing, no challenge [S08-D]', fontsize=7.6); ax.legend(frameon=False, fontsize=6.6, loc='lower left', handlelength=1.6, labelspacing=0.25); ax.set_ylim(83, 103)
ax.annotate('1 of 5 animals\nmissing at day 10', xy=(10, 90.6), xytext=(6.2, 85.2), fontsize=6.2, color=COL['PSLN-212/R848'], arrowprops=dict(arrowstyle='-', color=COL['PSLN-212/R848'], lw=0.6))
# (b) lung cytokines 16 h and 72 h
ax = fig.add_subplot(gs[0,1]); L = B['S09-A_left']; R = B['S09-A_right']
an = ['Ifnb1','Il6','Tnf','Ccl2','Ccl3','Ccl5','Il10']; w=0.26
for i,a in enumerate(an):
    for j,(src,g,c,lbl) in enumerate([(L,'PSLN-344',COL['PSLN-344'],'PSLN-344, 16 h'),(R,'PSLN-344','#7fb8e0','PSLN-344, 72 h'),(R,'PSLN-212',COL['PSLN-212'],'PSLN-212, 72 h')]):
        v = src[(src.analyte==a)&(src.group==g)]['value'].values
        ax.bar(i+(j-1)*w, v.mean(), width=w*0.92, color=c, label=lbl if i==0 else None, zorder=2)
        ax.scatter(np.full(len(v), i+(j-1)*w), v, s=5, color='k', zorder=3, lw=0)
ax.axhline(0, color='#444', lw=0.7); ax.set_xticks(range(len(an))); ax.set_xticklabels(an, fontstyle='italic'); ax.set_yticks([0,1,2,3]); ax.set_yticklabels(['1×','10×','100×','1,000×'])
ax.set_ylabel('Fold over control, log scale\n(aged mice, n=3; dots = animals)'); ax.set_title('b  Lung cytokine mRNA, 16 h and 72 h [S09-A]', fontsize=7.6); ax.legend(frameon=False, fontsize=6.6, loc='upper right', labelspacing=0.25, handlelength=1.2)
ax.set_ylim(-0.35, 3.35)
# (c) CNS transcripts
ax = fig.add_subplot(gs[1,0]); 
cc = {'PBS':'#bdbdbd','Sham':'#7f7f7f','PSLN-344':COL['PSLN-344'],'CT':COL['CT']}
for i,a in enumerate(['Ifnb1','Tnf','Isg15']):
    d = B[f'S10-A_{a}']
    for j,g in enumerate(['PBS','Sham','PSLN-344','CT']):
        v = d[d.group==g]['value'].values; x = i + (j-1.5)*0.2
        ax.bar(x, v.mean(), width=0.18, color=cc[g], label={'PBS':'Buffer','Sham':'Vaccine + empty liposome','PSLN-344':'Vaccine + PSLN-344','CT':'Vaccine + cholera toxin (positive control)'}[g] if i==0 else None, zorder=2)
        ax.scatter(np.full(len(v), x), v, s=5, color='k', zorder=3, lw=0)
ax.set_xticks(range(3)); ax.set_xticklabels(['Ifnb1','Tnf','Isg15'], fontstyle='italic'); ax.set_ylabel('CNS mRNA, fold over untreated\n(aged mice, n=5)'); ax.axhline(1, color='#999', lw=0.6, ls=':')
ax.set_title('c  Brain transcripts, 36 h after dosing [S10-A]', fontsize=7.6); ax.legend(frameon=False, fontsize=6.3, loc='upper right', labelspacing=0.2, handlelength=1.2); ax.set_ylim(0, 10.8)
# (d) weight loss after challenge in survivors-inclusive groups
ax = fig.add_subplot(gs[1,1])
r = pd.read_csv('bw_challenge_nadir.csv')
sets = [('S13-F','Matched\nH1N1, d14'),('S15-A','H3→H1\nd14'),('S15-B','H3→H1\nd3'),('S15-D','→H5N1\nd3'),('S15-E','H3→H1\nd60'),('S15-F','→H5N1\nd60'),('S15-G','H1→H3\nd60')]
for i,(b,l) in enumerate(sets):
    for j,g in enumerate(['PSLN-212','PSLN-344','PSLN-212(Y)']):
        x = r[(r.block==b)&(r.group==g)].iloc[0]
        ax.bar(i+(j-1)*0.26, x.mean_max_loss, yerr=x.sd_nadir, width=0.24, color=COL[g], error_kw=dict(lw=0.7, capsize=1.5), label={'PSLN-212':'PSLN-212, aged','PSLN-344':'PSLN-344, aged','PSLN-212(Y)':'PSLN-212, young'}[g] if i==0 else None)
ax.set_xticks(range(len(sets))); ax.set_xticklabels([l for _,l in sets], fontsize=6.2); ax.set_ylabel('Maximum weight loss, %\n(mean ± SD, n=7 per group)')
ax.set_title('d  Weight loss after challenge [S13-F, S15-A–G]', fontsize=7.6); ax.legend(frameon=False, fontsize=6.2, loc='upper left', ncol=3, columnspacing=0.7, handlelength=0.9, handletextpad=0.4, bbox_to_anchor=(-0.03, 1.0)); ax.set_ylim(0, 27)
fig.savefig(OUT+'fig4_safety_tolerability.png'); print('ok')
