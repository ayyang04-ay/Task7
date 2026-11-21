---
title: "PSLN intranasal STING-agonist adjuvant: portfolio review proposal"
subtitle: "Recommendation, evidence, mechanism, biomarkers, target population and gated next steps"
date: "1 November 2026"
---

**Data basis.** `psln_program_dataset.xlsx` (15 sheets; file metadata: last modified 2026-09-03) and `psln_program_annotation.pdf`. Every block was extracted with cell-level provenance and re-analysed. Each number in this document traces to a block ID (e.g. S03-C) and an analysis output (e.g. `h2h.csv`). The full trail is in the evidence ledger (`analysis/evidence_ledger.csv`, [[ledger_n]] entries). Every table and figure can be regenerated with `code/run_all.sh`.

**Terminology.** *PSLN-344* = CDN-1807 in the surfactant-biomimetic liposome **with** Mn2+. *PSLN-212* = the same drug and vehicle **without** Mn2+. "Aged" = 20-month-old female BALB/c mice unless stated. "Young" = 7–8 weeks. *RI* (restoration index) = (PSLN-344 − aged PSLN-212) / (young PSLN-212 − aged PSLN-212): the fraction of the age-related deficit that Mn2+ closes (0 = none, 1 = young level). *pp* = percentage points.

# 1. Recommendation

> **KEEP the program. Advance PSLN-344 as the single lead. Stop developing PSLN-212 (keep it only as the Mn-free control in studies).**
>
> **Make this a gated keep, not an IND commitment.** Fund only what is needed to pass Gate A (data-integrity verification, end of January 2027) and Gate B (blinded confirmatory efficacy and Mn2+/CNS safety, October 2027). The kill criteria are fixed in advance (Section 7.3).

**How the asset looks, in one paragraph.** Scientifically, PSLN-344 has a large, consistent signal with a mechanistic explanation. In aged mice it is the only formulation we have tested that protects: pooled survival after lethal influenza challenge was [[arm_p344]] vs [[arm_p212]] for PSLN-212 and [[arm_sham]] for sham-adjuvanted vaccine (young mice with PSLN-212: [[arm_young]]). As a data package, however, it is **not yet investment-grade**. I found 4 critical and 8 major data-integrity problems that the committee would find if it checked (Section 3). None of them reverses the conclusion, but the exact magnitudes cannot be relied on until the source data are verified and the key experiment is repeated blind.

**Why keep (the evidence):**

1. **Survival, head-to-head.** Across all 14 aged or middle-aged strata, [[h2h_344]] PSLN-344 vs [[h2h_212]] PSLN-212 animals survived. The difference is [[h2h_rd]] pp (95% CI [[h2h_rd_ci]]); stratified hazard ratio [[h2h_hr]]. The point estimate favours PSLN-344 in [[h2h_strata]] strata. In the worst-case reconstruction of the record the difference is still [[sensC]] (Table 3).
2. **Breadth of the signal.** Of [[n_endpoints]] independent immune endpoints with both aged arms, [[n_sig]] differ at FDR<5% ([[n_sep]] with no overlap between individual animals). Every one of them that has a young benchmark moved toward the young level ([[n_sig_young]]); none moved away (Appendix B).
3. **Antibody titres close to young levels.** HAI GMT against CA09 H1N1 was [[hai1_344]] vs [[hai1_212]] (young: [[hai1_Y]]; RI [[hai1_ri]]). Against Aichi H3N2 it was [[hai3_344]] vs [[hai3_212]] (young: [[hai3_Y]]; RI [[hai3_ri]]) (S03-C/G).
4. **Protection where older adults need it most.** PSLN-344 protected against heterosubtypic challenge (H3 vaccine → H1 virus), H5N1 (wild-type VN04 two days after one dose: [[S03-J_344]] vs [[S03-J_212]]; S03-J does not state age, so it counts as aged under the annotation's convention), rapid-onset challenge (days 2–3: [[rapid]]) and challenge at day 60 ([[d60_344]] vs [[d60_212]]).
5. **A coherent, partly causal mechanism.** Mn2+ raises IFN-β and GM-CSF in the aged lung. This drives CCR2-dependent monocyte recruitment and IFNAR/GM-CSF-dependent monocyte-derived DC (moDC) differentiation, DC migration and priming, Tfh/germinal-centre responses, and CD8/resident-memory immunity. Several links are proven by loss- or gain-of-function experiments (Section 4).
6. **The benefit is age-specific.** In young mice, PSLN-212, PSLN-344 and even a cGAMP liposome all protect fully (S09-B/D/F, S13-E). The product's differentiation therefore lies in older adults, which is where the unmet need is (Section 6).

**Why only a conditional keep:**

1. **Data integrity** (Section 3). Examples: survival experiment S06-D is an exact copy of S06-C; body-weight trajectories are recycled between experiments, including the C57BL/6 and Swiss Webster "strain generality" studies; several survival records contradict their own body-weight records; and [[untreated_deaths]] of unvaccinated, *unchallenged* aged controls died within 14 days.
2. **Mn2+ intranasal safety is essentially untested.** The only data point is one 36-h CNS cytokine readout, which showed no signal (S10-A). We have no Mn dose per vial, no biodistribution and no olfactory-bulb exposure data. External literature describes olfactory transport of intranasal Mn to the brain.
3. **Rejuvenation is partial in the compartments that govern durability.** DC co-stimulation RI is [[ri_costim]], CD8 memory RI [[ri_cd8mem]] and post-boost antibody RI [[ri_boost]]. In matched designs, PSLN-344 survival was [[d14_vs_d60]] when challenge moved from day 14 to day 60.
4. **Missing commercially decisive evidence.** There is no comparator representing today's standard of care for older adults, no lung viral load, no mucosal IgA, female mice only, and no ferret or non-human-primate data.

**Decision asked of the committee today:**

- **Approve Gate A**: independent source-data verification, November 2026 – January 2027.
- **Approve the no-regret work that can start now**: Mn and CDN-1807 content per dose, particle characterisation, stability set-down, a human STING-variant potency screen, and a freedom-to-operate review of Mn2+–cyclic-dinucleotide formulations.
- **Approve immediate ordering of 20–22-month-old animals.** Aged-animal supply is the critical path for Gate B.
- **Pre-approve the Gate B package (Section 7), contingent on Gate A passing.**

# 2. How the two assets compare

**Table 1. Aged-mouse head-to-head on the decision-relevant endpoints.** Titres and qPCR: geometric means; cells: arithmetic means; n = 5 per group unless stated. Full statistics for all endpoints are in Appendix B.

[[TABLE1]]

*Notes.* Effects: geometric mean ratio (×) or mean difference (pp) with Welch 95% CI. q: Benjamini–Hochberg FDR across the [[n_endpoints]] independent endpoints. The survival row pools the aged arms of S03-I, S03-J, S06-A/B/C/E/F/G and S15-L/N (S06-D excluded as a duplicate). PSLN-344 vs young PSLN-212 survival: [[p344_vs_young]] (Newcombe CI). Source tables: `h2h.csv`, `survival_pooled_arms.csv`, `reactogenicity_s08d.csv`.

![Figure 3. Effect of Mn2+ along the immune cascade (A) and fraction of the age gap closed (B).](figures/fig3_cascade_restoration.png)

**Table 1b. How much of the young–aged deficit Mn2+ closes, by layer** (`restoration_index.csv`; RI per endpoint with bootstrap CIs in the file).

[[TABLE4]]

**Reading the comparison:**

- **PSLN-212 is active in aged mice but not enough to protect.** Versus sham it raises CA09 IgG about 7-fold (GMT [[igg_212]] vs [[igg_sham]]) and HAI about 6-fold ([[hai1_212]] vs [[hai1_sham]]). Yet survival was [[arm_p212]] vs [[arm_sham]].
- **Mn2+ is what converts immunogenicity into protection in the aged host.**
- **Where Mn2+ falls short.** Restoration is near-complete for innate cytokines (median RI [[ri_innate]]), myeloid recruitment (RI [[ri_myeloid]]) and d14 antibody (RI [[ri_ab]]). It is poor for DC co-stimulation: CD86 [[cd86_344]]% vs young [[cd86_Y]]%; CD40 [[cd40_344]]% vs [[cd40_Y]]% (RI [[cd86_ri]]/[[cd40_ri]]). It is partial for CD8 memory and post-boost titres (RI [[ri_cd8mem]] and [[ri_boost]]). These gaps are the main efficacy risk for durability in humans and are built into the next-step endpoints.
- **Th1 skew.** PSLN-344 induces a Th1-skewed response: IgG2a/IgG1 [[th1_h1_344]] vs [[th1_h1_212]] (H1) and [[th1_h3_344]] vs [[th1_h3_212]] (H3), against young [[th1_h1_Y]]/[[th1_h3_Y]]. These ratios are recomputed from the primary subclass titres (S13-A–D). The printed quotient blocks S03-B/F carry rotated labels and, read as printed, would wrongly suggest a Th2 skew (integrity finding M1).
- **Reactogenicity signal to monitor.** PSLN-344 vs PSLN-212 differences in Tnf and Il10 are not significant at FDR 5%. Compared with young animals, however, aged lungs given PSLN-344 overshoot for Tnf and keep both cytokines raised at 72 h (nominal, unadjusted p-values below). At 16 h, Tnf was [[tnf16_344]]× vs young [[tnf16_Y]]×. At 72 h it was [[tnf72_344]]× vs [[tnf72_Y]]× (p=[[tnf72_p_vsY]]), and Il10 [[il1072_344]]× vs [[il1072_Y]]× (p=[[il1072_p_vsY]]) (S09-A; the second panel is the 72-h timepoint, finding M3). Body-weight loss after vaccination was small (nadir [[nadir_344]] vs [[nadir_212]]; [[nadir_p]]; S08-D).

**Table 2. Survival by experiment (survivors/animals).**

[[TABLE2]]

![Figure 1. Head-to-head survival by experiment and pooled, including integrity sensitivity analyses.](figures/fig1_survival_forest.png)

**Table 3. Pooled PSLN-344 vs PSLN-212 survival and sensitivity to the integrity findings.**

[[TABLE3]]

*Leave-one-experiment-out:* the difference ranges [[loo_range]]. Stratified log-rank χ² = [[h2h_chi2]] and Cox HR [[h2h_hr]] were reproduced independently in R (`strat.R`). Log-rank was not computed for set C, which uses count overrides.

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
- **C2 – recycled body-weight trajectories.** The "vaccine + PSLN-344" arm of S15-I equals the PSLN-344 arm of S15-C for [[s15i_copy]] values (days 2–12). Young BALB/c PSLN-344 animals (S09-E) reappear as young C57BL/6 PSLN-212 animals (S15-M). Aged BALB/c PSLN-344 animals (S15-A) reappear in the C57BL/6 and Swiss Webster blocks (S15-M, S15-O). In total, [[fp_total]] high-precision values recur in the workbook; [[fp_bw]] of them are body weights shared between different experiments or arms.
- **C3 – survival records that contradict their own body weights.** S03-I lists all 7 PSLN-212 deaths by day 6, while S13-F shows three of those animals recovering to 95–99% body weight. S03-J lists 9/10 sham deaths, while S13-G shows four sham animals back to ≥99.7%. S06-E and S06-G have similar conflicts.
- **C4 – deaths in unchallenged controls.** [[untreated_deaths]] of unvaccinated, unchallenged aged controls died within 14 days, at flat body weight. In S06-G, PSLN-344 survival ([[S06-G_344]]) equals unchallenged-control survival ([[S06-G_untr]]).

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
| PSLN-344 outperforms PSLN-212 in aged mice | [[n_sig]]/[[n_endpoints]] endpoints at FDR<5%; [[h2h_strata]] strata; worst case [[sensC]] | **High** | Magnitudes pending source-data verification |
| Near-young antibody titres in aged mice | HAI RI [[hai1_ri]]/[[hai3_ri]] (S03-C/G), n=5 | Moderate–high | One experiment per antigen; not replicated |
| Cross-subtype and H5N1 protection in aged mice | S06-A/C/E/F/G, S03-J | Moderate | Several blocks carry survival vs body-weight conflicts (C3) |
| Rapid onset (day 2–3) | S03-J, S06-B ([[rapid]]) | Moderate | S06-D duplicate (C1); S03-J conflict (C3) |
| Protection at day 60 in aged mice | S06-E/F/G ([[d60_344]]) | Moderate–low | Conflicts (C3); unchallenged-control deaths (C4) |
| Works across mouse strains | S15-L/N | **Low** | Challenge not stated; recycled body weights (C2, M7) |
| Rapid protection needs antigen | S15-H | **Low** | Recycled body weights (C2) |
| MoA: IFN/GM-CSF → CCR2 monocytes → moDC → migration and priming | S02-H, S02-G, S07-B, S02-I, S02-C/E, S05-C | Moderate | STING dependence and link to protection untested |
| Safety: no CNS inflammation; mild weight loss | S10-A; S08-D | Low–moderate | One 36-h timepoint; no Mn biodistribution; S08-D may contain recycled values (C2) |

# 4. Mechanism of action (built from our data)

![Figure 5. Mechanism of action with the evidence type for each link.](figures/fig5_moa.png)

**Table 4. Interventional (causal) evidence.** All experiments used PSLN-344 (or PSLN-212 where stated).

[[TABLE5]]

**The mechanism in eight steps.** Confidence is given for each step.

1. **Delivery.** The surfactant-biomimetic vehicle is taken up by alveolar macrophages through SP-A/D: alveolar-macrophage uptake went from wild type to SP-A/D knockout as [[spad]] (S01-C). It also loads type II alveolar epithelium (S01-B). Confidence: high for vehicle targeting. The S08-C finding that Mn2+ lowers epithelial uptake is low confidence (M6).
2. **Mn2+ potentiates STING signalling in the aged lung.** Lung Ifnb1 at 16 h was [[ifnb_344]]× vs [[ifnb_212]]× (young: [[ifnb_Y]]×; RI [[ifnb_ri]]). In dose–response, Mn2+ mainly raises the ceiling (Emax [[emax344]]× vs [[emax212]]×) rather than potency (ED50 [[ed50_344]] vs [[ed50_212]] µg). The result is [[dose_sparing]] (S08-A), and going from 20 to 40 µg adds only [[plateau]]. Confidence: moderate. STING dependence itself has not been tested, and no Mn-only control exists.
3. **Paracrine amplification.** The gap-junction blocker carbenoxolone cut monocyte recruitment ([[cbx]]; S11-C). This is consistent with transfer of cyclic dinucleotide to bystander cells, but carbenoxolone has off-target effects. Confidence: moderate-low.
4. **Chemokines, GM-CSF and CCR2 monocytes.** At 16 h, Ccl2 was [[ccl216_344]]× vs [[ccl216_212]]×, Ccl3 [[ccl316_344]]× vs [[ccl316_212]]× and Il6 [[il616_344]]× vs [[il616_212]]× (S09-A). Gm-csf at 36 h was [[gmcsf_344]]× vs [[gmcsf_212]]× (S02-F). Lung monocytes at day 4 were [[mono_344]]% vs [[mono_212]]% (young [[mono_Y]]%; S01-D). A CCR2 antagonist removed most of this: monocytes [[ccr2mono]] and Ly6C+ macrophages [[ccr2mac]] (S07-B), and downstream lung GZMB+ CD8 [[ccr2cd8]] (S02-I, young). Confidence: high for CCR2 dependence of recruitment.
5. **moDC differentiation needs both type I IFN and GM-CSF.** Without IFNAR, bone marrow yielded few moDC ([[ifnar]]). GM-CSF partly rescued this ([[gmrescue]]; S02-H). Adding GM-CSF to PSLN-212 more than doubled moDC-like cells ([[gmgof]]; S02-G). **Interpretation:** the aged-lung defect with PSLN-212 is insufficient GM-CSF, and Mn2+ supplies it. Without Mn2+, monocytes instead accumulate as Ly6C+CCR2+ macrophages ([[ly6c5_212]] vs [[ly6c5_344]] ×10^5 at day 5, S07-A). M2-like CD206+ macrophages fall from [[cd206_212]]% to [[cd206_344]]% (S11-E; timepoint not stated). Confidence: moderate-high (two independent loss/gain experiments).
6. **DC migration and priming.** CCR7+ migratory DC were [[ccr7_344]]% vs [[ccr7_212]]% (S02-A; RI [[ccr7_ri]]). Pertussis toxin reduced antigen+ DC in the MLN ([[ptxdc]]) and MLN priming ([[ptxoti]] ex vivo; [[ptxmln]] in vivo), but not lung priming ([[ptxlung]]; S05-C). So PSLN-344 primes both in the draining node and locally in the lung. Co-stimulation stays low (RI [[ri_costim]]). Confidence: high for migration dependence.
7. **Tfh and germinal centre.** ICOS-hi Tfh were [[tfh_344]]% vs [[tfh_212]]% (S04-A), Tfr [[tfr_344]]% vs [[tfr_212]]% (S04-B) and germinal-centre B cells [[gc_344]]% vs [[gc_212]]% (S03-K). Together these give Th1-skewed, neutralising antibody (Table 1). Confidence: moderate (correlative).
8. **CD8 effector and resident memory.** IFN-γ+ CD8 were [[ifng14_344]]% vs [[ifng14_212]]% at day 14 and [[ifng60_344]]% vs [[ifng60_212]]% at day 60 (S05-F/G). Lung TRM at day 25 were [[trm_344]]% vs [[trm_212]]% (S05-I). These responses cross-react with H1, H3 and H5 antigens (S05-F, S14-A), which is the plausible basis of heterosubtypic protection. Confidence: moderate (correlative; no depletion-challenge experiment).

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

[[TABLE6]]

**How to use them:**

- **Tier 1, pharmacodynamic (hours–days).** Markers: IFN-β/ISG, CXCL10, CCL2, IL-6 and GM-CSF in nasal lining fluid and serum.
  - *Why:* Ifnb1 is dose-responsive (S08-A) and fully restored in aged mice (RI [[ifnb_ri]]).
  - *Use:* target engagement and dose selection in Phase 1.
  - *Gap:* we have lung tissue only. Study B4 must show that BAL, nasal-wash and serum levels track lung levels.
  - *Safety read:* TNF/IL-10 still raised at 72 h is the reactogenicity flag ([[tnf72_344]]× vs young [[tnf72_Y]]×).
- **Tier 2, cellular (days 3–10).** Markers: circulating Tfh (ICOS+PD-1+CXCR5+) and the cTfh:cTfr balance at day 7, plus day-7 plasmablasts.
  - *Why:* ICOS-hi Tfh and Tfr gave complete separation (S04-A/B), and circulating Tfh are measurable in blood.
  - *Use:* early go/no-go in the ≥65 cohort, well before titres peak.
- **Tier 3, efficacy surrogates (days 14–28).** Markers: HAI GMT and seroconversion, microneutralisation, nasal IgA (not yet measured, a gap) and IFN-γ ELISpot against conserved NP/M1 peptides.
  - *Candidate protective threshold, to be tested:* HAI ≥1:160. Animals reaching ≥1:160 (S03-C): [[hai160]]. In the matched survival experiment (S03-I), both groups in which every animal reached it survived 7/7; the others survived at most 3/7 (CMP-204 [[S03-I_cmp]], PSLN-212 [[S03-I_212]], sham [[S03-I_sham]]).
  - *Caveat:* PSLN-212 animals all reached the conventional ≥1:40 yet survived 0/7. This is group-level evidence from different animals, and S03-I carries integrity flags (M8). B1 measures titres and survival in the *same* animals to test the threshold properly.
- **Tier 4, durability (days 25–180).** Markers: IFN-γ ELISpot and nasal resident-memory T cells.
  - *Why:* heterosubtypic survival followed the T-cell rank order. TRM: sham [[trm_sham]]%, PSLN-212 [[trm_212]]%, PSLN-344 [[trm_344]]%, young [[trm_Y]]%. Day-60 heterosubtypic survival: sham [[d60_sham]], PSLN-212 [[d60_212]], PSLN-344 [[d60_344]], young [[d60_young]].
  - *Caveat:* every candidate marker has the same rank order (sham < PSLN-212 < PSLN-344 < young). The current design therefore **cannot say which marker is mechanistic**. The antibody-transfer and CD8-depletion arms of B4 are designed to answer that.
- **Safety biomarkers.**
  - Serum Mn.
  - Olfactory function (smell test).
  - CNS-proximal signals in animals: olfactory-bulb Mn, Ifnb1/Tnf/Isg15. In S10-A, CNS Ifnb1 went from sham to PSLN-344 as [[cns_ifnb]], and from sham to cholera toxin as [[ct_ifnb]].

# 6. Target demographic (for the market-research TAM check)

I do not estimate TAM here: it cannot be derived from our data. Below are segment definitions, the evidence for each, and the parameters market research needs to source.

**Primary segment: adults ≥65 years, seasonal influenza, annual intranasal dose.**

- *Evidence:* in 20-month-old mice only PSLN-344 protects ([[arm_p344]] vs [[arm_p212]]). In young mice Mn2+ adds little: both young arms survived 8/8 in S09-B/D/F, and Ifnb1 went from young PSLN-212 to young PSLN-344 as [[young_ifnb]].
- *Age mapping (external):* 18–24-month mice correspond roughly to humans in their late 50s to late 60s.
- *Value claims to test:*
  - needle-free, one dose;
  - near-young HAI (RI [[hai1_ri]]–[[hai3_ri]]);
  - cross-subtype T-cell protection for mismatch seasons;
  - Th1-skewed antibody.

**Secondary segment, conditional on Study B1: adults 50–64, particularly with chronic conditions.**

- *Evidence:* in 14-month-old naive mice, PSLN-212 already failed ([[S06-Eimp_Naive212]] and [[S06-Fimp_Naive212]]) while PSLN-344 protected ([[S06-Eimp_Naive344]], [[S06-Fimp_Naive344]]). The age-related failure therefore begins in middle age.
- *Imprinting:* prior infection did not reduce PSLN-344 protection ([[S06-Eimp_Imprinting344]], [[S06-Fimp_Imprinting344]]). This is relevant to an adult population with pre-existing immunity.

**Tertiary segment: pandemic preparedness (H5), via government stockpiles.**

- *Purchasers and recipients:* governments; all adults, with older adults prioritised.
- *Evidence:* against wild-type H5N1 two days after one dose, survival was [[S03-J_344]] vs [[S03-J_212]] (sham [[S03-J_sham]]). Against rgH5N1 in aged mice, after a bivalent H1/H3 vaccine (i.e. cross-subtype), it was [[S06-C_344]] at day 14 and [[S06-F_344]] at day 60. Young mice were protected at day 180 ([[S09-F_344Y]]).
- *Not yet tested:* antigen sparing (Study B3), which is what governments buy on.

**Exploratory segment: outbreak response in long-term-care settings.**

- *Evidence:* rapid onset ([[rapid]] survivors at days 2–3).
- *Open question:* whether the adjuvant alone protects. The only test (S15-H: [[S15H_adj]] alone vs [[S15H_combo]] with vaccine) carries an integrity flag.

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
- **E6.** Durability beyond 60 days in aged animals and the role of a boost (B1 durability cohort). Current data: [[d60_344]] at day 60, and post-boost RI [[ri_boost]].
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
  - CMC: Mn and CDN-1807 per dose (ICP-MS/HPLC); encapsulation efficiency (PSLN-212 → PSLN-344: [[ee]], S08-B); size, PDI, zeta and free Mn; lyophilised stability under ICH conditions (−20 °C, 2–8 °C, 25 °C); in-vitro IFN reporter release assay;
  - human STING haplotypes (WT, HAQ, R232H, AQ, R293Q) ± Mn2+.
- **Readout / timing:** Dec 2026 – Jul 2027; 6-month stability data by Jul 2027.
- **n / power:** 10/arm (9 per arm detects a 2-fold GMT difference at 80% power, using within-group SD 0.68 log2 from S03-C/G).
- **Go criteria:** minimal dose achieving ≥90% of maximum HAI; ≥6-month stability; activity across common human STING haplotypes. HAI has never been dose-ranged. The only dose data are Ifnb1 (S08-A), where 10 µg gives [[ifnb_10_vs_20]] of the 20-µg response and 40 µg adds only [[plateau]], which puts the plateau near 20 µg.

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

1. **The only formulation in the portfolio that protects aged animals:** [[arm_p344]] survival vs [[arm_p212]] (PSLN-212) and [[arm_sham]] (sham). This is the program's entire differentiation for the ≥65 market. Without Mn2+, CDN-1807 does not protect aged mice.
2. **Near-young antibody in the aged host.** HAI GMT [[hai1_344]] vs young [[hai1_Y]]. All 5 PSLN-344 animals reached ≥1:160, against none of 5 with PSLN-212.
3. **Breadth that matters for mismatch seasons and pandemics:**
   - heterosubtypic protection (S06-A [[S06-A_344]] vs [[S06-A_212]]; S06-G at day 60 [[S06-G_344]] vs [[S06-G_212]]);
   - H5N1 protection (wild-type, day 2: [[S03-J_344]] vs [[S03-J_212]]; rgH5N1 at day 60 [[S06-F_344]] vs [[S06-F_212]]);
   - rapid onset ([[rapid]]).
4. **A mechanistic explanation of *why* the aged lung fails** (insufficient GM-CSF/IFN for moDC differentiation) and a way to fix it. This may be reusable for other respiratory vaccines for older adults, but that is untested option value.
5. **Time.** Re-creating an aged-population adjuvant would, at best, restart at the equivalent of Gate B.

**The objective case for dropping:**

1. **Integrity.** Four critical findings. If Gate A fails, every magnitude in this document must be re-earned, and the recycled data are a governance risk in their own right.
2. **Mn2+ neurotoxicity risk.** Intranasal Mn is transported along the olfactory nerve in animals (external literature). Our CNS data are a single 36-h cytokine panel in 5 mice per group, with no Mn measurement.
3. **Intranasal-adjuvant regulatory history.** An intranasal toxin-adjuvanted influenza vaccine was withdrawn over facial-nerve palsy (external). STING agonists can provoke systemic inflammation, and we already see Tnf/Il10 persisting in aged lungs at 72 h.
4. **Incomplete rejuvenation.** Co-stimulation RI [[ri_costim]]; memory RI [[ri_cd8mem]]; a trend to lower survival at day 60. PSLN-344 may not beat entrenched enhanced IM vaccines in people.
5. **Translation and market risk.** Mouse-only and female-only data; human STING polymorphism; no ferret or NHP data; crowded ≥65 market; prior art on Mn–CDN particles.

**Net judgement.** Every one of these risks is testable within the Gate A–B window (November 2026 – October 2027, Section 7), at a cost that is small relative to IND-enabling spend. The efficacy signal is too large and consistent to discard on untested risks. If Gate A or B fails on the pre-specified criteria, the recommendation flips to **stop**, and this section is the record of what we knowingly gave up.

# 9. What I considered and ruled out

**Asset options:**

- **Advance PSLN-212, or both in parallel.** Ruled out.
  - In aged mice PSLN-212 is further from the young benchmark than PSLN-344 on every significant endpoint that has a benchmark ([[n_sig_young]]), and survival is [[arm_p212]] vs [[arm_p344]].
  - It offers no advantage in young mice (8/8 survivors in both arms in S09-B/D/F).
  - It shows no safety advantage (weight nadir [[nadir_212]] vs [[nadir_344]], p=0.56).
  - Its only theoretical advantage is absence of Mn2+. But if Mn fails B2, PSLN-212 still would not protect aged animals, so it is not a real fallback for ≥65.
  - Kept only as the Mn-free control.
- **R848 combinations (PSLN-R848, PSLN-212/R848, PSLN-344/R848).** Ruled out.
  - PSLN-212/R848 gave lower Ifnb1 than PSLN-344 ([[r848_ifnb]]) and higher Tnf/Il10 (S09-A).
  - It caused more weight loss (mean nadir [[nadir_r848]] vs PSLN-344 [[nadir_344]], [[nadir_p_r848]]; maximum individual loss [[maxloss_r848]]), with one unexplained missing animal at day 10 (S08-D).
  - PSLN-344/R848 is undefined in Materials and has a lower ceiling than PSLN-344 (Emax [[emax_r848]] vs [[emax344]]; S08-A).
- **cGAMP liposome (CMP-204).** Ruled out. Ifnb1 went from PSLN-212 to CMP-204 as [[cmp_ifnb]]. Day-14 titres were [[cmp_vs212]] lower than PSLN-212 and [[cmp_vs344]] lower than PSLN-344 (six titre endpoints, S03-A/C/D/E/G/H). This also supports CDN-1807 as our differentiating drug.
- **Adjuvant alone as a non-specific antiviral prophylactic.** Not supported: PSLN-344 alone gave [[S15H_adj]] survivors at day 3 (S15-H). The block carries an integrity flag, so this is retested in B1.
- **All-ages or young-adult indication.** Ruled out as the lead. There is no differentiation in young animals, and a licensed intranasal vaccine already serves young adults (external).

**Decision options:**

- **Kill now.** Ruled out. The effect is large (worst case [[sensC]]), consistent ([[h2h_strata]] strata; [[n_sig_young]] benchmarked endpoints moved toward young) and mechanistically explained, and the integrity questions can be tested cheaply.
- **Full go to IND-enabling work now.** Ruled out. There are critical integrity findings, no Mn/CNS data, no SOC comparator and no large-animal data.

**Analytical choices:**

- **Naive pooling of survival across experiments.** Rejected because challenge strains and timings differ. I used stratified analyses (Mantel–Haenszel, stratified log-rank, stratified Cox).
- **Sato variance CIs.** Rejected because they exceeded 100% in sparse subsets. I used Newcombe intervals; with balanced arms the Mantel–Haenszel difference equals the crude difference.
- **ANOVA/Tukey on raw titres, as in the stated methods.** Rejected because titres are log-normal. I used log-scale Welch tests with BH-FDR, and exact Mann–Whitney as a sensitivity check. Conclusions are unchanged: [[n_sig]] endpoints significant, [[n_sep]] of them with complete separation of the per-animal values.
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
- Multiplicity: Benjamini–Hochberg across [[n_endpoints]] independent endpoints. Excluded from the family: day-0 baselines (no pre-treatment imbalance, all p>0.13), derived metrics, duplicated or non-independent blocks and compromised blocks.

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

[[TABLE7]]

# Appendix B. Head-to-head statistics for all eligible endpoints (aged PSLN-344 vs PSLN-212)

[[TABLE8]]

**Endpoints excluded from the decision family, with reasons:**

[[TABLE9]]

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
