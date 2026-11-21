import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({'font.family':'DejaVu Sans'})
fig,ax = plt.subplots(figsize=(12,13)); ax.set_xlim(0,12); ax.set_ylim(1.2,13.9); ax.axis('off')
def box(x,y,w,h,title,body,fc):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.05,rounding_size=0.12',fc=fc,ec='#333333',lw=0.9))
    ax.text(x+0.12,y+h-0.15,title,fontsize=9.2,weight='bold',va='top')
    ax.text(x+0.12,y+h-0.48,body,fontsize=7.6,va='top',linespacing=1.35)
def arrow(x1,y1,x2,y2):
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='-|>',color='#333333',lw=1.2))
C1,C2,C3,C4,C5='#deebf7','#fee0d2','#e5f5e0','#f2f0f7','#fff7bc'
box(0.3,11.55,5.5,1.45,'1  Delivery: surfactant-mimetic liposome',
    'AECII take up PSLN 15.8% vs 0.38% free dye (S01-B, T9)\nAlveolar-macrophage uptake SP-A/D-dependent:\n43.1% WT vs 12.7% Sftpa1/Sftpd-/- (S01-C, T9)\nCaveat: Mn particle AEC uptake 76-78% LOWER (S08-C, T9)',C1)
box(6.2,11.55,5.5,1.45,'2  STING activation; Mn2+ raises the ceiling',
    'Lung Ifnb1 16 h: PSLN-344 36.9x vs PSLN-212 16.5x vs young\n37.5x -> restoration index 0.98 (S01-A, T4/T11)\nDose-response Emax 52 vs 16, EC50 11.5 vs 9.5 ug;\n7.3 ug PSLN-344 = 20 ug PSLN-212 (S08-A, T10)',C2)
arrow(5.8,12.3,6.2,12.3)
box(0.3,9.55,5.5,1.6,'3  Paracrine amplification',
    'Gap-junction block (carbenoxolone) cuts recruited\nmonocytes 58% (7.3 -> 3.1%) (S11-C, T9)\nGm-csf 4.2-5.4x PSLN-212 at 16-36 h (S02-F, T4)\nCcl2 77x, Ccl3 27x, Ccl5 7.6x PSLN-212 at 16 h\n(S09-A block 1, T6)',C2)
arrow(8.9,11.55,5.0,11.15)
box(6.2,9.55,5.5,1.6,'4  Monocyte recruitment (CCR2-dependent)',
    'Lung monocytes d4: 30.6% vs 16.7% (S01-D, T4)\nCCR2 antagonist INCB3344: monocytes -67%,\nLy6C+ macrophages -84% (S07-B, T9)\nRecruitment only partly IFNAR-dependent\n(21.3 vs 15.4%, p=0.12, n=3; S12-A)',C2)
arrow(5.8,10.35,6.2,10.35)
box(0.3,7.45,5.5,1.7,'5  Monocyte -> moDC needs type I IFN + GM-CSF',
    'Ifnar-/- marrow: moDC 2.1% vs WT 19.7% (S02-H, T9)\nGM-CSF partly rescues Ifnar-/- (12.4%) (S02-H)\nAged + PSLN-212: adding GM-CSF raises moDC\n5.9 -> 13.8% (S02-G) => GM-CSF is limiting in aged lung\nand Mn2+ supplies it (step 3)',C3)
arrow(8.9,9.55,5.0,9.15)
box(6.2,7.45,5.5,1.7,'6  DC mobilisation & antigen transport',
    'CD11b+ DC d4 18.9 vs 8.3%; cDC1 37.5 vs 22.8% (S01-E/F)\nCCR7+ migratory DC 30.7 vs 7.3% (S02-A)\nAntigen+ DC in MLN 7.1 vs 1.8%; blocked by PTX (S02-C)\nRESIDUAL GAP: CD40/CD86 on MLN DC only 17-22%\nrestored (11.2 vs 38.7% CD40) (S02-D, T11)',C3)
arrow(5.8,8.3,6.2,8.3)
box(0.3,4.9,3.7,2.1,'7a  Follicular help / antibody',
    'MLN DC prime OT-I: 18.7 vs 0.8%\n(S02-E)\nICOS-hi Tfh 10.3 vs 3.8% (S04-A)\nGC B 6.5 vs 2.3% (S03-K)\nAicda 3.5x, E47 3.9x (S03-L)',C4)
box(4.15,4.9,3.7,2.1,'7b  CD8 effector & memory',
    'Lung Ki-67+ CD8 d3 9.4 vs 3.5%\nIFNg+ CD8, H5N1 recall:\n  d14 6.4 vs 1.5%; d60 9.9 vs 3.0%\nLung TRM d25 4.0 vs 1.0% (S05)\nGZMB+ CD8 needs CCR2 (-79%; S02-I)',C4)
box(8.0,4.9,3.7,2.1,'7c  Regulatory brake released',
    'Tfr 10.8 vs 26.7% (S04-B)\nLung Treg 3.0 vs 6.7% (S04-D)\nCD206+ macrophages 48.9 vs 71.5%\n(S11-E)\nLy6C+CCR2+ macrophages d5 -82%\n(S07-A)  [S07-C causal test unreadable]',C4)
arrow(8.9,7.45,2.2,7.0); arrow(8.9,7.45,6.0,7.0); arrow(8.9,7.45,9.85,7.0)
box(0.3,2.55,11.4,1.9,'8  Outputs in aged mice (PSLN-344 vs PSLN-212)',
    'Serum IgG 18.6x (CA09) / 13.4x (Aichi); HAI 8.0x / 9.2x; neutralising Ab 9.2x; IgG2a:IgG1 1.85 vs 0.55 = Th1 skew (S03, S13; T4)\n'
    'Survival after lethal challenge, pooled de-duplicated: 84% (61/73) vs 12% (9/73); RD 71 pts (95% CI 60-82) (T3 set B)\n'
    'Heterosubtypic (H3 vaccine->H1 challenge; H1->H3; H1+H3->H5), early (challenge d2-3) and durable (d60: 57-71% vs 0-14%) (S06; T1/T2)\n'
    'Requires antigen: vaccine + PSLN-344 6/7 vs PSLN-344 alone 0/7 vs vaccine alone 0/7 (S15-H) -> adjuvant, not a stand-alone innate prophylactic\n'
    'Age-gap closure: restores ~80% of the young-vs-aged survival gap (index 0.80, 95% CI 0.69-0.91; T11)',C5)
arrow(2.15,4.9,2.15,4.45); arrow(6.0,4.9,6.0,4.45); arrow(9.85,4.9,9.85,4.45)
ax.text(0.3,2.35,'Numbers are group means (aged PSLN-344 vs aged PSLN-212 unless stated), per-animal source cells listed in the analysis workbook.\n'
        'Perturbation evidence (CBX, INCB3344, Ifnar-/-, GM-CSF, PTX) comes from single experiments with n=3-5 and needs independent confirmation.',fontsize=7.6,style='italic',va='top')
ax.text(0.3,13.75,'Figure 4. Mechanism of action of PSLN-344 in the aged lung, reconstructed from the programme dataset',fontsize=10.5,weight='bold',va='top')
plt.savefig('/tmp/outputs/figures/Fig4_MoA_schematic.png',dpi=190,bbox_inches='tight'); print('ok')
