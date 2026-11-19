# PSLN-344: portfolio review proposal
*Intranasal STING-agonist adjuvant (CDN-1807 + Mn²⁺ in a pulmonary-surfactant-biomimetic liposome) for influenza vaccination of older adults*

Prepared for the Portfolio Review Committee · Data cut: 1 November 2026 · Sources: *psln_program_dataset.xlsx* (sheets S01–S15) and *psln_program_annotation.pdf* (19 pp.) · All analyses are reproducible from the Python scripts in *analysis/*.

**How to check a number.** Bracketed codes such as [S03-C] are workbook blocks. Claim IDs in the form (E12) point to the claims sheet of *PSLN-344_evidence_ledger.xlsx*, which gives the exact cell range, groups, n, statistic and analysis file. Statistics: group mean ± SD (n = 5 per group unless stated); GM = geometric mean (titres and qPCR fold-changes). Comparisons are Welch t-tests on the log₂ scale for titres and fold-changes and on the raw scale for percentages; Tukey HSD (the method stated in the annotation) is also tabulated in the ledger. Survival: log-rank and Fisher exact tests per experiment, plus an exact stratified test pooled across experiments. "Aged" means female BALB/c ≥20 months and "young" means 7–8 weeks (annotation p.1), unless a block states otherwise.


## 1. Recommendation
> **Direct answer: on paper the asset looks scientifically promising, but it cannot be invested in on this data package. Keep it in the portfolio only as a frozen, gated asset, not as an active development programme. If we had to choose today between advancing and dropping, we would drop.**  
>   
> **Recommendation: HOLD. Do not advance PSLN-344 on the current data package.** Freeze development spend and fund only a time-boxed verification path. The default outcome is **termination** unless both gates below are passed.  
>   
> **Gate A (months 0–3): independent forensic audit** of the raw records behind the efficacy case. Pass = every critical finding is traced to contemporaneous raw data with a documented benign cause, and the corrected data keep the PSLN-344 > PSLN-212 direction. Fail = terminate and refer to the research-integrity process.  
> **Gate B (months 3–9, only if A passes): one independent, blinded, randomised confirmatory study in aged mice at a CRO.** It adds the missing CDN-free Mn²⁺-liposome control, a standard-of-care benchmark, mucosal IgA and within-animal correlates. It runs alongside a Mn²⁺/CNS safety package and a minimum CMC definition. Pre-specified pass criteria are in Section 2.  
> **Decision back to committee at about 9 months.** Translational or IND-enabling spend only if A and B both pass.

**Why we cannot advance today**

- **Data integrity.** Several findings are inconsistent with contemporaneous recording. Animal weight trajectories are duplicated across different experiments: 18 cross-experiment animal pairs share ≥4 identical live readings, against 0.005 expected by chance (I01). Two different survival experiments have identical records (S06-C = S06-D; I02). Two different cell types share 35 of 100 position-matched values (S11-A vs S11-B; 0.85 expected; I03). Appendix A lists 5 critical, 8 major and 10 minor findings. Several headline claims rest on affected blocks: onset of protection within 2–3 days, protection in C57BL/6 and Swiss Webster mice, and 180-day durability.
- **Attribution and benchmark gaps.** No block tests a CDN-free Mn²⁺-liposome, so the benefit cannot be attributed to our proprietary molecule (CDN-1807) rather than to Mn²⁺. Nothing is compared with the parenteral enhanced vaccines that older adults receive today. Mucosal IgA, the reason for an intranasal product, was never measured. *(External context, not our data: Mn²⁺ potentiation of cGAS–STING signalling and Mn-based adjuvants are described in the published literature, so a Mn-only effect would weaken our proprietary position. IP counsel to confirm.)*
- **Unaddressed class-specific safety.** The product delivers Mn²⁺ intranasally to an elderly population. The only CNS data are three transcripts at one time point in an unspecified CNS region [S10-A]. There are no Mn biodistribution, histopathology, neurobehavioural or repeat-dose data.

**Why we should not drop outright today**

- **The unflagged immunology blocks are coherent and the effects are large.** In aged mice, lung Ifnb1 at 16 h is restored to the young level: 37.1 ± 4.8-fold vs 16.6 ± 2.1-fold with PSLN-212; young 37.6 ± 3.5 (E01). HAI GMT is 368 vs 46 against H1N1 and 320 vs 35 against H3N2 (E02). Across 32 unflagged read-outs, PSLN-344 closes a median 71% (IQR 60–80%) of the aged-vs-young deficit (E03, Figure 2).
- **The survival advantage over the Mn-free formulation holds in every sensitivity scenario.** It is 65–71 percentage points in every scenario we built, including removing the duplicated experiment and using the less favourable of the survival and weight records. With S06-D removed, pooled survival is 85/101 vs 13/101 (E04, Figure 3).
- **The audit is needed in any case** under our data-governance obligations. One confirmatory study costs far less than the option value if the effect is real.

> **If the committee decides to drop now: what we give up, and why (statement for the record).**  
> *"We are forgoing an intranasal adjuvant concept. In its unflagged internal data in aged mice, it closed most of the age-related immune deficit (median 71% across 32 read-outs), gave 8–9-fold higher HAI titres than the Mn-free formulation, and induced cross-reactive CD8 T-cell immunity to H5N1. If verified, mucosal and heterosubtypic immunity would set it apart from today's parenteral, strain-matched vaccines for older adults. We are dropping it because the package cannot be relied upon. It contains records duplicated across experiments that must be resolved before any use. It does not show that the benefit needs our proprietary molecule rather than Mn²⁺. It has no benchmark against the standard of care. And the safety of intranasal Mn²⁺ in the elderly has not been characterised."*

**Table 0. What PSLN-344 would be worth if verified, and how much of it is verified today**

| Value driver | Our data (aged mice unless stated) | Verification status |
|---|---|---|
| Restores innate STING output in aged lung | Ifnb1 16 h 37.1 ± 4.8 vs 16.6 ± 2.1-fold; young 37.6 ± 3.5 [S01-A] (E01) | No integrity flag |
| Humoral immunogenicity in aged | IgG GMT 7,305 vs 393 (H1N1); HAI GMT 368 vs 46 [S03-A/C/G] (E02, E12a–E12e) | No integrity flag |
| Cross-reactive (heterosubtypic) CD8 immunity | H5N1-restimulated IFN-γ⁺ CD8 6.4 ± 1.0 vs 1.5 ± 0.4% (d14); 9.9 ± 2.8 vs 3.0 ± 1.3% (d60) [S05-F/G] (E13a, E13b) | No integrity flag |
| Heterosubtypic protection | PR8 / H5N1 / Perth challenges: PSLN-344 4–7/7 vs PSLN-212 0–2/7 [S06-A to G] (E17) | Mixed: S06-B clean; S06-C/D critical; S06-A/G major |
| Durability (aged, day 60) | 5/7, 5/7, 4/7 vs 0/7, 1/7, 0/7 [S06-E/F/G] | Minor / moderate / major (sentinel deaths) |
| Works after prior infection (imprinting) | PSLN-344 6/7 in naive and imprinted 14-month mice [S06-E′/F′] | Moderate |
| Rapid onset (2–3 days) | H5N1 at d2: 10/10 vs 3/10 [S03-J]; d3: 6/7 vs vaccine alone 0/7 [S15-H] | Major / critical |
| Generalises across mouse strains | C57BL/6 6/7 vs 0/7 [S15-L]; Swiss Webster 6/7 vs 2/7 [S15-N] | Critical / major |
| Dose-sparing | ≈7–8 µg PSLN-344 matches PSLN-212 at 20–40 µg on Ifnb1 [S08-A] (E05) | No integrity flag (PD only) |
| Tolerability | Post-vaccination weight nadir 96.4% [S08-D]; no CNS ISG rise vs Sham at 36 h [S10-A] | No integrity flag, but very limited |


## 2. Next steps: what each study must establish, and its endpoints
This section comes straight after the recommendation because it is the decision the committee is asked to fund. The evidence behind it follows in Sections 3–8. Integrity-finding IDs (C1–C5, M1–M8, m1–m10, S1) are defined in Section 4 and Appendix A.

**Rule used to set thresholds.** Each go criterion requires the replication to reach at least half of the effect we observed, on the log scale. For example, an observed 8.0× HAI ratio requires ≥2.8× in the replication. This allows for the optimistic effect sizes typical of small first studies (Hedges g 2–9 here, soft signal S1). Sample sizes come from our own variance with the SD inflated 1.5× (design_power_*.csv).

| Study (timing) | What it must establish | Design essentials | Endpoints and go criteria (anchored to our data) | Stop if |
|---|---|---|---|---|
| A. Forensic data audit (months 0–3; QA, independent of project team) | The efficacy case rests on contemporaneous, traceable raw data (ALCOA+). | Retrieve balance logs with animal IDs, mortality/humane-endpoint logs, FCS files, plate-reader and qPCR exports, randomisation records. Cover every block cited here. | All 5 critical and 8 major findings explained with documents; original vs copy identified for each duplicated trajectory (C1); S06-C/S06-D mortality logs (C2); FCS re-analysis of S11-A/B and S01-B/S08-C (C3, C5); strain confirmed for S02-E, S05-A/B (M4); labels corrected (M1, M2, M6, m3); S08 orphan region identified (M7). Corrected data keep PSLN-344 > PSLN-212 in every affected block. | Any critical finding not traceable to raw data; any evidence that values were generated rather than measured → terminate and refer. |
| B1. Independent confirmatory efficacy and attribution study in aged mice (months 3–9; CRO, blinded, randomised, pre-registered analysis plan) | (a) The Mn-dependent effect reproduces in an independent laboratory; (b) the benefit needs CDN-1807, not Mn²⁺ alone; (c) performance vs standard-of-care approaches; (d) within-animal correlates of protection. | ≥20-month BALB/c and C57BL/6, both sexes. Split/subunit HA antigen as well as whole inactivated virus. Arms: Sham; PSLN-212; PSLN-344; CDN-free Mn-liposome; free CDN-1807 + MnCl₂; i.m. squalene-emulsion-adjuvanted vaccine; i.m. high-dose (4× HA); young PSLN-212; unvaccinated, unchallenged aged sentinels. Immunogenicity n = 12 per arm per sex (≥90% power for half the observed HAI effect with SD ×1.5: n = 11–13). Challenge n = 20 per arm over two independent runs (power 0.85 for 70% vs 20%). | HAI GMT d28 ≥2.8× (H1N1) and ≥3.0× (H3N2) vs PSLN-212 (observed 8.0×/9.2×) [S03-C/G]; IgG ≥4.3× (H1N1) and ≥3.7× (H3N2) (observed 18.6×/13.4×) [S03-A/E]. Attribution: PSLN-344 ≥2× HAI GMT over CDN-free Mn-liposome and better survival. SoC: PSLN-344 HAI GMT not below i.m. benchmark (ratio ≥1.0, lower 95% bound ≥0.5) and nasal IgA ≥4× the i.m. benchmark. NP/M1 IFN-γ ≥2× (observed 4.2×) [S05-F]. Heterosubtypic challenge (d28; d90 subset): PSLN-344 survival ≥60% and ≥35 points above PSLN-212 (observed 84% vs 13%); lung virus d3/d5 ≥1 log₁₀ lower. PD: Ifnb1 16 h ≥1.5× (observed 2.23×, CI 1.85–2.69) [S01-A]; Csf2 36 h ≥2.3× (observed 5.4×) [S02-F]. Correlates: ≥1 pre-specified pre-challenge marker with AUC ≥0.75 for individual survival. | Any primary criterion missed; or CDN-free Mn-liposome equivalent to PSLN-344 (value would then sit in Mn²⁺, not CDN-1807 → IP/strategy review, likely terminate). |
| B2. Mn²⁺ and STING safety package in aged animals (months 3–9, parallel) | Intranasal PSLN-344 does not deliver Mn²⁺ to the CNS at levels of concern, causes no olfactory, facial-nerve or neurobehavioural toxicity, and has acceptable lung and systemic reactogenicity, including after repeat dosing. | Single dose and 3 doses (2-week interval), aged rodents, vehicle and CT controls; ICP-MS Mn in olfactory bulb, striatum, globus pallidus and cerebellum at 24 h, 7 d and 28 d; T1-weighted MRI subset; histopathology of nasal cavity, olfactory bulb, trigeminal/facial nerve and ganglia, and lung at d1, d3, d7 and d28; BAL; serum cytokines; neurobehaviour at d28. | Mn per dose defined. Olfactory-bulb Mn back to vehicle level by d28 and no basal-ganglia rise at any time (equivalence margin agreed with Toxicology). No histopathology above minimal persisting to d28. No neurobehavioural difference vs vehicle. CNS ISG/Tnf in olfactory bulb at 6 h–7 d not different from vehicle, with CT positive (our 36 h data: Tnf 1.20× vs Sham) [S10-A]. Lung Tnf back to baseline by d7 (our data: about 8× at 72 h in aged vs 0.5× young) [S09-A]. Weight nadir ≥95% (observed 96.4%) [S08-D]. | CNS Mn persisting at d28; any neurobehavioural or facial-nerve finding; non-resolving lung pathology. |
| B3. CMC minimum product definition (months 3–9, parallel) | A defined, reproducible, stable product with a dose unit that can be translated. | 3 consecutive batches; define the Mn:CDN ratio; release assays (DLS size/PDI/zeta and TEM are described in the annotation but no data are in the package). | Dose stated as µg CDN-1807 and µg Mn²⁺. EE ≥80% (current 54.8 ± 5.1%) [S08-B], or justification for free CDN. Lyophilised (2.5% trehalose) stability at 2–8 °C and −20 °C for ≥6 months: potency (Ifnb1-induction ED50 within 2× of fresh, S08-A as reference curve) and EE within 10% of release. | Cannot reach stable, reproducible EE and potency. |
| C. Translational bridge (months 9–18; only if A and B pass) | The effect survives human-relevant delivery (nasal-spray device, upper-airway deposition) and a second species with human-like influenza disease. | Ferret heterosubtypic challenge and transmission (aged if available). Aged NHP immunogenicity with the clinical nasal device, including deposition imaging. | Ferret: nasal-wash virus AUC ≥1 log₁₀ lower than i.m. benchmark, clinical score, HAI, nasal IgA. NHP: nasal ISG/GM-CSF/CCL2 ≥2× vehicle at 24–48 h (PD bridge to S01-A/S02-F); cTfh d7; HAI GMT not below i.m. benchmark with superior nasal IgA; NP/M1 ELISpot; olfactory safety; Mn in plasma/CSF. | No nasal PD signal, or no mucosal advantage over the i.m. benchmark. |
| D. IND-enabling (month 18 onwards) | Regulatory safety package. | GLP repeat-dose intranasal toxicity in two species with Mn toxicokinetics, local tolerance, CNS safety pharmacology. | Per ICH and regulatory guidance for vaccine adjuvants. | Standard toxicology stop rules. |

**Decision points.** Month 3: Gate A (audit), go or terminate. Month 9: Gate B (B1–B3), advance to C or terminate. Month 18: Gate C, advance to IND-enabling or terminate. Only Study A and the design work for B are funded before the month-3 decision.


## 3. What the data show

### 3.1 Asset and comparators
From the annotation (p.1): **PSLN-344** is the STING agonist CDN-1807 in a DPPC/DPPG/DPPE-PEG2000/cholesterol liposome, with Mn²⁺ incorporated by coordination polymerisation. **PSLN-212** is identical except that it has no Mn²⁺. It is the decisive comparator, because it isolates the contribution of Mn²⁺. **CMP-204** carries cGAMP instead of CDN-1807. R848-containing variants also appear. "**Sham**" is empty liposome given with the vaccine. All products were given intranasally at 20 µg adjuvant per animal with formalin-inactivated whole-virus vaccine (CA09 H1N1 0.5 µg HA; Aichi H3N2 1 µg HA). The BALB/c animals were female (annotation p.1); sex is not stated for the other strains.


### 3.2 Immunogenicity in aged mice: large, consistent, mechanistically connected
**Table 1. PSLN-344 vs the Mn-free formulation in aged mice (blocks with no integrity flag; n = 5 per group).**

| Read-out [block] | Sham | PSLN-212 | PSLN-344 | PSLN-212 young | PSLN-344 vs PSLN-212 (95% CI); p | RI* |
|---|---|---|---|---|---|---|
| Lung Ifnb1 16 h, fold (GM) [S01-A] (E06) | 0.9 | 16.5 | 36.9 | 37.5 | 2.2× (1.8–2.7); p<0.001 | 0.98 |
| Lung Csf2 (GM-CSF) 36 h, fold (GM) [S02-F] (E07) | 1.2 | 1.6 | 8.5 | – | 5.4× (3.9–7.3); p<0.001 | – |
| Lung monocytes day 4, % [S01-D] (E08) | 10.4 ± 0.6 | 16.7 ± 1.6 | 30.6 ± 4.7 | 32.2 ± 3.9 | +13.8 pts (+8.1 to +19.5); p=0.002 | 0.89 |
| Lung cDC1 72 h, % [S01-F] (E09) | 17.9 ± 2.5 | 22.8 ± 3.6 | 37.5 ± 7.0 | 43.4 ± 5.3 | +14.7 pts (+6.1 to +23.3); p=0.006 | 0.71 |
| Lung CCR7⁺ migratory CD11b⁺ DC 72 h, % [S02-A] (E10a) | 2.5 ± 0.7 | 7.3 ± 2.0 | 30.7 ± 7.9 | 35.0 ± 4.8 | +23.4 pts (+13.8 to +33.0); p=0.002 | 0.84 |
| MLN antigen⁺ DC 36 h, % [S02-C] (E10b) | – | 1.8 ± 0.4 | 7.1 ± 1.4 | 9.4 ± 1.5 | +5.3 pts (+3.6 to +7.1); p<0.001 | 0.70 |
| MLN CD40⁺ CD11b⁺ DC day 3, % [S02-D] (E10c) | 4.0 ± 1.0 | 5.6 ± 1.1 | 11.2 ± 3.0 | 38.7 ± 7.3 | +5.6 pts (+2.0 to +9.3); p=0.01 | 0.17 |
| MLN ICOS-hi Tfh day 7, % [S04-A] (E11a) | 0.3 ± 0.2 | 3.8 ± 0.9 | 10.3 ± 3.2 | 13.6 ± 1.6 | +6.4 pts (+2.6 to +10.3); p=0.009 | 0.66 |
| MLN Tfr (Foxp3⁺) day 7, % [S04-B] (E11b) | 22.6 ± 4.4 | 26.7 ± 6.7 | 10.8 ± 1.8 | 7.1 ± 3.7 | -15.9 pts (-24.0 to -7.7); p=0.005 | 0.81 |
| MLN germinal-centre B day 7, % [S03-K] (E11c) | 1.2 ± 0.4 | 2.3 ± 0.5 | 6.5 ± 1.5 | 9.8 ± 3.1 | +4.2 pts (+2.3 to +6.1); p=0.002 | 0.56 |
| Serum IgG anti-H1N1 d14, GMT [S03-A] (E12a) | 56 | 393 | 7,305 | 11,959 | 18.6× (9.1–37.9); p<0.001 | 0.86 |
| Serum IgG anti-H3N2 d14, GMT [S03-E] (E12b) | 52 | 426 | 5,701 | 13,855 | 13.4× (6.1–29.6); p<0.001 | 0.75 |
| HAI anti-H1N1 d14, GMT [S03-C] (E12c) | 7.6 | 46 | 368 | 485 | 8.0× (3.9–16.4); p<0.001 | 0.88 |
| HAI anti-H3N2 d14, GMT [S03-G] (E12d) | 10 | 35 | 320 | 368 | 9.2× (4.2–20.2); p<0.001 | 0.94 |
| Neutralising anti-H1N1 d14, GMT [S03-D] (E12e) | 52 | 418 | 3,840 | 6,686 | 9.2× (3.1–27.2); p=0.002 | 0.80 |
| IFN-γ⁺ CD8, H5N1 restim. d14, % [S05-F] (E13a) | 0.7 ± 0.4 | 1.5 ± 0.4 | 6.4 ± 1.0 | 9.2 ± 0.9 | +4.9 pts (+3.6 to +6.1); p<0.001 | 0.63 |
| IFN-γ⁺ CD8, H5N1 restim. d60, % [S05-G] (E13b) | 1.5 ± 1.1 | 3.0 ± 1.3 | 9.9 ± 2.8 | 14.4 ± 2.9 | +6.8 pts (+3.4 to +10.3); p=0.003 | 0.60 |
| Lung TRM CD8 d25, % [S05-I] (E13c) | 0.6 ± 0.3 | 1.0 ± 0.4 | 4.0 ± 0.6 | 6.0 ± 0.6 | +3.0 pts (+2.2 to +3.7); p<0.001 | 0.59 |
| Lung GZMB⁺ CD8 d3, % [S05-E] (E13d) | 1.0 ± 0.4 | 3.0 ± 0.8 | 5.7 ± 0.9 | 9.6 ± 1.2 | +2.7 pts (+1.5 to +3.9); p=0.001 | 0.41 |

*RI (restoration index) = (PSLN-344 aged − PSLN-212 aged) / (PSLN-212 young − PSLN-212 aged), computed on the log₂ scale for titres and fold-changes. 1 = young level; 0 = no better than PSLN-212. Percentages are mean ± SD; effects for percentages are differences in percentage points. Csf2 has no young group. HAI values recorded as 0 (<1:10) were set to 5.

![Figure 1. Selected read-outs from blocks without integrity flags (dots = animals).](figures/fig1_key_efficacy_readouts.png)

![Figure 2. Fraction of the aged-vs-young deficit closed by PSLN-344 across 32 unflagged read-outs (median 0.71, IQR 0.60–0.80) (E03).](figures/fig2_restoration_index.png)


### 3.3 Where PSLN-344 does not restore youth, and where it adds nothing
- **DC co-stimulation stays largely aged.** CD40⁺ DC are 11.2 ± 3.0% with PSLN-344 vs 38.7 ± 7.3% in young mice (RI 0.17). CD86⁺ DC are 14.5 ± 2.7% vs 37.9 ± 5.5% (RI 0.22) [S02-D] (E14).
- **Titres remain below young.** IgG GMT is 0.61× (p=0.11) and 0.41× (p=0.04) of young for H1N1 and H3N2 [S03-A/E]. After a boost it is 0.38× and 0.29× of young [S13-I/J]. Early lung GZMB⁺ CD8 reach RI 0.41 [S05-E].
- **There is an inflammatory overshoot in aged lung (a reactogenicity flag).** At 16 h, Tnf is 40.5-fold with PSLN-344 vs 13.9-fold in young (ratio 2.9×, p=0.009). Il10 is 7.3- vs 1.8-fold (p=0.02). In the panel that is printed as 16 h but matches the 72 h data, Tnf is 8.4- vs 0.48-fold (p=0.008) [S09-A] (E15).
- **In young mice, Mn²⁺ adds little.** Ifnb1 is 1.34× (p=0.009), antigen⁺ MLN DC 1.18× (p=0.14), OT-I priming 1.20× (p=0.26) and cDC1 1.02× (p=0.75). Young survival is 8/8 vs 8/8 in all three young challenge studies [S09-B/D/F], and in young mice even the cGAMP formulation protected 7/7 against homologous H1N1 [S13-E] (E16). The differentiation is therefore specific to aged animals, and so is the target population.


### 3.4 Protection: the direction is robust, the magnitude is not verified
**Table 2. Survival at the end of observation, by experiment (aged or middle-aged animals).**

| Experiment [block] | Vaccine; challenge | PSLN-344 | PSLN-212 | Sham | log-rank p (344 vs 212) | Integrity |
|---|---|---|---|---|---|---|
| [S03-I] | Bivalent; 10× H1N1 homologous, d14 | 7/7 | 0/7 | 0/7 | <0.001 | major |
| [S03-J] | rgH5N1; WT H5N1 at d2 (age not stated) | 10/10 | 3/10 | 1/10 | 0.001 | major |
| [S06-A] | H3N2; PR8 H1N1 d14 | 6/7 | 1/7 | 0/7 | 0.008 | major |
| [S06-B] | H3N2; PR8 H1N1 d3 | 5/7 | 0/7 | 0/7 | <0.001 | none detected |
| [S06-C] | Bivalent; rgH5N1 d14 | 7/7 | 2/7 | 0/7 | 0.007 | critical |
| [S06-D] | Bivalent; rgH5N1 d3 | 7/7 | 2/7 | 0/7 | 0.007 | critical |
| [S06-E] | H3N2; PR8 H1N1 d60 | 5/7 | 0/7 | 0/7 | 0.002 | minor |
| [S06-F] | Bivalent; rgH5N1 d60 | 5/7 | 1/7 | 0/7 | 0.009 | moderate |
| [S06-G] | H1N1; Perth H3N2 d60 | 4/7 | 0/7 | 0/7 | 0.02 | major |
| [S15-L] | Bivalent; aged C57BL/6 | 6/7 | 0/7 | 0/7 | 0.001 | critical |
| [S15-N] | Bivalent; aged Swiss Webster | 6/7 | 2/7 | 0/7 | 0.06 | major |
| [S06-E′] 14-mo; PR8 | naive / imprinted | 6/7 / 6/7 | 0/7 / 4/7 | – | 0.002 / 0.23 | moderate |
| [S06-F′] 14-mo; Perth H3N2 | naive / imprinted | 6/7 / 6/7 | 0/7 / 0/7 | – | <0.001 / <0.001 | moderate |
| [S15-H] | Given 3 d before H5N1 | vaccine+PSLN-344 6/7 | vaccine alone 0/7 | PSLN-344 alone 0/7 | <0.001 (vs vaccine) | critical (C1) |

For S15-H the three columns hold vaccine + PSLN-344, vaccine alone and PSLN-344 alone. S03-J follow-up ran to day 21; all others to day 14. Integrity flags are explained in Section 4 and Appendix A.

| Pooled analysis (stratified by experiment) | PSLN-344 | PSLN-212 | Difference (MH, pts) | Exact stratified p |
|---|---|---|---|---|
| A. All aged/middle-aged strata as recorded | 92/108 (85%) | 15/108 (14%) | 71 | 8.0e-29 |
| B. As recorded, S06-D removed (exact duplicate of S06-C) | 85/101 (84%) | 13/101 (13%) | 71 | 6.4e-27 |
| C. Worst case: S06-D removed + weight-implied counts least favourable to PSLN-344 | 85/101 (84%) | 17/101 (17%) | 67 | 4.6e-24 |
| D. Strictly >=20-month strata only (excl. S03-J age unstated, S06-E/F' 14-mo), S06-D removed, worst case | 51/63 (81%) | 10/63 (16%) | 65 | 2.4e-14 |
| E. Strata with no critical/major integrity flag only (S06-B, S06-E, S06-F, S06-E', S06-F') | 39/49 (80%) | 6/49 (12%) | 67 | 6.3e-12 |
| F. Single stratum with no integrity flag detected (S06-B) | 5/7 (71%) | 0/7 (0%) | 71 | 1.0e-02 |

- **The direction is robust.** PSLN-344 beats PSLN-212 in every aged experiment. The pooled advantage is 65–71 points in every scenario, including scenario F (the only experiment with no integrity flag, S06-B: 5/7 vs 0/7, p=0.010).
- **Frailty confounds the model.** Unvaccinated, unchallenged aged sentinels died during the 14-day windows: 4/21 (19%; 95% CI 5–42%) [S06-E/F/G] (E18). In S06-G, sentinel survival (4/7) equals PSLN-344 survival (4/7). Future aged studies need sentinel arms and larger n.
- **Protection requires antigen.** PSLN-344 given alone 3 days before H5N1 challenge protected 0/7 animals, compared with 6/7 when given with vaccine [S15-H]. It is not a stand-alone antiviral, although this block is itself affected by C1.
- **Imprinting does not blunt PSLN-344.** Survival was 6/7 in both naive and previously infected 14-month-old mice [S06-E′/F′]. This matters for older adults with lifelong exposure.

![Figure 3. Per-experiment survival with integrity flag (left) and pooled sensitivity analyses (right) (E04, E17).](figures/fig3_survival_strata_sensitivity.png)


### 3.5 Tolerability and safety: what exists and what does not
- **Systemic tolerability after vaccination [S08-D].** The mean per-animal weight nadir was 96.4% with PSLN-344 (lowest animal 94.2%), similar to vaccine alone (98.2%). With PSLN-212/R848 it was 90.0% (lowest 84.7%), and one animal was missing by day 10 (T01).
- **CNS at 36 h [S10-A].** Compared with Sham, PSLN-344 changed Ifnb1 1.14×, Tnf 1.20× and Isg15 1.08× (all p≥0.36). Cholera toxin raised them 4.8×, 2.6× and 2.5× (p≤0.002). Against buffer (PBS), PSLN-344 Tnf was 1.57× (p=0.033), and the empty vehicle contributes part of this (T02). This is encouraging but narrow: one time point, three transcripts, unspecified CNS region, no Mn measurement.
- **Not in the package:** Mn²⁺ content per dose; Mn biodistribution (olfactory bulb, basal ganglia); nasal, olfactory and facial-nerve histopathology; neurobehaviour; lung histopathology or BAL; repeat dosing; a second species. *External context, not our data: intranasal manganese reaches the brain along olfactory pathways in published rodent studies, and an enterotoxin-adjuvanted intranasal influenza vaccine was previously associated with facial-nerve (Bell's palsy) events. Both make this gap decision-relevant for an elderly population.*

![Figure 4. Tolerability and safety-relevant read-outs (T01, T02, E15).](figures/fig4_safety.png)


### 3.6 CMC and dose
- **Encapsulation.** Efficiency is 54.8 ± 5.1% for PSLN-344 vs 59.6 ± 4.6% for PSLN-212 (n = 3; p=0.29) [S08-B] (Q01). Roughly 45% of the CDN is unencapsulated. The dose unit ("20 µg of adjuvant") is not defined as CDN or total mass, and Mn content is not reported.
- **Dose-response [S08-A].** Mn²⁺ raises the maximal response, not the potency: Emax 49- vs 14-fold, with ED50 11.5 vs 9.5 µg. The response plateaus between 20 µg (45.8-fold) and 40 µg (50.2-fold). About 7–8 µg of PSLN-344 matches PSLN-212 at 20–40 µg (E05). This supports testing lower doses, which would also lower Mn exposure.

![Figure 5. Ifnb1 dose-response [S08-A] with Emax fits (E05).](figures/fig5_dose_response.png)


## 4. Data integrity: summary of findings
We checked the workbook for internal consistency (stated vs observed n, label consistency across sheets, survival vs companion body-weight records) and for duplicated values (position-matched comparisons, cross-experiment animal-trajectory matching against an empirical chance benchmark, and recomputation of derived quantities). Table 3 lists the critical and major findings; the full register is in Appendix A. **None of these findings is, on its own, proof of misconduct.** Template or copy errors can produce several of them. Only the raw records can settle it, and until then the affected blocks cannot support an investment or regulatory decision.

| ID | Finding (blocks) | Evidence | What it affects |
|---|---|---|---|
| C1 (Critical) | Whole body-weight trajectories of individual animals are identical across different experiments (different challenge timing, age cohorts and even mouse strains), in several cases with exact-integer edits on the remaining days. [S15-C/S15-I; S09-E/S15-M; S15-A/S15-M; S09-E/S09-G; S15-M/S15-O] | 18 cross-experiment animal pairs share >=4 identical live (non-carried-forward) weight readings vs 0.005 pairs expected by chance (126,074 pairs compared; dup_chance_benchmark.csv). Examples: 6 of 7 "3d Vaccine+PSLN-344" animals (S15-I) = S15-C PSLN-344 animals on days 2-12; S15-M young C57BL/6 controls I-N = S09-E young BALB/c PSLN-344(Y) X-AC; S15-M PSLN-344 AE/AF = S15-A PSLN-344 X/Y with offsets of -1.0 and -2.0 on days 2 and 8. | Rapid (3-day) protection (S15-H/I); cross-strain protection in C57BL/6 and Swiss Webster (S15-L/M, S15-N/O); 180-day durability in young (S09-F/G); companion weights for S06-A/S06-C. |
| C2 (Critical) | Time-to-event records of two different experiments (challenge on day 14 vs day 3) are identical for all four groups, row for row; the companion weights for S06-D (S15-D) show two PSLN-344 and two PSLN-212(Y) animals flat-lining (carried-forward = dead by the workbook convention) although S06-D records 7/7 survival. [S06-C, S06-D (and S15-D)] | Identity of 28 rows x 5 columns (integrity_checks.csv); S15-D cols W, AC, F, G constant from day 8-10 to day 14. | Rapid heterosubtypic protection (S06-D, 7/7) and H5N1 protection (S06-C). |
| C3 (Critical) | Alveolar-macrophage (%) and neutrophil (%) panels share identical per-animal values in the same positions for 1-2 of 5 animals in every group at every time point. [S11-A, S11-B] | 35 of 100 position-matched values identical; chance expectation 0.85 (max 6 in 20,000 permutations); all other comparable block pairs show 0-1 identical values. | Any claim about alveolar macrophages or neutrophils after PSLN-344 (not used in MoA). |
| C4 (Critical) | Day-12 body weights of all 8 PSLN-212(Y) animals are identical to those of all 8 PSLN-344(Y) animals. [S09-C] | 8/8 values identical in order. | Young-mouse comparison PSLN-344(Y) vs PSLN-212(Y) (S09-B/C). |
| C5 (Critical) | Values recur between two AEC-uptake experiments under different labels (S01-B AECII/PSLN-SRB shares 17.7, 17.5, 12.2 with S08-C AECII-PSLN-SRB; S01-B AECI/PSLN-SRB shares 4.92, 4.13 with S08-C AECII-PSLN-344-SRB). [S01-B, S08-C] | 3/5 and 2/5 exact matches at 3-4 significant figures under different group labels. | AECII targeting by the vehicle (S01-B) and the finding that Mn reduces AEC uptake ~4-fold (S08-C). |
| M1 (Major) | Printed IgG2a/IgG1 quotients reproduce exactly from the S13 subclass titres, but with group labels cyclically rotated (S03 "PSLN-212" = S13 "PSLN-212(Y)"; S03 "PSLN-344" = S13 "PSLN-212"; S03 "PSLN-212(Y)" = S13 "PSLN-344"). [S03-B, S03-F vs S13-A to S13-D] | Max relative error <0.07% for the rotated mapping (check_IgG2a_IgG1_labels.csv). S13 labelling is the one consistent with total IgG ranking (S03-A/E). | Th1 (IgG2a) skew claim: under S13 labels PSLN-344 raises IgG2a/IgG1 from 0.55 to 1.85 (H1N1); under S03 labels it lowers it. |
| M2 (Major) | Second S09-A panel is labelled "16h" but every group matches the S01-A 72 h values; the S09-A "PBS" group equals the S01-A "Sham" (empty liposome) group. [S09-A] | Ifnb1: 21/21 panel-2 values match S01-A 72 h (+/-0.01); 3/3 "PBS" values match S01-A "Sham". | Kinetics of cytokine induction; vehicle vs buffer attribution. |
| M3 (Major) | Body-weight blocks described as "the animals of" a survival block contradict it: different group sets (S13-F has "Naive", lacks CMP-204; S13-G has "Naive", lacks PSLN-212), different survivor counts (S03-I PSLN-212 0/7 recorded vs 3 animals recovering to 95-99% in S13-F; S03-J Sham 1/10 vs >=5 by weight), or weights recorded after the recorded death day (S09-C). [S03-I/S13-F; S03-J/S13-G; S06-E/S15-E; S06-G/S15-G; S15-L/S15-M; S09-B/S09-C; S09-F/S09-G] | bw_vs_survival_reconciliation.csv | Homologous protection magnitude vs PSLN-212 (S03-I), H5N1 2-day protection (S03-J). |
| M4 (Major) | MHC-restricted read-outs in mice not stated to carry the restricting haplotype: OT-I (H-2Kb) priming by DCs from donors that default to BALB/c (H-2d); NP366-374 tetramer (H-2Db) in default BALB/c animals. S05-A/B conditions also conflict (ovalbumin vs bivalent vaccine) and have 2 of 3 stated observations. [S02-E; S05-A, S05-B] | Annotation: BALB/c default; C57BL/6 only "in the blocks that name them". | Antigen-presentation (S02-E) and NP-specific CD8 kinetics (S05-A/B). |
| M5 (Major) | Unvaccinated, unchallenged aged sentinels die during the 14-day window. [S06-E, S06-F, S06-G (Untreated)] | 4/21 died (19.0%, 95% CI 5.4-41.9%); S06-G: 3/7 sentinels died - identical to PSLN-344 survival in that experiment (4/7). | Interpretability of every aged survival endpoint (frailty confound). |
| M6 (Major) | Both transfer groups carry the same label ("Ly6C-CD206+ MΦ"). [S07-C] | Duplicate header. | Macrophage-driven Treg induction (MoA step). |
| M7 (Major) | Unlabelled numeric region (A=14 in every row; six 0s in C, seven 0s in D) resembling censored survival records without block ID, groups or measurand. [S08 rows 89-101] | Annotation: "A region of numeric data carrying no block label." | Unknown - possibly a survival experiment not otherwise reported. |
| M8 (Major) | Group "PSLN-344/R848" is not defined in the Materials section (only PSLN-R848 and PSLN-212/R848 are). [S08-A] | Annotation Materials list. | Dose-response comparator identity. |

![Figure 6. Examples of integrity findings: (a) the same animal trajectories in two experiments; (b) the same weights in different strains, adjuvants and experiments; (c) two cell types sharing values; (d) cross-experiment trajectory matches vs chance (I01–I03).](figures/fig6_integrity_evidence.png)


## 5. Mechanism of action, built from our data
Our data support the following model. Mn²⁺ co-delivery **raises the ceiling of the STING/type-I interferon response in the aged lung** (Emax about 3.4× that of PSLN-212 at a similar ED50). The signal appears to spread through gap junctions and induces Ccl2/Ccl3 and GM-CSF (Csf2). This drives **CCR2-dependent monocyte recruitment and IFNAR- and GM-CSF-dependent differentiation into monocyte-derived DCs**, together with cDC1 expansion and CCR7⁺ DC migration to the mediastinal lymph node. Downstream, **Tfh expand while Tfr contract**, germinal centres form, and high-titre HAI/neutralising antibody appears alongside **cross-reactive IFN-γ⁺ CD8 and lung TRM**. Together these plausibly explain homologous and heterosubtypic protection. Figure 7 shows each step with its evidence grade.

| Step | Evidence in our data (aged, PSLN-344 vs PSLN-212 unless stated) | Grade | Gap to close |
|---|---|---|---|
| Uptake | Alveolar macrophage uptake depends on SP-A/SP-D: 43.1% vs 12.7% in Sftpa1/Sftpd KO (p<0.001) [S01-C] (M01). AEC-II targeting [S01-B] and the "Mn lowers AEC uptake ~4×" result [S08-C] are unreliable (C5). | Moderate | Cell-resolved biodistribution of PSLN-344 itself (the Mn form) |
| STING → IFN-β | Ifnb1 16 h 37.1 ± 4.8 vs 16.6 ± 2.1-fold (2.23×, p<0.001), equal to young (RI 0.98) [S01-A]. Emax 49 vs 14 [S08-A]. Transient: no difference at 72 h (p=0.33) (M02). | Strong | STING/cGAS-knockout or STING inhibitor; IFN-β protein |
| Gap-junction spread | Carbenoxolone: recruited monocytes 3.1% vs 7.3% (p=0.004) [S11-C] (M03). | Moderate | Second, more selective blocker; cell-type-specific connexin KO |
| Chemokines, GM-CSF | Csf2 4.2× (16 h), 5.4× (36 h) [S02-F]. Ccl2 77×, Ccl3 27×, Ccl5 7.6× at 16 h (n = 3) [S09-A] (M04). | Strong (S02-F) | Protein levels (BAL); S09-A PBS/Sham label fix (M2) |
| Monocyte influx | Day-4 monocytes 30.6 ± 4.7 vs 16.7 ± 1.6% (p=0.002) [S01-D]. CCR2 antagonist: monocytes 9.9 → 3.3%, Ly6C⁺ Mφ 15.4 → 2.5% [S07-B]. IFNAR⁻/⁻ marrow: 15.4 vs 21.3% (n = 3, p=0.12) [S12-A] (M05). | Strong | Link to protection (CCR2 antagonist + challenge) |
| moDC differentiation | IFNAR⁻/⁻ marrow moDC 2.1 vs 19.7% (p<0.001); GM-CSF rescue to 12.4% [S02-H]. GM-CSF + PSLN-212: 13.8 vs 5.9% (p=0.002) [S02-G] (M06). | Strong | GM-CSF neutralisation with PSLN-344 |
| DC mobilisation | cDC1 37.5 ± 7.0 vs 22.8 ± 3.6% [S01-F]; migratory DC 30.7 ± 7.9 vs 7.3 ± 2.0% [S02-A]; antigen⁺ MLN DC 7.1 ± 1.4 vs 1.8 ± 0.4%, pertussis-toxin arm 2.4 ± 0.9% [S02-C]; co-stimulation RI only 0.17–0.22 [S02-D]. | Moderate | OT-I/NP-tetramer strain check (M4); co-stimulation deficit |
| Tfh / Tfr / GC | ICOS-hi Tfh 10.3 ± 3.2 vs 3.8 ± 0.9% [S04-A]; Tfr 10.8 ± 1.8 vs 26.7 ± 6.7% [S04-B]; GC B 6.5 ± 1.5 vs 2.3 ± 0.5% [S03-K]; Tfr difference gone by d30 (p=0.11) [S04-C]. | Strong | Tfh/Tfr causality; durability of GC |
| Antibody | IgG 18.6× / 13.4×; HAI 8.0× / 9.2×; neutralising 9.2× [S03]. IgG2a/IgG1 rises 0.55 → 1.85 (H1N1) only under the S13 labels, and S03-B/F contradict this (M1). | Strong | Mucosal IgA (never measured); subclass labels |
| CD8 / TRM | Ki-67⁺ CD8 9.4 ± 1.8 vs 3.5 ± 1.4% [S05-D]; H5N1-reactive IFN-γ⁺ CD8 6.4 ± 1.0 vs 1.5 ± 0.4% (d14) [S05-F]; TRM 4.0 ± 0.6 vs 1.0 ± 0.4% [S05-I]. Lung priming is insensitive to pertussis toxin (59 vs 55%), MLN priming is sensitive (30.9 → 6.8%) [S05-C]. | Strong | CD8 depletion + heterosubtypic challenge |
| Suppressive milieu | CD206⁺ Mφ 48.9 ± 8.1 vs 71.5 ± 8.3% (time point not stated) [S11-E]; lung Treg 3.0 ± 0.4 vs 6.7 ± 0.3% (n = 3) [S04-D]; PSLN-212 accumulates Ly6C⁺CCR2⁺ Mφ (day 5: 19.0 vs 3.4 ×10⁵) [S07-A]; S07-C cannot be interpreted (M6). | Weak | Macrophage transfer with correct labels |

**What the MoA does not yet show.** (i) Every step is either a PSLN-344 vs PSLN-212 association or a single-intervention experiment. No step has been causally linked to survival: there are no depletion or knockout experiments with challenge. (ii) STING dependence is assumed, not demonstrated: there is no STING/cGAS knockout and no STING inhibitor. (iii) The contribution of Mn²⁺ alone is untested. These are the first experiments in Study B1.

![Figure 7. Mechanism of action assembled from our data, with the evidence grade of each step (M01–M06).](figures/fig7_moa.png)


## 6. Biomarkers to validate efficacy
We proposed 23 candidate read-outs. All of them separate the protective regimens (aged PSLN-344, young) from the non-protective ones (Sham, aged PSLN-212) perfectly at the animal level in 22 of 23 (AUC 1.0, or 0.0 for Tfr, which falls); the exception is neutralising titre, at 0.995 (B01). **So our data cannot rank biomarkers by discrimination.** We ranked them instead by how early they read out, how Mn-specific they are, and whether they have a human-accessible analogue. All of this concordance is between groups, because challenged animals were not sampled. True correlates of protection need within-animal pre-challenge sampling, which is built into Study B1.

| Tier / timing | Marker in our data [block] | PSLN-344 vs PSLN-212 (aged) | RI | Human-accessible analogue | Proposed use |
|---|---|---|---|---|---|
| 1. PD, 16–36 h | Lung Ifnb1 16 h [S01-A] | 2.23× (p<0.001) | 0.98 | Nasal-mucosa ISG score; IFN-β/λ in nasal lining fluid; blood ISG at 24 h | Target engagement; dose selection (Emax plateau) |
| 1. PD, 16–36 h | Lung Csf2 36 h [S02-F] | 5.4× (p<0.001); PSLN-212 ≈ Sham | – | Nasal GM-CSF (nasosorption) | Most Mn-specific marker → proof of Mn action |
| 1. PD, 16 h | Lung Ccl2 [S09-A] | 77× (n = 3) | 0.84 | Nasal/serum CCL2 | Supportive PD |
| 1. Safety PD, 16–72 h | Lung Il6/Tnf [S09-A] | Il6 6.5×; Tnf above young | – | Serum IL-6/TNF; solicited reactogenicity | Reactogenicity ceiling |
| 2. Priming, d7 | ICOS-hi Tfh; Tfr [S04-A/B] | +6.4 / -15.9 pts | 0.66 / 0.81 | Blood cTfh (ICOS⁺PD-1⁺CXCR5⁺) and cTfh:cTfr at d7 | Early predictor of antibody response |
| 2. Priming, d3–7 | Ki-67⁺ CD8 [S05-D]; GC B [S03-K] | +5.9 / +4.2 pts | 0.91 / 0.56 | Blood Ki-67⁺/CD38⁺HLA-DR⁺ CD8; plasmablasts d7 | Early cellular signal |
| 3. Efficacy surrogate, d14–28 | HAI GMT [S03-C/G] | 8.0× / 9.2× | 0.88 / 0.94 | HAI GMT and fold-rise (regulatory surrogate) | Primary immunogenicity (GMT, not the ≥1:40 threshold) |
| 3. Efficacy surrogate, d14 | Neutralising [S03-D/H]; IgG [S03-A/E] | 9.2×; 18.6× | 0.80 | Microneutralisation; ELISA | Secondary |
| 3. Heterosubtypic arm, d14–60 | IFN-γ⁺ CD8, H5N1 restim. [S05-F/G] | +4.9 pts (d14); +6.8 (d60) | 0.63 | IFN-γ ELISpot to conserved NP/M1 peptides | Key differentiation marker |
| 3. Mucosal | Not measured | – | – | Nasal HA-specific IgA | Must add: the rationale for i.n. delivery |

- **Do not use HAI ≥1:40 as the success criterion.** Aged PSLN-212 mice were 5/5 at ≥1:40 against H1N1 [S03-C], yet under the same protocol 0/7 survived homologous H1N1 challenge [S03-I] (B02). Even the body-weight record that conflicts with S03-I (M3) implies no more than 3/7. Use GMT and fold-rise, together with mucosal and T-cell markers.
- **Not recommended as biomarkers:** the IgG2a/IgG1 ratio (its labels conflict between sheets, M1, and the subclass biology is mouse-specific); the printed Tfh:Tfr (it is derived arithmetically from Foxp3%, m5); alveolar macrophage and neutrophil counts (C3).
- **Bridging logic for the clinic.** Day 1–2 nasal IFN/ISG and GM-CSF show that Mn²⁺ is acting (PD). Day 7 blood cTfh and plasmablasts predict the antibody response. Day 28 HAI GMT, microneutralisation, nasal IgA and NP/M1 ELISpot are the efficacy surrogates. Studies B1 and C must show that the mouse PD markers carry over to the ferret/NHP nasal compartment.


## 7. Target demographic for TAM sizing
The differentiation in our data is **specific to aged animals**. In young mice, Mn²⁺ adds no survival benefit and little immunological benefit (Section 3.3). The aged cohort is ≥20 months old (annotation p.1). By common lifespan-mapping conventions (external, not our data), that is roughly the seventh decade of human life. Our data therefore most directly support adults in their 60s and early 70s; they say nothing about the very old or frail.

| Segment | Definition for market research | Status | Basis in our data |
|---|---|---|---|
| Core (base case) | Adults ≥65 y receiving annual seasonal influenza vaccination, in markets that preferentially recommend enhanced vaccines for this age group | Base case | Age-specific benefit: RI median 0.71 in aged vs no incremental benefit in young [S09-B/D/F, S02-C/E] |
| Sensitivity | Adults 60–64 y where national programmes start at 60 | Sensitivity | ≥20-month cohort; imprinting model at 14 months also responsive [S06-E′/F′] |
| Sub-segments | 65–74; 75–84; ≥85; long-term-care residents | Size separately; ≥75 extrapolated | Very old/frail not modelled; 19% sentinel mortality shows the model is already frail [S06-E/F/G] |
| Upside only | Pandemic / pre-pandemic H5 preparedness for older adults (government procurement) | Only if verified | H5N1 protection and H5N1-reactive CD8 [S06-C/F, S05-F/G]; rapid onset [S03-J, S15-H] is compromised |
| Exclude | <50 y; paediatric | Excluded | No differentiation over Mn-free formulation in young; no paediatric data |
| Downside haircuts | Possible label restrictions: Parkinson's disease or hepatic impairment (Mn handling); chronic rhinosinusitis or severe airway disease (intranasal STING activation); immunocompromised | Hypotheses pending Study B2 | No Mn or airway-disease safety data exist; Tnf/Il10 overshoot in aged lung [S09-A] |

**Parameters market research should provide for each segment and key market:** population size; annual influenza vaccination coverage; share of enhanced (high-dose, adjuvanted or recombinant) vaccines; price corridor of enhanced vaccines; acceptability of and preference for needle-free intranasal delivery; prevalence of the possible label-restriction conditions above; and, for the upside case, H5 stockpile procurement volumes. **Note:** the BALB/c animals were female and sex is not stated for the other strains (annotation p.1), so the benefit in males is untested.


## 8. What we considered and ruled out
| Option or claim considered | Decision | Reason (our data) |
|---|---|---|
| Advance PSLN-344 to IND-enabling now | Ruled out | Critical integrity findings (C1–C5); no attribution control; no SoC benchmark; no Mn safety data. |
| Partner or out-license now | Ruled out | Partner due diligence would find the same duplications (Figure 6), creating reputational and legal exposure. Value cannot be shown until verified. |
| Terminate immediately | Considered; not the first action | The audit is required regardless; unflagged blocks show large, coherent effects (Table 1). Termination remains the default if the gates fail. |
| PSLN-212 (no Mn) as lead | Ruled out | Inferior in aged mice: IgG 19× lower, HAI GMT 46 vs 368 [S03-A/C]; pooled survival 13/101 vs 85/101. |
| CMP-204 (cGAMP instead of CDN-1807) | Ruled out | Lower IFN ceiling: Ifnb1 7.8- vs 16.6-fold for PSLN-212 [S01-A]; Emax 7.2 vs 14.4 [S08-A]; IgG GMT 181 vs 393 [S03-A]; aged survival 3/7 [S03-I]. |
| Adding TLR7/8 agonist R848 | Ruled out | PSLN-R848 Ifnb1 only 5.0-fold [S01-A]; PSLN-212/R848 weight nadir 90.0% with one animal lost [S08-D]; Tnf about 202× and Il10 about 179× at 16 h [S09-A]; PSLN-344/R848 Emax 36 vs 49 for PSLN-344 [S08-A]. |
| Young-adult or paediatric indication | Ruled out | No incremental benefit in young mice: 8/8 vs 8/8 survival in three studies [S09-B/D/F]; antigen⁺ DC and OT-I gains not significant [S02-C/E]. |
| Stand-alone intranasal antiviral (no antigen) | Ruled out | PSLN-344 alone 3 d before H5N1: 0/7 survived [S15-H] (block also affected by C1). |
| Dose escalation above 20 µg | Ruled out | Plateau: 45.8-fold at 20 µg vs 50.2-fold at 40 µg [S08-A]. Explore lower doses instead. |
| Claim "restores a young immune system" | Ruled out as stated | Partial: median RI 0.71; DC co-stimulation RI 0.17–0.22; titres 0.3–0.6× of young [S02-D, S03, S13]. |
| Claims of 2–3-day onset, cross-strain protection, 180-day durability | Withheld | They rest on blocks with critical or major integrity findings (S03-J, S06-D, S15-H/I, S15-L–O, S09-F/G). |
| HAI ≥1:40 as success threshold | Ruled out | Aged PSLN-212: 5/5 ≥1:40 but 0/7 homologous survival [S03-C, S03-I]. |
| IgG2a/IgG1 (Th1 skew) as evidence or biomarker | Ruled out pending audit | S03-B/F labels are cyclically permuted relative to S13-A–D (M1); mouse-specific. |
| AEC-II targeting as the explanation for the Mn benefit | Ruled out | S08-C says Mn lowers AEC uptake about 4×, and S01-B/S08-C share values (C5). |
| Aged survival endpoints without sentinels | Ruled out for future studies | 19% 14-day mortality in unchallenged aged mice [S06-E/F/G]. |
| Using the current package for a regulatory filing | Ruled out | Not ALCOA+-compliant until the audit is complete. |


## 9. Methods and reproducibility
**Parsing.** All 15 sheets were mapped block by block to explicit cell ranges (*analysis/blocks.py*) and converted into tidy tables with a cell reference for every value (*tidy_continuous.csv, tidy_survival.csv, tidy_bodyweight.csv*). Group names were normalised (e.g. "PSLN-212Y" → "PSLN-212(Y)").

**Statistics.** Titres, ratios and qPCR fold-changes were analysed on the log₂ scale (S09-A log₁₀ values converted), and percentages on the raw scale. For each block we report Welch t-tests with 95% CIs, Hedges g and Tukey HSD (the stated method; *block_tukey_hsd.csv*), with Benjamini–Hochberg q-values across all contrasts. Survival: log-rank (statsmodels *survdiff*) and Fisher exact per experiment. Pooled survival used an exact conditional (stratified) test, the convolution of per-experiment hypergeometric distributions, and a Mantel–Haenszel risk difference. The one missing day value (S03!G46) was treated as censored at day 21.

**Integrity checks.** Stated vs observed n; labels across sheets; recomputation of derived quantities (IgG2a/IgG1 from S13; Tfh:Tfr from Foxp3%); survival vs companion body-weight records, using the workbook's carry-forward convention (≥3 identical trailing values, or missing values, counted as deaths); position-matched duplicate tests with permutation null; and cross-experiment animal-trajectory matching on live (non-carried-forward) readings against a Poisson-binomial expectation from per-day value frequencies. That benchmark is conservative, because the duplicates themselves inflate the collision rates.

**Limitations.** n = 3–8 per group; female BALB/c (sex not stated for other strains); single experiments with no replicate runs; vaccine antigen was formalin-inactivated whole virus rather than licensed split/subunit antigen; mouse intranasal dosing reaches the lung, unlike a human nasal spray. External context is marked as such and carries no numbers.


## Appendix A. Full data-integrity register
| ID | Severity | Blocks / cells | Finding | Required action |
|---|---|---|---|---|
| C1 | Critical | S15-C/S15-I; S09-E/S15-M; S15-A/S15-M; S09-E/S09-G; S15-M/S15-O (S15!W24:AC29 vs S15!W73:AC78; S09!X40:AC46 vs S15!I104:N110; S15!X4:Y10 vs S15!AE104:AF110; S09!N40:N46 vs S09!N67:N73) | Whole body-weight trajectories of individual animals are identical across different experiments (different challenge timing, age cohorts and even mouse strains), in several cases with exact-integer edits on the remaining days. | Retrieve raw balance logs (grams) and animal IDs for every body-weight block; establish which record is original; re-derive all % values; if not traceable, exclude the experiment and refer to research-integrity process. |
| C2 | Critical | S06-C, S06-D (and S15-D) (S06!M3:Q30 vs S06!A34:E61; S15!B33:AC40) | Time-to-event records of two different experiments (challenge on day 14 vs day 3) are identical for all four groups, row for row; the companion weights for S06-D (S15-D) show two PSLN-344 and two PSLN-212(Y) animals flat-lining (carried-forward = dead by the workbook convention) although S06-D records 7/7 survival. | Recover original mortality logs for both experiments; treat S06-D as unverified until then. |
| C3 | Critical | S11-A, S11-B (S11!B3:U7 vs S11!B10:U14) | Alveolar-macrophage (%) and neutrophil (%) panels share identical per-animal values in the same positions for 1-2 of 5 animals in every group at every time point. | Re-export from FCS files; exclude both blocks until resolved. |
| C4 | Critical | S09-C (S09!G18:N18 = S09!W18:AD18) | Day-12 body weights of all 8 PSLN-212(Y) animals are identical to those of all 8 PSLN-344(Y) animals. | Re-derive from raw weights. |
| C5 | Critical | S01-B, S08-C (S01!B14:F15 vs S08!A14:B18) | Values recur between two AEC-uptake experiments under different labels (S01-B AECII/PSLN-SRB shares 17.7, 17.5, 12.2 with S08-C AECII-PSLN-SRB; S01-B AECI/PSLN-SRB shares 4.92, 4.13 with S08-C AECII-PSLN-344-SRB). | Re-export both from FCS files; treat AEC-targeting claims as unverified. |
| M1 | Major | S03-B, S03-F vs S13-A to S13-D (S03!G2:I14; S13!A2:O7) | Printed IgG2a/IgG1 quotients reproduce exactly from the S13 subclass titres, but with group labels cyclically rotated (S03 "PSLN-212" = S13 "PSLN-212(Y)"; S03 "PSLN-344" = S13 "PSLN-212"; S03 "PSLN-212(Y)" = S13 "PSLN-344"). | Confirm plate maps; until then do not use IgG subclass ratio as evidence or biomarker. |
| M2 | Major | S09-A (S09!X1:AS9; S09!B3:D3) | Second S09-A panel is labelled "16h" but every group matches the S01-A 72 h values; the S09-A "PBS" group equals the S01-A "Sham" (empty liposome) group. | Relabel panel 2 as 72 h; correct PBS/Sham identity. |
| M3 | Major | S03-I/S13-F; S03-J/S13-G; S06-E/S15-E; S06-G/S15-G; S15-L/S15-M; S09-B/S09-C; S09-F/S09-G (S13!A32:AJ40; S13!A42:AE50; S15!A41:AJ70; S15!H102:AJ110; S09!F11:AD19; S09!F65:AD73) | Body-weight blocks described as "the animals of" a survival block contradict it: different group sets (S13-F has "Naive", lacks CMP-204; S13-G has "Naive", lacks PSLN-212), different survivor counts (S03-I PSLN-212 0/7 recorded vs 3 animals recovering to 95-99% in S13-F; S03-J Sham 1/10 vs >=5 by weight), or weights recorded after the recorded death day (S09-C). | Reconcile against mortality/humane-endpoint logs. |
| M4 | Major | S02-E; S05-A, S05-B (S02!K9:O14; S05!A1:I10) | MHC-restricted read-outs in mice not stated to carry the restricting haplotype: OT-I (H-2Kb) priming by DCs from donors that default to BALB/c (H-2d); NP366-374 tetramer (H-2Db) in default BALB/c animals. S05-A/B conditions also conflict (ovalbumin vs bivalent vaccine) and have 2 of 3 stated observations. | Confirm strain per block; if BALB/c, exclude. |
| M5 | Major | S06-E, S06-F, S06-G (Untreated) (S06!L62:L68; S06!R62:R68; S06!F99:F105) | Unvaccinated, unchallenged aged sentinels die during the 14-day window. | Add sentinel arms and pre-specified exclusion rules; health-screen aged cohorts. |
| M6 | Major | S07-C (S07!B15:C20) | Both transfer groups carry the same label ("Ly6C-CD206+ MΦ"). | Recover group identity; exclude until then. |
| M7 | Major | S08 rows 89-101 (S08!A89:D101) | Unlabelled numeric region (A=14 in every row; six 0s in C, seven 0s in D) resembling censored survival records without block ID, groups or measurand. | Identify the experiment; disclose outcome. |
| M8 | Major | S08-A (S08!K2:M7) | Group "PSLN-344/R848" is not defined in the Materials section (only PSLN-R848 and PSLN-212/R848 are). | Define the preparation. |
| m1 | Minor | S03-J, S13-E, S05-A/B, S09-B, S09-F (S03!G15; S13!R1; S05!A1; S09!A10; S09!A64) | Stated n differs from observations: S03-J 9 vs 10/group; S13-E 5 vs 7; S05-A/B 3 vs 2; annotation says S09-B Sham has 7 and S09-F Sham 8, workbook has 8 and 7. | Correct metadata. |
| m2 | Minor | S03-J (S03!G46) | One PSLN-344 record has no day value (treated as censored at 21 d); stated follow-up 22 d vs max 21 d recorded. | Correct record. |
| m3 | Minor | S06 (S06!G69, S06!M69) | Block IDs S06-E and S06-F are each used for two different experiments (rows 34-68 and rows 71-105). | Re-number (cited here as S06-E' and S06-F'). |
| m4 | Minor | S07-B, S11-E, S13-H, S14-A | Timepoint not stated. | Add timepoints. |
| m5 | Minor | S04-B Tfh:Tfr (S04!A14:D19) | Printed "Tfh:Tfr" equals (100 - Foxp3%)/Foxp3% of the same block (Foxp3- : Foxp3+ within CXCR5+ICOShi), not an independent Tfh/Tfr measurement. | Relabel; do not count separately. |
| m6 | Minor | S08-B (S08!A10:O11) | Encapsulation of PSLN-R848 and CMP-204 reported via "absorbance of CDN-1807 at 260 nm" although neither contains CDN-1807. | Specify assay per payload. |
| m7 | Minor | S10-A (S10!A1:N7) | Annotation says block "reported as mean with standard deviation" while the file stores per-animal values. | Clarify. |
| m8 | Minor | S02-C, S02-E (PTX arm) (S02!N2, S02!N9) | Adjuvant and age of the pertussis-toxin arm are not stated. | Clarify. |
| m9 | Minor | S01-A vs S09-A; S01-F vs S01-G | Not independent: S09-A Ifnb1 values are a subset of S01-A animals; cDC1% and cDC2% are complementary fractions of one gate (sum 97-99%). | Count once. |
| m10 | Minor | All PSLN-344 blocks | No Mn2+-only (CDN-free Mn-liposome) arm exists anywhere; whether "Sham" contains Mn is not stated. | Add 2x2 factorial arms. |
| S1 | Soft signal | Most immunology blocks | Effect sizes are unusually large and clean for aged-mouse immunology with n=3-5 (Hedges g 2-9; perfect separation of protective vs non-protective regimens in 22 of 23 candidate read-outs). | Power confirmatory studies on effects well below those observed. |


## Appendix B. Deliverables
- **PSLN-344_Portfolio_Proposal.pdf / .md**: this document.
- **PSLN-344_evidence_ledger.xlsx**: claims with cell references; group summaries; all contrasts; Tukey HSD; survival counts, tests and pooled sensitivity; mechanism contrasts; biomarker table; safety; dose-response; integrity register; duplication analyses.
- **figures/**: Figures 1–7 as PNG.
- **analysis/**: Python scripts, plus tidy data tables with a cell reference for every value. Run order: parse.py → surv_summary.py → stats_continuous.py → stats_survival.py → stats_survival_pooled.py → check_derived.py → bw_reconcile.py → dup_scan.py → dup_exact_bw.py → dup_trajectories.py → dup_trajectories2.py → dup_null.py → integrity_checks.py → integrity_register.py → mechanism_contrasts.py → biomarkers.py → safety_cmc_dose.py → design_power.py → keynums.py → figures.py → fig_moa.py → build_report.py → build_ledger.py. Environment: micromamba env *chem* (pandas, scipy, statsmodels, matplotlib, reportlab, openpyxl).
