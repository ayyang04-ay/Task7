# -*- coding: utf-8 -*-
"""Narrative content of the committee proposal. Every number carries an evidence (E#) or integrity (I-##) reference
that resolves to workbook cells in Appendix A/B. Numbers are copied from evidence_register.csv outputs."""

TITLE = "PSLN Program: CDN-1807 STING-agonist adjuvant (PSLN-212 / PSLN-344)"
SUBTITLE = "Portfolio review proposal: recommendation, evidence, mechanism, biomarkers, target population and gated next steps"
META = ("Prepared 1 November 2026. Sources: psln_program_dataset.xlsx (15 sheets; 108 data blocks; 6,120 data values; "
        "last modified 3 Sep 2026) and psln_program_annotation.pdf. Every number below carries a reference: "
        "E-numbers resolve to workbook cells and the statistical test in Appendix A, and I-numbers to the data-integrity register in Appendix B. "
        "The reproducible analysis (code, tidy data with cell provenance, all statistics) is provided alongside this document.")

S = []  # list of (kind, payload)
def H1(t): S.append(('h1', t))
def H2(t): S.append(('h2', t))
def P(t): S.append(('p', t))
def B(items): S.append(('bullets', items))
def CALL(t): S.append(('callout', t))
def TAB(header, rows, widths=None, size=7.6): S.append(('table', (header, rows, widths, size)))
def FIG(path, caption, width=17.0): S.append(('fig', (path, caption, width)))
def BR(): S.append(('pagebreak', None))

# =====================================================================================
H1("1. Recommendation")
CALL("<b>KEEP, BUT CONDITIONALLY AND ONLY AS PSLN-344</b> (CDN-1807 + Mn<super>2+</super> in the surfactant-biomimetic liposome), "
     "positioned as a mucosal adjuvant for influenza vaccines in older adults. <b>Do not fund IND-enabling work on the current data package.</b> "
     "Release money one gate at a time: <b>Gate 0</b> is data-integrity remediation; <b>Gate 1</b> is independent blinded confirmation plus Mn<super>2+</super> CNS safety and CMC. "
     "Terminate at the first failed gate. Discontinue PSLN-212 and all other variants now.")
P("<b>How the asset looks.</b>")
B([
 "<b>Biologically strong in the population that matters.</b> In aged mice, adding Mn<super>2+</super> turns a failing adjuvant into a protective one. "
 "Across 9 lethal influenza-challenge experiments, survival was 81% (51/63) with PSLN-344, 13% (8/63) with the same CDN without Mn<super>2+</super> (PSLN-212) and 0% (0/63) with vehicle. "
 "The risk difference versus PSLN-212 is +68 points (95% CI 56 to 79) [E1, E2]. "
 "The effect holds in the experiments with no integrity flag (75% vs 7%) [E4]. "
 "It is present 3 days after a single dose [E5], lasts to day 60 (67% vs 5%) [E8], "
 "and is seen in three mouse strains [E9] and in influenza-experienced animals [E10]. "
 "A mechanism tested by perturbation explains it: Mn<super>2+</super> restores the aged lung's interferon-β response to the STING agonist to the young level [E13], and this drives GM-CSF, monocyte-derived dendritic cells, germinal centres and cross-reactive CD8 T cells [E17 to E45].",
 "<b>Not decision-grade as a data package.</b> Values are duplicated across independent experiments: 22 body-weight group pairs match far beyond chance (p as low as 10<super>-74</super>), "
 "and an alveolar-macrophage dataset shares 35 of 100 per-animal values with a neutrophil dataset (p about 10<super>-79</super>). "
 "Several blocks are mislabelled, and one mislabel reverses a mechanistic conclusion [I-01 to I-08]. This would not survive partner due diligence or a regulatory audit.",
 "<b>Translationally unproven on four points.</b> (1) There is no comparison with a licensed older-adult vaccine or adjuvant, so differentiation versus standard of care is unknown. "
 "(2) Mn<super>2+</super> CNS safety rests on a single 36-hour transcript panel [E48]. "
 "(3) The vehicle targets alveolar cells through surfactant proteins [E46, E47], which implies an inhaled product. "
 "(4) Basic CMC is undefined: Mn<super>2+</super> content, the meaning of the dose, and encapsulation of 55% [E50, I-21].",
])
P("<b>Why keep rather than drop.</b> The effect is large and consistent: PSLN-344 beat vehicle in 9/9 experiments and PSLN-212 in 8/9 [E54]. "
  "It survives restriction to Tier-A data [E4], is mechanistically coherent, and targets the population with the greatest unmet need. "
  "Verifying it (Gates 0 and 1) costs a fraction of IND-enabling work. If Gate 0 fails, the program can be stopped at that point with no further spend, and Section 9 lists exactly what that forgoes.")
P("<b>Discontinue now (no further spend).</b> "
  "PSLN-212 as a candidate: it fails in aged mice and has no advantage in young mice, where every formulation protects [E1, E11, E54]. "
  "Also stop the R848 combinations [E51], the cGAMP payload CMP-204 [E52] and antigen-free standalone use [E6]. "
  "Keep PSLN-212 only as a comparator arm.")
P("<b>Decisions requested today.</b> "
  "(1) Approve Gate 0 and Gate 1 only, with the pass and kill criteria in Section 2. "
  "(2) Refer integrity findings I-01 to I-08 to QA / research integrity; this step is independent of the portfolio decision. "
  "(3) Ask Market Research to size the segments defined in Section 3.")

P("<b>Scorecard</b> (qualitative; each rating is justified by the cited evidence):")
TAB(["Dimension", "Rating", "Basis"], [
 ["Efficacy in aged mice (PSLN-344)", "Strong", "Large, consistent survival benefit; robust to excluding flagged experiments [E1, E4, E54]"],
 ["Breadth, onset, durability", "Good; durability is the weak point", "3 subtypes, protection by day 3, 67% at day 60 vs 100% young [E5, E8]"],
 ["Mechanism", "Coherent, partly causal", "Perturbation-tested steps (CCR2, gap junctions, IFNAR/GM-CSF, pertussis toxin); STING-dependence untested [Section 4]"],
 ["Data integrity", "FAILS today", "Critical duplications and mislabels [I-01 to I-08]; must be fixed from source"],
 ["Safety", "Largely unknown", "Mild reactogenicity; CNS panel reassuring but minimal; no Mn<super>2+</super> biodistribution or toxicology [E48, E49]"],
 ["Differentiation vs standard of care", "Unknown", "No licensed-comparator arm anywhere in the package"],
 ["CMC / product definition", "Undefined", "Mn<super>2+</super> content and dose basis not stated; encapsulation 55% by A260 [E50, I-21]"],
 ["Fit to unmet need", "High (older adults, pandemic)", "Benefit is specific to aged hosts [E11]; rapid single-dose protection [E5 to E7]"],
], widths=[4.4, 3.6, 8.7], size=7.4)

# =====================================================================================
H1("2. Next steps: what each study must establish, and the endpoints we need to see")
FIG("fig7_gated_plan.png", "", 17.0)
P("All thresholds below are proposals anchored to our observed effects. They should be frozen in a pre-registered statistical analysis plan before any study starts. "
  "In-life durations are taken from the designs already used in the dataset (e.g. S06-A: vaccinate, challenge at day 14, observe 14 days, which is 28 days in-life). "
  "Calendar time and cost must come from Operations; aged (≥20-month) cohorts have a procurement lead time.")
TAB(["Study", "Must establish", "Design (key features)", "Primary endpoint and GO criterion", "Secondary endpoints", "KILL if"], [
 ["G0. Source-data verification (Gate 0)", "That recorded outcomes happened as recorded",
  "Independent QA audit of vivarium mortality/euthanasia logs, raw weights, FCS, qPCR and ELISA files for all survival blocks and all Tier B/C blocks. No animals",
  "100% of survival records in the 18 labelled survival blocks (plus the unlabelled S08 region) traced to contemporaneous records. I-01 to I-08 root-caused and corrected from raw data or retracted",
  "Dose defined (µg CDN-1807); Mn<super>2+</super> per dose; S15-L/N challenge conditions; cause of 19% background mortality [I-14]",
  "Survival not traceable, or evidence values were not generated as recorded"],
 ["S1. Independent blinded confirmation (Gate 1, the decision study)", "The Mn<super>2+</super> effect is real, reproducible elsewhere, and differentiated versus standard of care",
  "Independent lab; randomised and blinded; aged BALB/c and C57BL/6, both sexes. Arms: vehicle, PSLN-212, PSLN-344, Mn<super>2+</super>-only, licensed benchmark (chosen with Clinical), young reference. "
  "Heterosubtypic challenge at day 14 (28 days in-life). n=25/arm gives 80% power if the true difference is 40 pts rather than the observed 68; n=12 gives 93% at the observed effect [E56]",
  "14-day survival. GO: PSLN-344 minus PSLN-212 ≥40 pts with 95% CI excluding 0 (observed +68, CI 56 to 79 [E1]); same direction in each strain and sex; Mn<super>2+</super>-only no better than PSLN-212; PSLN-344 not inferior to benchmark (margin pre-set)",
  "Lung viral titre day 3/5 (absent today); weight-loss AUC with a pre-set humane-endpoint rule and no carry-forward; HAI/MN at day 14; NP/M1 IFN-γ+ CD8; 16-h ISG",
  "Difference <40 pts or CI includes 0; benchmark clearly superior; Mn<super>2+</super>-only reproduces the effect"],
 ["S2. Mn<super>2+</super> biodistribution and CNS safety (Gate 1)", "Intranasal Mn<super>2+</super> does not accumulate in, or inflame, the CNS",
  "Aged mice; PSLN-344, PSLN-212, vehicle, Mn<super>2+</super>-only; single dose and prime-boost (days 0 and 14 as in S13-I/J); cholera toxin positive control; 16 h to day 28",
  "Brain and olfactory-bulb Mn (ICP-MS) not above vehicle beyond a margin set with Toxicology. CNS Ifnb1/Tnf/Isg15 <2-fold vs vehicle at every time and below cholera toxin (today 1.16 to 1.57x vs 2.7 to 5.5x at 36 h [E48])",
  "Histopathology of olfactory epithelium, bulb and brain; olfaction and neurobehaviour; lung Mn clearance",
  "Dose-related CNS Mn accumulation, or inflammation approaching cholera toxin"],
 ["S3. CMC characterisation (Gate 1)", "PSLN-344 is a defined, reproducible product",
  "At least 3 batches; orthogonal assays", "Encapsulation by HPLC/LC-MS (A260 today 54.8% ± 5.1 [E50]); Mn:CDN ratio; free Mn<super>2+</super>; size/PDI/zeta; lyophilised stability",
  "TEM morphology; endotoxin; batch consistency", "Specifications not reproducibly met"],
 ["S4. Dose-ranging and reactogenicity (Gate 2)", "The lowest effective dose and the tolerability window",
  "Aged mice at 5, 10 and 20 µg (10 µg already exceeds the PSLN-212 maximum on Ifnb1 [E14])",
  "Survival non-inferior to 20 µg (margin pre-set), with mean weight-nadir loss ≤5% (today 3.6% [E49])",
  "BAL cells and protein; lung histopathology; lung Il6/Tnf [E16]", "No dose meets both criteria"],
 ["S5. Per-animal correlates of protection (Gate 2)", "Which non-terminal biomarker predicts survival",
  "Sample each animal before challenge: 16-h nasal/serum ISG, CCL2, GM-CSF; day-7 blood Tfh; day-14 HAI/MN, nasal IgA, NP/M1 ELISpot. Dose titration creates a range of protection",
  "At least one non-terminal biomarker with ROC AUC ≥0.80 for survival (proposed), which becomes the Phase 1 efficacy biomarker",
  "Multivariable model; thresholds", "No biomarker reaches AUC ≥0.70 (no usable Phase 1 efficacy biomarker)"],
 ["S6. Durability and boost in aged mice (Gate 2)", "Protection lasts in the elderly",
  "Prime vs prime-boost; challenge at days 60, 90 and 180 (180 + 14 days in-life, as in S09-F)",
  "≥80% survival at day 60 with the chosen regimen (today 67% after a single dose [E8])",
  "IFN-γ+ CD8 and TRM maintenance; titres [E40, E42, E43]", "Below 60% at day 60 even with a boost"],
 ["S7. Second species and human-relevant delivery (Gate 2)", "Effect translates beyond mice, with a human-relevant device",
  "Ferrets (aged if available) with intranasal or aerosol delivery; nasal vs lung deposition study",
  "Reduced viral shedding and disease after heterosubtypic challenge vs vaccine alone and vs PSLN-212",
  "HAI/MN, nasal IgA, ISG/GM-CSF bridging; local tolerability", "No benefit over vaccine alone"],
 ["S8. Mechanism closure (Gate 2, parallel)", "Causality for the claims in Section 4",
  "STING-deficient aged mice ± PSLN-344; uptake of PSLN-344 vs PSLN-212 by macrophages vs epithelium; CD8 depletion / TRM blockade before challenge; S07-C repeated with correct labels; macrophage and neutrophil kinetics re-measured",
  "Protection lost without STING; CD8 dependence quantified", "Costimulation-enhancing variants (CD40 gap [E29])",
  "Effect is STING-independent AND Mn<super>2+</super>-only protects (re-scope to an Mn adjuvant)"],
], widths=[2.3, 2.4, 3.7, 3.6, 2.6, 2.1], size=6.5)
P("<b>After Gate 2:</b> route-matched GLP repeat-dose toxicology in two species, CNS safety pharmacology, a GMP process, and antigen partnering, leading to IND.")

# =====================================================================================
H1("3. Target demographic (for Market Research TAM sizing)")
TAB(["Segment", "Why (our data)", "Status", "What Market Research should size"], [
 ["PRIMARY: older adults receiving seasonal influenza vaccine (the ≥65 segment is the conventional older-adult definition; external convention)",
  "Benefit is specific to aged hosts [E1, E11]; cross-strain protection [E1]; unaffected by prior exposure [E10]; seen in 3 strains [E9]",
  "Supported pre-clinically (mouse only)",
  "Older-adult population x vaccination coverage x share of 'enhanced' older-adult vaccines. Price premium requires the benchmark comparison (Gate 1)"],
 ["SECONDARY: pandemic preparedness (H5N1 and other novel subtypes), older-adult priority groups",
  "Single dose protects when challenge comes 2 to 3 days later [E5, E6]; wild-type H5N1 10/10 [E7]",
  "Supported pre-clinically (E7 is Tier B)",
  "Government stockpile and rapid-response procurement; dose-sparing [E14] matters for stockpile economics"],
 ["EXPLORATORY (no data): long-term-care residents; adults with chronic lung disease; immunocompromised adults",
  "Outbreak use is inferred from rapid onset [E5]. Caution for lung disease: uptake depends on surfactant proteins [E46]",
  "Not studied", "Size only as upside; needs dedicated studies"],
 ["NOT A TARGET: young and healthy adults; antigen-free prophylaxis",
  "No differentiation in young animals [E11]; no protection without antigen [E6]", "Ruled out", "Do not include in TAM"],
], widths=[4.2, 5.0, 2.6, 4.9], size=7.1)
P("<b>Product attributes that change TAM assumptions:</b>")
B([
 "<b>Mucosal (intranasal or inhaled) administration.</b> The vehicle's alveolar targeting [E46, E47] makes device development probable.",
 "<b>The adjuvant needs an antigen partner</b> [E6].",
 "<b>Possible dose-sparing</b> [E14].",
 "<b>A booster may be needed in the elderly for durability</b> [E8, E40].",
])
P("<b>Caveat.</b> \"Aged\" means female mice aged 20 months or more. Mapping this to a specific human age band is an assumption.")

# =====================================================================================
H1("4. Mechanism of action, built from our data")
P("Unless noted, comparisons are aged PSLN-344 versus aged PSLN-212, i.e. the contribution of Mn<super>2+</super>. "
  "<i>Established</i> means supported by a perturbation (knockout, antagonist, blocker or rescue). "
  "<i>Associated</i> means a consistent correlation without causal test. <i>Gap</i> means not shown.")
TAB(["Step", "What our data show", "Ref", "Status"], [
 ["1. Delivery", "Alveolar-macrophage uptake depends on surfactant proteins A/D: 43.1% vs 12.7% in knockouts. Liposomes reach epithelial cells (15.8% vs 0.38% for free dye). Mn<super>2+</super> cuts epithelial uptake about 4-fold (3.8% vs 15.8%)", "E46, E47", "Established for the vehicle. Gap: which cell PSLN-344 acts through"],
 ["2. STING → IFN-β (target engagement)", "Lung Ifnb1 2.2x higher at 16 h (36.9- vs 16.5-fold), equal to young (37.5). Dose-dependent; ≥4x dose-sparing. Transient: by 72 h 4.2- vs 3.4-fold, no longer different", "E13 to E15", "Established as a readout. Gap: no STING-knockout or Mn<super>2+</super>-only arm"],
 ["3. Innate amplification", "Ccl2 77x, Ccl3 27x, Ccl5 7.6x, Il6 6.5x at 16 h. Gm-csf 4.2 to 5.4x at 16 to 36 h. Monocyte recruitment needs gap junctions (carbenoxolone: 7.3% → 3.1%)", "E16, E17, E20", "Established (carbenoxolone)"],
 ["4. Monocyte recruitment", "Lung monocytes 30.6% vs 16.7% at day 4; CCR2 antagonist 9.9% → 3.3%. IFNAR dependence of recruitment NOT shown (p=0.12, n=3)", "E18, E19, E21", "Established via CCR2; IFNAR link is a gap"],
 ["5. Monocyte fate: DC, not macrophage", "moDC formation needs IFNAR (2.1% vs 19.7%) and is rescued by GM-CSF (12.4%). GM-CSF converts the PSLN-212 response (13.8% vs 5.9%). Without Mn<super>2+</super>, Ly6C+CCR2+ macrophages accumulate instead (19.0 vs 3.4 x10<super>5</super>)", "E22 to E24", "Established (knockout and rescue)"],
 ["6. DC migration and priming", "CD11b+ DC 18.9% vs 8.3%; cDC1 37.5% vs 22.8%; CCR7+ migratory DC 30.7% vs 7.3%; antigen-positive DC in lymph node 7.1% vs 1.8% (blocked by pertussis toxin); OT-I priming 18.7% vs 0.8%. Costimulation only partly restored: CD40 11.2% vs 5.6%, young 38.7%", "E25 to E30, E45", "Established (pertussis toxin in S05-C; the PTX arm's adjuvant is unstated in S02-C/E). Costimulation is the residual gap"],
 ["7. Germinal centre and regulation", "Tfh 10.3% vs 3.8%; Tfr 10.8% vs 26.7%; GC B cells 6.5% vs 2.3%; lung Treg 3.0% vs 6.7%; CD206+ macrophages 48.9% vs 71.5%", "E31 to E34", "Associated. Macrophage → Treg causality unreadable (I-05)"],
 ["8. Antibodies", "CA09 IgG 18.6x, HAI 8.0x, neutralising 9.2x; Aichi similar. Th1-skewed: IgG2a/IgG1 1.85 vs 0.54", "E35 to E39", "Readout"],
 ["9. Cross-reactive CD8 and TRM", "IFN-γ+ CD8 6.4% vs 1.5% (day 14) and 9.9% vs 3.0% (day 60); lung TRM 4.0% vs 1.0%; CCR2-dependent (shown in young mice)", "E42, E43, E45", "Associated. Causal role untested (no depletion)"],
 ["10. Protection", "Heterosubtypic survival 81% vs 13%; rapid onset, durable to day 60, seen in 3 strains", "E1 to E10", "Outcome"],
], widths=[3.0, 8.6, 2.0, 3.1], size=7.1)
FIG("fig3_restoration_cascade.png", "", 14.5)
P("<b>The key mechanistic insight is where Mn<super>2+</super> stops helping.</b> "
  "Fig. 3 scores each step against the young benchmark. The restoration index (RI) is 0 for no gain over PSLN-212 in aged mice and 1 for a full match to young. "
  "Mn<super>2+</super> fully restores the innate trigger (Ifnb1 RI 0.98) and most myeloid and DC trafficking (RI 0.70 to 0.89). "
  "It does <b>not</b> restore DC costimulation (CD40 RI 0.17; CD86 RI 0.22) [E29] or CD8 effector and memory quality (GZMB RI 0.41; TRM RI 0.59) [E41, E43]. "
  "This matches the residual survival gap, which is largest at day 60 [E3, E8]. Three implications follow:")
B([
 "durability is the efficacy risk to test first;",
 "DC maturation is the lever for a next-generation formulation;",
 "costimulation and CD8 quality, not IFN induction, are the biomarkers most likely to limit response in older humans.",
])
FIG("fig4_dose_ifnb1.png", "", 16.0)
P("<b>Mechanistic gaps to close</b> (Study 8):")
B([
 "The effect has not been shown to be STING-dependent: there is no STING-knockout arm and no Mn<super>2+</super>-only arm.",
 "Which lung cell takes up PSLN-344 is unknown.",
 "Whether CD8/TRM cells cause protection is untested.",
 "The macrophage → Treg link cannot be read (I-05).",
 "Alveolar-macrophage and neutrophil kinetics are unusable (I-02).",
])

# =====================================================================================
H1("5. Biomarkers to validate efficacy")
TAB(["Biomarker (timing)", "Mouse evidence, PSLN-344 vs PSLN-212 (aged)", "Role", "Proposed human analogue (to validate)"], [
 ["Lung Ifnb1 / ISG (16 h)", "36.9- vs 16.5-fold (2.2x); RI 0.98; dose-responsive [E13, E14]", "Target engagement; dose selection", "Blood or nasal-wash ISG score; IFN-β / CXCL10"],
 ["Gm-csf (16 to 36 h)", "4.2x at 16 h; 5.4x at 36 h. Largest standardised effect of the 76 readouts ranked (Hedges g 7.9) [E17, E55]", "Mn<super>2+</super>-specific pharmacodynamics (DC licensing)", "Nasal-wash / serum GM-CSF"],
 ["Ccl2 (16 h)", "77x [E16]", "Innate amplification", "Nasal / serum CCL2 (MCP-1)"],
 ["Monocyte → moDC; CCR7+ DC (day 3 to 4)", "30.6% vs 16.7%; 30.7% vs 7.3% [E18, E27]", "Mechanism (animal studies only)", "n/a (BAL in animals)"],
 ["Tfh ICOS-hi / Tfr (day 7)", "10.3% vs 3.8%; 10.8% vs 26.7% [E31, E32]", "Early adaptive predictor", "Circulating Tfh (ICOS+PD-1+CXCR5+) at day 7"],
 ["HAI / neutralising titre (day 14)", "8.0x and 9.2x (CA09); 9.2x (Aichi) [E36 to E38]", "Registrational immunogenicity (strain-matched)", "Standard HAI / microneutralisation"],
 ["IgG2a/IgG1 (day 14)", "1.85 vs 0.54 (CA09); 2.30 vs 0.46 (Aichi) [E39]", "Response quality (Th1)", "IgG-subclass profile (mapping to define)"],
 ["Cross-reactive IFN-γ+ CD8 (days 14 and 60)", "6.4% vs 1.5%; 9.9% vs 3.0% [E42]", "Heterosubtypic protection and durability", "PBMC IFN-γ ELISpot to conserved NP/M1 peptides"],
 ["Lung TRM CD8 (day 25)", "4.0% vs 1.0%; RI 0.59 [E43]", "Durability", "n/a (animal)"],
 ["Safety: CNS Ifnb1/Tnf/Isg15; weight nadir; lung Il6/Tnf", "CNS 1.16 to 1.57x PBS vs cholera toxin 2.7 to 5.5x; nadir 96.4% vs 98.2% vaccine-only; lung Il6 6.5x [E48, E49, E16]", "Safety / reactogenicity", "Olfactory/neurological monitoring; solicited reactogenicity"],
], widths=[3.3, 5.6, 3.4, 4.4], size=7.1)
P("<b>Which biomarker predicts protection is not yet known.</b> The principal readouts (Fig. 3) rank the groups in the same order (vehicle < PSLN-212 < PSLN-344 ≤ young; inverted for Tfr and Treg), "
  "and immune readouts and survival were measured in different animals. No per-animal correlate of protection can be estimated from this package, so Study 5 is designed to produce one. "
  "HAI alone is unlikely to be enough for the older-adult cross-strain claim, for two reasons. Most protection data involve strain-mismatched challenge, which HAI does not measure. "
  "And in S03-I (Tier B), aged PSLN-212 mice all died after homologous challenge (0/7), although the same regimen gave a HAI GMT of 46 in a parallel cohort (S03-C) [E12, E36].")

# =====================================================================================
H1("6. Evidence base (1): the asset as tested")
B([
 "<b>Active drug.</b> CDN-1807, a cyclic-dinucleotide STING agonist.",
 "<b>Vehicle.</b> A pulmonary-surfactant-biomimetic liposome (DPPC, DPPG, DPPE-PEG2000, cholesterol).",
 "<b>Two versions.</b> PSLN-212 is drug plus vehicle. PSLN-344 additionally incorporates Mn<super>2+</super> by coordination polymerisation.",
 "<b>Comparators.</b> CMP-204 (cGAMP in the same vehicle, a prior-art analogue); R848 variants; empty-vehicle Sham.",
 "<b>It is an adjuvant, not a stand-alone drug.</b> Every efficacy experiment co-administers it intranasally with an inactivated influenza vaccine (20 µg adjuvant per mouse). "
 "Given without antigen, PSLN-344 gave 0/7 survival, versus 6/7 with antigen [E6]. Commercially this means an antigen partner or our own adjuvanted vaccine.",
 "<b>The vehicle is appropriate as a vehicle.</b> It is inert: lung Ifnb1 0.94-fold; no CNS signal versus PBS (all p≥0.16); 0/63 survival in aged mice [E53].",
 "<b>Study population.</b> \"Aged\" means female BALB/c mice aged 20 months or more unless stated; \"young\" means 7 to 8 weeks. Only female mice were used.",
])

# =====================================================================================
H1("7. Evidence base (2): efficacy, what the data show")
TAB(["Question", "Result (aged mice unless stated)", "Ref", "Tier"], [
 ["Does Mn<super>2+</super> make the asset work in aged animals?", "Survival 81% (51/63) PSLN-344 vs 13% (8/63) PSLN-212 vs 0% (0/63) vehicle. Risk difference +68 pts (95% CI 56 to 79); stratified log-rank p=1.6e-16", "E1, E2", "A/B"],
 ["Is it robust to the integrity findings?", "Tier-A experiments only: 75% (21/28) vs 7% (2/28); +68 pts (95% CI 50 to 86); p=4.6e-09", "E4", "A"],
 ["Is it consistent across experiments?", "Beats vehicle in 9/9 and PSLN-212 in 8/9 (log-rank p<0.05). PSLN-212 never significantly raised end-of-study survival over vehicle (Fisher p≥0.46)", "E54", "A/B"],
 ["How fast?", "Challenge 3 days after a single dose: 86% (12/14) vs 14% (2/14) vs 0/14. Vaccine + PSLN-344 6/7 vs vaccine alone 0/7. Wild-type VN04 H5N1 at day 2: 10/10 vs 3/10 vs 1/10", "E5, E6, E7", "A/B, B, B"],
 ["How durable?", "Challenge at day 60: 67% (14/21) vs 5% (1/21); young benchmark 21/21. At day 14: 93% (13/14)", "E8", "A/B"],
 ["How broad?", "Protection across H3→H1 (PR8), H1+H3→H5 (rgH5N1) and H1→H3 (Perth) (Fig. 1)", "E1", "A/B"],
 ["Other genetic backgrounds?", "C57BL/6: 6/7 vs 0/7 vs 0/7. Swiss Webster: 6/7 vs 2/7 vs 0/7 (challenge details not recorded)", "E9", "B"],
 ["Prior influenza exposure?", "14-month mice: PSLN-344 6/7 in both naive and imprinted animals, in both challenges. PSLN-212 0/7 to 4/7", "E10", "B"],
 ["Does it match young animals?", "No. 81% vs 98% for young PSLN-212 (−17.5 pts, 95% CI −27 to −8); the gap is largest at day 60", "E3, E8", "A/B"],
 ["Any benefit in young animals?", "None measurable. PSLN-344, PSLN-212 and cGAMP all protect 100% (S09-B/D/F, S13-E)", "E11", "A/B"],
 ["Any internal inconsistency?", "S03-I: PSLN-212 (0/7) did worse than cGAMP (3/7) despite higher titres. The paired weights contradict S03-I", "E12, I-07", "B"],
], widths=[3.6, 9.6, 2.0, 1.5])
FIG("fig1_survival_aged.png", "", 16.5)
FIG("fig2_km_tierA.png", "", 17.0)
P("<b>Interpretation.</b>")
B([
 "<b>Mn<super>2+</super> is what makes the asset work in older hosts.</b> Without Mn<super>2+</super>, CDN-1807 delays death in some experiments but does not improve survival [E54].",
 "<b>The commercial case rests entirely on older adults.</b> Every formulation tested in young animals protected completely, including the prior-art cGAMP analogue (homologous challenge) [E11].",
 "<b>Restoration is substantial but incomplete.</b> Durability in the elderly is the main efficacy risk: 67% at day 60 [E8]. The young benchmark was 100%.",
 "<b>Rapid single-dose protection, including against wild-type H5N1, is a distinct second value proposition</b> (pandemic response) [E5 to E7].",
])

# =====================================================================================
H1("8. Evidence base (3): data integrity, what must be fixed before any investment")
P("We audited every block against its annotation and against every other block using four checks: "
  "(a) stated versus observed group sizes; "
  "(b) exact duplication and 'copy-and-shift' duplication (the same 4 to 5 decimals with an integer offset), tested against a chance model built from non-corresponding positions; "
  "(c) recomputation of derived metrics from their primary data; "
  "(d) concordance of every survival block with its paired body-weight block. "
  "The audit produced 23 findings: 3 critical, 5 major, 7 moderate, 6 minor and 2 informational (Appendix B). "
  "Each of the 108 blocks was graded: 49 Tier A (usable), 32 Tier B (usable with caveat), 26 Tier C (excluded or unusable as printed) and 1 Tier D (derived, not independent).")
TAB(["ID", "Finding", "Key evidence", "Consequence"], [
 ["I-01 Critical", "Body-weight values copied across independent experiments, verbatim or with identical decimals plus an integer offset",
  "22 block-group pairs significant after Bonferroni correction. Example: S15-C PSLN-344 vs S15-I Vaccine+PSLN-344 share 40/48 same-animal, same-day values (chance 0.4; p=1e-74). S08-D CMP-204 → S15-F PSLN-212(Y) shift-copy (p=2e-26)",
  "All challenge-weight data excluded. Survival must be source-verified"],
 ["I-02 Critical", "Alveolar-macrophage (S11-A) and neutrophil (S11-B) percentages identical for the same animals",
  "35/100 positions identical (expected 0.1; p=3e-79). Replicate 1 identical in 19/20 cells", "Both blocks excluded"],
 ["I-03 Critical", "S09-C day-12 weights identical for all 16 animals of two groups", "S09!G18:N18 = S09!W18:AD18", "Excluded"],
 ["I-04 Major", "IgG2a/IgG1 blocks S03-B/F have rotated group labels. As printed, PSLN-344 looks Th2-skewed; the primary titres show it is Th1-skewed",
  "Printed 'PSLN-344' equals the PSLN-212 ratios recomputed from S13 (max |diff| 3e-7)", "Replaced by recomputed ratios [E39]"],
 ["I-05 Major", "S07-C: both transferred-macrophage groups carry the same label", "S07!B15 = S07!C15", "Macrophage → Treg claim unsupported"],
 ["I-06 Major", "S09-A second panel labelled 16 h, but it matches the 72-h data", "Mean |Δlog10| vs 72 h 0.02; vs 16 h 0.90", "Not used"],
 ["I-07 Major", "Weights said to belong to S03-I and S03-J contradict those survival blocks",
  "Different group sets. S03-J Sham 9/10 deaths vs 2 in the weights", "S13-F/G excluded; S03-I/J downgraded"],
 ["I-08 Major", "Unlabelled survival-format data region", "S08!A89:D101 (13 animals)", "Origin must be established"],
], widths=[1.9, 5.0, 6.0, 3.8], size=7.2)
FIG("fig6_integrity.png", "", 17.0)
P("<b>What this means for the decision.</b>")
B([
 "<b>Some findings could be clerical.</b> Mislabelled exports or template errors can explain I-04 to I-06 and I-16.",
 "<b>Others cannot be explained by chance.</b> Shift-copying of 5-decimal body weights across experiments, and identical per-animal values for two different cell types (I-01 to I-03), need a formal, independent review. We make no finding of intent.",
 "<b>The survival records themselves show no copy signature, with one exception.</b> S06-C and S06-D have identical outcome vectors (chance about 0.06% per pair) [I-13].",
 "<b>Every key immunology contrast in this proposal comes from Tier-A blocks.</b>",
 "<b>But the survival experiments' paired body-weight records are the most compromised data family,</b> and some contradict their survival blocks [I-07, I-13, I-14]. "
 "Survival outcomes must therefore be checked against contemporaneous vivarium records before they support investment. That is Gate 0.",
])

# =====================================================================================
H1("9. If we drop it: exactly what we give up, and when dropping is the right call")
TAB(["What we would give up", "Evidence"], [
 ["The only formulation in our data that protects aged mice from lethal heterosubtypic influenza: +68 pts vs CDN without Mn<super>2+</super> and +81 pts vs vehicle", "E1, E2, E54"],
 ["Single-dose protection within 2 to 3 days (86%; 6/7 vs 0/7 for vaccine alone; 10/10 vs wild-type H5N1), relevant to pandemic response", "E5, E6, E7"],
 ["Cross-subtype breadth (H3→H1, H1+H3→H5, H1→H3) and durability to day 60 (67% vs 5%)", "E1, E8"],
 ["Robustness to prior influenza exposure (6/7 naive and 6/7 imprinted) and to genetic background", "E9, E10"],
 ["At least 4-fold dose-sparing on target engagement", "E14"],
 ["8- to 19-fold higher titres than PSLN-212, 40-fold higher IgG than the cGAMP comparator, and a Th1 profile", "E35 to E39, E52"],
 ["A mechanism tested by perturbation, and a biomarker set ready for translation (Ifnb1/ISG, GM-CSF, CCL2, Tfh/Tfr, cross-reactive CD8)", "E13 to E45"],
], widths=[13.5, 3.2], size=7.4)
P("<b>What dropping avoids.</b>")
B([
 "Investing on a package that cannot pass audit today [I-01 to I-08].",
 "Open Mn<super>2+</super> neuro-safety exposure [E48].",
 "Inhaled-device development [E46, E47].",
 "Undefined CMC [E50, I-21].",
 "Dependence on an antigen partner [E6].",
])
P("<b>When dropping is the correct, defensible decision.</b>")
B([
 "If the committee will not fund Gates 0 and 1: the table above is the price.",
 "If Gate 0 cannot verify the survival records: the table above is void, because there is nothing to give up.",
 "If Gate 1 misses its pre-specified criteria.",
])

# =====================================================================================
H1("10. What we considered and ruled out")
TAB(["Considered", "Decision", "Reason (evidence)"], [
 ["Advance PSLN-344 straight to IND-enabling work", "Rejected", "Integrity defects [I-01 to I-08]; no standard-of-care benchmark; Mn<super>2+</super> CNS safety and CMC undefined [E48, E50, I-21]"],
 ["Terminate now", "Not the first choice", "Large, consistent, Tier-A-robust effect [E4, E54]; cheap to verify. Correct if Gates 0/1 are not funded or fail"],
 ["Out-license or partner now", "Deferred", "Package would not survive diligence [I-01 to I-08]. Revisit after Gate 1; the adjuvant needs an antigen partner anyway [E6]"],
 ["PSLN-212 (drug + vehicle, no Mn<super>2+</super>) as lead", "Rejected", "13% aged survival; no significant end-of-study benefit vs vehicle in any experiment [E1, E54]; no young-animal advantage [E11]"],
 ["Young-adult / general-population indication", "Rejected", "Ceiling effect: all formulations, including cGAMP, give 100% in young mice [E11]"],
 ["Antigen-free innate prophylactic", "Rejected", "PSLN-344 alone 0/7 [E6]"],
 ["Add R848 (TLR7/8)", "Rejected", "Weaker Ifnb1 (PSLN-R848 4.6x; PSLN-344/R848 29.4 vs 45.8 at 20 µg); Tnf 13x and Il10 48x; 10% weight loss with 1 animal lost [E51, E49]"],
 ["cGAMP payload (CMP-204)", "Rejected", "40x lower IgG, 16x lower HAI, 4.8x lower Ifnb1 than PSLN-344 [E52]"],
 ["Higher dose (above 20 µg)", "Rejected", "20 to 40 µg adds only 9.6% Ifnb1 [E14]. Explore lower doses instead (S4)"],
 ["Claim 'restores aged immunity to young levels'", "Rejected", "Survival −17.5 pts vs young [E3]; CD40/CD86 RI about 0.2 [E29]"],
 ["Use body-weight curves as efficacy evidence", "Rejected", "Copied and internally inconsistent [I-01, I-03, I-07, I-17]"],
 ["Use S03-B/F (IgG2a/IgG1) as printed", "Rejected", "Labels rotated; recomputed from primary titres [I-04, E39]"],
 ["Use alveolar-macrophage and neutrophil kinetics (S11-A/B)", "Rejected", "Duplicated [I-02]"],
 ["Claim CD206+ macrophages drive Tregs", "Not supported", "S07-C groups carry identical labels [I-05]"],
 ["Claim IFNAR drives monocyte recruitment", "Not supported", "p=0.12, n=3 [E21]. IFNAR dependence of moDC differentiation is supported [E22]"],
 ["Count 'Tfh:Tfr' as a separate biomarker", "Rejected", "Arithmetically derived from Tfr [I-22]"],
 ["Pool every survival block naively", "Rejected", "Only the 9 aged four-arm experiments are pooled (stratified by experiment). S03-I/J, S15-H and the imprinting blocks are reported separately; a Tier-A-only sensitivity analysis is provided [E4]"],
 ["HAI as the sole efficacy biomarker", "Rejected", "Protection is mostly cross-strain; PSLN-212 gave HAI GMT 46 (S03-C) yet 0/7 survival on homologous challenge (S03-I, Tier B) [E12, E36]"],
], widths=[5.0, 2.4, 9.3], size=7.2)

# =====================================================================================
H1("11. Limitations of this analysis")
B([
 "<b>Model limits.</b> Mouse-only, female-only, small groups (n=2 to 10 per group), lethal mouse-adapted challenge viruses. There are no viral-load, histopathology, Mn<super>2+</super> biodistribution or licensed-comparator data.",
 "<b>The statistics assume the recorded values are genuine.</b> Gate 0 tests that assumption, and nothing here should be treated as confirmed until it passes.",
 "<b>Pooled survival is heterogeneous.</b> It combines experiments with different vaccines, challenge strains and timings; S15-L/N have undocumented challenge conditions. Stratification removes between-experiment baseline differences but does not model effect heterogeneity. The per-experiment results in Fig. 1 show the same direction in every experiment.",
 "<b>The restoration index is a ratio of differences.</b> Its CIs are wide where the aged-young gap is small. Bootstrap intervals with n=3 to 5 per group are approximate.",
 "<b>Multiplicity.</b> Tests are Welch t-tests (log scale for titres and fold-changes), with Holm adjustment within each block and Tukey HSD per block, as the stated methods require. There is no global correction across the 108 blocks. The decision rests on the pre-specified survival contrasts, not on any single immunology p-value.",
 "<b>Age mapping.</b> Mapping 20-month mice to a human age band is an assumption. TAM sizing should treat it as such.",
])

BR()
H1("Appendix A. Evidence register (E1 to E56)")
P("Each item lists the workbook blocks and cells, the statistical method, and the evidence tier of the underlying blocks "
  "(A usable; B usable with caveat; C excluded; D derived). The machine-readable version, with all group statistics, is in the accompanying workbook.")
S.append(('evidence_table', None))
BR()
H1("Appendix B. Data-integrity register (I-01 to I-23)")
S.append(('integrity_table', None))
BR()
H1("Appendix C. Methods")
B([
 "<b>Parsing.</b> All 108 blocks were mapped explicitly to cell ranges. 535 header checks confirmed every group label against the workbook. "
 "A coverage check confirmed every numeric cell is either parsed data (6,120 values) or a day/dose axis cell. Each value keeps its cell address.",
 "<b>Survival.</b> Kaplan-Meier curves; pairwise log-rank tests; Fisher exact test on end-of-study survival; Wilson 95% CIs. "
 "Pooled analyses cover the 9 aged four-arm experiments (S06-A to S06-G, S15-L, S15-N), stratified by experiment, using a stratified log-rank test, the Cochran-Mantel-Haenszel test and the Mantel-Haenszel risk difference with a stratified bootstrap CI (20,000 resamples).",
 "<b>Immunology.</b> Titres and qPCR fold-changes were analysed on the log10 scale (geometric means). HAI values below the lowest dilution (10) were set to 5. Percentages and counts were analysed on the linear scale. "
 "Welch t-tests were used for key contrasts, with Mann-Whitney tests as sensitivity analyses, Holm adjustment within each block, and one-way ANOVA with Tukey HSD per block. Two-way ANOVA (group x time) was used for time courses.",
 "<b>Derived readouts.</b> IgG2a/IgG1 ratios were recomputed per animal from the S13-A to D subclass titres. "
 "Restoration index = (aged PSLN-344 − aged PSLN-212) / (young PSLN-212 − aged PSLN-212), with a bootstrap 95% CI (5,000 resamples). "
 "Hedges' g was computed for PSLN-344 vs PSLN-212. Ifnb1 dose-response was fitted with an Emax model. Power for Study 1 was estimated by simulation of the Fisher exact test (4,000 simulations per scenario).",
 "<b>Integrity tests.</b> "
 "(1) Stated vs observed n. "
 "(2) Positional concordance: same-animal-position matches between block-groups on the same day, compared with a chance rate estimated from non-corresponding positions (binomial test, Bonferroni-corrected). Carried-forward repeats were removed first. "
 "(3) A fractional-part (\"copy-and-shift\") test for values with 4 or more decimals. "
 "(4) Recomputation of derived blocks. "
 "(5) Survival versus paired-weight concordance, treating a value carried forward for 3 or more steps as a death. "
 "(6) A Monte Carlo probability for identical survival vectors. "
 "(7) Cross-block consistency (S09-A vs S01-A).",
 "<b>Software.</b> Python 3.11 with pandas, SciPy, statsmodels, lifelines and matplotlib; openpyxl for cell-level extraction.",
])
