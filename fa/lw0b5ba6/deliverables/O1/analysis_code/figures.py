import pandas as pd, numpy as np, warnings, matplotlib
warnings.filterwarnings('ignore')
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from lifelines import KaplanMeierFitter
from statsmodels.stats.proportion import proportion_confint
OUT = '/tmp/outputs/figures'
import os; os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.size':9, 'font.family':'DejaVu Sans', 'axes.spines.top':False, 'axes.spines.right':False})
COL = {'Sham':'#9e9e9e','PSLN-212':'#e6862e','PSLN-344':'#1f5fa8','PSLN-212(Y)':'#3a9e5a'}
df = pd.read_csv('/tmp/work/tidy.csv')
tiers = pd.read_csv('/tmp/work/evidence_tiers.csv').set_index('block').tier.to_dict()
s = df[df.event.notna() & (df.block!='S08-UNLABELLED')]

# ---------------- Fig 1: survival dot plot across aged experiments ----------------
exps = [('S06-B','H3 vacc -> PR8 (H1), d3'),('S06-D','H1+H3 -> rgH5N1, d3'),('S06-A','H3 vacc -> PR8 (H1), d14'),('S06-C','H1+H3 -> rgH5N1, d14'),
        ('S06-E','H3 vacc -> PR8 (H1), d60'),('S06-F','H1+H3 -> rgH5N1, d60'),('S06-G','H1 vacc -> Perth (H3), d60'),
        ('S15-L','C57BL/6 aged (challenge n.s.)'),('S15-N','Swiss Webster aged (challenge n.s.)'),('S03-I','CA09 10x homologous, d14')]
groups = ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']
fig, ax = plt.subplots(figsize=(8.2,5.6))
y=0; yt=[]; yl=[]
for b,lab in exps:
    for k,g in enumerate(groups):
        sub = s[(s.block==b)&(s.group==g)]
        if sub.empty: continue
        n=len(sub); sv=int((sub.event==0).sum()); lo,hi = proportion_confint(sv,n,method='wilson')
        yy = y + (k-1.5)*0.17
        ax.plot([100*lo,100*hi],[yy,yy],color=COL[g],lw=1.2,alpha=0.7)
        ax.plot(100*sv/n, yy, 'o', color=COL[g], ms=5.5, mec='white', mew=0.5)
    yt.append(y); yl.append(f'{b} [{tiers.get(b,"?")}]  {lab}'); y+=1
# pooled
P = pd.read_csv('/tmp/work/surv_pooled.csv')
y+=0.4
pool = {'Sham':(0,63),'PSLN-212':(8,63),'PSLN-344':(51,63),'PSLN-212(Y)':(62,63)}
for k,g in enumerate(groups):
    sv,n = pool[g]; lo,hi = proportion_confint(sv,n,method='wilson'); yy=y+(k-1.5)*0.17
    ax.plot([100*lo,100*hi],[yy,yy],color=COL[g],lw=2.2); ax.plot(100*sv/n,yy,'D',color=COL[g],ms=6.5,mec='black',mew=0.6)
yt.append(y); yl.append('POOLED 9 aged 4-arm blocks (S06-A..G, S15-L/N)')
ax.set_yticks(yt); ax.set_yticklabels(yl, fontsize=7.8); ax.invert_yaxis()
ax.set_xlabel('Survival at end of observation (%), dot = observed, bar = Wilson 95% CI')
ax.set_xlim(-3,103); ax.axvline(50,color='#dddddd',lw=0.8,zorder=0)
ax.legend(handles=[Patch(color=COL[g],label=(g+' (aged)' if '(Y)' not in g else 'PSLN-212 (young)')) for g in groups], loc='upper center', bbox_to_anchor=(0.45,-0.09), ncol=4, fontsize=7.5, frameon=False)
fig.suptitle('Fig. 1  Survival after lethal influenza challenge in aged mice (n=7/group/experiment)\n[tier] = evidence tier from integrity audit. Pooled PSLN-344 vs PSLN-212: MH risk difference +68 pts (95% CI 56-79)', fontsize=8.8, x=0.01, ha='left')
plt.tight_layout(rect=(0,0,1,0.95)); plt.savefig(f'{OUT}/fig1_survival_aged.png', dpi=200); plt.close()

# ---------------- Fig 2: KM curves, tier-A aged experiments ----------------
fig, axs = plt.subplots(1,4, figsize=(10,2.8), sharey=True)
for ax,(b,lab) in zip(axs,[('S06-A','H3 vacc -> PR8, d14'),('S06-B','H3 vacc -> PR8, d3'),('S06-E','H3 vacc -> PR8, d60'),('S06-F','H1+H3 -> rgH5N1, d60')]):
    for g in groups:
        sub = s[(s.block==b)&(s.group==g)]
        kmf = KaplanMeierFitter().fit(sub.time, sub.event)
        ax.step(kmf.survival_function_.index, 100*kmf.survival_function_.iloc[:,0], where='post', color=COL[g], lw=1.8, label=g)
    ax.set_title(f'{b}: {lab}', fontsize=8); ax.set_xlabel('days post-challenge'); ax.set_xlim(0,14.5); ax.set_ylim(-3,103)
axs[0].set_ylabel('% surviving'); axs[-1].legend(fontsize=6.5, frameon=False, loc='lower left')
fig.suptitle('Fig. 2  Kaplan-Meier curves, Tier-A aged challenge experiments (S06 sheet)', fontsize=9, x=0.01, ha='left')
plt.tight_layout(); plt.savefig(f'{OUT}/fig2_km_tierA.png', dpi=200); plt.close()

# ---------------- Fig 3: restoration index cascade ----------------
RI = pd.read_csv('/tmp/work/restoration_index.csv')
sel = [('S01-A_16h',None,'Lung Ifnb1, 16 h','Innate trigger'),
       ('S01-D',4.0,'Lung monocytes, d4','Myeloid recruitment'),('S01-E',4.0,'Lung CD11b+ DC, d4','Myeloid recruitment'),
       ('S01-F',None,'Lung cDC1, 72 h','DC'),('S02-A',None,'CCR7+ migratory DC, 72 h','DC'),('S02-B',None,'MLN CD11b+ DC, 72 h','DC'),
       ('S02-C',None,'Antigen+ DC in MLN, 36 h','DC'),('S02-D_CD40',None,'CD40+ MLN DC, d3','DC'),('S02-D_CD86',None,'CD86+ MLN DC, d3','DC'),
       ('S02-E',None,'OT-I priming by MLN DC','DC'),
       ('S04-A_ICOShi',None,'Tfh ICOS-hi, d7','B/Tfh'),('S04-B_Foxp3',None,'Tfr (lower=better), d7','B/Tfh'),('S03-K',None,'GC B cells, d7','B/Tfh'),
       ('S03-A',None,'IgG anti-CA09, d14','Antibody'),('S03-C',None,'HAI anti-CA09, d14','Antibody'),('S03-D',None,'Neut anti-CA09, d14','Antibody'),
       ('S03-E',None,'IgG anti-Aichi, d14','Antibody'),('S03-G',None,'HAI anti-Aichi, d14','Antibody'),('S13-AB_ratio_CA09',None,'IgG2a/IgG1 (recomputed)','Antibody'),
       ('S05-D',None,'Lung Ki-67+ CD8, d3','CD8'),('S05-E',None,'Lung GZMB+ CD8, d3','CD8'),('S05-F',None,'X-reactive IFNg+ CD8, d14','CD8'),
       ('S05-G',None,'X-reactive IFNg+ CD8, d60','CD8'),('S05-I',None,'Lung TRM CD8, d25','CD8'),('S04-D',None,'Lung Treg (lower=better), d7','Regulatory'),
       ('S11-E',None,'CD206+ macrophages (lower=better)','Regulatory')]
rows=[]
for b,t,lab,stage in sel:
    r = RI[(RI.block==b) & ((RI.time.isna()) if t is None else (RI.time==t))].iloc[0]
    rows.append((lab,stage,r.RI,r.RI_lo,r.RI_hi,b))
# add survival RI (pooled): (81-13)/(98-13)
rows.append(('Survival, heterosubtypic challenge (pooled)','Protection',(51/63-8/63)/(62/63-8/63),np.nan,np.nan,'S06/S15'))
R = pd.DataFrame(rows, columns=['lab','stage','ri','lo','hi','block'])
stc = {'Innate trigger':'#1f5fa8','Myeloid recruitment':'#2c7fb8','DC':'#7b3294','B/Tfh':'#c2a5cf','Antibody':'#008837','CD8':'#a6611a','Regulatory':'#666666','Protection':'#d7191c'}
fig, ax = plt.subplots(figsize=(7.8,7.2))
for i,r in R.iterrows():
    c = stc[r.stage]
    if np.isfinite(r.lo): ax.plot([r.lo,r.hi],[i,i],color=c,lw=1.3)
    ax.plot(r.ri,i,'o' if r.stage!='Protection' else 'D',color=c,ms=6)
ax.axvline(0,color='k',lw=0.8); ax.axvline(1,color='k',lw=0.8,ls='--')
ax.set_yticks(range(len(R))); ax.set_yticklabels([f'{a}  ({b})' for a,b in zip(R.lab,R.block)], fontsize=7.3); ax.invert_yaxis()
ax.set_xlim(-0.3,1.65)
ax.set_xlabel('Restoration index (RI), bootstrap 95% CI\nRI = (aged PSLN-344 - aged PSLN-212) / (young PSLN-212 - aged PSLN-212)\n0 = no gain over PSLN-212 in aged; 1 = matches young benchmark', fontsize=8)
ax.legend(handles=[Patch(color=v,label=k) for k,v in stc.items()], fontsize=7, frameon=False, loc='lower right')
ax.set_title('Fig. 3  Where Mn2+ (PSLN-344) closes the age gap, and where it does not\n(log scale for titres and fold-changes; Tier A/B blocks only)', fontsize=9, loc='left')
plt.tight_layout(); plt.savefig(f'{OUT}/fig3_restoration_cascade.png', dpi=200); plt.close()
R.to_csv('/tmp/work/fig3_data.csv', index=False)

# ---------------- Fig 4: dose response + Ifnb1 aged vs young ----------------
fig, axs = plt.subplots(1,2, figsize=(9,3.4))
d = df[df.block=='S08-A']; cd = {'CMP-204':'#8c564b','PSLN-212':COL['PSLN-212'],'PSLN-344':COL['PSLN-344'],'PSLN-344/R848':'#17becf'}
for g,sub in d.groupby('group'):
    m = sub.groupby('time').value.agg(['mean','std'])
    axs[0].errorbar(m.index, m['mean'], yerr=m['std'], color=cd[g], marker='o', ms=4, capsize=2, lw=1.4, label=g)
axs[0].set_xscale('log'); axs[0].set_xticks([1,5,10,20,40]); axs[0].set_xticklabels(['1','5','10','20','40'])
axs[0].set_xlabel('dose (µg/mouse, intranasal)'); axs[0].set_ylabel('lung Ifnb1, fold vs untreated (16 h)')
axs[0].set_title('S08-A dose-response (n=3/dose; mean±SD)', fontsize=8.5); axs[0].legend(fontsize=7, frameon=False)
a = df[df.block=='S01-A_16h']
order = ['Sham','CMP-204','PSLN-R848','PSLN-212','PSLN-212/R848','PSLN-344','PSLN-212(Y)','PSLN-344(Y)']
for i,g in enumerate(order):
    v = a[a.group==g].value.values
    c = COL.get(g.replace('(Y)',''), '#8c564b') if '(Y)' not in g else ('#3a9e5a' if g=='PSLN-212(Y)' else '#6fa8dc')
    axs[1].bar(i, np.exp(np.log(v).mean()), color=c, alpha=0.85)
    axs[1].plot(np.full(len(v),i)+np.linspace(-0.15,0.15,len(v)), v, 'k.', ms=3)
axs[1].set_xticks(range(len(order))); axs[1].set_xticklabels(order, rotation=40, ha='right', fontsize=7)
axs[1].set_ylabel('lung Ifnb1, fold (geo-mean, 16 h)'); axs[1].set_title('S01-A: aged vs young (Y), n=5', fontsize=8.5)
fig.suptitle('Fig. 4  STING target engagement: Mn2+ restores aged Ifnb1 to the young level and gives >=4x dose-sparing', fontsize=9, x=0.01, ha='left')
plt.tight_layout(); plt.savefig(f'{OUT}/fig4_dose_ifnb1.png', dpi=200); plt.close()

# ---------------- Fig 5: safety ----------------
fig, axs = plt.subplots(1,2, figsize=(9,3.3))
cn = {'PBS':'#bdbdbd','Sham':'#9e9e9e','PSLN-344':COL['PSLN-344'],'CT':'#d62728'}
for j,(b,lab) in enumerate([('S10-A_Ifnb1','Ifnb1'),('S10-A_Tnf','Tnf'),('S10-A_Isg15','Isg15')]):
    for k,g in enumerate(['PBS','Sham','PSLN-344','CT']):
        v = df[(df.block==b)&(df.group==g)].value.values
        x = j*5+k
        axs[0].bar(x, v.mean(), color=cn[g]); axs[0].plot(np.full(len(v),x)+np.linspace(-0.2,0.2,len(v)), v, 'k.', ms=3)
axs[0].set_xticks([1.5,6.5,11.5]); axs[0].set_xticklabels(['Ifnb1','Tnf','Isg15'])
axs[0].set_ylabel('CNS transcript, fold vs untreated (36 h)'); axs[0].set_title('S10-A CNS inflammation (aged, n=5)', fontsize=8.5)
axs[0].legend(handles=[Patch(color=v,label=k+(' (cholera toxin)' if k=='CT' else '')) for k,v in cn.items()], fontsize=7, frameon=False)
w = df[df.block=='S08-D']
cw = {'Vaccine':'#bdbdbd','PSLN-212(Y)':COL['PSLN-212(Y)'],'CMP-204':'#8c564b','PSLN-212':COL['PSLN-212'],'PSLN-344':COL['PSLN-344'],'PSLN-212/R848':'#9467bd'}
for g,sub in w.groupby('group'):
    m = sub.groupby('time').value.agg(['mean','count'])
    axs[1].plot(m.index, m['mean'], marker='o', ms=3, color=cw[g], lw=1.5, label=f'{g}' + (' (1 animal lost by d10)' if g=='PSLN-212/R848' else ''))
axs[1].set_xlabel('days after vaccination (no challenge)'); axs[1].set_ylabel('body weight, % of day 0 (mean)')
axs[1].set_title('S08-D reactogenicity (n=5; Tier B)', fontsize=8.5); axs[1].legend(fontsize=6.5, frameon=False)
fig.suptitle('Fig. 5  Safety signals available in the package (no Mn biodistribution, histopathology or repeat-dose data exist)', fontsize=9, x=0.01, ha='left')
plt.tight_layout(); plt.savefig(f'{OUT}/fig5_safety.png', dpi=200); plt.close()

# ---------------- Fig 6: integrity evidence ----------------
fig, axs = plt.subplots(1,3, figsize=(11,3.6))
a = df[(df.block=='S15-C')&(df.group=='PSLN-344')&(df.time>0)]; b_ = df[(df.block=='S15-I')&(df.group=='3d Vaccine+PSLN-344')&(df.time>0)]
m = a.merge(b_, on=['time','rep'], suffixes=('_c','_i'))
same = m.value_c==m.value_i
axs[0].scatter(m.value_c[same], m.value_i[same], s=14, color='#d7191c', label=f'identical ({same.sum()}/{len(m)})')
axs[0].scatter(m.value_c[~same], m.value_i[~same], s=14, color='#2c7bb6', label='different')
axs[0].plot([75,105],[75,105],'k--',lw=0.7); axs[0].set_xlabel('S15-C PSLN-344 (rgH5N1 at d14)'); axs[0].set_ylabel('S15-I Vaccine+PSLN-344 (VN04 at d3)')
axs[0].set_title('Same animal position & day, two different experiments', fontsize=8); axs[0].legend(fontsize=7, frameon=False)
a = df[(df.block=='S11-A')]; b_ = df[(df.block=='S11-B')]
m = a.merge(b_, on=['group','time','rep'], suffixes=('_am','_neu'))
same = m.value_am==m.value_neu
axs[1].scatter(m.value_am[same], m.value_neu[same], s=14, color='#d7191c', label=f'identical ({same.sum()}/{len(m)})')
axs[1].scatter(m.value_am[~same], m.value_neu[~same], s=14, color='#2c7bb6', label='different')
axs[1].plot([10,55],[10,55],'k--',lw=0.7); axs[1].set_xlabel('S11-A alveolar macrophages (%)'); axs[1].set_ylabel('S11-B neutrophils (%)')
axs[1].set_title('Two different cell types, same animals', fontsize=8); axs[1].legend(fontsize=7, frameon=False)
T = pd.read_csv('/tmp/work/evidence_tiers.csv')
T['sheet'] = T.block.str[:3]
ct = pd.crosstab(T.sheet, T.tier).reindex(columns=['A','B','C','D'], fill_value=0)
bottom = np.zeros(len(ct)); tc = {'A':'#1a9641','B':'#fdae61','C':'#d7191c','D':'#abd9e9'}
for t in ['A','B','C','D']:
    axs[2].bar(ct.index, ct[t], bottom=bottom, color=tc[t], label={'A':'A usable','B':'B caveat','C':'C excluded','D':'D derived'}[t]); bottom += ct[t].values
axs[2].set_ylabel('number of data blocks'); axs[2].tick_params(axis='x', rotation=60, labelsize=7); axs[2].legend(fontsize=7, frameon=False)
axs[2].set_title('Evidence tier by sheet (108 blocks)', fontsize=8)
fig.suptitle('Fig. 6  Data-integrity findings that must be resolved before investment (details: integrity register I-01..I-23)', fontsize=9, x=0.01, ha='left')
plt.tight_layout(); plt.savefig(f'{OUT}/fig6_integrity.png', dpi=200); plt.close()
print('figures written')
