# PSLN-344 — portfolio review: recommendation and next-step proposal

*Prepared 1 Nov 2026 from `psln_program_dataset.xlsx` (last saved 3 Sep 2026) and `psln_program_annotation.pdf` (15 Sep 2026). Codes in square brackets, e.g. [S06-A], are workbook blocks; "T" numbers are analysis tables in `analysis/tables/`. "Aged" = mice ≥ 20 months; "young benchmark" = 7–8-week-old mice given the same vaccine with PSLN-212. The asset is taken to be PSLN-344 (CDN-1807 + Mn²⁺ in the surfactant-mimetic liposome).*

---

## 1. Recommendation

**Keep PSLN-344 — conditionally. Hold it at its current stage and run a gated de-risking package of roughly 12 months. Authorise only the data audit (Gate 0) now, release each later tranche when the preceding gate is passed, and make no IND-enabling commitment before the last gate (Gate 2, about month 12).**

**How it looks in one line:** a large, age-specific efficacy signal in mice, resting on a data package that is not yet decision-grade and on three things nobody has tested: that the effect comes from our molecule, that it is safe, and that it translates.

Three things the committee should know before the detail:

1. **What the asset is, on our own data: an intranasal vaccine adjuvant for aged hosts, not a stand-alone STING drug.** Given without antigen it protected {{h_adj}} animals; vaccine alone protected {{h_vac}}; the two together protected {{h_combo}} [S15-H; T02]. There is no oncology experiment anywhere in the dataset.
2. **The efficacy signal is large and consistent.** After one intranasal dose and a lethal influenza challenge 2–14 days later, {{early_344}} aged mice survived with PSLN-344 ({{early_344_pct}}%, 95% CI {{early_344_ci}}%), against {{early_sham}} with vaccine + empty liposome and {{early_212}} with our Mn-free formulation PSLN-212 (six experiments of 7–10 animals per arm, none repeated; stratified log-rank p {{early_p_212}} vs PSLN-212) [S03-I, S03-J, S06-A–D; T04]. Without S03-J, the one block that does not state animal age, the counts are {{noJ_344}}, {{noJ_sham}} and {{noJ_212}}.
3. **The package is not yet decision-grade.** The workbook has labelling errors that reverse at least one conclusion if read as printed, duplicated values, and body-weight tables that disagree with the survival tables in {{iv_dis}} of {{iv_total}} group comparisons (Appendix A). The headline survives a worst-case reading of every conflict ({{worst_344}} vs {{worst_212}}), but individual numbers may move. The controls that would tie the effect to *our* STING agonist (Mn-only, STING-deficient) were never run, and safety rests on one body-weight curve and a handful of lung and brain transcripts.

The asset is worth keeping because the effect is large, it is specific to aged hosts (where our Mn-free formulation fails), and the open questions can be answered with a handful of mouse and in-vitro studies. It does not justify more than gated spend until they are answered.

![Figure 1](figures/fig1_survival_overview.png)

| Gate | Question | Pass | Fail → |
|---|---|---|---|
| **0** (≈ 6 weeks, no animals) | Do the pivotal numbers survive reconciliation with raw records? | Every pivotal survival and serology block re-derived from source; Appendix A items closed | Stop |
| **1** (≈ month 7) | Does it replicate blinded, is it our molecule, and is it acceptably safe at first look? | Studies 1, 3a, 4 below | Stop or re-scope |
| **2** (≈ month 12) | Is there a dose window, does it work with a clinical-format antigen by a deliverable route, and in a second species? | Studies 2, 3b, 5, 6 below | Stop, partner or re-scope |

Timings are planning assumptions, not data. They assume ≥ 20-month mice of both sexes are on hand; Study 1 alone needs {{n_aged_arms}}.

---

## 2. Next steps: what each study must establish and the endpoints we need to see

Thresholds are anchored to what we observed; where we have no data the threshold is a conventional one and is marked *new*.

### Gate 0 — Data audit (before any new spend)
- **Must establish:** that the survival, serology and T-cell tables match raw records (animal IDs, cage cards, balance and plate-reader exports, FCS files), and why weight trajectories recur across experiments.
- **Endpoints:** corrected, animal-level workbook; each Appendix A item closed with evidence; pivotal results ([S03-I/J], [S06-A–G], [S15-H/L/N], [S03-A–H], [S13-A–D]) re-derived independently.
- **Stop if:** pivotal survival tables cannot be traced to source, or the re-derived PSLN-344 vs PSLN-212 difference in aged mice is no longer significant.

### Study 1 — Blinded replication with the missing controls (Gate 1)
- **Must establish:** (a) the aged-host benefit replicates under randomisation and blinding in both sexes; (b) it needs CDN-1807 and Mn together in the particle; (c) it runs through STING.
- **Design essentials:** aged (≥ 20 months) mice, heterosubtypic model of [S06-A]; aged C57BL/6 is an option because STING-deficient lines share that background and the effect was seen there ({{s15l_344}} vs {{s15l_sham}}) [S15-L]; arms: empty liposome, PSLN-212, PSLN-344, Mn-only liposome, PSLN-212 + free Mn²⁺, free CDN-1807 + Mn²⁺, young + PSLN-212; 18 per arm (9 F + 9 M; {{n_aged_arms}} aged mice), which gives {{pw18}}% power for 85% vs 30% survival (the n = 7 used so far gives {{pw7}}%) [T11]. Serology and challenge in the same individually identified animals. Target-engagement arm in STING-deficient mice or with a STING antagonist.
- **Endpoints we need to see:**
    - Survival ≥ 75% with PSLN-344 and ≥ 40 points above each of PSLN-212, Mn-only and empty liposome, p < 0.05 each (observed so far: {{early_344_pct}}% vs {{early_212_pct}}% vs {{early_sham_pct}}%; worst-case reading of conflicting tables {{worst_344_pct}}% vs {{worst_212_pct}}%) [T04, T04c].
    - HAI GMT ≥ 4-fold over PSLN-212 and ≥ 50% of the young benchmark (observed {{hai1_fold}}- and {{hai3_fold}}-fold; {{hai1_pct}}% and {{hai3_pct}}%) [S03-C, S03-G].
    - Lung virus titre ≥ 2 log₁₀ below sham 4–5 days after challenge (*new* — no virological read-out exists).
    - Mucosal IgA in nasal wash and lavage above PSLN-212 (*new*).
    - *Ifnb1* induction cut by ≥ 80% and the HAI advantage lost when STING is absent or blocked (*new*).
- **Stop or re-scope if:** survival < 60%; or Mn-only liposome comes within 20 points of PSLN-344 (CDN-1807 is then not contributing); or the effect persists without STING.

### Study 2 — Dose window, clinical-format antigen and head-to-head comparators (Gate 2)
- **Must establish:** the lowest effective dose and the margin to the first tolerability signal; that the benefit holds with a licensed-format split or recombinant antigen (everything so far used in-house formalin-inactivated whole virus); and how it compares with the injected enhanced-vaccine approaches used in older adults (high antigen dose; squalene-emulsion adjuvant). None of these comparators is in our dataset.
- **Design essentials:** aged mice; PSLN-344 at 2.5, 5, 10, 20 µg (5 and 10 µg gave {{pct40_5}}% and {{pct40_10}}% of the *Ifnb1* response seen at 40 µg) [S08-A]; one dose vs prime-boost (a day-14 boost took anti-H1N1 IgG GMT from {{boost1_base}} to {{boost1_344}}, still {{boost1_pct}}% of young) [S03-A, S13-I].
- **Endpoints we need to see:** at ≤ 10 µg, HAI GMT ≥ 4-fold over unadjuvanted vaccine and at least equal to both injected comparators; heterosubtypic survival ≥ 75%; cross-reactive IFN-γ⁺ CD8 T cells at least the level seen today ({{ifng14_344}}% vs {{ifng14_212}}%) [S05-F]; post-dose weight loss ≤ 5% mean and no animal > 10% (today {{wl_344}}%, worst {{wl_344_worst}}%) [S08-D].
- **Stop or re-scope if:** efficacy is lost below 20 µg while tolerability signals appear at 20 µg, or the benefit disappears with split/recombinant antigen.

### Study 3 — Safety and manganese exposure (3a at Gate 1, 3b at Gate 2)
- **Must establish:** that intranasal Mn²⁺ plus a STING agonist does not accumulate in or inflame the brain, and that lung inflammation resolves in aged animals.
- **Design essentials:** aged and young, both sexes; single dose (3a) and three doses (3b) at 1× and the highest feasible multiple; comparators saline, empty liposome, equimolar MnCl₂, cholera toxin.
- **Endpoints we need to see:**
    - Mn per dose measured and reported (*new*); brain and olfactory-bulb Mn by ICP-MS not above vehicle at days 1, 7, 28 (*new*).
    - CNS *Tnf*, *Ifnb1*, *Isg15* with upper 95% bound < 1.5× PBS at 6 h, 36 h, 72 h and day 7, n ≥ 10 (today: *Tnf* {{cns_Tnf}}× PBS, difference {{cns_Tnf_diff}}, 95% CI {{cns_Tnf_ci}}; the n = 5 design could only detect ≥ 1.6–1.8-fold) [S10-A; T08d]; olfactory epithelium and facial-nerve histology clean (*new*).
    - Lung *Tnf* and *Il6* back to ≤ 2× baseline by day 7 (today {{cy72_Tnf_344}}× and {{cy72_Il6_344}}× at 72 h) [S09-A]; lavage neutrophils and lung histopathology at days 1, 3, 7, 28 (*new* — our only neutrophil table, S11-B, is unusable).
- **Stop if:** dose-related Mn accumulation in brain, or neuro-inflammatory or unresolved lung pathology at ≤ 3× the efficacious dose.

### Study 4 — Human translation in vitro (Gate 1)
- **Must establish:** that CDN-1807 activates the common human STING variants and that Mn²⁺ lifts the response in cells from older donors. We have no human data of any kind.
- **Endpoints we need to see:** IFN-β/CXCL10 potency within 10-fold across the common STING alleles; ≥ 2-fold Mn-dependent increase in monocytes/macrophages from donors ≥ 65 years (mouse lung: {{ifn_fold}}-fold) [S01-A]; GM-CSF induction reproduced (mouse: {{gm_344_36h}}× vs {{gm_212_36h}}×) [S02-F].
- **Stop if:** inactive on a common allele, or no Mn effect in aged human cells.

### Study 5 — Where the dose has to land (Gate 2)
- **Must establish:** whether upper-airway deposition is enough. Our mechanism data are all alveolar (alveolar macrophages, alveolar epithelium) [S01-B, S01-C]; a human nasal spray does not reach the alveolus. This decides device, safety population and TAM.
- **Endpoints we need to see:** HAI ≥ 4-fold and survival ≥ 75% with nose-restricted dosing; if only deep-lung dosing works, an explicit go/no-go on an inhaled product.

### Study 6 — Second species (starts after Gate 1)
- **Must establish:** immunogenicity and protection outside the mouse, ideally in older, pre-immune ferrets with a clinical-format antigen.
- **Endpoints we need to see:** ≥ 4-fold HAI rise in ≥ 80% of animals; ≥ 1.5 log₁₀ lower nasal-wash virus than unadjuvanted vaccine; no neurological or respiratory adverse signs (all *new*).

**In parallel (CMC):** three consecutive lots within ± 20% for size, encapsulation (today {{ee_344}}%) and *Ifnb1* potency; Mn content and release specified; ≥ 6 months stability at 2–8 °C; compatibility with the partner antigen.

---

## 3. How the asset looks

| Dimension | What our data show | Verdict |
|---|---|---|
| **Protection in aged hosts** | PSLN-344 beat vaccine + empty liposome in all {{n_expt_sham}} aged-host experiments (exact log-rank p ≤ {{max_p_sham}} in each) and beat PSLN-212 in {{n_expt_212_sig}} of {{n_expt_212}} (the exception, Swiss Webster, p {{p_212_ns}}) [T03]. Pooled, challenge 2–14 d after dosing: {{early_344}} vs {{early_212}} vs {{early_sham}} [T04; Figures 1 and A1]. | Strong signal; each experiment is n = 7–10, no replicate runs in the dataset, females only |
| **Breadth** | H3N2 vaccine → H1N1 challenge and H1N1+H3N2 vaccine → rgH5N1 challenge: {{het_344}} vs {{het_212}} [S06-A–D]. Wild-type H5N1 two days after an rgH5N1 vaccine dose: {{j_344}} vs {{j_sham}} sham [S03-J]. Two other aged strains: {{str_344}} vs {{str_sham}} [S15-L, S15-N]. 14-month mice with or without prior PR8 infection: {{imp_344}} vs {{imp_212}} [S06-E/F rows 71–105]. | Strong; challenge virus for S15-L/N is not stated, and their weight tables re-use BALB/c trajectories (Appendix A, #16) |
| **Speed** | Challenge on day 3: {{d3_344}} vs {{d3_212}} [S06-B, S06-D]; day 2: {{j_344}} [S03-J]. Not a non-specific innate effect: adjuvant alone {{h_adj}} [S15-H]. | Strong; S06-D conflicts with its weight table (5/7 rather than 7/7) |
| **Durability** | Challenge on day 60: {{d60_344}} ({{d60_344_pct}}%) vs {{d60_212}} and {{d60_sham}} [S06-E–G]. Young benchmark {{d60_y}} (p {{d60_p_y}}). Age-matched mice that were **not challenged** lost {{bg_deaths}} animals over the same 14 days [same blocks], so waning and old-age attrition cannot be separated (PSLN-344 vs unchallenged: p {{d60_p_unt}}). | Moderate; nothing beyond day 60 in aged animals |
| **Immune restoration** | Across {{n_endpoints}} immune read-outs, aged + PSLN-344 reached a median {{med_344}}% of the young benchmark (range {{rng_344_lo}}–{{rng_344_hi}}%); aged + PSLN-212 reached {{med_212}}%. PSLN-344 > PSLN-212 in {{n_sig}} of {{n_endpoints}} (exact Mann-Whitney p < 0.05) [T07; Figure A3]. HAI GMT {{hai1_344}} vs {{hai1_212}} (H1N1) and {{hai3_344}} vs {{hai3_212}} (H3N2) [S03-C, S03-G]. | Strong, but partial: DC co-stimulation only {{cd40_pct}}–{{cd86_pct}}% of young [S02-D] |
| **Differentiation** | Confined to aged hosts. In young mice PSLN-344 and PSLN-212 both gave {{yb_344}} survival in three challenge models [S09-B/D/F], and downstream DC read-outs did not differ (ratios {{y_down_lo}}–{{y_down_hi}}, {{y_down_nsig}} of {{y_down_n}} significant), although Mn still raised *Ifnb1* {{y_ifn_ratio}}-fold [T09b]. In the one 180-day study all young mice survived in both groups, but the PSLN-344 group regained weight more slowly (day 14: {{s09g_344}}% vs {{s09g_212}}% of baseline, p {{s09g_p}}) [S09-G; T09c; weight tables carry the caveats in Appendix A, #15–16]. | Clear niche, narrow label; no long-term advantage in young hosts |
| **Attribution to our molecule** | No Mn-only liposome, no free CDN-1807, no STING-deficient or STING-inhibited arm exists (the Mn content of the empty-liposome sham is not stated). IFNAR-dependence is shown [S02-H]; STING-dependence is not. In the same Mn-free liposome CDN-1807 induced {{ifn_212}}× *Ifnb1* against {{ifn_cmp}}× for cGAMP [S01-A]. | **Open — the largest scientific gap** |
| **Tolerability** | Post-dose weight loss {{wl_344}}% (worst animal {{wl_344_worst}}%) vs {{wl_vac}}% for vaccine alone, recovered by day 10 [S08-D; T08a]. Lung *Tnf* and *Il6* still {{cy72_Tnf_344}}× and {{cy72_Il6_344}}× baseline at 72 h in aged mice, against {{cy72_Tnf_y}}× and {{cy72_Il6_y}}× in young mice [S09-A, n = 3, panel mislabelled 16 h; T08b]. Lung monocytes were still {{mono8_344}}% on day 8 (baseline {{mono0_344}}%; young mice {{mono8_y}}%, p {{mono8_p}}) [S01-D]. CNS *Tnf* {{cns_Tnf}}× PBS (p {{cns_Tnf_p2}} unadjusted; cholera-toxin control {{cns_Tnf_ct}}×), n = 5, one time-point [S10-A; T08d; Figure A2]. | **Thin.** No histopathology, no Mn exposure data, no repeat dose, no second species |
| **Dose** | *Ifnb1* Emax {{emax_344}}× (PSLN-212: {{emax_212}}×) with similar ED50 (~{{ed50_344}} µg) [S08-A; T08e]. Every efficacy study used 20 µg, which gives {{pct40_20}}% of the 40 µg response. | No therapeutic window defined |
| **Formulation** | Encapsulation {{ee_344}} ± {{ee_344_sd}}% (three preparations) [S08-B]. Mn content per dose is not reported anywhere. Stored lyophilised at −20 °C. | Early |
| **Data quality** | {{n_dq}} logged issues (Appendix A), including rotated column headers in S03-B/F, {{s11_same}} of {{s11_tot}} identical values between two different cell populations [S11-A/B], and {{traj_pairs}} re-used body-weight trajectories across "different" experiments [T01f]. | **Audit before relying on any single number** |

---

## 4. Target demographic (for the TAM check)

**Primary: adults aged 65 and over receiving an annual seasonal influenza vaccine.** The product is the adjuvant co-administered with an inactivated influenza vaccine, one dose per season, needle-free. One dose per season is an assumption: in aged mice protection was tested to day 60 only ({{d60_344}}); young mice were still protected at day 180 ({{yf_344}}) [S06-E–G, S09-F].

| Segment | Basis in our data | Caveat for sizing |
|---|---|---|
| **Core: ≥ 65 years, annual flu vaccination** | All differentiation is in ≥ 20-month mice: survival {{early_344}} vs {{early_212}}; HAI {{hai1_fold}}–{{hai3_fold}}-fold over the Mn-free form [T04, T07] | 20-month mice correspond roughly to humans in their 60s (external equivalence); nothing older was tested, so the ≥ 75/frail sub-segment is an extrapolation |
| **Expansion: 50–64 years** | In 14-month mice PSLN-212 already failed ({{imp_per_n212}}, {{imp_pr8_n212}}) and PSLN-344 protected ({{imp_per_n344}}, {{imp_pr8_n344}}), including animals with prior influenza infection ({{imp_per_i344}} vs {{imp_per_i212}}) [S06-E/F rows 71–105] | Two experiments, n = 7; 14-month mice are nearer to humans in their late 40s (external equivalence) |
| **Outbreak and pandemic use in older adults** (care-home outbreaks; H5 preparedness procurement) | Protection when challenged 2–3 days after one dose ({{d3_344}}; {{j_344}} against wild-type H5N1) and seasonal vaccine → rgH5N1 cross-protection [S06-B/D, S03-J, S06-C/F] | Procurement-driven, not an annual market |
| **Not supported: children and adults under 50** | No advantage over the Mn-free form or over cGAMP liposomes in young mice ({{yb_344}} vs {{yb_212}}; {{ye_344}} vs {{ye_cmp}}) [S09-B/D/F, S13-E] | Exclude from TAM |

The dataset gives no basis for an oncology population. Filters market research should apply: (i) both sexes are assumed, but only females were tested; (ii) if Study 5 shows deep-lung delivery is required, people with chronic lung disease may be excluded and the product is an inhaler, not a nasal spray; (iii) PSLN-344 has no value without an antigen, so the commercial unit is a combination or a partnered supply, not a stand-alone drug; (iv) the relevant comparators are the enhanced injectable vaccines already recommended for this age group, against which we have no data. A sizing chain that matches the evidence: people ≥ 65 vaccinated against influenza each year → minus exclusions under (ii) → share reachable by a needle-free enhanced vaccine → price benchmarked to enhanced injectables → our share under a partnered model.

---

## 5. Mechanism of action, from our data

In aged lungs the Mn-free formulation triggers too little type-I interferon and almost no GM-CSF; recruited monocytes appear to become inflammatory macrophages rather than dendritic cells, regulatory T cells stay high, and priming fails. Adding Mn²⁺ restores both signals, and the rest of the cascade follows (Figure 2).

![Figure 2](figures/fig2_moa_map.png)

In the table below, pairs of numbers are aged + PSLN-344 vs aged + PSLN-212 unless stated. P-values are Welch t-tests on 3–5 animals per group and should be read as indicative [T06].

| Link | Evidence | Type | Strength |
|---|---|---|---|
| Liposome is taken up by alveolar macrophages via SP-A/SP-D | DiD⁺ macrophages {{am_wt}}% in wild-type vs {{am_ko}}% in *Sftpa1/Sftpd*-null (p {{am_p}}) [S01-C, n = 4, young] | Genetic | Good for the vehicle; not shown in aged lung or for the Mn form |
| Cargo reaches alveolar epithelium | Type II cells {{aec2_np}}% vs {{aec2_free}}% with free dye [S01-B] | Tracer | Good; the Mn-form comparison [S08-C] is unusable |
| Mn restores the interferon trigger | *Ifnb1* {{ifn_344}}× vs {{ifn_212}}× (p {{ifn_p}}); young benchmark {{ifn_y}}× [S01-A] | Comparative | Good |
| Mn switches on GM-CSF | *Gm-csf* {{gm_344_16h}}×, {{gm_344_36h}}×, {{gm_344_72h}}× at 16, 36, 72 h vs ≤ {{gm_212_max}}× (36 h: p {{gm36_p}}) [S02-F] | Comparative | Good; no young comparator, source cell unknown |
| Monocytes arrive via CCR2 | CCR2 antagonist: monocytes {{ccr2_mono_a}}% → {{ccr2_mono_b}}% (p {{ccr2_p}}) [S07-B] | Pharmacological | Good |
| Interferon and GM-CSF together make monocyte-derived DCs | *Ifnar*-null marrow {{h_ko}}% vs wild-type {{h_wt}}% (p {{h_p_ko}}); GM-CSF rescues to {{h_gm}}% (p {{h_p_gm}}) [S02-H]. GM-CSF lifts PSLN-212 from {{g_212}}% to {{g_212gm}}%, but does little alone ({{g_gm}}%) [S02-G] | Genetic + add-back | Good for sufficiency; necessity of GM-CSF not tested |
| DCs migrate, carry antigen, cross-prime | CCR7⁺ DC {{ccr7_344}}% vs {{ccr7_212}}%; antigen⁺ DC in node {{agdc_344}}% vs {{agdc_212}}%; cross-priming {{xprime_344}}% vs {{xprime_212}}% [S02-A, S02-C, S02-E] | Comparative + PTX | Good |
| Regulatory brake is released | Follicular regulatory T {{tfr7_344}}% vs {{tfr7_212}}% at day 7 (p {{tfr7_p}}); no longer different at day 30 ({{tfr30_344}}% vs {{tfr30_212}}%, p {{tfr30_p}}) [S04-B, S04-C] | Comparative | Moderate; transient |
| Antibody and CD8 responses recover | Germinal-centre B {{gcb_344}}% vs {{gcb_212}}%; IgG2a:IgG1 {{ratio1_344}} vs {{ratio1_212}}; cross-reactive IFN-γ⁺ CD8 {{ifng14_344}}% vs {{ifng14_212}}%; lung resident-memory CD8 {{trm_344}}% vs {{trm_212}}% [S03-K, S13-A/B, S05-F, S05-I] | Comparative | Good |
| **That STING is the receptor** | — | Not tested | **Gap** |
| **That CDN-1807, not Mn alone, is required** | — | Not tested | **Gap** |
| **Which effector protects** | No depletion or transfer experiment; no virus titres; no IgA | Not tested | **Gap** |

One correction matters here. Read as printed, S03-B says PSLN-344 gives an IgG2a:IgG1 ratio of {{ratio1_printed_344}}, i.e. a type-2-skewed response. Recomputing the ratio from the subclass titres in S13-A and S13-B gives {{ratio1_344}} for PSLN-344, close to the young benchmark ({{ratio1_y}}): the S03-B headers are rotated by one column. The S13 titres rank the groups in the same order as total IgG in S03-A, so the error is most likely in S03-B [T01a].

---

## 6. Biomarkers to validate efficacy

None of these is a validated correlate yet: every association below is between groups of different animals. Study 1 measures them and the challenge outcome in the same animals so that they can be tested properly. Figure A3 (Appendix B) shows how far each read-out moves towards the young level.

| Use | Biomarker | PSLN-344 vs PSLN-212 in aged mice | When | Human read-out |
|---|---|---|---|---|
| Target engagement | *Ifnb1* / interferon signature | {{ifn_344}}× vs {{ifn_212}}× [S01-A] | 16 h | Blood interferon-gene score, CXCL10; nasal-lining-fluid IFN-β |
| Target engagement (age-specific) | GM-CSF | {{gm_344_36h}}× vs {{gm_212_36h}}× [S02-F] | 16–36 h | GM-CSF in nasal lining fluid or sputum |
| Early cellular response | CD11b⁺ DC; CCR7⁺ migratory DC | {{dc_344}}% vs {{dc_212}}%; {{ccr7_344}}% vs {{ccr7_212}}% [S01-E, S02-A] | Day 3–4 | Activated monocytes/DC in blood or nasal curettage |
| Early adaptive response | ICOS⁺ Tfh; Tfh:Tfr ratio | {{tfh_344}}% vs {{tfh_212}}% [S04-A]; Tfr {{tfr7_344}}% vs {{tfr7_212}}% [S04-B] | Day 7 | Circulating Tfh and plasmablasts at day 7 |
| **Primary immunogenicity** | HAI titre | GMT {{hai1_344}} vs {{hai1_212}}; {{hai3_344}} vs {{hai3_212}} [S03-C, S03-G] | Day 14 | HAI seroconversion and GMT ratio (the conventional regulatory read-out for influenza vaccines) |
| Supporting immunogenicity | Neutralising titre; IgG2a:IgG1 | {{nt1_344}} vs {{nt1_212}} [S03-D]; {{ratio1_344}} vs {{ratio1_212}} [S13-A/B] | Day 14 | Microneutralisation; IgG subclass |
| Breadth | Cross-reactive IFN-γ⁺ CD8; lung resident-memory CD8 | {{ifng14_344}}% vs {{ifng14_212}}% [S05-F]; {{trm_344}}% vs {{trm_212}}% [S05-I] | Day 14–60 | IFN-γ ELISpot to conserved antigens |
| Tolerability | Lung *Tnf*, *Il6* at 72 h; CNS *Tnf*; body weight | {{cy72_Tnf_344}}× and {{cy72_Il6_344}}× [S09-A]; {{cns_Tnf}}× [S10-A]; −{{wl_344}}% [S08-D] | 36 h – day 7 | Reactogenicity, serum IL-6/TNF, olfactory testing |
| **Missing, add now** | Mucosal IgA; virus titre after challenge; Mn in brain | not measured | — | Nasal IgA; viral shedding |

---

## 7. If we drop it: what we give up, and why we might

**What we give up**

- The only formulation in our dataset that reliably protects aged animals: {{early_344}} survivors vs {{early_212}} for our own Mn-free version and {{early_sham}} for vaccine + empty liposome [T04], with surviving animals still losing about {{nad_344}}% of body weight (protection from death, not from illness) [T09a].
- Single-dose, needle-free protection that starts within 2–3 days ({{d3_344}}) and is still present at day 60 ({{d60_344}}) [S06-B/D, S06-E–G].
- Protection across subtypes, including seasonal vaccine → H5N1 ({{c_344}}, {{d_344}}, {{f_344}}) and wild-type H5N1 ({{j_344}}) [S06-C/D/F, S03-J].
- An age-specific mechanism (restored interferon + GM-CSF → monocyte-derived DCs) that returns immune read-outs from {{med_212}}% to {{med_344}}% of the young level [T07] and could, in principle, be carried to other vaccines for older adults. That last step is untested: the only non-influenza antigen used was ovalbumin [S02-C, S02-E].

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
| Positioning as a stand-alone STING agonist (antiviral or oncology) | Ruled out | Adjuvant alone {{h_adj}} [S15-H]; no tumour data exist |
| Leading with PSLN-212 (no Mn) | Ruled out for older adults | {{early_212}} survival; {{med_212}}% of young immune response [T04, T07]. If the committee defines the asset as PSLN-212 rather than PSLN-344, my recommendation for this population would be to drop it |
| Giving more of the Mn-free PSLN-212 | Ruled out | Its *Ifnb1* response plateaus at {{obs40_212}}× at 40 µg, below PSLN-344 at 10 µg ({{obs10_344}}×) [S08-A] |
| CMP-204 (cGAMP in the same liposome) | Ruled out | *Ifnb1* {{ifn_cmp}}× vs {{ifn_344}}×; {{i_cmp}} survival in aged mice [S01-A, S03-I] |
| Adding the TLR7/8 agonist R848 | Ruled out | PSLN-212/R848: {{wl_combo}}% mean weight loss, {{wl_combo_n10}} of 5 animals ≥ 10%, one animal not recorded at day 10, lung *Tnf* {{cy72_Tnf_combo}}× and *Il10* {{cy72_Il10_combo}}× still at 72 h, and lower *Ifnb1* than PSLN-344 ({{ifn_combo}}× vs {{ifn_344}}×) [S08-D, S09-A, S01-A] |
| Replacing Mn with co-delivered GM-CSF | Held in reserve | Recombinant GM-CSF lifted monocyte-derived DCs with PSLN-212 from {{g_212}}% to {{g_212gm}}% [S02-G], but there are no antibody or survival data; worth one arm if Study 3 raises a manganese concern |
| A young-adult or paediatric label | Ruled out | No advantage in young hosts [S09-B/D/F, S13-E] |
| Advancing straight to IND-enabling work | Ruled out | Data not decision-grade; no toxicology; no attribution controls |
| Partnering or out-licensing now | Ruled out for now | With open data-integrity questions and no attribution or safety data the package would be valued low; Gate 1 is the earliest sensible point |
| Dropping now | Ruled out for now | Effect size and consistency (Section 3) against a staged programme that can be stopped at each gate |
| Early protection is a non-specific innate antiviral state | Ruled out | Adjuvant alone {{h_adj}}, vaccine alone {{h_vac}}, together {{h_combo}} [S15-H] |
| Day-60 deaths mean the response wanes | Cannot tell | Unchallenged aged controls died at {{bg_pct}}% ({{bg_deaths}}; 95% CI {{bg_ci}}) over the same window [S06-E–G] |
| Using the "Untreated" groups as challenge controls | Ruled out | The annotation states they received no virus; they measure old-age attrition |
| Mn improves delivery to epithelium | Cannot tell | S08-C contradicts S01-B for the same measurement ({{aec1_s08c}}% vs {{aec1_np}}% for type I cells) |
| Using S03-B/F, S11-A/B, S07-C, S08 rows 89–101, S05-A/B as printed | Excluded | Rotated headers; duplicated values; duplicate labels; no labels; n = 2 with contradictory conditions (Appendix A) |
| Body-weight curves as primary efficacy evidence | Excluded | Carried-forward values for dead animals and re-used trajectories [T01d, T01f] |
| Claims of sterilising immunity, mucosal IgA, durability beyond day 60, efficacy in males or the very old, or efficacy with split/recombinant antigen | Not made | Not measured |

---

## Appendix A — Data-integrity log

Survival tables were used as the primary efficacy record because they are complete and the paired weight tables agree with them on the number of deaths in {{iv_agree}} of {{iv_total}} group comparisons ({{iv_dis}} disagree, {{iv_amb}} are ambiguous). Resolving every conflict against PSLN-344 moves the pooled result from {{early_344}} vs {{early_212}} to {{worst_344}} vs {{worst_212}} (p {{worst_p}}) [T04c]. The conclusion holds; the individual numbers need the audit. Figure 3, after the table, shows four of the findings.

| # | Where | Finding | Handling |
|---|---|---|---|
| 1 | S03-B, S03-F | Column headers rotated by one position relative to the subclass titres in S13-A–D (Figure 3a); as printed PSLN-344 looks type-2-skewed ({{ratio1_printed_344}}), recomputed it is {{ratio1_344}} [T01a] | Recomputed values used |
| 2 | S09-A, columns X–AS | Labelled 16 h, but all 21 *Ifnb1* values equal the 72 h panel of S01-A [T01b] | Treated as 72 h |
| 3 | S09-A vs S01-A | The same control values are labelled "PBS" in one block and "Sham" in the other | Noted |
| 4 | S11-A, S11-B | {{s11_same}} of {{s11_tot}} values identical in the same cell position, for alveolar macrophages and neutrophils [T01c] | Both excluded |
| 5 | S07-C | Both groups carry the same label | Excluded |
| 6 | S08 rows 89–101 | Thirteen unlabelled time-to-event rows | Excluded |
| 7 | S08-C vs S01-B | Type I epithelial uptake of the same particle {{aec1_s08c}}% vs {{aec1_np}}%; column 2 of S08-C matches S01-B's type I values, suggesting transposed headers | Excluded |
| 8 | S08-A | Group "PSLN-344/R848" is not in the materials list | Not used |
| 9 | S03-J, S13-E, S05-A/B, S09-F | Stated n differs from observations (9 vs 10; 5 vs 7; 3 vs 2; 8 vs 7 in sham; the annotation attributes the last to S09-B) | Analysed as found; S05-A/B not used |
| 10 | S03-J, cell J46 | A PSLN-344 animal has a survival flag but no day | Counted as survivor; omitted from log-rank |
| 11 | S06 | Labels S06-E and S06-F are each used for two different experiments | Separated by row range |
| 12 | S03-I vs S13-F; S03-J vs S13-G | Paired survival and weight blocks list different groups; death patterns indicate shifted labels (aged PSLN-212: 0/7 survivors in S03-I, 3/7 in S13-F) | Survival table used; sensitivity analysis |
| 13 | Survival vs weight tables | Number of deaths disagrees in {{iv_dis}} of {{iv_total}} group comparisons, e.g. PSLN-344 in S06-D (7/7 vs 5/7), S06-E (5/7 vs 6/7), S06-G (4/7 vs 5–7/7) [T01d] | Sensitivity analysis [T04c] |
| 14 | S06-C vs S06-D | Identical time-to-event vectors for Sham and PSLN-212 in two different experiments | Flagged |
| 15 | Weight tables | Dead animals are blank in some groups and carried forward in others | Carried-forward values removed before summarising |
| 16 | Weight tables | {{traj_pairs}} animal trajectories recur in a different experiment, identical or shifted by whole numbers ({{traj_blockpairs}} pairs of experiment arms, e.g. all seven PSLN-344 animals of S15-C reappear in S15-I); {{frac_shared}} of {{frac_total}} high-precision values share their decimal part with a value in another block; one row of S09-C is duplicated between groups [T01f, T01g] | Weight data treated as supporting only |
| 17 | S05-A, S05-B, S05-I | Conditions name both ovalbumin and influenza vaccine; the NP tetramer used requires a strain that is not stated; n = 2 in S05-A/B. S05-I refers to the same conditions | S05-A/B not used; S05-I used, antigen uncertain |
| 18 | Several | Not stated: challenge virus and interval for S15-L/N; interval for S06-E rows 71–105; time-points for S11-E, S13-H, S14-A; adjuvant and age of the pertussis-toxin arm; age in S03-J; whether "20 µg" refers to CDN or total particle; Mn content; instillation volume | Flagged for Gate 0 |
| 19 | S08-B | Encapsulation is stated as CDN-1807 absorbance but reported for two preparations that contain no CDN-1807 | Noted |
| 20 | S03-C, S03-G | HAI values of 0 are below the lowest dilution tested (1:10) | Set to 5 for geometric means |
| 21 | Annotation vs workbook | Annotation says PSLN-212 observations decline in S13-F; the workbook carries values forward | Noted |
| 22 | All sheets | Last digits are far from evenly spread: 2, 3 and 5 are over-represented among the {{td_n2}} two-decimal immunology values (χ² = {{td_chi2}}, 9 d.f.) and the {{td_nw}} one-decimal body weights (χ² = {{td_chiw}}); instrument read-outs normally give even last digits, so the tables look hand-entered or transcribed [T01h] | Reconcile against instrument exports at Gate 0 |

![Figure 3](figures/fig3_data_integrity.png)

---

## Appendix B — Supporting figures and tables

![Figure A1](figures/figA1_km_grid.png)

**Survival by experiment (survivors / animals, as printed)**

| Block | Host | Vaccine → challenge (day after dose) | Sham | PSLN-212 | PSLN-344 | Young + 212 | Other |
|---|---|---|---|---|---|---|---|
{{SURVIVAL_ROWS}}

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
