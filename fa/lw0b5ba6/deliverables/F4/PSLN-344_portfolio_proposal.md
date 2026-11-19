# PSLN-344 — portfolio review: recommendation and next-step proposal

*Prepared 1 Nov 2026 from `psln_program_dataset.xlsx` (last saved 3 Sep 2026) and `psln_program_annotation.pdf` (15 Sep 2026). Codes in square brackets, e.g. [S06-A], are workbook blocks; "T" numbers are analysis tables in `analysis/tables/`. "Aged" = mice ≥ 20 months; "young benchmark" = 7–8-week-old mice given the same vaccine with PSLN-212. The asset is taken to be PSLN-344 (CDN-1807 + Mn²⁺ in the surfactant-mimetic liposome).*

---

## 1. Recommendation

**Keep PSLN-344 — conditionally. Hold it at its current stage and run a gated de-risking package of roughly 12 months. Authorise only the data audit (Gate 0) now, release each later tranche when the preceding gate is passed, and make no IND-enabling commitment before the last gate (Gate 2, about month 12).**

**How it looks in one line:** a large, age-specific efficacy signal in mice, resting on a data package that is not yet decision-grade and on three things nobody has tested: that the effect comes from our molecule, that it is safe, and that it translates.

Three things the committee should know before the detail:

1. **What the asset is, on our own data: an intranasal vaccine adjuvant for aged hosts, not a stand-alone STING drug.** Given without antigen it protected 0/7 animals; vaccine alone protected 0/7; the two together protected 6/7 [S15-H; T02]. There is no oncology experiment anywhere in the dataset.
2. **The efficacy signal is large and consistent.** After one intranasal dose and a lethal influenza challenge 2–14 days later, 42/45 aged mice survived with PSLN-344 (93%, 95% CI 82–99%), against 1/45 with vaccine + empty liposome and 8/45 with our Mn-free formulation PSLN-212 (six experiments of 7–10 animals per arm, none repeated; stratified log-rank p < 0.0001 vs PSLN-212) [S03-I, S03-J, S06-A–D; T04]. Without S03-J, the one block that does not state animal age, the counts are 32/35, 0/35 and 5/35.
3. **The package is not yet decision-grade.** The workbook has labelling errors that reverse at least one conclusion if read as printed, duplicated values, and body-weight tables that disagree with the survival tables in 10 of 65 group comparisons (Appendix A). The headline survives a worst-case reading of every conflict (40/45 vs 12/45), but individual numbers may move. The controls that would tie the effect to *our* STING agonist (Mn-only, STING-deficient) were never run, and safety rests on one body-weight curve and a handful of lung and brain transcripts.

The asset is worth keeping because the effect is large, it is specific to aged hosts (where our Mn-free formulation fails), and the open questions can be answered with a handful of mouse and in-vitro studies. It does not justify more than gated spend until they are answered.

![Figure 1](figures/fig1_survival_overview.png)

| Gate | Question | Pass | Fail → |
|---|---|---|---|
| **0** (≈ 6 weeks, no animals) | Do the pivotal numbers survive reconciliation with raw records? | Every pivotal survival and serology block re-derived from source; Appendix A items closed | Stop |
| **1** (≈ month 7) | Does it replicate blinded, is it our molecule, and is it acceptably safe at first look? | Studies 1, 3a, 4 below | Stop or re-scope |
| **2** (≈ month 12) | Is there a dose window, does it work with a clinical-format antigen by a deliverable route, and in a second species? | Studies 2, 3b, 5, 6 below | Stop, partner or re-scope |

Timings are planning assumptions, not data. They assume ≥ 20-month mice of both sexes are on hand; Study 1 alone needs 108.

---

## 2. Next steps: what each study must establish and the endpoints we need to see

Thresholds are anchored to what we observed; where we have no data the threshold is a conventional one and is marked *new*.

### Gate 0 — Data audit (before any new spend)
- **Must establish:** that the survival, serology and T-cell tables match raw records (animal IDs, cage cards, balance and plate-reader exports, FCS files), and why weight trajectories recur across experiments.
- **Endpoints:** corrected, animal-level workbook; each Appendix A item closed with evidence; pivotal results ([S03-I/J], [S06-A–G], [S15-H/L/N], [S03-A–H], [S13-A–D]) re-derived independently.
- **Stop if:** pivotal survival tables cannot be traced to source, or the re-derived PSLN-344 vs PSLN-212 difference in aged mice is no longer significant.

### Study 1 — Blinded replication with the missing controls (Gate 1)
- **Must establish:** (a) the aged-host benefit replicates under randomisation and blinding in both sexes; (b) it needs CDN-1807 and Mn together in the particle; (c) it runs through STING.
- **Design essentials:** aged (≥ 20 months) mice, heterosubtypic model of [S06-A]; aged C57BL/6 is an option because STING-deficient lines share that background and the effect was seen there (6/7 vs 0/7) [S15-L]; arms: empty liposome, PSLN-212, PSLN-344, Mn-only liposome, PSLN-212 + free Mn²⁺, free CDN-1807 + Mn²⁺, young + PSLN-212; 18 per arm (9 F + 9 M; 108 aged mice), which gives 91% power for 85% vs 30% survival (the n = 7 used so far gives 36%) [T11]. Serology and challenge in the same individually identified animals. Target-engagement arm in STING-deficient mice or with a STING antagonist.
- **Endpoints we need to see:**
    - Survival ≥ 75% with PSLN-344 and ≥ 40 points above each of PSLN-212, Mn-only and empty liposome, p < 0.05 each (observed so far: 93% vs 18% vs 2%; worst-case reading of conflicting tables 89% vs 27%) [T04, T04c].
    - HAI GMT ≥ 4-fold over PSLN-212 and ≥ 50% of the young benchmark (observed 8.0- and 9.2-fold; 76% and 87%) [S03-C, S03-G].
    - Lung virus titre ≥ 2 log₁₀ below sham 4–5 days after challenge (*new* — no virological read-out exists).
    - Mucosal IgA in nasal wash and lavage above PSLN-212 (*new*).
    - *Ifnb1* induction cut by ≥ 80% and the HAI advantage lost when STING is absent or blocked (*new*).
- **Stop or re-scope if:** survival < 60%; or Mn-only liposome comes within 20 points of PSLN-344 (CDN-1807 is then not contributing); or the effect persists without STING.

### Study 2 — Dose window, clinical-format antigen and head-to-head comparators (Gate 2)
- **Must establish:** the lowest effective dose and the margin to the first tolerability signal; that the benefit holds with a licensed-format split or recombinant antigen (everything so far used in-house formalin-inactivated whole virus); and how it compares with the injected enhanced-vaccine approaches used in older adults (high antigen dose; squalene-emulsion adjuvant). None of these comparators is in our dataset.
- **Design essentials:** aged mice; PSLN-344 at 2.5, 5, 10, 20 µg (5 and 10 µg gave 16% and 42% of the *Ifnb1* response seen at 40 µg) [S08-A]; one dose vs prime-boost (a day-14 boost took anti-H1N1 IgG GMT from 7,305 to 15,651, still 38% of young) [S03-A, S13-I].
- **Endpoints we need to see:** at ≤ 10 µg, HAI GMT ≥ 4-fold over unadjuvanted vaccine and at least equal to both injected comparators; heterosubtypic survival ≥ 75%; cross-reactive IFN-γ⁺ CD8 T cells at least the level seen today (6.4% vs 1.5%) [S05-F]; post-dose weight loss ≤ 5% mean and no animal > 10% (today 3.6%, worst 5.8%) [S08-D].
- **Stop or re-scope if:** efficacy is lost below 20 µg while tolerability signals appear at 20 µg, or the benefit disappears with split/recombinant antigen.

### Study 3 — Safety and manganese exposure (3a at Gate 1, 3b at Gate 2)
- **Must establish:** that intranasal Mn²⁺ plus a STING agonist does not accumulate in or inflame the brain, and that lung inflammation resolves in aged animals.
- **Design essentials:** aged and young, both sexes; single dose (3a) and three doses (3b) at 1× and the highest feasible multiple; comparators saline, empty liposome, equimolar MnCl₂, cholera toxin.
- **Endpoints we need to see:**
    - Mn per dose measured and reported (*new*); brain and olfactory-bulb Mn by ICP-MS not above vehicle at days 1, 7, 28 (*new*).
    - CNS *Tnf*, *Ifnb1*, *Isg15* with upper 95% bound < 1.5× PBS at 6 h, 36 h, 72 h and day 7, n ≥ 10 (today: *Tnf* 1.59× PBS, difference 0.59, 95% CI 0.00 to 1.19; the n = 5 design could only detect ≥ 1.6–1.8-fold) [S10-A; T08d]; olfactory epithelium and facial-nerve histology clean (*new*).
    - Lung *Tnf* and *Il6* back to ≤ 2× baseline by day 7 (today 8.4× and 7.2× at 72 h) [S09-A]; lavage neutrophils and lung histopathology at days 1, 3, 7, 28 (*new* — our only neutrophil table, S11-B, is unusable).
- **Stop if:** dose-related Mn accumulation in brain, or neuro-inflammatory or unresolved lung pathology at ≤ 3× the efficacious dose.

### Study 4 — Human translation in vitro (Gate 1)
- **Must establish:** that CDN-1807 activates the common human STING variants and that Mn²⁺ lifts the response in cells from older donors. We have no human data of any kind.
- **Endpoints we need to see:** IFN-β/CXCL10 potency within 10-fold across the common STING alleles; ≥ 2-fold Mn-dependent increase in monocytes/macrophages from donors ≥ 65 years (mouse lung: 2.2-fold) [S01-A]; GM-CSF induction reproduced (mouse: 8.5× vs 1.6×) [S02-F].
- **Stop if:** inactive on a common allele, or no Mn effect in aged human cells.

### Study 5 — Where the dose has to land (Gate 2)
- **Must establish:** whether upper-airway deposition is enough. Our mechanism data are all alveolar (alveolar macrophages, alveolar epithelium) [S01-B, S01-C]; a human nasal spray does not reach the alveolus. This decides device, safety population and TAM.
- **Endpoints we need to see:** HAI ≥ 4-fold and survival ≥ 75% with nose-restricted dosing; if only deep-lung dosing works, an explicit go/no-go on an inhaled product.

### Study 6 — Second species (starts after Gate 1)
- **Must establish:** immunogenicity and protection outside the mouse, ideally in older, pre-immune ferrets with a clinical-format antigen.
- **Endpoints we need to see:** ≥ 4-fold HAI rise in ≥ 80% of animals; ≥ 1.5 log₁₀ lower nasal-wash virus than unadjuvanted vaccine; no neurological or respiratory adverse signs (all *new*).

**In parallel (CMC):** three consecutive lots within ± 20% for size, encapsulation (today 54.8%) and *Ifnb1* potency; Mn content and release specified; ≥ 6 months stability at 2–8 °C; compatibility with the partner antigen.

---

## 3. How the asset looks

| Dimension | What our data show | Verdict |
|---|---|---|
| **Protection in aged hosts** | PSLN-344 beat vaccine + empty liposome in all 11 aged-host experiments (exact log-rank p ≤ 0.003 in each) and beat PSLN-212 in 10 of 11 (the exception, Swiss Webster, p = 0.086) [T03]. Pooled, challenge 2–14 d after dosing: 42/45 vs 8/45 vs 1/45 [T04; Figures 1 and A1]. | Strong signal; each experiment is n = 7–10, no replicate runs in the dataset, females only |
| **Breadth** | H3N2 vaccine → H1N1 challenge and H1N1+H3N2 vaccine → rgH5N1 challenge: 25/28 vs 5/28 [S06-A–D]. Wild-type H5N1 two days after an rgH5N1 vaccine dose: 10/10 vs 1/10 sham [S03-J]. Two other aged strains: 12/14 vs 0/14 [S15-L, S15-N]. 14-month mice with or without prior PR8 infection: 24/28 vs 4/28 [S06-E/F rows 71–105]. | Strong; challenge virus for S15-L/N is not stated, and their weight tables re-use BALB/c trajectories (Appendix A, #16) |
| **Speed** | Challenge on day 3: 12/14 vs 2/14 [S06-B, S06-D]; day 2: 10/10 [S03-J]. Not a non-specific innate effect: adjuvant alone 0/7 [S15-H]. | Strong; S06-D conflicts with its weight table (5/7 rather than 7/7) |
| **Durability** | Challenge on day 60: 14/21 (67%) vs 1/21 and 0/21 [S06-E–G]. Young benchmark 21/21 (p = 0.005). Age-matched mice that were **not challenged** lost 4/21 animals over the same 14 days [same blocks], so waning and old-age attrition cannot be separated (PSLN-344 vs unchallenged: p = 0.48). | Moderate; nothing beyond day 60 in aged animals |
| **Immune restoration** | Across 38 immune read-outs, aged + PSLN-344 reached a median 70% of the young benchmark (range 29–98%); aged + PSLN-212 reached 20%. PSLN-344 > PSLN-212 in 36 of 38 (exact Mann-Whitney p < 0.05) [T07; Figure A3]. HAI GMT 368 vs 46 (H1N1) and 320 vs 35 (H3N2) [S03-C, S03-G]. | Strong, but partial: DC co-stimulation only 29–38% of young [S02-D] |
| **Differentiation** | Confined to aged hosts. In young mice PSLN-344 and PSLN-212 both gave 8/8 survival in three challenge models [S09-B/D/F], and downstream DC read-outs did not differ (ratios 0.95–1.26, 0 of 7 significant), although Mn still raised *Ifnb1* 1.34-fold [T09b]. In the one 180-day study all young mice survived in both groups, but the PSLN-344 group regained weight more slowly (day 14: 95.6% vs 99.2% of baseline, p = 0.004) [S09-G; T09c; weight tables carry the caveats in Appendix A, #15–16]. | Clear niche, narrow label; no long-term advantage in young hosts |
| **Attribution to our molecule** | No Mn-only liposome, no free CDN-1807, no STING-deficient or STING-inhibited arm exists (the Mn content of the empty-liposome sham is not stated). IFNAR-dependence is shown [S02-H]; STING-dependence is not. In the same Mn-free liposome CDN-1807 induced 17× *Ifnb1* against 7.7× for cGAMP [S01-A]. | **Open — the largest scientific gap** |
| **Tolerability** | Post-dose weight loss 3.6% (worst animal 5.8%) vs 1.8% for vaccine alone, recovered by day 10 [S08-D; T08a]. Lung *Tnf* and *Il6* still 8.4× and 7.2× baseline at 72 h in aged mice, against 0.48× and 3.1× in young mice [S09-A, n = 3, panel mislabelled 16 h; T08b]. Lung monocytes were still 18.4% on day 8 (baseline 9.2%; young mice 14.1%, p = 0.006) [S01-D]. CNS *Tnf* 1.59× PBS (p = 0.05 unadjusted; cholera-toxin control 3.5×), n = 5, one time-point [S10-A; T08d; Figure A2]. | **Thin.** No histopathology, no Mn exposure data, no repeat dose, no second species |
| **Dose** | *Ifnb1* Emax 53× (PSLN-212: 16×) with similar ED50 (~11 µg) [S08-A; T08e]. Every efficacy study used 20 µg, which gives 91% of the 40 µg response. | No therapeutic window defined |
| **Formulation** | Encapsulation 54.8 ± 5.1% (three preparations) [S08-B]. Mn content per dose is not reported anywhere. Stored lyophilised at −20 °C. | Early |
| **Data quality** | 22 logged issues (Appendix A), including rotated column headers in S03-B/F, 35 of 100 identical values between two different cell populations [S11-A/B], and 25 re-used body-weight trajectories across "different" experiments [T01f]. | **Audit before relying on any single number** |

---

## 4. Target demographic (for the TAM check)

**Primary: adults aged 65 and over receiving an annual seasonal influenza vaccine.** The product is the adjuvant co-administered with an inactivated influenza vaccine, one dose per season, needle-free. One dose per season is an assumption: in aged mice protection was tested to day 60 only (14/21); young mice were still protected at day 180 (8/8) [S06-E–G, S09-F].

| Segment | Basis in our data | Caveat for sizing |
|---|---|---|
| **Core: ≥ 65 years, annual flu vaccination** | All differentiation is in ≥ 20-month mice: survival 42/45 vs 8/45; HAI 8.0–9.2-fold over the Mn-free form [T04, T07] | 20-month mice correspond roughly to humans in their 60s (external equivalence); nothing older was tested, so the ≥ 75/frail sub-segment is an extrapolation |
| **Expansion: 50–64 years** | In 14-month mice PSLN-212 already failed (0/7, 0/7) and PSLN-344 protected (6/7, 6/7), including animals with prior influenza infection (6/7 vs 0/7) [S06-E/F rows 71–105] | Two experiments, n = 7; 14-month mice are nearer to humans in their late 40s (external equivalence) |
| **Outbreak and pandemic use in older adults** (care-home outbreaks; H5 preparedness procurement) | Protection when challenged 2–3 days after one dose (12/14; 10/10 against wild-type H5N1) and seasonal vaccine → rgH5N1 cross-protection [S06-B/D, S03-J, S06-C/F] | Procurement-driven, not an annual market |
| **Not supported: children and adults under 50** | No advantage over the Mn-free form or over cGAMP liposomes in young mice (8/8 vs 8/8; 7/7 vs 7/7) [S09-B/D/F, S13-E] | Exclude from TAM |

The dataset gives no basis for an oncology population. Filters market research should apply: (i) both sexes are assumed, but only females were tested; (ii) if Study 5 shows deep-lung delivery is required, people with chronic lung disease may be excluded and the product is an inhaler, not a nasal spray; (iii) PSLN-344 has no value without an antigen, so the commercial unit is a combination or a partnered supply, not a stand-alone drug; (iv) the relevant comparators are the enhanced injectable vaccines already recommended for this age group, against which we have no data. A sizing chain that matches the evidence: people ≥ 65 vaccinated against influenza each year → minus exclusions under (ii) → share reachable by a needle-free enhanced vaccine → price benchmarked to enhanced injectables → our share under a partnered model.

---

## 5. Mechanism of action, from our data

In aged lungs the Mn-free formulation triggers too little type-I interferon and almost no GM-CSF; recruited monocytes appear to become inflammatory macrophages rather than dendritic cells, regulatory T cells stay high, and priming fails. Adding Mn²⁺ restores both signals, and the rest of the cascade follows (Figure 2).

![Figure 2](figures/fig2_moa_map.png)

In the table below, pairs of numbers are aged + PSLN-344 vs aged + PSLN-212 unless stated. P-values are Welch t-tests on 3–5 animals per group and should be read as indicative [T06].

| Link | Evidence | Type | Strength |
|---|---|---|---|
| Liposome is taken up by alveolar macrophages via SP-A/SP-D | DiD⁺ macrophages 43% in wild-type vs 13% in *Sftpa1/Sftpd*-null (p < 0.0001) [S01-C, n = 4, young] | Genetic | Good for the vehicle; not shown in aged lung or for the Mn form |
| Cargo reaches alveolar epithelium | Type II cells 15.8% vs 0.4% with free dye [S01-B] | Tracer | Good; the Mn-form comparison [S08-C] is unusable |
| Mn restores the interferon trigger | *Ifnb1* 37× vs 17× (p < 0.0001); young benchmark 37× [S01-A] | Comparative | Good |
| Mn switches on GM-CSF | *Gm-csf* 6.0×, 8.5×, 3.6× at 16, 36, 72 h vs ≤ 1.6× (36 h: p < 0.0001) [S02-F] | Comparative | Good; no young comparator, source cell unknown |
| Monocytes arrive via CCR2 | CCR2 antagonist: monocytes 9.9% → 3.3% (p = 0.001) [S07-B] | Pharmacological | Good |
| Interferon and GM-CSF together make monocyte-derived DCs | *Ifnar*-null marrow 2.1% vs wild-type 19.7% (p = 0.0004); GM-CSF rescues to 12.4% (p = 0.003) [S02-H]. GM-CSF lifts PSLN-212 from 5.9% to 13.8%, but does little alone (1.5%) [S02-G] | Genetic + add-back | Good for sufficiency; necessity of GM-CSF not tested |
| DCs migrate, carry antigen, cross-prime | CCR7⁺ DC 30.7% vs 7.3%; antigen⁺ DC in node 7.1% vs 1.8%; cross-priming 18.7% vs 0.8% [S02-A, S02-C, S02-E] | Comparative + PTX | Good |
| Regulatory brake is released | Follicular regulatory T 10.8% vs 26.7% at day 7 (p = 0.005); no longer different at day 30 (14.0% vs 18.0%, p = 0.11) [S04-B, S04-C] | Comparative | Moderate; transient |
| Antibody and CD8 responses recover | Germinal-centre B 6.5% vs 2.3%; IgG2a:IgG1 2.1 vs 0.6; cross-reactive IFN-γ⁺ CD8 6.4% vs 1.5%; lung resident-memory CD8 4.0% vs 1.0% [S03-K, S13-A/B, S05-F, S05-I] | Comparative | Good |
| **That STING is the receptor** | — | Not tested | **Gap** |
| **That CDN-1807, not Mn alone, is required** | — | Not tested | **Gap** |
| **Which effector protects** | No depletion or transfer experiment; no virus titres; no IgA | Not tested | **Gap** |

One correction matters here. Read as printed, S03-B says PSLN-344 gives an IgG2a:IgG1 ratio of 0.6, i.e. a type-2-skewed response. Recomputing the ratio from the subclass titres in S13-A and S13-B gives 2.1 for PSLN-344, close to the young benchmark (3.0): the S03-B headers are rotated by one column. The S13 titres rank the groups in the same order as total IgG in S03-A, so the error is most likely in S03-B [T01a].

---

## 6. Biomarkers to validate efficacy

None of these is a validated correlate yet: every association below is between groups of different animals. Study 1 measures them and the challenge outcome in the same animals so that they can be tested properly. Figure A3 (Appendix B) shows how far each read-out moves towards the young level.

| Use | Biomarker | PSLN-344 vs PSLN-212 in aged mice | When | Human read-out |
|---|---|---|---|---|
| Target engagement | *Ifnb1* / interferon signature | 37× vs 17× [S01-A] | 16 h | Blood interferon-gene score, CXCL10; nasal-lining-fluid IFN-β |
| Target engagement (age-specific) | GM-CSF | 8.5× vs 1.6× [S02-F] | 16–36 h | GM-CSF in nasal lining fluid or sputum |
| Early cellular response | CD11b⁺ DC; CCR7⁺ migratory DC | 18.9% vs 8.3%; 30.7% vs 7.3% [S01-E, S02-A] | Day 3–4 | Activated monocytes/DC in blood or nasal curettage |
| Early adaptive response | ICOS⁺ Tfh; Tfh:Tfr ratio | 10.3% vs 3.8% [S04-A]; Tfr 10.8% vs 26.7% [S04-B] | Day 7 | Circulating Tfh and plasmablasts at day 7 |
| **Primary immunogenicity** | HAI titre | GMT 368 vs 46; 320 vs 35 [S03-C, S03-G] | Day 14 | HAI seroconversion and GMT ratio (the conventional regulatory read-out for influenza vaccines) |
| Supporting immunogenicity | Neutralising titre; IgG2a:IgG1 | 3,840 vs 418 [S03-D]; 2.1 vs 0.6 [S13-A/B] | Day 14 | Microneutralisation; IgG subclass |
| Breadth | Cross-reactive IFN-γ⁺ CD8; lung resident-memory CD8 | 6.4% vs 1.5% [S05-F]; 4.0% vs 1.0% [S05-I] | Day 14–60 | IFN-γ ELISpot to conserved antigens |
| Tolerability | Lung *Tnf*, *Il6* at 72 h; CNS *Tnf*; body weight | 8.4× and 7.2× [S09-A]; 1.59× [S10-A]; −3.6% [S08-D] | 36 h – day 7 | Reactogenicity, serum IL-6/TNF, olfactory testing |
| **Missing, add now** | Mucosal IgA; virus titre after challenge; Mn in brain | not measured | — | Nasal IgA; viral shedding |

---

## 7. If we drop it: what we give up, and why we might

**What we give up**

- The only formulation in our dataset that reliably protects aged animals: 42/45 survivors vs 8/45 for our own Mn-free version and 1/45 for vaccine + empty liposome [T04], with surviving animals still losing about 11% of body weight (protection from death, not from illness) [T09a].
- Single-dose, needle-free protection that starts within 2–3 days (12/14) and is still present at day 60 (14/21) [S06-B/D, S06-E–G].
- Protection across subtypes, including seasonal vaccine → H5N1 (7/7, 7/7, 5/7) and wild-type H5N1 (10/10) [S06-C/D/F, S03-J].
- An age-specific mechanism (restored interferon + GM-CSF → monocyte-derived DCs) that returns immune read-outs from 20% to 70% of the young level [T07] and could, in principle, be carried to other vaccines for older adults. That last step is untested: the only non-influenza antigen used was ovalbumin [S02-C, S02-E].

**Why dropping could still be the right call**

- Every result is from mice, n = 7–10, with no replicate runs in the dataset, females only, and the supporting workbook fails basic consistency checks (Appendix A).
- We cannot show the benefit comes from our STING agonist rather than from manganese.
- Intranasal manganese and intranasal adjuvants both carry known class safety concerns (external knowledge, not our data), and our safety package is one weight curve and a handful of transcripts.
- The value sits only in older adults, needs a partner antigen, and would be judged against enhanced injectable vaccines we have never tested against.

**What I would tell the committee:** dropping now forfeits a large, age-specific effect before we know whether it is real, ours and safe. Roughly a year of gated work answers all three. Dropping is the right call if Gate 0 fails, or if the portfolio has no route to a vaccine partner.

---

## 8. What I considered and ruled out

| Considered | Outcome | Why |
|---|---|---|
| Positioning as a stand-alone STING agonist (antiviral or oncology) | Ruled out | Adjuvant alone 0/7 [S15-H]; no tumour data exist |
| Leading with PSLN-212 (no Mn) | Ruled out for older adults | 8/45 survival; 20% of young immune response [T04, T07]. If the committee defines the asset as PSLN-212 rather than PSLN-344, my recommendation for this population would be to drop it |
| Giving more of the Mn-free PSLN-212 | Ruled out | Its *Ifnb1* response plateaus at 15× at 40 µg, below PSLN-344 at 10 µg (21×) [S08-A] |
| CMP-204 (cGAMP in the same liposome) | Ruled out | *Ifnb1* 7.7× vs 37×; 3/7 survival in aged mice [S01-A, S03-I] |
| Adding the TLR7/8 agonist R848 | Ruled out | PSLN-212/R848: 10.0% mean weight loss, 4 of 5 animals ≥ 10%, one animal not recorded at day 10, lung *Tnf* 50× and *Il10* 45× still at 72 h, and lower *Ifnb1* than PSLN-344 (24× vs 37×) [S08-D, S09-A, S01-A] |
| Replacing Mn with co-delivered GM-CSF | Held in reserve | Recombinant GM-CSF lifted monocyte-derived DCs with PSLN-212 from 5.9% to 13.8% [S02-G], but there are no antibody or survival data; worth one arm if Study 3 raises a manganese concern |
| A young-adult or paediatric label | Ruled out | No advantage in young hosts [S09-B/D/F, S13-E] |
| Advancing straight to IND-enabling work | Ruled out | Data not decision-grade; no toxicology; no attribution controls |
| Partnering or out-licensing now | Ruled out for now | With open data-integrity questions and no attribution or safety data the package would be valued low; Gate 1 is the earliest sensible point |
| Dropping now | Ruled out for now | Effect size and consistency (Section 3) against a staged programme that can be stopped at each gate |
| Early protection is a non-specific innate antiviral state | Ruled out | Adjuvant alone 0/7, vaccine alone 0/7, together 6/7 [S15-H] |
| Day-60 deaths mean the response wanes | Cannot tell | Unchallenged aged controls died at 19% (4/21; 95% CI 5–42%) over the same window [S06-E–G] |
| Using the "Untreated" groups as challenge controls | Ruled out | The annotation states they received no virus; they measure old-age attrition |
| Mn improves delivery to epithelium | Cannot tell | S08-C contradicts S01-B for the same measurement (13.8% vs 3.8% for type I cells) |
| Using S03-B/F, S11-A/B, S07-C, S08 rows 89–101, S05-A/B as printed | Excluded | Rotated headers; duplicated values; duplicate labels; no labels; n = 2 with contradictory conditions (Appendix A) |
| Body-weight curves as primary efficacy evidence | Excluded | Carried-forward values for dead animals and re-used trajectories [T01d, T01f] |
| Claims of sterilising immunity, mucosal IgA, durability beyond day 60, efficacy in males or the very old, or efficacy with split/recombinant antigen | Not made | Not measured |

---

## Appendix A — Data-integrity log

Survival tables were used as the primary efficacy record because they are complete and the paired weight tables agree with them on the number of deaths in 51 of 65 group comparisons (10 disagree, 4 are ambiguous). Resolving every conflict against PSLN-344 moves the pooled result from 42/45 vs 8/45 to 40/45 vs 12/45 (p < 0.0001) [T04c]. The conclusion holds; the individual numbers need the audit. Figure 3, after the table, shows four of the findings.

| # | Where | Finding | Handling |
|---|---|---|---|
| 1 | S03-B, S03-F | Column headers rotated by one position relative to the subclass titres in S13-A–D (Figure 3a); as printed PSLN-344 looks type-2-skewed (0.6), recomputed it is 2.1 [T01a] | Recomputed values used |
| 2 | S09-A, columns X–AS | Labelled 16 h, but all 21 *Ifnb1* values equal the 72 h panel of S01-A [T01b] | Treated as 72 h |
| 3 | S09-A vs S01-A | The same control values are labelled "PBS" in one block and "Sham" in the other | Noted |
| 4 | S11-A, S11-B | 35 of 100 values identical in the same cell position, for alveolar macrophages and neutrophils [T01c] | Both excluded |
| 5 | S07-C | Both groups carry the same label | Excluded |
| 6 | S08 rows 89–101 | Thirteen unlabelled time-to-event rows | Excluded |
| 7 | S08-C vs S01-B | Type I epithelial uptake of the same particle 13.8% vs 3.8%; column 2 of S08-C matches S01-B's type I values, suggesting transposed headers | Excluded |
| 8 | S08-A | Group "PSLN-344/R848" is not in the materials list | Not used |
| 9 | S03-J, S13-E, S05-A/B, S09-F | Stated n differs from observations (9 vs 10; 5 vs 7; 3 vs 2; 8 vs 7 in sham; the annotation attributes the last to S09-B) | Analysed as found; S05-A/B not used |
| 10 | S03-J, cell J46 | A PSLN-344 animal has a survival flag but no day | Counted as survivor; omitted from log-rank |
| 11 | S06 | Labels S06-E and S06-F are each used for two different experiments | Separated by row range |
| 12 | S03-I vs S13-F; S03-J vs S13-G | Paired survival and weight blocks list different groups; death patterns indicate shifted labels (aged PSLN-212: 0/7 survivors in S03-I, 3/7 in S13-F) | Survival table used; sensitivity analysis |
| 13 | Survival vs weight tables | Number of deaths disagrees in 10 of 65 group comparisons, e.g. PSLN-344 in S06-D (7/7 vs 5/7), S06-E (5/7 vs 6/7), S06-G (4/7 vs 5–7/7) [T01d] | Sensitivity analysis [T04c] |
| 14 | S06-C vs S06-D | Identical time-to-event vectors for Sham and PSLN-212 in two different experiments | Flagged |
| 15 | Weight tables | Dead animals are blank in some groups and carried forward in others | Carried-forward values removed before summarising |
| 16 | Weight tables | 25 animal trajectories recur in a different experiment, identical or shifted by whole numbers (9 pairs of experiment arms, e.g. all seven PSLN-344 animals of S15-C reappear in S15-I); 173 of 268 high-precision values share their decimal part with a value in another block; one row of S09-C is duplicated between groups [T01f, T01g] | Weight data treated as supporting only |
| 17 | S05-A, S05-B, S05-I | Conditions name both ovalbumin and influenza vaccine; the NP tetramer used requires a strain that is not stated; n = 2 in S05-A/B. S05-I refers to the same conditions | S05-A/B not used; S05-I used, antigen uncertain |
| 18 | Several | Not stated: challenge virus and interval for S15-L/N; interval for S06-E rows 71–105; time-points for S11-E, S13-H, S14-A; adjuvant and age of the pertussis-toxin arm; age in S03-J; whether "20 µg" refers to CDN or total particle; Mn content; instillation volume | Flagged for Gate 0 |
| 19 | S08-B | Encapsulation is stated as CDN-1807 absorbance but reported for two preparations that contain no CDN-1807 | Noted |
| 20 | S03-C, S03-G | HAI values of 0 are below the lowest dilution tested (1:10) | Set to 5 for geometric means |
| 21 | Annotation vs workbook | Annotation says PSLN-212 observations decline in S13-F; the workbook carries values forward | Noted |
| 22 | All sheets | Last digits are far from evenly spread: 2, 3 and 5 are over-represented among the 711 two-decimal immunology values (χ² = 149, 9 d.f.) and the 2,410 one-decimal body weights (χ² = 422); instrument read-outs normally give even last digits, so the tables look hand-entered or transcribed [T01h] | Reconcile against instrument exports at Gate 0 |

![Figure 3](figures/fig3_data_integrity.png)

---

## Appendix B — Supporting figures and tables

![Figure A1](figures/figA1_km_grid.png)

**Survival by experiment (survivors / animals, as printed)**

| Block | Host | Vaccine → challenge (day after dose) | Sham | PSLN-212 | PSLN-344 | Young + 212 | Other |
|---|---|---|---|---|---|---|---|
| S03-I | Aged BALB/c | H1N1+H3N2 → CA09 H1N1, 10× LD50 (d14) | 0/7 | 0/7 | **7/7** | 7/7 | CMP-204 3/7 |
| S03-J | BALB/c, age not stated | rgH5N1 → wild-type H5N1 (d2), 22-day follow-up | 1/10 | 3/10 | **10/10** | — | — |
| S06-A | Aged BALB/c | H3N2 → PR8 H1N1, 5× LD50 (d14) | 0/7 | 1/7 | **6/7** | 7/7 | — |
| S06-B | Aged BALB/c | H3N2 → PR8 H1N1 (d3) | 0/7 | 0/7 | **5/7** | 7/7 | — |
| S06-C | Aged BALB/c | H1N1+H3N2 → rgH5N1 (d14) | 0/7 | 2/7 | **7/7** | 7/7 | — |
| S06-D | Aged BALB/c | H1N1+H3N2 → rgH5N1 (d3) | 0/7 | 2/7 | **7/7** | 7/7 | — |
| S06-E | Aged BALB/c | H3N2 → PR8 H1N1 (d60) | 0/7 | 0/7 | **5/7** | 7/7 | unchallenged 6/7 |
| S06-F | Aged BALB/c | H1N1+H3N2 → rgH5N1 (d60) | 0/7 | 1/7 | **5/7** | 7/7 | unchallenged 7/7 |
| S06-G | Aged BALB/c | H1N1 → Perth H3N2 (d60) | 0/7 | 0/7 | **4/7** | 7/7 | unchallenged 4/7 |
| S15-L | Aged C57BL/6 | H1N1+H3N2 → not stated | 0/7 | 0/7 | **6/7** | 6/7 | — |
| S15-N | Aged Swiss Webster | H1N1+H3N2 → not stated | 0/7 | 2/7 | **6/7** | 7/7 | — |
| S15-H | Aged BALB/c | H1N1+H3N2 or none → rgH5N1 (d3) | — | — | **6/7** | — | vaccine alone 0/7; PSLN-344 alone 0/7 |
| S06-E (rows 71–105) | 14-month BALB/c | H1N1+H3N2 → PR8 H1N1; naive / PR8-imprinted | — | 0/7 / 4/7 | **6/7 / 6/7** | — | — |
| S06-F (rows 71–105) | 14-month BALB/c | H1N1+H3N2 → Perth H3N2 (d14); naive / PR8-imprinted | — | 0/7 / 0/7 | **6/7 / 6/7** | — | — |
| S09-B | Young BALB/c | H3N2 → PR8 H1N1 (d21) | 0/8 | — | — | 8/8 | young + PSLN-344 8/8 |
| S09-D | Young BALB/c | H1N1 → Perth H3N2 (d21) | 0/8 | — | — | 8/8 | young + PSLN-344 8/8 |
| S09-F | Young BALB/c | H1N1+H3N2 → rgH5N1 (d180) | 0/7 | — | — | 8/8 | young + PSLN-344 8/8 |
| S13-E | Young BALB/c | H1N1+H3N2 → CA09 H1N1, 10× LD50 (d14) | 1/7 | — | — | — | young + PSLN-344 7/7; young + CMP-204 7/7; naive 0/7 |

![Figure A2](figures/figA2_safety_dose.png)

![Figure A3](figures/figA3_restoration_cascade.png)

---

## Appendix C — Methods, assumptions and file index

- **Traceability:** every statistic was recomputed from the per-animal values; each number quoted in this document is listed with its source block and analysis in `T10_numbers_cited.csv`, and the headline numbers were re-derived independently from the raw cells [`12_independent_check.py`].
- **Event coding:** in time-to-event blocks the group column holds 1 or 0 (annotation, sheet S06); 1 is read as death and 0 as alive at the end of observation, because every 0 sits on the last observation day.
- **Survival:** log-rank (the stated method), with exact permutation p-values and Fisher's exact test because arms are 7–10 animals; exact 95% confidence intervals; pooled analyses stratified by experiment [`04_survival.py`].
- **Titres and qPCR** were analysed on the log scale and summarised as geometric means; percentages and counts on the linear scale. One-way ANOVA with Tukey's test is reported as the stated method, with Welch t and exact Mann-Whitney tests as checks [`05_endpoints.py`]. With n = 5 per group the smallest possible exact two-sided p is 0.008.
- **"% of young benchmark"** is the ratio of the aged-group mean (geometric mean for titres) to the young + PSLN-212 mean in the same block, with a bootstrap 95% interval [`05b_curated_restoration.py`].
- **External context** (not from our data, to be verified by the team): the class safety history of intranasal adjuvants and inhaled manganese; Mn²⁺ as a sensitiser of the cGAS–STING pathway; the existence of enhanced injectable influenza vaccines for older adults; mouse-to-human age equivalence.
- **Not assessed:** intellectual property, cost of goods, market size, regulatory strategy.

| File | Content |
|---|---|
| `analysis/run_all.sh` | Rebuilds every table, figure and this document from the workbook (scripts `01` to `14`) |
| `analysis/parsed/` | Every numeric cell of the workbook in long format, with its cell address |
| `analysis/tables/T00`, `T01a–g` | Block inventory; evidence for each data-integrity finding |
| `analysis/tables/T02–T04c` | Survival by group, contrasts, pooled and sensitivity analyses |
| `analysis/tables/T05–T07` | Descriptives, contrasts and restoration index for every immune read-out |
| `analysis/tables/T08a–e`, `T09a–b` | Tolerability, cytokines, CNS, dose-response, morbidity, young-host comparison |
| `analysis/tables/T10_numbers_cited.csv` | Every number in this document with its source block and analysis |
| `analysis/tables/T11_power.csv` | Sample-size calculations for Study 1 |
