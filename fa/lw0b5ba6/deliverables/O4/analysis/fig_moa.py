import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({'font.family': 'DejaVu Sans'})
GR = {'strong': '#1f5fa8', 'moderate': '#5b9bd5', 'weak': '#f0ad4e', 'unreliable': '#c0392b', 'gap': '#ffffff'}
fig, ax = plt.subplots(figsize=(12.5, 9.6)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
def box(x, y, w, h, title, body, grade, ls='-'):
    fc = GR[grade]; tc = 'white' if grade in ('strong', 'moderate', 'unreliable') else 'black'
    p = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.4,rounding_size=1.2', fc=fc, ec='k', lw=0.8, ls=ls, alpha=0.95)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h - 1.6, title, ha='center', va='top', fontsize=8.2, weight='bold', color=tc)
    ax.text(x + w / 2, y + h - 4.6, body, ha='center', va='top', fontsize=6.6, color=tc, linespacing=1.25)
def arrow(x1, y1, x2, y2, ls='-'):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', mutation_scale=11, lw=1.1, color='k', ls=ls))
# Row 1: delivery
box(2, 86, 30, 11, '1. Intranasal PSLN-344', 'CDN-1807 (STING agonist) + Mn2+ in\nsurfactant-mimetic liposome (DPPC/DPPG/PEG/chol)\nEE 54.8 +/- 5.1% -> ~45% CDN free [S08-B]', 'moderate')
box(36, 86, 30, 11, '2a. Alveolar macrophage uptake', 'SP-A/SP-D-dependent: DiD+ AM 43.1% WT vs\n12.7% Sftpa1/Sftpd KO (p<0.001) [S01-C]', 'moderate')
box(70, 86, 28, 11, '2b. AEC-II uptake / Mn effect', 'Liposome vs free dye 15.8 vs 0.4% [S01-B];\nMn lowers AEC uptake ~4x [S08-C]\nUNRELIABLE: shared values (C5)', 'unreliable')
# Row 2: STING/IFN
box(2, 68, 30, 13, '3. STING -> IFN-b burst (Mn raises ceiling)', 'Ifnb1 16 h: 37.1x vs 16.6x (2.2-fold, p<0.001)\n= young level 37.6x (RI 0.98) [S01-A]\nEmax 49x vs 14x; ED50 ~10 ug both [S08-A]\nTransient: 72 h 4.4x vs 3.4x (NS)', 'strong')
box(36, 68, 30, 13, '4. Gap-junction propagation', 'Carbenoxolone pre-treatment halves monocyte\nrecruitment: 3.1 vs 7.3% (p=0.004) [S11-C]\n(single block; CBX is non-selective)', 'moderate')
box(70, 68, 28, 13, '5. Chemokines + GM-CSF', 'Csf2 16 h 4.2x, 36 h 5.4x vs PSLN-212 [S02-F]\nCcl2 77x, Ccl3 27x, Ccl5 7.6x (16 h, n=3)\n[S09-A; PBS/Sham label conflict M2]', 'strong')
# Row 3: myeloid
box(2, 49, 30, 14, '6. CCR2-dependent monocyte influx', 'Lung monocytes d4: 30.6 vs 16.7% (p=0.002) [S01-D]\nCCR2 antagonist: 9.9 -> 3.3% monocytes,\n15.4 -> 2.5% Ly6C+ Mphi [S07-B]\nIFNAR-/- BM: 15.4 vs 21.3% (n=3, p=0.12) [S12-A]', 'strong')
box(36, 49, 30, 14, '7. IFNAR + GM-CSF drive moDC', 'IFNAR-/- BM moDC 2.1 vs 19.7% WT; GM-CSF\nrescues to 12.4% [S02-H]\nGM-CSF + PSLN-212: 13.8 vs 5.9% [S02-G]\n-> Mn-driven Csf2 is the proposed missing link', 'strong')
box(70, 49, 28, 14, '8. Less suppressive milieu', 'CD206+ Mphi 48.9 vs 71.5% [S11-E, no timepoint]\nLung Treg 3.0 vs 6.7% (n=3) [S04-D]\nPSLN-212 accumulates Ly6C+CCR2+ Mphi\n19.0 vs 3.4 x1e5 at d5 [S07-A]; S07-C unusable', 'weak')
# Row 4: DC
box(2, 30, 45, 14, '9. DC mobilisation and priming', 'cDC1 37.5 vs 22.8% [S01-F]; CCR7+ migratory CD11b+ DC 30.7 vs 7.3% [S02-A]\nAntigen+ MLN DC 7.1 vs 1.8%; pertussis toxin 2.4% [S02-C]\nCD40/CD86 only 17-22% of age gap closed (11.2 vs young 38.7% CD40) [S02-D]\nOT-I priming 18.7 vs 0.8% [S02-E: MHC/strain question, M4]', 'moderate')
box(52, 30, 46, 14, '10. Tfh up / Tfr down -> germinal centre', 'ICOS-hi Tfh 10.3 vs 3.8% [S04-A]; Tfr 10.8 vs 26.7% [S04-B]\nGC B 6.5 vs 2.3% [S03-K]; Aicda 3.5x, E47 3.9x (n=3) [S03-L]\nTfr difference not sustained at d30 (14.0 vs 18.0%, NS) [S04-C]', 'strong')
# Row 5: effector
box(2, 11, 45, 14, '11a. CD8 / TRM (heterosubtypic arm)', 'Ki-67+ CD8 9.4 vs 3.5%, GZMB+ 5.7 vs 3.0% (d3) [S05-D/E]\nH5N1-reactive IFN-g+ CD8 6.4 vs 1.5% (d14), 9.9 vs 3.0% (d60) [S05-F/G]\nLung TRM 4.0 vs 1.0% (d25) [S05-I]; GZMB+ CD8 CCR2-dependent [S02-I]\nLung priming pertussis-toxin-insensitive (59 vs 55%) [S05-C]', 'strong')
box(52, 11, 46, 14, '11b. Antibody (homologous arm)', 'IgG 18.6x (H1N1), 13.4x (H3N2) vs PSLN-212 [S03-A/E]\nHAI GMT 368 vs 46 (H1N1), 320 vs 35 (H3N2) [S03-C/G]\nNeutralising 9.2x [S03-D/H]; boost d28 3.6-11.5x [S13-I/J]\nIgG2a/IgG1 0.55 -> 1.85 only under S13 labels (M1)', 'strong')
box(22, 0.5, 56, 7.5, '12. Protection in aged mice (magnitude NOT verified)', 'Pooled survival 85/101 vs 13/101 (S06-D removed); 65-71 pt advantage in every sensitivity scenario [S03/S06/S15]\nbut critical integrity findings C1-C2, M3 and 19% sentinel mortality (M5) - replication required', 'weak')
for (x1, y1, x2, y2) in [(17, 86, 17, 81.5), (32.5, 91.5, 35.5, 91.5), (51, 86, 40, 81.5), (32.5, 74.5, 35.5, 74.5), (66.5, 74.5, 69.5, 74.5),
                         (84, 68, 84, 63.5), (70, 70, 32.5, 60), (17, 68, 17, 63.5), (32.5, 56, 35.5, 56), (51, 49, 30, 44.5), (17, 49, 17, 44.5),
                         (47.5, 37, 51.5, 37), (24, 30, 24, 25.5), (75, 30, 75, 25.5), (24, 11, 40, 8.3), (75, 11, 60, 8.3), (84, 49, 84, 44.5)]:
    arrow(x1, y1, x2, y2)
# legend
lx = 2; ly = -4.5
for i, (k, lab) in enumerate([('strong', 'strong: >=1 clean block, large effect'), ('moderate', 'moderate: single block / caveat'), ('weak', 'weak or indirect'), ('unreliable', 'unreliable (integrity finding)')]):
    ax.add_patch(FancyBboxPatch((lx + i * 25, ly), 2.5, 2.2, boxstyle='round,pad=0.2', fc=GR[k], ec='k', lw=0.5, clip_on=False))
    ax.text(lx + i * 25 + 3.5, ly + 1.1, lab, fontsize=7, va='center')
ax.text(50, -8.6, 'Not yet tested (required to complete the MoA): STING/cGAS-knockout or STING-inhibitor control; CDN-free Mn-liposome arm; IFN-b protein; mucosal IgA;\nCD8 / B-cell / CCR2 depletion linked to survival; Mn biodistribution. Numbers are PSLN-344 vs PSLN-212 in aged mice unless stated; cell refs in evidence ledger.',
        ha='center', fontsize=7, style='italic')
ax.set_title('Figure 7. Proposed mechanism of action of PSLN-344 in the aged lung, built only from our data (evidence grade shown by colour)', fontsize=10)
fig.savefig('/tmp/outputs/figures/fig7_moa.png', dpi=200, bbox_inches='tight'); plt.close(fig)
print('ok')
