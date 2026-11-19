---
title: "PSLN-344: portfolio recommendation and next-step proposal"
subtitle: "Intranasal STING-agonist adjuvant (CDN-1807 with Mn²⁺ in a surfactant-mimetic liposome) for influenza vaccination of older adults"
date: "Prepared for the portfolio review, 1 November 2026"
---

# 1. Recommendation

**Yes, keep the asset, but as a gated preclinical programme and not yet as a development candidate.** Approve two items now: a records audit (Step 0) and one confirmatory study (Study 1). Release further funding only against the endpoints in Section 3.

I have taken "the asset" to be PSLN-344: the STING agonist CDN-1807 with Mn²⁺ in the surfactant-mimetic liposome, given intranasally with inactivated influenza vaccine. PSLN-212 is the same drug and vehicle without Mn²⁺. The distinction decides the answer, because in aged animals (mice of 20 months or more) PSLN-212 fails and PSLN-344 works. If the asset under review is PSLN-212, it should not go forward for older adults.

**How the asset looks.** The efficacy signal is strong on the endpoint that matters (survival) in the model that matters (aged animals). The package around that signal is thin, and the data file contains errors that the committee will find if it checks.

**Why keep it**

1. *It rescues survival in aged animals.* Eight challenge experiments remain once the duplicated survival table is counted once and the two tables with label conflicts are set aside. In those eight, {{clean8.s344|v}} aged animals given vaccine plus PSLN-344 survived, against {{clean8.s212|v}} with PSLN-212 and {{clean8.shams|v}} with vehicle (empty liposome plus vaccine) {{clean8|t}}. As printed, across all eleven experiments, the counts are {{all11.s344s|v}}, {{all11.s212s|v}} and {{all11.shams|v}} {{all11|t}}. The risk of death fell about nine-fold ({{hr.clean8}}). The effect appears in three mouse strains, one of them outbred, and against five challenge viruses including wild-type H5N1 {{breadth|t}}.
2. *It acts fast and across subtypes.* When challenge came only 2–3 days after a single dose, {{rapid.short|v}} animals survived {{rapid|t}}. Given with an H3N2 vaccine, PSLN-344 protected {{hetero.h1|v}} aged animals against an H1N1 virus; given with the seasonal H1N1+H3N2 vaccine, it protected {{hetero.h5d60|v}} against H5N1 two months later {{hetero|t}}. Neither challenge subtype was in the vaccine.
3. *It corrects a defined defect of ageing.* After PSLN-212, interferon-β message in the lung rose {{ifn.a|v}}-fold in aged animals against {{ifn.y|v}}-fold in young ones; PSLN-344 raised it {{ifn.m|v}}-fold in aged animals {{ifn|t}}. Over PSLN-212, antibody titres (HAI, the standard read-out for influenza vaccines) rose {{hai.fold|v}} {{hai|t}} and H5N1-reactive CD8 T cells {{cd8.fold|v}} {{cd8|t}}.
4. *Tolerability at the effective dose is acceptable, as far as it was measured.* Mean peak weight loss was {{tol.m|v}} against {{tol.vac|v}} for vaccine alone, with recovery by day 10 {{tol|t}} (Figure 8). Brain inflammatory transcripts at 36 hours did not differ from vehicle, while the positive control, cholera toxin, raised them {{cns.ct|v}} {{cns|t}}. The assays can detect a poorly tolerated adjuvant: the combination with the TLR7/8 agonist R848 cost {{tol.r848|v}} and one animal has no day-10 record {{r848|t}}.

**Why the "keep" is conditional**

1. *The record has defects* (Section 8). One of the eleven survival tables is a row-for-row copy of another (D1). Two have control-arm labels that conflict with their own body-weight records (D2, D3). An antibody-subclass block has its column headers rotated (D4), and a "neutrophil" block repeats a macrophage block (D5). None of these reverses the conclusion, which is why I lead with 44 of 56 rather than 68 of 80; even the worst-case reading of every conflict leaves {{worst.a|v}} survivors on PSLN-344 against {{worst.b|v}} on PSLN-212 {{worst|t}}. But the file should not reach the committee uncorrected.
2. *Restoration is partial.* Aged animals on PSLN-344 still did worse than young animals on PSLN-212, the benchmark for what a working adjuvant achieves: {{gap.a|v}} survived against {{gap.y|v}} ({{gap.p|v}}) {{gap|t}}. Across {{ri.n|v}} immune read-outs PSLN-344 moved aged animals a median {{ri.pct|v}} of the way from the aged level to the young level, and {{ri.short|v}} read-outs stayed significantly short of young {{ri|t}}. The weakest step is dendritic-cell co-stimulation: its two markers were restored by only {{costim.cd40|v}} and {{costim.cd86|v}} {{costim|t}}.
3. *Durability is unproven.* {{dur.d14|v}} survived when challenged on day 14 and {{dur.d60|v}} on day 60 {{dur|t}}. But {{bg.deaths|v}} untreated aged controls that were never challenged also died in the same two-week windows {{bg|t}}, so the day-60 result cannot separate waning protection from old age (Figure 7).
4. *We cannot yet say what our proprietary molecule contributes.* No group received Mn²⁺ without CDN-1807, or Mn²⁺ with the generic agonist cGAMP. Without Mn²⁺ and at the same dose, CDN-1807 gives {{cdn.ratio|v}} the interferon signal of cGAMP {{cdn|t}}, but without Mn²⁺ neither formulation protected aged animals reliably.
5. *Safety is largely unmeasured.* There is no histopathology, no manganese distribution, no blood exposure and no repeat dosing {{design|t}}. The route is nasal and manganese is a recognised neurotoxicant†. Lung inflammatory transcripts were still raised at 72 hours ({{cyto.h72|v}}; see D6) {{cyto|t}}. On day 8, the last day sampled, monocytes still made up {{resol.mono|v}} of lung cells, against {{resol.veh|v}} with vehicle {{resol|t}}. Every challenge study used the same single dose (Figures 8 and 9).
6. *Translation is untested.* The data come from mice only, female where the sex is stated, with 5–7 animals per group and no comparison with the high-dose or adjuvanted vaccines that older adults already receive† {{design|t}}. Mouse intranasal dosing reaches the lung and the mechanism runs through lung cells (Section 5); a human nasal spray may not reach them†.

**Stop rules.** I would recommend dropping the asset if any of the following happens:

- the audit cannot trace the primary survival tables to source records;
- Study 1 shows survival on PSLN-344 below 50%, or less than 30 points above PSLN-212, or no better than Mn²⁺ alone;
- Study 3 finds manganese accumulating in brain, or lung pathology persisting to day 28, at up to twice the effective dose.

**Confidence.** High that the survival effect in these records is not chance (p = {{clean8.p|v}}, stratified log-rank test {{clean8|t}}). Moderate that it will replicate, given the record defects and that nothing in the file indicates randomisation or blinding. Low that it reaches people unchanged, because route, dose and safety are open.

**Reading this document.** Every number carries an evidence tag such as [E7]. Appendix A gives, for each tag, the workbook cells and the calculation behind it, and the scripts in `analysis/` reproduce every value. Record defects are numbered D1 to D16 (Section 8). Statements marked † rest on general scientific knowledge, not on our dataset, and should be confirmed independently. "Vehicle" is the workbook's "Sham"; the "young benchmark" is young mice (7–8 weeks) given PSLN-212. Sources: `psln_program_dataset.xlsx` (15 sheets, 102 data blocks) and `psln_program_annotation.pdf`.

# 2. The asset at a glance

**Table 1. Scorecard.**

| Question | What our data show | Rating |
|:---------------|:---------------------------------------------------------------|:----------|
| Does it protect aged animals? | {{clean8.pct344|v}} to {{all11.pct344|v}} survival, against {{clean8.pct212|v}} to {{all11.pct212|v}} with PSLN-212 and 0 to 1% with vehicle; three strains, five viruses {{clean8|t}} {{all11|t}} {{breadth|t}} | Strong |
| How fast? | {{rapid.all|v}} survive a challenge 2–3 days after one dose {{rapid|t}}. Antigen is needed: adjuvant alone protected {{antigen.adj|v}} {{antigen|t}} | Strong |
| How broad? | Protects against subtypes absent from the vaccine: H1N1 {{hetero.h1|v}}; H5N1 {{hetero.h5|v}} at day 14 (table affected by D1) and {{hetero.h5d60|v}} at day 60; H3N2 {{hetero.h3|v}} at day 60 {{hetero|t}} | Strong, small groups |
| How durable? | {{dur.d60|v}} at day 60 against {{dur.d14|v}} at day 14 (p = {{dur.p|v}}) {{dur|t}}, confounded by {{bg.pct|v}} background deaths {{bg|t}} | Unresolved |
| As good as a young response? | No. Survival {{gap.rd|v}} lower than the young benchmark {{gap|t}}; median restoration {{ri.pct|v}} {{ri|t}}; survivors lose more weight (lowest weight {{nadir.m|v}} against {{nadir.y|v}} of baseline {{nadir|t}}) | Partial |
| Is the mechanism understood? | Yes for the main chain; seven of its thirteen links are tested by an intervention (Section 5) | Good |
| Is it tolerated? | Weight loss {{tol.m|v}}, recovered by day 10; no brain signal at 36 h; adjuvant given alone before infection did not hasten death; lung inflammation not shown to resolve; no pathology or manganese data {{tol|t}} {{cns|t}} {{antigen|t}} {{resol|t}} | Thin |
| Is the dose known? | One dose (20 µg) in every challenge study. Interferon response near plateau: 40 µg adds {{dose.step|v}} over 20 µg {{dose|t}} | Gap |
| Is it differentiated? | Against PSLN-212: yes in aged animals, no in young ({{young.a|v}} against {{young.b|v}} survive {{young|t}}). Against cGAMP: {{cdn.ratio|v}} the interferon signal without Mn²⁺ {{cdn|t}}. Against marketed enhanced vaccines: no data | Partly |
| Can the file be trusted? | The main effect survives every sensitivity analysis (Table 2), but 16 record defects need correcting, three of them in survival tables | Needs audit |
| Will it translate? | Mice only, female where the sex is stated; no second species; no human cells; delivery route open {{design|t}} | Unknown |

![**Figure 1.** Survivors in every aged-animal challenge experiment. Rows marked a, b or c have a record defect (Section 8). Source: T5, T7.](figures/fig1_survival_by_experiment.png){width=6.7in}

![**Figure 2.** Pooled survival curves for the eight headline experiments. Source: S06-A, -B, -C, -E, -F, -G; S15-L, -N.](figures/fig2_pooled_survival.png){width=6.3in}

**Table 2. The survival result under each reading of the record.**

<<TABLE:sensitivity>>

![**Figure 3.** How far PSLN-344 moves aged animals towards the young benchmark, for each of 40 immune read-outs. DC, dendritic cell; MLN, lung-draining lymph node; GC, germinal centre; Tfh and Tfr, follicular helper and regulatory T cells; TRM, resident memory T cells; GZMB, granzyme B; d, day. Source: T11.](figures/fig3_restoration_index.png){width=6.5in}

# 3. Next steps

![**Figure 4.** The gated plan. Each gate has a stop rule.](figures/fig4_gated_plan.png){width=6.7in}

Where our data allow, thresholds are set from them, and the "Today" entries show the current value. The remaining thresholds are my judgement and should be agreed with the study directors. Group sizes come from exact power calculations {{power|t}}. With seven animals per group, a single historical experiment had {{power.hist|v}} power for the effect actually observed, and {{power.histdur|v}} power to detect a day-60 decline of the size seen {{power|t}}.

**Step 0. Records audit (no animals)**

- *Must establish:* that the numbers the committee sees are the numbers in the laboratory records.
- *Work:* trace the 16 defects in Section 8 to source (animal-facility mortality logs, cytometer and plate-reader exports); correct or withdraw each block; add the missing conditions (D9); re-issue the workbook with a change log.
- *Endpoints we need to see:* every survival table matched to the mortality log. After corrections, pooled survival on PSLN-344 in aged animals still at least 70%, and at least 50 points above PSLN-212 (today: {{clean8.pct344|v}} to {{all11.pct344|v}}, and {{clean8.rd|v}} to {{all11.rd|v}} points {{clean8|t}} {{all11|t}}). S06-D, S11-B and the re-used weight traces either sourced or withdrawn.
- *Stop or rethink if:* two or more primary survival tables cannot be sourced. Then the package is unverified, and Study 1 must be run as a fully independent replication before anything else is funded.

**Study 1. Confirm, attribute and compare (aged mice, both sexes)**

- *Must establish:* (a) the effect reproduces under randomised, blinded conditions and in males; (b) what Mn²⁺ and CDN-1807 each contribute; (c) PSLN-344 is at least as good as the kind of enhanced vaccine older adults receive now†; (d) which biomarkers predict survival in the same animal.
- *Design essentials:* arms are vehicle, PSLN-212, PSLN-344, Mn²⁺ without CDN-1807, cGAMP with Mn²⁺, an intramuscular high-dose or emulsion-adjuvanted vaccine, the young benchmark, and unchallenged aged controls. Use 24 animals per key arm (12 per sex), which gives {{power.p24|v}} power for 75% against 25% survival and {{power.p24attr|v}} for 80% against 40% {{power|t}}. With satellites that is roughly 200 aged animals, so sourcing them will set the timetable (my planning estimate). Bleed every animal before challenge. Add satellite groups for lung virus titre, which the current package lacks, and for T cells.
- *Endpoints we need to see:*

| Endpoint | Need to see | Today |
|:-----------------------|:------------------------------|:-----------------------------|
| Survival 14 days after mismatched-subtype challenge (primary) | PSLN-344 at least 70%, and at least 40 points above PSLN-212, p < 0.05 | {{clean8.pct344|v}} against {{clean8.pct212|v}} {{clean8|t}} |
| Each sex | at least 8 of 12 survive | no data in males {{design|t}} |
| Attribution | PSLN-344 at least 30 points above Mn²⁺ alone, and not below cGAMP with Mn²⁺ | not tested |
| Comparator | survival and weight loss not worse than the intramuscular enhanced vaccine against a matched strain; better against a mismatched strain | not tested |
| Lung virus titre, day 3–5 after challenge | at least 1 log₁₀ below vehicle | not measured |
| Weight loss after challenge | lowest weight within 4 points of the comparator arm | {{nadir.m|v}} against {{nadir.y|v}} in young {{nadir|t}} |
| Biomarkers before challenge, same animals | HAI at least 160; interferon-β message at 16 h at least 30-fold (satellite); H5N1-reactive CD8 T cells at least 5%. Each should predict survival with an area under the ROC curve of 0.8 or more | thresholds from {{bm|t}}; never tested within animals |
| Tolerability after dosing | mean weight loss no more than 5%; no animal above 10% | {{tol.m|v}} mean, {{tol.worst|v}} worst {{tol|t}} |

- *Stop or rethink if:* survival is below 50%, or less than 30 points above PSLN-212, or no better than Mn²⁺ alone. If PSLN-344 only equals cGAMP with Mn²⁺, the science holds but the case for our own molecule becomes a commercial question.

**Study 2. Dose, booster and durability (aged mice)**

- *Must establish:* the lowest effective dose and its margin to the highest tolerated dose; whether a booster closes the gap to young; whether protection lasts 90 days once background deaths are counted.
- *Design essentials:* PSLN-344 at 5, 10, 20 and 40 µg; 20 µg given twice; challenge at day 14 and day 90; at least 20 unchallenged aged controls per time point, because even 20 animals pin a 19% background death rate down only to {{bgn.ci20|v}} {{bgn|t}}.
- *Endpoints we need to see:* a dose of 20 µg or less giving at least 70% survival; at least a two-fold margin between the lowest effective dose and the highest dose with weight loss under 5% and lung cytokines back within two-fold of baseline by day 7; day-90 survival within 15 points of day-14 survival after subtracting background deaths; antibody and CD8 responses at day 90 at least half their day-14 values. Today: interferon response half-maximal at {{dose.ed50|v}} and near plateau at 20 µg {{dose|t}}; a booster lifts aged IgG only to {{ab.boost|v}} of the boosted young level {{ab|t}}.
- *Stop or rethink if:* no dose separates efficacy from tolerability, or protection is gone by day 90. The second outcome would turn the product into a seasonal two-dose regimen, which changes the commercial case.

**Study 3. Safety, exposure and manganese distribution (pilot, not GLP)**

- *Must establish:* that intranasal Mn²⁺ does not accumulate in brain; that lung inflammation resolves; what reaches the blood; that repeat dosing is tolerated.
- *Design essentials:* aged and young mice of both sexes; one and three doses at 1×, 2× and the highest feasible multiple of the effective dose; samples at 6 h, 36 h and days 3, 7, 14 and 28.
- *Endpoints we need to see:*

| Endpoint | Need to see | Today |
|:-----------------------|:------------------------------|:-----------------------------|
| Manganese in olfactory bulb and striatum | no more than 1.25× vehicle at day 14 | not measured |
| Lung *Il6*, *Tnf*, *Ccl2* | within 2× of baseline by day 7 | {{cyto.il6|v}}×, {{cyto.tnf|v}}×, {{cyto.ccl2|v}}× at 72 h {{cyto|t}} |
| Lung monocytes and neutrophils (lavage) | back to vehicle level by day 14 | monocytes {{resol.mono|v}} against {{resol.veh|v}} with vehicle at day 8 {{resol|t}}; neutrophil block unusable (D5) |
| Brain transcripts (*Ifnb1*, *Tnf*, *Isg15*) | within 2× of vehicle at 6 h, 36 h and day 7 | {{cns.m|v}} of untreated at 36 h only; an increase up to {{cns.up|v}} over vehicle not excluded {{cns|t}} |
| Histopathology of nose, lung and brain | nothing above minimal grade at day 28 | not done |
| Plasma CDN-1807; serum interferon-β, IL-6, TNF | characterised; back to baseline by 72 h | not measured |
| Second-dose response | not lower than first-dose response (anti-PEG antibodies checked) | not tested |

- *Stop if:* manganese accumulates in brain in a dose-related way, or lung pathology persists at day 28, at up to twice the effective dose.

**Study 4. Second species and human cells**

- *Must establish:* that the effect exists outside the mouse; whether nasal deposition is enough or the lung must be reached, which fixes the device and the market; and that the age defect and its rescue by Mn²⁺ exist in human cells.
- *Design essentials:* ferrets (aged if obtainable) given whole-virus or split vaccine, with or without PSLN-344, by nasal spray or by lower-airway delivery, then matched or mismatched challenge. Blood-derived cells from donors aged 65 or over and 18–40, stimulated with CDN-1807 or cGAMP, each with and without Mn²⁺, covering the common human STING variants†.
- *Endpoints we need to see:* HAI at least four-fold above vaccine alone; nasal-wash virus at least 1 log₁₀ lower after mismatched challenge; no more fever or weight loss than vaccine alone; in cells from older donors, Mn²⁺ restores the interferon response to at least 70% of the young-donor response; activity on every common STING variant.
- *Stop or rethink if:* no clinically feasible delivery route gives an effect.

**Study 5. Manufacturing readiness (runs alongside)**

- *Must establish:* that the product can be made reproducibly and stored in a refrigerator.
- *Endpoints we need to see:* encapsulation of at least 70% (today {{ee.m|v}}); manganese content and particle size within specification across three batches; six months' stability at 2–8 °C (today: stored lyophilised at −20 °C); endotoxin within limits; particles intact after spraying or nebulising. None of these except encapsulation is in the package {{ee|t}}.

# 4. Target demographic

**Primary: adults aged 65 and over who receive seasonal inactivated influenza vaccine.** This is the only population in which our data show an advantage. In aged animals the Mn²⁺-free formulation fails and PSLN-344 works ({{all11.s212s|v}} against {{all11.s344s|v}} survive {{all11|t}}). In young animals the two are indistinguishable ({{young.b|v}} against {{young.a|v}} survive; interferon, antigen transport and weight loss similar {{young|t}} {{youngpd|t}}), so there is no case for a premium product in younger adults.

**Table 3. Segments for the market team to size.**

| Segment | Basis in our data | Confidence | What to size |
|:--------------------|:------------------------------------------|:------------|:--------------------------|
| Adults 65+ (core) | Mice of 20 months or older: PSLN-344 {{all11.pct344|v}} survival against {{all11.pct212|v}} {{all11|t}} | Moderate: mouse only, no males | People 65+ by region × seasonal vaccination coverage × share willing to take a nasal or inhaled vaccine |
| Adults 50–64 (upside) | The age defect is already present at 14 months: PSLN-212 protected {{mid.a|v}}, PSLN-344 {{mid.b|v}} {{mid|t}} | Low: two experiments | As above for 50–64 |
| Outbreak or pandemic use in older adults (upside) | Protection 2–3 days after one dose ({{rapid.short|v}} {{rapid|t}}), including wild-type H5N1 ({{h5wt.n|v}} {{h5wt|t}}) | Low to moderate | Government stockpile and outbreak-response procurement |
| Adults under 50 | No advantage over PSLN-212 {{young|t}} | — | Exclude from the base case |
| Men; people with chronic lung disease; immunocompromised people | No data {{design|t}} | — | Treat as sensitivity cases, not base case |

Five points define what is being sold:

- **It is an adjuvant, not a stand-alone product.** PSLN-344 without vaccine protected {{antigen.adj|v}} animals; with vaccine, {{antigen.both|v}} {{antigen|t}}. The unit of sale is an adjuvanted vaccine dose, so the plan needs a vaccine antigen partner or in-house antigen supply.
- **It would replace the injected vaccine, not add to it.** Adjuvant and antigen were always given together by the respiratory route. Nothing in the data supports giving PSLN-344 nasally alongside an injected vaccine.
- **Prior influenza exposure did not change the result.** PSLN-344 protected {{imprint.a|v}} previously infected animals and {{imprint.b|v}} previously uninfected ones {{imprint|t}}. Every older adult has met influenza before, so this removes one reason to segment.
- **The antigen was whole inactivated virus.** Every study used formalin-inactivated whole virus {{design|t}}. Most licensed seasonal vaccines are split or subunit products†. Whether PSLN-344 gives the same cross-subtype protection with those is untested, so Study 4 includes one.
- **The device is open.** If Study 4 shows the lung must be reached, the product is an inhaled vaccine rather than a nasal spray†, which changes cost, acceptance and the addressable share.

The link from mouse age to human age (20 months to roughly 60–65 years; 14 months to roughly 45–50) is a convention†, not something our data establish. Dose frequency is also an assumption: protection is shown to 60 days at most, so annual dosing is untested.

# 5. Mechanism and biomarkers

![**Figure 5.** Mechanism supported by the dataset. Green links were tested by an intervention; blue links rest on group differences. DC, dendritic cell; Tfh, follicular helper T cell; TRM, resident memory T cell; Treg, regulatory T cell.](figures/fig5_mechanism.png){width=6.7in}

**The mechanism in five stages** (box numbers refer to Figure 5)

- *Delivery (boxes 1–2).* Alveolar macrophages take up the liposome through surfactant proteins: {{uptake.wt|v}} of them in normal mice against {{uptake.ko|v}} in mice lacking surfactant proteins A and D. Cargo then reaches the lung epithelium ({{uptake.aec2|v}} of type II cells against {{uptake.free|v}} with free dye) {{uptake|t}}. Blocking gap junctions cuts the downstream monocyte influx by {{gapj.cut|v}} {{gapj|t}}.

- *Interferon (box 3).* Mn²⁺ restores the interferon signal that ageing blunts; Section 1 gives the numbers {{ifn|t}}. It raises the ceiling of the response ({{dose.emax|v}} against {{dose.emax212|v}}) and leaves the half-maximal dose unchanged ({{dose.ed50|v}} against {{dose.ed50b|v}}) {{dose|t}}.

- *Monocytes become dendritic cells (boxes 4–6).* GM-CSF message rose {{gmcsf.m16|v}}-fold, against {{gmcsf.a16|v}}-fold with PSLN-212 {{gmcsf|t}}. Lung monocytes peaked at {{mono.m|v}} against {{mono.a|v}} and needed the receptor CCR2 {{mono|t}}. Their conversion to dendritic cells needed the interferon receptor ({{modc.wt|v}} fell to {{modc.ko|v}}) and was partly rescued by GM-CSF ({{modc.gm|v}}) {{modc|t}}.

- *Antigen transport, and only partial maturation (boxes 7–8).* Migratory dendritic cells rose to {{dcmig.ccr7|v}} from {{dcmig.ccr7a|v}}, and antigen-carrying cells in the lymph node to {{dcmig.ag|v}} from {{dcmig.aga|v}} {{dcmig|t}}. Their capacity to prime CD8 T cells recovered to {{xprime.m|v}} from {{xprime.a|v}}, against {{xprime.y|v}} in young animals {{xprime|t}}. The co-stimulatory markers CD40 and CD86 reached only {{costim.m40|v}} and {{costim.m86|v}}, against {{costim.y40|v}} and {{costim.y86|v}} in young animals {{costim|t}}. This is the main reason the response stays below the young benchmark.

- *Two arms of immunity (boxes 9–11).* The antibody arm: germinal-centre B cells {{gc.gcb|v}} against {{gc.gcba|v}} {{gc|t}}; HAI {{hai.m|v}} against {{hai.a|v}} {{hai|t}}; and a shift towards the IgG2a subclass (ratio {{igratio.m|v}} against {{igratio.a|v}}, recomputed because of D4) {{igratio|t}}. The T-cell arm: CD8 T cells are primed in the lung itself {{lungcd8|t}}, respond to H5N1 that was never in the vaccine ({{cd8.m|v}} against {{cd8.a|v}}) {{cd8|t}}, and leave resident memory cells in the lung ({{trm.m|v}} against {{trm.a|v}}) {{trm|t}}. In parallel, the suppressive cells that accumulate in aged lungs recede: CD206⁺ macrophages {{brake.cd206|v}} against {{brake.cd206a|v}}, and regulatory T cells {{brake.treg|v}} against {{brake.trega|v}} {{brake|t}}.

Protection needs antigen: adjuvant alone protected {{antigen.adj|v}} {{antigen|t}}. So the benefit is an immune response to the vaccine, not a general antiviral state.

**What the mechanism does not yet show.** No experiment removes STING, so on-target action is inferred. No experiment removes CD8 T cells or transfers serum, so we do not know which arm protects against mismatched strains. No group received Mn²⁺ alone. And whether Mn²⁺ changes delivery to the epithelium cannot be read from the file (D8) {{aecmn|t}}. One finding bears on durability: follicular regulatory T cells, which PSLN-344 lowered on day 7 ({{gc.tfr7m|v}} against {{gc.tfr7a|v}}), had returned to the vehicle level by day 30 ({{gc.tfr30m|v}}; vehicle {{gc.tfr30s|v}}; PSLN-212 {{gc.tfr30a|v}}; young {{gc.tfr30y|v}}) {{gc|t}}.

**Biomarkers.** Table 4 lists markers that separate the two protective regimens (aged PSLN-344, young PSLN-212) from the two non-protective ones (vehicle, aged PSLN-212) with no overlap between individual animals. In all, {{bm.nsep|v}} read-outs do so {{bm|t}}; the table keeps those that are early, mechanistically placed or measurable in blood.

**Table 4. Candidate biomarkers and provisional thresholds** (values from {{bm|t}} unless tagged).

| Marker (when) | Fig. 5 box | Protective against non-protective regimens | Use |
|:------------------------|:------|:--------------------------|:------------------------------------|
| Lung interferon-β message (16 h) | 3 | {{bm.ifn|v}} | Target engagement. Tissue only: a blood or nasal surrogate (for example an interferon-gene signature) must be added in Study 1 |
| Lung GM-CSF message (16 h) | 4 | {{bmgm.t|v}} {{bmgm|t}} | Target engagement, aged animals only |
| Lung monocytes (day 4) | 5 | {{bm.mono|v}} | Animal studies; links dose to cell response |
| Migratory dendritic cells (72 h) | 7 | {{bm.ccr7|v}} | Animal studies |
| Germinal-centre B cells (day 7) | 9a | {{bm.gcb|v}} | Animal studies; circulating follicular helper T cells are the clinical analogue† |
| HAI titre (day 14) | 10a | {{bm.hai|v}} | Blood; clinical. Use 160, not 40, as the programme threshold |
| Total IgG titre (day 14) | 10a | {{bm.igg|v}} | Blood; clinical |
| H5N1-reactive CD8 T cells (day 14) | 9b | {{bm.cd8|v}} | Blood in the clinic (interferon-γ ELISpot†); the only marker tied to cross-subtype protection |
| Lung resident memory CD8 T cells (day 25) | 10b | {{bm.trm|v}} | Animal studies; durability |

Three cautions apply. First, these are differences between regimens, not correlates within animals: markers and survival were measured in different animals, so no marker is yet validated, and Study 1 is designed to do that. Second, the conventional human threshold of HAI 40† failed here: all five aged animals on PSLN-212 reached it, yet that group was not protected {{hai40|t}}. Third, there is no blood marker of target engagement; every early marker is from lung tissue.

# 6. What we give up if we drop it

**What we would lose**

- The only formulation in the programme that protects aged animals: {{clean8.pct344|v}} to {{all11.pct344|v}} survival, against {{clean8.pct212|v}} to {{all11.pct212|v}} for the Mn²⁺-free version {{clean8|t}} {{all11|t}}.
- Protection within 2–3 days of one dose ({{rapid.short|v}} {{rapid|t}}), including against wild-type H5N1 ({{h5wt.n|v}} {{h5wt|t}}). That matters for outbreak response.
- Cross-subtype protection from an inactivated vaccine made of seasonal strains {{hetero|t}}, which injected inactivated vaccines are not expected to give†.
- A worked-out mechanism, with seven of thirteen links tested by an intervention, and a set of thresholds that tell us what to measure next.
- Twelve recorded challenge studies in aged animals (one of them the duplicated table) and two in middle-aged animals {{counts|t}}. Aged animals take 20 months to produce, so this evidence is slow to rebuild.

**What we would not lose, because we do not have it yet:** evidence in males or in a second species; a safety package; proof of durability; proof that CDN-1807 is needed; a presentation people can spray or inhale; a clean dataset.

**Why a committee could still reasonably drop it**

- The portfolio cannot carry an asset that needs a records audit and four more preclinical studies before an IND decision.
- The audit fails.
- The company does not want to take an inhaled or nasal product containing manganese through toxicology.
- No vaccine antigen partner is available, given that the adjuvant alone does nothing {{antigen|t}}.

**The trade.** Dropping now gives up a survival effect of {{clean8.rd|v}} to {{all11.rd|v}} points {{clean8|t}} {{all11|t}} on the strength of evidence that is missing, not evidence that is negative. Keeping it without gates would build on unverified records. The gated plan prices the option at one audit and one study.

# 7. What I considered and ruled out

**Other ways to position the programme**

- *PSLN-212 for older adults.* Ruled out: only {{all11.s212|v}} aged animals survived {{all11|t}}.
- *PSLN-344 for all adults.* Ruled out as a differentiated product: no advantage over PSLN-212 in young animals {{young|t}} {{youngpd|t}}.
- *PSLN-344 alone as an antiviral.* Ruled out: {{antigen.adj|v}} survived without vaccine {{antigen|t}}.
- *Adding the TLR7/8 agonist R848.* Ruled out: more weight loss, more sustained inflammation and less interferon {{r848|t}}.
- *cGAMP as the active ingredient.* Weaker than CDN-1807 without Mn²⁺ {{cdn|t}}; never tested with Mn²⁺, so it stays open and becomes an arm of Study 1.

**Other explanations for the survival effect**

- *Chance.* Ruled out: p = {{all11.p|v}} across eleven experiments {{all11|t}}.
- *The vehicle.* Ruled out: {{all11.shams|v}} survived on vehicle plus vaccine {{all11|t}}.
- *A non-specific antiviral state.* Ruled out: adjuvant alone did not protect {{antigen|t}}.
- *Age-related deaths flattering the result.* Ruled out: background deaths count against PSLN-344, not for it {{bg|t}}.
- *A single-strain artefact.* Ruled out: three strains {{breadth|t}}. In the outbred strain the comparison with PSLN-212 (6 of 7 against 2 of 7) is not significant on its own {{s15n|t}}.
- *Prior influenza exposure.* Ruled out as a modifier {{imprint|t}}.
- *Record errors.* Not ruled out, which is why Step 0 comes first. The worst-case reading still gives {{worst.a|v}} against {{worst.b|v}} {{worst|t}}.
- *Antibody alone explains protection.* Not ruled out for matched strains. It cannot explain protection against subtypes absent from the vaccine, but no depletion experiment tests the T-cell explanation directly.

**Data I chose not to rely on**

- S06-D (D1), S11-B (D5), S03-B and S03-F as printed (D4), S08-C (D8), S07-C (D10), S05-A and S05-B (D12), and the unlabelled rows on sheet S08 (D14).
- Body-weight blocks as primary evidence, because traces are re-used across experiments (D7). I use them only for morbidity and as a cross-check.
- Group mean weight curves after the first death (D15).

**Claims I decided the data do not support**

- *"Restores young-level immunity."* Restoration is {{ri.pct|v}} at the median, and {{costim.cd40|v}} to {{costim.cd86|v}} for dendritic-cell co-stimulation {{ri|t}} {{costim|t}}.
- *"Protection lasts at least 60 days."* Confounded by background deaths {{dur|t}} {{bg|t}}.
- *"HAI of 40 shows protection."* It did not in aged animals {{hai40|t}}.
- *"CDN-1807 is required."* Not tested with Mn²⁺ {{cdn|t}}.

**Recommendations I rejected**

- *Advance straight to IND-enabling work.* The record defects, the missing safety data, the attribution gap and the single species make that premature.
- *Drop now.* That would discard the largest effect in the file because of gaps, most of which the audit and the first study would either close or expose.

# 8. Record defects the committee will find

I checked every block against its label, its stated group size, its paired blocks and every other block in the workbook. Sixteen defects came out; three affect survival tables. Figure 6 shows four of them. None changes the direction of the main result, and Table 2 shows the size of the result under each reading.

![**Figure 6.** Four of the record defects (D4, D5, D7 and D1).](figures/fig6_record_defects.png){width=6.7in}

**Table 5. Register of record defects.**

<<TABLE:defects>>

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Appendix A. Evidence ledger

Each tag used in the text, with the statement it supports, the workbook cells and the analysis. Cell ranges include the header row of the block. Scripts are in `analysis/`; tables T1 to T17 are sheets of `PSLN-344_evidence_workbook.xlsx`.

<<TABLE:ledger>>

# Appendix B. Supporting figures

![**Figure 7.** Survival after challenge on day 14 and day 60, with the deaths seen in untreated aged animals that were never challenged. Bars show exact 95% confidence intervals. Source: T8.](figures/fig7_durability_background.png){width=5.4in}

![**Figure 8.** Tolerability read-outs. (a) Body weight after intranasal dosing without challenge. (b) Brain transcripts 36 hours after dosing; dots are individual animals. (c) Lung transcripts. Source: S08-D, S10-A, S09-A.](figures/fig8_tolerability.png){width=6.7in}

![**Figure 9.** Dose-response of the lung interferon-β transcript. Curves are Hill fits. Source: S08-A, T14.](figures/fig9_dose_response.png){width=6.0in}

# Appendix C. Methods

- **Data handling.** All 6,819 numeric cells of the workbook were read. Each of the 102 blocks was mapped by hand to its cell range (`psln_blocks.py`); the only numeric cells not mapped as data are day and dose axis values. Group labels were taken as printed. Where I depart from a printed label (D4, D6) the departure is stated wherever the value is used.
- **Survival.** A flag of 1 in a time-to-event block was read as death and 0 as alive at the end of observation. Proportions carry exact (Clopper–Pearson) 95% confidence intervals. Groups were compared with the log-rank test (with an exact permutation p-value for single experiments) and Fisher's exact test; pooled comparisons were stratified by experiment (stratified log-rank, Mantel–Haenszel risk difference, stratified Cox model). The log-rank code was checked against R `survival::survdiff` and gives identical statistics (T6b). The one PSLN-344 record in S03-J with no day was treated as alive at day 21.
- **Immune read-outs.** One-way ANOVA with Tukey's test, as in the annotation's stated methods; titres, fold-changes and ratios were analysed on the log scale and are reported as geometric means where stated. HAI values printed as 0 were set to 5, half the starting dilution. With five animals per group and about 40 read-outs, individual p-values are indicative.
- **Restoration index.** (aged PSLN-344 − aged PSLN-212) ÷ (young PSLN-212 − aged PSLN-212), with a bootstrap 95% interval from 10,000 resamples of animals within groups.
- **Biomarker thresholds.** For each read-out, the lowest value seen in any animal of a protective regimen and the highest seen in any animal of a non-protective regimen. These describe regimens, not individual correlates.
- **Body weight.** The lowest weight of each animal as a percentage of day 0. Death was inferred from a trace that ends before day 14 or ends in repeated identical values, because the workbook uses both conventions (D15).
- **Dose–response.** Hill model with baseline fixed at 1, fitted on the log scale, with a bootstrap interval.
- **Duplicate detection.** Exact comparison of every group vector, every animal trace and every survival vector against all others. Between unrelated animals, two weight values coincide less than 1% of the time.
- **Power.** Exact power of Fisher's test by enumeration.
- **Limits.** Animals are treated as independent units; the file does not record cages or litters. I had the workbook and the annotation only: no raw instrument files, protocols, manufacturing records, intellectual-property position, costs or competitor data. Nothing in the file states whether studies were randomised or blinded.

# Appendix D. Survival in every time-to-event block

<<TABLE:survival>>

# Appendix E. Files delivered

| File | Content |
|:-----------------------------|:-----------------------------------------------------|
| `PSLN-344_portfolio_proposal.docx` and `.pdf` | This document, in Word and PDF |
| `PSLN-344_evidence_workbook.xlsx` | Evidence ledger (E tags), defect register (D1 to D16) and the analysis tables (T0 to T16) |
| `figures/` | Figures 1 to 9 as PNG files |
| `analysis/` | Python and R scripts that reproduce every number and figure from the workbook; `README.md` gives the run order |
