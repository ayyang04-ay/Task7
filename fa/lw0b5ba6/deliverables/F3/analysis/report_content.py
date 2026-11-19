"""Content of the committee proposal.  All numbers come from ledger.pkl (built and cross-checked by build_ledger.py)."""
import pickle, numpy as np, pandas as pd
_d = pickle.load(open('ledger.pkl','rb')); F = _d['F']; LEDGER = _d['L']
per = pd.read_csv('survival_per_experiment.csv'); tests = pd.read_csv('survival_tests.csv'); a2 = pd.read_csv('audit_02_survival_vs_weight.csv')

def fr(d): return f"{d['k']}/{d['n']}"
def pc(d): return f"{d['pct']:.0f}%"
def t2(x): return f"{x[0]}/{x[1]}"
def pf(p):
    import math
    if p < 0.0001: return '< 0.0001'
    if p < 0.001: return f'{p:.4f}'
    if p < 0.01: return f'{p:.3f}'
    return f'{p:.2f}' if p >= 0.095 else f'{p:.3f}'
g = F['gmcsf']; c72 = F['c72']; c16 = F['c16']; cns = F['cns']

DOC = []
def H1(t): DOC.append(('h1', t))
def H2(t): DOC.append(('h2', t))
def P(t): DOC.append(('p', t))
def B(items): DOC.append(('bullets', items))
def BOX(title, items): DOC.append(('box', title, items))
def T(header, rows, widths, caption=None, fs=7.4): DOC.append(('table', header, rows, widths, caption, fs))
def IMG(path, width_mm, caption): DOC.append(('img', path, width_mm, caption))
def PB(): DOC.append(('pagebreak',))
def NOTE(t): DOC.append(('note', t))

TITLE = 'PSLN-344: portfolio review proposal'
SUBTITLE = 'Recommendation, next studies, target population, mechanism and biomarkers, grounded in the program dataset'
META = ('Prepared for the portfolio committee, 1 November 2026. Basis: psln_program_dataset.xlsx (15 sheets; all 6,120 observations parsed) and psln_program_annotation.pdf. '
        'Square-bracket references ([L..], [Q..]) point to the evidence ledger in Appendix A, which gives the workbook cells and analysis behind every number.')

# ------------------------------------------------------------------------------------------------------------------
H1('1. Recommendation')
P('**Keep PSLN-344 in the portfolio, conditionally.** Re-scope it as an intranasal influenza-vaccine adjuvant for older adults, fund only work packages 0 to 2 of section 4, and hold any IND-enabling spend until they pass. '
  'If the asset you have in mind is the manganese-free drug-plus-liposome (PSLN-212), the data say drop it for this use.')
BOX('The asset, as the data define it', [
 'I have taken the asset to be **PSLN-344**: the STING agonist CDN-1807 plus manganese (Mn²⁺) in a surfactant-mimicking liposome, given intranasally.',
 f"All efficacy data are as a **vaccine adjuvant**, given with inactivated influenza vaccine. Alone it protected {t2(F['ag']['3d PSLN-344'])} animals [L16].",
 'The same drug and liposome **without manganese** is the comparator PSLN-212, the arm that fails in aged animals [L02]. There is no manganese-only control.',
 'All data are from mice; the BALB/c animals that carry most of the evidence were female. "Aged" means 20 months or older, "young" 7 to 8 weeks, "Sham" vaccine with empty liposome.'])
P('**Why keep it**')
B([f"**It turns a vaccine that fails in aged animals into one that protects.** Across ten experiments, {fr(F['p344'])} aged mice ({pc(F['p344'])}) survived lethal influenza challenge after one intranasal dose of vaccine with PSLN-344, against {fr(F['p212'])} ({pc(F['p212'])}) with PSLN-212 and {fr(F['psham'])} with vaccine plus empty liposome: a difference from PSLN-212 of {F['rd']['rd']:.0f} points (95% CI {F['rd']['newcombe']}) [L01, L02, L03, L05].",
   f"**The result survives the least favourable reading of the record problems** in section 9: {F['adverse']['a']} against {F['adverse']['b']} [L06].",
   f"**Protection is broad and fast.** It held against viruses of a different subtype from the vaccine ({t2(F['het']['PSLN-344'])} against {t2(F['het']['PSLN-212'])}) [L09b], 2 to 3 days after the single dose ({fr(F['early344'])}) [L08], in two further mouse strains ({t2(F['b6']['PSLN-344'])} each) [L14] and after prior influenza infection ({t2(F['imp344'])}) [L15].",
   f"**The immunology agrees.** PSLN-344 closes a median {F['rest']['median']:.0f}% of the gap between aged and young responses across {F['rest']['n']} read-outs [L43]."])
P('**Why only conditionally**')
B(["**The record is not audit-clean.** One experiment appears twice, nine survival counts disagree with their own weight tables and three blocks carry demonstrably wrong headers (section 9). None changes the conclusion, but a committee that checks will find them.",
   "**Attribution is untested.** With no manganese-only arm and no STING-deficient host, the data cannot show that the STING agonist, rather than the manganese, restores protection (section 6).",
   "**Nothing bridges to people:** no human-cell data, second species, licensed vaccine antigen or licensed comparator.",
   f"**The safety package is thin.** Lung transcripts for the inflammatory cytokines TNF and IL-6 were still {c72['Tnf'][0]:.1f}- and {c72['Il6'][0]:.1f}-fold above baseline at 72 h, the last time measured [L62]; the only central-nervous-system (CNS) data are three transcripts at one time point [L63]; manganese disposition was not measured.",
   f"**The benefit is specific to aged hosts and fades.** Young animals are fully protected without manganese ({t2(F['y212'])}; with it {t2(F['y344'])}) [L17]; aged survival falls from {F['wane']['k1']}/{F['wane']['n1']} within two weeks to {fr(F['d60_344'])} at day 60 [L11]."])
P('**Decision requested:** approve work packages 0 to 2, agree the stop rules in section 4 now, and review at Gate 1.')

# ------------------------------------------------------------------------------------------------------------------
H1('2. How the asset looks')
T(['Question', 'What the data show', 'Ref'], [
 ['Does it protect aged animals from death?', f"PSLN-344 {fr(F['p344'])} ({pc(F['p344'])}; 95% CI {F['p344']['lo']:.0f} to {F['p344']['hi']:.0f}%). PSLN-212 {fr(F['p212'])} ({pc(F['p212'])}). Vaccine + empty liposome {fr(F['psham'])} ({F['psham']['pct']:.0f}%). Young animals on PSLN-212 {fr(F['pyoung'])} ({pc(F['pyoung'])}).", 'L01 to L04'],
 ['How sure is the difference?', f"{F['rd']['rd']:.0f} points (95% CI {F['rd']['newcombe']}). Each experiment has only 7 to 10 animals per arm, so the weight of evidence is the replication: ten experiments, all in the same direction. Least favourable reading of the records: {F['adverse']['a']} against {F['adverse']['b']}.", 'L05, L06'],
 ['Across virus subtypes?', f"Challenge virus of a different subtype from the vaccine: {t2(F['het']['PSLN-344'])} against {t2(F['het']['PSLN-212'])}. Wild-type H5N1: {fr(F['h5']['PSLN-344'])} against {fr(F['h5']['PSLN-212'])} (comparator labels in that experiment are unconfirmed).", 'L09b, L12'],
 ['How soon after the dose?', f"Challenge 2 to 3 days after a single dose: {fr(F['early344'])} ({pc(F['early344'])}) against {fr(F['early212'])} for PSLN-212.", 'L08'],
 ['How long does it last?', f"Challenge at day 60: {fr(F['d60_344'])} ({pc(F['d60_344'])}) against {fr(F['d60_212'])} for PSLN-212 and {fr(F['d60_y'])} in the young. Within two weeks it was {F['wane']['k1']}/{F['wane']['n1']} (p = {pf(F['wane']['p'])} for the decline). There are no aged data beyond day 60.", 'L08 to L11'],
 ['In other hosts?', f"C57BL/6: {t2(F['b6']['PSLN-344'])} against {t2(F['b6']['PSLN-212'])}. Outbred Swiss Webster: {t2(F['sw']['PSLN-344'])} against {t2(F['sw']['PSLN-212'])}. 14-month animals: {t2(F['mid344'])} against {t2(F['mid212'])}, the same with or without prior infection ({t2(F['imp344'])} and {t2(F['nai344'])}). The BALB/c animals were all female.", 'L14, L15'],
 ['Does it work without antigen?', f"No. Dosed 3 days before challenge: PSLN-344 alone {t2(F['ag']['3d PSLN-344'])}, vaccine alone {t2(F['ag']['3d Vaccine'])}, both together {t2(F['ag']['3d Vaccine+PSLN-344'])}.", 'L16'],
 ['Any advantage in young animals?', f"None on survival: young animals are already at {t2(F['y212'])} without manganese, so there is no room to improve. On immune read-outs manganese adds much less in young than in aged animals: Ifnb1 {F['ageint']['S01-A/16h']['y']:.1f}-fold against {F['ageint']['S01-A/16h']['a']:.1f}-fold; antigen-bearing dendritic cells +{F['ageint']['S02-C']['y']:.1f} against +{F['ageint']['S02-C']['a']:.1f} points (interaction p = {pf(F['ageint']['S01-A/16h']['p'])} and {pf(F['ageint']['S02-C']['p'])}).", 'L17, L55, L55b'],
 ['How much of the aged immune deficit is corrected?', f"A median {F['rest']['median']:.0f}% of the aged-to-young gap across {F['rest']['n']} read-outs (range {F['rest']['min']:.0f} to {F['rest']['max']:.0f}%). Weakest on the activation markers of dendritic cells: CD40 {F['cd40']['rest']:.0f}%, CD86 {F['cd86']['rest']:.0f}%.", 'L43, L29a, L29b'],
 ['Are survivors spared illness?', f"No. Survivors' weight fell to {F['nadir344'][0]:.0f} to {F['nadir344'][1]:.1f}% of baseline before recovering (young: {F['nadiry'][0]:.0f} to {F['nadiry'][1]:.1f}%). The claim the data support is protection from death, not from infection.", 'L19'],
], [38, 118, 18], caption='Table 1a. Headline evidence: protection.', fs=7.1)
IMG('../figures/fig1_survival_by_experiment.png', 165, 'Figure 1. Survival in each aged-animal experiment (survival tables as printed) and pooled. E05 is shown but excluded from pooling because its table duplicates E06.')
IMG('../figures/fig2_pooled_kaplan_meier.png', 143, 'Figure 2. Pooled survival curves. Panel B includes untreated, unchallenged animals of the same age, which shows how much mortality age alone contributes at that stage.')
P(f"Three readings of these data matter for positioning. First, PSLN-212 is weak in aged animals but not inert ({fr(F['p212'])} against {fr(F['psham'])} for empty liposome, p = {pf(F['p212_vs_sham']['p'])}) [L02b]; manganese raises an existing effect rather than creating one. "
  f"Second, PSLN-344 does not fully reach the young benchmark ({F['p344_vs_young']['a']} against {F['p344_vs_young']['b']} in the nine experiments that contain both arms) [L04b]. "
  f"Third, the day-60 shortfall is probably real rather than old age: untreated, unchallenged animals of the same age lost {F['un_dead'][0]} of {F['un_dead'][1]} over the same two weeks [L18], but those animals left the study at {F['term'][3]:.1f} to {F['term'][4]:.1f}% of starting weight, whereas the PSLN-344 animals that died had fallen to {F['term'][0]:.1f} to {F['term'][1]:.1f}% [L20], the pattern of infection.")
IMG('../figures/fig3_restoration_of_aged_response.png', 150, 'Figure 3. Share of the gap between aged and young responses that PSLN-344 closes (0% = aged animals on PSLN-212; 100% = young animals on PSLN-212).')
T(['Question', 'What the data show', 'Ref'], [
 ['Tolerability signals so far', f"Weight after vaccination dipped to {F['react']['nadir']:.1f}% against {F['react']['vac']:.1f}% for vaccine alone and recovered by day 10. Lung Tnf and Il6 transcripts {c72['Tnf'][0]:.1f}- and {c72['Il6'][0]:.1f}-fold above baseline at 72 h. Tnf transcript in the CNS {cns[('Tnf','PBS')][0]:.2f} times buffer.", 'L60, L62, L63'],
 ['Does the proprietary agonist matter?', f"Partly shown. In the same liposome without manganese, CDN-1807 gives about twice the interferon signal of cGAMP ({F['ifnb16']['b']:.0f}- against {F['cmp']['ifnb']:.0f}-fold, p = {pf(F['cmp']['p_ifnb'])}) and about twice the antibody, though that second difference is not statistically secure (IgG {F['igg_h1']['b']:.0f} against {F['cmp']['igg']:.0f}, p = {F['cmp']['p_igg']:.2f}). Nothing combines cGAMP with manganese, so whether CDN-1807 is still needed once manganese is present is untested.", 'L57'],
 ['Is the vehicle right?', f"It does what it was designed to do: uptake by alveolar macrophages depends on surfactant proteins ({F['spad']['a']:.0f}% against {F['spad']['b']:.0f}% in knockouts), it carries cargo into alveolar epithelium ({F['srb2']['a']:.1f}% against {F['srb2']['b']:.1f}% for free dye), and alone it is inert ({fr(F['psham'])}). Whether it is the best vehicle is untested: there is no free-drug or alternative-vehicle arm, and encapsulation is {F['ee']['mean']:.0f}%.", 'L45, L46a, L03, L64'],
 ['Is the dose right?', f"Unknown. Every efficacy experiment used 20 µg. At that dose the interferon marker is {F['dose']['d20']:.0f}-fold against a fitted ceiling of {F['dose']['emax']:.0f}-fold, and 40 µg adds nothing (ratio {F['dose']['d40']/F['dose']['d20']:.2f}). No lower dose was tested for protection.", 'L59'],
], [38, 118, 18], caption='Table 1b. Headline evidence: tolerability, components and dose.', fs=7.1)
P(f"**Tolerability.** Three small blocks bear on it (Figure 4). After vaccination without challenge, weight dipped to {F['react']['nadir']:.1f}% with PSLN-344 against {F['react']['vac']:.1f}% with vaccine alone (difference {F['react']['diff']:.1f} points, 95% CI {F['react']['lo']:.1f} to {F['react']['hi']:.1f}) and was back to {F['react']['d10']:.1f}% by day 10 [L60]. "
  f"The early cytokine response in aged lung was no larger than the manganese-free formulation produces in young lung for Il6 and Ccl2 ({F['c16y']['Il6'][0]:.1f}- and {F['c16y']['Ccl2'][0]:.1f}-fold of it) but was higher for Tnf ({F['c16y']['Tnf'][0]:.1f}-fold) and Il10 ({F['c16y']['Il10'][0]:.1f}-fold) [L61]. "
  f"By 72 h young lungs were back to baseline for Tnf ({c72['Tnf'][2]:.1f}-fold) while aged lungs on PSLN-344 were at {c72['Tnf'][0]:.1f}-fold [L62]. Part of that is age, since aged lungs on PSLN-212 were at {c72['Tnf'][1]:.1f}-fold, but there is no later time point to show that it resolves. "
  f"In the central nervous system PSLN-344 did not differ from vaccine plus empty liposome on any of three transcripts, while cholera toxin, the positive control, gave {F['cns_ct']['Isg15'][0]:.1f}- to {F['cns_ct']['Ifnb1'][0]:.1f}-fold [L63]. That study could not exclude a two-fold rise in Tnf, and nothing was measured about manganese itself.")
IMG('../figures/fig4_safety.png', 168, 'Figure 4. Tolerability data. A: body weight after intranasal vaccination without challenge. B: lung cytokine transcripts at 16 h and 72 h. C: central-nervous-system transcripts at 36 h.')
P(f"**Dose.** The interferon marker rises with dose and levels off between 20 and 40 µg (Figure 5). Manganese raises the ceiling of the response rather than its potency: the half-maximal dose is {F['dose']['ed50']:.0f} µg with manganese and {F['dose']['ed50_212']:.0f} µg without, while the fitted maximum is {F['dose']['emax']:.0f}-fold against {F['dose']['emax212']:.0f}-fold. About {F['dose']['eq']:.1f} µg of PSLN-344 is predicted to match 20 µg of PSLN-212 on this marker [L59]. If protection tracks the marker, the protective threshold lies between the {F['ifnb16']['b']:.0f}-fold that fails and the {F['ifnb16']['a']:.0f}-fold that protects [L21], which corresponds to somewhere between about 7 and 20 µg: there may be little room to lower the dose and nothing to gain by raising it. Only a dose-ranging study with protection as the read-out can settle this.")
IMG('../figures/fig5_dose_response.png', 78, 'Figure 5. Lung Ifnb1 at 16 h against intranasal dose, with fitted curves.')

# ------------------------------------------------------------------------------------------------------------------
H1('3. What we give up if we drop it')
T(['We would be giving up', 'Evidence', 'Ref'], [
 ['The only formulation in our file that protects aged animals', f"PSLN-344 {fr(F['p344'])}. The alternatives we hold do not: PSLN-212 {fr(F['p212'])}; the cGAMP version (CMP-204) {F['homo']['CMP-204']['k']}/7 in its one aged challenge test; vaccine + empty liposome {fr(F['psham'])}.", 'L01, L02, L03, L57'],
 ['Protection across subtypes from one intranasal dose, including H5N1', f"Different-subtype challenge {t2(F['het']['PSLN-344'])} against {t2(F['het']['PSLN-212'])}; wild-type H5N1 {fr(F['h5']['PSLN-344'])}. This is the property relevant to mismatched seasons and to pandemic preparedness.", 'L09b, L12'],
 ['Onset within days', f"{fr(F['early344'])} survive a challenge given 2 to 3 days after the dose.", 'L08'],
 ['Evidence that the aged deficit can be corrected at its source', f"The first interferon signal in aged lung returns to the young level ({F['ifnb16']['a']:.0f}-fold against {F['ifnb16']['b']:.0f}-fold for PSLN-212; young {F['ifnb16']['y']:.0f}-fold) and most downstream responses follow.", 'L21, L43'],
 ['Robustness to genetic background and prior infection', f"Two further strains ({t2(F['b6']['PSLN-344'])} each); previously infected animals {t2(F['imp344'])}.", 'L14, L15'],
], [52, 104, 18], caption='Table 2a. What dropping the asset would cost.')
T(['We would not be giving up, because the data do not contain it', 'Why', 'Ref'], [
 ['A stand-alone STING-agonist product', f"Without antigen PSLN-344 protected {t2(F['ag']['3d PSLN-344'])}. Every efficacy result is as an adjuvant.", 'L16'],
 ['An advantage in young or general adult populations', f"Young animals: {t2(F['y344'])} with PSLN-344, {t2(F['y212'])} without manganese.", 'L17, L55b'],
 ['Proof that the STING agonist is the active principle', 'No manganese-only arm; no STING-deficient host.', 'section 6'],
 ['Evidence in human cells or a second species; a safety package; a clean record', 'Absent from the file; see sections 4 and 9.', 'Q01 to Q11'],
], [52, 104, 18], caption='Table 2b. What is not at stake.')
P('Keeping the asset costs the first three work packages below. I have no information on the rest of the portfolio, so I cannot weigh that against other uses of the money.')

# ------------------------------------------------------------------------------------------------------------------
H1('4. Next studies: what each must establish and the endpoints we need to see')
P('The packages are ordered so that the cheapest questions that could end the program are asked first: package 0 needs no animals, packages 1 and 2 run side by side, and nothing after Gate 1 is committed until all three pass. Thresholds are my proposals, set from the effect sizes in the file; the committee can move them, but they should be fixed before the studies start.')
T(['Package', 'What it must establish', 'Endpoints we need to see (today\'s value in brackets)', 'Stop if'], [
 ['**0. Reconcile and lock the record** (no animals)', 'That every survival, weight and derived table matches the raw records, and that the committee sees the corrected set.',
  f"Every item in section 9 closed against source records. The duplicated day-14 H5N1 experiment either documented or withdrawn. Group identities confirmed for the same-strain H1N1 and wild-type H5N1 experiments. Corrected pooled survival still at least 70% for PSLN-344 (today {pc(F['p344'])}, lower confidence bound {F['p344']['lo']:.0f}%) and at least 40 points above PSLN-212 (today {F['rd']['rd']:.0f}; least favourable reading {F['adverse']['apct']-F['adverse']['bpct']:.0f}) [L01, L05, L06].",
  'Raw records cannot be produced for more than two of the ten experiments, or the corrected difference is below 40 points.'],
 ['**1. Confirm and attribute** (one blinded, randomised study in aged mice of both sexes)', 'That the effect reproduces under blinding and in males (the BALB/c animals so far are all female), and which component is responsible.',
  f"Arms: vaccine + empty liposome; + manganese liposome without CDN-1807; + manganese liposome with cGAMP; + PSLN-212; + PSLN-344; PSLN-344 without vaccine; untreated, unchallenged sentinels. {F['power']['cons']} per arm gives 90% power if the true rates are 70% and 15% [L65]. "
  f"Survival with PSLN-344 at least 70% and at least 40 points above PSLN-212 ({pc(F['p344'])} against {pc(F['p212'])}). Manganese-only arm at least 40 points below PSLN-344; the cGAMP-with-manganese arm shows whether the proprietary agonist is needed. Lung Ifnb1 at 16 h at least 2 times PSLN-212 ({F['ifnb16']['eff']:.1f} times). Haemagglutination-inhibition (HAI) titre, geometric mean, at least 4 times PSLN-212 with every animal at 160 or above ({F['hai_h1']['eff']:.1f} and {F['hai_h3']['eff']:.1f} times; {F['hai160']['a']}/{F['hai160']['an']}). IFN-γ⁺ CD8 T cells to a virus not in the vaccine at least 3 times PSLN-212 ({F['ifng14']['a']/F['ifng14']['b']:.1f} times). [L21, L33a, L39a, L39b, L44]",
  'Survival below 50% or less than 30 points above PSLN-212. Or the manganese-only arm matches PSLN-344: the asset as defined, a STING agonist, would then have no role.'],
 ['**2. On-target and human relevance** (cells, plus one small mouse study; runs alongside 1)', 'That PSLN-344 acts through STING, and that CDN-1807 with manganese engages human STING in the relevant cells.',
  f"STING-deficient mice: at least 90% loss of the 16-h Ifnb1 response (wild type {F['ifnb16']['a']:.0f}-fold). Human primary airway and myeloid cells from donors aged 65 or over, covering the common STING variants: dose-dependent interferon-β, CXCL10 and GM-CSF, with manganese adding at least 2-fold at matched dose (mouse: {F['ifnb16']['eff']:.1f}-fold at 20 µg; ceiling {F['dose']['emax']:.0f}- against {F['dose']['emax212']:.0f}-fold) [L21, L59].",
  'No STING dependence, or no activity on human STING.'],
 ['**Gate 1**', 'Packages 0 to 2 all pass.', 'Release packages 3 to 5.', ''],
 ['**3. Dose, durability and tolerability window** (aged mice; single and repeat dose)', 'The lowest protective dose, its margin to reactogenicity, and whether protection lasts an influenza season. Only 20 µg has been tested, and nothing beyond day 60.',
  f"Doses 2.5, 5, 10 and 20 µg (half-maximal interferon response at {F['dose']['ed50']:.0f} µg, 95% CI {F['dose']['dlo']:.0f} to {F['dose']['dhi']:.0f}) [L59]. A dose with survival of at least 70% at which weight stays at or above 95% after dosing (20 µg: {F['react']['nadir']:.1f}%, worst animal {F['react']['worst']:.1f}%) and lung Tnf and Il6 are within 2-fold of baseline by day 7 (20 µg: {c72['Tnf'][0]:.1f}- and {c72['Il6'][0]:.1f}-fold at 72 h, nothing later) [L60, L62]. Lung histology and neutrophil counts at days 3, 7 and 14; the file has no usable neutrophil data [Q07]. Durability at the chosen dose: challenge at day 60 and day 120 with unchallenged sentinels of the same age, and at least 50% survival at day 120 or a booster schedule that restores it (today {fr(F['d60_344'])} at day 60, nothing later; {F['power']['d60']} per arm detects the day-60 contrast) [L10, L65].",
  'No dose separates protection from unresolved lung inflammation, or protection is gone by day 120 and a booster does not restore it.'],
 ['**4. Manganese and nose-to-brain safety** (aged mice; one and three doses)', 'That intranasal manganese does not accumulate in the olfactory bulb or brain and causes no injury there.',
  f"Manganese by mass spectrometry in olfactory bulb, brain, lung and blood at 6 h, 24 h, 7 and 28 days, back in the control range by day 28. CNS Tnf, Ifnb1 and Isg15 at 6 h, 36 h and 7 days with the upper confidence bound of the ratio to vehicle below 1.5 (today Tnf {cns[('Tnf','PBS')][0]:.2f}, CI {cns[('Tnf','PBS')][1]:.2f} to {cns[('Tnf','PBS')][2]:.2f} against buffer; {cns[('Tnf','Sham')][0]:.2f}, CI {cns[('Tnf','Sham')][1]:.2f} to {cns[('Tnf','Sham')][2]:.2f} against vaccine + empty liposome) [L63]. Histology of olfactory epithelium, olfactory bulb and lung. Neurobehavioural observation.",
  'Persistent manganese accumulation, or neural or olfactory pathology.'],
 ['**5. Product-relevant antigen, comparator and second species**', 'That it works with an antigen format we could partner (all data use formalin-inactivated whole virus) and matches or beats what older adults receive today; and that it holds in ferrets.',
  f"Aged mice, licensed-type split or subunit antigen: cross-subtype protection retained. Against a licensed-type enhanced intramuscular vaccine: {F['power']['act50_80']} to {F['power']['act50']} per arm are needed if that comparator reaches 50% survival [L65]. Ferrets: lower virus in nasal washes than vaccine alone, HAI seroconversion, protection against a different-subtype challenge.",
  'Benefit confined to whole-virus antigen with no partner route, or no advantage over the licensed-type comparator.'],
 ['**6. Mechanism of protection and biomarker qualification** (can run with 3)', 'Which immune arm protects, and which two or three markers predict it.',
  'CD8 depletion, serum transfer, CCR2 blockade and GM-CSF neutralisation in aged mice with survival as the read-out; nasal and lung IgA, which the file lacks. A loss of 40 points of survival identifies a necessary arm. Markers and outcome measured in the same animals.',
  'Not a stop gate; it decides which biomarkers go forward.'],
 ['**7. Manufacturing readiness** (light, in parallel)', 'That the product can be made reproducibly.',
  f"Release specifications set and met by three consecutive batches for encapsulation (today {F['ee']['mean']:.0f}%, range {F['ee']['min']:.0f} to {F['ee']['max']:.0f}%), manganese-to-drug ratio, particle size and potency; stability of the freeze-dried product. Size, charge and stability data are described in the annotation but absent from the workbook [L64].",
  'Batches cannot be held within specification.'],
], [30, 34, 80, 30], caption='Table 3. Work packages, endpoints and stop rules.', fs=7.0)

# ------------------------------------------------------------------------------------------------------------------
H1('5. Target demographic')
P(f"**Primary target: adults aged 65 and over receiving seasonal influenza vaccination.** The benefit in our data is specific to aged hosts. Mice of 20 months or more correspond, by the usual approximation, to people in their sixties and older; that mapping is a convention, not something our data establish.")
T(['Population', 'What our data say', 'Position', 'Ref'], [
 ['Adults 65 and over, seasonal vaccination', f"Aged mice of three strains: {fr(F['p344'])} against {fr(F['p212'])} without manganese and {fr(F['psham'])} with vaccine + empty liposome.", 'Primary target', 'L01 to L03, L14'],
 ['Adults 50 to 64', f"In 14-month mice the manganese-free formulation had already failed ({t2(F['nai212'])} in infection-naive animals; young {fr(F['pyoung'])}), and PSLN-344 protected {t2(F['mid344'])}.", 'Plausible extension; needs its own evidence', 'L15, L04'],
 ['Older adults in outbreak or pre-pandemic settings, such as care homes or an H5N1 response', f"Protection 2 to 3 days after one dose ({fr(F['early344'])}); wild-type H5N1 {fr(F['h5']['PSLN-344'])}.", 'Secondary use; the H5N1 record needs reconciling', 'L08, L12'],
 ['Adults under 50; children', f"Young mice are fully protected by the manganese-free formulation ({t2(F['y212'])}; PSLN-344 {t2(F['y344'])}), so there is no advantage to show; no paediatric model.", 'Not supported', 'L17, L55b'],
 ['Use without vaccine', f"As prophylaxis 3 days before challenge: {t2(F['ag']['3d PSLN-344'])} protected. Treatment after infection was not tested.", 'Prophylaxis ruled out; treatment untested', 'L16'],
 ['Men; frail or immunosuppressed older adults', 'No data. The BALB/c animals were female (sex is not given for the other strains) and all were housed pathogen-free.', 'Unknown', 'annotation p. 1'],
], [42, 76, 36, 20], caption='Table 4. Populations and the data behind each.')
P('**For the TAM check, market research should size:**')
B(['People aged 65 and over in the launch geographies, and the share vaccinated against influenza each year.',
   'Within that, the share already receiving an enhanced vaccine. That segment sets the realistic price reference and is the competition.',
   'The 50-to-64 band as an upside case only.',
   'Care-home residents and government pandemic-preparedness purchasing as separate, smaller lines.',
   'The route to market. PSLN-344 needs an antigen, so the unit sold is an adjuvanted intranasal vaccine dose, either with a vaccine partner or with our own antigen supply. The TAM should be built on doses, not on a stand-alone drug.',
   'A discount for antigen format. Everything so far used whole inactivated virus. If package 5 shows the benefit needs that format, the addressable share shrinks to manufacturers who make it.',
   'Annual re-dosing. The market is yearly, and repeat-dose safety is untested.'])
BOX('Outside our data (from general knowledge; please verify before use)', [
 'High-dose, MF59-adjuvanted and recombinant influenza vaccines are the enhanced products already used in adults of 65 and over; any new product will be compared with them.',
 'The licensed intranasal influenza vaccine is live-attenuated and is not indicated for older adults.',
 'An earlier intranasal inactivated influenza vaccine with a bacterial-toxin adjuvant was withdrawn after cases of facial-nerve palsy. Regulators will expect nose-to-brain safety data, which is presumably why cholera toxin is the positive control in block S10-A.',
 'Manganese is a recognised neurotoxicant on chronic exposure and can travel along the olfactory nerve after nasal exposure in rodents.',
 'STING agonists can differ in activity between mouse and human STING, so activity in human cells cannot be assumed from mouse data.'])

# ------------------------------------------------------------------------------------------------------------------
PB()
H1('6. Mechanism of action, from our data')
P('**In one sentence:** PSLN-344 uses the lung\'s surfactant-uptake route to deliver a STING agonist with manganese to the alveolar compartment; in aged lungs this brings the early interferon-β response back to the young level and adds a GM-CSF signal that the manganese-free formulation does not produce; together these draw in CCR2⁺ monocytes and turn them into antigen-carrying dendritic cells; those cells prime cross-reactive CD8 T cells and tilt follicular T cells towards help, giving germinal centres and class-switched antibody; and the animals survive.')
IMG('../figures/fig6_mechanism_of_action.png', 172, 'Figure 6. Mechanism map. Green arrows mark links tested by an intervention in the dataset; grey, links supported only by group differences; red, links assumed but not tested.')
T(['Step', 'Evidence', 'Kind of evidence', 'Ref'], [
 ['Liposome uptake depends on surfactant proteins', f"Labelled liposome in alveolar macrophages: {F['spad']['a']:.0f}% in wild type, {F['spad']['b']:.0f}% in SP-A/SP-D knockout.", 'Intervention (young knockout mice)', 'L45'],
 ['The liposome carries cargo into alveolar epithelium', f"Dye-positive type-II cells: {F['srb2']['a']:.1f}% with liposomal dye, {F['srb2']['b']:.1f}% with free dye.", 'Formulation comparison (aged)', 'L46a, L46b'],
 ['A gap-junction blocker blunts the downstream response', f"Carbenoxolone before PSLN-344: recruited monocytes {F['cbx']['a']:.1f}% to {F['cbx']['b']:.1f}%. This fits transfer of the signal from cell to cell, though the blocker is not specific.", 'Intervention (aged)', 'L47'],
 ['Manganese restores the interferon-β burst in aged lung', f"Ifnb1 (the interferon-β gene) at 16 h: {F['ifnb16']['a']:.0f}-fold against {F['ifnb16']['b']:.0f}-fold (young {F['ifnb16']['y']:.0f}-fold); without manganese the aged lung mounts {100*F['ifnb16']['b']/F['ifnb16']['y']:.0f}% of the young response. Manganese raises the ceiling, not the potency: half-maximal dose {F['dose']['ed50']:.0f} against {F['dose']['ed50_212']:.0f} µg, maximum {F['dose']['emax']:.0f}- against {F['dose']['emax212']:.0f}-fold.", 'Group comparison; dose-response', 'L21, L59'],
 ['... and the GM-CSF signal', f"Gm-csf at 16, 36, 72 h: {g[('PSLN-344',16)]:.1f}, {g[('PSLN-344',36)]:.1f}, {g[('PSLN-344',72)]:.1f}-fold against {g[('PSLN-212',16)]:.1f}, {g[('PSLN-212',36)]:.1f}, {g[('PSLN-212',72)]:.1f}-fold.", 'Group comparison', 'L23'],
 ['Monocytes enter through CCR2', f"CCR2 antagonist: lung monocytes {F['ccr2mono']['a']:.1f}% to {F['ccr2mono']['b']:.1f}%; Ly6C⁺ macrophages {F['ccr2mac']['a']:.1f}% to {F['ccr2mac']['b']:.1f}%. Entry itself does not clearly need the interferon receptor ({F['ifnar_rec']['a']:.0f}% against {F['ifnar_rec']['b']:.0f}%, three animals per group).", 'Intervention', 'L48a, L48b, L49c'],
 ['Monocytes need interferon signalling to become dendritic cells; GM-CSF can partly substitute', f"Donor marrow lacking the interferon receptor: {F['ifnar']['a']:.0f}% to {F['ifnar']['b']:.0f}%; with added GM-CSF {F['ifnar_gm']['a']:.0f}%.", 'Intervention (marrow transfer)', 'L49a, L49b'],
 ['Added GM-CSF raises the dendritic-cell output of PSLN-212', f"GM-CSF added to PSLN-212: dendritic-cell-like monocyte progeny {F['gmrescue']['b']:.1f}% to {F['gmrescue']['a']:.1f}%; GM-CSF without adjuvant {F['gmalone']:.1f}%.", 'Intervention (aged); cells only, no survival read-out', 'L50'],
 ['Fewer CD206⁺ macrophages and regulatory T cells', f"CD206⁺ macrophages {F['cd206']['a']:.0f}% against {F['cd206']['b']:.0f}% (young {F['cd206']['y']:.0f}%); lung regulatory T cells {F['treg']['a']:.1f}% against {F['treg']['b']:.1f}% (young {F['treg']['y']:.1f}%; three animals per group).", 'Group comparison', 'L52b, L53'],
 ['Dendritic cells migrate and carry antigen to the lymph node', f"Migratory cells {F['migdc']['a']:.0f}% against {F['migdc']['b']:.0f}%; antigen-bearing cells in the node {F['ovadc']['a']:.1f}% against {F['ovadc']['b']:.1f}%, and {F['ptx_ova']:.1f}% when migration is blocked with pertussis toxin.", 'Group comparison; intervention', 'L26, L27, L28'],
 ['Dendritic cells arriving in the node can prime CD8 T cells', f"Sorted node dendritic cells drive T-cell proliferation: {F['prime']['a']:.0f}% against {F['prime']['b']:.0f}% (young {F['prime']['y']:.0f}%).", 'Group comparison (ex vivo)', 'L30'],
 ['Priming happens in the node and, independently, in the lung', f"Pertussis toxin cuts T-cell proliferation in the node ({F['ptx_mln']['a']:.0f}% to {F['ptx_mln']['b']:.0f}%) but not in the lung ({F['ptx_lung']['a']:.0f}% and {F['ptx_lung']['b']:.0f}%).", 'Intervention (three animals per group)', 'L51a, L51b'],
 ['The CD8 response needs the recruited monocytes', f"CCR2 antagonist: armed (granzyme-B-positive, GZMB⁺) lung CD8 T cells {F['ccr2cd8']['a']:.1f}% to {F['ccr2cd8']['b']:.1f}%.", 'Intervention, in young animals', 'L48c'],
 ['Cross-reactive and lung-resident CD8 T cells', f"Dividing (Ki-67⁺) lung CD8 T cells on day 3 {F['ki67']['a']:.1f}% against {F['ki67']['b']:.1f}%; IFN-γ⁺ CD8 T cells to a virus not in the vaccine {F['ifng14']['a']:.1f}% against {F['ifng14']['b']:.1f}%; lung-resident memory {F['trm']['a']:.1f}% against {F['trm']['b']:.1f}%.", 'Group comparison', 'L31, L32, L33a, L34'],
 ['Follicular help, germinal centres, antibody', f"Helper-to-regulatory ratio {F['tfhtfr']['a']:.1f} against {F['tfhtfr']['b']:.1f}; class-switch transcripts Aicda and E47 in B cells {F['aicda']['eff']:.1f}- and {F['e47']['eff']:.1f}-fold higher; germinal-centre B cells {F['gcb']['a']:.1f}% against {F['gcb']['b']:.1f}%; HAI titre {F['hai_h1']['a']:.0f} against {F['hai_h1']['b']:.0f}; IgG2a-to-IgG1 ratio, a sign of a type-1 response, {F['ratio_h1']['a']:.2f} against {F['ratio_h1']['b']:.2f}.", 'Group comparison', 'L35a to L35c, L36, L37a, L37b, L38a, L38b, L39a, L41a'],
], [44, 78, 28, 24], caption='Table 5. The chain step by step. Unless stated, values are aged animals on PSLN-344 against aged animals on PSLN-212.')
P('**What this chain does not yet establish**')
B(['**That it runs through STING.** No STING-deficient host or STING antagonist was used. The only knockout in the file is of the interferon receptor, in donor marrow.',
   f"**What manganese and the drug each contribute.** No block has a manganese-only or drug-free manganese liposome, and none pairs manganese with a different agonist. The only evidence that CDN-1807 itself matters is that it beats cGAMP in the manganese-free liposome ({F['ifnb16']['b']:.0f}- against {F['cmp']['ifnb']:.0f}-fold Ifnb1) [L57].",
   f"**Which effector protects.** No CD8 depletion, no serum transfer and no mucosal IgA. The interventions stop at cell counts; none has survival as its read-out.",
   f"**Full restoration of dendritic-cell activation.** CD40 and CD86 on lymph-node dendritic cells reach {F['cd40']['a']:.0f}% and {F['cd86']['a']:.0f}% against {F['cd40']['y']:.0f}% and {F['cd86']['y']:.0f}% in the young [L29a, L29b]. More cells arrive, but they are less activated: a residual deficit worth knowing about.",
   f"**What happens to the macrophages.** As printed, inflammatory (Ly6C⁺CCR2⁺) macrophages are {F['ccr2mac_tc']['b']/F['ccr2mac_tc']['a']:.1f}-fold fewer with PSLN-344 on day 5 ({F['ccr2mac_tc']['a']:.1f} against {F['ccr2mac_tc']['b']:.1f} ×10⁵ cells) [L52a]. That would fit monocytes being diverted into dendritic cells, but it sits oddly with a monocyte influx twice as large and a {c16['Ccl2'][0]/c16['Ccl2'][1]:.0f}-fold stronger Ccl2 signal [L24, L61], and the neighbouring block on the same sheet is mislabelled [L54]. I have not built on it [Q11].",
   f"**Durability of the follicular effect.** The fall in regulatory follicular T cells is gone by day 30 ({F['tfr30']['a']:.1f}% against {F['tfr30sham']:.1f}% with empty liposome) [L35d].",
   'The chain is assembled from experiments in different strains and ages: the marrow-transfer and CCR2-to-CD8 experiments used young animals, and several blocks do not state strain or age. Two further blocks that would have closed gaps cannot be used because of labelling (S08-C, S07-C; section 9).'])

# ------------------------------------------------------------------------------------------------------------------
H1('7. Biomarkers to validate efficacy')
P('The table lists markers the data already support, in the order they occur, with a pass mark for the next study read off the present values. Values are aged animals on PSLN-344 against aged animals on PSLN-212, with young animals on PSLN-212 in brackets.')
T(['Marker', 'Sample, time', 'Today', 'What it shows', 'Suggested pass mark', 'Ref'], [
 ['Ifnb1 mRNA', 'Lung, 16 h', f"{F['ifnb16']['a']:.0f}× vs {F['ifnb16']['b']:.0f}× ({F['ifnb16']['y']:.0f}×)", 'Target engagement', f"At least 2× the manganese-free comparator; at most 5× by 72 h (today {F['ifnb72']['a']:.1f}×)", 'L21, L22'],
 ['Gm-csf mRNA', 'Lung, 16 to 36 h', f"{g[('PSLN-344',16)]:.1f} to {g[('PSLN-344',36)]:.1f}× vs {g[('PSLN-212',16)]:.1f} to {g[('PSLN-212',36)]:.1f}×", 'The step that separates PSLN-344 from PSLN-212', 'At least 4× comparator at 36 h', 'L23'],
 ['Monocytes; CD11b⁺ dendritic cells', 'Lung, day 4', f"{F['mono']['v']['PSLN-344']:.0f}% vs {F['mono']['v']['PSLN-212']:.0f}% ({F['mono']['v']['PSLN-212(Y)']:.0f}%); {F['cd11bdc']['v']['PSLN-344']:.0f}% vs {F['cd11bdc']['v']['PSLN-212']:.0f}% ({F['cd11bdc']['v']['PSLN-212(Y)']:.0f}%)", 'Cellular response', 'Each at least 1.5× comparator', 'L24, L25'],
 ['CCR7⁺ migratory dendritic cells', 'Lung, 72 h', f"{F['migdc']['a']:.0f}% vs {F['migdc']['b']:.0f}% ({F['migdc']['y']:.0f}%)", 'Antigen transport', f"At least 20% (lowest protected animal {F['sep']['mig'][1]:.0f}%; highest unprotected {F['sep']['mig'][0]:.0f}%)", 'L27, L66'],
 ['Helper-to-regulatory follicular T-cell ratio', 'Lymph node, day 7', f"{F['tfhtfr']['a']:.1f} vs {F['tfhtfr']['b']:.1f} ({F['tfhtfr']['y']:.1f})", 'Help for antibody', f"At least 6.5 (lowest protected {F['sep']['tfh'][1]:.1f}; highest unprotected {F['sep']['tfh'][0]:.1f})", 'L35c, L66'],
 ['HAI and neutralising titres', 'Serum, day 14', f"HAI {F['hai_h1']['a']:.0f} vs {F['hai_h1']['b']:.0f} ({F['hai_h1']['y']:.0f}); neutralising {F['nt_h1']['a']:,.0f} vs {F['nt_h1']['b']:,.0f} ({F['nt_h1']['y']:,.0f})", 'Antibody; the accepted immunogenicity read-out', 'Geometric mean at least 4× comparator; every animal at 160 or above', 'L39a, L39b, L40a, L40b, L44'],
 ['IgG2a/IgG1', 'Serum, day 14', f"{F['ratio_h1']['a']:.2f} vs {F['ratio_h1']['b']:.2f} ({F['ratio_h1']['y']:.2f})", 'Antibody quality', 'Above 1', 'L41a'],
 ['IFN-γ⁺ CD8 T cells to a virus not in the vaccine', 'Lymph node, days 14 and 60', f"{F['ifng14']['a']:.1f}% vs {F['ifng14']['b']:.1f}% ({F['ifng14']['y']:.1f}%); {F['ifng60']['a']:.1f}% vs {F['ifng60']['b']:.1f}% ({F['ifng60']['y']:.1f}%)", 'Cross-subtype cellular immunity, the likeliest basis of cross-subtype protection', f"At least 5% at day 14 (lowest protected {F['sep']['ifng'][1]:.1f}%; highest unprotected {F['sep']['ifng'][0]:.1f}%)", 'L33a, L33b, L66'],
 ['Lung-resident memory CD8 T cells', 'Lung, day 25', f"{F['trm']['a']:.1f}% vs {F['trm']['b']:.1f}% ({F['trm']['y']:.1f}%)", 'Local memory', f"At least 3% (lowest protected {F['sep']['trm'][1]:.1f}%)", 'L34, L66'],
 ['Safety: Tnf, Il6, Il10 mRNA', 'Lung, 72 h and later', f"{c72['Tnf'][0]:.1f}×, {c72['Il6'][0]:.1f}×, {c72['Il10'][0]:.1f}× (young {c72['Tnf'][2]:.1f}×, {c72['Il6'][2]:.1f}×, {c72['Il10'][2]:.1f}×)", 'Resolution of inflammation', 'Within 2× of baseline by day 7', 'L62'],
], [30, 22, 40, 30, 36, 16], caption='Table 6. Candidate biomarkers and pass marks.', fs=7.0)
P('**Four cautions.**')
B([f"At five animals per group almost every read-out separates protected from unprotected groups ({F['sep']['nsep']} of {F['sep']['n']}) [L66], so the present data cannot rank the markers. Markers and survival were also measured in different animals. Package 6 exists to settle which markers predict protection.",
   f"The conventional human benchmark, an HAI titre of 1:40, did not signal protection here: {F['hai160']['b40']} of {F['hai160']['bn']} PSLN-212 sera reached it [L44], yet PSLN-212 survival was {fr(F['p212'])} [L02]. Every protected group was at 160 or above.",
   f"One marker moved against the outcome over time. IFN-γ⁺ CD8 T cells were more frequent at day 60 than at day 14 ({F['ifng60']['a']:.1f}% against {F['ifng14']['a']:.1f}%) [L33a, L33b] while survival was lower ({fr(F['d60_344'])} against {F['wane']['k1']}/{F['wane']['n1']}) [L11]. Frequency in the lymph node is therefore not, on its own, a measure of protection.",
   'No mucosal IgA was measured, which is a notable absence for an intranasal vaccine.'])
P('For clinical translation these lung and lymph-node read-outs need accessible counterparts, such as interferon-induced proteins in nasal fluid or blood within a day of dosing, activated circulating follicular helper T cells at about day 7, HAI and microneutralisation, and interferon-γ responses to conserved internal viral proteins. None of these has been bridged in our data.')

# ------------------------------------------------------------------------------------------------------------------
H1('8. What I considered and ruled out')
T(['Considered', 'What the data say', 'Verdict', 'Ref'], [
 ['**Positioning**', '', '', ''],
 ['A stand-alone STING agonist, or antiviral prophylaxis without antigen', f"PSLN-344 alone {t2(F['ag']['3d PSLN-344'])}; with vaccine {t2(F['ag']['3d Vaccine+PSLN-344'])}.", 'Ruled out', 'L16'],
 ['An adjuvant for all adults', f"Young animals are fully protected without manganese ({t2(F['y212'])}; with it {t2(F['y344'])}), and manganese adds little to their immune read-outs (Ifnb1 {F['ageint']['S01-A/16h']['y']:.1f}-fold against {F['ageint']['S01-A/16h']['a']:.1f}-fold in aged). At day 180 the PSLN-344 group recovered weight more slowly ({F['y180']['d1']:.1f}% against {F['y180']['d2']:.1f}% on day 14).", 'Ruled out as a differentiated position', 'L17, L55b, L56'],
 ['Oncology or other STING indications', 'No data of any kind in the file.', 'Not assessed', ''],
 ['**Formulation alternatives**', '', '', ''],
 ['PSLN-212 (no manganese) for older adults', f"{fr(F['p212'])} survival in aged animals.", 'Ruled out', 'L02'],
 ['cGAMP as payload (CMP-204)', f"Ifnb1 {F['cmp']['ifnb']:.0f}-fold against {F['ifnb16']['b']:.0f}-fold for PSLN-212 and {F['ifnb16']['a']:.0f}-fold for PSLN-344; {F['homo']['CMP-204']['k']}/7 survival.", 'Ruled out', 'L57'],
 ['Adding the TLR7/8 agonist R848', f"Weight fell to {F['r848']['nadir']:.0f}% and had not recovered by day 10, with one of five animals no longer recorded; Il10 transcript {F['r848']['il10']:.0f}-fold at 16 h; on the interferon marker the R848 versions stay below PSLN-344 ({F['r848']['ifnb_212r']:.0f}- against {F['ifnb16']['a']:.0f}-fold, and {F['r848']['d20']:.0f}- against {F['r848']['d20_344']:.0f}-fold in the dose series).", 'Ruled out on tolerability', 'L58'],
 ['A higher dose', f"40 µg gives {F['dose']['d40']:.0f}-fold against {F['dose']['d20']:.0f}-fold at 20 µg (p = {pf(F['dose']['p2040'])}).", 'No case for it', 'L59'],
 ['Two doses of PSLN-212 instead of manganese', f"After a boost PSLN-212 reaches IgG titres of {F['boost_h1']['b']:,.0f} (H1N1) and {F['boost_h3']['b']:,.0f} (H3N2): below what one dose of PSLN-344 gave at day 14 ({F['igg_h1']['a']:,.0f} and {F['igg_h3']['a']:,.0f}) and {F['boost_h1']['eff']:.1f}- and {F['boost_h3']['eff']:.1f}-fold below boosted PSLN-344. No challenge data after boosting.", 'Not sufficient on antibody; not formally excluded', 'L42a, L42b, L38a, L38b'],
 ['GM-CSF given with PSLN-212', f"Raises dendritic-cell-like cells from {F['gmrescue']['b']:.1f}% to {F['gmrescue']['a']:.1f}%, but there is no efficacy read-out and it adds a biologic.", 'Mechanistic tool only', 'L50'],
 ['**Other explanations for the survival result**', '', '', ''],
 ['The liposome alone does it', f"Vaccine + empty liposome {fr(F['psham'])}.", 'Ruled out', 'L03'],
 ['It is peculiar to one mouse strain', f"C57BL/6 {t2(F['b6']['PSLN-344'])}; outbred Swiss Webster {t2(F['sw']['PSLN-344'])}.", 'Ruled out', 'L14'],
 ['It only works in hosts that have never met influenza', f"Previously infected {t2(F['imp344'])}; never infected {t2(F['nai344'])}.", 'Ruled out', 'L15'],
 ['It is antibody matched to the challenge strain', f"Different-subtype challenge {t2(F['het']['PSLN-344'])}.", 'Ruled out', 'L09b'],
 ['It is a non-specific antiviral state', f"PSLN-344 without antigen {t2(F['ag']['3d PSLN-344'])}.", 'Ruled out', 'L16'],
 ['The record errors create the effect', f"Least favourable reading {F['adverse']['a']} against {F['adverse']['b']}; weight tables alone give {F['wt344']} against {F['wt212']}.", 'Ruled out', 'L06, L07'],
 ['Day-60 deaths are just old age', f"Untreated animals of the same age lost {F['un_dead'][0]}/{F['un_dead'][1]}, but at {F['term'][3]:.0f} to {F['term'][4]:.0f}% of weight; PSLN-344 deaths came at {F['term'][0]:.0f} to {F['term'][1]:.0f}%.", 'Not supported; some waning is likely real', 'L18, L20'],
 ['**Readings of the file I rejected**', '', '', ''],
 ['The printed IgG2a/IgG1 blocks', f"As printed they give PSLN-344 the lowest ratio ({F['ratio_h1']['printed']['PSLN-344']:.2f}). Recomputed from the subclass titres it is {F['ratio_h1']['a']:.2f} against {F['ratio_h1']['b']:.2f}: the headers are rotated.", 'Recomputed', 'L41a, L41b, Q04'],
 ['Both S09-A panels as 16 h', 'The second panel reproduces the 72-h interferon values of S01-A.', 'Second panel treated as 72 h', 'Q05'],
 ['Averaging weight columns as printed', 'Dead animals are carried forward as constant values in some groups and left blank in others, so printed-cell means mix the living and the dead.', 'Decoded before use', 'Q02, L19'],
 ['Counting the day-14 H5N1 experiment (S06-C)', 'Identical, row for row, to the day-3 experiment.', 'Excluded', 'Q03'],
 ['S08-C: manganese cuts epithelial uptake four-fold', 'Conflicts with S01-B unless its headers are permuted.', 'Not used', 'Q06'],
 ['S07-C: which macrophage drives regulatory T cells', 'Both groups carry the same label.', 'Not used', 'L54'],
 ['S07-A: PSLN-344 leaves fewer inflammatory macrophages', f"As printed {F['ccr2mac_tc']['a']:.1f} against {F['ccr2mac_tc']['b']:.1f} ×10⁵ cells, which sits oddly with the larger monocyte influx and stronger Ccl2 signal; no cross-check exists and its sheet-mate is mislabelled.", 'Reported, not relied on', 'L52a, Q11'],
 ['An HAI titre of 1:40 as a sign of protection', f"{F['hai160']['b40']} of {F['hai160']['bn']} PSLN-212 sera reach it; survival {fr(F['p212'])}.", 'Rejected as a pass mark', 'L44, L02'],
], [46, 84, 28, 16], caption='Table 7. Options, explanations and readings considered.', fs=7.0)

# ------------------------------------------------------------------------------------------------------------------
H1('9. Data quality: what the committee will find if it checks')
P(f"I checked every block against its stated n, every survival table against the body-weight table for the same animals, every derived block against its source, and the whole workbook for repeated values. The headline survives all of it, but the file should be corrected before it circulates. The first three rows matter most.")
T(['Finding', 'Effect on the conclusions', 'Action', 'Ref'], [
 ['One experiment appears twice. The day-14 H5N1 survival table (S06-C) is identical to the day-3 table (S06-D), and its PSLN-344 weight columns repeat those of another experiment in 40 of 42 cells.', f"One fewer independent experiment. Excluded throughout. With it the totals would be 68/80 against 11/80; without it {fr(F['p344'])} against {fr(F['p212'])}.", 'Find the day-14 records or withdraw the block.', 'Q03'],
 [f"Survival tables and weight tables disagree on the number of deaths in 9 of 69 arm-level comparisons, for example PSLN-344 in S06-D: 7/7 by the table, 5/7 by the weights.", f"Single-experiment counts are uncertain by one to three animals. The PSLN-344 total is {F['wt344']} either way. Least favourable reading: {F['adverse']['a']} against {F['adverse']['b']}. The six experiments free of duplication, label conflicts and reused trajectories give {t2(F['strict']['PSLN-344'])} against {t2(F['strict']['PSLN-212'])}.", 'Reconcile with cage records. Use one convention for dead animals in weight tables.', 'Q02, L06, L06b, L07'],
 ['Group labels differ between the survival and weight tables of the same-strain H1N1 experiment (S03-I, S13-F) and the wild-type H5N1 experiment (S03-J, S13-G).', f"The PSLN-344 arms agree ({fr(F['homo']['PSLN-344'])} and {fr(F['h5']['PSLN-344'])}). The comparator results do not: PSLN-212 is 0/7 or 3/7 in the first, and the second may have had no PSLN-212 arm.", 'Confirm group identities from the study records.', 'L12, L13, Q02'],
 ['The printed IgG2a/IgG1 blocks (S03-B, S03-F) have their headers rotated relative to the source titres.', 'Read as printed they reverse the conclusion on antibody quality. Recomputed values are used here.', 'Correct the headers.', 'Q04, L41a'],
 ['Both cytokine panels of S09-A are labelled 16 h; the second is the 72-h sample set. The same control animals are called Sham in one sheet and PBS in another.', 'Decides whether inflammation is read as resolving. On the corrected reading Tnf is still 8-fold up at 72 h.', 'Correct the label; confirm what the control received.', 'Q05, L62'],
 ['The epithelial-uptake block for PSLN-344 (S08-C) conflicts with S01-B; the macrophage-transfer block (S07-C) has one label for both groups; the macrophage time-course beside it (S07-A) runs against neighbouring blocks.', 'Three mechanistic questions stay open: whether manganese alters delivery, how the macrophage pool changes, and which macrophage drives regulatory T cells.', 'Recover the correct headers or repeat.', 'Q06, Q11, L54'],
 ['The alveolar-macrophage and neutrophil time-courses (S11-A, S11-B) share 35 of 100 values.', 'No usable neutrophil data, a safety-relevant gap.', 'Re-export from source.', 'Q07'],
 ['Stated n differs from the rows present in five blocks.', 'None on the conclusions. S05-A and S05-B are not used.', 'Correct labels or restore missing animals.', 'Q01'],
 [f"Weight tables reuse values across experiments, including whole-animal trajectories; {F['wt_dec'][0]} of {F['wt_dec'][1]:,} cells carry extra decimals, and the same four-digit fractions recur from one experiment to another.", 'Weight-based figures (morbidity, reactogenicity) are indicative only. Survival counts do not depend on them.', 'Regenerate the weight tables from balance records.', 'Q08'],
 ['Missing or ambiguous annotation: challenge details for the two extra-strain experiments, several time points, an undefined material, duplicate block names, an unlabelled region.', 'Limits interpretation of individual blocks, as flagged where used.', 'Complete the annotation.', 'Q09'],
 ['Both files were last changed in September 2026.', 'The cut-off for this analysis is September, not 1 November.', 'Confirm nothing newer exists.', 'Q10'],
], [62, 56, 38, 18], caption='Table 8. Data-quality register.', fs=7.0)

# ------------------------------------------------------------------------------------------------------------------
H1('10. Limits of this analysis')
B(['I worked only from the two files. I had no protocols, raw instrument files, or records of randomisation or blinding; the annotation mentions neither.',
   f"Groups are 3 to 10 animals. Of {F['mult']['n']} contrasts between PSLN-344 and PSLN-212, {F['mult']['bh05']} stay below 0.05 after false-discovery adjustment [L67], but any single read-out is modest evidence. The survival result rests on replication across experiments.",
   'Several readings rest on my inference from internal consistency: the identity of the second S09-A panel, the rotated headers, and treating constant terminal weights as animals that had died. The audit scripts reproduce each one; the data owners should confirm them.',
   'Statements marked as outside our data come from general knowledge and were not checked against sources here.',
   'I have no information on cost, timelines, intellectual property, competitors or the rest of the portfolio.'])

# ------------------------------------------------------------------------------------------------------------------
def appendix_B():
    order = [('S03-I','E01'),('S03-J','E02'),('S06-A','E03'),('S06-B','E04'),('S06-C','E05'),('S06-D','E06'),('S06-E(r34)','E07'),('S06-F(r34)','E08'),('S06-G','E09'),('S15-H','E10'),
             ('S06-E(r71)','E11'),('S06-F(r71)','E12'),('S15-L','E13'),('S15-N','E14'),('S09-B','Y01'),('S09-D','Y02'),('S09-F','Y03'),('S13-E','Y04')]
    rows = []
    for b, e in order:
        x = per[per.block == b]; r0 = x.iloc[0]
        def arm(a):
            r = x[x.arm == a]
            if len(r) == 0: return None
            r = r.iloc[0]; s = f"{int(r.survivors)}/{int(r.n)}"
            w = a2[(a2.surv_block == b) & (a2.group.str.replace('Naïve', 'Naive').str.strip().isin([a, a.replace('(Y)', 'Y')]))]
            if len(w) and not np.isnan(w.wt_n.iloc[0]):
                ws = int(w.wt_n.iloc[0] - w.wt_exits.iloc[0])
                if ws != int(r.survivors) or int(w.wt_n.iloc[0]) != int(r.n): s += f" [weights {ws}/{int(w.wt_n.iloc[0])}]"
            return s
        main = []
        for a, lab in [('PSLN-344', 'PSLN-344'), ('PSLN-212', 'PSLN-212'), ('Sham', 'Sham'), ('PSLN-212(Y)', 'Young PSLN-212'), ('CMP-204', 'CMP-204'), ('Untreated', 'Untreated'),
                       ('3d Vaccine+PSLN-344', 'Vaccine + PSLN-344'), ('3d PSLN-344', 'PSLN-344 alone'), ('3d Vaccine', 'Vaccine alone'),
                       ('Naive+PSLN-344', 'Naive + PSLN-344'), ('Imprinting+PSLN-344', 'Prior infection + PSLN-344'), ('Naive+PSLN-212', 'Naive + PSLN-212'), ('Imprinting+PSLN-212', 'Prior infection + PSLN-212'),
                       ('PSLN-344(Y)', 'Young PSLN-344'), ('CMP-204(Y)', 'Young CMP-204'), ('Naive', 'Naive')]:
            v = arm(a)
            if v: main.append(f"{lab} {v}")
        t = tests[(tests.block == b) & (((tests.arm1 == 'PSLN-344') & (tests.arm2 == 'PSLN-212')) | ((tests.arm1 == '3d Vaccine+PSLN-344') & (tests.arm2 == '3d PSLN-344')) | ((tests.arm1 == 'Naive+PSLN-344') & (tests.arm2 == 'Naive+PSLN-212')) | ((tests.arm1 == 'PSLN-344(Y)') & (tests.arm2 == 'PSLN-212(Y)')) | ((tests.arm1 == 'PSLN-344(Y)') & (tests.arm2 == 'Sham')))]
        pv = f"{t.iloc[0].logrank_p_exact:.4f}" if len(t) else ''
        if b == 'S15-H': pv += ' (both vs PSLN-344 alone)'
        if b in ('S06-E(r71)', 'S06-F(r71)'): pv += ' (naive arms)'
        if b in ('S09-B', 'S09-D', 'S09-F'): pv = '1.00 (young PSLN-344 vs young PSLN-212)'
        if b == 'S13-E': pv = f"{tests[(tests.block==b)&(tests.arm1=='PSLN-344(Y)')&(tests.arm2=='Sham')].iloc[0].logrank_p_exact:.4f} (young PSLN-344 vs Sham)"
        day = '' if pd.isna(r0.chal_day) else f", day {int(r0.chal_day)}"
        rows.append([e, f"{b.replace('(r34)',' (rows 32-68)').replace('(r71)',' (rows 69-98)')}<br/>{r0.cells}", f"{r0.age.replace('>=20 mo','(20 mo or more)').replace('aged','Aged').replace('young','Young')}. {r0.vaccine} vaccine; {r0.challenge.replace('homologous','same strain').replace('heterosubtypic','different subtype')}{day}", '; '.join(main), pv])
    return rows
APP_B = appendix_B()
APP_C = [
 ('h2', 'How the numbers were produced'),
 ('bullets', [
  'Parsing. Every block of the workbook is declared with explicit cell ranges in psln_blocks.py; a coverage check confirms that every non-empty cell is accounted for. The result is 6,120 observations, each with its cell address (13 of them form an unlabelled region on sheet S08 that is set aside); the remaining numeric cells are day, dose and time labels.',
  'Scales. Flow-cytometry percentages are analysed as they stand. qPCR fold-changes are analysed on the log10 scale and reported as geometric means. Antibody titres are analysed on the log2 scale and reported as geometric mean titres; HAI values printed as 0 are below the 1:10 starting dilution and are set to 5. Block S09-A is stored as log10 and is back-transformed for reporting.',
  'Tests. The methods stated in the annotation (one-way ANOVA with Tukey, two-way ANOVA, t test, log-rank) are reported alongside Welch t tests with confidence intervals, exact Mann-Whitney tests, Fisher exact tests, and log-rank tests with exact permutation p-values. Survival proportions carry Clopper-Pearson intervals. Pooled survival treats each experiment as a stratum (Cochran-Mantel-Haenszel); the interval for the pooled difference is Newcombe\'s.',
  'Body weights. Animals that leave a study appear either as blank cells or as a constant value repeated to day 14. Both are decoded (a terminal run of three or more identical values, or of two below 90%) so that dead animals are not averaged as if alive, and so that each weight table can be compared with its survival table.',
  'Share of the age gap closed. (PSLN-344 minus PSLN-212 in aged animals) divided by (young PSLN-212 minus aged PSLN-212), on the scale used for testing, with bootstrap intervals.',
  'Dose-response. fold = 1 + Emax x dose^h / (ED50^h + dose^h), fitted on the log scale with parametric-bootstrap intervals.',
  f"Header screen. Because three blocks proved to carry wrong headers, every block containing aged PSLN-212, aged PSLN-344 and young PSLN-212 was screened for group order. PSLN-344 lies between the other two in {F['screen']['inside']} of {F['screen']['n']} blocks; the exceptions are the two mislabelled ratio blocks and the 72-h interferon block [Q04].",
  'Ledger. build_ledger.py recomputes every cited number directly from the cited workbook cells, independently of the parser, and stops if any value disagrees with the analysis output.']),
 ('h2', 'Files'),
 ('bullets', [
  'analysis/psln_blocks.py, tidy_all_observations.csv: the parsed dataset, one row per observation with its cell address.',
  'analysis/audit_01 to audit_05 (scripts and CSVs): stated n against observed n; survival against weight tables; duplicated values; derived blocks against their sources; group-order screen.',
  'analysis/analysis_01 to analysis_08 (scripts and CSVs): survival; single-time-point immunology; time-courses; safety; challenge morbidity; dose-response; sensitivity, biomarker separation and power; age-by-manganese interaction.',
  'analysis/build_ledger.py, ledger.csv; PSLN-344_evidence_ledger.xlsx: the evidence ledger and supporting tables.',
  'figures/: the six figures used here, plus supp_onset_and_durability.png, a bar-chart view of survival by interval between dose and challenge.']),
]
