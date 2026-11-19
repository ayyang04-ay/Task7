# PSLN Program: CDN-1807 STING-agonist adjuvant (PSLN-212 / PSLN-344)
### Portfolio review proposal: recommendation, evidence, mechanism, biomarkers, target population and gated next steps
*Prepared 1 November 2026. Sources: psln_program_dataset.xlsx (15 sheets; 108 data blocks; 6,120 data values; last modified 3 Sep 2026) and psln_program_annotation.pdf. Every number below carries a reference: E-numbers resolve to workbook cells and the statistical test in Appendix A, and I-numbers to the data-integrity register in Appendix B. The reproducible analysis (code, tidy data with cell provenance, all statistics) is provided alongside this document.*


## 1. Recommendation

> **KEEP, BUT CONDITIONALLY AND ONLY AS PSLN-344** (CDN-1807 + Mn2+ in the surfactant-biomimetic liposome), positioned as a mucosal adjuvant for influenza vaccines in older adults. **Do not fund IND-enabling work on the current data package.** Release money one gate at a time: **Gate 0** is data-integrity remediation; **Gate 1** is independent blinded confirmation plus Mn2+ CNS safety and CMC. Terminate at the first failed gate. Discontinue PSLN-212 and all other variants now.

**How the asset looks.**

- **Biologically strong in the population that matters.** In aged mice, adding Mn2+ turns a failing adjuvant into a protective one. Across 9 lethal influenza-challenge experiments, survival was 81% (51/63) with PSLN-344, 13% (8/63) with the same CDN without Mn2+ (PSLN-212) and 0% (0/63) with vehicle. The risk difference versus PSLN-212 is +68 points (95% CI 56 to 79) [E1, E2]. The effect holds in the experiments with no integrity flag (75% vs 7%) [E4]. It is present 3 days after a single dose [E5], lasts to day 60 (67% vs 5%) [E8], and is seen in three mouse strains [E9] and in influenza-experienced animals [E10]. A mechanism tested by perturbation explains it: Mn2+ restores the aged lung's interferon-β response to the STING agonist to the young level [E13], and this drives GM-CSF, monocyte-derived dendritic cells, germinal centres and cross-reactive CD8 T cells [E17 to E45].
- **Not decision-grade as a data package.** Values are duplicated across independent experiments: 22 body-weight group pairs match far beyond chance (p as low as 10^-74), and an alveolar-macrophage dataset shares 35 of 100 per-animal values with a neutrophil dataset (p about 10^-79). Several blocks are mislabelled, and one mislabel reverses a mechanistic conclusion [I-01 to I-08]. This would not survive partner due diligence or a regulatory audit.
- **Translationally unproven on four points.** (1) There is no comparison with a licensed older-adult vaccine or adjuvant, so differentiation versus standard of care is unknown. (2) Mn2+ CNS safety rests on a single 36-hour transcript panel [E48]. (3) The vehicle targets alveolar cells through surfactant proteins [E46, E47], which implies an inhaled product. (4) Basic CMC is undefined: Mn2+ content, the meaning of the dose, and encapsulation of 55% [E50, I-21].

**Why keep rather than drop.** The effect is large and consistent: PSLN-344 beat vehicle in 9/9 experiments and PSLN-212 in 8/9 [E54]. It survives restriction to Tier-A data [E4], is mechanistically coherent, and targets the population with the greatest unmet need. Verifying it (Gates 0 and 1) costs a fraction of IND-enabling work. If Gate 0 fails, the program can be stopped at that point with no further spend, and Section 9 lists exactly what that forgoes.

**Discontinue now (no further spend).** PSLN-212 as a candidate: it fails in aged mice and has no advantage in young mice, where every formulation protects [E1, E11, E54]. Also stop the R848 combinations [E51], the cGAMP payload CMP-204 [E52] and antigen-free standalone use [E6]. Keep PSLN-212 only as a comparator arm.

**Decisions requested today.** (1) Approve Gate 0 and Gate 1 only, with the pass and kill criteria in Section 2. (2) Refer integrity findings I-01 to I-08 to QA / research integrity; this step is independent of the portfolio decision. (3) Ask Market Research to size the segments defined in Section 3.

**Scorecard** (qualitative; each rating is justified by the cited evidence):

| Dimension | Rating | Basis |
|---|---|---|
| Efficacy in aged mice (PSLN-344) | Strong | Large, consistent survival benefit; robust to excluding flagged experiments [E1, E4, E54] |
| Breadth, onset, durability | Good; durability is the weak point | 3 subtypes, protection by day 3, 67% at day 60 vs 100% young [E5, E8] |
| Mechanism | Coherent, partly causal | Perturbation-tested steps (CCR2, gap junctions, IFNAR/GM-CSF, pertussis toxin); STING-dependence untested [Section 4] |
| Data integrity | FAILS today | Critical duplications and mislabels [I-01 to I-08]; must be fixed from source |
| Safety | Largely unknown | Mild reactogenicity; CNS panel reassuring but minimal; no Mn2+ biodistribution or toxicology [E48, E49] |
| Differentiation vs standard of care | Unknown | No licensed-comparator arm anywhere in the package |
| CMC / product definition | Undefined | Mn2+ content and dose basis not stated; encapsulation 55% by A260 [E50, I-21] |
| Fit to unmet need | High (older adults, pandemic) | Benefit is specific to aged hosts [E11]; rapid single-dose protection [E5 to E7] |


## 2. Next steps: what each study must establish, and the endpoints we need to see

![fig7_gated_plan.png](figures/fig7_gated_plan.png)

All thresholds below are proposals anchored to our observed effects. They should be frozen in a pre-registered statistical analysis plan before any study starts. In-life durations are taken from the designs already used in the dataset (e.g. S06-A: vaccinate, challenge at day 14, observe 14 days, which is 28 days in-life). Calendar time and cost must come from Operations; aged (≥20-month) cohorts have a procurement lead time.

| Study | Must establish | Design (key features) | Primary endpoint and GO criterion | Secondary endpoints | KILL if |
|---|---|---|---|---|---|
| G0. Source-data verification (Gate 0) | That recorded outcomes happened as recorded | Independent QA audit of vivarium mortality/euthanasia logs, raw weights, FCS, qPCR and ELISA files for all survival blocks and all Tier B/C blocks. No animals | 100% of survival records in the 18 labelled survival blocks (plus the unlabelled S08 region) traced to contemporaneous records. I-01 to I-08 root-caused and corrected from raw data or retracted | Dose defined (µg CDN-1807); Mn2+ per dose; S15-L/N challenge conditions; cause of 19% background mortality [I-14] | Survival not traceable, or evidence values were not generated as recorded |
| S1. Independent blinded confirmation (Gate 1, the decision study) | The Mn2+ effect is real, reproducible elsewhere, and differentiated versus standard of care | Independent lab; randomised and blinded; aged BALB/c and C57BL/6, both sexes. Arms: vehicle, PSLN-212, PSLN-344, Mn2+-only, licensed benchmark (chosen with Clinical), young reference. Heterosubtypic challenge at day 14 (28 days in-life). n=25/arm gives 80% power if the true difference is 40 pts rather than the observed 68; n=12 gives 93% at the observed effect [E56] | 14-day survival. GO: PSLN-344 minus PSLN-212 ≥40 pts with 95% CI excluding 0 (observed +68, CI 56 to 79 [E1]); same direction in each strain and sex; Mn2+-only no better than PSLN-212; PSLN-344 not inferior to benchmark (margin pre-set) | Lung viral titre day 3/5 (absent today); weight-loss AUC with a pre-set humane-endpoint rule and no carry-forward; HAI/MN at day 14; NP/M1 IFN-γ+ CD8; 16-h ISG | Difference <40 pts or CI includes 0; benchmark clearly superior; Mn2+-only reproduces the effect |
| S2. Mn2+ biodistribution and CNS safety (Gate 1) | Intranasal Mn2+ does not accumulate in, or inflame, the CNS | Aged mice; PSLN-344, PSLN-212, vehicle, Mn2+-only; single dose and prime-boost (days 0 and 14 as in S13-I/J); cholera toxin positive control; 16 h to day 28 | Brain and olfactory-bulb Mn (ICP-MS) not above vehicle beyond a margin set with Toxicology. CNS Ifnb1/Tnf/Isg15 <2-fold vs vehicle at every time and below cholera toxin (today 1.16 to 1.57x vs 2.7 to 5.5x at 36 h [E48]) | Histopathology of olfactory epithelium, bulb and brain; olfaction and neurobehaviour; lung Mn clearance | Dose-related CNS Mn accumulation, or inflammation approaching cholera toxin |
| S3. CMC characterisation (Gate 1) | PSLN-344 is a defined, reproducible product | At least 3 batches; orthogonal assays | Encapsulation by HPLC/LC-MS (A260 today 54.8% ± 5.1 [E50]); Mn:CDN ratio; free Mn2+; size/PDI/zeta; lyophilised stability | TEM morphology; endotoxin; batch consistency | Specifications not reproducibly met |
| S4. Dose-ranging and reactogenicity (Gate 2) | The lowest effective dose and the tolerability window | Aged mice at 5, 10 and 20 µg (10 µg already exceeds the PSLN-212 maximum on Ifnb1 [E14]) | Survival non-inferior to 20 µg (margin pre-set), with mean weight-nadir loss ≤5% (today 3.6% [E49]) | BAL cells and protein; lung histopathology; lung Il6/Tnf [E16] | No dose meets both criteria |
| S5. Per-animal correlates of protection (Gate 2) | Which non-terminal biomarker predicts survival | Sample each animal before challenge: 16-h nasal/serum ISG, CCL2, GM-CSF; day-7 blood Tfh; day-14 HAI/MN, nasal IgA, NP/M1 ELISpot. Dose titration creates a range of protection | At least one non-terminal biomarker with ROC AUC ≥0.80 for survival (proposed), which becomes the Phase 1 efficacy biomarker | Multivariable model; thresholds | No biomarker reaches AUC ≥0.70 (no usable Phase 1 efficacy biomarker) |
| S6. Durability and boost in aged mice (Gate 2) | Protection lasts in the elderly | Prime vs prime-boost; challenge at days 60, 90 and 180 (180 + 14 days in-life, as in S09-F) | ≥80% survival at day 60 with the chosen regimen (today 67% after a single dose [E8]) | IFN-γ+ CD8 and TRM maintenance; titres [E40, E42, E43] | Below 60% at day 60 even with a boost |
| S7. Second species and human-relevant delivery (Gate 2) | Effect translates beyond mice, with a human-relevant device | Ferrets (aged if available) with intranasal or aerosol delivery; nasal vs lung deposition study | Reduced viral shedding and disease after heterosubtypic challenge vs vaccine alone and vs PSLN-212 | HAI/MN, nasal IgA, ISG/GM-CSF bridging; local tolerability | No benefit over vaccine alone |
| S8. Mechanism closure (Gate 2, parallel) | Causality for the claims in Section 4 | STING-deficient aged mice ± PSLN-344; uptake of PSLN-344 vs PSLN-212 by macrophages vs epithelium; CD8 depletion / TRM blockade before challenge; S07-C repeated with correct labels; macrophage and neutrophil kinetics re-measured | Protection lost without STING; CD8 dependence quantified | Costimulation-enhancing variants (CD40 gap [E29]) | Effect is STING-independent AND Mn2+-only protects (re-scope to an Mn adjuvant) |

**After Gate 2:** route-matched GLP repeat-dose toxicology in two species, CNS safety pharmacology, a GMP process, and antigen partnering, leading to IND.


## 3. Target demographic (for Market Research TAM sizing)

| Segment | Why (our data) | Status | What Market Research should size |
|---|---|---|---|
| PRIMARY: older adults receiving seasonal influenza vaccine (the ≥65 segment is the conventional older-adult definition; external convention) | Benefit is specific to aged hosts [E1, E11]; cross-strain protection [E1]; unaffected by prior exposure [E10]; seen in 3 strains [E9] | Supported pre-clinically (mouse only) | Older-adult population x vaccination coverage x share of 'enhanced' older-adult vaccines. Price premium requires the benchmark comparison (Gate 1) |
| SECONDARY: pandemic preparedness (H5N1 and other novel subtypes), older-adult priority groups | Single dose protects when challenge comes 2 to 3 days later [E5, E6]; wild-type H5N1 10/10 [E7] | Supported pre-clinically (E7 is Tier B) | Government stockpile and rapid-response procurement; dose-sparing [E14] matters for stockpile economics |
| EXPLORATORY (no data): long-term-care residents; adults with chronic lung disease; immunocompromised adults | Outbreak use is inferred from rapid onset [E5]. Caution for lung disease: uptake depends on surfactant proteins [E46] | Not studied | Size only as upside; needs dedicated studies |
| NOT A TARGET: young and healthy adults; antigen-free prophylaxis | No differentiation in young animals [E11]; no protection without antigen [E6] | Ruled out | Do not include in TAM |

**Product attributes that change TAM assumptions:**

- **Mucosal (intranasal or inhaled) administration.** The vehicle's alveolar targeting [E46, E47] makes device development probable.
- **The adjuvant needs an antigen partner** [E6].
- **Possible dose-sparing** [E14].
- **A booster may be needed in the elderly for durability** [E8, E40].

**Caveat.** "Aged" means female mice aged 20 months or more. Mapping this to a specific human age band is an assumption.


## 4. Mechanism of action, built from our data

Unless noted, comparisons are aged PSLN-344 versus aged PSLN-212, i.e. the contribution of Mn2+. *Established* means supported by a perturbation (knockout, antagonist, blocker or rescue). *Associated* means a consistent correlation without causal test. *Gap* means not shown.

| Step | What our data show | Ref | Status |
|---|---|---|---|
| 1. Delivery | Alveolar-macrophage uptake depends on surfactant proteins A/D: 43.1% vs 12.7% in knockouts. Liposomes reach epithelial cells (15.8% vs 0.38% for free dye). Mn2+ cuts epithelial uptake about 4-fold (3.8% vs 15.8%) | E46, E47 | Established for the vehicle. Gap: which cell PSLN-344 acts through |
| 2. STING → IFN-β (target engagement) | Lung Ifnb1 2.2x higher at 16 h (36.9- vs 16.5-fold), equal to young (37.5). Dose-dependent; ≥4x dose-sparing. Transient: by 72 h 4.2- vs 3.4-fold, no longer different | E13 to E15 | Established as a readout. Gap: no STING-knockout or Mn2+-only arm |
| 3. Innate amplification | Ccl2 77x, Ccl3 27x, Ccl5 7.6x, Il6 6.5x at 16 h. Gm-csf 4.2 to 5.4x at 16 to 36 h. Monocyte recruitment needs gap junctions (carbenoxolone: 7.3% → 3.1%) | E16, E17, E20 | Established (carbenoxolone) |
| 4. Monocyte recruitment | Lung monocytes 30.6% vs 16.7% at day 4; CCR2 antagonist 9.9% → 3.3%. IFNAR dependence of recruitment NOT shown (p=0.12, n=3) | E18, E19, E21 | Established via CCR2; IFNAR link is a gap |
| 5. Monocyte fate: DC, not macrophage | moDC formation needs IFNAR (2.1% vs 19.7%) and is rescued by GM-CSF (12.4%). GM-CSF converts the PSLN-212 response (13.8% vs 5.9%). Without Mn2+, Ly6C+CCR2+ macrophages accumulate instead (19.0 vs 3.4 x10^5) | E22 to E24 | Established (knockout and rescue) |
| 6. DC migration and priming | CD11b+ DC 18.9% vs 8.3%; cDC1 37.5% vs 22.8%; CCR7+ migratory DC 30.7% vs 7.3%; antigen-positive DC in lymph node 7.1% vs 1.8% (blocked by pertussis toxin); OT-I priming 18.7% vs 0.8%. Costimulation only partly restored: CD40 11.2% vs 5.6%, young 38.7% | E25 to E30, E45 | Established (pertussis toxin in S05-C; the PTX arm's adjuvant is unstated in S02-C/E). Costimulation is the residual gap |
| 7. Germinal centre and regulation | Tfh 10.3% vs 3.8%; Tfr 10.8% vs 26.7%; GC B cells 6.5% vs 2.3%; lung Treg 3.0% vs 6.7%; CD206+ macrophages 48.9% vs 71.5% | E31 to E34 | Associated. Macrophage → Treg causality unreadable (I-05) |
| 8. Antibodies | CA09 IgG 18.6x, HAI 8.0x, neutralising 9.2x; Aichi similar. Th1-skewed: IgG2a/IgG1 1.85 vs 0.54 | E35 to E39 | Readout |
| 9. Cross-reactive CD8 and TRM | IFN-γ+ CD8 6.4% vs 1.5% (day 14) and 9.9% vs 3.0% (day 60); lung TRM 4.0% vs 1.0%; CCR2-dependent (shown in young mice) | E42, E43, E45 | Associated. Causal role untested (no depletion) |
| 10. Protection | Heterosubtypic survival 81% vs 13%; rapid onset, durable to day 60, seen in 3 strains | E1 to E10 | Outcome |

![fig3_restoration_cascade.png](figures/fig3_restoration_cascade.png)

**The key mechanistic insight is where Mn2+ stops helping.** Fig. 3 scores each step against the young benchmark. The restoration index (RI) is 0 for no gain over PSLN-212 in aged mice and 1 for a full match to young. Mn2+ fully restores the innate trigger (Ifnb1 RI 0.98) and most myeloid and DC trafficking (RI 0.70 to 0.89). It does **not** restore DC costimulation (CD40 RI 0.17; CD86 RI 0.22) [E29] or CD8 effector and memory quality (GZMB RI 0.41; TRM RI 0.59) [E41, E43]. This matches the residual survival gap, which is largest at day 60 [E3, E8]. Three implications follow:

- durability is the efficacy risk to test first;
- DC maturation is the lever for a next-generation formulation;
- costimulation and CD8 quality, not IFN induction, are the biomarkers most likely to limit response in older humans.

![fig4_dose_ifnb1.png](figures/fig4_dose_ifnb1.png)

**Mechanistic gaps to close** (Study 8):

- The effect has not been shown to be STING-dependent: there is no STING-knockout arm and no Mn2+-only arm.
- Which lung cell takes up PSLN-344 is unknown.
- Whether CD8/TRM cells cause protection is untested.
- The macrophage → Treg link cannot be read (I-05).
- Alveolar-macrophage and neutrophil kinetics are unusable (I-02).


## 5. Biomarkers to validate efficacy

| Biomarker (timing) | Mouse evidence, PSLN-344 vs PSLN-212 (aged) | Role | Proposed human analogue (to validate) |
|---|---|---|---|
| Lung Ifnb1 / ISG (16 h) | 36.9- vs 16.5-fold (2.2x); RI 0.98; dose-responsive [E13, E14] | Target engagement; dose selection | Blood or nasal-wash ISG score; IFN-β / CXCL10 |
| Gm-csf (16 to 36 h) | 4.2x at 16 h; 5.4x at 36 h. Largest standardised effect of the 76 readouts ranked (Hedges g 7.9) [E17, E55] | Mn2+-specific pharmacodynamics (DC licensing) | Nasal-wash / serum GM-CSF |
| Ccl2 (16 h) | 77x [E16] | Innate amplification | Nasal / serum CCL2 (MCP-1) |
| Monocyte → moDC; CCR7+ DC (day 3 to 4) | 30.6% vs 16.7%; 30.7% vs 7.3% [E18, E27] | Mechanism (animal studies only) | n/a (BAL in animals) |
| Tfh ICOS-hi / Tfr (day 7) | 10.3% vs 3.8%; 10.8% vs 26.7% [E31, E32] | Early adaptive predictor | Circulating Tfh (ICOS+PD-1+CXCR5+) at day 7 |
| HAI / neutralising titre (day 14) | 8.0x and 9.2x (CA09); 9.2x (Aichi) [E36 to E38] | Registrational immunogenicity (strain-matched) | Standard HAI / microneutralisation |
| IgG2a/IgG1 (day 14) | 1.85 vs 0.54 (CA09); 2.30 vs 0.46 (Aichi) [E39] | Response quality (Th1) | IgG-subclass profile (mapping to define) |
| Cross-reactive IFN-γ+ CD8 (days 14 and 60) | 6.4% vs 1.5%; 9.9% vs 3.0% [E42] | Heterosubtypic protection and durability | PBMC IFN-γ ELISpot to conserved NP/M1 peptides |
| Lung TRM CD8 (day 25) | 4.0% vs 1.0%; RI 0.59 [E43] | Durability | n/a (animal) |
| Safety: CNS Ifnb1/Tnf/Isg15; weight nadir; lung Il6/Tnf | CNS 1.16 to 1.57x PBS vs cholera toxin 2.7 to 5.5x; nadir 96.4% vs 98.2% vaccine-only; lung Il6 6.5x [E48, E49, E16] | Safety / reactogenicity | Olfactory/neurological monitoring; solicited reactogenicity |

**Which biomarker predicts protection is not yet known.** The principal readouts (Fig. 3) rank the groups in the same order (vehicle < PSLN-212 < PSLN-344 ≤ young; inverted for Tfr and Treg), and immune readouts and survival were measured in different animals. No per-animal correlate of protection can be estimated from this package, so Study 5 is designed to produce one. HAI alone is unlikely to be enough for the older-adult cross-strain claim, for two reasons. Most protection data involve strain-mismatched challenge, which HAI does not measure. And in S03-I (Tier B), aged PSLN-212 mice all died after homologous challenge (0/7), although the same regimen gave a HAI GMT of 46 in a parallel cohort (S03-C) [E12, E36].


## 6. Evidence base (1): the asset as tested

- **Active drug.** CDN-1807, a cyclic-dinucleotide STING agonist.
- **Vehicle.** A pulmonary-surfactant-biomimetic liposome (DPPC, DPPG, DPPE-PEG2000, cholesterol).
- **Two versions.** PSLN-212 is drug plus vehicle. PSLN-344 additionally incorporates Mn2+ by coordination polymerisation.
- **Comparators.** CMP-204 (cGAMP in the same vehicle, a prior-art analogue); R848 variants; empty-vehicle Sham.
- **It is an adjuvant, not a stand-alone drug.** Every efficacy experiment co-administers it intranasally with an inactivated influenza vaccine (20 µg adjuvant per mouse). Given without antigen, PSLN-344 gave 0/7 survival, versus 6/7 with antigen [E6]. Commercially this means an antigen partner or our own adjuvanted vaccine.
- **The vehicle is appropriate as a vehicle.** It is inert: lung Ifnb1 0.94-fold; no CNS signal versus PBS (all p≥0.16); 0/63 survival in aged mice [E53].
- **Study population.** "Aged" means female BALB/c mice aged 20 months or more unless stated; "young" means 7 to 8 weeks. Only female mice were used.


## 7. Evidence base (2): efficacy, what the data show

| Question | Result (aged mice unless stated) | Ref | Tier |
|---|---|---|---|
| Does Mn2+ make the asset work in aged animals? | Survival 81% (51/63) PSLN-344 vs 13% (8/63) PSLN-212 vs 0% (0/63) vehicle. Risk difference +68 pts (95% CI 56 to 79); stratified log-rank p=1.6e-16 | E1, E2 | A/B |
| Is it robust to the integrity findings? | Tier-A experiments only: 75% (21/28) vs 7% (2/28); +68 pts (95% CI 50 to 86); p=4.6e-09 | E4 | A |
| Is it consistent across experiments? | Beats vehicle in 9/9 and PSLN-212 in 8/9 (log-rank p<0.05). PSLN-212 never significantly raised end-of-study survival over vehicle (Fisher p≥0.46) | E54 | A/B |
| How fast? | Challenge 3 days after a single dose: 86% (12/14) vs 14% (2/14) vs 0/14. Vaccine + PSLN-344 6/7 vs vaccine alone 0/7. Wild-type VN04 H5N1 at day 2: 10/10 vs 3/10 vs 1/10 | E5, E6, E7 | A/B, B, B |
| How durable? | Challenge at day 60: 67% (14/21) vs 5% (1/21); young benchmark 21/21. At day 14: 93% (13/14) | E8 | A/B |
| How broad? | Protection across H3→H1 (PR8), H1+H3→H5 (rgH5N1) and H1→H3 (Perth) (Fig. 1) | E1 | A/B |
| Other genetic backgrounds? | C57BL/6: 6/7 vs 0/7 vs 0/7. Swiss Webster: 6/7 vs 2/7 vs 0/7 (challenge details not recorded) | E9 | B |
| Prior influenza exposure? | 14-month mice: PSLN-344 6/7 in both naive and imprinted animals, in both challenges. PSLN-212 0/7 to 4/7 | E10 | B |
| Does it match young animals? | No. 81% vs 98% for young PSLN-212 (−17.5 pts, 95% CI −27 to −8); the gap is largest at day 60 | E3, E8 | A/B |
| Any benefit in young animals? | None measurable. PSLN-344, PSLN-212 and cGAMP all protect 100% (S09-B/D/F, S13-E) | E11 | A/B |
| Any internal inconsistency? | S03-I: PSLN-212 (0/7) did worse than cGAMP (3/7) despite higher titres. The paired weights contradict S03-I | E12, I-07 | B |

![fig1_survival_aged.png](figures/fig1_survival_aged.png)

![fig2_km_tierA.png](figures/fig2_km_tierA.png)

**Interpretation.**

- **Mn2+ is what makes the asset work in older hosts.** Without Mn2+, CDN-1807 delays death in some experiments but does not improve survival [E54].
- **The commercial case rests entirely on older adults.** Every formulation tested in young animals protected completely, including the prior-art cGAMP analogue (homologous challenge) [E11].
- **Restoration is substantial but incomplete.** Durability in the elderly is the main efficacy risk: 67% at day 60 [E8]. The young benchmark was 100%.
- **Rapid single-dose protection, including against wild-type H5N1, is a distinct second value proposition** (pandemic response) [E5 to E7].


## 8. Evidence base (3): data integrity, what must be fixed before any investment

We audited every block against its annotation and against every other block using four checks: (a) stated versus observed group sizes; (b) exact duplication and 'copy-and-shift' duplication (the same 4 to 5 decimals with an integer offset), tested against a chance model built from non-corresponding positions; (c) recomputation of derived metrics from their primary data; (d) concordance of every survival block with its paired body-weight block. The audit produced 23 findings: 3 critical, 5 major, 7 moderate, 6 minor and 2 informational (Appendix B). Each of the 108 blocks was graded: 49 Tier A (usable), 32 Tier B (usable with caveat), 26 Tier C (excluded or unusable as printed) and 1 Tier D (derived, not independent).

| ID | Finding | Key evidence | Consequence |
|---|---|---|---|
| I-01 Critical | Body-weight values copied across independent experiments, verbatim or with identical decimals plus an integer offset | 22 block-group pairs significant after Bonferroni correction. Example: S15-C PSLN-344 vs S15-I Vaccine+PSLN-344 share 40/48 same-animal, same-day values (chance 0.4; p=1e-74). S08-D CMP-204 → S15-F PSLN-212(Y) shift-copy (p=2e-26) | All challenge-weight data excluded. Survival must be source-verified |
| I-02 Critical | Alveolar-macrophage (S11-A) and neutrophil (S11-B) percentages identical for the same animals | 35/100 positions identical (expected 0.1; p=3e-79). Replicate 1 identical in 19/20 cells | Both blocks excluded |
| I-03 Critical | S09-C day-12 weights identical for all 16 animals of two groups | S09!G18:N18 = S09!W18:AD18 | Excluded |
| I-04 Major | IgG2a/IgG1 blocks S03-B/F have rotated group labels. As printed, PSLN-344 looks Th2-skewed; the primary titres show it is Th1-skewed | Printed 'PSLN-344' equals the PSLN-212 ratios recomputed from S13 (max /diff/ 3e-7) | Replaced by recomputed ratios [E39] |
| I-05 Major | S07-C: both transferred-macrophage groups carry the same label | S07!B15 = S07!C15 | Macrophage → Treg claim unsupported |
| I-06 Major | S09-A second panel labelled 16 h, but it matches the 72-h data | Mean /Δlog10/ vs 72 h 0.02; vs 16 h 0.90 | Not used |
| I-07 Major | Weights said to belong to S03-I and S03-J contradict those survival blocks | Different group sets. S03-J Sham 9/10 deaths vs 2 in the weights | S13-F/G excluded; S03-I/J downgraded |
| I-08 Major | Unlabelled survival-format data region | S08!A89:D101 (13 animals) | Origin must be established |

![fig6_integrity.png](figures/fig6_integrity.png)

**What this means for the decision.**

- **Some findings could be clerical.** Mislabelled exports or template errors can explain I-04 to I-06 and I-16.
- **Others cannot be explained by chance.** Shift-copying of 5-decimal body weights across experiments, and identical per-animal values for two different cell types (I-01 to I-03), need a formal, independent review. We make no finding of intent.
- **The survival records themselves show no copy signature, with one exception.** S06-C and S06-D have identical outcome vectors (chance about 0.06% per pair) [I-13].
- **Every key immunology contrast in this proposal comes from Tier-A blocks.**
- **But the survival experiments' paired body-weight records are the most compromised data family,** and some contradict their survival blocks [I-07, I-13, I-14]. Survival outcomes must therefore be checked against contemporaneous vivarium records before they support investment. That is Gate 0.


## 9. If we drop it: exactly what we give up, and when dropping is the right call

| What we would give up | Evidence |
|---|---|
| The only formulation in our data that protects aged mice from lethal heterosubtypic influenza: +68 pts vs CDN without Mn2+ and +81 pts vs vehicle | E1, E2, E54 |
| Single-dose protection within 2 to 3 days (86%; 6/7 vs 0/7 for vaccine alone; 10/10 vs wild-type H5N1), relevant to pandemic response | E5, E6, E7 |
| Cross-subtype breadth (H3→H1, H1+H3→H5, H1→H3) and durability to day 60 (67% vs 5%) | E1, E8 |
| Robustness to prior influenza exposure (6/7 naive and 6/7 imprinted) and to genetic background | E9, E10 |
| At least 4-fold dose-sparing on target engagement | E14 |
| 8- to 19-fold higher titres than PSLN-212, 40-fold higher IgG than the cGAMP comparator, and a Th1 profile | E35 to E39, E52 |
| A mechanism tested by perturbation, and a biomarker set ready for translation (Ifnb1/ISG, GM-CSF, CCL2, Tfh/Tfr, cross-reactive CD8) | E13 to E45 |

**What dropping avoids.**

- Investing on a package that cannot pass audit today [I-01 to I-08].
- Open Mn2+ neuro-safety exposure [E48].
- Inhaled-device development [E46, E47].
- Undefined CMC [E50, I-21].
- Dependence on an antigen partner [E6].

**When dropping is the correct, defensible decision.**

- If the committee will not fund Gates 0 and 1: the table above is the price.
- If Gate 0 cannot verify the survival records: the table above is void, because there is nothing to give up.
- If Gate 1 misses its pre-specified criteria.


## 10. What we considered and ruled out

| Considered | Decision | Reason (evidence) |
|---|---|---|
| Advance PSLN-344 straight to IND-enabling work | Rejected | Integrity defects [I-01 to I-08]; no standard-of-care benchmark; Mn2+ CNS safety and CMC undefined [E48, E50, I-21] |
| Terminate now | Not the first choice | Large, consistent, Tier-A-robust effect [E4, E54]; cheap to verify. Correct if Gates 0/1 are not funded or fail |
| Out-license or partner now | Deferred | Package would not survive diligence [I-01 to I-08]. Revisit after Gate 1; the adjuvant needs an antigen partner anyway [E6] |
| PSLN-212 (drug + vehicle, no Mn2+) as lead | Rejected | 13% aged survival; no significant end-of-study benefit vs vehicle in any experiment [E1, E54]; no young-animal advantage [E11] |
| Young-adult / general-population indication | Rejected | Ceiling effect: all formulations, including cGAMP, give 100% in young mice [E11] |
| Antigen-free innate prophylactic | Rejected | PSLN-344 alone 0/7 [E6] |
| Add R848 (TLR7/8) | Rejected | Weaker Ifnb1 (PSLN-R848 4.6x; PSLN-344/R848 29.4 vs 45.8 at 20 µg); Tnf 13x and Il10 48x; 10% weight loss with 1 animal lost [E51, E49] |
| cGAMP payload (CMP-204) | Rejected | 40x lower IgG, 16x lower HAI, 4.8x lower Ifnb1 than PSLN-344 [E52] |
| Higher dose (above 20 µg) | Rejected | 20 to 40 µg adds only 9.6% Ifnb1 [E14]. Explore lower doses instead (S4) |
| Claim 'restores aged immunity to young levels' | Rejected | Survival −17.5 pts vs young [E3]; CD40/CD86 RI about 0.2 [E29] |
| Use body-weight curves as efficacy evidence | Rejected | Copied and internally inconsistent [I-01, I-03, I-07, I-17] |
| Use S03-B/F (IgG2a/IgG1) as printed | Rejected | Labels rotated; recomputed from primary titres [I-04, E39] |
| Use alveolar-macrophage and neutrophil kinetics (S11-A/B) | Rejected | Duplicated [I-02] |
| Claim CD206+ macrophages drive Tregs | Not supported | S07-C groups carry identical labels [I-05] |
| Claim IFNAR drives monocyte recruitment | Not supported | p=0.12, n=3 [E21]. IFNAR dependence of moDC differentiation is supported [E22] |
| Count 'Tfh:Tfr' as a separate biomarker | Rejected | Arithmetically derived from Tfr [I-22] |
| Pool every survival block naively | Rejected | Only the 9 aged four-arm experiments are pooled (stratified by experiment). S03-I/J, S15-H and the imprinting blocks are reported separately; a Tier-A-only sensitivity analysis is provided [E4] |
| HAI as the sole efficacy biomarker | Rejected | Protection is mostly cross-strain; PSLN-212 gave HAI GMT 46 (S03-C) yet 0/7 survival on homologous challenge (S03-I, Tier B) [E12, E36] |


## 11. Limitations of this analysis

- **Model limits.** Mouse-only, female-only, small groups (n=2 to 10 per group), lethal mouse-adapted challenge viruses. There are no viral-load, histopathology, Mn2+ biodistribution or licensed-comparator data.
- **The statistics assume the recorded values are genuine.** Gate 0 tests that assumption, and nothing here should be treated as confirmed until it passes.
- **Pooled survival is heterogeneous.** It combines experiments with different vaccines, challenge strains and timings; S15-L/N have undocumented challenge conditions. Stratification removes between-experiment baseline differences but does not model effect heterogeneity. The per-experiment results in Fig. 1 show the same direction in every experiment.
- **The restoration index is a ratio of differences.** Its CIs are wide where the aged-young gap is small. Bootstrap intervals with n=3 to 5 per group are approximate.
- **Multiplicity.** Tests are Welch t-tests (log scale for titres and fold-changes), with Holm adjustment within each block and Tukey HSD per block, as the stated methods require. There is no global correction across the 108 blocks. The decision rests on the pre-specified survival contrasts, not on any single immunology p-value.
- **Age mapping.** Mapping 20-month mice to a human age band is an assumption. TAM sizing should treat it as such.


## Appendix A. Evidence register (E1 to E56)

Each item lists the workbook blocks and cells, the statistical method, and the evidence tier of the underlying blocks (A usable; B usable with caveat; C excluded; D derived). The machine-readable version, with all group statistics, is in the accompanying workbook.

| ID | Area | Claim | Result | Blocks | Cells | Method | Tier |
|---|---|---|---|---|---|---|---|
| E1 | Efficacy | Pooled heterosubtypic/other lethal challenge, aged mice, 9 four-arm experiments: PSLN-344 vs PSLN-212 | Survival PSLN-344 51/63 (81%) vs PSLN-212 8/63 (13%); Sham 0/63 (0%); young PSLN-212 62/63 (98%). MH risk difference +68.3 pts (95% bootstrap CI 55.6 to 79.4); stratified log-rank chi2=68.0, p=1.6e-16 | S06-A,S06-B,S06-C,S06-D,S06-E,S06-F,S06-G,S15-L,S15-N | S06!A3:R105; S15!A103:E161 | Mantel-Haenszel risk difference (stratified bootstrap CI, 20,000 resamples); stratified log-rank | A/B |
| E2 | Efficacy | Same pool: PSLN-344 vs vehicle (Sham) | 51/63 (81%) vs 0/63 (0%); MH risk difference +81.0 pts (95% CI 71.4 to 88.9); stratified log-rank p=1.3e-27 | S06-A,S06-B,S06-C,S06-D,S06-E,S06-F,S06-G,S15-L,S15-N | as E1 | as E1 | A/B |
| E3 | Efficacy | Same pool: aged PSLN-344 vs young PSLN-212 benchmark (restoration is incomplete) | 51/63 (81%) vs 62/63 (98%); MH risk difference -17.5 pts (95% CI -27.0 to -7.9); stratified log-rank p=0.001 | S06-A,S06-B,S06-C,S06-D,S06-E,S06-F,S06-G,S15-L,S15-N | as E1 | as E1 | A/B |
| E4 | Efficacy | Sensitivity: only experiments with no survival-side integrity flag (S06-A, B, E, F) | PSLN-344 21/28 (75%) vs PSLN-212 2/28 (7%); MH risk difference +67.9 pts (95% CI 50.0 to 85.7); stratified log-rank p=4.6e-09 | S06-A,S06-B,S06-E,S06-F | S06!A3:K30; S06!G34:R68 | as E1 | A |
| E5 | Efficacy | Speed of onset: challenge 3 days after a single dose (S06-B, S06-D) | PSLN-344 12/14 (86%) vs PSLN-212 2/14 (14%) vs Sham 0/14; stratified log-rank p=1.9e-05 | S06-B,S06-D | S06!G3:K30; S06!A34:E61 | stratified log-rank | A/B |
| E6 | Efficacy | Adjuvant, not standalone: vaccine, PSLN-344 alone, or both, 3 d before VN04 rgH5N1 (S15-H) | Vaccine+PSLN-344 6/7 vs vaccine alone 0/7 (log-rank p=1.6e-04) vs PSLN-344 alone 0/7 (log-rank p=1.4e-04) | S15-H | S15!A73:D93 | log-rank; Fisher exact | B |
| E7 | Efficacy | Wild-type VN04 H5N1 (BSL-3), challenge 2 d after single rgH5N1 dose (S03-J) | PSLN-344 10/10 vs PSLN-212 3/10 (log-rank p=0.002) vs Sham 1/10 (log-rank p=1.7e-04). Caveat: stated n=9; one PSLN-344 record lacks a day value | S03-J | S03!G17:J46 | log-rank; Fisher exact | B |
| E8 | Efficacy | Durability: challenge at day 60 (S06-E, F, G) vs day 14 (S06-A, C) | PSLN-344 d60 14/21 (67%) vs PSLN-212 1/21 (5%) (stratified log-rank p=2.4e-06); young PSLN-212 d60 21/21 (100%). PSLN-344 d14 13/14 (93%); d14 vs d60 Fisher p=0.11 | S06-A,S06-C,S06-E,S06-F,S06-G | S06!A3:E30; S06!M3:Q30; S06!G34:R68; S06!A71:F105 | stratified log-rank; Fisher exact | A/B |
| E9 | Efficacy | Genetic background: aged C57BL/6 (S15-L) and Swiss Webster (S15-N) | C57BL/6: PSLN-344 6/7 vs PSLN-212 0/7 vs Sham 0/7 (log-rank vs PSLN-212 p=0.001); Swiss Webster: 6/7 vs 2/7 vs 0/7 (vs PSLN-212 p=0.056; vs Sham p=0.001). Challenge virus/timing not stated | S15-L,S15-N | S15!A103:E130; S15!A134:E161 | log-rank | B |
| E10 | Efficacy | Prior influenza exposure ("imprinting"), 14-month mice (S06-E2, S06-F2) | PR8 challenge: PSLN-344 6/7 (naive) and 6/7 (imprinted) vs PSLN-212 0/7 and 4/7. Perth H3N2 challenge: PSLN-344 6/7 and 6/7 vs PSLN-212 0/7 and 0/7 (imprinted 344 vs 212 log-rank p=2.2e-04) | S06-E2_imprint,S06-F2_imprint | S06!G70:Q98 | log-rank | B |
| E11 | Efficacy | Young mice: no differentiation between formulations (ceiling) | PSLN-344Y 8/8 = PSLN-212Y 8/8 in each of S09-B, S09-D, S09-F (d180 challenge); Sham 0/8, 0/8, 0/7. S13-E: CMP-204(Y) 7/7 = PSLN-344(Y) 7/7 vs Sham 1/7 | S09-B,S09-D,S09-F,S13-E | S09!A12:D88; S13!R3:V30 | descriptive; log-rank vs Sham p<=0.0016 | A/B |
| E12 | Efficacy | Homologous 10x CA09 challenge, aged (S03-I); internally inconsistent | PSLN-344 7/7, young PSLN-212 7/7, CMP-204 3/7, PSLN-212 0/7, Sham 0/7. PSLN-212 does worse than the cGAMP comparator (log-rank p=0.001) despite higher titres (E35, E36); paired weights (S13-F) contradict it | S03-I | S03!A17:F51 | log-rank | B |
| E13 | Target engagement | Lung Ifnb1 16 h after intranasal dose (no vaccine), aged vs young (S01-A) | Geometric mean fold: aged PSLN-344 36.9 vs aged PSLN-212 16.5 (ratio 2.23, p=9.6e-06) vs young PSLN-212 37.5 (ratio 0.98, p=0.82); Sham 0.94; CMP-204 7.7 (PSLN-344/CMP-204 4.8x, p=3.8e-06). Restoration index 0.98 (95% CI 0.84 to 1.14) | S01-A_16h | S01!B8..S01!F8; S01!B5..S01!F5; S01!B9..S01!F9 | Welch t-test on log10; bootstrap restoration index | A |
| E14 | Target engagement | Dose-response, lung Ifnb1 at 16 h (S08-A, n=3/dose) | PSLN-344: 1.4/8.3/21.1/45.8/50.2-fold at 1/5/10/20/40 ug; PSLN-212 max 14.9 at 40 ug. PSLN-344 at 10 ug exceeds PSLN-212 at 40 ug (>=4x dose-sparing). 20->40 ug adds only +9.6% | S08-A | S08!A3:M7 | descriptive; Emax fit (ED50 imprecise, SE ~50%) | B |
| E15 | Target engagement | Transience: lung Ifnb1 at 72 h (S01-A) | aged PSLN-344 4.2 vs PSLN-212 3.4-fold (ratio 1.22, p=0.33) | S01-A_72h | S01!H3:L10 | Welch t-test on log10 | A |
| E16 | Innate amplification | Lung cytokine/chemokine transcripts at 16 h, PSLN-344 vs PSLN-212 (S09-A panel 1, n=3; log10 data) | Ccl2 77.4x (p=0.002); Ccl3 26.7x (p=7.9e-04); Ccl5 7.6x (p=0.025); Il6 6.5x (p=0.021); Tnf 2.6x (p=0.11); Il10 2.0x (p=0.19) | S09-A_panel1_A-U | S09!B3:V9 | Welch t-test on log10 values | A |
| E17 | Innate amplification | Lung Gm-csf after vaccination (S02-F) | PSLN-344 vs PSLN-212: 4.2x at 16 h (p=5.1e-04), 5.4x at 36 h (p=3.8e-05), 2.6x at 72 h (p=0.004); PSLN-344 vs Sham 7.1x at 36 h | S02-F | S02!B17:P19 | Welch t-test on log10 | A |
| E18 | Myeloid | Lung monocytes at day 4 (S01-D) | PSLN-344 30.6% vs PSLN-212 16.7% (p=0.002) vs Sham 10.4% vs young 32.2%; group x time interaction p=4.5e-07 (two-way ANOVA) | S01-D | S01!B26:U26 | Welch t-test; two-way ANOVA | A |
| E19 | Myeloid | CCR2 dependence (INCB3344) after PSLN-344 (S07-B) | monocytes 9.9% -> 3.3% (p=0.001); Ly6C+ macrophages 15.4% -> 2.5% (p=0.003). Timepoint not stated | S07-B_Mono,S07-B_Ly6CMac | S07!B10:F14 | Welch t-test | B |
| E20 | Myeloid | Gap-junction blockade (carbenoxolone) before PSLN-344 vaccination (S11-C) | recruited monocytes 7.3% -> 3.1% (p=0.004) | S11-C | S11!A17:B21 | Welch t-test | A |
| E21 | Myeloid | IFNAR dependence of monocyte infiltration (S12-A, young, n=3) - NOT established | IFNAR-/- BM 15.4% vs WT BM 21.3% (p=0.12) | S12-A | S12!A3:B5 | Welch t-test | A |
| E22 | Myeloid | moDC differentiation needs IFNAR and is rescued by GM-CSF (S02-H, BM chimeras, PSLN-344) | moDC from IFNAR-/- BM 2.1% vs WT 19.7% (p=4.0e-04); + GM-CSF 12.4% (p=0.003 vs IFNAR-/-) | S02-H | S02!B30:F34 | Welch t-test | B |
| E23 | Myeloid | GM-CSF supplementation converts the PSLN-212 response toward moDC (S02-G) | Ly6C+CD11c+MHC-II+ cells 13.8% vs PSLN-212 5.9% (p=0.002) vs GM-CSF alone 1.5% | S02-G | S02!B22:D26 | Welch t-test | B |
| E24 | Myeloid | Inflammatory Ly6C+CCR2+ macrophages accumulate with PSLN-212, not PSLN-344 (S07-A, n=3) | day 5: PSLN-212 19.0 vs PSLN-344 3.4 x10^5 cells (p=0.036); day 10: 14.6 vs 2.9 (p=0.001) | S07-A | S07!B3:G7 | Welch t-test; two-way ANOVA interaction p=8.6e-05 | A |
| E25 | Dendritic cells | Lung CD11b+ DC, day 4 (S01-E) | PSLN-344 18.9% vs PSLN-212 8.3% (Welch p=0.049; Mann-Whitney p=0.008) vs young 21.4% | S01-E | S01!B32:Z32 | Welch; Mann-Whitney | A |
| E26 | Dendritic cells | Lung cDC1 (XCR1+), 72 h (S01-F) | PSLN-344 37.5% vs PSLN-212 22.8% (p=0.006) vs young 43.4%; Sham 17.9% | S01-F | S01!B36:Z36 | Welch | A |
| E27 | Dendritic cells | CCR7+ migratory CD11b+ DC in lung, 72 h (S02-A) | PSLN-344 30.7% vs PSLN-212 7.3% (p=0.002) vs young 35.0%; Sham 2.5% | S02-A | S02!A3:D7 | Welch | A |
| E28 | Dendritic cells | Antigen-bearing DC in MLN at 36 h (S02-C) | PSLN-344 7.1% vs PSLN-212 1.8% (p=6.9e-04); pertussis toxin 2.4% (p=4.7e-04 vs PSLN-344); young 9.4% | S02-C | S02!K3:O7 | Welch | B |
| E29 | Dendritic cells | Costimulatory maturation of MLN CD11b+ DC, day 3 (S02-D) - the largest residual gap | CD40+: PSLN-344 11.2% vs PSLN-212 5.6% (p=0.011) vs young 38.7% (RI 0.17, 95% CI 0.09-0.26); CD86+: 14.5% vs 8.1% (p=0.003) vs young 37.9% (RI 0.22) | S02-D_CD40,S02-D_CD86 | S02!A10:I14 | Welch; bootstrap RI | A |
| E30 | Dendritic cells | Ex vivo OT-I priming by MLN CD11b+ DC (S02-E) | PSLN-344 18.7% vs PSLN-212 0.8% (p=1.0e-04) vs young 26.2%; PTX 2.5% | S02-E | S02!K10:O14 | Welch | B |
| E31 | Germinal centre | Tfh (CXCR5+PD1+ICOS-hi), day 7 (S04-A) | PSLN-344 10.3% vs PSLN-212 3.8% (p=0.009) vs young 13.6%; Sham 0.30% | S04-A_ICOShi | S04!G2:K5 | Welch | A |
| E32 | Germinal centre | Tfr (Foxp3+ of CXCR5+ICOS-hi), day 7 (S04-B) | PSLN-344 10.8% vs PSLN-212 26.7% (p=0.005) vs young 7.1%; day 30 (S04-C): 14.0% vs 18.0% (p=0.11). The "Tfh:Tfr" block is derived from these values | S04-B_Foxp3,S04-C | S04!A8:D12; S04!A22:D26 | Welch | A |
| E33 | Germinal centre | GC B cells (CXCR5+GL7+), MLN day 7 (S03-K); Aicda/E47 (S03-L, n=3) | GC B 6.5% vs 2.3% (p=0.002) vs young 9.8%; Aicda 3.5x (p=0.007), E47 3.9x (p=0.007) | S03-K,S03-L_Aicda | S03!L17:O21; S03!L26:Q28 | Welch (log10 for qPCR) | A |
| E34 | Regulatory | Lung Treg day 7 (S04-D, n=3) and lung CD206+ macrophages (S11-E, timepoint not stated) | Treg 3.0% vs PSLN-212 6.7% (p=3.4e-04), young 1.8%; CD206+ macrophages 48.9% vs 71.5% (p=0.002), Sham 85.2%, young 35.5% | S04-D,S11-E | S04!A29:D31; S11!A31:D35 | Welch | A/B |
| E35 | Antibody | Serum IgG anti-CA09 H1N1, day 14 (S03-A) | GMT PSLN-344 7,305 vs PSLN-212 393 (18.6x, p=1.3e-05) vs young 11,959; Sham 56; CMP-204 181 | S03-A | S03!A3:E7 | Welch t-test on log10 titres | A |
| E36 | Antibody | HAI anti-CA09, day 14 (S03-C; values <10 set to 5) | GMT PSLN-344 368 vs PSLN-212 46 (8.0x, p=3.7e-04) vs young 485; Sham 8; CMP-204 23 | S03-C | S03!K3:O7 | Welch t-test on log10 titres | A |
| E37 | Antibody | Neutralising titre anti-CA09, day 14 (S03-D) | GMT PSLN-344 3,840 vs PSLN-212 418 (9.2x, p=0.002) vs young 6,686; Sham 52; CMP-204 182 | S03-D | S03!Q3:U7 | Welch t-test on log10 titres | A |
| E38 | Antibody | Aichi H3N2: IgG (S03-E), HAI (S03-G), neutralising (S03-H), day 14 | IgG GMT PSLN-344 5,701 vs PSLN-212 426 (13.4x, p=7.0e-05) vs young 13,855; Sham 52; CMP-204 200 | HAI GMT PSLN-344 320 vs PSLN-212 35 (9.2x, p=2.1e-04) vs young 368; Sham 10; CMP-204 30 | Neut GMT PSLN-344 2,533 vs PSLN-212 276 (9.2x, p=3.9e-04) vs young 4,411; Sham 40; CMP-204 138 | S03-E,S03-G,S03-H | S03!A10:U14 | Welch t-test on log10 titres | A |
| E39 | Antibody | IgG2a/IgG1 (Th1 skew) recomputed from primary subclass titres (S13-A..D) - replaces mislabelled S03-B/F | CA09: PSLN-344 1.85 vs PSLN-212 0.54 (3.4x, p=0.007) vs young 2.50; Aichi: 2.30 vs 0.46 (5.0x, p=0.003) vs young 2.79 | S13-A,S13-B,S13-C,S13-D | S13!A3:O7 | Welch on log10 of per-animal ratio | A |
| E40 | Antibody | After boost (day 28; S13-I, S13-J) | CA09 IgG GMT PSLN-344 15,651 vs PSLN-212 4,411 (3.5x, p=0.010) vs young 40,739; Sham 57; CMP-204 940 | Aichi IgG GMT PSLN-344 12,435 vs PSLN-212 1,086 (11.5x, p=7.6e-04) vs young 43,472; Sham 101; CMP-204 474 | S13-I,S13-J | S13!F53:P57 | Welch t-test on log10 titres | A |
| E41 | CD8 T cells | Lung CD8 proliferation (Ki-67+, S05-D) and cytotoxic (GZMB+, S05-E), day 3 | Ki-67+ 9.4% vs PSLN-212 3.5% (p=4.7e-04) vs young 9.9%; Sham 0.8% | GZMB+ 5.7% vs PSLN-212 3.0% (p=0.001) vs young 9.6%; Sham 1.0% (GZMB RI 0.41) | S05-D,S05-E | S05!A19:D30 | Welch | A |
| E42 | CD8 T cells | Cross-reactive (rgH5N1-restimulated) IFN-g+ CD8 in MLN: day 14 (S05-F) and day 60 (S05-G); GZMB+ day 60 (S05-H) | d14 6.4% vs PSLN-212 1.5% (p=1.3e-04) vs young 9.2%; Sham 0.7% | d60 9.9% vs PSLN-212 3.0% (p=0.003) vs young 14.4%; Sham 1.5% | GZMB d60 4.1% vs PSLN-212 1.0% (p=0.003) vs young 5.6%; Sham 0.6% | S05-F,S05-G,S05-H | S05!A33:D51 | Welch | A |
| E43 | CD8 T cells | Lung resident-memory CD8 (CD69+CD103+), day 25 (S05-I) | 4.0% vs PSLN-212 1.0% (p=6.2e-05) vs young 6.0%; Sham 0.6% (RI 0.59, 95% CI 0.47-0.70) | S05-I | S05!A54:D58 | Welch; bootstrap RI | B |
| E44 | CD8 T cells | IFN-g+ CD8 after CA09 or Aichi restimulation (S14-A; timepoint not stated) | H1N1 11.0% vs PSLN-212 3.1% (p=7.4e-04) vs young 13.7%; Sham 0.8% | H3N2 9.9% vs PSLN-212 3.6% (p=3.3e-04) vs young 14.0%; Sham 1.0% | S14-A_H1N1,S14-A_H3N2 | S14!A3:I7 | Welch | B |
| E45 | CD8 T cells | CCR2 blockade abolishes lung GZMB+ CD8 (S02-I, young); PTX blocks MLN but not lung OT-I proliferation (S05-C, n=3) | GZMB+ CD8 6.8% -> 1.4% (p=8.1e-05); OT-I MLN 30.9% -> 6.8% (p=0.007); lung 59.0% vs 55.1% (p=0.57) | S02-I,S05-C | S02!H30:I34; S05!A13:D15 | Welch | A/B |
| E46 | Delivery | Alveolar macrophage uptake depends on surfactant proteins A/D (S01-C, n=4) | DiD+ AM: WT 43.1% vs Sftpa1-/-Sftpd-/- 12.7% (p=3.9e-05) | S01-C | S01!B20:E21 | Welch | A |
| E47 | Delivery | Epithelial uptake: liposome vs free dye (S01-B) and Mn2+ formulation vs non-Mn liposome (S08-C) | AECII SRB+: PSLN-SRB 15.8% vs free SRB 0.38% (p=1.1e-04); PSLN-344-SRB 3.8% vs PSLN-SRB 15.8% (p=5.2e-04); AECI 3.0% vs 13.8% (p=1.6e-05) | S01-B,S08-C | S01!B14:F17; S08!A14:D18 | Welch | B |
| E48 | Safety | CNS transcripts 36 h after intranasal vaccine +/- PSLN-344 or cholera toxin (S10-A, aged, n=5) | Ifnb1: PSLN-344 1.30x PBS (p=0.20), CT 5.5x (p=4.4e-06), PSLN-344 vs Sham p=0.57; Tnf: PSLN-344 1.57x PBS (p=0.033), CT 3.4x (p=3.3e-04), PSLN-344 vs Sham p=0.36; Isg15: PSLN-344 1.16x PBS (p=0.39), CT 2.7x (p=7.6e-04), PSLN-344 vs Sham p=0.50 | S10-A_Ifnb1,S10-A_Tnf,S10-A_Isg15 | S10!A3:N7 | Welch on log10; no multiplicity adjustment | B |
| E49 | Safety | Reactogenicity: body-weight nadir after vaccination, no challenge (S08-D, n=5) | Vaccine alone 98.2%; PSLN-344 96.4% (p=0.065 vs vaccine); PSLN-212 97.0%; PSLN-212/R848 90.0% (p=0.020), 4/5 animals at day 10 | S08-D | S08!B21:AE26 | per-animal nadir days 2-10; Welch vs vaccine | B |
| E50 | CMC | Encapsulation efficiency by A260 (S08-B, n=3) | CMP-204 65.2% (SD 6.0); PSLN-212 59.6% (SD 4.6); PSLN-212/R848 52.4% (SD 7.3); PSLN-344 54.8% (SD 5.1); PSLN-R848 61.3% (SD 6.8) | S08-B | S08!A11:O11 | descriptive | B |
| E51 | Ruled out | R848 combinations: weaker or more inflammatory | Ifnb1 16 h (S01-A): PSLN-R848 4.6x, PSLN-212/R848 24.0x vs PSLN-344 36.9x; S08-A at 20 ug: PSLN-344/R848 29.4 vs PSLN-344 45.8; PSLN-212/R848 vs PSLN-212 lung Tnf 13x (p=0.009), Il10 48x (p=0.006); weight nadir 90.0% with 1 animal lost (E49) | S01-A_16h,S08-A,S09-A_panel1_A-U,S08-D | S01!B3:F10; S08!K3:M7; S09!H3:P9 | Welch | A/B |
| E52 | Ruled out | cGAMP comparator (CMP-204, prior-art analogue) vs PSLN-344, aged | IgG anti-CA09 40x lower than PSLN-344 (p=3.2e-05); HAI 16x lower (p=6.6e-05); Ifnb1 4.8x lower (E13); survival S03-I 3/7 vs 7/7 (Tier B) | S03-A,S03-C,S01-A_16h,S03-I | S03!A3:O7 | Welch on log10 | A/B |
| E53 | Vehicle | The vehicle (empty PSLN, "Sham") is inert, as a vehicle should be | Lung Ifnb1 16 h: Sham 0.94-fold (95% CI 0.57-1.54) vs untreated; CNS Sham vs PBS: Ifnb1 1.15x (p=0.50), Tnf 1.30x (p=0.16), Isg15 1.07x (p=0.68); vaccine + vehicle 0/63 survival in aged mice (E2) | S01-A_16h,S10-A_Ifnb1 | S01!B3:F3; S10!A3:N7 | geometric mean with t-CI on log10; Welch on log10 | A/B |
| E54 | Efficacy | Per-experiment consistency across the 9 aged four-arm experiments | PSLN-344 beat vehicle (log-rank p<0.05) in 9/9 and PSLN-212 in 8/9 experiments (exception S15-N, p=0.056). PSLN-212 never significantly increased end-of-study survival over vehicle in any experiment (Fisher p>=0.46 in all 9), although it delayed death in 5/9 (log-rank p<0.05) | S06-A,S06-B,S06-C,S06-D,S06-E,S06-F,S06-G,S15-L,S15-N | as E1 | per-experiment log-rank and Fisher exact | A/B |
| E55 | Biomarkers | Standardised effect size (Hedges g), PSLN-344 vs PSLN-212 (aged), across all Tier A/B readouts | 76 readout-timepoints ranked; top 6: S02-F 36 h g=7.95 (n=5/5); S01-D d8 g=7.93 (n=5/5); S08-A 20 ug g=7.89 (n=3/3); S02-E g=7.88 (n=5/5); S04-D g=-7.82 (n=3/3); S13-B g=7.55 (n=5/5). Full ranking in workbook sheet Hedges_g | all Tier A/B blocks with both groups | see workbook | Hedges g (bias-corrected), log10 scale for titres/fold-changes | A/B |
| E56 | Study design | Simulated power of a two-arm survival comparison (Fisher exact, two-sided alpha=0.05, 4,000 simulations/scenario) | Observed effect (81% vs 13%): n=7/arm 0.61, n=10 0.80, n=12 0.93, n=15 0.96. If the true difference is 40 pts (60% vs 20%): n=15 0.45, n=20 0.64, n=25 0.80. The historical n=7 design therefore had ~61% power per experiment at the observed effect | S06-A,S06-B,S06-E,S06-F | derived from E1/E4 rates | Monte Carlo simulation | A |


## Appendix B. Data-integrity register (I-01 to I-23)

| ID | Severity | Blocks | Finding | Evidence | Decision impact |
|---|---|---|---|---|---|
| I-01 | Critical | S08-D, S09-C, S09-E, S09-G, S15-A, S15-C, S15-F, S15-I, S15-J, S15-K, S15-M, S15-O | Body-weight values duplicated across independent experiments/groups, either verbatim or with an identical 4-5-decimal fractional part plus an integer offset ("copy-and-shift"). | 22 block-group pairs significant after Bonferroni correction (2,628 pairs x 2 tests). Strongest: S15-C PSLN-344 vs S15-I "3d Vaccine+PSLN-344": 40 of 48 same-animal/same-day values identical (e.g., S15!W25:AC25 = S15!W74:AC74), chance expectation 0.4, p=1e-74; S08-D CMP-204 vs S15-F PSLN-212(Y): 14 of 20 high-precision values share 5-decimal fractional parts at integer offsets (e.g., S08!G22=97.79487 vs S15!B54=99.79487), p=2e-26; S15-A Sham day 4 = S15-M PSLN-212 day 4 for 7/7 animals incl. 89.42307692 and 90.10989011 (S15!I5:O5 = S15!W105:AC105). | All challenge body-weight data excluded from the evidence base. Because these blocks are the paired records of the survival experiments, survival data require source verification before they can support investment. |
| I-02 | Critical | S11-A, S11-B | Alveolar-macrophage (S11-A) and neutrophil (S11-B) percentages are identical for the same animals in 35/100 positions; replicate 1 identical in 19/20 group-timepoints, replicate 2 in 15/20. | e.g., S11!B3:C3 = S11!B10:C10 (23.5, 17.2); S11!Q5:R5 = S11!Q12:R12 (53.0, 44.1). Chance expectation 0.10; p=3e-79. Structurally identical block S11-D shows no such overlap. | S11-A and S11-B excluded. Alveolar-macrophage and neutrophil kinetics are unknown. |
| I-03 | Critical | S09-C | Day-12 body weights identical for all 8 PSLN-212Y and all 8 PSLN-344Y animals. | S09!G18:N18 = S09!W18:AD18 (97.7, 95.2, 93.3, 93.5, 99.1, 96.9, 100.3, 99.8). | Excluded (weights not used). |
| I-04 | Major | S03-B, S03-F | Printed group labels of the IgG2a/IgG1 ratio blocks are rotated relative to the primary subclass titres. As printed, PSLN-344 appears the most Th2-skewed group; recomputed from primary titres, it is Th1-skewed. | S03-B "PSLN-212" = S13-A/S13-B PSLN-212(Y) ratios (max |diff| 1.8e-4); "PSLN-344" = PSLN-212 (3e-7); "PSLN-212(Y)" = PSLN-344 (3e-7). Same rotation in S03-F vs S13-C/S13-D. | S03-B/F replaced by ratios recomputed from S13 primary titres. Source files must confirm which labels are correct. |
| I-05 | Major | S07-C | Both transferred-macrophage groups carry the identical label "Ly6C-CD206+ MΦ", so the experiment (which macrophage subset raises lung Tregs) cannot be read. | S07!B15 and S07!C15 identical; means 10.4% (B16:B20) vs 5.1% (C16:C20). | The "CD206+ macrophage -> Treg" arm of the MoA is unsupported until relabelled from source. |
| I-06 | Major | S09-A (columns X-AS) | Second S09-A panel is labelled "16h" but reproduces the 72-h Ifnb1 values of S01-A. | Mean |difference| of group log10 means vs S01-A 72 h = 0.02; vs S01-A 16 h = 0.90 (6 shared groups). | Treated as an unconfirmed 72-h panel; not used for primary claims. |
| I-07 | Major | S13-F, S13-G (vs S03-I, S03-J) | Body-weight blocks stated to be "the animals of S03-I/S03-J" do not match those survival blocks. The group sets differ (S13-F has Naive and no CMP-204; S13-G has Naive and no PSLN-212), and the death counts conflict. | S03-J Sham: 9/10 deaths incl. days 3 and 4 (S03!G17:H26) vs 10/10 Sham weights recorded to day 14 with only 2 carried-forward runs (S13!L43:U50). S03-I PSLN-212: 7/7 dead by day 6 (S03!A31:D37) vs 3 S13-F "PSLN-212" animals recovering to day 14 (S13!T40:V40). | S13-F/G excluded. S03-I and S03-J downgraded to Tier B. |
| I-08 | Major | S08 rows 89-101 | Unlabelled survival-format region: 13 animals in two columns, all censored at day 14. No block label, group or condition. | S08!A89:D101 (col C: 6 rows, col D: 7 rows). | Cannot be used. Origin must be established. |
| I-09 | Moderate | S03-J | Stated n=9 but 10 records per group. One PSLN-344 record has an event value but no time. | S03!G15 "n=9"; S03!J46=0 with S03!G46 blank. | PSLN-344 10/10 survival reported with this caveat. |
| I-10 | Moderate | S13-E | Stated n=5, 7 records per group. | S13!R1 vs S13!S3:V30. | Usable with caveat. |
| I-11 | Moderate | S05-A, S05-B | Stated n=3 but 2 values per group per timepoint. Conditions are contradictory (OVA immunisation vs bivalent vaccine; NP366 tetramer readout). | S05!B3:I10. | Excluded from inference. |
| I-12 | Moderate | S09-F, S09-G | S09-F Sham has 7 survival records (stated 8) while S09-G has 8 Sham weight columns. The annotation attributes the 7-animal Sham group to S09-B, which actually has 8. | S09!B66:B72 (7) vs S09!O66:V66 (8); S09!B12:B19 (8). | Usable with caveat (young-animal data only). |
| I-13 | Moderate | S06-C, S06-D | Identical PSLN-212 outcome vectors (deaths d5, 8, 10, 10, 12; 2 survivors) and identical Sham vectors in two experiments. S15-D weights imply 2 deaths each in PSLN-344 and PSLN-212(Y) that S06-D does not record. | S06!M10:O16 vs S06!A41:C47; S15!W37:W40 (79.5 carried d8-14), S15!AC36:AC40 (85.2 carried). | Downgraded to Tier B; excluded in sensitivity analysis. |
| I-14 | Moderate | S06-G, S06-E | Unchallenged aged "Untreated" controls died: 3/7 in S06-G and 1/7 in S06-E (4/21 = 19% in 14 days). The 3 PSLN-344 deaths in S06-G are not reflected in the S15-G weights. | S06!F99:F105; S06!L62:L68; S15!W63:AC70. | Background mortality in the aged colony biases aged survival downward and needs explaining (husbandry / health status). |
| I-15 | Moderate | S01-B, S08-C | AECII/PSLN-SRB values for animals 1-2 are identical in two experiments that state different gating strategies. | S01!B14:C14 = S08!A14:A15 (17.7, 17.5); p=4e-05 (Bonferroni-significant). | Possible reuse of control data. Kept for the PSLN vs free-SRB contrast (effect >40x) with caveat. |
| I-16 | Minor | S06 | Block labels "S06-E" and "S06-F" are each used twice on the sheet. | S06!G32/G69, S06!M32/M69. | Renamed S06-E2/S06-F2 (imprinting) in this analysis. |
| I-17 | Minor | S15 (all weight blocks), S13-G | Dead animals are handled inconsistently in weight blocks: blank after death in some groups, last value carried forward in others, sometimes within the same block. | e.g., S15-A Sham blank (S15!I7:O10) vs S15-A PSLN-212 carried forward (S15!P6:P10 = 81.6). | Group-mean weight curves computed from the workbook would be biased. |
| I-18 | Minor | S07-B, S11-E, S13-H, S14-A; S15-L, S15-N; S02-G, S02-H, S05-C, S08-A; S02-C/E | Missing metadata: timepoint not stated (S07-B, S11-E, S13-H, S14-A); challenge virus and timing not stated (S15-L, S15-N); age not stated (S02-G, S02-H, S05-C, S08-A); adjuvant of the PTX group not stated (S02-C/E). | Annotation PDF. | Usable only descriptively for those dimensions. |
| I-19 | Minor | S10-A | Annotation says the block is reported as mean with SD, but it contains 5 per-animal values per group (PBS group means = 1.000 exactly). | S10!A3:N7. | Treated as per-animal values; needs confirmation. |
| I-20 | Minor | S08-B | "Encapsulation efficiency of CDN-1807 by A260" is reported for CMP-204 (cGAMP) and PSLN-R848 (no CDN-1807). A260 may be confounded by Mn coordination in PSLN-344. | S08!A11:O11. | Encapsulation efficiency needs an orthogonal assay (HPLC/LC-MS). |
| I-21 | Minor | Materials / S08-A | PSLN-344/R848 is used in S08-A but not defined. The Mn2+ content of PSLN-344 is not stated anywhere. "20 µg of adjuvant" is not defined as CDN, lipid or total mass. | Annotation p.1; S08!K2. | Dose and Mn exposure cannot be scaled to humans until defined. |
| I-22 | Info | S04-B Tfh:Tfr | The "Tfh:Tfr" block is exactly (100 - Foxp3%)/Foxp3% of S04-B Foxp3. It is not an independent measurement. | S04!A15:D19 vs S04!A8:D12 (max |diff| 4e-6). | Not counted as independent evidence. |
| I-23 | Info | All | Female mice only. No viral-load, histopathology, Mn-biodistribution or licensed-comparator data anywhere in the package. | Annotation p.1. | Gaps addressed in the next-step plan. |


## Appendix C. Methods

- **Parsing.** All 108 blocks were mapped explicitly to cell ranges. 535 header checks confirmed every group label against the workbook. A coverage check confirmed every numeric cell is either parsed data (6,120 values) or a day/dose axis cell. Each value keeps its cell address.
- **Survival.** Kaplan-Meier curves; pairwise log-rank tests; Fisher exact test on end-of-study survival; Wilson 95% CIs. Pooled analyses cover the 9 aged four-arm experiments (S06-A to S06-G, S15-L, S15-N), stratified by experiment, using a stratified log-rank test, the Cochran-Mantel-Haenszel test and the Mantel-Haenszel risk difference with a stratified bootstrap CI (20,000 resamples).
- **Immunology.** Titres and qPCR fold-changes were analysed on the log10 scale (geometric means). HAI values below the lowest dilution (10) were set to 5. Percentages and counts were analysed on the linear scale. Welch t-tests were used for key contrasts, with Mann-Whitney tests as sensitivity analyses, Holm adjustment within each block, and one-way ANOVA with Tukey HSD per block. Two-way ANOVA (group x time) was used for time courses.
- **Derived readouts.** IgG2a/IgG1 ratios were recomputed per animal from the S13-A to D subclass titres. Restoration index = (aged PSLN-344 − aged PSLN-212) / (young PSLN-212 − aged PSLN-212), with a bootstrap 95% CI (5,000 resamples). Hedges' g was computed for PSLN-344 vs PSLN-212. Ifnb1 dose-response was fitted with an Emax model. Power for Study 1 was estimated by simulation of the Fisher exact test (4,000 simulations per scenario).
- **Integrity tests.** (1) Stated vs observed n. (2) Positional concordance: same-animal-position matches between block-groups on the same day, compared with a chance rate estimated from non-corresponding positions (binomial test, Bonferroni-corrected). Carried-forward repeats were removed first. (3) A fractional-part ("copy-and-shift") test for values with 4 or more decimals. (4) Recomputation of derived blocks. (5) Survival versus paired-weight concordance, treating a value carried forward for 3 or more steps as a death. (6) A Monte Carlo probability for identical survival vectors. (7) Cross-block consistency (S09-A vs S01-A).
- **Software.** Python 3.11 with pandas, SciPy, statsmodels, lifelines and matplotlib; openpyxl for cell-level extraction.
