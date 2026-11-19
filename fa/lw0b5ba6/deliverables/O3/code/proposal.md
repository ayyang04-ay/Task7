---
title: "PSLN program (CDN-1807 STING agonist in a surfactant-biomimetic liposome): portfolio recommendation and next-step proposal"
subtitle: "Portfolio Review Committee | Data: psln_program_dataset.xlsx and psln_program_annotation.pdf, complete as of 1 November 2026 | Every number cites its source block [Sxx-X]; the workbook PSLN_analysis_tables.xlsx traces each value to its cell and test"
---

# 1. Recommendation

**Keep the asset, with a narrower scope and staged funding.** I recommend neither funding it at its current scope nor dropping it yet.

| Decision | What it covers |
|---|---|
| **Keep and advance** | **PSLN-344**, which is CDN-1807 plus Mn²⁺ in the surfactant-biomimetic liposome. Use: as an intranasal adjuvant for inactivated influenza vaccine in **adults aged 65 and over**. |
| **Stop** | PSLN-212 for older adults; all R848 combinations; the cGAMP payload (CMP-204). Reasons are in Section 9. |
| **Fund in two gates** | **Gate 0**: data-integrity and provenance audit (about 8 weeks). **Gate 1**: independent, blinded replication in aged mice that adds the missing controls and a licensed-vaccine benchmark (about 6 months). Toxicology, large-animal work and CMC scale-up are funded only after both gates are passed. Kill criteria are set in advance (Section 2). |

**How the asset looks: scientifically strong, but the evidence behind it is fragile.**

**Strong.** PSLN-344 is the only arm in our data that consistently protects aged mice.

- Pooled across the 11 aged-mouse challenge experiments, survival was:
    - PSLN-344: **68/80 (85%)**
    - PSLN-212: 11/80 (14%)
    - vaccine + empty-liposome vehicle: 1/80 (1%)
- Versus PSLN-212, the Mantel–Haenszel risk difference is +71 percentage points (stratified log-rank χ² = 90.0, p ≈ 2 × 10⁻²¹) [Table 2].
- The advantage holds in every integrity scenario I tested:
    - excluding all 7 flagged experiments: 21/28 vs 2/28 vs 0/28;
    - a worst case built against PSLN-344: 66/80 vs 15/80 vs 5/80 (Figure 2).
- Haemagglutination-inhibition (HI) titres are 8.0–9.2× those on PSLN-212. That reaches 76–87% of the young-mouse reference [S03-C, S03-G].

**Fragile.**

- **17 data-integrity findings, 5 of them critical** (Section 4). Examples:
    - body-weight curves copied between experiments that are described as independent;
    - two different cell populations sharing 35 of 100 animal-level values;
    - survival tables contradicted by their own weight records.
- The committee will check the numbers and will find these. We should disclose them first.
- **Evidence gaps:**
    - STING dependence has never been tested;
    - there is no Mn-only control and no free-drug control;
    - Mn has not been measured in the brain after nasal dosing;
    - there is no comparison with a licensed older-adult vaccine;
    - mucosal IgA was never measured;
    - all the mice are female.

**Why keep rather than drop.** The upside is a differentiated, needle-free influenza vaccine for older adults with broad protection (Section 8). Answering the open questions takes one audit and one replication study. That work comes before any of the larger downstream spend.

# 2. Next steps: what each study must establish, and the endpoints we need to see

| Gate | Timing (planning estimate) | Decision it informs | Stop if |
|---|---|---|---|
| G0: integrity audit | Weeks 0–8 | Whether the dataset can support any decision | Any finding is unexplained, or there is evidence of falsification |
| G1: independent replication with missing controls | Months 2–8 | Whether the efficacy is real, and whether Mn, CDN and the liposome are each needed | PSLN-344 survival < 50% or not different from PSLN-212; or no advantage over the IM benchmark |
| G1b: mechanism | Months 2–8, in parallel | Whether the claimed STING-agonist MoA holds | No STING dependence. In that case the MoA, the claims and the IP strategy are rewritten before G2 |
| G2: Mn and STING safety | Months 4–12 | Whether there is a safety margin for intranasal Mn²⁺ | Mn reaches the CNS at relevant doses; NOAEL < 10× the minimum effective dose (MED) |
| G3: translational model and delivery route | Months 8–18 | Whether a human-relevant device reproduces the effect | No benefit with nasal-spray or aerosol delivery in ferrets or NHP |
| CMC, in parallel | Months 0–12 | Whether the product can be manufactured and stored | Specifications cannot be met before GLP toxicology |

## G0. Data-integrity and provenance audit (weeks 0–8)

- **Must establish:** that every table reflects primary records.
- **Design:** an independent QA review, covering all 17 findings in Section 4, of:
    - raw FCS files and gating;
    - ELISA and HI plate data;
    - qPCR Ct exports;
    - animal health and death logs;
    - cage cards.
- **Endpoints we need to see:**
    1. A documented root cause for each finding.
    2. Survival re-derived from death logs for all 18 survival blocks, with no unexplained mismatch against the weight records.
    3. Corrected labels for S03-B/F, S07-C, S09-A, the duplicate S06 labels, and S13-F/G.
    4. The primary analyses re-run on the corrected data.
- **Go:**
    - every finding is explained by documented error; **and**
    - the corrected pooled survival gap between PSLN-344 and PSLN-212 is still ≥50 points. It is 64–71 points under all four scenarios today (Table 2b).
- **Stop:** if any finding remains unexplained, or there is evidence of falsification:
    - stop the program;
    - escalate under the research-integrity policy;
    - do not use the dataset externally.

## G1. Independent, blinded replication with the missing controls (months 2–8)

**Must establish:**

1. that protection in aged mice replicates in a second lab;
2. that Mn²⁺, CDN-1807 and the liposome each contribute;
3. how PSLN-344 compares with a current older-adult standard of care;
4. an **individual-level** correlate of protection, which the current data cannot provide because biomarkers and outcomes were measured in different mice.

**Design.**

- Mice: aged (≥20 months) BALB/c and C57BL/6, both sexes.
- Conduct: pre-registered, randomised, blinded.
- Arms, each given bivalent inactivated vaccine intranasally unless stated:
    1. vehicle (empty liposome);
    2. PSLN-212;
    3. PSLN-344;
    4. **Mn-only liposome** (PSLN-344 without CDN);
    5. **free CDN-1807 + free MnCl₂** at matched doses;
    6. **IM benchmark**: the same antigen given intramuscularly with a squalene-emulsion adjuvant;
    7. young PSLN-212 reference;
    8. **unchallenged aged sentinels**.
- Size: **29 mice per challenged arm**.
    - This gives ≥80% exact power against PSLN-212 (assumed 70% vs 20% survival) and against the Mn-only arm (assumed 75% vs 30%).
    - It allows for the 19% background mortality we observed in unchallenged aged mice (I-06).
    - The IM comparison is powered on HI titre: 21 per arm detects a 1.5× GMT difference. Powering it on survival would need 46 per arm. See workbook sheet Sample_size.
- The rgH5N1 heterosubtypic cohort is limited to the vehicle, PSLN-212, PSLN-344 and IM-benchmark arms.

**Endpoints we need to see.**

- **Primary:** 14-day survival after a homologous 10× LD50 CA09 challenge at day 14, repeating S03-I. A second cohort receives an rgH5N1 heterosubtypic challenge, repeating S06-C.
- **Secondary:**
    - weight AUC, censored at death;
    - lung and nasal viral titres on days 3 and 5;
    - from the same mice before challenge, on day 14: HI, neutralising titre, and **nasal and BAL IgA**;
    - IgG2a(c)/IgG1 ratio;
    - IFN-γ ELISpot and lung TRM;
    - necropsy of every death.

**Go if all of the following hold:**

- PSLN-344 survival ≥70%, and ≥50 points above both PSLN-212 and vehicle (our data: 85% vs 14% vs 1%);
- HI GMT ratio over PSLN-212 ≥4 (our data: 8.0–9.2);
- PSLN-344 beats both the Mn-only arm and the free-drug arm;
- PSLN-344 is non-inferior to the IM benchmark on HI (lower 95% bound of the GMT ratio ≥0.67) **and** superior to it on mucosal IgA or heterosubtypic protection;
- the benefit is present in both sexes.

**Stop if:**

- PSLN-344 survival is <50%, or does not differ from PSLN-212; **or**
- the IM benchmark equals or beats PSLN-344 on every endpoint, leaving no differentiation.

## G1b. Mechanism confirmation (in parallel with G1)

- **Must establish:** that the effect depends on STING, and what roles cGAS and IFNAR play. Mn²⁺ can also act through cGAS. Our data show IFNAR dependence only for moDC formation [S02-H] and do not address STING at all.
- **Design:** Sting1^gt/gt^ or Sting1⁻/⁻, Cgas⁻/⁻ and Ifnar1⁻/⁻ mice against wild-type. Young mice are acceptable here, with an aged wild-type bridge.
- **Endpoints we need to see:** Ifnb1 at 16 h; Gm-csf at 36 h; moDC at day 3; HI at day 14; survival.
- **Go:** in Sting1⁻/⁻ mice, ≥80% of the Ifnb1 induction and ≥75% of the HI gain are lost. If they are not, we rewrite the MoA, the claims and the IP position before G2.

## G2. Safety de-risking of Mn²⁺ and STING agonism (months 4–12)

**Must establish:** an adequate margin for intranasal Mn²⁺ and a STING agonist in aged animals, after single and repeated doses.

**Why:**

- Manganese is a recognised neurotoxicant, and the nose-to-brain (olfactory) route is a known exposure path (external context).
- Our dataset has no Mn measurement at all.
- The only CNS readout we have [S10-A] is three transcripts at one time point.

**Design:**

- **(a) Mn distribution.** ICP-MS of olfactory bulb, striatum, globus pallidus, lung and blood at days 1, 7 and 28.
    - Doses: 1×, 3× and 10×, plus a 3-dose repeat schedule.
    - MnCl₂ as a positive control; T1-weighted MRI.
- **(b) CNS and facial-nerve inflammation** at 6 h, 36 h and 7 days, with cholera toxin as the comparator, extending S10-A.
- **(c) Local and systemic effects.** Lung and nasal histopathology; BAL; systemic IL-6, TNF, IFN-β and CXCL10.
- **(d) Dose-ranging** from 2.5 to 40 µg to find the MED for HI and survival. For reference, 20 µg already gives 91% of the Ifnb1 response seen at 40 µg [S08-A].

**Endpoints we need to see:**

- brain Mn compared with vehicle;
- histopathology;
- neurobehaviour;
- CNS Tnf, Il1b and Isg15;
- MED and NOAEL.

**Go if all of the following hold:**

- no increase in basal-ganglia Mn at 1×;
- no neuropathology at 3×;
- NOAEL ≥10× MED;
- the CNS Tnf signal is not confirmed. Today it is 1.59× PBS (p = 0.033 unadjusted; Tukey p = 0.12) [S10-A].

**If Mn fails G2:** evaluate the Mn-free fallback described in Section 9 (PSLN-212 plus GM-CSF) rather than stopping outright.

## G3. Translational model and delivery route (months 8–18)

- **Must establish:** that a human-relevant device reproduces the effect. In mice, intranasal instillation reaches the alveoli, and our MoA depends on alveolar cells (Section 5). A human nasal spray deposits mainly in the upper airway (external context).
- **Design:**
    - Species: ferrets (aged, if available) and/or aged NHP.
    - Arms: nasal spray vs aerosol, with an IM benchmark.
    - Deposition imaging.
- **Endpoints we need to see:**
    - HI and neutralising-antibody seroconversion;
    - nasal IgA;
    - nasal ISG signature and GM-CSF at 16–48 h;
    - viral shedding, clinical score and transmission.
- **Go:**
    - HI GMT ≥4× the unadjuvanted vaccine and non-inferior to the IM benchmark;
    - lower viral shedding;
    - acceptable tolerability.

## CMC (in parallel, months 0–12)

- **Must establish:** a characterised, stable product before GLP toxicology.
- **Endpoints we need to see:**
    - Encapsulation efficiency ≥80% (today 54.8 ± 5.1% [S08-B]), or else a specification for free drug.
    - Mn content and Mn:CDN ratio.
    - Size, PDI and zeta-potential specifications. The methods are described, but no data were supplied.
    - Lyophilised stability at 2–8 °C (product is stored at −20 °C today, with no stability data).
    - HA potency (SRID) in the co-formulated product.

## Biomarkers built into the gates

- G1 and G3 measure the Section 6 panel in the same animals that are later challenged:
    - ISG signature and CCL2 at 16 h;
    - GM-CSF at 36 h;
    - blood Tfh at day 7;
    - HI, neutralising titre and IgA at day 14.
- This converts arm-level associations into individual-level thresholds. Those thresholds become the candidate pharmacodynamic and immunogenicity endpoints for Phase 1.

# 3. How the asset looks: the evidence

**The asset.** CDN-1807 is a cyclic-dinucleotide STING agonist. Its vehicle is a pulmonary-surfactant-biomimetic liposome made of DPPC, DPPG, DPPE-PEG2000 and cholesterol. The two development forms differ only in Mn²⁺:

- **PSLN-212**: CDN-1807 in the liposome.
- **PSLN-344**: the same, with Mn²⁺ incorporated by coordination polymerisation.

**Comparators.**

- **CMP-204**: cGAMP in place of CDN-1807.
- **PSLN-R848**: the TLR7/8 agonist R848 in the liposome.
- **PSLN-212/R848**: CDN-1807 and R848 together.
- **"Sham"**: vaccine plus empty liposome. This is the vehicle control, called "vehicle" throughout.
- **"Vaccine" / "PBS"**: no liposome.

**Dosing.** Unless stated otherwise, every arm received 20 µg of adjuvant intranasally together with an inactivated vaccine: CA09 H1N1 (0.5 µg HA), Aichi H3N2 (1 µg HA), the bivalent combination of the two, or rgH5N1.

**Models.**

- Primary model: female BALB/c mice aged 20 months or more.
- Reference arm: young (7–8-week-old) mice given PSLN-212. This is the only young arm present in most blocks.
- One survival experiment each in aged C57BL/6 and aged Swiss Webster mice.
- A 14-month-old "imprinting" model with prior influenza infection.

**How I handled the data.**

- I parsed every value with hand-verified cell coordinates. That is 2,121 continuous values, 514 survival records and 3,472 body-weight records, each tagged with its source cell.
- I applied the stated methods: one- and two-way ANOVA with Tukey, Student's t, and log-rank. Welch and exact Mann–Whitney tests were added as robustness checks.
- Titres were analysed on a log₂ scale and qPCR fold-changes on a log₁₀ scale.
- Pooled survival was stratified by experiment (Appendix A).

## 3.1 Scorecard

| Dimension | What our data show (aged mice unless stated) | Confidence |
|---|---|---|
| Protection | Pooled survival: PSLN-344 68/80 (85%), PSLN-212 11/80 (14%), vehicle 1/80 (1%). Holds in all four integrity scenarios (Table 2b). | Strong signal, but 7 of the 11 experiments are flagged |
| Breadth | Homologous H1N1 7/7 [S03-I]; wild-type H5N1 10/10 [S03-J]; H3 vaccine → H1 challenge 6/7 [S06-A]; bivalent vaccine → H5 challenge 7/7 [S06-C]. | Moderate: n = 7–10; three of the four are flagged |
| Durability | Day-60 challenge: 5/7 and 5/7 vs 0/7 and 1/7 on PSLN-212 [S06-E, S06-F]. The third day-60 experiment [S06-G] is confounded by deaths among unchallenged controls. | Moderate |
| Speed of onset | Challenge 2–3 days after vaccination: 10/10 [S03-J], 5/7 [S06-B], 7/7 [S06-D]. PSLN-344 given without antigen: 0/7 [S15-H]. | Weak to moderate: S03-J, S06-D and S15-H are all flagged |
| Antibody response | HI 8.0–9.2×, neutralising titre 9.2×, IgG 13.4–18.6× over PSLN-212. HI reaches 76–87% of young [S03]. | Strong |
| Quality of response | Th1-skewed IgG2a/IgG1: 1.85–2.30 vs 0.46–0.54 on PSLN-212 [S13-A–D]. | Strong. S03-B/F not used (rotated labels, I-05) |
| T-cell response | IFN-γ⁺ CD8 4.2× at day 14 and 3.2× at day 60; lung TRM 4.0× [S05]. | Strong signal |
| Mechanism | A coherent cascade; four of its steps are supported by blocking, knockout or add-back experiments (Figure 4). | Moderate. STING dependence untested |
| Tolerability | Weight nadir 96.4% vs 98.2% for vaccine alone; no mouse lost ≥10% [S08-D]. CNS Ifnb1 and Isg15 not raised; CNS Tnf 1.6× (p = 0.033 unadjusted) [S10-A]. | Limited: n = 5, one time point, no histopathology, no Mn measurement |
| Vehicle (empty liposome) | Inert on its own: it did not change CNS Ifnb1, Tnf or Isg15 compared with buffer (p = 0.16–0.68) [S10-A]. Tracer data say it delivers to AECII and alveolar macrophages [S01-B/C]. Whether it improves on free drug has never been tested. | Inert: supported. Added value: untested |
| Manufacturability | Encapsulation efficiency 54.8 ± 5.1% [S08-B]. Size, charge and stability methods described, but no data supplied. | Weak |
| Where the value lies | In young mice, Mn adds nothing: PSLN-344(Y) 8/8 = PSLN-212(Y) 8/8 in three experiments [S09-B/D/F]. | Clear |
| Data integrity | 17 findings, 5 critical (Section 4). | Major risk |

## 3.2 Protection in aged mice

| Experiment | Challenge (day after vaccination) | Vehicle | PSLN-212 | PSLN-344 | Young ref. | p, 344 vs 212 (log-rank) | Flag |
|---|---|---|---|---|---|---|---|
| S03-I | 10× LD50 CA09 H1N1, homologous (d14) | 0/7 | 0/7 | 7/7 | 7/7 | 0.0004 | I-03 |
| S03-J | Wild-type VN04 H5N1 (d2) | 1/10 | 3/10 | 10/10 | – | 0.0014 | I-03, I-12 |
| S06-A | 5× PR8 H1N1 after H3 vaccine (d14) | 0/7 | 1/7 | 6/7 | 7/7 | 0.008 | – |
| S06-B | 5× PR8 H1N1 after H3 vaccine (d3) | 0/7 | 0/7 | 5/7 | 7/7 | 0.0009 | – |
| S06-C | 5× rgH5N1 after bivalent vaccine (d14) | 0/7 | 2/7 | 7/7 | 7/7 | 0.007 | I-07 |
| S06-D | 5× rgH5N1 after bivalent vaccine (d3) | 0/7 | 2/7 | 7/7 | 7/7 | 0.007 | I-03, I-07 |
| S06-E | 5× PR8 H1N1 (d60) | 0/7 | 0/7 | 5/7 | 7/7 | 0.002 | – |
| S06-F | 5× rgH5N1 (d60) | 0/7 | 1/7 | 5/7 | 7/7 | 0.009 | – |
| S06-G | 5× Perth H3N2 after H1 vaccine (d60) | 0/7 | 0/7 | 4/7 | 7/7 | 0.015 | I-06: unchallenged controls also 4/7 |
| S15-L | Aged C57BL/6; challenge not stated | 0/7 | 0/7 | 6/7 | 6/7 | 0.001 | I-01, I-14 |
| S15-N | Aged Swiss Webster; challenge not stated | 0/7 | 2/7 | 6/7 | 7/7 | 0.056 | I-14 |
| **Pooled (11 experiments)** | Stratified by experiment | **1/80** | **11/80** | **68/80** | **69/70** | **2 × 10⁻²¹** | |

*Table 2. Survivors/animals at the end of observation. Against vehicle, p ≤ 0.0011 in each of the 11 experiments; pooled stratified log-rank χ² = 148.2. Source: workbook sheets Aged_survival_by_experiment and Survival_pairwise.*

![Figure 1. Survival by arm in each aged-mouse experiment, with exact 95% CIs. Shaded rows carry an integrity flag.](/tmp/outputs/figures/fig1_survival_by_experiment.png)

| Integrity scenario | PSLN-344 | PSLN-212 | Vehicle | Risk difference, 344 vs 212 (Mantel–Haenszel) | p (CMH) |
|---|---|---|---|---|---|
| As recorded (11 experiments) | 68/80 | 11/80 | 1/80 | +71 points | 1 × 10⁻¹⁸ |
| Excluding the 7 flagged experiments (S06-A, B, E, F remain) | 21/28 | 2/28 | 0/28 | +68 points | 2 × 10⁻⁶ |
| Deaths inferred from paired weight records where they exist | 68/80 | 14/80 | 5/80 | +68 points | 1 × 10⁻¹⁶ |
| Worst case for PSLN-344 (most deaths for PSLN-344, fewest for comparators) | 66/80 | 15/80 | 5/80 | +64 points | 3 × 10⁻¹⁵ |

*Table 2b. Pooled survival under the four integrity scenarios (workbook sheet Pooled_survival_scenarios; Figure 2).*

![Figure 2. Pooled aged survival under the four integrity scenarios.](/tmp/outputs/figures/fig2_pooled_survival_scenarios.png)

**Other survival experiments:**

- **Prior infection.** In 14-month-old mice, PSLN-344 protected 6/7 with or without prior infection, against both PR8 and Perth challenges. PSLN-212 protected naive mice 0/7 in both challenges, and previously infected mice 4/7 (PR8) and 0/7 (Perth) [S06-E/F, rows 71–105].
- **Young mice.** Both formulations protected 8/8 in each of three challenges: PR8 and Perth at day 21, and rgH5N1 at day 180. Vehicle protected 0 of 23 [S09-B/D/F].
- **Antigen is required.** Challenged at day 3:
    - vaccine + PSLN-344: 6/7 survived;
    - vaccine alone: 0/7;
    - PSLN-344 alone: 0/7 [S15-H].

  PSLN-344 is not a stand-alone antiviral.
- **Versus young mice, protection is not fully restored.** Pooled survival was 58/70 (83%) for aged PSLN-344 vs 69/70 (99%) for young PSLN-212. Mantel–Haenszel risk difference 16 points, p = 0.004.

## 3.3 Immunogenicity: what Mn²⁺ adds

| Readout (day 14 unless stated) | Vehicle | PSLN-212 | PSLN-344 | Young ref. | 344 vs 212 | Aged 344 as % of young |
|---|---|---|---|---|---|---|
| HI titre, H1N1 (GMT) [S03-C] | 7.6 | 46 | 368 | 485 | 8.0× (p = 0.0004) | 76% |
| HI titre, H3N2 (GMT) [S03-G] | 10 | 35 | 320 | 368 | 9.2× (p = 0.0002) | 87% |
| Neutralising titre, H1N1 (GMT) [S03-D] | 52 | 418 | 3,840 | 6,686 | 9.2× (p = 0.002) | 57% |
| Neutralising titre, H3N2 (GMT) [S03-H] | 40 | 276 | 2,533 | 4,411 | 9.2× (p = 0.0004) | 57% |
| IgG, H1N1 (GMT) [S03-A] | 56 | 393 | 7,305 | 11,959 | 18.6× (p < 0.0001) | 61% |
| IgG, H3N2, day 28 after boost (GMT) [S13-J] | 101 | 1,086 | 12,435 | 43,472 | 11.5× (p = 0.0008) | 29% |
| IgG2a/IgG1, H1N1 (GM) [S13-A/B] | – | 0.54 | 1.85 | 2.50 | 3.4× (p = 0.007) | – |
| Tfh ICOS-high, MLN, day 7 (%) [S04-A] | 0.30 | 3.8 | 10.3 | 13.6 | 2.7× (p = 0.009) | 75% |
| Germinal-centre B cells, day 7 (%) [S03-K] | 1.2 | 2.3 | 6.5 | 9.8 | 2.8× (p = 0.002) | 67% |
| IFN-γ⁺ CD8, H5N1 restimulation, day 14 (%) [S05-F] | 0.67 | 1.5 | 6.4 | 9.2 | 4.2× (p = 0.0001) | 69% |
| IFN-γ⁺ CD8, day 60 (%) [S05-G] | 1.5 | 3.0 | 9.9 | 14.4 | 3.2× (p = 0.003) | 69% |
| Lung CD8 TRM, day 25 (%) [S05-I] | 0.58 | 1.0 | 4.0 | 6.0 | 4.0× (p < 0.0001) | 66% |

*Table 3. n = 5 per arm; GMT/GM = geometric mean. p = Welch test on the analysis scale (log₂ for titres); Tukey-adjusted p values are in the workbook sheet Continuous_contrasts.*

![Figure 3. PSLN-344 vs PSLN-212 in aged mice across the immune cascade (ratio of geometric means with 95% CI), and aged PSLN-344 as a percentage of the young reference.](/tmp/outputs/figures/fig3_forest_344_vs_212.png)

**What the immunogenicity data show.**

- **Mn is the active difference.** PSLN-344 exceeds PSLN-212 on every adaptive readout in Table 3, all with p ≤ 0.009.
- **Without Mn, aged responses stay far below young.** PSLN-212's HI GMT is 46 and 35, about 9.5% of the young values.
- **"Restores young immunity" overstates it.** Depending on the readout, aged PSLN-344 reaches only:
    - 29–38% of young for DC co-stimulation (CD40/CD86 on MLN DCs) [S02-D];
    - 29–61% for IgG;
    - 57% for neutralising titre;
    - 76–87% for HI.
- **Payload.** Without Mn, CDN-1807 beats cGAMP.
    - Ifnb1 at 16 h: 16.6× vs 7.8× (p = 0.0003) [S01-A].
    - cGAMP's dose–response plateaus near 9×; fitted Emax 9.0 ± 1.0 [S08-A].
    - Day-14 titres were 1.1–2.3× higher with CDN-1807, but no difference was significant (Welch p = 0.056–0.67) [S03].

## 3.4 Tolerability

These are the only tolerability data available.

**Body weight after vaccination** [S08-D; n = 5 aged mice per arm].

- PSLN-344 caused a small, transient dip:
    - nadir 96.4 ± 1.5% vs 98.2 ± 1.1% for vaccine alone (p = 0.065);
    - no mouse lost 10% or more;
    - back to 99.8% by day 10.
- PSLN-212/R848 was clearly worse:
    - nadir 90.0 ± 5.0%;
    - 4 of 5 mice lost at least 10%;
    - weights were still falling at day 10;
    - one mouse has no day-10 record.

**CNS transcripts 36 h after nasal dosing** [S10-A].

- PSLN-344 did not raise Ifnb1 (group mean 1.32× vs PBS 1.00×, p = 0.20) or Isg15 (1.13×, p = 0.39).
- Cholera toxin, the positive control, raised all three transcripts: 2.7–5.5×, p ≤ 0.0008.
- CNS Tnf had a group mean of 1.59× vs PBS (Welch p = 0.033; Tukey p = 0.12). This is a weak signal that G2 must follow up.

**Never measured:**

- Mn in brain or olfactory bulb;
- lung or nasal histopathology;
- systemic cytokines;
- repeat dosing;
- male animals.

![Figure 6. Available tolerability data: post-vaccination weight (S08-D) and CNS transcripts (S10-A).](/tmp/outputs/figures/fig6_safety.png)

# 4. Data-integrity findings

I recommend the project present this section to the committee itself.

| ID | Severity | Finding (short form; full evidence in the workbook sheet Integrity_findings) | Consequence |
|---|---|---|---|
| I-01 | Critical | Weight curves recycled across experiments described as independent. S15-I "vaccine + PSLN-344" matches S15-C PSLN-344 on 40 of 42 day-2–12 values. Young C57BL/6 weights in S15-M match young BALB/c weights in S09-E to 8 decimal places. 26 cross-block trajectory pairs share ≥3 distinct values. | The weight records do not support the rapid-onset result [S15-H] or the C57BL/6 result [S15-L] |
| I-02 | Critical | Alveolar-macrophage % [S11-A] and neutrophil % [S11-B] share 35 of 100 animal-level values. Other panel pairs on the same sheet share 0–1 of 100. | S11-A/B excluded |
| I-03 | Critical | Survival tables contradict their paired weight tables. S03-I shows PSLN-212 7/7 dead by day 6, while S13-F has weights for all 7 through day 14, with 3 recovering. Similar conflicts in S03-J vs S13-G and S06-D vs S15-D. The group sets also differ. | S03-I, S03-J and S06-D outcomes uncertain |
| I-04 | Critical | Epithelial-uptake values shared between S01-B and S08-C, even though these are different experiments, gating strategies and formulations. | The delivery claim is not independently supported |
| I-05 | Critical | The printed IgG2a/IgG1 ratios [S03-B/F] are quotients of the S13 titres, but with group labels rotated. Read as printed, PSLN-344 would look Th2-skewed (GM 0.54) rather than Th1-skewed (1.85). | S13 used instead |
| I-06 | Major | 4 of 21 unchallenged, unvaccinated aged controls died within 14 days without prior weight loss [S06-E, S06-G; S15-E/G]. | Background mortality; S06-G uninterpretable |
| I-07 | Major | The PSLN-212 survival vector is identical in S06-C and S06-D (deaths on days 5, 8, 10, 10, 12). | Possible duplicated arm |
| I-08 | Major | The S09-A Ifnb1 rows are log₁₀ of S01-A animals. The second block is labelled 16 h but matches 72 h. | Not independent replication |
| I-09–I-11 | Major | Duplicated day-12 row in S09-C; Tfh:Tfr computed as (100 − Foxp3%)/Foxp3%; weights of dead animals carried forward in some groups and removed in others. | Corrected or excluded |
| I-12–I-17 | Moderate or minor | Stated n ≠ observed n [S03-J, S13-E, S05-A/B]; duplicate block labels [S06]; ambiguous S07-C labels; unlabelled region [S08 rows 89–101]; challenge not stated [S15-L/N]; HI "0" below the limit of detection; MHC-strain questions for the NP-tetramer and OT-I assays. | Metadata to be corrected |

![Figure 5. Examples of the integrity findings.](/tmp/outputs/figures/fig5_integrity_examples.png)

**How the analysis handled them.**

- Excluded: S07-C, S08 rows 89–101, S11-A/B.
- For IgG subclasses, the S13 source titres replace S03-B/F.
- Derived blocks (S09-A; Tfh:Tfr) are not counted as independent evidence.
- The survival conclusion was tested under four reconciliation scenarios (Table 2b), and it holds under all four.

**What the analysis cannot rule out.** Copying and contradictions found in the weight tables could also affect the survival tables. Only an audit against primary records (G0) can settle this.

# 5. Mechanism of action, built from our data

![Figure 4. MoA reconstructed from the dataset. Thick borders mark steps tested by a blocking, knockout or add-back experiment.](/tmp/outputs/figures/fig4_moa.png)

**Proposed MoA.**

1. **Ageing blunts the response to the CDN.** Aged lungs given PSLN-212 induce Ifnb1 16.6×, against 37.6× in young lungs (p < 0.0001). Adding Mn²⁺ (PSLN-344) restores it to 37.1×, indistinguishable from young (p = 0.82) [S01-A]. PSLN-344 also induces GM-CSF, which PSLN-212 barely does (8.7× vs 1.6×) [S02-F].
2. **Monocytes are recruited.** Type-I IFN and GM-CSF bring in CCR2⁺ monocytes.
3. **They become moDCs.** The monocytes develop into antigen-presenting moDCs in a way that depends on IFNAR and GM-CSF, rather than becoming macrophages.
4. **DCs prime the adaptive response.** The DCs migrate to the mediastinal lymph node and prime CD8 T cells, Tfh cells and germinal-centre B cells.
5. **Outcome.** Neutralising, Th1-skewed antibody, lung TRM, and survival.

| Step | Evidence from our data | Evidence type |
|---|---|---|
| 1. Delivery | AECII uptake 15.8% vs 0.38% for free dye (p = 0.0001) [S01-B]. Alveolar-macrophage uptake depends on SP-A/SP-D: 43.1% vs 12.7% in Sftpa1/Sftpd⁻/⁻ (p < 0.0001) [S01-C]. | Tracer only; S01-B values reappear in S08-C (I-04) |
| 2. IFN and GM-CSF | Ifnb1 at 16 h: 37.1× vs 16.6× vs 1.0×; young 37.6× (p < 0.0001) [S01-A]. Gm-csf at 36 h: 8.7× vs 1.6× (p < 0.0001) [S02-F]. Ccl2 ≈ 590× at 16 h [S09-A]. | Formulation comparison. **No Sting⁻/⁻ or Cgas⁻/⁻ test** |
| 3. Monocyte recruitment | Day 4: 30.6% vs 16.7% vs 10.4% [S01-D]. CCR2 antagonist: 9.9% → 3.3% (p = 0.001) [S07-B]. Gap-junction blocker carbenoxolone: 7.3% → 3.1% (p = 0.004) [S11-C]. | Perturbation |
| 4. moDC differentiation | IFNAR⁻/⁻ precursors: 2.1% vs 19.7% (p = 0.0004); GM-CSF rescues to 12.4% [S02-H]. GM-CSF added to PSLN-212: 5.9% → 13.8% (p = 0.002) [S02-G]. Without Mn, monocytes instead accumulate as Ly6C⁺CCR2⁺ macrophages: 19.0 vs 3.4 ×10⁵ at day 5 (n = 3) [S07-A]. CD206⁺ macrophages 49% vs 71% [S11-E]. | Perturbation (knockout, add-back) |
| 5. DC migration and priming | CCR7⁺ migratory DCs 30.7% vs 7.3% [S02-A]. Antigen⁺ DCs in MLN 7.1% vs 1.8%; pertussis toxin (PTX) cuts this to 2.4% [S02-C]. OT-I priming 18.7% vs 0.8% [S02-E]. In-vivo MLN priming 30.9% → 6.8% with PTX [S05-C]. | Perturbation; OT-I donor strain to confirm (I-16) |
| 6. Tfh and germinal centre | Tfh 10.3% vs 3.8% [S04-A]. Tfr 10.8% vs 26.7% [S04-B]. GC B cells 6.5% vs 2.3% [S03-K]. Aicda 12× vs 3.4× [S03-L]. | Correlative |
| 7. CD8 effector and memory | GZMB⁺ CD8 5.7% vs 3.0% on day 3 [S05-E]; CCR2 blockade cuts it from 6.8% to 1.4% (young) [S02-I]. TRM 4.0% vs 1.0% [S05-I]. | Perturbation (in young mice) |

**What is established in our data:**

- that Mn makes IFN-β and GM-CSF induction possible in aged lungs (a formulation comparison);
- the downstream chain from CCR2 monocytes, through IFNAR/GM-CSF-dependent moDCs, to DC migration and priming. Each of these links has a blocking, knockout or add-back experiment behind it.

**What is inferred, not shown:**

1. **STING dependence.** Mn²⁺ could act through cGAS or other pathways.
2. **Synergy between Mn and CDN-1807.** There is no Mn-only arm.
3. **Any benefit of the liposome over free drug.** There is no free-CDN arm.

Regulators will expect the contribution of each component of a combination adjuvant to be justified (external context). These three gaps are the G1 and G1b controls.

# 6. Biomarkers to validate efficacy

**All 18 candidate markers separate PSLN-344 from PSLN-212 in aged mice.**

- The animal-level AUC is 0.98–1.00. For Tfr, where lower is better, separation is complete in the opposite direction.
- 17 of the 18 rank the arms in the same order as survival: vehicle < PSLN-212 < PSLN-344 < young (workbook sheet Biomarker_candidates).

The markers therefore differ mainly in timing, translatability to humans and dynamic range (Figure 7).

![Figure 7. Candidate biomarkers by time point.](/tmp/outputs/figures/fig7_biomarker_timeline.png)

| Tier and timing | Marker (mouse evidence) | Human assay | Decision use |
|---|---|---|---|
| Target engagement, 16–24 h | Lung Ifnb1 37× vs 17× (Hedges g 5.6) [S01-A]; CCL2 ≈ 590× (g 5.6, n = 3) [S09-A] | Interferon-stimulated-gene (ISG) signature and CCL2 (MCP-1) in nasal-lining fluid and blood | Confirms the drug hits its target; dose selection |
| Mn-specific pharmacodynamics, 24–48 h | Gm-csf 8.7× vs 1.6× (g 7.9, the largest separation of any candidate) [S02-F] | GM-CSF in nasal-lining fluid | **Confirms the Mn-specific step that distinguishes PSLN-344** |
| Early adaptive, day 7 | Tfh 10.3% vs 3.8% [S04-A]; Tfr 10.8% vs 26.7% [S04-B]; GC B cells 6.5% vs 2.3% [S03-K] | Circulating Tfh (CXCR5⁺PD-1⁺ICOS⁺), cTfh:cTfr ratio, plasmablasts | Early read on germinal-centre quality |
| Antibody, day 14–28 | HI GMT 368/320 vs 46/35 [S03-C/G]; neutralising titre 9.2× [S03-D/H] | HI, microneutralisation; nasal IgA (not yet measured) | **Primary immunogenicity endpoint** |
| Breadth and durability, day 14–60+ | IFN-γ⁺ CD8 6.4% vs 1.5% (day 14), 9.9% vs 3.0% (day 60) [S05-F/G] | IFN-γ ELISpot against conserved NP/M1 peptides | Supports a broader-protection claim |

**Threshold.** In aged mice, an HI titre of 160 or more separated protected arms from unprotected ones:

- all 10 PSLN-344 and all 10 young titres were ≥160;
- none of the 30 vehicle, PSLN-212 or CMP-204 titres reached 160 [S03-C, S03-G].

The conventional human cut-off of 1:40 would not have separated them: 8 of 10 PSLN-212 titres were ≥40, yet PSLN-212's pooled aged survival was 14%.

**Caveat.** These are arm-level associations only, because the biomarkers and challenge outcomes come from different mice. G1 fixes this by measuring both in the same animals.

# 7. Target demographic for the TAM check

| Segment | Definition for market research | Support in our data | Status |
|---|---|---|---|
| **Primary** | Adults **≥65** eligible for annual seasonal influenza vaccination. Start with community-dwelling 65–85-year-olds; extend to ≥85 and long-term-care residents later. | The Mn benefit appears only in aged mice: 85% vs 14% survival (aged) against 8/8 = 8/8 (young) [S09]. | Lead indication |
| **Secondary** | Pre-pandemic and pandemic **H5N1** preparedness: government stockpiles, with older adults prioritised. | Wild-type H5N1 10/10 vs 3/10 [S03-J]; rgH5N1 7/7 vs 2/7 [S06-C]; protection at day 3 [S06-D, S15-H]. All flagged. | Option value; depends on G1 |
| Exploratory | Adults **50–64**. | One experiment in 14-month-old mice: PSLN-212 0/7 vs PSLN-344 6/7 in naive mice [S06-E/F, rows 71–105]. | Needs age-bridging data |
| Not targeted | Children and adults under 50; immunocompromised people; treatment after infection. | No Mn benefit in young mice [S09]; no data for the other groups. | Excluded |

**Context for market research.** None of the following comes from our data, and none is used in the recommendation; all figures are approximate and should be verified.

- **Age mapping.** Mice aged 18–24 months are conventionally equated with humans aged roughly 56–69, and 14-month-old mice with middle age.
- **Population and coverage:**
    - US adults aged ≥65: roughly 58–62 million, with about 70% influenza-vaccine coverage;
    - EU-27 adults aged ≥65: about 95 million, with coverage varying widely by country;
    - Japan adults aged ≥65: about 36 million.

**Questions for market research:**

1. What share of the enhanced older-adult segment (high-dose, adjuvanted and recombinant vaccines) could a needle-free intranasal product take?
2. What price premium would a broader-protection claim support?
3. What does the current −20 °C storage requirement cost commercially?
4. How large is the H5N1 stockpile opportunity?

# 8. If we drop it: exactly what we give up, and why dropping could still be right

**What we give up** (all figures from our data):

1. **The only formulation in our data that consistently protects aged animals.** Pooled survival was 68/80, vs 11/80 for PSLN-212 and 1/80 for vehicle. With every flagged experiment removed, it is still 21/28 vs 2/28 vs 0/28.
2. **Breadth in aged mice:**
    - wild-type H5N1: 10/10 [S03-J];
    - subtypes absent from the vaccine: 6/7 [S06-A] and 7/7 [S06-C];
    - protection at day 60: 5/7 and 5/7 [S06-E/F].
3. **Near-young immunogenicity plus airway T-cell memory:**
    - HI at 76–87% of young, 8–9× PSLN-212;
    - IFN-γ⁺ CD8 T cells 4.2× and lung TRM 4.0× PSLN-212.

   Injectable older-adult vaccines are not designed to induce airway TRM (external context).
4. **A Mn-dependent mechanism that differentiates PSLN-344 from PSLN-212.** IFN-β restored in aged lungs, plus GM-CSF → moDC. This can underpin IP, and it carries option value for H5N1 preparedness.

**Why dropping could still be right:**

1. If G0 cannot reconcile the records, none of the evidence above can be relied on.
2. Mn²⁺ is a recognised neurotoxicant, and its nose-to-brain transfer has not been measured for this formulation.
3. The MoA depends on alveolar cells, which a human nasal spray may not reach.
4. Everything rests on one species and one sex.

**The gates answer exactly these questions before any large spend.** If the committee is not willing to fund G0 and G1, dropping the asset is the defensible alternative; keeping it without funding is not.

# 9. What I considered and ruled out

| Option or analytical choice | Decision | Reason (from our data) |
|---|---|---|
| Advance PSLN-212 (no Mn) for older adults | Ruled out | Pooled aged survival 14% vs 1% for vehicle. The gain over vehicle is only 7–13 points, and not significant once flagged experiments are excluded (CMH p = 0.48). HI GMT 46/35, about 9.5% of young. |
| Either formulation for young adults or children | Ruled out | No Mn advantage in young mice: 8/8 vs 8/8 in three experiments [S09]. No differentiation. |
| R848 combinations (PSLN-R848, PSLN-212/R848, PSLN-344/R848) | Ruled out | PSLN-R848 gave Ifnb1 of only 5.1× [S01-A]. PSLN-212/R848: weight nadir 90.0%, with 4/5 mice losing ≥10% [S08-D]; its Il6, Tnf and Il10 were still high in the second S09-A block (probably 72 h). PSLN-344/R848 gave lower Ifnb1 than PSLN-344 alone: 29× vs 46× at 20 µg [S08-A]. |
| cGAMP payload (CMP-204) | Ruled out | Half the Ifnb1 of CDN-1807 (7.8× vs 16.6×, p = 0.0003); dose–response plateaus at an Emax of about 9 [S01-A, S08-A]. |
| PSLN-344 as an antigen-free antiviral | Ruled out | 0/7 survival, the same as vaccine alone [S15-H]. |
| Claim that PSLN-344 "restores young immunity" | Ruled out as an overclaim | It reaches 29–87% of young depending on readout; pooled survival 83% vs 99% (p = 0.004). |
| Drop now | Considered; not recommended | The effect survives every integrity scenario (+64 to +71 points over PSLN-212), and it can be verified before any large spend. Becomes the recommendation if G0 or G1 fails. |
| Go straight to IND-enabling toxicology and scale-up | Ruled out | Premature. The integrity findings are unresolved; STING dependence, the Mn-only control and Mn distribution to the CNS are all untested; there are no large-animal data and no decision on route or device. |
| Take the dataset to partners now | Ruled out until G0 is complete | Due diligence would find the same 17 findings. |
| Use S03-B/F ratios, S09-A, S04-B Tfh:Tfr, S11-A/B, S13-F/G, S15-I/M weights, S07-C or S08 rows 89–101 as evidence | Excluded | Rotated labels, derived or duplicated values, or unlabelled data (Section 4). |
| Use S06-G as evidence of day-60 protection, for or against | Excluded | Unchallenged controls survived 4/7, the same as PSLN-344 [S06-G]. |
| Adopt the human HI ≥1:40 threshold as protective | Not supported in aged mice | PSLN-212 met it (8/10 titres ≥40), but its pooled survival was 14%. |
| Keep PSLN-212 as the Mn-free back-up | Ruled out as is; a back-up concept is noted | PSLN-212 alone fails in aged mice (Section 3.2). But the MoA data point to GM-CSF as the missing factor: adding it to PSLN-212 raised moDC from 5.9% to 13.8% (p = 0.002) [S02-G], and it rescued IFNAR⁻/⁻ moDC [S02-H]. A GM-CSF-supplemented, Mn-free formulation is the logical fallback if G2 fails on Mn. It has not been tested for protection. |

# Appendix A. Methods

**Parsing.** Every block was read from hand-verified cell coordinates (code in `code/parse.py`). Values were kept as printed. Group labels were normalised only for suffixes (e.g. "PSLN-212Y" → "PSLN-212(Y)"); the printed labels are retained in the workbook.

**Scales.**

- Titres: log₂. HI values below the limit of detection were set to 5.
- qPCR fold-changes: log₁₀.
- Percentages and counts: linear, following the stated methods.

**Tests.**

- One-way ANOVA with Tukey HSD across all groups in a block.
- Welch and Student's t for pre-specified contrasts.
- Exact Mann–Whitney U as a robustness check.
- Hedges g as the effect size.
- Two-way ANOVA (group × time) for time courses.
- For each experiment: Kaplan–Meier, log-rank and Fisher's exact.
- Pooled across experiments: Mantel–Haenszel risk difference, Cochran–Mantel–Haenszel test and log-rank, all stratified by experiment.
- Clopper–Pearson 95% CIs.
- Sample sizes: exact Fisher power by full enumeration; t-test power for HI, using the pooled log₂ SD of 0.66 from our data.

**Integrity checks.**

- Positional and any-position duplicate values across blocks.
- Derived blocks compared against their sources.
- Each survival block reconciled with its paired weight block; trajectories that stop or flat-line were counted as deaths.
- Trajectory matching across blocks: flagged if ≥3 distinct values are shared.

**Limitation.** No raw instrument files were supplied, so nothing could be checked against primary data.

# Appendix B. Deliverables

- `PSLN_portfolio_proposal.docx` and `.pdf`: this proposal.
- `PSLN_analysis_tables.xlsx`: every table behind every number, plus tidy data with source cells.
- `figures/`: Figures 1–7.
- `code/`: all scripts needed to reproduce the analysis, figures and documents.
