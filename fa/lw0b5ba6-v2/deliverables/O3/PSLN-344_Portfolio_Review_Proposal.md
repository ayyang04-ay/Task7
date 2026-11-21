---
title: "PSLN-344 / PSLN-212 intranasal STING-agonist adjuvant: portfolio review proposal"
subtitle: "Recommendation, evidence, mechanism, biomarkers, target demographic and gated next steps"
date: "1 November 2026"
---

**Sources:** `psln_program_dataset.xlsx` (15 sheets, last modified 3 Sep 2026) and `psln_program_annotation.pdf` (per-block annotation, 15 Sep 2026). These are the only data used. Each number below gives its source block (e.g. **S03-C**) and the analysis behind it. Exact cell ranges are in `tables/T1`–`T7` and `A1`, and every analysis can be re-run from `code/`. Outside literature appears only as labelled context (Appendix D). It is never used as evidence.

**Terms.** *Aged* = female BALB/c mice aged ≥20 months, unless a block says otherwise. *Young* = 7–8 weeks old. *PSLN-212* = surfactant-biomimetic liposome carrying CDN-1807. *PSLN-344* = the same liposome with Mn²⁺ added by coordination polymerisation. *Sham* = vaccine plus empty liposome. *Restoration* = how far aged PSLN-344 closes the gap between the floor (sham or aged PSLN-212) and young PSLN-212: 0% means no change, 100% means it reaches the young level.

# 1. Recommendation

> **Keep PSLN-344 in the portfolio as the lead asset and stop developing PSLN-212 as a candidate.** Keep PSLN-212 as the internal comparator and as the Mn-free fallback.
>
> **The recommendation is conditional.** Before any IND-enabling money is spent, two short gates must be passed:
>
> * **Gate 0 (about 8 weeks):** a source-data integrity audit.
> * **Gate 1 (primary readout about 6 months after approval; day-60 cohort about month 8):** an independent, blinded, pre-registered confirmatory study in aged mice against a clinically relevant benchmark.
>
> The biology justifies keeping the asset. The condition of the dataset means we should not yet commit further.

**Why keep PSLN-344.** It is the only preparation in our data that protects aged animals.

| What the committee will ask | Answer from our data | Source / analysis |
|------------------|-------------------------------------------------------|----------------------|
| Is PSLN-344 better than PSLN-212 where it matters (aged)? | Yes, on all 43 immune readouts that passed the integrity checks. 41 are nominally significant and 32 survive Holm correction. | T1; Welch t-tests on log scale for titres and fold-changes, exact Mann-Whitney, ANOVA with Tukey |
| Does it protect aged animals? | Mortality was **24% vs 90%** for PSLN-212 (10/42 vs 38/42) and 100% for sham across six heterosubtypic challenge studies. Mantel-Haenszel (MH) risk ratio (RR) 0.26 (95% CI 0.15–0.45). In the most conservative 5-study set: **29% vs 94%**, RR 0.30 (0.18–0.51) | S06-A,B,C,E,F,G; MH stratified by study; stratified Cox model |
| Does it restore young-like immunity? | For functional antibody, largely yes. HAI is **368 vs 46** (CA09) and **320 vs 35** (Aichi), against 485 and 368 in young mice. HAI and neutralisation in aged PSLN-344 mice are statistically indistinguishable from young PSLN-212 (GMT ratios 0.57–0.87, p = 0.18–0.61, n=5). Binding IgG is 0.41–0.61× the young level. CD8 effector and memory readouts are 55–79% restored. | S03-A–H; T1 restoration index; Welch t-test on log2 scale |
| Is it specific, fast and durable? | Protection needs the antigen: PSLN-344 alone gave 7/7 deaths vs 1/7 with vaccine (S15-H). It works when challenge comes **3 days** after vaccination (2/7 vs 7/7 deaths; S06-B). It lasts to **day 60** (7/21 vs 20/21; S06-E,F,G). It protects across subtypes. | Fisher exact test; MH |
| Is there a safety red flag so far? | None seen. Weight nadir 96.4% vs 98.2% for vaccine alone (p=0.065; S08-D). No CNS Ifnb1/Tnf/Isg15 induction at 36 h (PSLN-344/sham Ifnb1 1.14×, 95% CI 0.69–1.86). The cholera-toxin control gave 5.4× (S10-A). | Welch t-test; ANOVA with Tukey |
| Is PSLN-212 good enough on its own? | **No.** In aged mice its survival is close to sham (38/42 vs 42/42 deaths, p=0.12). It only matches PSLN-344 in young mice, where both give 0% mortality and there is no unmet need (S09-B/D/F). | Fisher exact test |

**Why the recommendation is conditional.** The committee will find the following problems when it checks the data, so they are stated here first. Details are in Appendix A.

* Body-weight records have been copied across experiments. Eighteen pairs of animals from *different* experiments share ≥4 identical daily weights; about 0.02 such pairs would be expected by chance.
* One survival block is a row-for-row copy of another: **S06-D = S06-C**.
* The two most striking survival results, homologous CA09 (S03-I) and wild-type VN04 H5N1 (S03-J), contradict their own body-weight records.
* A neutrophil block partly duplicates an alveolar-macrophage block (S11-B / S11-A).
* Several blocks are mislabelled: S03-B/F labels are rotated; the second S09-A block labelled "16 h" is really 72 h; S08-C cannot be reconciled with S01-B.

The efficacy conclusion **survives excluding every flagged block**:

* The immunogenicity cross-checks pass. S13 subclass titres reconcile with S03 total IgG, and the S09-A panel reproduces the S01-A animals exactly.
* The survival effect holds in the most conservative subset.

Until the root cause is known, though, we cannot rule out that the problem is more than clerical.

**What we give up if we drop PSLN-344.** We give up the only adjuvant in our hands with these properties in aged animals, all backed by our data:

* cuts lethal-challenge mortality by **66 percentage points** (90% → 24%; conservative set 94% → 29%);
* brings functional antibody titres to young levels, with 100% of aged mice at HAI ≥1:160 vs 0% on PSLN-212 (S03-C/G);
* shifts responses toward Th1 (IgG2a/IgG1 2.14 vs 0.58; S13-A/B) and induces CD8 and lung-resident memory (TRM) responses that track with heterosubtypic protection;
* protects within 3 days of vaccination and lasts at least 60 days;
* has been clean on early safety.

It is also needle-free and aimed at the age segment with the weakest vaccine responses. If we drop it, what we avoid is the Mn²⁺ safety question, the cost of fixing the data, and a more complex formulation. **The case for dropping now would be the data-integrity risk alone. Gate 0 resolves that risk cheaply and quickly, so dropping now would be premature.**

# 2. What the data show

## 2.1 Head-to-head in aged mice (selected readouts; all 43 are in T1 and Figure 1)

![Figure 1. PSLN-344 vs PSLN-212 in aged mice: effect sizes (A) and restoration toward young immunity (B). Source: T1.](figures/Fig1_head_to_head_forest.png)

| Readout (block) | Sham | Aged PSLN-212 | Aged PSLN-344 | Young PSLN-212 | PSLN-344 vs PSLN-212 (95% CI) | Holm p | Restored |
|------------------------------|-------|---------|---------|---------|----------------|--------|--------|
| Lung Ifnb1 at 16 h, fold (S01-A) | 0.94 | 16.5 | 36.9 | 37.5 | 2.2× (1.8–2.7) | 4.0e-4 | 100% |
| Lung Gm-csf at 36 h, fold (S02-F) | 1.2 | 1.6 | 8.5 | – | 5.4× (3.9–7.3) | 0.001 | – |
| CCR7⁺ migratory DC at 72 h, % (S02-A) | 2.5 | 7.3 | 30.7 | 35.0 | +23.4 pts (13.8–33.0) | 0.037 | 87% |
| Antigen⁺ DC in MLN, % (S02-C) | – | 1.8 | 7.1 | 9.4 | +5.3 pts (3.6–7.1) | 0.017 | 70% |
| Tfh ICOS-hi at d7, % (S04-A) | 0.3 | 3.8 | 10.3 | 13.6 | +6.4 pts (2.6–10.3) | 0.059 | 75% |
| GC B cells at d7, % (S03-K) | 1.2 | 2.3 | 6.5 | 9.8 | +4.2 pts (2.3–6.1) | 0.041 | 62% |
| Serum IgG CA09 at d14, GMT (S03-A) | 56 | 393 | 7,305 | 11,959 | 18.6× (9.1–37.9) | 5.2e-4 | 91% |
| HAI CA09 at d14, GMT (S03-C) | 8 | 46 | 368 | 485 | 8.0× (3.9–16.4) | 0.011 | 93% |
| HAI Aichi at d14, GMT (S03-G) | 10 | 35 | 320 | 368 | 9.2× (4.2–20.2) | 0.007 | 96% |
| Neutralising CA09, GMT (S03-D) | 52 | 418 | 3,840 | 6,686 | 9.2× (3.1–27.2) | 0.037 | 89% |
| IgG2a/IgG1, CA09 (S13-A/B)* | – | 0.58 | 2.14 | 2.97 | Th2 → Th1 | – | – |
| IFN-γ⁺ CD8 after H5 restimulation, d60, % (S05-G) | 1.5 | 3.0 | 9.9 | 14.4 | +6.8 pts (3.4–10.3) | 0.047 | 65% |
| Lung CD8 TRM at d25, % (S05-I) | 0.6 | 1.0 | 4.0 | 6.0 | +3.0 pts (2.2–3.7) | 0.002 | 62% |

*\*The S03-B/F quotients as printed have rotated group labels (Appendix A6), so the values here were recomputed from the raw subclass titres in S13. Titre and fold values are geometric means; percentages are arithmetic means; n = 3–5 per group. HAI readings of <1:10 were set to 5. "Holm p" is the Holm adjustment across all 43 clean readouts.*

## 2.2 Protection

![Figure 2. Survival by study (tier B = minor inconsistencies; tier C = integrity flags) and pooled risk ratios. Source: T2, T3.](figures/Fig2_survival.png)

| Analysis set | Studies | PSLN-344 deaths | PSLN-212 deaths | MH risk ratio (95% CI) | Stratified Cox HR (95% CI) |
|----------------------------------|-------|-------------|-------------|-----------------|-----------------|
| All aged head-to-head studies (S06-D excluded as a copy) | 10 | 12/73 (16%) | 64/73 (88%) | 0.19 (0.11–0.31) | 0.08 (0.04–0.16) |
| S06 series, BALB/c (**primary**) | 6 | 10/42 (24%) | 38/42 (90%) | 0.26 (0.15–0.45) | 0.11 (0.05–0.23) |
| Most conservative (also excludes S06-C) | 5 | 10/35 (29%) | 33/35 (94%) | 0.30 (0.18–0.51) | 0.12 (0.06–0.26) |
| Durability: challenge at d60 (S06-E,F,G) | 3 | 7/21 (33%) | 20/21 (95%) | 0.35 (0.19–0.64) | 0.14 (0.06–0.35) |

Other protection findings:

* **Middle-aged mice (14 months), with or without prior PR8 infection (imprinting).** PSLN-344: 1/7 deaths in each of the 4 arms. PSLN-212: 7/7 (naive) and 3/7–7/7 (imprinted) (S06 rows 71–105; Fisher p = 0.006 and 6e-6).
* **Young mice.** 0 deaths with either adjuvant after PR8 or Perth H3N2 challenge at day 21, or rgH5N1 challenge at day 180 (S09-B/D/F).

## 2.3 Where PSLN-344 falls short (must be disclosed)

1. **Cellular immunity and DC maturation are only partly restored.** DC CD40⁺/CD86⁺ reach 21–24% of the young level (aged PSLN-344 11.2%/14.5% vs young 38.7%/37.9%; p ≤ 0.0004; S02-D). TRM is −34% vs young (p = 0.0007; S05-I). IFN-γ⁺ CD8 at d14 is −31% vs young (p = 0.0016; S05-F).
2. **Survival is not fully restored.** Aged PSLN-344 mortality was 10/42 vs 0/42 for young PSLN-212 (p = 0.0011; S06 series).
3. **Binding IgG is below young levels, and the boost narrows the gap with PSLN-212 for CA09.**
   * Day-14 IgG is 0.41× young for Aichi (p = 0.039) and 0.61× for CA09 (p = 0.11) (S03-A/E).
   * After a day-14 boost, IgG is 0.29–0.38× young (p ≤ 0.048).
   * After the boost, PSLN-344 is only 3.5× above PSLN-212 for CA09 (1.5–8.4; Holm p = 0.059; S13-I), though it remains 11.5× higher for Aichi (S13-J).
   * There are no challenge data after a boost.
4. **Some tissue responses are slower to resolve.** Lung Tnf (8.4×) and Il10 (4.2×) are still raised at 72 h with PSLN-344, whereas young animals have resolved (0.5×, 0.1×) (second S09-A block, which is the 72 h timepoint). At 16 h, Tnf is 41× vs 14× in young animals.
5. **Several key measurements were never made.** There are no data on mucosal IgA, the upper airway, Mn²⁺ content or biodistribution, male mice, or a licensed-vaccine benchmark.

## 2.4 Safety and dose (Figure 4)

![Figure 4. Dose-response (S08-A), reactogenicity (S08-D) and CNS transcripts (S10-A).](figures/Fig4_dose_reactogenicity_CNS.png)

* **Dose.** Mn²⁺ raises the ceiling of the response rather than its potency. In an Emax fit, PSLN-344 reaches 49× (SE 5) vs 14× (SE 2) for PSLN-212, with similar ED50 (11.5 vs 9.5 µg). At 20 µg the response is 3.6× higher (p = 0.0003; S08-A). The 20 µg dose used in all efficacy studies is near the fitted ED90 (23 µg).
* **Reactogenicity.** No PSLN-344 animal lost ≥10% body weight. PSLN-212/R848 caused ≥10% loss in 4/5 animals, and one animal was missing on day 10 (S08-D).
* **CNS.** There was no induction at 36 h (S10-A). However, this covers one timepoint, transcripts only, n=5, and no Mn measurement.
* **Formulation.** Encapsulation efficiency is 54.8% for PSLN-344 vs 59.6% for PSLN-212 (p = 0.29; S08-B). No stability data are in the file.

## 2.5 Data integrity in one paragraph (full register in Appendix A; exhibits in Figure 5)

Seventeen findings were logged: 2 critical, 4 high, 4 medium, 6 low and 1 informational. They cluster in the body-weight and survival blocks (S06, S09, S13-F/G, S15) and in a small number of labels.

The immunogenicity blocks (S01–S05, S13-A–D and H–J, S14) are in better shape:

* Apart from the label and timepoint errors (A6–A8), they reconcile across blocks wherever we could test it: S13 subclass titres against S03 total IgG, S09-A against the S01-A animals, and the S04-B ratio against its source.
* No duplication was detected in them, other than the values S08-C shares with S01-B.

![Figure 5. Data-integrity exhibits: label rotation (A), duplicated survival block (B), duplicated weight records (C), duplicated flow data (D), duplication vs chance (E), reused decimals with edited integers (F).](figures/Fig5_data_integrity_exhibits.png)

# 3. Mechanism of action built from our data

![Figure 3. Mechanism of action with supporting numbers and block references.](figures/Fig3_mechanism_of_action.png)

| Step | Evidence | Type of evidence |
|----------------------|--------------------------------------------------------------|----------------|
| 1. Surfactant-mimetic liposome targets the alveolar niche | AECII SRB⁺ 15.8% vs 0.4% with free dye (p = 1e-4; S01-B). Alveolar macrophage uptake falls from 43.1% to 12.7% in Sftpa1/Sftpd-KO mice (p = 4e-5; S01-C) | Causal (genetic) |
| 2. Mn²⁺ raises the ceiling of STING output in aged lung | Ifnb1 at 16 h is 36.9× vs 16.5×, equal to young (S01-A). Emax 49× vs 14× (S08-A). Blocking gap junctions with CBX lowers recruited monocytes from 7.3% to 3.1% (S11-C), consistent with cell-to-cell propagation (CBX has off-target effects) | Correlative + pharmacological |
| 3. The aged lung's chemokine programme is restored | At 16 h: Ccl2 590× vs 7.6× (young 1,390×); Ccl3 30× vs 1.1×; Ccl5 20× vs 2.6×; Il6 36× vs 5.6× (S09-A, n=3). Gm-csf 8.5× vs 1.6× at 36 h (S02-F) | Correlative |
| 4. CCR2⁺ monocytes are recruited and become moDCs, not inflammatory macrophages | Monocytes at d4: 30.6% vs 16.7% (S01-D). CCR2 blockade cuts monocytes by 67% and Ly6C⁺ macrophages by 84% (S07-B), and GZMB⁺ CD8 by 79% (S02-I). moDC formation depends on IFNAR: 19.7% → 2.1% with IFNAR-KO marrow, rescued to 12.4% by GM-CSF (S02-H). GM-CSF converts PSLN-212 responses (moDC 5.9% → 13.8%; S02-G). Without Mn, Ly6C⁺CCR2⁺ macrophages accumulate (19.0 vs 3.4 ×10⁵ at d5; S07-A, n=3, age not stated) | Causal (antagonist, chimera, rescue) |
| 5. DCs migrate and carry antigen to the MLN (Gi/CCR7) | CCR7⁺ DC 30.7% vs 7.3% (S02-A). Antigen⁺ MLN DC 7.1% vs 1.8%, blocked by pertussis toxin (PTX) to 2.4% (S02-C). MLN DCs prime OT-I T cells: 18.7% vs 0.8% (S02-E). In vivo priming in the MLN is PTX-sensitive (30.9% → 6.8%) but lung priming is not (S05-C) | Causal (PTX) |
| 6. Tfh/GC output rises and suppression falls | Tfh ICOS-hi 10.3% vs 3.8%. Tfr 10.8% vs 26.7% (S04-A/B). GC B 6.5% vs 2.3% (S03-K). Aicda 3.5× (S03-L). Lung Treg 3.0% vs 6.7% (S04-D). CD206⁺ macrophages 48.9% vs 71.5% (S11-E) | Correlative |
| 7. Antibody and T-cell effector responses follow, then protection | See 2.1–2.2. Protection is antigen-dependent (S15-H) | Correlative + specificity control |

**Not yet shown.** These gaps drive study S2:

* The Mn²⁺ contribution has never been isolated. There is no Mn-only arm, no Mn-liposome without CDN, and no free-Mn arm.
* Dependence on STING itself has not been tested.
* IFNAR dependence in intact aged animals is unknown. The S12-A chimera result (21.3% vs 15.4%, n=3, p=0.12) is not significant.
* Which epithelial cells take up PSLN-344 is uncertain, because S08-C is unreliable.
* Uptake in the human nasal cavity, as opposed to mouse lung, is unknown.

# 4. Biomarkers to validate efficacy

![Figure 6. Biomarker cascade: readouts that separate PSLN-344 from PSLN-212 in aged mice, by time of measurement.](figures/Fig6_biomarker_cascade.png)

| Tier / role | Biomarker (mouse evidence) | Effect in aged mice, PSLN-344 vs PSLN-212 | Proposed human / large-animal measure | Use |
|--------------|----------------------|--------------------|--------------------------|------------------|
| **1. PD / target engagement (16–36 h)** | Lung Ifnb1 (S01-A); Gm-csf (S02-F); Ccl2, Ccl3, Il6 (S09-A) | 2.2× (Hedges g 5.6); 5.4× at 36 h (g 8.0); Ccl2 77× (p = 0.002) | Nasal lining fluid (nasosorption) IFN-β, CXCL10, CCL2 and GM-CSF at 24 h; blood ISG score | Dose selection; batch potency bridge (a reporter assay for release); early go/no-go in Phase 1 |
| **2. Mechanism (d3–7)** | CCR7⁺ DC (S02-A); Tfh ICOS-hi and Tfr (S04-A/B); GC B (S03-K) | +23 pts; +6.4 pts; −15.9 pts; +4.2 pts | Circulating Tfh (ICOS⁺PD-1⁺CXCR5⁺) at d7; cTfh:cTfr ratio; plasmablasts at d7 | Confirms the adaptive arm is restored in older adults |
| **3. Efficacy surrogate (d14–28)** | HAI (S03-C/G); neutralisation (S03-D/H); IgG2a/IgG1 (S13) | 8–9× GMT; 100% at ≥1:160 vs 0% | HAI GMT, seroconversion and seroprotection; MN; IgG subclass; **nasal IgA** (not yet measured) | Regulatory immunogenicity endpoints; comparison with licensed enhanced vaccines |
| **4. Breadth / durability** | IFN-γ⁺ CD8 after heterologous H5 restimulation (S05-F/G, S14-A); lung TRM (S05-I) | +4.9 to +7.9 pts; +3.0 pts | IFN-γ ELISpot to conserved NP/M1; nasal-curettage TRM in a subset | Supports a heterosubtypic claim |
| **5. Safety** | Tnf/Il10 overshoot and 72 h persistence (S09-A); CNS Ifnb1/Tnf/Isg15 (S10-A); weight (S08-D); Tnf:Ifnb1 ratio (1.1 for PSLN-344 vs 8–30 for R848 arms) | See 2.3–2.4 | Serum IL-6/TNF/CRP on days 1–3; smell testing; facial-nerve adverse events of special interest; blood Mn | Reactogenicity and neuro-safety gating |

**Correlate of protection: what our data can and cannot say.** Immunogenicity and survival were measured in different animals, so no individual-level correlate can be derived.

* At group level, HAI ≥1:40 was **not** protective in aged mice. All 5/5 PSLN-212 mice had HAI ≥40, yet 0/7 survived 10× LD50 CA09 (S03-C vs S03-I; note S03-I is tier C).
* Every protected group had an HAI GMT ≥368, and every animal in those groups had HAI ≥160.
* **Study S1 must bleed the challenged animals before challenge**, so that a protective HAI/MN/IgA threshold can be estimated directly.

# 5. Target demographic (for market-research TAM sizing)

| Segment | Definition for sizing | Strength of evidence | Basis in our data |
|----------|------------------------------|------------|------------------------------------------------|
| **Primary** | Adults **≥65 years** receiving seasonal influenza vaccine. Prioritise ≥75 years and residents of long-term-care facilities (LTCF) | Strongest | Differentiation from PSLN-212 is best established in ≥20-month mice: BALB/c throughout (S01–S06, S13, S14), plus C57BL/6 and Swiss Webster (S15-L/N). By an external mapping, 18–24-month mice correspond to humans aged about 56–69 (Appendix D) |
| **Secondary** | Adults **50–64 years** | Moderate (one study) | In 14-month (middle-aged) mice, PSLN-212 failed (7/7 deaths in naive mice) while PSLN-344 protected (1/7), and prior influenza imprinting did not change this (S06 rows 71–105). The external mapping puts these mice at about 38–47 human years, so the benefit may begin below 65; 50–64 is proposed as the conservative commercial definition. The companion weight data carry the A1 flag |
| **Strategic** | **Pandemic and pre-pandemic H5** programmes for older adults (government stockpile or tender). Outbreak use, because onset is fast | Moderate | Heterosubtypic rgH5N1 protection in aged mice (S06-C/F). Protection 3 days after dosing (S06-B, S15-H). Wild-type H5N1 result (S03-J) held until audited |
| **Not a target (current data)** | Adults <50 and children | – | No efficacy difference in young mice: 0/8 deaths with either adjuvant (S09-B/D/F). Ages between young and 14 months were not tested; juveniles were not tested |
| **Not a product** | Stand-alone antigen-free antiviral | – | PSLN-344 alone gave 7/7 deaths (S15-H) |

**Parameters market research should size or verify (no external numbers are assumed here):**

* population aged ≥65, ≥75 and 50–64 in target geographies, and the LTCF population;
* age-specific influenza vaccination coverage;
* the share of ≥65 vaccinees currently receiving "enhanced" vaccines (adjuvanted, high-dose, recombinant), and their price premium;
* acceptability of intranasal vaccination in older adults. The currently licensed intranasal influenza vaccine is live-attenuated and is not labelled for people ≥50 (check against the current label);
* pandemic-preparedness procurement volumes;
* business model: own vaccine vs licensing the adjuvant to antigen partners, which changes the TAM from vaccine sales to royalties;
* potential extension to other respiratory antigens used in older adults. This is an upside only; our data cover influenza and the model antigen ovalbumin.

# 6. Next steps: gated plan

**Timeline (months from committee approval; in-life durations come from our own study designs):**

| Study | M0–2 | M2–4 | M4–6 | M6–8 | M8–12 | M12–24 |
|----------------------------------------|----------|----------|----------|----------|----------|----------|
| **S0** Data-integrity audit (**Gate 0**) | ■ | | | | | |
| **S1** Confirmatory aged efficacy vs benchmark (**Gate 1**) | order aged mice | ■ | ■ | ■ (d60 cohort) | | |
| **S2** Mn²⁺ decomposition and STING/IFNAR dependence | | ■ | ■ | | | |
| **S3** Mn²⁺ biodistribution and neuro/lung safety (non-GLP) | | ■ | ■ | ■ | | |
| **S4** Dose, regimen and durability to d180 in aged mice | | ■ | ■ | ■ | ■ | |
| **S5** Large-animal translational study (device, upper airway) | | | | ■ (Gate 1 passed) | ■ | |
| **S6** CMC: Mn specification, encapsulation efficiency, lyophilised stability, potency assay | | ■ | ■ | ■ | ■ | ■ |
| **S7** GLP toxicology → IND/CTA → Phase 1 (indicative) | | | | | | ■ (Gate 2) |

## S0: Data-integrity audit and re-baselining (Gate 0; M0–M2)

* **Must establish** that the primary results are supported by source records, and the root cause of findings A1–A10.
* **Population / scope:** All 15 sheets. Priority blocks: S06-A–G, S03-I/J, S13-F/G, S15 (all), S09-C/E/G, S11-A/B, S03-B/F, S08-C, S09-A. Source material: animal-room weight and clinical-score logs, euthanasia records, FCS files, qPCR Ct files, ELISA plate reads, randomisation records.
* **Comparators:** Reported values vs source records.
* **Endpoints / readouts:**
  * percentage of reported values verified;
  * for each duplicated column, which is the original;
  * corrected labels for S03-B/F, S09-A, S07-C and S08-C;
  * colony-health records explaining deaths in unchallenged animals (A9).
* **Go:** ≥95% of values in the primary blocks are verified, and the duplication is explained as clerical with originals recovered.
* **Stop / escalate:** any evidence of deliberate alteration. In that case, freeze the programme, open a formal QA investigation, and re-base the programme only on S1/S2 data.

## S1: Independent confirmatory efficacy study in aged mice vs a clinical benchmark (Gate 1; dosing starts M2, readout about M6 for the d14 cohort and M8 for the d60 cohort)

* **Must establish:**
  1. that the PSLN-344 vs PSLN-212 survival advantage replicates under blinding and randomisation in both sexes;
  2. where PSLN-344 stands against the enhanced intramuscular approaches used clinically in older adults;
  3. an individual-level protective threshold.
* **Population:**
  * aged mice (≥20 months), BALB/c and C57BL/6, **15 male + 15 female per key arm** (BALB/c primary; C57BL/6 replicate at 15 per arm);
  * a young reference arm (8–10 weeks);
  * unchallenged aged controls to monitor colony health.
* **Arms and comparators** (bivalent inactivated CA09 H1N1 + Aichi H3N2 vaccine, as in S03 and S06-C):
  1. intranasal vaccine + PSLN-344 20 µg;
  2. intranasal vaccine + PSLN-212 20 µg;
  3. intranasal vaccine + empty liposome (sham);
  4. **intramuscular vaccine + squalene emulsion (MF59-type research analogue)**;
  5. **intramuscular high-dose antigen (4× HA)**;
  6. young + PSLN-212 (reference);
  7. unchallenged aged controls.
* **Primary endpoint:** 14-day survival after 5× mLD50 rgH5N1 challenge at d14. This challenge is heterosubtypic to the bivalent vaccine (design of S06-C, run independently here).
* **Key secondaries:**
  * the same endpoint at d60 (design of S06-F);
  * pre-challenge (d13) HAI, MN and **nasal-wash and BAL IgA** in the challenged animals themselves;
  * lung viral titre at d3 and d5 post-challenge (satellite group);
  * weight-loss AUC with a single pre-specified humane-endpoint rule.
* **Exploratory:** Ifnb1, Ccl2 and Gm-csf at 16 and 36 h (satellite); Tfh/Tfr at d7.
* **Sample size (from our data):**
  * With 30 per arm, a Fisher exact test has ≥99% power if the observed effect is real (90% vs 24%). It has 78% power if the true effect is half that (90% vs 57%), and 85% power against a benchmark with 70% mortality. Simulation used 6,000 replicates; mortality inputs are from S06.
  * 30 per arm also gives 90% power to detect a 1.5-fold HAI GMT difference (pooled SD 0.68 log2 from S03-C/G).
* **Go criteria:**
  * mortality RR for PSLN-344 vs PSLN-212 ≤0.5 with upper 95% CI <1;
  * HAI GMT ratio for PSLN-344 vs PSLN-212 ≥4 (we observed 8–9×);
  * PSLN-344 non-inferior to the better intramuscular benchmark on survival (upper 95% CI of the RR ≤1.5), and superior on mucosal IgA or heterosubtypic survival;
  * ≤1 death in the unchallenged aged controls.
* **Timing:** In-life is 28 days for the d14 cohort and 74 days for the d60 cohort, plus analysis. Order aged mice at M0.

## S2: Mechanism decomposition (M2–M5; can run in parallel with S1)

* **Must establish:** whether the benefit needs Mn²⁺ bound in the particle rather than present separately; whether it depends on STING; and whether it depends on IFNAR in the intact host.
* **Population:**
  * aged BALB/c;
  * young *Sting1* mutant (gt/gt) and *Ifnar1*-KO mice with their wild-type controls;
  * aged wild-type mice given a STING inhibitor.
* **Arms:**
  * PSLN-344;
  * PSLN-212;
  * PSLN-212 + free MnCl₂, matched to the Mn content of PSLN-344 (which CMC must measure first);
  * Mn-liposome without CDN-1807;
  * empty liposome;
  * PSLN-344 + STING inhibitor.
* **Readouts:** Ifnb1, Isg15, Ccl2 and Gm-csf (lung/BAL, 16 and 36 h); CCR7⁺ and antigen⁺ MLN DC (36–72 h); Tfh (d7); HAI (d14).
* **Sample size:** 6–8 per arm, based on our SDs (Ifnb1 g = 5.6, CCR7⁺ DC g = 3.7).
* **Go:** the benefit requires STING and particle-bound Mn. If free Mn or the Mn-liposome alone reproduces it, that changes our IP and CMC strategy.

## S3: Mn²⁺ biodistribution and neuro/lung safety (non-GLP; M2–M8)

* **Must establish** that intranasal Mn²⁺ does not accumulate in the olfactory bulb or brain, or cause neurobehavioural or respiratory toxicity, at multiples of the efficacious dose. Intranasal Mn is known to travel along olfactory pathways (Appendix D).
* **Population:** aged mice and rats (the likely GLP species), both sexes.
* **Arms:** PSLN-344 at 1×, 3× and 10×; PSLN-212; vehicle; MnCl₂ positive control. Single and repeat dosing.
* **Readouts:**
  * Mn by ICP-MS in olfactory bulb, striatum, lung, liver and blood at d1, 7 and 28;
  * Mn-enhanced T1 MRI of the olfactory bulb;
  * olfactory and motor behaviour;
  * nasal and olfactory epithelium, lung and brain histopathology;
  * CNS Ifnb1, Tnf and Isg15 at 6 h, 36 h, d7 and d28 (extends S10-A);
  * serum IL-6, TNF and IFN.
* **Go:** no Mn elevation in brain regions above a pre-specified limit and no histopathology or behavioural signal at ≥3× the efficacious dose. **If it fails,** switch to the Mn-free fallback (PSLN-212 + a GM-CSF-pathway strategy; S02-G supports this) or a lower-Mn design.

## S4: Dose, regimen and durability in aged mice (M2–M12)

* **Must establish:** the minimal fully effective dose; whether prime-boost adds protection; and whether protection lasts to d180 in aged mice (so far shown only to d60 in aged and to d180 in young mice; S09-F).
* **Arms:**
  * PSLN-344 at 5, 10, 20 and 40 µg (dose grid from S08-A);
  * prime only vs prime-boost (boost at d14, as in S13-I/J);
  * PSLN-212 prime-boost, to test whether a boost can substitute for Mn.
* **Readouts:** HAI, MN and IgA at d14, 28, 90 and 180; TRM at d25 and d180; lethal challenge at d180.
* **Sample size:** 10–12 per arm for immunogenicity (2-fold GMT, 90% power); 30 per arm for the d180 challenge arms.
* **Timing:** 194-day in-life.

## S5: Large-animal translational study (after Gate 1; M8–M16)

* **Must establish:** immunogenicity, upper-airway protection and local/CNS safety in a species with human-like upper airways, **using the intended human delivery device**. Mouse intranasal dosing reaches the lungs, and our mechanism is alveolar. A human nasal spray would mainly deposit in the nose, so the deposition question is a key translational risk.
* **Population:** ferrets (adult, and aged if they can be sourced); aged non-human primates as an alternative.
* **Arms:** PSLN-344 vs PSLN-212 vs intramuscular benchmark vs intranasal antigen alone; spray vs aerosol delivery.
* **Readouts:** HAI, MN, nasal IgA, nasal-wash viral titres and shedding, transmission to contacts, olfactory-epithelium and brain histology, tissue Mn, and the tier 1 PD biomarkers in nasal fluid.

## S6: CMC (M2 onward)

* **Must establish:** Mn content per dose and its uniformity (currently unknown); improved encapsulation (currently 54.8% ± 5.1; S08-B); particle size and zeta release specifications; stability of the lyophilised product (2.5% trehalose, −20 °C; no stability data yet), including a 2–8 °C option; and a cell-based ISG-reporter potency assay bridged to the lung Ifnb1 response (S08-A).
* **Go:** specifications are defined and the product is stable for the planned clinical-supply period.

## S7: IND-enabling and first-in-human (indicative; Gate 2 = S1–S3 and S6 passed)

* **Toxicology:** GLP repeat-dose intranasal studies in two species, with nasal local tolerance, a neuro-toxicology component (Mn) and safety pharmacology.
* **Phase 1 design (to be finalised with clinical and regulatory):**
  * **Population:** staggered cohorts of healthy adults aged 18–49 (safety sentinels), then 50–64, then ≥65, then ≥75.
  * **Comparators:** a licensed enhanced intramuscular vaccine for ≥65 (adjuvanted or high-dose), and intranasal antigen without adjuvant.
  * **Primary endpoint:** safety: solicited nasal and systemic reactions d0–7; unsolicited adverse events to d28; serious and medically attended events to month 6; adverse events of special interest including facial-nerve palsy and smell loss (formal smell testing).
  * **Secondary endpoints:** HAI GMT, seroconversion and seroprotection at d28; MN; nasal IgA; cTfh at d7; ISG/CXCL10/CCL2 in nasal fluid at d1.
  * **Sizing:** by biostatistics, using the comparator's variance. Our mouse variances cannot size a human trial.

# 7. What we considered and ruled out

| Option considered | Decision | Evidence |
|------------------------|------------------|----------------------------------------------------------|
| Advance **PSLN-212** (no Mn) as lead | **Ruled out** for the target population; kept as comparator and fallback | Aged survival close to sham (38/42 vs 42/42 deaths, p = 0.12). HAI 46 vs 368. Equivalent only in young mice, where both give 0% mortality (S06, S03, S09) |
| Add the TLR7/8 agonist **R848** (PSLN-R848, PSLN-212/R848, PSLN-344/R848) | **Ruled out** | R848 alone: Ifnb1 4.3×, Tnf 130×, Il10 29× (S09-A). PSLN-212/R848: weight nadir 90.0%, 4/5 mice lost ≥10%, 1 animal missing (S08-D). Adding R848 to PSLN-344 **lowered** Ifnb1 (0.64× at 20 µg, p = 0.043; S08-A) |
| **cGAMP** instead of CDN-1807 (CMP-204) | **Ruled out** | Ifnb1 7.7× vs 16.5× for PSLN-212 (p = 3e-4). Post-boost IgG 4.7× lower (p = 8e-4) (S01-A, S13-I). Day-14 IgG, CA09 HAI and neutralising titres about 2× lower (p = 0.06–0.13); Aichi HAI similar (S03) |
| **PSLN-212 with a boost** instead of Mn | **Not sufficient on current data; retested in S4** | Post-boost IgG still 3.5× (CA09) and 11.5× (Aichi) below PSLN-344 (S13-I/J). No challenge data after a boost |
| **PSLN-212 + recombinant GM-CSF** | **Fallback only** | Mechanistically rescues moDCs (5.9% → 13.8%; S02-G), but adds a biologic and two-component complexity |
| PSLN-344 as a **stand-alone, antigen-free** prophylactic | **Ruled out** | 7/7 deaths without vaccine vs 1/7 with vaccine (S15-H) |
| Indication in **young adults or the general population** | **Ruled out** | No efficacy difference; both adjuvants 100% protective (S09-B/D/F) |
| **40 µg** dose | Not needed now; dose-ranging in S4 | Ifnb1 49.7× vs 45.5× at 20 µg (S08-A). Plateau above the fitted ED90 of about 23 µg |
| Citing the **wild-type H5N1** (S03-J) and **homologous** (S03-I) results as headlines | **Withheld until audit** | Contradicted by their own weight records (A3, A4) |
| Claiming **lower epithelial uptake** of PSLN-344 (S08-C) | **Rejected** | Cannot be reconciled with S01-B (A8) |
| Reading S03-B/F as printed (would imply PSLN-344 is **Th2-skewed**) | **Corrected** | Labels rotated; raw S13 titres show a Th1 shift (A6) |
| Using S11-A/B, S05-A/B, S07-C, and S08 rows 89–101 | **Excluded** | Duplication, n=2 with an MHC mismatch, duplicate labels, orphan data (A5, A11–A13) |
| Counting Tfh:Tfr (S04-B) as separate evidence | **Not counted** | Arithmetically derived from the Tfr block (A17) |
| Analysis choices | Per-study and stratified pooling (MH, stratified Cox) rather than naive pooling. Log scale for titres and fold-changes. HAI <10 set to 5. Holm and BH multiplicity control. Sensitivity sets built by integrity tier | Appendix B |

# 8. Key risks

1. **Data integrity (highest).** Gate 0 resolves this in about 8 weeks. If deliberate alteration is found, the survival evidence is void and only S1 can re-establish efficacy.
2. **Translation from mouse to human.** Immunosenescence differs between species. Deposition in the human nose vs mouse lung is a major unknown, addressed by S5.
3. **Mn²⁺ neuro-safety** via olfactory transport: addressed by S3, with a fallback design.
4. **Competition.** Enhanced intramuscular vaccines are already standard for ≥65. We have no benchmark data yet (S1 supplies it).
5. **Generality.** Only female mice were used, mainly BALB/c. The cross-strain studies (S15-L/N) have an unstated challenge virus.

# Appendix A. Data-integrity register (summary; full evidence with cell references in `tables/A1_data_integrity_register.csv`)

| ID | Severity | Blocks | Finding | How it was handled |
|-----|----------|-----------------|--------------------------------------------------|------------------|
| A1 | Critical | Strong: S15-A, C, F, I, J, M; S09-E, G; S08-D; S09-C (day-12 row). Weaker (3 shared values or 2–3 fractional matches): S15-D, K, O; S13-F | Body weights duplicated across experiments. 18 cross-experiment animal pairs share ≥4 identical non-repeated readings (0.02 expected) and 15 share ≥5 (0.0001 expected). Decimal fragments are reused with edited integers. Examples: S09-E col AA = S15-M col L (7/7); S15-C PSLN-344 = S15-I vaccine + PSLN-344 (6 animals × 6 days); S09-C d12 PSLN-344Y = PSLN-212Y (8/8) | Weights not used as efficacy evidence; survival analysed by tier |
| A2 | Critical | S06-D vs S06-C | 28/28 survival rows identical despite different challenge days; the S15-D weights imply deaths that S06-D does not record | S06-D excluded |
| A3 | High | S03-I vs S13-F | PSLN-212: 7/7 dead by d6 in S03-I, yet all 7 were weighed on d8–10 and 3 recovered in S13-F. Group lists differ | Tier C |
| A4 | High | S03-J vs S13-G | Sham: 9/10 deaths in S03-J vs 10 animals weighed on d10 in S13-G. S13-G has a "Naive" group not in S03-J. One time value missing; n 9 vs 10 | Tier C |
| A5 | High | S11-B vs S11-A | 35/100 aligned cells identical (the first 2 animals of every group at all 5 timepoints) | Both excluded |
| A6 | High (interpretation) | S03-B/F vs S13-A–D | Group labels cyclically rotated; only the S13 labels are consistent with total IgG | Used S13 |
| A7 | Medium | S09-A block 2 | Labelled 16 h but is 72 h (r = 0.999 with S01-A 72 h) | Treated as 72 h |
| A8 | Medium | S08-C vs S01-B | Values and labels irreconcilable | Excluded |
| A9 | Medium | S06-E/G "Untreated" | "Unchallenged" mice died (1/7, 3/7) with no weight loss | Colony-health check in S0 |
| A10 | Medium | 28/69 group reconciliations | Weights recorded after recorded deaths; mixed blank and carried-forward handling of deaths | Single humane-endpoint rule in S1 |
| A11–A16 | Low | S07-C; S05-A/B; S08 rows 89–101; S09-B/F, S13-E, S03-J n; S15-L/N; S08-A/B | Duplicate labels; n=2 with an H-2Db tetramer in BALB/c mice; orphan data; n mismatches; challenge not stated; undefined preparations | Excluded or noted |
| A17 | Info | S04-B | Tfh:Tfr = (100−Tfr)/Tfr exactly | Not double-counted |

# Appendix B. Methods

* **Parsing.** Every block was parsed with its cell address kept (`code/load.py`; tidy file `tables/tidy_values.csv`). Observed counts were reconciled with the n stated in the annotation.
* **Two-group comparisons:**
  * titres and qPCR fold-changes on a log2 scale, reported as geometric-mean ratios with Welch 95% CIs;
  * percentages on the linear scale, reported as mean differences;
  * exact Mann-Whitney tests;
  * one-way ANOVA with Tukey, as stated in the annotation;
  * Hedges' g;
  * Holm and Benjamini-Hochberg adjustment across the 43 clean readouts.
* **Restoration index.** (PSLN-344 − floor)/(young PSLN-212 − floor) on the analysis scale. The floor is sham, or aged PSLN-212 where there was no sham arm.
* **Survival:**
  * per study: Fisher exact and log-rank tests;
  * pooled: Mantel-Haenszel risk ratio with the Greenland-Robins variance, the Cochran-Mantel-Haenszel test, and a Cox model stratified by study;
  * integrity tiers: B = minor inconsistencies; C = flagged; S06-D excluded as a copy.
* **Dose-response.** Four-parameter Emax model by nonlinear least squares.
* **Power.** Fisher exact test by simulation (4,000–6,000 replicates); t-test power on the log2 scale.
* **Integrity tests:**
  * aligned comparison of every pair of animal columns across experiments, counting identical non-repeated values;
  * chance baseline from the empirical per-day match rate, checked with a control that misaligns days;
  * fractional-part matching for values with ≥4 decimals;
  * derived-quantity checks (Tfh:Tfr; IgG2a/IgG1);
  * survival vs body-weight reconciliation per group.

# Appendix C. Traceability

| File | Contents |
|----------------------------------------|------------------------------------------------------------|
| `tables/T1_head_to_head_PSLN344_vs_PSLN212_aged.csv` | All 46 readouts (43 clean + 3 excluded) with group means, effect size and 95% CI, all p-values, restoration, and **cell ranges** |
| `tables/T2_survival_by_study_aged.csv`, `T3_survival_pooled.csv` | Per-study and pooled survival with cell ranges and integrity notes |
| `tables/T4_lung_cytokine_chemokine_panel_16h_S09A.csv` | S09-A panel at 16 h and 72 h |
| `tables/T5_moa_interventions.csv` | Causal MoA experiments: CCR2 blockade, IFNAR chimeras, GM-CSF rescue, PTX, CBX, SP-A/D |
| `tables/T6_survival_vs_bodyweight_reconciliation.csv`, `T7_bodyweight_duplication_pairs.csv`, `A1_data_integrity_register.csv` | Integrity evidence |
| `code/*.py` | All analyses, runnable against the original workbook |

# Appendix D. External context (not our data; for the committee to verify)

* Mn²⁺ sensitises the cGAS–STING pathway (Wang C. et al., *Immunity* 2018;48:675) and has adjuvant activity (Zhang R. et al., *Cell Mol Immunol* 2021;18:1222). This supports the plausibility of step 2.
* Intranasal manganese can reach the CNS through olfactory pathways (Tjälve H. et al., *Pharmacol Toxicol* 1996). This is the rationale for S3.
* An intranasal inactivated influenza vaccine adjuvanted with *E. coli* heat-labile toxin was associated with Bell's palsy (Mutsch M. et al., *NEJM* 2004;350:896). This is why the CNS data (S10-A) and the facial-nerve surveillance in S7 matter.
* Approximate mouse-to-human age mapping: 18–24 months ≈ 56–69 years; 10–14 months ≈ 38–47 years (Jackson Laboratory / Flurkey et al. 2007).
* FDA 2007 guidance on seasonal inactivated influenza vaccines defines HAI seroconversion and seroprotection criteria and non-inferiority margins. This is the framework for Phase 1/2 immunogenicity endpoints.
