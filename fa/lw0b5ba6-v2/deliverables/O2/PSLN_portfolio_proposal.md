---
title: "PSLN STING-agonist adjuvant program: portfolio-review proposal"
subtitle: "Recommendation, evidence, mechanism of action, biomarkers and gated next steps. Data as of 1 November 2026 (psln_program_dataset.xlsx; psln_program_annotation.pdf)."
---


# 1. Recommendation


> **Recommendation: keep the program in the portfolio. Take PSLN-344 forward as the single lead asset and stop PSLN-212 now. Release funding in gated tranches: first a short data-verification gate that is a hard stop, then a confirmatory and attribution study, before any IND-enabling spend.**
>
> **Why PSLN-344.** It is the only formulation in our data that reliably protects aged (20-month) mice. Across 8 aged-mouse challenge experiments (59 animals per arm), survival was **83% with PSLN-344, 12% with PSLN-212 and 2% with vaccine plus empty liposome**. The stratified hazard ratio for PSLN-344 vs PSLN-212 is 0.083 (95% CI 0.041–0.167) [S03-I, S03-J, S06-A/B/C/E/F/G; A5].
>
> **Why it works.** Mn²⁺ repairs the aged lung's blunted innate response. Lung IFN-β at 16 h is 36.9-fold with PSLN-344 vs 16.5-fold with PSLN-212; the young reference is 37.5-fold [S01-A; A2]. Downstream, PSLN-344 closes a median **74%** (IQR 63–82%) of the age-related deficit across 40 immune readouts [A3].
>
> **Why PSLN-212 goes.** In aged animals it cannot be distinguished from vaccine plus empty liposome on survival (7/59 vs 1/59, p=0.061) [A4/A5]. In young animals it adds nothing: PSLN-212, PSLN-344 and the cGAMP comparator liposome CMP-204 all give 100% survival [S09-B/D/F, S13-E; A4].
>
> **Why gated rather than a full go.** The workbook contains data-integrity defects that the committee will find if it checks (Section 3). The core conclusion survives every sensitivity analysis, with a hazard ratio of 0.08–0.10 [A5]. Four value-defining questions are still open: whether CDN-1807 is needed at all, how PSLN-344 compares with licensed vaccines for older adults, whether intranasal Mn²⁺ is safe for the CNS, and whether protection lasts in aged animals.


### What the committee is asked to approve today


1. **Gate 0, data verification (months 0–2, internal).** Source-record audit of 23 logged issues. Hard stop if the 8 primary survival experiments cannot be substantiated.
2. **Gate 1, confirmatory and attribution study (months 1–7).** Blinded, randomized, both sexes. Adds Mn-only and Mn+cGAMP arms to test whether the proprietary CDN-1807 is required.
3. **Gates 2–3 released only after Gate 1 passes.** These cover benchmarking against licensed enhanced vaccines, durability, Mn/CNS safety, and CMC/device work. They lead toward an IND at around months 18–24 (planning estimate).


### How confident we are


- **Biological signal: high.** Effects are large (8–19-fold titre gains; survival 83% vs 12%) and consistent across about 40 readouts and 8 independent survival experiments.
- **Evidence quality: moderate to low until verified.** There is one exact duplicate experiment, body-weight records reused across experiments and strains, rotated labels, and unexplained deaths among untreated controls (Section 3).
- **Translational risk: substantial.** Open items are the delivery route (alveolar targeting in mice vs nasal spray in people), intranasal Mn²⁺ neurotoxicity, the lack of any head-to-head against licensed enhanced vaccines, female-only data, and day-60 durability (67% vs 100% in young).


Citation convention: [Sxx-Y] = block in psln_program_dataset.xlsx (sheet-block as annotated); [A#] = analysis (Appendix A; numbers reproducible from PSLN_analysis_workbook.xlsx and the code folder). Unless stated, “aged” = 20-month female BALB/c, single intranasal dose, 20 µg adjuvant; PSLN-212(Y) = young (7–8-week) reference. Titres are geometric means; percentages are arithmetic means.


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


# 2. How the asset looks: the evidence


## 2.1 Protection in aged mice (primary outcome)


**Table 1. Survivors / animals at end of follow-up in aged BALB/c mice [A4, A5]**


| Block | Vaccine → challenge, day post-vaccination | Sham | PSLN-212 | PSLN-344 | Young PSLN-212 | Untreated, unchallenged | Log-rank p, 344 vs 212 |
|-------------|----------------------------------|----------|-----------|-----------|------------|--------------|------------|
| S03-I | Bivalent → 10× CA09 H1N1 (homologous), day 14 | 0/7 | 0/7 | 7/7 | 7/7 | – | 0.0004 |
| S06-A | Aichi H3N2 → PR8 H1N1 (heterosubtypic), day 14 | 0/7 | 1/7 | 6/7 | 7/7 | – | 0.008 |
| S06-C | Bivalent → rgH5N1 (heterosubtypic), day 14 | 0/7 | 2/7 | 7/7 | 7/7 | – | 0.007 |
| S03-J | rgH5N1 → wild-type VN04 H5N1, day 2 (age not stated; aged by default) | 1/10 | 3/10 | 10/10 | – | – | 0.001 |
| S06-B | Aichi H3N2 → PR8 H1N1, day 3 | 0/7 | 0/7 | 5/7 | 7/7 | – | 0.0009 |
| S06-E(d60) | Aichi H3N2 → PR8 H1N1, day 60 | 0/7 | 0/7 | 5/7 | 7/7 | 6/7 | 0.002 |
| S06-F(d60) | Bivalent → rgH5N1, day 60 | 0/7 | 1/7 | 5/7 | 7/7 | 7/7 | 0.009 |
| S06-G(d60) | CA09 H1N1 → Perth H3N2, day 60 | 0/7 | 0/7 | 4/7 | 7/7 | 4/7 | 0.015 |
| **Pooled (8)** | **Stratified by experiment; S06-D excluded (duplicate)** | **1/59 (2%)** | **7/59 (12%)** | **49/59 (83%)** | **49/49 (100%)** | 17/21 | **HR 0.083** |


_Pooled PSLN-344 vs PSLN-212: stratified Cox HR 0.083 (95% CI 0.041–0.167), p<0.0001. Mantel–Haenszel risk difference in death -71 percentage points (95% CI -83 to -60). Sensitivity analyses: dropping S03-I (conflicting records, DI-05) gives HR 0.097; dropping S03-J gives HR 0.092; adding the compromised S15-L/N blocks gives HR 0.084 [A5]. “Untreated” = 20-month animals given no vaccine, adjuvant or virus._


**Subgroups [A5].** Challenge at day 14: 20/21 (95%) vs 3/21 (14%). Early challenge (day 2–3): 15/17 (88%) vs 3/17 (18%). Heterosubtypic challenges: 32/42 (76%) vs 4/42 (10%). Day-60 challenge: 14/21 (67%) vs 1/21 (5%). Middle-aged (14-month) mice, with or without a prior PR8 infection (“imprinting”): PSLN-344 12/14 in both groups, vs PSLN-212 0/14 (naive) and 4/14 (imprinted) [S06-E/F imprint; A5]. PSLN-344 survivors still lose somewhat more weight than protected young animals: mean nadir 87.3% vs 89.8% (p=0.0035) [S15-A/B/C/E/F/G; A9]. PSLN-344 therefore attenuates disease rather than preventing it.


**Durability is the weak point.** At day 60, PSLN-344 protected 14/21 aged animals vs 21/21 young (p=0.009). Over the same 14 days, 4/21 untreated, unchallenged aged animals died, so the day-60 PSLN-344 result is statistically indistinguishable from background mortality (17/21 survived; p=0.48) [S06-E/F/G(d60); A4]. Antibody durability in aged animals was not measured beyond day 28.


## 2.2 Immunology: PSLN-344 vs PSLN-212 in aged mice


**Table 2. Key immune readouts (n=5 per group unless noted; one-way ANOVA + Tukey on log₁₀ scale for titres/fold-changes, linear for %) [A2, A3]**


| Stage | Readout [block] | Sham | PSLN-212 | PSLN-344 | Young 212 | PSLN-344 vs 212 (95% CI) | Tukey p | Age gap closed |
|----------|--------------------------------|--------|----------|----------|----------|--------------------|---------|---------|
| Innate | Lung Ifnb1, 16 h (fold) [S01-A] | 0.94 | 16.5 | 36.9 | 37.5 | ×2.2 (1.8–2.7) | 0.0006 | 98% |
| Innate | Lung Gm-csf, 36 h (fold) [S02-F] | 1.20 | 1.59 | 8.52 | n/a | ×5.4 (3.9–7.3) | <0.0001 | n/a |
| Myeloid | Lung Ly6C+ monocytes, d4 (%) [S01-D] | 10.4 | 16.7 | 30.6 | 32.2 | +13.8 pp (+8.1 to +19.5) | <0.0001 | 89% |
| DC | CCR7+ migratory DC, 72 h (%) [S02-A] | 2.54 | 7.28 | 30.7 | 35.0 | +23.4 pp (+13.8 to +33.0) | <0.0001 | 84% |
| DC | Antigen+ DC in MLN, 36 h (%) [S02-C] | n/a | 1.77 | 7.09 | 9.39 | +5.3 pp (+3.6 to +7.1) | <0.0001 | 70% |
| DC | MLN DC CD86+, d3 (%) [S02-D CD86] | 7.18 | 8.13 | 14.5 | 37.9 | +6.4 pp (+3.0 to +9.9) | 0.033 | 22% |
| GC | ICOS-high Tfh, d7 (%) [S04-A] | 0.30 | 3.82 | 10.3 | 13.6 | +6.4 pp (+2.6 to +10.3) | 0.0002 | 66% |
| GC | Tfr (Foxp3+), d7 (%) [S04-B Foxp3] | 22.6 | 26.7 | 10.8 | 7.12 | -15.9 pp (-24.0 to -7.7) | 0.0002 | 81% |
| GC | GC B cells, d7 (%) [S03-K] | 1.18 | 2.34 | 6.54 | 9.82 | +4.2 pp (+2.3 to +6.1) | 0.007 | 56% |
| Antibody | HAI anti-CA09, d14 (GMT) [S03-C] | 7.58 | 45.9 | 368 | 485 | ×8.0 (3.9–16.4) | <0.0001 | 88% |
| Antibody | HAI anti-Aichi, d14 (GMT) [S03-G] | 10.0 | 34.8 | 320 | 368 | ×9.2 (4.2–20.2) | <0.0001 | 94% |
| Antibody | Neutralising anti-CA09, d14 (GMT) [S03-D] | 52.2 | 418 | 3,840 | 6,686 | ×9.2 (3.1–27.2) | 0.0002 | 80% |
| Antibody | IgG anti-CA09, d14 (GMT) [S03-A] | 55.7 | 393 | 7,305 | 11,959 | ×18.6 (9.1–37.9) | <0.0001 | 86% |
| Antibody | IgG2a/IgG1 anti-CA09 (from S13-A/B) [S13-A/B] | n/a | 0.54 | 1.85 | 2.50 | ×3.4 (1.6–7.4) | 0.016 | n/a |
| CD8 | Lung Ki-67+ CD8, d3 (%) [S05-D] | 0.83 | 3.48 | 9.38 | 9.94 | +5.9 pp (+3.6 to +8.2) | 0.0008 | 91% |
| CD8 | IFN-γ+ CD8 (H5 restim), d14 (%) [S05-F] | 0.67 | 1.50 | 6.36 | 9.18 | +4.9 pp (+3.6 to +6.1) | <0.0001 | 63% |
| CD8 | Lung TRM CD69+CD103+, d25 (%) [S05-I] | 0.58 | 1.00 | 3.96 | 6.04 | +3.0 pp (+2.2 to +3.7) | <0.0001 | 59% |
| Memory | IFN-γ+ CD8, d60 (%) [S05-G] | 1.46 | 3.04 | 9.86 | 14.4 | +6.8 pp (+3.4 to +10.3) | 0.0008 | 60% |


_×: geometric-mean ratio; pp: percentage-point difference. Age gap closed = (PSLN-344 − PSLN-212)/(young PSLN-212 − PSLN-212), on the analysis scale. Sham HAI values recorded as 0 (below the 1:10 LOD) imputed as 5 (DI-18). The IgG2a/IgG1 ratio is recomputed from the source titres (S13-A/B) because the printed ratio block S03-B carries rotated labels (DI-04)._


**Multiplicity.** Across the 40 curated readouts (Fig 3), 36 PSLN-344 vs PSLN-212 differences stay significant after Holm correction using the block-wise Tukey p-values, and 31 using Welch p-values [A2, A3]. The conclusion does not depend on selective reporting.


### Where PSLN-344 falls short


- **Dendritic-cell co-stimulation is barely restored.** CD40+ DCs are 11.2% vs 5.6% (young 38.7%; Tukey p=0.16) and CD86+ DCs 14.5% vs 8.1% (young 37.9%). That is only 17–22% of the age gap [S02-D; A3], the weakest link in the mechanism.
- **CD8 effector and memory responses are about 60% restored.** Examples: IFN-γ+ CD8 at d60 is 9.9% vs 3.0% (young 14.4%), and lung TRM is 4.0% vs 1.0% (young 6.0%) [S05-G, S05-I; A3]. This matches the loss of protection by day 60.
- **Boosting narrows the H1 gap.** After a day-14 boost, anti-CA09 IgG is 15,651 vs 4,411 (×3.5, Tukey p=0.19) but remains ×11.5 for H3 [S13-I/J; A2].
- **The aged lung response is prolonged and TNF-rich, with or without Mn²⁺.** At 72 h, Ifnb1 is still 4.2-fold with PSLN-344 and 3.4-fold with PSLN-212, vs 1.5-fold in young animals (Tukey p<0.0001 and p=0.0006) [S01-A; A2]. At 16 h, Tnf is 40-fold with PSLN-344 vs 14-fold in young (Welch p=0.009; Tukey p=0.058) [S09-A]. At about 72 h, Il6 is 7.2-fold and Tnf 8.4-fold, vs 3.1-fold and 0.5-fold in young (n=3; timepoint mislabelled, DI-08) [S09-A panel 2]. Post-vaccination weight loss was minimal (Table D4), but this belongs on the safety watch-list for older recipients.


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


# 3. Data integrity: what the committee should hear from us first


Before the committee decides, it should know that the workbook has defects that a careful reviewer will find. I ran systematic scans for exact and partial duplication (values, whole experiments, per-animal weight trajectories), checked derived values against their sources, and reconciled survival records against body-weight records [A1]. 23 issues are logged (Appendix B). The 7 critical ones:


**Table 3. Critical data-integrity findings [A1] (see Fig 8 for visual exhibits)**


| ID | Blocks | Finding | Consequence for the case |
|-------|-----------------|------------------------------------------------------------|------------------------------------|
| DI-01 | S06-C, S06-D | S06-D (rgH5N1 challenge on day 3) is cell-for-cell identical to S06-C (challenge on day 14) across all 4 groups x 7 animals. Moreover, the S15-D weights for the S06-D animals show 2 PSLN-344 and 2 young deaths that S06-D does not record. | S06-D excluded; the day-3 rgH5N1 claim has no independent data. |
| DI-02 | S15-H, S15-I vs S15-C | Body weights of the '3d Vaccine+PSLN-344' group (S15-I) reproduce the PSLN-344 group of S15-C, a different experiment: 6 of 7 animals are identical on every day from d2 to d12 (the 7th on 4 of 7 days). Values differ only at d14, where an animal that recovers in S15-C (77.9% -> 90.1%) is carried forward as dead in S15-I. | S15-H/S15-I excluded from primary evidence; reported as sensitivity only. |
| DI-03 | S15-L/M, S15-N/O vs S09-E, S15-A | C57BL/6 block S15-M: young-reference (PSLN-212(Y)) weights reproduce BALB/c S09-E PSLN-344(Y) animals (6 animals, 4-7 identical days); aged PSLN-344 shares 2 animals (5/7 days) with BALB/c S15-A. S15-O (Swiss Webster) PSLN-344 shares partial trajectories (3 or more days) with S15-M and S15-A. | Cross-strain survival (S15-L, S15-N) moved to sensitivity analysis; strain generality must be re-established. |
| DI-04 | S03-B, S03-F vs S13-A..D | Printed IgG2a/IgG1 ratios carry rotated group labels: S03-B 'PSLN-212' = S13 PSLN-212(Y), 'PSLN-344' = S13 PSLN-212, 'PSLN-212(Y)' = S13 PSLN-344 (identical to 4 d.p.). Taken as printed, PSLN-344 would look Th2-skewed; the source titres show the opposite. | Use S13-derived ratios only; S03-B/S03-F as printed are not used. |
| DI-05 | S13-F vs S03-I; S13-G vs S03-J | Body-weight blocks do not match the survival blocks they describe. S13-F lists 'Naive' (not in S03-I) and omits CMP-204; its 'PSLN-212' arm has 3 animals recovering to 95-99% at d14 although S03-I records all 7 PSLN-212 animals dead by d6. S13-G lists 'Naive' (not in S03-J) and omits PSLN-212; its 'Sham' arm has 4 recovering animals although S03-J records 9/10 Sham deaths. | PSLN-344 arms are concordant (all survive in both). PSLN-212 arm of S03-I treated as uncertain; sensitivity analysis run without it. |
| DI-06 | S11-A, S11-B | Alveolar macrophage (S11-A) and neutrophil (S11-B) blocks share the first 1-2 of 5 replicate values in every group at every timepoint - biologically implausible for two different cell types. | Both blocks excluded. |
| DI-07 | S06-E(d60), S06-G(d60), S15-E, S15-G | 'Untreated' 20-month animals (no vaccine, adjuvant or virus) died: 1/7 (S06-E) and 3/7 (S06-G) within 14 days; matching weight records are carried forward (LOCF) after death without infection-like weight loss. | Background non-infectious mortality (4/21 = 19% over 14 d) is reported alongside every day-60 aged result; PSLN-344 deaths in S06-G (3/7) are indistinguishable from background. |


> **Does the recommendation survive?** Yes. The PSLN-344 vs PSLN-212 conclusion rests on blocks with no duplication flags: 8 survival experiments and about 40 immune readouts. It also holds in every sensitivity analysis: dropping the conflicting S03-I gives HR 0.097, dropping S03-J gives HR 0.092, and adding the compromised cross-strain blocks gives HR 0.084 [A5].
>
> **Claims we should not make until verified:** “protects against H5N1 when challenged 3 days after vaccination” (S06-D duplicate; S15-H/I copied weights); “works across mouse strains” (S15-L–O); “PSLN-344 is Th2-skewed” (an artefact of the rotated S03-B/F labels); any alveolar-macrophage or neutrophil kinetics (S11-A/B); “Mn²⁺ improves epithelial uptake” (S08-C contradicts S01-B). Rapid protection is still supported by the unflagged S03-J (day 2, 10/10 vs 3/10) and S06-B (day 3, 5/7 vs 0/7).
>
> **Recommended handling.** Disclose these findings to the committee proactively, with the Gate 0 audit plan. Where records cannot be reconciled, refer them to the standard research-integrity process; the patterns (copied trajectories with altered final values) are not explainable as transcription slips. This does not by itself imply misconduct, but it has to be resolved before the dataset supports an investment decision.


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


# 4. Mechanism of action, built from our data


The data support a seven-step mechanism (Fig 6). The central idea is that **ageing blunts the lung's type I interferon response to the cyclic dinucleotide, and co-formulated Mn²⁺ restores it**. That unlocks an IFNAR- and GM-CSF-dependent monocyte-to-dendritic-cell program, which in turn drives dendritic-cell migration, T follicular helper and germinal-centre responses, Th1-type antibody, and CD8 effector and tissue-resident memory.


![Fig 6. Proposed mechanism of action with supporting numbers and blocks. Dashed boxes = correlative or inferred steps that need confirmation (Gate 1B).](figures/fig6_moa_schematic.png){width=100%}


**Table 4. Mechanism claims and the strength of the supporting evidence [A2, A6, A7]**


| Step | Claim | Evidence (aged PSLN-344 vs PSLN-212 unless stated) | Evidence grade |
|-----------|--------------------------|------------------------------------------------------------|-----------------------|
| 1 Delivery | Liposome reaches alveolar type II cells and alveolar macrophages | AECII 15.8% vs AECI 3.8% SRB+ (p<0.0001); liposome vs free dye 42× [S01-B]; AM uptake 43.1% WT vs 12.7% SP-A/D-KO (p<0.0001; young KO mice) [S01-C] | Direct (tracer, knockout in young mice) |
| 2 Sensing | Mn²⁺ raises the CDN-driven IFN-β response to the young level | 16 h Ifnb1 36.9× vs 16.5× (GMR 2.23, 1.85–2.69; Tukey p=0.0006); young 37.5× [S01-A]; Hill-fit top 52× vs 16×, ED50 11 vs 10 µg [S08-A; A7]; encapsulation 55% vs 60% (n.s.) [S08-B] | Direct for IFN-β; STING dependence and Mn mechanism not tested |
| 3 Spread | Signal spreads between cells through gap junctions | Carbenoxolone: recruited monocytes 3.1% vs 7.3% (p=0.003) [S11-C] | Inferred (non-specific blocker) |
| 4 Myeloid | IFNAR + GM-CSF convert recruited monocytes into moDCs; CCR2-dependent | Gm-csf 8.5× vs 1.6× at 36 h [S02-F]; monocytes 30.6% vs 16.7% d4 [S01-D]; CCR2 antagonist 9.9% → 3.3% [S07-B]; IFNAR-KO BM moDC 2.1% vs 19.7%, GM-CSF rescue 12.4% [S02-H]; GM-CSF add-back to PSLN-212 5.9% → 13.8% [S02-G] | Direct (genetic + pharmacologic), partly in young mice |
| 5 DC | DCs mature, migrate (Gαi) and prime T cells | CCR7+ DC 30.7% vs 7.3%; antigen+ MLN DC 7.1% vs 1.8%; OT-I priming 18.7% vs 0.8% [S02-A/C/E]; pertussis toxin 30.9% → 6.8% in MLN [S05-C]; CD40/CD86 only ≈20% restored [S02-D] | Direct; co-stimulation gap remains |
| 6 Adaptive | Tfh/GC drive Th1-type antibody; CD8 effector and TRM | Tfh 10.3% vs 3.8%, Tfr 10.8% vs 26.7% [S04]; GC B 6.5% vs 2.3% [S03-K]; HAI ×8–9, IgG2a/IgG1 ×3.4–5.0 [S03, S13]; IFN-γ+ CD8 6.4% vs 1.5%, TRM 4.0% vs 1.0% [S05-F/I]; INCB3344 GZMB+ CD8 6.8% → 1.4% [S02-I] | Correlative (group level) + CCR2 intervention |
| 7 Outcome | Protection in aged mice | 83% vs 12% survival, HR 0.083 [A5] | Direct; no per-animal immune–outcome link |


**What the mechanism does not yet establish.** (i) No STING-deficient animals were tested, so on-target STING dependence is inferred. (ii) There is no Mn-only liposome. Mn²⁺ is itself a known innate stimulus (external context), so we cannot say how much of the benefit needs CDN-1807. The only molecule-level comparison favours CDN-1807 over cGAMP in the same vehicle: IFN-β 16.5× vs 7.7× (GMR 2.15, p=0.001) [S01-A; A2]. (iii) Several mechanistic interventions (S02-H, S02-I, S12-A) were done in young mice. (iv) Without Mn²⁺, aged lungs accumulate Ly6C+CCR2+ macrophages: 19.0 vs 3.4 ×10⁵ at day 5 (two-way ANOVA interaction p<0.0001) [S07-A; A12]. These may be the suppressive population, but the transfer experiment that would test this (S07-C) is uninterpretable because of duplicated labels (DI-10).


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


# 5. Biomarkers to validate efficacy


Each of the readouts below separates the protective regimens (aged PSLN-344, young PSLN-212) from the non-protective ones (aged Sham, aged PSLN-212) at the regimen level; at n=5 the per-animal AUC is 1.0 for nearly all of them [A10]. AUC therefore cannot rank them, so selection rests on three criteria: how close the marker is to the mechanism, whether it can be measured in people, and whether regulators accept it. Biomarkers and survival come from different animals, so these are regimen-level markers, not validated individual correlates of protection. Study 3C is designed to close that gap.


**Table 5. Biomarker plan [A2, A10] (PD = pharmacodynamic)**


| Tier | Mouse marker [block] | Our data (aged PSLN-344 vs PSLN-212 unless stated) | Human analogue | Proposed use |
|--------------|-----------------------|--------------------------------|--------------------------|------------------------|
| PD (6–24 h) | Lung Ifnb1 16 h [S01-A] | Sham 0.94×; 212: 16.5×; 344: 36.9×; young 37.5×; CMP-204 7.7×. Protective ≥32.6×, non-protective ≤19.0× | Nasal-lining-fluid IFN-β/IFN-λ and CXCL10 (nasosorption); blood ISG score at 24 h | Phase 1 “young-equivalence” PD endpoint: the older-adult response should reach the young-adult response to the same dose |
| PD (6–36 h) | Lung Ccl2 16 h and Gm-csf 36 h [S09-A†, S02-F] | Ccl2 590× vs 7.6× (GMR 77); Gm-csf 8.5× vs 1.6× (GMR 5.4) | Nasal CCL2; serum CCL2 and GM-CSF | Dose selection; confirms the Mn-specific arm of the mechanism |
| Cellular (d3–7) | Ly6C+ monocytes d4, CCR7+ DC [S01-D, S02-A] | 30.6% vs 16.7%; 30.7% vs 7.3% | Blood monocyte IFN signature (e.g., SIGLEC1/CD169) | Exploratory |
| Germinal centre (d7) | ICOS-high Tfh; Tfr; GC B [S04-A/B, S03-K] | Tfh 10.3% vs 3.8%; Tfr 10.8% vs 26.7%; GC B 6.5% vs 2.3% | Blood ICOS+PD-1+CXCR5+ cTfh and plasmablasts at d7; cTfr:cTfh ratio | Early read of adjuvant effect in Phase 1 (d7) |
| Humoral (d14–28) | HAI; microneutralization; IgG2a/IgG1 [S03-C/G/D, S13-A–D] | HAI ×8.0 (CA09), ×9.2 (Aichi); neut ×9.2; IgG2a/IgG1 ×3.4 | HAI GMT and seroconversion; MN; IgG subclasses | Primary immunogenicity endpoint (licensure surrogate); non-inferiority vs licensed comparator |
| Mucosal (d14–28) | Not measured | Gap: no IgA data anywhere in the dataset | Nasal-wash secretory IgA | Must be added (Gates 1–2); the core rationale for intranasal delivery |
| Cellular memory (d14–180) | IFN-γ+ CD8; TRM [S05-F/G/I, S14-A] | d14 6.4% vs 1.5%; d60 9.9% vs 3.0%; TRM 4.0% vs 1.0% | IFN-γ ELISpot to conserved NP/M1 peptides; nasal TRM (curettage, exploratory) | Supports the heterosubtypic (mismatch-season) claim |
| Safety | CNS Ifnb1/Tnf/Isg15 36 h [S10-A]; weight [S08-D]; lung Il6/Tnf 72 h [S09-A†] | No CNS signal vs PBS (p≥0.54); weight nadir 96.4% vs 98.2%; Il6 7.2×, Tnf 8.4× at about 72 h | Olfactory testing (e.g., UPSIT), blood Mn, serum IL-6/CRP, facial-nerve AESI monitoring | Stopping rules in Phase 1 |


_† S09-A shares its animals with S01-A (DI-08); its panel 2 is the ~72 h timepoint despite the 16 h label._


**Go thresholds for the Gate 1 replication** are set deliberately below the observed effects to allow for regression to the mean: Ifnb1 16 h ratio ≥2 (observed 2.23, 95% CI 1.85–2.69) [S01-A]; Gm-csf 36 h ratio ≥3 (observed 5.36, 3.93–7.32) [S02-F]; HAI GMT ratio ≥4 (observed 8.0, 3.9–16.4) [S03-C]; IFN-γ+ CD8 d14 at least 2× PSLN-212 (observed 4.2×) [S05-F]; survival ≥70% and ≥40 points above PSLN-212 (observed 95% vs 14% at day 14) [A5].


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


# 6. Next steps: a gated plan


M0 is the committee decision. Timings are planning estimates. Aged (≥20-month) mice are the critical-path resource and must be ordered at M0.


**Table 6. Gated development plan**


| Gate | Study | Question it answers | Months | Decision at |
|------|----------------------------------------|-------------------------------------------|--------------|-----------------|
| 0 | Data verification and reconciliation | Are the primary data real and correctly labelled? | M0–M2 | M2 (hard stop) |
| 1 | 1A Confirmatory efficacy + attribution (aged, both sexes) | Does PSLN-344 beat PSLN-212 when blinded? Is CDN-1807 needed? | M1–M7 | M7 |
| 1 | 1B Mechanism confirmation (STING, IFNAR, GM-CSF) | Is the MoA on-target? Are the PD biomarkers valid? | M2–M6 | M7 |
| 2 | 2A Benchmark vs licensed enhanced vaccines (aged) | Is IN PSLN-344 differentiated vs IM high-dose/adjuvanted? | M7–M12 | M12 |
| 2 | 2B Durability and boosting (aged) | Does protection last to d90–d180? Does a boost fix it? | M7–M15 | M12 (interim), M15 |
| 3 | 3A Mn/CNS and intranasal safety (non-GLP → GLP) | Is intranasal Mn²⁺ safe? Where is the NOAEL? | M3–M15 | M9 (pilot), M15 |
| 3 | 3B CMC, stability and delivery device | Can it be made, stored and delivered to the right airway tissue? | M0–M12 | M12 |
| 3 | 3C Correlates of protection (embedded in 1A, 2A, 2B) | Which per-animal markers predict protection? | M1–M15 | M15 |
| – | Phase 1/2a first-in-human (older adults) | Safe? Young-equivalent PD? Non-inferior HAI plus mucosal IgA? | IND ≈M18–24 | – |


### Gate 0: data verification and reconciliation (M0–M2)


| Item | Detail |
|--------------------|----------------------------------------------------------------------------------------------------|
| **Must establish** | That the primary survival and immunogenicity data are authentic, correctly labelled and complete before any further spend. |
| **Population** | Not an animal study. Scope: all 23 logged issues (Appendix B), DI-01 to DI-07 first. Collect notebooks, randomisation and cage cards, mortality logs, raw FACS (.fcs) and qPCR run files, and ELISA/HAI plate maps. Recover the real S06-D, S15-H/I and S15-L–O data or declare them lost. Re-gate S11-A/B from the raw files. |
| **Arms / comparators** | Source records vs the workbook, cell by cell for the flagged blocks; an independent QA reviewer plus a statistician not involved in the original work. |
| **Endpoints** | For each issue: resolved (record found and workbook corrected), explained, or unresolvable. |
| **Readouts & timing** | Interim list at week 4; signed reconciliation memo and version-locked dataset at M2. |
| **Sample size** | n/a |
| **Go / no-go** | Go: source records substantiate the 8 primary survival experiments (S03-I, S03-J, S06-A/B/C, S06-E/F/G d60) and the d14 immunogenicity blocks (S03, S04, S05, S13, S14). No-go: two or more primary survival experiments cannot be substantiated, or duplication extends into primary blocks. Then stop, refer to research integrity, and fund nothing further until a clean re-run. |


### Gate 1A: confirmatory efficacy and attribution study (M1–M7)


| Item | Detail |
|--------------------|----------------------------------------------------------------------------------------------------|
| **Must establish** | That PSLN-344 beats PSLN-212 in aged mice under blinded, randomised, pre-registered conditions in both sexes; and whether the proprietary CDN-1807 is required or Mn²⁺ does the work. |
| **Population** | Aged BALB/c 20–22 months, **female and male** (all existing data are female). Young 8–10-week reference. Aged C57BL/6 confirmatory arm set to re-establish strain generality (S15-L/M compromised). |
| **Arms / comparators** | Single intranasal dose of bivalent inactivated vaccine (CA09 0.5 µg + Aichi 1 µg HA) with 20 µg adjuvant, as in S03: (1) vaccine + empty PSLN (Sham); (2) PSLN-212; (3) PSLN-344; (4) **Mn-PSLN without CDN-1807**; (5) **Mn-PSLN + cGAMP**; (6) young + PSLN-212; (7) aged, unvaccinated, unchallenged (background mortality). Coded vials; sex-stratified randomisation. |
| **Endpoints** | Primary: survival for 14 d after 10× mLD50 CA09 challenge at d14, PSLN-344 vs PSLN-212 (log-rank stratified by sex). Key secondary: heterosubtypic cohort (Aichi vaccine → PR8 at d14) survival; HAI and MN GMT at d14; **nasal-wash and BAL IgA** (new); **lung viral titre at d3 and d5 post-challenge** (new; mortality alone cannot separate reduced replication from tolerance); weight nadir in survivors. PD satellites: lung Ifnb1 16 h, Gm-csf and Ccl2 36 h, CCR7+ DC 72 h. |
| **Readouts & timing** | PD at M3–M4; HAI/IgA at M4; survival and viral load at M5–M6; final report and decision at M7. |
| **Sample size** | 24/arm for survival (12 F + 12 M): 90% power for 70% vs 20% (Fisher, α=0.05) [A11]. HAI needs ≥11/arm to detect a 2-fold difference (pooled SD log₂ HAI = 0.66) [A11]. PD satellites n=8/arm (Ifnb1 needs only 3/arm; SD log₂ = 0.17). |
| **Go / no-go** | Go: PSLN-344 survival ≥70% and ≥40 points above PSLN-212 (lower 95% CI bound of the difference >0); HAI GMR ≥4; Ifnb1 ratio ≥2; effect in both sexes. Attribution rule: if Mn-only (arm 4) reaches ≥80% of PSLN-344 on HAI and survival, CDN-1807 is not needed: re-scope IP and CMC (a strategic pivot, not automatically a stop). If Mn + cGAMP (arm 5) matches PSLN-344, the moat is vehicle + Mn, not CDN-1807: freedom-to-operate review before Gate 2. No-go: PSLN-344 survival <50% or not different from PSLN-212. |


### Gate 1B: mechanism confirmation (M2–M6)


| Item | Detail |
|--------------------|----------------------------------------------------------------------------------------------------|
| **Must establish** | That the effect is on-target (STING-dependent) and that the IFNAR/GM-CSF axis, and therefore the proposed PD biomarkers, sits on the causal path. |
| **Population** | Young Sting1-deficient, Ifnar1-deficient and wild-type mice. Aged wild-type mice given anti-IFNAR1 or anti-GM-CSF neutralising antibody or isotype control. |
| **Arms / comparators** | PSLN-344 vs PSLN-212 within each genotype or treatment; wild-type and isotype controls as comparators. |
| **Endpoints** | Lung Ifnb1 16 h, Gm-csf 36 h, moDC d3, antigen+ MLN DC 36 h, HAI d14. |
| **Readouts & timing** | Innate readouts M3–M4; HAI M5; report M6. |
| **Sample size** | n=8/arm (sufficient for ≥2-fold effects given observed SDs [A11]). |
| **Go / no-go** | Go: ≥70% loss of PSLN-344 PD and HAI in STING-deficient mice; GM-CSF neutralisation reduces moDC and HAI in aged animals. If the effect is STING-independent, the MoA and biomarker plan must be rebuilt before Gate 2. |


### Gate 2A: benchmark against licensed enhanced vaccines for older adults (M7–M12)


| Item | Detail |
|--------------------|----------------------------------------------------------------------------------------------------|
| **Must establish** | That intranasal PSLN-344 is differentiated from what older adults already receive: non-inferior on HAI and better on mucosal or cross-protective immunity. |
| **Population** | Aged BALB/c and C57BL/6, both sexes, 20–22 months. |
| **Arms / comparators** | (1) IN vaccine + PSLN-344; (2) IM standard-dose vaccine; (3) IM high-dose (4× HA); (4) IM vaccine + squalene oil-in-water emulsion (MF59-like); (5) IN vaccine alone; (6) IM vaccine + PSLN-344 (route control). |
| **Endpoints** | Primary: HAI GMT at d28, non-inferiority of IN PSLN-344 vs the best IM comparator (margin 1.5-fold). Key secondary: nasal and BAL IgA; lung TRM; IFN-γ ELISpot (NP/M1); heterosubtypic challenge at d28 (survival and lung viral titre); drifted-strain challenge. |
| **Readouts & timing** | Immunogenicity d28 at ≈M9; challenge outcomes ≈M10–M11; decision M12. |
| **Sample size** | 23/arm for 90% power on the HAI non-inferiority test (one-sided α=0.025) [A11]. |
| **Go / no-go** | Go: non-inferior HAI **and** superiority on at least one mucosal or cross-protection endpoint (IgA, TRM or heterosubtypic survival). No-go: an IM enhanced vaccine matches PSLN-344 on these endpoints; the product is then undifferentiated, so stop or reposition (e.g., pandemic H5 only). |


### Gate 2B: durability and boosting in aged mice (M7–M15)


| Item | Detail |
|--------------------|----------------------------------------------------------------------------------------------------|
| **Must establish** | Whether protection lasts to d90–d180 in aged animals, and whether a boost fixes the day-60 shortfall (67% vs 100% in young). |
| **Population** | Aged BALB/c (plus C57BL/6), both sexes, 20 months at vaccination, with a young reference. |
| **Arms / comparators** | PSLN-344 prime only; PSLN-344 prime + boost (d28 or d90); best IM comparator from 2A; young reference; background-mortality control (unvaccinated, unchallenged). |
| **Endpoints** | Primary: HAI, MN and IgA kinetics (d14, 28, 60, 90, 180). Secondary: IFN-γ ELISpot and lung TRM at d60/180; heterosubtypic challenge at d90 and d180 (survival and viral load). |
| **Readouts & timing** | d90 interim at ≈M11–M12; d180 and challenge outcomes at ≈M14–M15. |
| **Sample size** | Immunogenicity n=12/arm. Challenge n=20–24/arm/timepoint; the observed day-60 gap (67% vs 100%) would need ≈42/arm to confirm (90% power) [A11], so immunogenicity is primary and survival secondary. |
| **Go / no-go** | Go: PSLN-344 (with or without a boost) gives ≥70% survival at d90 and HAI GMT ≥ comparator at d180. No-go: survival <50% at d90 even with a boost. |


### Gate 3A: Mn²⁺/CNS and intranasal safety (pilot M3–M9; GLP M9–M15)


| Item | Detail |
|--------------------|----------------------------------------------------------------------------------------------------|
| **Must establish** | That intranasal Mn²⁺ does not accumulate in, or injure, the olfactory bulb or brain, that local airway tolerance is acceptable, and a NOAEL with margin. Why: intranasal Mn²⁺ can travel along olfactory neurons to the brain, and intranasal vaccine adjuvants have a history of facial-nerve safety signals (both external context). Our only CNS data point is S10-A: no Ifnb1/Tnf/Isg15 rise at 36 h vs PBS (Tukey p=0.87/0.54/0.96) while cholera toxin rose (p≤0.0002) [A8]. Manganese itself was never measured. |
| **Population** | Young and aged mice, both sexes; a second species (rat) for GLP repeat-dose; ferret or rabbit for nasal local tolerance. |
| **Arms / comparators** | Vehicle; PSLN-212; PSLN-344 at 1×, 3× and 10× the efficacious dose; Mn-salt equivalent (positive Mn control); cholera toxin (positive CNS control, as in S10-A). |
| **Endpoints** | Mn by ICP-MS in olfactory bulb, striatum, cerebellum and blood; MEMRI (T1); olfactory (buried-food) and motor (rotarod/open-field) tests; CNS Ifnb1/Tnf/Isg15 and microglial activation; nasal and lung histopathology; BAL cytokines at 16 h, 72 h and 7 d (S09-A watch item); serum IL-6/TNF/IFN-α; repeat-dose (n+1) GLP toxicology with recovery. |
| **Readouts & timing** | Tissue Mn and CNS markers at 36 h, 1, 7 and 28 d; pilot report M9; GLP report M15. |
| **Sample size** | Pilot n=6/sex/arm/timepoint; GLP per guideline. |
| **Go / no-go** | Go: no brain Mn above vehicle beyond 7 d at ≤3× dose; no neurobehavioural change; no persistent nasal or lung pathology at 28 d; NOAEL ≥10× the planned human dose. No-go: dose-related brain Mn accumulation with neurobehavioural or histological change. |


### Gate 3B: CMC, stability and delivery (M0–M12)


| Item | Detail |
|--------------------|----------------------------------------------------------------------------------------------------|
| **Must establish** | That the product can be made to specification, stored, and delivered to the airway tissue the mechanism needs. |
| **Population** | Product lots; a large-animal deposition model (ferret or NHP); nasal vs small-airway air–liquid-interface (ALI) cultures from donors ≥65 years. |
| **Arms / comparators** | Nasal spray vs inhaled aerosol; PSLN-344 vs PSLN-212 (PD in ALI). |
| **Endpoints** | Specifications: particle size/PDI, zeta potential, CDN-1807 encapsulation (current 54.8% ± 5.1 [S08-B]), Mn content and Mn:CDN ratio, endotoxin, sterility. No size, zeta or stability data are in the dataset although the methods are described. Stability: lyophilised (2.5% trehalose) at −20 °C and 2–8 °C. Delivery (critical): the mouse mechanism depends on **alveolar** targets (AECII and alveolar macrophages) [S01-B/C], but a human nasal spray deposits mostly in the upper airway (external context). So measure regional deposition of labelled liposomes, and PD (IFNB1, CCL2, CSF2) in nasal vs small-airway ALI. |
| **Readouts & timing** | Release specifications M3; stability at 0, 3, 6 and 12 months (6-month read at ≈M8); deposition and ALI PD by M9; device decision M12. |
| **Sample size** | 3 lots for stability; deposition n=4–6 animals per device. |
| **Go / no-go** | Go: a device/formulation achieves target-tissue exposure and a young-equivalent PD response in the large-animal/ALI models, and the lyophilised product is stable for ≥6 months. |


### Gate 3C: correlates of protection (embedded in 1A, 2A, 2B)


| Item | Detail |
|--------------------|----------------------------------------------------------------------------------------------------|
| **Must establish** | Which per-animal markers predict protection, to set Phase 1 biomarker thresholds (today, biomarkers and outcomes come from different animals). |
| **Population** | Every challenged animal in 1A, 2A and 2B. |
| **Arms / comparators** | All arms pooled; protected vs unprotected animals. |
| **Endpoints** | Pre-challenge HAI, MN, nasal IgA, 24 h blood ISG, T-cell ELISpot; outcomes are survival and lung viral load. |
| **Readouts & timing** | Interim with 1A at M7; final with 2B at M15. |
| **Sample size** | Accrues across studies (≥150 challenged animals). |
| **Go / no-go** | Deliverable rather than gate: cross-validated thresholds (logistic and Cox models) for the Phase 1 PD and immunogenicity endpoints. |


### Phase 1/2a outline (after IND; about M18–24 onward)


| Item | Detail |
|--------------------|----------------------------------------------------------------------------------------------------|
| **Must establish** | Safety of intranasal Mn-containing adjuvant in older adults; a young-equivalent PD response; HAI non-inferior to a licensed enhanced vaccine with a mucosal IgA advantage. |
| **Population** | Sentinel cohort of healthy adults 18–49, then adults 65–85 stratified 65–74 / 75–85. Exclude significant chronic lung disease, prior Bell's palsy or anosmia, neurodegenerative disease, and hepatic impairment (Mn clearance) initially. |
| **Arms / comparators** | IN inactivated vaccine + PSLN-344 at 3 dose levels (fixed Mn:CDN ratio); IN vaccine alone; licensed IM enhanced vaccine for older adults (high-dose or adjuvanted) as active comparator. |
| **Endpoints** | Safety: solicited nasal and systemic reactions d0–7, unsolicited events to d28, AESIs (Bell's palsy, olfactory change) to d180, blood Mn. PD: blood ISG score d1; nasal IFN/CXCL10/CCL2 d1. Immunogenicity: HAI GMT and seroconversion d28; nasal IgA; cTfh and plasmablasts d7; IFN-γ ELISpot d28/d180. |
| **Readouts & timing** | Safety and PD by d7; immunogenicity d28; durability d180; about 12–15 months from first subject in. |
| **Sample size** | To be set from the Gate 2 variance and margin (indicatively 30–50 per arm per age stratum for HAI precision). |
| **Go / no-go** | Go to Phase 2b: acceptable safety; older-adult PD at least equal to the young-adult response; HAI non-inferior to the IM comparator under standard seasonal-influenza criteria (to be confirmed with Regulatory) with a mucosal IgA advantage. |


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


# 7. Target demographic (for the market-research TAM check)


The data define a clear boundary. **PSLN-344 adds value only where immunity is aged.** Young mice are fully protected by PSLN-212, PSLN-344 and CMP-204 alike [S09-B/D/F, S13-E]. Aged mice are protected only by PSLN-344 [Table 1]. The demographic should therefore be anchored on immunosenescence, not on general-population influenza vaccination.


**Table 7. Target demographic and segments**


| Segment | Definition for sizing | What our data support | Status |
|-----------------|----------------------------------------|----------------------------------------------|------------------|
| **Primary** | Adults ≥65 years eligible for annual seasonal influenza vaccination; positioned against IM enhanced vaccines (high-dose, adjuvanted, recombinant; external context) as a needle-free, mucosal, broader-protection option | 20-month mice: 83% vs 12% survival; heterosubtypic 76% vs 10% [A5]. External context, to be verified: 18–24-month mice are conventionally classed as “old” (≈ late 50s–60s in human years) | Core |
| Priority sub-segment | Adults ≥75, frail adults and long-term-care residents (highest disease burden and weakest vaccine responses; external context) | The aged-mouse phenotype (blunted IFN-β, DC, Tfh) is the mechanistic target; durability is the open risk | Core, likely first label |
| Adjacent (hypothesis) | Adults 50–64 | At 14 months (middle-aged), PSLN-212 already fails (0/14 naive) while PSLN-344 protects (12/14) [S06-E/F imprint]. Needs clinical proof | TAM upside, not base case |
| Pandemic preparedness | Government H5N1 (and other pandemic) stockpile procurement, adults including the elderly | Wild-type H5N1 10/10 vs 3/10 [S03-J]; heterosubtypic H5 protection from a seasonal vaccine 7/7 vs 2/7 [S06-C] | Option value; separate buyer |
| Excluded for now | Children and adults <50; immunocompromised people or those on type I IFN/JAK-pathway blockade; severe chronic lung disease | No differentiation in young mice; the mechanism is IFNAR-dependent [S02-H]; lung-targeted STING agonism has not been safety-tested in diseased lungs | Not in TAM |


**Inputs the market-research team will need (not in our dataset):** population by age band (50–64, 65–74, ≥75) and geography; seasonal influenza vaccination coverage by age; current share and price of enhanced vaccines for older adults; acceptance of needle-free/intranasal delivery in older adults; prevalence of exclusion comorbidities (COPD and other chronic lung disease, immunosuppression); and pandemic stockpile procurement volumes and pricing.


# 8. If we drop PSLN-344: what we give up, and what we don't


### What we would give up


1. **The only formulation in our data that reliably protects aged animals:** 83% vs 12% survival over 8 experiments, HR 0.083 [A5].
2. **A mechanistically explained “age fix”:** IFN-β restored to the young level (98% of the gap) and a median 74% of the deficit closed across 40 readouts [S01-A; A3]. This is a differentiated story for the ≥65 segment.
3. **Breadth:** heterosubtypic protection of 32/42 (76%) vs 4/42 (10%), including H5, plus wild-type H5N1 protection of 10/10 vs 3/10 [A5, S03-J]. This is pandemic-preparedness option value.
4. **Speed:** protection when challenged 2–3 days after one dose, 15/17 (88%) vs 3/17 (18%) [S03-J, S06-B; A5].
5. **Mucosal T-cell memory from a needle-free product:** lung TRM 4.0% vs 1.0%; IFN-γ+ CD8 still 3.2× higher at d60 [S05-I, S05-G].
6. **Dose-sparing within the formulation:** about 8 µg of PSLN-344 matches the IFN-β response of 40 µg PSLN-212, about 5× dose sparing [S08-A; A7]. No added biologic is needed; GM-CSF add-back would achieve something similar only with a second active [S02-G].


### What we would not give up


- **Nothing in young adults or the general population.** All adjuvants protect young mice, including the cGAMP comparator CMP-204 [S09, S13-E].
- **PSLN-212 has no standalone value in the target population**: 7/59 vs 1/59 survival vs Sham (p=0.061) [A4].
- **Downside is cappable.** Gates 0–1 are about 7 months and mostly internal; the expensive steps (GLP toxicology, CMC scale-up, device) start only after Gate 1.


**Bottom line.** Dropping now would trade a large, consistent, mechanistically coherent efficacy signal in exactly the population where current vaccines underperform, in exchange for avoiding a few months of verification work. I would not make that trade. I would stop the program without hesitation if Gate 0 fails.


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


# 9. What I considered and ruled out


**Table 8. Alternatives considered**


| Option considered | Evidence | Verdict |
|--------------------------|-------------------------------------------------------------------|--------------------------|
| Take PSLN-212 forward (or both assets) | Aged: survival 7/59 vs Sham 1/59 (p=0.061); HAI GMT 46 vs 368 for PSLN-344 [A4, S03-C]. PSLN-344 is equal or better on every readout, with similar reactogenicity (nadir 97.0% vs 96.4%) [S08-D] | Ruled out: no scenario favours PSLN-212 |
| Dose up PSLN-212 instead of adding Mn²⁺ | PSLN-212 IFN-β plateaus at ≈15× (40 µg), below PSLN-344 at 10 µg (21×); fitted tops 16× vs 52× [S08-A; A7] | Ruled out: ceiling, not potency |
| Add the TLR7/8 agonist R848 | PSLN-212/R848: IFN-β 24× (n.s. vs PSLN-344 37×) but Tnf ×5.0 and Il10 ×24.5 vs PSLN-344; weight nadir 90.0% (p<0.001) with one animal unaccounted for [S01-A, S09-A, S08-D; A12]. PSLN-344/R848 lowers IFN-β about 30–36% vs PSLN-344 at 10–20 µg (p=0.018, 0.029) [S08-A] | Ruled out: less potent, more reactogenic |
| Use cGAMP (CMP-204) instead of CDN-1807 | Same vehicle: IFN-β 7.7× vs 16.5× (PSLN-212) and 36.9× (PSLN-344) [S01-A]; post-boost IgG 940 vs 4,411 (PSLN-212) [S13-I]; aged survival 3/7 vs 7/7 (PSLN-344) [S03-I] | Ruled out as the active (Mn + cGAMP is still tested in Gate 1A) |
| PSLN-344 alone as antigen-free innate prophylaxis | S15-H: PSLN-344 without vaccine 0/7, vaccine alone 0/7 (block compromised, DI-02) | Ruled out; no claim of antigen-independent protection |
| Young-adult / general-population indication | Young mice: PSLN-212(Y), PSLN-344(Y) and CMP-204(Y) all 100% [S09-B/D/F, S13-E] | Ruled out: no differentiation |
| Co-administer GM-CSF (biologic) as the age fix | Works mechanistically: moDC-like cells 5.9% → 13.8% [S02-G]; but adds a second active and biologic CMC | Ruled out as a product; kept as a research tool |
| Any CCR2-modulating combination | CCR2 blockade removes monocytes (9.9% → 3.3%) and GZMB+ CD8 (6.8% → 1.4%) [S07-B, S02-I] | Ruled out; flag CCR2 antagonists as a co-medication risk |
| Go straight to IND-enabling work | Integrity defects; no attribution, benchmark or Mn-safety data; female-only | Ruled out: gate first |
| Terminate the program now | Large, consistent efficacy signal in the target population; verification is cheap relative to the upside | Ruled out unless Gate 0 fails |
| Claims resting on compromised blocks | S06-D duplicate; S15-H/I and S15-L–O copied weights; S03-B/F rotated labels; S11-A/B shared replicates; S08-C vs S01-B conflict | Excluded from the case (Section 3) |


# 10. Key risks and open questions


**Table 9. Risk register**


| Risk | Current evidence | Mitigation / gate |
|--------------------------------|----------------------------------------------------|------------------------------------|
| Data integrity | 7 critical and 16 other issues (Appendix B) | Gate 0 hard stop |
| CDN-1807 not needed (Mn does the work), so IP is weaker | No Mn-only arm; CDN-1807 beats cGAMP in the same vehicle (IFN-β ×2.15) [S01-A] | Gate 1A arms 4–5; FTO review |
| Intranasal Mn²⁺ neurotoxicity | No CNS inflammation at 36 h [S10-A]; Mn never measured | Gate 3A |
| Mouse alveolar targeting does not translate to human nasal delivery | Mechanism relies on AECII and alveolar macrophages [S01-B/C] | Gate 3B deposition + ALI PD |
| Not differentiated vs IM enhanced vaccines | No head-to-head data | Gate 2A |
| Durability in the elderly | Day-60 survival 67% vs young 100% (p=0.009); antibody not followed past d28 in aged | Gate 2B (boost arm) |
| Prolonged lung inflammation in aged recipients | Ifnb1 4.2× at 72 h vs 1.5× young [S01-A]; Tnf 40× vs 14× at 16 h [S09-A]; Il6 7.2×, Tnf 8.4× at ≈72 h (n=3; DI-08) | Gate 3A BAL time course; Phase 1 stopping rules |
| Sex, strain and platform generality | Female BALB/c only in clean data; whole inactivated virus only | Gate 1A both sexes + C57BL/6; test split/recombinant HA in 2A |
| Background mortality in aged colonies confounds survival endpoints | Untreated aged deaths 4/21 in 14 days [S06-E/G d60] | Background arm in every aged challenge; viral-load endpoint |


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


# Appendix A. Methods and analysis index


- **Data handling [A1].** All 15 sheets were parsed cell by cell into tidy tables that keep the source cell address (code/01_extract.py). Observation counts were compared with the annotation’s stated n. Integrity scans looked for identical vectors, whole-block duplicates, and per-animal weight trajectories shared across experiments, with dead-animal LOCF tails stripped. The chance per-day match rate between animals of different experiments was 0.88%, so ≥5 identical days cannot be coincidence. Derived blocks were recomputed from their sources (S03-B/F from S13-A–D; S04-B Tfh:Tfr from Foxp3; S09-A from S01-A).
- **Continuous endpoints [A2].** Stated methods: one-way ANOVA with Tukey HSD across all groups in a block (log₁₀ scale for titres and qPCR fold-changes, linear for %). Also Welch t and exact Mann–Whitney for key pairs. Effects are geometric-mean ratios or mean differences with Welch 95% CIs, plus Hedges’ g. HAI values below the 1:10 LOD were imputed at 5. Time courses used two-way ANOVA (group × time) [A12]. Multiplicity across the 40 curated readouts was handled with Holm correction (table multiplicity_holm).
- **Age-gap closure [A3].** (PSLN-344 − PSLN-212)/(PSLN-212(Y) − PSLN-212) on the analysis scale, with a percentile bootstrap (5,000 resamples) 95% CI. The curated set has 40 readouts, one pre-specified or peak timepoint each, excluding derived ratios and flagged blocks.
- **Survival [A4, A5].** Kaplan–Meier, pairwise log-rank (stated method), and Fisher exact on final status. Pooled analyses: Cox proportional hazards stratified by experiment (Efron ties; Breslow ties give HR 0.099, 95% CI 0.050–0.199, cross-checked in statsmodels from raw cells, code/16), plus the Mantel–Haenszel risk difference (Sato variance) and odds ratio. S06-D was excluded as a duplicate; one S03-J record without a day value was censored at day 21. Sensitivity sets are listed in the workbook.
- **Mechanistic interventions [A6]:** Student’s t (stated) with Mann–Whitney as sensitivity. **Dose–response [A7]:** 4-parameter Hill fits to S08-A with a within-dose bootstrap. **Safety [A8]:** S10-A reported as mean ± SD per the annotation, with ANOVA + Tukey; S08-D per-animal weight nadir with ANOVA + Tukey vs vaccine. **Weights vs survival [A9]:** deaths inferred from truncated or LOCF trajectories and reconciled with the survival blocks. **Biomarker screen [A10]:** regimen-level AUC and separation. **Sample sizes [A11]:** t-test power on observed log₂ SDs; simulated Fisher power for survival.
- **Software:** Python 3.11 (pandas, scipy, statsmodels, lifelines, matplotlib). All code is in /code, and all tables are in PSLN_analysis_workbook.xlsx.


# Appendix B. Full data-integrity log [A1]


| ID | Severity | Blocks | Finding | Handling |
|-------|---------|----------------|--------------------------------------------------------|--------------------------------|
| DI-01 | Critical | S06-C, S06-D | S06-D (rgH5N1 challenge on day 3) is cell-for-cell identical to S06-C (challenge on day 14) across all 4 groups x 7 animals. Moreover, the S15-D weights for the S06-D animals show 2 PSLN-344 and 2 young deaths that S06-D does not record. | S06-D excluded; the day-3 rgH5N1 claim has no independent data. |
| DI-02 | Critical | S15-H, S15-I vs S15-C | Body weights of the '3d Vaccine+PSLN-344' group (S15-I) reproduce the PSLN-344 group of S15-C, a different experiment: 6 of 7 animals are identical on every day from d2 to d12 (the 7th on 4 of 7 days). Values differ only at d14, where an animal that recovers in S15-C (77.9% -> 90.1%) is carried forward as dead in S15-I. | S15-H/S15-I excluded from primary evidence; reported as sensitivity only. |
| DI-03 | Critical | S15-L/M, S15-N/O vs S09-E, S15-A | C57BL/6 block S15-M: young-reference (PSLN-212(Y)) weights reproduce BALB/c S09-E PSLN-344(Y) animals (6 animals, 4-7 identical days); aged PSLN-344 shares 2 animals (5/7 days) with BALB/c S15-A. S15-O (Swiss Webster) PSLN-344 shares partial trajectories (3 or more days) with S15-M and S15-A. | Cross-strain survival (S15-L, S15-N) moved to sensitivity analysis; strain generality must be re-established. |
| DI-04 | Critical | S03-B, S03-F vs S13-A..D | Printed IgG2a/IgG1 ratios carry rotated group labels: S03-B 'PSLN-212' = S13 PSLN-212(Y), 'PSLN-344' = S13 PSLN-212, 'PSLN-212(Y)' = S13 PSLN-344 (identical to 4 d.p.). Taken as printed, PSLN-344 would look Th2-skewed; the source titres show the opposite. | Use S13-derived ratios only; S03-B/S03-F as printed are not used. |
| DI-05 | Critical | S13-F vs S03-I; S13-G vs S03-J | Body-weight blocks do not match the survival blocks they describe. S13-F lists 'Naive' (not in S03-I) and omits CMP-204; its 'PSLN-212' arm has 3 animals recovering to 95-99% at d14 although S03-I records all 7 PSLN-212 animals dead by d6. S13-G lists 'Naive' (not in S03-J) and omits PSLN-212; its 'Sham' arm has 4 recovering animals although S03-J records 9/10 Sham deaths. | PSLN-344 arms are concordant (all survive in both). PSLN-212 arm of S03-I treated as uncertain; sensitivity analysis run without it. |
| DI-06 | Critical | S11-A, S11-B | Alveolar macrophage (S11-A) and neutrophil (S11-B) blocks share the first 1-2 of 5 replicate values in every group at every timepoint - biologically implausible for two different cell types. | Both blocks excluded. |
| DI-07 | Critical | S06-E(d60), S06-G(d60), S15-E, S15-G | 'Untreated' 20-month animals (no vaccine, adjuvant or virus) died: 1/7 (S06-E) and 3/7 (S06-G) within 14 days; matching weight records are carried forward (LOCF) after death without infection-like weight loss. | Background non-infectious mortality (4/21 = 19% over 14 d) is reported alongside every day-60 aged result; PSLN-344 deaths in S06-G (3/7) are indistinguishable from background. |
| DI-08 | Moderate | S09-A | S09-A Ifnb1 values are log10 of S01-A per-animal values (3 of 5 animals per group, /diff/<0.002). Panel 2 (cols Y-AS), printed '16h', reproduces the S01-A 72h data. S09-A 'PBS' = S01-A 'Sham'. | S09-A Ifnb1 not counted as replication; panel 2 treated as 72 h; other S09-A cytokines used descriptively. |
| DI-09 | Moderate | S01-B, S08-C | Same formulation (PSLN-SRB) gives AECI uptake of 3.8% in S01-B but 13.8% in S08-C; S08-C shares values with S01-B (17.7, 17.5, 12.2; and 4.92, 4.13 reappear under a different label). | Epithelial-uptake claims (incl. PSLN-344 vs PSLN uptake) treated as unresolved. |
| DI-10 | Moderate | S07-C | Both transferred-macrophage groups are labelled 'Ly6C-CD206+ MPhi'; one should be Ly6C+CD206-. | Excluded (direction of effect cannot be assigned). |
| DI-11 | Moderate | S04-B Tfh:Tfr | Printed Tfh:Tfr equals (100 - Foxp3%)/Foxp3% from the adjacent Foxp3 block to 4 d.p.; it is a transform of Tfr%, not an independent Tfh measurement. | Not counted as independent evidence; Tfh taken from S04-A. |
| DI-12 | Moderate | S05-A, S05-B | NP366-374 is an H-2Db epitope (C57BL/6); the annotation's default strain is BALB/c (H-2d). n=2 observed vs 3 stated; conditions describe both OVA and bivalent-vaccine immunisation. | Excluded. |
| DI-13 | Moderate | S03-J | Stated n=9 but 10 records per group; one PSLN-344 record (S03!J46) has no day value. Animal age is not stated (aged only by the annotation's default convention). | Record kept as censored at end of follow-up (21 d); pooled sensitivity analysis run without S03-J. |
| DI-14 | Moderate | S09-B, S09-F, S09-G | Annotation says S09-B Sham has 7 records and S09-F Sham 8; the workbook has 8 and 7. S09-G weighs 8 Sham animals whereas S09-F has 7 survival records. | Analysed as recorded; young-mouse results are at ceiling so conclusions unaffected. |
| DI-15 | Moderate | S13-E | Stated n=5, 7 records per group; annotation says 'vaccinated as in S03-I' but groups differ (Naive, Sham, CMP-204(Y), PSLN-344(Y)). | Analysed as recorded. |
| DI-16 | Minor | S09-C, S09-E/G, S15-C | S09-C day-12 weights for PSLN-344(Y) identical to PSLN-212(Y) (8 animals); S09-G PSLN-212(Y) #8 identical to S09-E #8 (7/7 days); S15-C PSLN-212(Y) #6 shares 5 days with S09-E. | Young-mouse weight curves not used for inference. |
| DI-17 | Minor | Body-weight blocks (S13, S15) | Dead animals are sometimes carried forward at their last weight (LOCF) and sometimes left blank, even within one block. | Weights summarised for survivors only; mortality taken from survival blocks. |
| DI-18 | Minor | S03-C, S03-G | Three HAI values recorded as 0 although the lowest dilution tested was 1:10. | Imputed as 5 (LOD/2) for GMT; affects Sham only. |
| DI-19 | Minor | S08-A, S08-B, S08 rows 89-101 | 'PSLN-344/R848' (S08-A) is not defined in Materials; S08-B reports CDN-1807 encapsulation for PSLN-R848, which contains no CDN-1807; rows 89-101 hold unlabelled data (day 14, event 0) with no group names. | PSLN-344/R848 reported descriptively; orphan rows excluded. |
| DI-20 | Minor | S07-B, S11-E, S13-H, S14-A | Timepoint not stated. | Used descriptively; timing flagged. |
| DI-21 | Minor | S08-D | One PSLN-212/R848 animal missing at day 10 with no explanation. | Reported as unexplained loss in a reactogenicity study. |
| DI-22 | Minor | S06 sheet labels | Labels 'S06-E' and 'S06-F' are each used for two different experiments (day-60 challenge; imprinting). | Disambiguated as S06-E(d60)/S06-E(imprint) etc. |
| DI-23 | Minor | S02-C, S02-E | The 'PTX' group's adjuvant, vaccine and age are not stated; the annotation describes only the pertussis-toxin dosing. | Comparisons with the PTX arm treated as directional only; S05-C (conditions stated) is the primary evidence for Gai-dependent migration. |


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


# Appendix C. Figures


![Fig 1. Survival by experiment and pooled [A4, A5].](figures/fig1_survival_overview.png){width=100%}


![Fig 2. Kaplan–Meier curves for representative aged-mouse experiments [A4].](figures/fig2_km_panels.png){width=100%}


![Fig 3. Age-gap closure across 40 readouts [A3].](figures/fig3_age_gap_closure.png){width=82%}


![Fig 4. Immunogenicity in aged mice; Sham HAI values below LOD plotted at 5 [A2].](figures/fig4_immunogenicity.png){width=100%}


![Fig 5. S08-A dose–response with Hill fits [A7].](figures/fig5_dose_response.png){width=62%}


![Fig 7. CNS transcripts (S10-A) and post-vaccination weight (S08-D) [A8].](figures/fig7_safety.png){width=100%}


![Fig 8. Visual exhibits for DI-01, DI-02, DI-04 and DI-06 [A1].](figures/fig8_integrity_exhibits.png){width=100%}


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


# Appendix D. Supporting tables


**Table D1. Mechanistic interventions [A6] (groups a and b as named in the question; MW = exact Mann–Whitney)**


| Block | Question | Mean a vs b | Ratio | Student t p | MW p |
|-----------|------------------------------------------------------------|-----------------|--------|------------|------------|
| S01-B | PSLN tropism: type II vs type I alveolar epithelium | 15.8 vs 3.83 | 4.12 | <0.0001 | 0.008 |
| S01-B | Liposome vs free dye uptake by AECII | 15.8 vs 0.38 | 41.80 | <0.0001 | 0.008 |
| S01-C | Alveolar-macrophage uptake depends on SP-A/SP-D | 43.1 vs 12.7 | 3.41 | <0.0001 | 0.029 |
| S11-C | Gap-junction blockade (carbenoxolone) reduces monocyte recruitment | 7.28 vs 3.08 | 2.36 | 0.003 | 0.008 |
| S12-A | Monocyte infiltration with IFNAR-/- bone marrow | 21.3 vs 15.4 | 1.38 | 0.10 | 0.20 |
| S02-H | moDC generation requires IFNAR (cDC-depleted BM) | 19.7 vs 2.09 | 9.43 | <0.0001 | 0.008 |
| S02-H | moDC generation requires IFNAR (cDC-replete BM) | 27.2 vs 6.07 | 4.48 | 0.0002 | 0.008 |
| S02-H | GM-CSF partially rescues IFNAR-/- moDC | 12.4 vs 2.09 | 5.94 | 0.0003 | 0.008 |
| S02-H | GM-CSF rescue vs WT | 19.7 vs 12.4 | 1.59 | 0.018 | 0.056 |
| S02-G | Adding GM-CSF to PSLN-212 (no Mn) raises moDC-like cells | 13.8 vs 5.86 | 2.36 | 0.0008 | 0.008 |
| S02-G | PSLN-212 vs GM-CSF alone | 5.86 vs 1.52 | 3.85 | 0.0002 | 0.008 |
| S02-I | CCR2 blockade abolishes lung GZMB+ CD8 (young) | 6.77 vs 1.39 | 4.87 | <0.0001 | 0.008 |
| S07-B | CCR2 blockade reduces monocytes (aged) | 9.86 vs 3.26 | 3.03 | 0.0005 | 0.008 |
| S07-B | CCR2 blockade reduces Ly6C+ macrophages (aged) | 15.4 vs 2.52 | 6.09 | 0.0002 | 0.008 |
| S05-C | Pertussis toxin blocks OT-I priming in MLN | 30.9 vs 6.83 | 4.52 | 0.0005 | 0.10 |
| S05-C | Pertussis toxin does not block OT-I proliferation in lung | 59.0 vs 55.1 | 1.07 | 0.56 | 1.00 |
| S02-C | Antigen+ DC in MLN: PSLN-344 vs PTX arm | 7.09 vs 2.36 | 3.01 | 0.0002 | 0.008 |
| S02-E | OT-I priming by MLN DC: PSLN-344 vs PTX arm | 18.7 vs 2.55 | 7.32 | <0.0001 | 0.008 |
| S08-C | Epithelial uptake PSLN vs PSLN-344 (AECII) [DI-09] | 15.8 vs 3.81 | 4.14 | <0.0001 | 0.008 |
| S08-C | Epithelial uptake PSLN vs PSLN-344 (AECI) [DI-09] | 13.8 vs 3.00 | 4.59 | <0.0001 | 0.008 |


**Table D2. S10-A CNS inflammation [A8]**


| CNS transcript (36 h) | Group | Mean ± SD (fold) | Tukey p vs PBS |
|------------------------------------|------------------------|------------------------------------|------------------------|
| CNS Ifnb1 | PBS | 1.00 ± 0.23 | n/a |
| CNS Ifnb1 | Sham | 1.17 ± 0.34 | 0.98 |
| CNS Ifnb1 | PSLN-344 | 1.32 ± 0.41 | 0.87 |
| CNS Ifnb1 | CT | 5.50 ± 1.19 | <0.0001 |
| CNS Tnf | PBS | 1.00 ± 0.22 | n/a |
| CNS Tnf | Sham | 1.32 ± 0.39 | 0.88 |
| CNS Tnf | PSLN-344 | 1.59 ± 0.49 | 0.54 |
| CNS Tnf | CT | 3.50 ± 1.22 | 0.0002 |
| CNS Isg15 | PBS | 1.00 ± 0.34 | n/a |
| CNS Isg15 | Sham | 1.04 ± 0.17 | 1.00 |
| CNS Isg15 | PSLN-344 | 1.13 ± 0.21 | 0.96 |
| CNS Isg15 | CT | 2.68 ± 0.74 | 0.0001 |


**Table D3. S08-A lung Ifnb1 dose–response [A7]**


| Formulation | Fitted top (fold) | Emax (95% CI) | ED50 µg (95% CI) | Mean 10 µg | Mean 20 µg | Mean 40 µg |
|------------------------|--------------|----------------------|----------------------|------------|------------|--------------|
| CMP-204 | 8.0 | 7.2 (6.0–11.6) | 5.9 (5.0–10.7) | 6.3 | 7.3 | 8.0 |
| PSLN-212 | 15.5 | 14.4 (11.1–22.8) | 9.5 (7.5–18.4) | 8.9 | 12.6 | 14.9 |
| PSLN-344 | 52.0 | 49.3 (40.0–61.3) | 11.5 (10.2–14.3) | 21.1 | 45.8 | 50.2 |
| PSLN-344/R848 | 37.6 | 36.2 (28.7–59.5) | 12.1 (10.1–25.1) | 14.7 | 29.4 | 34.9 |


**Table D4. S08-D reactogenicity [A8]**


| Group | n | Nadir % (mean ± SD) | Lowest | >10% loss | Present d10 | Tukey p vs vaccine |
|--------------------------|-------|----------------------|------------|--------------|--------------|------------------------|
| CMP-204 | 5 | 95.9 ± 2.0 | 93.2 | 0 | 5 | 0.70 |
| PSLN-212 | 5 | 97.0 ± 1.7 | 94.5 | 0 | 5 | 0.97 |
| PSLN-212(Y) | 5 | 97.6 ± 1.3 | 96.0 | 0 | 5 | 1.00 |
| PSLN-212/R848 | 5 | 90.0 ± 5.0 | 84.7 | 4 | 4 | 0.0003 |
| PSLN-344 | 5 | 96.4 ± 1.5 | 94.2 | 0 | 5 | 0.86 |
| Vaccine | 5 | 98.2 ± 1.1 | 97.1 | 0 | 5 | n/a |


**Table D5. Pooled survival analyses and sensitivity sets [A5]**


| Pooled analysis | PSLN-344 (or named arm) | PSLN-212 (or named arm) | Cox HR (95% CI) | MH risk diff. in death, pp |
|------------------------------------------------|-----------------|-----------------|--------------------|------------------|
| PRIMARY: all aged BALB/c experiments not compromised (8) | 49/59 (83%) | 7/59 (12%) | 0.083 (0.041–0.167) | -71 (-83 to -60) |
| Sens-1: drop S03-I (DI-05) | 42/52 (81%) | 7/52 (13%) | 0.097 (0.048–0.197) | -67 (-80 to -54) |
| Sens-2: drop S03-J (age not stated; DI-13) | 39/49 (80%) | 4/49 (8%) | 0.092 (0.045–0.187) | -71 (-84 to -59) |
| Challenge 14 d post-vaccination (3) | 20/21 (95%) | 3/21 (14%) | 0.028 (0.004–0.217) | -81 (-97 to -64) |
| Challenge 2-3 d post-vaccination (2) | 15/17 (88%) | 3/17 (18%) | 0.055 (0.012–0.257) | -71 (-92 to -49) |
| Challenge 60 d post-vaccination (3) | 14/21 (67%) | 1/21 (5%) | 0.143 (0.059–0.349) | -62 (-84 to -40) |
| Heterosubtypic challenges only (6) | 32/42 (76%) | 4/42 (10%) | 0.110 (0.053–0.227) | -67 (-81 to -52) |
| Sens-3: add duplicate S06-D (should NOT be used) | 56/66 (85%) | 9/66 (14%) | 0.077 (0.039–0.155) | -71 (-82 to -60) |
| Sens-4: add compromised cross-strain blocks S15-L, S15-N | 61/73 (84%) | 9/73 (12%) | 0.084 (0.045–0.159) | -71 (-82 to -61) |
| Middle-aged (14 mo) naive animals | 12/14 (86%) | 0/14 (0%) | 0.057 (0.012–0.266) | -86 (-104 to -67) |
| Middle-aged (14 mo) imprinted animals | 12/14 (86%) | 4/14 (29%) | 0.051 (0.006–0.417) | -57 (-83 to -31) |


_Sens-3 deliberately adds the duplicate S06-D to show that it would inflate apparent evidence without changing the estimate; it is not used. The middle-aged rows compare the named Naive/Imprinting arms._


# Appendix E. Files delivered


- PSLN_portfolio_proposal.pdf: this document.
- PSLN_portfolio_proposal.docx and .md: editable versions with the same content.
- PSLN_analysis_workbook.xlsx: every statistic with source block and cell range (evidence register, integrity log, all analysis tables).
- figures/: Figs 1–8 (PNG).
- code/: the analysis pipeline (01_extract → 14_content), reproducible end to end from the two source files.
