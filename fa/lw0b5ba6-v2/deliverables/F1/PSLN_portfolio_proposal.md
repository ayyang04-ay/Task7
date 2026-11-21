# PSLN program: portfolio recommendation and proposal for next steps

*Independent assessment and proposal, prepared for the project lead ahead of the portfolio review. 1 November 2026.*

**Data reviewed.** `psln_program_dataset.xlsx` (15 sheets, 6,819 numeric cells, last saved 3 September 2026) and `psln_program_annotation.pdf` (dated 15 September 2026). Every numeric cell was mapped to a labelled block except 26 cells in an unlabelled region (sheet S08, rows 89–101), which are excluded.

**How to check a number.** Square brackets give the workbook block, for example [S06-A]. Every number quoted here is listed in the evidence ledger (`tables/T0_evidence_ledger.csv`) with its cell range, the statistical method and the script that produced it. The text is generated from that ledger, so the two cannot disagree.

**Terms.** *Aged* = 20 months or older. *Young* = 7–8 weeks. *Sham* = vaccine plus empty liposome. *Core experiments* = S06-A, S06-B and S06-C: the aged-mouse challenge experiments that remain after setting aside the two whose group labels are disputed (S03-I, S03-J) and one of a duplicated pair (S06-D); see section 10. All dosing is one intranasal dose of 20 µg adjuvant with inactivated influenza vaccine unless stated.

---

## 1. Recommendation

**Keep the program, narrow it to PSLN-344, and fund it to the next decision gate only.**

| Question | Answer |
|----------------------|------------------------------------------------------------------------------|
| Keep or drop? | **Keep, conditionally.** |
| Which asset goes forward? | **PSLN-344** (CDN-1807 with Mn²⁺). PSLN-212 stops as a lead and continues only as the Mn-free reference arm. |
| As what? | An intranasal adjuvant for inactivated influenza vaccine in **adults aged 65 and over**. On our data it is not a stand-alone drug. |
| How far? | To Gate 1 (about July 2027): reconcile the data, repeat the key experiment blinded with the controls that are missing, and run a first safety and biodistribution study. No IND-enabling spend before Gate 2 (about March 2028). |
| What must happen first? | Reconcile the workbook with the raw records. It contains 15 inconsistencies, 6 of them serious (section 10). The case below holds without the affected blocks, but the committee will find them. |

### Why keep it

1. **It is the only preparation in our data that protects most aged animals.** In the three core experiments, one dose of vaccine with PSLN-344 left 18/21 aged mice alive after lethal challenge (86%; 95% CI 64–97%), against 3/21 with PSLN-212 and 0/21 with vaccine alone [S06-A, S06-B, S06-C]. The difference from PSLN-212 is 71 percentage points (95% CI 51 to 91; stratified log-rank p = 5.6×10⁻⁷). Taking all six experiments as printed, it is 42/45 against 8/45 and 1/45 [adding S03-I, S03-J, S06-D].
2. **The advantage exists only in the aged host, which is where the need is.** In young mice both assets protected every animal (24/24 and 24/24) [S09-B, S09-D, S09-F]. In aged mice PSLN-344 brought 34 immune read-outs to a median of 70% of the young-adult level, where PSLN-212 reached 19% (Figure 3).
3. **Protection is fast and crosses subtypes.** 21/24 aged mice survived when challenged 2–3 days after the dose, including 10/10 against wild-type H5N1 [S03-J, S06-B, S15-H]. An H3N2 vaccine protected against H1N1, and a seasonal H1N1 + H3N2 vaccine against H5N1 [S06-A, S06-B, S06-C].
4. **The mechanism is coherent and gives us things to measure.** Mn²⁺ restores the blunted interferon response of the aged lung, adds a GM-CSF signal that PSLN-212 lacks, and steers recruited monocytes into dendritic cells (section 5).

### Why only conditionally

1. **The evidence file is not yet ready for committee scrutiny.** Two survival blocks are identical to each other; two others disagree with their own body-weight records about which group is which; two derived tables have their column headers rotated; the neutrophil table shares values with the macrophage table (section 10).
2. **There is no safety package.** What exists is reassuring but thin: weight loss of at most 5.8% with recovery by day 10 (n = 5) and no inflammatory signal in the brain at 36 hours (n = 5, three transcripts) [S08-D, S10-A]. There is no histopathology, no repeat-dose study, and the amount of Mn²⁺ in a dose is not reported anywhere. Intranasal manganese reaching the brain is the obvious question a regulator will ask.
3. **We have not shown what the active ingredient is.** Both assets carry the same agonist; the whole difference is Mn²⁺. There is no Mn²⁺-only control and no Mn²⁺ + cGAMP control, and CDN-1807 has not been shown to protect better than the natural ligand cGAMP. PSLN-344 given without vaccine protected no animal (0/7) [S15-H], so the product is an adjuvant and needs an antigen.
4. **Nothing has been compared with what older adults already receive.** The only comparators are vaccine alone and a cGAMP liposome. All BALB/c data are from female mice (sex is not stated for the other strains), with whole inactivated virus as antigen, delivered to the lower airway.
5. **Protection in aged animals is lower at two months.** Survival was 14/21 (67%) when challenge came 60 days after the dose, against 21/21 in young animals [S06-E, S06-F, S06-G].

### What would change this recommendation

I would recommend dropping the program if any of the following is found: the survival and antibody differences do not reproduce from raw records or in the blinded repeat; an Mn²⁺-only liposome does as well as PSLN-344 and we have no position on it; manganese persists in the olfactory bulb or brain, or lung pathology does not resolve; a licensed-type high-dose or adjuvanted vaccine matches PSLN-344 on every endpoint in the same study. Section 8 turns these into gate criteria.

---

## 2. What the asset is, on our data

- **Composition.** Both assets are pulmonary-surfactant-mimetic liposomes (DPPC, DPPG, DPPE-PEG2000, cholesterol) carrying the cyclic-dinucleotide STING agonist CDN-1807. PSLN-344 also contains Mn²⁺ incorporated by coordination polymerisation; PSLN-212 does not (annotation, page 1). Encapsulation efficiency is similar: 54.8% and 59.6% (p = 0.86) [S08-B].
- **Use tested.** Only one: mixed with inactivated influenza vaccine and given once into the airway. Every efficacy block is of this kind.
- **Not a stand-alone agent.** Three days before an H5N1 challenge, vaccine alone protected 0/7, PSLN-344 alone 0/7, the two together 6/7 (exact log-rank p = 0.0006 for the combination against PSLN-344 alone) [S15-H].
- **A wording point for the committee.** The program is described as a "small-molecule STING agonist". CDN-1807 is a cyclic dinucleotide formulated in a liposome, and on our data its value is as a vaccine adjuvant. I would present it that way, because "small-molecule STING agonist" will lead some members to expect a stand-alone drug with oral or systemic exposure, which nothing here supports.
- **Route.** "Intranasal" in a mouse delivers to the alveoli. The mechanism data are alveolar (alveolar macrophages, alveolar epithelium, surfactant proteins) [S01-B, S01-C]. A human nasal spray does not reach the alveoli. Whether the product is a nasal spray or an inhaled aerosol is open and changes the device, the safety questions and the market (Study 6).

---

## 3. How the asset looks

### 3.1 Protection from lethal challenge

Survivors / animals at the end of observation. Bold totals are the figures used in section 1.

| Experiment | Vaccine → challenge virus; days from dose to challenge | Vaccine alone (sham) | PSLN-212, aged | PSLN-344, aged | PSLN-212, young | Notes |
|-------------|-------------------------|----------|-------------|-------------|---------|-----------------|
| S06-A | H3N2 → H1N1 (PR8); 14 d | 0/7 | 1/7 | **6/7** | 7/7 |  |
| S06-B | H3N2 → H1N1 (PR8); 3 d | 0/7 | 0/7 | **5/7** | 7/7 |  |
| S06-C | H1N1 + H3N2 → H5N1 (reverse-genetics); 14 d | 0/7 | 2/7 | **7/7** | 7/7 | One of an identical pair with S06-D (Q4); counted once |
| **Core experiments, total** | | **0/21** | **3/21** | **18/21** | **21/21** | |
| S03-I | H1N1 + H3N2 → H1N1 (CA09, matched strain); 14 d | 0/7 | 0/7 | **7/7** | 7/7 | Labels disputed (Q2); CMP-204 3/7 |
| S03-J | H5N1 → wild-type H5N1; 2 d | 1/10 | 3/10 | **10/10** | not tested | Labels disputed (Q3) |
| S06-D | H1N1 + H3N2 → H5N1; 3 d | 0/7 | 2/7 | **7/7** | 7/7 | Identical to S06-C (Q4) |
| **All six as printed, total** | | **1/45** | **8/45** | **42/45** | **35/35** | |
| S15-H | H1N1 + H3N2 → H5N1; 3 d | 0/7 (no liposome) | not tested | **6/7** | not tested | PSLN-344 without vaccine: 0/7 |
| S06-E | H3N2 → H1N1 (PR8); 60 d | 0/7 | 0/7 | **5/7** | 7/7 | Untreated, unchallenged: 6/7 |
| S06-F | H1N1 + H3N2 → H5N1; 60 d | 0/7 | 1/7 | **5/7** | 7/7 | Untreated, unchallenged: 7/7 |
| S06-G | H1N1 → H3N2 (Perth); 60 d | 0/7 | 0/7 | **4/7** | 7/7 | Untreated, unchallenged: 4/7 |
| **Day 60, total** | | **0/21** | **1/21** | **14/21** | **21/21** | Untreated, unchallenged: 17/21 |
| S15-L | C57BL/6, 20 months; challenge not stated | 0/7 | 0/7 | **6/7** | 6/7 | Q5, Q15 |
| S15-N | Swiss Webster, 20 months; challenge not stated | 0/7 | 2/7 | **6/7** | 7/7 | Q5, Q15 |
| S06-E, rows 71–105 | 14-month BALB/c; H1N1 + H3N2 → H1N1 (PR8) | not tested | 0/7 (4/7 if previously infected) | **6/7** (6/7 if previously infected) | not tested | Label used twice (Q13) |
| S06-F, rows 71–105 | 14-month BALB/c; H1N1 + H3N2 → H3N2 (Perth); 14 d | not tested | 0/7 (0/7 if previously infected) | **6/7** (6/7 if previously infected) | not tested | Label used twice (Q13) |

What the table supports (Figure 1 shows every curve; Figure 2 pools them):

- **PSLN-344 in aged animals:** 18/21 (core experiments) to 42/45 (all six as printed) when challenge came 2–14 days after the dose. Vaccine alone: 0/21 to 1/45.
- **PSLN-212 in aged animals:** 3/21 to 8/45. It delays death in some experiments but rarely prevents it.
- **Other ages and strains:** 12/14 against 2/14 in aged C57BL/6 and Swiss Webster mice [S15-L, S15-N]; 12/14 against 0/14 in 14-month BALB/c, and 12/14 in 14-month mice that had earlier recovered from influenza [S06-E and S06-F at rows 71–105]. The second- and third-strain body-weight records share values with the BALB/c experiment (flag Q5), so treat "three strains" as provisional.
- **All three core experiments are cross-subtype challenges.** The matched-strain experiment [S03-I] is flagged because its comparator labels conflict with its body-weight block, but both blocks agree that all 7 PSLN-344 animals and all 7 young PSLN-212 animals survived.

![Figure 1. Time-to-event data for all lethal-challenge experiments in aged or 14-month animals.](figures/Fig1_survival_KM_grid.png){width=100%}

![Figure 2. Pooled survival with exact 95% confidence intervals.](figures/Fig2_survival_pooled.png){width=100%}

### 3.2 Immune response

Group means (geometric mean titres, GMT, for antibody; HAI = haemagglutination inhibition). p: Tukey test within the block, on log2 titres for antibody. n = 5 per group.

| Read-out [block] | Vaccine alone | PSLN-212, aged | PSLN-344, aged | PSLN-212, young | PSLN-344 ÷ PSLN-212 | p |
|------------------------------------|---------|----------|----------|----------|------------|-------------|
| Lung Ifnb1 mRNA at 16 h (fold) [S01-A 16h] | 1.0 | 16.6 | **37.1** | 37.6 | 2.2 | 3.7×10⁻⁸ |
| Lung Gm-csf mRNA at 36 h (fold) [S02-F] | 1.2 | 1.6 | **8.7** | — | 5.5 | 3.0×10⁻⁶ |
| Lung monocytes, day 4 (%) [S01-D] | 10.4 | 16.7 | **30.6** | 32.2 | 1.8 | 2.0×10⁻⁵ |
| CCR7⁺ lung dendritic cells, 72 h (%) [S02-A] | 2.5 | 7.3 | **30.7** | 35.0 | 4.2 | 4.1×10⁻⁶ |
| Antigen-carrying dendritic cells in node, 36 h (%) [S02-C] | — | 1.8 | **7.1** | 9.4 | 4.0 | 2.2×10⁻⁵ |
| Germinal-centre B cells, day 7 (%) [S03-K] | 1.2 | 2.3 | **6.5** | 9.8 | 2.8 | 0.007 |
| Follicular regulatory T cells, day 7 (%) [S04-B Foxp3] | 22.6 | 26.7 | **10.8** | 7.1 | 0.41 | 0.0002 |
| HAI titre, H1N1, day 14 (GMT) [S03-C] | 7.6 | 45.9 | **368** | 485 | 8.0 | 5.7×10⁻⁶ |
| HAI titre, H3N2, day 14 (GMT) [S03-G] | 10.0 | 34.8 | **320** | 368 | 9.2 | 2.2×10⁻⁶ |
| Neutralising titre, H1N1, day 14 (GMT) [S03-D] | 52.2 | 418 | **3,840** | 6,686 | 9.2 | 0.0002 |
| Neutralising titre, H3N2, day 14 (GMT) [S03-H] | 39.6 | 276 | **2,533** | 4,411 | 9.2 | 3.2×10⁻⁵ |
| IgG titre, H1N1, day 14 (GMT) [S03-A] | 55.7 | 393 | **7,305** | 11,959 | 18.6 | 3.1×10⁻⁶ |
| Granzyme-B⁺ lung CD8 T cells, day 3 (%) [S05-E] | 0.99 | 3.0 | **5.7** | 9.6 | 1.9 | 0.0008 |
| Interferon-γ⁺ CD8 T cells after H5N1 restimulation, day 14 (%) [S05-F] | 0.67 | 1.5 | **6.4** | 9.2 | 4.2 | 6.5×10⁻⁸ |
| Interferon-γ⁺ CD8 T cells, day 60 (%) [S05-G] | 1.5 | 3.0 | **9.9** | 14.4 | 3.2 | 0.0008 |
| Resident-memory CD8 T cells in lung, day 25 (%) [S05-I] | 0.58 | 1.0 | **4.0** | 6.0 | 4.0 | 3.3×10⁻⁷ |
| IgG2a / IgG1 quotient, H1N1 (recomputed) [S13-A ÷ S13-B] | — | 0.58 | **2.14** | 2.97 | — | — |
| IgG2a / IgG1 quotient, H3N2 (recomputed) [S13-C ÷ S13-D] | — | 0.51 | **2.73** | 2.89 | — | — |

- Across the 34 read-outs in Figure 3, PSLN-344 reached a median 70% of the young-adult response (interquartile range 50–83%, range 29–99%); PSLN-212 reached 19% (9–30%). PSLN-344 exceeded PSLN-212 by 1.6–24-fold, with p < 0.05 in 32 of 34. These read-outs come from a handful of experiments and are not independent of one another, so the median is a description, not a test.
- **The benefit of Mn²⁺ is specific to age.** Mn²⁺ raised lung Ifnb1 2.2-fold in aged mice and 1.3-fold in young mice (age × Mn²⁺ interaction p = 0.0004) [S01-A]. The same interaction holds for lung dendritic cells, antigen transport to the lymph node and T-cell priming (all p ≤ 0.006) [S01-E, S01-F, S02-C, S02-E].
- **A correction to the antibody subclass data.** The IgG2a/IgG1 table [S03-B] says PSLN-344 is IgG1-skewed (0.58). Its column headers are rotated (flag Q1). Recomputed from the titres, PSLN-344 is IgG2a-skewed like young animals (2.14 against 2.97 in young), and aged PSLN-212 is the IgG1-skewed group (0.58) [S13-A ÷ S13-B]. Anyone reading S03-B as printed will draw the opposite conclusion.
- **What PSLN-344 does not restore.** Co-stimulatory markers on lymph-node dendritic cells stay far below young levels (CD40⁺ 11.2% against 38.7%; CD86⁺ 14.5% against 37.9%) [S02-D]. Antibody titres reach 41–87% of young levels after one dose [S03-A to S03-H] and only 29–38% after a booster [S13-I, S13-J]. By day 30 the fraction of follicular regulatory T cells is back at the sham level (14.0% against 13.9%) [S04-C].

![Figure 3. Recovery of the young-adult immune response in aged mice.](figures/Fig3_immune_restoration.png){width=100%}

### 3.3 Durability and illness

- **Two months after one dose**, PSLN-344 protected 14/21 aged animals (67%; 95% CI 43–85%), PSLN-212 1/21, vaccine alone 0/21, and PSLN-212 in young animals 21/21 [S06-E, S06-F, S06-G]. The shortfall against young animals is significant (stratified log-rank p = 0.005). The fall from early protection in aged animals themselves is not statistically secure: p = 0.28 against the core experiments, 0.009 against all six as printed.
- **Old mice die without being challenged.** 4/21 untreated, unchallenged aged animals (19%; 95% CI 5–42%) died in the same 14-day window, and PSLN-344 survival after challenge is not distinguishable from that background (p = 0.44). I do not think background mortality explains the PSLN-344 deaths, though. The weight records of the PSLN-344 animals that were lost (5 can be identified; the survival tables count 7) stop at 77.5–85.3% of starting weight, the pattern of influenza, whereas those of the 4 untreated animals stop at 94.5–96.6% [S15-E, S15-F, S15-G]. The likelier reading is that protection wanes in aged animals, but these data cannot settle it. Any future study in old mice needs unchallenged controls and larger groups.
- **Young animals** were still fully protected at 180 days with either asset (8/8 and 8/8) [S09-F].
- **Protected aged animals still fall ill.** Averaged over the seven challenge experiments, aged PSLN-344 animals lost 14% of body weight at the worst point, young PSLN-212 animals 10%, aged PSLN-212 animals 18% [S15-A to S15-G; supportive only, flag Q5]. The vaccine prevents death, not infection. Lung virus load has never been measured.

### 3.4 Safety and tolerability

The table lists everything in the dataset that bears on safety; Figure 4 shows the data.

| Question | What the data show | Limits |
|-------------|--------------------------------------------------|-------------------------------------|
| General tolerability | Mean weight nadir 96.4% of baseline with PSLN-344 against 98.2% with vaccine alone; difference −1.8 points (95% CI −6.7 to +3.1); back to 99.8% by day 10 [S08-D]. | n = 5 per group; able to detect only differences of 3.5 points or more. No clinical observations, temperature or blood chemistry. |
| Lung inflammation at 16 h | PSLN-344 in aged mice: Il6 36-fold, Ccl2 590-fold, Tnf 40-fold. Interferon and chemokines are at or below what PSLN-212 does in young mice (Il6 60-fold, Ccl2 1,391-fold); Tnf and Il10 are above it (Tnf 40 against 14; Il10 7.3 against 1.8) [S09-A, columns A–U]. | n = 3. Transcripts only. |
| Does it resolve? | In the second S09-A panel, aged PSLN-344 lungs still show Tnf 8.4-fold, Il6 7.2-fold and Il10 4.2-fold when young lungs are at 0.5, 3.1 and 0.1 [S09-A, columns X–AS]. Lung monocytes and dendritic cells are still above baseline on day 8 (18.4% against 9.5% in sham; 13.7% against 2.4%) [S01-D, S01-E]. | The second panel is printed "16 h"; I treat it as 72 h because its Ifnb1 values are the 72 h values of S01-A, three of the five animals in every group (flag Q8). Aged PSLN-212 lungs also resolve slowly (Tnf 5.2-fold), so this is mostly an age effect. Nothing is measured after day 8. |
| Brain | No rise in Ifnb1, Tnf or Isg15 at 36 h against sham (differences +0.16, +0.27, +0.09; all p ≥ 0.92); the cholera-toxin positive control rose 5.50-, 3.50- and 2.68-fold [S10-A]. | n = 5, one time point, three transcripts, brain region not stated. With five animals a real rise could have been missed: the 95% CI for the Tnf difference is −0.98 to +1.53, on a scale where sham is 1.32 and the positive control 3.50. Manganese in brain was not measured. |
| Lung cell infiltrates | Not usable. The neutrophil table shares 35 of 100 values with the alveolar-macrophage table [S11-A, S11-B] (flag Q6). | — |
| Never measured | Histopathology of nose, lung or brain; Mn²⁺ dose and tissue levels; repeat dosing; males; any species other than mouse. | — |

![Figure 4. Safety and tolerability read-outs available in the dataset.](figures/Fig4_safety.png){width=100%}

### 3.5 Scorecard

| Dimension | Assessment | Basis |
|------------------------|--------------|--------------------------------------------------------------|
| Efficacy signal in aged animals | **Strong** | 18/21 against 3/21 survival; antibody titres 8.0- to 18.6-fold higher; consistent across 34 immune read-outs. |
| Reliability of the evidence | **Moderate** | One laboratory source, 2–10 animals per group, no statement of randomisation or blinding, 15 data-integrity items. |
| Mechanism | **Good, with gaps** | Two knock-outs and three inhibitors support individual steps; STING dependence and the role of Mn²⁺ alone are untested. |
| Safety | **Unknown** | Short-term tolerability only; no pathology; no manganese data. |
| Advantage over current vaccines for older adults | **Untested** | No licensed-type comparator in any experiment. |
| Translatability | **Uncertain** | Mouse only; BALB/c data female only; lower-airway delivery; whole-virus antigen; human STING variants untested. |
| Definition of the active ingredient | **Open** | Mn²⁺ is the difference-maker; CDN-1807 has not been separated from it or shown superior to cGAMP for protection. |
| Manufacturing | **Minimal** | Encapsulation efficiency for three preparations; particle and stability data not in the dataset. |

---

## 4. What we give up if we drop it, and what we do not

**We would give up:**

1. The only candidate in our hands that overcomes the failure of an intranasal STING-agonist adjuvant in old animals: 86% survival against 14% for the Mn-free version and 0% for vaccine alone [S06-A, S06-B, S06-C].
2. Single-dose protection within 2–3 days (21/24; 95% CI 68–97%), including against wild-type H5N1 (10/10) [S03-J, S06-B, S15-H]. If the duplicated block S06-D is replaced by what its body-weight record implies, the figure is 26/31.
3. Cross-subtype protection from seasonal-strain vaccine [S06-A, S06-B, S06-C, S06-G].
4. Near-young antibody and CD8 T-cell responses in old animals: haemagglutination-inhibition (HAI) titres 8.0–9.2-fold above PSLN-212 [S03-C, S03-G]; neutralising titres 9.2-fold [S03-D, S03-H]; cross-reactive CD8 T cells 6.4% against 1.5% [S05-F].
5. A mechanism with measurable markers at each step (sections 5 and 6), which shortens the path to a pharmacodynamic read-out in people.

**We would not be giving up, because our data do not contain it:**

- any human data, or any safety package;
- proof that CDN-1807, rather than Mn²⁺, is what works;
- superiority to the high-dose and adjuvanted vaccines already given to older adults;
- protection beyond 60 days in aged animals;
- a stand-alone antiviral or a product for younger adults (both assets and the cGAMP benchmark all give full protection in young mice: 24/24, 24/24, 7/7) [S09-B, S09-D, S09-F, S13-E].

**Dropping PSLN-212** costs nothing for the 65-and-over indication. It keeps a role as the Mn-free control and as a fall-back only if manganese proves unacceptable, in which case the elderly indication goes with it.

**The honest case for dropping the whole program** is not in the efficacy data. It is that the next gate needs about 480 aged mice, that the product needs an antigen partner, that intranasal manganese may be judged an unacceptable regulatory risk whatever the animal data show, and that we cannot yet say what we own. If the committee weighs those more heavily than a large, consistent preclinical effect in an under-served population, dropping is defensible. My judgement is that the effect is too large to discard before one blinded repeat and one safety study have been run.

---

## 5. Mechanism of action

**In one paragraph** (Figure 5 gives the same chain as a diagram). The surfactant-like liposome is taken up in the alveolus by macrophages, in a way that depends on surfactant proteins A and D, and its cargo reaches alveolar epithelial cells. The STING agonist triggers a short burst of type I interferon. In old lungs given PSLN-212 this burst is 44% of the young response; Mn²⁺ brings it to 99% and adds GM-CSF. Monocytes are recruited through CCR2. With interferon and GM-CSF present they become dendritic cells, which carry antigen to the draining lymph node and prime CD8 T cells; without Mn²⁺, in old lungs, they accumulate as macrophages instead and regulatory T cells stay high. The result with PSLN-344 is a germinal-centre and antibody response and a lung CD8 T-cell response close to those of young animals, and survival.

| Step | Evidence (aged mice, PSLN-344 against PSLN-212 unless stated) | Type of evidence |
|---------------|------------------------------------------------------------------------|-------------|
| 1. Uptake in the alveolus | Labelled liposome in 43.1% of alveolar macrophages in wild-type mice, 12.7% in mice lacking surfactant proteins A and D (p = 2.1×10⁻⁵) [S01-C]. Tracer in 15.8% of type II and 3.8% of type I epithelial cells, against 0.38% with free tracer [S01-B]. | Genetic; tracer |
| 2. Signal passes between cells | Blocking gap junctions with carbenoxolone cut monocyte recruitment from 7.3% to 3.1% (p = 0.003) [S11-C]. | Inhibitor |
| 3. Interferon burst | Lung Ifnb1 at 16 h: 37.1-fold against 16.6-fold (p = 3.7×10⁻⁸); young PSLN-212 37.6-fold. Down to 4.4-fold by 72 h [S01-A]. Mn²⁺ raises the maximum response (16- to 58-fold) without changing the half-maximal dose (11 and 13 µg) [S08-A]. | Observed |
| 4. GM-CSF | Lung Gm-csf 6.0-, 8.7- and 3.9-fold at 16, 36 and 72 h; never above 1.6-fold with PSLN-212 [S02-F]. | Observed |
| 5. Monocyte recruitment | Lung monocytes on day 4: 30.6% against 16.7% (sham 10.4%; young 32.2%) [S01-D]. A CCR2 antagonist cut them from 9.9% to 3.3% [S07-B] and cut the lung CD8 response from 6.8% to 1.4% (young mice) [S02-I]. | Observed; inhibitor |
| 6. Monocyte becomes dendritic cell | Donor-derived dendritic cells: 19.7% from wild-type marrow, 2.1% from marrow lacking the interferon receptor (p = 1.3×10⁻⁵), 12.4% when GM-CSF was added back [S02-H]. GM-CSF given with PSLN-212 raised these cells from 5.9% to 13.8% [S02-G]. Without Mn²⁺, old lungs accumulated Ly6C⁺CCR2⁺ macrophages instead (19.0 against 3.4 ×10⁵ cells on day 5; n = 3) [S07-A]. | Genetic; observed |
| 7. Migration and priming | CCR7⁺ lung dendritic cells 30.7% against 7.3% [S02-A]; antigen-carrying dendritic cells in the node 7.1% against 1.8% [S02-C]; priming of test CD8 T cells by those dendritic cells 18.7% against 0.8% [S02-E]. Transferred T cells also divide in the lung itself whether or not trafficking is blocked with pertussis toxin (59.0% and 55.1%), while division in the node falls from 30.9% to 6.8% [S05-C]. | Observed; inhibitor |
| 8. Less regulatory restraint | Follicular regulatory T cells 10.8% against 26.7% on day 7 [S04-B]; lung regulatory T cells 3.0% against 6.7% (n = 3) [S04-D]; CD206⁺ macrophages 48.9% against 71.5% [S11-E]. | Observed |
| 9. Adaptive response | Germinal-centre B cells 6.5% against 2.3% [S03-K]; HAI titre 368 against 46 [S03-C]; lung CD8 T cells making granzyme B on day 3 5.7% against 3.0% [S05-E]; resident-memory CD8 T cells in lung on day 25 4.0% against 1.0% [S05-I]. | Observed |

![Figure 5. Mechanism of action assembled from our data.](figures/Fig5_mechanism_of_action.png){width=100%}

![Figure 6. Pharmacodynamics: dose–response of lung Ifnb1, its time course, and Gm-csf.](figures/Fig6_pharmacodynamics.png){width=100%}

Figure 6 shows the interferon dose–response and time course and the GM-CSF signal on which steps 3 and 4 rest.

**What the mechanism does not yet rest on.**

- *STING itself.* No experiment uses STING-deficient animals or cells.
- *Mn²⁺ on its own.* There is no Mn²⁺-only liposome. Manganese is known outside our data to activate this pathway by itself, so we cannot say how much of the effect needs CDN-1807.
- *Which arm protects.* No depletion experiment shows whether CD8 T cells or antibody account for protection, particularly at 2–3 days.
- *Two blocks that should have helped and cannot.* The macrophage-transfer experiment has the same label on both groups [S07-C]. The uptake comparison with and without Mn²⁺ conflicts with S01-B about which column is which [S08-C]: as printed, Mn²⁺ cuts epithelial uptake about four-fold; with the headers in the order S01-B implies, it changes little.

---

## 6. Biomarkers

**What our data allow.** Every assay was terminal, so no animal has both a marker value and a challenge outcome. What we can say is which markers separate PSLN-344 from PSLN-212 animal by animal in aged mice, and which rank the groups in the same order as survival. 26 of 27 candidates show no overlap between the two groups (Table T13). That is unusually clean for groups of five and is one more reason to confirm against raw data.

Means are geometric for titres. n = 5 per group. The right-hand column is a proposal; none of these equivalents has been measured by us.

| Stage | Marker [block] | PSLN-212, aged: mean (range) | PSLN-344, aged: mean (range) | PSLN-212, young: mean | Overlap between the two aged groups | Accessible equivalent in people |
|------------|----------------------|-------------|-------------|---------|---------|----------------------|
| Target engagement (hours) | Lung Ifnb1 mRNA, 16 h (fold) [S01-A 16h] | 16.6 (13.4–19.0) | 37.1 (32.6–44.3) | 37.6 | none | Interferon-induced genes or CXCL10 in blood or nasal fluid (to be bridged in Study 1) |
| Target engagement (hours) | Lung Gm-csf mRNA, 36 h (fold) [S02-F] | 1.6 (1.4–1.8) | 8.7 (6.5–10.9) | not measured | none | GM-CSF protein in nasal fluid or serum (to be bridged) |
| Mechanism (days) | Lung monocytes, day 4 (%) [S01-D] | 16.7 (15.1–18.9) | 30.6 (24.4–36.2) | 32.2 | none | Blood monocyte subsets; nasal or sputum cells |
| Mechanism (days) | CCR7⁺ lung dendritic cells, 72 h (%) [S02-A] | 7.3 (5.2–10.0) | 30.7 (20.0–36.6) | 35.0 | none | Not routinely accessible |
| Mechanism (days) | Antigen-carrying dendritic cells in node, 36 h (%) [S02-C] | 1.8 (1.2–2.2) | 7.1 (5.4–8.9) | 9.4 | none | Not accessible |
| Response (weeks) | HAI titre, H1N1, day 14 [S03-C] | 45.9 (40–80) | 368 (160–640) | 485 | none | HAI titre (standard immunogenicity endpoint) |
| Response (weeks) | HAI titre, H3N2, day 14 [S03-G] | 34.8 (20–80) | 320 (160–640) | 368 | none | HAI titre |
| Response (weeks) | IgG2a titre, H1N1, day 14 [S13-A] | 83.4 (49–128) | 1,642 (936–3,452) | 4,642 | none | IgG subclass profile |
| Response (weeks) | Granzyme-B⁺ lung CD8 T cells, day 3 (%) [S05-E] | 3.0 (2.1–3.9) | 5.7 (4.2–6.5) | 9.6 | none | Activated CD8 T cells in blood, about day 7 |
| Response (weeks) | Interferon-γ⁺ CD8 T cells after H5N1 restimulation (%) [S05-F] | 1.5 (1.2–2.2) | 6.4 (5.2–7.4) | 9.2 | none | Interferon-γ ELISpot to conserved influenza proteins |
| Response (weeks) | Resident-memory CD8 T cells in lung, day 25 (%) [S05-I] | 1.0 (0.7–1.5) | 4.0 (3.0–4.8) | 6.0 | none | Bronchial or nasal sampling in a sub-study only |

**How I would use them.**

1. **Target engagement (hours).** Lung Ifnb1 and Gm-csf. Gm-csf is the more specific marker of the Mn²⁺ effect: at 16 and 36 h the lowest PSLN-344 animal was 2.7- and 3.7-fold above the highest PSLN-212 animal. Neither can be sampled from lung in people, so Study 1 must find blood or nasal-fluid equivalents (interferon-induced proteins such as CXCL10, and GM-CSF) measured in the same animals.
2. **Mechanism (days).** Lung monocytes on day 4, CCR7⁺ dendritic cells at 72 h and the follicular regulatory T-cell fraction on day 7. In people the accessible analogues are blood monocyte subsets and circulating follicular helper T cells about a week after dosing.
3. **Response (weeks).** HAI and neutralising titres, the IgG2a/IgG1 balance (recomputed values only), and interferon-γ-producing CD8 T cells after restimulation with a different subtype.

**Three cautions.**

- *HAI alone understates the difference, and the usual threshold does not transfer.* Every aged PSLN-212 animal had an HAI titre of 40–80 against H1N1, at or above the 1:40 level used as a benchmark in people, yet that group did not survive the matched challenge at 10 times the median lethal dose as printed (0/7; or 3 of 7 on the body-weight record) [S03-C, S03-I, S13-F]. T-cell markers should be co-primary.
- *Two markers every intranasal vaccine is judged on were never measured:* mucosal IgA and virus load in the lung or nose.
- *None of these is validated.* Study 1 takes serum and blood T-cell markers from the same animals that are then challenged, which is what turns a group difference into a correlate of protection.

---

## 7. Target demographic, for the market research team

**Primary population: adults aged 65 and over who are eligible for annual influenza vaccination.** Product: adjuvanted inactivated influenza vaccine, one dose per season, given into the airway without a needle.

Why this group, on our data:

- The advantage of PSLN-344 over the Mn-free version exists only in aged animals: 18/21 against 3/21 survival in aged mice, 24/24 against 24/24 in young mice [S06-A to S06-C; S09-B, -D, -F], with a significant age × Mn²⁺ interaction (p = 0.0004) [S01-A].
- Prior influenza infection, which virtually every older adult has had, did not reduce the benefit: 12/14 in previously infected and 12/14 in never-infected 14-month mice [S06-E and S06-F at rows 71–105].
- Mapping mouse age to human age is a convention from outside our data (mice of 18–24 months are commonly equated with people of about 56–69 years); treat "65 and over" as the working definition, not a result.

| Segment | Include in base-case TAM? | Basis in our data | What market research needs to supply |
|----------------------|--------------|--------------------------------|--------------------------------|
| Community-dwelling adults 65+ | Yes | Aged-mouse efficacy (above) | Head-count by country; seasonal vaccination coverage; price of current enhanced vaccines |
| Long-term-care residents 65+ | Yes | Same; none specific to frailty | Head-count; who administers; acceptability of airway dosing |
| Adults 65+ now receiving high-dose, adjuvanted or recombinant vaccine | Yes, as the share to be displaced | None: no head-to-head data yet (Study 1) | Current share of enhanced vaccines; recommendation status by country |
| Adults 50–64 | Upside case only | 14-month mice: 12/14 against 0/14 for PSLN-212 | Head-count; coverage |
| Pandemic or pre-pandemic H5 programmes | Size separately | 10/10 against wild-type H5N1 two days after dosing [S03-J]; seasonal vaccine protecting against H5N1 [S06-C, S06-F] | Government stockpile and tender volumes; these are procurement decisions, not per-head demand |
| Adults under 50; children | No | No difference between assets or against cGAMP in young mice | — |
| People with severe asthma or COPD, immunosuppression, or liver disease | Exclude for now | No data; likely early exclusions for an inhaled immune stimulant containing manganese | Prevalence within 65+, to discount the base case |

**Base-case formula, per country:** adults 65+ × seasonal influenza vaccination coverage × share who would take an enhanced or needle-free vaccine × price per dose, less the excluded groups in the last row. The 50–64 and pandemic rows are added only as separate upside cases.

Two further points for sizing:

- **Two commercial models give two different TAMs.** (A) Our own adjuvanted vaccine, which needs an antigen source. (B) The adjuvant licensed to vaccine manufacturers. Our data cover only mixing with in-house formalin-inactivated whole virus (annotation, page 1); licensed vaccines are split, subunit or recombinant.
- **Nasal spray or inhaler is undecided** (section 2), and affects both cost of goods and acceptability in this age group.

I have deliberately put no population or revenue figures here: none are in our data, and every number in this document is meant to trace to it.

---

## 8. Next steps

![Figure 7. Indicative sequence of next studies and decision gates.](figures/Fig7_plan_timeline.png){width=100%}

The studies are ordered so that the cheapest tests of the largest uncertainties come first (Figure 7). Timings are planning estimates from 1 November 2026; the limiting item is the supply of mice aged 18–20 months. Group sizes come from the variances and effect sizes in our own data (Table T12).

**Overview**

| Study | Question it must answer | Population | Comparators | Primary endpoint | Timing |
|-----------------|----------------------|---------------|--------------------|--------------|------------|
| Step 0. Data reconciliation | Does the workbook match the raw records? | None | Raw records | Each of the 15 items closed | Now to mid-December 2026 |
| 1. Confirmatory efficacy, attribution, benchmark | Is the benefit real, what is the active ingredient, and is it as good as licensed-type vaccines? | Aged BALB/c, both sexes, 16 per arm | PSLN-212; Mn²⁺-only; Mn²⁺ + cGAMP; CMP-204; intramuscular MF59-type and high-dose antigen; antigen alone | Survival after matched-strain challenge | Results about June 2027 |
| 2. Safety and biodistribution | Does inflammation resolve and does manganese stay out of the brain? | Aged and young BALB/c, both sexes | Saline; empty liposome; Mn²⁺-only; PSLN-212 | Histopathology; tissue manganese | Results about June 2027 |
| 3. Human cells | Does it work on human STING variants and in cells from older donors? | Reporter lines; donors 65+ and 18–40 | PSLN-212; Mn²⁺-only; CMP-204 | Interferon-β and CXCL10 release | Results about April 2027 |
| 4. Manufacturing and analytics | What is in a dose, and is it reproducible and stable? | Five or more batches | — | Mn²⁺ content, particle attributes, potency, stability | Analytics by June 2027; stability to early 2028 |
| 5. Dose, regimen, durability | What is the lowest dose, is a booster needed, does it last six months? | BALB/c dosed at 18 months, 25 per arm | PSLN-212 two doses; intramuscular MF59-type | Antibody titres to day 180 | Results about February 2028 |
| 6. Ferret | Does it work in a second species with a device people can use? | Adult ferrets, 6–8 per arm | Antigen alone; licensed intramuscular vaccine; nasal spray against aerosol | Virus shedding after challenge | Results about February 2028 |
| 7. IND-enabling and first-in-human | Is it safe and immunogenic in people? | Adults 50–64, then 65+ | Licensed high-dose or adjuvanted vaccine; antigen alone | Reactogenicity; HAI titres at day 28 | Not before 2029 |

**Gates**

| Gate | When | Proceed if | Stop or re-scope if |
|------|-------------|------------------------------------------|---------------------------------------|
| 0 | Mid-December 2026 | Reconciled data still show a survival difference of at least 50 points and an HAI ratio of at least 4-fold between PSLN-344 and PSLN-212 in aged mice | Key blocks cannot be reconciled and will not be repeated |
| 1 | About July 2027 | Study 1 meets its "Go" rule; Study 2 triggers no stop rule; Study 3 raises no concern | Benefit not reproduced; Mn²⁺-only liposome equals PSLN-344; manganese persists in brain; a licensed-type vaccine is as good on every endpoint |
| 2 | About March 2028 | Day-180 titres at least half the day-28 level, with one or two doses; less virus shedding in ferrets with a usable device; consistent batches and six months' stability | Protection gone by six months even with two doses; no effect in ferrets with any usable device; product cannot be made consistently |

The gate thresholds are my proposals for the committee to amend, not values derived from the data.

Two items outside the laboratory should start now, because Study 1 may change their answers. First, ask IP counsel what we can protect if manganese rather than CDN-1807 turns out to carry the effect. Second, open discussions with an antigen source, since the product cannot exist without one. Neither question can be answered from our data.

### Step 0. Reconcile and lock the data (now to mid-December 2026; no animals)

| Element | Plan |
|--------------|--------------------------------------------------------------------------------------|
| Must establish | That the workbook matches the raw records for every block the case uses. |
| Scope | The 15 items in section 10, starting with Q1–Q6. Sources: ELISA plate files, flow-cytometry exports, cage-side survival and weight sheets, study plans (for group identity and group size). |
| Output | A corrected, version-controlled workbook; a closure note per item; a re-run of the scripts supplied with this proposal, which regenerate every table, figure and number. |
| Gate 0 | Proceed if, after correction, the survival difference between PSLN-344 and PSLN-212 in aged mice is still at least 50 percentage points (now 71; 95% CI 51 to 91) and the HAI ratio still at least 4-fold (now 8.0–9.2). A flagged experiment that cannot be reconciled is repeated inside Study 1, not cited. |

### Study 1. Confirmatory efficacy, attribution and benchmark in aged mice

| Element | Plan |
|--------------|--------------------------------------------------------------------------------------|
| Must establish | (a) The survival benefit reproduces under randomisation and blinding, in both sexes. (b) What the active ingredient is: CDN-1807, Mn²⁺, or both. (c) Whether PSLN-344 matches or beats the types of vaccine older adults already receive. (d) Which markers predict protection in the same animal. |
| Population | BALB/c mice aged 20 months or more, 8 female and 8 male per arm (all existing BALB/c data are female); one young (8-week) reference arm. |
| Arms and comparators | Intranasal unless stated, with a licensed-format split H1N1 + H3N2 antigen: (1) antigen + empty liposome; (2) PSLN-212; (3) PSLN-344; (4) Mn²⁺-only liposome; (5) Mn²⁺ + cGAMP liposome; (6) CMP-204; (7) intramuscular antigen with a squalene oil-in-water emulsion adjuvant (MF59-type); (8) intramuscular high-dose antigen, 4× haemagglutinin; (9) PSLN-344 with whole inactivated virus, to bridge to the existing data; (10) unvaccinated, challenged; (11) unvaccinated, unchallenged, for background mortality; (12) young mice, PSLN-212. |
| Conduct | Animals randomised by weight and cage; dosing, scoring and assays blinded; analysis plan fixed before unblinding; the event that ends an animal's record (death or a defined humane end-point) written down in advance. None of this is stated for the existing data. |
| Primary endpoint | Survival 14 days after matched-strain H1N1 challenge (10× the median lethal dose) given on day 14: arm 3 against arm 2, and arm 3 against arm 1. |
| Key secondary endpoints | Day-14 serum HAI and neutralising geometric mean titres, arm 3 against arms 7 and 8; lung virus titre 3 and 6 days after challenge (satellite animals); weight-loss area under the curve; arm 3 against arm 4 and against arm 5 (attribution). |
| Other read-outs | IgA in nasal wash and lung lavage; IgG2a/IgG1; influenza-specific CD8 T cells in blood on day 10; lung Ifnb1 and Gm-csf at 16 h and lung monocytes and dendritic cells on day 4 (satellites); serum CXCL10, interferon-β and GM-CSF at 6 and 24 h as candidate blood surrogates. Serum and blood T-cell markers are taken from the animals that are then challenged. |
| Timing | Dose on day 0; satellites at 16 h and day 4; bleeds on days 10 and 14; challenge on day 14; observation to day 28. About seven months including animal supply and analysis. If positive, a second cohort (arms 1, 2, 3, 7, 8) receives a cross-subtype challenge. |
| Size and power | About 270 aged and 16 young mice. Sixteen per arm gives 99% power for the survival difference seen so far, 60% if PSLN-212 truly protects 3 of 7, and 43% against an active comparator assumed to protect half. Comparisons with licensed-type vaccines therefore rest on titres and virus load: a 2-fold HAI difference needs 11 per arm and a 2-fold neutralising difference 22 (90% power; log2 SD 0.68 and 0.98) [S03-C, -D, -G, -H]. |
| Decision rule | **Go:** arm 3 survival at least 75% and at least 40 points above arms 1 and 2; arm 3 better than arm 4; HAI no more than 2-fold below the better of arms 7 and 8, and better on at least one of cross-subtype survival, lung virus or CD8 response. **Re-scope:** arm 4 equals arm 3 (the asset is manganese, not CDN-1807), or arm 5 equals arm 3 (the agonist is interchangeable with cGAMP). **Stop:** benefit not reproduced, or arms 7 or 8 at least as good on every endpoint. |

### Study 2. Safety, tolerability and biodistribution (non-GLP)

| Element | Plan |
|--------------|--------------------------------------------------------------------------------------|
| Must establish | That inflammation in nose and lung resolves, that manganese does not accumulate in the olfactory bulb or brain, and that repeat dosing is tolerated, in aged animals. |
| Population | BALB/c mice aged 20 months or more, both sexes; 3 per sex per group per time point for pathology and 5 per time point for manganese. A young (8–10-week) subset for saline and both PSLN-344 doses. |
| Groups and comparators | Each with vaccine: saline; empty liposome; Mn²⁺-only liposome; PSLN-212 20 µg; PSLN-344 20 µg; PSLN-344 40 µg (the highest dose tested so far [S08-A]). Single dose for all; three doses two weeks apart for saline, Mn²⁺-only and both PSLN-344 doses. Intranasal cholera toxin as positive control for the brain panel, as in S10-A. |
| Primary endpoints | Blind-scored histopathology of nasal cavity including olfactory epithelium, olfactory bulb, brain, lung and draining lymph node at 24 h, day 8 and day 28 after the last dose. Manganese by mass spectrometry in olfactory bulb, striatum, remaining brain, lung, liver and blood at 6 h, 24 h, day 7 and day 28. |
| Other read-outs | Differential cell count, protein and LDH in lung lavage (replaces the unusable neutrophil table); lung cytokine panel at 16 h, 72 h, day 7 and day 14 (also settles the time point of the second S09-A panel); serum IL-6, TNF and interferon-β; daily weight, temperature and clinical score; haematology and clinical chemistry; brain transcripts at 6 h, 36 h and day 7 (Ifnb1, Tnf, Isg15 as before, plus Il1b, Il6, Gfap, Aif1); a test of smell. |
| Timing | About four months in life, including the repeat-dose arm and 28 days of recovery. Reports for Gate 1. |
| Size and power | About 250 mice, some 215 of them aged. Weight is recorded on every animal kept to day 8 or later (12–18 per group). Fourteen per group detect a 2-point difference in weight nadir with 90% power (SD 1.55 points) [S08-D]; the existing study could detect 3.5 points. |
| Decision rule | **Stop or reformulate** if manganese in olfactory bulb or brain is still above control on day 28; if any lesion of moderate or greater grade persists to day 28; if weight loss exceeds 10% or any death is attributed to treatment; or if brain transcripts reach the cholera-toxin level. |

### Study 3. Human cells

| Element | Plan |
|--------------|--------------------------------------------------------------------------------------|
| Must establish | That CDN-1807 activates the common human variants of STING, and that the age-related deficit and its rescue by Mn²⁺ exist in human cells. (Human STING variants differ in their response to cyclic dinucleotides; this is knowledge from outside our data.) |
| Population | Reporter cell lines carrying the main human STING variants; monocyte-derived macrophages and dendritic cells from about 20 donors aged 65 or more and 20 aged 18–40; alveolar macrophages from lavage where available. |
| Comparators | PSLN-212, PSLN-344, Mn²⁺-only liposome, CMP-204, empty liposome; six-point dose series. |
| Endpoints | Primary: interferon-β and CXCL10 release (half-maximal concentration and maximum) by age group and preparation. Secondary: GM-CSF, TNF, IL-6, IL-10; cell viability. |
| Timing | Three to four months, alongside Study 1. |
| Decision rule | **Concern** if CDN-1807 is inactive on a common variant, or if Mn²⁺ adds nothing in cells from older donors. In mice Mn²⁺ raised Ifnb1 2.2-fold in aged and 1.3-fold in young animals [S01-A]. |

### Study 4. Manufacturing and analytical package

| Element | Plan |
|--------------|--------------------------------------------------------------------------------------|
| Must establish | What a dose contains and that it can be made reproducibly. |
| Scope | What "20 µg of adjuvant" refers to (agonist or whole particle), Mn²⁺ content per dose and Mn : CDN ratio (none is reported in our data); which of the two preparation methods named in the annotation made which batch; particle size, charge and morphology (measured according to the annotation, absent from the workbook); encapsulation efficiency over at least five batches (so far 49–59% in three PSLN-344 preparations [S08-B]); release of CDN-1807 and Mn²⁺ in simulated lung fluid; a cell-based potency assay; stability of the freeze-dried product at −20 °C, 2–8 °C and 25 °C for 3, 6 and 12 months; compatibility with the vaccine antigen and with a nasal-spray pump and a nebuliser. |
| Timing | Analytical package in six months; stability read-outs to month 15. |
| Decision rule | Gate 2 requires consistent batches and at least six months' stability at 2–8 °C, or a credible cold-chain plan. |

### Gate 1 (about July 2027)

Go to Studies 5 and 6 only if Study 1 meets its "Go" rule, Study 2 triggers no stop rule, and Study 3 raises no concern. This is the point at which the largest uncertainties (reproducibility, active ingredient, manganese safety) are resolved for the cost of roughly 480 aged mice.

### Study 5. Dose, regimen and durability (after Gate 1)

| Element | Plan |
|--------------|--------------------------------------------------------------------------------------|
| Must establish | The lowest effective dose, whether a second dose is needed, and whether protection lasts a six-month influenza season in old animals. |
| Population | BALB/c mice dosed at 18 months, so that the day-180 challenge falls at 24 months; both sexes; 25 per arm to leave about 20 evaluable (untreated aged animals died at 19% per fortnight at about 22 months [S06-E, -F, -G]). |
| Arms and comparators | Sham; PSLN-344 at 5, 10 and 20 µg once; PSLN-344 20 µg on days 0 and 28; PSLN-212 20 µg on days 0 and 28; intramuscular MF59-type comparator; PSLN-344-vaccinated but unchallenged; untreated and unchallenged. |
| Primary endpoint | HAI and neutralising geometric mean titres on days 14, 28, 60, 120 and 180 from serial bleeds; the day-180 titre relative to day 28. |
| Other read-outs | Survival and lung virus after challenge on day 180; influenza-specific CD8 T cells in blood over time; resident-memory CD8 T cells in lung and plasma cells in bone marrow on day 180 (satellites). |
| Timing | Six and a half months in life; results about February 2028. |
| Size and power | About 250 aged mice. Twenty evaluable per arm give 99% power for the day-60 difference already seen, but only 46% to tell 67% survival from 93% (83% even at 40 per arm). Waning is therefore judged on titres and T cells, not survival. |
| Why these doses | Lung Ifnb1 at 5 and 10 µg PSLN-344 (8.3- and 21.1-fold) already matches or exceeds PSLN-212 at 20 µg (12.6-fold); 20 µg gives 91% of the 40 µg response [S08-A]. A booster raised IgG 2.1-fold with PSLN-344 (separate experiments, S13-I against S03-A). |

### Study 6. Ferret (after Gate 1)

| Element | Plan |
|--------------|--------------------------------------------------------------------------------------|
| Must establish | That the effect is not specific to the mouse and survives a delivery method people can use. |
| Population | Adult ferrets, influenza-naive and previously infected (prior infection did not blunt PSLN-344 in 14-month mice); aged ferrets if they can be sourced; 6–8 per arm. |
| Arms and comparators | Antigen alone by nasal spray; antigen + PSLN-344 by nasal spray at two dose levels; antigen + PSLN-344 by small-particle aerosol; intramuscular licensed adjuvanted or high-dose vaccine. |
| Primary endpoint | Virus shed in nasal washes, as area under the curve over days 1–7 after challenge. |
| Other read-outs | Fever, weight and clinical score; HAI and neutralising titres on days 14 and 28; nasal IgA; lung virus and pathology at necropsy; tolerability of each route. |
| Timing | About seven months. |
| Decision rule | Gate 2 requires less shedding than antigen alone with a device people can use, and antibody responses not inferior to the intramuscular comparator. If only aerosol works, the product is an inhaled vaccine, with different device, safety and market assumptions. |

### Gate 2 (about March 2028) and Study 7

Gate 2 asks whether durability (Study 5), a second species with a usable device (Study 6) and manufacturing (Study 4) justify the IND-enabling package.

**Study 7, only after Gate 2.** GLP repeat-dose toxicology in two species with the clinical formulation and device, including neuropathology and manganese kinetics; GMP manufacture. First-in-human concept: randomised, observer-blind, dose-escalating, in healthy adults aged 50–64 first and then 65 and over. Arms: intranasal antigen + PSLN-344 at three dose levels; intranasal antigen alone; a licensed high-dose or adjuvanted intramuscular vaccine. Primary endpoints: solicited nasal, respiratory and systemic reactions on days 0–7, adverse events to day 28, serious adverse events to 12 months, smell test and spirometry. Immunogenicity: HAI geometric mean titre ratio and seroconversion on day 28 against the licensed comparator; neutralising titres; nasal IgA; interferon-γ T-cell response; blood interferon signature, CXCL10 and GM-CSF at 6–24 h as target-engagement markers; persistence at day 180. Not before 2029 on this plan.

---

## 9. What I considered and ruled out

**Assets and combinations**

| Option | Verdict | Why |
|----------------------|-------------|-----------------------------------------------------------------|
| PSLN-212 as lead for older adults | Ruled out | 3/21 survival in aged mice; 19% of the young immune response. Not a dosing problem: its interferon response levels off at 16-fold against 58-fold for PSLN-344 [S08-A]. |
| Two doses of PSLN-212 instead of adding Mn²⁺ | Ruled out on current data | After a booster, IgG was still 3.5-fold (H1N1, p = 0.19) and 11.5-fold (H3N2, p = 3.1×10⁻⁵) below PSLN-344, and 9- to 40-fold below young animals [S13-I, S13-J]. No challenge data. Kept as an arm in Study 5. |
| PSLN-212 plus recombinant GM-CSF | Ruled out as a product | GM-CSF raised monocyte-derived dendritic cells 5.9% to 13.8% [S02-G], which supports the mechanism, but it took four daily doses of a protein and there are no protection data. |
| Adding the TLR7/8 agonist R848 | Ruled out | Less interferon than PSLN-344 (24.3- against 37.1-fold) [S01-A]; mean weight nadir 90.0% with 4 of 5 animals losing more than 10% and one with no day-10 record [S08-D]; Tnf 202-fold and Il10 179-fold at 16 h and still 50- and 45-fold in the later panel [S09-A]. |
| CMP-204 (cGAMP liposome) | Benchmark only | Weakest interferon response (7.8-fold; maximum 7-fold) [S01-A, S08-A]. Not ours. |
| A higher dose of PSLN-344 | Ruled out | 20 µg already gives 91% of the response at 40 µg [S08-A]. |

**Positioning**

| Option | Verdict | Why |
|----------------------|-------------|-----------------------------------------------------------------|
| Stand-alone antiviral or prophylactic | Ruled out | PSLN-344 without vaccine: 0/7 [S15-H]. |
| Younger adults or all ages | Ruled out as lead indication | No difference between the assets (24/24 and 24/24) or from the cGAMP benchmark (7/7) in young mice [S09-B, -D, -F; S13-E]. |
| Pandemic H5N1 as lead indication | Kept as secondary | The strongest single result (10/10 against wild-type virus two days after dosing) sits in a block whose comparator labels are disputed (flag Q3), and demand is set by government procurement. |

**Explanations for the advantage of PSLN-344 that the data exclude**

| Explanation | Verdict | Why |
|----------------------|-------------|-----------------------------------------------------------------|
| More drug per particle | Excluded | Encapsulation 54.8% against 59.6% [S08-B]. |
| The same effect at a higher effective dose | Excluded | Mn²⁺ raises the maximum, not the potency; PSLN-212 at 40 µg (14.9-fold) stays below PSLN-344 at 10 µg (21.1-fold) [S08-A]. |
| Non-specific innate protection | Excluded | No protection without antigen [S15-H]. |
| Better uptake by airway epithelium | Not supported | Uptake is lower or equal depending on how the S08-C headers are read (flag Q7). |

**Recommendations I considered**

| Option | Verdict | Why |
|----------------------|-------------|-----------------------------------------------------------------|
| Drop now | Rejected for now | The effect is large and consistent, and one blinded repeat plus one safety study would settle most of the doubt. The case for dropping is set out in section 4. |
| Advance both assets | Rejected | PSLN-212 adds nothing for this population except as a control. |
| Move straight to IND-enabling work | Rejected | Data not reconciled; no safety data; active ingredient undefined; no comparator data. |

**Data I chose not to rely on:** S06-D (duplicate of S06-C); S03-B and S03-F as printed (replaced by recomputed values); S07-C; S11-A and S11-B; S08-C; the unlabelled rows in S08; body-weight blocks as independent confirmation; S05-A and S05-B (two animals per point and contradictory conditions).

---

## 10. Data integrity: what must be fixed before the committee sees the file

I checked every block against the annotation and against the other blocks it should agree with. The items below are reproducible with the scripts named in `tables/QC_log.csv`, which also gives the full wording. None reverses the direction of the main result. Several change individual numbers that a committee member could quote back. Figure 8 shows the six that matter most.

| ID | Where | What is wrong | Consequence | How handled here |
|-----|-------------|--------------------------------|------------------------------|--------------------|
| Q1 | S03-B, S03-F | Column headers rotated one place relative to the titres the quotients are computed from (S13-A to S13-D). The S13 labels agree with total IgG in S03-A; the S03-B and S03-F labels do not. | As printed, PSLN-344 looks IgG1-skewed (0.58); recomputed it is IgG2a-skewed (2.14). | Recomputed values used. |
| Q2 | S03-I against S13-F | Same animals, different group lists; the survival table has all 7 "PSLN-212" animals dead by day 6, the weight table has 3 of them recovering. | PSLN-212 in the matched-strain model is 0 of 7 or 3 of 7. As printed, the cGAMP benchmark (3/7) beats PSLN-212 (p = 0.001), against every immune read-out. | Set aside from the core experiments; the PSLN-344 result (7/7) agrees in both blocks. |
| Q3 | S03-J against S13-G | Same animals, different group lists (one has PSLN-212, the other Naive). Stated n = 9, ten per group found; one animal has no day recorded. | Unclear whether the wild-type H5N1 study had a PSLN-212 arm. | Set aside from the core experiments; PSLN-344 (10/10) agrees in both blocks. |
| Q4 | S06-C and S06-D | Identical for all 28 animals. | One of the two H5N1 experiments (day 14 or day 3) is undocumented. | S06-D dropped; day-3 result taken from S15-H. |
| Q5 | S15-C and S15-I; S15-A, S15-M, S15-O | Body-weight values repeated across experiments that should be independent (40 of 49 identical between S15-C and S15-I). | Weight data are not independent confirmation; the second- and third-strain experiments need verifying. | Weights used as a consistency check only. |
| Q6 | S11-A and S11-B | 35 of 100 values identical between "alveolar macrophages" and "neutrophils". | No usable neutrophil data. | Both excluded. |
| Q7 | S08-C against S01-B | Column headers probably out of order. | Effect of Mn²⁺ on epithelial uptake is a four-fold fall or no change, depending on the reading. | Not used. |
| Q8 | S09-A, second panel | Printed "16 h"; all 21 of its Ifnb1 values are 72 h values of the same groups in S01-A, none are 16 h values. The block is on a log10 scale; every other transcript block is linear. | The only evidence on resolution of lung cytokines has an inferred time point; read as linear, the values would understate every response. | Back-transformed; treated as 72 h, and said so. |
| Q9 | S07-C | Both groups have the same label. | Uninterpretable. | Excluded. |
| Q10 | S08 rows 89–101 | Unlabelled data. | Unknown experiment. | Excluded. |
| Q11 | S08-A | "PSLN-344/R848" is not a preparation described in the annotation. | Identity of one dose-response curve unknown. | Shown as printed; not relied on. |
| Q12 | S03-J, S13-E, S05-A, S05-B, S09-F, S08-D | Stated group size differs from the number of observations. | Sample sizes quoted must be the observed ones. | Observed n used throughout. |
| Q13 | Sheet S06 | Labels "S06-E" and "S06-F" each used for two different experiments. | Risk of citing the wrong experiment. | Second pair cited as "S06-E/F at rows 71–105". |
| Q14 | Survival against body-weight tables | 54 of 65 group-level comparisons agree; apart from the cases in Q2–Q4, the rest differ by one or two animals. | Individual survival counts carry about ±1 animal of uncertainty. | Survival tables used as primary. |
| Q15 | Annotation | Challenge conditions missing for S15-L and S15-N; several time points and ages not stated; Mn²⁺ dose, particle size and stability data absent. | Limits interpretation; the missing Mn²⁺ dose is a gap in the asset description itself. | Stated where used. |

Two observations that are not errors but belong here. First, the Ifnb1 rows of S09-A are three of the five animals of each S01-A group, so they are the same data and not independent evidence. Second, the separation between PSLN-344 and PSLN-212 is complete in 26 of 27 biomarker read-outs; real data from groups of five usually overlap more than that.

![Figure 8. The six most consequential data-integrity findings.](figures/Fig8_data_integrity.png){width=100%}

---

## Appendix A. Methods

- **Parsing.** Each block was read from explicit cell ranges (`analysis/psln_blocks.py`) into one tidy table of 6,107 observations (`data_tidy/psln_tidy_all_blocks.csv`). Group labels were kept as printed.
- **What "survival" means here.** An animal counts as surviving if the time-to-event block records no event for it. The annotation does not say whether the event is death or a humane end-point.
- **Survival.** Survivors over animals with exact (Clopper–Pearson) 95% confidence intervals; log-rank tests, asymptotic and by exact permutation; pooled comparisons stratified by experiment (stratified log-rank; Mantel–Haenszel risk difference). Log-rank statistics were reproduced with R `survival::survdiff`. The one animal with a survival flag but no day [S03-J] was treated as censored on day 21.
- **Other read-outs.** The methods stated in the annotation: one-way ANOVA with Tukey's test, two-way ANOVA, Student's t test. Titres were analysed on the log2 scale and summarised as geometric means; titres of 0 were set to 5 (half the lowest dilution).
- **Dose–response.** Hill model fitted on the log scale with bootstrap confidence intervals.
- **Body weight.** An animal was taken to have left the study when its cells go blank or its record ends in two or more identical values. The rule was checked on the untreated groups, where it matches the recorded death days to within one weighing interval.
- **Power.** Exact power of Fisher's test for survival; t-test power on log2 titres using within-group variances from our data.
- **Not done.** No adjustment for multiple comparisons across blocks; p values are descriptive. No external data were used for any number in this document.

## Appendix B. Files supplied

| File | Content |
|-----------------------------------|-----------------------------------------------------------------|
| `tables/T0_evidence_ledger.csv` | Every number quoted in this document: value, block, cell range, method, script |
| `tables/PSLN_supporting_analysis.xlsx` | All tables below in one workbook |
| `tables/T1`–`T3` | Survival by group, pairwise tests, pooled analyses |
| `tables/T4`–`T7` | Group summaries, pairwise tests, omnibus tests, restoration table |
| `tables/T8`–`T13` | Dose–response, tolerability, lung cytokines, morbidity, power, biomarker separation |
| `tables/QC_log.csv` and `QC_*.csv` | Data-integrity log and supporting checks |
| `figures/Fig1`–`Fig8` | Figures used here, drawn at printed size (7.2 in wide, 300 dpi) |
| `data_tidy/` | Tidy export of the workbook and block index |
| `analysis/` | Scripts; `run_all.sh` regenerates everything from the workbook, including this document as `.md`, `.docx`, `.html` and `.pdf` |
