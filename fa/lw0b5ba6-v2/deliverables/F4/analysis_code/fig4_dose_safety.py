import pandas as pd, numpy as np
from fig_style import *
Q = pd.read_csv('quant_long.csv'); W = pd.read_csv('wt_long.csv'); R = pd.read_csv('dose_response_fit.csv')
fig, axes = plt.subplots(2, 2, figsize=(FIGW, 5.9), gridspec_kw={'wspace':0.27, 'hspace':0.55, 'left':0.075, 'right':0.99, 'top':0.955, 'bottom':0.12})
# (a) dose response
ax = axes[0,0]
d = Q[Q.block=='S08-A'].copy(); d['dose']=d.time.astype(float)
cmap = {'CMP-204':COL['CMP-204'],'PSLN-212':COL['PSLN-212'],'PSLN-344':COL['PSLN-344'],'PSLN-344/R848':COL['PSLN-212/R848']}
xx = np.logspace(0, np.log10(40), 100)
for g in ['CMP-204','PSLN-212','PSLN-344','PSLN-344/R848']:
    x = d[d.group==g]
    ax.plot(x.dose, x.value, 'o', color=cmap[g], ms=3, alpha=0.8)
    r = R[R.group==g].iloc[0]
    ax.plot(xx, 1+(r.Emax-1)*xx**r.hill/(r.ED50**r.hill+xx**r.hill), color=cmap[g], lw=1.4, label=f"{g + ('*' if 'R848' in g else '')}: max {r.Emax:.0f}×, ED50 {r.ED50:.0f} µg")
ax.set_xscale('log'); ax.set_xticks([1,5,10,20,40]); ax.set_xticklabels(['1','5','10','20','40']); ax.set_xlabel('Dose, µg per animal (no vaccine)')
ax.set_ylabel('Lung Ifnb1 mRNA at 16 h, fold'); ax.legend(frameon=False, fontsize=6.2, loc='upper left', handlelength=1.4, borderaxespad=0.2)
ax.axvline(20, color='#999999', lw=0.7, ls=':'); ax.set_ylim(-2, 66); ax.text(20.8, 65.5, 'dose used in all\nefficacy studies', fontsize=6, color='#555555', va='top')
ax.text(0.0, -0.26, '*as labeled in the workbook; not a listed preparation', transform=ax.transAxes, fontsize=5.8, color='#555555')
ax.set_title('A  Dose-response: Ifnb1 only (S08-A, n=3)', loc='left', fontweight='bold')
# (b) body weight after immunization
ax = axes[0,1]
d = W[W.block=='S08-D']
cm = {'Vaccine':COL['Sham'],'PSLN-212':COL['PSLN-212'],'PSLN-344':COL['PSLN-344'],'PSLN-212(Y)':COL['PSLN-212(Y)'],'CMP-204':COL['CMP-204'],'PSLN-212/R848':COL['PSLN-212/R848']}
lab = {'Vaccine':'Vaccine alone','PSLN-212':'PSLN-212','PSLN-344':'PSLN-344','PSLN-212(Y)':'Young + PSLN-212','CMP-204':'CMP-204','PSLN-212/R848':'PSLN-212/R848 (4 of 5 at day 10)'}
for g in ['Vaccine','CMP-204','PSLN-212','PSLN-344','PSLN-212(Y)','PSLN-212/R848']:
    m = d[d.group==g].groupby('day').value.agg(['mean','std'])
    ax.errorbar(m.index, m['mean'], yerr=m['std'], color=cm[g], lw=1.4, marker='o', ms=2.6, capsize=1.6, elinewidth=0.8, label=lab[g])
ax.axhline(100, color='#CCCCCC', lw=0.6); ax.set_xlabel('Days after intranasal dose (no challenge)'); ax.set_ylabel('Body weight, % of day 0 (mean ± SD)')
ax.legend(frameon=False, fontsize=6.2, loc='lower left', handlelength=1.4, borderaxespad=0.2); ax.set_ylim(84, 103)
ax.set_title('B  Body weight after dosing (S08-D, n=5)', loc='left', fontweight='bold')
# (c) lung cytokines
ax = axes[1,0]
d = Q[Q.block=='S09-A'].copy(); d['an']=d.analyte.str.replace(' (log10 fold)','',regex=False)
grp = [('PSLN-212',COL['PSLN-212'],'Aged + PSLN-212'),('PSLN-344',COL['PSLN-344'],'Aged + PSLN-344'),('PSLN-212(y)',COL['PSLN-212(Y)'],'Young + PSLN-212'),('PSLN-212/R848',COL['PSLN-212/R848'],'Aged + PSLN-212/R848')]
ans = ['Tnf','Il6','Il10']; x0 = 0; xt=[]; xl=[]
for pi, (panel, tl) in enumerate([('panel1(A-U)','16 h'),('panel2(X-AS)','72 h†')]):
    for an in ans:
        for gi,(g,c,l) in enumerate(grp):
            v = d[(d.time==panel)&(d.an==an)&(d.group==g)].value.values
            xs = x0 + gi*0.2
            ax.plot([xs]*len(v), 10**v, 'o', color=c, ms=3, alpha=0.85, label=l if (pi==0 and an=='Tnf') else None)
            ax.plot([xs-0.07, xs+0.07], [10**v.mean()]*2, color=c, lw=1.6)
        xt.append(x0+0.3); xl.append(f"{an}\n{tl}"); x0 += 1.1
    x0 += 0.35
ax.set_yscale('log'); ax.axhline(1, color='#999999', lw=0.7, ls='--'); ax.set_xticks(xt); ax.set_xticklabels(xl, fontsize=6.6)
ax.set_ylabel('Lung mRNA, fold (log scale)'); ax.legend(frameon=False, fontsize=6.2, loc='upper right', ncol=2, bbox_to_anchor=(1.03, 1.02), columnspacing=0.8, handletextpad=0.2)
ax.set_ylim(0.05, 6000)
ax.set_title('C  Lung cytokines after dosing (S09-A, n=3)', loc='left', fontweight='bold')
ax.text(0.0, -0.26, '†labeled “16h” in the workbook; Ifnb1 values are the S01-A 72-h animals', transform=ax.transAxes, fontsize=5.8, color='#555555')
# (d) CNS
ax = axes[1,1]
d = Q[Q.block=='S10-A']; x0=0; xt=[]; xl=[]
cc = {'PBS':'#BBBBBB','Sham':COL['Sham'],'PSLN-344':COL['PSLN-344'],'CT':'#000000'}; ll = {'PBS':'Buffer','Sham':'Vaccine alone','PSLN-344':'Vaccine + PSLN-344','CT':'Vaccine + cholera toxin'}
for an in ['CNS Ifnb1 (fold)','CNS Tnf (fold)','CNS Isg15 (fold)']:
    for gi,g in enumerate(['PBS','Sham','PSLN-344','CT']):
        v = d[(d.analyte==an)&(d.group==g)].value.values; xs = x0+gi*0.2
        ax.plot([xs]*len(v), v, 'o', color=cc[g], ms=3, alpha=0.85, label=ll[g] if an.startswith('CNS Ifnb1') else None)
        ax.plot([xs-0.07,xs+0.07],[v.mean()]*2, color=cc[g], lw=1.6)
    xt.append(x0+0.3); xl.append(an.replace('CNS ','').replace(' (fold)','')); x0 += 1.1
ax.axhline(1, color='#999999', lw=0.7, ls='--'); ax.set_xticks(xt); ax.set_xticklabels(xl); ax.set_ylabel('Brain mRNA at 36 h, fold')
ax.legend(frameon=False, fontsize=6.2, loc='upper right', borderaxespad=0.2)
ax.set_title('D  Brain transcripts, aged (S10-A, n=5)', loc='left', fontweight='bold')
fig.savefig(OUT+'Fig4_dose_and_tolerability.png'); print('ok')
