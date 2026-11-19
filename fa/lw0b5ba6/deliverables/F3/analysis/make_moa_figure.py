"""Mechanism-of-action map, drawn at printed size (6.77 in wide; coordinates are inches, fonts are true point sizes).
All numbers are read from the analysis CSVs.  qPCR and titres: geometric means; flow cytometry: arithmetic means."""
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({'font.family':'DejaVu Sans'})
D=pd.read_csv('immunology_descriptives.csv'); T=pd.read_csv('timecourse_descriptives.csv'); P=pd.read_csv('survival_pooled.csv').iloc[1]
def m(block,group,col='centre_on_test_scale'): return float(D[(D.block==block)&(D.group==group)][col].iloc[0])
def mm(block,g): return float(D[(D.block==block)&(D.group==g)]['mean'].iloc[0])
def tc(block,group,time,col='mean'): return float(T[(T.block==block)&(T.group==group)&(T.time==time)][col].iloc[0])
W=6.77; FS=6.4; FT=7.4; LH=0.122; PADT=0.2; PADB=0.075; GAP=0.37
G=dict(I='#1a7f37',C='#555555',N='#c0392b'); LS=dict(I='-',C='--',N=':')
items=[]   # layout pass first, then draw
def box_h(n): return PADT+LH*n+PADB
boxes=[
 ('1  Delivery through the surfactant route',
  [f"Alveolar-macrophage uptake depends on surfactant proteins A and D: {m('S01-C','WT'):.0f}% (wild type) vs {m('S01-C','SPA/D'):.0f}% (knockout)   [S01-C]",
   f"Cargo reaches type-II alveolar epithelium only when formulated: {m('S01-B','AECII/PSLN-SRB'):.1f}% vs {m('S01-B','AECII/FreeSRB'):.2f}% for free dye   [S01-B]"],'#eef3fb'),
 ('2  Innate burst restored in the aged lung',
  [f"Ifnb1 at 16 h: {m('S01-A/16h','PSLN-344'):.0f}-fold vs {m('S01-A/16h','PSLN-212'):.0f}-fold (young {m('S01-A/16h','PSLN-212(Y)'):.0f}-fold); down to {m('S01-A/72h','PSLN-344'):.1f}-fold by 72 h   [S01-A]",
   f"Gm-csf at 16 / 36 / 72 h: {tc('S02-F','PSLN-344',16,'geo_mean'):.1f} / {tc('S02-F','PSLN-344',36,'geo_mean'):.1f} / {tc('S02-F','PSLN-344',72,'geo_mean'):.1f}-fold vs {tc('S02-F','PSLN-212',16,'geo_mean'):.1f} / {tc('S02-F','PSLN-212',36,'geo_mean'):.1f} / {tc('S02-F','PSLN-212',72,'geo_mean'):.1f}-fold   [S02-F]"],'#f1edf9'),
 ('3  Monocytes recruited and converted into dendritic cells',
  [f"Lung monocytes, day 4: {tc('S01-D','PSLN-344',4):.0f}% vs {tc('S01-D','PSLN-212',4):.0f}% (young {tc('S01-D','PSLN-212(Y)',4):.0f}%)   [S01-D]",
   f"Lung CD11b+ dendritic cells, day 4: {tc('S01-E','PSLN-344',4):.0f}% vs {tc('S01-E','PSLN-212',4):.0f}% (young {tc('S01-E','PSLN-212(Y)',4):.0f}%)   [S01-E]",
   f"CD206+ macrophages: {m('S11-E','PSLN-344'):.0f}% vs {m('S11-E','PSLN-212'):.0f}% (young {m('S11-E','PSLN-212(Y)'):.0f}%)   [S11-E]",
   f"Lung regulatory T cells, day 7: {m('S04-D','PSLN-344'):.1f}% vs {m('S04-D','PSLN-212'):.1f}% (young {m('S04-D','PSLN-212(Y)'):.1f}%)   [S04-D, n=3]"],'#e9f4f8'),
 ('4  Dendritic cells migrate, carry antigen to the lymph node, prime T cells',
  [f"CCR7+ migratory dendritic cells in lung: {m('S02-A','PSLN-344'):.0f}% vs {m('S02-A','PSLN-212'):.0f}% (young {m('S02-A','PSLN-212(Y)'):.0f}%)   [S02-A]",
   f"Antigen-bearing dendritic cells in lymph node: {m('S02-C','PSLN-344'):.1f}% vs {m('S02-C','PSLN-212'):.1f}% (young {m('S02-C','PSLN-212(Y)'):.1f}%)   [S02-C]",
   f"Ex vivo CD8 priming by lymph-node dendritic cells: {m('S02-E','PSLN-344'):.0f}% vs {m('S02-E','PSLN-212'):.0f}% (young {m('S02-E','PSLN-212(Y)'):.0f}%)   [S02-E]",
   f"CD40 / CD86 on those cells: {m('S02-D CD40','PSLN-344'):.0f}% / {m('S02-D CD86','PSLN-344'):.0f}% vs {m('S02-D CD40','PSLN-212'):.0f}% / {m('S02-D CD86','PSLN-212'):.0f}% (young {m('S02-D CD40','PSLN-212(Y)'):.0f}% / {m('S02-D CD86','PSLN-212(Y)'):.0f}%)   [S02-D]"],'#e9f4f8'),
]
arrows=[
 [(f"Gap-junction blocker (carbenoxolone) before PSLN-344: recruited lung monocytes {mm('S11-C','CBX-'):.1f}% to {mm('S11-C','CBX+'):.1f}%   [S11-C]",)],
 [(f"CCR2 antagonist: lung monocytes {mm('S07-B/Mono','PSLN-344'):.1f}% to {mm('S07-B/Mono','PSLN-344+INCB3344'):.1f}%   [S07-B]",
   f"Interferon-receptor-knockout marrow: monocyte-derived dendritic cells {mm('S02-H','WT w/o cDC'):.0f}% to {mm('S02-H','IFN w/o cDC'):.0f}%; added GM-CSF restores to {mm('S02-H','GMCSF'):.0f}%   [S02-H]")],
 [(f"GM-CSF added to PSLN-212: dendritic-cell-like monocyte progeny {mm('S02-G','PSLN-212'):.1f}% to {mm('S02-G','PSLN-212+GM-CSF'):.1f}%   [S02-G]",
   f"Pertussis toxin (blocks migration): antigen-bearing dendritic cells in node {mm('S02-C','PTX'):.1f}% (vs {mm('S02-C','PSLN-344'):.1f}%)   [S02-C]")],
]
b5a=('5a  Cross-reactive CD8 T cells',
     [f"Dividing lung CD8 T cells, day 3:",f"   {m('S05-D','PSLN-344'):.1f}% vs {m('S05-D','PSLN-212'):.1f}% (young {m('S05-D','PSLN-212(Y)'):.1f}%)   [S05-D]",
      f"IFN-γ+ CD8 T cells to H5N1 (not in vaccine), day 14:",f"   {m('S05-F','PSLN-344'):.1f}% vs {m('S05-F','PSLN-212'):.1f}% (young {m('S05-F','PSLN-212(Y)'):.1f}%)   [S05-F]",
      f"Lung-resident memory CD8 T cells, day 25:",f"   {m('S05-I','PSLN-344'):.1f}% vs {m('S05-I','PSLN-212'):.1f}% (young {m('S05-I','PSLN-212(Y)'):.1f}%)   [S05-I]"],'#fbeaf3')
b5b=('5b  Follicular help, germinal centres, antibody',
     [f"Helper-to-regulatory follicular T-cell ratio, day 7:",f"   {m('S04-B Tfh:Tfr','PSLN-344'):.1f} vs {m('S04-B Tfh:Tfr','PSLN-212'):.1f} (young {m('S04-B Tfh:Tfr','PSLN-212(Y)'):.1f})   [S04-B]",
      f"Germinal-centre B cells, day 7:",f"   {m('S03-K','PSLN-344'):.1f}% vs {m('S03-K','PSLN-212'):.1f}% (young {m('S03-K','PSLN-212(Y)'):.1f}%)   [S03-K]",
      f"HAI titre, day 14:",f"   {m('S03-C','PSLN-344'):.0f} vs {m('S03-C','PSLN-212'):.0f} (young {m('S03-C','PSLN-212(Y)'):.0f})   [S03-C]"],'#fdf0e4')
b6=('6  Protection of aged animals from lethal influenza challenge',
    [f"Survival, ten experiments in animals of 20 months or more: {P.arm1_surv} ({P.arm1_pct:.0f}%) vs {P.arm2_surv} ({P.arm2_pct:.0f}%)   [S03, S06, S15]",
     "Antigen is required. Dosed 3 days before challenge: PSLN-344 alone 0/7, vaccine alone 0/7, both together 6/7   [S15-H]"],'#e8f5e9')
gaps=['STING dependence of PSLN-344: no STING-deficient host or STING antagonist was used; the only knockout is of the interferon receptor.',
      'The contribution of manganese alone: no block has a manganese-only or drug-free liposome arm.',
      'Which cell senses the drug: the PSLN-344 epithelial-uptake block (S08-C) conflicts with S01-B.',
      'How the macrophage pool changes and which subset drives regulatory T cells: S07-A is unconfirmed and S07-C has one label for both groups.',
      'Which effector protects: no CD8 depletion, no serum transfer, no mucosal IgA measurement.',
      'Whether GM-CSF and CCR2 are needed for survival in aged animals: both were tested on cell counts only, CCR2-to-CD8 in young animals.']
H=sum(box_h(len(b[1])) for b in boxes)+box_h(6)+box_h(2)+GAP*5+0.25+ (0.2+LH*6+0.1) +0.42
fig=plt.figure(figsize=(W,H),dpi=300); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(0,H); ax.axis('off')
def box(x,ytop,w,title,lines,fc):
    h=box_h(len(lines)); ax.add_patch(FancyBboxPatch((x+0.02,ytop-h),w-0.04,h,boxstyle='round,pad=0.0,rounding_size=0.05',fc=fc,ec='#4d4d4d',lw=.6))
    ax.text(x+0.09,ytop-0.055,title,fontsize=FT,fontweight='bold',va='top')
    for i,l in enumerate(lines): ax.text(x+0.11,ytop-PADT-LH*i,l,fontsize=FS,va='top')
    return ytop-h
def arrow(x,y1,y2,lines,kind='I'):
    ax.add_patch(FancyArrowPatch((x,y1-0.02),(x,y2+0.02),arrowstyle='-|>',mutation_scale=7,lw=1.1,color=G[kind],ls=LS[kind]))
    ax.text(x+0.1,(y1+y2)/2,'\n'.join(lines),fontsize=6.0,color=G[kind],va='center',ha='left',linespacing=1.3)
y=H-0.02
for i,b in enumerate(boxes):
    y=box(0,y,W,*b)
    if i<3: arrow(0.45,y,y-GAP,arrows[i][0]); y-=GAP
arrow(0.45,y,y-GAP,[f"CCR2 antagonist: lung GZMB+ CD8 T cells {mm('S02-I','PSLN-344(Y)'):.1f}% to {mm('S02-I','PSLN-344(Y)+INCB3344'):.1f}%",'(young animals)   [S02-I]']); arrow(W/2+0.45,y,y-GAP,['group comparison only'],'C'); y-=GAP
ya=box(0,y,W/2,*b5a); box(W/2,y,W/2,*b5b); y=ya
arrow(0.45,y,y-GAP,['not tested: CD8 depletion'],'N'); arrow(W/2+0.45,y,y-GAP,['not tested: serum transfer'],'N'); y-=GAP
y=box(0,y,W,*b6); y-=0.12
# not established panel (two columns)
hN=0.2+LH*6+0.1
ax.add_patch(FancyBboxPatch((0.02,y-hN),W-0.04,hN,boxstyle='round,pad=0.0,rounding_size=0.05',fc='#fff5f5',ec='#c0392b',lw=.7))
ax.text(0.09,y-0.055,'Not established by this dataset',fontsize=FT,fontweight='bold',color='#c0392b',va='top')
for i,gp in enumerate(gaps):
    ax.text(0.11,y-0.2-LH*i,'- '+gp,fontsize=6.2,va='top',color='#7b241c')
y-=hN+0.1
# key
xk=0.1
for k,t in [('I','link tested by an intervention in this dataset'),('C','groups differ in the expected direction'),('N','assumed, not tested')]:
    ax.add_patch(FancyArrowPatch((xk,y-0.08),(xk+0.32,y-0.08),arrowstyle='-|>',mutation_scale=6,lw=1.0,color=G[k],ls=LS[k])); ax.text(xk+0.38,y-0.08,t,fontsize=6.0,va='center',color=G[k]); xk+=0.38+len(t)*0.047+0.25
ax.text(0.1,y-0.27,'Each line reads: aged animals on PSLN-344 vs aged animals on PSLN-212 (young animals on PSLN-212 in brackets). Square brackets give the workbook block.',fontsize=5.8,va='center',color='#333333')
fig.savefig('/tmp/outputs/figures/fig6_mechanism_of_action.png',dpi=300); plt.close(fig); print('ok',W,round(H,2))
