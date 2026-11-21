---
title: "PSLN intranasal STING-agonist adjuvant: portfolio review proposal"
subtitle: "Recommendation, evidence, mechanism, biomarkers, target population and gated next steps"
date: "1 November 2026"
---

**Data basis.** `psln_program_dataset.xlsx` (15 sheets; file metadata: last modified 2026-09-03) and `psln_program_annotation.pdf`. Every block was extracted with cell-level provenance and re-analysed. Each number in this document traces to a block ID (e.g. S03-C) and an analysis output (e.g. `h2h.csv`). The full trail is in the evidence ledger (`analysis/evidence_ledger.csv`, 353 entries). Every table and figure can be regenerated with `code/run_all.sh`.

**Terminology.** *PSLN-344* = CDN-1807 in the surfactant-biomimetic liposome **with** Mn2+. *PSLN-212* = the same drug and vehicle **without** Mn2+. "Aged" = 20-month-old female BALB/c mice unless stated. "Young" = 7–8 weeks. *RI* (restoration index) = (PSLN-344 − aged PSLN-212) / (young PSLN-212 − aged PSLN-212): the fraction of the age-related deficit that Mn2+ closes (0 = none, 1 = young level). *pp* = percentage points.

# 1. Recommendation

> **KEEP the program. Advance PSLN-344 as the single lead. Stop developing PSLN-212 (keep it only as the Mn-free control in studies).**
>
> **Make this a gated keep, not an IND commitment.** Fund only what is needed to pass Gate A (data-integrity verification, end of January 2027) and Gate B (blinded confirmatory efficacy and Mn2+/CNS safety, October 2027). The kill criteria are fixed in advance (Section 7.3).

**How the asset looks, in one paragraph.** Scientifically, PSLN-344 has a large, consistent signal with a mechanistic explanation. In aged mice it is the only formulation we have tested that protects: pooled survival after lethal influenza challenge was 61/73 (84%) vs 9/73 (12%) for PSLN-212 and 1/73 (1%) for sham-adjuvanted vaccine (young mice with PSLN-212: 62/63 (98%)). As a data package, however, it is **not yet investment-grade**. I found 4 critical and 8 major data-integrity problems that the committee would find if it checked (Section 3). None of them reverses the conclusion, but the exact magnitudes cannot be relied on until the source data are verified and the key experiment is repeated blind.

**Why keep (the evidence):**

1. **Survival, head-to-head.** Across all 14 aged or middle-aged strata, 85/101 PSLN-344 vs 13/101 PSLN-212 animals survived. The difference is 71 pp (95% CI 60-79); stratified hazard ratio 0.076 (0.043-0.134). The point estimate favours PSLN-344 in 14/14 strata. In the worst-case reconstruction of the record the difference is still 63 pp (51-72) (Table 3).
2. **Breadth of the signal.** Of 76 independent immune endpoints with both aged arms, 59 differ at FDR<5% (55/59 with no overlap between individual animals). Every one of them that has a young benchmark moved toward the young level (47/47); none moved away (Appendix B).
3. **Antibody titres close to young levels.** HAI GMT against CA09 H1N1 was 368 vs 46 (young: 485; RI 0.88). Against Aichi H3N2 it was 320 vs 35 (young: 368; RI 0.94) (S03-C/G).
4. **Protection where older adults need it most.** PSLN-344 protected against heterosubtypic challenge (H3 vaccine → H1 virus), H5N1 (wild-type VN04 two days after one dose: 10/10 vs 3/10; S03-J does not state age, so it counts as aged under the annotation's convention), rapid-onset challenge (days 2–3: 15/17 vs 3/17) and challenge at day 60 (14/21 vs 1/21).
5. **A coherent, partly causal mechanism.** Mn2+ raises IFN-β and GM-CSF in the aged lung. This drives CCR2-dependent monocyte recruitment and IFNAR/GM-CSF-dependent monocyte-derived DC (moDC) differentiation, DC migration and priming, Tfh/germinal-centre responses, and CD8/resident-memory immunity. Several links are proven by loss- or gain-of-function experiments (Section 4).
6. **The benefit is age-specific.** In young mice, PSLN-212, PSLN-344 and even a cGAMP liposome all protect fully (S09-B/D/F, S13-E). The product's differentiation therefore lies in older adults, which is where the unmet need is (Section 6).

**Why only a conditional keep:**

1. **Data integrity** (Section 3). Examples: survival experiment S06-D is an exact copy of S06-C; body-weight trajectories are recycled between experiments, including the C57BL/6 and Swiss Webster "strain generality" studies; several survival records contradict their own body-weight records; and 4/21 (19%; 95% CI 5-42%) of unvaccinated, *unchallenged* aged controls died within 14 days.
2. **Mn2+ intranasal safety is essentially untested.** The only data point is one 36-h CNS cytokine readout, which showed no signal (S10-A). We have no Mn dose per vial, no biodistribution and no olfactory-bulb exposure data. External literature describes olfactory transport of intranasal Mn to the brain.
3. **Rejuvenation is partial in the compartments that govern durability.** DC co-stimulation RI is 0.19, CD8 memory RI 0.62 and post-boost antibody RI 0.62. In matched designs, PSLN-344 survival was 13/14 vs 10/14 (Fisher p=0.33) when challenge moved from day 14 to day 60.
4. **Missing commercially decisive evidence.** There is no comparator representing today's standard of care for older adults, no lung viral load, no mucosal IgA, female mice only, and no ferret or non-human-primate data.

**Decision asked of the committee today:**

- **Approve Gate A**: independent source-data verification, November 2026 – January 2027.
- **Approve the no-regret work that can start now**: Mn and CDN-1807 content per dose, particle characterisation, stability set-down, a human STING-variant potency screen, and a freedom-to-operate review of Mn2+–cyclic-dinucleotide formulations.
- **Approve immediate ordering of 20–22-month-old animals.** Aged-animal supply is the critical path for Gate B.
- **Pre-approve the Gate B package (Section 7), contingent on Gate A passing.**

# 2. How the two assets compare

**Table 1. Aged-mouse head-to-head on the decision-relevant endpoints.** Titres and qPCR: geometric means; cells: arithmetic means; n = 5 per group unless stated. Full statistics for all endpoints are in Appendix B.

| Endpoint (aged mice unless stated) | Sham | PSLN-212 | **PSLN-344** | Young PSLN-212 | PSLN-344 vs PSLN-212 (95% CI) | FDR q | Gap closed (RI) | Source |
|---|---|---|---|---|---|---|---|---|
| Lung Ifnb1 at 16 h (fold vs untreated) | 0.9 | 16.5 | **36.9** | 37.5 | 2.2x (1.8-2.7) | <0.001 | 0.98 | S01-A |
| Lung Gm-csf at 36 h (fold) | 1.2 | 1.6 | **8.5** | - | 5.4x (3.9-7.3) | <0.001 | - | S02-F |
| Lung monocytes, day 4 (%) | 10.4 | 16.7 | **30.6** | 32.2 | +13.8 pp (+8.1 to +19.5) | 0.004 | 0.89 | S01-D |
| CCR7+ migratory CD11b+ DC, 72 h (%) | 2.5 | 7.3 | **30.7** | 35.0 | +23.4 pp (+13.8 to +33.0) | 0.004 | 0.84 | S02-A |
| Antigen+ DC in MLN, 36 h (%) | - | 1.8 | **7.1** | 9.4 | +5.3 pp (+3.6 to +7.1) | 0.002 | 0.70 | S02-C |
| OT-I CD8 priming by MLN DC (%) | - | 0.8 | **18.7** | 26.2 | +17.9 pp (+14.4 to +21.4) | <0.001 | 0.70 | S02-E |
| CD86+ of MLN CD11b+ DC, day 3 (%) | 7.2 | 8.1 | **14.5** | 37.9 | +6.4 pp (+3.0 to +9.9) | 0.006 | 0.22 | S02-D CD86 |
| ICOS-hi Tfh, day 7 (%) | 0.3 | 3.8 | **10.3** | 13.6 | +6.4 pp (+2.6 to +10.3) | 0.014 | 0.66 | S04-A |
| Tfr (Foxp3+ of CXCR5+ICOShi), day 7 (%) - lower is better | 22.6 | 26.7 | **10.8** | 7.1 | -15.9 pp (-24.0 to -7.7) | 0.008 | 0.81 | S04-B Foxp3 |
| Germinal-centre B cells, day 7 (%) | 1.2 | 2.3 | **6.5** | 9.8 | +4.2 pp (+2.3 to +6.1) | 0.005 | 0.56 | S03-K |
| Serum IgG anti-CA09 H1N1, day 14 (GMT) | 56 | 393 | **7,305** | 11,959 | 18.6x (9.1-37.9) | <0.001 | 0.86 | S03-A |
| HAI anti-CA09 H1N1, day 14 (GMT) | 8 | 46 | **368** | 485 | 8.0x (3.9-16.4) | 0.001 | 0.88 | S03-C |
| HAI anti-Aichi H3N2, day 14 (GMT) | 10 | 35 | **320** | 368 | 9.2x (4.2-20.2) | 0.001 | 0.94 | S03-G |
| Neutralising Ab anti-CA09 H1N1, day 14 (GMT) | 52 | 418 | **3,840** | 6,686 | 9.2x (3.1-27.2) | 0.004 | 0.80 | S03-D |
| IgG anti-CA09 after boost, day 28 (GMT) | 57 | 4,411 | **15,651** | 40,739 | 3.5x (1.5-8.4) | 0.016 | 0.57 | S13-I |
| IFN-g+ CD8 (rgH5N1 restim), day 14 (%) | 0.7 | 1.5 | **6.4** | 9.2 | +4.9 pp (+3.6 to +6.1) | <0.001 | 0.63 | S05-F |
| IFN-g+ CD8 (rgH5N1 restim), day 60 (%) | 1.5 | 3.0 | **9.9** | 14.4 | +6.8 pp (+3.4 to +10.3) | 0.006 | 0.60 | S05-G |
| Lung resident-memory CD8, day 25 (%) | 0.6 | 1.0 | **4.0** | 6.0 | +3.0 pp (+2.2 to +3.7) | <0.001 | 0.59 | S05-I |
| **Survival after lethal challenge, pooled aged arms (10 experiments)** | 1/73 (1%) | 9/73 (12%) | **61/73 (84%)** | 62/63 (98%) | see Table 2 | - | 0.83 | S03-I/J, S06-A-G (excl. D), S15-L/N |
| Post-vaccination weight nadir, no challenge (% of day 0) | 98.2 (vaccine only) | 97.0 | **96.4** | 97.6 | -0.6 pp (p=0.56) | - | - | S08-D |

*Notes.* Effects: geometric mean ratio (×) or mean difference (pp) with Welch 95% CI. q: Benjamini–Hochberg FDR across the 76 independent endpoints. The survival row pools the aged arms of S03-I, S03-J, S06-A/B/C/E/F/G and S15-L/N (S06-D excluded as a duplicate). PSLN-344 vs young PSLN-212 survival: -15 pp (-25 to -5) (Newcombe CI). Source tables: `h2h.csv`, `survival_pooled_arms.csv`, `reactogenicity_s08d.csv`.

![Figure 3. Effect of Mn2+ along the immune cascade (A) and fraction of the age gap closed (B).](figures/fig3_cascade_restoration.png)

**Table 1b. How much of the young–aged deficit Mn2+ closes, by layer** (`restoration_index.csv`; RI per endpoint with bootstrap CIs in the file).

| Layer of the immune response | Endpoints | Median RI | Range | Reading |
|---|---|---|---|---|
| Innate cytokine (16-36h) | 5 | 0.83 | 0.64-0.98 | Near-complete rescue |
| Myeloid recruitment & DC (d3-4) | 7 | 0.75 | 0.70-0.89 | Substantial rescue |
| DC co-stimulation (d3) | 2 | 0.19 | 0.17-0.22 | Largely NOT rescued |
| CD8 priming/effector (d3) | 3 | 0.70 | 0.41-0.91 | Substantial, but effector (GZMB) partial |
| Tfh/GC/regulation (d7) | 7 | 0.72 | 0.38-0.93 | Substantial |
| Antibody (d14) | 10 | 0.77 | 0.59-0.94 | Substantial (HAI near-young) |
| Antibody post-boost (d28) | 2 | 0.62 | 0.57-0.66 | Partial: boosted titres stay below young |
| CD8 memory (d14-60) | 6 | 0.62 | 0.59-0.75 | Partial: memory below young |

**Reading the comparison:**

- **PSLN-212 is active in aged mice but not enough to protect.** Versus sham it raises CA09 IgG about 7-fold (GMT 393 vs 56) and HAI about 6-fold (46 vs 8). Yet survival was 9/73 (12%) vs 1/73 (1%).
- **Mn2+ is what converts immunogenicity into protection in the aged host.**
- **Where Mn2+ falls short.** Restoration is near-complete for innate cytokines (median RI 0.83), myeloid recruitment (RI 0.75) and d14 antibody (RI 0.77). It is poor for DC co-stimulation: CD86 14.5% vs young 37.9%; CD40 11.2% vs 38.7% (RI 0.22/0.17). It is partial for CD8 memory and post-boost titres (RI 0.62 and 0.62). These gaps are the main efficacy risk for durability in humans and are built into the next-step endpoints.
- **Th1 skew.** PSLN-344 induces a Th1-skewed response: IgG2a/IgG1 2.14 vs 0.58 (H1) and 2.73 vs 0.51 (H3), against young 2.97/2.89. These ratios are recomputed from the primary subclass titres (S13-A–D). The printed quotient blocks S03-B/F carry rotated labels and, read as printed, would wrongly suggest a Th2 skew (integrity finding M1).
- **Reactogenicity signal to monitor.** PSLN-344 vs PSLN-212 differences in Tnf and Il10 are not significant at FDR 5%. Compared with young animals, however, aged lungs given PSLN-344 overshoot for Tnf and keep both cytokines raised at 72 h (nominal, unadjusted p-values below). At 16 h, Tnf was 40.5× vs young 13.9×. At 72 h it was 8.4× vs 0.5× (p=0.008), and Il10 4.2× vs 0.1× (p=0.002) (S09-A; the second panel is the 72-h timepoint, finding M3). Body-weight loss after vaccination was small (nadir 96.4% vs 97.0%; p=0.56; S08-D).

**Table 2. Survival by experiment (survivors/animals).**

| Block | Design | Sham | PSLN-212 | PSLN-344 | Young PSLN-212 | Log-rank p (344 vs 212) | Fisher p |
|---|---|---|---|---|---|---|---|
| S03-I | Aged BALB/c; bivalent vaccine, homologous CA09 H1N1 10x LD50 at d14 | 0/7 | 0/7 | **7/7** | 7/7 | 0.0004 | 0.0006 |
| S03-J | BALB/c (aged by convention); rgH5N1 vaccine, wild-type VN04 H5N1 at d2 | 1/10 | 3/10 | **10/10** | - | 0.0014 | 0.0031 |
| S06-A | Aged; Aichi H3N2 vaccine -> PR8 H1N1 at d14 (heterosubtypic) | 0/7 | 1/7 | **6/7** | 7/7 | 0.0083 | 0.0291 |
| S06-B | Aged; Aichi H3N2 vaccine -> PR8 H1N1 at d3 (rapid) | 0/7 | 0/7 | **5/7** | 7/7 | 0.0009 | 0.0210 |
| S06-C | Aged; bivalent -> rgH5N1 at d14 | 0/7 | 2/7 | **7/7** | 7/7 | 0.0068 | 0.0210 |
| S06-D | Aged; bivalent -> rgH5N1 at d3 - EXCLUDED (identical to S06-C) | 0/7 | 2/7 | **7/7** | 7/7 | 0.0068 | 0.0210 |
| S06-E | Aged; Aichi H3N2 vaccine -> PR8 H1N1 at d60 (durability) | 0/7 | 0/7 | **5/7** | 7/7 | 0.0016 | 0.0210 |
| S06-F | Aged; bivalent -> rgH5N1 at d60 | 0/7 | 1/7 | **5/7** | 7/7 | 0.0094 | 0.1026 |
| S06-G | Aged; CA09 H1N1 vaccine -> Perth H3N2 at d60 | 0/7 | 0/7 | **4/7** | 7/7 | 0.0151 | 0.0699 |
| S06-E[imprint] | 14-month naive; bivalent -> PR8 H1N1 | - | 0/7 | **6/7** | - | 0.0024 | 0.0047 |
| S06-E[imprint] | 14-month PR8-imprinted; bivalent -> PR8 H1N1 | - | 4/7 | **6/7** | - | 0.2321 | 0.5594 |
| S06-F[imprint] | 14-month naive; bivalent -> Perth H3N2 at d14 | - | 0/7 | **6/7** | - | 0.0006 | 0.0047 |
| S06-F[imprint] | 14-month PR8-imprinted; bivalent -> Perth H3N2 at d14 | - | 0/7 | **6/7** | - | 0.0002 | 0.0047 |
| S15-L | Aged C57BL/6 (challenge not stated; body weight recycled) | 0/7 | 0/7 | **6/7** | 6/7 | 0.0011 | 0.0047 |
| S15-N | Aged Swiss Webster (challenge not stated; body weight recycled) | 0/7 | 2/7 | **6/7** | 7/7 | 0.0563 | 0.1026 |
| S09-B | Young; Aichi H3N2 vaccine -> PR8 at d21 | 0/8 | - | young PSLN-344: **8/8** | 8/8 | - | - |
| S09-D | Young; CA09 vaccine -> Perth H3N2 at d21 | 0/8 | - | young PSLN-344: **8/8** | 8/8 | - | - |
| S09-F | Young; bivalent -> rgH5N1 at d180 | 0/7 | - | young PSLN-344: **8/8** | 8/8 | - | - |
| S13-E | Young; bivalent -> CA09 10x LD50 at d14 (CMP-204 young 7/7; naive 0/7) | 1/7 | - | young PSLN-344: **7/7** | - | - | - |
| S15-H | Aged; given 3 d before rgH5N1: vaccine alone 0/7; PSLN-344 alone 0/7; vaccine + PSLN-344 6/7 (body-weight record duplicated, C2) | - | - | - | - | - | - |

![Figure 1. Head-to-head survival by experiment and pooled, including integrity sensitivity analyses.](figures/fig1_survival_forest.png)

**Table 3. Pooled PSLN-344 vs PSLN-212 survival and sensitivity to the integrity findings.**

| Analysis set | Strata | PSLN-344 survivors | PSLN-212 survivors | Difference, pp (95% CI, Newcombe) | Stratified log-rank p | CMH p | Strata favouring PSLN-344 |
|---|---|---|---|---|---|---|---|
| A. As recorded (S06-D excluded as exact duplicate of S06-C) | 14 | 85/101 (84%) | 13/101 (13%) | 71.3 (59.8 to 79.1) | 3.5e-27 | <1e-15 | 14/14 (ties 0) |
| B. Excluding experiments whose survival record conflicts with the body-weight record | 7 | 40/49 (82%) | 6/49 (12%) | 69.4 (51.7 to 80.0) | 2.3e-14 | 2.4e-10 | 7/7 (ties 0) |
| C. Worst case for PSLN-344 (BW-implied counts where less favourable; S06-D re-entered with S15-D BW counts) | 15 | 90/108 (83%) | 22/108 (20%) | 63.0 (51.2 to 71.7) | - | <1e-15 | 15/15 (ties 0) |
| D. Aged BALB/c S06 series only (S06-A,B,C,E,F,G; challenge d3, d14 or d60) | 6 | 32/42 (76%) | 4/42 (10%) | 66.7 (47.3 to 78.5) | 6.7e-12 | 2.0e-08 | 6/6 (ties 0) |
| E. Durability only (challenge at day 60: S06-E,F,G) | 3 | 14/21 (67%) | 1/21 (5%) | 61.9 (34.1 to 78.5) | 2.4e-06 | 3.7e-04 | 3/3 (ties 0) |
| F. Rapid onset (challenge day 2-3: S03-J, S06-B) | 2 | 15/17 (88%) | 3/17 (18%) | 70.6 (38.1 to 84.8) | 4.1e-06 | 3.2e-04 | 2/2 (ties 0) |

*Leave-one-experiment-out:* the difference ranges 69-74 pp. Stratified log-rank χ² = 117 and Cox HR 0.076 (0.043-0.134) were reproduced independently in R (`strat.R`). Log-rank was not computed for set C, which uses count overrides.

![Figure 2. Kaplan–Meier curves for the main aged-mouse challenge experiments.](figures/fig2_km_grid.png)

# 3. Data integrity: what the committee must know before relying on these numbers

I audited every block against the annotation and against the other blocks. The checks were:

- stated vs observed n;
- exact and partial duplicate vectors;
- repeated high-precision values ("fingerprints");
- derived vs primary metrics;
- survival records vs body-weight records;
- biological plausibility.

The full register is Appendix A (`analysis/integrity_register.csv`).

**Critical findings:**

- **C1 – duplicated experiment.** S06-D (rgH5N1 challenge at day 3) is identical, animal for animal, to S06-C (challenge at day 14). This includes five PSLN-212 death days. S06-D's own body-weight record (S15-D) shows PSLN-344 and young animals dying that S06-D lists as survivors.
- **C2 – recycled body-weight trajectories.** The "vaccine + PSLN-344" arm of S15-I equals the PSLN-344 arm of S15-C for 40 of 42 values (days 2–12). Young BALB/c PSLN-344 animals (S09-E) reappear as young C57BL/6 PSLN-212 animals (S15-M). Aged BALB/c PSLN-344 animals (S15-A) reappear in the C57BL/6 and Swiss Webster blocks (S15-M, S15-O). In total, 39 high-precision values recur in the workbook; 33 of them are body weights shared between different experiments or arms.
- **C3 – survival records that contradict their own body weights.** S03-I lists all 7 PSLN-212 deaths by day 6, while S13-F shows three of those animals recovering to 95–99% body weight. S03-J lists 9/10 sham deaths, while S13-G shows four sham animals back to ≥99.7%. S06-E and S06-G have similar conflicts.
- **C4 – deaths in unchallenged controls.** 4/21 (19%; 95% CI 5-42%) of unvaccinated, unchallenged aged controls died within 14 days, at flat body weight. In S06-G, PSLN-344 survival (4/7) equals unchallenged-control survival (4/7).

**Major findings that would change a reader's conclusion if missed:**

- **M1.** IgG2a/IgG1 labels are rotated (S03-B/F). As printed they invert the Th1/Th2 conclusion.
- **M2.** The alveolar-macrophage and neutrophil blocks (S11-A/B) share identical values.
- **M3.** The second S09-A panel is the 72-h timepoint, not 16 h, and re-uses the S01-A animals.
- **M7.** The strain-generality experiments (S15-L/N) state no challenge virus.
- **M4–M6, M8.** An undecodable group label (S07-C), an MHC-mismatched tetramer in BALB/c (S05-A/B), inconsistent epithelial-uptake blocks (S01-B vs S08-C), and an implausible PSLN-212 survival pattern in S03-I.

**How this affects the recommendation:**

- **The direction of the result is robust.** Every version of the survival record favours PSLN-344 by 63–71 pp (Table 3).
- **The antibody and most mechanistic blocks carry no integrity flag** (S03-A/C/D/E/G/H, S13-A–D/I/J, S01-A, S02).
- **What is compromised:** the exact survival magnitudes, the strain-generality claim, the claim that antigen is required for rapid protection, and every body-weight endpoint.
- **Therefore:** (a) no conclusion in this document relies on body weight; (b) strain generality and antigen requirement are listed as *unproven*; (c) Gate A must verify source records before any money beyond Gate B is committed.
- **Escalation.** The recycled trajectories look like copy-paste rather than independent measurement. They should be referred to QA and research-integrity review under our policy. This document makes no finding about intent.


**Table 3b. What we can and cannot claim today.**

| Claim | Key evidence | Confidence | Main caveat |
|---|---|---|---|
| PSLN-344 outperforms PSLN-212 in aged mice | 59/76 endpoints at FDR<5%; 14/14 strata; worst case 63 pp (51-72) | **High** | Magnitudes pending source-data verification |
| Near-young antibody titres in aged mice | HAI RI 0.88/0.94 (S03-C/G), n=5 | Moderate–high | One experiment per antigen; not replicated |
| Cross-subtype and H5N1 protection in aged mice | S06-A/C/E/F/G, S03-J | Moderate | Several blocks carry survival vs body-weight conflicts (C3) |
| Rapid onset (day 2–3) | S03-J, S06-B (15/17 vs 3/17) | Moderate | S06-D duplicate (C1); S03-J conflict (C3) |
| Protection at day 60 in aged mice | S06-E/F/G (14/21) | Moderate–low | Conflicts (C3); unchallenged-control deaths (C4) |
| Works across mouse strains | S15-L/N | **Low** | Challenge not stated; recycled body weights (C2, M7) |
| Rapid protection needs antigen | S15-H | **Low** | Recycled body weights (C2) |
| MoA: IFN/GM-CSF → CCR2 monocytes → moDC → migration and priming | S02-H, S02-G, S07-B, S02-I, S02-C/E, S05-C | Moderate | STING dependence and link to protection untested |
| Safety: no CNS inflammation; mild weight loss | S10-A; S08-D | Low–moderate | One 36-h timepoint; no Mn biodistribution; S08-D may contain recycled values (C2) |

# 4. Mechanism of action (built from our data)

![Figure 5. Mechanism of action with the evidence type for each link.](figures/fig5_moa.png)

**Table 4. Interventional (causal) evidence.** All experiments used PSLN-344 (or PSLN-212 where stated).

| Intervention | Readout | Control | Intervention | Change | p (Welch / exact MW) | Block |
|---|---|---|---|---|---|---|
| Test: SP-A/D knockout vs WT (liposomes of PSLN-344 composition) | DiD+ alveolar macrophages, %, 16 h | 43.1 | 12.7 | -71% | <0.0001 / 0.0286 | S01-C |
| Test: carbenoxolone vs saline (PSLN-344) | Recruited lung monocytes, %, d3 | 7.3 | 3.1 | -58% | 0.0041 / 0.0079 | S11-C |
| Test: IFNAR-/- vs WT bone marrow (no cDC precursors), PSLN-344 | Donor-derived moDC, %, d3 | 19.7 | 2.1 | -89% | 0.0004 / 0.0079 | S02-H |
| Rescue: IFNAR-/- marrow + GM-CSF vs IFNAR-/- marrow | Donor-derived moDC, %, d3 | 2.1 | 12.4 | +494% | 0.0027 / 0.0079 | S02-H |
| Gain: PSLN-212 + rGM-CSF vs PSLN-212 | Lung Ly6C+CD11c+MHC-II+ moDC-like, %, d5 | 5.9 | 13.8 | +136% | 0.0021 / 0.0079 | S02-G |
| Test: IFNAR-/- vs WT marrow (young, n=3) | Infiltrating donor monocytes, %, d3 | 21.3 | 15.4 | -28% | 0.1203 / 0.2000 | S12-A |
| Test: CCR2 antagonist vs vehicle (PSLN-344) | Lung CD11b+Ly6C+ monocytes, % | 9.9 | 3.3 | -67% | 0.0010 / 0.0079 | S07-B |
| Test: CCR2 antagonist vs vehicle (PSLN-344) | Lung Ly6C+ macrophages, % | 15.4 | 2.5 | -84% | 0.0029 / 0.0079 | S07-B |
| Test: CCR2 antagonist vs vehicle (PSLN-344, young) | Lung GZMB+ CD8, %, d5 | 6.8 | 1.4 | -79% | <0.0001 / 0.0079 | S02-I |
| Test: pertussis toxin (blocks Gi chemokine signalling) | AF647-OVA+ DC in MLN, %, 36 h | 7.1 | 2.4 | -67% | 0.0005 / 0.0079 | S02-C |
| Test: pertussis toxin | OT-I proliferation driven by MLN DC, % | 18.7 | 2.5 | -86% | <0.0001 / 0.0079 | S02-E |
| Test: pertussis toxin in vivo (n=3) | OT-I proliferation in MLN, %, d4 | 30.9 | 6.8 | -78% | 0.0066 / 0.1000 | S05-C |
| Test: pertussis toxin in vivo (n=3) | OT-I proliferation in lung, %, d4 | 59.0 | 55.1 | -7% | 0.5687 / 1.0000 | S05-C |

**The mechanism in eight steps.** Confidence is given for each step.

1. **Delivery.** The surfactant-biomimetic vehicle is taken up by alveolar macrophages through SP-A/D: alveolar-macrophage uptake went from wild type to SP-A/D knockout as 43.1 → 12.7, -71%, p<0.001 (S01-C). It also loads type II alveolar epithelium (S01-B). Confidence: high for vehicle targeting. The S08-C finding that Mn2+ lowers epithelial uptake is low confidence (M6).
2. **Mn2+ potentiates STING signalling in the aged lung.** Lung Ifnb1 at 16 h was 36.9× vs 16.5× (young: 37.5×; RI 0.98). In dose–response, Mn2+ mainly raises the ceiling (Emax 49× vs 14×) rather than potency (ED50 11.5 vs 9.5 µg). The result is about 3-fold dose-sparing: PSLN-344 at 6.7–7.3 µg matches PSLN-212 at 20 µg (S08-A), and going from 20 to 40 µg adds only 10%. Confidence: moderate. STING dependence itself has not been tested, and no Mn-only control exists.
3. **Paracrine amplification.** The gap-junction blocker carbenoxolone cut monocyte recruitment (7.3 → 3.1, -58%, p=0.004; S11-C). This is consistent with transfer of cyclic dinucleotide to bystander cells, but carbenoxolone has off-target effects. Confidence: moderate-low.
4. **Chemokines, GM-CSF and CCR2 monocytes.** At 16 h, Ccl2 was 590.1× vs 7.6×, Ccl3 29.8× vs 1.1× and Il6 36.1× vs 5.6× (S09-A). Gm-csf at 36 h was 8.5× vs 1.6× (S02-F). Lung monocytes at day 4 were 30.6% vs 16.7% (young 32.2%; S01-D). A CCR2 antagonist removed most of this: monocytes 9.9 → 3.3, -67%, p=0.001 and Ly6C+ macrophages 15.4 → 2.5, -84%, p=0.003 (S07-B), and downstream lung GZMB+ CD8 6.8 → 1.4, -79%, p<0.001 (S02-I, young). Confidence: high for CCR2 dependence of recruitment.
5. **moDC differentiation needs both type I IFN and GM-CSF.** Without IFNAR, bone marrow yielded few moDC (19.7 → 2.1, -89%, p<0.001). GM-CSF partly rescued this (2.1 → 12.4, +494%, p=0.003; S02-H). Adding GM-CSF to PSLN-212 more than doubled moDC-like cells (5.9 → 13.8, +136%, p=0.002; S02-G). **Interpretation:** the aged-lung defect with PSLN-212 is insufficient GM-CSF, and Mn2+ supplies it. Without Mn2+, monocytes instead accumulate as Ly6C+CCR2+ macrophages (18.5 vs 3.4 ×10^5 at day 5, S07-A). M2-like CD206+ macrophages fall from 71.5% to 48.9% (S11-E; timepoint not stated). Confidence: moderate-high (two independent loss/gain experiments).
6. **DC migration and priming.** CCR7+ migratory DC were 30.7% vs 7.3% (S02-A; RI 0.84). Pertussis toxin reduced antigen+ DC in the MLN (7.1 → 2.4, -67%, p<0.001) and MLN priming (18.7 → 2.5, -86%, p<0.001 ex vivo; 30.9 → 6.8, -78%, p=0.007 in vivo), but not lung priming (59.0 → 55.1, -7%, p=0.569; S05-C). So PSLN-344 primes both in the draining node and locally in the lung. Co-stimulation stays low (RI 0.19). Confidence: high for migration dependence.
7. **Tfh and germinal centre.** ICOS-hi Tfh were 10.3% vs 3.8% (S04-A), Tfr 10.8% vs 26.7% (S04-B) and germinal-centre B cells 6.5% vs 2.3% (S03-K). Together these give Th1-skewed, neutralising antibody (Table 1). Confidence: moderate (correlative).
8. **CD8 effector and resident memory.** IFN-γ+ CD8 were 6.4% vs 1.5% at day 14 and 9.9% vs 3.0% at day 60 (S05-F/G). Lung TRM at day 25 were 4.0% vs 1.0% (S05-I). These responses cross-react with H1, H3 and H5 antigens (S05-F, S14-A), which is the plausible basis of heterosubtypic protection. Confidence: moderate (correlative; no depletion-challenge experiment).

**What the mechanism does not yet show:**

- that the effect requires STING (or cGAS);
- that the proprietary drug CDN-1807 is needed at all (no Mn-only liposome arm);
- whether antibody or CD8 T cells mediate protection;
- that moDC or GM-CSF are required *for protection*, as opposed to immunogenicity.

These four gaps define Study B4. They are commercially important: if a Mn-only liposome reproduces the effect, the value sits in Mn2+, not in CDN-1807.

**External context (not from our dataset; verify before external use).** Published work reports that Mn2+ sensitises the cGAS–STING pathway and that Mn2+–cyclic-dinucleotide coordination particles amplify STING activation. This supports plausibility but also creates prior art, so a freedom-to-operate review is needed.

![Figure 4. Ifnb1 dose–response (S08-A).](figures/fig4_dose_response.png)

# 5. Biomarkers to validate efficacy

**Design logic.** Each candidate below separates PSLN-344 from PSLN-212 in our data, usually with complete separation of the per-animal values. For human use, each needs an accessible matrix: nasal lining fluid, nasal brushings or blood.

**Table 5. Candidate biomarkers by tier.**

| Tier / timing | Marker (our data) | n (344 v 212) | Sham | PSLN-212 | PSLN-344 | Young PSLN-212 | Separation 344 vs 212 | Source | Human-measurable analogue |
|---|---|---|---|---|---|---|---|---|---|
| T1 PD (16-36 h) | Ifnb1 (lung) | 5v5 | 0.9 | 16.5 | 36.9 | 37.5 | complete (AUC 1.0) | S01-A (16h) | IFN-beta / ISG score (blood); CXCL10, IFN-lambda in nasal lining fluid |
| T1 PD (16-36 h) | Ccl2 (lung) | 3v3 | 1.0 | 7.6 | 590 | 1,391 | complete (AUC 1.0) | S09-A (16 h) | CCL2/MCP-1 in nasal lining fluid & serum |
| T1 PD (16-36 h) | Il6 (lung) | 3v3 | 1.0 | 5.6 | 36.1 | 60.3 | complete (AUC 1.0) | S09-A (16 h) | IL-6 (nasal, serum) - also reactogenicity marker |
| T1 PD (16-36 h) | Gm-csf (lung, 36 h) | 5v5 | 1.2 | 1.6 | 8.5 | - | complete (AUC 1.0) | S02-F (36h) | GM-CSF in nasal lining fluid |
| T1 PD (16-36 h) | Tnf (lung, 72 h) [safety] | 3v3 | 1.0 | 5.2 | 8.4 | 0.5 | complete (AUC 1.0) | S09-A (72 h; printed "16h") | TNF/IL-10 persistence = reactogenicity flag |
| T2 cellular (d3-7) | Lung monocytes d4 | 5v5 | 10.4 | 16.7 | 30.6 | 32.2 | complete (AUC 1.0) | S01-D (d4) | nasal brush/curettage myeloid cells (research only) |
| T2 cellular (d3-7) | CCR7+ migratory DC 72 h | 5v5 | 2.5 | 7.3 | 30.7 | 35.0 | complete (AUC 1.0) | S02-A (72h) | not accessible; mechanistic only |
| T2 cellular (d3-7) | ICOS-hi Tfh d7 (MLN) | 5v5 | 0.3 | 3.8 | 10.3 | 13.6 | complete (AUC 1.0) | S04-A (d7) | circulating Tfh (ICOS+PD-1+CXCR5+CXCR3+) d7 blood |
| T2 cellular (d3-7) | Tfr d7 (MLN) | 5v5 | 22.6 | 26.7 | 10.8 | 7.1 | complete (AUC 1.0) | S04-B Foxp3 (d7) | circulating Tfr / cTfh:cTfr ratio d7 blood |
| T2 cellular (d3-7) | GC B cells d7 (MLN) | 5v5 | 1.2 | 2.3 | 6.5 | 9.8 | complete (AUC 1.0) | S03-K (d7) | plasmablasts d7 blood (surrogate) |
| T2 cellular (d3-7) | Ki-67+ CD8 lung d3 | 5v5 | 0.8 | 3.5 | 9.4 | 9.9 | complete (AUC 1.0) | S05-D (d3) | activated CD38+HLA-DR+ CD8 d7-10 blood |
| T3 efficacy surrogate (d14-28) | HAI CA09 d14 | 5v5 | 7.6 | 45.9 | 368 | 485 | complete (AUC 1.0) | S03-C (d14) | HAI GMT, seroconversion, % >= threshold |
| T3 efficacy surrogate (d14-28) | HAI Aichi d14 | 5v5 | 10.0 | 34.8 | 320 | 368 | complete (AUC 1.0) | S03-G (d14) | HAI GMT |
| T3 efficacy surrogate (d14-28) | Neut CA09 d14 | 5v5 | 52.2 | 418 | 3,840 | 6,686 | AUC 0.98 | S03-D (d14) | microneutralisation GMT |
| T3 efficacy surrogate (d14-28) | IgG2a CA09 d14 (Th1) | 5v5 | - | 83.4 | 1,642 | 4,642 | complete (AUC 1.0) | S13-A (d14) | IgG subclass (IgG1/IgG3) + Th1 cytokines |
| T3 efficacy surrogate (d14-28) | IFNg+ CD8 d14 (rgH5N1 restim) | 5v5 | 0.7 | 1.5 | 6.4 | 9.2 | complete (AUC 1.0) | S05-F (d14) | IFN-gamma ELISpot, conserved NP/M1 peptides |
| T4 durability (d25-60) | Lung TRM CD8 d25 | 5v5 | 0.6 | 1.0 | 4.0 | 6.0 | complete (AUC 1.0) | S05-I (d25) | nasal TRM (CD69+CD103+) by nasal brushing |
| T4 durability (d25-60) | IFNg+ CD8 d60 | 5v5 | 1.5 | 3.0 | 9.9 | 14.4 | complete (AUC 1.0) | S05-G (d60) | IFN-gamma ELISpot month 3-6 |
| T4 durability (d25-60) | GZMB+ CD8 d60 | 5v5 | 0.6 | 1.0 | 4.1 | 5.6 | complete (AUC 1.0) | S05-H (d60) | granzyme B+ CD8 (blood) |

**How to use them:**

- **Tier 1, pharmacodynamic (hours–days).** Markers: IFN-β/ISG, CXCL10, CCL2, IL-6 and GM-CSF in nasal lining fluid and serum.
  - *Why:* Ifnb1 is dose-responsive (S08-A) and fully restored in aged mice (RI 0.98).
  - *Use:* target engagement and dose selection in Phase 1.
  - *Gap:* we have lung tissue only. Study B4 must show that BAL, nasal-wash and serum levels track lung levels.
  - *Safety read:* TNF/IL-10 still raised at 72 h is the reactogenicity flag (8.4× vs young 0.5×).
- **Tier 2, cellular (days 3–10).** Markers: circulating Tfh (ICOS+PD-1+CXCR5+) and the cTfh:cTfr balance at day 7, plus day-7 plasmablasts.
  - *Why:* ICOS-hi Tfh and Tfr gave complete separation (S04-A/B), and circulating Tfh are measurable in blood.
  - *Use:* early go/no-go in the ≥65 cohort, well before titres peak.
- **Tier 3, efficacy surrogates (days 14–28).** Markers: HAI GMT and seroconversion, microneutralisation, nasal IgA (not yet measured, a gap) and IFN-γ ELISpot against conserved NP/M1 peptides.
  - *Candidate protective threshold, to be tested:* HAI ≥1:160. Animals reaching ≥1:160 (S03-C): PSLN-344 5/5, young 5/5, PSLN-212 0/5, CMP-204 0/5, Sham 0/5. In the matched survival experiment (S03-I), both groups in which every animal reached it survived 7/7; the others survived at most 3/7 (CMP-204 3/7, PSLN-212 0/7, sham 0/7).
  - *Caveat:* PSLN-212 animals all reached the conventional ≥1:40 yet survived 0/7. This is group-level evidence from different animals, and S03-I carries integrity flags (M8). B1 measures titres and survival in the *same* animals to test the threshold properly.
- **Tier 4, durability (days 25–180).** Markers: IFN-γ ELISpot and nasal resident-memory T cells.
  - *Why:* heterosubtypic survival followed the T-cell rank order. TRM: sham 0.6%, PSLN-212 1.0%, PSLN-344 4.0%, young 6.0%. Day-60 heterosubtypic survival: sham 0/21, PSLN-212 1/21, PSLN-344 14/21, young 21/21.
  - *Caveat:* every candidate marker has the same rank order (sham < PSLN-212 < PSLN-344 < young). The current design therefore **cannot say which marker is mechanistic**. The antibody-transfer and CD8-depletion arms of B4 are designed to answer that.
- **Safety biomarkers.**
  - Serum Mn.
  - Olfactory function (smell test).
  - CNS-proximal signals in animals: olfactory-bulb Mn, Ifnb1/Tnf/Isg15. In S10-A, CNS Ifnb1 went from sham to PSLN-344 as 1.1 → 1.3, +14%, p=0.568, and from sham to cholera toxin as 1.1 → 5.4, +384%, p<0.001.

# 6. Target demographic (for the market-research TAM check)

I do not estimate TAM here: it cannot be derived from our data. Below are segment definitions, the evidence for each, and the parameters market research needs to source.

**Primary segment: adults ≥65 years, seasonal influenza, annual intranasal dose.**

- *Evidence:* in 20-month-old mice only PSLN-344 protects (61/73 (84%) vs 9/73 (12%)). In young mice Mn2+ adds little: both young arms survived 8/8 in S09-B/D/F, and Ifnb1 went from young PSLN-212 to young PSLN-344 as 37.5 → 50.2, +34%, p=0.009.
- *Age mapping (external):* 18–24-month mice correspond roughly to humans in their late 50s to late 60s.
- *Value claims to test:*
  - needle-free, one dose;
  - near-young HAI (RI 0.88–0.94);
  - cross-subtype T-cell protection for mismatch seasons;
  - Th1-skewed antibody.

**Secondary segment, conditional on Study B1: adults 50–64, particularly with chronic conditions.**

- *Evidence:* in 14-month-old naive mice, PSLN-212 already failed (0/7 and 0/7) while PSLN-344 protected (6/7, 6/7). The age-related failure therefore begins in middle age.
- *Imprinting:* prior infection did not reduce PSLN-344 protection (6/7, 6/7). This is relevant to an adult population with pre-existing immunity.

**Tertiary segment: pandemic preparedness (H5), via government stockpiles.**

- *Purchasers and recipients:* governments; all adults, with older adults prioritised.
- *Evidence:* against wild-type H5N1 two days after one dose, survival was 10/10 vs 3/10 (sham 1/10). Against rgH5N1 in aged mice, after a bivalent H1/H3 vaccine (i.e. cross-subtype), it was 7/7 at day 14 and 5/7 at day 60. Young mice were protected at day 180 (8/8).
- *Not yet tested:* antigen sparing (Study B3), which is what governments buy on.

**Exploratory segment: outbreak response in long-term-care settings.**

- *Evidence:* rapid onset (15/17 vs 3/17 survivors at days 2–3).
- *Open question:* whether the adjuvant alone protects. The only test (S15-H: 0/7 alone vs 6/7 with vaccine) carries an integrity flag.

**Exclude from the initial TAM (no data):** people under 18, pregnancy, immunocompromised people, pre-existing olfactory or neurological disease (Mn2+), and severe asthma/COPD (intranasal route).

**Parameters for market research to source,** by region (US, EU4+UK, Japan) and segment:

- population size;
- seasonal influenza vaccine uptake;
- share of "enhanced" vaccines (high-dose, adjuvanted, recombinant) in ≥65;
- net price of enhanced vaccines;
- stated preference for needle-free vaccination;
- H5 stockpile volumes and procurement cadence.

**External context (verify):** in the US, the only licensed intranasal influenza vaccine (live attenuated) is approved up to age 49, and enhanced vaccines are preferentially recommended for ≥65. Positioning therefore depends on beating those enhanced vaccines. B1 includes analogues of them for exactly this reason.

# 7. Next steps: what the studies must establish

## 7.1 What the next studies have to establish

- **E1.** The existing data are authentic, and the effect reproduces blind, in both sexes and two strains (Gate A; B1).
- **E2.** PSLN-344 is differentiated from what older adults receive today (B1 standard-of-care analogue arms).
- **E3.** Intranasal Mn2+ does not reach or injure the olfactory system or CNS at efficacious doses (B2; then C1–C3).
- **E4.** CDN-1807 is necessary (Mn-only control), and the product is defined, stable, potent and active on human STING variants (B3, B4).
- **E5.** We know what mediates protection and which human-measurable biomarkers track it (B4; individual-animal correlates in B1).
- **E6.** Durability beyond 60 days in aged animals and the role of a boost (B1 durability cohort). Current data: 14/21 at day 60, and post-boost RI 0.62.
- **E7.** Translation to species with human-like airway and influenza biology (C1 ferret, C2 aged NHP).

## 7.2 Study plan

Timings are planning estimates from 2 November 2026.

**Study A. Data-integrity remediation (Gate A).**

- **Population:** not an animal study. Scope is all 15 sheets, starting with C1–C4 and M1–M8.
- **Comparator:** primary records, i.e. FCS files and gating templates, ELISA/HAI plate reads, qPCR Ct files, animal-room weight, health and euthanasia logs, randomisation and blinding records.
- **Endpoints:** each flagged block either reconciled to source or declared unverifiable; locked, version-controlled dataset; root cause and CAPA (electronic lab notebook with audit trail, two-person data verification).
- **Readout / timing:** independent QA group. Nov 2026 – Jan 2027 (about 12 weeks); decision early Feb 2027.
- **n / power:** not applicable.
- **Pass criteria:** survival records for S03-I, S03-J and S06-A–G, and antibody records for S03 and S13, verified. If not, B1 becomes the sole efficacy evidence; the committee may choose to stop.

**Study B1. Confirmatory randomised, blinded, pre-registered efficacy in aged mice.**

- **Population:** 20–22-month BALB/c (full arm set) and C57BL/6 (core arms), **both sexes**. Young (8–10-week) benchmark; unchallenged aged controls.
- **Comparators (vaccine = inactivated bivalent or Aichi H3N2, as in our studies):**
  - intranasal: sham liposome; PSLN-212; PSLN-344; Mn-only liposome;
  - intramuscular: high-dose (4× HA) analogue; squalene-emulsion (AddaVax, MF59-like) analogue;
  - rapid-onset cohort adds PSLN-344 alone (no antigen).
- **Primary endpoint:** survival to day 14 after 5× mLD50 heterosubtypic challenge (PR8 H1N1 after H3N2 vaccine) at day 28, scored blind.
- **Key secondary endpoints:** lung viral titre on days 3 and 5 (satellite n = 6/arm/day); weight-loss AUC; HAI and microneutralisation GMT and % ≥1:160 (pre-challenge bleed, same animals); nasal and BAL IgA; IFN-γ ELISpot; lung TRM.
- **Additional cohorts:**
  - homologous CA09 challenge;
  - rapid onset (challenge at day 3), replacing the duplicated S06-D;
  - durability (challenge at days 90 and 180);
  - exploratory 12–14-month cohort for the 50–64 segment.
- **n / power:** 28/arm (14 per sex). This gives 80% power for 80% vs 40% survival (PSLN-344 vs best SOC analogue; exact Fisher, α 0.05) and ≥80% for the worst-case observed 63% vs 20% (24/arm needed) (`power.py`).
- **Readout / timing:** in-life Feb – Jul 2027; report Sep 2027.
- **Go criteria:** PSLN-344 heterosubtypic survival ≥70%; superior to PSLN-212 (p<0.05); HAI GMT ≥4× PSLN-212 (observed 8–9×); point estimate of survival ≥20 pp above the best IM analogue. The study can confirm a 40-pp advantage statistically; smaller advantages will need the ferret and NHP data.
- **Redirect:** if PSLN-344 is not better than IM analogues, reposition to pandemic/needle-free only, or stop.
- **Stop:** if it is not superior to PSLN-212.

**Study B2. Mn2+ and intranasal safety: olfactory/CNS and systemic.**

- **Population:** Sprague-Dawley rats (young adult, plus aged if available), both sexes; aged-mouse satellite from B1.
- **Comparators:** vehicle; PSLN-212 (Mn-free); PSLN-344 at 1×, 3× and 10× the intended dose (dose defined after Mn content is measured in B3); free MnCl2 at the Mn-equivalent of the top dose (positive control for olfactory transport). Dosing on days 0, 14 and 28, with recovery.
- **Endpoints:**
  - Mn by ICP-MS in olfactory bulb, striatum, cortex, blood and turbinates;
  - histopathology of olfactory epithelium, olfactory bulb, facial nerve/geniculate and trigeminal ganglia;
  - CNS Ifnb1/Tnf/Isg15/Cxcl10 (extends S10-A beyond 36 h);
  - neurobehaviour: functional observational battery, open field, rotarod, buried-food olfaction;
  - serum IL-6/TNF/IFN-β/CXCL10; clinical pathology.
- **Readout / timing:** days 1, 7, 28, 90 (cytokines also at 4, 24, 72 h). Jan – Aug 2027 (starts once dose is defined).
- **n / power:** 10 per sex per group per timepoint. This gives 80% power to detect a 1.5-fold rise in olfactory-bulb Mn at CV 30%; at CV 50%, 23/group would be needed (`power.py`).
- **Go criteria:** no treatment-related olfactory/CNS histopathology; olfactory-bulb Mn at day 28 ≤1.5× vehicle at the intended dose, with ≥10× margin to any finding; no neurobehavioural change; no cytokine elevation beyond 72 h.
- **Stop:** otherwise, stop PSLN-344.

**Study B3. Dose, CMC, potency assay and human STING variants.**

- **Population:** aged BALB/c for dose-ranging; human cell lines for potency.
- **Comparators:** PSLN-344 at 2.5, 5, 10, 20 and 40 µg with fixed antigen; antigen-sparing arms (0.5, 0.15, 0.05 µg HA) at the selected dose; PSLN-212 and cGAMP as potency references.
- **Endpoints:**
  - in vivo: HAI/MN at day 28, Ifnb1/Cxcl10 at 16 h, weight nadir, serum IL-6 at 6 h;
  - CMC: Mn and CDN-1807 per dose (ICP-MS/HPLC); encapsulation efficiency (PSLN-212 → PSLN-344: 59.6 → 54.8, -8%, p=0.289, S08-B); size, PDI, zeta and free Mn; lyophilised stability under ICH conditions (−20 °C, 2–8 °C, 25 °C); in-vitro IFN reporter release assay;
  - human STING haplotypes (WT, HAQ, R232H, AQ, R293Q) ± Mn2+.
- **Readout / timing:** Dec 2026 – Jul 2027; 6-month stability data by Jul 2027.
- **n / power:** 10/arm (9 per arm detects a 2-fold GMT difference at 80% power, using within-group SD 0.68 log2 from S03-C/G).
- **Go criteria:** minimal dose achieving ≥90% of maximum HAI; ≥6-month stability; activity across common human STING haplotypes. HAI has never been dose-ranged. The only dose data are Ifnb1 (S08-A), where 10 µg gives 46% of the 20-µg response and 40 µg adds only 10%, which puts the plateau near 20 µg.

**Study B4. Mechanism and correlates of protection.**

- **Population:** aged BALB/c; young Sting1^gt/gt and WT where knockouts are needed.
- **Comparators:**
  - STING inhibitor H-151 vs vehicle;
  - Mn-only liposome vs PSLN-212 vs PSLN-344 (synergy test);
  - passive transfer of aged PSLN-344 immune serum;
  - anti-CD8β depletion;
  - anti-GM-CSF and CCR2 antagonist before challenge;
  - PSLN-212 + GM-CSF (fallback hypothesis if Mn fails).
- **Endpoints:** Ifnb1, Gm-csf, moDC and HAI (dependence); survival after challenge (mediators); serum, BAL and nasal-wash IFN-β/CXCL10/CCL2/IL-6/GM-CSF at 6, 16 and 36 h vs lung qPCR (biomarker bridging).
- **Readout / timing:** Feb – Sep 2027.
- **n / power:** 8–10/arm.
- **Criteria:** informative, not a kill gate, except that if Mn-only equals PSLN-344, the asset thesis must be re-set.

**Gate B decision: October 2027.**

**Study C1. Ferret efficacy and transmission (after Gate B).**

- **Population:** adult ferrets (aged ferrets if obtainable).
- **Comparators:** PSLN-344 intranasal; unadjuvanted intranasal vaccine; licensed enhanced IM vaccine.
- **Endpoints:** nasal-wash viral shedding AUC (days 1–7); transmission to naive contacts; HAI/MN; nasal IgA; olfactory-bulb Mn.
- **Readout / timing:** Nov 2027 – Mar 2028.
- **n / power:** 6–8/arm.
- **Go criteria:** shedding AUC reduced vs IM comparator; no olfactory findings.

**Study C2. Aged non-human-primate immunogenicity and safety with the clinical nasal device.**

- **Population:** rhesus or cynomolgus macaques ≥18 years.
- **Comparators:** PSLN-344 intranasal vs enhanced IM vaccine.
- **Endpoints:** HAI/MN; nasal IgA; circulating Tfh at day 7; ELISpot; CRP/IL-6; nasal CXCL10 (pharmacodynamic bridge); Mn in blood and CSF.
- **Readout / timing:** Jan – Jul 2028.
- **n / power:** 6/arm.
- **Go criteria:** HAI/IgA/T-cell responses non-inferior to IM; acceptable reactogenicity.

**Study C3. GMP lot and GLP toxicology (IND-enabling).**

- **Population:** rats; repeat intranasal dosing (N+1) with recovery.
- **Comparator:** vehicle.
- **Endpoints:** standard GLP endpoints plus CNS/olfactory histopathology and local tolerance.
- **Readout / timing:** Q2 – Q4 2028; IND/CTA target about Q1 2029.
- **Go criteria:** no adverse findings at ≥10× the clinical dose.

## 7.3 Gates and pre-specified kill criteria

| Gate | Date | Proceed if | Stop or redirect if |
|---|---|---|---|
| **A: integrity** | Feb 2027 | Critical findings reconciled; locked dataset | Primary records unverifiable → B1 becomes the only evidence base (committee may stop). Evidence of manipulation → research-integrity process |
| **B: confirm and de-risk** | Oct 2027 | B1, B2 and B3 go criteria met | Not superior to PSLN-212 → **stop**. CNS Mn or histopathology → **stop PSLN-344** (test the GM-CSF fallback only if B4 supports it). No edge over SOC analogues → **reposition** (pandemic/needle-free) or stop |
| **C: IND readiness** | ~Q4 2028 | Ferret and NHP criteria met; GLP clean; GMP lot released | Adverse GLP findings or NHP non-response → stop |

## 7.4 First-in-human outline (for planning only)

- **Design:** randomised, observer-blind, active-controlled.
- **Part A:** adults 18–49, sentinel-dosed escalation across 3 dose levels.
- **Part B:** adults ≥65, 2 dose levels vs a licensed enhanced IM vaccine and unadjuvanted intranasal vaccine.
- **Safety endpoints:**
  - solicited nasal and systemic reactions to day 7; unsolicited to day 28;
  - adverse events of special interest: facial-nerve palsy, anosmia or hyposmia (formal smell testing), neurological events;
  - serum Mn; CRP/IL-6.
- **Immunogenicity endpoints:**
  - HAI GMT, seroconversion, % ≥1:40, plus an exploratory % ≥1:160;
  - microneutralisation; nasal IgA;
  - circulating Tfh at day 7; IFN-γ ELISpot at day 28.
- **Pharmacodynamic endpoints:** nasal CXCL10/IFN-λ on days 1–2; blood ISG score on day 1.

# 8. If we drop PSLN-344: what we give up, and the objective case for dropping

**What we would give up (from our data):**

1. **The only formulation in the portfolio that protects aged animals:** 61/73 (84%) survival vs 9/73 (12%) (PSLN-212) and 1/73 (1%) (sham). This is the program's entire differentiation for the ≥65 market. Without Mn2+, CDN-1807 does not protect aged mice.
2. **Near-young antibody in the aged host.** HAI GMT 368 vs young 485. All 5 PSLN-344 animals reached ≥1:160, against none of 5 with PSLN-212.
3. **Breadth that matters for mismatch seasons and pandemics:**
   - heterosubtypic protection (S06-A 6/7 vs 1/7; S06-G at day 60 4/7 vs 0/7);
   - H5N1 protection (wild-type, day 2: 10/10 vs 3/10; rgH5N1 at day 60 5/7 vs 1/7);
   - rapid onset (15/17 vs 3/17).
4. **A mechanistic explanation of *why* the aged lung fails** (insufficient GM-CSF/IFN for moDC differentiation) and a way to fix it. This may be reusable for other respiratory vaccines for older adults, but that is untested option value.
5. **Time.** Re-creating an aged-population adjuvant would, at best, restart at the equivalent of Gate B.

**The objective case for dropping:**

1. **Integrity.** Four critical findings. If Gate A fails, every magnitude in this document must be re-earned, and the recycled data are a governance risk in their own right.
2. **Mn2+ neurotoxicity risk.** Intranasal Mn is transported along the olfactory nerve in animals (external literature). Our CNS data are a single 36-h cytokine panel in 5 mice per group, with no Mn measurement.
3. **Intranasal-adjuvant regulatory history.** An intranasal toxin-adjuvanted influenza vaccine was withdrawn over facial-nerve palsy (external). STING agonists can provoke systemic inflammation, and we already see Tnf/Il10 persisting in aged lungs at 72 h.
4. **Incomplete rejuvenation.** Co-stimulation RI 0.19; memory RI 0.62; a trend to lower survival at day 60. PSLN-344 may not beat entrenched enhanced IM vaccines in people.
5. **Translation and market risk.** Mouse-only and female-only data; human STING polymorphism; no ferret or NHP data; crowded ≥65 market; prior art on Mn–CDN particles.

**Net judgement.** Every one of these risks is testable within the Gate A–B window (November 2026 – October 2027, Section 7), at a cost that is small relative to IND-enabling spend. The efficacy signal is too large and consistent to discard on untested risks. If Gate A or B fails on the pre-specified criteria, the recommendation flips to **stop**, and this section is the record of what we knowingly gave up.

# 9. What I considered and ruled out

**Asset options:**

- **Advance PSLN-212, or both in parallel.** Ruled out.
  - In aged mice PSLN-212 is further from the young benchmark than PSLN-344 on every significant endpoint that has a benchmark (47/47), and survival is 9/73 (12%) vs 61/73 (84%).
  - It offers no advantage in young mice (8/8 survivors in both arms in S09-B/D/F).
  - It shows no safety advantage (weight nadir 97.0% vs 96.4%, p=0.56).
  - Its only theoretical advantage is absence of Mn2+. But if Mn fails B2, PSLN-212 still would not protect aged animals, so it is not a real fallback for ≥65.
  - Kept only as the Mn-free control.
- **R848 combinations (PSLN-R848, PSLN-212/R848, PSLN-344/R848).** Ruled out.
  - PSLN-212/R848 gave lower Ifnb1 than PSLN-344 (36.9 → 24.0, -35%, p=0.001) and higher Tnf/Il10 (S09-A).
  - It caused more weight loss (mean nadir 90.0% vs PSLN-344 96.4%, p=0.043; maximum individual loss 15%), with one unexplained missing animal at day 10 (S08-D).
  - PSLN-344/R848 is undefined in Materials and has a lower ceiling than PSLN-344 (Emax 36 vs 49; S08-A).
- **cGAMP liposome (CMP-204).** Ruled out. Ifnb1 went from PSLN-212 to CMP-204 as 16.5 → 7.7, -54%, p<0.001. Day-14 titres were 1.1-2.3x lower than PSLN-212 and 11-40x lower than PSLN-344 (six titre endpoints, S03-A/C/D/E/G/H). This also supports CDN-1807 as our differentiating drug.
- **Adjuvant alone as a non-specific antiviral prophylactic.** Not supported: PSLN-344 alone gave 0/7 survivors at day 3 (S15-H). The block carries an integrity flag, so this is retested in B1.
- **All-ages or young-adult indication.** Ruled out as the lead. There is no differentiation in young animals, and a licensed intranasal vaccine already serves young adults (external).

**Decision options:**

- **Kill now.** Ruled out. The effect is large (worst case 63 pp (51-72)), consistent (14/14 strata; 47/47 benchmarked endpoints moved toward young) and mechanistically explained, and the integrity questions can be tested cheaply.
- **Full go to IND-enabling work now.** Ruled out. There are critical integrity findings, no Mn/CNS data, no SOC comparator and no large-animal data.

**Analytical choices:**

- **Naive pooling of survival across experiments.** Rejected because challenge strains and timings differ. I used stratified analyses (Mantel–Haenszel, stratified log-rank, stratified Cox).
- **Sato variance CIs.** Rejected because they exceeded 100% in sparse subsets. I used Newcombe intervals; with balanced arms the Mantel–Haenszel difference equals the crude difference.
- **ANOVA/Tukey on raw titres, as in the stated methods.** Rejected because titres are log-normal. I used log-scale Welch tests with BH-FDR, and exact Mann–Whitney as a sensitivity check. Conclusions are unchanged: 59 endpoints significant, 55/59 of them with complete separation of the per-animal values.
- **Body weight as an efficacy endpoint.** Rejected (recycled, C2).
- **Tfh:Tfr ratio as independent evidence.** Rejected: it is derived from Foxp3%.
- **S09-A Ifnb1 as independent evidence.** Rejected: it re-uses S01-A animals.
- **S03-B/F ratios as printed.** Rejected: labels rotated.
- **S11-A/B, S07-C, S05-A/B and the S08 unlabelled region.** Excluded.
- **Individual-animal correlates of protection.** Not possible, because immunogenicity and challenge used different animals. Only group-level associations are reported, and B1 fixes this.
- **A TAM figure.** Not derivable from our data; handed to market research with segment definitions (Section 6).

# 10. Methods (summary)

**Extraction.** All 15 sheets were parsed block by block into tidy tables with cell references (`tidy/values.csv`, `tte.csv`, `bw.csv`).

**Integrity checks.** Stated vs observed n; exact, partial and multiset duplicates; high-precision value fingerprints; derived-metric reconstruction; survival vs body-weight reconciliation; biological plausibility.

**Continuous endpoints.**

- Scale: titres, qPCR and counts analysed on log2 (HAI <1:10 set to 5); the S09-A log10 values used as stored; percentages on the linear scale.
- Tests: Welch t with 95% CI (primary); exact Mann–Whitney (sensitivity).
- Multiplicity: Benjamini–Hochberg across 76 independent endpoints. Excluded from the family: day-0 baselines (no pre-treatment imbalance, all p>0.13), derived metrics, duplicated or non-independent blocks and compromised blocks.

**Restoration index.** Computed on the analysis scale, with bootstrap CIs (4,000 resamples).

**Survival.**

- Per experiment: log-rank and Fisher exact tests.
- Pooled: Mantel–Haenszel risk difference with Newcombe CI, CMH test, stratified log-rank and stratified Cox (R survival 3.8-3).
- Robustness: sensitivity sets A–F plus leave-one-out.

**Dose–response.** 4-parameter Emax fit.

**Power.** Exact Fisher enumeration and non-central t, using SDs from our data.

**Caveats.**

- n is 3–10 per group, and immunogenicity and challenge were done in separate animals.
- Female mice only.
- The restoration index is a ratio of differences and is imprecise when the young–aged gap is small.

# Appendix A. Data-integrity register

**C1 (Critical) - S06-C, S06-D, S15-D.** *Evidence:* `S06!M3:Q30 vs S06!A34:E61; audit.py / tte_bw_check.py`

- *Finding:* S06-D (rgH5N1 challenge at day 3) is identical, animal for animal, to S06-C (challenge at day 14): all 28 time/event pairs match, including 5 PSLN-212 death days (5,8,10,10,12). The S15-D body-weight record for S06-D shows flat-lined (dead) PSLN-344 and young animals (S15!W37:W40, AC37:AC40, F37:F40, G38:G40) that S06-D records as survivors.
- *Impact:* One of the 8 aged BALB/c challenge experiments is not independent; the true day-3 rgH5N1 result is unknown.
- *How handled here:* S06-D excluded from all pooled analyses; worst-case sensitivity re-enters it with the body-weight-implied counts (PSLN-344 5/7, PSLN-212 3/7).
- *Remediation:* Retrieve primary survival logs for both experiments; repeat the day-3 rgH5N1 challenge in Study B1 (rapid-onset cohort).

**C2 (Critical) - S15-I/S15-C; S15-M, S15-O vs S15-A and S09-E; S15-J/K; S09-E/G; S08-D/S15-F.** *Evidence:* `bw_recycle.py; fingerprint.py (39 repeated high-precision values)`

- *Finding:* Body-weight trajectories are reused across experiments: the S15-I "3d Vaccine+PSLN-344" arm equals S15-C PSLN-344 for 40 of 42 values on days 2-12; young BALB/c PSLN-344 animals (S09-E, e.g. S09!X40:X45) reappear as young C57BL/6 PSLN-212 animals (S15!I104:I109); aged BALB/c PSLN-344 animals (S15-A) reappear in the C57BL/6 and Swiss Webster blocks (S15-M, S15-O); S15-M and S15-O share Sham values (S15!Q104/Q135, Q105/Q136, R105/R136).
- *Impact:* Body weight cannot serve as independent evidence. The multi-strain experiments (S15-L/N) and the antigen-requirement experiment (S15-H) are in doubt.
- *How handled here:* Body weight not used for any efficacy inference. S15-L, S15-N and S15-H are flagged wherever cited. Strain generality and antigen requirement are not claimed as established.
- *Remediation:* Forensic review of animal-room weight logs; repeat strain-generality (C57BL/6) and adjuvant-alone arms in Study B1.

**C3 (Critical) - S03-I/S13-F; S03-J/S13-G; S06-E/S15-E; S06-G/S15-G.** *Evidence:* `bw_vs_tte.csv`

- *Finding:* Survival records conflict with their own body-weight records. Examples: S03-I lists all 7 PSLN-212 deaths by day 6, but S13-F shows 7 PSLN-212 animals weighed on day 10 and 3 recovering to 95-99% (S13!T40:V40). S03-J lists 9/10 Sham deaths, but S13-G shows 4 Sham animals recovering to >=99.7% (S13!L50, M50, O50, P50). S06-E lists 7/7 PSLN-212 deaths, but one recovers to 99.7% in S15-E (S15!P50). S13-F and S13-G also list groups (Naive) that their parent survival blocks do not contain.
- *Impact:* Exact survival counts are uncertain; the direction (PSLN-344 > PSLN-212) holds in every version of the record.
- *How handled here:* Sensitivity analyses: (B) exclude conflicting experiments; (C) take the count less favourable to PSLN-344. Difference stays 63-71 percentage points in all versions.
- *Remediation:* Source-data verification of euthanasia/death logs; a blinded confirmatory study (B1) is the definitive fix.

**C4 (Critical) - S06-E, S06-G (Untreated arms); S15-E, S15-G.** *Evidence:* `S06!G62, S06!A99:A101; S15!AD65:AF70`

- *Finding:* Unvaccinated, unchallenged 20-month-old controls died: 4/21 (19%, 95% CI 5-42%) within 14 days, at flat body weights of ~95-97% (no wasting).
- *Impact:* Background mortality this high is implausible and confounds aged survival. In S06-G, PSLN-344 survival (4/7) equals unchallenged-control survival (4/7).
- *How handled here:* Reported; treated as noise common to all arms (it cannot favour PSLN-344 over PSLN-212).
- *Remediation:* Check colony health-monitoring, sentinel serology and necropsy records (cross-infection vs recording error); include unchallenged aged controls in B1.

**M1 (Major) - S03-B, S03-F vs S13-A-D.** *Evidence:* `crosscheck.py`

- *Finding:* The printed IgG2a/IgG1 quotients carry rotated group labels. Printed "PSLN-212" = computed young ratio; printed "PSLN-344" = computed PSLN-212 ratio; printed "PSLN-212(Y)" = computed PSLN-344 ratio (exact to 3 decimals).
- *Impact:* As printed, the quotients would suggest PSLN-344 is Th2-skewed (0.58). The primary titres show the opposite: 2.14 vs 0.58 (H1) and 2.73 vs 0.51 (H3).
- *How handled here:* Quotients recomputed from the primary S13 titres; S03-B and S03-F not used.
- *Remediation:* Correct the figure source; confirm against raw subclass ELISA plates.

**M2 (Major) - S11-A, S11-B.** *Evidence:* `audit.py`

- *Finding:* Alveolar-macrophage (S11-A) and neutrophil (S11-B) blocks share identical values for animals 1-2 in every group at every day (about 40 of 100 values).
- *Impact:* Copy error; neither block is interpretable.
- *How handled here:* Both excluded.
- *Remediation:* Re-export from FCS files.

**M3 (Major) - S09-A.** *Evidence:* `crosscheck.py`

- *Finding:* The second S09-A panel ("16h") reproduces log10 of the S01-A 72-h Ifnb1 values (21/21 matches), so it is the 72-h timepoint. The S09-A "PBS" group reproduces the S01-A "Sham" group, so the S09-A Ifnb1 row is not independent of S01-A.
- *Impact:* Without correction, 72-h cytokines would be read as 16-h values.
- *How handled here:* Panel 2 treated as 72 h. S09-A Ifnb1 not counted as independent evidence.
- *Remediation:* Correct labels in the source figure.

**M4 (Major) - S07-C.** *Evidence:* `S07!B15:C15`

- *Finding:* Both columns are labelled "Ly6C-CD206+ MPhi"; the annotation says one should be Ly6C+CD206-.
- *Impact:* Cannot tell which macrophage subset induces lung Treg.
- *How handled here:* Excluded.
- *Remediation:* Re-label from the sort records.

**M5 (Major) - S05-A, S05-B.** *Evidence:* `S05!A1:I10`

- *Finding:* Stated n=3 but 2 observations per group. Conditions are contradictory (ovalbumin vs bivalent vaccine). NP366-374 is an H-2Db epitope, but BALB/c mice are H-2d.
- *Impact:* Tetramer data are not interpretable as described.
- *How handled here:* Excluded.
- *Remediation:* Confirm strain and epitope; repeat if needed.

**M6 (Major) - S01-B vs S08-C.** *Evidence:* `crosscheck.py`

- *Finding:* Same condition (PSLN-SRB, aged, 16 h) in two blocks. The AECII columns share 3 of 5 values, yet AECI uptake differs 3.6-fold (3.8% vs 13.8%). The S08-C "AECII-PSLN-344-SRB" values resemble the S01-B AECI values.
- *Impact:* The claim that Mn2+ reduces epithelial uptake is low confidence.
- *How handled here:* Reported as low confidence; not used in the MoA backbone.
- *Remediation:* Re-analyse the FCS files with one gating template.

**M7 (Major) - S15-L, S15-N.** *Evidence:* `annotation p.19; tte_bw_check.py`

- *Finding:* Challenge virus, dose and timing are not stated. The PSLN-344 survival vectors are identical to S06-A and the imprinting arms, and the body-weight records are recycled (C2).
- *Impact:* Strain generality (C57BL/6, Swiss Webster) is not established.
- *How handled here:* Included in the as-recorded pool but excluded in sensitivity analysis B. Leave-one-out shows no influence.
- *Remediation:* Repeat in aged C57BL/6 (Study B1).

**M8 (Major) - S03-I.** *Evidence:* `S03!D31:D37 vs S03-C`

- *Finding:* Aged PSLN-212 animals die earlier (days 5-6) than Sham (days 5-11) despite 6x higher HAI. CMP-204, with lower HAI, has 3/7 survivors. The record also conflicts with S13-F (C3).
- *Impact:* Biologically anomalous; may overstate the PSLN-212 deficit in this one experiment.
- *How handled here:* Covered by sensitivity analysis C (PSLN-212 set to 3/7).
- *Remediation:* Source-data verification.

**m1 (Minor) - S03-J.** *Evidence:* `S03!G46`

- *Finding:* Stated n=9 but 10 per group; PSLN-344 animal 10 has event=0 but no day value.
- *Impact:* Negligible.
- *How handled here:* Censoring time imputed as 21 days (all other censored animals were recorded at 21 days).
- *Remediation:* Complete the record.

**m2 (Minor) - S13-E; S09-B; S09-F.** *Evidence:* `annotation vs workbook`

- *Finding:* Stated n does not match observed counts: S13-E stated 5, observed 7. S09-B Sham has 8 animals (annotation: 7). S09-F Sham has 7 (annotation: 8).
- *Impact:* Negligible.
- *How handled here:* Observed counts used.
- *Remediation:* Correct the annotation.

**m3 (Minor) - S06.** *Evidence:* `S06!G69, M69`

- *Finding:* Block labels S06-E and S06-F are each used twice (rows 34-68 and rows 71-105).
- *Impact:* Risk of citing the wrong experiment.
- *How handled here:* Renamed S06-E[imprint] and S06-F[imprint].
- *Remediation:* Relabel.

**m4 (Minor) - S04-B Tfh:Tfr.** *Evidence:* `audit: (100-Foxp3)/Foxp3 reproduces every value (max error 4e-6)`

- *Finding:* The Tfh:Tfr ratio is an algebraic transform of the Foxp3+ percentage.
- *Impact:* Not independent evidence.
- *How handled here:* Excluded from endpoint counts.
- *Remediation:* Present as derived.

**m5 (Minor) - S08-A, S08-B.** *Evidence:* `S08!K2; S08!G10`

- *Finding:* "PSLN-344/R848" is not defined in Materials. Encapsulation of PSLN-R848 was measured by CDN-1807 absorbance although it contains no CDN-1807.
- *Impact:* Limited.
- *How handled here:* R848 formulations treated as deprioritised.
- *Remediation:* Document the formulations.

**m6 (Minor) - S08 rows 89-101.** *Evidence:* `S08!A89:D101`

- *Finding:* Unlabelled numeric region: A=14, C/D=0 for 13 rows, resembling censored survival records.
- *Impact:* Unattributable.
- *How handled here:* Excluded.
- *Remediation:* Identify the source or delete.

**m7 (Minor) - S11-E, S13-H, S14-A; S02-C/E; S06-E[imprint].** *Evidence:* `annotation`

- *Finding:* Timepoints not stated (S11-E, S13-H, S14-A); the adjuvant in the PTX groups is not stated (S02-C/E); the challenge day is not stated (S06-E[imprint]).
- *Impact:* Limits interpretation.
- *How handled here:* Reported as "not stated".
- *Remediation:* Complete the metadata.

**m8 (Minor) - S09-C.** *Evidence:* `S09!G18:N18 vs W18:AD18`

- *Finding:* Day-12 weights are identical for young PSLN-212 and young PSLN-344 (8/8 animals).
- *Impact:* Part of C2.
- *How handled here:* Body weight not used.
- *Remediation:* See C2.

**m9 (Minor) - S08-D.** *Evidence:* `S08!W26`

- *Finding:* One PSLN-212/R848 animal is missing at day 10 without explanation, after 11.7% weight loss.
- *Impact:* Possible unreported adverse event in an R848 arm.
- *How handled here:* Supports deprioritising R848 combinations.
- *Remediation:* Report the animal fate.

**m10 (Minor) - Whole dataset.** *Evidence:* `annotation p.1; workbook metadata`

- *Finding:* Female mice only. Mn2+ content per dose, particle size, zeta potential and stability were measured but are not in the dataset. The workbook was last modified 2026-09-03.
- *Impact:* Translational gaps (sex, dose definition, CMC).
- *How handled here:* Listed as gaps in the next-step studies.
- *Remediation:* Provide the CMC data; confirm this is the latest data cut.


# Appendix B. Head-to-head statistics for all eligible endpoints (aged PSLN-344 vs PSLN-212)

| Block | Endpoint | Time | Scale | PSLN-212 | PSLN-344 | Young 212 | Effect (95% CI) | p (Welch) | p (exact MW) | FDR q | RI |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S01-A | Ifnb1 | 16h | log2 | 16.53 | 36.87 | 37.47 | 2.23x (1.85-2.69) | 9.6e-06 | 0.0079 | <0.001 | 0.98 |
| S01-A | Ifnb1 | 72h | log2 | 3.41 | 4.17 | 1.46 | 1.22x (0.75-1.99) | 0.33 | 0.22 | 0.348 | -0.24 |
| S01-D | Lung monocytes | d2 | linear % | 12.48 | 15.00 | 15.64 | +2.52 pp (-3.13 to +8.17) | 0.29 | 0.69 | 0.311 | 0.80 |
| S01-D | Lung monocytes | d4 | linear % | 16.72 | 30.56 | 32.22 | +13.84 pp (+8.13 to +19.55) | 0.0016 | 0.0079 | 0.004 | 0.89 |
| S01-D | Lung monocytes | d6 | linear % | 13.22 | 24.48 | 25.22 | +11.26 pp (+7.39 to +15.13) | 0.00016 | 0.0079 | <0.001 | 0.94 |
| S01-D | Lung monocytes | d8 | linear % | 9.66 | 18.44 | 14.08 | +8.78 pp (+7.21 to +10.35) | 1.3e-05 | 0.0079 | <0.001 | 1.99 |
| S01-E | Lung CD11b+ DC | d2 | linear % | 3.72 | 4.72 | 3.80 | +1.00 pp (-0.24 to +2.24) | 0.099 | 0.15 | 0.114 | 12.50 |
| S01-E | Lung CD11b+ DC | d4 | linear % | 8.28 | 18.88 | 21.40 | +10.60 pp (+0.07 to +21.13) | 0.049 | 0.0079 | 0.062 | 0.81 |
| S01-E | Lung CD11b+ DC | d6 | linear % | 7.80 | 15.38 | 12.98 | +7.58 pp (+2.49 to +12.67) | 0.012 | 0.0079 | 0.018 | 1.46 |
| S01-E | Lung CD11b+ DC | d8 | linear % | 6.04 | 13.68 | 9.48 | +7.64 pp (+4.25 to +11.03) | 0.0018 | 0.0079 | 0.004 | 2.22 |
| S01-F | Lung cDC1 | 72h | linear % | 22.80 | 37.52 | 43.42 | +14.72 pp (+6.12 to +23.32) | 0.0058 | 0.0079 | 0.010 | 0.71 |
| S01-G | Lung cDC2 | 72h | linear % | 75.30 | 59.46 | 54.08 | -15.84 pp (-24.18 to -7.50) | 0.0041 | 0.0079 | 0.007 | 0.75 |
| S02-A | CCR7+ migratory CD11b+ DC (lung) | 72h | linear % | 7.28 | 30.68 | 35.00 | +23.40 pp (+13.77 to +33.03) | 0.0019 | 0.0079 | 0.004 | 0.84 |
| S02-B | MLN CD11b+CD103- DC | 72h | linear % | 18.22 | 36.76 | 44.70 | +18.54 pp (+6.69 to +30.39) | 0.0075 | 0.016 | 0.012 | 0.70 |
| S02-C | MLN AF647-OVA+ DC | 36h | linear % | 1.77 | 7.09 | 9.39 | +5.32 pp (+3.59 to +7.05) | 0.00069 | 0.0079 | 0.002 | 0.70 |
| S02-D CD40 | CD40+ of MLN CD11b+ DC | d3 | linear % | 5.56 | 11.20 | 38.72 | +5.65 pp (+1.98 to +9.31) | 0.011 | 0.0079 | 0.016 | 0.17 |
| S02-D CD86 | CD86+ of MLN CD11b+ DC | d3 | linear % | 8.13 | 14.54 | 37.94 | +6.41 pp (+2.97 to +9.85) | 0.0032 | 0.0079 | 0.006 | 0.22 |
| S02-E | OT-I proliferation (DC co-culture) | 72h+3d | linear % | 0.77 | 18.65 | 26.24 | +17.89 pp (+14.38 to +21.40) | 0.0001 | 0.0079 | <0.001 | 0.70 |
| S02-F | Gm-csf (lung) | 16h | log2 | 1.42 | 5.99 | - | 4.21x (2.78-6.38) | 0.00051 | 0.0079 | 0.002 | - |
| S02-F | Gm-csf (lung) | 36h | log2 | 1.59 | 8.52 | - | 5.36x (3.93-7.32) | 3.8e-05 | 0.0079 | <0.001 | - |
| S02-F | Gm-csf (lung) | 72h | log2 | 1.37 | 3.61 | - | 2.63x (1.61-4.30) | 0.0036 | 0.0079 | 0.007 | - |
| S03-A | IgG CA09 H1N1 | d14 | log2 | 393 | 7,305 | 11,959 | 18.58x (9.11-37.87) | 1.3e-05 | 0.0079 | <0.001 | 0.86 |
| S03-C | HAI CA09 H1N1 | d14 | log2 | 45.95 | 368 | 485 | 8.00x (3.91-16.38) | 0.00037 | 0.0079 | 0.001 | 0.88 |
| S03-D | Neut CA09 H1N1 | d14 | log2 | 418 | 3,840 | 6,686 | 9.19x (3.10-27.20) | 0.0019 | 0.016 | 0.004 | 0.80 |
| S03-E | IgG Aichi H3N2 | d14 | log2 | 426 | 5,701 | 13,855 | 13.40x (6.07-29.57) | 7e-05 | 0.0079 | <0.001 | 0.75 |
| S03-G | HAI Aichi H3N2 | d14 | log2 | 34.82 | 320 | 368 | 9.19x (4.18-20.18) | 0.00021 | 0.0079 | 0.001 | 0.94 |
| S03-H | Neut Aichi H3N2 | d14 | log2 | 276 | 2,533 | 4,411 | 9.19x (3.83-22.07) | 0.00039 | 0.0079 | 0.001 | 0.80 |
| S03-K | MLN GC B cells | d7 | linear % | 2.34 | 6.54 | 9.82 | +4.20 pp (+2.33 to +6.08) | 0.0023 | 0.0079 | 0.005 | 0.56 |
| S03-L | Aicda | d5 | log2 | 3.33 | 11.56 | - | 3.47x (1.76-6.86) | 0.0073 | 0.1 | 0.012 | - |
| S03-L | E47 | d5 | log2 | 6.12 | 24.11 | - | 3.94x (1.96-7.93) | 0.0066 | 0.1 | 0.011 | - |
| S04-A | Tfh ICOS-hi | d7 | linear % | 3.82 | 10.26 | 13.63 | +6.44 pp (+2.57 to +10.31) | 0.0086 | 0.0079 | 0.014 | 0.66 |
| S04-A | Tfh ICOS-lo | d7 | linear % | 2.70 | 5.74 | 6.91 | +3.04 pp (+0.53 to +5.55) | 0.027 | 0.016 | 0.035 | 0.72 |
| S04-B Foxp3 | Tfr (Foxp3+ of CXCR5+ICOShi) | d7 | linear % | 26.66 | 10.80 | 7.12 | -15.86 pp (-24.03 to -7.69) | 0.0047 | 0.0079 | 0.008 | 0.81 |
| S04-C | Tfr (Foxp3+ of CXCR5+ICOShi) | d30 | linear % | 18.04 | 14.00 | 7.40 | -4.04 pp (-9.21 to +1.13) | 0.11 | 0.15 | 0.122 | 0.38 |
| S04-D | Lung Treg | d7 | linear % | 6.66 | 2.99 | 1.78 | -3.67 pp (-4.54 to -2.81) | 0.00034 | 0.1 | 0.001 | 0.75 |
| S05-D | Lung Ki-67+ CD8 | d3 | linear % | 3.48 | 9.38 | 9.94 | +5.90 pp (+3.57 to +8.23) | 0.00047 | 0.0079 | 0.002 | 0.91 |
| S05-E | Lung GZMB+ CD8 | d3 | linear % | 2.99 | 5.69 | 9.61 | +2.70 pp (+1.46 to +3.94) | 0.0011 | 0.0079 | 0.003 | 0.41 |
| S05-F | MLN IFNg+ CD8 (rgH5N1 restim) | d14 | linear % | 1.50 | 6.36 | 9.18 | +4.85 pp (+3.63 to +6.07) | 0.00013 | 0.0079 | <0.001 | 0.63 |
| S05-G | MLN IFNg+ CD8 (rgH5N1 restim) | d60 | linear % | 3.04 | 9.86 | 14.36 | +6.82 pp (+3.39 to +10.25) | 0.0032 | 0.0079 | 0.006 | 0.60 |
| S05-H | MLN GZMB+ CD8 | d60 | linear % | 1.02 | 4.11 | 5.55 | +3.08 pp (+1.71 to +4.45) | 0.0025 | 0.0079 | 0.005 | 0.68 |
| S05-I | Lung TRM CD8 | d25 | linear % | 1.00 | 3.96 | 6.04 | +2.96 pp (+2.18 to +3.74) | 6.2e-05 | 0.0079 | <0.001 | 0.59 |
| S07-A | Lung Ly6C+CCR2+ macrophages (x1e5) | d10 | log2 | 14.48 | 2.65 | - | 0.18x (0.06-0.60) | 0.024 | 0.1 | 0.033 | - |
| S07-A | Lung Ly6C+CCR2+ macrophages (x1e5) | d2 | log2 | 9.43 | 3.16 | - | 0.33x (0.13-0.86) | 0.033 | 0.1 | 0.042 | - |
| S07-A | Lung Ly6C+CCR2+ macrophages (x1e5) | d30 | log2 | 3.88 | 2.31 | - | 0.60x (0.23-1.54) | 0.18 | 0.2 | 0.194 | - |
| S07-A | Lung Ly6C+CCR2+ macrophages (x1e5) | d5 | log2 | 18.55 | 3.36 | - | 0.18x (0.10-0.32) | 0.0013 | 0.1 | 0.003 | - |
| S08-A | Ifnb1 dose-response 16h | 10ug | log2 | 8.92 | 20.98 | - | 2.35x (1.77-3.12) | 0.004 | 0.1 | 0.007 | - |
| S08-A | Ifnb1 dose-response 16h | 1ug | log2 | 1.36 | 1.38 | - | 1.01x (0.79-1.30) | 0.87 | 1 | 0.882 | - |
| S08-A | Ifnb1 dose-response 16h | 20ug | log2 | 12.51 | 45.52 | - | 3.64x (2.69-4.92) | 0.00033 | 0.1 | 0.001 | - |
| S08-A | Ifnb1 dose-response 16h | 40ug | log2 | 14.72 | 49.68 | - | 3.38x (2.23-5.12) | 0.0013 | 0.1 | 0.003 | - |
| S08-A | Ifnb1 dose-response 16h | 5ug | log2 | 4.04 | 8.17 | - | 2.02x (1.28-3.20) | 0.013 | 0.1 | 0.019 | - |
| S09-A panel1[A:U] | Ccl2 | 16h (as printed) | log10 (as stored) | 7.63 | 590 | 1,391 | 77.37x (16.75-357.42) | 0.0023 | 0.1 | 0.005 | 0.84 |
| S09-A panel1[A:U] | Ccl3 | 16h (as printed) | log10 (as stored) | 1.12 | 29.83 | 57.28 | 26.70x (9.96-71.59) | 0.00079 | 0.1 | 0.002 | 0.83 |
| S09-A panel1[A:U] | Ccl5 | 16h (as printed) | log10 (as stored) | 2.62 | 19.82 | 62.11 | 7.58x (1.82-31.56) | 0.025 | 0.1 | 0.034 | 0.64 |
| S09-A panel1[A:U] | Il10 | 16h (as printed) | log10 (as stored) | 3.71 | 7.31 | 1.84 | 1.97x (0.58-6.66) | 0.19 | 0.4 | 0.211 | -0.97 |
| S09-A panel1[A:U] | Il6 | 16h (as printed) | log10 (as stored) | 5.57 | 36.08 | 60.32 | 6.48x (1.60-26.18) | 0.021 | 0.1 | 0.029 | 0.78 |
| S09-A panel1[A:U] | Tnf | 16h (as printed) | log10 (as stored) | 15.71 | 40.49 | 13.88 | 2.58x (0.61-10.87) | 0.11 | 0.1 | 0.122 | -7.67 |
| S09-A panel2[X:AS] | Ccl2 | 72 h (printed "16h"; see M3) | log10 (as stored) | 5.23 | 27.41 | 102 | 5.24x (2.32-11.83) | 0.01 | 0.1 | 0.015 | 0.56 |
| S09-A panel2[X:AS] | Ccl3 | 72 h (printed "16h"; see M3) | log10 (as stored) | 4.73 | 9.23 | 41.45 | 1.95x (0.90-4.25) | 0.076 | 0.2 | 0.090 | 0.31 |
| S09-A panel2[X:AS] | Ccl5 | 72 h (printed "16h"; see M3) | log10 (as stored) | 1.21 | 2.01 | 0.55 | 1.66x (0.89-3.10) | 0.082 | 0.1 | 0.096 | -0.64 |
| S09-A panel2[X:AS] | Il10 | 72 h (printed "16h"; see M3) | log10 (as stored) | 4.18 | 4.16 | 0.11 | 1.00x (0.29-3.39) | 0.99 | 1 | 0.991 | 0.00 |
| S09-A panel2[X:AS] | Il6 | 72 h (printed "16h"; see M3) | log10 (as stored) | 1.86 | 7.19 | 3.10 | 3.85x (1.36-10.91) | 0.026 | 0.1 | 0.035 | 2.65 |
| S09-A panel2[X:AS] | Tnf | 72 h (printed "16h"; see M3) | log10 (as stored) | 5.23 | 8.44 | 0.48 | 1.62x (0.99-2.62) | 0.052 | 0.1 | 0.064 | -0.20 |
| S11-D | Lung NK cells | d2 | linear % | 28.82 | 34.02 | 23.14 | +5.20 pp (-0.09 to +10.49) | 0.053 | 0.056 | 0.065 | -0.92 |
| S11-D | Lung NK cells | d4 | linear % | 24.70 | 31.08 | 18.10 | +6.38 pp (-0.55 to +13.31) | 0.066 | 0.15 | 0.080 | -0.97 |
| S11-D | Lung NK cells | d6 | linear % | 21.76 | 23.88 | 17.60 | +2.12 pp (-3.52 to +7.76) | 0.41 | 0.42 | 0.422 | -0.51 |
| S11-D | Lung NK cells | d8 | linear % | 25.46 | 24.06 | 18.14 | -1.40 pp (-4.48 to +1.68) | 0.31 | 0.31 | 0.325 | 0.19 |
| S11-E | Lung CD206+ macrophages | not stated | linear % | 71.46 | 48.92 | 35.54 | -22.54 pp (-34.48 to -10.60) | 0.0024 | 0.0079 | 0.005 | 0.63 |
| S13-A | IgG2a CA09 H1N1 | d14 | log2 | 83.42 | 1,642 | 4,642 | 19.68x (10.05-38.54) | 1.1e-05 | 0.0079 | <0.001 | 0.74 |
| S13-B | IgG1 CA09 H1N1 | d14 | log2 | 153 | 887 | 1,855 | 5.79x (4.26-7.87) | 1e-06 | 0.0079 | <0.001 | 0.70 |
| S13-C | IgG2a Aichi H3N2 | d14 | log2 | 80.26 | 1,331 | 3,701 | 16.59x (8.57-32.10) | 9.9e-06 | 0.0079 | <0.001 | 0.73 |
| S13-D | IgG1 Aichi H3N2 | d14 | log2 | 173 | 579 | 1,326 | 3.35x (2.24-5.00) | 0.00014 | 0.0079 | <0.001 | 0.59 |
| S13-H | MLN IgG+ of B220+ | not stated | log2 | 11.03 | 25.31 | 26.85 | 2.29x (1.66-3.17) | 0.00038 | 0.0079 | 0.001 | 0.93 |
| S13-I | IgG CA09 H1N1 post-boost | d28 | log2 | 4,411 | 15,651 | 40,739 | 3.55x (1.50-8.41) | 0.01 | 0.032 | 0.016 | 0.57 |
| S13-J | IgG Aichi H3N2 post-boost | d28 | log2 | 1,086 | 12,435 | 43,472 | 11.45x (4.05-32.37) | 0.00076 | 0.0079 | 0.002 | 0.66 |
| S14-A H1N1 | MLN IFNg+ CD8 (H1N1 restim) | not stated | linear % | 3.14 | 11.02 | 13.70 | +7.88 pp (+4.59 to +11.17) | 0.00074 | 0.0079 | 0.002 | 0.75 |
| S14-A H3N2 | MLN IFNg+ CD8 (H3N2 restim) | not stated | linear % | 3.58 | 9.86 | 13.98 | +6.28 pp (+4.01 to +8.55) | 0.00033 | 0.0079 | 0.001 | 0.60 |

**Endpoints excluded from the decision family, with reasons:**

| Block | Endpoint | Time | Reason excluded from the decision family |
|---|---|---|---|
| S05-B | MLN NP366 tetramer+ CD8 | d3 | as S05-A |
| S05-B | MLN NP366 tetramer+ CD8 | d5 | as S05-A |
| S05-B | MLN NP366 tetramer+ CD8 | d7 | as S05-A |
| S01-D | Lung monocytes | d0 | baseline (day 0, pre-immunisation) balance check |
| S01-E | Lung CD11b+ DC | d0 | baseline (day 0, pre-immunisation) balance check |
| S07-A | Lung Ly6C+CCR2+ macrophages (x1e5) | d0 | baseline (day 0, pre-immunisation) balance check |
| S11-D | Lung NK cells | d0 | baseline (day 0, pre-immunisation) balance check |
| S04-B Tfh:Tfr | Tfh:Tfr | d7 | derived: equals (100-Foxp3%)/Foxp3% of S04-B Foxp3 -> not independent |
| S11-A | Lung alveolar macrophages | d0 | first two animals of every group/day identical to S11-B (AM vs neutrophils) -> compromised |
| S11-A | Lung alveolar macrophages | d2 | first two animals of every group/day identical to S11-B (AM vs neutrophils) -> compromised |
| S11-A | Lung alveolar macrophages | d4 | first two animals of every group/day identical to S11-B (AM vs neutrophils) -> compromised |
| S11-A | Lung alveolar macrophages | d6 | first two animals of every group/day identical to S11-B (AM vs neutrophils) -> compromised |
| S11-A | Lung alveolar macrophages | d8 | first two animals of every group/day identical to S11-B (AM vs neutrophils) -> compromised |
| S08-B | Encapsulation efficiency |  | formulation attribute, not an immune endpoint (reported separately) |
| S03-B | IgG2a/IgG1 CA09 H1N1 (as printed) | d14 | group labels rotated vs primary S13-A/B titres; ratio recomputed from S13 |
| S03-F | IgG2a/IgG1 Aichi H3N2 (as printed) | d14 | group labels rotated vs primary S13-C/D titres; ratio recomputed from S13 |
| S05-A | Lung NP366 tetramer+ CD8 | d3 | n=2/group; conditions contradictory (OVA vs bivalent); NP366-374 is H-2Db-restricted but BALB/c are H-2d |
| S05-A | Lung NP366 tetramer+ CD8 | d5 | n=2/group; conditions contradictory (OVA vs bivalent); NP366-374 is H-2Db-restricted but BALB/c are H-2d |
| S05-A | Lung NP366 tetramer+ CD8 | d7 | n=2/group; conditions contradictory (OVA vs bivalent); NP366-374 is H-2Db-restricted but BALB/c are H-2d |
| S09-A panel1[A:U] | Ifnb1 | 16h (as printed) | not independent: same animals as S01-A Ifnb1 (see M3) |
| S09-A panel2[X:AS] | Ifnb1 | 16h (as printed) | not independent: same animals as S01-A Ifnb1 (see M3) |
| S11-B | Lung neutrophils | d0 | see S11-A |
| S11-B | Lung neutrophils | d2 | see S11-A |
| S11-B | Lung neutrophils | d4 | see S11-A |
| S11-B | Lung neutrophils | d6 | see S11-A |
| S11-B | Lung neutrophils | d8 | see S11-A |

# Appendix C. Supporting files

| File | Contents |
|---|---|
| `analysis/tidy/values.csv`, `tte.csv`, `bw.csv` | Every extracted observation, with its workbook cell |
| `analysis/h2h_endpoints.csv` | Appendix B with exclusions and reasons |
| `analysis/survival_*.csv` | By group, pairwise, pooled (sets A–F), leave-one-out |
| `analysis/restoration_index.csv`, `biomarker_table.csv`, `moa_contrasts.csv`, `dose_response.csv`, `reactogenicity_s08d.csv` | Supporting analyses |
| `analysis/integrity_register.csv`, `bw_vs_tte.csv`, `audit_logs/` | Integrity audit and raw check outputs |
| `analysis/evidence_ledger.csv` | Every number quoted in the text → value, source block/cells, analysis script |
| `code/` (`run_all.sh` + scripts) | Full reproduction from the workbook (about 2 minutes) |
