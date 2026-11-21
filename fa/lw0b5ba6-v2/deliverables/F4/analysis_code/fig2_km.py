import pandas as pd, numpy as np
from lifelines import KaplanMeierFitter
from fig_style import *
S = pd.read_csv('surv_long.csv'); S = S[S.day.notna()]
core7 = ['S03-I','S06-A','S06-B','S06-C','S06-E','S06-F','S06-G']
fig, axes = plt.subplots(1, 3, figsize=(FIGW, 3.55), gridspec_kw={'wspace':0.2, 'left':0.07, 'right':0.995, 'top':0.92, 'bottom':0.37})
def fmt(ax):
    ax.set_xlim(0,14.3); ax.set_ylim(-3,104); ax.set_xticks(range(0,15,2))
ax = axes[0]
for g in ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']:
    d = S[S.block.isin(core7)&(S.group==g)]
    km = KaplanMeierFitter().fit(d.day, d.event)
    sf = km.survival_function_; ci = km.confidence_interval_
    ax.step(sf.index, 100*sf.iloc[:,0], where='post', color=COL[g], lw=1.6, label=f"{LAB[g]}: {int((d.event==0).sum())}/{len(d)}")
    ax.fill_between(ci.index, 100*ci.iloc[:,0], 100*ci.iloc[:,1], step='post', color=COL[g], alpha=0.12, lw=0)
fmt(ax); ax.set_xlabel('Days after challenge'); ax.set_ylabel('Survival, %')
ax.set_title('A  Aged BALB/c, 7 experiments', loc='left', fontweight='bold'); ax.legend(frameon=False, loc='upper left', fontsize=6.5, bbox_to_anchor=(-0.12,-0.24), ncol=1, handlelength=1.6)
ax = axes[1]
sets = [('challenge day 3 (S06-B)', ['S06-B'], ':'), ('day 14 (S03-I, S06-A, C)', ['S03-I','S06-A','S06-C'], '-'), ('day 60 (S06-E, F, G)', ['S06-E','S06-F','S06-G'], '--')]
for lab, bl, ls in sets:
    d = S[S.block.isin(bl)&(S.group=='PSLN-344')]
    km = KaplanMeierFitter().fit(d.day, d.event); sf = km.survival_function_
    ax.step(sf.index, 100*sf.iloc[:,0], where='post', color=COL['PSLN-344'], lw=1.6, ls=ls, label=f"PSLN-344, {lab}: {int((d.event==0).sum())}/{len(d)}")
d = S[S.block.isin(['S06-E','S06-F','S06-G'])&(S.group=='Untreated')]
km = KaplanMeierFitter().fit(d.day, d.event); sf = km.survival_function_
ax.step(sf.index, 100*sf.iloc[:,0], where='post', color=COL['Untreated'], lw=1.6, label=f"Aged, NOT challenged (S06-E, F, G): {int((d.event==0).sum())}/{len(d)}")
fmt(ax); ax.set_xlabel('Days after challenge (or observation start)', fontsize=6.8); ax.set_yticklabels([])
ax.set_title('B  PSLN-344 by time since dose', loc='left', fontweight='bold'); ax.legend(frameon=False, loc='upper left', fontsize=6.5, bbox_to_anchor=(-0.08,-0.24), ncol=1, handlelength=1.6)
ax = axes[2]
for g, lab in [('3d Vaccine','Vaccine alone'),('3d PSLN-344','PSLN-344 alone (no antigen)'),('3d Vaccine+PSLN-344','Vaccine + PSLN-344')]:
    d = S[(S.block=='S15-H')&(S.group==g)]
    km = KaplanMeierFitter().fit(d.day, d.event); sf = km.survival_function_
    c = {'3d Vaccine':COL['Sham'],'3d PSLN-344':'#9ecae1','3d Vaccine+PSLN-344':COL['PSLN-344']}[g]
    ax.step(sf.index, 100*sf.iloc[:,0], where='post', color=c, lw=1.6, label=f"{lab}: {int((d.event==0).sum())}/{len(d)}")
fmt(ax); ax.set_xlabel('Days after H5N1 challenge'); ax.set_yticklabels([])
ax.set_title('C  Antigen is required (S15-H)', loc='left', fontweight='bold'); ax.legend(frameon=False, loc='upper left', fontsize=6.5, bbox_to_anchor=(0.0,-0.24), ncol=1, handlelength=1.6)
fig.savefig(OUT+'Fig2_kaplan_meier.png'); print('ok')
