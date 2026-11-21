"""07_immunogenicity_moa.py
Group summaries and contrasts for every non-survival block.

Scale rules (from the annotation):
  * titres (IgG, subclass, HAI, neutralising) are reciprocal dilutions stored on a linear scale -> analysed on log2;
    summary = geometric mean titre (GMT), contrasts = geometric mean ratios (GMR).  HAI printed as 0 is below the
    lowest dilution tested (1:10) and is set to 5 (half the LLOQ) for the GMT.
  * qPCR blocks S01-A, S02-F, S03-L, S08-A, S10-A are linear fold-change -> analysed on log scale (GM fold);
    S09-A is already log10.
  * flow-cytometry percentages and ratios -> arithmetic mean, SD.
Contrasts: Welch t-test on the analysis scale (two-sided) plus the exact Mann-Whitney p (min. attainable p with
5 v 5 = 0.0079, 3 v 3 = 0.10).  Holm adjustment across the PSLN-344-vs-PSLN-212 family is reported.
"""
import json, math, itertools
import numpy as np
from scipy import stats
B = json.load(open('/tmp/work/parsed/parsed_blocks.json'))
G = lambda bid: B[bid]['groups']
OUT = {}

def gm(x): x = np.asarray(x, float); return float(np.exp(np.mean(np.log(x))))
def gm_ci(x):
    lx = np.log(np.asarray(x, float)); n = len(lx); m = lx.mean(); se = lx.std(ddof=1) / math.sqrt(n)
    tcrit = stats.t.ppf(0.975, n - 1); return math.exp(m), math.exp(m - tcrit * se), math.exp(m + tcrit * se)
def welch(a, b, log=False):
    a = np.asarray(a, float); b = np.asarray(b, float)
    if log: a, b = np.log(a), np.log(b)
    t, p = stats.ttest_ind(a, b, equal_var=False)
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    df = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))
    d = a.mean() - b.mean(); se = math.sqrt(va + vb); tc = stats.t.ppf(0.975, df)
    est, lo, hi = d, d - tc * se, d + tc * se
    if log: est, lo, hi = math.exp(est), math.exp(lo), math.exp(hi)
    return est, lo, hi, p
def mwu(a, b):
    return stats.mannwhitneyu(a, b, alternative='two-sided', method='exact').pvalue

# ---------------------------------------------------------------------------------------------- 1. titres
print("=" * 118)
print("1. SEROLOGY  (GMT [95% CI]; GMR with 95% CI from Welch on log scale; exact Mann-Whitney p)")
print("=" * 118)
TITRE = [('S03-A', 'IgG anti-H1N1 d14'), ('S03-E', 'IgG anti-H3N2 d14'), ('S03-C', 'HAI H1N1 d14'), ('S03-G', 'HAI H3N2 d14'),
         ('S03-D', 'Neut H1N1 d14'), ('S03-H', 'Neut H3N2 d14'), ('S13-I', 'IgG anti-H1N1 d28 post-boost'), ('S13-J', 'IgG anti-H3N2 d28 post-boost'),
         ('S13-A', 'IgG2a anti-H1N1 d14'), ('S13-B', 'IgG1 anti-H1N1 d14'), ('S13-C', 'IgG2a anti-H3N2 d14'), ('S13-D', 'IgG1 anti-H3N2 d14')]
fam = []
for bid, name in TITRE:
    g = {k: [5 if (v == 0 and 'HAI' in name) else v for v in vals] for k, vals in G(bid).items()}
    OUT[bid] = {'name': name, 'groups': {}}
    line = f"{bid:<6} {name:<30}"
    for k in B[bid]['order']:
        m, lo, hi = gm_ci(g[k]); OUT[bid]['groups'][k] = dict(gmt=m, lo=lo, hi=hi, n=len(g[k]), raw=G(bid)[k])
        line += f" | {k}: {m:,.0f} [{lo:,.0f}-{hi:,.0f}]"
    print(line)
    for a, b_ in [('PSLN-344', 'PSLN-212'), ('PSLN-344', 'PSLN-212(Y)'), ('PSLN-344', 'Sham'), ('PSLN-212', 'Sham'), ('PSLN-212', 'CMP-204')]:
        if a in g and b_ in g:
            est, lo, hi, p = welch(g[a], g[b_], log=True); pm = mwu(g[a], g[b_])
            OUT[bid][f'GMR {a}/{b_}'] = dict(gmr=est, lo=lo, hi=hi, p_welch=p, p_mwu=pm)
            print(f"         GMR {a}/{b_:<12} = {est:7.2f}  [{lo:.2f}-{hi:.2f}]  Welch p={p:.2g}  MWU exact p={pm:.3g}")
            if (a, b_) == ('PSLN-344', 'PSLN-212'): fam.append((bid, name, p))
    if 'HAI' in name:
        sp = {k: f"{sum(1 for v in G(bid)[k] if v >= 40)}/{len(G(bid)[k])}" for k in B[bid]['order']}
        OUT[bid]['seroprotection_ge40'] = sp
        print(f"         animals with HAI >= 40: {sp}")

# IgG2a/IgG1 from raw subclass blocks (NOT from S03-B/S03-F whose column labels are rotated; see 05_derived_value_checks.py)
print("\n   IgG2a:IgG1 per-animal quotient recomputed from the raw subclass blocks (labels as in S13-A..D):")
for num, den, virus in [('S13-A', 'S13-B', 'H1N1'), ('S13-C', 'S13-D', 'H3N2')]:
    q = {k: [a / b for a, b in zip(G(num)[k], G(den)[k])] for k in B[num]['order']}
    OUT[f'IgG2a:IgG1 {virus}'] = {k: dict(gm=gm(v), vals=v) for k, v in q.items()}
    est, lo, hi, p = welch(q['PSLN-344'], q['PSLN-212'], log=True)
    est2, lo2, hi2, p2 = welch(q['PSLN-344'], q['PSLN-212(Y)'], log=True)
    print(f"     {virus}: " + ' | '.join(f"{k}: GM {gm(v):.2f}" for k, v in q.items()) + f"   ratio 344/212 = {est:.1f} [{lo:.1f}-{hi:.1f}] p={p:.2g};  344/212(Y) = {est2:.2f} [{lo2:.2f}-{hi2:.2f}] p={p2:.2g}")
    OUT[f'IgG2a:IgG1 {virus}']['ratio_344_212'] = dict(est=est, lo=lo, hi=hi, p=p)
    OUT[f'IgG2a:IgG1 {virus}']['ratio_344_Y'] = dict(est=est2, lo=lo2, hi=hi2, p=p2)
    print(f"       (as PRINTED in {'S03-B' if virus=='H1N1' else 'S03-F'}: " + ' | '.join(f"{k}: GM {gm(v):.2f}" for k, v in G('S03-B' if virus == 'H1N1' else 'S03-F').items()) + ")")

# ---------------------------------------------------------------------------------------------- 2. static % blocks
print("\n" + "=" * 118)
print("2. CELLULAR / MECHANISTIC BLOCKS WITH THE FOUR STANDARD ARMS  (mean +/- SD; difference 344-212 [95% CI]; % of young benchmark)")
print("=" * 118)
STATIC = [
 ('S01-F', 'lung cDC1 % (72 h)'), ('S01-G', 'lung cDC2 % (72 h)'),
 ('S02-A', 'CCR7+ of lung CD11b+ DC % (72 h)'), ('S02-B', 'MLN CD11b+CD103- DC % (72 h)'),
 ('S02-D_CD40', 'CD40+ of MLN CD11b+ DC % (d3)'), ('S02-D_CD86', 'CD86+ of MLN CD11b+ DC % (d3)'),
 ('S02-C', 'OVA-AF647+ MLN DC % (36 h)'), ('S02-E', 'OT-I proliferation by MLN CD11b+ DC % (ex vivo)'),
 ('S03-K', 'GC B cells in MLN % (d7)'),
 ('S04-A_ICOShi', 'Tfh ICOS-hi % (d7)'), ('S04-A_ICOSlo', 'Tfh ICOS-lo % (d7)'),
 ('S04-B_Foxp3', 'Tfr (Foxp3+ of CXCR5+ICOShi) % (d7)'), ('S04-B_TfhTfr', 'Tfh:Tfr quotient (d7)'), ('S04-C', 'Tfr % (d30)'), ('S04-D', 'lung Treg % (d7)'),
 ('S05-D', 'Ki-67+ lung CD8 % (d3)'), ('S05-E', 'GZMB+ lung CD8 % (d3)'), ('S05-F', 'IFN-g+ CD8 MLN, rgH5N1 restim % (d14)'),
 ('S05-G', 'IFN-g+ CD8 MLN, rgH5N1 restim % (d60)'), ('S05-H', 'GZMB+ CD8 MLN % (d60)'), ('S05-I', 'lung CD8 TRM % (d25)'),
 ('S14-A_H1N1', 'IFN-g+ CD8 MLN, H1N1 restim %'), ('S14-A_H3N2', 'IFN-g+ CD8 MLN, H3N2 restim %'),
 ('S13-H', 'IgG+ of MLN B220+ %'), ('S11-E', 'CD206+ lung macrophages %'),
]
for bid, name in STATIC:
    g = G(bid); OUT[bid] = {'name': name, 'groups': {k: dict(mean=float(np.mean(v)), sd=float(np.std(v, ddof=1)), n=len(v)) for k, v in g.items()}}
    line = f"{bid:<13}{name:<48}" + ' | '.join(f"{k}: {np.mean(v):.2f}±{np.std(v, ddof=1):.2f}" for k, v in g.items())
    print(line)
    if 'PSLN-344' in g and 'PSLN-212' in g:
        est, lo, hi, p = welch(g['PSLN-344'], g['PSLN-212']); pm = mwu(g['PSLN-344'], g['PSLN-212'])
        fold = np.mean(g['PSLN-344']) / np.mean(g['PSLN-212'])
        y = g.get('PSLN-212(Y)')
        pct_y = 100 * np.mean(g['PSLN-344']) / np.mean(y) if y else float('nan')
        py = welch(g['PSLN-344'], y)[3] if y else float('nan')
        OUT[bid].update(diff_344_212=est, lo=lo, hi=hi, p_welch=p, p_mwu=pm, fold_344_212=float(fold), pct_of_young=float(pct_y), p_vs_young=float(py))
        print(f"{'':<13}   344-212 = {est:+.2f} [{lo:+.2f},{hi:+.2f}]  fold {fold:.2f}x  Welch p={p:.2g}  MWU p={pm:.3g}   | 344 as % of young 212(Y): {pct_y:.0f}% (Welch p vs young = {py:.2g})")
        fam.append((bid, name, p))

# Holm across the 344-vs-212 family
fam_sorted = sorted(fam, key=lambda x: x[2]); m = len(fam_sorted); holm = {}; running = 0
for i, (bid, name, p) in enumerate(fam_sorted):
    adj = min(1.0, (m - i) * p); running = max(running, adj); holm[bid] = running
print(f"\n   Holm-adjusted p (family of {m} PSLN-344 vs PSLN-212 contrasts, aged animals): " )
print('   ' + '; '.join(f"{bid} {holm[bid]:.2g}" for bid, _, _ in fam_sorted))
OUT['holm_344_v_212'] = holm

# ---------------------------------------------------------------------------------------------- 3. time courses
print("\n" + "=" * 118)
print("3. TIME COURSES (mean per group per timepoint)")
print("=" * 118)
for bid, name in [('S01-D', 'lung monocytes %'), ('S01-E', 'lung CD11b+ DC %'), ('S02-F', 'Gm-csf mRNA fold (GM)'), ('S07-A', 'lung Ly6C+CCR2+ macrophages x10^5'),
                  ('S11-A', 'alveolar macrophages %'), ('S11-B', 'neutrophils % (shares replicates with S11-A)'), ('S11-D', 'NK cells %'),
                  ('S05-A', 'NP tetramer+ lung CD8 % (n=2)'), ('S05-B', 'NP tetramer+ MLN CD8 % (n=2)')]:
    b = B[bid]; OUT[bid] = {'name': name, 'groups': {}}
    print(f"{bid}  {name}")
    for k in b['order']:
        vals = b['groups'][k]
        f = gm if 'fold' in name else np.mean
        ms = {t: float(f([x for x in v if x is not None])) for t, v in vals.items()}
        OUT[bid]['groups'][k] = ms
        print(f"      {k:<14}" + '  '.join(f"{t}: {m:6.2f}" for t, m in ms.items()))
    if bid in ('S01-D', 'S01-E'):
        for t in b['times'][1:]:
            est, lo, hi, p = welch(b['groups']['PSLN-344'][t], b['groups']['PSLN-212'][t])
            print(f"         day {t}: 344-212 = {est:+.1f} [{lo:+.1f},{hi:+.1f}] p={p:.2g}")
            OUT[bid][f'd{t}_344_v_212'] = dict(est=est, lo=lo, hi=hi, p=p)
    if bid == 'S02-F':
        for t in b['times']:
            est, lo, hi, p = welch(b['groups']['PSLN-344'][t], b['groups']['PSLN-212'][t], log=True)
            print(f"         {t}: GM ratio 344/212 = {est:.2f} [{lo:.2f}-{hi:.2f}] p={p:.2g}")
            OUT[bid][f'{t}_344_v_212'] = dict(est=est, lo=lo, hi=hi, p=p)
    if bid == 'S07-A':
        for t in b['times']:
            est, lo, hi, p = welch(b['groups']['PSLN-212'][t], b['groups']['PSLN-344'][t])
            print(f"         day {t}: 212-344 = {est:+.1f} [{lo:+.1f},{hi:+.1f}] x10^5, p={p:.2g} (n=3)")

# ---------------------------------------------------------------------------------------------- 4. innate / dose
print("\n" + "=" * 118)
print("4. INNATE ACTIVATION (Ifnb1) AND DOSE-RESPONSE")
print("=" * 118)
for bid in ['S01-A_16h', 'S01-A_72h']:
    g = G(bid); OUT[bid] = {'groups': {}}
    print(bid, ' GM fold [95% CI]: ' + ' | '.join(f"{k}: {gm_ci(v)[0]:.1f} [{gm_ci(v)[1]:.1f}-{gm_ci(v)[2]:.1f}]" for k, v in g.items()))
    for k, v in g.items(): OUT[bid]['groups'][k] = dict(zip(['gm', 'lo', 'hi'], gm_ci(v)))
    for a, b_ in [('PSLN-344', 'PSLN-212'), ('PSLN-344', 'PSLN-212(Y)'), ('PSLN-212', 'PSLN-212(Y)'), ('PSLN-212', 'CMP-204'), ('PSLN-344(Y)', 'PSLN-212(Y)'), ('PSLN-344', 'PSLN-212/R848')]:
        est, lo, hi, p = welch(g[a], g[b_], log=True)
        OUT[bid][f'{a}/{b_}'] = dict(est=est, lo=lo, hi=hi, p=p)
        print(f"       ratio {a}/{b_:<14} = {est:.2f} [{lo:.2f}-{hi:.2f}]  p={p:.2g}")
b = B['S08-A']; OUT['S08-A'] = {}
print("S08-A Ifnb1 16 h dose-response, GM fold (n=3):")
for k in b['order']:
    ms = {t: gm(v) for t, v in b['groups'][k].items()}; OUT['S08-A'][k] = ms
    print(f"      {k:<14}" + '  '.join(f"{t} ug: {m:5.1f}" for t, m in ms.items()))
r = {t: OUT['S08-A']['PSLN-344'][t] / OUT['S08-A']['PSLN-212'][t] for t in b['times']}
print("      ratio 344/212 by dose: " + '  '.join(f"{t} ug: {v:.2f}" for t, v in r.items()))
print(f"      PSLN-344 20 ug as % of its 40 ug response: {100*OUT['S08-A']['PSLN-344']['20']/OUT['S08-A']['PSLN-344']['40']:.0f}% ; PSLN-212 at 40 ug vs PSLN-344 at 5/10/20 ug: {OUT['S08-A']['PSLN-212']['40']:.1f} vs {OUT['S08-A']['PSLN-344']['5']:.1f}/{OUT['S08-A']['PSLN-344']['10']:.1f}/{OUT['S08-A']['PSLN-344']['20']:.1f}")
from scipy.optimize import curve_fit
def hill(d, top, ed50, h): return 1 + (top - 1) * d ** h / (ed50 ** h + d ** h)
for k in ['PSLN-344', 'PSLN-212', 'CMP-204']:
    d = np.repeat([1, 5, 10, 20, 40], 3).astype(float); y = np.array([v for t in b['times'] for v in b['groups'][k][t]], float)
    try:
        popt, pcov = curve_fit(hill, d, y, p0=[y.max(), 10, 2], bounds=([1, 0.5, 0.3], [500, 200, 8]))
        se = np.sqrt(np.diag(pcov))
        print(f"      Hill fit {k}: Emax {popt[0]:.1f} (SE {se[0]:.1f}), ED50 {popt[1]:.1f} ug (SE {se[1]:.1f}), slope {popt[2]:.2f}")
        OUT['S08-A'][f'hill_{k}'] = dict(top=popt[0], ed50=popt[1], h=popt[2], se=se.tolist())
    except Exception as ex:
        print('      fit failed', k, ex)
print("S08-B encapsulation efficiency % (mean ± SD): " + ' | '.join(f"{k}: {np.mean(v):.1f}±{np.std(v, ddof=1):.1f}" for k, v in G('S08-B').items()))
OUT['S08-B'] = {k: dict(mean=float(np.mean(v)), sd=float(np.std(v, ddof=1))) for k, v in G('S08-B').items()}

# ---------------------------------------------------------------------------------------------- 5. intervention experiments
print("\n" + "=" * 118)
print("5. INTERVENTION (cause-and-effect) EXPERIMENTS")
print("=" * 118)
def contrast(bid, a, b_, label, log=False):
    g = G(bid); est, lo, hi, p = welch(g[a], g[b_], log=log)
    ma, mb = (gm(g[a]), gm(g[b_])) if log else (np.mean(g[a]), np.mean(g[b_]))
    pm = mwu(g[a], g[b_])
    print(f"   {bid:<11}{label:<62} {a}: {ma:.2f} vs {b_}: {mb:.2f}  -> {'ratio' if log else 'diff'} {est:.2f} [{lo:.2f},{hi:.2f}]  Welch p={p:.2g}, MWU p={pm:.3g} (n={len(g[a])},{len(g[b_])})")
    OUT[f'{bid}::{a} vs {b_}'] = dict(label=label, a=float(ma), b=float(mb), est=est, lo=lo, hi=hi, p=p, p_mwu=pm, n=(len(g[a]), len(g[b_])))
contrast('S01-C', 'WT', 'SPA/D', 'SP-A/D needed for liposome uptake by AM (DiD+ %)')
contrast('S01-B', 'AECII/PSLN-SRB', 'AECII/FreeSRB', 'liposome delivers cargo to AEC-II (SRB+ %)')
contrast('S01-B', 'AECI/PSLN-SRB', 'AECI/FreeSRB', 'liposome delivers cargo to AEC-I (SRB+ %)')
contrast('S11-C', 'CBX-', 'CBX+', 'gap-junction block (CBX) lowers monocyte recruitment %')
contrast('S07-B_mono', 'PSLN-344', 'PSLN-344+INCB3344', 'CCR2 antagonist lowers lung monocytes %')
contrast('S07-B_mac', 'PSLN-344', 'PSLN-344+INCB3344', 'CCR2 antagonist lowers Ly6C+ macrophages %')
contrast('S02-I', 'PSLN-344(Y)', 'PSLN-344(Y)+INCB3344', 'CCR2 antagonist lowers GZMB+ lung CD8 % (young)')
contrast('S02-H', 'WT w/o cDC', 'IFN w/o cDC', 'IFNAR needed for monocyte->DC (pre-cDC depleted) %')
contrast('S02-H', 'WT w/ cDC', 'IFN w/ cDC', 'IFNAR needed (pre-cDC present) %')
contrast('S02-H', 'GMCSF', 'IFN w/o cDC', 'rGM-CSF rescues IFNAR-KO monocyte->DC %')
contrast('S02-H', 'GMCSF', 'WT w/o cDC', 'rGM-CSF rescue vs WT %')
contrast('S12-A', 'WT to WT', 'IFNAR-/- to WT', 'IFNAR dispensable for monocyte infiltration % (n=3)')
contrast('S02-G', 'PSLN-212+GM-CSF', 'PSLN-212', 'rGM-CSF adds to PSLN-212 for moDC % (d5)')
contrast('S02-G', 'PSLN-212', 'GM-CSF', 'PSLN-212 vs rGM-CSF alone for moDC %')
contrast('S02-C', 'PSLN-344', 'PTX', 'PTX blocks antigen+ DC arrival in MLN % (PTX arm adjuvant not stated)')
contrast('S02-E', 'PSLN-344', 'PTX', 'PTX abolishes DC cross-priming capacity %')
contrast('S05-C', 'MLN', 'MLN+PTX', 'PTX blocks OT-I proliferation in MLN % (n=3)')
contrast('S05-C', 'Lung', 'Lung+PTX', 'PTX does not block OT-I proliferation in lung % (n=3)')
g = G('S07-C'); ks = list(g)
print(f"   S07-C      macrophage transfer -> lung Treg %: both columns are printed with the same label ({ks[0]!r}); col B mean {np.mean(g[ks[0]]):.2f}, col C mean {np.mean(g[ks[1]]):.2f}; Welch p={welch(g[ks[0]], g[ks[1]])[3]:.2g} -> direction cannot be assigned")
OUT['S07-C'] = dict(colB=float(np.mean(g[ks[0]])), colC=float(np.mean(g[ks[1]])), p=welch(g[ks[0]], g[ks[1]])[3])
for an, bid in [('Aicda', 'S03-L_Aicda'), ('E47', 'S03-L_E47')]:
    g = G(bid); print(f"   {bid:<11} {an} fold in MLN B cells (GM, n=3): " + ' | '.join(f"{k}: {gm(v):.1f}" for k, v in g.items()) + f"   344/212 = {welch(g['PSLN-344'], g['PSLN-212'], log=True)[0]:.1f}x, p={welch(g['PSLN-344'], g['PSLN-212'], log=True)[3]:.2g}")
    OUT[bid] = {k: gm(v) for k, v in g.items()}; OUT[bid]['ratio'] = welch(g['PSLN-344'], g['PSLN-212'], log=True)[:4]

# SRB S08-C both readings
g = G('S08-C'); ks = list(g)
print("\n   S08-C SRB+ epithelial cells, two readings of the header:")
print(f"      as printed      : " + ' | '.join(f"{k}: {np.mean(v):.1f}" for k, v in g.items()))
alt = dict(zip(['AECII-PSLN-SRB', 'AECI-PSLN-SRB', 'AECII-PSLN-344-SRB', 'AECI-PSLN-344-SRB'], [g[k] for k in ks]))
print(f"      reconciled to S01-B (cols = AECII-PSLN, AECI-PSLN, AECII-344, AECI-344): " + ' | '.join(f"{k}: {np.mean(v):.1f}" for k, v in alt.items()))
OUT['S08-C'] = dict(printed={k: float(np.mean(v)) for k, v in g.items()}, reconciled={k: float(np.mean(v)) for k, v in alt.items()})

json.dump(OUT, open('/tmp/work/parsed/immuno_moa_results.json', 'w'), indent=1, default=float)
