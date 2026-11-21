import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, textwrap
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({'font.family': 'DejaVu Sans'})
fig, ax = plt.subplots(figsize=(17, 9.6)); ax.set_xlim(0, 170); ax.set_ylim(0, 96); ax.axis('off')
W, H = 39, 25
def box(x, y, title, lines, color, w=W, h=H, wrap=46):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.5', fc=color, ec='#333', lw=0.9))
    ax.text(x + 1, y + h - 1.2, title, fontsize=10, weight='bold', va='top')
    body = '\n'.join(textwrap.fill(l, wrap, subsequent_indent='   ') for l in lines)
    ax.text(x + 1, y + h - 5.2, body, fontsize=8.1, va='top', linespacing=1.3)
def arrow(x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='-|>', lw=1.4, color='#333', mutation_scale=14))
L1, L2, L3, L4, L5 = '#FDEDEC', '#EBF5FB', '#E9F7EF', '#FEF9E7', '#F5B7B1'
xs = [1, 44, 87, 130]; ys = [64, 34, 3]
box(xs[0], ys[0], '1. Delivery (biomimetic liposome)', [
    '- Alveolar-macrophage uptake 43% -> 13% in SP-A/D knockout (-71%) (S01-C) [LoF]',
    '- AECII uptake 15.8% vs 0.4% for free dye (S01-B)',
    '- Mn-PSLN lower epithelial uptake (S08-C) [low confidence: overlaps S01-B]',
    '- CDN-1807 > cGAMP: Ifnb1 16.5x vs 7.7x (S01-A)'], L1)
box(xs[1], ys[0], '2. Mn2+-potentiated STING signalling', [
    '- Ifnb1 16 h: 36.9x vs 16.5x (GMR 2.2; restoration index 0.98) (S01-A)',
    '- Emax 49x vs 14x; ~3x dose-sparing (S08-A)',
    '- Ccl2 77x, Ccl3 27x, Il6 6.5x higher than PSLN-212 (S09-A)',
    '- Gm-csf 8.5x vs 1.6x at 36 h (S02-F)',
    '- STING-dependence itself NOT yet tested'], L2)
box(xs[2], ys[0], '3. Paracrine spread (gap junctions)', [
    '- Carbenoxolone cuts recruited monocytes 7.3% -> 3.1% (-58%) (S11-C) [LoF]',
    '- Consistent with CDN transfer to bystander cells; CBX has off-target effects'], L2)
box(xs[3], ys[0], '4. CCR2-dependent monocyte influx', [
    '- Lung monocytes d4: 30.6% vs 16.7% (S01-D; RI 0.89)',
    '- CCR2 antagonist: monocytes -67%, Ly6C+ MPhi -84% (S07-B); lung GZMB+ CD8 -79% (S02-I) [LoF]',
    '- PSLN-212 instead accumulates Ly6C+CCR2+ macrophages (18.5 vs 3.4 x1e5 at d5, S07-A)'], L3)
box(xs[3], ys[1], '5. moDC via IFNAR + GM-CSF', [
    '- IFNAR-/- marrow: moDC 19.7% -> 2.1% (-89%) (S02-H) [LoF]',
    '- GM-CSF rescues IFNAR-/- marrow to 12.4% (S02-H) [GoF]',
    '- PSLN-212 + rGM-CSF: 5.9% -> 13.8% (S02-G) [GoF] => GM-CSF is the aged-lung deficit; Mn2+ supplies it',
    '- M2-like CD206+ macrophages 71% -> 49% (S11-E)'], L3)
box(xs[2], ys[1], '6. DC activation, migration, priming', [
    '- CCR7+ migratory DC 30.7% vs 7.3% (S02-A); cDC1 37.5% vs 22.8% (S01-F)',
    '- Pertussis toxin blocks antigen+ DC in MLN (-67%, S02-C) and MLN OT-I priming (-78 to -86%, S02-E, S05-C) [LoF]',
    '- Lung priming PTX-insensitive (-7%, S05-C)',
    '- CD40/CD86 only partly restored (RI 0.17-0.22)'], L3)
box(xs[1], ys[1], '7. Tfh / germinal centre', [
    '- ICOS-hi Tfh 10.3% vs 3.8% (S04-A)',
    '- Tfr 10.8% vs 26.7% (S04-B); lung Treg 3.0% vs 6.7% (S04-D)',
    '- GC B cells 6.5% vs 2.3% (S03-K)',
    '- Aicda 3.5x, E47 3.9x vs PSLN-212 (S03-L)'], L4)
box(xs[0], ys[1], '8. Antibody (Th1-skewed)', [
    '- HAI GMT d14: 368 vs 46 (H1), 320 vs 35 (H3); neut 3840 vs 418 (S03-C/D/G/H)',
    '- IgG2a/IgG1 2.1 vs 0.58, recomputed from S13-A/B (S03-B printed labels rotated)',
    '- Post-boost IgG gap only partly closed (RI 0.57-0.66, S13-I/J)'], L4)
box(xs[0], ys[2], '9. CD8 effector and resident memory', [
    '- Ki-67+ CD8 d3 9.4% vs 3.5% (S05-D)',
    '- IFNg+ CD8 d14 6.4% vs 1.5% (S05-F); d60 9.9% vs 3.0% (S05-G)',
    '- Lung TRM d25 4.0% vs 1.0% (S05-I; RI 0.59)',
    '- Cross-reactive with H1, H3 and H5 antigens (S05-F, S14-A)'], L4)
box(xs[1], ys[2], '10. Protection in aged mice', [
    '- Pooled survival 85/101 (84%) vs 13/101 (13%); difference 71 pp (95% CI 60-79); point estimate favours PSLN-344 in 14/14 strata',
    '- Homologous, heterosubtypic (H1<->H3, H5N1), rapid (day 2-3) and 60-day durability',
    '- Needs antigen at day 3 (S15-H) [integrity caveat]'], L5)
box(xs[2], ys[2], 'Not yet shown -> next-step studies', [
    '- STING/cGAS dependence (knockout or H-151)', '- Mn-only liposome (synergy vs additive)',
    '- Antibody vs CD8 contribution (transfer / depletion)', '- Mucosal IgA; lung viral load',
    '- Human STING haplotype activity', '- Mn dose, biodistribution, CNS'], '#F2F3F4', w=82, wrap=95)
for (x1, y1, x2, y2) in [(40.5, 76, 43.5, 76), (83.5, 76, 86.5, 76), (126.5, 76, 129.5, 76), (149.5, 63.5, 149.5, 59.5),
                         (129.5, 46, 126.5, 46), (86.5, 46, 83.5, 46), (43.5, 46, 40.5, 46), (20, 33.5, 20, 28.5), (106, 33.5, 70, 28.5), (40.5, 15, 43.5, 15)]:
    arrow(x1, y1, x2, y2)
ax.text(1, 94.5, 'Figure 5. Mechanism of action supported by our data (aged mice; PSLN-344 vs PSLN-212 unless stated)', fontsize=12, weight='bold')
ax.text(1, 92, '[LoF] loss-of-function and [GoF] gain-of-function evidence establishes causality for that link; other links are correlative. RI = restoration index (fraction of young-aged gap closed).', fontsize=8.5)
plt.savefig('/tmp/outputs/figures/fig5_moa.png', dpi=170, bbox_inches='tight'); print('ok')
