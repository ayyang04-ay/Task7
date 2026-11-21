---
title: "PSLN program: portfolio recommendation and proposal for next steps"
subtitle: "Prepared for the portfolio review · analysis dated 1 November 2026"
---

# 1. Recommendation

**Keep one asset, PSLN-344, on a gated budget, positioned as what the data show it to be: an intranasal adjuvant for inactivated influenza vaccine in older adults. Stop PSLN-212 as a candidate for that population; retain it only as the manganese-free comparator and fallback. Do not commit IND-enabling spend until six questions are answered at a decision gate in late June 2027.**

In short: the efficacy signal in aged mice is large and consistent, and everything else a product needs is still unproven. The case for keeping it rests on one result, which held under every check I ran:

|  | Vaccine alone | Vaccine + PSLN-212 | Vaccine + PSLN-344 | Young benchmark (vaccine + PSLN-212) |
|:---------------------------------------|:----------:|:------------:|:------------:|:------------------:|
| **Aged mice surviving lethal influenza challenge after one intranasal dose; seven experiments pooled** | 0/49 (0%) | 4/49 (8%) | **39/49 (80%)** | 49/49 (100%) |

- PSLN-344 beats PSLN-212 by 71 percentage points (95% CI 59 to 84). When survival is re-derived from the body-weight records instead of the survival tables, the counts are 41/49 against 7/49. [E1–E3; Figure 1]
- Protection extended to viruses the vaccine did not match (H3N2 vaccine against H1N1 challenge; seasonal vaccine against a laboratory H5N1 virus) and was present 3 days after dosing (5/7). The same pattern is recorded in two further mouse strains (12/14), although those records need checking (Section 2.5). [E4, E7]

Four things the committee should hear from us first:

1. **The asset as it has been described, a STING agonist in its vehicle, is PSLN-212, and in aged animals it fails (8%).** What works is the same product with Mn2+ added. No experiment tested Mn2+ without our agonist, or Mn2+ with generic cGAMP (the natural STING activator, which is not proprietary), so we cannot yet show that the proprietary agonist is what carries the benefit. In young animals PSLN-344, PSLN-212 and generic cGAMP all protect fully (24/24, 24/24, 7/7). [E10, E11]
2. **It is a vaccine adjuvant, not a stand-alone drug.** PSLN-344 given without vaccine protected 0 of 7 animals. [E6]
3. **The evidence is mouse-only and thin on safety.** Female mice only, one dose level (20 µg), and no comparison with any licensed-type vaccine. There are no human-cell data, no toxicology, and no measurement of where intranasally delivered manganese goes.
4. **The dataset has 19 integrity problems.** They include column labels that reverse one conclusion, a survival table that is a copy of another, and body-weight values reused across experiments (Section 2.5, Appendix A). None overturns the headline result. All need to be fixed before anyone outside the company sees the package.

**What the committee is asked to approve.** Stage 1 only: six studies plus formulation characterization, running November 2026 to September 2027, with an early checkpoint in mid-January 2027 and a go/no-go review in late June 2027 (Section 5). Stage 2 (ferret, GLP toxicology, scale-up) is not requested now.

**What would make me recommend dropping it.** Any one of: the source records do not support the survival tables; CDN-1807 is inactive on human STING; Mn2+ alone or Mn2+ with generic cGAMP performs as well as PSLN-344; manganese accumulates in brain after an efficacious dose; a licensed-type intramuscular vaccine matches it against mismatched virus in aged animals.

*How to read the references. Data are from `psln_program_dataset.xlsx` (15 sheets; file last modified 3 September 2026) and `psln_program_annotation.pdf` (dated 15 September 2026). Labels such as S06-A are block names in that workbook. Tags such as [E7] point to the evidence index in Appendix C, which gives the source cells and the analysis table for each number; codes such as DI-04 are entries in the data-integrity register in Appendix A. Supporting tables are in `PSLN_analysis_tables.xlsx`; the scripts that produce them are in `analysis_code/`.*

# 2. How the asset looks

## 2.1 Protection: PSLN-344 works in aged animals, PSLN-212 does not

Table 1 lists every lethal-challenge experiment. Unless a row says otherwise, animals were female BALB/c aged 20 months or more, given one intranasal dose of inactivated vaccine with 20 µg of adjuvant, challenged with 5 times the median lethal dose (10 times in S03-I) and followed for 14 days. "Vaccine alone" is the group the workbook calls Sham: vaccine with empty liposome. "H5N1" in Table 1a is rgH5N1, a laboratory virus carrying the H5 and N1 surface genes on an H1N1 (PR8) backbone; only S03-J used wild-type H5N1, and there the vaccine was itself an H5N1 vaccine.

**Table 1a. Aged BALB/c, one dose: survivors / n at 14 days after challenge.**

| Block | Vaccine → challenge virus, day of challenge | Vaccine alone | PSLN-212 | PSLN-344 | Young + PSLN-212 | Source cells | Note |
|:------|:--------------------|:------:|:-------:|:-------:|:-------:|:------------|:-----------------------|
| S03-I | Bivalent vaccine → matched H1N1 (CA09), day 14 | 0/7 | 0/7 | **7/7** | 7/7 | S03!A16:F51 | Weight record: PSLN-212 3/7 (DI-04) |
| S06-A | H3N2 vaccine → H1N1 (PR8), day 14 | 0/7 | 1/7 | **6/7** | 7/7 | S06!A2:E30 | Table and weight record agree |
| S06-C | Bivalent vaccine → H5N1 (rgH5N1), day 14 | 0/7 | 2/7 | **7/7** | 7/7 | S06!M2:Q30 | Weight record: PSLN-212 1/7 |
| S06-B | H3N2 vaccine → H1N1 (PR8), day 3 | 0/7 | 0/7 | **5/7** | 7/7 | S06!G2:K30 | Table and weight record agree |
| S06-D | Bivalent vaccine → H5N1 (rgH5N1), day 3 | 0/7 | 2/7 | **7/7** | 7/7 | S06!A33:E61 | Table is a copy of S06-C; weight record: PSLN-344 5/7, young 5/7 (DI-03). Not pooled |
| S06-E | H3N2 vaccine → H1N1 (PR8), day 60 | 0/7 | 0/7 | **5/7** | 7/7 | S06!G33:L68 | Weight record: PSLN-344 6/7, PSLN-212 1/7 |
| S06-F | Bivalent vaccine → H5N1 (rgH5N1), day 60 | 0/7 | 1/7 | **5/7** | 7/7 | S06!M33:R68 | Table and weight record agree |
| S06-G | H1N1 vaccine → H3N2 (Perth), day 60 | 0/7 | 0/7 | **4/7** | 7/7 | S06!A70:F105 | Weight record: PSLN-344 5/7 |
| **Pooled** | **Seven experiments (S06-D excluded), survival tables** | **0/49** | **4/49** | **39/49** | **49/49** | as above | PSLN-344 minus PSLN-212: +71 points (CI 59 to 84); stratified log-rank p<0.0001 |
|  | Same seven, from body-weight records | 0/49 | 7/49 | 41/49 | 49/49 | S13-F; S15-A, B, C, E, F, G | +69 points (CI 56 to 83) |

**Table 1b. Other lethal-challenge experiments.**

| Block | Design | Survivors / n | Source cells |
|:-----------|:---------------------------------|:-----------------------------------------|:-----------|
| S15-L | C57BL/6, 20 months; bivalent vaccine; challenge virus not stated | Vaccine alone 0/7; PSLN-212 0/7; **PSLN-344 6/7**; young + PSLN-212 6/7 | S15!A102:E130 |
| S15-N | Swiss Webster, 20 months; bivalent vaccine; challenge virus not stated | Vaccine alone 0/7; PSLN-212 2/7; **PSLN-344 6/7**; young + PSLN-212 7/7 | S15!A133:E161 |
| S15-H | Aged BALB/c; H5N1 (rgH5N1) challenge 3 days after dosing | Vaccine alone 0/7; PSLN-344 alone 0/7; **vaccine + PSLN-344 6/7** | S15!A72:D93 |
| S03-J | rgH5N1 vaccine; wild-type H5N1 challenge 2 days after dosing; followed to day 21; age not stated | **PSLN-344 9/9** (a tenth row has no day recorded); arms labeled PSLN-212 3/10 and Sham 1/10 | S03!G16:J46 |
| S06 rows 71–98 (left) | BALB/c, 14 months at vaccination, with or without H1N1 infection 4 months earlier; H1N1 (PR8) challenge | No prior infection: PSLN-212 0/7, **PSLN-344 6/7**. Prior infection: PSLN-212 4/7, **PSLN-344 6/7** | S06!G70:K98 |
| S06 rows 71–98 (right) | Same design; H3N2 (Perth) challenge at day 14 | No prior infection: PSLN-212 0/7, **PSLN-344 6/7**. Prior infection: PSLN-212 0/7, **PSLN-344 6/7** | S06!M70:Q98 |
| S09-B, S09-D, S09-F | Young BALB/c; mismatched-virus challenge at day 21, 21 and 180 | Vaccine alone 0/8, 0/8, 0/7; PSLN-212 8/8, 8/8, 8/8; PSLN-344 8/8, 8/8, 8/8 | S09!A11:D35; A38:D62; A65:D88 |
| S13-E | Young BALB/c; matched H1N1 challenge at day 14 | No vaccine 0/7; vaccine alone 1/7; cGAMP liposome (CMP-204) 7/7; PSLN-344 7/7 | S13!R2:V30 |
| S03-I | Aged BALB/c; matched H1N1 challenge at day 14; cGAMP arm | cGAMP liposome (CMP-204) 3/7 (see DI-04) | S03!C24:C30 |

Pooled survival with PSLN-344 is 80% (95% CI 66% to 90%); with PSLN-212 it is 8% (2% to 20%). The young benchmark is 100% (93% to 100%), and PSLN-344 in aged animals remains below it (p=0.001). PSLN-212 is not inert in aged animals: it delays death (p<0.001 against vaccine alone, stratified log-rank test) and raises IgG about 7-fold (S03-A), but it rescues only 4 of 49. [E1]

![**Figure 1.** Survival by experiment (A) and the difference between PSLN-344 and PSLN-212 (B). Counts are as printed in the survival tables; open diamonds show where the paired body-weight record implies a different count. Pooled rows exclude S06-D. For S03-J the identity of the two comparator arms is uncertain (DI-05).](figures/Fig1_survival_by_experiment.png){width=94%}

![**Figure 2.** Kaplan–Meier curves. A: aged BALB/c, seven experiments pooled (shading = 95% CI). B: PSLN-344 by interval from vaccination to challenge, with unchallenged aged controls from the day-60 cohorts. C: PSLN-344 without antigen gives no protection.](figures/Fig2_kaplan_meier.png){width=100%}

Three further points from Table 1:

- **The effect needs antigen.** Three days after dosing, vaccine with PSLN-344 protected 6/7, PSLN-344 alone 0/7 and vaccine alone 0/7 (S15-H). The early protection is therefore not a non-specific antiviral state, and the product cannot be positioned as a stand-alone immune stimulant. [E6]
- **It works in animals that have had influenza before.** In 14-month-old animals with or without a prior H1N1 infection, PSLN-344 protected 6/7 in each of four groups; PSLN-212 protected 0/7, 4/7, 0/7 and 0/7 (blocks at S06 rows 71 to 98). This matters because every older adult has prior influenza immunity. It also shows PSLN-212 already failing at 14 months. [E9]
- **Wild-type H5N1.** All PSLN-344 animals survived challenge given 2 days after a single dose (9/9 with a recorded day; 10/10 in the weight record), against 1/10 and 3/10 in the two comparator arms (S03-J). The identity of those comparator arms, and the age of the animals, are uncertain (Appendix A, DI-05). [E8]

## 2.2 Immune responses: PSLN-344 closes most of the age gap, not all of it

Figure 3 shows each immune read-out in aged animals as a percentage of the young benchmark; Table 2 gives the numbers for the main ones.

![**Figure 3.** Responses in aged animals as a percentage of the young benchmark (young animals given PSLN-212). Titers and mRNA: ratio of geometric means; cell percentages: ratio of means. HAI, hemagglutination inhibition; DC, dendritic cell; Tfh and Tfr, follicular helper and follicular regulatory T cells.](figures/Fig3_restoration_vs_young.png){width=86%}

**Table 2. Key immune read-outs in aged animals (group mean; geometric mean for titers, mRNA and ratios). n=5 per group.**

| Read-out (block) | Vaccine alone | PSLN-212 | PSLN-344 | Young + PSLN-212 | Ratio, 344 to 212 | p (Tukey) | 344 as % of young | Source cells |
|:---------------------------|:------:|:-------:|:-------:|:-------:|:------:|:------:|:------:|:------------|
| Lung Ifnb1 mRNA at 16 h, fold (S01-A) | 0.94 | 16.5 | **36.9** | 37.5 | 2.2× | <0.001 | 98% | S01!B3:F9 |
| Lung monocytes at day 4, % (S01-D) | 10.4 | 16.7 | **30.6** | 32.2 | 1.8× | <0.001 | 95% | S01!B26:U26 |
| CCR7+ migratory dendritic cells in lung, 72 h, % (S02-A) | 2.5 | 7.3 | **30.7** | 35.0 | 4.2× | <0.001 | 88% | S02!A3:D7 |
| CD86+ dendritic cells in lymph node, day 3, % (S02-D CD86) | 7.2 | 8.1 | **14.5** | 37.9 | 1.8× | 0.033 | 38% | S02!F10:I14 |
| Germinal-center B cells, day 7, % (S03-K) | 1.2 | 2.3 | **6.5** | 9.8 | 2.8× | 0.007 | 67% | S03!L17:O21 |
| Follicular helper : follicular regulatory T-cell ratio, day 7 (S04-B Tfh:Tfr) | 3.5 | 2.8 | **8.4** | 14.4 | 3.0× | <0.001 | 58% | S04!A15:D19 |
| Serum IgG to H1N1, day 14, titer (S03-A) | 55.7 | 393 | **7,305** | 11,959 | 18.6× | <0.001 | 61% | S03!A3:E7 |
| Hemagglutination inhibition, H1N1, day 14, titer (S03-C) | 7.6 | 45.9 | **368** | 485 | 8.0× | <0.001 | 76% | S03!K3:O7 |
| Hemagglutination inhibition, H3N2, day 14, titer (S03-G) | 10.0 | 34.8 | **320** | 368 | 9.2× | <0.001 | 87% | S03!K10:O14 |
| Neutralizing antibody, H1N1, day 14, titer (S03-D) | 52.2 | 418 | **3,840** | 6,686 | 9.2× | <0.001 | 57% | S03!Q3:U7 |
| IgG2a : IgG1 ratio, H1N1, day 14, recomputed from raw titers (S13-A ÷ S13-B) | – | 0.54 | **1.85** | 2.50 | 3.4× | 0.016 | 74% | S13!A3:G7 |
| Ki-67+ CD8 T cells in lung, day 3, % (S05-D) | 0.83 | 3.5 | **9.4** | 9.9 | 2.7× | <0.001 | 94% | S05!A19:D23 |
| Interferon-γ+ CD8 T cells responding to H5N1, day 14, % (S05-F) | 0.67 | 1.5 | **6.4** | 9.2 | 4.2× | <0.001 | 69% | S05!A33:D37 |
| Interferon-γ+ CD8 T cells responding to H5N1, day 60, % (S05-G) | 1.5 | 3.0 | **9.9** | 14.4 | 3.2× | <0.001 | 69% | S05!A40:D44 |
| Lung-resident memory CD8 T cells, day 25, % (S05-I) | 0.58 | 1.0 | **4.0** | 6.0 | 4.0× | <0.001 | 66% | S05!A54:D58 |

- The early interferon response is fully restored: lung Ifnb1 at 16 hours is 37-fold with PSLN-344, 17-fold with PSLN-212 and 38-fold in young animals (S01-A). [E12]
- Serum antibody is 8 to 19 times higher than with PSLN-212 and reaches 41% to 87% of the young benchmark (S03-A to S03-H). [E13–E16]
- CD8 T-cell responses reach 59% to 94% of the young benchmark, include cells that respond to H5N1 after seasonal vaccine, and are still present at day 60 (S05-D to S05-I). [E17, E18]
- The least restored step is dendritic-cell activation in the lymph node: CD40 and CD86 reach only 29% and 38% of young (S02-D). [E20, E21]

## 2.3 Where the case is weaker than the headline

1. **No benefit in young animals.** Survival was 24/24 with either product, and maximum weight loss was the same (10.7% vs 10.8%). After challenge at day 180, young animals given PSLN-344 recovered more slowly than those given PSLN-212 (95.6% vs 99.2% of starting weight at day 14, p=0.004). The added value of Mn2+ is specific to aged hosts. [E10]
2. **It prevents death, not illness.** Aged survivors given PSLN-344 still lost 11.9% of body weight at the low point, against 9.7% for young animals given PSLN-212 (p=0.007). No experiment measured virus in the lung or nose. [E28]
3. **Durability in the aged is unproven beyond 60 days and already lower at day 60.** Survival was 20/21 with challenge at day 14 and 14/21 at day 60 (p=0.045). In the same day-60 cohorts, 4 of 21 aged control animals that were never challenged also died within the 14-day window, so part of the shortfall may be background mortality. The two kinds of death look different, though: the PSLN-344 deaths followed 15% to 23% weight loss, the unchallenged deaths only 3% to 6%. A 180-day result exists only in young animals. [E4, E5]
4. **The comparator is a low bar.** The only vaccine control is unadjuvanted intranasal vaccine, which protected 0/49. There is no comparison with the high-dose or adjuvanted intramuscular vaccines that older adults receive today.
5. **One dose level.** Every efficacy and tolerability experiment used 20 µg. A dose-response exists only for Ifnb1 (S08-A), where 20 µg already gives 92% of the 40 µg response. There is no margin between an effective dose and a poorly tolerated one because neither has been located. [E23]
6. **Our agonist against generic cGAMP.** In the same vehicle in aged animals, CDN-1807 (PSLN-212) induced 2.2 times more Ifnb1 than cGAMP (CMP-204) (p=0.001) and about twice the antibody titer (not significant at n=5). Survival as printed was no better (0/7 vs 3/7), although that comparison is unreliable (DI-04). [E30]
7. **Antigen format.** All vaccines were formalin-inactivated whole virus. Licensed seasonal vaccines for older adults are split or subunit antigens.
8. **Design limits.** Female animals only; 3 to 10 animals per group; single experiments; no randomization or blinding information in the annotation.
9. **Where the dose lands.** The mechanism data point to the deep lung: uptake by alveolar macrophages and delivery to alveolar type II cells (S01-B, S01-C). The instillation volume is not recorded. A nasal spray in a person deposits mainly in the nose.

## 2.4 Tolerability and safety: no alarm so far, but very little has been measured

- **Body weight after dosing (S08-D).** PSLN-344 caused a transient loss: mean 96.7% of baseline at day 4 against 98.8% with vaccine alone, back to 99.8% by day 10. PSLN-212 was similar (97.0% at day 4). [E24]
- **Lung cytokines (S09-A, n=3).** Tnf was 40-fold at 16 hours with PSLN-344 (young benchmark 14-fold) and still 8.4-fold at 72 hours, when young animals had returned to baseline (0.5-fold). Il6 was 7.2-fold at 72 hours. PSLN-212 also resolved slowly in aged lung (Tnf 5.2-fold at 72 hours), so this is mainly an age effect with a modest Mn2+ increment. No later time point exists. [E25]
- **Central nervous system (S10-A, n=5, 36 hours).** PSLN-344 did not produce the signal seen with cholera toxin (Ifnb1 1.3-fold vs 5.5-fold; Tnf 1.6-fold vs 3.5-fold). Tnf was 1.6 times buffer, which is not significant after correction for multiple comparisons (p=0.12) but is at p=0.03 uncorrected. One time point, no manganese measurement, region of brain not stated. [E26]
- **Neutrophils.** The only lung-neutrophil block (S11-B) is not independent data and cannot be used (DI-08).
- **Not in the dataset at all:** Mn2+ content per dose; manganese in brain or olfactory tissue; histopathology; repeat dosing; any second species; particle size and stability results.

![**Figure 4.** A: Ifnb1 dose-response. B: body weight after dosing without challenge. C: lung cytokine mRNA. D: brain transcripts with cholera toxin as positive control.](figures/Fig4_dose_and_tolerability.png){width=88%}

## 2.5 Can the committee rely on these data?

I checked every block for internal consistency: stated against observed group sizes, survival tables against their paired body-weight records, derived quantities against their raw inputs, and repeated values across blocks. There are 19 findings (6 high, 7 medium, 6 low). Table 3 lists the ones that change how a block should be read; the full register with cell references, and a figure showing four of the findings, are in Appendix A.

**Table 3. Integrity findings that change how a block should be read.**

| ID | Where | What is wrong | Consequence | Handling |
|:-----|:-----------------|:-----------------------------|:---------------------------------|:-------------|
| DI-01 | IgG2a:IgG1 ratio blocks S03-B and S03-F | Column labels are rotated relative to the raw titers in S13-A to S13-D | As printed, PSLN-344 looks IgG1-skewed (0.54). Recomputed, it is IgG2a-skewed (1.85; 2.30 for H3N2) and PSLN-212 is the skewed one | Recomputed from raw titers |
| DI-02 | Second cytokine panel in S09-A | Labeled 16 h; its values are the 72-hour animals of S01-A (21 of 21 match) | Read as a replicate, it would hide that Tnf and Il6 are still raised in aged lung at 72 hours | Analyzed as 72 hours |
| DI-03 | Survival table S06-D | Identical row for row to S06-C, a different experiment | Day-3 H5N1 survival for PSLN-344 is 7/7 (table), 5/7 (weights) or 6/7 (independent run S15-H) | Excluded from pooled estimate |
| DI-04 | S03-I against its weight record S13-F | Table has all PSLN-212 animals dead by day 6; weights show all seven alive at day 8 and three recovering | PSLN-212 survival after matched-virus challenge is 0/7 or 3/7; the cGAMP against PSLN-212 ranking is unreliable | Reported as a range |
| DI-05 | Wild-type H5N1 study S03-J | Stated n of 9 with 10 rows; one row has no day; group names differ between table and weight record; age not stated | PSLN-344 result is firm; which comparator is which is not | Comparator identity flagged |
| DI-07 | Body-weight blocks on S15 and S09 | Values shared between different experiments (S15-I and S15-C: 40 of 42 cells) | Weight curves are not independent confirmation; strain generalization is provisional | Used as cross-check only |
| DI-08 | Lung neutrophils S11-B | 35 of 100 values identical to the alveolar-macrophage block S11-A | No usable neutrophil read-out | Excluded |
| DI-16 | "Untreated" groups at day 60 | Not challenged; 4 of 21 died in 14 days | They measure background mortality in old animals and are not an efficacy comparator | Used as background only |

**What survives the audit.** The PSLN-344 against PSLN-212 difference in aged animals is +71 points from the survival tables and +69 points from the body-weight records, and no single experiment drives it (range +57 to +100). The immune read-outs in Table 2 come from blocks with no integrity finding, except the IgG2a:IgG1 ratio, which I recomputed from raw titers.

**What does not.** Five things should not be quoted until the source records are checked: survival with PSLN-212 after matched-virus challenge (0/7 or 3/7); survival with PSLN-344 after H5N1 challenge at day 3 (7/7 in a copied table, 5/7 in the weight record, 6/7 in an independent run); the comparison with PSLN-212 against wild-type H5N1; generalization to other strains, where the weight records are partly copies; and anything about neutrophils or macrophage subsets.

# 3. Mechanism of action and biomarkers

**Mechanism in one paragraph.** The liposome is taken up by alveolar macrophages through surfactant proteins A and D, and its cargo reaches alveolar type II cells. In young lung this triggers a burst of type I interferon at 16 hours; in aged lung the burst is less than half as large with PSLN-212, and Mn2+ restores it. Interferon, the chemokine CCL2 and GM-CSF then recruit CCR2-positive monocytes, which become dendritic cells in a step that needs the interferon receptor and is rescued by GM-CSF. These cells carry antigen to the lymph node, and CD8 T cells are also primed inside the lung. The result is a germinal-center response with IgG2a-dominant antibody, and CD8 T cells that recognize conserved viral antigens and persist in the lung, which is the plausible basis for protection against mismatched virus. Five of the seven steps have at least one knockout, blocker or add-back experiment behind them (Figure 5).

**What the mechanism does not yet include.** The dataset never tests whether the effect requires STING or cGAS, never isolates what Mn2+ contributes, and never shows whether antibody or CD8 T cells are responsible for protection against mismatched virus. Several interventional experiments were done in young animals (S02-I, S12-A) or in a different strain (S05-C), not in the aged BALB/c animals where the efficacy claim sits.

![**Figure 5.** Mechanism supported by our data, with the interventional evidence for each step and what remains unproven.](figures/Fig5_mechanism.png){width=100%}

**Biomarkers.** Table 4 gives the panel I would carry forward, ordered by time after dosing. Every entry separates PSLN-344 from PSLN-212 in aged animals in our data. The clinical analogues in the fourth column are proposals; none has been measured by us.

**Table 4. Biomarker panel. Values are aged animals given PSLN-344 vs PSLN-212.**

| When and what for | Marker in our data (block) | PSLN-344 vs PSLN-212 | Proposed measure in people | Use |
|:------------|:------------------------|:-----------------------|:---------------------|:---------------|
| Hours: target engagement | Lung Ifnb1 mRNA at 16 h (S01-A) | 37-fold vs 17-fold; no overlap between groups (5 vs 5); dose-dependent (S08-A) | Interferon-β and CXCL10 in nasal lining fluid; interferon-stimulated gene score in blood at 24 h | Proof of pharmacology; dose selection |
| Hours: recruitment signals | Lung Ccl2 mRNA at 16 h (S09-A, n=3); Gm-csf mRNA at 16–36 h (S02-F) | Ccl2 590-fold vs 7.6-fold; Gm-csf 6.0- to 8.5-fold vs 1.4- to 1.6-fold | CCL2 and GM-CSF protein in nasal lining fluid | Widest dynamic range; most sensitive to the Mn2+ effect |
| Days 3–7: cellular | Lung monocytes day 4 (S01-D); CCR7+ dendritic cells (S02-A); ICOS-high follicular helper T cells and germinal-center B cells day 7 (S04-A, S03-K) | 30.6% vs 16.7%; 30.7% vs 7.3%; 10.3% vs 3.8%; 6.5% vs 2.3% | Activated circulating follicular helper T cells and plasmablasts in blood at day 7 | Early predictor of antibody response |
| Days 14–28: antibody | Hemagglutination inhibition and neutralizing titers (S03-C, D, G, H); IgG2a:IgG1 ratio (S13-A to D) | Titers 368 vs 46 (H1N1) and 320 vs 35 (H3N2); neutralizing 3,840 vs 418; ratio 1.85 vs 0.54 | Hemagglutination inhibition and microneutralization (the regulatory standard); nasal IgA, which we have never measured | Immunogenicity endpoint for matched strains |
| Days 14–60: T cells | Interferon-γ+ CD8 T cells responding to H5N1 (S05-F, S05-G); lung-resident memory CD8 T cells (S05-I) | 6.4% vs 1.5% at day 14; 9.9% vs 3.0% at day 60; 4.0% vs 1.0% | Interferon-γ T-cell response in blood to conserved antigens (nucleoprotein, matrix) and to mismatched virus | Candidate correlate for mismatched-virus protection; unproven |
| Safety | Lung Tnf and Il6 at 72 h (S09-A); body weight after dosing (S08-D); brain Tnf (S10-A) | Tnf 8.4-fold and Il6 7.2-fold at 72 h (young: 0.5 and 3.1); weight 96.7% at day 4; brain Tnf 1.6-fold | TNF and IL-6 in nasal fluid and serum; blood manganese; brain manganese by MRI; smell testing | Reactogenicity and manganese monitoring |

**Two cautions on using these to validate efficacy.**

- *No marker has been linked to outcome in individual animals.* Serology and challenge used different animals in every experiment, so the associations are between group averages only. Study 2 collects pre-challenge serum from every challenged animal to close this gap.
- *The conventional antibody threshold did not predict survival here.* Aged animals given PSLN-212 reached hemagglutination-inhibition titers of 40 to 80 (S03-C; cells S03!M3:M7), which is at or above the 1:40 level usually treated as protective in people, yet 0/7 (survival table) to 3/7 (weight record) survived matched-virus challenge. All animals given PSLN-344 were at 160 to 640 (S03!N3:N7). For protection against mismatched virus, antibody to the vaccine strain is not expected to be the correlate at all; the CD8 T-cell measures are the candidates, and they are unproven.

# 4. Target demographic for the market-size check

**Primary population: adults aged 65 and over receiving their annual influenza vaccination**, in markets that recommend or reimburse enhanced vaccines for this age group. The product would be one intranasal dose per season, given with (or co-formulated with) an inactivated influenza antigen.

The reasons come from our data:

- The benefit of PSLN-344 over PSLN-212 exists only in aged animals (80% vs 8% survival at 20 months or more). In young animals there is none (24/24 vs 24/24), and generic cGAMP in the same vehicle protects young animals equally (7/7). A claim in adults under 65 would have no differentiation to stand on. [E1, E10, E11]
- The animals were 20 months or older. On the usual mouse-to-human life-stage conversion this corresponds to roughly 60 to 70 human years (external reference, not from our data).
- The benefit was seen with and without prior influenza infection, which is the normal state of this population. [E9]

**Filters the market-research team should apply or hold open:**

| Filter | Basis | Status |
|:-------------------------------|:---------------------------------------|:---------------------------|
| Age 65 and over, both sexes | Aged-specific benefit; all animals were female | Sex not yet tested (Study 2) |
| Annual seasonal vaccination, one dose per season | Single-dose efficacy; repeat dosing never tested | Annual re-dosing safety open (Study 3, Stage 2) |
| Exclude, until safety data exist: chronic lung disease (asthma, COPD); liver impairment; pre-existing parkinsonism or other neurodegenerative disease; immunocompromise | Lung Tnf and Il6 still raised at 72 hours in aged lung (S09-A); manganese is cleared by the liver and is neurotoxic when it accumulates (external) | Open (Study 3, Stage 2 toxicology) |
| Must be sold with, or as part of, a specific vaccine | PSLN-344 alone 0/7 (S15-H); adjuvants are licensed as part of a vaccine, not separately (external) | Requires an antigen partner or in-house antigen |
| Route: nasal spray or inhaled | Mechanism points to deep lung; dosing volume not recorded | Open (Study 2); an inhaled product would narrow the population and change the device |

**Upside segments, not in the base case:**

- *Adults 50 to 64.* PSLN-212 already failed in 14-month-old animals (0/14 vs 12/14 for PSLN-344 in animals without prior infection). This suggests the age-related deficit starts earlier than 65, but it rests on two experiments. [E9]
- *Pandemic and zoonotic influenza stockpiles (government purchasers).* Protection against wild-type H5N1 two days after one dose of H5N1 vaccine (S03-J), and against laboratory H5N1 virus after seasonal vaccine (S06-C, S06-F), supports the concept. The animals' age is not stated in S03-J, and the advantage of PSLN-344 over PSLN-212 in non-elderly recipients is not shown. [E8]

*Orientation figures, not from our data and not verified here:* roughly 59 million people aged 65 and over in the United States with about 70% vaccinated each season; roughly 95 million in the European Union; roughly 36 million in Japan.

# 5. Next steps: what the next studies must establish

The program has one strong efficacy signal and almost no information on the six things that decide whether it can become a product. Stage 1 answers those six, cheapest first. A checkpoint in mid-January 2027 separates the two studies that need no aged animals from the four that do: if the records do not reconcile (Study 0), or CDN-1807 is inactive on human STING in reporter cells (first part of Study 1), the aged-animal studies are not dosed. Figure 6 shows the schedule; dates assume animals of both sexes aged 20 months or more are available in January 2027, which I could not confirm from the data. Supply of aged animals is the critical path: Studies 2 to 5 together need about 725 of them. If supply is limiting, Studies 2 and 3 come first (about 375 animals), because they carry four of the six gate criteria.

![**Figure 6.** Proposed schedule. Aged animals are dosed only after the mid-January checkpoint. Stage 2 is shown for context and is not requested now.](figures/Fig6_timeline.png){width=100%}

## Study 0. Reconcile the data (no animals)

| Item | Specification |
|:----------------|:----------------------------------------------------------------------------------|
| **Must establish** | That the headline results stand when every flagged block is checked against source records (cage cards, daily health sheets, balance logs, flow-cytometry files, plate reads). |
| **Scope** | The 19 findings in Appendix A; DI-01 to DI-08 first. |
| **Read-out** | A corrected, locked dataset; this analysis re-run unchanged on it (scripts supplied). |
| **Timing** | 2 November to 11 December 2026. |
| **Pass** | The pooled survival difference between PSLN-344 and PSLN-212 in aged BALB/c stays at or above 50 points (now +71, CI 59 to 84), and no further block proves to be a copy. |

## Study 1. Is the active relevant to people, and is it on target?

| Item | Specification |
|:----------------|:----------------------------------------------------------------------------------|
| **Must establish** | (a) CDN-1807, with and without Mn2+, activates human STING across its common genetic variants. (b) The age-related deficit and its rescue by Mn2+ reproduce in human cells. (c) The effect in mice requires STING. The dataset contains no human data and no STING knockout. |
| **Populations** | (a) Reporter cells expressing each common human STING variant. (b) Primary cells from donors aged 65 and over and donors aged 18 to 40, at least 8 per group, both sexes: monocyte-derived macrophages, alveolar macrophages if obtainable, and airway epithelium at air-liquid interface co-cultured with macrophages. (c) Sting1-null and Cgas-null mice against wild type, young, 5 per arm. |
| **Comparators** | 2'3'-cGAMP (the agonist in CMP-204); a clinical-stage synthetic STING agonist as benchmark; MnCl2 alone; empty liposome. |
| **Endpoints and read-outs** | Primary: concentration-response for IFN-β and CXCL10 (potency and maximum), with and without Mn2+. Secondary: CCL2, GM-CSF, IL-6, TNF (the analytes of S09-A and S02-F); cell viability. In knockout mice: lung Ifnb1 at 16 hours and IgG at day 14. |
| **Timing** | 16 November 2026 to 26 February 2027; reporter-cell result by 8 January, before any aged animal is dosed. |
| **Go / no-go** | Go: activity on the three commonest variants within 10-fold of cGAMP; Mn2+ raises the maximum response in cells from older donors; no response in Sting1-null mice. No-go: activity confined to mouse STING. |

## Study 2. Which component does the work, at what dose, and where must it land? (aged mice)

| Item | Specification |
|:----------------|:----------------------------------------------------------------------------------|
| **Must establish** | (a) What each component contributes: CDN-1807, Mn2+, and the liposome. (b) How efficacy and tolerability change with dose; every result so far is at 20 µg. (c) Whether protection survives dosing restricted to the nose. (d) Whether the result holds in males. |
| **Population** | BALB/c aged 20 months or more, 6 female and 6 male per arm for challenge; 6 more per arm in seven arms for 16-hour lung read-outs and post-dose tolerability; 5 per time point in five arms for virus titer. Young BALB/c given PSLN-212 as benchmark. About 225 aged animals. |
| **Arms and comparators** | Vaccine with each of: empty liposome; PSLN-212 20 µg; PSLN-344 at 5, 10, 20 and 40 µg; liposome with Mn2+ only (matched to 20 µg PSLN-344); CMP-204 20 µg; CMP-204 with Mn2+; free CDN-1807 with MnCl2 and no liposome; PSLN-344 20 µg in a low volume confined to the nose. |
| **Model** | Aichi H3N2 vaccine, 5 times the median lethal dose of PR8 H1N1 at day 14. This is the S06-A design, where PSLN-344 protected 6/7 and PSLN-212 1/7 and the survival table and weight record agree. |
| **Endpoints and read-outs** | Primary: survival to day 14 after challenge. Key secondary: maximum weight loss; lung virus titer at days 3 and 6 after challenge (never measured so far); serum hemagglutination-inhibition and neutralizing titers on day 13 in every challenged animal, so that titer and outcome can be paired; nasal-wash and lavage IgA, and lung Ifnb1, Ccl2, Tnf and Il6 at 16 hours, in the extra animals; body weight for 10 days after dosing. |
| **Size** | 12 per arm gives 81% power to detect 80% against 20% survival and 80% power to detect a 2-fold difference in titer (Power sheet of the analysis workbook). |
| **Timing** | Protocol amendment in November and December 2026; dosing 18 January 2027, after the checkpoint; read-out late April 2027. |
| **Go / no-go** | Go: PSLN-344 beats both Mn2+-only liposome and CMP-204 with Mn2+ by at least 30 points of survival or 4-fold in antibody titer; a dose exists with at least 70% survival and no more than 5% weight loss after dosing; the benefit is reproduced in males. No-go: Mn2+ alone or with cGAMP is equivalent. If nose-only dosing loses the effect, the product is an inhaled vaccine and Stage 2 must be re-planned; that is a flag, not a stop. |

## Study 3. Manganese and local safety (non-GLP)

| Item | Specification |
|:----------------|:----------------------------------------------------------------------------------|
| **Must establish** | Where the manganese goes after intranasal dosing, whether it accumulates in brain, and whether inflammation in aged lung and nose resolves. First task: measure the Mn2+ content per dose, which is not in the dataset. |
| **Population** | BALB/c aged 20 months or more and 8 weeks, both sexes, 5 per arm per time point. About 150 aged animals. |
| **Arms and comparators** | Buffer; vaccine alone; vaccine with PSLN-212 20 µg (manganese-free control); vaccine with PSLN-344 20 µg once; the same three times (days 0, 14, 28); the maximum feasible dose three times; MnCl2 solution intranasally at matched manganese (positive control for the route); cholera toxin (positive control for the brain, as in S10-A). |
| **Endpoints and read-outs** | Primary: manganese concentration by mass spectrometry in olfactory bulb, striatum, cerebellum, blood, liver and lung at 1, 7, 28 and 90 days after the last dose. Secondary: histopathology of nasal cavity, olfactory bulb, brain and lung; lavage cell counts including neutrophils; lung Tnf, Il6 and Il10 at 16 hours, 72 hours, 7 days and 14 days; body weight; tests of smell and motor function at days 28 and 90. |
| **Timing** | 18 January to 18 June 2027; interim at 28 days in early April. |
| **Stop** | Brain manganese above the control range 28 days after a single efficacious dose; olfactory or brain histopathology; lung cytokines not back to within 2-fold of baseline by day 14. |

## Study 4. Is it better than what older adults already receive?

| Item | Specification |
|:----------------|:----------------------------------------------------------------------------------|
| **Must establish** | That intranasal vaccine with PSLN-344 protects aged animals at least as well as high-dose and oil-in-water-adjuvanted intramuscular vaccine, and that it works with the split antigen used in licensed products. |
| **Population** | BALB/c aged 20 months or more, both sexes, 15 per arm for challenge and 10 per arm for virus titer; a young intramuscular standard-dose arm as reference. About 150 aged animals. |
| **Arms and comparators** | Intranasal whole-virus vaccine with PSLN-344; intranasal split vaccine with PSLN-344; intramuscular split vaccine at 4 times the antigen dose; intramuscular split vaccine with a squalene oil-in-water adjuvant; intramuscular split vaccine, standard dose; intranasal whole-virus vaccine alone. |
| **Endpoints and read-outs** | Primary: survival and maximum weight loss after mismatched-virus challenge at day 28. Secondary: hemagglutination-inhibition and neutralizing titers at days 14 and 28; IgA in nasal wash and lavage (never measured so far); lung virus titer at days 3 and 6; interferon-γ CD8 T cells against conserved antigen. |
| **Size** | 15 per arm gives 80% power for a 4-point difference in maximum weight loss (SD 3.7 points in our data). |
| **Timing** | 8 February to 4 June 2027. |
| **Go / no-go** | Go: antibody to the vaccine strain not worse than the best intramuscular arm (lower confidence bound of the titer ratio above 0.5) and better survival or weight loss against mismatched virus. No-go: a licensed-type intramuscular vaccine matches it against mismatched virus. |

## Study 5. Does protection last a season in the aged?

| Item | Specification |
|:----------------|:----------------------------------------------------------------------------------|
| **Must establish** | Protection 90 and 180 days after one dose in aged animals, separated from background mortality. Aged data stop at day 60, where survival was 14/21 against 20/21 at day 14 and unchallenged controls lost 4/21. |
| **Population** | BALB/c vaccinated at 18 months, so that the last challenge falls at 24 months; both sexes; 15 per arm per time point. About 100 aged animals per time point. |
| **Arms and comparators** | Vaccine alone; PSLN-212; PSLN-344; PSLN-344 with a second dose at day 28; two unchallenged arms at each time point (vaccinated with PSLN-344; untreated) to measure background mortality; young animals given PSLN-212. |
| **Endpoints and read-outs** | Primary: survival and weight loss after mismatched-virus challenge at day 90 and day 180. Secondary: serum titers monthly in the same animals; interferon-γ CD8 T cells and lung-resident memory CD8 T cells at days 90 and 180. |
| **Timing** | Dosing 18 January 2027; day-90 read-out in mid-May 2027 (in time for the gate); day-180 read-out early September 2027. |
| **Go / no-go** | Go: survival at day 90 within 20 points of the unchallenged vaccinated arm and at least 50 points above vaccine alone. |

## Formulation characterization (in parallel, November 2026 to June 2027)

Encapsulation efficiency for PSLN-344 is 54.8% (range 49.3% to 59.4% across three preparations; S08-B), at the low end of the five preparations tested (means 52% to 65%). [E27] The work needed: an assay and specification for Mn2+ content; particle size and charge with acceptance limits (stated in the annotation as measured, absent from the workbook); a tighter encapsulation range; and stability at refrigerator temperature, since the material is currently stored freeze-dried at −20 °C.

## Three actions that are not experiments

- **Intellectual property.** The differentiating ingredient in the target population is Mn2+. Counsel should confirm whether our claims cover the Mn2+-coordinated composition and what others hold in that space. This is outside the dataset and I have not assessed it.
- **Antigen strategy.** An adjuvant is licensed as part of a specific vaccine. The program needs a decision on whether the antigen is in-house or partnered before Stage 2, and Study 4 tests the split-antigen format a partner would most likely supply.
- **Data currency.** The files are stamped 3 and 15 September 2026. Confirm that nothing newer exists before the committee meets.

## Gate 1 (late June 2027): all six must be met to enter Stage 2

| Question | Criterion | Source |
|:---------------------------|:---------------------------------------------------------|:-------------|
| Are the data sound? | Survival difference of 50 points or more after reconciliation | Study 0 |
| Is the active relevant to people? | Active on the three commonest human STING variants; Mn2+ effect reproduced in cells from older donors | Study 1 |
| Is our agonist the value driver? | PSLN-344 better than Mn2+ alone and than cGAMP with Mn2+ | Study 2 |
| Is there a usable dose? | A dose with at least 70% survival and no more than 5% post-dose weight loss | Study 2 |
| Is manganese acceptable? | No brain accumulation, no olfactory pathology, lung inflammation resolved by day 14 | Study 3 |
| Is it better than current practice? | Not worse on matched-strain antibody and better against mismatched virus than licensed-type intramuscular vaccine | Study 4 |

Day-90 durability (Study 5) and the nose-only dosing result (Study 2) inform the design of Stage 2 but do not decide the gate.

## Stage 2 and first-in-human, for context only

| Step | Population | Comparators | Endpoints and read-outs | Earliest timing |
|:------------------|:--------------|:----------------|:----------------------------------|:-------------|
| Ferret immunogenicity, challenge and shedding with a clinical-type device | Ferrets, oldest obtainable, both sexes | Intramuscular high-dose and adjuvanted vaccine; intranasal antigen alone | Virus shedding in nasal wash, fever, weight, antibody titers, nasal IgA; brain manganese | July 2027 to February 2028 |
| GLP repeat-dose toxicology | Two species; intranasal route with the clinical device | Vehicle; manganese-free formulation | Standard toxicology plus neurobehavior, olfactory and brain histopathology, manganese toxicokinetics, recovery groups | September 2027 to June 2028 |
| Phase 1, randomized, observer-blind, dose-escalating | Healthy adults 50 to 64, then 65 and over | Licensed high-dose intramuscular vaccine; intranasal antigen alone | Primary: safety and reactogenicity to day 28, with neurological events (facial palsy, loss of smell) and wheeze followed for 6 to 12 months. Secondary: antibody titer ratio and seroconversion at day 28, nasal IgA, interferon-γ T-cell response to conserved antigen. Pharmacology: nasal-fluid interferon-β, CXCL10 and CCL2 at 24 hours; blood interferon signature; circulating follicular helper T cells at day 7; blood manganese | 2029, if both gates are passed |

# 6. If we drop it: what we give up, and why someone reasonably might

**What we give up**

- The only formulation in our dataset that restores vaccine protection in aged animals: 80% survival against 8% and 0% (difference +71 points, CI 59 to 84), consistent across seven experiments. [E1, E2]
- Breadth: protection against virus subtypes not in the vaccine, including a laboratory H5N1 virus after seasonal vaccine (12/14 in the two aged experiments with a valid table, S06-C and S06-F). [Table 1]
- Speed: protection by day 3 after a single dose (5/7 and 6/7). [E4, E6]
- A single-dose, needle-free format, effective in animals with prior influenza immunity. [E9]
- A mechanism worked out in unusual detail for a program at this stage, with a ready biomarker panel (Section 3).
- An understanding of why the unmodified agonist fails in the aged (blunted interferon, CCL2 and GM-CSF responses), which is reusable knowledge for any mucosal adjuvant.

**What we do not give up, because we do not have it**

- Evidence in people or human cells.
- A stand-alone STING-agonist drug. The one test without antigen gave 0/7 survival (S15-H).
- An advantage in adults under 65.
- Demonstrated superiority over licensed enhanced vaccines.
- A safety package.

**The honest case for dropping.** The differentiating ingredient is Mn2+, and we have not shown that our proprietary agonist is needed alongside it. Intranasal manganese carries a known neurotoxicity concern, and intranasal adjuvants face a high safety bar with regulators. The product may need to reach the deep lung, in the population least able to tolerate lung inflammation. The efficacy evidence is from mice, against a weak comparator, and the records behind it are untidy. A committee that weights those risks heavily could decline Stage 1. My view is that Stage 1 is built to fail early: Studies 0 and 1 need no aged animals, and the mid-January checkpoint can stop the program before any of the animal-heavy studies is dosed.

# 7. What I considered and ruled out

**Development options**

| Option | Decision | Reason and evidence |
|:--------------------------|:--------------|:---------------------------------------------------------|
| Take PSLN-212 forward for older adults | Ruled out | 4/49 survival in aged animals against 39/49; antibody titers 3% to 10% of the young benchmark. [E1; Figure 3] |
| Give more PSLN-212 instead of adding Mn2+ | Ruled out | Its Ifnb1 response levels off at 13- to 15-fold between 20 and 40 µg; PSLN-344 at 10 µg already gives 21-fold (S08-A). [E23] |
| Give PSLN-212 twice | Not pursued | A boost raised IgG to 4,411 (H1N1) and 1,086 (H3N2), still below one dose of PSLN-344 at day 14 (7,305 and 5,701); no challenge after boosting; two doses per season is a weaker product. [E29, E16] |
| Add the TLR7/8 agonist R848 | Ruled out | Progressive weight loss to about 91% of baseline by day 10 with one of five animals unrecorded; lung Tnf 200-fold and Il10 180-fold at 16 hours; Ifnb1 lower than with PSLN-344 (24-fold vs 37-fold) (S08-D, S09-A, S01-A). [E24] |
| Use generic cGAMP (CMP-204) in place of CDN-1807 | Not ruled out; tested in Study 2 | Weaker than CDN-1807 without Mn2+ (Ifnb1 7.7-fold vs 16.5-fold); never tested with Mn2+. [E30] |
| Add GM-CSF instead of Mn2+ | Not pursued | GM-CSF restored monocyte-derived dendritic cells with PSLN-212 (5.9% to 13.8%, S02-G), but it is a protein requiring four daily doses, and there are no efficacy data. |
| Position PSLN-344 as a stand-alone immune stimulant or antiviral | Ruled out | 0/7 survival without antigen (S15-H). [E6] |
| Position for all adults | Ruled out as base case | No advantage over PSLN-212 or cGAMP in young animals. [E10, E11] |
| Go straight to GLP toxicology and ferret studies | Ruled out for now | Five smaller studies, two of which need no aged animals, could each end the program first. |
| Drop the program | Not recommended | See Section 6. |

**Interpretations**

| Interpretation | Decision | Reason and evidence |
|:-----------------------------|:--------------|:------------------------------------------------------|
| Early protection is a non-specific interferon effect | Ruled out | PSLN-344 alone 0/7 at day 3 (S15-H). |
| PSLN-344 skews antibody toward IgG1 (a Th2 pattern) | Ruled out | That reading comes from mislabeled columns in S03-B and S03-F; recomputed ratios are 1.85 and 2.30, against 0.54 and 0.46 for PSLN-212 (DI-01). [E22] |
| Deaths at day 60 with PSLN-344 are background mortality of old animals | Partly ruled out | Unchallenged controls did lose 4/21, but after only 3% to 6% weight loss; the PSLN-344 deaths followed 15% to 23% weight loss. Both contribute. [E5] |
| Mn2+ works by changing which cells take up the particle | Cannot be assessed | S08-C is the only block on this and its header order conflicts with S01-B (DI-09). |
| PSLN-344 works by replacing suppressive macrophages and lowering regulatory T cells | Unresolved | Lung regulatory T cells are lower with PSLN-344 (3.0% vs 6.7%, S04-D, n=3) and CD206-positive macrophages fewer (49% vs 71%, S11-E), but the two blocks that test the link have conflicting or duplicated labels (DI-10). |
| An antibody titer of 1:40 can serve as the efficacy surrogate | Ruled out as sole criterion | Aged animals given PSLN-212 reached 40 to 80 and were not protected (Section 3). |

**Data and analyses set aside**

| Item | Reason |
|:--------------------------------------------|:------------------------------------------------------|
| S06-D survival table in the pooled estimate | Row-for-row copy of S06-C (DI-03). Including it gives 46/56 against 6/56 and the same conclusion. |
| "Untreated" groups as efficacy comparators | They were not challenged (DI-16). |
| S03-B and S03-F as printed; second S09-A panel as a 16-hour replicate | Mislabeled (DI-01, DI-02). |
| S11-B neutrophils; S07-A and S07-C macrophage subsets; S08-C uptake; S05-A and S05-B tetramer kinetics | Not interpretable as recorded (DI-08 to DI-11). |
| The unlabeled block at S08 rows 89 to 101 | Thirteen rows that look like survivors, with no group or experiment (DI-15). |
| Pooling young with aged, or the prior-infection study with the day-60 study | Different populations; the second pair shares block labels by error (DI-13). |
| Correcting p-values for the number of blocks | Effects are large and group sizes small; p-values are reported as descriptive. |

# Appendix A. Data-integrity register

![**Figure A1.** Four of the integrity findings. A: the IgG2a:IgG1 ratios printed in S03-B (open) sit under the wrong labels; recomputed from raw titers (filled) the conclusion reverses. B: the second S09-A panel, labeled 16 h, reproduces the S01-A 72-hour values. C: body weights in S15-I are those of S15-C. D: the neutrophil block shares 35 of 100 values with the alveolar-macrophage block.](figures/FigA1_data_integrity_examples.png){width=86%}

| ID | Severity | Location | Issue and evidence | Effect on conclusions | Handling here; action for the lab |
|:-----|:-------|:------------|:-----------------------------------|:------------------|:-----------------|
| **DI-01** | High | S03-B, S03-F (S03!G2:I7, G9:I14) vs S13-A–D (S13!A2:O7) | Column labels of the IgG2a:IgG1 ratio blocks are rotated relative to the raw subclass titers. *Evidence:* Dividing S13-A by S13-B animal-by-animal reproduces S03-B exactly, but under different labels: the values printed under "PSLN-344" are the PSLN-212 ratios; those under "PSLN-212(Y)" are the PSLN-344 ratios; those under "PSLN-212" are the young ratios. Same rotation in S03-F vs S13-C/S13-D. The S13 labels agree with total IgG in S03-A/E. | As printed, PSLN-344 looks IgG1-skewed (ratio 0.54); correctly labeled it is IgG2a-skewed (1.85 H1N1; 2.30 H3N2) and PSLN-212 is the skewed one (0.54; 0.46). Reverses the Th1/Th2 reading of the lead. | Ratios recomputed from S13 raw titers; S03-B/F not used as printed. *Lab action:* Correct headers at source; confirm from plate files. |
| **DI-02** | High | S09-A, columns X–AS (S09!X1:AS9) | Second cytokine panel carries the same label as the first ("16h") but holds the 72-h data. Control is called "PBS" here and "Sham" in S01-A for the same animals. *Evidence:* Back-transformed Ifnb1 values of the second panel match 21 of 21 S01-A 72-h values (7 groups × 3 animals); the first panel matches 21 of 21 S01-A 16-h values. | Treating both panels as 16 h would hide that Tnf/Il6/Il10 are still raised in aged lung at 72 h. | Second panel analyzed as 72 h; values back-transformed from log10. *Lab action:* Relabel; confirm control identity (buffer vs empty liposome). |
| **DI-03** | High | S06-C vs S06-D (S06!M2:Q30 vs S06!A33:E61); S15-D | The two time-to-event blocks are identical row for row in all four groups although they are different experiments (challenge day 14 vs day 3). *Evidence:* All 28 rows identical. The paired weight block S15-D implies 5/7 survivors for PSLN-344 and 5/7 for young PSLN-212, not 7/7. | Day-3 rgH5N1 survival for PSLN-344 is 7/7 (table) or 5/7 (weights). An independent run of the same condition (S15-H) gave 6/7. | S06-D excluded from the base-case pooled analysis; shown as sensitivity. *Lab action:* Retrieve the original S06-D survival sheet. |
| **DI-04** | High | S03-I (S03!A16:F51) vs S13-F (S13!A31:AJ40) | Survival table and body-weight record disagree for PSLN-212 in the matched-virus challenge, and the two blocks do not list the same groups. *Evidence:* Table: all 7 PSLN-212 animals dead by day 6. Weights: all 7 have day-8 readings and 3 regain to 95–99% by day 14. S13-F has a Naive arm and no CMP-204 arm; S03-I the reverse. As printed PSLN-212 dies faster than vaccine alone (log-rank p=0.056) and CMP-204 (3/7) beats PSLN-212 despite lower titers. | PSLN-212 survival after matched-virus challenge is 0/7 or 3/7; CMP-204 vs PSLN-212 ranking on survival is unreliable. PSLN-344 (7/7) and vaccine alone (0/7) agree in both records. | PSLN-344 and Sham used; PSLN-212 reported as a range; no claim made on CMP-204 vs PSLN-212 survival. *Lab action:* Check cage cards for column assignment of CMP-204 and PSLN-212. |
| **DI-05** | High | S03-J (S03!G16:J46) vs S13-G (S13!A42:AE50) | Wild-type H5N1 study: stated n=9 but 10 rows per group; the last PSLN-344 row has an event flag but no day (S03!G46 blank); group sets differ between survival (Sham, PSLN-212, PSLN-344) and weights (PSLN-344, Sham, Naive); animal age and strain not stated; observation stated as 22 days, censoring at 21. *Evidence:* Weights "Naive" (1/10 alive) matches table "Sham" (1/10); weights "Sham" (5/10 alive at day 14) is closest to table "PSLN-212" (3/10). | PSLN-344 result is solid (9/9 with a recorded day; 10/10 by weights). Identity of the two comparator arms is uncertain, so "PSLN-344 beats PSLN-212 against wild-type H5N1" cannot be claimed with confidence. | PSLN-344 survival used; comparators described as "comparator arms, 10–50 %". *Lab action:* Confirm arm identities, age and strain. |
| **DI-06** | Medium | S06-C/E/G, S15-L, S09-F vs paired weight blocks | Survivor counts differ by one animal between time-to-event table and weight record in six group-level comparisons. *Evidence:* S06-C PSLN-212 2/7 vs 1/7; S06-E PSLN-212 0/7 vs 1/7; S06-E PSLN-344 5/7 vs 6/7; S06-G PSLN-344 4/7 vs 5/7; S15-L young PSLN-212 6/7 vs 7/7; S09-F Sham 7 rows vs 8 animals. | Pooled aged BALB/c survival for PSLN-344 is 39/49 by tables and 41/49 by weights; PSLN-212 4/49 vs 7/49. Conclusion unchanged. | Both reported; tables are the base case. *Lab action:* Reconcile against daily health sheets. |
| **DI-07** | Medium | S15 and S09 body-weight blocks | Weight values are shared between blocks that are described as different experiments. *Evidence:* S15-I "3d Vaccine+PSLN-344" equals S15-C PSLN-344 in 40 of 42 cells for days 2–12; the S15-C day-14 row departs from its own trajectories (animal Y 77.9 → 90.1) and shares 5 of 7 values with S15-M PSLN-344. S15-M PSLN-344 shares 16 of 49 cells with S15-A PSLN-344; S15-O PSLN-344 shares 11 of 49 with S15-M; S15-A Sham day 4 equals S15-M PSLN-212 day 4 (7 of 7); S09-C day-12 row is identical for PSLN-212Y and PSLN-344Y (8 of 8). | Body-weight curves cannot be treated as independent confirmation of each survival table; strain-generalization weights (S15-M, S15-O) are partly copies of the BALB/c record. | Weights used only as a cross-check and for pooled morbidity summaries, with this caveat; strain generalization treated as provisional. *Lab action:* Re-export weights from the balance log. |
| **DI-08** | High | S11-B (S11!A8:U14) vs S11-A (S11!A1:U7) | The neutrophil block is not independent of the alveolar-macrophage block. *Evidence:* 35 of 100 cells are identical in the same position (19 of 20 first replicates, 15 of 20 second replicates); group-by-day means correlate r=0.997 and differ by at most 2.5 points. | The only lung-neutrophil (inflammation) read-out in the dataset is unusable; no conclusion on neutrophilic inflammation is possible. | S11-B excluded. *Lab action:* Re-export from FCS files. |
| **DI-09** | Medium | S08-C (S08!A13:D18) vs S01-B (S01!A14:F17) | Header order of S08-C is inconsistent with S01-B. *Evidence:* As printed, type I cells take up PSLN-SRB at 13.8% (S08-C) vs 3.8% for the same condition in S01-B; columns A and B of S08-C share values with the S01-B type II and type I rows (17.7, 17.5, 12.2; 4.92, 4.13). | As printed, Mn2+ would cut type II delivery four-fold (15.8% to 3.8%); with headers in the S01-B order it leaves delivery unchanged (15.8% vs 13.8%). | Not used for any conclusion; both readings stated. *Lab action:* Confirm column order. |
| **DI-10** | Medium | S07-A (S07!A1:H7), S07-C (S07!A15:C20) | S07-C gives both groups the same label ("Ly6C-CD206+ MΦ"). S07-A shows more Ly6C+CCR2+ macrophages with PSLN-212 than PSLN-344 (18.5 vs 3.4 x 10^5 at day 5), the opposite direction to monocytes (S01-D), CCR2-dependent Ly6C+ macrophages (S07-B) and CD206+ macrophage share (S11-E). *Evidence:* Printed labels; group means. | The macrophage-subset → regulatory-T-cell arm of the mechanism cannot be interpreted. | Treated as an unresolved hypothesis; not in the mechanism chain. *Lab action:* Confirm labels for both blocks. |
| **DI-11** | Medium | S05-A, S05-B (S05!A1:I10) | Stated n=3, two observations per time point; conditions contradictory (ovalbumin immunization vs bivalent vaccine; NP366-374 tetramer is H-2Db-restricted, default strain is BALB/c). *Evidence:* Annotation text; cell counts. | Tetramer kinetics are supportive only. | Not used quantitatively. *Lab action:* Clarify strain, antigen and n. |
| **DI-12** | Low | S13-E, S03-J, S09-F, S05-A/B | Stated n differs from rows present. *Evidence:* S13-E: n=5 stated, 7 rows per group. S03-J: 9 vs 10. S09-F Sham: 8 vs 7 (the annotation attributes the 7 to S09-B, where 8 are present). S05-A/B: 3 vs 2. | None on direction; affects exact denominators. | Observed rows used; stated n reported alongside. *Lab action:* Correct labels. |
| **DI-13** | Low | S06!G69, S06!M69 | Block labels S06-E and S06-F are each used twice for different experiments (rows 34–68: day-60 challenge; rows 71–98: prior-infection "imprinting" study). *Evidence:* Annotation confirms. | Risk of pooling unrelated experiments. | Lower blocks referred to as S06-E(r71) and S06-F(r71) and analyzed separately. *Lab action:* Rename. |
| **DI-14** | Low | S08-A (S08!K2:M7) | Group "PSLN-344/R848" is not a preparation described in the annotation (only PSLN-212/R848 is). *Evidence:* Its 20-µg response (GM 29×) is close to PSLN-212/R848 in S01-A (GM 24×). | None. | Reported as labeled; not used for decisions. *Lab action:* Confirm identity. |
| **DI-15** | Low | S08 rows 89–101 (S08!A89:D101) | Unlabeled survival-like fragment: 13 rows, day 14, event 0, no block, group or condition. *Evidence:* Annotation confirms no label exists. | If attributed to a treatment arm it would add 13 survivors. | Excluded. *Lab action:* Identify or delete. |
| **DI-16** | Medium | "Untreated" groups in S06-E/F/G and S15-E/F/G | These animals were not challenged (no vaccine, no adjuvant, no virus), and 4 of 21 died within the 14-day window (1/7, 0/7, 3/7) after only 3% to 6% weight loss. *Evidence:* Annotation; S06!L62:L68, S06!R62:R68, S06!F99:F105; weights carried forward at 94.5–96.6%. | They are a background-mortality benchmark for 22-month-old animals, not a no-vaccine challenge control; survival in aged cohorts has a ceiling near 81%. | Used only as background benchmark. *Lab action:* Add necropsy cause of death. |
| **DI-17** | Medium | Annotation | Conditions missing: challenge virus and timing for S15-L/N; challenge day for S06-E(r71); time point for S13-H, S14-A, S11-E, S07-B; adjuvant given to the "PTX" group in S02-C/E; age in S03-J, S02-G, S02-H, S08-A; instillation volume; Mn2+ content per dose; particle size, zeta potential and stability results (stated as measured, not in the workbook). *Evidence:* Annotation text. | Limits interpretation of strain generalization and prevents any dose or exposure statement for Mn2+. | Stated wherever relevant. *Lab action:* Complete the annotation. |
| **DI-18** | Low | File metadata | Workbook last modified 3 Sep 2026; annotation created 15 Sep 2026. The data could not be confirmed as current to 1 Nov 2026. *Evidence:* docProps/core.xml; PDF metadata. | None if nothing newer exists. | Analysis describes the 3 Sep 2026 data cut. *Lab action:* Confirm no later data. |
| **DI-19** | Low | S08-B (S08!A9:O11) | Encapsulation efficiency is described as measured by CDN-1807 absorbance, but the block includes CMP-204 (cGAMP) and PSLN-R848, which contain no CDN-1807. *Evidence:* Annotation text. | None for the lead (54.8%). | PSLN-344 and PSLN-212 values used. *Lab action:* Clarify assay per preparation. |

# Appendix B. Methods

- **Extraction.** Every numeric cell in the workbook was read with its address (6,819 cells). All but 199 are assigned to a block; the 199 are axis values (day or dose columns) and the 26 cells of the unlabeled S08 fragment.
- **Groups.** Names are used as printed. The suffix (Y) or Y marks young animals (7 to 8 weeks); other groups are aged (20 months or more) unless the annotation says otherwise. Sham is vaccine with empty liposome. Untreated animals received no vaccine, adjuvant or virus.
- **Continuous endpoints.** One-way ANOVA with Tukey's test, as stated in the annotation, on log10 values for titers and mRNA fold-change and on the original scale for percentages; Welch's t-test and the exact Mann–Whitney test as checks. Hemagglutination-inhibition values of 0 (below the 1:10 starting dilution) were set to 5. S09-A was back-transformed from log10.
- **Survival.** Kaplan–Meier estimates, log-rank and Fisher exact tests per experiment. Pooled estimates use exact binomial confidence intervals, the Mantel–Haenszel risk difference stratified by experiment, and a stratified log-rank test. The S03-J row with no day value was excluded.
- **Body-weight records.** An animal was counted as removed when its cells go blank, or when its value is repeated unchanged to the last day (three or more repeats, or two repeats at 90% of baseline or less), which is how the workbook carries forward the last weight of a dead animal.
- **Dose-response.** Four-parameter Hill model with baseline fixed at 1, fitted on the log scale (S08-A).
- **Power.** Exact power for Fisher's test; t-test power for titers and weight loss using the within-group spread in our data.
- **Limits.** No correction for multiple testing across blocks. Group sizes are 3 to 10. The annotation gives no information on randomization, blinding or replication.
- **Background not from our data.** Statements about licensed influenza vaccines, how adjuvants are licensed, the 1:40 antibody threshold, human STING variants, manganese toxicology, where a nasal spray deposits, mouse-to-human age equivalence and population sizes are general background. They are marked as external where they carry weight, were not checked against sources for this document, and none of them is used to compute a number in it.

# Appendix C. Evidence index

| Ref | What | Value | Source cells | Analysis table or script |
|:----|:--------------------|:----------------------------------|:--------------------|:-----------------|
| E1a | Pooled survival, aged BALB/c, 7 experiments: PSLN-344 | 39/49 = 80%  (S03-I 7/7; S06-A 6/7; S06-B 5/7; S06-C 7/7; S06-E 5/7; S06-F 5/7; S06-G 4/7) | S03!E38:E44; S06!D17:D23; S06!J17:J23; S06!P17:P23; S06!J48:J54; S06!P48:P54; S06!D85:D91 | Survival_by_block; Survival_pooled (stats_surv.py, pooled_surv.py) |
| E1b | Pooled survival, aged BALB/c, 7 experiments: PSLN-212 | 4/49 = 8%  (S03-I 0/7; S06-A 1/7; S06-B 0/7; S06-C 2/7; S06-E 0/7; S06-F 1/7; S06-G 0/7) | S03!D31:D37; S06!C10:C16; S06!I10:I16; S06!O10:O16; S06!I41:I47; S06!O41:O47; S06!C78:C84 | Survival_by_block; Survival_pooled (stats_surv.py, pooled_surv.py) |
| E1c | Pooled survival, aged BALB/c, 7 experiments: vaccine alone (Sham) | 0/49 = 0%  (S03-I 0/7; S06-A 0/7; S06-B 0/7; S06-C 0/7; S06-E 0/7; S06-F 0/7; S06-G 0/7) | S03!B17:B23; S06!B3:B9; S06!H3:H9; S06!N3:N9; S06!H34:H40; S06!N34:N40; S06!B71:B77 | Survival_by_block; Survival_pooled (stats_surv.py, pooled_surv.py) |
| E1d | Pooled survival, aged BALB/c, 7 experiments: young + PSLN-212 | 49/49 = 100%  (S03-I 7/7; S06-A 7/7; S06-B 7/7; S06-C 7/7; S06-E 7/7; S06-F 7/7; S06-G 7/7) | S03!F45:F51; S06!E24:E30; S06!K24:K30; S06!Q24:Q30; S06!K55:K61; S06!Q55:Q61; S06!E92:E98 | Survival_by_block; Survival_pooled (stats_surv.py, pooled_surv.py) |
| E2 | PSLN-344 minus PSLN-212 survival, Mantel–Haenszel, 7 experiments | +71 points (95% CI 59 to 84); stratified log-rank chi2=59.0, p=1.6e-14 | as E1a and E1b | Survival_pooled |
| E3 | Same 7 experiments re-derived from body-weight records | PSLN-344 41/49, PSLN-212 7/49, Sham 0/49, young 49/49; difference +69 (56 to 83) | S13!A31:AJ40 (S13-F); S15!A1:AC30 (S15-A,B,C); S15!A41:AJ70 (S15-E,F,G) | Weight_status; Survival_vs_weights (wt_status.py) |
| E4 | Survival by challenge interval, PSLN-344 aged BALB/c | day 3: 5/7 (S06-B); day 14: 20/21 (S03-I, S06-A, S06-C); day 60: 14/21 (S06-E, S06-F, S06-G); day 14 vs day 60 Fisher p=0.045 | S06!J17:J23; S03!E38:E44; S06!D17:D23; S06!P17:P23; S06!J48:J54; S06!P48:P54; S06!D85:D91 | Survival_pooled |
| E5 | Unchallenged aged controls ("Untreated"), day-60 cohorts | 17/21 alive at 14 days (6/7, 7/7, 4/7); the 4 deaths followed only 3% to 6% weight loss | S06!L62:L68; S06!R62:R68; S06!F99:F105; S15!AD43:AJ50, AD53:AJ60, AD63:AJ70 | Survival_by_block; Weight_status |
| E6 | Antigen requirement (aged, rgH5N1 3 d after dosing) | vaccine + PSLN-344 6/7; PSLN-344 alone 0/7; vaccine alone 0/7 | S15!A72:D93 | Survival_by_block |
| E7 | Other strains, aged 20 months | C57BL/6 (S15-L): PSLN-344 6/7, PSLN-212 0/7, Sham 0/7; Swiss Webster (S15-N): 6/7, 2/7, 0/7 | S15!A102:E130; S15!A133:E161 | Survival_by_block |
| E8 | Wild-type H5N1, challenge 2 d after one dose | PSLN-344 9/9 with a recorded day (10 rows; 10/10 by weights); comparator arms 3/10 and 1/10 | S03!G16:J46; S13!A42:AE50 | Survival_by_block; Integrity_register DI-05 |
| E9 | Prior-infection ("imprinting") study, 14 months old at vaccination | naive: PSLN-344 6/7 and 6/7 vs PSLN-212 0/7 and 0/7; imprinted: PSLN-344 6/7 and 6/7 vs PSLN-212 4/7 and 0/7 | S06!G70:K98; S06!M70:Q98 | Survival_by_block |
| E10 | Young animals, head to head | PSLN-344 24/24, PSLN-212 24/24, vaccine alone 0/23 (S09-B, S09-D, S09-F); maximum weight loss 10.7% vs 10.8%; day-14 weight after day-180 challenge 95.6% vs 99.2% (p=0.004) | S09!A11:D35; S09!A38:D62; S09!A65:D88; S09!F11:AD19, F38:AD46, F65:AD73 | Survival_by_block; morbidity.py |
| E11 | Young animals, cGAMP comparator | CMP-204(Y) 7/7, PSLN-344(Y) 7/7, vaccine alone 1/7, naive 0/7 | S13!R2:V30 | Survival_by_block |
| E12 | Lung Ifnb1 at 16 h, fold (geometric mean) [S01-A] | Sham 0.9; PSLN-212 16.5; PSLN-344 36.9; PSLN-212(Y) 37.5 | S01!B3:F3; S01!B5:F5; S01!B8:F8; S01!B9:F9 | Endpoint_descriptives; Scorecard (stats_quant.py) |
| E13 | HAI GMT, H1N1, day 14 [S03-C] | Sham 8; PSLN-212 46; PSLN-344 368; PSLN-212(Y) 485 | S03!K3:K7; S03!M3:M7; S03!N3:N7; S03!O3:O7 | Endpoint_descriptives; Scorecard (stats_quant.py) |
| E14 | HAI GMT, H3N2, day 14 [S03-G] | Sham 10; PSLN-212 35; PSLN-344 320; PSLN-212(Y) 368 | S03!K10:K14; S03!M10:M14; S03!N10:N14; S03!O10:O14 | Endpoint_descriptives; Scorecard (stats_quant.py) |
| E15 | Neutralizing GMT, H1N1, day 14 [S03-D] | Sham 52; PSLN-212 418; PSLN-344 3840; PSLN-212(Y) 6686 | S03!Q3:Q7; S03!S3:S7; S03!T3:T7; S03!U3:U7 | Endpoint_descriptives; Scorecard (stats_quant.py) |
| E16 | IgG GMT, H1N1, day 14 [S03-A] | Sham 56; PSLN-212 393; PSLN-344 7305; PSLN-212(Y) 11959 | S03!A3:A7; S03!C3:C7; S03!D3:D7; S03!E3:E7 | Endpoint_descriptives; Scorecard (stats_quant.py) |
| E17 | IFN-γ+ CD8 T cells vs rgH5N1, day 14, % [S05-F] | Sham 0.7; PSLN-212 1.5; PSLN-344 6.4; PSLN-212(Y) 9.2 | S05!A33:A37; S05!B33:B37; S05!C33:C37; S05!D33:D37 | Endpoint_descriptives; Scorecard (stats_quant.py) |
| E18 | Lung resident-memory CD8 T cells, day 25, % [S05-I] | Sham 0.6; PSLN-212 1.0; PSLN-344 4.0; PSLN-212(Y) 6.0 | S05!A54:A58; S05!B54:B58; S05!C54:C58; S05!D54:D58 | Endpoint_descriptives; Scorecard (stats_quant.py) |
| E19 | Germinal-center B cells, day 7, % [S03-K] | Sham 1.2; PSLN-212 2.3; PSLN-344 6.5; PSLN-212(Y) 9.8 | S03!L17:L21; S03!M17:M21; S03!N17:N21; S03!O17:O21 | Endpoint_descriptives; Scorecard (stats_quant.py) |
| E20 | CD40+ lymph-node DC, day 3, % [S02-D CD40] | Sham 4.0; PSLN-212 5.6; PSLN-344 11.2; PSLN-212(Y) 38.7 | S02!A10:A14; S02!B10:B14; S02!C10:C14; S02!D10:D14 | Endpoint_descriptives; Scorecard (stats_quant.py) |
| E21 | CD86+ lymph-node DC, day 3, % [S02-D CD86] | Sham 7.2; PSLN-212 8.1; PSLN-344 14.5; PSLN-212(Y) 37.9 | S02!F10:F14; S02!G10:G14; S02!H10:H14; S02!I10:I14 | Endpoint_descriptives; Scorecard (stats_quant.py) |
| E22 | IgG2a:IgG1 ratio recomputed from raw subclass titers (geometric mean) | H1N1: PSLN-212 0.54, PSLN-344 1.85, young 2.50; H3N2: 0.46, 2.30, 2.79 | S13!A3:C7 ÷ S13!E3:G7; S13!I3:K7 ÷ S13!M3:O7 | audit_derived.py; Integrity_register DI-01 |
| E23 | Ifnb1 dose-response (Hill fit) | Emax PSLN-344 59×, PSLN-212 17×, CMP-204 8×; ED50 13, 11, 6 µg; 20 µg = 92% of 40-µg response for PSLN-344; PSLN-344 at 10 µg 21.0× vs PSLN-212 at 40 µg 14.7× | S08!A2:M7 | Dose_response (dose_response.py) |
| E24 | Body weight after dosing, no challenge | PSLN-344 lowest mean 96.7% (day 4), 99.8% by day 10; vaccine alone 98.8% at day 4; PSLN-212/R848 90.65% at day 10 (4 of 5 recorded), lowest animal 84.7% | S08!A20:AE26 | stats_misc.py |
| E25 | Lung cytokines, fold vs untreated (geometric mean, n=3) | Tnf 16 h: PSLN-344 40×, PSLN-212 16×, young 14×; Tnf 72 h: 8.4×, 5.2×, 0.5×; Il6 72 h: 7.2×, 1.9×, 3.1×; Ccl2 16 h: 590×, 7.6×, 1,390× | S09!B2:V9 (16 h); S09!Y2:AS9 (72 h, labeled 16h) | Endpoint_descriptives; Integrity_register DI-02 |
| E26 | CNS transcripts at 36 h (mean fold, n=5) | Tnf: buffer 1.00, vaccine alone 1.32, PSLN-344 1.59, cholera toxin 3.50; Ifnb1: 1.00, 1.17, 1.32, 5.50; PSLN-344 vs buffer Tnf Tukey p=0.12, Welch p=0.03 | S10!A2:N7 | stats_misc.py |
| E27 | Encapsulation efficiency, % (mean, range, n=3) | PSLN-344 54.8 (49.3–59.4); PSLN-212 59.6 (54.9–64.0); CMP-204 65.2 (59.1–71.1) | S08!A10:O11 | Endpoint_descriptives |
| E28 | Maximum weight loss among survivors of lethal challenge, 7 aged BALB/c experiments | PSLN-344 aged 11.9% (n=41) vs young + PSLN-212 9.7% (n=49); difference 2.2 points, Welch p=0.007 | S13!A31:AJ40; S15!A1:AC30; S15!A41:AJ70 | morbidity.py; Weight_status |
| E29 | IgG after a day-14 boost (GMT, day 28) | H1N1: PSLN-212 4,411; PSLN-344 15,651; young 40,739. H3N2: 1,086; 12,435; 43,472 | S13!F52:J57; S13!L52:P57 | Endpoint_descriptives |
| E30 | CDN-1807 vs cGAMP in the same vehicle, aged (PSLN-212 vs CMP-204) | Ifnb1 16 h 2.15× (Tukey p=0.001); HAI H1N1 2.0× (p=0.16); neutralizing H1N1 2.3× (p=0.29); survival 0/7 vs 3/7 as printed (S03-I; see DI-04) | S01!B4:F5; S03!L3:M7; S03!R3:S7; S03!C24:D37 | Endpoint_pairwise; Survival_by_block |
