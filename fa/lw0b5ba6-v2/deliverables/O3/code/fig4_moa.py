import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig,ax=plt.subplots(figsize=(16,19)); ax.set_xlim(0,100); ax.set_ylim(8,124); ax.axis('off')
def box(x,y,w,h,title,body,fc,ec='k'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.4,rounding_size=1.2',fc=fc,ec=ec,lw=1.2))
    ax.text(x+1,y+h-1.2,title,fontsize=11.5,fontweight='bold',va='top')
    ax.text(x+1,y+h-4.6,body,fontsize=9.0,va='top',family='DejaVu Sans')
def arrow(x1,y1,x2,y2,txt=''):
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='-|>',lw=1.8,color='#444'))
    if txt: ax.text((x1+x2)/2+0.8,(y1+y2)/2,txt,fontsize=8.5,color='#444',style='italic')
ax.text(50,123,'PSLN-344 mechanism of action in the aged lung, as supported by our data (aged BALB/c unless noted; values = aged PSLN-344 vs aged PSLN-212 [young PSLN-212])',ha='center',fontsize=12,fontweight='bold')
box(2,106,45,14,'1. Delivery: surfactant-mimetic liposome',
 "- AECII take up liposome cargo: 15.8% SRB+ vs 0.4% free dye (S01-B)\n- Alveolar macrophage uptake is SP-A/D-dependent:\n  43.1% WT vs 12.7% Sftpa1/Sftpd KO (S01-C)\n- Encapsulation of CDN-1807: 54.8% (344) vs 59.6% (212), p=0.29 (S08-B)",'#f2f0f7')
box(52,106,46,14,'2. Mn2+ amplifies STING output (ceiling, not potency)',
 "- Lung Ifnb1 16h: 36.9x vs 16.5x [young 37.5x] (S01-A): 100% restored\n- Dose-response Emax 49x vs 14x; ED50 ~11.5 vs ~9.5 ug (S08-A)\n- Gap-junction blocker CBX cuts recruited monocytes 7.3->3.1%\n  (S11-C): signal propagates cell-to-cell (e.g. cGAMP transfer)",'#e7e1ef')
arrow(47,113,52,113)
box(52,84,46,19,'3. Restored chemokine / growth-factor programme (16-36 h)',
 "- Ccl2 590x vs 7.6x [young 1,390x]; Ccl3 30x vs 1.1x [57x];\n  Ccl5 20x vs 2.6x [62x]; Il6 36x vs 5.6x [60x] (S09-A, n=3)\n- Gm-csf 8.5x vs 1.6x at 36 h (S02-F)\n- Residual: Tnf 41x [young 14x], Il10 7x [young 2x]; aged lungs\n  still elevated at 72 h (S09-A 2nd block = 72 h) -> monitor\n- R848 arms instead give TNF/IL-10-dominant profile (Tnf/Ifnb1\n  8-30 vs 1.1) and weight loss (S09-A, S08-D)",'#efe6f3')
arrow(75,106,75,103)
box(2,80,45,23,'4. CCR2+ monocytes -> moDC fate (IFNAR, GM-CSF)',
 "- Lung monocytes d4: 30.6% vs 16.7% [32.2%] (S01-D)\n- CCR2 antagonist INCB3344 (PSLN-344): monocytes -67%,\n  Ly6C+ macrophages -84% (S07-B); GZMB+ CD8 -79% (S02-I, young)\n- IFNAR-KO marrow: moDC 19.7->2.1% (-89%); GM-CSF rescues to\n  12.4% (S02-H)\n- GM-CSF added to PSLN-212: moDC-like 5.9->13.8% (S02-G)\n- Without Mn (PSLN-212), Ly6C+CCR2+ macrophages accumulate:\n  19.0 vs 3.4 x1e5 at d5 (S07-A, n=3, age not stated); CD206+\n  macrophages 71.5% vs 48.9% [35.5%] (S11-E)",'#ede3f2')
arrow(52,92,47,92)
box(2,55,45,21,'5. DC migration & antigen delivery to the MLN (Gi / CCR7)',
 "- CCR7+ migratory CD11b+ DC 72 h: 30.7% vs 7.3% [35.0%] (S02-A)\n- Lung cDC1 72 h: 37.5% vs 22.8% [43.4%] (S01-F)\n- Antigen+ (OVA-AF647) MLN DC 36 h: 7.1% vs 1.8% [9.4%] (S02-C);\n  pertussis toxin blocks (2.4%)\n- Sorted MLN DC prime OT-I: 18.7% vs 0.8% [26.2%] (S02-E)\n- In vivo OT-I priming in MLN PTX-sensitive (30.9->6.8%) but not\n  in lung (59->55%) (S05-C)\n- GAP: DC CD40+/CD86+ only 21-24% restored (S02-D)",'#f6dcea')
arrow(24.5,80,24.5,76)
box(52,55,46,25,'6. Adaptive immunity restored toward young levels',
 "Tfh/GC (d5-7): Tfh ICOS-hi 10.3% vs 3.8% [13.6%] (S04-A);\n  Tfr 10.8% vs 26.7% [7.1%] (S04-B); GC B 6.5% vs 2.3% [9.8%]\n  (S03-K); Aicda 3.5x, E47 3.9x (S03-L); lung Treg 3.0 vs 6.7% (S04-D)\nAntibody (d14): IgG GMT 18.6x; HAI GMT 368 vs 46 [485] (CA09);\n  neutralising 9.2x (S03-A/C/D/E/G/H); IgG2a/IgG1 2.1 vs 0.58\n  [3.0] = Th1 shift (S13-A/B; S03-B labels rotated)\nCD8 (d3-60): Ki-67+ 9.4 vs 3.5% (S05-D); IFNg+ vs H5 6.4 vs 1.5%\n  d14, 9.9 vs 3.0% d60 (S05-F/G); lung TRM 4.0 vs 1.0% [6.0%] (S05-I)\n  GAP: TRM, IFNg CD8, GZMB CD8 55-71% of young",'#fbd0e2')
arrow(47,66,52,66)
box(20,31,60,20,'7. Protection in aged mice (antigen-specific, heterosubtypic, durable, rapid)',
 "- Pooled over 6 S06 challenge studies: mortality 10/42 (24%) vs 38/42 (90%); MH RR 0.26 (0.15-0.45);\n  most conservative 5-study set 29% vs 94%, RR 0.30 (0.18-0.51) (S06-A,B,C,E,F,G)\n- Heterosubtypic (H3N2 vaccine -> H1N1; bivalent -> H5N1; H1N1 -> H3N2), durable to d60, and\n  protective when challenged 3 d after dosing (S06-B: 2/7 vs 7/7 deaths)\n- Antigen-specific: PSLN-344 without vaccine 7/7 deaths vs with vaccine 1/7 (S15-H)\n- Works in 14-month mice with or without prior PR8 imprinting (S06 rows 71-105)\n- Young mice: PSLN-212 and PSLN-344 both 0 deaths (S09-B/D/F) -> Mn adds value only where immunity is aged",'#fde0dd')
arrow(75,55,60,51); arrow(24.5,55,40,51)
box(2,10,96,17,'Where the mechanism is still unproven (drives next studies)',
 "- Mn2+ contribution not isolated: no Mn-only, Mn-liposome-without-CDN, or free-Mn controls; Mn biodistribution/olfactory transport never measured.\n"
 "- Direct STING dependence not shown (no Sting1-/- / Tmem173 gt mice, no cGAS/STING inhibitor); IFNAR evidence is from bone-marrow chimeras only (S02-H, S12-A n=3 not significant).\n"
 "- Epithelial uptake of PSLN-344 itself is uncertain: S08-C (PSLN-SRB vs PSLN-344-SRB) contradicts S01-B and appears mislabelled.\n"
 "- Correlate of protection not established: immunogenicity and survival were measured in different animals; HAI>=40 did not protect (aged PSLN-212:\n  5/5 mice >=40, 0/7 survived, S03-C/S03-I) whereas all protected groups had HAI GMT >=368.\n"
 "- Mucosal IgA, nasal-associated lymphoid tissue and upper-airway immunity were not measured - central for an intranasal product.\n"
 "- Only female mice were used (annotation: 'Female BALB/c').",'#fff7bc')
plt.savefig('/tmp/outputs/figures/Fig3_mechanism_of_action.png',dpi=140,bbox_inches='tight'); print('ok')
