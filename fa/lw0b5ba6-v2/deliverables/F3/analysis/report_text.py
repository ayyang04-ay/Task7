# report_text.py - text of the proposal. Executed inside build_report.py (uses sub, grid, fig, PB, SEP, LOG, DESIGN_LIMITS, FACTS, USED).
# Numbers appear only as {{fact_key}} placeholders; plan parameters (dates, arm lists, thresholds) are design choices, not data.

def sec_front():
    return sub(r'''---
title: "PSLN program: portfolio recommendation and proposal for next steps"
---

*Prepared for the portfolio review committee, 1 November 2026. Codes in square brackets, such as [S06-A], are block IDs in the dataset. Definitions and sources follow the recommendation.*

# 1. Recommendation

**Keep the program in the portfolio, on three conditions.**

1. **One lead.** Take PSLN-344 forward. Stop active development of PSLN-212 and keep it as the comparator arm.
2. **One indication.** Present the asset as what the data show it to be: an adjuvant, given through the nose together with inactivated influenza vaccine, for older adults. Every efficacy experiment in the dataset is an influenza vaccination-and-challenge experiment in mice. The data do not support a stand-alone STING drug: PSLN-344 without vaccine protected {{s15h_adj}} animals [S15-H].
3. **One gate.** Approve a six-week audit of the dataset and then Stage 1, a package of six mouse and human-cell studies that ends at a go/no-go gate in October 2027. Commit to IND-enabling work only if that gate is passed.

## Why keep it

- **It is the only formulation we have that protects aged animals.** Across 11 lethal-challenge experiments, {{pool_344}} aged mice survived after vaccine with PSLN-344, against {{pool_212}} after vaccine with PSLN-212 and {{pool_sham}} after vaccine with empty liposome (sham). PSLN-344 was ahead in {{n_exp_dir}} experiments (Figure 1). Resolving every discrepancy in the dataset against PSLN-344 still leaves {{sens_worst_344}} against {{sens_worst_212}} (Section 9).
- **It restores the antibody response that age removes.** Fourteen days after one dose, hemagglutination-inhibition (HAI) titers were {{hai_h1_gmr_short}} (H1N1) and {{hai_h3_gmr_short}} (H3N2) higher than with PSLN-212, and reached {{hai_h1_vs_young_pct}} and {{hai_h3_vs_young_pct}} of the titers in young animals given PSLN-212, the benchmark for a full response [S03-C, S03-G] (Figure 2).
- **Protection is broad, fast, and still present at two months.** Against strains whose hemagglutinin did not match the vaccine, {{het_344_frac}} survived versus {{het_212_frac}} [S06-A to S06-G]. When challenge came 2 to 3 days after the single dose, {{early_344_frac}} versus {{early_212_frac}} [S03-J, S06-B, S06-D]. At 60 days, {{d60_344_frac}} versus {{d60_212_frac}}; for reference, {{untreated_surv}} unchallenged animals of the same age survived the same two weeks [S06-E, S06-F, S06-G].
- **The advantage over PSLN-212 is specific to age, and that defines where we are differentiated.** In young animals both formulations protected {{young_344}} against mismatched strains, against {{young_sham}} with sham [S09-B, S09-D, S09-F]. In aged animals only PSLN-344 did. PSLN-212 therefore has no case as the lead.

## Why only conditionally

- **The dataset is not yet fit to put in front of the committee.** I logged {{n_disc}} discrepancies (Section 9). Two headline experiments have group labels that conflict with their paired body-weight tables [S03-I, S03-J]. One derived table has rotated column labels, which reverses what it says about PSLN-344 [S03-B, S03-F]. Identical body-weight series appear in unrelated experiments. None of these changes the direction of a conclusion above, but the committee will find them. Each should be closed against raw records, or disclosed, before the review.
- **We cannot yet say which ingredient is doing the work.** The two formulations differ only in Mn²⁺, and no experiment gave Mn²⁺ without our agonist. In the same liposome our agonist outperforms the natural ligand cGAMP by about 2-fold on interferon induction and on {{n_ab_2fold}} antibody readouts [S01-A, S03-A to S03-H]; adding Mn²⁺ then adds {{ab_fold_lo}}- to {{ab_fold_hi}}-fold on antibody. Whether our agonist is still needed once Mn²⁺ is present has not been tested.
- **The safety of that ingredient by this route is untested.** There is no measurement of manganese in any tissue, no histopathology, and nothing after repeat dosing. What exists is reassuring but thin: body weight dipped to {{bw_nadir_344}} of baseline and recovered by day 10 [S08-D], and brain cytokine transcripts stayed within {{cns_sham_max}} of the level seen with vaccine and empty liposome, while the cholera-toxin positive control rose {{cns_ct_range}} [S10-A]. Against that, lung *Tnf* and *Il6* were still {{c72_tnf_344}}- and {{c72_il6_344}}-fold above baseline at the last time point measured [S09-A, second panel; see D5 in Appendix A], and the neutrophil data cannot be used [S11-B].
- **Everything is in mice, and four links to a human product are missing.** The mechanism starts in the deep lung [S01-B, S01-C], which a nasal spray generally does not reach in people (*external*). No human cells have been tested. The antigen is in-house whole inactivated virus, not a licensed vaccine. And there is no comparison with the high-dose or adjuvanted vaccines that older adults already receive.
- **The gap to young animals is narrowed, not closed.** In the 10 experiments of Figure 1 that ran both arms, survival was {{aged344_vs_young}} (aged PSLN-344 versus young benchmark), with most of the shortfall at day 60.

## What would turn this into a recommendation to drop

Any one of the following, each of which is tested in Stage 0 or Stage 1:

- the audit removes the difference between PSLN-344 and PSLN-212;
- a particle carrying Mn²⁺ but no agonist performs as well as PSLN-344;
- manganese accumulates in brain or olfactory tissue, or causes lesions, at the intended dose;
- the effect is lost when the dose is delivered in a way people can take, and an inhaled product is not acceptable to us;
- the agonist does not activate the common human variants of STING;
- PSLN-344 shows no advantage over the enhanced vaccines already used in older adults.

## About this document

**Basis.** `psln_program_dataset.xlsx` (15 sheets, {{n_blocks}} data blocks, {{n_numeric}} numeric cells; last saved 3 September 2026) and `psln_program_annotation.pdf` (dated 15 September 2026). I had no later data; if newer results exist they are not reflected here. All of the data are from mice.

**Terms.** "Aged" means 20 months or older and "young" means 7 to 8 weeks, unless stated. PSLN-212 is the STING agonist CDN-1807 in a surfactant-mimetic liposome. The annotation describes CDN-1807 as a cyclic dinucleotide, and that is the class it should be compared with. PSLN-344 is the same particle with Mn²⁺ added. "Sham" is vaccine with empty liposome. "Young benchmark" is young animals given vaccine with PSLN-212. Statements marked *external* rest on general knowledge, not on our data.

**Sources.** Appendix B gives the source cells and the calculation for every number quoted. The same table, the per-block statistics and the discrepancy log are in `PSLN_evidence_tables.xlsx`.

**Where things are.** Section 2 assesses the asset and Section 3 compares the two candidates. Section 4 gives the mechanism and biomarkers, Section 5 the target population, and Section 6 the next studies. Section 7 sets out what we give up if we drop the program, Section 8 what I considered and ruled out, and Section 9 the state of the data. Appendix A is the full discrepancy log.
''')


def sec_asset():
    t = grid(['Question', 'What the data show', 'Assessment'], [
        ['Does it protect aged animals from death?',
         '{{pool_344}} alive (95% CI {{pool_344_ci}}) versus {{pool_212}} with PSLN-212 and {{pool_sham}} with sham. Difference from PSLN-212: {{mh_rd}}; stratified log-rank test {{strat_lr}}. '
         '{{n_exp_sig}} experiments are significant on their own. The deaths that did occur came later (median {{death_med_344}}, against {{death_med_sham}} for sham).',
         '**Strong.** Holds under every sensitivity analysis in Section 9.'],
        ['Does it restore the immune response?',
         'Over PSLN-212 in aged animals: IgG {{igg_h1_gmr_short}} and {{igg_h3_gmr_short}}, HAI {{hai_h1_gmr_short}} and {{hai_h3_gmr_short}}, neutralizing titer {{nt_h1_gmr_short}} and {{nt_h3_gmr_short}} (H1N1 and H3N2) '
         '[S03-A to S03-H]. {{holm_sig}} of {{holm_n}} antibody and cellular comparisons stay significant after correction for multiple testing.',
         '**Strong.**'],
        ['How close does it get to young animals?',
         'PSLN-344 closes {{gap_main_range}} of the aged-to-young gap on {{gap_n_main}} readouts (Figure 3), but only {{gap_cd40}} and {{gap_cd86}} for the co-stimulatory molecules CD40 and CD86 [S02-D] and {{gap_gzmb}} for granzyme B in lung CD8 T cells [S05-E]. '
         'HAI relative to young: {{hai_h1_vs_young}} and {{hai_h3_vs_young}}; with 5 animals per group a two-fold shortfall cannot be excluded. Survival {{aged344_vs_young}}, which is {{aged344_vs_young_rd}}.',
         '**Partial.** Most of the gap, not all of it.'],
        ['How broad is protection?',
         'Mismatched strains: {{het_344}} versus {{het_212}} [S06-A to S06-G]. Wild-type H5N1: {{surv_S03-J_344}} [S03-J]. Animals previously infected with another strain: {{imp_344_imp}} '
         '[S06-E and S06-F, rows 71 to 98]. C57BL/6 and Swiss Webster mice: {{strains_344_frac}} [S15-L, S15-N].',
         '**Strong signal**, from one experiment per setting.'],
        ['How fast?',
         '{{early_344}} alive when challenged 2 to 3 days after one dose [S03-J, S06-B, S06-D]. It needs antigen and adjuvant together: adjuvant alone {{s15h_adj}}, vaccine alone {{s15h_vac}}, both {{s15h_both}} [S15-H].',
         '**Strong.** The data do not explain how protection arises this quickly.'],
        ['How durable?',
         'Day 60: {{d60_344}} alive, against {{untreated_surv}} unchallenged animals of the same age ({{d60_vs_untreated_p}}) [S06-E, S06-F, S06-G]. Aged animals were not tested beyond day 60. '
         'Young animals were protected at day 180 with either formulation ({{young_d180_344}}) [S09-F]. One early marker had faded by day 30: the follicular regulatory T-cell share was back at the sham level ({{tfr30_344}} versus {{tfr30_sham}}; young benchmark {{tfr30_young}}) [S04-C].',
         '**Moderate.** Background deaths in very old mice blur the day-60 result.'],
        ['Does it work in young animals?',
         'Yes, and so does PSLN-212: {{young_344}} and {{young_212}} survived mismatched-strain challenge, against {{young_sham}} with sham, including a challenge 180 days after the dose [S09-B, S09-D, S09-F].',
         'Works, but is not differentiated from PSLN-212 there.'],
        ['Does it prevent illness, or only death?',
         'Aged survivors lost on average {{nadir_344}} of body weight at the worst point, against {{nadir_young}} for the young benchmark [S13-F, S15-A to S15-G, S15-M, S15-O; body-weight data, see D9 in Section 9]. No lung virus load was measured.',
         'Protects from death; does not prevent illness.'],
        ['Is the adjuvant itself tolerated?',
         'Body weight after dosing fell to {{bw_nadir_344}} (vaccine alone {{bw_nadir_vac}}) and was back to {{bw_d10_344}} by day 10; {{bw_lt90_344}} animals fell below 90% [S08-D]. Brain transcripts relative to vaccine with empty liposome: '
         '*Ifnb1* {{cns_ifnb1_344_sham}}, *Tnf* {{cns_tnf_344_sham}}, *Isg15* {{cns_isg15_344_sham}}. Relative to buffer, *Tnf* was {{cns_tnf_344}}; cholera toxin gave {{cns_tnf_ct}} [S10-A]. See Figure 5.',
         '**Acceptable as far as measured:** one dose, 10 days, 5 animals per group.'],
        ['Is Mn²⁺ safe by this route?', 'Not measured: no tissue manganese, no histopathology, no repeat dosing.', '**Not tested.**'],
        ['Is the mechanism understood?', 'Six steps from delivery to protection. Delivery, monocyte fate and migration to the lymph node are each supported by an intervention experiment; the rest rests on comparing formulations (Figure 4, Section 4).', '**Good** upstream; association only downstream.'],
        ['Is the dose justified?',
         'Interferon induction is half-maximal at about {{dose_344_ed50}}; 20 µg gives {{dose_344_pct}} of the 40 µg response [S08-A]. Every efficacy experiment used 20 µg, once.',
         'One dose level only.'],
        ['Is the formulation characterized?',
         'Encapsulation efficiency {{ee_344}} for PSLN-344 and {{ee_212}} for PSLN-212 [S08-B]. No particle size, charge, manganese content or stability data are in the workbook.',
         'Thin.'],
        ['Is it relevant to people?', 'No human cells, no second species, no licensed antigen, no comparison with licensed enhanced vaccines.', '**Not tested.**'],
        ['Can the data be relied on?', '{{n_disc}} discrepancies, {{n_disc_high}} of which would change a number the committee sees if taken at face value (Section 9).', 'Needs an audit before the review.'],
    ], [26, 66, 22])
    return sub(r'''
# 2. How the asset looks

In brief: a strong and consistent efficacy signal for PSLN-344 in aged mice, a coherent mechanism, thin safety data, no human data, and a dataset that needs an audit.

''') + t + fig(1, 'fig1_survival_by_experiment.png',
        'Survival in the 11 aged-mouse challenge experiments. PSLN-344 has more survivors than PSLN-212 in every experiment; pooled {{pool_344_frac}} versus {{pool_212_frac}}.', '6.6in') \
      + fig(2, 'fig2_serology.png', 'Antibody titers 14 days after one dose. Aged mice given PSLN-344 reach {{hai_h1_vs_young_pct}} (H1N1) and {{hai_h3_vs_young_pct}} (H3N2) of the young HAI titer; aged mice given PSLN-212 reach about a tenth.') \
      + fig(3, 'fig3_gap_closed.png', 'Share of the aged-to-young gap closed by PSLN-344, by step. The response is restored almost completely at the interferon step and for HAI, and least for co-stimulatory molecules on dendritic cells.', '6.3in')


def sec_choice():
    t = grid(['Measure', 'PSLN-212', 'PSLN-344', 'Young benchmark', 'Source'], [
        ['**Aged animals**', '', '', '', ''],
        ['Survival, 11 challenge experiments', '{{pool_212}}', '{{pool_344}}', '{{pool_young}}', 'Figure 1'],
        ['HAI titer day 14, H1N1 / H3N2', '{{hai_h1_212}} / {{hai_h3_212}}', '{{hai_h1_344}} / {{hai_h3_344}}', '{{hai_h1_young}} / {{hai_h3_young}}', 'S03-C, S03-G'],
        ['HAI values at 160 or above', '{{hai160_212}}', '{{hai160_344}}', '{{hai160_young}}', 'S03-C, S03-G'],
        ['Neutralizing titer, H1N1 / H3N2', '{{nt_h1_212}} / {{nt_h3_212}}', '{{nt_h1_344}} / {{nt_h3_344}}', '{{nt_h1_young}} / {{nt_h3_young}}', 'S03-D, S03-H'],
        ['IgG2a:IgG1 ratio, H1N1', '{{sub_h1_212}}', '{{sub_h1_344}}', '{{sub_h1_young}}', 'S13-A, S13-B (recomputed)'],
        ['*Ifnb1* in lung at 16 h (fold)', '{{ifn16_212}}', '{{ifn16_344}}', '{{ifn16_young}}', 'S01-A'],
        ['*Gm-csf* in lung at 36 h (fold)', '{{gmcsf_36h_212}}', '{{gmcsf_36h_344}}', 'not measured', 'S02-F'],
        ['Lung CD11b⁺ dendritic cells, day 4', '{{cd11bdc_212}}', '{{cd11bdc_344}}', '{{cd11bdc_young}}', 'S01-E'],
        ['H5N1-cross-reactive CD8 T cells, day 14', '{{ifng14_212}}', '{{ifng14_344}}', '{{ifng14_young}}', 'S05-F'],
        ['Lowest body weight after dosing', '{{bw_nadir_212}}', '{{bw_nadir_344}}', '{{bw_nadir_young}}', 'S08-D'],
        ['Lung *Tnf* at the later time point (fold)', '{{c72_tnf_212}}', '{{c72_tnf_344}}', '{{c72_tnf_young}}', 'S09-A, second panel'],
        ['**Young animals**', '', '', '', ''],
        ['Survival, three mismatched-strain challenges', '{{young_212}}', '{{young_344}}', '', 'S09-B, S09-D, S09-F'],
        ['*Ifnb1* in lung at 16 h / 72 h (fold)', '{{ifn16_young}} / {{ifn72_young}}', '{{ifn16_344y}} / {{ifn72_344y}}', '', 'S01-A'],
        ['Body weight 14 days after a day-180 challenge', '{{bw180_212}}', '{{bw180_344}}', '', 'S09-G'],
    ], [40, 16, 16, 17, 25])
    return sub(r'''
# 3. PSLN-344 or PSLN-212

The two candidates contain the same agonist in the same liposome. The only difference is Mn²⁺ (annotation, Materials). Choosing between them is a decision about whether to include Mn²⁺.

''') + t + sub(r'''
Four points follow.

1. **In aged animals PSLN-344 is better on every efficacy and immune measure, by a wide margin.** Tolerability looks similar on body weight, but lung cytokine transcripts at the later time point are higher with PSLN-344 (*Tnf* {{c72_tnf_344}} versus {{c72_tnf_212}}-fold, *Il6* {{c72_il6_344}} versus {{c72_il6_212}}-fold) [S09-A].
2. **In young animals Mn²⁺ buys nothing we can measure.** Survival is identical. At the one late time point tested, PSLN-344 animals regained weight more slowly (one experiment). Mn²⁺ does raise and prolong the interferon response in young animals, which is added stimulation without added benefit. If a product for younger adults were ever wanted, the Mn²⁺-free particle would be the simpler candidate; that is the one reason to keep PSLN-212 on file.
3. **Most of the value sits in the Mn²⁺ step.** In aged mice, H1N1 HAI titers step from {{hai_h1_sham}} (sham) to {{hai_h1_cmp}} (cGAMP liposome) to {{hai_h1_212}} (PSLN-212) to {{hai_h1_344}} (PSLN-344) [S03-C]. The committee will ask whether we own that last step. The workbook cannot answer; Study A and a freedom-to-operate review (Section 6) are designed to.
4. **The vehicle's contribution is delivery, and it is only partly tested.** Liposomal dye reached {{int_srb2_a}} of type II lung epithelial cells against {{int_srb2_b}} for free dye [S01-B], and uptake by alveolar macrophages fell from {{int_did_a}} to {{int_did_b}} without surfactant proteins [S01-C]. The empty vehicle has no adjuvant effect of its own (sham, {{pool_sham_frac}} survivors). But no experiment gave the agonist without the vehicle, so what the vehicle adds to efficacy is inferred, not measured. Study A adds that arm.
''')


def sec_moa():
    bm = grid(['Use', 'Readout in mice (time after dose)', 'Aged PSLN-212 → PSLN-344 (young benchmark)', 'Clean split?', 'Counterpart in a clinical study'], [
        ['Did the dose engage the target?', '*Ifnb1* transcript in lung (16 h) [S01-A]', '{{ifn16_212}} → {{ifn16_344}} ({{ifn16_young}})-fold', SEP['ifn'], 'Interferon-signature genes or CXCL10 in blood or nasal fluid at 24 h'],
        ['', '*Gm-csf* transcript in lung (36 h) [S02-F]', '{{gmcsf_36h_212}} → {{gmcsf_36h_344}}-fold (no young arm)', SEP['gmcsf'], 'GM-CSF in nasal fluid'],
        ['Did antigen-presenting cells respond?', 'CD11b⁺ dendritic cells in lung (day 4) [S01-E]', '{{cd11bdc_212}} → {{cd11bdc_344}} ({{cd11bdc_young}})', SEP['dc'], 'Activation markers on blood monocytes (exploratory)'],
        ['', 'CCR7⁺ share of those cells (72 h) [S02-A]', '{{ccr7_212}} → {{ccr7_344}} ({{ccr7_young}})', SEP['ccr7'], 'As above'],
        ['Is T-cell help in place?', 'ICOS-high follicular helper T cells (day 7) [S04-A]', '{{tfh_212}} → {{tfh_344}} ({{tfh_young}})', SEP['tfh'], 'Circulating follicular helper T cells, day 7'],
        ['', 'Follicular regulatory share, lower is better (day 7) [S04-B]', '{{tfr_212}} → {{tfr_344}} ({{tfr_young}})', SEP['tfr'], 'Helper-to-regulatory ratio in blood'],
        ['Are B cells responding?', 'Germinal-center B cells (day 7) [S03-K]', '{{gc_212}} → {{gc_344}} ({{gc_young}})', SEP['gc'], 'Plasmablasts in blood, day 7'],
        ['Is antibody protective?', 'HAI titer, H1N1 and H3N2 (day 14) [S03-C, S03-G]', '{{hai_h1_212}} → {{hai_h1_344}} ({{hai_h1_young}}); {{hai_h3_212}} → {{hai_h3_344}} ({{hai_h3_young}})', SEP['hai1'] + '; ' + SEP['hai3'], 'HAI and neutralizing titer, day 28 (accepted immunogenicity endpoints)'],
        ['', 'IgG2a:IgG1 ratio (day 14) [S13-A, S13-B]', '{{sub_h1_212}} → {{sub_h1_344}} ({{sub_h1_young}})', SEP['sub'], 'IgG subclass profile'],
        ['Are cross-reactive T cells present?', 'H5N1-cross-reactive IFN-γ⁺ CD8 T cells (day 14; day 60) [S05-F, S05-G]', '{{ifng14_212}} → {{ifng14_344}} ({{ifng14_young}}); {{ifng60_212}} → {{ifng60_344}} ({{ifng60_young}})', SEP['ifng'] + '; ' + SEP['ifng60'], 'Interferon-γ T-cell response to conserved influenza proteins, day 14 to 28'],
        ['', 'Lung resident-memory CD8 T cells (day 25) [S05-I]', '{{trm_212}} → {{trm_344}} ({{trm_young}})', SEP['trm'], 'Research use only'],
    ], [18, 32, 30, 9, 29])
    return sub(r'''
# 4. Mechanism of action and biomarkers

## Mechanism

Figure 4 assembles the mechanism from the workbook. In short: the liposome delivers the agonist to alveolar macrophages and on to the lung epithelium, and the data are consistent with transfer through gap junctions. The resulting interferon and GM-CSF signals recruit monocytes and turn them into dendritic cells, which carry antigen to the lymph node and start the antibody and CD8 T-cell responses. Aging weakens the interferon signal, so in aged animals given PSLN-212 the monocytes accumulate as macrophages instead (one small experiment [S07-A]), regulatory T cells stay high in the lung ({{treg_212}}, against {{treg_344}} with PSLN-344 and {{treg_young}} in the young benchmark [S04-D]) and the response stalls. Adding Mn²⁺ restores the signal.
''') + fig(4, 'fig4_mechanism.png', 'Mechanism of action with the supporting numbers at each step. Blue boxes are supported by an intervention experiment; orange boxes only by comparing formulations.', '6.3in') + sub(r'''
How strong each link is:

- **Shown by intervention.** Uptake needs surfactant proteins ({{int_did_a}} of alveolar macrophages took up liposome in wild-type mice, {{int_did_b}} in knockouts) [S01-C]. Blocking gap junctions cuts monocyte recruitment from {{int_cbx_a}} to {{int_cbx_b}} [S11-C]. A CCR2 antagonist removes the monocytes ({{int_incb_mono_a}} to {{int_incb_mono_b}}) [S07-B] and with them the CD8 effector response ({{int_incb_gzmb_a}} to {{int_incb_gzmb_b}}, in young animals) [S02-I]. Bone marrow lacking the interferon receptor cannot produce monocyte-derived dendritic cells ({{int_ifnar_a}} to {{int_ifnar_b}}) unless GM-CSF is supplied ({{int_gmcsf_rescue_a}}) [S02-H]; monocyte entry itself did not clearly depend on that receptor ({{int_ifnar_mono_a}} versus {{int_ifnar_mono_b}}, three animals per arm) [S12-A]. Blocking cell migration stops T-cell priming in the lymph node ({{int_ptx_mln_a}} to {{int_ptx_mln_b}}) but not in the lung ({{int_ptx_lung_a}} versus {{int_ptx_lung_b}}) [S05-C].
- **Shown only by comparing formulations.** This covers the claim that Mn²⁺ is the cause of the higher interferon and GM-CSF, and every step from T-cell help onward.
- **Not tested.** The workbook has no arm with Mn²⁺ and no agonist, and no animals lacking STING. It does not show whether antibody, CD8 T cells or both are needed for protection, or why protection appears within 2 to 3 days, which is too early for antibody, yet requires the vaccine antigen [S15-H].
- **Weak point.** Co-stimulatory molecules on lymph-node dendritic cells reach only {{cd40_pct_young}} (CD40) and {{cd86_pct_young}} (CD86) of the young benchmark [S02-D]. If the aged response is still limited somewhere, the data point here.
- **Unusable.** The experiment meant to show which macrophage type drives regulatory T cells cannot be read, because both arms carry the same label [S07-C].

## Biomarkers to carry into the next studies

"Clean split" in the table means that no individual animal from a regimen that protects (PSLN-344 in aged, PSLN-212 in young) overlaps with any animal from a regimen that does not (sham and PSLN-212 in aged).

''') + bm + sub(r'''
Three cautions:

1. **These are group-level associations.** The animals that gave samples are not the animals that were challenged. Study A bleeds every animal the day before challenge, so that we can test whether an individual titer predicts an individual outcome.
2. **The usual HAI threshold of 1:40 does not discriminate here.** {{hai40_h1_212}} aged PSLN-212 animals reached 40 against H1N1 [S03-C], yet that regimen protected {{surv_S03-I_212}} against the matched virus [S03-I] (or 3/7 on the other reading of that experiment; D2 in Section 9). Every PSLN-344 animal was at {{hai_min_344}} or above and every PSLN-212 animal at {{hai_max_212}} or below. I would use 160 as the working threshold in mice until Study A refines it.
3. **Use the IgG2a:IgG1 ratio computed from the raw subclass titers,** not the printed ratio tables [S03-B, S03-F], whose column labels are rotated (D1 in Section 9).

Safety biomarkers for the same studies: body weight after dosing; lung *Tnf*, *Il6* and *Il10* at 72 hours and 7 days (the R848 combination that caused weight loss had *Tnf* at {{c72_tnf_r848combo}}-fold and *Il10* at {{c72_il10_r848combo}}-fold at the later time point, against {{c72_tnf_344}} and {{c72_il10_344}} for PSLN-344) [S09-A, S08-D]; brain transcripts with cholera toxin as the positive control [S10-A]; and tissue manganese, which is new.
''') + fig(5, 'fig5_tolerability.png', 'Tolerability data in the workbook. (a) PSLN-344 causes a small, transient weight dip; the R848 combination does not recover. (b) No brain signal at 36 hours relative to the positive control. (c) In aged mice several lung cytokines remain above baseline at the later time point.', '6.6in')


def sec_population():
    return sub(r'''
# 5. Target population, for the market-research check

**Primary population: adults aged 65 and over who are offered seasonal influenza vaccination.**

Why this group, from our data:

- The advantage of PSLN-344 over PSLN-212 exists only in aged animals: {{pool_344_frac}} versus {{pool_212_frac}} survived in aged mice, {{young_344}} versus {{young_212}} in young mice.
- The aged mice were 20 months or older. On the usual lifespan conversion that corresponds to people in their late 50s to late 60s and beyond (*external*: Jackson Laboratory equivalence, 18 to 24 months is roughly 56 to 69 years).
- It works in animals that had a previous influenza infection ({{imp_344_imp}} survived) [S06-E and S06-F, rows 71 to 98], which is the situation of every adult.

**Possible extension: adults aged 50 to 64.** In 14-month-old mice, roughly the human mid-40s, PSLN-212 had already failed in animals without prior infection ({{imp_212_naive}}) while PSLN-344 protected {{imp_344_naive}} [same blocks]. So the age at which the Mn²⁺ formulation becomes necessary lies below 14 months in mice. Study F locates it. Until then, treat 50 to 64 as upside and not as base case.

**Secondary use, bought by governments and not by the seasonal market: outbreak and pandemic response in older adults.** The support is protection 2 to 3 days after a single dose ({{early_344_frac}}), including against wild-type H5N1 ({{surv_S03-J_344}}) [S03-J, S06-B, S06-D].

**Adults under 50: a later option, not part of the core case.** Both formulations gave young mice full protection against mismatched strains ({{young_344}} each, against {{young_sham}} with sham) [S09-B, S09-D, S09-F], so a broader-acting intranasal vaccine could have value in this group too. But the case there is breadth, not rescue of a failing response; PSLN-344 has no advantage over PSLN-212; a cGAMP liposome also protected young animals ({{s13e_cmp}}, matched challenge) [S13-E]; and existing vaccines already work in young adults (*external*). Keep this group out of the base case.

**Outside the addressable market on current data:**

- children: there are no data;
- any use without a vaccine antigen: adjuvant alone protected {{s15h_adj}} [S15-H];
- any indication other than influenza, including oncology: there are no data.

**Deductions to apply inside the 65-and-over group** (assumptions that Studies B and C and the clinical program will confirm or remove):

- People with chronic lung disease such as asthma or COPD, at least at first, because the product acts in the airway and on current evidence needs to reach the lung.
- People in whom manganese clearance or neurological vulnerability is a concern, such as chronic liver disease or neurodegenerative disease, pending Study C.

One caveat applies to the whole population: all animals tested were female. Study A adds males.

**How the product reaches the patient.** It is an adjuvant and is only useful combined with an influenza antigen. The sizing should therefore be framed as a share of enhanced influenza vaccines for older adults, and should state whether we supply an adjuvant to a vaccine partner or a complete vaccine.

**Inputs market research will need that are not in our dataset:** number of people aged 65 and over by market; seasonal vaccination coverage in that group; the share already receiving enhanced vaccines (high-dose, adjuvanted, recombinant) and their price; acceptance of a nasal or inhaled route; and the 50 to 64 population as a separate line.

For orientation only (*external*, quoted from memory of public statistics, to be replaced by market research): about 60 million people aged 65 and over in the United States with seasonal influenza vaccine coverage near 70%, roughly 95 to 100 million in the European Union, and about 36 million in Japan.
''')


def sec_next():
    q = grid(['No.', 'Question the next studies must answer', 'Why it is open', 'Study', 'What counts as a pass at Gate 1'], [
        ['1', 'Are the existing results sound?', '{{n_disc}} discrepancies; two headline experiments with conflicting labels (Section 9).', 'Stage 0 audit', 'Every decision-critical block reconciled to raw records; the PSLN-344 advantage stands.'],
        ['2', 'Does the result reproduce under controlled conditions and in both sexes?', 'All animals female. No record of randomization or blinding. Seven per arm gives only {{power_n7_big}} power even for the difference observed.', 'A', 'Survival difference versus PSLN-212 of at least 40 points with a 95% confidence interval above zero; same direction in each sex.'],
        ['3', 'What does our agonist add beyond Mn²⁺?', 'No arm with Mn²⁺ and no agonist.', 'A', 'HAI titer with PSLN-344 at least 3 times that of the Mn²⁺-only particle.'],
        ['4', 'Is it safe, given that Mn²⁺ is delivered to the airway?', 'No tissue manganese, no pathology, one dose, 10 days of follow-up.', 'C', 'No manganese accumulation in brain or olfactory bulb and no treatment-related lesion at the intended dose; lung cytokines within 2-fold of baseline by day 7.'],
        ['5', 'Can it work in a form people can take?', 'Mechanism starts in the alveoli. One dose level. No human cells. In-house antigen.', 'B, D, E', 'Effect retained by a route usable in people, or an inhaled product accepted; activity on the common human STING variants; effect retained with a licensed antigen.'],
        ['6', 'Is it better than what older adults already get?', 'No comparison with high-dose or adjuvanted vaccines.', 'E', 'Not worse on HAI (lower 95% bound of the titer ratio above 0.5) and better on mismatched-strain protection.'],
        ['7', 'How long does it last, and from what age is it needed?', 'Aged animals tested only to day 60; {{untreated_dead_frac}} unchallenged aged animals died in the same window; PSLN-212 already fails at 14 months.', 'F', 'Sets dosing interval and lower age bound. A stop only if protection in aged animals is gone by day 120.'],
    ], [3, 25, 35, 9, 38])

    def study(rows):
        return grid(['Item', 'Specification'], rows, [22, 94])

    a = study([
        ['Must establish', '1. The advantage of PSLN-344 over PSLN-212 in aged mice reproduces under randomized, blinded conditions and in both sexes.\n2. How much of it requires our agonist and our vehicle, as opposed to Mn²⁺ alone.\n3. Whether an individual animal\'s antibody titer predicts its outcome.'],
        ['Population', 'BALB/c mice aged 20 months or older, males and females in equal numbers. One arm of young (8-week) mice as benchmark.'],
        ['Arms and comparators', 'One intranasal dose of the bivalent inactivated vaccine used in S03-A, with:\n1. empty liposome (sham);\n2. PSLN-212;\n3. PSLN-344;\n4. Mn²⁺ at matched dose in the same liposome without agonist, for example coordinated with an inactive nucleotide (new);\n5. PSLN-212 with free Mn²⁺ mixed in, not co-formulated (new);\n6. cGAMP liposome with Mn²⁺, if it can be made (new);\n7. free CDN-1807 with free Mn²⁺, no liposome (new; shows what the vehicle adds);\n8. young mice, PSLN-212;\n9. no vaccine, challenged;\n10. no vaccine, not challenged (background deaths).'],
        ['Primary endpoints', 'Survival to day 14 after challenge with matched H1N1 virus at 10 times the median lethal dose, given on day 14 (arm 3 versus arm 2). This repeats S03-I and settles discrepancy D2.\nHAI titer on day 13 (arm 3 versus arm 4).'],
        ['Other readouts', 'Body-weight loss; lung virus titer 3 and 5 days after challenge in satellite animals; neutralizing titer; IgG subclasses; IgA in nasal wash and lung lavage; day-13 titer against individual outcome.'],
        ['Group size', '17 per arm. That gives {{power_n17_rep}} power for survival of 78% versus 19%, the worst-case estimates from the existing data, and more than 90% power to detect a two-fold difference in HAI titer ({{n_hai2}} per arm are needed at the observed spread of {{sd_hai}} log2 units). For survival alone, arm 3 versus arm 4 has {{power_n17_attr}} power if the Mn²⁺-only particle protects 40%. About 155 aged mice plus 40 satellites.'],
        ['Timing', 'Dose on day 0, bleed on day 13, challenge on day 14, satellites on days 17 and 19, end on day 28. January to May 2027.'],
        ['Decision rule', 'Pass if the survival difference between arms 3 and 2 is at least 40 points with a 95% confidence interval above zero, the direction is the same in each sex, and the HAI titer in arm 3 is at least 3 times that in arm 4. If arm 4 matches arm 3, the agonist is not earning its place: stop or re-scope.'],
    ])
    b = study([
        ['Must establish', '1. Whether the dose has to reach the deep lung or whether the nose is enough.\n2. The lowest effective dose.\n3. Whether a second dose helps.'],
        ['Population', 'BALB/c mice aged 20 months or older, both sexes. 11 per arm for antibody, 5 per arm for early transcripts.'],
        ['Arms and comparators', 'Route, PSLN-344 at 20 µg with vaccine: (a) the current instillation method; (b) low-volume, nose-only dosing; (c) direct dosing to the lung.\nDose, by the best route: 2.5, 5, 10, 20 and 40 µg.\nRegimen: one dose versus two doses three weeks apart.\nComparators: sham; PSLN-212 at 20 and 40 µg.'],
        ['Primary endpoint', 'HAI titer 14 days after the last dose.'],
        ['Other readouts', 'Where the dose lands (labeled liposome in nose and lung at 1 hour); *Ifnb1* and *Gm-csf* in lung and nasal tissue at 16 hours, 72 hours and 7 days; body weight; survival after mismatched-strain challenge for the selected route and dose.'],
        ['Timing', 'February to June 2027.'],
        ['Decision rule', 'Selects route and dose for Study C and the ferret study. If nose-only dosing gives less than half the HAI titer of lung-reaching dosing, the product is an inhaled vaccine, and the committee decides at Gate 1 whether that is a product it wants.'],
    ])
    c = study([
        ['Must establish', '1. That manganese does not accumulate in the olfactory system or brain.\n2. That lung inflammation resolves.\n3. That there is no nasal, lung or nerve pathology.\n4. The margin between the intended dose and the first adverse finding.'],
        ['Population', 'BALB/c mice aged 20 months or older, both sexes, 6 per arm at each necropsy time. A smaller set of young adults for comparison.'],
        ['Arms and comparators', 'Buffer; empty liposome; Mn²⁺ liposome without agonist; PSLN-212; PSLN-344 at the intended dose (20 µg) and at 3 times that dose. Each as a single dose and as three doses two weeks apart. Cholera toxin as positive control for the brain-transcript assay, as in S10-A.'],
        ['Primary endpoints', 'Manganese content of olfactory bulb, striatum, cerebellum, lung and liver at 24 hours, 7 days and 28 days after the last dose. Histopathology of nasal cavity, olfactory bulb, brain, facial nerve and lung.'],
        ['Other readouts', 'Cell counts in lung lavage including neutrophils (replaces S11-B); lung *Ifnb1*, *Tnf*, *Il6* and *Il10* at 16 hours, 72 hours, 7 days and 14 days; brain *Ifnb1*, *Tnf* and *Isg15* at 36 hours and 7 days; daily body weight; sense of smell and motor function; serum chemistry.'],
        ['Timing', 'February to August 2027.'],
        ['Decision rule', 'Pass if, at the intended dose after three doses, tissue manganese is back within the range of the buffer group by day 28, there is no treatment-related lesion, lung cytokines are within 2-fold of baseline by day 7, and weight loss is no more than 5% and recovered by day 10.'],
    ])
    d = study([
        ['Must establish', 'That CDN-1807, with and without Mn²⁺, activates human STING including its common variants, and that Mn²⁺ helps cells from older donors as it helps aged mice.'],
        ['Test systems', 'Reporter cells carrying each common human STING variant. Blood monocytes and monocyte-derived macrophages from 12 donors aged 18 to 40 and 12 donors aged 65 or over. Human alveolar macrophages or lung slices if they can be obtained.'],
        ['Comparators', 'cGAMP; CDN-1807 alone; Mn²⁺ alone; CDN-1807 with Mn²⁺; PSLN-212; PSLN-344; empty liposome.'],
        ['Readouts', 'Interferon-β, CXCL10, IL-6, TNF and GM-CSF protein at 6 and 24 hours; interferon-stimulated gene expression; cell viability; concentration giving half-maximal response for each variant.'],
        ['Timing', 'December 2026 to May 2027.'],
        ['Decision rule', 'Pass if PSLN-344 induces interferon-β in cells carrying each common variant and the Mn²⁺ effect is present in cells from older donors. No activity on a common variant narrows or ends the program.'],
    ])
    e = study([
        ['Must establish', 'That the adjuvant works with a licensed type of antigen, and how vaccine with PSLN-344 compares with the enhanced vaccines older adults already receive.'],
        ['Population', 'BALB/c mice aged 20 months or older, both sexes, 17 per arm. Young benchmark arm.'],
        ['Arms and comparators', 'Intranasal: licensed split or subunit antigen alone; the same with PSLN-344; in-house whole-virus antigen with PSLN-344 (bridge to the existing data).\nIntramuscular: standard-dose antigen; four-fold (high-dose) antigen; antigen with an oil-in-water emulsion adjuvant of the MF59 type.'],
        ['Primary endpoint', 'HAI titer on days 14 and 28, H1N1 and H3N2.'],
        ['Other readouts', 'Neutralizing titer; IgA in nasal wash and lung lavage; cross-reactive CD8 T cells; survival, weight loss and lung virus titer after mismatched-strain challenge.'],
        ['Timing', 'March to August 2027.'],
        ['Decision rule', 'Pass if intranasal PSLN-344 with licensed antigen is not worse than the intramuscular enhanced comparators on HAI (lower 95% bound of the titer ratio above 0.5) and is better on mismatched-strain protection.'],
    ])
    f_ = study([
        ['Must establish', '1. How long protection lasts in aged animals once background deaths are accounted for.\n2. From what age PSLN-212 stops working, which sets the lower age bound of the market.'],
        ['Population', 'BALB/c mice vaccinated at 6, 12 and 16 to 18 months, both sexes, so that the day-180 challenge falls before 24 months of age.'],
        ['Arms and comparators', 'PSLN-344; PSLN-212; sham; no vaccine, challenged; no vaccine, not challenged (30 animals, to estimate background deaths).'],
        ['Primary endpoint', 'Lung virus titer 4 days after mismatched-strain challenge on days 60, 120 and 180.'],
        ['Other readouts', 'Weight loss; survival as a secondary endpoint, because {{untreated_dead_frac}} unchallenged aged animals died in the existing data; HAI titer on days 14, 60, 120 and 180; cross-reactive CD8 T cells and lung resident memory at each challenge time.'],
        ['Timing', 'February to September 2027. Day-60 and day-120 results arrive well before Gate 1 and the day-180 result just ahead of it.'],
        ['Decision rule', 'Sets the dosing interval and the lower age bound. Stops the program only if protection in aged animals is gone by day 120.'],
    ])
    later = grid(['Study', 'Population', 'Comparators', 'Endpoints and readouts', 'Timing'], [
        ['G. Ferret immunogenicity and challenge', 'Ferrets of both sexes, including animals previously infected with a different strain.', 'Intranasal antigen alone; antigen with PSLN-344 at two doses; intramuscular enhanced vaccine; mock.',
         'Primary: virus in nasal washes over days 1 to 7 after mismatched-strain challenge. Also HAI and neutralizing seroconversion on day 28, fever, weight, lung pathology on day 4.', 'November 2027 to August 2028'],
        ['GLP toxicology', 'Species and design agreed with the regulator; adjuvant-alone arms included.', 'Vehicle; antigen alone.',
         'Repeat-dose toxicity with one dose more than the clinical schedule, local tolerance, manganese distribution, recovery group.', 'January to October 2028'],
        ['Clinical batch', 'Not applicable.', 'Not applicable.', 'Scale-up, release testing, stability.', 'November 2027 to October 2028'],
        ['H. Phase 1', 'Healthy adults aged 18 to 49 first, then adults aged 65 to 80 without chronic lung disease.', 'Intranasal licensed antigen alone; intramuscular enhanced vaccine.',
         'Primary: solicited reactions on days 0 to 7, adverse events to day 28, serious events and events of special interest (facial palsy, change in sense of smell, wheeze, neurological symptoms) to day 180, blood manganese.\n'
         'Secondary: HAI and neutralizing titers on days 28 and 180; nasal IgA.\nExploratory: blood interferon signature at 24 hours; circulating follicular helper T cells and plasmablasts on day 7; interferon-γ T-cell response to conserved antigens on days 14 to 28.', '2029'],
    ], [18, 22, 21, 39, 14])
    return sub(r'''
# 6. Next steps

The next studies have to answer seven questions. They are listed in the order in which an answer would move the decision.

''') + q + fig(6, 'fig6_timeline.png', 'Indicative timeline. Stage 0 and Stage 1 are what this proposal asks the committee to approve.', '6.6in') + sub(r'''
**Standards for every Stage 1 animal study.** Each study uses both sexes, randomizes animals to arms and scores outcomes blind. Each has one primary endpoint and an analysis plan fixed in advance, with titers analyzed on the log scale and survival by exact tests. Each animal keeps one identifier across every table. Where they answer the question, virus load and weight loss are used as endpoints in preference to death.

**Critical path.** The supply of mice aged 20 months or older, in both sexes, sets the schedule. The timeline assumes they are available from January 2027.

## Stage 0. Data audit and dataset lock (November to mid-December 2026)

This stage uses no animals. It closes discrepancies D1 to D20 (Appendix A) against plate-reader files, flow-cytometry exports, balance records and animal-room records. It records for each experiment whether it was repeated, randomized and scored blind. It ends with the workbook and its annotation reissued as one locked version and this analysis rerun on it; the scripts are supplied. The stage is passed if every decision-critical block is reconciled and the survival difference between PSLN-344 and PSLN-212 in aged mice is still at least 40 points.

## Study A. Replication and attribution in aged mice

''') + a + sub(r'''
## Study B. Delivery route and dose

''') + b + sub(r'''
## Study C. Pilot safety and manganese distribution

''') + c + sub(r'''
## Study D. Activity in human cells

Human STING exists in several common variants that respond differently to some cyclic dinucleotides, and an earlier STING agonist that worked in mice failed in patients because it did not bind the human protein (*external*). Nothing in the workbook addresses this.

''') + d + sub(r'''
## Study E. Licensed antigen and benchmark against enhanced vaccines

''') + e + sub(r'''
## Study F. Durability and age range

''') + f_ + sub(r'''
## Formulation and intellectual-property workstream (December 2026 to September 2027)

This workstream has to deliver:

- the manganese content per dose, and how much of it is free;
- particle size and charge, which the annotation says were measured but which are not in the workbook;
- a potency assay in reporter cells that can be used for batch release;
- stability of the freeze-dried product at −20 °C, 2 to 8 °C and 25 °C over six months;
- compatibility with licensed antigen;
- a clear definition of what "20 µg of adjuvant" refers to;
- a freedom-to-operate review for particles that combine a cyclic dinucleotide with manganese. Published work from other groups exists (*external*, to be checked by counsel).

## Gate 1, October 2027

Proceed to Stage 2 only if all of the following hold:

1. The audited dataset still shows the PSLN-344 advantage (Stage 0).
2. Study A reproduces it in both sexes.
3. PSLN-344 beats the Mn²⁺-only particle by at least 3-fold on HAI titer (Study A).
4. No manganese accumulation, no lesions, and resolving lung inflammation at the intended dose (Study C).
5. A delivery route usable in people is identified, or the committee accepts an inhaled product (Study B).
6. The agonist is active on the common human STING variants (Study D).
7. With a licensed antigen, PSLN-344 is not worse than enhanced intramuscular vaccines on HAI and is better on mismatched-strain protection (Study E).

## Stage 2 and Stage 3, only if Gate 1 is passed

''') + later + sub(r'''
The events of special interest in Phase 1 reflect two known hazards of this route (*external*): an earlier intranasal influenza vaccine with a bacterial-toxin adjuvant was withdrawn after cases of facial palsy, and manganese delivered to the nose can travel along the olfactory nerve to the brain.
''')


def sec_drop():
    t = grid(['What we would be giving up', 'Evidence', 'Caveat'], [
        ['The only formulation in the dataset that protects aged animals', '{{pool_344}} alive versus {{pool_212}} with PSLN-212 and {{pool_sham}} with sham, over 11 experiments (Figure 1).', 'Mice only; audit pending.'],
        ['Near-young antibody responses in aged animals after one needle-free dose', 'HAI at {{hai_h1_vs_young_pct}} and {{hai_h3_vs_young_pct}} of the young benchmark; {{hai160_344}} values at 160 or above, against {{hai160_212}} with PSLN-212 [S03-C, S03-G].', 'In-house antigen; 5 animals per group.'],
        ['Protection against strains the vaccine does not match, including H5N1', '{{het_344}} against mismatched strains [S06-A to S06-G]; {{surv_S03-J_344}} against wild-type H5N1 [S03-J].', 'Identity of the H5N1 control arms is uncertain (D3, Appendix A).'],
        ['Protection within 2 to 3 days of one dose', '{{early_incl_s15h}} across four experiments [S03-J, S06-B, S06-D, S15-H].', 'Mechanism not explained.'],
        ['Activity in animals with prior influenza infection', '{{imp_344_imp}} previously infected animals survived; PSLN-212 {{imp_212_imp}} [S06-E and S06-F, rows 71 to 98].', 'One experiment per challenge virus.'],
        ['A mechanism with intervention evidence and a working biomarker set', 'Figure 4 and Section 4.', 'Downstream steps are associations.'],
        ['Cross-strain protection in young animals that lasts six months', '{{young_344}} with either formulation against {{young_sham}} with sham, including a challenge 180 days after one dose [S09-B, S09-D, S09-F].', 'Not specific to PSLN-344; PSLN-212 does the same.'],
        ['Consistency across three mouse strains', '{{strains_344_frac}} in C57BL/6 and Swiss Webster [S15-L, S15-N].', 'Challenge virus not recorded (D17, Appendix A).'],
    ], [34, 56, 24])
    return sub(r'''
# 7. If we drop the program: what we give up, and why we might

''') + t + sub(r'''
**What we would not be giving up.** A stand-alone STING drug: adjuvant alone protected {{s15h_adj}} [S15-H]. A differentiated position in younger adults: there PSLN-344 adds nothing over PSLN-212, and a cGAMP liposome also protected ({{s13e_cmp}}) [S13-E]. Any human or formal safety data: there are none.

**Reasons the committee could legitimately drop it.**

- It does not want to fund a vaccine-type development path. An adjuvant needs an antigen partner, and an intranasal vaccine for older adults is likely to need a trial with a clinical endpoint (my judgment, to be confirmed with regulators).
- The value currently rests on Mn²⁺, and both its ownership and its safety are open.
- The audit or any Gate 1 criterion fails.

I have no cost figures. The committee should set the cost of Stage 1 against the list above: dropping now gives up these results before the first three questions in Section 6 have been asked, and those three can be answered by mid-2027.
''')


def sec_ruled_out():
    t = grid(['Option considered', 'Why I ruled it out', 'Source'], [
        ['Lead with PSLN-212 (simpler, no Mn²⁺)', 'Fails in older animals, where the need is greatest: {{pool_212}} survival in aged mice and HAI about a tenth of the young benchmark. Already fails at 14 months ({{imp_212_naive}} in animals without prior infection).', 'Figure 1; S03-C, S03-G; S06-E and S06-F rows 71 to 98'],
        ['Give more PSLN-212', 'Interferon induction by PSLN-212 levels off: 40 µg gives {{dose_212_40}}-fold, less than PSLN-344 at 10 µg ({{dose_344_10}}-fold).', 'S08-A'],
        ['Give PSLN-212 twice', 'IgG after two doses of PSLN-212 ({{boost_h1_212}} H1N1, {{boost_h3_212}} H3N2, day 28) is below IgG after one dose of PSLN-344 ({{igg_h1_344}}, {{igg_h3_344}}, day 14). No challenge data after a boost.', 'S13-I, S13-J; S03-A, S03-E'],
        ['Add a TLR7/8 agonist (R848)', 'Not tolerated: weight still falling at day 10 ({{bw_d10_r848combo}}), {{bw_lt90_r848combo}} animals below 90%, and one of five has no day-10 value. Lung *Tnf* {{c16_tnf_r848combo}}-fold at 16 hours. No gain in interferon over PSLN-344 ({{ifn16_r848combo}} versus {{ifn16_344}}-fold).', 'S08-D; S09-A; S01-A'],
        ['Use cGAMP in place of CDN-1807', 'About half the response in aged mice: *Ifnb1* {{ifn16_cmp}} versus {{ifn16_212}}-fold, HAI {{hai_h1_cmp}} versus {{hai_h1_212}}. Its real value is as a control: a cGAMP particle with Mn²⁺ is arm 6 of Study A.', 'S01-A; S03-C'],
        ['Rescue PSLN-212 with recombinant GM-CSF', 'Raises monocyte-derived dendritic cells from {{int_gmcsf_add_b}} to {{int_gmcsf_add_a}}, which supports the mechanism, but needs four daily doses of a protein and has no efficacy data.', 'S02-G'],
        ['Use PSLN-344 alone as an antiviral', 'No protection without antigen: {{s15h_adj}}.', 'S15-H'],
        ['Position PSLN-344 for all adults from the start', 'In young animals it adds nothing over PSLN-212 ({{young_344}} versus {{young_212}}) and prolongs the interferon response. The differentiated case is in older adults; younger adults stay a later option.', 'S09-B, S09-D, S09-F; S01-A'],
        ['Go straight to IND-enabling work', 'The control that shows what our agonist adds is missing, there is no safety package for Mn²⁺, no human-cell data, and the dataset has {{n_disc}} open discrepancies.', 'Sections 6 and 9'],
        ['Drop now', 'The effect is large, consistent across 11 experiments and robust to the data problems. The questions that could end the program can be answered in mouse and cell studies by October 2027, before any IND-enabling spend.', 'Sections 2 and 7'],
    ], [26, 62, 26])
    return sub(r'''
# 8. What I considered and ruled out

''') + t + sub(r'''
**Readings of the data that I ruled out**, because each would have led to a wrong number (IDs refer to the discrepancy log in Appendix A):

- Taking the IgG2a:IgG1 ratio from S03-B and S03-F as printed. It would show PSLN-344 at {{sub_h1_344_printed}} instead of {{sub_h1_344}} (D1).
- Treating the "Untreated" groups as infected controls. They were not challenged (D4).
- Reading S09-A on a linear scale. It is log10 (D6).
- Averaging body weights as printed. Dead animals carry their last value forward in some groups (D8).
- Using the neutrophil block S11-B, the macrophage-transfer block S07-C, the tetramer blocks S05-A and S05-B, or the unlabeled region of S08 (D7, D12, D13, D15).
- Claiming that PSLN-344 beats PSLN-212 against wild-type H5N1. The paired weight table suggests there may have been no PSLN-212 arm in that experiment (D3).
- Pooling the young benchmark with aged animals as if it were an age-matched control. It is a benchmark for what a full response looks like, nothing more.
''')


def sec_integrity():
    short = {
        'D1': ('The IgG2a:IgG1 tables S03-B and S03-F carry rotated column labels.', 'PSLN-344 would show a ratio of {{sub_h1_344_printed}} instead of {{sub_h1_344}}.', 'Ratios recomputed from the raw subclass titers S13-A to S13-D.'),
        'D2': ('Matched-strain challenge: the survival table S03-I and its body-weight table S13-F list different groups.', 'PSLN-212 is {{surv_S03-I_212}} in one table and 3/7 in the other. PSLN-344 is {{surv_S03-I_344}} in both.', 'Both readings carried; the less favorable one is used in the worst-case analysis.'),
        'D3': ('Wild-type H5N1 challenge: S03-J and its body-weight table S13-G list different groups; stated n is 9 in one and 10 in the other; one day value is missing.', 'The arm printed as PSLN-212 may be a sham arm.', 'PSLN-344 result ({{surv_S03-J_344}}) used; no claim made against PSLN-212 from this experiment.'),
        'D4': ('"Untreated" groups in the day-60 blocks received no virus.', 'Read as infected controls they would make PSLN-344 look no better than no treatment.', 'Used as background mortality: {{untreated_dead_frac}} died in two weeks.'),
        'D7': ('The neutrophil block S11-B shares {{s11_same}} values with the alveolar-macrophage block S11-A.', 'A lung-safety readout would be taken from duplicated data.', 'S11-B excluded. There are no usable neutrophil data.'),
        'D9': ('Identical body-weight series recur in different experiments, for example {{dup_s15c_s15i}} cells between S15-C and S15-I.', 'Weight curves would be presented as independent confirmation when part of the data is shared.', 'Body weight used as supporting evidence only; survival tables are the primary record.'),
    }
    t = grid(['ID', 'Discrepancy', 'Effect if taken at face value', 'What I did'], [[k, v[0], v[1], v[2]] for k, v in short.items()], [4, 42, 34, 32])
    lim = '\n'.join(f'- {x}' for x in DESIGN_LIMITS)
    return sub(r"""
# 9. State of the data

I parsed all {{n_numeric}} numeric cells into {{n_blocks}} blocks and ran four checks: stated group size against the values present; every derived table recomputed from its raw table; every survival table against its paired body-weight table; and a scan for number sequences that recur between blocks. That produced {{n_disc}} discrepancies, all listed with their evidence in Appendix A. I describe them as discrepancies in the files. I have not seen the raw records and draw no conclusion about how they arose.

The {{n_disc_high}} below would change a number the committee sees if taken at face value.

""") + t + sub(r"""
**Does any of this change the recommendation?** No, for three reasons.

1. With every survival-versus-weight conflict resolved against PSLN-344 and the disputed PSLN-212 arm of the H5N1 experiment removed, survival is {{sens_worst_344}} versus {{sens_worst_212}}.
2. Restricting to the three experiments in which the survival table and the weight table agree for every arm and the design is fully recorded [S06-A, S06-B, S06-F], it is {{strict_344}} versus {{strict_212}}.
3. The antibody results come from raw titers in blocks whose group sizes match their labels and in which the only repeated values are coincident dilution steps [S03-A, S03-C to S03-E, S03-G, S03-H, S13-A to S13-D].

What the discrepancies do change is how much weight any single experiment can bear. They are the reason the first step I propose is an audit.

**Limits of the dataset that are not errors:**

""") + lim + '\n'


def sec_log():
    parts = []
    for e in LOG:
        parts.append(f"**{e['id']}. {e['title']}** ({e['rank']}; {e['blocks']}). {e['finding']} *Why it matters:* {e['face']} *What I did:* {e['handling']} *For the audit:* {e['audit']}\n")
    return sub(r"""
# Appendix A. Discrepancy log

Each entry gives the evidence, why it matters, how I handled it in this analysis, and what the audit should close. Rank reflects how far the discrepancy could move a number the committee sees. The same log, with one row per entry, is in the sheet "Integrity_log" of `PSLN_evidence_tables.xlsx`.

""") + sub('\n'.join(parts))


def sec_appendix():
    from facts import AGED11
    A10 = [b for b in AGED11 if b != 'S03-J']
    SETS = {tuple(AGED11): 'the 11 survival blocks shown in Figure 1',
            tuple(A10): 'the 10 survival blocks of Figure 1 that include a young arm (all except S03-J)',
            tuple(AGED11 + ['S13-F', 'S13-G', 'S15-A..G', 'S15-M', 'S15-O']): 'the 11 survival blocks of Figure 1 and their paired body-weight blocks (S13-F, S13-G, S15-A to S15-G, S15-M, S15-O)',
            ('S06-A', 'S06-B', 'S06-C', 'S06-D', 'S06-E_r34', 'S06-F_r34', 'S06-G'): 'S06-A to S06-D, S06-E and S06-F (rows 34-68), S06-G',
            ('S13-F', 'S15-A', 'S15-B', 'S15-C', 'S15-D', 'S15-E', 'S15-F', 'S15-G', 'S15-M', 'S15-O'): 'body-weight blocks S13-F, S15-A to S15-G, S15-M, S15-O'}
    def tidy(x):
        return x.replace('_16h', '').replace('_72h', '').replace('_r34', ' (rows 34-68)').replace('_r71', ' (rows 71-98)').replace('_panel1', ' (first panel)').replace('_panel2', ' (second panel)')
    rows = []
    for i, k in enumerate(USED, 1):
        fct = FACTS[k]
        key = tuple(fct['blocks'])
        if key in SETS:
            src = SETS[key]
        else:
            blocks = ', '.join(tidy(b) for b in fct['blocks']) if fct['blocks'] else 'design calculation'
            cells = fct['cells']
            generic = cells in ('all group ranges of the listed blocks', 'n/a', 'n/a (design calculation)', 'all', 'survival and paired weight blocks') or cells.startswith('see ')
            src = blocks if generic else f"{blocks}: {cells}"
        rows.append([str(i), fct['text'], fct['what'], src, fct['method'] + ' [`' + fct['script'].replace(' / ', '`, `').replace(' + ', '`, `') + '`]'])
    t = grid(['No.', 'Number as quoted', 'What it is', 'Source blocks and cells', 'How computed [script]'], rows, [3, 18, 34, 27, 32])
    return sub(r'''
# Appendix B. Source and calculation for every number quoted

Numbers are listed in the order in which they first appear. Cell ranges use workbook notation (sheet!range). Where a number pools several blocks, the blocks are listed and the per-block values are in the sheet "Survival" or "Serology" of the accompanying evidence workbook (`PSLN_evidence_tables.xlsx`). Scripts are in the folder `analysis`.

''') + t + sub(r'''
# Appendix C. Methods

**Parsing.** Each block was defined by hand from the printed layout, so that every value keeps its cell address. All {{n_numeric}} numeric cells are accounted for (`01_parse_workbook.py`). Labels were taken as printed; nothing was relabeled.

**Survival.** Time-to-event blocks store one row per animal with a day and a code. Comparison with the paired body-weight blocks confirms that 1 means death or humane endpoint on that day and 0 means alive at the end of observation. Survival proportions carry exact (Clopper-Pearson) 95% confidence intervals. Two-arm comparisons use the two-sided Fisher exact test. The pooled comparison is stratified by experiment: a Mantel-Haenszel difference in survival, and a log-rank test whose reference distribution comes from permuting labels within each experiment (200,000 permutations). Pooling across experiments with different viruses and intervals is a summary, not a claim that the experiments are replicates; Figure 1 shows each one (`06_survival.py`). The stratified log-rank statistic, the pooled Fisher test and one titer ratio were recomputed independently in R and agree (`crosscheck_in_R.R`).

**Titers and fold-changes.** These were analyzed on the log scale. Summaries are geometric means and ratios of geometric means, with 95% confidence intervals from Welch's t-test. HAI values recorded as 0 were set to 5, half the lowest dilution tested. S09-A is stored as log10 and was back-transformed (`07_immunogenicity_moa.py`, `08_safety_tolerability.py`).

**Percentages from flow cytometry.** These are summarized as arithmetic means and compared with Welch's t-test; exact Mann-Whitney p-values are in the evidence workbook. With 5 animals per group the smallest attainable exact p-value is 0.008. Holm's method was applied across the {{holm_n}} comparisons of PSLN-344 with PSLN-212 in aged animals.

**Body weight.** Trailing repeated values (three identical final cells, or two below 90%) and blank cells were treated as end of observation. Body weight was used as supporting evidence only (`03_weight_vs_survival.py`, `08_safety_tolerability.py`).

**Gap closed (Figure 3).** This is (PSLN-344 aged minus PSLN-212 aged) divided by (PSLN-212 young minus PSLN-212 aged), computed on the log scale for titers, ratios and fold-changes (`12_fig3_restoration.py`).

**Integrity checks.** The checks were: stated versus observed group size (`02_n_audit.py`); survival versus weight tables (`03_weight_vs_survival.py`); repeated sequences (`04_duplicate_scan.py`, `04b_weight_trajectory_dups.py`); derived versus raw tables and scale checks (`05_derived_value_checks.py`).

**Sample sizes for proposed studies.** These use the exact power of the two-sided Fisher test for survival, and a t-test on log2 titers for HAI with the spread observed in S03-C and S03-G (`09_biomarkers_power.py`).

**What was not done.** No value was imputed, relabeled or excluded as an outlier. No raw instrument file was available, so none of the discrepancies could be resolved, only bounded.
''')


def build_markdown():
    body = sec_front() + sec_asset() + sec_choice() + sec_moa() + sec_population() + PB + sec_next() + sec_drop() + sec_ruled_out() + PB + sec_integrity()
    return body + PB + sec_log() + PB + sec_appendix()
