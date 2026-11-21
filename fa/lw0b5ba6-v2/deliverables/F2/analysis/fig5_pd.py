import numpy as np, pandas as pd
from figstyle import *
from blocks import *
plt.rcParams.update({'axes.labelsize':7.2,'xtick.labelsize':7,'ytick.labelsize':7})
fig = plt.figure(figsize=(7.3, 5.5))
gs = fig.add_gridspec(2, 2, hspace=0.48, wspace=0.27, left=0.085, right=0.985, top=0.955, bottom=0.085)
# (a) dose response
ax = fig.add_subplot(gs[0,0]); d = T['S08-A']; fit = pd.read_csv('dose_response_S08A.csv').set_index('group')
def hill(D, emax, ed50, h): return 1 + emax*D**h/(ed50**h + D**h)
xx = np.logspace(0, np.log10(40), 200)
for g,lab in [('CMP-204','CMP-204 (cGAMP)'),('PSLN-212','PSLN-212'),('PSLN-344','PSLN-344')]:
    x = d[d.group==g]; ax.scatter(x['dose_ug'], x['value'], s=9, color=COL[g], zorder=3)
    f = fit.loc[g]; ax.plot(xx, hill(xx, f.Emax_fold, f.ED50_ug, f.hill), color=COL[g], lw=1.3, label=f'{lab}: plateau {f.Emax_fold:.0f}×, ED50 {f.ED50_ug:.0f} µg')
ax.axvline(20, color='#999', lw=0.7, ls=':'); ax.text(21.5, 30, '20 µg: dose used in\nall efficacy studies', fontsize=6, color='#555', va='center')
ax.set_xscale('log'); ax.set_xticks([1,5,10,20,40]); ax.set_xticklabels(['1','5','10','20','40']); ax.set_xlabel('Adjuvant dose, µg per mouse'); ax.set_ylabel('Lung Ifnb1 mRNA at 16 h, fold')
ax.set_title('a  Dose–response: Mn raises the ceiling [S08-A]', fontsize=7.6); ax.legend(frameon=False, fontsize=6.2, loc='upper left', labelspacing=0.25, handlelength=1.2); ax.set_ylim(0, 66); ax.set_xlim(0.85, 62)
# (b) Ifnb1 by group 16h
ax = fig.add_subplot(gs[0,1]); d = B['S01-A_16h']; d72 = B['S01-A_72h']
groups = ['Sham','CMP-204','PSLN-212','PSLN-344','PSLN-212(Y)','PSLN-344(Y)']; labs = ['Empty\nliposome','CMP-204','PSLN-212','PSLN-344','PSLN-212','PSLN-344']
for i,g in enumerate(groups):
    v = d[d.group==g]['value'].values; v2 = d72[d72.group==g]['value'].values
    ax.bar(i-0.2, v.mean(), width=0.38, color=COL[g], zorder=2); ax.scatter(np.full(len(v), i-0.2), v, s=5, color='k', zorder=3, lw=0)
    ax.bar(i+0.2, v2.mean(), width=0.38, color=COL[g], alpha=0.45, zorder=2, hatch='///', edgecolor='white', lw=0); ax.scatter(np.full(len(v2), i+0.2), v2, s=5, color='k', zorder=3, lw=0)
ax.set_xticks(range(len(groups))); ax.set_xticklabels(labs, fontsize=5.9); ax.set_ylabel('Lung Ifnb1 mRNA, fold over untreated')
ax.text(1.5, -14.5, 'aged mice', ha='center', fontsize=6.8, fontweight='bold'); ax.text(4.5, -14.5, 'young mice', ha='center', fontsize=6.8, fontweight='bold')
ax.plot([-0.45, 3.45], [-11.0, -11.0], color='#444', lw=0.7, clip_on=False); ax.plot([3.55, 5.45], [-11.0, -11.0], color='#444', lw=0.7, clip_on=False)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(fc='#555', label='16 h'), Patch(fc='#555', alpha=0.45, hatch='///', ec='white', label='72 h')], frameon=False, fontsize=6.6, loc='upper left')
ax.set_title('b  Interferon-β mRNA by group (n=5) [S01-A]', fontsize=7.6); ax.set_ylim(0, 66)
# (c) GM-CSF time course
ax = fig.add_subplot(gs[1,0]); d = T['S02-F']; tm = {'16h':16,'36h':36,'72h':72}
for g,lab in [('Sham','Vaccine + empty liposome'),('PSLN-212','Vaccine + PSLN-212'),('PSLN-344','Vaccine + PSLN-344')]:
    x = d[d.group==g].copy(); x['t'] = x['time'].map(tm); m = x.groupby('t')['value'].agg(['mean','std'])
    ax.errorbar(m.index, m['mean'], yerr=m['std'], color=COL[g], marker='o', ms=3, lw=1.3, capsize=2, label=lab)
ax.set_xticks([16,36,72]); ax.set_xlabel('Hours after immunisation'); ax.set_ylabel('Lung Gm-csf mRNA, fold (mean ± SD)'); ax.set_title('c  GM-CSF mRNA in lung (aged, n=5) [S02-F]', fontsize=7.6)
ax.legend(frameon=False, fontsize=6.4, loc='upper right', labelspacing=0.25); ax.set_ylim(0, 12.5)
# (d) CD11b+ DC time course
ax = fig.add_subplot(gs[1,1]); d = T['S01-E'].copy(); d['day'] = d['day'].astype(int)
for g,lab in [('Sham','Empty liposome, aged'),('PSLN-212','PSLN-212, aged'),('PSLN-344','PSLN-344, aged'),('PSLN-212(Y)','PSLN-212, young'),('PSLN-344(Y)','PSLN-344, young')]:
    m = d[d.group==g].groupby('day')['value'].agg(['mean','std'])
    ax.errorbar(m.index + {'Sham':-0.16,'PSLN-212':-0.08,'PSLN-344':0,'PSLN-212(Y)':0.08,'PSLN-344(Y)':0.16}[g], m['mean'], yerr=m['std'], color=COL[g], marker='o', ms=3, lw=1.3, capsize=2, label=lab, ls='-' if '(Y)' not in g else '--')
ax.set_xticks([0,2,4,6,8]); ax.set_xlabel('Days after immunisation'); ax.set_ylabel('CD11b+ dendritic cells, % (mean ± SD)'); ax.set_title('d  Monocyte-derived DC in lung (n=5) [S01-E]', fontsize=7.6)
ax.legend(frameon=False, fontsize=6.2, loc='upper left', labelspacing=0.2, handlelength=1.8); ax.set_ylim(0, 31)
fig.savefig(OUT+'fig5_pharmacodynamics.png'); print('ok')
