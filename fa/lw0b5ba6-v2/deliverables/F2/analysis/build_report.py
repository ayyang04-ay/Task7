import pandas as pd, numpy as np, os, sys
from docengine import Doc
_LED = pd.read_csv('evidence_ledger.csv', dtype=str, keep_default_na=False)      # written by ledger_numbers.py
N = dict(zip(_LED.Key, _LED.Value_as_cited))
USED = {}
SECTION = ['front']
def n(key):
    if key not in N: raise KeyError(key)
    USED.setdefault(key, SECTION[0]); return N[key]
def sec(name): SECTION[0] = name
def pc(key): return n(key).split('(')[1].rstrip(')')       # "56/66 (85%)" -> "85%"
OUTDIR = os.environ.get('PSLN_OUT', '/tmp/outputs')
FIG = os.path.join(OUTDIR, 'figures') + '/'
D = Doc()
q = pd.read_csv('qc_log.csv')

# =====================================================================================================
sec('§1')
D.title('PSLN program: portfolio recommendation and next-step proposal',
        'PSLN-344 and PSLN-212 (CDN-1807 STING-agonist liposomes) · portfolio review · 1 November 2026',
        f'Basis: psln_program_dataset.xlsx (15 sheets, {n("cells_total")} numeric cells, last modified 3 September 2026) and psln_program_annotation.pdf (15 September 2026); nothing later is included. '
        'Every efficacy, safety and mechanism number is computed from that workbook: source blocks are in square brackets, cell ranges and methods in Appendix B and the evidence workbook. '
        'Statements marked *external* are general knowledge, not our data; check them before use.')
D.h1('1. Recommendation')
D.lead('Keep the program, with one lead and a gated budget. Take PSLN-344 forward. Stop developing PSLN-212 as a candidate and keep it only as the manganese-free comparator. '
       'Approve the work up to Gate 1 (October 2027) now; release nothing beyond it until the criteria in Section 2 are met.')
D.p(f'**What the asset is.** The data do not describe a stand-alone STING-agonist drug. They describe a vaccine adjuvant: the cyclic dinucleotide CDN-1807 in a lung-surfactant-like liposome, '
    f'with Mn²⁺ (PSLN-344) or without it (PSLN-212), given into the airway of mice together with inactivated influenza vaccine. Given without vaccine, PSLN-344 protected {n("h_adj")} aged animals; '
    f'vaccine alone protected {n("h_vac")}; the two together {n("h_both")} [S15-H]. All data are from mice.')
D.p('**How it looks.** Promising but not yet decision-grade: a large and consistent survival benefit in aged mice, inside a mouse-only package with real gaps in safety, comparators and data hygiene.')
D.bullets([
    f'**The efficacy signal in aged animals is large and consistent.** Across the nine lethal-challenge experiments in aged BALB/c mice, vaccine + PSLN-344 left {n("survA_344")} alive, against {n("survA_212")} '
    f'for PSLN-212 and {n("survA_sham")} for vaccine + empty liposome; hazard ratio for death against PSLN-212, {n("hr_A")} [S03-I, S03-J, S06-A–G]. Removing the duplicated experiment and the two whose comparator arms are uncertain gives '
    f'{n("survB_344")} against {n("survB_212")}; reading every remaining disagreement in the records against PSLN-344 gives {n("survF_344")} against {n("survF_212")}.',
    f'**The advantage exists only in aged animals.** In young mice both candidates gave {n("y344")} survival [S09-B, S09-D, S09-F]. The case for PSLN-344 is therefore a case for an older-adult vaccine.',
    f'**The mechanism is coherent and measurable.** Mn²⁺ returns the interferon-β response of aged lung to the young level ({n("ifn16_344")}-fold against {n("ifn16_212")}-fold; young {n("ifn16_young")}-fold) [S01-A] '
    f'and switches on GM-CSF ({n("gm_344_36h")}-fold against {n("gm_212_36h")}-fold at 36 h) [S02-F]. Downstream, PSLN-344 brought aged animals closer to the young benchmark than PSLN-212 in '
    f'{n("ri_closer")} of {n("ri_n")} immune read-outs; where aged animals fall short of young ones, it reached a median {n("ri_def_med344")} of the young value against {n("ri_def_med212")} (Figure 3).'])
D.p('**Why the approval should be conditional.**')
D.bullets([
    f'**The data file is not yet committee-grade.** I raised {n("qc_n")} data-quality flags, {n("qc_high")} of them serious: two blocks with rotated column headers, two nominally different survival experiments with identical data, '
    f'a mislabelled time point, a neutrophil data set that duplicates another block, recycled body-weight traces, and survival and weight blocks that disagree in {n("qc_mismatch_n")} groups (Section 3.4, Appendix A). '
    'None reverses the headline result, but they must be settled from source records before anyone outside the project relies on the file.',
    '**There is no comparison with what older adults already receive.** Every comparator is our own material or an empty liposome: no intramuscular arm, no high-dose antigen, no licensed adjuvant.',
    '**Attribution is open.** No experiment tests manganese in the liposome without CDN-1807, or free CDN-1807. We cannot yet say the STING agonist is needed once manganese is present.',
    f'**Safety evidence is thin where it matters most.** Manganese is delivered to the nose and lung, yet no block reports how much manganese is given or where it goes. Brain read-outs are three transcripts at one time point [S10-A]. '
    f'Lung *Il6*, *Tnf* and *Ccl2* are still {n("cyt_Il6_344_72h")}, {n("cyt_Tnf_344_72h")} and {n("cyt_Ccl2_344_72h")} control at 72 h, the last time point [S09-A]. There is no histopathology, and the neutrophil block is unusable.',
    '**Translation is untested.** No male animals, no second species, no human cells; and the site of action is the alveolus, which a human nasal spray largely does not reach (*external*).'], numbered=True)
D.table('Table 1. How the asset looks today',
  ['Dimension', 'Assessment', 'Basis in our data'],
  [['Efficacy in aged hosts', '**Strong signal**', f'{n("survA_344")} vs {n("survA_212")} survival; PSLN-344 ahead in {n("h2h_ahead")} head-to-head experiments; three mouse strains [S03-I/J, S06, S15-L/N]'],
   ['Advantage in young hosts', '**None shown**', f'{n("y344")} vs {n("y212")} survival; interferon-β {n("ifn16_yfold")}; no difference in dendritic-cell read-outs; slower recovery than PSLN-212 after challenge at day 180 [S09, S01-A/E/F, S02-C/E]'],
   ['Mechanism', '**Coherent, partly causal**', 'Seven-step chain; five steps tested by knockout or inhibitor; the manganese-specific step is inferred, not tested (Section 4)'],
   ['Tolerability in mice', '**Acceptable but thin**', f'Weight loss after dosing {n("wl_344")} (worst animal {n("wl_344_worst")}), recovered by day 10 [S08-D]; lung cytokines not back to baseline at 72 h [S09-A]; no histology'],
   ['Manganese and brain safety', '**Unknown**', f'No manganese measurement. Brain *Ifnb1* {n("cns_Ifnb1_344")} buffer (95% CI {n("cns_Ifnb1_344ci")}) at 36 h; cholera-toxin control {n("cns_Ifnb1_ct")} [S10-A]'],
   ['Versus current vaccines for older adults', '**Not tested**', 'No intramuscular, high-dose or licensed-adjuvant comparator in any block'],
   ['Translation to people', '**Not addressed**', 'Mice only; BALB/c all female, no male data; alveolar site of action [S01-B, S01-C]; no human cells'],
   ['Product quality (CMC)', '**Early**', f'Encapsulation efficiency {n("ee_344")} [S08-B]; no manganese content, particle size or stability data in the file'],
   ['Data integrity', '**Audit needed**', f'{n("qc_n")} flags, {n("qc_high")} rated high (Appendix A)']],
  [1.55, 1.25, 4.2], keep=True,
  note='Terms. Aged = mice of 20 months or more; young = 7–8 weeks; young benchmark = young mice given vaccine + PSLN-212; empty liposome = the workbook\'s "Sham". HAI = haemagglutination-inhibition titre, the antibody measure regulators accept for influenza vaccines. '
       'S06-E2 and S06-F2 are my names for the second pair of blocks that the workbook also labels S06-E and S06-F (14-month-old animals).')

# =====================================================================================================
sec('§2')
D.h1('2. Next steps: what the next studies have to establish')
D.p('Five studies behind three gates. Each study answers one question the current data cannot, and each has a stop rule agreed in advance. Gate 0 and Studies 1–4 run in parallel and report by October 2027; '
    'the ferret study and any IND-enabling spend wait for Gate 1. I have not costed the plan, because the data give no basis for it; the scale is about 540 aged mice for Study 1, about 400 for Study 2, 60–80 ferrets for Study 5 and three formulation batches.')
D.fig(FIG+'fig6_timeline.png', 'Figure 1. Proposed timeline. Hatched bar: not part of this request.', 6.3)
D.table('Table 2. Gates',
  ['Gate', 'When', 'Question', 'Passed if', 'If not'],
  [['**Gate 0**', 'Dec 2026', 'Are the numbers in the workbook the numbers in the laboratory records?', f'All {n("qc_high")} high flags resolved from source; in the re-locked file pooled aged survival is still ≥ 70% for PSLN-344 and ≤ 30% for PSLN-212 (today, worst case: {n("survF_344")} vs {n("survF_212")})', 'Freeze Studies 2–4; Study 1 becomes the only route to re-establish the claim'],
   ['**Gate 1**', 'Oct 2027', 'Is the effect real, attributable to the product, at least as good as current practice, tolerable, translatable and makeable?', 'Go criteria of Studies 1–4 all met', 'Stop, or re-scope as stated under each study'],
   ['**Gate 2**', 'Jul 2028', 'Does it work in a second species with a delivery method usable in people?', 'Go criteria of Study 5 met', 'Stop before IND-enabling spend']],
  [0.6, 0.65, 1.75, 2.45, 1.55], keep=True)

def study(title, rows, keep=False):
    D.table(title, ['Item', 'Specification'], [[f'**{a}**', b] for a, b in rows], [1.15, 5.85], zebra=True, keep=keep)

study('Gate 0. Source-data audit and re-lock of the data set (no animals; 2 November – 18 December 2026)', [
  ('Must establish', 'That every number in this proposal matches the primary records: cage cards, balance logs, flow-cytometry exports, plate-reader files.'),
  ('Scope', f'The {n("qc_n")} flags in Appendix A, starting with the {n("qc_high")} rated high (Q01–Q06, Q10, Q11). Also confirm that no data generated after 3 September 2026 are missing.'),
  ('Comparator', 'Primary records against the workbook, block by block, by someone outside the study team.'),
  ('Read-outs', 'Each flagged block classed as confirmed, corrected or withdrawn; workbook and annotation re-issued with animal identifiers; the analysis scripts supplied with this proposal re-run on the new file.'),
  ('Also decide', 'Whether 20-month-old mice of both sexes can be supplied for Studies 1 and 2 in January 2027. This is the critical-path item.')], keep=True)
study('Study 1. Confirmatory efficacy, attribution and benchmark in aged mice (January – August 2027)', [
  ('Must establish', '(a) The survival benefit in aged mice replicates under randomisation and blinding, in both sexes. (b) It needs CDN-1807 and Mn²⁺ together in the liposome. '
                     '(c) It is at least as good as surrogates for the vaccines older adults receive now. (d) The lowest effective dose. (e) Which pre-challenge marker predicts survival in the individual animal.'),
  ('Why (gap)', f'Current experiments have 5–10 female animals per group and no stated blinding; one experiment of 7 per arm has only {n("power_n7")} power even for {pc("survA_344")} vs {pc("survA_212")}. '
                f'No manganese-only, free-CDN, intramuscular or licensed-adjuvant arm exists. All efficacy data are at 20 µg, which already gives {n("d20_40")} of the interferon response seen at 40 µg [S08-A]. Immune read-outs and challenge outcomes come from different animals.'),
  ('Population', 'BALB/c, 20–21 months at dosing, male and female. Young adults (8 weeks) as benchmark. A C57BL/6 cohort for the two lead arms, because the cross-strain weight records are flagged (Q06, Q07).'),
  ('Groups and comparators', 'One dose into the airway with inactivated H1N1 + H3N2 vaccine unless stated: (A) empty liposome; (B) manganese liposome without CDN-1807, manganese matched to PSLN-344 (or empty liposome plus manganese chloride, if manganese cannot be loaded without the CDN); (C) free CDN-1807, 20 µg; (D) PSLN-212, 20 µg; '
                             '(E) PSLN-344, 20 µg; (F) PSLN-344, 10 µg; (G) PSLN-344, 5 µg; (H) intramuscular vaccine with a squalene oil-in-water emulsion, as surrogate for an MF59-adjuvanted vaccine; '
                             '(I) intramuscular vaccine at four times the antigen dose, as surrogate for a high-dose vaccine; (J) young mice + PSLN-212; (K) unvaccinated, mock-challenged aged mice, for background mortality.'),
  ('Primary endpoint', 'Survival 14 days after a lethal challenge with a virus of a different subtype (5 × mLD50 rgH5N1, the design of S06-C) given 14 days after dosing: E against D, and E against the better of H and I. Humane end-point, randomisation and blinded scoring fixed in the protocol; lethal dose re-titrated in aged animals of each sex beforehand.'),
  ('Secondary endpoints and read-outs', 'Survival after matched H1N1 challenge (the design of S03-I) in groups A, D, E, H, I. Weight-loss area under the curve. Lung virus titre 3 and 5 days after challenge (never measured so far). '
                             'On day 13 in every challenged animal: HAI, neutralising titre, IgG2a/IgG1, blood IFN-γ-producing CD8 T cells. IgA in nasal wash and lung lavage (never measured). Lung resident-memory CD8 T cells at day 25. '
                             'Lung histopathology 3 and 7 days after dosing. Durability: challenge 90 days after dosing in animals dosed at 18 months (groups D, E, H). Which arm protects: CD8 T-cell depletion before mismatched challenge in an extra group E cohort (16 animals).'),
  ('Size and power', f'32 per arm (16 per sex) for D, E, H, I; 16 per arm for the others. Sixteen per arm gives {n("power_16")} power for 71% vs 12% survival, the worst-case reading of today\'s data; 32 per arm gives {n("power_32")} power for 80% vs 40%, the margin assumed over a current-practice surrogate. '
                      'Challenge cohorts about 320 aged mice, satellite read-outs 120, durability 72, C57BL/6 32.'),
  ('Timing', 'Protocol and animal supply January 2027; dosing February; interim read-out of the day-14 mismatched challenge mid-April; immune read-outs May; day-90 challenge June; report August 2027. Staged: the matched-challenge and depletion cohorts are dosed only after the interim read-out.'),
  ('Go / stop', f'**Go:** (i) E at least 40 survival points above D overall, same direction in each sex (met with {n("go_prob_worst")} probability if today\'s worst-case rates are true, and {n("go_prob_20pt")} if the true difference is only 20 points); (ii) E above B and C, p < 0.05; '
                '(iii) E above the better of H and I after mismatched challenge, p < 0.05, and not worse on lung virus titre after matched challenge (upper confidence limit of the difference below 0.5 log10). '
                '**Stop or re-scope:** B matches E (the asset is then manganese, not the STING agonist); or H or I matches E on survival, virus titre and weight loss (no differentiation).')])
study('Study 2. Dose range, airway tolerability and manganese safety, non-GLP (January – July 2027)', [
  ('Must establish', 'The margin between the effective dose and the first adverse dose; whether manganese from PSLN-344 accumulates in the olfactory bulb or brain; whether lung inflammation resolves; tolerability of a second dose.'),
  ('Why (gap)', f'Tolerability rests on body weight in 5 animals for 10 days [S08-D] and three brain transcripts at 36 h [S10-A]. Lung *Il6*, *Tnf* and *Ccl2* are {n("cyt_Il6_344_72h")}, {n("cyt_Tnf_344_72h")} and {n("cyt_Ccl2_344_72h")} control at 72 h with no later time point [S09-A]. '
                'The neutrophil block is unusable (Q04). The manganese content of PSLN-344 is not in the file. A booster was given in S13-I/J with no tolerability read-out.'),
  ('Population', 'Aged BALB/c (20 months), both sexes, 8 per group and time point (5 for tissue manganese); young adults at the top dose.'),
  ('Groups and comparators', 'All with vaccine: buffer; empty liposome; PSLN-212 20 µg (manganese-free comparator); PSLN-344 at 5, 20, 40 and 80 µg; manganese chloride alone at the manganese dose of the 80 µg group (positive control for uptake); '
                             'cholera toxin (positive control for brain inflammation, as in S10-A). One dose, and two doses 14 days apart.'),
  ('Primary endpoints', 'Manganese by ICP-MS in olfactory bulb, striatum, cerebellum, lung, liver and blood at 1, 3, 7 and 28 days. Lung histopathology score and lavage cell differential (neutrophils) at 1, 3, 7, 14 and 28 days.'),
  ('Secondary endpoints and read-outs', 'Daily weight and clinical score. Lung and serum IL-6, TNF, CCL2, IFN-β, IL-10 until back to baseline. Brain *Ifnb1*, *Tnf*, *Isg15* at 6 h, 36 h and 7 days, with microglia and astrocyte staining of the olfactory bulb. '
                             'Olfaction (buried-food test) and motor function (rotarod) at days 7 and 28. Clinical chemistry. Anti-PEG IgM and IgG after the second dose (the liposome contains a PEG-lipid).'),
  ('Timing', 'In-life February – May 2027; pathology and manganese analysis to July 2027.'),
  ('Go / stop', '**Go:** at 40 µg, twice the efficacy dose: no adverse histopathology, brain manganese not above buffer controls at day 28, weight loss ≤ 5% with recovery by day 10, lung cytokines at baseline by day 14. '
                f'**Stop PSLN-344:** persistent manganese in brain or olfactory bulb, behavioural change, or unresolved lung pathology at or below 40 µg. PSLN-212 is not a fall-back for older adults ({n("survA_212")} survival in aged mice).')])
study('Study 3. Human cells: STING variants and older donors (December 2026 – April 2027)', [
  ('Must establish', 'That CDN-1807 activates human STING across its common variants; that Mn²⁺ raises the ceiling of the response in myeloid cells from older donors as it does in mouse lung; that IFN-β, GM-CSF and CCL2 can serve as pharmacodynamic markers in people.'),
  ('Why (gap)', f'There are no human data of any kind in the package. In mouse lung manganese raised the interferon plateau from {n("emax_212")} to {n("emax_344")} without changing the half-maximal dose ({n("ed50_212")} vs {n("ed50_344")}) [S08-A]. '
                '*External:* STING agonists have failed before on mouse–human differences, and human STING has common variants that respond differently to cyclic dinucleotides.'),
  ('Population', 'Monocytes, monocyte-derived macrophages and dendritic cells from donors aged ≥ 65 (n = 15) and 18–40 (n = 15), both sexes, STING-genotyped. Alveolar macrophages from lavage and primary airway epithelium where obtainable (n ≥ 5). Reporter cells carrying each common STING variant, and STING-deficient cells as the test of whether manganese acts through STING.'),
  ('Comparators', 'Empty liposome; manganese liposome without CDN; free CDN-1807; PSLN-212; PSLN-344; cGAMP liposome (CMP-204). Six concentrations each.'),
  ('Primary endpoint', 'IFN-β protein: plateau and half-maximal concentration for PSLN-344 against PSLN-212, by donor age group and by STING variant.'),
  ('Secondary read-outs', 'GM-CSF, CCL2, CXCL10, IL-6, TNF, IL-10; cell viability.'),
  ('Go / stop', '**Go:** plateau with PSLN-344 at least twice that with PSLN-212 in cells from older donors; activity on every variant carried by more than 5% of people. **Stop or re-engineer:** no activity on a common variant, or no manganese effect in human cells.')])
study('Study 4. Product quality and delivery (January – September 2027)', [
  ('Must establish', 'That PSLN-344 can be made reproducibly to a specification that includes manganese; that it is stable and survives mixing with antigen and aerosolisation; and that a device exists which puts it where the mouse data say it acts.'),
  ('Why (gap)', f'The only product-quality number in the file is encapsulation efficiency, {n("ee_344")}, against {n("ee_212")} for PSLN-212 [S08-B]. Particle size, charge and storage are named in the annotation but no values are given. '
                'In mice the liposome acts through alveolar macrophages and alveolar epithelium [S01-B, S01-C]; *external:* a liquid dose instilled into a mouse nose reaches the lung, whereas a human nasal spray deposits mainly in the nose.'),
  ('Material', 'Three independent batches at ten times the current scale or more.'),
  ('Read-outs', 'Mn : CDN ratio and free Mn²⁺. Size, polydispersity, zeta potential. Encapsulation efficiency (target ≥ 70% with batch-to-batch coefficient of variation ≤ 10%, or a justified lower specification). CDN integrity. Release in simulated lung fluid. '
                'Stability of lyophilised product at −20 °C, 2–8 °C and 25 °C at 1, 3 and 6 months. Haemagglutinin potency after mixing. Sterility and endotoxin. Droplet size for nasal-spray and for nebuliser or soft-mist delivery, and potency after aerosolisation.'),
  ('Go / stop', '**Go:** specification met on three consecutive batches; at least 3 months stability at 2–8 °C; potency kept after aerosolisation; a delivery route defined for Study 5. **Stop or partner:** no reproducible specification, or no feasible route to the lower airway.')])
study('Study 5. Ferret: efficacy with a delivery method usable in people (October 2027 – July 2028; starts only after Gate 1)', [
  ('Must establish', 'Efficacy in the standard influenza species; whether deposition in the nose is enough or the lower airway must be reached; effect on virus shedding; safety in a second species.'),
  ('Population', f'Ferrets, both sexes, 8–12 per group; influenza-naive and previously infected animals (in 14-month-old mice prior infection did not blunt PSLN-344: {n("imp_perth_344")} with and {n("nai_perth_344")} without prior infection [S06-F2]); older ferrets if obtainable.'),
  ('Groups and comparators', 'Placebo; vaccine alone into the airway; vaccine + PSLN-344 by nasal spray; vaccine + PSLN-344 by aerosol to the lower airway at two doses; vaccine + PSLN-212; a licensed enhanced human vaccine given intramuscularly.'),
  ('Primary endpoint', 'Virus titre in nasal wash (area under the curve, days 1–7) and in lung on day 4 after challenge with a drifted H3N2 virus 4 weeks after dosing; a second cohort challenged with a different subtype.'),
  ('Secondary read-outs', 'Fever, weight, clinical score. HAI, neutralising and anti-neuraminidase antibody. Nasal IgA. IFN-γ ELISpot. Lung histopathology. Manganese in olfactory bulb and brain. Transmission to contact animals (exploratory).'),
  ('Go / stop', '**Go (Gate 2):** at least a ten-fold reduction in lung virus titre against vaccine alone, not worse than the licensed comparator against drifted virus, clean histopathology. Then GLP toxicology in two species and a GMP batch.')])
D.p('**Line of sight to the clinic (not part of this request).** If Gate 2 is passed, the first human study would be a randomised, observer-blind, dose-escalating study in healthy adults aged 65 and over (after a sentinel cohort aged 50–64), about 30 per arm, '
    'against a licensed high-dose or adjuvanted seasonal vaccine and against unadjuvanted vaccine by the study route. Primary endpoint: safety, including nasal and respiratory reactions, spirometry, blood manganese, and facial palsy and other neurological events followed for 12 months. '
    'Secondary: HAI titre ratio and seroconversion at day 28. Exploratory: the biomarkers in Table 8. On the timeline above this is not before 2029.')

# =====================================================================================================
sec('§3')
D.pagebreak()
D.h1('3. The evidence behind the recommendation')
D.h2('3.1 Efficacy in aged animals')
D.fig(FIG+'fig1_survival_by_experiment.png', 'Figure 2. Survivors / animals challenged in every survival experiment in the workbook, as printed. One intranasal dose of vaccine with the adjuvant shown; lethal challenge on the day shown; '
      '14 days of observation (21 for S03-J). Flags refer to Appendix A.', 6.75)
D.table('Table 3. Pooled survival of aged mice, PSLN-344 against PSLN-212, with sensitivity analyses',
  ['Analysis set', 'PSLN-344', 'PSLN-212', 'Difference (stratified by experiment)', 'Test'],
  [['**As printed:** 9 experiments in aged BALB/c [S03-I, S03-J, S06-A–G]', f'{n("survA_344")}\n95% CI {n("survA_344_ci")}', f'{n("survA_212")}\n95% CI {n("survA_212_ci")}', n('rdci_A'), f'Stratified log-rank {n("p_slr_A")}; hazard ratio {n("hr_A")}'],
   ['**Conservative:** without S03-I, S03-J (comparator arms uncertain, Q11) and S06-C (identical to S06-D, Q03)', f'{n("survB_344")}\n95% CI {n("survB_344_ci")}', f'{n("survB_212")}\n95% CI {n("survB_212_ci")}', n('rdci_B'), f'Stratified log-rank {n("p_slr_B")}; hazard ratio {n("hr_B")}'],
   ['**Worst case:** conservative set, using the weight-trace count wherever it is less favourable to PSLN-344 or more favourable to PSLN-212 (Q10)', n('survF_344'), n('survF_212'), n('rdci_F'), f'Cochran–Mantel–Haenszel {n("p_cmh_F")}'],
   ['**All head-to-head experiments:** the 9 above + aged C57BL/6 + aged Swiss Webster + four groups of 14-month-old BALB/c', n('survC_344'), n('survC_212'), n('rdci_C'), f'PSLN-344 ahead in {n("h2h_ahead")}']],
  [2.55, 1.0, 1.0, 1.15, 1.3], keep=True)
D.bullets([
  f'**Breadth.** Matched H1N1 challenge {n("S03-I_344")} [S03-I]; challenge with a different subtype {n("het_344")} against {n("het_212")} for PSLN-212 [S06-A–G]; wild-type H5N1 two days after one dose {n("S03-J_344")} [S03-J]; '
  f'aged C57BL/6 {n("b6_344")} and Swiss Webster {n("sw_344")} against {n("b6_212")} and {n("sw_212")} [S15-L, S15-N; challenge virus not stated]; 14-month-old animals with or without earlier infection {n("m14_344")} against {n("m14_212")} [S06-E2, S06-F2].',
  f'**Onset and duration.** {n("early_344")} survived challenge 2–3 days after the single dose, {n("d14_344")} at day 14 and {n("d60_344")} at day 60 (day 14 against day 60, {n("p_d14_d60")}). '
  f'The day-60 figure needs care: unvaccinated, unchallenged aged controls lost {n("unt_deaths")} during the same 14 days [S06-E–G], so background mortality in animals this old is not negligible. '
  f'But the PSLN-344 animals whose weight traces stop after day-60 challenge had fallen to {n("d60_deathwt_344")} of starting weight, whereas the unchallenged controls that died were at {n("unt_deathwt")} [S15-E–G]. I read this as partial waning, not only old age. Nothing is known beyond day 60 in aged animals; the only six-month data are in young mice, where all survived with either candidate but PSLN-344 animals recovered more slowly (Section 3.2).',
  f'**Protection is from death, not from illness.** After challenge with a different subtype, PSLN-344 groups lost on average {n("morb_344")} of body weight at the lowest point, the young benchmark {n("morb_young")}, PSLN-212 groups {n("morb_212")} [S15-A, B, D–G]; after matched challenge PSLN-344 animals lost {n("morb_344_hom")} [S13-F].',
  f'**Antigen is required.** PSLN-344 without vaccine: {n("h_adj")} [S15-H]. The early protection is not a general antiviral state induced by the adjuvant.',
  f'**Statistical caution.** Each experiment has 7–10 animals per arm and appears to have been run once; a single experiment of 7 per arm has {n("power_n7")} power for a difference as large as the pooled one. Taken singly, PSLN-344 differs from PSLN-212 at p < 0.05 in {n("single_lr_sig")} experiments by log-rank test (permutation p up to {n("single_lr_max")}) and in {n("single_fisher_sig")} by Fisher\'s test on survivor counts. The strength of the evidence is the consistency across experiments, not any one of them.'])

D.h2('3.2 PSLN-344 against PSLN-212: which to take forward')
D.bullets([
  f'**In aged animals PSLN-344 is better on nearly every read-out** (Figure 3), and on about half of them it cannot be told apart from the young benchmark ({n("ri_ns_young")} of {n("ri_n")}, five animals per group). HAI titres reach {n("hai_h1_pctyoung")} and {n("hai_h3_pctyoung")} of the young level for H1N1 and H3N2 '
  f'({n("hai_h1_344")} and {n("hai_h3_344")} against {n("hai_h1_212")} and {n("hai_h3_212")} for PSLN-212) [S03-C, S03-G].',
  f'**It does not restore everything.** Co-stimulatory molecules on lymph-node dendritic cells stay at {n("cd40_pctyoung")} (CD40) and {n("cd86_pctyoung")} (CD86) of the young level [S02-D]; IgG subclass titres at {n("igg2a_h1_pctyoung")}–{n("igg1_h1_pctyoung")} [S13-A, S13-B]; lung resident-memory CD8 T cells at {n("trm_pctyoung")} [S05-I].',
  f'**In young animals manganese adds nothing, and at six months PSLN-344 does slightly worse.** Survival {n("y344")} with either; interferon-β {n("ifn16_y344")}-fold against {n("ifn16_young")}-fold; dendritic cells, antigen transport and T-cell priming indistinguishable (Table 4). '
  f'Even the cGAMP liposome protected {n("s13e_ecmp")} young animals [S13-E]: in young hosts the platform works whatever the payload. When young animals were challenged 180 days after dosing, all survived, but those given PSLN-344 lost more weight ({n("y180_nadir")}) '
  f'and had regained less by day 14 ({n("y180_d14_344")} against {n("y180_d14_212")} of starting weight, {n("y180_d14_p")}) [S09-G].',
  f'**Conclusion.** PSLN-344 is the better asset because of, and only for, the aged setting. PSLN-212 is ahead on three counts only: it carries no manganese; it leaves less lung inflammation at 72 h, because it induces less (*Il6* {n("cyt72_ratio_Il6")} and *Ccl2* {n("cyt72_ratio_Ccl2")} lower) [S09-A]; '
  'and young animals recovered faster with it after the day-180 challenge. None of these gives it a use in older adults, but the last is a warning about durability that the day-90 cohort of Study 1 has to resolve. PSLN-212 stays in the plan as the comparator in Studies 1, 2 and 3.'])
D.fig(FIG+'fig2_restoration_vs_young.png', f'Figure 3. Immune read-outs in aged mice as a percentage of the young benchmark. Each row is one block with five animals per group (three for S04-D); geometric means for titres. '
      f'PSLN-344 is closer to the young benchmark than PSLN-212 in {n("ri_closer")} of {n("ri_n")} read-outs ({n("ri_sig")} at p < 0.05, Welch test, unadjusted); 32 are shown. The exception is *Ifnb1* at 72 h, which stays above the young level with both.', 6.2)
D.table('Table 4. Young mice: PSLN-344 against PSLN-212',
  ['Read-out', 'PSLN-344, young', 'PSLN-212, young', 'Source'],
  [['Survival, three challenge experiments (day 21, 21 and 180)', n('y344'), n('y212'), 'S09-B, S09-D, S09-F'],
   ['Lung *Ifnb1* at 16 h, fold', f'{n("ifn16_y344")} ({n("ifn16_yfold")}; {n("ifn16_y_p")})', n('ifn16_young'), 'S01-A'],
   ['Lung CD11b+ dendritic cells, day 4', n('y_dc4').split(' vs ')[0], n('y_dc4').split(' vs ')[1], 'S01-E'],
   ['Lung cDC1, 72 h', n('y_cdc1').split(' vs ')[0], n('y_cdc1').split(' vs ')[1], 'S01-F'],
   ['Antigen-carrying dendritic cells in lymph node', n('y_agdc').split(' vs ')[0], n('y_agdc').split(' vs ')[1], 'S02-C'],
   ['CD8 T-cell priming by lymph-node dendritic cells', n('y_prime').split(' vs ')[0], n('y_prime').split(' vs ')[1], 'S02-E'],
   ['Largest weight loss after challenge at day 21, 21 and 180', f'{n("y_wl_pr8").split(" vs ")[0]}, {n("y_wl_perth").split(" vs ")[0]}, {n("y_wl_h5").split(" vs ")[0]}', f'{n("y_wl_pr8").split(" vs ")[1]}, {n("y_wl_perth").split(" vs ")[1]}, {n("y_wl_h5").split(" vs ")[1]}', 'S09-C, S09-E, S09-G'],
   ['Body weight 14 days after the day-180 challenge, % of starting weight', f'{n("y180_d14_344")} ({n("y180_d14_p")})', n('y180_d14_212'), 'S09-G']],
  [3.0, 1.75, 1.15, 1.1], keep=True)


D.h2('3.3 Tolerability and safety')
D.bullets([
  f'**After dosing.** Mean largest weight loss {n("wl_344")} with PSLN-344 (worst animal {n("wl_344_worst")}) against {n("wl_vac")} with vaccine alone ({n("wl_p")}) and {n("wl_212")} with PSLN-212; weight back to {n("wd10_344")} by day 10 [S08-D]. '
  f'Adding the TLR7/8 agonist R848 was not tolerated: {n("wl_r848")} mean loss, {n("wl_r848_worst")} in the worst animal, {n("wd10_r848")} at day 10 with one of five animals missing.',
  f'**Lung inflammation is strong and has not resolved by 72 h.** At 16 h PSLN-344 raised *Il6* {n("cyt_Il6_344_16h")}, *Tnf* {n("cyt_Tnf_344_16h")} and *Ccl2* {n("cyt_Ccl2_344_16h")}; the young benchmark shows {n("cyt_Il6_young_16h")}, {n("cyt_Tnf_young_16h")} and {n("cyt_Ccl2_young_16h")}, so *Il6* and *Ccl2* are no higher than in young animals but *Tnf* is. '
  f'At 72 h they were still {n("cyt_Il6_344_72h")}, {n("cyt_Tnf_344_72h")} and {n("cyt_Ccl2_344_72h")} (PSLN-212: {n("cyt_Il6_212_72h")}, {n("cyt_Tnf_212_72h")}, {n("cyt_Ccl2_212_72h")}), three animals per group, and there is no later time point [S09-A]. '
  f'Lung monocytes were still {n("mono8_344")} at day 8 against {n("mono8_sham")} with empty liposome [S01-D]. This inflammation is the mechanism; it is also the main tolerability question for older people.',
  f'**Brain.** 36 h after dosing, *Ifnb1* was {n("cns_Ifnb1_344")} buffer (95% CI {n("cns_Ifnb1_344ci")}), *Isg15* {n("cns_Isg15_344")} and *Tnf* {n("cns_Tnf_344")} (95% CI {n("cns_Tnf_344ci")}; not significant after Tukey correction and not different from empty liposome); '
  f'cholera toxin gave {n("cns_Ifnb1_ct")}, {n("cns_Isg15_ct")} and {n("cns_Tnf_ct")} [S10-A]. So there is no interferon signal in the brain at that time, but a two-fold change cannot be excluded, it is one time point, and manganese itself was not measured.',
  '**Not in the file at all.** Manganese dose and tissue exposure; histopathology of nose, lung or brain; clinical pathology; tolerability of a second dose; male animals; any GLP study. *External:* inhaled manganese is a recognised neurotoxicant that can reach the brain along the olfactory nerve, '
  'and an intranasal influenza vaccine with a toxin adjuvant was withdrawn after cases of facial palsy; regulators will ask about both.'])
D.fig(FIG+'fig4_safety_tolerability.png', 'Figure 4. Tolerability read-outs. (a) Body weight after dosing without challenge. (b) Lung cytokine transcripts; the 72 h values come from the panel printed as "16h" on the right of sheet S09 (flag Q02). '
      '(c) Brain transcripts 36 h after dosing. (d) Largest weight loss after lethal challenge; animals that died are included.', 6.6)

D.h2('3.4 Reliability of the data set')
D.p(f'I parsed all {n("cells_total")} numeric cells and cross-checked every block against the annotation and against linked blocks. Appendix A lists the {n("qc_n")} flags with cell ranges; the {n("qc_high")} serious ones are in Table 5. '
    'They have the pattern of assembly errors (pasting and labelling), which the audit has to confirm, and they do not all point the same way: some make PSLN-344 look worse than the underlying numbers, some better.')
short = {'Q01':('IgG2a/IgG1 ratio blocks have rotated column headers [S03-B, S03-F]', f'As printed PSLN-344 looks Th2-skewed (ratio {n("ratio_h1_printed344")}). Recomputed from the subclass titres it is {n("ratio_h1_344")} against {n("ratio_h1_212")} for PSLN-212 and {n("ratio_h1_young")} for young.', 'Recomputed from S13-A–D; printed blocks not used'),
         'Q02':('Second cytokine panel labelled "16h" is the 72 h time point [S09-A]', 'Its *Ifnb1* values equal the 72 h values of S01-A for 21 of 21 animals. Read correctly, it shows inflammation persisting at 72 h.', 'Analysed as 72 h'),
         'Q03':('Two survival experiments are identical [S06-C = S06-D]', 'Day-14 and day-3 rgH5N1 challenges carry the same death days in all four groups; the 7/7 result for PSLN-344 is counted twice.', 'S06-C dropped in the conservative analysis'),
         'Q04':('Neutrophil block duplicates the alveolar-macrophage block [S11-B ≈ S11-A]', '8 of 20 animal time-series identical; group means correlate r = 0.997. There is no usable neutrophil read-out.', 'S11-B excluded'),
         'Q05':('Weight traces re-used between experiments [S15-C = S15-I]', '40 of the 42 values for days 2–12 identical animal by animal; only day 14 differs.', 'S15-C weights for PSLN-344 not used'),
         'Q06':('Young C57BL/6 weights re-use young BALB/c traces from another adjuvant group [S15-M ≈ S09-E]', '6 of 7 animals match at four or more time points. Cross-strain weight evidence is not independent.', 'Cross-strain claim rests on survival blocks; graded moderate'),
         'Q10':(f'Survival and weight blocks disagree in {n("qc_mismatch_n")} groups', f'For example day-3 rgH5N1: PSLN-344 {n("S06-D_344")} in the survival block, {n("s15d_344_bw")} by weight traces; matched H1N1: PSLN-212 {n("S03-I_212")} against {n("s13f_212_bw")}.', 'Worst-case analysis uses the less favourable count'),
         'Q11':('Linked blocks list different groups [S03-I/S13-F; S03-J/S13-G]', 'In the wild-type H5N1 experiment the comparators are "Sham, PSLN-212" in one block and "Sham, Naïve" in the other. The PSLN-344 arm is 10/10 in both.', 'Reported as printed; not called a clean head-to-head; dropped in the conservative analysis')}
D.table('Table 5. The serious data-quality flags and what I did about them', ['Flag', 'Finding', 'Why it matters', 'Handling here'],
        [[k, v[0], v[1], v[2]] for k, v in short.items()], [0.4, 2.0, 3.0, 1.6], keep=True)
D.table('Table 6. Which conclusions survive the flags', ['Conclusion', 'Rests on', 'After removing flagged data or reading them least favourably'],
  [['PSLN-344 protects aged mice where PSLN-212 does not', '9 survival experiments', f'**Holds.** {n("survB_344")} vs {n("survB_212")} in the six remaining experiments; worst case {n("survF_344")} vs {n("survF_212")}'],
   ['Protection within 2–3 days of one dose', 'S03-J, S06-B, S06-D, S15-H', f'**Holds for the PSLN-344 arm.** S06-B {n("S06-B_344")} and S15-H {n("h_both")} are unflagged; S06-D is {n("S06-D_344")} or {n("s15d_344_bw")}'],
   ['Protection against wild-type H5N1', 'S03-J only', f'**Holds for the arm** ({n("S03-J_344")} in both linked blocks); what it was compared with is uncertain'],
   ['Works in other mouse strains', 'S15-L, S15-N', '**Moderate.** Survival blocks only; the weight blocks contain recycled traces; challenge virus not stated'],
   ['Antibody restored to near the young level', 'S03-A, C, D, E, G, H; S13-A–D', '**Holds.** These blocks are unflagged; the ratio blocks were corrected'],
   ['Lung inflammation resolves', '—', '**Cannot be concluded.** Still raised at 72 h; neutrophil block unusable'],
   ['Manganese does not change uptake by lung epithelium', 'S08-C', '**No claim.** The block conflicts with S01-B for the same material (Q14)']],
  [2.3, 1.6, 3.1], keep=True)
D.h2('3.5 Formulation')
D.p(f'Encapsulation efficiency is {n("ee_344")} for PSLN-344 and {n("ee_212")} for PSLN-212 ({n("ee_p")}) [S08-B]. About 45% of the CDN is therefore not encapsulated, and the file does not say whether doses are stated as total or encapsulated CDN. '
    'The annotation says size, charge and morphology were measured and that the product is lyophilised with trehalose and stored at −20 °C, but gives no values. The manganese content is not stated anywhere.')

# =====================================================================================================
sec('§4')
D.h1('4. Mechanism of action and biomarkers')
D.h2('4.1 Mechanism')
D.fig(FIG+'fig3_mechanism.png', 'Figure 5. Mechanism supported by the data: the same liposome and the same STING agonist, with and without manganese, in aged lung. Source blocks for every number are in Table 7.', 7.0)
D.p(f'The liposome is the delivery system and is common to both candidates. What manganese changes is the size of the first signal. In aged lung PSLN-212 gives a type I interferon response less than half that of a young animal ({n("ifn16_212")}-fold against {n("ifn16_young")}-fold); '
    f'PSLN-344 gives the young response ({n("ifn16_344")}-fold). The dose-response shows a higher ceiling, not a shift in potency: plateau {n("emax_344")} against {n("emax_212")}, half-maximal dose {n("ed50_344")} against {n("ed50_212")} [S08-A], and encapsulation is the same. '
    'My reading of the chain: with the weaker signal, aged lung makes no GM-CSF, recruited monocytes become Ly6C+ macrophages instead of dendritic cells, regulatory T cells stay high and little antigen reaches the lymph node; with the stronger signal the cascade proceeds as in a young animal. '
    'Two links are inferred rather than tested: that manganese acts through STING, and which arm of immunity, antibody or CD8 T cells, protects against mismatched virus.')
D.table('Table 7. Mechanism: evidence for each step, in aged mice unless stated',
  ['Step', 'PSLN-344 vs PSLN-212 (young benchmark)', 'Causal test in our data', 'Strength'],
  [['**1. Delivery to the alveolus**', f'Dye-labelled liposome in {n("srb2_b")} of type II and {n("srb1_b")} of type I alveolar epithelial cells, against {n("srb2_a")} and {n("srb1_a")} for free dye [S01-B]. Same liposome for both candidates.',
    f'Uptake by alveolar macrophages {n("spad_a")} in wild-type and {n("spad_b")} in SP-A/D-knockout mice [S01-C, young]. Gap-junction blocker cuts monocyte recruitment from {n("cbx_a")} to {n("cbx_b")} [S11-C].', 'Causal, platform-level. Effect of Mn on uptake unresolved (Q14)'],
   ['**2. STING → interferon-β; Mn²⁺ raises the ceiling**', f'*Ifnb1* at 16 h {n("ifn16_344")} vs {n("ifn16_212")}-fold ({n("ifn16_young")}); ratio {n("ifn16_fold")} (95% CI {n("ifn16_foldci")}) [S01-A]. Plateau {n("emax_344")} vs {n("emax_212")}; half-maximal dose {n("ed50_344")} vs {n("ed50_212")} [S08-A]. cGAMP liposome {n("ifn16_cmp")}-fold.',
    'None. No manganese-only arm, no free CDN, no STING knockout.', 'Associative. **Key gap**'],
   ['**3. GM-CSF and CCL2**', f'*Gm-csf* {n("gm_344_16h")}, {n("gm_344_36h")}, {n("gm_344_72h")}-fold at 16, 36, 72 h vs {n("gm_212_16h")}, {n("gm_212_36h")}, {n("gm_212_72h")} [S02-F]. *Ccl2* at 16 h {n("cyt_Ccl2_344_16h")} vs {n("cyt_Ccl2_212_16h")} ({n("cyt_Ccl2_young_16h")}) [S09-A, n = 3].',
    f'Giving GM-CSF with PSLN-212 raises monocyte-derived dendritic cells from {n("gmres_a")} to {n("gmres_b")} [S02-G]. Marrow lacking the interferon receptor: {n("ifnar_a")} → {n("ifnar_b")}; GM-CSF restores to {n("ifnar_gm")} [S02-H].', 'Causal'],
   ['**4. Monocytes become dendritic cells, not Ly6C+ macrophages**', f'Lung monocytes day 4: {n("mono4_344")} vs {n("mono4_212")} ({n("mono4_young")}) [S01-D]. CD11b+ dendritic cells day 4: {n("dc4_344")} vs {n("dc4_212")} ({n("dc4_young")}) [S01-E]. Ly6C+CCR2+ macrophages day 5: {n("mac5_344")} vs {n("mac5_212")} ×10⁵ [S07-A, n = 3]. CD206+ macrophages {n("cd206_344")} vs {n("cd206_212")} ({n("cd206_young")}) [S11-E].',
    f'CCR2 antagonist: monocytes {n("ccr2mono_a")} → {n("ccr2mono_b")} [S07-B]; granzyme B+ CD8 T cells {n("ccr2gzmb_a")} → {n("ccr2gzmb_b")} [S02-I, young].', 'Causal for recruitment. Macrophage → Treg link unproven (Q13)'],
   ['**5. Migration, antigen transport, priming**', f'Migratory dendritic cells {n("migdc_344")} vs {n("migdc_212")} ({n("migdc_young")}) [S02-A]. Antigen-carrying dendritic cells in lymph node {n("agdc_344")} vs {n("agdc_212")} ({n("agdc_young")}) [S02-C]. CD8 priming ex vivo {n("prime_344")} vs {n("prime_212")} ({n("prime_young")}) [S02-E]. CD40 {n("cd40_344")} vs {n("cd40_212")} ({n("cd40_young")}) [S02-D].',
    f'Pertussis toxin: antigen-carrying cells {n("agdc_344")} → {n("ptx_dc")} [S02-C]; priming in lymph node {n("ptx_mln_a")} → {n("ptx_mln_b")} but in lung {n("ptx_lung_a")} → {n("ptx_lung_b")} [S05-C].', 'Causal; T cells are also primed inside the lung'],
   ['**6a. Germinal centre and antibody**', f'Germinal-centre B cells {n("gcb_344")} vs {n("gcb_212")} ({n("gcb_young")}) [S03-K]. Tfh:Tfr ratio {n("tfhtfr_344m")} vs {n("tfhtfr_212m")} [S04-B]; by day 30 Tfr no longer differ ({n("tfr30_344")} vs {n("tfr30_212")}) [S04-C]. HAI {n("hai_h1_344")} vs {n("hai_h1_212")} ({n("hai_h1_young")}); neutralising titre {n("mn_h1_344")} vs {n("mn_h1_212")} ({n("mn_h1_young")}) [S03-C, S03-D]. IgG2a/IgG1 {n("ratio_h1_344")} vs {n("ratio_h1_212")} ({n("ratio_h1_young")}) [S13-A/B].',
    'None.', 'Associative'],
   ['**6b. CD8 T cells**', f'IFN-γ+ CD8 T cells responding to H5N1 antigen after H1N1 + H3N2 vaccine: {n("ifng14_344")} vs {n("ifng14_212")} at day 14, {n("ifng60_344")} vs {n("ifng60_212")} at day 60 [S05-F, S05-G]. Lung resident-memory CD8 T cells {n("trm_344")} vs {n("trm_212")} ({n("trm_young")}) [S05-I].',
    'None. No CD8 or antibody depletion; antibody to the mismatched virus not measured.', 'Associative. Which arm gives cross-protection is not known'],
   ['**7. Protection**', f'{n("survA_344")} vs {n("survA_212")} survival.', f'Without antigen {n("h_adj")} [S15-H].', 'Direct']],
  [1.25, 2.95, 1.85, 0.95], small=True)

D.h2('4.2 Biomarkers')
D.p('The chain in Table 7 gives markers at three levels: the first signal (hours), the cellular response (days) and the adaptive response (weeks). None has been tied to protection in the individual animal, because immune read-outs and challenge outcomes were taken from different animals; Study 1 is designed to do that, and Study 3 tests the first level in human cells.')
D.table('Table 8. Biomarkers to validate efficacy',
  ['Marker', 'What our data show (aged: PSLN-344 vs PSLN-212; young benchmark)', 'How to measure in people', 'Use, and caveat'],
  [['**Interferon-β / interferon-stimulated genes**', f'*Ifnb1* {n("ifn16_344")} vs {n("ifn16_212")}-fold at 16 h ({n("ifn16_young")}); back to {n("ifn72_344")}-fold by 72 h [S01-A]; dose-dependent from 5 µg [S08-A]', 'Nasal lining fluid and blood at 12–24 h: IFN-β, CXCL10, interferon-gene score', '**Target engagement, dose selection.** Separates the candidates by about two-fold only'],
   ['**GM-CSF**', f'{n("gm_344_36h")} vs {n("gm_212_36h")}-fold at 36 h; empty liposome {n("gm_sham_36h")} [S02-F]. Adding GM-CSF rescues PSLN-212 [S02-G]', 'Nasal lining fluid, sputum or lavage at 24–48 h', '**Best discriminator of PSLN-344 from PSLN-212, and causal.** Transcript only so far; protein not measured'],
   ['**CCL2 and blood monocytes**', f'*Ccl2* {n("cyt_Ccl2_344_16h")} vs {n("cyt_Ccl2_212_16h")} at 16 h [S09-A]; lung monocytes {n("mono4_344")} vs {n("mono4_212")} at day 4 [S01-D]', 'Serum CCL2 at 24 h; monocyte activation markers on days 1–4', '**Pharmacodynamic and tolerability marker**: also tracks the inflammation that must resolve'],
   ['**Circulating Tfh and plasmablasts**', f'Lymph-node ICOS-high Tfh {n("tfhhi_344")} vs {n("tfhhi_212")} ({n("tfhhi_young")}); germinal-centre B cells {n("gcb_344")} vs {n("gcb_212")} at day 7 [S04-A, S03-K]', 'Blood, day 7: activated circulating Tfh, plasmablasts', '**Early predictor of antibody response.** Blood surrogate of a lymph-node finding'],
   ['**HAI and neutralising titre**', f'HAI {n("hai_h1_344")} vs {n("hai_h1_212")} ({n("hai_h1_young")}) for H1N1, {n("hai_h3_344")} vs {n("hai_h3_212")} ({n("hai_h3_young")}) for H3N2; neutralising {n("mn_h1_344")} vs {n("mn_h1_212")} [S03-C, G, D]', 'Serum, day 28', f'**Accepted regulatory surrogate.** Not sufficient here: all {n("hai40_h1_212")} aged PSLN-212 animals had HAI ≥ 40 to H1N1, yet {n("S03-I_212")} (survival block) or {n("s13f_212_bw")} (weight block) survived matched challenge'],
   ['**IgG subclass balance**', f'IgG2a/IgG1 {n("ratio_h1_344")} vs {n("ratio_h1_212")} ({n("ratio_h1_young")}) for H1N1; {n("ratio_h3_344")} vs {n("ratio_h3_212")} ({n("ratio_h3_young")}) for H3N2 [S13-A–D]', 'Serum IgG1/IgG3 against IgG2/IgG4, day 28', '**Quality of the response.** Use the recomputed values, not S03-B/F as printed (Q01)'],
   ['**Cross-reactive CD8 T cells**', f'IFN-γ+ CD8 to H5N1 antigen {n("ifng14_344")} vs {n("ifng14_212")} ({n("ifng14_young")}) at day 14; {n("ifng60_344")} vs {n("ifng60_212")} at day 60 [S05-F, G]', 'Blood, days 14–28: IFN-γ / granzyme B ELISpot to conserved nucleoprotein and matrix peptides', '**Marker for protection against mismatched virus.** Link to protection not yet tested'],
   ['**Lung resident-memory CD8 T cells**', f'{n("trm_344")} vs {n("trm_212")} ({n("trm_young")}) at day 25 [S05-I]', 'Nasal or bronchial sampling in a sub-study only', '**Mechanistic.** Not accessible in routine trials']],
  [1.25, 2.5, 1.5, 1.75], small=True)
D.p('Not measured at all, and needed for a vaccine given by the airway: mucosal IgA, virus titre in the lung after challenge, and antibody against the mismatched challenge virus. All three are in Study 1.')
D.fig(FIG+'fig5_pharmacodynamics.png', 'Figure 6. Candidate pharmacodynamic markers. (a) The age of the animals in S08-A is not stated; the values match the aged groups of S01-A. Curves are three-parameter Hill fits.', 6.3)

# =====================================================================================================
sec('§5')
D.h1('5. Target demographic, for the TAM check')
D.lead('Primary population: adults aged 65 and over who receive a seasonal influenza vaccine each year, both sexes.')
D.bullets([
  f'**Why this group.** The product separates from its manganese-free twin only in aged animals ({n("survA_344")} vs {n("survA_212")} survival), where it returns HAI titres to {n("hai_h1_pctyoung")}–{n("hai_h3_pctyoung")} of the young-adult level. '
  'What it corrects is the age-related loss of vaccine response. *External rule of thumb:* a 20-month-old mouse corresponds to a person in the 60s.',
  f'**Why not younger adults.** No advantage in young mice ({n("y344")} vs {n("y212")} survival), and no evidence against current vaccines in any age group.',
  '**Product form.** An adjuvant needs an antigen. The TAM should be modelled per vaccinee for a combined product (our adjuvant with a partner\'s or our own inactivated seasonal antigen), or as a royalty on a partner\'s vaccine, not as a stand-alone drug.',
  '**Caveat for the model.** The BALB/c animals were all female and no male data exist. Nothing in the data speaks to men, frail or immunosuppressed people, or people with lung disease.'])
D.table('Table 9. Segments for the TAM model',
  ['Segment', 'In the TAM?', 'Support in our data', 'What market research needs to supply (external)'],
  [['Adults ≥ 65, annual seasonal vaccination', '**Core**', f'Aged mice of three strains; survival {n("survA_344")} vs {n("survA_212")}', 'People ≥ 65 by market; vaccine coverage in that group; share already on high-dose, adjuvanted or recombinant vaccines and their price premium'],
   ['Adults 50–64', 'Upside', f'14-month-old mice only: {n("m14_344")} vs {n("m14_212")} [S06-E2, S06-F2]', 'Size and coverage; whether enhanced vaccines are reimbursed below 65'],
   ['Pandemic and pre-pandemic H5N1 preparedness for older adults', 'Upside, procurement-led', f'Wild-type H5N1: {n("S03-J_344")} alive when challenged 2 days after one dose [S03-J, comparators uncertain]; seasonal vaccine + PSLN-344 protected against rgH5N1 [S06-D, S06-F]', 'Government stockpile programmes; not a per-head market'],
   ['Older adults with asthma or COPD', 'Discount until shown safe', f'The product works by inflaming the lung: *Il6* {n("cyt_Il6_344_16h")}, *Tnf* {n("cyt_Tnf_344_16h")} at 16 h [S09-A]', 'Prevalence of chronic lung disease in people ≥ 65; likely excluded from early labels'],
   ['Adults under 50; children', 'Exclude', 'No advantage in young mice; no juvenile data', '—'],
   ['Immunocompromised', 'Exclude for now', 'No data', '—']],
  [1.7, 0.9, 2.3, 2.1], keep=True)
D.p('*External context for the model, to be verified:* in the United States enhanced influenza vaccines are already preferentially recommended from age 65, so the realistic comparator and price anchor is an enhanced vaccine, not a standard one; '
    'and the licensed nasal influenza vaccine is a live vaccine not approved for older adults, so there is no needle-free option in this age group today. Acceptance of an inhaled or nasal product by older adults, and the late-stage mRNA and combination respiratory vaccines aimed at the same group, should be part of the TAM check.')

# =====================================================================================================
sec('§6')
D.h1('6. If we drop it: what we give up, and why one might still drop')
D.p('**What we would give up.**')
D.bullets([
  f'**The only candidate we have that works in aged hosts.** {n("survA_344")} survival against {n("survA_212")} for the manganese-free version and {n("survA_sham")} for vaccine with empty liposome; antibody (HAI) {n("hai_h1_fold")} (95% CI {n("hai_h1_foldci")}) and {n("hai_h3_fold")} (95% CI {n("hai_h3_foldci")}) higher than PSLN-212 [S03-C, S03-G].',
  f'**Protection against viruses the vaccine does not match.** {n("het_344")} against {n("het_212")} when the challenge virus was of a different subtype, including an H5N1 reassortant after a seasonal-type vaccine [S06-A–G].',
  f'**Fast onset from a single dose.** {n("early_344")} survival when challenged 2–3 days after dosing [S03-J, S06-B, S06-D, S15-H].',
  f'**Dose-sparing potential.** 10 µg of PSLN-344 induced more interferon-β ({n("dr_344_10")}-fold) than 40 µg of PSLN-212 ({n("dr_212_40")}-fold) [S08-A].',
  f'**Indifference to earlier infection.** In 14-month-old mice PSLN-344 protected {n("imp_perth_344")} with and {n("nai_perth_344")} without prior influenza infection against H3N2; PSLN-212 protected {n("imp_perth_212")} and {n("nai_perth_212")} [S06-F2].',
  '**A mechanism with ready-made markers** (Tables 7 and 8) that could transfer to other inactivated or subunit antigens given to older adults. The data do not test any antigen other than influenza.'], numbered=True)
D.p('**What we would not be giving up.** No human data, no GLP toxicology, no manufacturing process and no comparison with marketed vaccines exist; what would be written off is a mouse package. '
    'Keeping PSLN-212 alone would preserve nothing of value for older adults, and in young adults it has no demonstrated edge.')
D.p('**The honest case for dropping.** (1) The safety bar for a preventive product given to healthy older people is very high, and this one delivers manganese and a strong inflammatory stimulus to the airway; Study 2 could end the program. '
    '(2) The route to market needs an antigen partner, a delivery device and a large efficacy trial against enhanced vaccines. (3) Protection is against death rather than illness, falls to '
    f'{n("d60_344")} by day 60 in aged mice, and at six months in young mice recovery was slower than with PSLN-212. (4) Freedom to operate cannot be judged from the data; *external:* manganese–cyclic-dinucleotide particles and surfactant-like liposomes are both described in the academic literature. '
    'If the committee weighs these above an unreplicated mouse signal, dropping is defensible. My recommendation is to spend the eleven months to Gate 1 first: by then the safety, benchmark and attribution questions each have a yes-or-no answer for the cost of a mouse and cell programme, and a freedom-to-operate review can run alongside.')

# =====================================================================================================
sec('§7')
D.h1('7. What I considered and ruled out')
D.table('Table 10. Options and interpretations considered and rejected',
  ['Considered', 'Why ruled out'],
  [['**Take PSLN-212 forward**, alone or alongside PSLN-344', f'{n("survA_212")} survival in aged mice. In young mice it equals PSLN-344 on survival ({n("y212")} each) and recovers somewhat faster at day 180, but young adults are not where the unmet need is, and PSLN-212 was never compared with a current vaccine. Running both doubles toxicology and manufacturing for no added market.'],
   ['**Go straight to IND-enabling work**', 'Five open questions in Section 1, each able to stop the program, can be answered first for far less.'],
   ['**Drop now**', f'The effect is large, is present in {n("h2h_ahead")} head-to-head experiments and survives the worst-case reading ({n("survF_344")} vs {n("survF_212")}).'],
   ['**PSLN-344 as a stand-alone antiviral or emergency prophylactic**', f'Without antigen it protected {n("h_adj")} [S15-H].'],
   ['**Young-adult, general-population or paediatric positioning**', 'No advantage in young mice (Table 4); no juvenile data.'],
   ['**Oncology positioning** (the usual home of STING agonists)', 'There is not one tumour experiment in the data set.'],
   ['**Adding the TLR7/8 agonist R848**', f'Weight loss {n("wl_r848")} (worst {n("wl_r848_worst")}), not recovered by day 10 [S08-D]; interferon-β at 16 h {n("ifn16_r848")}-fold, below PSLN-344 ({n("ifn16_344")}); combined with PSLN-344 it lowered interferon-β ({n("dr_344r848_20")} vs {n("dr_344_20")}-fold at 20 µg) [S01-A, S08-A].'],
   ['**cGAMP as payload** (CMP-204)', f'Interferon-β {n("ifn16_cmp")}-fold in aged lung, against {n("ifn16_212")} for CDN-1807 without manganese; {n("S03-I_cmp")} survival [S01-A, S03-I].'],
   ['**Rescuing PSLN-212 with GM-CSF or a booster**', f'GM-CSF rescue is a mechanistic tool (four daily doses of a recombinant protein; no survival data) [S02-G]. After a booster, PSLN-212 IgG was {n("boost_h1_212")} (H1N1) and {n("boost_h3_212")} (H3N2), still below one dose of PSLN-344 ({n("igg_h1_344")}; {n("igg_h3_344")}) [S13-I/J, S03-A/E]; no challenge was done.'],
   ['**"Manganese works by improving delivery"**', f'Encapsulation is the same ({n("ee_344").split(" ")[0]} vs {n("ee_212").split(" ")[0]}); the half-maximal dose is the same; only the ceiling rises [S08-A, S08-B]. The uptake block is unresolved (Q14).'],
   ['**Reading the workbook as printed**', f'Would have shown PSLN-344 with the lowest IgG2a/IgG1 ratio ({n("ratio_h1_printed344")}; recomputed value {n("ratio_h1_344")}), a second "16 h" cytokine panel, and an independent replicate of the rgH5N1 result. See Appendix A.'],
   ['**Using these blocks as evidence**', f'S11-B (neutrophils; duplicate), S07-C (both columns carry the same label; {n("s07c")}), S05-A/B (two animals per point, contradictory conditions), S08-C (conflicts with S01-B), S08 rows 89–101 (unlabelled).'],
   ['**Fisher tests on single experiments as the main analysis**', f'{n("power_n7")} power at 7 per arm. I pooled across experiments with stratification and give the individual results in Figure 2.'],
   ['**Arithmetic means for titres; "0" HAI titres as zero**', 'Titres analysed on the log scale with geometric means; HAI below the lowest dilution (1:10) set to 5.'],
   ['**Claims I do not think the data support**', f'"Restores the aged response to young" (CD40/CD86 at {n("cd40_pctyoung")}/{n("cd86_pctyoung")} of young); "sterilising" (weight loss {n("morb_344")}); "durable" ({n("d60_344")} at day 60 in aged mice, nothing later; slower recovery than PSLN-212 at day 180 in young mice); "safe for the brain" (three transcripts, one time point); "universal influenza vaccine" (survival only, in mice).']],
  [2.15, 4.85])

# =====================================================================================================
sec('App.')
D.pagebreak()
D.h1('Appendix A. Data-quality log')
D.p('Every flag was derived by script from the workbook and the annotation (qc_log.py and the qc_*.csv files in the analysis folder). The rating reflects the effect on conclusions, not a judgement about cause.')
D.table(None, ['ID', 'Rating', 'Blocks', 'Finding and evidence', 'Effect', 'Handling here / action for Gate 0'],
        [[r.ID, r.Severity, r.Blocks, f'**{r.Finding}** {r.Evidence}'.replace('>=', '≥ ').replace('->', '→'), r.Impact.replace('>=', '≥ ').replace('->', '→'), f'{r.Handling_in_this_analysis} / {r.Gate0_action}'.replace('->', '→')] for r in q.itertuples()],
        [0.33, 0.5, 0.95, 2.9, 1.25, 1.07], small=True)

# ---- consistency checks between hand-written table text and the computed QC log
qtxt = {r.ID: r.Evidence for r in q.itertuples()}
assert '21/21' in qtxt['Q02'] and '8 of 20' in qtxt['Q04'] and 'r=0.997' in qtxt['Q04'] and '40 of the 42' in qtxt['Q05'] and '6/7 animals' in qtxt['Q06'], 'QC text mismatch'

D.h1('Appendix B. Evidence ledger: source of each data-derived number')
D.p('In order of first appearance in the text (the column "Cited" gives the section): value as cited, what it is, where it comes from and how it was computed. The evidence workbook (PSLN_evidence_workbook.xlsx) holds the same table with the raw values, plus every other computed number, per-block statistics and the tidy data. Design parameters of the proposed studies and the counts quoted from Appendix A are not repeated here.')
APPB_INDEX = len(D.items)

def finish():
    L = _LED.copy()
    order = {k: i for i, k in enumerate(USED.keys())}
    Lu = L[L.Key.isin(USED.keys())].copy(); Lu['ord'] = Lu.Key.map(order); Lu['Section'] = Lu.Key.map(USED); Lu = Lu.sort_values('ord')
    D.items.insert(APPB_INDEX, ('table', None, ['ID', 'Cited', 'Value as cited', 'What it is', 'Source blocks (cells)', 'Method'],
        [[r.ID, r.Section, r.Value_as_cited, r.Description.replace('>=', '≥ ').replace('->', '→'), (r.Source_blocks + (f' ({r.Cells})' if isinstance(r.Cells, str) and r.Cells else '')), r.Method.replace('->', '→')] for r in Lu.itertuples()],
        [0.36, 0.38, 0.95, 2.55, 1.56, 1.2], True, None, True, False))
    return L, Lu

D.h1('Appendix C. Methods')
D.bullets([
  f'**Data handling.** All 15 sheets were read cell by cell using explicit block coordinates (blocks.py). Of {n("cells_total")} numeric cells, {n("cells_data")} are data values, {n("cells_axis")} are axis values (days, hours, doses) and {n("cells_orphan")} belong to an unlabelled region (Q15). No value was altered. Block names are the workbook\'s; the second blocks labelled S06-E and S06-F are called S06-E2 and S06-F2, and the two S09-A panels "left" and "right".',
  '**Statistics for single-time-point blocks.** As stated in the annotation: one-way ANOVA with Tukey\'s test across all groups of the block. In addition, for each contrast: Welch\'s t-test with a 95% interval, and the exact Mann–Whitney test (with five animals per group its smallest possible two-sided p is 0.008). '
  'Titres and fold-change transcripts were analysed on the log10 scale and summarised as geometric means; HAI values of 0 are below the lowest dilution tested (1:10) and were set to 5; S09-A is stored as log10.',
  '**Time courses.** Two-way ANOVA (group × time) with Tukey\'s test; Welch tests at each time point.',
  '**Survival.** Status 1 = death, 0 = alive at the end of observation. Proportions with exact (Clopper–Pearson) intervals; log-rank tests per experiment (reproduced exactly by R survival::survdiff), with permutation p-values and Fisher tests in the workbook. '
  'Pooled analyses are stratified by experiment: stratified log-rank, Cox model with strata, Mantel–Haenszel survival difference with Greenland–Robins variance, Cochran–Mantel–Haenszel test.',
  '**Weight traces.** An animal is counted as dead when its series ends before day 14, or when its value is frozen through day 14 (identical at the last three time points, or at the last two if below 90% of starting weight); the annotation describes such groups as "declining". Used only for cross-checks and the worst-case analysis.',
  '**Dose-response.** Three-parameter Hill model, fold = 1 + Emax·Dʰ/(ED50ʰ + Dʰ), least squares on individual values.',
  '**Comparison with the young benchmark.** Group mean (geometric for titres) of the aged group divided by that of young mice given PSLN-212 in the same block.',
  '**Power.** Exact power of the two-sided Fisher test at 5% by enumeration of binomial outcomes.',
  '**Multiplicity.** p-values are not adjusted across blocks. The argument rests on effect sizes, intervals and consistency across independent blocks.',
  '**Limits.** I had the workbook and its annotation only: no instrument files, animal identifiers or protocols. I cannot verify randomisation, blinding or whether experiments were repeated. No external data source was consulted; the statements marked external are from general knowledge and are not needed for any number.',
  '**Software.** Python 3.11 (pandas, scipy, statsmodels, matplotlib, reportlab) and R (survival). Scripts are in the analysis folder and regenerate every table, figure and number.'])

if __name__ == '__main__':
    L, Lu = finish()
    out_pdf = os.path.join(OUTDIR, 'PSLN_portfolio_proposal.pdf'); out_md = os.path.join(OUTDIR, 'PSLN_portfolio_proposal.md')
    D.to_pdf(out_pdf, 'PSLN program: portfolio recommendation and next-step proposal · 1 November 2026 · data cut 3 September 2026')
    D.to_md(out_md)
    Lall = L.copy(); Lall['Cited_in_proposal_section'] = Lall.Key.map(USED).fillna('')
    Lall.to_csv('evidence_ledger_with_usage.csv', index=False)
    print('built', out_pdf, '| ledger rows cited:', len(Lu), 'of', len(Lall))
