# PSLN program: portfolio recommendation and next-step proposal

*PSLN-344 and PSLN-212 (CDN-1807 STING-agonist liposomes) · portfolio review · 1 November 2026*

<sub>Basis: psln_program_dataset.xlsx (15 sheets, 6,819 numeric cells, last modified 3 September 2026) and psln_program_annotation.pdf (15 September 2026); nothing later is included. Every efficacy, safety and mechanism number is computed from that workbook: source blocks are in square brackets, cell ranges and methods in Appendix B and the evidence workbook. Statements marked *external* are general knowledge, not our data; check them before use.</sub>


## 1. Recommendation

**Keep the program, with one lead and a gated budget. Take PSLN-344 forward. Stop developing PSLN-212 as a candidate and keep it only as the manganese-free comparator. Approve the work up to Gate 1 (October 2027) now; release nothing beyond it until the criteria in Section 2 are met.**

**What the asset is.** The data do not describe a stand-alone STING-agonist drug. They describe a vaccine adjuvant: the cyclic dinucleotide CDN-1807 in a lung-surfactant-like liposome, with Mn²⁺ (PSLN-344) or without it (PSLN-212), given into the airway of mice together with inactivated influenza vaccine. Given without vaccine, PSLN-344 protected 0/7 aged animals; vaccine alone protected 0/7; the two together 6/7 [S15-H]. All data are from mice.

**How it looks.** Promising but not yet decision-grade: a large and consistent survival benefit in aged mice, inside a mouse-only package with real gaps in safety, comparators and data hygiene.

- **The efficacy signal in aged animals is large and consistent.** Across the nine lethal-challenge experiments in aged BALB/c mice, vaccine + PSLN-344 left 56/66 (85%) alive, against 9/66 (14%) for PSLN-212 and 1/66 (2%) for vaccine + empty liposome; hazard ratio for death against PSLN-212, 0.08 (95% CI 0.04–0.15) [S03-I, S03-J, S06-A–G]. Removing the duplicated experiment and the two whose comparator arms are uncertain gives 32/42 (76%) against 4/42 (10%); reading every remaining disagreement in the records against PSLN-344 gives 30/42 (71%) against 5/42 (12%).
- **The advantage exists only in aged animals.** In young mice both candidates gave 24/24 survival [S09-B, S09-D, S09-F]. The case for PSLN-344 is therefore a case for an older-adult vaccine.
- **The mechanism is coherent and measurable.** Mn²⁺ returns the interferon-β response of aged lung to the young level (37.1-fold against 16.6-fold; young 37.6-fold) [S01-A] and switches on GM-CSF (8.7-fold against 1.6-fold at 36 h) [S02-F]. Downstream, PSLN-344 brought aged animals closer to the young benchmark than PSLN-212 in 38 of 39 immune read-outs; where aged animals fall short of young ones, it reached a median 69% of the young value against 18% (Figure 3).

**Why the approval should be conditional.**

1. **The data file is not yet committee-grade.** I raised 22 data-quality flags, 8 of them serious: two blocks with rotated column headers, two nominally different survival experiments with identical data, a mislabelled time point, a neutrophil data set that duplicates another block, recycled body-weight traces, and survival and weight blocks that disagree in 10 groups (Section 3.4, Appendix A). None reverses the headline result, but they must be settled from source records before anyone outside the project relies on the file.
2. **There is no comparison with what older adults already receive.** Every comparator is our own material or an empty liposome: no intramuscular arm, no high-dose antigen, no licensed adjuvant.
3. **Attribution is open.** No experiment tests manganese in the liposome without CDN-1807, or free CDN-1807. We cannot yet say the STING agonist is needed once manganese is present.
4. **Safety evidence is thin where it matters most.** Manganese is delivered to the nose and lung, yet no block reports how much manganese is given or where it goes. Brain read-outs are three transcripts at one time point [S10-A]. Lung *Il6*, *Tnf* and *Ccl2* are still 7.2×, 8.4× and 27× control at 72 h, the last time point [S09-A]. There is no histopathology, and the neutrophil block is unusable.
5. **Translation is untested.** No male animals, no second species, no human cells; and the site of action is the alveolus, which a human nasal spray largely does not reach (*external*).

**Table 1. How the asset looks today**

| Dimension | Assessment | Basis in our data |
|---|---|---|
| Efficacy in aged hosts | **Strong signal** | 56/66 (85%) vs 9/66 (14%) survival; PSLN-344 ahead in 15 of 15 head-to-head experiments; three mouse strains [S03-I/J, S06, S15-L/N] |
| Advantage in young hosts | **None shown** | 24/24 vs 24/24 survival; interferon-β 1.3×; no difference in dendritic-cell read-outs; slower recovery than PSLN-212 after challenge at day 180 [S09, S01-A/E/F, S02-C/E] |
| Mechanism | **Coherent, partly causal** | Seven-step chain; five steps tested by knockout or inhibitor; the manganese-specific step is inferred, not tested (Section 4) |
| Tolerability in mice | **Acceptable but thin** | Weight loss after dosing 3.6% (worst animal 5.8%), recovered by day 10 [S08-D]; lung cytokines not back to baseline at 72 h [S09-A]; no histology |
| Manganese and brain safety | **Unknown** | No manganese measurement. Brain *Ifnb1* 1.3× buffer (95% CI 0.8–2.0) at 36 h; cholera-toxin control 5.5× [S10-A] |
| Versus current vaccines for older adults | **Not tested** | No intramuscular, high-dose or licensed-adjuvant comparator in any block |
| Translation to people | **Not addressed** | Mice only; BALB/c all female, no male data; alveolar site of action [S01-B, S01-C]; no human cells |
| Product quality (CMC) | **Early** | Encapsulation efficiency 54.8% (SD 5.1, n=3) [S08-B]; no manganese content, particle size or stability data in the file |
| Data integrity | **Audit needed** | 22 flags, 8 rated high (Appendix A) |

<sub>Terms. Aged = mice of 20 months or more; young = 7–8 weeks; young benchmark = young mice given vaccine + PSLN-212; empty liposome = the workbook's "Sham". HAI = haemagglutination-inhibition titre, the antibody measure regulators accept for influenza vaccines. S06-E2 and S06-F2 are my names for the second pair of blocks that the workbook also labels S06-E and S06-F (14-month-old animals).</sub>


## 2. Next steps: what the next studies have to establish

Five studies behind three gates. Each study answers one question the current data cannot, and each has a stop rule agreed in advance. Gate 0 and Studies 1–4 run in parallel and report by October 2027; the ferret study and any IND-enabling spend wait for Gate 1. I have not costed the plan, because the data give no basis for it; the scale is about 540 aged mice for Study 1, about 400 for Study 2, 60–80 ferrets for Study 5 and three formulation batches.

![fig6_timeline.png](figures/fig6_timeline.png)

<sub>Figure 1. Proposed timeline. Hatched bar: not part of this request.</sub>

**Table 2. Gates**

| Gate | When | Question | Passed if | If not |
|---|---|---|---|---|
| **Gate 0** | Dec 2026 | Are the numbers in the workbook the numbers in the laboratory records? | All 8 high flags resolved from source; in the re-locked file pooled aged survival is still ≥ 70% for PSLN-344 and ≤ 30% for PSLN-212 (today, worst case: 30/42 (71%) vs 5/42 (12%)) | Freeze Studies 2–4; Study 1 becomes the only route to re-establish the claim |
| **Gate 1** | Oct 2027 | Is the effect real, attributable to the product, at least as good as current practice, tolerable, translatable and makeable? | Go criteria of Studies 1–4 all met | Stop, or re-scope as stated under each study |
| **Gate 2** | Jul 2028 | Does it work in a second species with a delivery method usable in people? | Go criteria of Study 5 met | Stop before IND-enabling spend |

**Gate 0. Source-data audit and re-lock of the data set (no animals; 2 November – 18 December 2026)**

| Item | Specification |
|---|---|
| **Must establish** | That every number in this proposal matches the primary records: cage cards, balance logs, flow-cytometry exports, plate-reader files. |
| **Scope** | The 22 flags in Appendix A, starting with the 8 rated high (Q01–Q06, Q10, Q11). Also confirm that no data generated after 3 September 2026 are missing. |
| **Comparator** | Primary records against the workbook, block by block, by someone outside the study team. |
| **Read-outs** | Each flagged block classed as confirmed, corrected or withdrawn; workbook and annotation re-issued with animal identifiers; the analysis scripts supplied with this proposal re-run on the new file. |
| **Also decide** | Whether 20-month-old mice of both sexes can be supplied for Studies 1 and 2 in January 2027. This is the critical-path item. |

**Study 1. Confirmatory efficacy, attribution and benchmark in aged mice (January – August 2027)**

| Item | Specification |
|---|---|
| **Must establish** | (a) The survival benefit in aged mice replicates under randomisation and blinding, in both sexes. (b) It needs CDN-1807 and Mn²⁺ together in the liposome. (c) It is at least as good as surrogates for the vaccines older adults receive now. (d) The lowest effective dose. (e) Which pre-challenge marker predicts survival in the individual animal. |
| **Why (gap)** | Current experiments have 5–10 female animals per group and no stated blinding; one experiment of 7 per arm has only 67% power even for 85% vs 14%. No manganese-only, free-CDN, intramuscular or licensed-adjuvant arm exists. All efficacy data are at 20 µg, which already gives 91% of the interferon response seen at 40 µg [S08-A]. Immune read-outs and challenge outcomes come from different animals. |
| **Population** | BALB/c, 20–21 months at dosing, male and female. Young adults (8 weeks) as benchmark. A C57BL/6 cohort for the two lead arms, because the cross-strain weight records are flagged (Q06, Q07). |
| **Groups and comparators** | One dose into the airway with inactivated H1N1 + H3N2 vaccine unless stated: (A) empty liposome; (B) manganese liposome without CDN-1807, manganese matched to PSLN-344 (or empty liposome plus manganese chloride, if manganese cannot be loaded without the CDN); (C) free CDN-1807, 20 µg; (D) PSLN-212, 20 µg; (E) PSLN-344, 20 µg; (F) PSLN-344, 10 µg; (G) PSLN-344, 5 µg; (H) intramuscular vaccine with a squalene oil-in-water emulsion, as surrogate for an MF59-adjuvanted vaccine; (I) intramuscular vaccine at four times the antigen dose, as surrogate for a high-dose vaccine; (J) young mice + PSLN-212; (K) unvaccinated, mock-challenged aged mice, for background mortality. |
| **Primary endpoint** | Survival 14 days after a lethal challenge with a virus of a different subtype (5 × mLD50 rgH5N1, the design of S06-C) given 14 days after dosing: E against D, and E against the better of H and I. Humane end-point, randomisation and blinded scoring fixed in the protocol; lethal dose re-titrated in aged animals of each sex beforehand. |
| **Secondary endpoints and read-outs** | Survival after matched H1N1 challenge (the design of S03-I) in groups A, D, E, H, I. Weight-loss area under the curve. Lung virus titre 3 and 5 days after challenge (never measured so far). On day 13 in every challenged animal: HAI, neutralising titre, IgG2a/IgG1, blood IFN-γ-producing CD8 T cells. IgA in nasal wash and lung lavage (never measured). Lung resident-memory CD8 T cells at day 25. Lung histopathology 3 and 7 days after dosing. Durability: challenge 90 days after dosing in animals dosed at 18 months (groups D, E, H). Which arm protects: CD8 T-cell depletion before mismatched challenge in an extra group E cohort (16 animals). |
| **Size and power** | 32 per arm (16 per sex) for D, E, H, I; 16 per arm for the others. Sixteen per arm gives 91% power for 71% vs 12% survival, the worst-case reading of today's data; 32 per arm gives 89% power for 80% vs 40%, the margin assumed over a current-practice surrogate. Challenge cohorts about 320 aged mice, satellite read-outs 120, durability 72, C57BL/6 32. |
| **Timing** | Protocol and animal supply January 2027; dosing February; interim read-out of the day-14 mismatched challenge mid-April; immune read-outs May; day-90 challenge June; report August 2027. Staged: the matched-challenge and depletion cohorts are dosed only after the interim read-out. |
| **Go / stop** | **Go:** (i) E at least 40 survival points above D overall, same direction in each sex (met with 97% probability if today's worst-case rates are true, and 4% if the true difference is only 20 points); (ii) E above B and C, p < 0.05; (iii) E above the better of H and I after mismatched challenge, p < 0.05, and not worse on lung virus titre after matched challenge (upper confidence limit of the difference below 0.5 log10). **Stop or re-scope:** B matches E (the asset is then manganese, not the STING agonist); or H or I matches E on survival, virus titre and weight loss (no differentiation). |

**Study 2. Dose range, airway tolerability and manganese safety, non-GLP (January – July 2027)**

| Item | Specification |
|---|---|
| **Must establish** | The margin between the effective dose and the first adverse dose; whether manganese from PSLN-344 accumulates in the olfactory bulb or brain; whether lung inflammation resolves; tolerability of a second dose. |
| **Why (gap)** | Tolerability rests on body weight in 5 animals for 10 days [S08-D] and three brain transcripts at 36 h [S10-A]. Lung *Il6*, *Tnf* and *Ccl2* are 7.2×, 8.4× and 27× control at 72 h with no later time point [S09-A]. The neutrophil block is unusable (Q04). The manganese content of PSLN-344 is not in the file. A booster was given in S13-I/J with no tolerability read-out. |
| **Population** | Aged BALB/c (20 months), both sexes, 8 per group and time point (5 for tissue manganese); young adults at the top dose. |
| **Groups and comparators** | All with vaccine: buffer; empty liposome; PSLN-212 20 µg (manganese-free comparator); PSLN-344 at 5, 20, 40 and 80 µg; manganese chloride alone at the manganese dose of the 80 µg group (positive control for uptake); cholera toxin (positive control for brain inflammation, as in S10-A). One dose, and two doses 14 days apart. |
| **Primary endpoints** | Manganese by ICP-MS in olfactory bulb, striatum, cerebellum, lung, liver and blood at 1, 3, 7 and 28 days. Lung histopathology score and lavage cell differential (neutrophils) at 1, 3, 7, 14 and 28 days. |
| **Secondary endpoints and read-outs** | Daily weight and clinical score. Lung and serum IL-6, TNF, CCL2, IFN-β, IL-10 until back to baseline. Brain *Ifnb1*, *Tnf*, *Isg15* at 6 h, 36 h and 7 days, with microglia and astrocyte staining of the olfactory bulb. Olfaction (buried-food test) and motor function (rotarod) at days 7 and 28. Clinical chemistry. Anti-PEG IgM and IgG after the second dose (the liposome contains a PEG-lipid). |
| **Timing** | In-life February – May 2027; pathology and manganese analysis to July 2027. |
| **Go / stop** | **Go:** at 40 µg, twice the efficacy dose: no adverse histopathology, brain manganese not above buffer controls at day 28, weight loss ≤ 5% with recovery by day 10, lung cytokines at baseline by day 14. **Stop PSLN-344:** persistent manganese in brain or olfactory bulb, behavioural change, or unresolved lung pathology at or below 40 µg. PSLN-212 is not a fall-back for older adults (9/66 (14%) survival in aged mice). |

**Study 3. Human cells: STING variants and older donors (December 2026 – April 2027)**

| Item | Specification |
|---|---|
| **Must establish** | That CDN-1807 activates human STING across its common variants; that Mn²⁺ raises the ceiling of the response in myeloid cells from older donors as it does in mouse lung; that IFN-β, GM-CSF and CCL2 can serve as pharmacodynamic markers in people. |
| **Why (gap)** | There are no human data of any kind in the package. In mouse lung manganese raised the interferon plateau from 15× to 52× without changing the half-maximal dose (9 µg vs 11 µg) [S08-A]. *External:* STING agonists have failed before on mouse–human differences, and human STING has common variants that respond differently to cyclic dinucleotides. |
| **Population** | Monocytes, monocyte-derived macrophages and dendritic cells from donors aged ≥ 65 (n = 15) and 18–40 (n = 15), both sexes, STING-genotyped. Alveolar macrophages from lavage and primary airway epithelium where obtainable (n ≥ 5). Reporter cells carrying each common STING variant, and STING-deficient cells as the test of whether manganese acts through STING. |
| **Comparators** | Empty liposome; manganese liposome without CDN; free CDN-1807; PSLN-212; PSLN-344; cGAMP liposome (CMP-204). Six concentrations each. |
| **Primary endpoint** | IFN-β protein: plateau and half-maximal concentration for PSLN-344 against PSLN-212, by donor age group and by STING variant. |
| **Secondary read-outs** | GM-CSF, CCL2, CXCL10, IL-6, TNF, IL-10; cell viability. |
| **Go / stop** | **Go:** plateau with PSLN-344 at least twice that with PSLN-212 in cells from older donors; activity on every variant carried by more than 5% of people. **Stop or re-engineer:** no activity on a common variant, or no manganese effect in human cells. |

**Study 4. Product quality and delivery (January – September 2027)**

| Item | Specification |
|---|---|
| **Must establish** | That PSLN-344 can be made reproducibly to a specification that includes manganese; that it is stable and survives mixing with antigen and aerosolisation; and that a device exists which puts it where the mouse data say it acts. |
| **Why (gap)** | The only product-quality number in the file is encapsulation efficiency, 54.8% (SD 5.1, n=3), against 59.6% (SD 4.6, n=3) for PSLN-212 [S08-B]. Particle size, charge and storage are named in the annotation but no values are given. In mice the liposome acts through alveolar macrophages and alveolar epithelium [S01-B, S01-C]; *external:* a liquid dose instilled into a mouse nose reaches the lung, whereas a human nasal spray deposits mainly in the nose. |
| **Material** | Three independent batches at ten times the current scale or more. |
| **Read-outs** | Mn : CDN ratio and free Mn²⁺. Size, polydispersity, zeta potential. Encapsulation efficiency (target ≥ 70% with batch-to-batch coefficient of variation ≤ 10%, or a justified lower specification). CDN integrity. Release in simulated lung fluid. Stability of lyophilised product at −20 °C, 2–8 °C and 25 °C at 1, 3 and 6 months. Haemagglutinin potency after mixing. Sterility and endotoxin. Droplet size for nasal-spray and for nebuliser or soft-mist delivery, and potency after aerosolisation. |
| **Go / stop** | **Go:** specification met on three consecutive batches; at least 3 months stability at 2–8 °C; potency kept after aerosolisation; a delivery route defined for Study 5. **Stop or partner:** no reproducible specification, or no feasible route to the lower airway. |

**Study 5. Ferret: efficacy with a delivery method usable in people (October 2027 – July 2028; starts only after Gate 1)**

| Item | Specification |
|---|---|
| **Must establish** | Efficacy in the standard influenza species; whether deposition in the nose is enough or the lower airway must be reached; effect on virus shedding; safety in a second species. |
| **Population** | Ferrets, both sexes, 8–12 per group; influenza-naive and previously infected animals (in 14-month-old mice prior infection did not blunt PSLN-344: 6/7 with and 6/7 without prior infection [S06-F2]); older ferrets if obtainable. |
| **Groups and comparators** | Placebo; vaccine alone into the airway; vaccine + PSLN-344 by nasal spray; vaccine + PSLN-344 by aerosol to the lower airway at two doses; vaccine + PSLN-212; a licensed enhanced human vaccine given intramuscularly. |
| **Primary endpoint** | Virus titre in nasal wash (area under the curve, days 1–7) and in lung on day 4 after challenge with a drifted H3N2 virus 4 weeks after dosing; a second cohort challenged with a different subtype. |
| **Secondary read-outs** | Fever, weight, clinical score. HAI, neutralising and anti-neuraminidase antibody. Nasal IgA. IFN-γ ELISpot. Lung histopathology. Manganese in olfactory bulb and brain. Transmission to contact animals (exploratory). |
| **Go / stop** | **Go (Gate 2):** at least a ten-fold reduction in lung virus titre against vaccine alone, not worse than the licensed comparator against drifted virus, clean histopathology. Then GLP toxicology in two species and a GMP batch. |

**Line of sight to the clinic (not part of this request).** If Gate 2 is passed, the first human study would be a randomised, observer-blind, dose-escalating study in healthy adults aged 65 and over (after a sentinel cohort aged 50–64), about 30 per arm, against a licensed high-dose or adjuvanted seasonal vaccine and against unadjuvanted vaccine by the study route. Primary endpoint: safety, including nasal and respiratory reactions, spirometry, blood manganese, and facial palsy and other neurological events followed for 12 months. Secondary: HAI titre ratio and seroconversion at day 28. Exploratory: the biomarkers in Table 8. On the timeline above this is not before 2029.


---


## 3. The evidence behind the recommendation


### 3.1 Efficacy in aged animals

![fig1_survival_by_experiment.png](figures/fig1_survival_by_experiment.png)

<sub>Figure 2. Survivors / animals challenged in every survival experiment in the workbook, as printed. One intranasal dose of vaccine with the adjuvant shown; lethal challenge on the day shown; 14 days of observation (21 for S03-J). Flags refer to Appendix A.</sub>

**Table 3. Pooled survival of aged mice, PSLN-344 against PSLN-212, with sensitivity analyses**

| Analysis set | PSLN-344 | PSLN-212 | Difference (stratified by experiment) | Test |
|---|---|---|---|---|
| **As printed:** 9 experiments in aged BALB/c [S03-I, S03-J, S06-A–G] | 56/66 (85%)<br>95% CI 74–92% | 9/66 (14%)<br>95% CI 6–24% | 71 points (95% CI 60–82) | Stratified log-rank p = 2×10⁻¹⁸; hazard ratio 0.08 (95% CI 0.04–0.15) |
| **Conservative:** without S03-I, S03-J (comparator arms uncertain, Q11) and S06-C (identical to S06-D, Q03) | 32/42 (76%)<br>95% CI 61–88% | 4/42 (10%)<br>95% CI 3–23% | 67 points (95% CI 52–81) | Stratified log-rank p = 7×10⁻¹²; hazard ratio 0.11 (95% CI 0.05–0.23) |
| **Worst case:** conservative set, using the weight-trace count wherever it is less favourable to PSLN-344 or more favourable to PSLN-212 (Q10) | 30/42 (71%) | 5/42 (12%) | 60 points (95% CI 43–76) | Cochran–Mantel–Haenszel p = 2×10⁻⁷ |
| **All head-to-head experiments:** the 9 above + aged C57BL/6 + aged Swiss Webster + four groups of 14-month-old BALB/c | 92/108 (85%) | 15/108 (14%) | 71 points (95% CI 63–80) | PSLN-344 ahead in 15 of 15 |

- **Breadth.** Matched H1N1 challenge 7/7 [S03-I]; challenge with a different subtype 39/49 (80%) against 6/49 (12%) for PSLN-212 [S06-A–G]; wild-type H5N1 two days after one dose 10/10 [S03-J]; aged C57BL/6 6/7 and Swiss Webster 6/7 against 0/7 and 2/7 [S15-L, S15-N; challenge virus not stated]; 14-month-old animals with or without earlier infection 24/28 (86%) against 4/28 (14%) [S06-E2, S06-F2].
- **Onset and duration.** 28/31 (90%) survived challenge 2–3 days after the single dose, 20/21 (95%) at day 14 and 14/21 (67%) at day 60 (day 14 against day 60, p = 0.045). The day-60 figure needs care: unvaccinated, unchallenged aged controls lost 4/21 during the same 14 days [S06-E–G], so background mortality in animals this old is not negligible. But the PSLN-344 animals whose weight traces stop after day-60 challenge had fallen to 78–85% of starting weight, whereas the unchallenged controls that died were at 94–97% [S15-E–G]. I read this as partial waning, not only old age. Nothing is known beyond day 60 in aged animals; the only six-month data are in young mice, where all survived with either candidate but PSLN-344 animals recovered more slowly (Section 3.2).
- **Protection is from death, not from illness.** After challenge with a different subtype, PSLN-344 groups lost on average 11–16% of body weight at the lowest point, the young benchmark 9–12%, PSLN-212 groups 17–19% [S15-A, B, D–G]; after matched challenge PSLN-344 animals lost 8.5% [S13-F].
- **Antigen is required.** PSLN-344 without vaccine: 0/7 [S15-H]. The early protection is not a general antiviral state induced by the adjuvant.
- **Statistical caution.** Each experiment has 7–10 animals per arm and appears to have been run once; a single experiment of 7 per arm has 67% power for a difference as large as the pooled one. Taken singly, PSLN-344 differs from PSLN-212 at p < 0.05 in 9 of 9 experiments by log-rank test (permutation p up to 0.021) and in 7 of 9 by Fisher's test on survivor counts. The strength of the evidence is the consistency across experiments, not any one of them.


### 3.2 PSLN-344 against PSLN-212: which to take forward

- **In aged animals PSLN-344 is better on nearly every read-out** (Figure 3), and on about half of them it cannot be told apart from the young benchmark (21 of 39, five animals per group). HAI titres reach 76% and 87% of the young level for H1N1 and H3N2 (368 and 320 against 46 and 35 for PSLN-212) [S03-C, S03-G].
- **It does not restore everything.** Co-stimulatory molecules on lymph-node dendritic cells stay at 29% (CD40) and 38% (CD86) of the young level [S02-D]; IgG subclass titres at 35%–48% [S13-A, S13-B]; lung resident-memory CD8 T cells at 66% [S05-I].
- **In young animals manganese adds nothing, and at six months PSLN-344 does slightly worse.** Survival 24/24 with either; interferon-β 50.7-fold against 37.6-fold; dendritic cells, antigen transport and T-cell priming indistinguishable (Table 4). Even the cGAMP liposome protected 7/7 young animals [S13-E]: in young hosts the platform works whatever the payload. When young animals were challenged 180 days after dosing, all survived, but those given PSLN-344 lost more weight (12.7% against 10.7%, p = 0.03) and had regained less by day 14 (95.6% against 99.2% of starting weight, p = 0.004) [S09-G].
- **Conclusion.** PSLN-344 is the better asset because of, and only for, the aged setting. PSLN-212 is ahead on three counts only: it carries no manganese; it leaves less lung inflammation at 72 h, because it induces less (*Il6* 3.9× and *Ccl2* 5.2× lower) [S09-A]; and young animals recovered faster with it after the day-180 challenge. None of these gives it a use in older adults, but the last is a warning about durability that the day-90 cohort of Study 1 has to resolve. PSLN-212 stays in the plan as the comparator in Studies 1, 2 and 3.

![fig2_restoration_vs_young.png](figures/fig2_restoration_vs_young.png)

<sub>Figure 3. Immune read-outs in aged mice as a percentage of the young benchmark. Each row is one block with five animals per group (three for S04-D); geometric means for titres. PSLN-344 is closer to the young benchmark than PSLN-212 in 38 of 39 read-outs (37 at p < 0.05, Welch test, unadjusted); 32 are shown. The exception is *Ifnb1* at 72 h, which stays above the young level with both.</sub>

**Table 4. Young mice: PSLN-344 against PSLN-212**

| Read-out | PSLN-344, young | PSLN-212, young | Source |
|---|---|---|---|
| Survival, three challenge experiments (day 21, 21 and 180) | 24/24 | 24/24 | S09-B, S09-D, S09-F |
| Lung *Ifnb1* at 16 h, fold | 50.7 (1.3×; p = 0.009 Welch, 0.63 after Tukey) | 37.6 | S01-A |
| Lung CD11b+ dendritic cells, day 4 | 22.6% | 21.4% | S01-E |
| Lung cDC1, 72 h | 44.3% | 43.4% | S01-F |
| Antigen-carrying dendritic cells in lymph node | 11.1% | 9.4% | S02-C |
| CD8 T-cell priming by lymph-node dendritic cells | 31.4% | 26.2% | S02-E |
| Largest weight loss after challenge at day 21, 21 and 180 | 10.3%, 9.3%, 12.7% | 11.1%, 10.5%, 10.7% | S09-C, S09-E, S09-G |
| Body weight 14 days after the day-180 challenge, % of starting weight | 95.6% (p = 0.004) | 99.2% | S09-G |


### 3.3 Tolerability and safety

- **After dosing.** Mean largest weight loss 3.6% with PSLN-344 (worst animal 5.8%) against 1.8% with vaccine alone (p = 0.06) and 3.0% with PSLN-212; weight back to 99.8% by day 10 [S08-D]. Adding the TLR7/8 agonist R848 was not tolerated: 10.0% mean loss, 15.3% in the worst animal, 90.6% at day 10 with one of five animals missing.
- **Lung inflammation is strong and has not resolved by 72 h.** At 16 h PSLN-344 raised *Il6* 36×, *Tnf* 40× and *Ccl2* 590×; the young benchmark shows 60×, 14× and 1,391×, so *Il6* and *Ccl2* are no higher than in young animals but *Tnf* is. At 72 h they were still 7.2×, 8.4× and 27× (PSLN-212: 1.9×, 5.2×, 5.2×), three animals per group, and there is no later time point [S09-A]. Lung monocytes were still 18.4% at day 8 against 9.5% with empty liposome [S01-D]. This inflammation is the mechanism; it is also the main tolerability question for older people.
- **Brain.** 36 h after dosing, *Ifnb1* was 1.3× buffer (95% CI 0.8–2.0), *Isg15* 1.2× and *Tnf* 1.6× (95% CI 1.0–2.3; not significant after Tukey correction and not different from empty liposome); cholera toxin gave 5.5×, 2.7× and 3.4× [S10-A]. So there is no interferon signal in the brain at that time, but a two-fold change cannot be excluded, it is one time point, and manganese itself was not measured.
- **Not in the file at all.** Manganese dose and tissue exposure; histopathology of nose, lung or brain; clinical pathology; tolerability of a second dose; male animals; any GLP study. *External:* inhaled manganese is a recognised neurotoxicant that can reach the brain along the olfactory nerve, and an intranasal influenza vaccine with a toxin adjuvant was withdrawn after cases of facial palsy; regulators will ask about both.

![fig4_safety_tolerability.png](figures/fig4_safety_tolerability.png)

<sub>Figure 4. Tolerability read-outs. (a) Body weight after dosing without challenge. (b) Lung cytokine transcripts; the 72 h values come from the panel printed as "16h" on the right of sheet S09 (flag Q02). (c) Brain transcripts 36 h after dosing. (d) Largest weight loss after lethal challenge; animals that died are included.</sub>


### 3.4 Reliability of the data set

I parsed all 6,819 numeric cells and cross-checked every block against the annotation and against linked blocks. Appendix A lists the 22 flags with cell ranges; the 8 serious ones are in Table 5. They have the pattern of assembly errors (pasting and labelling), which the audit has to confirm, and they do not all point the same way: some make PSLN-344 look worse than the underlying numbers, some better.

**Table 5. The serious data-quality flags and what I did about them**

| Flag | Finding | Why it matters | Handling here |
|---|---|---|---|
| Q01 | IgG2a/IgG1 ratio blocks have rotated column headers [S03-B, S03-F] | As printed PSLN-344 looks Th2-skewed (ratio 0.58). Recomputed from the subclass titres it is 2.14 against 0.58 for PSLN-212 and 2.97 for young. | Recomputed from S13-A–D; printed blocks not used |
| Q02 | Second cytokine panel labelled "16h" is the 72 h time point [S09-A] | Its *Ifnb1* values equal the 72 h values of S01-A for 21 of 21 animals. Read correctly, it shows inflammation persisting at 72 h. | Analysed as 72 h |
| Q03 | Two survival experiments are identical [S06-C = S06-D] | Day-14 and day-3 rgH5N1 challenges carry the same death days in all four groups; the 7/7 result for PSLN-344 is counted twice. | S06-C dropped in the conservative analysis |
| Q04 | Neutrophil block duplicates the alveolar-macrophage block [S11-B ≈ S11-A] | 8 of 20 animal time-series identical; group means correlate r = 0.997. There is no usable neutrophil read-out. | S11-B excluded |
| Q05 | Weight traces re-used between experiments [S15-C = S15-I] | 40 of the 42 values for days 2–12 identical animal by animal; only day 14 differs. | S15-C weights for PSLN-344 not used |
| Q06 | Young C57BL/6 weights re-use young BALB/c traces from another adjuvant group [S15-M ≈ S09-E] | 6 of 7 animals match at four or more time points. Cross-strain weight evidence is not independent. | Cross-strain claim rests on survival blocks; graded moderate |
| Q10 | Survival and weight blocks disagree in 10 groups | For example day-3 rgH5N1: PSLN-344 7/7 in the survival block, 5/7 by weight traces; matched H1N1: PSLN-212 0/7 against 3/7. | Worst-case analysis uses the less favourable count |
| Q11 | Linked blocks list different groups [S03-I/S13-F; S03-J/S13-G] | In the wild-type H5N1 experiment the comparators are "Sham, PSLN-212" in one block and "Sham, Naïve" in the other. The PSLN-344 arm is 10/10 in both. | Reported as printed; not called a clean head-to-head; dropped in the conservative analysis |

**Table 6. Which conclusions survive the flags**

| Conclusion | Rests on | After removing flagged data or reading them least favourably |
|---|---|---|
| PSLN-344 protects aged mice where PSLN-212 does not | 9 survival experiments | **Holds.** 32/42 (76%) vs 4/42 (10%) in the six remaining experiments; worst case 30/42 (71%) vs 5/42 (12%) |
| Protection within 2–3 days of one dose | S03-J, S06-B, S06-D, S15-H | **Holds for the PSLN-344 arm.** S06-B 5/7 and S15-H 6/7 are unflagged; S06-D is 7/7 or 5/7 |
| Protection against wild-type H5N1 | S03-J only | **Holds for the arm** (10/10 in both linked blocks); what it was compared with is uncertain |
| Works in other mouse strains | S15-L, S15-N | **Moderate.** Survival blocks only; the weight blocks contain recycled traces; challenge virus not stated |
| Antibody restored to near the young level | S03-A, C, D, E, G, H; S13-A–D | **Holds.** These blocks are unflagged; the ratio blocks were corrected |
| Lung inflammation resolves | — | **Cannot be concluded.** Still raised at 72 h; neutrophil block unusable |
| Manganese does not change uptake by lung epithelium | S08-C | **No claim.** The block conflicts with S01-B for the same material (Q14) |


### 3.5 Formulation

Encapsulation efficiency is 54.8% (SD 5.1, n=3) for PSLN-344 and 59.6% (SD 4.6, n=3) for PSLN-212 (p = 0.29) [S08-B]. About 45% of the CDN is therefore not encapsulated, and the file does not say whether doses are stated as total or encapsulated CDN. The annotation says size, charge and morphology were measured and that the product is lyophilised with trehalose and stored at −20 °C, but gives no values. The manganese content is not stated anywhere.


## 4. Mechanism of action and biomarkers


### 4.1 Mechanism

![fig3_mechanism.png](figures/fig3_mechanism.png)

<sub>Figure 5. Mechanism supported by the data: the same liposome and the same STING agonist, with and without manganese, in aged lung. Source blocks for every number are in Table 7.</sub>

The liposome is the delivery system and is common to both candidates. What manganese changes is the size of the first signal. In aged lung PSLN-212 gives a type I interferon response less than half that of a young animal (16.6-fold against 37.6-fold); PSLN-344 gives the young response (37.1-fold). The dose-response shows a higher ceiling, not a shift in potency: plateau 52× against 15×, half-maximal dose 11 µg against 9 µg [S08-A], and encapsulation is the same. My reading of the chain: with the weaker signal, aged lung makes no GM-CSF, recruited monocytes become Ly6C+ macrophages instead of dendritic cells, regulatory T cells stay high and little antigen reaches the lymph node; with the stronger signal the cascade proceeds as in a young animal. Two links are inferred rather than tested: that manganese acts through STING, and which arm of immunity, antibody or CD8 T cells, protects against mismatched virus.

**Table 7. Mechanism: evidence for each step, in aged mice unless stated**

| Step | PSLN-344 vs PSLN-212 (young benchmark) | Causal test in our data | Strength |
|---|---|---|---|
| **1. Delivery to the alveolus** | Dye-labelled liposome in 15.8% of type II and 3.8% of type I alveolar epithelial cells, against 0.4% and 0.3% for free dye [S01-B]. Same liposome for both candidates. | Uptake by alveolar macrophages 43.1% in wild-type and 12.7% in SP-A/D-knockout mice [S01-C, young]. Gap-junction blocker cuts monocyte recruitment from 7.3% to 3.1% [S11-C]. | Causal, platform-level. Effect of Mn on uptake unresolved (Q14) |
| **2. STING → interferon-β; Mn²⁺ raises the ceiling** | *Ifnb1* at 16 h 37.1 vs 16.6-fold (37.6); ratio 2.2× (95% CI 1.8–2.7) [S01-A]. Plateau 52× vs 15×; half-maximal dose 11 µg vs 9 µg [S08-A]. cGAMP liposome 7.8-fold. | None. No manganese-only arm, no free CDN, no STING knockout. | Associative. **Key gap** |
| **3. GM-CSF and CCL2** | *Gm-csf* 6.0, 8.7, 3.9-fold at 16, 36, 72 h vs 1.5, 1.6, 1.4 [S02-F]. *Ccl2* at 16 h 590× vs 7.6× (1,391×) [S09-A, n = 3]. | Giving GM-CSF with PSLN-212 raises monocyte-derived dendritic cells from 5.9% to 13.8% [S02-G]. Marrow lacking the interferon receptor: 19.7% → 2.1%; GM-CSF restores to 12.4% [S02-H]. | Causal |
| **4. Monocytes become dendritic cells, not Ly6C+ macrophages** | Lung monocytes day 4: 30.6% vs 16.7% (32.2%) [S01-D]. CD11b+ dendritic cells day 4: 18.9% vs 8.3% (21.4%) [S01-E]. Ly6C+CCR2+ macrophages day 5: 3.4 vs 19.0 ×10⁵ [S07-A, n = 3]. CD206+ macrophages 49% vs 71% (36%) [S11-E]. | CCR2 antagonist: monocytes 9.9% → 3.3% [S07-B]; granzyme B+ CD8 T cells 6.8% → 1.4% [S02-I, young]. | Causal for recruitment. Macrophage → Treg link unproven (Q13) |
| **5. Migration, antigen transport, priming** | Migratory dendritic cells 30.7% vs 7.3% (35.0%) [S02-A]. Antigen-carrying dendritic cells in lymph node 7.1% vs 1.8% (9.4%) [S02-C]. CD8 priming ex vivo 18.7% vs 0.8% (26.2%) [S02-E]. CD40 11.2% vs 5.6% (38.7%) [S02-D]. | Pertussis toxin: antigen-carrying cells 7.1% → 2.4% [S02-C]; priming in lymph node 30.9% → 6.8% but in lung 59.0% → 55.1% [S05-C]. | Causal; T cells are also primed inside the lung |
| **6a. Germinal centre and antibody** | Germinal-centre B cells 6.5% vs 2.3% (9.8%) [S03-K]. Tfh:Tfr ratio 8.5 vs 2.9 [S04-B]; by day 30 Tfr no longer differ (14.0% vs 18.0%) [S04-C]. HAI 368 vs 46 (485); neutralising titre 3,840 vs 418 (6,686) [S03-C, S03-D]. IgG2a/IgG1 2.14 vs 0.58 (2.97) [S13-A/B]. | None. | Associative |
| **6b. CD8 T cells** | IFN-γ+ CD8 T cells responding to H5N1 antigen after H1N1 + H3N2 vaccine: 6.4% vs 1.5% at day 14, 9.9% vs 3.0% at day 60 [S05-F, S05-G]. Lung resident-memory CD8 T cells 4.0% vs 1.0% (6.0%) [S05-I]. | None. No CD8 or antibody depletion; antibody to the mismatched virus not measured. | Associative. Which arm gives cross-protection is not known |
| **7. Protection** | 56/66 (85%) vs 9/66 (14%) survival. | Without antigen 0/7 [S15-H]. | Direct |


### 4.2 Biomarkers

The chain in Table 7 gives markers at three levels: the first signal (hours), the cellular response (days) and the adaptive response (weeks). None has been tied to protection in the individual animal, because immune read-outs and challenge outcomes were taken from different animals; Study 1 is designed to do that, and Study 3 tests the first level in human cells.

**Table 8. Biomarkers to validate efficacy**

| Marker | What our data show (aged: PSLN-344 vs PSLN-212; young benchmark) | How to measure in people | Use, and caveat |
|---|---|---|---|
| **Interferon-β / interferon-stimulated genes** | *Ifnb1* 37.1 vs 16.6-fold at 16 h (37.6); back to 4.4-fold by 72 h [S01-A]; dose-dependent from 5 µg [S08-A] | Nasal lining fluid and blood at 12–24 h: IFN-β, CXCL10, interferon-gene score | **Target engagement, dose selection.** Separates the candidates by about two-fold only |
| **GM-CSF** | 8.7 vs 1.6-fold at 36 h; empty liposome 1.2 [S02-F]. Adding GM-CSF rescues PSLN-212 [S02-G] | Nasal lining fluid, sputum or lavage at 24–48 h | **Best discriminator of PSLN-344 from PSLN-212, and causal.** Transcript only so far; protein not measured |
| **CCL2 and blood monocytes** | *Ccl2* 590× vs 7.6× at 16 h [S09-A]; lung monocytes 30.6% vs 16.7% at day 4 [S01-D] | Serum CCL2 at 24 h; monocyte activation markers on days 1–4 | **Pharmacodynamic and tolerability marker**: also tracks the inflammation that must resolve |
| **Circulating Tfh and plasmablasts** | Lymph-node ICOS-high Tfh 10.3% vs 3.8% (13.6%); germinal-centre B cells 6.5% vs 2.3% at day 7 [S04-A, S03-K] | Blood, day 7: activated circulating Tfh, plasmablasts | **Early predictor of antibody response.** Blood surrogate of a lymph-node finding |
| **HAI and neutralising titre** | HAI 368 vs 46 (485) for H1N1, 320 vs 35 (368) for H3N2; neutralising 3,840 vs 418 [S03-C, G, D] | Serum, day 28 | **Accepted regulatory surrogate.** Not sufficient here: all 5/5 aged PSLN-212 animals had HAI ≥ 40 to H1N1, yet 0/7 (survival block) or 3/7 (weight block) survived matched challenge |
| **IgG subclass balance** | IgG2a/IgG1 2.14 vs 0.58 (2.97) for H1N1; 2.73 vs 0.51 (2.89) for H3N2 [S13-A–D] | Serum IgG1/IgG3 against IgG2/IgG4, day 28 | **Quality of the response.** Use the recomputed values, not S03-B/F as printed (Q01) |
| **Cross-reactive CD8 T cells** | IFN-γ+ CD8 to H5N1 antigen 6.4% vs 1.5% (9.2%) at day 14; 9.9% vs 3.0% at day 60 [S05-F, G] | Blood, days 14–28: IFN-γ / granzyme B ELISpot to conserved nucleoprotein and matrix peptides | **Marker for protection against mismatched virus.** Link to protection not yet tested |
| **Lung resident-memory CD8 T cells** | 4.0% vs 1.0% (6.0%) at day 25 [S05-I] | Nasal or bronchial sampling in a sub-study only | **Mechanistic.** Not accessible in routine trials |

Not measured at all, and needed for a vaccine given by the airway: mucosal IgA, virus titre in the lung after challenge, and antibody against the mismatched challenge virus. All three are in Study 1.

![fig5_pharmacodynamics.png](figures/fig5_pharmacodynamics.png)

<sub>Figure 6. Candidate pharmacodynamic markers. (a) The age of the animals in S08-A is not stated; the values match the aged groups of S01-A. Curves are three-parameter Hill fits.</sub>


## 5. Target demographic, for the TAM check

**Primary population: adults aged 65 and over who receive a seasonal influenza vaccine each year, both sexes.**

- **Why this group.** The product separates from its manganese-free twin only in aged animals (56/66 (85%) vs 9/66 (14%) survival), where it returns HAI titres to 76%–87% of the young-adult level. What it corrects is the age-related loss of vaccine response. *External rule of thumb:* a 20-month-old mouse corresponds to a person in the 60s.
- **Why not younger adults.** No advantage in young mice (24/24 vs 24/24 survival), and no evidence against current vaccines in any age group.
- **Product form.** An adjuvant needs an antigen. The TAM should be modelled per vaccinee for a combined product (our adjuvant with a partner's or our own inactivated seasonal antigen), or as a royalty on a partner's vaccine, not as a stand-alone drug.
- **Caveat for the model.** The BALB/c animals were all female and no male data exist. Nothing in the data speaks to men, frail or immunosuppressed people, or people with lung disease.

**Table 9. Segments for the TAM model**

| Segment | In the TAM? | Support in our data | What market research needs to supply (external) |
|---|---|---|---|
| Adults ≥ 65, annual seasonal vaccination | **Core** | Aged mice of three strains; survival 56/66 (85%) vs 9/66 (14%) | People ≥ 65 by market; vaccine coverage in that group; share already on high-dose, adjuvanted or recombinant vaccines and their price premium |
| Adults 50–64 | Upside | 14-month-old mice only: 24/28 (86%) vs 4/28 (14%) [S06-E2, S06-F2] | Size and coverage; whether enhanced vaccines are reimbursed below 65 |
| Pandemic and pre-pandemic H5N1 preparedness for older adults | Upside, procurement-led | Wild-type H5N1: 10/10 alive when challenged 2 days after one dose [S03-J, comparators uncertain]; seasonal vaccine + PSLN-344 protected against rgH5N1 [S06-D, S06-F] | Government stockpile programmes; not a per-head market |
| Older adults with asthma or COPD | Discount until shown safe | The product works by inflaming the lung: *Il6* 36×, *Tnf* 40× at 16 h [S09-A] | Prevalence of chronic lung disease in people ≥ 65; likely excluded from early labels |
| Adults under 50; children | Exclude | No advantage in young mice; no juvenile data | — |
| Immunocompromised | Exclude for now | No data | — |

*External context for the model, to be verified:* in the United States enhanced influenza vaccines are already preferentially recommended from age 65, so the realistic comparator and price anchor is an enhanced vaccine, not a standard one; and the licensed nasal influenza vaccine is a live vaccine not approved for older adults, so there is no needle-free option in this age group today. Acceptance of an inhaled or nasal product by older adults, and the late-stage mRNA and combination respiratory vaccines aimed at the same group, should be part of the TAM check.


## 6. If we drop it: what we give up, and why one might still drop

**What we would give up.**

1. **The only candidate we have that works in aged hosts.** 56/66 (85%) survival against 9/66 (14%) for the manganese-free version and 1/66 (2%) for vaccine with empty liposome; antibody (HAI) 8.0× (95% CI 3.9–16.4) and 9.2× (95% CI 4.2–20.2) higher than PSLN-212 [S03-C, S03-G].
2. **Protection against viruses the vaccine does not match.** 39/49 (80%) against 6/49 (12%) when the challenge virus was of a different subtype, including an H5N1 reassortant after a seasonal-type vaccine [S06-A–G].
3. **Fast onset from a single dose.** 28/31 (90%) survival when challenged 2–3 days after dosing [S03-J, S06-B, S06-D, S15-H].
4. **Dose-sparing potential.** 10 µg of PSLN-344 induced more interferon-β (21.1-fold) than 40 µg of PSLN-212 (14.9-fold) [S08-A].
5. **Indifference to earlier infection.** In 14-month-old mice PSLN-344 protected 6/7 with and 6/7 without prior influenza infection against H3N2; PSLN-212 protected 0/7 and 0/7 [S06-F2].
6. **A mechanism with ready-made markers** (Tables 7 and 8) that could transfer to other inactivated or subunit antigens given to older adults. The data do not test any antigen other than influenza.

**What we would not be giving up.** No human data, no GLP toxicology, no manufacturing process and no comparison with marketed vaccines exist; what would be written off is a mouse package. Keeping PSLN-212 alone would preserve nothing of value for older adults, and in young adults it has no demonstrated edge.

**The honest case for dropping.** (1) The safety bar for a preventive product given to healthy older people is very high, and this one delivers manganese and a strong inflammatory stimulus to the airway; Study 2 could end the program. (2) The route to market needs an antigen partner, a delivery device and a large efficacy trial against enhanced vaccines. (3) Protection is against death rather than illness, falls to 14/21 (67%) by day 60 in aged mice, and at six months in young mice recovery was slower than with PSLN-212. (4) Freedom to operate cannot be judged from the data; *external:* manganese–cyclic-dinucleotide particles and surfactant-like liposomes are both described in the academic literature. If the committee weighs these above an unreplicated mouse signal, dropping is defensible. My recommendation is to spend the eleven months to Gate 1 first: by then the safety, benchmark and attribution questions each have a yes-or-no answer for the cost of a mouse and cell programme, and a freedom-to-operate review can run alongside.


## 7. What I considered and ruled out

**Table 10. Options and interpretations considered and rejected**

| Considered | Why ruled out |
|---|---|
| **Take PSLN-212 forward**, alone or alongside PSLN-344 | 9/66 (14%) survival in aged mice. In young mice it equals PSLN-344 on survival (24/24 each) and recovers somewhat faster at day 180, but young adults are not where the unmet need is, and PSLN-212 was never compared with a current vaccine. Running both doubles toxicology and manufacturing for no added market. |
| **Go straight to IND-enabling work** | Five open questions in Section 1, each able to stop the program, can be answered first for far less. |
| **Drop now** | The effect is large, is present in 15 of 15 head-to-head experiments and survives the worst-case reading (30/42 (71%) vs 5/42 (12%)). |
| **PSLN-344 as a stand-alone antiviral or emergency prophylactic** | Without antigen it protected 0/7 [S15-H]. |
| **Young-adult, general-population or paediatric positioning** | No advantage in young mice (Table 4); no juvenile data. |
| **Oncology positioning** (the usual home of STING agonists) | There is not one tumour experiment in the data set. |
| **Adding the TLR7/8 agonist R848** | Weight loss 10.0% (worst 15.3%), not recovered by day 10 [S08-D]; interferon-β at 16 h 24.3-fold, below PSLN-344 (37.1); combined with PSLN-344 it lowered interferon-β (29.4 vs 45.8-fold at 20 µg) [S01-A, S08-A]. |
| **cGAMP as payload** (CMP-204) | Interferon-β 7.8-fold in aged lung, against 16.6 for CDN-1807 without manganese; 3/7 survival [S01-A, S03-I]. |
| **Rescuing PSLN-212 with GM-CSF or a booster** | GM-CSF rescue is a mechanistic tool (four daily doses of a recombinant protein; no survival data) [S02-G]. After a booster, PSLN-212 IgG was 4,411 (H1N1) and 1,086 (H3N2), still below one dose of PSLN-344 (7,305; 5,701) [S13-I/J, S03-A/E]; no challenge was done. |
| **"Manganese works by improving delivery"** | Encapsulation is the same (54.8% vs 59.6%); the half-maximal dose is the same; only the ceiling rises [S08-A, S08-B]. The uptake block is unresolved (Q14). |
| **Reading the workbook as printed** | Would have shown PSLN-344 with the lowest IgG2a/IgG1 ratio (0.58; recomputed value 2.14), a second "16 h" cytokine panel, and an independent replicate of the rgH5N1 result. See Appendix A. |
| **Using these blocks as evidence** | S11-B (neutrophils; duplicate), S07-C (both columns carry the same label; 10.4% vs 5.1%), S05-A/B (two animals per point, contradictory conditions), S08-C (conflicts with S01-B), S08 rows 89–101 (unlabelled). |
| **Fisher tests on single experiments as the main analysis** | 67% power at 7 per arm. I pooled across experiments with stratification and give the individual results in Figure 2. |
| **Arithmetic means for titres; "0" HAI titres as zero** | Titres analysed on the log scale with geometric means; HAI below the lowest dilution (1:10) set to 5. |
| **Claims I do not think the data support** | "Restores the aged response to young" (CD40/CD86 at 29%/38% of young); "sterilising" (weight loss 11–16%); "durable" (14/21 (67%) at day 60 in aged mice, nothing later; slower recovery than PSLN-212 at day 180 in young mice); "safe for the brain" (three transcripts, one time point); "universal influenza vaccine" (survival only, in mice). |


---


## Appendix A. Data-quality log

Every flag was derived by script from the workbook and the annotation (qc_log.py and the qc_*.csv files in the analysis folder). The rating reflects the effect on conclusions, not a judgement about cause.

| ID | Rating | Blocks | Finding and evidence | Effect | Handling here / action for Gate 0 |
|---|---|---|---|---|---|
| Q01 | High | S03-B, S03-F vs S13-A..D | **Column headers of the IgG2a/IgG1 quotient blocks are rotated relative to the subclass titres they are computed from.** S03-B columns reproduce the S13-A/S13-B quotients exactly (5/5 animals each) but under other names: printed "PSLN-212" = quotient of PSLN-212(Y); printed "PSLN-344" = quotient of PSLN-212; printed "PSLN-212(Y)" = quotient of PSLN-344. S03-F shows the same rotation against S13-C/S13-D ("PSLN-212" = PSLN-212(Y); "PSLN-344" = PSLN-212; "PSLN-212(Y)" = PSLN-344). The rank order of total IgG (S03-A/E: PSLN-212 < PSLN-344 < PSLN-212(Y)) agrees with the S13 labels. | As printed, PSLN-344 would look Th2-skewed (ratio 0.58 / 0.51, the lowest of the three). Recomputed from S13: PSLN-344 2.14 / 2.73; PSLN-212 0.58 / 0.51; PSLN-212(Y) 2.97 / 2.89 (means). | S03-B and S03-F not used as printed; ratios recomputed from S13-A..D. / Confirm group identity of S13-A..D and S03-B/F columns against plate maps. |
| Q02 | High | S09-A (cols X-AS) vs S01-A | **Both cytokine panels on S09 are labelled "16h"; the right-hand panel is the 72 h time point.** 10^(Ifnb1 row) of the right panel (S09!Y3:AS3) equals the 72 h Ifnb1 values of S01-A (S01!H3:L9) for 21/21 animals; the left panel (S09!B3:V3) equals the 16 h values (S01!B3:F9) for 21/21. The "PBS" group of S09-A carries the values of the "Sham" group of S01-A. | Read as printed, the right panel would be taken as a discordant 16 h replicate. Read correctly it shows that Il6, Tnf, Ccl2 are still elevated at 72 h with PSLN-344. | Right panel analysed as 72 h. Control group treated as the common control (PBS/Sham identity unresolved). / Correct the label; confirm whether the control was PBS or empty liposome. |
| Q03 | High | S06-C vs S06-D | **Two nominally different challenge experiments (rgH5N1 at day 14 vs day 3) carry identical time-to-event data in all four groups.** S06!M3:Q30 equals S06!A34:E61 in all four groups; Sham deaths on days 4,4,5,6,6,6,7 and PSLN-212 deaths on days 5,8,10,10,12 in both. The linked body-weight blocks differ from each other (S15-C vs S15-D), and S15-D implies 5/7, not 7/7, survivors for PSLN-344 and for PSLN-212(Y). Separately, the Sham columns of S06-B and S06-F carry the same seven death days (4,4,4,5,5,6,6); their other columns differ. | One of the two blocks is probably a paste of the other; the 7/7 PSLN-344 result is counted twice in any pooled analysis. | Primary pooled analysis as printed; sensitivity analysis drops S06-C and uses body-weight-inferred counts for S06-D. / Retrieve both survival records from cage cards. |
| Q04 | High | S11-A vs S11-B | **The neutrophil block (S11-B) largely duplicates the alveolar-macrophage block (S11-A).** 8 of 20 animal time-series are identical at ≥ 4 of 5 time points (Vaccine rep1=rep1 (4/5); Vaccine rep2=rep2 (5/5); PSLN-212 rep1=rep1 (5/5); PSLN-212 rep4=rep2 (5/5); PSLN-344 rep1=rep1 (5/5); PSLN-344 rep2=rep2 (5/5); PSLN-212(Y) rep1=rep1 (5/5); PSLN-212(Y) rep2=rep2 (5/5)); the 20 group-by-day means correlate r=0.997 (max difference 2.5 points). | There is no independent neutrophil data set, i.e. no usable read-out of acute lung inflammation by cell influx. | S11-B excluded. S11-A used only descriptively. / Re-export neutrophil gate from FACS files. |
| Q05 | High | S15-C (PSLN-344) vs S15-I (3d Vaccine+PSLN-344) | **Body-weight traces of the PSLN-344 group after day-14 rgH5N1 challenge are the traces of a different experiment (day-3 challenge).** 40 of the 42 values for days 2-12 are identical animal by animal (S15!W24:AC29 vs S15!W73:AC78); 7/7 animals match at ≥ 4 time points; 0 of 7 day-14 values match. | S15-C weight data for PSLN-344 are not independent evidence; the day-14 values in S15-C do not continue the traces (e.g. animal 3: 77.9 at day 12, 90.1 at day 14). | S15-C PSLN-344 weights not used. Survival taken from S06-C with flag Q03. / Locate the true S15-C weights. |
| Q06 | High | S15-M (young C57BL/6, PSLN-212(Y)) vs S09-E (young BALB/c, PSLN-344Y) | **Weight traces of the young C57BL/6 reference group re-use traces from a BALB/c experiment with a different adjuvant.** 33 of 49 post-baseline values identical; 6/7 animals match at ≥ 4 of 7 time points (S15!I104:O110 vs S09!W40:AD46). | Cross-strain weight evidence (S15-M) is not independent. S15-M also shows 7/7 young animals alive while S15-L records one death (day 12). | Cross-strain conclusions rest on the time-to-event blocks S15-L/N only and are graded "moderate". / Source-verify S15-L..O. |
| Q07 | Medium | S15-A / S15-M / S15-O (PSLN-344) | **Several PSLN-344 animals share weight traces across BALB/c, C57BL/6 and Swiss Webster experiments.** S15-A vs S15-M: 16 identical values, 3 animals at ≥ 4 time points; S15-A vs S15-O: 7 values, 1 animal(s); S15-M vs S15-O: 11 values, 1 animal(s). | Same as Q06. | Same as Q06. / Same as Q06. |
| Q08 | Medium | S09-C | **Day-12 weights of PSLN-344Y are a copy of the PSLN-212Y row.** S09!W18:AD18 equals S09!G18:N18 in order (8/8 identical). | Minor; young-mouse weight comparison at day 12 is uninformative. | Day 12 ignored for PSLN-344Y vs PSLN-212Y. / Correct from balance log. |
| Q09 | Low | S09-E vs S09-G (PSLN-212Y) | **One young animal has the same weight trace in two experiments.** 1 animal identical at all 7 post-baseline time points (S09!N40:N46 vs S09!N67:N73). | Minor. | None needed. / Correct from balance log. |
| Q10 | High | Time-to-event blocks vs their linked body-weight blocks | **Survivor counts or animal numbers disagree between the survival block and the weight block of the same animals in 10 groups.** S09-F/S09-G Sham: survival block 0/7, weight traces imply 0/8; S03-I/S13-F PSLN-212: survival block 0/7, weight traces imply 3/7; S03-J/S13-G Sham: survival block 1/10, weight traces imply 5/10; S06-C/S15-C PSLN-212: survival block 2/7, weight traces imply 1/7; S06-D/S15-D PSLN-212(Y): survival block 7/7, weight traces imply 5/7; S06-D/S15-D PSLN-344: survival block 7/7, weight traces imply 5/7; S06-E/S15-E PSLN-212: survival block 0/7, weight traces imply 1/7; S06-E/S15-E PSLN-344: survival block 5/7, weight traces imply 6/7; S06-G/S15-G PSLN-344: survival block 4/7, weight traces imply 5/7; S15-L/S15-M PSLN-212(Y): survival block 6/7, weight traces imply 7/7. (Weight traces frozen at a constant value to day 14, or blank, are read as deaths; the annotation describes these groups as "declining".) | Individual survival fractions are uncertain by 1-3 animals in the flagged groups; direction of every PSLN-344 vs PSLN-212 comparison is unchanged. | Survival blocks used as printed; worst-case sensitivity analysis uses the weight-inferred count wherever it is less favourable to PSLN-344 or more favourable to PSLN-212. / Reconcile against humane-endpoint records. |
| Q11 | High | S03-I vs S13-F; S03-J vs S13-G | **Survival and weight blocks said to describe the same animals list different groups.** S03-I lists Sham, CMP-204, PSLN-212, PSLN-344, PSLN-212(Y); S13-F lists PSLN-212(Y), Sham, PSLN-212, PSLN-344, Naïve. S03-J lists Sham, PSLN-212, PSLN-344; S13-G lists PSLN-344, Sham, Naïve. In S13-G the 'Sham' traces (5 dead by d14, deaths from d10) resemble S03-J 'PSLN-212' (deaths d10-12, 3/10 alive) and the 'Naive' traces (1/10 alive, two deaths by d4) resemble S03-J 'Sham' (1/10 alive, deaths d3, d4, d9-10). | The identity of the comparator arms in the wild-type H5N1 experiment is uncertain (PSLN-212 and Sham, or Sham and Naive). The PSLN-344 arm (10/10 alive in both blocks) is not affected. In S03-I the PSLN-212 arm (0/7, all dead by day 6, faster than Sham) conflicts with S13-F (3/7 alive). | S03-I and S03-J reported as printed but excluded from the conservative pooled analysis; S03-J not described as a clean head-to-head. / Establish the true arm list for both experiments. |
| Q12 | Medium | S03-J, S05-A/B, S13-E, S09-F, S08-D | **Stated n differs from the number of observations.** S03-J stated n=9, 10 rows per group, and one PSLN-344 row has status 0 but no day (S03!J46, G46 empty); S05-A/B stated n=3, 2 values per group and day; S13-E stated n=5, 7 per group; S09-F Sham has 7 events for 8 animals in the weight block S09-G (the annotation attributes the 7 to S09-B, where the workbook has 8); S08-D PSLN-212/R848 has 4 of 5 values at day 10 (S08!W26 empty). | Denominators uncertain by one animal in the affected groups. | Observed counts used; the PSLN-344 row without a day treated as censored at the end of observation. / Reconcile n per group. |
| Q13 | Medium | S07-C | **Both columns carry the same header ("Ly6C-CD206+ MPhi").** S07!B15 and S07!C15 identical; means 10.4 vs 5.1 % lung Treg. | Cannot tell which macrophage subset raised lung Treg; the macrophage-to-Treg link in the mechanism is unproven. | Not used. / Recover the labels. |
| Q14 | Medium | S08-C vs S01-B | **Epithelial-uptake block is inconsistent with the earlier block for the same formulation.** S01-B: AECII/PSLN-SRB mean 15.8 %, AECI/PSLN-SRB 3.8 %. S08-C as printed: AECII-PSLN-SRB 15.8, AECII-PSLN-344-SRB 3.8, AECI-PSLN-SRB 13.8, AECI-PSLN-344-SRB 3.0. The first two S08-C columns share 3 and 2 of 5 values with the S01-B AECII and AECI columns. | Either Mn lowers epithelial uptake about four-fold (as printed) or the column order is AECII, AECI, AECII, AECI and Mn changes nothing. Unresolved. | No claim made on the effect of Mn on uptake. / Check column order against FACS export; gating differs between the two blocks. |
| Q15 | Low | S08 rows 89-101 | **Unlabelled numeric region.** S08!A89:A101 = 14; S08!C89:C94 = 0; S08!D95:D101 = 0. Looks like the censored tail of a survival block (6 + 7 animals). | None (cannot be attributed). | Excluded. / Identify or delete. |
| Q16 | Low | S06 (labels), S09 (labels) | **Duplicate block labels.** "S06-E" and "S06-F" are each used for two different experiments (rows 32 and 69); "S09-A 16h" is used twice. | Risk of citing the wrong block. | Second S06-E/S06-F referred to here as S06-E2/S06-F2 (imprinting experiments). / Rename. |
| Q17 | Medium | S05-A, S05-B, S05-I | **Conditions contradictory and n=2.** Annotation gives both ovalbumin and bivalent-vaccine immunisation for a read-out (NP366-374 tetramer) that requires influenza antigen; strain not stated; 2 animals per point. | Tetramer kinetics are illustrative only. | Reported descriptively; not used for decisions. / Clarify protocol and strain. |
| Q18 | Low | S08-A | **Undefined preparation and age not stated.** "PSLN-344/R848" appears only in S08-A and is not defined under Materials; the age of the animals is not given (values at 20 ug match the aged groups of S01-A). | Minor. | Dose-response interpreted as aged animals, flagged. / Confirm. |
| Q19 | Low | S13-H, S14-A, S11-E, S07-B, S15-L..O, S06-E2 | **Time point, challenge virus or interval not stated.** S13-H, S14-A, S11-E, S07-B: time point missing; S15-L/N: challenge virus and interval missing; S06-E2: interval missing; S03-J: challenge dose missing and observation stated as 22 days (workbook censors at day 21). | Limits interpretation of kinetics. | Stated where relevant. / Complete the annotation. |
| Q20 | Medium | S06-E/F/G Untreated; S15-E/F/G | **Unvaccinated, unchallenged aged controls died during the 14-day window.** Deaths without challenge: S06-E 1/7, S06-F 0/7, S06-G 3/7 = 4/21; their weights stayed at 94-100 % (S15!AD43:AJ70). | Background mortality of about 19 % in 14 days among untreated aged animals (stated age 20 months) limits what the day-60 challenge can show. | Day-60 results interpreted against this background. / Use younger "aged" animals (18 months) for durability work. |
| Q21 | Low | File metadata | **Data cut-off earlier than the review date.** Workbook last modified 2026-09-03; annotation PDF created 2026-09-15. | Anything generated after early September 2026 is not in this analysis. | Stated on the title page. / Confirm no newer data exist. |
| Q22 | Low | S09-E, S15-A..G, S15-J..O, S08-D | **Mixed numeric precision within weight blocks.** Values with 5-8 decimals sit next to 1-decimal values in the same group (e.g. S09!W40:Y44, S15!B24:D29). | Suggests values assembled from more than one source. | None. / Explain during audit. |


## Appendix B. Evidence ledger: source of each data-derived number

In order of first appearance in the text (the column "Cited" gives the section): value as cited, what it is, where it comes from and how it was computed. The evidence workbook (PSLN_evidence_workbook.xlsx) holds the same table with the raw values, plus every other computed number, per-block statistics and the tidy data. Design parameters of the proposed studies and the counts quoted from Appendix A are not repeated here.

| ID | Cited | Value as cited | What it is | Source blocks (cells) | Method |
|---|---|---|---|---|---|
| E489 | §1 | 6,819 | Numeric cells in the workbook | all 15 sheets | openpyxl count |
| E033 | §1 | 0/7 | Survival, aged BALB/c, "3d PSLN-344", rgH5N1 challenge 3 days later | S15-H (S15!C80:C86) | Count |
| E032 | §1 | 0/7 | Survival, aged BALB/c, "3d Vaccine", rgH5N1 challenge 3 days later | S15-H (S15!B73:B79) | Count |
| E034 | §1 | 6/7 | Survival, aged BALB/c, "3d Vaccine+PSLN-344", rgH5N1 challenge 3 days later | S15-H (S15!D87:D93) | Count |
| E001 | §1 | 56/66 (85%) | Pooled 14-day survival, aged BALB/c, vaccine + PSLN-344, nine challenge experiments as printed | S03-I, S03-J, S06-A, S06-B, S06-C, S06-D, S06-E, S06-F, S06-G (S03!A17:F51; S03!G17:J46; S06!A3:Q30; S06!A34:R68; S06!A71:F105) | Sum of survivors / animals; event column 0 = alive at end of observation |
| E005 | §1 | 9/66 (14%) | Pooled 14-day survival, aged BALB/c, vaccine + PSLN-212, nine challenge experiments as printed | S03-I, S03-J, S06-A, S06-B, S06-C, S06-D, S06-E, S06-F, S06-G (S03!A17:F51; S03!G17:J46; S06!A3:Q30; S06!A34:R68; S06!A71:F105) | Sum of survivors / animals; event column 0 = alive at end of observation |
| E009 | §1 | 1/66 (2%) | Pooled 14-day survival, aged BALB/c, vaccine + Sham, nine challenge experiments as printed | S03-I, S03-J, S06-A, S06-B, S06-C, S06-D, S06-E, S06-F, S06-G (S03!A17:F51; S03!G17:J46; S06!A3:Q30; S06!A34:R68; S06!A71:F105) | Sum of survivors / animals; event column 0 = alive at end of observation |
| E019 | §1 | 0.08 (95% CI 0.04–0.15) | Hazard ratio for death, PSLN-344 vs PSLN-212, Cox model stratified by experiment, set A | S03-I, S03-J, S06-A, S06-B, S06-C, S06-D, S06-E, S06-F, S06-G (S03!A17:F51; S03!G17:J46; S06!A3:Q30; S06!A34:R68; S06!A71:F105) | R survival::coxph with strata(block); script check_lr.R; stratified log-rank chi-square identical in R and Python |
| E003 | §1 | 32/42 (76%) | Pooled survival, aged BALB/c, PSLN-344, conservative set (S03-I, S03-J, S06-C removed for unresolved flags Q03/Q10/Q11) | S06-A, S06-B, S06-D, S06-E, S06-F, S06-G (S06!A3:K30; S06!A34:R68; S06!A71:F105) | Sum of survivors / animals |
| E007 | §1 | 4/42 (10%) | Pooled survival, aged BALB/c, PSLN-212, conservative set (S03-I, S03-J, S06-C removed for unresolved flags Q03/Q10/Q11) | S06-A, S06-B, S06-D, S06-E, S06-F, S06-G (S06!A3:K30; S06!A34:R68; S06!A71:F105) | Sum of survivors / animals |
| E014 | §1 | 30/42 (71%) | Worst case for PSLN-344: conservative set, with body-weight-inferred survivor counts wherever they are less favourable to PSLN-344 or more favourable to PSLN-212 | S06-A,B,D,E,F,G + S15-A..G (see qc_tte_vs_bodyweight) | Counts replaced: S06-D PSLN-344 7→5; S06-E PSLN-212 0→1 |
| E015 | §1 | 5/42 (12%) | Worst case, PSLN-212 | as above | as above |
| E035 | §1 | 24/24 | Young BALB/c, pooled survival, PSLN-344Y, three challenge experiments (day 21, 21, 180) | S09-B, S09-D, S09-F (S09!A12:D35; S09!A39:D62; S09!A66:D88) | Sum |
| E091 | §1 | 37.1 | Lung Ifnb1 mRNA 16 h after dosing, fold over untreated: PSLN-344, mean (n=5) | S01-A_16h (S01!B8:F8) | mean |
| E092 | §1 | 16.6 | Lung Ifnb1 mRNA 16 h after dosing, fold over untreated: PSLN-212, mean (n=5) | S01-A_16h (S01!B5:F5) | mean |
| E095 | §1 | 37.6 | Lung Ifnb1 mRNA 16 h after dosing, fold over untreated: young benchmark (PSLN-212(Y)), mean | S01-A_16h (S01!B9:F9) | mean |
| E129 | §1 | 8.7 | Lung Gm-csf mRNA fold, 36h, PSLN-344, mean (n=5) | S02-F (S02!B18:F18) | mean |
| E130 | §1 | 1.6 | Lung Gm-csf mRNA fold, 36h, PSLN-212, mean (n=5) | S02-F (S02!G18:K18) | mean |
| E451 | §1 | 38 | Read-outs in which PSLN-344 is closer to the young benchmark than PSLN-212 (on the ratio scale) | as above | \|log(aged/young)\| comparison |
| E450 | §1 | 39 | Number of single-time-point immunology read-outs that include PSLN-212 aged, PSLN-344 aged and the young benchmark | S01-A_16h; S01-A_72h; S01-F; S01-G; S02-A; S02-B; S02-C; S02-D_CD40; S02-D_CD86; S02-E; S03-A; S03-C; S03-D; S03-E; S03-G; S03-H; S03-K; S04-A_ICOSlo; S04-A_ICOShi; S04-B_Tfr; S04-B_TfhTfr; S04-C; S04-D; S05-D; S05-E; S05-F; S05-G; S05-H; S05-I; S11-E; S13-A; S13-B; S13-C; S13-D; S13-H; S13-I; S13-J; S14-A_H1N1; S14-A_H3N2 | see restoration_index.csv |
| E515 | §1 | 69% | Median of PSLN-344 (aged) as % of young benchmark across the deficit read-outs | as above | median of ratios of (geometric) means |
| E516 | §1 | 18% | Median of PSLN-212 (aged) as % of young benchmark across the deficit read-outs | as above | median of ratios of (geometric) means |
| E487 | §1 | 22 | Number of data-quality flags raised | all | see qc_log.csv / Appendix A |
| E488 | §1 | 8 | Flags rated High | all | see qc_log.csv |
| E500 | §1 | 10 | Groups in which the survival block and the linked weight block imply different survivor counts or animal numbers | S09-F/S09-G Sham; S03-I/S13-F PSLN-212; S03-J/S13-G Sham; S06-C/S15-C PSLN-212; S06-D/S15-D PSLN-212(Y); S06-D/S15-D PSLN-344; S06-E/S15-E PSLN-212; S06-E/S15-E PSLN-344; S06-G/S15-G PSLN-344; S15-L/S15-M PSLN-212(Y) | see qc_tte_vs_bodyweight.csv |
| E168 | §1 | 7.2× | Lung Il6 mRNA, 72h panel of S09-A (right panel, printed 16h, identified as 72 h, flag Q02), PSLN-344: geometric-mean fold over control (95% CI 2.3-22.2; n=3) | S09-A (S09!AN4:AP4) | 10^(mean log10 difference vs control); Welch CI |
| E172 | §1 | 8.4× | Lung Tnf mRNA, 72h panel of S09-A (right panel, printed 16h, identified as 72 h, flag Q02), PSLN-344: geometric-mean fold over control (95% CI 3.4-21.0; n=3) | S09-A (S09!AN8:AP8) | 10^(mean log10 difference vs control); Welch CI |
| E176 | §1 | 27× | Lung Ccl2 mRNA, 72h panel of S09-A (right panel, printed 16h, identified as 72 h, flag Q02), PSLN-344: geometric-mean fold over control (95% CI 10.0-75.4; n=3) | S09-A (S09!AN5:AP5) | 10^(mean log10 difference vs control); Welch CI |
| E492 | §1 | 15 of 15 | Head-to-head survival comparisons (aged BALB/c x9, aged C57BL/6, aged Swiss Webster, 14-month BALB/c x4) in which PSLN-344 has the higher survival fraction | S03-I/J, S06-A..G, S15-L, S15-N, S06-E2, S06-F2 | count |
| E036 | §1 | 24/24 | Young BALB/c, pooled survival, PSLN-212Y, three challenge experiments (day 21, 21, 180) | S09-B, S09-D, S09-F (S09!A12:D35; S09!A39:D62; S09!A66:D88) | Sum |
| E100 | §1 | 1.3× | Ifnb1 16 h, young mice: PSLN-344/PSLN-212 ratio of geometric means; Welch p=0.0092, Tukey p=0.63 | S01-A (S01!B9:F9; S01!B10:F10) | Welch t-test on log10; Tukey |
| E456 | §1 | 3.6% | Mean of per-animal maximum weight loss over 10 days after immunisation, PSLN-344 (n=5) | S08-D (S08!Q21:U26) | per-animal minimum of % day-0 weight, days 2-10 |
| E457 | §1 | 5.8% | Largest individual weight loss after immunisation, PSLN-344 | S08-D (S08!Q21:U26) | max |
| E470 | §1 | 1.3× | CNS Ifnb1 mRNA 36 h after dosing, PSLN-344 vs buffer: ratio of geometric means (95% CI 0.84-2.01); Tukey p=0.50; Welch p=0.20 | S10-A (S10!A3:A7; S10!C3:C7) | Welch on log10; ANOVA + Tukey |
| E471 | §1 | 0.8–2.0 | 95% CI of the above | S10-A | Welch |
| E472 | §1 | 5.5× | CNS Ifnb1, cholera toxin vs buffer: ratio of geometric means | S10-A (S10!D3:D7) | as above |
| E483 | §1 | 54.8% (SD 5.1, n=3) | Encapsulation efficiency, PSLN-344 | S08-B (S08!M11:O11) | mean, SD |
| E088 | §2 | 67% | Power of a single n=7 per arm experiment to detect 85% vs 14% survival (Fisher exact, two-sided 5%) | design calculation | Exact enumeration of binomial outcomes |
| E118 | §2 | 91% | PSLN-344: mean Ifnb1 at 20 µg as % of 40 µg | S08-A (S08!H6:J7) | ratio of means |
| E518 | §2 | 91% | Power with 16 per arm for 71% vs 12% survival (Fisher exact, two-sided 5%) | design calculation | Exact enumeration |
| E517 | §2 | 89% | Power with 32 per arm for 80% vs 40% survival (Fisher exact, two-sided 5%) | design calculation | Exact enumeration |
| E532 | §2 | 97% | Probability that Study 1 meets its go rule for E vs D if the true survival rates are the worst-case estimates (71% vs 12%) | design calculation | Simulation, 400,000 draws, 16 per sex per arm |
| E533 | §2 | 4% | Probability that Study 1 meets its go rule for E vs D if the true difference is only 20 points (40% vs 20%) | design calculation | Simulation, 400,000 draws, 16 per sex per arm |
| E114 | §2 | 15× | Fitted plateau (Emax) of Ifnb1 induction, PSLN-212 (SE 1.3) | S08-A (S08!E3:G7) | Three-parameter Hill fit, fold = 1 + Emax*D^h/(ED50^h + D^h), least squares on individual values (n=3 x 5 doses) |
| E112 | §2 | 52× | Fitted plateau (Emax) of Ifnb1 induction, PSLN-344 (SE 3.9) | S08-A (S08!H3:J7) | Three-parameter Hill fit, fold = 1 + Emax*D^h/(ED50^h + D^h), least squares on individual values (n=3 x 5 doses) |
| E115 | §2 | 9 µg | Fitted ED50, PSLN-212 (SE 1.4) | S08-A (S08!E3:G7) | Hill fit |
| E113 | §2 | 11 µg | Fitted ED50, PSLN-344 (SE 1.2) | S08-A (S08!H3:J7) | Hill fit |
| E484 | §2 | 59.6% (SD 4.6, n=3) | Encapsulation efficiency, PSLN-212 | S08-B (S08!D11:F11) | mean, SD |
| E054 | §2 | 6/7 | S06-F2 Imprinting+PSLN-344 | S06-F2 (S06!Q92:Q98) | Count |
| E058 | §2 | 6/7 | S06-F2 Naïve+PSLN-344 | S06-F2 (S06!P85:P91) | Count |
| E002 | §3 | 74–92% | Exact (Clopper-Pearson) 95% CI for the pooled proportion, PSLN-344 | S03-I, S03-J, S06-A, S06-B, S06-C, S06-D, S06-E, S06-F, S06-G (S03!A17:F51; S03!G17:J46; S06!A3:Q30; S06!A34:R68; S06!A71:F105) | Clopper-Pearson |
| E006 | §3 | 6–24% | Exact (Clopper-Pearson) 95% CI for the pooled proportion, PSLN-212 | S03-I, S03-J, S06-A, S06-B, S06-C, S06-D, S06-E, S06-F, S06-G (S03!A17:F51; S03!G17:J46; S06!A3:Q30; S06!A34:R68; S06!A71:F105) | Clopper-Pearson |
| E493 | §3 | 71 points (95% CI 60–82) | Mantel-Haenszel difference in survival, PSLN-344 minus PSLN-212, set A, stratified by experiment | see set definition | Mantel-Haenszel risk difference, Greenland-Robins variance |
| E017 | §3 | p = 2×10⁻¹⁸ | Stratified log-rank test, PSLN-344 vs PSLN-212, set A (chi-square 76.5, 1 df) | S03-I, S03-J, S06-A, S06-B, S06-C, S06-D, S06-E, S06-F, S06-G (S03!A17:F51; S03!G17:J46; S06!A3:Q30; S06!A34:R68; S06!A71:F105) | Log-rank stratified by experiment; verified against R survival::survdiff |
| E004 | §3 | 61–88% | Exact 95% CI, conservative set, PSLN-344 | S06-A, S06-B, S06-D, S06-E, S06-F, S06-G | Clopper-Pearson |
| E008 | §3 | 3–23% | Exact 95% CI, conservative set, PSLN-212 | S06-A, S06-B, S06-D, S06-E, S06-F, S06-G | Clopper-Pearson |
| E494 | §3 | 67 points (95% CI 52–81) | Mantel-Haenszel difference in survival, PSLN-344 minus PSLN-212, set B, stratified by experiment | see set definition | Mantel-Haenszel risk difference, Greenland-Robins variance |
| E018 | §3 | p = 7×10⁻¹² | Stratified log-rank, conservative set B (chi-square 47.1) | S06-A, S06-B, S06-D, S06-E, S06-F, S06-G | as above |
| E020 | §3 | 0.11 (95% CI 0.05–0.23) | Hazard ratio for death, PSLN-344 vs PSLN-212, Cox model stratified by experiment, set B | S06-A, S06-B, S06-D, S06-E, S06-F, S06-G | R survival::coxph with strata(block); script check_lr.R; stratified log-rank chi-square identical in R and Python |
| E495 | §3 | 60 points (95% CI 43–76) | Mantel-Haenszel difference in survival, PSLN-344 minus PSLN-212, set F, stratified by experiment | see set definition | Mantel-Haenszel risk difference, Greenland-Robins variance |
| E511 | §3 | p = 2×10⁻⁷ | Cochran-Mantel-Haenszel test, worst-case set F | S06-A,B,D,E,F,G with weight-inferred counts | CMH with continuity correction (statsmodels StratifiedTable) |
| E496 | §3 | 92/108 (85%) | All head-to-head experiments as printed (aged BALB/c x9, C57BL/6, Swiss Webster, 14-month x4), PSLN-344 | S03-I/J, S06-A..G, S15-L/N, S06-E2/F2 | Sum |
| E497 | §3 | 15/108 (14%) | Same, PSLN-212 | as above | Sum |
| E512 | §3 | 71 points (95% CI 63–80) | Mantel-Haenszel difference in survival, all 15 head-to-head strata | S03-I/J, S06-A..G, S15-L/N, S06-E2/F2 | Mantel-Haenszel risk difference, Greenland-Robins variance |
| E060 | §3 | 7/7 | S03-I survival, PSLN-344 | S03-I (S03!E38:E44) | Count |
| E021 | §3 | 39/49 (80%) | Aged BALB/c, challenge virus of a different subtype from the vaccine (as printed), PSLN-344 | S06-A, S06-B, S06-C, S06-D, S06-E, S06-F, S06-G (S06!A3:Q30; S06!A34:R68; S06!A71:F105) | Sum |
| E022 | §3 | 6/49 (12%) | Same, PSLN-212 | S06-A, S06-B, S06-C, S06-D, S06-E, S06-F, S06-G | Sum |
| E063 | §3 | 10/10 | S03-J survival, PSLN-344 | S03-J (S03!J37:J46) | Count |
| E042 | §3 | 6/7 | S15-L survival, PSLN-344 | S15-L (S15!D117:D123) | Count |
| E046 | §3 | 6/7 | S15-N survival, PSLN-344 | S15-N (S15!D148:D154) | Count |
| E043 | §3 | 0/7 | S15-L survival, PSLN-212 | S15-L (S15!C110:C116) | Count |
| E047 | §3 | 2/7 | S15-N survival, PSLN-212 | S15-N (S15!C141:C147) | Count |
| E050 | §3 | 24/28 (86%) | 14-month-old BALB/c (with or without prior PR8 infection), PSLN-344, four groups pooled | S06-E2, S06-F2 (second blocks labelled S06-E / S06-F) (S06!J85:K98; S06!P85:Q98) | Sum |
| E051 | §3 | 4/28 (14%) | Same, PSLN-212 | S06-E2, S06-F2 (S06!H71:I84; S06!N71:O84) | Sum |
| E023 | §3 | 28/31 (90%) | PSLN-344 + vaccine, aged BALB/c, challenged 2-3 days after the single dose | S03-J, S06-B, S06-D, S15-H (S03!J37:J46; S06!J17:J23; S06!D48:D54; S15!D87:D93) | Sum |
| E024 | §3 | 20/21 (95%) | PSLN-344, aged BALB/c, challenged at day 14 | S03-I, S06-A, S06-C (S03!E38:E44; S06!D17:D23; S06!P17:P23) | Sum |
| E025 | §3 | 14/21 (67%) | PSLN-344, aged BALB/c, challenged at day 60 | S06-E, S06-F, S06-G (S06!J48:J54; S06!P48:P54; S06!D85:D91) | Sum |
| E029 | §3 | p = 0.045 | Fisher exact test, PSLN-344 survival day-14 vs day-60 challenge | S03-I, S06-A, S06-C vs S06-E..G | Fisher exact, two-sided |
| E027 | §3 | 4/21 | Deaths among unvaccinated, unchallenged aged controls | S06-E/F/G Untreated | Sum |
| E490 | §3 | 78–85% | Last recorded body weight (frozen trace) of PSLN-344 animals that died after day-60 challenge, percent of day 0; n=5 animals | S15-E, S15-F, S15-G (S15!W43:AC70) | weight value carried forward to day 14 |
| E491 | §3 | 94–97% | Last recorded body weight (frozen trace) of unvaccinated, unchallenged aged controls that died; n=4 animals | S15-E, S15-G (S15!AD43:AJ70) | weight value carried forward to day 14 |
| E479 | §3 | 11–16% | Range across six mismatched-virus experiments of the group mean of maximum weight loss after challenge, PSLN-344 aged (all 7 animals per group; S15-C excluded, flag Q05) | S15-A, B, D, E, F, G (S15!W3:AC70) | per-animal minimum weight, group mean |
| E480 | §3 | 9–12% | Same, young benchmark | S15-A, B, D, E, F, G (S15!B3:H70) | as above |
| E481 | §3 | 17–19% | Same, PSLN-212 aged | S15-A, B, D, E, F, G (S15!P3:V70) | as above |
| E482 | §3 | 8.5% | Mean maximum weight loss after matched H1N1 challenge, PSLN-344 aged | S13-F (S13!W33:AC40) | as above |
| E529 | §3 | 9 of 9 | Aged BALB/c experiments in which PSLN-344 vs PSLN-212 reaches p<0.05 by permutation log-rank test (range of p 0.0006-0.021) | S03-I, S03-J, S06-A, S06-B, S06-C, S06-D, S06-E, S06-F, S06-G (S03!A17:F51; S03!G17:J46; S06!A3:Q30; S06!A34:R68; S06!A71:F105) | Log-rank statistic, exact permutation p |
| E530 | §3 | 0.021 | Largest permutation log-rank p among the nine experiments | S03-I, S03-J, S06-A, S06-B, S06-C, S06-D, S06-E, S06-F, S06-G | as above |
| E531 | §3 | 7 of 9 | Aged BALB/c experiments in which PSLN-344 vs PSLN-212 reaches p<0.05 by Fisher exact test on survivor counts | S03-I, S03-J, S06-A, S06-B, S06-C, S06-D, S06-E, S06-F, S06-G (S03!A17:F51; S03!G17:J46; S06!A3:Q30; S06!A34:R68; S06!A71:F105) | Fisher exact, two-sided |
| E455 | §3 | 21 | Read-outs in which PSLN-344 (aged) does not differ from the young benchmark at Welch p<0.05 (n=5 per group; low power) | as above | Welch |
| E328 | §3 | 76% | HAI titre to H1N1, day 14: PSLN-344 as % of young benchmark; Welch p vs young = 0.4 | S03-C | ratio |
| E335 | §3 | 87% | HAI titre to H3N2, day 14: PSLN-344 as % of young benchmark; Welch p vs young = 0.61 | S03-G | ratio |
| E323 | §3 | 368 | HAI titre to H1N1, day 14: PSLN-344, geometric mean (n=5) | S03-C (S03!N3:N7) | geometric mean |
| E330 | §3 | 320 | HAI titre to H3N2, day 14: PSLN-344, geometric mean (n=5) | S03-G (S03!N10:N14) | geometric mean |
| E324 | §3 | 46 | HAI titre to H1N1, day 14: PSLN-212, geometric mean (n=5) | S03-C (S03!M3:M7) | geometric mean |
| E331 | §3 | 35 | HAI titre to H3N2, day 14: PSLN-212, geometric mean (n=5) | S03-G (S03!M10:M14) | geometric mean |
| E251 | §3 | 29% | CD40+ lymph-node CD11b+ DC, day 3: PSLN-344 as % of young benchmark; Welch p vs young = 0.00042 | S02-D_CD40 | ratio |
| E257 | §3 | 38% | CD86+ lymph-node CD11b+ DC, day 3: PSLN-344 as % of young benchmark; Welch p vs young = 0.00017 | S02-D_CD86 | ratio |
| E356 | §3 | 35% | IgG2a to H1N1, day 14: PSLN-344 as % of young benchmark; Welch p vs young = 0.012 | S13-A | ratio |
| E362 | §3 | 48% | IgG1 to H1N1, day 14: PSLN-344 as % of young benchmark; Welch p vs young = 0.002 | S13-B | ratio |
| E411 | §3 | 66% | Lung resident-memory CD8 T cells (CD69+CD103+), day 25: PSLN-344 as % of young benchmark; Welch p vs young = 0.00068 | S05-I | ratio |
| E099 | §3 | 50.7 | Lung Ifnb1 16 h, PSLN-344 in young mice, mean | S01-A (S01!B10:F10) | mean |
| E039 | §3 | 7/7 | Young BALB/c, matched H1N1 challenge, CMP-204(Y) | S13-E (S13!U17:U23) | Count |
| E522 | §3 | 12.7% against 10.7%, p = 0.03 | Young mice, day-180 challenge: mean largest weight loss, PSLN-344 vs PSLN-212 (Welch) | S09-G (S09!G67:AD73) | per-animal minimum; Welch |
| E519 | §3 | 95.6% | Young mice challenged 180 days after dosing: body weight 14 days after challenge, PSLN-344 (n=8), % of day 0 | S09-G (S09!W73:AD73) | mean |
| E520 | §3 | 99.2% | Same, PSLN-212 (n=8) | S09-G (S09!G73:N73) | mean |
| E521 | §3 | p = 0.004 | Day-14 weight after day-180 challenge, PSLN-344 vs PSLN-212 in young mice: Welch t-test (exact Mann-Whitney p = 0.005) | S09-G | Welch; Mann-Whitney exact |
| E523 | §3 | 3.9× | Lung Il6 at 72 h (right panel of S09-A): PSLN-344 over PSLN-212, ratio of geometric means; Welch p=0.03; n=3 | S09-A (S09!AE4:AG4; S09!AN4:AP4) | 10^(difference of mean log10); Welch |
| E524 | §3 | 5.2× | Lung Ccl2 at 72 h (right panel of S09-A): PSLN-344 over PSLN-212, ratio of geometric means; Welch p=0.01; n=3 | S09-A (S09!AE5:AG5; S09!AN5:AP5) | 10^(difference of mean log10); Welch |
| E452 | §3 | 37 | Read-outs with Welch p<0.05 for PSLN-344 vs PSLN-212 | as above | Welch t-test per read-out (log10 for titres/fold values); not adjusted across read-outs |
| E513 | §3 | p = 0.009 Welch, 0.63 after Tukey | Ifnb1 16 h, young mice, PSLN-344 vs PSLN-212: p-values | S01-A | Welch on log10; one-way ANOVA + Tukey over 8 groups |
| E504 | §3 | 22.6% vs 21.4% | Lung CD11b+ DC day 4, young mice: PSLN-344 vs PSLN-212; Welch p=0.46 | S01-E (S01!V32:Z32; S01!Q32:U32) | mean; Welch |
| E501 | §3 | 44.3% vs 43.4% | Lung cDC1 72 h, young mice: PSLN-344 vs PSLN-212, means (n=5); Welch p=0.75 | S01-F (S01!V36:Z36; S01!Q36:U36) | mean; Welch |
| E502 | §3 | 11.1% vs 9.4% | Antigen-positive DC in lymph node, young mice: PSLN-344 vs PSLN-212, means (n=5); Welch p=0.14 | S02-C (S02!O3:O7; S02!M3:M7) | mean; Welch |
| E503 | §3 | 31.4% vs 26.2% | OT-I priming ex vivo, young mice: PSLN-344 vs PSLN-212, means (n=5); Welch p=0.26 | S02-E (S02!O10:O14; S02!M10:M14) | mean; Welch |
| E505 | §3 | 10.3% vs 11.1% | Young mice, mean maximum weight loss after challenge, PSLN-344 vs PSLN-212 (n=8) | S09-C | per-animal minimum, group mean |
| E506 | §3 | 9.3% vs 10.5% | Young mice, mean maximum weight loss after challenge, PSLN-344 vs PSLN-212 (n=8) | S09-E | per-animal minimum, group mean |
| E507 | §3 | 12.7% vs 10.7% | Young mice, mean maximum weight loss after challenge, PSLN-344 vs PSLN-212 (n=8) | S09-G | per-animal minimum, group mean |
| E460 | §3 | 1.8% | Mean of per-animal maximum weight loss over 10 days after immunisation, Vaccine (n=5) | S08-D (S08!AA21:AE26) | per-animal minimum of % day-0 weight, days 2-10 |
| E469 | §3 | p = 0.06 | Maximum weight loss after immunisation, PSLN-344 vs vaccine alone, Welch t-test (Tukey p = 0.86) | S08-D | Welch |
| E458 | §3 | 3.0% | Mean of per-animal maximum weight loss over 10 days after immunisation, PSLN-212 (n=5) | S08-D (S08!L21:P26) | per-animal minimum of % day-0 weight, days 2-10 |
| E466 | §3 | 99.8% | Mean weight at day 10 after immunisation, PSLN-344 (n=5) | S08-D (S08!Q26:U26) | mean |
| E462 | §3 | 10.0% | Mean of per-animal maximum weight loss over 10 days after immunisation, PSLN-212/R848 (n=5) | S08-D (S08!V21:Z26) | per-animal minimum of % day-0 weight, days 2-10 |
| E463 | §3 | 15.3% | Largest individual weight loss after immunisation, PSLN-212/R848 | S08-D (S08!V21:Z26) | max |
| E467 | §3 | 90.6% | Mean weight at day 10 after immunisation, PSLN-212/R848 (n=4) | S08-D (S08!V26:Z26) | mean |
| E140 | §3 | 36× | Lung Il6 mRNA, 16h panel of S09-A (left panel), PSLN-344: geometric-mean fold over control (95% CI 7.8-167.5; n=3) | S09-A (S09!Q4:S4) | 10^(mean log10 difference vs control); Welch CI |
| E144 | §3 | 40× | Lung Tnf mRNA, 16h panel of S09-A (left panel), PSLN-344: geometric-mean fold over control (95% CI 9.2-177.4; n=3) | S09-A (S09!Q8:S8) | 10^(mean log10 difference vs control); Welch CI |
| E148 | §3 | 590× | Lung Ccl2 mRNA, 16h panel of S09-A (left panel), PSLN-344: geometric-mean fold over control (95% CI 114.6-3037.0; n=3) | S09-A (S09!Q5:S5) | 10^(mean log10 difference vs control); Welch CI |
| E142 | §3 | 60× | Lung Il6 mRNA, 16h panel of S09-A (left panel), PSLN-212(y): geometric-mean fold over control (95% CI 14.7-248.0; n=3) | S09-A (S09!T4:V4) | 10^(mean log10 difference vs control); Welch CI |
| E146 | §3 | 14× | Lung Tnf mRNA, 16h panel of S09-A (left panel), PSLN-212(y): geometric-mean fold over control (95% CI 3.7-52.1; n=3) | S09-A (S09!T8:V8) | 10^(mean log10 difference vs control); Welch CI |
| E150 | §3 | 1,391× | Lung Ccl2 mRNA, 16h panel of S09-A (left panel), PSLN-212(y): geometric-mean fold over control (95% CI 292.7-6606.1; n=3) | S09-A (S09!T5:V5) | 10^(mean log10 difference vs control); Welch CI |
| E169 | §3 | 1.9× | Lung Il6 mRNA, 72h panel of S09-A (right panel, printed 16h, identified as 72 h, flag Q02), PSLN-212: geometric-mean fold over control (95% CI 0.7-5.3; n=3) | S09-A (S09!AE4:AG4) | 10^(mean log10 difference vs control); Welch CI |
| E173 | §3 | 5.2× | Lung Tnf mRNA, 72h panel of S09-A (right panel, printed 16h, identified as 72 h, flag Q02), PSLN-212: geometric-mean fold over control (95% CI 2.0-13.9; n=3) | S09-A (S09!AE8:AG8) | 10^(mean log10 difference vs control); Welch CI |
| E177 | §3 | 5.2× | Lung Ccl2 mRNA, 72h panel of S09-A (right panel, printed 16h, identified as 72 h, flag Q02), PSLN-212: geometric-mean fold over control (95% CI 1.7-16.2; n=3) | S09-A (S09!AE5:AG5) | 10^(mean log10 difference vs control); Welch CI |
| E193 | §3 | 18.4% | Lung monocytes day 8, PSLN-344, mean (n=5) | S01-D (S01!L28:P28) | mean |
| E197 | §3 | 9.5% | Lung monocytes day 8, Sham, mean (n=5) | S01-D (S01!B28:F28) | mean |
| E476 | §3 | 1.2× | CNS Isg15 mRNA 36 h after dosing, PSLN-344 vs buffer: ratio of geometric means (95% CI 0.79-1.72); Tukey p=0.77; Welch p=0.39 | S10-A (S10!K3:K7; S10!M3:M7) | Welch on log10; ANOVA + Tukey |
| E473 | §3 | 1.6× | CNS Tnf mRNA 36 h after dosing, PSLN-344 vs buffer: ratio of geometric means (95% CI 1.05-2.34); Tukey p=0.12; Welch p=0.03 | S10-A (S10!F3:F7; S10!H3:H7) | Welch on log10; ANOVA + Tukey |
| E474 | §3 | 1.0–2.3 | 95% CI of the above | S10-A | Welch |
| E478 | §3 | 2.7× | CNS Isg15, cholera toxin vs buffer: ratio of geometric means | S10-A (S10!N3:N7) | as above |
| E475 | §3 | 3.4× | CNS Tnf, cholera toxin vs buffer: ratio of geometric means | S10-A (S10!I3:I7) | as above |
| E448 | §3 | 0.58 | IgG2a/IgG1 quotient as printed under the header "PSLN-344" in S03-B (header rotated, flag Q01) | S03-B (S03!H3:H7) | mean |
| E440 | §3 | 2.14 | IgG2a/IgG1 quotient to H1N1, PSLN-344, mean of per-animal quotients recomputed from subclass titres (not from the mislabelled quotient block; flag Q01) | S13-A, S13-B (S13!B3:B7 / S13!F3:F7) | per-animal quotient, mean |
| E441 | §3 | 0.58 | IgG2a/IgG1 quotient to H1N1, PSLN-212, mean of per-animal quotients recomputed from subclass titres (not from the mislabelled quotient block; flag Q01) | S13-A, S13-B (S13!A3:A7 / S13!E3:E7) | per-animal quotient, mean |
| E442 | §3 | 2.97 | IgG2a/IgG1 quotient to H1N1, PSLN-212(Y), mean of per-animal quotients recomputed from subclass titres (not from the mislabelled quotient block; flag Q01) | S13-A, S13-B (S13!C3:C7 / S13!G3:G7) | per-animal quotient, mean |
| E075 | §3 | 7/7 | S06-D survival, PSLN-344 | S06-D (S06!D48:D54) | Count |
| E499 | §3 | 5/7 | PSLN-344 aged animals alive at day 14 according to the weight traces of the day-3 rgH5N1 challenge (survival block says 7/7; flag Q10) | S15-D (S15!W33:AC40) | traces not frozen at day 14 |
| E061 | §3 | 0/7 | S03-I survival, PSLN-212 | S03-I (S03!D31:D37) | Count |
| E498 | §3 | 3/7 | PSLN-212 aged animals alive at day 14 according to the weight traces of the matched-H1N1 challenge (flag Q10/Q11) | S13-F (S13!P33:V40) | traces not frozen/blank at day 14 |
| E069 | §3 | 5/7 | S06-B survival, PSLN-344 | S06-B (S06!J17:J23) | Count |
| E486 | §3 | p = 0.29 | Encapsulation efficiency, PSLN-344 vs PSLN-212, Welch t-test | S08-B | Welch |
| E212 | §4 | 15.8% | Dye-positive type II alveolar epithelial cells: AECII/PSLN-SRB, mean (n=5); Welch p=0.00011 | S01-B (S01!B14:F14) | mean; Welch t-test |
| E214 | §4 | 3.8% | Dye-positive type I alveolar epithelial cells: AECI/PSLN-SRB, mean (n=5); Welch p=0.002 | S01-B (S01!B15:F15) | mean; Welch t-test |
| E211 | §4 | 0.4% | Dye-positive type II alveolar epithelial cells: AECII/FreeSRB, mean (n=5) | S01-B (S01!B16:F16) | mean |
| E213 | §4 | 0.3% | Dye-positive type I alveolar epithelial cells: AECI/FreeSRB, mean (n=5) | S01-B (S01!B17:F17) | mean |
| E209 | §4 | 43.1% | Dye-positive alveolar macrophages 16 h after DiD-liposome: WT, mean (n=4) | S01-C (S01!B20:E20) | mean |
| E210 | §4 | 12.7% | Dye-positive alveolar macrophages 16 h after DiD-liposome: SPA/D, mean (n=4); Welch p=3.9e-05 | S01-C (S01!B21:E21) | mean; Welch t-test |
| E215 | §4 | 7.3% | Recruited lung monocytes day 3, PSLN-344, without / with carbenoxolone: CBX-, mean (n=5) | S11-C (S11!B17:B21) | mean |
| E216 | §4 | 3.1% | Recruited lung monocytes day 3, PSLN-344, without / with carbenoxolone: CBX+, mean (n=5); Welch p=0.0041 | S11-C (S11!A17:A21) | mean; Welch t-test |
| E093 | §4 | 2.2× | Lung Ifnb1 mRNA 16 h after dosing, fold over untreated: ratio PSLN-344/PSLN-212 (ratio of geometric means); Welch p=9.6e-06; Tukey p=0.00062 | S01-A_16h (S01!B5:F5; S01!B8:F8) | Welch t-test (log10 scale for titres/fold values); one-way ANOVA + Tukey across all groups of the block |
| E094 | §4 | 1.8–2.7 | Lung Ifnb1 mRNA 16 h after dosing, fold over untreated: 95% CI of the ratio | S01-A_16h | Welch interval on log10 scale |
| E098 | §4 | 7.8 | Lung Ifnb1 16 h, CMP-204 (cGAMP liposome), aged, mean | S01-A (S01!B4:F4) | mean |
| E126 | §4 | 6.0 | Lung Gm-csf mRNA fold, 16h, PSLN-344, mean (n=5) | S02-F (S02!B17:F17) | mean |
| E132 | §4 | 3.9 | Lung Gm-csf mRNA fold, 72h, PSLN-344, mean (n=5) | S02-F (S02!B19:F19) | mean |
| E127 | §4 | 1.5 | Lung Gm-csf mRNA fold, 16h, PSLN-212, mean (n=5) | S02-F (S02!G17:K17) | mean |
| E133 | §4 | 1.4 | Lung Gm-csf mRNA fold, 72h, PSLN-212, mean (n=5) | S02-F (S02!G19:K19) | mean |
| E149 | §4 | 7.6× | Lung Ccl2 mRNA, 16h panel of S09-A (left panel), PSLN-212: geometric-mean fold over control (95% CI 1.9-31.4; n=3) | S09-A (S09!H5:J5) | 10^(mean log10 difference vs control); Welch CI |
| E217 | §4 | 5.9% | Lung Ly6C+CD11c+MHC-II+ cells day 5: PSLN-212, mean (n=5) | S02-G (S02!C22:C26) | mean |
| E218 | §4 | 13.8% | Lung Ly6C+CD11c+MHC-II+ cells day 5: PSLN-212+GM-CSF, mean (n=5); Welch p=0.0021 | S02-G (S02!D22:D26) | mean; Welch t-test |
| E220 | §4 | 19.7% | Donor-derived monocyte-derived DC day 3, PSLN-344: wild-type vs Ifnar-knockout marrow (pre-cDC removed): WT w/o cDC, mean (n=5) | S02-H (S02!B30:B34) | mean |
| E221 | §4 | 2.1% | Donor-derived monocyte-derived DC day 3, PSLN-344: wild-type vs Ifnar-knockout marrow (pre-cDC removed): IFN w/o cDC, mean (n=5); Welch p=0.0004 | S02-H (S02!D30:D34) | mean; Welch t-test |
| E222 | §4 | 12.4% | Same, Ifnar-knockout marrow + GM-CSF intratracheally | S02-H (S02!F30:F34) | mean |
| E192 | §4 | 30.6% | Lung monocytes day 4, PSLN-344, mean (n=5) | S01-D (S01!L26:P26) | mean |
| E194 | §4 | 16.7% | Lung monocytes day 4, PSLN-212, mean (n=5) | S01-D (S01!G26:K26) | mean |
| E198 | §4 | 32.2% | Lung monocytes day 4, PSLN-212(Y), mean (n=5) | S01-D (S01!Q26:U26) | mean |
| E200 | §4 | 18.9% | Lung CD11b+ dendritic cells day 4, PSLN-344, mean (n=5) | S01-E (S01!L32:P32) | mean |
| E201 | §4 | 8.3% | Lung CD11b+ dendritic cells day 4, PSLN-212, mean (n=5) | S01-E (S01!G32:K32) | mean |
| E203 | §4 | 21.4% | Lung CD11b+ dendritic cells day 4, PSLN-212(Y), mean (n=5) | S01-E (S01!Q32:U32) | mean |
| E205 | §4 | 3.4 | Lung Ly6C+CCR2+ macrophages, day 5, PSLN-344, x10^5 cells, mean (n=3) | S07-A (S07!E5:G5) | mean |
| E207 | §4 | 19.0 | Lung Ly6C+CCR2+ macrophages, day 5, PSLN-212, x10^5 cells, mean (n=3) | S07-A (S07!B5:D5) | mean |
| E303 | §4 | 49% | CD206+ lung macrophages: PSLN-344, mean (n=5) | S11-E (S11!C31:C35) | mean |
| E304 | §4 | 71% | CD206+ lung macrophages: PSLN-212, mean (n=5) | S11-E (S11!B31:B35) | mean |
| E306 | §4 | 36% | CD206+ lung macrophages: young benchmark (PSLN-212(Y)), mean | S11-E (S11!D31:D35) | mean |
| E223 | §4 | 9.9% | Lung CD11b+Ly6C+ monocytes, PSLN-344 without / with CCR2 antagonist: PSLN-344, mean (n=5) | S07-B_mono (S07!B10:B14) | mean |
| E224 | §4 | 3.3% | Lung CD11b+Ly6C+ monocytes, PSLN-344 without / with CCR2 antagonist: PSLN-344+INCB3344, mean (n=5); Welch p=0.001 | S07-B_mono (S07!C10:C14) | mean; Welch t-test |
| E227 | §4 | 6.8% | Lung granzyme B+ CD8 T cells day 5, young mice, PSLN-344 without / with CCR2 antagonist: PSLN-344(Y), mean (n=5) | S02-I (S02!H30:H34) | mean |
| E228 | §4 | 1.4% | Lung granzyme B+ CD8 T cells day 5, young mice, PSLN-344 without / with CCR2 antagonist: PSLN-344(Y)+INCB3344, mean (n=5); Welch p=8.1e-05 | S02-I (S02!I30:I34) | mean; Welch t-test |
| E236 | §4 | 30.7% | CCR7+ migratory CD11b+ DC in lung, 72 h: PSLN-344, mean (n=5) | S02-A (S02!C3:C7) | mean |
| E237 | §4 | 7.3% | CCR7+ migratory CD11b+ DC in lung, 72 h: PSLN-212, mean (n=5) | S02-A (S02!B3:B7) | mean |
| E239 | §4 | 35.0% | CCR7+ migratory CD11b+ DC in lung, 72 h: young benchmark (PSLN-212(Y)), mean | S02-A (S02!D3:D7) | mean |
| E242 | §4 | 7.1% | Antigen (OVA-AF647)-positive DC in lymph node, 36 h: PSLN-344, mean (n=5) | S02-C (S02!L3:L7) | mean |
| E243 | §4 | 1.8% | Antigen (OVA-AF647)-positive DC in lymph node, 36 h: PSLN-212, mean (n=5) | S02-C (S02!K3:K7) | mean |
| E245 | §4 | 9.4% | Antigen (OVA-AF647)-positive DC in lymph node, 36 h: young benchmark (PSLN-212(Y)), mean | S02-C (S02!M3:M7) | mean |
| E259 | §4 | 18.7% | OT-I CD8 proliferation driven by lymph-node DC ex vivo: PSLN-344, mean (n=5) | S02-E (S02!L10:L14) | mean |
| E260 | §4 | 0.8% | OT-I CD8 proliferation driven by lymph-node DC ex vivo: PSLN-212, mean (n=5) | S02-E (S02!K10:K14) | mean |
| E262 | §4 | 26.2% | OT-I CD8 proliferation driven by lymph-node DC ex vivo: young benchmark (PSLN-212(Y)), mean | S02-E (S02!M10:M14) | mean |
| E247 | §4 | 11.2% | CD40+ lymph-node CD11b+ DC, day 3: PSLN-344, mean (n=5) | S02-D_CD40 (S02!C10:C14) | mean |
| E248 | §4 | 5.6% | CD40+ lymph-node CD11b+ DC, day 3: PSLN-212, mean (n=5) | S02-D_CD40 (S02!B10:B14) | mean |
| E250 | §4 | 38.7% | CD40+ lymph-node CD11b+ DC, day 3: young benchmark (PSLN-212(Y)), mean | S02-D_CD40 (S02!D10:D14) | mean |
| E235 | §4 | 2.4% | Antigen-positive DC in lymph node, pertussis-toxin group | S02-C (S02!N3:N7) | mean |
| E233 | §4 | 30.9% | Proliferating OT-I CD8 T cells in lymph node day 4, without / with pertussis toxin: MLN, mean (n=3) | S05-C (S05!C13:C15) | mean |
| E234 | §4 | 6.8% | Proliferating OT-I CD8 T cells in lymph node day 4, without / with pertussis toxin: MLN+PTX, mean (n=3); Welch p=0.0066 | S05-C (S05!D13:D15) | mean; Welch t-test |
| E231 | §4 | 59.0% | Proliferating OT-I CD8 T cells in lung day 4, without / with pertussis toxin: Lung, mean (n=3) | S05-C (S05!A13:A15) | mean |
| E232 | §4 | 55.1% | Proliferating OT-I CD8 T cells in lung day 4, without / with pertussis toxin: Lung+PTX, mean (n=3); Welch p=0.57 | S05-C (S05!B13:B15) | mean; Welch t-test |
| E264 | §4 | 6.5% | Germinal-centre B cells in lymph node, day 7: PSLN-344, mean (n=5) | S03-K (S03!N17:N21) | mean |
| E265 | §4 | 2.3% | Germinal-centre B cells in lymph node, day 7: PSLN-212, mean (n=5) | S03-K (S03!M17:M21) | mean |
| E267 | §4 | 9.8% | Germinal-centre B cells in lymph node, day 7: young benchmark (PSLN-212(Y)), mean | S03-K (S03!O17:O21) | mean |
| E289 | §4 | 8.5 | Tfh:Tfr ratio day 7, PSLN-344, arithmetic mean | S04-B Tfh:Tfr (S04!C15:C19) | mean |
| E290 | §4 | 2.9 | Tfh:Tfr ratio day 7, PSLN-212, arithmetic mean | S04-B Tfh:Tfr (S04!B15:B19) | mean |
| E291 | §4 | 14.0% | Follicular regulatory T cells, day 30: PSLN-344, mean (n=5) | S04-C (S04!C22:C26) | mean |
| E292 | §4 | 18.0% | Follicular regulatory T cells, day 30: PSLN-212, mean (n=5) | S04-C (S04!B22:B26) | mean |
| E327 | §4 | 485 | HAI titre to H1N1, day 14: young benchmark (PSLN-212(Y)), geometric mean | S03-C (S03!O3:O7) | geometric mean |
| E337 | §4 | 3,840 | Neutralising titre to H1N1, day 14: PSLN-344, geometric mean (n=5) | S03-D (S03!T3:T7) | geometric mean |
| E338 | §4 | 418 | Neutralising titre to H1N1, day 14: PSLN-212, geometric mean (n=5) | S03-D (S03!S3:S7) | geometric mean |
| E341 | §4 | 6,686 | Neutralising titre to H1N1, day 14: young benchmark (PSLN-212(Y)), geometric mean | S03-D (S03!U3:U7) | geometric mean |
| E389 | §4 | 6.4% | IFN-gamma+ CD8 T cells after restimulation with rgH5N1 antigen, day 14: PSLN-344, mean (n=5) | S05-F (S05!C33:C37) | mean |
| E390 | §4 | 1.5% | IFN-gamma+ CD8 T cells after restimulation with rgH5N1 antigen, day 14: PSLN-212, mean (n=5) | S05-F (S05!B33:B37) | mean |
| E395 | §4 | 9.9% | IFN-gamma+ CD8 T cells after restimulation with rgH5N1 antigen, day 60: PSLN-344, mean (n=5) | S05-G (S05!C40:C44) | mean |
| E396 | §4 | 3.0% | IFN-gamma+ CD8 T cells after restimulation with rgH5N1 antigen, day 60: PSLN-212, mean (n=5) | S05-G (S05!B40:B44) | mean |
| E407 | §4 | 4.0% | Lung resident-memory CD8 T cells (CD69+CD103+), day 25: PSLN-344, mean (n=5) | S05-I (S05!C54:C58) | mean |
| E408 | §4 | 1.0% | Lung resident-memory CD8 T cells (CD69+CD103+), day 25: PSLN-212, mean (n=5) | S05-I (S05!B54:B58) | mean |
| E410 | §4 | 6.0% | Lung resident-memory CD8 T cells (CD69+CD103+), day 25: young benchmark (PSLN-212(Y)), mean | S05-I (S05!D54:D58) | mean |
| E105 | §4 | 4.4 | Lung Ifnb1 mRNA 72 h after dosing, fold: PSLN-344, mean (n=5) | S01-A_72h (S01!H8:L8) | mean |
| E131 | §4 | 1.2 | Lung Gm-csf mRNA fold, 36h, Sham, mean (n=5) | S02-F (S02!L18:P18) | mean |
| E270 | §4 | 10.3% | ICOS-high follicular helper T cells, day 7: PSLN-344, mean (n=5) | S04-A_ICOShi (S04!G4:K4) | mean |
| E271 | §4 | 3.8% | ICOS-high follicular helper T cells, day 7: PSLN-212, mean (n=5) | S04-A_ICOShi (S04!G3:K3) | mean |
| E273 | §4 | 13.6% | ICOS-high follicular helper T cells, day 7: young benchmark (PSLN-212(Y)), mean | S04-A_ICOShi (S04!G5:K5) | mean |
| E334 | §4 | 368 | HAI titre to H3N2, day 14: young benchmark (PSLN-212(Y)), geometric mean | S03-G (S03!O10:O14) | geometric mean |
| E431 | §4 | 5/5 | Animals with HAI titre ≥  40, PSLN-212 | S03-C (S03!M3:M7) | Count |
| E444 | §4 | 2.73 | IgG2a/IgG1 quotient to H3N2, PSLN-344, mean of per-animal quotients recomputed from subclass titres (not from the mislabelled quotient block; flag Q01) | S13-C, S13-D (S13!J3:J7 / S13!N3:N7) | per-animal quotient, mean |
| E445 | §4 | 0.51 | IgG2a/IgG1 quotient to H3N2, PSLN-212, mean of per-animal quotients recomputed from subclass titres (not from the mislabelled quotient block; flag Q01) | S13-C, S13-D (S13!I3:I7 / S13!M3:M7) | per-animal quotient, mean |
| E446 | §4 | 2.89 | IgG2a/IgG1 quotient to H3N2, PSLN-212(Y), mean of per-animal quotients recomputed from subclass titres (not from the mislabelled quotient block; flag Q01) | S13-C, S13-D (S13!K3:K7 / S13!O3:O7) | per-animal quotient, mean |
| E392 | §4 | 9.2% | IFN-gamma+ CD8 T cells after restimulation with rgH5N1 antigen, day 14: young benchmark (PSLN-212(Y)), mean | S05-F (S05!D33:D37) | mean |
| E325 | §6 | 8.0× | HAI titre to H1N1, day 14: ratio PSLN-344/PSLN-212 (ratio of geometric means); Welch p=0.00037; Tukey p=5.7e-06 | S03-C (S03!M3:M7; S03!N3:N7) | Welch t-test (log10 scale for titres/fold values); one-way ANOVA + Tukey across all groups of the block |
| E326 | §6 | 3.9–16.4 | HAI titre to H1N1, day 14: 95% CI of the ratio | S03-C | Welch interval on log10 scale |
| E332 | §6 | 9.2× | HAI titre to H3N2, day 14: ratio PSLN-344/PSLN-212 (ratio of geometric means); Welch p=0.00021; Tukey p=2.2e-06 | S03-G (S03!M10:M14; S03!N10:N14) | Welch t-test (log10 scale for titres/fold values); one-way ANOVA + Tukey across all groups of the block |
| E333 | §6 | 4.2–20.2 | HAI titre to H3N2, day 14: 95% CI of the ratio | S03-G | Welch interval on log10 scale |
| E119 | §6 | 21.1 | Ifnb1 fold at 10 µg, PSLN-344, mean of 3 | S08-A (S08!H5:J5) | mean |
| E124 | §6 | 14.9 | Ifnb1 fold at 40 µg, PSLN-212, mean of 3 | S08-A (S08!E7:G7) | mean |
| E055 | §6 | 0/7 | S06-F2 Imprinting+PSLN-212 | S06-F2 (S06!O78:O84) | Count |
| E059 | §6 | 0/7 | S06-F2 Naïve+PSLN-212 | S06-F2 (S06!N71:N77) | Count |
| E101 | §7 | 24.3 | Lung Ifnb1 16 h, PSLN-212/R848, aged | S01-A (S01!B7:F7) | mean |
| E125 | §7 | 29.4 | Ifnb1 fold at 20 µg, PSLN-344/R848 | S08-A (S08!K6:M6) | mean |
| E121 | §7 | 45.8 | Ifnb1 fold at 20 µg, PSLN-344, mean of 3 | S08-A (S08!H6:J6) | mean |
| E087 | §7 | 3/7 | S03-I survival, CMP-204 (cGAMP liposome), aged | S03-I (S03!C24:C30) | Count |
| E364 | §7 | 4,411 | IgG to H1N1, day 28 after boost at day 14: PSLN-212, geometric mean (n=5) | S13-I (S13!H53:H57) | geometric mean |
| E371 | §7 | 1,086 | IgG to H3N2, day 28 after boost at day 14: PSLN-212, geometric mean (n=5) | S13-J (S13!N53:N57) | geometric mean |
| E309 | §7 | 7,305 | Serum IgG to H1N1, day 14, reciprocal titre: PSLN-344, geometric mean (n=5) | S03-A (S03!D3:D7) | geometric mean |
| E316 | §7 | 5,701 | Serum IgG to H3N2, day 14, reciprocal titre: PSLN-344, geometric mean (n=5) | S03-E (S03!D10:D14) | geometric mean |
| E510 | §7 | 10.4% vs 5.1% | Lung Treg after transfer of two macrophage subsets whose column labels are identical (flag Q13) | S07-C (S07!B16:C20) | mean |
| E526 | App. | 6,107 | Numeric cells parsed as data values | all sheets | blocks.py |
| E527 | App. | 686 | Numeric cells that are axis values (days, hours, doses) | all sheets | blocks.py |
| E528 | App. | 26 | Numeric cells in the unlabelled region of sheet S08 (rows 89-101) | S08 (S08!A89:D101) | blocks.py |


## Appendix C. Methods

- **Data handling.** All 15 sheets were read cell by cell using explicit block coordinates (blocks.py). Of 6,819 numeric cells, 6,107 are data values, 686 are axis values (days, hours, doses) and 26 belong to an unlabelled region (Q15). No value was altered. Block names are the workbook's; the second blocks labelled S06-E and S06-F are called S06-E2 and S06-F2, and the two S09-A panels "left" and "right".
- **Statistics for single-time-point blocks.** As stated in the annotation: one-way ANOVA with Tukey's test across all groups of the block. In addition, for each contrast: Welch's t-test with a 95% interval, and the exact Mann–Whitney test (with five animals per group its smallest possible two-sided p is 0.008). Titres and fold-change transcripts were analysed on the log10 scale and summarised as geometric means; HAI values of 0 are below the lowest dilution tested (1:10) and were set to 5; S09-A is stored as log10.
- **Time courses.** Two-way ANOVA (group × time) with Tukey's test; Welch tests at each time point.
- **Survival.** Status 1 = death, 0 = alive at the end of observation. Proportions with exact (Clopper–Pearson) intervals; log-rank tests per experiment (reproduced exactly by R survival::survdiff), with permutation p-values and Fisher tests in the workbook. Pooled analyses are stratified by experiment: stratified log-rank, Cox model with strata, Mantel–Haenszel survival difference with Greenland–Robins variance, Cochran–Mantel–Haenszel test.
- **Weight traces.** An animal is counted as dead when its series ends before day 14, or when its value is frozen through day 14 (identical at the last three time points, or at the last two if below 90% of starting weight); the annotation describes such groups as "declining". Used only for cross-checks and the worst-case analysis.
- **Dose-response.** Three-parameter Hill model, fold = 1 + Emax·Dʰ/(ED50ʰ + Dʰ), least squares on individual values.
- **Comparison with the young benchmark.** Group mean (geometric for titres) of the aged group divided by that of young mice given PSLN-212 in the same block.
- **Power.** Exact power of the two-sided Fisher test at 5% by enumeration of binomial outcomes.
- **Multiplicity.** p-values are not adjusted across blocks. The argument rests on effect sizes, intervals and consistency across independent blocks.
- **Limits.** I had the workbook and its annotation only: no instrument files, animal identifiers or protocols. I cannot verify randomisation, blinding or whether experiments were repeated. No external data source was consulted; the statements marked external are from general knowledge and are not needed for any number.
- **Software.** Python 3.11 (pandas, scipy, statsmodels, matplotlib, reportlab) and R (survival). Scripts are in the analysis folder and regenerate every table, figure and number.
