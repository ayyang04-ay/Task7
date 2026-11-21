---
title: "PSLN-344 (CDN-1807 in a Mn²⁺ surfactant-biomimetic liposome): portfolio review proposal"
subtitle: "Recommendation, evidence, mechanism, biomarkers, next studies and target demographic"
date: "1 November 2026"
---

**Data basis.** *psln_program_dataset.xlsx* (workbook last modified 3 Sep 2026) and *psln_program_annotation.pdf* (15 Sep 2026). No external data were used for any efficacy, safety or mechanism number. Every statistic below was recomputed from the per-animal values in the workbook.

**How to check a number.** Each number carries a source tag:

- **[S06-A]** is a workbook block. Its exact cell range is listed in the *Source_map* tab of *PSLN_analysis_workbook.xlsx*.
- **[T3]** is an analysis table in the same workbook.
- **[A1]** is a finding in the data-integrity audit log (Appendix B).

"Aged" means female BALB/c mice aged 20 months or more; "young" means 7–8 weeks, as defined in the annotation. External facts used only for context are marked *(external)*.

---

# 1. Recommendation

> **Keep PSLN-344 in the portfolio as the single lead asset, and discontinue PSLN-212 as a development candidate. Do not release IND-enabling funding yet.** Fund an eight-month verification stage with three pre-defined gates. If the gates fail, terminate.

**What the committee is being asked to approve.** The proposal is a *conditional keep*. PSLN-344 is the only formulation in our data that protects the target population. However, the dataset has serious integrity defects, and the manganese component has not yet been tested for safety. The next money should buy certainty, not scale.

**Asset scorecard (PSLN-344)**

| Dimension | Assessment | Key evidence |
|------------|----------|--------------------|
| Efficacy in the target population (aged) | **Strong, if verified** | Survival 84% vs 12% (PSLN-212) and 1% (sham) [T3-B]; robust to worst case: +65 points (53–78) [T3-C] |
| Breadth, onset, durability | **Strong** | Heterosubtypic; protection with challenge at d3 and d60 [S06-B/E/F/G]; 3 mouse strains [S15-L/N] |
| Mechanism | **Coherent, partly causal** | Mn²⁺ raises Ifnb1 Emax 3.4× [T10]; GM-CSF/IFNAR-dependent moDC step [S02-G/H] (Fig 4) |
| Differentiation vs standard of care | **Unknown** | No licensed or benchmark comparator in any experiment [A17] |
| General tolerability | **Acceptable so far (limited data)** | Post-vaccination weight nadir 96.4% vs 97.0% for PSLN-212 [T8]; CNS transcripts equal to sham [T7] |
| Local reactogenicity | **Higher than PSLN-212** | Lung Il6 6.5×, Ccl2 77×, Tnf 2.6× at 16 h [T6] |
| Mn²⁺-specific safety | **Unknown: the key risk** | No Mn dose, biodistribution, histopathology or neurobehaviour data [A17] |
| CMC maturity | **Early** | Encapsulation 54.8%; no size, zeta, Mn-content or stability data [S08-B; A17] |
| Data integrity | **Critical issues** | Duplicated survival block, copied flow and body-weight values [A1–A3] |
| Human translatability | **Untested** | No human-cell or STING-variant data; mouse dosing reached the alveoli [A17] |

## 1.1 Why keep PSLN-344 (if the data hold)

1. **It works where PSLN-212 fails: in aged animals.**
   - Across 10 de-duplicated lethal-challenge experiments in aged mice, PSLN-344 protected **84% (61/73)**. PSLN-212 protected **12% (9/73)** and sham **1% (1/73)**.
   - The Mantel–Haenszel survival difference versus PSLN-212 is **+71 points (95% CI 60–82)** [T3-B].
   - The advantage holds in every sensitivity analysis built around the integrity findings: **+65 (53–78)** and **+69 (52–85)** points [T3-C, T3-D; Fig 1].
2. **The protection is broad, fast and durable.**
   - *Broad:* it is heterosubtypic. H3N2 vaccine protected against H1N1 challenge, H1N1 vaccine against H3N2, and H1N1+H3N2 vaccine against H5N1 [S06-A/C/G].
   - *Fast:* it was present when challenge came 3 days after vaccination: **71% vs 0%** [S06-B].
   - *Durable:* it was present 60 days after vaccination: **57–71% vs 0–14%** [S06-E/F/G].
   - It held in three mouse genetic backgrounds [S15-L/N] and in animals with prior influenza imprinting [S06-E/F imprint].
3. **It repairs most of the age-related immune deficit.** PSLN-344 closes **80% (95% CI 69–91%)** of the survival gap between aged and young animals [T11]. The mechanism is coherent and partly tested by perturbation (Section 4).
4. **The proprietary agonist matters.** In the same liposome, CDN-1807 gives about 2× the Ifnb1 response of cGAMP (16.5 vs 7.7-fold; p<0.001) [S01-A]. Adding Mn²⁺ then gives 2.7× dose-sparing on that response: 7.3 µg PSLN-344 matches 20 µg PSLN-212 [T10].

## 1.2 Why not advance PSLN-344 now

1. **The data have integrity problems** [Appendix B; Fig 6]. These make the dataset hypothesis-generating until source records are checked.
   - An entire survival experiment is duplicated: S06-D is a cell-for-cell copy of S06-C [A1].
   - Two flow populations share copied values: 35 of 100 positions are identical, against a chance maximum of 19 [A2].
   - Body-weight series were copied across independent experiments: 68 shared high-precision decimal strings [A3].
   - Survival and body-weight records disagree in 10 group comparisons [A4].
   - Rotated labels reverse a conclusion: IgG subclass data *as printed* show PSLN-344 as Th2-skewed, when it is actually Th1-skewed [A6].
2. **The manganese-specific safety question is open.** There are no data on:
   - Mn dose per administration;
   - Mn biodistribution;
   - olfactory-bulb Mn;
   - histopathology;
   - neurobehaviour.

   The only CNS readout is three innate transcripts at 36 h [S10-A]. Intranasal Mn²⁺ is known to reach the brain along olfactory neurons in rodents *(external: Tjälve et al., Pharmacol Toxicol 1996)*. An intranasal adjuvant has previously been withdrawn over Bell's palsy *(external: LT-adjuvanted Nasalflu; Mutsch et al., NEJM 2004)*.
3. **Translational gaps.**
   - All animals were female and came from one facility.
   - There is no comparison with a licensed or benchmark older-adult vaccine.
   - There are no human-cell or human-STING-variant data.
   - Mouse intranasal instillation reaches the alveoli, where the carrier's targeting operates; a human nasal spray largely will not.

**Confidence statement.** Two questions need separate answers:

1. *If the data are genuine, is PSLN-344 better than PSLN-212 in aged animals?* **Yes, with high confidence.** The advantage is consistent across 10 challenge experiments, 3 mouse strains and about 40 immunological readouts, and it survives worst-case reconciliation [T3, T4].
2. *Are the data genuine?* **This cannot be determined from the dataset itself.** Resolving it is what Gates G1 and G2 are for. The recommendation is built to be right under either answer: a bounded cost if the data fail, and retention of the only older-adult candidate if they hold.

## 1.3 Gates (details and timing in Section 6)

| Gate | Due (planning estimate) | Pass criterion, and its basis in our data |
|--------|------|-----------------------------------|
| **G1: Data validity** | Month 3 | A1–A6 are root-caused from source records (death logs, balance print-outs, FCS files, plate maps), and ≥95% of efficacy endpoint values are traceable. |
| **G2: Independent replication** | Month 8 | In aged mice of both sexes, blinded, n=20/arm: PSLN-344 minus PSLN-212 survival is **≥40 points** with a 95% CI excluding 0. Basis: 40 is about 60% of the most conservative pooled estimate (65 points [T3-C]), and 11/20 vs 3/20 survivors gives exact Fisher p=0.019. PSLN-344 must also beat an injected benchmark in a heterosubtypic challenge. |
| **G3: Mn²⁺ neuro-safety and CMC** | Month 8 | Mn content per dose is specified. At the efficacious dose there is no olfactory-bulb or brain Mn above vehicle, no olfactory or CNS histopathology, no behavioural change, and no CNS interferon signature. Cholera toxin must remain detectable as the positive control (5.5-fold Ifnb1 in [S10-A; T7]). |

**Stop rules.** Terminate if any of the following occurs:

- the audit finds fabrication rather than transcription error;
- the replicated survival difference is **below 20 points**, or its 95% CI includes 0. A difference of 20–40 points triggers re-scoping, not advancement;
- Mn accumulation or a neuro finding occurs at the efficacious dose.

## 1.4 What we give up if we drop PSLN-344 today

- **The only older-adult candidate in the dataset.** PSLN-212 adds just 11 points of survival over sham in aged mice (12% vs 1%; 95% CI 3–19) [T3-H]. Young-animal data cannot be used instead, because in young mice PSLN-212 and PSLN-344 are both 100% protective [S09-B/D/F].
- **A heterosubtypic, rapid-onset, 60-day-durable mucosal adjuvant effect** in aged animals [S06-A…G].
- **An 8–19-fold humoral advantage in aged animals:**
  - IgG: 18.6× (CA09) and 13.4× (Aichi);
  - HAI: 8.0× and 9.2×;
  - neutralising antibody: 9.2×

  [T4]. There is also a **4.2-fold cross-reactive CD8 T-cell advantage** (IFN-γ⁺ CD8 after heterologous H5N1 restimulation: 6.36% vs 1.50%) [S05-F; T4].
- **A mechanism that supports biomarker-guided development** (Sections 4–5).

**What dropping would avoid:** the cost and eight months of the verification stage, exposure to an unquantified Mn²⁺ neuro-risk, and the reputational risk attached to the integrity findings.

---

# 2. Which asset? PSLN-344 vs PSLN-212

The two candidates differ in one respect only: PSLN-344 incorporates Mn²⁺ (annotation, Materials). Encapsulation efficiency of CDN-1807 is similar: 54.8% vs 59.6%, p=0.29 [S08-B; T9].

| Dimension (aged unless stated) | PSLN-212 | PSLN-344 | Source |
|------------|--------|----------|------|
| Survival, pooled, de-duplicated | 12% (9/73) | **84% (61/73)** | T3-B |
| Survival gap vs young PSLN-212 (98%, 62/63), same 9 experiments | −89 points (10% survival; 95% CI −97 to −81) | −17 points (81%; 95% CI −28 to −7) | T3-G, T3-I |
| Serum IgG CA09, d14 (GMT) | 393 | **7,310** | S03-A; T4 |
| HAI CA09, d14 (GMT) | 46 | **368** (young PSLN-212: 485) | S03-C; T4 |
| IgG2a:IgG1, CA09 (labels corrected) | 0.55 (Th2-leaning) | **1.85 (Th1-leaning)** | S03-B/S13-A,B; A6 |
| IFN-γ⁺ CD8, H5N1 recall, d14 | 1.50% | **6.36%** | S05-F; T4 |
| Lung Ifnb1, 16 h (fold) | 16.5 | **36.9** (young: 37.5) | S01-A; T4 |
| Post-vaccination weight nadir | 97.0% | 96.4% (Tukey p>0.99 vs PSLN-212) | S08-D; T8 |
| Lung Tnf / Il6, 16 h (fold) | 15.7 / 5.6 | 40.5 / 36.1 (higher inflammation) | S09-A; T6 |
| CNS Ifnb1/Tnf/Isg15, 36 h | not tested | not different from sham | S10-A; T7 |
| Young animals: survival | 100% (24/24) | 100% (24/24) | S09-B/D/F |
| Extra CMC or safety burden | none | **Mn²⁺: content, release, neuro-toxicology** | annotation; A17 |

**Verdict.** PSLN-344 is the better asset for the only population where an advantage exists. PSLN-212 should be kept only as the Mn-free control arm in future studies.

---

# 3. Evidence summary

## 3.1 Protection against lethal challenge (primary efficacy)

**Table 1. Survivors at end of observation, aged mice** [T1, T2; Fig 2]. Log-rank p is for PSLN-344 vs PSLN-212.

| Block | Model (vaccine → challenge, challenge day) | Sham | PSLN-212 | **PSLN-344** | Young PSLN-212 | Log-rank p |
|----|--------------------|---|----|----|----|----|
| S03-I | Bivalent → CA09 10×LD50 (homologous), d14 | 0/7 | 0/7 | **7/7** | 7/7 | 0.0004 |
| S03-J | rgH5N1 → wild-type VN04 H5N1, d2 (age not stated; n flag A9) | 1/10 | 3/10 | **10/10** | – | 0.001 |
| S06-A | Aichi H3N2 → PR8 H1N1, d14 | 0/7 | 1/7 | **6/7** | 7/7 | 0.008 |
| S06-B | Aichi H3N2 → PR8 H1N1, **d3** | 0/7 | 0/7 | **5/7** | 7/7 | <0.001 |
| S06-C | Bivalent → rgH5N1, d14 | 0/7 | 2/7 | **7/7** | 7/7 | 0.007 |
| ~~S06-D~~ | Bivalent → rgH5N1, d3: **exact copy of S06-C, excluded** [A1] | – | – | – | – | – |
| S06-E | Aichi → PR8, **d60** | 0/7 | 0/7 | **5/7** | 7/7 | 0.002 |
| S06-F | Bivalent → rgH5N1, **d60** | 0/7 | 1/7 | **5/7** | 7/7 | 0.009 |
| S06-G | CA09 → Perth H3N2, **d60** (untreated unchallenged controls 4/7 [A12]) | 0/7 | 0/7 | **4/7** | 7/7 | 0.015 |
| S15-L | Aged **C57BL/6**, bivalent (challenge not stated, A16) | 0/7 | 0/7 | **6/7** | 6/7 | 0.001 |
| S15-N | Aged **Swiss Webster**, bivalent (challenge not stated) | 0/7 | 2/7 | **6/7** | 7/7 | 0.056 |
| S06-E imprint | 14-month, PR8-naive / PR8-imprinted → PR8 | – | 0/7 / 4/7 | **6/7 / 6/7** | – | 0.002 / 0.23 |
| S06-F imprint | 14-month, naive / imprinted → Perth H3N2 | – | 0/7 / 0/7 | **6/7 / 6/7** | – | <0.001 / <0.001 |

**Pooled results and sensitivity analyses** [T3; Fig 1]:

| Analysis set | PSLN-344 | PSLN-212 | Survival difference (95% CI) |
|-----------------------|----|----|--------|
| A: all 11 aged experiments as recorded | 85% | 14% | +71 (61–82) |
| B: de-duplicated (S06-D removed) | 84% | 12% | **+71 (60–82)** |
| C: B, worst-case body-weight reconciliation, S03-J removed | 81% | 16% | +65 (53–78) |
| D: only experiments whose survival agrees with body weights | 80% | 11% | +69 (52–85) |
| E: 14-month animals, both imprinting strata | 86% | 14% | +71 (53–90) |

![Figure 1. Head-to-head survival, PSLN-344 vs PSLN-212, aged mice](figures/Fig1_forest_survival.png)

![Figure 2. Kaplan–Meier curves by experiment](figures/Fig2_KM_panels.png)

**Other survival findings:**

- **PSLN-344 is an adjuvant, not a stand-alone prophylactic.** With challenge 3 days after dosing, vaccine + PSLN-344 protected 6/7 animals. Vaccine alone protected 0/7, and PSLN-344 alone 0/7 (p<0.001 each) [S15-H].
- **Young animals show no difference between the formulations.** PSLN-344 and PSLN-212 each protected 8/8 against PR8 (d21), Perth H3N2 (d21) and H5N1 (**d180**); sham protected 0/8, 0/8 and 0/7 [S09-B/D/F]. In S13-E, young PSLN-344 and young CMP-204 each protected 7/7.
- **Caveat 1: background mortality in aged controls.** Unvaccinated, unchallenged 20-month-old mice died within 14 days in 4 of 21 cases (19%; 95% CI 5–42%) [A12]. In S06-G the untreated group (4/7 survived) matched the PSLN-344 group.
- **Caveat 2: the current design is underpowered.** With n=7 per arm, power was only about 55% at the conservative effect size [T12].

## 3.2 Immunogenicity (aged PSLN-344 vs aged PSLN-212) [T4; Fig 3]

**Antibody.**

- Serum IgG: **18.6×** against CA09 (95% CI 9.1–37.9) and **13.4×** against Aichi.
- HAI: **8.0×** (CA09) and **9.2×** (Aichi). Geometric mean titres (GMT) were 368 vs 46 and 320 vs 35; young PSLN-212 reached 485 and 368.
- Neutralising antibody: **9.2×** against both strains.
- Post-boost IgG at d28: 3.6× (CA09; Tukey p=0.19, not significant) and 11.5× (Aichi) [S13-I/J].

**Germinal-centre machinery.**

- Germinal-centre B cells: 6.5% vs 2.3%.
- ICOS-hi Tfh cells: 10.3% vs 3.8%.
- Aicda and E47 transcripts: 3.5× and 3.9× [S03-L; T9].
- Tfr cells (Foxp3⁺ within CXCR5⁺ICOS-hi): **10.8% vs 26.7%** (young PSLN-212: 7.1%).
- Lung Treg cells: 3.0% vs 6.7%.

**CD8 T cells.**

- Lung Ki-67⁺ cells, d3: 9.4% vs 3.5%.
- IFN-γ⁺ cells after heterologous H5N1 restimulation: 6.4% vs 1.5% at d14, and 9.9% vs 3.0% at d60.
- Lung resident-memory (TRM) cells, d25: 4.0% vs 1.0%.

**Restoration index** [T11]. This index measures what fraction of the young–aged gap PSLN-344 closes.

- It is **0.7–0.98** for innate, antigen-transport, antibody and Tfr readouts, in line with survival (0.80).
- It is lowest for **DC costimulation**: CD40 0.17 and CD86 0.22. CD40⁺ MLN DCs were 11.2% with PSLN-344 vs 38.7% in young animals [S02-D].
- It is also low for **early GZMB⁺ CD8 cells** (0.41).

These are the residual deficits a next-generation formulation would need to fix.

![Figure 3. Restoration index](figures/Fig3_restoration_index.png)

## 3.3 Safety and tolerability (limited)

- **Systemic tolerability after vaccination, without challenge** [S08-D; T8]:
  - Mean weight nadir was 96.4% for PSLN-344, 97.0% for PSLN-212 and 98.2% for vaccine alone; none of these differ (Tukey p≥0.86).
  - **PSLN-212/R848 caused weight loss:** nadir 90.0%, worst animal 84.7% (p=0.005 vs PSLN-344). One animal is unaccounted for at day 10.
  - Caveat: S08-D shares copied decimal strings with S15-F [A3].
- **Lung inflammation at 16 h** [S09-A block 1; T6]. PSLN-344 raised several transcripts relative to PSLN-212:

  | Transcript | PSLN-344 vs PSLN-212 | p |
  |---|---|---|
  | Il6 | 6.5× | 0.021 |
  | Ccl2 | 77× | 0.002 |
  | Ccl3 | 27× | 0.001 |
  | Ccl5 | 7.6× | 0.025 |
  | Tnf | 2.6× | 0.11 |

  Tnf with PSLN-344 was 2.9× the young PSLN-212 level. Expect more local reactogenicity than with PSLN-212. By 72 h, Ifnb1 had fallen to 4.2-fold [S01-A].
- **CNS at 36 h** [S10-A; T7]. Ifnb1, Tnf and Isg15 with PSLN-344 (1.32, 1.59, 1.13-fold) did not differ from sham (Tukey p 0.92–0.99). Cholera toxin raised them 5.5-, 3.5- and 2.7-fold (p≤0.001), so the assay can detect CNS inflammation. This is reassuring but narrow: one timepoint, one dose, an unspecified CNS region, and no Mn measurement.
- **Not available:** histopathology, lung or nasal viral load, neutrophil kinetics (S11-B is unusable [A2]), repeat-dose data and data in males.

## 3.4 CMC status

- **Encapsulation efficiency of PSLN-344 is 54.8% ± 5.1%** (n=3) [S08-B], so nearly half of the CDN is not encapsulated.
- **The workbook contains no particle size, zeta-potential, morphology, Mn-content or stability data.** The methods state that DLS and TEM were performed [A17].
- **"20 µg of adjuvant per animal" is not defined** as CDN mass or total particle mass.
- **One formulation in the dataset (PSLN-344/R848) is undocumented** [A14].

---

# 4. Mechanism of action, built from our data (Figs 4–5)

| Step | What happens | Key evidence (aged PSLN-344 vs PSLN-212 unless stated) | Evidence type; confidence |
|-----|--------|--------------------|-------|
| 1. Delivery | Surfactant-mimetic liposomes are taken up by AECII cells and by alveolar macrophages via SP-A/SP-D. | AECII uptake 15.8% vs 0.38% for free dye [S01-B]. Macrophage uptake 43.1% in WT vs 12.7% in Sftpa1⁻/⁻Sftpd⁻/⁻ mice [S01-C]. **However, the Mn particle is taken up 76–78% *less* by epithelium [S08-C], with a partial-overlap caveat [A13].** | Genetic KO; moderate. Mn's benefit is **not** explained by greater epithelial uptake. |
| 2. STING sensing and Mn²⁺ amplification | CDN-1807 induces IFN-β, and Mn²⁺ raises the maximum response rather than the potency. | Ifnb1 36.9× vs 16.5× at 16 h, equal to young animals (restoration 0.98) [S01-A]. Emax 52 vs 16 with similar EC50 (11.5 vs 9.5 µg); 7.3 µg PSLN-344 matches 20 µg PSLN-212 [S08-A; T10; Fig 5]. Consistent with Mn²⁺ sensitising cGAS–STING *(external: Wang et al., Immunity 2018)*. | Dose-response; moderate. **No STING-knockout control exists in the dataset.** |
| 3. Paracrine amplification | Gap-junction transfer, GM-CSF and chemokines spread the signal. | Carbenoxolone reduces recruited monocytes by 58% [S11-C]. Gm-csf 4.2–5.4× at 16–36 h [S02-F]. Ccl2 77×, Ccl3 27×, Ccl5 7.6× [S09-A]. | Pharmacological (carbenoxolone is not fully selective); moderate. |
| 4. Monocyte recruitment | Recruitment depends on CCR2. | Monocytes at d4: 30.6% vs 16.7% [S01-D]. INCB3344 reduces monocytes by 67% and Ly6C⁺ macrophages by 84% [S07-B]. Recruitment is only modestly IFNAR-dependent (21.3% vs 15.4%, p=0.12) [S12-A]. | Pharmacological; moderate. |
| 5. Differentiation to monocyte-derived DCs | Needs type I IFN plus GM-CSF; GM-CSF is limiting in the aged lung. | Ifnar⁻/⁻ marrow gives 2.1% vs 19.7% moDCs; GM-CSF rescues to 12.4% [S02-H]. GM-CSF added to PSLN-212 in aged mice raises moDCs from 5.9% to 13.8% [S02-G]. | Genetic plus rescue; strongest link. |
| 6. DC mobilisation and antigen transport | DCs carry antigen to the mediastinal lymph node via Gi/CCR7. | CCR7⁺ DCs 30.7% vs 7.3% [S02-A]. Antigen⁺ DCs in the lymph node 7.1% vs 1.8%; pertussis toxin reduces this by 67% [S02-C]. **CD40/CD86 are only about 20% restored** [S02-D]. | Pharmacological; moderate. |
| 7a. Follicular response | Stronger Tfh/germinal-centre activity drives class-switched, Th1-skewed antibody. | T-cell priming by lymph-node DCs 18.7% vs 0.8% [S02-E]. Tfh 10.3% vs 3.8%. GC B 6.5% vs 2.3%. IgG2a:IgG1 1.85 vs 0.55. | Correlative; moderate. |
| 7b. CD8 effector and memory | Cross-reactive CD8 responses and lung resident memory are raised. | IFN-γ⁺ CD8 6.4% vs 1.5%; TRM 4.0% vs 1.0% [S05]. GZMB⁺ CD8 is CCR2-dependent (−79%) [S02-I]. | Correlative plus pharmacological. |
| 7c. Regulatory brake | The suppressive macrophage/Treg environment of the aged lung is reduced. | Tfr 10.8% vs 26.7% [S04-B]. Lung Treg 3.0% vs 6.7% [S04-D]. CD206⁺ macrophages 48.9% vs 71.5% [S11-E]. Ly6C⁺CCR2⁺ macrophages −82% at d5 [S07-A]. **The causal transfer experiment S07-C cannot be read** [A11]. | Correlative only; weak-to-moderate. |
| 8. Protection | Protection requires antigen and is heterosubtypic, early and durable. | Vaccine + PSLN-344 6/7 vs PSLN-344 alone 0/7 [S15-H]. Survival restoration 0.80 [T11]. | Strong for antigen dependence. |

**In one sentence.** In the aged lung, the liposome delivers CDN-1807 to alveolar cells. Mn²⁺ raises the ceiling of the STING/IFN-β response and the GM-CSF it triggers. This lets CCR2⁺ monocytes become antigen-carrying DCs, which restore Tfh/germinal-centre and cross-reactive CD8/TRM responses while reducing the Treg/Tfr brake. The result is heterosubtypic, antigen-dependent protection.

**Mechanistic gaps to close:**

- a STING-knockout control;
- a Mn-only liposome (to separate Mn's own activity from its potentiation of CDN-1807; regulators will expect each component's contribution);
- relabelling of S07-C;
- the residual CD40/CD86 deficit.

![Figure 4. Mechanism of action](figures/Fig4_MoA_schematic.png)

![Figure 5. Ifnb1 dose-response](figures/Fig5_dose_response.png)

---

# 5. Biomarkers to validate efficacy

**Principle.** Our immunology and survival readouts come from *different animals*, so no readout can yet be called a correlate of protection. Below, candidates are ranked by three criteria: position in the mechanism, size and consistency of effect, and whether the same measurement can be taken in people. Validation at the level of individual animals is built into study WS2/WS7 (Section 6).

| Tier and timing | Candidate biomarker | What our data show | Human sampling | Role |
|-----|------|----------|-------|-----|
| **A. Pharmacodynamic / target engagement, 6–24 h** | IFN-β and interferon-stimulated genes (ISGs) | Ifnb1 2.2× PSLN-212; dose-responsive (EC50 ≈ 11.5 µg); matches young level (restoration 0.98) [T4, T10, T11] | Nasal mucosal lining fluid (nasosorption): IFN-β/IFN-λ, CXCL10; blood ISG score | Dose selection; confirms activation |
| | **GM-CSF (Csf2): the Mn-specific marker** | 4.2–5.4× PSLN-212 [S02-F]; the causal step [S02-G/H] | Nasal GM-CSF | Distinguishes PSLN-344 from PSLN-212 |
| | CCL2 | 77× [T6] | Nasal/serum MCP-1 | Monocyte recruitment |
| | Safety counter-markers: TNF, IL-6 | 2.6×, 6.5× [T6] | Nasal/serum cytokines | Reactogenicity ceiling |
| **B. Cellular mechanism, day 7** | Tfh:Tfr balance | Tfr 10.8% vs 26.7% (restoration 0.81); ICOS-hi Tfh 2.7× [T4, T11] | Circulating Tfh (CXCR5⁺PD-1⁺ICOS⁺) and circulating Tfr; plasmablasts | Early predictor of antibody response |
| **C. Immunogenicity, day 14–28** | HAI and microneutralisation (homologous strains) | 8–9×; restoration 0.80–0.94 [T4, T11] | Serum; established regulatory surrogates | Registrational immunogenicity |
| | IgG subclass / Th1 skew | IgG2a:IgG1 3.4–5.0× [T4] | IgG1/IgG3 profile | Quality of response |
| | Cross-reactive T cells to conserved NP/M1 | IFN-γ⁺ CD8 4.2× (d14), 3.2× (d60) [S05-F/G] | IFN-γ ELISpot or intracellular staining | **The correlate for heterosubtypic protection**, since HAI does not cross subtypes |
| | Mucosal IgA | **Not measured (gap)** | Nasal wash / nasosorption | Essential for an intranasal product |
| **D. Protection** | Survival, lung viral load, weight loss | Survival: T3. **Viral load not measured.** Body weight unusable [A3, A8] | Confirmed influenza (efficacy trials) | Final validation |

**Which candidates track protection?** At group level, the restoration indices for Ifnb1, monocytes, CCR7⁺ DCs, Tfr, IgG, HAI and neutralising antibody overlap the survival index of 0.80 (95% CI 0.69–0.91). CD40/CD86 (0.17–0.22) and early GZMB (0.41) do not [T11; Fig 3].

**Proposed lead panel to validate in WS7:**

1. IFN/ISG response (IFN-β, or CXCL10 as a human-measurable ISG proxy; CXCL10 was not measured in our data) plus GM-CSF, in nasal wash/BAL at 16–24 h;
2. blood Tfh:Tfr ratio at day 7;
3. HAI/microneutralisation plus mucosal IgA at day 14;
4. IFN-γ⁺ T cells to conserved NP/M1 at day 14.

**Success criterion:** a pre-specified marker predicts survival in individual animals with ROC AUC ≥ 0.75. This is a planning threshold.

---

# 6. Next steps: gated plan

**About timing.** Timings are planning estimates from standard in-life durations, not outputs of the dataset. Month 0 (M0) is committee approval. Aged mice (20 months or older) must be available at the start: if they have to be aged in-house from 7–8 weeks, add about 18 months. This is the single largest schedule risk, so the procurement decision is needed at M0.

**Overview**

| Workstream | Gate | Timing (planning) | Decision it informs |
|-----------|------|------|------------------|
| WS1: Forensic data audit | G1 | M0–M3 | Continue or stop at M3 |
| WS3: CMC characterisation (Mn dose, stability) | G3 | M0–M4 (stability ongoing) | Defines the dose used by WS4 and WS2 |
| WS5: Human-cell and STING-variant translatability | G3 (supporting) | M0–M4 | Human relevance; informs the first-in-human dose |
| WS4: Mn²⁺ olfactory/CNS safety pilot | G3 | M2–M7 | Go, re-scope or stop at M8 |
| WS2: Independent blinded replication and benchmark (WS7 biomarkers nested) | G2 | M1–M8 | Go, re-scope or stop at M8 |
| WS6: Delivery and device translation | G2 (supporting) | M3–M8 | Nasal spray vs inhaled product concept |
| WS8: Durability (d180), dose and regimen in aged mice | post-G2 | M3–M12 | Label and regimen assumptions |
| IND-enabling package | after G1–G3 | M9–M24 | First-in-human |

## WS1. Forensic data audit and source-data verification (Gate 1)

| Item | Specification |
|----|-----------------------|
| Must establish | Whether the existing dataset can support investment decisions |
| Population | All in-vivo blocks, with priority on A1–A6: S06-C/D, S11-A/B, the S15 and S13 body-weight blocks, S03-B/F and S09-A |
| Comparator | Source records: death and clinical-score logs, balance print-outs, animal census, FCS files and gating templates, ELISA plate maps, qPCR Ct exports, protocol PCL-26-0417 and its amendments |
| Endpoints / readouts | % of efficacy endpoint values traceable to source; root cause for each of A1–A17; corrected dataset; re-run of the provided scripts on the corrected data |
| Design | Independent QA (not the originating lab); interviews with data originators |
| Timing | M0–M3 |
| Go / no-go | **Go:** ≥95% traceable and A1–A3 explained as transcription or assembly errors. **Stop and escalate under the research-integrity policy:** evidence of fabrication. |

## WS2. Independent, blinded, randomised replication and benchmark differentiation (Gate 2)

| Item | Specification |
|----|-----------------------|
| Must establish | (1) That the aged-animal advantage of PSLN-344 over PSLN-212 is real. (2) That PSLN-344 (intranasal) beats an injected older-adult benchmark in a heterosubtypic challenge — the commercial differentiation claim. |
| Population | **Primary model:** aged BALB/c (≥20 months), 50% male. **Second model:** aged C57BL/6. **Reference:** young BALB/c. Both sexes because the current data are female-only [A17]. |
| Comparators / arms (primary model) | (1) Sham: empty liposome + vaccine. (2) PSLN-212 20 µg + vaccine. (3) PSLN-344 20 µg + vaccine. (4) PSLN-344 7 µg + vaccine; 7 µg matches PSLN-212 at 20 µg on Ifnb1 [T10]. (5) Intramuscular vaccine + squalene-emulsion (MF59-like) benchmark. (6) Mn-only liposome + vaccine, to show each component's contribution. (7) Unvaccinated, unchallenged aged controls, for background mortality [A12]. (8) Young PSLN-212. |
| Challenge models | **Primary:** Aichi H3N2 vaccine → PR8 H1N1 challenge at d14 (the S06-A model). **Second (aged C57BL/6; durability):** bivalent vaccine → rgH5N1 at d60 (the S06-F model). |
| Primary endpoint | Survival to day 14 after challenge, with a pre-specified humane endpoint, blinded assessors and necropsy confirmation of cause of death |
| Secondary endpoints / readouts | Lung viral titre at d3/d5 (satellite n=5/arm; not measured to date); weight-loss AUC with pre-specified handling of dead animals [A8]; HAI, microneutralisation, nasal IgA and IFN-γ ELISpot (NP/M1) at d13, before challenge |
| Sample size | **n=20/arm** for arms 1–6; n=10 for arms 7–8. Power is 99% at the conservative effect (81% vs 16%) and 91% at its lower 95% bound (69% vs 16%) [T12]. The current n=7 design had about 55% power [T12]. |
| Analysis | Pre-registered analysis plan; independent statistician; stratified log-rank (sex, strain); risk difference with 95% CI |
| Timing | M1–M8 |
| Go / no-go | **Go:** PSLN-344 minus PSLN-212 ≥40 points with 95% CI >0 (40 ≈ 60% of the most conservative estimate, 65 points [T3-C]); **and** PSLN-344 superior to the benchmark (p<0.05) in the heterosubtypic model; **and** HAI GMT ratio ≥4 (observed 8.0, 95% CI 3.9–16.4 [T4]). **Re-scope:** 20–40 points, or not superior to the benchmark. **Stop:** <20 points, or CI including 0. |

## WS7. Biomarker and correlate validation (nested in WS2)

| Item | Specification |
|----|-----------------------|
| Must establish | Which early measurements predict protection in individual animals. Today they cannot: immunology and survival were measured in different animals. |
| Population | All WS2 animals, with non-terminal sampling |
| Comparators | As WS2 |
| Readouts | **16–24 h:** nasal wash and blood CXCL10, GM-CSF, CCL2, ISG score, TNF/IL-6 (Tier A, Section 5). **d7:** blood Tfh/Tfr, plasmablasts. **d13:** HAI, microneutralisation, nasal IgA, IFN-γ ELISpot. |
| Analysis | Logistic regression and ROC against survival; pre-specified marker hierarchy |
| Timing | M1–M8 |
| Go / no-go | At least one marker measured by d7 predicts survival with AUC ≥0.75 (planning threshold). Failure does not stop the programme but removes biomarker-guided dose selection. |

## WS3. CMC characterisation of PSLN-344 (Gate 3 prerequisite)

| Item | Specification |
|----|-----------------------|
| Must establish | What one dose contains, particularly how much Mn²⁺, and whether it is reproducible and stable |
| Population | ≥3 independent batches each of PSLN-344 and PSLN-212 |
| Comparators | PSLN-212 (Mn-free); Mn-only liposome |
| Readouts | Mn per dose (ICP-MS); Mn:CDN ratio; free vs bound Mn²⁺ and release in simulated lung/nasal fluid; CDN-1807 encapsulation by HPLC (currently 54.8% ± 5.1% by A260 [S08-B]); size, PDI and zeta (DLS); TEM; lyophilised stability at −20 °C, 2–8 °C and 25 °C; endotoxin; sterility. Defines whether "20 µg per animal" refers to CDN or particle mass [A16]. |
| Timing | M0–M4 (real-time stability continues) |
| Go / no-go | Batch-to-batch CV ≤15% on Mn content and encapsulation (planning); Mn dose per administration defined for WS4 |

## WS4. Mn²⁺ olfactory and CNS safety pilot (Gate 3)

| Item | Specification |
|----|-----------------------|
| Must establish | That intranasal Mn²⁺ at the efficacious dose does not accumulate in, or injure, the olfactory pathway or brain |
| Population | Aged and young mice, both sexes (pilot); rats in the later GLP study |
| Comparators / arms | Vehicle; PSLN-212 (Mn-free); PSLN-344 at 1×, 3× and 10× the efficacious dose; MnCl₂ at matched Mn (positive control for olfactory transport); cholera toxin (positive control for CNS inflammation, as in S10-A) |
| Readouts | Mn in olfactory bulb, striatum, cortex and cerebellum (ICP-MS) at d1, d7 and d28 after single and 3-dose schedules; Mn-enhanced MRI; histopathology of olfactory epithelium and bulb (GFAP, Iba1; TH in striatum); behaviour (buried-food olfaction, open field, rotarod); CNS Ifnb1/Tnf/Isg15 at 36 h, 72 h and 7 d; serum Mn |
| Size / design basis | n≈8 per sex per arm (planning). Cholera toxin gave 5.5× Ifnb1 in S10-A [T7], which confirms the assay can detect CNS inflammation. |
| Timing | M2–M7 (starts once WS3 defines the Mn dose) |
| Go / no-go | **Go:** no increase over vehicle at 1×, no histopathology or behavioural change, and a margin of ≥10× (planning target). **Stop or re-scope:** any Mn-attributable finding at 1×. This would trigger the Mn-free contingency in Section 8. |

## WS5. Human translatability in vitro (supports Gate 3)

| Item | Specification |
|----|-----------------------|
| Must establish | That CDN-1807 ± Mn²⁺ activates human STING across common alleles, in cells from older donors, and through STING |
| Population | Reporter lines for human STING alleles (R232, HAQ, R232H, AQ, R293Q); PBMC and monocyte-derived DCs from donors ≥65 and 18–40 years; primary nasal and bronchial air–liquid-interface cultures from older donors |
| Comparators | PSLN-344; PSLN-212; free CDN-1807; cGAMP (CMP-204); MnCl₂ alone; Mn-only liposome; STING-knockout cells |
| Readouts | IFN-β, IFN-λ, CXCL10 and GM-CSF secretion (EC50, Emax); ISG panel; cytotoxicity (LDH); epithelial barrier (TEER) |
| Benchmark from our data | In mice, Mn²⁺ raised Ifnb1 2.2× [T4] and Emax 3.4× [T10] |
| Timing | M0–M4 |
| Go / no-go | Active on the major alleles (EC50 within 10× of R232; planning); Mn amplification ≥2× in older-donor cells; activity lost in STING-knockout cells |

## WS6. Delivery and device translation (supports Gate 2)

| Item | Specification |
|----|-----------------------|
| Must establish | Whether protection needs deep-lung deposition, as after mouse instillation (the carrier targets alveolar cells [S01-B/C]), or survives nasal-only delivery, as from a human spray. The instillation volume is not recorded [A16]. |
| Population | Aged mice, both sexes |
| Comparators / arms | Low-volume nasal-restricted dosing (awake) vs high-volume lung-reaching dosing (anaesthetised) vs aerosol or intratracheal delivery |
| Readouts | Deposition imaging (DiD/SRB-labelled particle); nasal vs lung Ifnb1/Gm-csf; germinal centres in nasal lymphoid tissue vs mediastinal lymph node; nasal IgA; survival (n=15–20/arm) |
| Timing | M3–M8 |
| Go / no-go | Nasal-only delivery keeps ≥50% of the survival benefit. If it does not, change the product concept to an inhaled device; this changes CMC and regulatory strategy. |

## WS8. Durability, dose and regimen in aged mice (after Gate 2)

| Item | Specification |
|----|-----------------------|
| Must establish | Durability beyond d60 in aged animals (d180 has been tested only in young mice [S09-F]), the lowest effective dose, and the value of a boost |
| Population | Aged BALB/c, both sexes |
| Comparators / arms | PSLN-344 at 5, 10 and 20 µg (Ifnb1 8.3×, 21.1× and 45.8× in S08-A [T10]); prime vs prime-boost (PSLN-344 IgG CA09 was 2.1× higher after a boost [S03-A vs S13-I], in different animals); PSLN-212; injected benchmark |
| Readouts | Survival after challenge at d90 and d180; HAI/microneutralisation kinetics; TRM; Tfr |
| Timing | M3–M12 |
| Go / no-go | ≥50% survival at d180 (planning threshold) supports a seasonal-duration claim |

## Mechanism closure (within WS2/WS5)

| Item | Specification |
|----|-----------------------|
| Must establish | That PSLN-344 acts through STING (no knockout control exists in the dataset), and the macrophage→Treg step, since S07-C cannot be read [A11] |
| Design and readouts | Sting⁻/⁻ (Goldenticket) mice vs WT: Ifnb1 and GM-CSF at 16 h, moDCs at d5, antibody response; S07-C relabelled from source; n=5–8/arm |
| Timing | M2–M6 |

## After all gates pass: IND-enabling and first-in-human concept (indicative)

- **IND-enabling (M9–M24, planning):**
  - GLP repeat-dose toxicology in two species, with N+1 doses, intranasal local tolerance and neuropathology;
  - ferret challenge study;
  - non-human primate immunogenicity and local tolerability;
  - GMP process development.
- **First-in-human concept:**
  - *Population.* Part A: adults 18–49 years as sentinels. Part B: adults 65–85 years, stratified 65–74 / 75–85, both sexes. Exclude chronic lung disease, neurological disease and immunosuppression.
  - *Arms.* Intranasal inactivated vaccine + PSLN-344 at 2–3 dose levels; intranasal vaccine alone; a licensed enhanced intramuscular vaccine for older adults.
  - *Endpoints.* Safety: solicited nasal and systemic reactions, smell-identification testing, facial-nerve surveillance, serum Mn. Immunogenicity: HAI/microneutralisation GMT and seroconversion at d28, nasal IgA, T cells. Tier A–B biomarkers at 16–24 h and d7.
  - *Dose.* Set from the GLP NOAEL and the WS5 human EC50; **it cannot be derived from current data.**

**Decision points:**

- **M3 (G1):** continue or stop, based on the audit.
- **M8 (G2 + G3):** go to IND-enabling, re-scope, or stop.

---

# 7. Target demographic for the market-research TAM check

**Basis in our data.** The PSLN-344 advantage exists only where immunity is age-impaired:

- aged mice: survival 84% vs 12% [T3-B];
- 14-month mice: 86% vs 14% [T3-E];
- young mice: no difference, both 100% [S09-B/D/F].

For orientation, 20-month mice correspond roughly to human age 56–69 and 10–14-month mice to 38–47 *(external: Flurkey, Currer & Harrison, The Mouse in Biomedical Research, 2007)*.

| Segment | Definition for sizing | Evidence strength |
|----|------------------|--------|
| **Primary** | **Adults ≥65 years** receiving seasonal influenza vaccination, positioned as an intranasal adjuvanted inactivated vaccine with heterosubtypic breadth. Size separately: 65–74, 75–84, ≥85, and long-term-care residents. | Direct (20-month mice). The ≥80 range is extrapolation, because no mice older than about 20 months were tested. |
| **Secondary** | **Adults 50–64 years.** Intranasal live attenuated vaccine is not licensed at ≥50 *(external, US label)*. | Indirect (14-month mice [S06-E/F imprint]) |
| **Option value** | **Pandemic-preparedness (H5N1) procurement** for older adults as a priority group | Heterosubtypic H5N1 protection [S06-C/F; S03-J flagged A9] |
| **Out of scope** (no data) | Children, pregnancy, immunocompromised adults, therapeutic or post-exposure use | – |

**Inputs market research should size:**

1. population by segment and geography;
2. influenza vaccine uptake in each segment;
3. share already receiving enhanced injected vaccines (high-dose, adjuvanted, recombinant) — the comparator we must beat in WS2;
4. the fraction with **chronic lung disease or asthma** (likely precaution for an intranasal STING agonist, as for live attenuated vaccine) and with **neurological disease** (Mn²⁺ precaution). These reduce the addressable market;
5. analogue price premiums;
6. government stockpile tenders.

**Evidence limits that affect the claim:**

- Our data are from female mice only.
- The earliest efficacy claim in humans will be immunogenicity-based (HAI/microneutralisation, mucosal IgA). Heterosubtypic efficacy claims will need field or challenge studies.

---

# 8. What we considered and ruled out

| Option considered | Decision | Why (data) |
|---------|----|-------------------|
| Advance PSLN-344 straight to IND-enabling | **Ruled out** | Critical integrity findings A1–A3; no Mn safety data; n=7/arm gave about 55% power [T12] |
| Drop the programme now | **Not recommended** | It discards the only older-adult candidate (84% vs 12% [T3-B]) when verification is bounded (about 8 months) with explicit stop rules |
| Advance PSLN-212 (Mn-free, simpler) | **Ruled out** | Only +11 points over sham in aged mice [T3-H]; HAI 46 vs 368 [T4]; in young mice it equals PSLN-344 but offers no differentiation [S09-B/D/F] |
| Advance both candidates | **Ruled out** | No scenario in the data where PSLN-212 wins |
| PSLN-212 + GM-CSF as a Mn-free backup | **Contingency idea only** | GM-CSF raises moDCs from 5.9% to 13.8% [S02-G], but there are no protection data. Revisit only if G3 fails. |
| R848 combinations (PSLN-212/R848, PSLN-344/R848) | **Ruled out** | Weight nadir 90.0% (worst 84.7%) and one animal missing [S08-D]. Tnf 202× and Il10 179× at 16 h [T6]. Adding R848 *lowers* Ifnb1 Emax (37.6 vs 52.0 [T10]). No efficacy data. PSLN-344/R848 is undocumented [A14]. |
| cGAMP (CMP-204) instead of CDN-1807 | **Ruled out** | Ifnb1 7.7 vs 16.5 (p<0.001) [S01-A]; Emax 8 vs 16 [T10]; aged survival 3/7 vs PSLN-344 7/7 (p=0.022) [S03-I]; post-boost IgG 0.21× PSLN-212 [S13-I] |
| PSLN-344 alone as an innate "rapid-protection" prophylactic | **Ruled out** | 0/7 survival without antigen [S15-H] |
| Young-adult or paediatric positioning | **Ruled out** | No efficacy difference in young mice [S09-B/D/F; S13-E] |
| Claiming surfactant/AECII targeting as the reason PSLN-344 is better | **Ruled out** | The Mn particle is taken up less by epithelium (−76%) [S08-C]; the gain is in signalling amplitude [T10] |
| Claiming CNS safety from S10-A | **Qualified** | Transcripts at one timepoint only; no Mn measurement (Section 3.3) |
| Claiming d180 durability in aged mice | **Ruled out** | d180 tested in young mice only [S09-F]; aged data stop at d60 |
| Using body-weight curves as secondary efficacy or tolerability evidence | **Ruled out** | Copied series [A3]; mixed handling of dead animals [A8] |
| Using S11-B neutrophils as an inflammation/tolerability readout | **Ruled out** | Duplication with S11-A [A2] |
| Reading S03-B/S03-F as printed (PSLN-344 "Th2") | **Corrected** | Labels rotated relative to raw titres [A6] |
| Reading S09-A block 2 as 16 h | **Corrected** | Matches 72 h [T5; A7] |
| Tetramer kinetics (S05-A/B) and macrophage-transfer Treg data (S07-C) | **Excluded** | MHC or strain mismatch, contradictory conditions, n=2 [A10]; duplicated labels [A11] |
| Stated n as authoritative | **Not used** | Analysed observed n; discrepancies logged [A9] |
| Claiming superiority over licensed older-adult vaccines | **Not possible yet** | No benchmark arm in any experiment [A17]; WS2 adds one |

---

# Appendix A. Methods (summary)

- **Extraction.** Every block was parsed with its exact sheet and cell address. A coverage check confirmed that every numeric cell in the workbook was either captured or is a day/dose label, except the unlabelled S08 rows 89–101 [A15].
- **Survival.** Kaplan–Meier estimates and log-rank tests; the log-rank implementation was cross-validated against *lifelines* 0.30.3 and gives identical statistics. Pooled analyses used stratified log-rank tests and Mantel–Haenszel risk differences (Sato / Greenland–Robins variance). Per-experiment differences use Newcombe 95% CIs; exact tests are Fisher.
- **Continuous readouts.**
  - One-way ANOVA with Tukey HSD (the annotation's stated method), plus Welch t-tests with 95% CI.
  - Titres and fold-changes were analysed on a log10 scale and reported as geometric means. Percentages were analysed on a linear scale.
  - HAI values below 1:10 were set to 5.
- **Restoration index.** (aged PSLN-344 − aged PSLN-212) / (young PSLN-212 − aged PSLN-212), with a percentile bootstrap (4,000 resamples).
- **Dose-response.** Four-parameter Hill fits.
- **Power.** Exact power of the Fisher test.
- **Integrity forensics.**
  - Whole-block and positional duplicate scans, with permutation nulls.
  - Survival–body-weight concordance: death inferred from trailing blank weights, or from ≥3 identical trailing weights (≥2 if below 90%).
  - A search for shared high-precision fractional parts in weight ratios.

# Appendix B. Data-integrity audit log (abridged; full text in workbook tab *A_audit_log*)

| ID | Severity | Finding | Handling |
|--|---|--------------------|-----|
| A1 | Critical | S06-D (rgH5N1, challenge d3) is an exact copy of S06-C (challenge d14), all 28 rows × 4 groups. The matching body-weight record S15-D implies 2/7 deaths each for PSLN-344 and young PSLN-212, where S06-D shows 0. | S06-D excluded |
| A2 | Critical | S11-A (alveolar macrophages) and S11-B (neutrophils) are identical at 35/100 positions, concentrated in replicate columns 1–2 (permutation maximum 19/100). | Both excluded |
| A3 | Critical | 68 high-precision fractional parts are shared across animals in 10 body-weight blocks. Example: S09-E column X (young BALB/c) equals S15-M column I (C57BL/6) on 6 of 7 days, and the 7th differs only in the integer digit. | Body weight not used as an endpoint |
| A4 | High | Survival and body-weight records disagree in 10 group comparisons. Example: S03-I PSLN-212 shows 7/7 dead by d6, while S13-F shows 3 of the same group recovering to 95–99%. | Sensitivity sets C and D |
| A5 | High | S13-F and S13-G group lists do not match S03-I and S03-J (extra "Naive" group, missing arms); the labels appear shifted. | Not used as corroboration |
| A6 | High | S03-B and S03-F IgG2a:IgG1 labels are rotated relative to the raw titres in S13-A–D. | Corrected |
| A7 | High | The second S09-A block, labelled 16 h, is the 72 h panel. | Relabelled |
| A8 | Medium | Dead animals are recorded as blank in some groups and as last weight carried forward in others. | Noted |
| A9 | Medium | Stated vs observed n differs in S03-J, S13-E, S09-F and S05-A/B; S03-J has a missing day value and its censoring date does not match the stated observation period. | Observed n used |
| A10 | Medium | S05-A/B use an H-2Db tetramer in H-2d BALB/c mice, with contradictory conditions and n=2. | Excluded |
| A11 | Medium | Both S07-C group labels are identical. | Excluded |
| A12 | Medium | 19% of unchallenged aged controls died within 14 days (4/21). | Caveat; controls required in WS2 |
| A13 | Low–Med | S01-B and S08-C share some values. | Caveat |
| A14 | Low | PSLN-344/R848 is undocumented; encapsulation efficiency was measured by CDN A260 on an R848-only preparation. | Descriptive only |
| A15 | Low | Unlabelled data in S08 rows 89–101. | Excluded |
| A16 | Low | Missing timepoints, challenge details and instillation volume; S10-A mislabelled as mean±SD; Tfh:Tfr is a derived readout; the S09-A Ifnb1 row reuses S01-A animals. | Noted |
| A17 | Info | Female mice only, one site, no documented blinding, no viral load, IgA, histology, Mn or DLS data, and no benchmark comparator. | Drives the next steps |

![Figure 6. Data-integrity exhibits](figures/Fig6_integrity_exhibits.png)

# Appendix C. Deliverables

| File | Contents |
|--------|-------------|
| `PSLN-344_portfolio_review_proposal.docx` / `.html` / `.md` | This proposal |
| `PSLN_analysis_workbook.xlsx` | README; audit log; Source_map (cell ranges); T1–T15; per-animal data with cell addresses |
| `figures/` | Fig 1 forest plot; Fig 2 Kaplan–Meier curves; Fig 3 restoration index; Fig 4 MoA schematic; Fig 5 dose-response; Fig 6 integrity exhibits |
| `analysis/code/` | Scripts that reproduce every number (run `parse.py` first) |
