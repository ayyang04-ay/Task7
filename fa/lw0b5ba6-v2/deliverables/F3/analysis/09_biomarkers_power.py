"""09_biomarkers_power.py
(a) Biomarker ranking.  For every readout measured in the four standard arms we ask two questions:
      1. Does it separate regimens that protect aged/young animals (PSLN-344 aged, PSLN-212 young) from regimens
         that do not (Sham aged, PSLN-212 aged)?  -> AUC (probability a protected-regimen animal ranks above a
         non-protected-regimen animal) and whether the two value ranges overlap.
      2. How much of the age-related deficit does Mn2+ recover?
         restoration = (PSLN-344 aged - PSLN-212 aged) / (PSLN-212 young - PSLN-212 aged), on the analysis scale.
    This is a GROUP-LEVEL association: the animals that gave biomarker samples are not the animals that were challenged.
(b) Sample sizes for the proposed confirmatory studies, using effect sizes and variances observed in the workbook.
"""
import json, math, itertools
import numpy as np
from scipy import stats
B = json.load(open('/tmp/work/parsed/parsed_blocks.json'))
G = lambda bid: B[bid]['groups']
OUT = {'biomarkers': [], 'power': {}}

def auc(pos, neg):
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    return float(np.mean([(p > n) + 0.5 * (p == n) for p in pos for n in neg]))

ROWS = [  # block, label, scale, direction(+1 higher=protective), timepoint, tier, translatable human analogue
 ('S01-A_16h', 'Ifnb1 mRNA, lung', 'log', +1, '16 h', 'innate (proximal PD)', 'blood/nasal ISG score, IFN-b/CXCL10 protein'),
 ('S02-A', 'CCR7+ of lung CD11b+ DC', 'lin', +1, '72 h', 'APC', 'CCR7/CD86 on blood or nasal-curettage moDC'),
 ('S02-B', 'CD11b+ DC in MLN', 'lin', +1, '72 h', 'APC', '(no direct human analogue; FNA of draining node)'),
 ('S02-D_CD40', 'CD40+ of MLN CD11b+ DC', 'lin', +1, 'd3', 'APC', 'CD40 on blood monocytes/moDC'),
 ('S02-D_CD86', 'CD86+ of MLN CD11b+ DC', 'lin', +1, 'd3', 'APC', 'CD86 on blood monocytes/moDC'),
 ('S01-F', 'cDC1 share of lung cDC', 'lin', +1, '72 h', 'APC', '-'),
 ('S04-A_ICOShi', 'ICOS-hi Tfh in MLN', 'lin', +1, 'd7', 'T-cell help', 'circulating ICOS+PD-1+CXCR5+ cTfh, d7'),
 ('S04-B_Foxp3', 'Tfr (Foxp3+ of CXCR5+ICOShi)', 'lin', -1, 'd7', 'T-cell help', 'circulating Tfr / cTfh:cTfr ratio'),
 ('S04-D', 'lung Treg', 'lin', -1, 'd7', 'T-cell help', '-'),
 ('S03-K', 'GC B cells in MLN', 'lin', +1, 'd7', 'B cell', 'd7 plasmablasts; FNA GC B cells'),
 ('S13-H', 'IgG+ of MLN B220+', 'lin', +1, 'n.s.', 'B cell', 'antigen-specific memory B cells'),
 ('S03-A', 'serum IgG anti-H1N1', 'log', +1, 'd14', 'antibody', 'serum IgG ELISA'),
 ('S03-E', 'serum IgG anti-H3N2', 'log', +1, 'd14', 'antibody', 'serum IgG ELISA'),
 ('S03-C', 'HAI H1N1', 'log', +1, 'd14', 'antibody', 'HAI (accepted immunogenicity endpoint)'),
 ('S03-G', 'HAI H3N2', 'log', +1, 'd14', 'antibody', 'HAI'),
 ('S03-D', 'neutralising titre H1N1', 'log', +1, 'd14', 'antibody', 'microneutralisation'),
 ('S03-H', 'neutralising titre H3N2', 'log', +1, 'd14', 'antibody', 'microneutralisation'),
 ('S05-D', 'Ki-67+ lung CD8', 'lin', +1, 'd3', 'CD8 T cell', 'Ki-67+CD38+ CD8 in blood d7'),
 ('S05-E', 'GZMB+ lung CD8', 'lin', +1, 'd3', 'CD8 T cell', 'GZMB+ CD8 in blood'),
 ('S05-F', 'IFN-g+ CD8 (H5N1 cross-reactive), MLN', 'lin', +1, 'd14', 'CD8 T cell', 'IFN-g ELISpot/ICS to conserved or heterosubtypic antigen'),
 ('S05-G', 'IFN-g+ CD8 (H5N1 cross-reactive), MLN', 'lin', +1, 'd60', 'CD8 T cell', 'as above, durability'),
 ('S05-I', 'lung CD8 TRM', 'lin', +1, 'd25', 'CD8 T cell', '(BAL/nasal TRM; research only)'),
 ('S14-A_H1N1', 'IFN-g+ CD8 (H1N1), MLN', 'lin', +1, 'n.s.', 'CD8 T cell', 'IFN-g ELISpot/ICS'),
 ('S14-A_H3N2', 'IFN-g+ CD8 (H3N2), MLN', 'lin', +1, 'n.s.', 'CD8 T cell', 'IFN-g ELISpot/ICS'),
 ('S11-E', 'CD206+ lung macrophages', 'lin', -1, 'n.s.', 'myeloid', '-'),
]
def tr(v, scale, hai=False):
    v = np.asarray([5 if (x == 0 and hai) else x for x in v], float)
    return np.log2(v) if scale == 'log' else v
print(f"{'block':<12}{'readout':<40}{'time':<6}{'Sham':>9}{'212 aged':>10}{'344 aged':>10}{'212 young':>10}{'AUC':>6}{'overlap':>9}{'restored':>10}{'344/young':>10}")
for bid, lab, scale, sgn, tp, tier, human in ROWS:
    g = G(bid); hai = 'HAI' in lab
    x = {k: tr(g[k], scale, hai) for k in ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']}
    pos = np.r_[x['PSLN-344'], x['PSLN-212(Y)']] * sgn; neg = np.r_[x['Sham'], x['PSLN-212']] * sgn
    a = auc(pos, neg); overlap = not (pos.min() > neg.max())
    m = {k: v.mean() for k, v in x.items()}
    restored = (m['PSLN-344'] - m['PSLN-212']) / (m['PSLN-212(Y)'] - m['PSLN-212'])
    disp = {k: (2 ** v if scale == 'log' else v) for k, v in m.items()}
    rel = disp['PSLN-344'] / disp['PSLN-212(Y)']
    # pairwise separation 344 vs 212 only
    sep = (x['PSLN-344'] * sgn).min() > (x['PSLN-212'] * sgn).max()
    thr = None
    if not overlap:
        lo, hi = neg.max() * sgn, pos.min() * sgn
        thr = (2 ** ((lo + hi) / 2)) if scale == 'log' else (lo + hi) / 2
    OUT['biomarkers'].append(dict(block=bid, readout=lab, time=tp, tier=tier, human=human, scale=scale, direction=sgn,
                                  sham=disp['Sham'], aged212=disp['PSLN-212'], aged344=disp['PSLN-344'], young212=disp['PSLN-212(Y)'],
                                  auc=a, ranges_overlap=bool(overlap), sep_344_vs_212=bool(sep), restored=float(restored), rel_to_young=float(rel), threshold=thr))
    print(f"{bid:<12}{lab:<40}{tp:<6}{disp['Sham']:>9.2f}{disp['PSLN-212']:>10.2f}{disp['PSLN-344']:>10.2f}{disp['PSLN-212(Y)']:>10.2f}{a:>6.2f}{('yes' if overlap else 'NO'):>9}{100*restored:>9.0f}%{100*rel:>9.0f}%")
# Gm-csf and monocyte/DC time-course peaks (no young arm for Gm-csf)
b = B['S01-E']; pk = {k: float(np.mean(b['groups'][k]['4'])) for k in b['order']}
b2 = B['S01-D']; pk2 = {k: float(np.mean(b2['groups'][k]['4'])) for k in b2['order']}
print("\nS01-E lung CD11b+ DC day-4 peak:", {k: round(v, 1) for k, v in pk.items()}, " restored:", round((pk['PSLN-344'] - pk['PSLN-212']) / (pk['PSLN-212(Y)'] - pk['PSLN-212']), 2))
print("S01-D lung monocytes day-4 peak:", {k: round(v, 1) for k, v in pk2.items()}, " restored:", round((pk2['PSLN-344'] - pk2['PSLN-212']) / (pk2['PSLN-212(Y)'] - pk2['PSLN-212']), 2))
OUT['S01-E_d4'] = pk; OUT['S01-D_d4'] = pk2

# --------------------------------------------------------------------------------- power
print("\n" + "=" * 100); print("SAMPLE-SIZE CALCULATIONS FOR PROPOSED STUDIES"); print("=" * 100)
def fisher_power(p1, p2, n, alpha=0.05):
    """exact power of two-sided Fisher exact test, n per arm"""
    pw = 0.0
    for a in range(n + 1):
        pa = stats.binom.pmf(a, n, p1)
        if pa < 1e-12: continue
        for c in range(n + 1):
            pc = stats.binom.pmf(c, n, p2)
            if pc < 1e-12: continue
            if stats.fisher_exact([[a, n - a], [c, n - c]])[1] <= alpha: pw += pa * pc
    return pw
def n_for(p1, p2, target=0.9, alpha=0.05, nmax=80):
    for n in range(4, nmax):
        if fisher_power(p1, p2, n, alpha) >= target: return n, fisher_power(p1, p2, n, alpha)
    return None, None
scen = [('replication: PSLN-344 85% vs PSLN-212 14% (pooled observed)', 0.85, 0.1375),
        ('conservative replication: 78% vs 19% (worst-case sensitivity)', 0.78, 0.19),
        ('attribution: PSLN-344 85% vs Mn-only control assumed 50%', 0.85, 0.50),
        ('attribution: PSLN-344 85% vs Mn-only control assumed 40%', 0.85, 0.40),
        ('benchmark: PSLN-344 85% vs licensed-type comparator assumed 45%', 0.85, 0.45)]
for lab, p1, p2 in scen:
    n80, pw80 = n_for(p1, p2, 0.8); n90, pw90 = n_for(p1, p2, 0.9)
    print(f"   survival, {lab}: n/arm = {n80} (power {pw80:.2f}) for 80%; {n90} (power {pw90:.2f}) for 90%  [two-sided Fisher exact, alpha 0.05]")
    OUT['power'][lab] = dict(n80=n80, n90=n90)
print(f"   power actually available in the existing n=7 design for 85% vs 14%: {fisher_power(0.85, 0.1375, 7):.2f}; for 85% vs 50%: {fisher_power(0.85, 0.5, 7):.2f}")
OUT['power']['existing_n7_85v14'] = fisher_power(0.85, 0.1375, 7); OUT['power']['existing_n7_85v50'] = fisher_power(0.85, 0.5, 7)

# continuous: HAI on log2 scale, pooled within-group SD across the adjuvanted arms of S03-C and S03-G
sds = []
for bid in ['S03-C', 'S03-G', 'S03-D', 'S03-H']:
    for k in ['CMP-204', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']:
        sds.append(np.std(np.log2(G(bid)[k]), ddof=1))
    print(f"   {bid} within-group SD of log2 titre by arm: " + ', '.join(f"{k} {np.std(np.log2(G(bid)[k]), ddof=1):.2f}" for k in ['CMP-204', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']))
sd_hai = float(np.sqrt(np.mean(np.square(sds[:8])))); sd_neut = float(np.sqrt(np.mean(np.square(sds[8:]))))
print(f"   pooled SD log2: HAI {sd_hai:.2f}; neutralising {sd_neut:.2f}")
def n_t(delta_log2, sd, power=0.9, alpha=0.05, sides=2):
    from scipy.stats import nct, t as tdist
    for n in range(3, 500):
        df = 2 * n - 2; nc = delta_log2 / (sd * math.sqrt(2 / n)); tc = tdist.ppf(1 - alpha / sides, df)
        pw = 1 - nct.cdf(tc, df, nc) + (nct.cdf(-tc, df, nc) if sides == 2 else 0)
        if pw >= power: return n, pw
for lab, fold in [('superiority, detect 4-fold GMR', 4), ('superiority, detect 3-fold GMR', 3), ('superiority, detect 2-fold GMR', 2)]:
    n, pw = n_t(math.log2(fold), sd_hai); n2, pw2 = n_t(math.log2(fold), sd_neut)
    print(f"   HAI {lab}: n/arm = {n} (power {pw:.2f});  neutralising titre: n/arm = {n2} (power {pw2:.2f})")
    OUT['power'][f'HAI {lab}'] = dict(n=n, n_neut=n2)
# non-inferiority of aged PSLN-344 vs young PSLN-212: margin GMR 0.5 (1 log2), true GMR assumed 0.8 (observed 0.76-0.87), one-sided 0.025
def n_ni(true_log2, margin_log2, sd, power=0.9, alpha=0.025):
    for n in range(3, 2000):
        se = sd * math.sqrt(2 / n); df = 2 * n - 2
        nc = (true_log2 - margin_log2) / se; tc = stats.t.ppf(1 - alpha, df)
        pw = 1 - stats.nct.cdf(tc, df, nc)
        if pw >= power: return n, pw
for true in [0.87, 0.76]:
    n, pw = n_ni(math.log2(true), math.log2(0.5), sd_hai)
    print(f"   HAI non-inferiority aged PSLN-344 vs young PSLN-212, margin GMR 0.5, assumed true GMR {true}: n/arm = {n} (power {pw:.2f})")
    OUT['power'][f'NI true {true}'] = n
OUT['power']['sd_hai_log2'] = sd_hai; OUT['power']['sd_neut_log2'] = sd_neut
# background mortality: how many unchallenged controls to estimate 14-d background mortality to +/- 10 points
u = 4 / 21
for n in [20, 30, 40]:
    lo, hi = stats.beta.ppf(0.025, max(round(u * n), 1), n - round(u * n) + 1), stats.beta.ppf(0.975, round(u * n) + 1, n - round(u * n))
    print(f"   unchallenged aged controls n={n}: if {round(u*n)}/{n} die, exact 95% CI {100*lo:.0f}-{100*hi:.0f}%")
json.dump(OUT, open('/tmp/work/parsed/biomarker_power.json', 'w'), indent=1, default=float)
