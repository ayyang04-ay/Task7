# PSLN-344 Portfolio Review: Recommendation and Proposed Next Steps

**Asset:** PSLN-344, an intranasal adjuvant. The STING agonist CDN-1807 plus Mn²⁺ (coordination polymer) in a pulmonary-surfactant-biomimetic liposome (DPPC/DPPG/DPPE-PEG2000/cholesterol). It is given together with an inactivated influenza vaccine.
**Comparator formulation in our data:** PSLN-212, the same liposome and CDN-1807 *without* Mn²⁺.
**Prepared:** 1 November 2026.
**Data basis:** `psln_program_dataset.xlsx` (15 sheets, last saved 3 Sep 2026) and `psln_program_annotation.pdf` (15 Sep 2026). No other data were used.
**Citation convention:** Each number carries the workbook block it comes from, e.g. **[S03-C]**. Where relevant it also names the evidence table, e.g. **(ET2)**, in `PSLN-344_evidence_tables.xlsx`. There, every per-animal value is traceable to its original cell address (ET13–ET15). "Aged" means BALB/c ≥20 months unless stated. n = 2–10 per group (most 5–7).

---

## 1. Recommendation

**Short answer:** not as a development asset today. Yes as a low-cost option of 6 months or less, with kill criteria agreed in advance.

**Do not advance PSLN-344 into development. Keep it in the portfolio only as a time-boxed "verify-or-kill" option, and make termination the default outcome.** Two gates come first:

- **Gate 0** (≤8 weeks): a source-data audit.
- **Gate 1** (≤6 months): decisive, independently run experiments.

No IND-enabling spend until both gates pass.

**The ask of the committee:**
- Approve Gate 0 now (QA-led, internal effort).
- Ring-fence the Gate 1 package, to be released only if Gate 0 passes.
- Freeze all other PSLN-344 spend.
- Schedule the go/kill decision for the first portfolio review after Gate 1 reads out.

**Why not advance.**
- **The data package is not bankable.** The audit found 20 integrity findings, 5 of them critical (Section 8). They include:
  - a survival experiment that is a cell-for-cell copy of another (S06-D = S06-C);
  - survival records contradicted by the body-weight records of the same cohorts in 11 arms;
  - body-weight values reused across independent experiments;
  - two flow-cytometry blocks sharing 35/100 position-matched values;
  - group labels rotated between two antibody-subclass blocks.
- Of the 18 challenge-survival blocks, only one (S06-B) has no detectable integrity flag, directly or through its companion weight data.
- **It is not yet shown that our small molecule does the work.** There is no Mn²⁺-only (no CDN-1807) arm anywhere in the dataset. The only vehicle control ("Sham") is described as empty liposome, with no Mn²⁺-containing vehicle arm. The entire advantage of PSLN-344 over PSLN-212 could come from Mn²⁺. STING dependence was never tested with a knockout.
- **Safety and CMC are essentially untested.** Specifically:
  - there is no Mn biodistribution or CNS histology;
  - the CNS readout is one timepoint, and the annotation describes its data as "mean ± SD";
  - the encapsulation assay is non-specific (it reports 61% "CDN-1807" in a preparation that contains none) [S08-B];
  - the mechanism depends on alveolar delivery, so a human product would have to be inhaled rather than a nasal spray [S01-B, S01-C].

**Why not drop today.**
- **The signal, if real, is large and internally coherent.** In aged mice, PSLN-344 beat PSLN-212 in the expected direction on 52 of 53 continuous immune readouts, 48 of them significantly (Welch p<0.05; ET2).
- **The survival effect holds up when flagged data are removed.**
  - Pooled survival after lethal challenge is 84% vs 12% as printed (Tier A: 61/73 vs 9/73).
  - It is 80% vs 11% using only blocks where survival and weight records agree (Tier B: 28/35 vs 4/35).
  - In the single unflagged experiment it is 5/7 vs 0/7 (S06-B; log-rank p=0.0009) (ET5).
- **The opportunity is differentiated.** The data point to a mucosal adjuvant that works in old animals and protects across subtypes. Settling whether the data are real costs little compared with what would be lost if they are.

**Decision rule to pre-agree.**
- **Terminate** if any of the following occurs:
  - the pivotal blocks cannot be source-verified (Gate 0);
  - an independent, blinded, adequately powered replication fails to show PSLN-344 > PSLN-212 on survival in aged mice;
  - a Mn-only liposome performs as well as PSLN-344;
  - Mn accumulates in the olfactory bulb or brain.
- **Advance** to IND-enabling work only if all Gate 1 criteria in Section 3 are met.

Independently of the asset decision, the Section 8 findings should go to QA/research-integrity review before any of these data are used externally (partnering, patents, regulators). The patterns are consistent with copy/paste and template errors. Some of them, such as integer-offset copies of computed values, are not typical of random error. **The cause is undetermined.**

---

## 2. How the asset looks (scorecard)

| Dimension | Assessment | Basis (block; evidence table) |
|---|---|---|
| Efficacy signal in aged mice | **Strong, if real** | 52/53 readouts favour PSLN-344 over PSLN-212. HAI ×8.0 [S03-C], IgG ×18.6 [S03-A], neutralisation ×9.2 [S03-D]. Survival 84% vs 12% (Tier A) (ET2, ET5) |
| Restoration toward young-animal response | **Partial to near-complete** | Median restoration index 0.72 across 43 readouts with a significant age gap. HAI 0.88–0.94; DC CD40/CD86 only 0.17–0.22. Survival vs young benchmark 81% vs 98% (ET7, ET5) |
| Mechanism of action | **Coherent; partly causal** | Supported by knockouts and blockers (SP-A/D KO, carbenoxolone, CCR2 antagonist, IFNAR⁻/⁻ chimeras, GM-CSF rescue, pertussis toxin). No STING-KO; no Mn-only arm (Section 5) |
| Attribution to CDN-1807 (our small molecule) | **Unproven** | No Mn-only or free-CDN arm anywhere in the dataset |
| Data integrity | **Failing** | 5 critical, 8 major, 7 minor findings. 1 of 18 survival blocks unflagged (ET8) |
| Safety | **Largely untested** | Weight nadir 96.4% vs 98.2% vaccine-only [S08-D]. No significant CNS innate activation at 36 h (nominal Tnf 1.54×), but one timepoint, n=5 [S10-A]. No Mn biodistribution, histopathology or repeat-dose data |
| CMC | **Immature** | Non-specific A260 EE assay (54.8 ± 5.1% for PSLN-344) [S08-B]. Size/zeta/TEM/stability described in the methods but absent from the data. Storage at −20 °C |
| Translatability | **High risk** | Female mice only. Inactivated whole virus at 0.5–1 µg HA. The mouse nasal dose reaches the alveoli, but a human nasal spray would not. No mucosal IgA or lung viral load measured |
| Commercial differentiation | **Potentially high** | Works in aged mice, protects across subtypes (H1/H3/H5), onset within 3 days. Requires co-administered antigen [S15-H] |

---

## 3. Next steps: what each study must establish, with endpoints and go/no-go criteria

*Reader's note:* F-numbers refer to the integrity findings in Section 8. Tiers A/B/C are the survival sensitivity pools defined in Section 7.2. Study thresholds are anchored to the effect sizes observed in our data, and the source of each is cited.

### Gate 0: source-data verification (≤8 weeks; QA-led; precondition for any further spend)
- **Must establish:** the pivotal blocks are genuine and correctly labelled.
- **Endpoints:**
  1. 100% of values in the pivotal blocks matched to raw instrument files (FCS, plate-reader, qPCR run files) and animal-room records. The pivotal blocks are S03-A–L, S06 (all), S13-A–J, S15 (all), S09-B–G, S11-A/B, S01-B and S08-C.
  2. A documented root cause and correct version for each of F01–F13.
  3. Identification of the unlabelled block S08!A89:D101.
  4. Colony health and necropsy reports for aged cohorts (background mortality 4/21; F08).
- **Kill:** any pivotal survival or titre block that cannot be sourced, or evidence of deliberate alteration.
- **In parallel (not data-dependent):** an IP and freedom-to-operate review of Mn²⁺-containing STING-agonist adjuvants. Mn²⁺ is the only thing that distinguishes PSLN-344 from PSLN-212, so the defensibility of the asset may rest on it.

### Gate 1A: independent, blinded, pre-registered replication in aged mice (≈4 months)
- **Must establish:** PSLN-344 protects aged mice better than PSLN-212, *and* CDN-1807 contributes beyond Mn²⁺, in both sexes.
- **Design:**
  - Aged (≥20 months) BALB/c, 12 males and 12 females per arm (n=24).
  - Power: 20–23 per arm gives 90% power for 60% vs 15% survival, half the observed Tier B gap. The extra animals cover background deaths.
  - Aichi H3N2 vaccine, then PR8 challenge at 5×LD50 on day 14 (the S06-A design).
  - Arms: vaccine + vehicle; vaccine + **Mn-liposome without CDN** (Mn-matched); vaccine + PSLN-212; vaccine + PSLN-344; young vaccine + PSLN-212 benchmark; unvaccinated, unchallenged aged controls.
  - **Commercial benchmark arm:** the same vaccine given intramuscularly with a squalene-in-water emulsion. This is a research analogue of the adjuvant already used in older-adult vaccines; its choice is external context.
- **Primary endpoint:** 14-day survival, with a pre-specified humane endpoint and no carrying forward of weights.
- **Secondary endpoints:** lung viral titre on days 3 and 5 (satellite cohorts; never measured to date); HAI and microneutralisation on day 14; IFN-γ ELISpot (NP/M1); lung resident-memory CD8 on day 25; lung histopathology.
- **Go criteria (all required):**
  - PSLN-344 survival ≥60% and ≥30 points above PSLN-212, with log-rank p<0.05. For reference, the Tier B observation was 80% vs 11%.
  - HAI GMT ratio PSLN-344/PSLN-212 ≥4. Observed was 8.0, with a lower 95% bound of 3.9 [S03-C].
  - PSLN-344 better than Mn-liposome (p<0.05) on survival or HAI.
  - Background mortality in unchallenged aged controls ≤10% (observed 19%).
  - *Differentiation readout, not a kill criterion at this stage:* PSLN-344 survival after the cross-subtype challenge should be at least equal to, and ideally better than, the intramuscular benchmark.
- **Kill:** Mn-liposome ≈ PSLN-344. In that case the asset is effectively a Mn²⁺ adjuvant, and the rationale for the CDN-1807 product and its IP must be re-examined. Also kill if there is no superiority over PSLN-212.

### Gate 1B: mechanism confirmation and biomarker qualification (≈4 months, in parallel)
- **Must establish:** STING dependence; whether the IFNAR/GM-CSF/CCR2 axis is needed for *protection*; an early biomarker that predicts outcome in individual animals.
- **Design:** Sting1-deficient, IFNAR⁻/⁻, anti-GM-CSF (or Csf2rb⁻/⁻) and CCR2 antagonist (or Ccr2⁻/⁻) arms. Use aged animals where obtainable, otherwise young animals plus aged wild type. Sample the same animals at 16–36 h, day 7 and day 14, then challenge.
- **Endpoints:** Ifnb1/ISG at 16 h; CCL2 and GM-CSF at 36 h; monocyte and moDC counts on days 3–4; ICOS-hi Tfh on day 7; HAI on day 14; survival.
- **Go criteria:**
  - Loss of ≥80% of PSLN-344's Ifnb1 induction and HAI advantage in STING-deficient mice.
  - An early composite (ISG + CCL2) with AUC ≥0.80 for predicting day-14 HAI at ≥4× the PSLN-212 GMT.

### Gate 1C: exploratory safety focused on Mn²⁺ and lung (≈3 months)
- **Must establish:** no Mn accumulation in the olfactory bulb or brain, no neuro-inflammation, and reversible lung effects in aged animals after one and two doses.
- **Endpoints:**
  - Mn by ICP-MS in olfactory bulb, striatum, cortex, lung and blood on days 1, 7 and 28. Comparators: vehicle, Mn-liposome, MnCl₂.
  - T1-weighted MRI of the olfactory bulb.
  - Histopathology of olfactory mucosa and bulb, brain, facial nerve and lung, with GFAP/Iba1 staining.
  - CNS Ifnb1, Tnf and Isg15 at 6 h, 36 h and 7 days. This follows up the nominal Tnf 1.54× signal [S10-A].
  - BAL neutrophils and cytokines through day 7. The second S09-A panel suggests Il6 7× and Tnf 8× persist at ~72 h (F07).
  - Serum IL-6, TNF and IFN-α at 4–24 h; body weight and temperature.
- **Go criteria:**
  - Mn in the olfactory bulb and brain on day 28 not above vehicle.
  - No neuropathology.
  - Lung findings minimal and resolved by day 14.
  - Weight nadir no worse than the current ≈96% [S08-D].

### Gate 1D: CMC feasibility (in parallel)
- **Must establish:** specific assays, a product that can reach the human lower airway, and acceptable stability.
- **Endpoints:**
  - A specific HPLC or LC-MS assay for CDN-1807, replacing A260 (F16), plus Mn content by ICP-MS and the Mn:CDN ratio.
  - Size, polydispersity and zeta potential (DLS), and TEM.
  - Encapsulation efficiency ≥ the current 55% with lot-to-lot CV ≤10% across 3 lots. The current value is 54.8 ± 5.1%, n=3 [S08-B].
  - Stability at 2–8 °C for ≥6 months (current storage is −20 °C).
  - Aerosol performance: mass median aerodynamic diameter 1–5 µm and ≥80% potency retained after aerosolisation (in-vitro IFN-β assay).

### Stage 2 (only if all of Gate 1 passes): IND/CTA-enabling
- GLP repeat-dose toxicology in two species, including local tolerance and CNS endpoints.
- Large-animal efficacy: a ferret cross-subtype challenge and an aged non-human-primate immunogenicity study with inhaled delivery. Benchmark against a licensed enhanced older-adult vaccine on HAI ratio, nasal IgA, IFN-γ ELISpot and viral shedding.
- A human-relevant antigen (split or recombinant HA) at the human dose.
- Durability to ≥6 months in *aged* animals. Today, aged durability is tested only to day 60 [S06]; 180-day data exist only in young animals [S09-F].
- A Phase 1 design with the Tier 1–4 biomarkers in Section 6.

---

## 4. Target demographic for the TAM check

The data define where the product is differentiated. Market research should size each segment separately, because confidence differs.

| Segment | Definition for TAM sizing | Supporting data | Confidence |
|---|---|---|---|
| **Core** | Adults **≥65** eligible for annual seasonal influenza vaccination. Report 65–74 and ≥75 separately | Aged mice: HAI restored to young level (368 vs 485, NS) [S03-C]; survival 84% vs 12% (Tier A) | Moderate, pending Gate 0/1 |
| High-value sub-segment | Long-term-care residents and **outbreak response** (protection needed within days) | Onset within 3 days: 5/7 vs 0/7 in the only unflagged experiment [S06-B]; 6/7 vs 0/7 [S15-H] | Low–moderate |
| Expansion | Adults **50–64** | 14-month mice: PSLN-212 0/14 vs PSLN-344 12/14 [S06-E, S06-F, rows 71–105] | Low (single design; weight flags F03) |
| Option value | **Pandemic preparedness (H5N1)** for older adults (government stockpiles) | H5N1 protection: 7/7 vs 2/7 [S06-C]; 5/7 vs 1/7 at day 60 [S06-F, rows 34–68]; 10/10 vs 3/10 against wild-type VN04 [S03-J]. All three blocks carry integrity flags | Low–moderate |
| Exclude | Under 50, including children | Young mice (7–8 weeks): no incremental benefit over PSLN-212 (8/8 vs 8/8) [S09-B, D, F]. The benefit is first documented at 14 months (middle age). The age-50 cut-off is therefore an extrapolation to be refined | — |

**Modelling assumptions for market research:**
- **The product is an adjuvant.** PSLN-344 alone does not protect (0/7) [S15-H]. Revenue depends on an adjuvanted vaccine, either through a partner or our own.
- **The human product is inhaled.** Model eligibility with and without people who cannot use an inhaled product or have severe chronic lung disease, since lung safety in elderly people with COPD is untested.
- **Immunocompromised people** are not studied.
- **Both sexes are assumed,** but the data are female-only.
- **Price and positioning** are set against the enhanced influenza vaccines preferred for older adults (high-dose, adjuvanted and recombinant products). No mucosal influenza vaccine is licensed for older adults today. *This is external context, not from our data; market research should verify it.*

---

## 5. Mechanism of action built from our data (Fig. 6)

All contrasts are aged PSLN-344 vs aged PSLN-212 unless stated. "RI" is the restoration index: the share of the aged-vs-young gap that is closed.

1. **Delivery to the alveolus.**
   - The liposome targets type II epithelial cells: AECII 15.8% vs AECI 3.8%, and 0.4% for free dye (p<10⁻⁵) [S01-B].
   - Alveolar macrophage uptake depends on SP-A/SP-D: 43.1% in wild type vs 12.7% in Sftpa1/Sftpd knockouts (−71%) [S01-C].
   - Whether Mn²⁺ changes uptake is unresolved (F06).
2. **STING–type I IFN, amplified by Mn²⁺.**
   - Ifnb1 at 16 h: 36.9× vs 16.5× (×2.2, 95% CI 1.9–2.7; p=10⁻⁵). This equals the young benchmark of 37.5× (RI 0.98) [S01-A].
   - The response is dose-dependent, with a ×3.6 advantage at 20 µg [S08-A].
   - By 72 h the formulations converge (×1.2, NS).
   - *STING dependence and CDN-1807's contribution versus Mn²⁺ are untested.*
3. **Paracrine amplification.**
   - Gap-junction blockade (carbenoxolone) cut recruited monocytes from 7.3% to 3.1% (p=0.003) [S11-C].
   - Chemokines at 16 h: Ccl2 590× vs 7.6× (×77), Ccl3 ×27, Ccl5 ×7.6 [S09-A].
   - Gm-csf at 36 h: 8.5× vs 1.6× (×5.4, p=4×10⁻⁵) [S02-F].
4. **CCR2⁺ monocyte recruitment.**
   - Lung monocytes on day 4: 30.6% vs 16.7% (young 32.2%, RI 0.89) [S01-D].
   - A CCR2 antagonist reduced monocytes 9.9% → 3.3% and Ly6C⁺ macrophages 15.4% → 2.5% [S07-B].
   - In young mice it also reduced GZMB⁺ CD8 cells from 6.8% to 1.4% [S02-I].
5. **Monocytes become monocyte-derived DCs rather than suppressive macrophages.**
   - moDC differentiation requires IFNAR: 19.7% in wild type vs 2.1% in IFNAR⁻/⁻ chimeras (−89%). GM-CSF rescues it to 12.4% [S02-H].
   - Adding GM-CSF to PSLN-212 raises moDC from 5.9% to 13.8% [S02-G].
   - Ly6C⁺CCR2⁺ macrophages on day 5: 3.4 vs 19.0 ×10⁵ (−82%) [S07-A].
   - CD206⁺ macrophages: 48.9% vs 71.5% (young 35.5%) [S11-E].
6. **DC migration and antigen transport.**
   - CCR7⁺ migratory DCs: 30.7% vs 7.3% [S02-A].
   - Antigen⁺ DCs in the mediastinal node: 7.1% vs 1.8%; pertussis toxin blocks this (2.4%) [S02-C].
   - cDC1: 37.5% vs 22.8% [S01-F].
   - *Residual defect:* CD40⁺/CD86⁺ DCs reach only 11.2/14.5% vs 38.7/37.9% in young animals (RI 0.17–0.22) [S02-D].
7. **Less regulation, more T-cell help.**
   - Tfr on day 7: 10.8% vs 26.7% [S04-B]; lung Treg: 3.0% vs 6.7% [S04-D].
   - ICOS-hi Tfh: 10.3% vs 3.8% [S04-A].
   - The Tfr difference is not significant by day 30 [S04-C].
8. **Germinal-centre and antibody output.**
   - GC B cells: 6.5% vs 2.3% [S03-K]; Aicda ×3.5 [S03-L].
   - HAI ×8–9 and IgG ×13–19 [S03].
9. **Cross-reactive CD8 and resident memory.**
   - IFN-γ⁺ CD8 recalled by a heterologous antigen, rgH5N1 vaccine (immunisation was H1+H3; recall likely targets conserved internal proteins): ×4 on day 14 and ×3 on day 60 [S05-F, S05-G].
   - Lung resident-memory CD8: ×4 [S05-I].
   - This arm plausibly explains protection across subtypes.
10. **Protection is antigen-dependent** [S15-H].

**What the data do *not* establish** (these items are Gate 1 work):
- STING dependence (no knockout);
- CDN-1807's contribution beyond Mn²⁺;
- whether GM-CSF, CCR2 or IFNAR are needed for *protection*, rather than only for intermediate cell readouts;
- AECII-intrinsic signalling;
- mucosal IgA;
- lung viral load;
- any individual-animal link between an early readout and a later outcome. Each readout came from a separate cohort.

---

## 6. Biomarkers to validate efficacy

| Tier (time after dose) | Biomarker: mouse readout → proposed human measure | Our evidence, aged PSLN-344 vs PSLN-212 | RI | Intended use |
|---|---|---|---|---|
| Target engagement (16–24 h) | Type I IFN: lung Ifnb1 → IFN-β and interferon-stimulated-gene score (e.g., ISG15, MX1, CXCL10) in nasal/airway lining fluid and blood | ×2.2 (1.9–2.7), Hedges g 5.6 [S01-A]; dose-responsive [S08-A] | 0.98 | Dose selection; confirm Mn²⁺ amplification; earliest Phase 1 go/no-go |
| Pathway (16–36 h) | CCL2 (MCP-1) and GM-CSF protein in airway fluid | Ccl2 ×77 [S09-A]; Gm-csf ×5.4 at 36 h [S02-F] | 0.84 (Ccl2) | Links IFN to monocyte recruitment. Candidate *pair* with the IFN score |
| Cellular (day 3–4) | Monocyte recruitment and CCR7⁺ DC → activated blood/nasal monocytes (exploratory in humans) | +13.8 pts [S01-D]; +23.4 pts [S02-A] | 0.84–0.89 | Mechanistic proof in animal studies |
| Early adaptive (day 7) | ICOS-hi Tfh, GC B, Tfr ↓ → circulating Tfh (ICOS⁺PD-1⁺CXCR5⁺) and plasmablasts | Tfh +6.4 pts [S04-A]; GC B +4.2 pts [S03-K]; Tfr −15.9 pts [S04-B] | 0.56–0.81 | Early predictor of antibody response |
| Immunogenicity (day 14–28) | HAI and microneutralisation titres | HAI ×8.0–9.2; neutralisation ×9.2 [S03-C, D, G, H]; aged PSLN-344 ≈ young | 0.88–0.94 | Regulatory-accepted strain-specific endpoint. Does **not** explain cross-subtype protection |
| Breadth (day 14–60) | IFN-γ⁺ CD8 to conserved antigens; lung resident-memory CD8 → IFN-γ ELISpot to NP/M1 peptides | +4.9 to +6.8 pts [S05-F, G]; resident-memory +3.0 pts [S05-I] | 0.59–0.63 | Correlate for cross-subtype protection |
| Mucosal antibody | Nasal/BAL IgA | **Not measured** | — | Must be added; core to a mucosal value proposition |
| Protection | Survival, weight loss, **lung viral load** | Survival only; viral load **not measured** | — | Animal efficacy; later human challenge or field study |

**Do not use as efficacy biomarkers (yet):**
- IgG2a:IgG1 ratio (F05);
- alveolar macrophage and neutrophil kinetics (F04);
- the Tfh:Tfr ratio, which is derived from Tfr (F18);
- Ifnb1 at 72 h (no separation: ×1.22, p=0.33) [S01-A];
- body weight (F03, F13).

**Qualification needed.** No biomarker can yet be shown to predict protection in an individual animal, because every readout came from a separate cohort. Gate 1B samples the same animals over time: airway fluid at 16–36 h, blood on day 7, serum on day 14, then challenge. The candidate to qualify is an early composite, **IFN/ISG score + CCL2 at 16–24 h**, predicting day-14 HAI and survival. The bar is an AUC of at least 0.80.

---

## 7. What the data show (efficacy)

### 7.1 Humoral and cellular immunogenicity (aged mice, day 14 unless stated)

| Readout [block] | PSLN-212 (aged) | PSLN-344 (aged) | PSLN-344 vs PSLN-212 | Young PSLN-212 benchmark |
|---|---|---|---|---|
| Serum IgG anti-CA09, GMT [S03-A] | 393 | 7,305 | ×18.6 (95% CI 9.1–37.9), p=1.3×10⁻⁵ | 11,959 |
| HAI anti-CA09, GMT [S03-C] | 46 | 368 | ×8.0 (3.9–16.4), p=3.7×10⁻⁴ | 485 (PSLN-344 vs young: ×0.76, 0.36–1.58, NS) |
| HAI anti-Aichi H3N2, GMT [S03-G] | 35 | 320 | ×9.2 (4.2–20.2), p=2.1×10⁻⁴ | 368 (×0.87, NS) |
| Neutralisation anti-CA09, GMT [S03-D] | 418 | 3,840 | ×9.2 (3.1–27.2), p=0.002 | 6,686 |
| IgG anti-CA09 d28 after boost, GMT [S13-I] | 4,411 | 15,651 | ×3.5 (1.5–8.4), p=0.010; Tukey p=0.19 | 40,739 |
| GC B cells, MLN d7 [S03-K] | 2.3% | 6.5% | +4.2 pts (2.3–6.1), p=0.002 | 9.8% |
| ICOS-hi Tfh, MLN d7 [S04-A] | 3.8% | 10.3% | +6.4 pts (2.6–10.3), p=0.009 | 13.6% |
| IFN-γ⁺ CD8, H5 restim., d14 [S05-F] | 1.5% | 6.4% | +4.9 pts (3.6–6.1), p=1.3×10⁻⁴ | 9.2% |
| IFN-γ⁺ CD8, H5 restim., d60 [S05-G] | 3.0% | 9.9% | +6.8 pts (3.4–10.3), p=0.003 | 14.4% |
| Lung resident-memory CD8, d25 [S05-I] | 1.0% | 4.0% | +3.0 pts (2.2–3.7), p=6×10⁻⁵ | 6.0% |

Notes:
- Geometric means for titres, arithmetic means for percentages. p = Welch t-test (log scale for titres). Results agree with the stated one-way ANOVA + Tukey unless noted (ET2).
- After a boost, aged PSLN-344 IgG is still only 0.29–0.38× the young benchmark (restoration index 0.57–0.66) [S13-I, S13-J].

### 7.2 Protection (aged mice; lethal challenge; n=7 per arm unless stated)

| Experiment [block] | Sham | PSLN-212 | PSLN-344 | Log-rank, 344 vs 212 | Integrity status |
|---|---|---|---|---|---|
| H3 vaccine → PR8 (H1N1), challenge d14 [S06-A] | 0/7 | 1/7 | 6/7 | p=0.008 | Weight companion reuses values (F03) |
| H3 vaccine → PR8, challenge d3 [S06-B] | 0/7 | 0/7 | 5/7 | p=0.0009 | **No flag detected** |
| Bivalent → rgH5N1, d14 [S06-C] | 0/7 | 2/7 | 7/7 | p=0.007 | Death count conflicts with weights (F02) |
| Bivalent → rgH5N1, d3 [S06-D] | 0/7 | 2/7 | 7/7 | — | **Void: copy of S06-C** (F01) |
| H3 → PR8, d60 [S06-E, rows 34–68] | 0/7 | 0/7 | 5/7 | p=0.002 | Conflicts with weights (F02) |
| Bivalent → rgH5N1, d60 [S06-F, rows 34–68] | 0/7 | 1/7 | 5/7 | p=0.009 | Weight companion reuses values (F03) |
| H1 → Perth (H3N2), d60 [S06-G] | 0/7 | 0/7 | 4/7 | p=0.015 | Unchallenged aged controls: 3/7 died (F08) |
| Bivalent → CA09 (homologous), d14 [S03-I] | 0/7 | 0/7 | 7/7 | p=0.0004 | Contradicted by S13-F weights (F02) |
| rgH5N1 vaccine → wild-type VN04 H5N1, d2 [S03-J] (n=10) | 1/10 | 3/10 | 10/10 | p=0.002 | n and weight conflicts (F02, F11) |
| C57BL/6 aged [S15-L] | 0/7 | 0/7 | 6/7 | p=0.001 | Weight companion reuses values (F03) |
| Swiss Webster aged [S15-N] | 0/7 | 2/7 | 6/7 | p=0.056 | Weight companion reuses values (F03) |

**Pooled PSLN-344 vs PSLN-212** (Mantel–Haenszel risk difference; stratified log-rank) (ET5):

| Pool | PSLN-344 | PSLN-212 | Risk difference | Stratified log-rank p |
|---|---|---|---|---|
| Tier A (all aged blocks above except S06-D) | 61/73 (84%) | 9/73 (12%) | +71 pts | 1.5×10⁻¹⁹ |
| Tier B (survival and weights agree) | 28/35 (80%) | 4/35 (11%) | +69 pts | 7×10⁻¹⁰ |
| Tier C (S06-B only) | 5/7 | 0/7 | +71 pts | 0.0009 |
| Day-60 durability [S06-E, S06-F (rows 34–68), S06-G] | 14/21 (67%) | 1/21 (5%) | +62 pts | 2×10⁻⁶ |

Context for interpreting these pools:
- **Durability and background deaths.** Unvaccinated, unchallenged aged controls survived 17/21 (81%) over the same 14-day windows [S06-E, S06-F (rows 34–68), S06-G] (F08). The 67% day-60 figure should be read against that background.
- **Young benchmark.** Across the blocks that include the young PSLN-212 benchmark, PSLN-344 in aged mice reached 51/63 (81%) vs 62/63 (98%) for young animals (stratified log-rank p=0.001). Restoration is therefore substantial but not complete.
- **Antigen is required.** With challenge 3 days after dosing, vaccine + PSLN-344 protected 6/7, vaccine alone 0/7, and PSLN-344 alone 0/7 (p=1.6×10⁻⁴) [S15-H]. PSLN-344 is an adjuvant, not a stand-alone prophylactic.
- **Middle-aged (14-month) mice.** PSLN-344 protected 12/14 naive animals vs 0/14 with PSLN-212 (p=5×10⁻⁶). In imprinted animals (prior sublethal PR8 infection) it protected 12/14 vs 4/14 (p=3×10⁻⁴) [S06-E, S06-F, rows 71–105]. The age-related failure of PSLN-212 is therefore already present at 14 months.
- **Young mice.** PSLN-344 adds nothing over PSLN-212 on survival in young animals: 8/8 vs 8/8 in all three young studies [S09-B, S09-D, S09-F].

### 7.3 Tolerability signals available
- **Body weight after vaccination (no challenge) [S08-D] (ET6):**
  - PSLN-344 nadir 96.4 ± 1.5% vs vaccine alone 98.2 ± 1.1% (p=0.065), with recovery to 99.8% by day 10.
  - The R848 combination (PSLN-212/R848) reached a nadir of 90.0 ± 5.0%, and one animal was missing by day 10.
- **CNS innate activation 36 h after an intranasal dose [S10-A]:**
  - PSLN-344 did not differ significantly from PBS or Sham after multiplicity correction (Tukey on the log scale: Ifnb1 p=0.50, Tnf p=0.12, Isg15 p=0.77).
  - The cholera toxin positive control raised Ifnb1 5.4× (p<0.001).
  - Tnf was nominally higher with PSLN-344 than PBS (1.54× vs 0.98× geometric means; unadjusted p=0.031). With n=5 and a single timepoint, this is a signal to follow up, not a clearance.
- **Lung cytokines:** the second S09-A panel (labelled 16 h but matching 72 h data; F07) shows lung Il6 7×, Tnf 8× and Ccl2 27× still present with PSLN-344 [S09-A]. Duration of lung inflammation in aged lungs is therefore a safety question to answer.

---

## 8. Why the data cannot be banked (integrity findings)

Full register with cell addresses: ET8. Supporting evidence: ET9–ET12 and Fig. 5.

| ID | Severity | Finding | Evidence |
|---|---|---|---|
| F01 | Critical | **S06-D (challenge 3 days after vaccination) is a cell-for-cell copy of S06-C (challenge at 14 days).** | 28/28 rows identical in all 4 groups (S06!M3:Q30 vs S06!A34:E61). Weights of the S06-D design [S15-D] imply 2/7 PSLN-344 and 2/7 young deaths, vs 0/7 recorded. |
| F02 | Critical | **Survival records contradict the weights of the same cohorts in 11 arms across 9 block pairs.** | S03-I records all 7 aged PSLN-212 mice dead on d5–6. S13-F ("the animals of S03-I") weighs all 7 on day 8 and shows 3 recovering. S13-F and S13-G also contain a "Naive" group absent from the survival blocks they are annotated to. |
| F03 | Critical | **Body-weight values reused across independent experiments.** | 32 distinct 4–8-significant-digit values recur in 68 cells, and 74 shared fractional "signatures" appear at the same animal and day, often with an integer offset. Examples: young BALB/c PSLN-344(Y) [S09-E] = young C57BL/6 PSLN-212(Y) [S15-M] on d6–14; the 3-day study's vaccine+PSLN-344 arm [S15-I] = the S15-C PSLN-344 arm (40/42 values, d2–12). |
| F04 | Critical | **Alveolar macrophage [S11-A] and neutrophil [S11-B] kinetics share 35/100 position-matched values.** | The comparison with NK cells [S11-D] gives 0–1/100. Chance probability ≈10⁻⁴⁶. |
| F05 | Critical | **IgG2a:IgG1 quotients [S03-B, S03-F] are the S13-A–D ratios with group labels rotated.** | Agreement ≤0.06%. By the S13 labels, PSLN-344 is IgG2a-skewed (2.14 vs 0.58 for PSLN-212); by the S03 labels, the reverse. |
| F06 | Major | S08-C (PSLN vs PSLN-344 epithelial uptake) shares values with S01-B; its middle columns are probably swapped. | As printed, AECI uptake of the same PSLN-SRB is 13.8% (vs 3.8% in S01-B), and Mn²⁺ would cut AECII uptake 4-fold. |
| F07 | Major | Second S09-A panel labelled 16 h matches the 72 h data. | r=0.999 with S01-A 72 h vs r=0.35 with 16 h. |
| F08 | Major | Unchallenged aged controls died. | 4/21 within 14 days, with flat weights [S06-E, S06-F (rows 34–68), S06-G]. |
| F09 | Major | Unlabelled data region S08!A89:D101. | Looks like time-to-event data (n=6 and n=7, all censored at day 14). Provenance unknown. |
| F10 | Major | Both groups in S07-C are labelled "Ly6C-CD206+ MΦ". | Macrophage→Treg transfer result cannot be assigned. |
| F11 | Major | Stated n ≠ observed n. | S03-J, S13-E, S05-A/B, S09-B/F. One S03-J PSLN-344 record has no day value. |
| F12 | Major | Antigen-specific CD8 assays do not fit the stated strain. | NP366 tetramer (H-2Dᵇ) used in BALB/c (H-2ᵈ) [S05-A/B]. OT-I cells co-cultured with BALB/c-derived DCs [S02-E]. |
| F13 | Major | Weights of dead animals carried forward to day 14. | Mean weight curves are biased. |
| F14–F20 | Minor | Ambiguous or incomplete records. | S10-A "mean ± SD"; missing timepoints (S07-B, S11-E, S13-H, S14-A); non-specific EE assay; undocumented "PSLN-344/R848"; Tfh:Tfr arithmetically derived from Tfr; duplicate S06 block labels; red-formatted empty cells. |

**What this means.** Everything we would cite to regulators or partners about protection touches at least one finding. This covers:
- the 3-day H5N1 claim (F01);
- the homologous and wild-type H5N1 survival (F02);
- all weight curves (F03, F13);
- the Th1-skew claim (F05);
- the cross-priming assays (F12).

Note: finding no flag is not the same as verifying a block. The low-precision titre and flow data cannot be forensically screened as well as computed weights can.

---

## 9. What was considered and ruled out

| Option or analysis | Decision | Reason (with data) |
|---|---|---|
| Advance to IND-enabling now | Ruled out | Critical integrity findings F01–F05; no Mn-only control; no safety package; non-specific CMC assays |
| Terminate today without verification | Not preferred; becomes the default if Gate 0 fails | The signal holds up when flagged blocks are excluded (Tier B 80% vs 11%; the only unflagged block 5/7 vs 0/7). Verification is cheap relative to the upside |
| Pivot to PSLN-212 (no Mn²⁺) | Ruled out | Fails in aged mice (pooled survival 12%; HAI GMT 46) and in 14-month mice (0/14) |
| Pivot to CMP-204 (cGAMP liposome) | Ruled out | Weaker than PSLN-344 in aged mice: HAI ×16 lower, IgG ×40 lower, Ifnb1 ×4.8 lower [S03-C, S03-A, S01-A]; survival 3/7 vs 7/7 [S03-I] |
| Add a TLR7/8 agonist (R848) | Ruled out | PSLN-212/R848: weight nadir 90%, one animal lost [S08-D]; Il10 ×179 and Tnf ×202 [S09-A]. R848 lowered PSLN-344's Ifnb1 from 45.5× to 29.0× at 20 µg (geometric means) [S08-A] |
| Stand-alone innate prophylactic (no antigen) | Ruled out | PSLN-344 alone 0/7 [S15-H] |
| Young adults or children | Ruled out | No incremental benefit [S09-B, D, F]; even cGAMP-liposome protects young mice 7/7 [S13-E] |
| Nasal-spray human presentation | Ruled out | Efficacy relies on alveolar targeting [S01-B, S01-C]; an inhaled product is required |
| Claim "full restoration to youth" | Ruled out | Median RI 0.72; CD40/CD86 RI 0.17–0.22; survival 81% vs 98% vs young; post-boost IgG 0.29–0.38× young |
| Claim aged durability beyond 60 days | Ruled out | Aged durability is tested only to day 60; 6-month data exist only in young mice [S09-F] |
| Treat CNS safety as cleared | Ruled out | One timepoint, n=5, annotated as summary statistics; no Mn measurement; nominal Tnf signal (1.54×, unadjusted p=0.031, Tukey p=0.12) [S10-A] |
| Use of flagged blocks as evidence | Excluded | S06-D, S11-A/B, S03-B/F, S08-C, S09-A panel 2, S07-C, S05-A/B, S02-E |
| Terminal-digit test as integrity evidence | Considered; not relied on | Non-uniform (p<0.001), but confounded by mixed instruments and rounding; not diagnostic |
| Identical Sham death-day vectors in S06-B and S06-F (rows 34–68) (4,4,4,5,5,6,6) | Considered; not counted as a flag | Consistent with chance, because Sham deaths cluster on days 4–6. S06-B therefore stays the unflagged reference block |
| Identical HAI/neutralisation vectors across blocks | Considered; not counted | Titres are discrete 2-fold dilutions, so matches are expected |

---

## 10. If we drop PSLN-344: what we give up, and why that can be acceptable

**What we would give up, as recorded and not yet verified:**
- **A fix for the age-related failure of our own CDN-1807 liposome.** In aged mice, PSLN-344 turns a failing adjuvant (PSLN-212: 12% pooled survival, HAI GMT 46) into a protective one (84%, HAI GMT 368). The PSLN-344 HAI is not significantly different from young animals given PSLN-212 (485).
- **Protection across subtypes** (H1→H3, H3→H1, H5N1), including at day 60 (67% vs 5%).
- **Onset within 3 days** (5/7 vs 0/7 in the unflagged S06-B).
- **Activity in three mouse strains** and in imprinted 14-month animals.
- **A benign short-term weight profile** (nadir 96.4%).
- **Positioning:** these results point to a differentiated mucosal adjuvant for older adults and for pandemic preparedness.

**Why dropping can be defended if Gate 0 or Gate 1 fails:**
- None of these numbers can currently be defended to regulators, partners or auditors. The pivotal survival evidence has integrity defects, and one key experiment is a duplicate (F01–F05).
- The benefit has not been attributed to our small molecule rather than Mn²⁺.
- The safety of repeated Mn²⁺ dosing to the airway and nose in older people, and the feasibility of an inhaled product, are unknown.

**What keeping it costs:** a QA-led audit (weeks), then one focused package of four parallel studies over about 6 months. IND-enabling spend stays frozen until the gates are passed.

---

### Appendix A: Methods summary
- **Data handling.** Every block was parsed by explicit cell range, yielding 2,121 per-animal continuous values, 527 time-to-event records and 3,472 body-weight values, each with its source cell (ET13–ET15).
- **Statistics.**
  - The stated methods: one-way ANOVA with Tukey HSD, two-way ANOVA (group × time), Student and Welch t-tests, log-rank.
  - Robustness checks: Mann–Whitney, Fisher exact, Kaplan–Meier, Hedges' g.
  - Pooling: Mantel–Haenszel / CMH and a log-rank stratified by experiment.
  - Titres and fold-changes were analysed on the log scale. HAI values below the 1:10 limit of detection were set to 5.
  - S03-J: one PSLN-344 record has an event flag of 0 but no day value (S03!J46). It is counted as a survivor in proportions and excluded from the log-rank test.
- **Verification.** The log-rank implementation was checked against `lifelines` (maximum |Δp| = 3×10⁻¹⁶).
- **Restoration index.** (PSLN-344 aged − PSLN-212 aged) / (PSLN-212 young − PSLN-212 aged), computed only where the young-vs-aged gap is significant (Welch p<0.05; 43 readouts).
- **Integrity screens.**
  - Position-matched identity tests between blocks.
  - Recurrence of high-precision values and of sub-0.1 fractional signatures in computed body weights.
  - Survival vs weight concordance (deaths inferred from records that stop, or from constant carried-forward values).
  - Re-computation of derived quantities.
  - Label and timepoint cross-checks against related blocks.
- **Code.** All analysis code is in `code/` and reproduces every table and figure.

### Appendix B: Figures (full-size, Appendix C; PNG files in `figures/`)
- Fig. 1: effect sizes for PSLN-344 vs PSLN-212 across all readouts.
- Fig. 2: restoration index.
- Fig. 3: survival curves by experiment, with integrity flags.
- Fig. 4: pooled survival by sensitivity tier.
- Fig. 5: integrity evidence.
- Fig. 6: mechanism-of-action schematic.
- Fig. 7: tolerability and safety readouts.
