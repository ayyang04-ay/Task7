"""14_content.py -- builds the proposal (document blocks) from the analysis tables, then renders PDF + Markdown."""
import pandas as pd, numpy as np, sys
sys.path.insert(0, '/tmp/work/code')
T = '/tmp/work/tables/'
SUM = pd.read_csv(T+'continuous_summary.csv'); SUM['time'] = SUM['time'].astype(str)
CON = pd.read_csv(T+'continuous_contrasts.csv'); CON['time'] = CON['time'].astype(str)
GAP = pd.read_csv(T+'age_gap_curated.csv'); GAP['time'] = GAP['time'].astype(str)
SBG = pd.read_csv(T+'survival_by_group.csv'); STS = pd.read_csv(T+'survival_tests.csv'); SPL = pd.read_csv(T+'survival_pooled.csv')
MEC = pd.read_csv(T+'mechanism_tests.csv'); CNS = pd.read_csv(T+'cns_S10A.csv'); DR = pd.read_csv(T+'dose_response_S08A.csv')
RG = pd.read_csv(T+'reactogenicity_S08D.csv'); BIO = pd.read_csv(T+'biomarker_screen.csv'); SS = pd.read_csv(T+'sample_size_planning.csv')
LOG = pd.read_csv(T+'data_integrity_log.csv'); R848 = pd.read_csv(T+'r848_contrasts.csv')

def fnum(x, d=None):
    if pd.isna(x): return 'n/a'
    x = float(x)
    if d is not None: return f"{x:,.{d}f}"
    a = abs(x)
    if a >= 1000: return f"{x:,.0f}"
    if a >= 100: return f"{x:.0f}"
    if a >= 10: return f"{x:.1f}"
    if a >= 1: return f"{x:.2f}"
    return f"{x:.2f}"
def fp(p):
    if pd.isna(p): return 'n/a'
    if p < 0.0001: return '<0.0001'
    if p < 0.001: return f"{p:.4f}"
    return f"{p:.3f}" if p < 0.1 else f"{p:.2f}"
def center(block, group, time=None, meas=None):
    d = SUM[(SUM.block == block) & (SUM.group == group)]
    if time is not None: d = d[d.time == str(time)]
    if meas is not None: d = d[d.measurand.str.contains(meas, regex=False)]
    if len(d) == 0: return np.nan
    r = d.iloc[0]
    return r.gmean if r.scale == 'log' and not pd.isna(r.get('gmean', np.nan)) else r['mean']
def con(block, contrast, time=None, meas=None):
    d = CON[(CON.block == block) & (CON.contrast == contrast)]
    if time is not None: d = d[d.time == str(time)]
    if meas is not None: d = d[d.measurand.str.contains(meas, regex=False)]
    return d.iloc[0]
def gap(block, time=None, meas=None):
    d = GAP[GAP.block.str.startswith(block)]
    if time is not None: d = d[d.time == str(time)]
    if meas is not None: d = d[d.readout.str.contains(meas, regex=False)]
    return d.iloc[0].gap_closed if len(d) else np.nan
def sv(block, group):
    r = SBG[(SBG.block == block) & (SBG.group == group)]
    if len(r) == 0: return '–'
    r = r.iloc[0]; return f"{int(r.survivors)}/{int(r.n)}"
def lr(block, contrast):
    r = STS[(STS.block == block) & (STS.contrast == contrast)]
    return fp(r.iloc[0].logrank_p) if len(r) else '–'
PR = SPL[SPL.analysis.str.startswith('PRIMARY')].iloc[0]
def pool(prefix): return SPL[SPL.analysis.str.startswith(prefix)].iloc[0]

B = []   # document blocks
def H1(t): B.append(('h1', t))
def H2(t): B.append(('h2', t))
def H3(t): B.append(('h3', t))
def P(t): B.append(('p', t))
def SM(t): B.append(('small', t))
def BL(l): B.append(('bullets', l))
def NL(l): B.append(('numbered', l))
def CO(t, col='#eaf2fb'): B.append(('callout', t, col))
def TB(**k): B.append(('table', k))
def FG(path, w, cap): B.append(('figure', path, w, cap))
def PB(): B.append(('pagebreak',))

hr344 = f"{PR.cox_HR:.3f} (95% CI {PR.HR_lo:.3f}–{PR.HR_hi:.3f})"
rd344 = f"{100*PR.MH_RD_death:.0f} percentage points (95% CI {100*PR.RD_lo:.0f} to {100*PR.RD_hi:.0f})"
ifn = con('S01-A', 'PSLN-344 vs PSLN-212', '16h')
hai = con('S03-C', 'PSLN-344 vs PSLN-212'); haiA = con('S03-G', 'PSLN-344 vs PSLN-212')
medgap = GAP.gap_closed.median(); q1, q3 = GAP.gap_closed.quantile([.25, .75])
het = pool('Heterosubtypic'); early = pool('Challenge 2-3'); d14 = pool('Challenge 14'); d60 = pool('Challenge 60')

# =====================================================================================
H1('1. Recommendation')
CO(['**Recommendation: keep the program in the portfolio. Take PSLN-344 forward as the single lead asset and stop PSLN-212 now. Release funding in gated tranches: first a short data-verification gate that is a hard stop, then a confirmatory and attribution study, before any IND-enabling spend.**',
    f'**Why PSLN-344.** It is the only formulation in our data that reliably protects aged (20-month) mice. Across 8 aged-mouse challenge experiments (59 animals per arm), survival was **83% with PSLN-344, 12% with PSLN-212 and 2% with vaccine plus empty liposome**. The stratified hazard ratio for PSLN-344 vs PSLN-212 is {hr344} [S03-I, S03-J, S06-A/B/C/E/F/G; A5].',
    f'**Why it works.** Mn²⁺ repairs the aged lung\'s blunted innate response. Lung IFN-β at 16 h is {fnum(ifn.mean_a)}-fold with PSLN-344 vs {fnum(ifn.mean_b)}-fold with PSLN-212; the young reference is {fnum(center("S01-A","PSLN-212(Y)","16h"))}-fold [S01-A; A2]. Downstream, PSLN-344 closes a median **{100*medgap:.0f}%** (IQR {100*q1:.0f}–{100*q3:.0f}%) of the age-related deficit across 40 immune readouts [A3].',
    '**Why PSLN-212 goes.** In aged animals it cannot be distinguished from vaccine plus empty liposome on survival (7/59 vs 1/59, p=0.061) [A4/A5]. In young animals it adds nothing: PSLN-212, PSLN-344 and the cGAMP comparator liposome CMP-204 all give 100% survival [S09-B/D/F, S13-E; A4].',
    '**Why gated rather than a full go.** The workbook contains data-integrity defects that the committee will find if it checks (Section 3). The core conclusion survives every sensitivity analysis, with a hazard ratio of 0.08–0.10 [A5]. Four value-defining questions are still open: whether CDN-1807 is needed at all, how PSLN-344 compares with licensed vaccines for older adults, whether intranasal Mn²⁺ is safe for the CNS, and whether protection lasts in aged animals.'], '#eaf2fb')
H3('What the committee is asked to approve today')
NL([f'**Gate 0, data verification (months 0–2, internal).** Source-record audit of {len(LOG)} logged issues. Hard stop if the 8 primary survival experiments cannot be substantiated.',
    '**Gate 1, confirmatory and attribution study (months 1–7).** Blinded, randomized, both sexes. Adds Mn-only and Mn+cGAMP arms to test whether the proprietary CDN-1807 is required.',
    '**Gates 2–3 released only after Gate 1 passes.** These cover benchmarking against licensed enhanced vaccines, durability, Mn/CNS safety, and CMC/device work. They lead toward an IND at around months 18–24 (planning estimate).'])
H3('How confident we are')
BL(['**Biological signal: high.** Effects are large (8–19-fold titre gains; survival 83% vs 12%) and consistent across about 40 readouts and 8 independent survival experiments.',
    '**Evidence quality: moderate to low until verified.** There is one exact duplicate experiment, body-weight records reused across experiments and strains, rotated labels, and unexplained deaths among untreated controls (Section 3).',
    '**Translational risk: substantial.** Open items are the delivery route (alveolar targeting in mice vs nasal spray in people), intranasal Mn²⁺ neurotoxicity, the lack of any head-to-head against licensed enhanced vaccines, female-only data, and day-60 durability (67% vs 100% in young).'])
SM('Citation convention: [Sxx-Y] = block in psln_program_dataset.xlsx (sheet-block as annotated); [A#] = analysis (Appendix A; numbers reproducible from PSLN_analysis_workbook.xlsx and the code folder). Unless stated, “aged” = 20-month female BALB/c, single intranasal dose, 20 µg adjuvant; PSLN-212(Y) = young (7–8-week) reference. Titres are geometric means; percentages are arithmetic means.')

# =====================================================================================
PB(); H1('2. How the asset looks: the evidence')
H2('2.1 Protection in aged mice (primary outcome)')
rows = []
designs = [('S03-I', 'Bivalent → 10× CA09 H1N1 (homologous), day 14'), ('S06-A', 'Aichi H3N2 → PR8 H1N1 (heterosubtypic), day 14'),
           ('S06-C', 'Bivalent → rgH5N1 (heterosubtypic), day 14'), ('S03-J', 'rgH5N1 → wild-type VN04 H5N1, day 2 (age not stated; aged by default)'),
           ('S06-B', 'Aichi H3N2 → PR8 H1N1, day 3'), ('S06-E(d60)', 'Aichi H3N2 → PR8 H1N1, day 60'),
           ('S06-F(d60)', 'Bivalent → rgH5N1, day 60'), ('S06-G(d60)', 'CA09 H1N1 → Perth H3N2, day 60')]
for b, d in designs:
    rows.append([b, d, sv(b, 'Sham'), sv(b, 'PSLN-212'), sv(b, 'PSLN-344'), sv(b, 'PSLN-212(Y)'), sv(b, 'Untreated'), lr(b, 'PSLN-344 vs PSLN-212')])
rows.append(['**Pooled (8)**', '**Stratified by experiment; S06-D excluded (duplicate)**', '**1/59 (2%)**', '**7/59 (12%)**', '**49/59 (83%)**', '**49/49 (100%)**', '17/21', f'**HR {PR.cox_HR:.3f}**'])
TB(header=['Block', 'Vaccine → challenge, day post-vaccination', 'Sham', 'PSLN-212', 'PSLN-344', 'Young PSLN-212', 'Untreated, unchallenged', 'Log-rank p, 344 vs 212'],
   rows=rows, widths=[.105, .28, .08, .09, .09, .1, .12, .1], font=7.3,
   caption='Table 1. Survivors / animals at end of follow-up in aged BALB/c mice [A4, A5]',
   note=f'Pooled PSLN-344 vs PSLN-212: stratified Cox HR {hr344}, p<0.0001. Mantel–Haenszel risk difference in death {rd344}. Sensitivity analyses: dropping S03-I (conflicting records, DI-05) gives HR {pool("Sens-1").cox_HR:.3f}; dropping S03-J gives HR {pool("Sens-2").cox_HR:.3f}; adding the compromised S15-L/N blocks gives HR {pool("Sens-4").cox_HR:.3f} [A5]. “Untreated” = 20-month animals given no vaccine, adjuvant or virus.')
P(f'**Subgroups [A5].** Challenge at day 14: {d14.surv_344} vs {d14.surv_212}. Early challenge (day 2–3): {early.surv_344} vs {early.surv_212}. Heterosubtypic challenges: {het.surv_344} vs {het.surv_212}. Day-60 challenge: {d60.surv_344} vs {d60.surv_212}. Middle-aged (14-month) mice, with or without a prior PR8 infection (“imprinting”): PSLN-344 12/14 in both groups, vs PSLN-212 0/14 (naive) and 4/14 (imprinted) [S06-E/F imprint; A5]. PSLN-344 survivors still lose somewhat more weight than protected young animals: mean nadir 87.3% vs 89.8% (p=0.0035) [S15-A/B/C/E/F/G; A9]. PSLN-344 therefore attenuates disease rather than preventing it.')
P('**Durability is the weak point.** At day 60, PSLN-344 protected 14/21 aged animals vs 21/21 young (p=0.009). Over the same 14 days, 4/21 untreated, unchallenged aged animals died, so the day-60 PSLN-344 result is statistically indistinguishable from background mortality (17/21 survived; p=0.48) [S06-E/F/G(d60); A4]. Antibody durability in aged animals was not measured beyond day 28.')

H2('2.2 Immunology: PSLN-344 vs PSLN-212 in aged mice')
spec = [('Innate', 'Lung Ifnb1, 16 h (fold)', 'S01-A', '16h', None), ('Innate', 'Lung Gm-csf, 36 h (fold)', 'S02-F', '36h', None),
        ('Myeloid', 'Lung Ly6C+ monocytes, d4 (%)', 'S01-D', '4', None), ('DC', 'CCR7+ migratory DC, 72 h (%)', 'S02-A', '72h', None),
        ('DC', 'Antigen+ DC in MLN, 36 h (%)', 'S02-C', '36h', None), ('DC', 'MLN DC CD86+, d3 (%)', 'S02-D CD86', 'd3', None),
        ('GC', 'ICOS-high Tfh, d7 (%)', 'S04-A', 'd7', 'ICOS-high'), ('GC', 'Tfr (Foxp3+), d7 (%)', 'S04-B Foxp3', 'd7', None),
        ('GC', 'GC B cells, d7 (%)', 'S03-K', 'd7', None), ('Antibody', 'HAI anti-CA09, d14 (GMT)', 'S03-C', 'd14', None),
        ('Antibody', 'HAI anti-Aichi, d14 (GMT)', 'S03-G', 'd14', None), ('Antibody', 'Neutralising anti-CA09, d14 (GMT)', 'S03-D', 'd14', None),
        ('Antibody', 'IgG anti-CA09, d14 (GMT)', 'S03-A', 'd14', None), ('Antibody', 'IgG2a/IgG1 anti-CA09 (from S13-A/B)', 'S13-A/B', 'd14', None),
        ('CD8', 'Lung Ki-67+ CD8, d3 (%)', 'S05-D', 'd3', None), ('CD8', 'IFN-γ+ CD8 (H5 restim), d14 (%)', 'S05-F', 'd14', None),
        ('CD8', 'Lung TRM CD69+CD103+, d25 (%)', 'S05-I', 'd25', None), ('Memory', 'IFN-γ+ CD8, d60 (%)', 'S05-G', 'd60', None)]
rows = []
for stage, lab, b, t, m in spec:
    c = con(b, 'PSLN-344 vs PSLN-212', t, m)
    eff = (f"×{c.est:.1f} ({c.lo:.1f}–{c.hi:.1f})" if c.effect == 'GMR' else f"{c.est:+.1f} pp ({c.lo:+.1f} to {c.hi:+.1f})")
    g = GAP[(GAP.block == b) & (GAP.time == t)]
    if m: g = g[g.readout.str.contains('ICOS')]
    gtxt = f"{100*g.iloc[0].gap_closed:.0f}%" if len(g) else 'n/a'
    rows.append([stage, f"{lab} [{b}]", fnum(center(b, 'Sham', t, m)), fnum(center(b, 'PSLN-212', t, m)), fnum(center(b, 'PSLN-344', t, m)),
                 fnum(center(b, 'PSLN-212(Y)', t, m)), eff, fp(c.tukey_p), gtxt])
TB(header=['Stage', 'Readout [block]', 'Sham', 'PSLN-212', 'PSLN-344', 'Young 212', 'PSLN-344 vs 212 (95% CI)', 'Tukey p', 'Age gap closed'],
   rows=rows, widths=[.08, .265, .07, .08, .08, .08, .17, .075, .075], font=7.0,
   caption='Table 2. Key immune readouts (n=5 per group unless noted; one-way ANOVA + Tukey on log₁₀ scale for titres/fold-changes, linear for %) [A2, A3]',
   note='×: geometric-mean ratio; pp: percentage-point difference. Age gap closed = (PSLN-344 − PSLN-212)/(young PSLN-212 − PSLN-212), on the analysis scale. Sham HAI values recorded as 0 (below the 1:10 LOD) imputed as 5 (DI-18). The IgG2a/IgG1 ratio is recomputed from the source titres (S13-A/B) because the printed ratio block S03-B carries rotated labels (DI-04).')
MU = pd.read_csv(T+'multiplicity_holm.csv')
P(f"**Multiplicity.** Across the 40 curated readouts (Fig 3), {int((MU.tukey_p_holm<0.05).sum())} PSLN-344 vs PSLN-212 differences stay significant after Holm correction using the block-wise Tukey p-values, and {int((MU.welch_p_holm<0.05).sum())} using Welch p-values [A2, A3]. The conclusion does not depend on selective reporting.")
H3('Where PSLN-344 falls short')
cd40 = con('S02-D CD40', 'PSLN-344 vs PSLN-212', 'd3'); cd86 = con('S02-D CD86', 'PSLN-344 vs PSLN-212', 'd3')
BL([f'**Dendritic-cell co-stimulation is barely restored.** CD40+ DCs are {cd40.mean_a:.1f}% vs {cd40.mean_b:.1f}% (young {center("S02-D CD40","PSLN-212(Y)","d3"):.1f}%; Tukey p={fp(cd40.tukey_p)}) and CD86+ DCs {cd86.mean_a:.1f}% vs {cd86.mean_b:.1f}% (young {center("S02-D CD86","PSLN-212(Y)","d3"):.1f}%). That is only 17–22% of the age gap [S02-D; A3], the weakest link in the mechanism.',
    '**CD8 effector and memory responses are about 60% restored.** Examples: IFN-γ+ CD8 at d60 is 9.9% vs 3.0% (young 14.4%), and lung TRM is 4.0% vs 1.0% (young 6.0%) [S05-G, S05-I; A3]. This matches the loss of protection by day 60.',
    f'**Boosting narrows the H1 gap.** After a day-14 boost, anti-CA09 IgG is {fnum(con("S13-I","PSLN-344 vs PSLN-212").mean_a)} vs {fnum(con("S13-I","PSLN-344 vs PSLN-212").mean_b)} (×{con("S13-I","PSLN-344 vs PSLN-212").est:.1f}, Tukey p={fp(con("S13-I","PSLN-344 vs PSLN-212").tukey_p)}) but remains ×{con("S13-J","PSLN-344 vs PSLN-212").est:.1f} for H3 [S13-I/J; A2].',
    '**The aged lung response is prolonged and TNF-rich, with or without Mn²⁺.** At 72 h, Ifnb1 is still 4.2-fold with PSLN-344 and 3.4-fold with PSLN-212, vs 1.5-fold in young animals (Tukey p<0.0001 and p=0.0006) [S01-A; A2]. At 16 h, Tnf is 40-fold with PSLN-344 vs 14-fold in young (Welch p=0.009; Tukey p=0.058) [S09-A]. At about 72 h, Il6 is 7.2-fold and Tnf 8.4-fold, vs 3.1-fold and 0.5-fold in young (n=3; timepoint mislabelled, DI-08) [S09-A panel 2]. Post-vaccination weight loss was minimal (Table D4), but this belongs on the safety watch-list for older recipients.'])

# =====================================================================================
PB(); H1('3. Data integrity: what the committee should hear from us first')
P(f'Before the committee decides, it should know that the workbook has defects that a careful reviewer will find. I ran systematic scans for exact and partial duplication (values, whole experiments, per-animal weight trajectories), checked derived values against their sources, and reconciled survival records against body-weight records [A1]. {len(LOG)} issues are logged (Appendix B). The {(LOG.Severity=="Critical").sum()} critical ones:')
crit = LOG[LOG.Severity == 'Critical']
TB(header=['ID', 'Blocks', 'Finding', 'Consequence for the case'],
   rows=[[r.ID, r.Blocks, r.Finding, r['Handling in this analysis']] for _, r in crit.iterrows()],
   widths=[.06, .14, .50, .30], font=6.9, caption='Table 3. Critical data-integrity findings [A1] (see Fig 8 for visual exhibits)')
CO([f'**Does the recommendation survive?** Yes. The PSLN-344 vs PSLN-212 conclusion rests on blocks with no duplication flags: 8 survival experiments and about 40 immune readouts. It also holds in every sensitivity analysis: dropping the conflicting S03-I gives HR {pool("Sens-1").cox_HR:.3f}, dropping S03-J gives HR {pool("Sens-2").cox_HR:.3f}, and adding the compromised cross-strain blocks gives HR {pool("Sens-4").cox_HR:.3f} [A5].',
    '**Claims we should not make until verified:** “protects against H5N1 when challenged 3 days after vaccination” (S06-D duplicate; S15-H/I copied weights); “works across mouse strains” (S15-L–O); “PSLN-344 is Th2-skewed” (an artefact of the rotated S03-B/F labels); any alveolar-macrophage or neutrophil kinetics (S11-A/B); “Mn²⁺ improves epithelial uptake” (S08-C contradicts S01-B). Rapid protection is still supported by the unflagged S03-J (day 2, 10/10 vs 3/10) and S06-B (day 3, 5/7 vs 0/7).',
    '**Recommended handling.** Disclose these findings to the committee proactively, with the Gate 0 audit plan. Where records cannot be reconciled, refer them to the standard research-integrity process; the patterns (copied trajectories with altered final values) are not explainable as transcription slips. This does not by itself imply misconduct, but it has to be resolved before the dataset supports an investment decision.'], '#fff4e5')

# =====================================================================================
PB(); H1('4. Mechanism of action, built from our data')
P('The data support a seven-step mechanism (Fig 6). The central idea is that **ageing blunts the lung\'s type I interferon response to the cyclic dinucleotide, and co-formulated Mn²⁺ restores it**. That unlocks an IFNAR- and GM-CSF-dependent monocyte-to-dendritic-cell program, which in turn drives dendritic-cell migration, T follicular helper and germinal-centre responses, Th1-type antibody, and CD8 effector and tissue-resident memory.')
FG('/tmp/outputs/figures/fig6_moa_schematic.png', 1.0, 'Fig 6. Proposed mechanism of action with supporting numbers and blocks. Dashed boxes = correlative or inferred steps that need confirmation (Gate 1B).')
mrows = []
def mrow(step, claim, ev, grade): mrows.append([step, claim, ev, grade])
m = MEC.set_index('question')
mrow('1 Delivery', 'Liposome reaches alveolar type II cells and alveolar macrophages',
     f"AECII 15.8% vs AECI 3.8% SRB+ (p<0.0001); liposome vs free dye 42× [S01-B]; AM uptake 43.1% WT vs 12.7% SP-A/D-KO (p<0.0001; young KO mice) [S01-C]", 'Direct (tracer, knockout in young mice)')
mrow('2 Sensing', 'Mn²⁺ raises the CDN-driven IFN-β response to the young level',
     f"16 h Ifnb1 36.9× vs 16.5× (GMR 2.23, 1.85–2.69; Tukey p=0.0006); young 37.5× [S01-A]; Hill-fit top 52× vs 16×, ED50 11 vs 10 µg [S08-A; A7]; encapsulation 55% vs 60% (n.s.) [S08-B]", 'Direct for IFN-β; STING dependence and Mn mechanism not tested')
mrow('3 Spread', 'Signal spreads between cells through gap junctions',
     f"Carbenoxolone: recruited monocytes 3.1% vs 7.3% (p=0.003) [S11-C]", 'Inferred (non-specific blocker)')
mrow('4 Myeloid', 'IFNAR + GM-CSF convert recruited monocytes into moDCs; CCR2-dependent',
     f"Gm-csf 8.5× vs 1.6× at 36 h [S02-F]; monocytes 30.6% vs 16.7% d4 [S01-D]; CCR2 antagonist 9.9% → 3.3% [S07-B]; IFNAR-KO BM moDC 2.1% vs 19.7%, GM-CSF rescue 12.4% [S02-H]; GM-CSF add-back to PSLN-212 5.9% → 13.8% [S02-G]", 'Direct (genetic + pharmacologic), partly in young mice')
mrow('5 DC', 'DCs mature, migrate (Gαi) and prime T cells',
     f"CCR7+ DC 30.7% vs 7.3%; antigen+ MLN DC 7.1% vs 1.8%; OT-I priming 18.7% vs 0.8% [S02-A/C/E]; pertussis toxin 30.9% → 6.8% in MLN [S05-C]; CD40/CD86 only ≈20% restored [S02-D]", 'Direct; co-stimulation gap remains')
mrow('6 Adaptive', 'Tfh/GC drive Th1-type antibody; CD8 effector and TRM',
     f"Tfh 10.3% vs 3.8%, Tfr 10.8% vs 26.7% [S04]; GC B 6.5% vs 2.3% [S03-K]; HAI ×8–9, IgG2a/IgG1 ×3.4–5.0 [S03, S13]; IFN-γ+ CD8 6.4% vs 1.5%, TRM 4.0% vs 1.0% [S05-F/I]; INCB3344 GZMB+ CD8 6.8% → 1.4% [S02-I]", 'Correlative (group level) + CCR2 intervention')
mrow('7 Outcome', 'Protection in aged mice', f"83% vs 12% survival, HR {PR.cox_HR:.3f} [A5]", 'Direct; no per-animal immune–outcome link')
TB(header=['Step', 'Claim', 'Evidence (aged PSLN-344 vs PSLN-212 unless stated)', 'Evidence grade'], rows=mrows, widths=[.09, .22, .50, .19], font=6.9,
   caption='Table 4. Mechanism claims and the strength of the supporting evidence [A2, A6, A7]')
P('**What the mechanism does not yet establish.** (i) No STING-deficient animals were tested, so on-target STING dependence is inferred. (ii) There is no Mn-only liposome. Mn²⁺ is itself a known innate stimulus (external context), so we cannot say how much of the benefit needs CDN-1807. The only molecule-level comparison favours CDN-1807 over cGAMP in the same vehicle: IFN-β 16.5× vs 7.7× (GMR 2.15, p=0.001) [S01-A; A2]. (iii) Several mechanistic interventions (S02-H, S02-I, S12-A) were done in young mice. (iv) Without Mn²⁺, aged lungs accumulate Ly6C+CCR2+ macrophages: 19.0 vs 3.4 ×10⁵ at day 5 (two-way ANOVA interaction p<0.0001) [S07-A; A12]. These may be the suppressive population, but the transfer experiment that would test this (S07-C) is uninterpretable because of duplicated labels (DI-10).')

# =====================================================================================
PB(); H1('5. Biomarkers to validate efficacy')
P('Each of the readouts below separates the protective regimens (aged PSLN-344, young PSLN-212) from the non-protective ones (aged Sham, aged PSLN-212) at the regimen level; at n=5 the per-animal AUC is 1.0 for nearly all of them [A10]. AUC therefore cannot rank them, so selection rests on three criteria: how close the marker is to the mechanism, whether it can be measured in people, and whether regulators accept it. Biomarkers and survival come from different animals, so these are regimen-level markers, not validated individual correlates of protection. Study 3C is designed to close that gap.')
brow = [
 ['PD (6–24 h)', 'Lung Ifnb1 16 h [S01-A]', 'Sham 0.94×; 212: 16.5×; 344: 36.9×; young 37.5×; CMP-204 7.7×. Protective ≥32.6×, non-protective ≤19.0×', 'Nasal-lining-fluid IFN-β/IFN-λ and CXCL10 (nasosorption); blood ISG score at 24 h', 'Phase 1 “young-equivalence” PD endpoint: the older-adult response should reach the young-adult response to the same dose'],
 ['PD (6–36 h)', 'Lung Ccl2 16 h and Gm-csf 36 h [S09-A†, S02-F]', 'Ccl2 590× vs 7.6× (GMR 77); Gm-csf 8.5× vs 1.6× (GMR 5.4)', 'Nasal CCL2; serum CCL2 and GM-CSF', 'Dose selection; confirms the Mn-specific arm of the mechanism'],
 ['Cellular (d3–7)', 'Ly6C+ monocytes d4, CCR7+ DC [S01-D, S02-A]', '30.6% vs 16.7%; 30.7% vs 7.3%', 'Blood monocyte IFN signature (e.g., SIGLEC1/CD169)', 'Exploratory'],
 ['Germinal centre (d7)', 'ICOS-high Tfh; Tfr; GC B [S04-A/B, S03-K]', 'Tfh 10.3% vs 3.8%; Tfr 10.8% vs 26.7%; GC B 6.5% vs 2.3%', 'Blood ICOS+PD-1+CXCR5+ cTfh and plasmablasts at d7; cTfr:cTfh ratio', 'Early read of adjuvant effect in Phase 1 (d7)'],
 ['Humoral (d14–28)', 'HAI; microneutralization; IgG2a/IgG1 [S03-C/G/D, S13-A–D]', 'HAI ×8.0 (CA09), ×9.2 (Aichi); neut ×9.2; IgG2a/IgG1 ×3.4', 'HAI GMT and seroconversion; MN; IgG subclasses', 'Primary immunogenicity endpoint (licensure surrogate); non-inferiority vs licensed comparator'],
 ['Mucosal (d14–28)', 'Not measured', 'Gap: no IgA data anywhere in the dataset', 'Nasal-wash secretory IgA', 'Must be added (Gates 1–2); the core rationale for intranasal delivery'],
 ['Cellular memory (d14–180)', 'IFN-γ+ CD8; TRM [S05-F/G/I, S14-A]', 'd14 6.4% vs 1.5%; d60 9.9% vs 3.0%; TRM 4.0% vs 1.0%', 'IFN-γ ELISpot to conserved NP/M1 peptides; nasal TRM (curettage, exploratory)', 'Supports the heterosubtypic (mismatch-season) claim'],
 ['Safety', 'CNS Ifnb1/Tnf/Isg15 36 h [S10-A]; weight [S08-D]; lung Il6/Tnf 72 h [S09-A†]', 'No CNS signal vs PBS (p≥0.54); weight nadir 96.4% vs 98.2%; Il6 7.2×, Tnf 8.4× at about 72 h', 'Olfactory testing (e.g., UPSIT), blood Mn, serum IL-6/CRP, facial-nerve AESI monitoring', 'Stopping rules in Phase 1'],
]
TB(header=['Tier', 'Mouse marker [block]', 'Our data (aged PSLN-344 vs PSLN-212 unless stated)', 'Human analogue', 'Proposed use'], rows=brow,
   widths=[.12, .19, .27, .22, .20], font=6.9, caption='Table 5. Biomarker plan [A2, A10] (PD = pharmacodynamic)', note='† S09-A shares its animals with S01-A (DI-08); its panel 2 is the ~72 h timepoint despite the 16 h label.')
P('**Go thresholds for the Gate 1 replication** are set deliberately below the observed effects to allow for regression to the mean: Ifnb1 16 h ratio ≥2 (observed 2.23, 95% CI 1.85–2.69) [S01-A]; Gm-csf 36 h ratio ≥3 (observed 5.36, 3.93–7.32) [S02-F]; HAI GMT ratio ≥4 (observed 8.0, 3.9–16.4) [S03-C]; IFN-γ+ CD8 d14 at least 2× PSLN-212 (observed 4.2×) [S05-F]; survival ≥70% and ≥40 points above PSLN-212 (observed 95% vs 14% at day 14) [A5].')

# =====================================================================================
PB(); H1('6. Next steps: a gated plan')
P('M0 is the committee decision. Timings are planning estimates. Aged (≥20-month) mice are the critical-path resource and must be ordered at M0.')
TB(header=['Gate', 'Study', 'Question it answers', 'Months', 'Decision at'],
   rows=[['0', 'Data verification and reconciliation', 'Are the primary data real and correctly labelled?', 'M0–M2', 'M2 (hard stop)'],
         ['1', '1A Confirmatory efficacy + attribution (aged, both sexes)', 'Does PSLN-344 beat PSLN-212 when blinded? Is CDN-1807 needed?', 'M1–M7', 'M7'],
         ['1', '1B Mechanism confirmation (STING, IFNAR, GM-CSF)', 'Is the MoA on-target? Are the PD biomarkers valid?', 'M2–M6', 'M7'],
         ['2', '2A Benchmark vs licensed enhanced vaccines (aged)', 'Is IN PSLN-344 differentiated vs IM high-dose/adjuvanted?', 'M7–M12', 'M12'],
         ['2', '2B Durability and boosting (aged)', 'Does protection last to d90–d180? Does a boost fix it?', 'M7–M15', 'M12 (interim), M15'],
         ['3', '3A Mn/CNS and intranasal safety (non-GLP → GLP)', 'Is intranasal Mn²⁺ safe? Where is the NOAEL?', 'M3–M15', 'M9 (pilot), M15'],
         ['3', '3B CMC, stability and delivery device', 'Can it be made, stored and delivered to the right airway tissue?', 'M0–M12', 'M12'],
         ['3', '3C Correlates of protection (embedded in 1A, 2A, 2B)', 'Which per-animal markers predict protection?', 'M1–M15', 'M15'],
         ['–', 'Phase 1/2a first-in-human (older adults)', 'Safe? Young-equivalent PD? Non-inferior HAI plus mucosal IgA?', 'IND ≈M18–24', '–']],
   widths=[.05, .33, .36, .12, .14], font=7.2, caption='Table 6. Gated development plan')

def card(title, items):
    H3(title)
    TB(header=['', ''], rows=[[f"**{k}**", v] for k, v in items], widths=[.17, .83], font=7.2, zebra=False, noheader=True)
FIELDS = ['Must establish', 'Population', 'Arms / comparators', 'Endpoints', 'Readouts & timing', 'Sample size', 'Go / no-go']
card('Gate 0: data verification and reconciliation (M0–M2)', [
 ('Must establish', 'That the primary survival and immunogenicity data are authentic, correctly labelled and complete before any further spend.'),
 ('Population', f'Not an animal study. Scope: all {len(LOG)} logged issues (Appendix B), DI-01 to DI-07 first. Collect notebooks, randomisation and cage cards, mortality logs, raw FACS (.fcs) and qPCR run files, and ELISA/HAI plate maps. Recover the real S06-D, S15-H/I and S15-L–O data or declare them lost. Re-gate S11-A/B from the raw files.'),
 ('Arms / comparators', 'Source records vs the workbook, cell by cell for the flagged blocks; an independent QA reviewer plus a statistician not involved in the original work.'),
 ('Endpoints', 'For each issue: resolved (record found and workbook corrected), explained, or unresolvable.'),
 ('Readouts & timing', 'Interim list at week 4; signed reconciliation memo and version-locked dataset at M2.'),
 ('Sample size', 'n/a'),
 ('Go / no-go', 'Go: source records substantiate the 8 primary survival experiments (S03-I, S03-J, S06-A/B/C, S06-E/F/G d60) and the d14 immunogenicity blocks (S03, S04, S05, S13, S14). No-go: two or more primary survival experiments cannot be substantiated, or duplication extends into primary blocks. Then stop, refer to research integrity, and fund nothing further until a clean re-run.')])
card('Gate 1A: confirmatory efficacy and attribution study (M1–M7)', [
 ('Must establish', 'That PSLN-344 beats PSLN-212 in aged mice under blinded, randomised, pre-registered conditions in both sexes; and whether the proprietary CDN-1807 is required or Mn²⁺ does the work.'),
 ('Population', 'Aged BALB/c 20–22 months, **female and male** (all existing data are female). Young 8–10-week reference. Aged C57BL/6 confirmatory arm set to re-establish strain generality (S15-L/M compromised).'),
 ('Arms / comparators', 'Single intranasal dose of bivalent inactivated vaccine (CA09 0.5 µg + Aichi 1 µg HA) with 20 µg adjuvant, as in S03: (1) vaccine + empty PSLN (Sham); (2) PSLN-212; (3) PSLN-344; (4) **Mn-PSLN without CDN-1807**; (5) **Mn-PSLN + cGAMP**; (6) young + PSLN-212; (7) aged, unvaccinated, unchallenged (background mortality). Coded vials; sex-stratified randomisation.'),
 ('Endpoints', 'Primary: survival for 14 d after 10× mLD50 CA09 challenge at d14, PSLN-344 vs PSLN-212 (log-rank stratified by sex). Key secondary: heterosubtypic cohort (Aichi vaccine → PR8 at d14) survival; HAI and MN GMT at d14; **nasal-wash and BAL IgA** (new); **lung viral titre at d3 and d5 post-challenge** (new; mortality alone cannot separate reduced replication from tolerance); weight nadir in survivors. PD satellites: lung Ifnb1 16 h, Gm-csf and Ccl2 36 h, CCR7+ DC 72 h.'),
 ('Readouts & timing', 'PD at M3–M4; HAI/IgA at M4; survival and viral load at M5–M6; final report and decision at M7.'),
 ('Sample size', f"24/arm for survival (12 F + 12 M): 90% power for 70% vs 20% (Fisher, α=0.05) [A11]. HAI needs ≥11/arm to detect a 2-fold difference (pooled SD log₂ HAI = 0.66) [A11]. PD satellites n=8/arm (Ifnb1 needs only 3/arm; SD log₂ = 0.17)."),
 ('Go / no-go', 'Go: PSLN-344 survival ≥70% and ≥40 points above PSLN-212 (lower 95% CI bound of the difference >0); HAI GMR ≥4; Ifnb1 ratio ≥2; effect in both sexes. Attribution rule: if Mn-only (arm 4) reaches ≥80% of PSLN-344 on HAI and survival, CDN-1807 is not needed: re-scope IP and CMC (a strategic pivot, not automatically a stop). If Mn + cGAMP (arm 5) matches PSLN-344, the moat is vehicle + Mn, not CDN-1807: freedom-to-operate review before Gate 2. No-go: PSLN-344 survival <50% or not different from PSLN-212.')])
card('Gate 1B: mechanism confirmation (M2–M6)', [
 ('Must establish', 'That the effect is on-target (STING-dependent) and that the IFNAR/GM-CSF axis, and therefore the proposed PD biomarkers, sits on the causal path.'),
 ('Population', 'Young Sting1-deficient, Ifnar1-deficient and wild-type mice. Aged wild-type mice given anti-IFNAR1 or anti-GM-CSF neutralising antibody or isotype control.'),
 ('Arms / comparators', 'PSLN-344 vs PSLN-212 within each genotype or treatment; wild-type and isotype controls as comparators.'),
 ('Endpoints', 'Lung Ifnb1 16 h, Gm-csf 36 h, moDC d3, antigen+ MLN DC 36 h, HAI d14.'),
 ('Readouts & timing', 'Innate readouts M3–M4; HAI M5; report M6.'),
 ('Sample size', 'n=8/arm (sufficient for ≥2-fold effects given observed SDs [A11]).'),
 ('Go / no-go', 'Go: ≥70% loss of PSLN-344 PD and HAI in STING-deficient mice; GM-CSF neutralisation reduces moDC and HAI in aged animals. If the effect is STING-independent, the MoA and biomarker plan must be rebuilt before Gate 2.')])
card('Gate 2A: benchmark against licensed enhanced vaccines for older adults (M7–M12)', [
 ('Must establish', 'That intranasal PSLN-344 is differentiated from what older adults already receive: non-inferior on HAI and better on mucosal or cross-protective immunity.'),
 ('Population', 'Aged BALB/c and C57BL/6, both sexes, 20–22 months.'),
 ('Arms / comparators', '(1) IN vaccine + PSLN-344; (2) IM standard-dose vaccine; (3) IM high-dose (4× HA); (4) IM vaccine + squalene oil-in-water emulsion (MF59-like); (5) IN vaccine alone; (6) IM vaccine + PSLN-344 (route control).'),
 ('Endpoints', 'Primary: HAI GMT at d28, non-inferiority of IN PSLN-344 vs the best IM comparator (margin 1.5-fold). Key secondary: nasal and BAL IgA; lung TRM; IFN-γ ELISpot (NP/M1); heterosubtypic challenge at d28 (survival and lung viral titre); drifted-strain challenge.'),
 ('Readouts & timing', 'Immunogenicity d28 at ≈M9; challenge outcomes ≈M10–M11; decision M12.'),
 ('Sample size', f"23/arm for 90% power on the HAI non-inferiority test (one-sided α=0.025) [A11]."),
 ('Go / no-go', 'Go: non-inferior HAI **and** superiority on at least one mucosal or cross-protection endpoint (IgA, TRM or heterosubtypic survival). No-go: an IM enhanced vaccine matches PSLN-344 on these endpoints; the product is then undifferentiated, so stop or reposition (e.g., pandemic H5 only).')])
card('Gate 2B: durability and boosting in aged mice (M7–M15)', [
 ('Must establish', 'Whether protection lasts to d90–d180 in aged animals, and whether a boost fixes the day-60 shortfall (67% vs 100% in young).'),
 ('Population', 'Aged BALB/c (plus C57BL/6), both sexes, 20 months at vaccination, with a young reference.'),
 ('Arms / comparators', 'PSLN-344 prime only; PSLN-344 prime + boost (d28 or d90); best IM comparator from 2A; young reference; background-mortality control (unvaccinated, unchallenged).'),
 ('Endpoints', 'Primary: HAI, MN and IgA kinetics (d14, 28, 60, 90, 180). Secondary: IFN-γ ELISpot and lung TRM at d60/180; heterosubtypic challenge at d90 and d180 (survival and viral load).'),
 ('Readouts & timing', 'd90 interim at ≈M11–M12; d180 and challenge outcomes at ≈M14–M15.'),
 ('Sample size', f"Immunogenicity n=12/arm. Challenge n=20–24/arm/timepoint; the observed day-60 gap (67% vs 100%) would need ≈42/arm to confirm (90% power) [A11], so immunogenicity is primary and survival secondary."),
 ('Go / no-go', 'Go: PSLN-344 (with or without a boost) gives ≥70% survival at d90 and HAI GMT ≥ comparator at d180. No-go: survival <50% at d90 even with a boost.')])
card('Gate 3A: Mn²⁺/CNS and intranasal safety (pilot M3–M9; GLP M9–M15)', [
 ('Must establish', 'That intranasal Mn²⁺ does not accumulate in, or injure, the olfactory bulb or brain, that local airway tolerance is acceptable, and a NOAEL with margin. Why: intranasal Mn²⁺ can travel along olfactory neurons to the brain, and intranasal vaccine adjuvants have a history of facial-nerve safety signals (both external context). Our only CNS data point is S10-A: no Ifnb1/Tnf/Isg15 rise at 36 h vs PBS (Tukey p=0.87/0.54/0.96) while cholera toxin rose (p≤0.0002) [A8]. Manganese itself was never measured.'),
 ('Population', 'Young and aged mice, both sexes; a second species (rat) for GLP repeat-dose; ferret or rabbit for nasal local tolerance.'),
 ('Arms / comparators', 'Vehicle; PSLN-212; PSLN-344 at 1×, 3× and 10× the efficacious dose; Mn-salt equivalent (positive Mn control); cholera toxin (positive CNS control, as in S10-A).'),
 ('Endpoints', 'Mn by ICP-MS in olfactory bulb, striatum, cerebellum and blood; MEMRI (T1); olfactory (buried-food) and motor (rotarod/open-field) tests; CNS Ifnb1/Tnf/Isg15 and microglial activation; nasal and lung histopathology; BAL cytokines at 16 h, 72 h and 7 d (S09-A watch item); serum IL-6/TNF/IFN-α; repeat-dose (n+1) GLP toxicology with recovery.'),
 ('Readouts & timing', 'Tissue Mn and CNS markers at 36 h, 1, 7 and 28 d; pilot report M9; GLP report M15.'),
 ('Sample size', 'Pilot n=6/sex/arm/timepoint; GLP per guideline.'),
 ('Go / no-go', 'Go: no brain Mn above vehicle beyond 7 d at ≤3× dose; no neurobehavioural change; no persistent nasal or lung pathology at 28 d; NOAEL ≥10× the planned human dose. No-go: dose-related brain Mn accumulation with neurobehavioural or histological change.')])
card('Gate 3B: CMC, stability and delivery (M0–M12)', [
 ('Must establish', 'That the product can be made to specification, stored, and delivered to the airway tissue the mechanism needs.'),
 ('Population', 'Product lots; a large-animal deposition model (ferret or NHP); nasal vs small-airway air–liquid-interface (ALI) cultures from donors ≥65 years.'),
 ('Arms / comparators', 'Nasal spray vs inhaled aerosol; PSLN-344 vs PSLN-212 (PD in ALI).'),
 ('Endpoints', 'Specifications: particle size/PDI, zeta potential, CDN-1807 encapsulation (current 54.8% ± 5.1 [S08-B]), Mn content and Mn:CDN ratio, endotoxin, sterility. No size, zeta or stability data are in the dataset although the methods are described. Stability: lyophilised (2.5% trehalose) at −20 °C and 2–8 °C. Delivery (critical): the mouse mechanism depends on **alveolar** targets (AECII and alveolar macrophages) [S01-B/C], but a human nasal spray deposits mostly in the upper airway (external context). So measure regional deposition of labelled liposomes, and PD (IFNB1, CCL2, CSF2) in nasal vs small-airway ALI.'),
 ('Readouts & timing', 'Release specifications M3; stability at 0, 3, 6 and 12 months (6-month read at ≈M8); deposition and ALI PD by M9; device decision M12.'),
 ('Sample size', '3 lots for stability; deposition n=4–6 animals per device.'),
 ('Go / no-go', 'Go: a device/formulation achieves target-tissue exposure and a young-equivalent PD response in the large-animal/ALI models, and the lyophilised product is stable for ≥6 months.')])
card('Gate 3C: correlates of protection (embedded in 1A, 2A, 2B)', [
 ('Must establish', 'Which per-animal markers predict protection, to set Phase 1 biomarker thresholds (today, biomarkers and outcomes come from different animals).'),
 ('Population', 'Every challenged animal in 1A, 2A and 2B.'),
 ('Arms / comparators', 'All arms pooled; protected vs unprotected animals.'),
 ('Endpoints', 'Pre-challenge HAI, MN, nasal IgA, 24 h blood ISG, T-cell ELISpot; outcomes are survival and lung viral load.'),
 ('Readouts & timing', 'Interim with 1A at M7; final with 2B at M15.'),
 ('Sample size', 'Accrues across studies (≥150 challenged animals).'),
 ('Go / no-go', 'Deliverable rather than gate: cross-validated thresholds (logistic and Cox models) for the Phase 1 PD and immunogenicity endpoints.')])
card('Phase 1/2a outline (after IND; about M18–24 onward)', [
 ('Must establish', 'Safety of intranasal Mn-containing adjuvant in older adults; a young-equivalent PD response; HAI non-inferior to a licensed enhanced vaccine with a mucosal IgA advantage.'),
 ('Population', 'Sentinel cohort of healthy adults 18–49, then adults 65–85 stratified 65–74 / 75–85. Exclude significant chronic lung disease, prior Bell\'s palsy or anosmia, neurodegenerative disease, and hepatic impairment (Mn clearance) initially.'),
 ('Arms / comparators', 'IN inactivated vaccine + PSLN-344 at 3 dose levels (fixed Mn:CDN ratio); IN vaccine alone; licensed IM enhanced vaccine for older adults (high-dose or adjuvanted) as active comparator.'),
 ('Endpoints', 'Safety: solicited nasal and systemic reactions d0–7, unsolicited events to d28, AESIs (Bell\'s palsy, olfactory change) to d180, blood Mn. PD: blood ISG score d1; nasal IFN/CXCL10/CCL2 d1. Immunogenicity: HAI GMT and seroconversion d28; nasal IgA; cTfh and plasmablasts d7; IFN-γ ELISpot d28/d180.'),
 ('Readouts & timing', 'Safety and PD by d7; immunogenicity d28; durability d180; about 12–15 months from first subject in.'),
 ('Sample size', 'To be set from the Gate 2 variance and margin (indicatively 30–50 per arm per age stratum for HAI precision).'),
 ('Go / no-go', 'Go to Phase 2b: acceptable safety; older-adult PD at least equal to the young-adult response; HAI non-inferior to the IM comparator under standard seasonal-influenza criteria (to be confirmed with Regulatory) with a mucosal IgA advantage.')])

# =====================================================================================
PB(); H1('7. Target demographic (for the market-research TAM check)')
P('The data define a clear boundary. **PSLN-344 adds value only where immunity is aged.** Young mice are fully protected by PSLN-212, PSLN-344 and CMP-204 alike [S09-B/D/F, S13-E]. Aged mice are protected only by PSLN-344 [Table 1]. The demographic should therefore be anchored on immunosenescence, not on general-population influenza vaccination.')
TB(header=['Segment', 'Definition for sizing', 'What our data support', 'Status'],
   rows=[['**Primary**', 'Adults ≥65 years eligible for annual seasonal influenza vaccination; positioned against IM enhanced vaccines (high-dose, adjuvanted, recombinant; external context) as a needle-free, mucosal, broader-protection option', '20-month mice: 83% vs 12% survival; heterosubtypic 76% vs 10% [A5]. External context, to be verified: 18–24-month mice are conventionally classed as “old” (≈ late 50s–60s in human years)', 'Core'],
         ['Priority sub-segment', 'Adults ≥75, frail adults and long-term-care residents (highest disease burden and weakest vaccine responses; external context)', 'The aged-mouse phenotype (blunted IFN-β, DC, Tfh) is the mechanistic target; durability is the open risk', 'Core, likely first label'],
         ['Adjacent (hypothesis)', 'Adults 50–64', 'At 14 months (middle-aged), PSLN-212 already fails (0/14 naive) while PSLN-344 protects (12/14) [S06-E/F imprint]. Needs clinical proof', 'TAM upside, not base case'],
         ['Pandemic preparedness', 'Government H5N1 (and other pandemic) stockpile procurement, adults including the elderly', 'Wild-type H5N1 10/10 vs 3/10 [S03-J]; heterosubtypic H5 protection from a seasonal vaccine 7/7 vs 2/7 [S06-C]', 'Option value; separate buyer'],
         ['Excluded for now', 'Children and adults <50; immunocompromised people or those on type I IFN/JAK-pathway blockade; severe chronic lung disease', 'No differentiation in young mice; the mechanism is IFNAR-dependent [S02-H]; lung-targeted STING agonism has not been safety-tested in diseased lungs', 'Not in TAM']],
   widths=[.14, .33, .38, .15], font=7.1, caption='Table 7. Target demographic and segments')
P('**Inputs the market-research team will need (not in our dataset):** population by age band (50–64, 65–74, ≥75) and geography; seasonal influenza vaccination coverage by age; current share and price of enhanced vaccines for older adults; acceptance of needle-free/intranasal delivery in older adults; prevalence of exclusion comorbidities (COPD and other chronic lung disease, immunosuppression); and pandemic stockpile procurement volumes and pricing.')

# =====================================================================================
H1('8. If we drop PSLN-344: what we give up, and what we don\'t')
H3('What we would give up')
NL([f'**The only formulation in our data that reliably protects aged animals:** 83% vs 12% survival over 8 experiments, HR {PR.cox_HR:.3f} [A5].',
    f'**A mechanistically explained “age fix”:** IFN-β restored to the young level (98% of the gap) and a median {100*medgap:.0f}% of the deficit closed across 40 readouts [S01-A; A3]. This is a differentiated story for the ≥65 segment.',
    f'**Breadth:** heterosubtypic protection of {het.surv_344} vs {het.surv_212}, including H5, plus wild-type H5N1 protection of 10/10 vs 3/10 [A5, S03-J]. This is pandemic-preparedness option value.',
    f'**Speed:** protection when challenged 2–3 days after one dose, {early.surv_344} vs {early.surv_212} [S03-J, S06-B; A5].',
    '**Mucosal T-cell memory from a needle-free product:** lung TRM 4.0% vs 1.0%; IFN-γ+ CD8 still 3.2× higher at d60 [S05-I, S05-G].',
    '**Dose-sparing within the formulation:** about 8 µg of PSLN-344 matches the IFN-β response of 40 µg PSLN-212, about 5× dose sparing [S08-A; A7]. No added biologic is needed; GM-CSF add-back would achieve something similar only with a second active [S02-G].'])
H3('What we would not give up')
BL(['**Nothing in young adults or the general population.** All adjuvants protect young mice, including the cGAMP comparator CMP-204 [S09, S13-E].',
    '**PSLN-212 has no standalone value in the target population**: 7/59 vs 1/59 survival vs Sham (p=0.061) [A4].',
    '**Downside is cappable.** Gates 0–1 are about 7 months and mostly internal; the expensive steps (GLP toxicology, CMC scale-up, device) start only after Gate 1.'])
P('**Bottom line.** Dropping now would trade a large, consistent, mechanistically coherent efficacy signal in exactly the population where current vaccines underperform, in exchange for avoiding a few months of verification work. I would not make that trade. I would stop the program without hesitation if Gate 0 fails.')

# =====================================================================================
PB(); H1('9. What I considered and ruled out')
TB(header=['Option considered', 'Evidence', 'Verdict'],
   rows=[['Take PSLN-212 forward (or both assets)', 'Aged: survival 7/59 vs Sham 1/59 (p=0.061); HAI GMT 46 vs 368 for PSLN-344 [A4, S03-C]. PSLN-344 is equal or better on every readout, with similar reactogenicity (nadir 97.0% vs 96.4%) [S08-D]', 'Ruled out: no scenario favours PSLN-212'],
         ['Dose up PSLN-212 instead of adding Mn²⁺', 'PSLN-212 IFN-β plateaus at ≈15× (40 µg), below PSLN-344 at 10 µg (21×); fitted tops 16× vs 52× [S08-A; A7]', 'Ruled out: ceiling, not potency'],
         ['Add the TLR7/8 agonist R848', f"PSLN-212/R848: IFN-β 24× (n.s. vs PSLN-344 37×) but Tnf ×{R848[(R848.measurand=='Tnf')&(R848.a=='PSLN-212/R848')].GMR.iloc[0]:.1f} and Il10 ×{R848[(R848.measurand=='Il10')&(R848.a=='PSLN-212/R848')].GMR.iloc[0]:.1f} vs PSLN-344; weight nadir 90.0% (p<0.001) with one animal unaccounted for [S01-A, S09-A, S08-D; A12]. PSLN-344/R848 lowers IFN-β about 30–36% vs PSLN-344 at 10–20 µg (p=0.018, 0.029) [S08-A]", 'Ruled out: less potent, more reactogenic'],
         ['Use cGAMP (CMP-204) instead of CDN-1807', 'Same vehicle: IFN-β 7.7× vs 16.5× (PSLN-212) and 36.9× (PSLN-344) [S01-A]; post-boost IgG 940 vs 4,411 (PSLN-212) [S13-I]; aged survival 3/7 vs 7/7 (PSLN-344) [S03-I]', 'Ruled out as the active (Mn + cGAMP is still tested in Gate 1A)'],
         ['PSLN-344 alone as antigen-free innate prophylaxis', 'S15-H: PSLN-344 without vaccine 0/7, vaccine alone 0/7 (block compromised, DI-02)', 'Ruled out; no claim of antigen-independent protection'],
         ['Young-adult / general-population indication', 'Young mice: PSLN-212(Y), PSLN-344(Y) and CMP-204(Y) all 100% [S09-B/D/F, S13-E]', 'Ruled out: no differentiation'],
         ['Co-administer GM-CSF (biologic) as the age fix', 'Works mechanistically: moDC-like cells 5.9% → 13.8% [S02-G]; but adds a second active and biologic CMC', 'Ruled out as a product; kept as a research tool'],
         ['Any CCR2-modulating combination', 'CCR2 blockade removes monocytes (9.9% → 3.3%) and GZMB+ CD8 (6.8% → 1.4%) [S07-B, S02-I]', 'Ruled out; flag CCR2 antagonists as a co-medication risk'],
         ['Go straight to IND-enabling work', 'Integrity defects; no attribution, benchmark or Mn-safety data; female-only', 'Ruled out: gate first'],
         ['Terminate the program now', 'Large, consistent efficacy signal in the target population; verification is cheap relative to the upside', 'Ruled out unless Gate 0 fails'],
         ['Claims resting on compromised blocks', 'S06-D duplicate; S15-H/I and S15-L–O copied weights; S03-B/F rotated labels; S11-A/B shared replicates; S08-C vs S01-B conflict', 'Excluded from the case (Section 3)']],
   widths=[.22, .56, .22], font=7.0, caption='Table 8. Alternatives considered')

# =====================================================================================
H1('10. Key risks and open questions')
TB(header=['Risk', 'Current evidence', 'Mitigation / gate'],
   rows=[['Data integrity', f'{(LOG.Severity=="Critical").sum()} critical and {(LOG.Severity!="Critical").sum()} other issues (Appendix B)', 'Gate 0 hard stop'],
         ['CDN-1807 not needed (Mn does the work), so IP is weaker', 'No Mn-only arm; CDN-1807 beats cGAMP in the same vehicle (IFN-β ×2.15) [S01-A]', 'Gate 1A arms 4–5; FTO review'],
         ['Intranasal Mn²⁺ neurotoxicity', 'No CNS inflammation at 36 h [S10-A]; Mn never measured', 'Gate 3A'],
         ['Mouse alveolar targeting does not translate to human nasal delivery', 'Mechanism relies on AECII and alveolar macrophages [S01-B/C]', 'Gate 3B deposition + ALI PD'],
         ['Not differentiated vs IM enhanced vaccines', 'No head-to-head data', 'Gate 2A'],
         ['Durability in the elderly', 'Day-60 survival 67% vs young 100% (p=0.009); antibody not followed past d28 in aged', 'Gate 2B (boost arm)'],
         ['Prolonged lung inflammation in aged recipients', 'Ifnb1 4.2× at 72 h vs 1.5× young [S01-A]; Tnf 40× vs 14× at 16 h [S09-A]; Il6 7.2×, Tnf 8.4× at ≈72 h (n=3; DI-08)', 'Gate 3A BAL time course; Phase 1 stopping rules'],
         ['Sex, strain and platform generality', 'Female BALB/c only in clean data; whole inactivated virus only', 'Gate 1A both sexes + C57BL/6; test split/recombinant HA in 2A'],
         ['Background mortality in aged colonies confounds survival endpoints', 'Untreated aged deaths 4/21 in 14 days [S06-E/G d60]', 'Background arm in every aged challenge; viral-load endpoint']],
   widths=[.27, .43, .30], font=7.1, caption='Table 9. Risk register')

# =====================================================================================
PB(); H1('Appendix A. Methods and analysis index')
BL(['**Data handling [A1].** All 15 sheets were parsed cell by cell into tidy tables that keep the source cell address (code/01_extract.py). Observation counts were compared with the annotation’s stated n. Integrity scans looked for identical vectors, whole-block duplicates, and per-animal weight trajectories shared across experiments, with dead-animal LOCF tails stripped. The chance per-day match rate between animals of different experiments was 0.88%, so ≥5 identical days cannot be coincidence. Derived blocks were recomputed from their sources (S03-B/F from S13-A–D; S04-B Tfh:Tfr from Foxp3; S09-A from S01-A).',
    '**Continuous endpoints [A2].** Stated methods: one-way ANOVA with Tukey HSD across all groups in a block (log₁₀ scale for titres and qPCR fold-changes, linear for %). Also Welch t and exact Mann–Whitney for key pairs. Effects are geometric-mean ratios or mean differences with Welch 95% CIs, plus Hedges’ g. HAI values below the 1:10 LOD were imputed at 5. Time courses used two-way ANOVA (group × time) [A12]. Multiplicity across the 40 curated readouts was handled with Holm correction (table multiplicity_holm).',
    '**Age-gap closure [A3].** (PSLN-344 − PSLN-212)/(PSLN-212(Y) − PSLN-212) on the analysis scale, with a percentile bootstrap (5,000 resamples) 95% CI. The curated set has 40 readouts, one pre-specified or peak timepoint each, excluding derived ratios and flagged blocks.',
    '**Survival [A4, A5].** Kaplan–Meier, pairwise log-rank (stated method), and Fisher exact on final status. Pooled analyses: Cox proportional hazards stratified by experiment (Efron ties; Breslow ties give HR 0.099, 95% CI 0.050–0.199, cross-checked in statsmodels from raw cells, code/16), plus the Mantel–Haenszel risk difference (Sato variance) and odds ratio. S06-D was excluded as a duplicate; one S03-J record without a day value was censored at day 21. Sensitivity sets are listed in the workbook.',
    '**Mechanistic interventions [A6]:** Student’s t (stated) with Mann–Whitney as sensitivity. **Dose–response [A7]:** 4-parameter Hill fits to S08-A with a within-dose bootstrap. **Safety [A8]:** S10-A reported as mean ± SD per the annotation, with ANOVA + Tukey; S08-D per-animal weight nadir with ANOVA + Tukey vs vaccine. **Weights vs survival [A9]:** deaths inferred from truncated or LOCF trajectories and reconciled with the survival blocks. **Biomarker screen [A10]:** regimen-level AUC and separation. **Sample sizes [A11]:** t-test power on observed log₂ SDs; simulated Fisher power for survival.',
    '**Software:** Python 3.11 (pandas, scipy, statsmodels, lifelines, matplotlib). All code is in /code, and all tables are in PSLN_analysis_workbook.xlsx.'])
H1('Appendix B. Full data-integrity log [A1]')
TB(header=['ID', 'Severity', 'Blocks', 'Finding', 'Handling'], rows=[[r.ID, r.Severity, r.Blocks, r.Finding, r['Handling in this analysis']] for _, r in LOG.iterrows()],
   widths=[.055, .075, .13, .47, .27], font=6.5)
PB(); H1('Appendix C. Figures')
FG('/tmp/outputs/figures/fig1_survival_overview.png', 1.0, 'Fig 1. Survival by experiment and pooled [A4, A5].')
FG('/tmp/outputs/figures/fig2_km_panels.png', 1.0, 'Fig 2. Kaplan–Meier curves for representative aged-mouse experiments [A4].')
FG('/tmp/outputs/figures/fig3_age_gap_closure.png', 0.82, 'Fig 3. Age-gap closure across 40 readouts [A3].')
FG('/tmp/outputs/figures/fig4_immunogenicity.png', 1.0, 'Fig 4. Immunogenicity in aged mice; Sham HAI values below LOD plotted at 5 [A2].')
FG('/tmp/outputs/figures/fig5_dose_response.png', 0.62, 'Fig 5. S08-A dose–response with Hill fits [A7].')
FG('/tmp/outputs/figures/fig7_safety.png', 1.0, 'Fig 7. CNS transcripts (S10-A) and post-vaccination weight (S08-D) [A8].')
FG('/tmp/outputs/figures/fig8_integrity_exhibits.png', 1.0, 'Fig 8. Visual exhibits for DI-01, DI-02, DI-04 and DI-06 [A1].')
PB(); H1('Appendix D. Supporting tables')
rows = []
for _, r in MEC.iterrows():
    rows.append([r.block, r.question, f"{fnum(r.mean_a)} vs {fnum(r.mean_b)}", f"{r.ratio:.2f}", fp(r.student_p), fp(r.mw_p)])
TB(header=['Block', 'Question', 'Mean a vs b', 'Ratio', 'Student t p', 'MW p'], rows=rows, widths=[.09, .50, .14, .07, .1, .1], font=6.8,
   caption='Table D1. Mechanistic interventions [A6] (groups a and b as named in the question; MW = exact Mann–Whitney)')
rows = [[r.measurand.replace(' (fold)', ''), r.group, f"{r['mean']:.2f} ± {r['sd']:.2f}", fp(r.tukey_p_vs_PBS)] for _, r in CNS.iterrows()]
TB(header=['CNS transcript (36 h)', 'Group', 'Mean ± SD (fold)', 'Tukey p vs PBS'], rows=rows, widths=[.3, .2, .3, .2], font=7.0, caption='Table D2. S10-A CNS inflammation [A8]')
rows = [[r.formulation, f"{r.top:.1f}", f"{r.Emax:.1f} ({r.Emax_lo:.1f}–{r.Emax_hi:.1f})", f"{r.ED50:.1f} ({r.ED50_lo:.1f}–{r.ED50_hi:.1f})", f"{r.mean_10ug:.1f}", f"{r.mean_20ug:.1f}", f"{r.mean_40ug:.1f}"] for _, r in DR.iterrows()]
TB(header=['Formulation', 'Fitted top (fold)', 'Emax (95% CI)', 'ED50 µg (95% CI)', 'Mean 10 µg', 'Mean 20 µg', 'Mean 40 µg'], rows=rows, widths=[.2, .12, .18, .18, .1, .1, .12], font=7.0, caption='Table D3. S08-A lung Ifnb1 dose–response [A7]')
rows = [[r.group, str(int(r.n)), f"{r.mean_nadir:.1f} ± {r.sd:.1f}", f"{r.min_nadir:.1f}", str(int(r.n_gt10pct_loss)), str(int(r.n_present_d10)), fp(r.tukey_p_vs_Vaccine)] for _, r in RG.iterrows()]
TB(header=['Group', 'n', 'Nadir % (mean ± SD)', 'Lowest', '>10% loss', 'Present d10', 'Tukey p vs vaccine'], rows=rows, widths=[.22, .06, .18, .1, .12, .12, .2], font=7.0, caption='Table D4. S08-D reactogenicity [A8]')
rows = [[r.analysis, r.surv_344, r.surv_212, f"{r.cox_HR:.3f} ({r.HR_lo:.3f}–{r.HR_hi:.3f})", f"{100*r.MH_RD_death:.0f} ({100*r.RD_lo:.0f} to {100*max(r.RD_hi,-1):.0f})"] for _, r in SPL.iterrows()]
TB(header=['Pooled analysis', 'PSLN-344 (or named arm)', 'PSLN-212 (or named arm)', 'Cox HR (95% CI)', 'MH risk diff. in death, pp'], rows=rows, widths=[.40, .14, .14, .17, .15], font=6.9, caption='Table D5. Pooled survival analyses and sensitivity sets [A5]',
   note='Sens-3 deliberately adds the duplicate S06-D to show that it would inflate apparent evidence without changing the estimate; it is not used. The middle-aged rows compare the named Naive/Imprinting arms.')
H1('Appendix E. Files delivered')
BL(['PSLN_portfolio_proposal.pdf: this document.',
    'PSLN_portfolio_proposal.docx and .md: editable versions with the same content.',
    'PSLN_analysis_workbook.xlsx: every statistic with source block and cell range (evidence register, integrity log, all analysis tables).',
    'figures/: Figs 1–8 (PNG).',
    'code/: the analysis pipeline (01_extract → 14_content), reproducible end to end from the two source files.'])

if __name__ == '__main__':
    from docmodel import to_pdf, to_markdown
    title = 'PSLN STING-agonist adjuvant program: portfolio-review proposal'
    subtitle = 'Recommendation, evidence, mechanism of action, biomarkers and gated next steps. Data as of 1 November 2026 (psln_program_dataset.xlsx; psln_program_annotation.pdf).'
    to_pdf(B, '/tmp/outputs/PSLN_portfolio_proposal.pdf', title, subtitle, 'PSLN program | portfolio review | prepared 1 Nov 2026 | confidential')
    md = to_markdown(B, title, subtitle).replace('/tmp/outputs/', '')
    open('/tmp/outputs/PSLN_portfolio_proposal.md', 'w').write(md)
    print('blocks:', len(B))
