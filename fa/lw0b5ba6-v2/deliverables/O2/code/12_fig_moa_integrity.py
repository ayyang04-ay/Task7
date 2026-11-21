import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from lifelines import KaplanMeierFitter
plt.rcParams.update({'font.family':'DejaVu Sans'})
OUT='/tmp/outputs/figures/'
# ---------------- Fig 6: MoA schematic ----------------
fig=plt.figure(figsize=(11,11.0)); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,100); ax.set_ylim(19,120); ax.axis('off')
def box(x,y,w,h,title,body,fc,ls='-',ec='#333333'):
    b=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.4,rounding_size=1.2',fc=fc,ec=ec,lw=1.2,ls=ls); ax.add_patch(b)
    ax.text(x+1,y+h-1.2,title,fontsize=9.2,fontweight='bold',va='top')
    ax.text(x+1,y+h-4.0,body,fontsize=7.6,va='top',linespacing=1.3)
def arrow(x1,y1,x2,y2,style='-|>',ls='-'):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle=style,mutation_scale=14,lw=1.4,color='#333333',ls=ls))
ax.text(2,118.2,'Fig 6. Proposed mechanism of action of PSLN-344 in the aged lung, with the supporting data',fontsize=12,fontweight='bold',va='top')
ax.text(2,115.2,'Numbers are aged PSLN-344 vs aged PSLN-212 unless stated (group means; [block]). Solid border = direct intervention evidence; dashed = correlative or inferred, needs confirmation.',fontsize=8,va='top')
# tier 1
box(2,100,46,12,'1  Delivery: surfactant-mimetic liposome',
    'DPPC/DPPG/DPPE-PEG2000/cholesterol carrying CDN-1807 (+ Mn2+ in PSLN-344)\nTargets type II > type I alveolar epithelium: SRB+ 15.8% vs 3.8%; free dye 0.4%  [S01-B]\nAlveolar-macrophage uptake needs SP-A/SP-D: 43.1% WT vs 12.7% Sftpa1/Sftpd-KO  [S01-C]\nOpen: Mn2+ version may shift uptake away from epithelium (3.8% vs 15.8%) [S08-C, DI-09]','#eef3fb')
box(52,100,46,12,'2  Sensing: Mn2+ amplifies CDN-driven IFN-b (STING inferred)',
    'Aged lung under-responds: Ifnb1 16 h = 16.5x (aged, no Mn) vs 37.5x (young)  [S01-A]\nMn2+ restores it: 36.9x (98% of the age gap; GMR 2.23, Tukey p=0.0006)  [S01-A]\nRaises the ceiling, not only potency: top 52x vs 16x, ED50 11 vs 10 ug  [S08-A]\nNot more drug: encapsulation 55% vs 60% (p=0.29)  [S08-B]\nUntested: STING-KO, Mn-only liposome (attribution)','#fdecea',ls='--')
arrow(48,106,52,106)
# tier 2
box(2,80,46,16,'3  Local amplification and chemokines',
    'Gap-junction spread: carbenoxolone cuts monocyte recruitment\n7.3% -> 3.1% (p=0.003)  [S11-C]  (non-specific blocker; inferred)\nCcl2 590x vs 7.6x; Ccl3 30x vs 1.1x; Il6 36x vs 5.6x at 16 h  [S09-A*]\nGm-csf 8.5x vs 1.6x at 36 h (GMR 5.4, p<0.0001)  [S02-F]\nSafety watch: aged PSLN-344 lungs still Il6 7.2x, Tnf 8.4x at ~72 h\n(young 3.1x, 0.5x)  [S09-A panel 2, DI-08]','#fdf5e6',ls='--')
box(52,80,46,16,'4  Monocyte -> moDC program (IFNAR + GM-CSF)',
    'CCR2-dependent monocyte influx: 30.6% vs 16.7% at d4  [S01-D];\nINCB3344 cuts 9.9% -> 3.3%  [S07-B]\nmoDC formation needs IFNAR: 19.7% (WT BM) vs 2.1% (IFNAR-KO BM)  [S02-H]\nGM-CSF rescues IFNAR-KO to 12.4%  [S02-H]; GM-CSF add-back to Mn-free\nPSLN-212 raises moDC-like cells 5.9% -> 13.8%  [S02-G]\nWithout Mn: Ly6C+CCR2+ macrophages pile up (19.0 vs 3.4 x10^5 at d5) [S07-A]\nand CD206+ macrophages stay high (71.5% vs 48.9%)  [S11-E]','#eef8ee')
arrow(25,100,25,96); arrow(75,100,75,96); arrow(48,88,52,88)
# tier 3
box(2,64,96,12,'5  Dendritic-cell mobilisation, migration and antigen presentation',
    'Lung CD11b+ DC 18.9% vs 8.3% (d4) [S01-E];  cDC1 37.5% vs 22.8% (72 h) [S01-F];  CCR7+ migratory DC 30.7% vs 7.3% [S02-A];  MLN CD11b+ DC 36.8% vs 18.2% [S02-B]\n'
    'Antigen+ DC in MLN 7.1% vs 1.8% (36 h) [S02-C];  DC priming of OT-I CD8 18.7% vs 0.8% [S02-E];  migration is Gai-dependent: pertussis toxin cuts MLN priming 30.9% -> 6.8% [S05-C]\n'
    'WEAK LINK: co-stimulation only partly restored - CD40+ 11.2% vs 5.6% (young 38.7%), CD86+ 14.5% vs 8.1% (young 37.9%): ~20% of the age gap [S02-D]\n'
    'Tolerogenic tone falls: lung Treg 3.0% vs 6.7% (d7) [S04-D]','#eef3fb')
arrow(50,80,50,76.4)
# tier 4
box(2,40.5,47,20,'6a  Humoral: Tfh / germinal centre -> antibody',
    'ICOS-high Tfh 10.3% vs 3.8%; Tfr 10.8% vs 26.7% (d7) [S04-A/B]\nTfr back to 14.0% vs 18.0% by d30 (n.s.) [S04-C]\nGC B cells 6.5% vs 2.3% (d7) [S03-K]; Aicda 3.5x, E47 3.9x (n=3) [S03-L]\nIgG+ B cells 25.9% vs 11.2% [S13-H]\n\nd14 GMT: HAI 368 vs 46 (CA09), 320 vs 35 (Aichi); neut 8-9x;\nIgG 13-19x  [S03-A,C,D,E,G,H]\nTh1-type: IgG2a/IgG1 1.85 vs 0.54 (CA09), 2.30 vs 0.46 (Aichi)\n[S13-A-D; S03-B/F labels rotated, DI-04]','#eef3fb')
box(51,40.5,47,20,'6b  Cellular: CD8 effector and tissue-resident memory',
    'Early expansion: Ki-67+ CD8 9.4% vs 3.5%; GZMB+ 5.7% vs 3.0% (d3) [S05-D/E]\nIFN-g+ CD8 (H5 restim) 6.4% vs 1.5% (d14) [S05-F];\nH1 / H3 restim 11.0% vs 3.1%, 9.9% vs 3.6% [S14-A]\nLung TRM (CD69+CD103+) 4.0% vs 1.0% (d25) [S05-I]\nMemory at d60: IFN-g+ 9.9% vs 3.0%, GZMB+ 4.1% vs 1.0% [S05-G/H]\nCCR2-dependent: INCB3344 cuts GZMB+ CD8 6.8% -> 1.4% (young) [S02-I]\n\nLikely basis of heterosubtypic protection (conserved internal antigens;\nno per-animal link shown)','#fdecea')
arrow(25,64,25,60.9); arrow(75,64,75,60.9)
# tier 5
box(2,21.5,96,15,'7  Outcome in aged mice (single intranasal dose; 8 experiments, 59 animals per arm)',
    'Survival PSLN-344 49/59 (83%) vs PSLN-212 7/59 (12%) vs vaccine + empty liposome 1/59 (2%); stratified Cox HR 0.083 (0.041-0.167)  [S03-I, S03-J, S06-A/B/C/E/F/G]\n'
    'Heterosubtypic challenges 32/42 (76%) vs 4/42 (10%); challenge 2-3 d after vaccination 15/17 (88%) vs 3/17 (18%); wild-type H5N1 10/10 vs 3/10 [S03-J]\n'
    'Middle-aged (14 mo) mice, with or without prior infection: 12/14 vs 0/14 (naive) and 12/14 vs 4/14 (imprinted)  [S06-E/F imprint]\n'
    'LIMITS: day-60 survival 14/21 (67%) vs young 21/21 (p=0.009); survivors still lose more weight (nadir 87.3% vs 89.8%, p=0.004);\n'
    'young mice are protected by all adjuvants tested (PSLN-212, PSLN-344, CMP-204), so the edge is age-specific','#f3eefa')
arrow(25,40.5,25,36.9); arrow(75,40.5,75,36.9)
fig.savefig(OUT+'fig6_moa_schematic.png',dpi=170); plt.close()

# ---------------- Fig 8: integrity exhibits ----------------
S=pd.read_csv('/tmp/work/tidy/survival.csv'); B=pd.read_csv('/tmp/work/tidy/bodyweight.csv'); C=pd.read_csv('/tmp/work/tidy/continuous.csv'); C['time']=C['time'].astype(str)
COL={'Sham':'#8c8c8c','PSLN-212':'#3b75af','PSLN-344':'#d6452a','PSLN-212(Y)':'#2e9e5b'}
fig,axs=plt.subplots(2,2,figsize=(11,8))
ax=axs[0,0]
for blk,ls,lw in [('S06-C','-',3.2),('S06-D','--',1.4)]:
    for g in ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']:
        d=S[(S.block==blk)&(S.group==g)]
        KaplanMeierFitter().fit(d.time,d.event).plot_survival_function(ax=ax,ci_show=False,color=COL[g],ls=ls,lw=lw,legend=False,alpha=0.55 if blk=='S06-C' else 1)
ax.set_title('(a) DI-01: S06-D (challenge d3, dashed) is identical to\nS06-C (challenge d14, thick) in all 28 animals',fontsize=9,loc='left')
ax.set_xlabel('Days after challenge'); ax.set_ylabel('Fraction surviving')
ax=axs[0,1]
for blk,grp,ls,lw in [('S15-C','PSLN-344','-',3.2),('S15-I','3d Vaccine+PSLN-344','--',1.3)]:
    d=B[(B.block==blk)&(B.group==grp)]
    for a,dd in d.groupby('animal'):
        ax.plot(dd.day,dd.value,ls=ls,lw=lw,color=plt.cm.tab10(a-1),alpha=0.45 if blk=='S15-C' else 1)
ax.set_title('(b) DI-02: S15-I "3d Vaccine+PSLN-344" weights (dashed) reproduce\nS15-C PSLN-344 weights (thick), a different experiment (6/7 animals)',fontsize=9,loc='left')
ax.set_xlabel('Days after challenge'); ax.set_ylabel('Body weight, % day 0')
ax=axs[1,0]
lab=['PSLN-212','PSLN-344','PSLN-212(Y)']
for i,g in enumerate(lab):
    pr=C[(C.block=='S03-B')&(C.group==g)].sort_values('rep').value.values
    for j,g2 in enumerate(lab):
        a=C[(C.block=='S13-A')&(C.group==g2)].sort_values('rep').value.values; b=C[(C.block=='S13-B')&(C.group==g2)].sort_values('rep').value.values
        if np.allclose(pr,a/b,rtol=1e-3):
            ax.scatter(a/b,pr,s=30,label=f'printed "{g}" = computed {g2}')
ax.plot([0.2,5],[0.2,5],'k:',lw=0.8); ax.set_xscale('log'); ax.set_yscale('log')
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
for axis in (ax.xaxis, ax.yaxis):
    axis.set_major_locator(FixedLocator([0.25,0.5,1,2,4])); axis.set_major_formatter(FixedFormatter(['0.25','0.5','1','2','4'])); axis.set_minor_locator(NullLocator())
ax.set_xlabel('IgG2a/IgG1 computed from S13-A/S13-B titres'); ax.set_ylabel('IgG2a/IgG1 as printed in S03-B')
ax.legend(fontsize=7.5,frameon=False,loc='upper left')
ax.set_title('(c) DI-04: S03-B group labels are rotated relative to the\nsource titres; as printed, PSLN-344 would look Th2-biased',fontsize=9,loc='left')
ax=axs[1,1]
for g,c in [('Vaccine','#444444'),('PSLN-212','#3b75af'),('PSLN-344','#d6452a'),('PSLN-212(Y)','#2e9e5b')]:
    for t in ['0','2','4','6','8']:
        a=C[(C.block=='S11-A')&(C.group==g)&(C.time==t)].sort_values('rep').value.values
        b=C[(C.block=='S11-B')&(C.group==g)&(C.time==t)].sort_values('rep').value.values
        same=np.isclose(a,b)
        ax.scatter(a[same],b[same],color=c,marker='o',s=28)
        ax.scatter(a[~same],b[~same],color=c,marker='x',s=18,alpha=0.5)
ax.plot([10,55],[10,55],'k:',lw=0.8)
ax.set_xlabel('S11-A alveolar macrophages (%)'); ax.set_ylabel('S11-B neutrophils (%)')
ax.set_title('(d) DI-06: two different cell types share 1-2 of 5 replicate\nvalues in every group at every timepoint (circles = identical)',fontsize=9,loc='left')
fig.suptitle('Fig 8. Examples of data-integrity defects the committee should see before relying on the dataset',x=0.01,ha='left',fontsize=11,fontweight='bold')
plt.tight_layout(); fig.savefig(OUT+'fig8_integrity_exhibits.png',dpi=170); plt.close()
print('ok')
