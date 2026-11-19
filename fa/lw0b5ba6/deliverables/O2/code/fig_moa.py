import matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig,ax=plt.subplots(figsize=(17.5,11)); ax.set_xlim(0,100); ax.set_ylim(0,100); ax.axis('off')
# evidence grade colours
C={'causal':'#d9f2d9','assoc':'#e8eef9','weak':'#fff2cc','gap':'#f8d7da'}
def box(x,y,w,h,title,lines,grade):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.4',fc=C[grade],ec='#333333',lw=0.9))
    ax.text(x+w/2,y+h-1.6,title,ha='center',va='top',fontsize=8.4,fontweight='bold')
    ax.text(x+0.8,y+h-5.0,'\n'.join(lines),ha='left',va='top',fontsize=7.0,linespacing=1.4)
def arr(x1,y1,x2,y2):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=12,lw=1.1,color='#444444'))
ax.text(50,99,'Fig. 6  Mechanism of action of PSLN-344 in the aged lung, as supported by our data (aged vs aged PSLN-212 unless stated)',ha='center',va='top',fontsize=10.5,fontweight='bold')
# Row 1
box(1,73,23,21,'1  Delivery / targeting',['Liposome → AECII 15.8% vs AECI 3.8%','  (free dye 0.4%) [S01-B]','Alveolar macrophage uptake 43% → 13% in','  SP-A/SP-D KO (−71%) [S01-C]','CAVEAT: S08-C (PSLN vs PSLN-344) has a','  probable label swap → Mn effect on uptake unknown'],'causal')
box(26,73,23,21,'2  STING activation, amplified by Mn²⁺',['Ifnb1 16h: 36.9× vs 16.5× (×2.2, p<1e-4);','  = young benchmark 37.5× (RI 0.98) [S01-A]','Dose-dependent; 20 µg: ×3.6 vs PSLN-212 [S08-A]','Converges by 72h (4.2× vs 3.4×, NS)','GAP: no STING-KO and no Mn-only (no-CDN)','  arm → STING-dependence and CDN-1807','  contribution unproven'],'gap')
box(51,73,23,21,'3  Paracrine spread & chemokines',['Gap-junction block (CBX): recruited monocytes','  7.3% → 3.1% (−58%, p=0.003) [S11-C]','Ccl2 16h 590× vs 7.6× (×77) [S09-A]','Ccl3 ×27, Ccl5 ×7.6, Il6 ×6.5 [S09-A]','Gm-csf 36h 8.5× vs 1.6× (×5.4, p<1e-4) [S02-F]','CAVEAT: CBX has off-target effects'],'causal')
box(76,73,23,21,'4  CCR2⁺ monocyte recruitment',['Lung monocytes d4: 30.6% vs 16.7%','  (young 32.2%; RI 0.89) [S01-D]','CCR2 antagonist: monocytes 9.9% → 3.3%,','  Ly6C⁺ Mφ 15.4% → 2.5% [S07-B]','IFNAR⁻/⁻ BM: infiltration 21.3 → 15.4%','  (n=3, p=0.10; not IFN-dependent) [S12-A]'],'causal')
# Row 2
box(76,46,23,23,'5  Monocyte → moDC (not Mφ)',['moDC need IFNAR: WT 19.7% vs IFNAR⁻/⁻','  2.1% (−89%); GM-CSF rescues 12.4% [S02-H]','GM-CSF + PSLN-212: moDC 13.8% vs 5.9% [S02-G]','Ly6C⁺CCR2⁺ Mφ d5: 3.4 vs 19.0 ×10⁵','  (−82%) [S07-A]','CD206⁺ Mφ 48.9% vs 71.5% (young 35.5%) [S11-E]','GAP: no GM-CSF blockade of PSLN-344 itself'],'causal')
box(51,46,23,23,'6  DC migration & antigen transport',['CCR7⁺ migratory DC 30.7% vs 7.3% [S02-A]','MLN CD11b⁺ DC 36.8% vs 18.2% [S02-B]','Ag⁺ MLN DC 7.1% vs 1.8%; PTX → 2.4% [S02-C]','cDC1 37.5% vs 22.8% [S01-F]','CD40⁺/CD86⁺ 11.2/14.5% vs young 38.7/37.9%','  (RI 0.17–0.22: residual aged defect) [S02-D]'],'causal')
box(26,46,23,23,'7  Less regulation, more help',['Tfr d7 10.8% vs 26.7% [S04-B]','Lung Treg d7 3.0% vs 6.7% [S04-D]','ICOS-hi Tfh d7 10.3% vs 3.8% [S04-A]','Tfr d30 14.0 vs 18.0% (NS) [S04-C]','CAVEAT: Tfh:Tfr ratio is derived from Tfr','  (=(100−Tfr)/Tfr), not independent; S07-C','  macrophage→Treg transfer has duplicate labels'],'assoc')
box(1,46,23,23,'8  Germinal centre output',['GC B d7 6.5% vs 2.3% [S03-K]','Aicda ×3.5, E47 ×3.9 (n=3) [S03-L]','IgG⁺ of B220⁺ 25.9% vs 11.2% [S13-H]','IgG d14 ×18.6; HAI ×8.0 (CA09), ×9.2 (Aichi);','  neutralisation ×9.2 [S03-A–H]','HAI aged PSLN-344 ≈ young (0.76×, NS)','IgG2a:IgG1: direction unresolved (label rotation)'],'assoc')
# Row 3
box(1,17,23,24,'9  CD8 T cells incl. cross-reactive',['Ki-67⁺ CD8 d3 9.4% vs 3.5% [S05-D]','IFN-γ⁺ CD8 (H5 restim) d14 6.4 vs 1.5%;','  d60 9.9 vs 3.0% [S05-F/G]','H1/H3 restim 11.0/9.9 vs 3.1/3.6% [S14-A]','Lung TRM d25 4.0% vs 1.0% [S05-I]','CCR2 block: GZMB⁺ CD8 6.8→1.4% (young) [S02-I]','CAVEAT: NP366 tetramer (H-2Dᵇ) used in','  BALB/c (H-2ᵈ) [S05-A/B]'],'assoc')
box(26,17,23,24,'10  Protection (requires antigen)',['Aged pooled: 61/73 (84%) vs 9/73 (12%)','  Tier B 28/35 vs 4/35; Tier C 5/7 vs 0/7','Day-60: 14/21 vs 1/21 (background 17/21 alive)','3-day: vaccine+344 6/7; vaccine 0/7;','  PSLN-344 alone 0/7 [S15-H]','3 strains (BALB/c, C57BL/6, Swiss Webster)','CAVEAT: survival/weight conflicts (Fig. 5)'],'assoc')
box(51,17,48,24,'Key gaps before the MoA can be claimed externally',['• STING-dependence (Sting1-deficient mice) — not tested','• Contribution of CDN-1807 vs Mn²⁺ alone (Mn-liposome without CDN) — not tested; Sham vehicle lacks Mn²⁺','• Necessity of GM-CSF / CCR2 / IFNAR for PROTECTION (only intermediate cell readouts tested)','• AECII-intrinsic STING (conditional KO) and connexin-specific transfer (CBX is non-specific)','• Mucosal IgA and lung viral load — never measured; no individual-animal linkage of early PD to outcome','• Human route: MoA requires alveolar deposition → inhaled (not nasal-spray) product'],'gap')
for (x1,y1,x2,y2) in [(24.5,83.5,25.5,83.5),(49.5,83.5,50.5,83.5),(74.5,83.5,75.5,83.5),(87.5,72.5,87.5,69.6),(75.5,57.5,74.5,57.5),(50.5,57.5,49.5,57.5),(25.5,57.5,24.5,57.5),(12.5,45.5,12.5,41.6),(24.5,29,25.5,29)]:
    arr(x1,y1,x2,y2)
# legend
for i,(k,lab) in enumerate([('causal','perturbation-supported (KO, blocker, rescue)'),('assoc','associative (group differences)'),('gap','critical gap / unproven')]):
    ax.add_patch(FancyBboxPatch((2+i*31,3),2.5,2.5,boxstyle='round,pad=0.2',fc=C[k],ec='#333333',lw=0.7)); ax.text(5.5+i*31,4.2,lab,fontsize=7.5,va='center')
ax.text(2,9.5,'RI = restoration index (share of aged-vs-young gap closed). Fold-changes are geometric means vs untreated. All comparisons n=3–5/group, Welch t-test on log scale for titres/fold-changes.',fontsize=6.8)
plt.savefig('/tmp/outputs/figures/fig6_MoA_schematic.png',dpi=170,bbox_inches='tight'); print('ok')
