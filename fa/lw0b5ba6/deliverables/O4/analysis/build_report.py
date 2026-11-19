# -*- coding: utf-8 -*-
"""Builds the committee proposal (PDF + Markdown) and the claims list for the evidence ledger.
Every number is pulled from analysis outputs (keynums.json / CSVs) produced by the scripts in this folder."""
import json, re, os
import pandas as pd, numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib
FD = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')
pdfmetrics.registerFont(TTFont('DV', os.path.join(FD, 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DVB', os.path.join(FD, 'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DVI', os.path.join(FD, 'DejaVuSans-Oblique.ttf')))
pdfmetrics.registerFont(TTFont('DVBI', os.path.join(FD, 'DejaVuSans-BoldOblique.ttf')))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily('DV', normal='DV', bold='DVB', italic='DVI', boldItalic='DVBI')

A = '/tmp/outputs/analysis/'; FIG = '/tmp/outputs/figures/'; OUT = '/tmp/outputs/'
K = json.load(open(A + 'keynums.json'))
SC = pd.read_csv(A + 'survival_counts.csv'); ST = pd.read_csv(A + 'survival_tests.csv'); PO = pd.read_csv(A + 'survival_pooled_sensitivity.csv')
IR = pd.read_csv(A + 'integrity_register.csv'); BIO = pd.read_csv(A + 'biomarker_candidates.csv'); MECH = pd.read_csv(A + 'mechanism_contrasts.csv')
S10 = pd.read_csv(A + 'safety_S10A_CNS.csv'); S08D = pd.read_csv(A + 'safety_S08D_bodyweight.csv'); EM = pd.read_csv(A + 'dose_response_S08A_emax.csv')
DPC = pd.read_csv(A + 'design_power_continuous.csv'); DPS = pd.read_csv(A + 'design_power_survival.csv'); BM = pd.read_csv(A + 'dup_chance_benchmark.csv')
CON = pd.read_csv(A + 'block_contrasts.csv'); CON['level'] = CON.level.fillna('').astype(str)

CLAIMS = []   # (id, statement, blocks, cells, analysis file, method)
def claim(cid, text, blocks, cells, afile, method):
    CLAIMS.append(dict(claim_id=cid, statement=text, blocks=blocks, cells=cells, analysis_file=afile, method=method))
    return cid

# ---------------- formatting helpers
def fp(p):
    if p is None or (isinstance(p, float) and np.isnan(p)): return 'n/a'
    return '<0.001' if p < 0.001 else f'{p:.3f}' if p < 0.01 else f'{p:.2f}'
def fpe(p):
    v = fp(p)
    return 'p' + (v if v.startswith('<') else '=' + v)
def f3(x):
    if x is None: return '–'
    ax = abs(x)
    return f'{x:,.0f}' if ax >= 100 else f'{x:.1f}' if ax >= 10 else f'{x:.2f}' if ax < 1 else f'{x:.1f}'
def grp(key, g, kind='pct'):
    d = K[key]['groups'].get(g)
    if d is None: return '–'
    if kind in ('gm',): return (f"{d['gm']:,.0f}" if d['gm'] >= 10 else f"{d['gm']:.1f}")
    if kind == 'gmf': return f"{d['gm']:.1f}"
    return f"{d['mean']:.1f} ± {d['sd']:.1f}" if d['sd'] is not None else f"{d['mean']:.1f}"
def eff(key, name='mn', kind='pct'):
    e = K[key].get(name)
    if not e: return '–'
    if kind == 'pct':
        return f"{e['effect']:+.1f} pts ({e['lo']:+.1f} to {e['hi']:+.1f}); {fpe(e['p'])}"
    return f"{e['effect']:.1f}× ({e['lo']:.1f}–{e['hi']:.1f}); {fpe(e['p'])}"
def ri(key):
    e = K[key].get('ri'); return f"{e['effect']:.2f}" if e else '–'
def cellsof(key, groups):
    return '; '.join(f"{g}: {K[key]['groups'][g]['cells']}" for g in groups if g in K[key]['groups'])
def sv(block, group):
    r = SC[(SC.block == block) & (SC.group == group)]
    return f"{int(r.survivors.iloc[0])}/{int(r.n.iloc[0])}" if len(r) else '–'
def svp(block, g1, g2):
    r = ST[(ST.block == block) & (ST.g1 == g1) & (ST.g2 == g2)]
    if not len(r): return '–'
    p = r.p_logrank.iloc[0]
    return fp(p) if pd.notna(p) else 'n/a'
def mech(comp):
    r = MECH[MECH.comparison == comp].iloc[0]; return r

# ---------------- precomputed values used in several sections
def s10(an, t, ref):
    return S10[(S10.analyte == an) & (S10.test == t) & (S10.reference == ref)].iloc[0]
n344 = S08D[S08D.group == 'PSLN-344'].iloc[0]; nr = S08D[S08D.group == 'PSLN-212/R848'].iloc[0]
em344 = EM[EM.group == 'PSLN-344'].iloc[0]; em212 = EM[EM.group == 'PSLN-212'].iloc[0]
ee = K['S08-B']['groups']

# ---------------- document model: list of (kind, payload)
DOC = []
def H1(t): DOC.append(('h1', t))
def H2(t): DOC.append(('h2', t))
def P(t): DOC.append(('p', t))
def SMALL(t): DOC.append(('small', t))
def BUL(items): DOC.append(('bul', items))
def BOX(t, color='#e8f0fb'): DOC.append(('box', (t, color)))
def TAB(rows, widths, header=True, fs=7.0, zebra=True, hl=None): DOC.append(('tab', (rows, widths, header, fs, zebra, hl)))
def FIGURE(path, caption, w=175): DOC.append(('fig', (path, caption, w)))
def BR(): DOC.append(('br', None))

# =====================================================================================
# TITLE
DOC.append(('title', 'PSLN-344: portfolio review proposal'))
DOC.append(('subtitle', 'Intranasal STING-agonist adjuvant (CDN-1807 + Mn²⁺ in a pulmonary-surfactant-biomimetic liposome) for influenza vaccination of older adults'))
SMALL('Prepared for the Portfolio Review Committee · Data cut: 1 November 2026 · Sources: <i>psln_program_dataset.xlsx</i> (sheets S01–S15) and <i>psln_program_annotation.pdf</i> (19 pp.) · All analyses are reproducible from the Python scripts in <i>analysis/</i>.')
SMALL('<b>How to check a number.</b> Bracketed codes such as [S03-C] are workbook blocks. Claim IDs in the form (E12) point to the claims sheet of <i>PSLN-344_evidence_ledger.xlsx</i>, which gives the exact cell range, groups, n, statistic and analysis file. Statistics: group mean ± SD (n = 5 per group unless stated); GM = geometric mean (titres and qPCR fold-changes). Comparisons are Welch t-tests on the log₂ scale for titres and fold-changes and on the raw scale for percentages; Tukey HSD (the method stated in the annotation) is also tabulated in the ledger. Survival: log-rank and Fisher exact tests per experiment, plus an exact stratified test pooled across experiments. "Aged" means female BALB/c ≥20 months and "young" means 7–8 weeks (annotation p.1), unless a block states otherwise.')

# =====================================================================================
H1('1. Recommendation')
e_ifn = K['S01-A_16h']; e_hai1 = K['S03-C']; e_hai3 = K['S03-G']
claim('E01', 'Lung Ifnb1 16 h: PSLN-344 vs PSLN-212 (aged) and vs young PSLN-212', 'S01-A', cellsof('S01-A_16h', ['PSLN-344', 'PSLN-212', 'PSLN-212(Y)']), 'block_contrasts.csv', 'Welch t on log2')
claim('E02', 'HAI GMT H1N1 and H3N2 d14', 'S03-C; S03-G', cellsof('S03-C', ['PSLN-344', 'PSLN-212', 'PSLN-212(Y)', 'Sham']) + ' | ' + cellsof('S03-G', ['PSLN-344', 'PSLN-212', 'PSLN-212(Y)', 'Sham']), 'block_group_summary.csv; block_contrasts.csv', 'GMT; Welch t on log2 (0 -> 5)')
claim('E03', 'Restoration index median 0.71 (IQR 0.60-0.80) across 32 unflagged read-outs', 'S01-A(16h), S01-D(d4), S01-F, S02-A, S02-B, S02-C, S02-D CD40, S02-D CD86, S03-A, S03-C, S03-D, S03-E, S03-G, S03-H, S03-K, S04-A ICOShi, S04-B Foxp3, S04-D, S05-D, S05-E, S05-F, S05-G, S05-H, S05-I, S13-A, S13-B, S13-C, S13-D, S13-I, S13-J, S14-A H1N1, S14-A H3N2', 'group cell ranges in ledger sheet Group_summary', 'ledger sheet Contrasts (rows "Restoration index"); figures.py', '(344-212)/(212Y-212) on analysis scale (log2 for titres/fold)')
claim('E04', 'Pooled survival and sensitivity scenarios A-F', 'S03-I,S03-J,S06-A..G,S06-E\',S06-F\',S15-L,S15-N', 'per-animal cells in ledger sheet Tidy_survival (cell_days, cell_event)', 'ledger sheets Survival_counts, Survival_pooled, Survival_strata_flags', 'exact stratified (conditional) test; MH risk difference')
claim('I01', '18 cross-experiment animal pairs share >=4 identical live weight readings vs 0.005 expected', 'S08-D,S09-C/E/G,S13-F/G,S15-A..O', 'all body-weight cells (ledger sheet Tidy_bodyweight)', 'dup_null.py; ledger sheets Dup_chance_benchmark, Dup_trajectories, Dup_exact_highprec_bw', 'per-day empirical collision probability; Poisson-binomial expectation')
claim('I02', 'S06-C rows 3-30 identical to S06-D rows 34-61', 'S06-C; S06-D', 'S06!M3:Q30 vs S06!A34:E61', 'integrity_checks.py; ledger sheet Integrity_checks', 'cell-by-cell identity')
claim('I03', 'S11-A vs S11-B 35/100 position-matched identical values (0.85 expected)', 'S11-A; S11-B', 'S11!B3:U7 vs S11!B10:U14', 'dup_exact_bw.py; ledger sheet Dup_S11A_vs_S11B', 'position match; 20,000 permutations')
pool = PO.set_index(PO.analysis.str[0])
BOX('<b>Direct answer: on paper the asset looks scientifically promising, but it cannot be invested in on this data package. Keep it in the portfolio only as a frozen, gated asset, not as an active development programme. If we had to choose today between advancing and dropping, we would drop.</b><br/><br/><b>Recommendation: HOLD. Do not advance PSLN-344 on the current data package.</b> Freeze development spend and fund only a time-boxed verification path. '
    'The default outcome is <b>termination</b> unless both gates below are passed.<br/><br/>'
    '<b>Gate A (months 0–3): independent forensic audit</b> of the raw records behind the efficacy case. Pass = every critical finding is traced to contemporaneous raw data with a documented benign cause, and the corrected data keep the PSLN-344 > PSLN-212 direction. Fail = terminate and refer to the research-integrity process.<br/>'
    '<b>Gate B (months 3–9, only if A passes): one independent, blinded, randomised confirmatory study in aged mice at a CRO.</b> It adds the missing CDN-free Mn²⁺-liposome control, a standard-of-care benchmark, mucosal IgA and within-animal correlates. It runs alongside a Mn²⁺/CNS safety package and a minimum CMC definition. Pre-specified pass criteria are in Section 2.<br/>'
    '<b>Decision back to committee at about 9 months.</b> Translational or IND-enabling spend only if A and B both pass.', '#fdf2e3')
P('<b>Why we cannot advance today</b>')
BUL([
    f'<b>Data integrity.</b> Several findings are inconsistent with contemporaneous recording. Animal weight trajectories are duplicated across different experiments: {int(BM[BM.k_live_exact_matches==4].observed_pairs.iloc[0])} cross-experiment animal pairs share ≥4 identical live readings, against {BM[BM.k_live_exact_matches==4].expected_pairs_by_chance.iloc[0]:.3f} expected by chance (I01). Two different survival experiments have identical records (S06-C = S06-D; I02). Two different cell types share 35 of 100 position-matched values (S11-A vs S11-B; 0.85 expected; I03). Appendix A lists 5 critical, 8 major and 10 minor findings. Several headline claims rest on affected blocks: onset of protection within 2–3 days, protection in C57BL/6 and Swiss Webster mice, and 180-day durability.',
    '<b>Attribution and benchmark gaps.</b> No block tests a CDN-free Mn²⁺-liposome, so the benefit cannot be attributed to our proprietary molecule (CDN-1807) rather than to Mn²⁺. Nothing is compared with the parenteral enhanced vaccines that older adults receive today. Mucosal IgA, the reason for an intranasal product, was never measured. <i>(External context, not our data: Mn²⁺ potentiation of cGAS–STING signalling and Mn-based adjuvants are described in the published literature, so a Mn-only effect would weaken our proprietary position. IP counsel to confirm.)</i>',
    '<b>Unaddressed class-specific safety.</b> The product delivers Mn²⁺ intranasally to an elderly population. The only CNS data are three transcripts at one time point in an unspecified CNS region [S10-A]. There are no Mn biodistribution, histopathology, neurobehavioural or repeat-dose data.'])
P('<b>Why we should not drop outright today</b>')
BUL([
    f'<b>The unflagged immunology blocks are coherent and the effects are large.</b> In aged mice, lung Ifnb1 at 16 h is restored to the young level: {grp("S01-A_16h","PSLN-344")}-fold vs {grp("S01-A_16h","PSLN-212")}-fold with PSLN-212; young {grp("S01-A_16h","PSLN-212(Y)")} (E01). '
    f'HAI GMT is {grp("S03-C","PSLN-344","gm")} vs {grp("S03-C","PSLN-212","gm")} against H1N1 and {grp("S03-G","PSLN-344","gm")} vs {grp("S03-G","PSLN-212","gm")} against H3N2 (E02). '
    f'Across 32 unflagged read-outs, PSLN-344 closes a median 71% (IQR 60–80%) of the aged-vs-young deficit (E03, Figure 2).',
    f'<b>The survival advantage over the Mn-free formulation holds in every sensitivity scenario.</b> It is {pool.loc["D","MH_risk_difference_pct_points"]:.0f}–{pool.loc["A","MH_risk_difference_pct_points"]:.0f} percentage points in every scenario we built, including removing the duplicated experiment and using the less favourable of the survival and weight records. With S06-D removed, pooled survival is {pool.loc["B","PSLN344_surv"]} vs {pool.loc["B","PSLN212_surv"]} (E04, Figure 3).',
    '<b>The audit is needed in any case</b> under our data-governance obligations. One confirmatory study costs far less than the option value if the effect is real.'])
BOX('<b>If the committee decides to drop now: what we give up, and why (statement for the record).</b><br/>'
    '<i>"We are forgoing an intranasal adjuvant concept. In its unflagged internal data in aged mice, it closed most of the age-related immune deficit (median 71% across 32 read-outs), gave 8–9-fold higher HAI titres than the Mn-free formulation, and induced cross-reactive CD8 T-cell immunity to H5N1. If verified, mucosal and heterosubtypic immunity would set it apart from today\'s parenteral, strain-matched vaccines for older adults. '
    'We are dropping it because the package cannot be relied upon. It contains records duplicated across experiments that must be resolved before any use. It does not show that the benefit needs our proprietary molecule rather than Mn²⁺. It has no benchmark against the standard of care. And the safety of intranasal Mn²⁺ in the elderly has not been characterised."</i>', '#eef7ee')

# value table
P('<b>Table 0. What PSLN-344 would be worth if verified, and how much of it is verified today</b>')
rows = [['Value driver', 'Our data (aged mice unless stated)', 'Verification status']]
rows.append(['Restores innate STING output in aged lung', f'Ifnb1 16 h {grp("S01-A_16h","PSLN-344")} vs {grp("S01-A_16h","PSLN-212")}-fold; young {grp("S01-A_16h","PSLN-212(Y)")} [S01-A] (E01)', 'No integrity flag'])
rows.append(['Humoral immunogenicity in aged', f'IgG GMT {grp("S03-A","PSLN-344","gm")} vs {grp("S03-A","PSLN-212","gm")} (H1N1); HAI GMT {grp("S03-C","PSLN-344","gm")} vs {grp("S03-C","PSLN-212","gm")} [S03-A/C/G] (E02, E12a–E12e)', 'No integrity flag'])
rows.append(['Cross-reactive (heterosubtypic) CD8 immunity', f'H5N1-restimulated IFN-γ⁺ CD8 {grp("S05-F","PSLN-344")} vs {grp("S05-F","PSLN-212")}% (d14); {grp("S05-G","PSLN-344")} vs {grp("S05-G","PSLN-212")}% (d60) [S05-F/G] (E13a, E13b)', 'No integrity flag'])
rows.append(['Heterosubtypic protection', f'PR8 / H5N1 / Perth challenges: PSLN-344 4–7/7 vs PSLN-212 0–2/7 [S06-A to G] (E17)', 'Mixed: S06-B clean; S06-C/D critical; S06-A/G major'])
rows.append(['Durability (aged, day 60)', f'{sv("S06-E","PSLN-344")}, {sv("S06-F","PSLN-344")}, {sv("S06-G","PSLN-344")} vs {sv("S06-E","PSLN-212")}, {sv("S06-F","PSLN-212")}, {sv("S06-G","PSLN-212")} [S06-E/F/G]', 'Minor / moderate / major (sentinel deaths)'])
rows.append(['Works after prior infection (imprinting)', f'PSLN-344 6/7 in naive and imprinted 14-month mice [S06-E′/F′]', 'Moderate'])
rows.append(['Rapid onset (2–3 days)', f'H5N1 at d2: {sv("S03-J","PSLN-344")} vs {sv("S03-J","PSLN-212")} [S03-J]; d3: {sv("S15-H","3d Vaccine+PSLN-344")} vs vaccine alone {sv("S15-H","3d Vaccine")} [S15-H]', 'Major / critical'])
rows.append(['Generalises across mouse strains', f'C57BL/6 {sv("S15-L","PSLN-344")} vs {sv("S15-L","PSLN-212")} [S15-L]; Swiss Webster {sv("S15-N","PSLN-344")} vs {sv("S15-N","PSLN-212")} [S15-N]', 'Critical / major'])
rows.append(['Dose-sparing', f'≈7–8 µg PSLN-344 matches PSLN-212 at 20–40 µg on Ifnb1 [S08-A] (E05)', 'No integrity flag (PD only)'])
rows.append(['Tolerability', f'Post-vaccination weight nadir {S08D[S08D.group=="PSLN-344"].mean_of_animal_nadirs.iloc[0]:.1f}% [S08-D]; no CNS ISG rise vs Sham at 36 h [S10-A]', 'No integrity flag, but very limited'])
TAB(rows, [42 * mm, 86 * mm, 44 * mm], fs=6.8)

# =====================================================================================
H1('2. Next steps: what each study must establish, and its endpoints')
dd = DPC.set_index(['endpoint', 'SD_inflation'])
P('This section comes straight after the recommendation because it is the decision the committee is asked to fund. The evidence behind it follows in Sections 3–8. Integrity-finding IDs (C1–C5, M1–M8, m1–m10, S1) are defined in Section 4 and Appendix A.')
P('<b>Rule used to set thresholds.</b> Each go criterion requires the replication to reach at least half of the effect we observed, on the log scale. For example, an observed 8.0× HAI ratio requires ≥2.8× in the replication. This allows for the optimistic effect sizes typical of small first studies (Hedges g 2–9 here, soft signal S1). Sample sizes come from our own variance with the SD inflated 1.5× (design_power_*.csv).')
nrows = [['Study (timing)', 'What it must establish', 'Design essentials', 'Endpoints and go criteria (anchored to our data)', 'Stop if']]
nrows.append(['A. Forensic data audit (months 0–3; QA, independent of project team)', 'The efficacy case rests on contemporaneous, traceable raw data (ALCOA+).',
              'Retrieve balance logs with animal IDs, mortality/humane-endpoint logs, FCS files, plate-reader and qPCR exports, randomisation records. Cover every block cited here.',
              'All 5 critical and 8 major findings explained with documents; original vs copy identified for each duplicated trajectory (C1); S06-C/S06-D mortality logs (C2); FCS re-analysis of S11-A/B and S01-B/S08-C (C3, C5); strain confirmed for S02-E, S05-A/B (M4); labels corrected (M1, M2, M6, m3); S08 orphan region identified (M7). Corrected data keep PSLN-344 > PSLN-212 in every affected block.',
              'Any critical finding not traceable to raw data; any evidence that values were generated rather than measured → terminate and refer.'])
nrows.append(['B1. Independent confirmatory efficacy and attribution study in aged mice (months 3–9; CRO, blinded, randomised, pre-registered analysis plan)',
              '(a) The Mn-dependent effect reproduces in an independent laboratory; (b) the benefit needs CDN-1807, not Mn²⁺ alone; (c) performance vs standard-of-care approaches; (d) within-animal correlates of protection.',
              f'≥20-month BALB/c and C57BL/6, both sexes. Split/subunit HA antigen as well as whole inactivated virus. Arms: Sham; PSLN-212; PSLN-344; CDN-free Mn-liposome; free CDN-1807 + MnCl₂; i.m. squalene-emulsion-adjuvanted vaccine; i.m. high-dose (4× HA); young PSLN-212; unvaccinated, unchallenged aged sentinels. Immunogenicity n = 12 per arm per sex (≥90% power for half the observed HAI effect with SD ×1.5: n = {int(dd.loc[("HAI H1N1",1.5),"n_per_group_90pct_power"])}–{int(dd.loc[("HAI H3N2",1.5),"n_per_group_90pct_power"])}). Challenge n = 20 per arm over two independent runs (power {DPS[(DPS.scenario.str.startswith("conservative"))&(DPS.n_per_group==20)].power.iloc[0]:.2f} for 70% vs 20%).',
              f'HAI GMT d28 ≥2.8× (H1N1) and ≥3.0× (H3N2) vs PSLN-212 (observed 8.0×/9.2×) [S03-C/G]; IgG ≥4.3× (H1N1) and ≥3.7× (H3N2) (observed 18.6×/13.4×) [S03-A/E]. Attribution: PSLN-344 ≥2× HAI GMT over CDN-free Mn-liposome and better survival. SoC: PSLN-344 HAI GMT not below i.m. benchmark (ratio ≥1.0, lower 95% bound ≥0.5) and nasal IgA ≥4× the i.m. benchmark. NP/M1 IFN-γ ≥2× (observed 4.2×) [S05-F]. Heterosubtypic challenge (d28; d90 subset): PSLN-344 survival ≥60% and ≥35 points above PSLN-212 (observed 84% vs 13%); lung virus d3/d5 ≥1 log₁₀ lower. PD: Ifnb1 16 h ≥1.5× (observed 2.23×, CI 1.85–2.69) [S01-A]; Csf2 36 h ≥2.3× (observed 5.4×) [S02-F]. Correlates: ≥1 pre-specified pre-challenge marker with AUC ≥0.75 for individual survival.',
              'Any primary criterion missed; or CDN-free Mn-liposome equivalent to PSLN-344 (value would then sit in Mn²⁺, not CDN-1807 → IP/strategy review, likely terminate).'])
nrows.append(['B2. Mn²⁺ and STING safety package in aged animals (months 3–9, parallel)', 'Intranasal PSLN-344 does not deliver Mn²⁺ to the CNS at levels of concern, causes no olfactory, facial-nerve or neurobehavioural toxicity, and has acceptable lung and systemic reactogenicity, including after repeat dosing.',
              'Single dose and 3 doses (2-week interval), aged rodents, vehicle and CT controls; ICP-MS Mn in olfactory bulb, striatum, globus pallidus and cerebellum at 24 h, 7 d and 28 d; T1-weighted MRI subset; histopathology of nasal cavity, olfactory bulb, trigeminal/facial nerve and ganglia, and lung at d1, d3, d7 and d28; BAL; serum cytokines; neurobehaviour at d28.',
              f'Mn per dose defined. Olfactory-bulb Mn back to vehicle level by d28 and no basal-ganglia rise at any time (equivalence margin agreed with Toxicology). No histopathology above minimal persisting to d28. No neurobehavioural difference vs vehicle. CNS ISG/Tnf in olfactory bulb at 6 h–7 d not different from vehicle, with CT positive (our 36 h data: Tnf {s10("Tnf","PSLN-344","Sham").geo_fold:.2f}× vs Sham) [S10-A]. Lung Tnf back to baseline by d7 (our data: about 8× at 72 h in aged vs 0.5× young) [S09-A]. Weight nadir ≥95% (observed {n344.mean_of_animal_nadirs:.1f}%) [S08-D].',
              'CNS Mn persisting at d28; any neurobehavioural or facial-nerve finding; non-resolving lung pathology.'])
nrows.append(['B3. CMC minimum product definition (months 3–9, parallel)', 'A defined, reproducible, stable product with a dose unit that can be translated.',
              '3 consecutive batches; define the Mn:CDN ratio; release assays (DLS size/PDI/zeta and TEM are described in the annotation but no data are in the package).',
              f'Dose stated as µg CDN-1807 and µg Mn²⁺. EE ≥80% (current {ee["PSLN-344"]["mean"]:.1f} ± {ee["PSLN-344"]["sd"]:.1f}%) [S08-B], or justification for free CDN. Lyophilised (2.5% trehalose) stability at 2–8 °C and −20 °C for ≥6 months: potency (Ifnb1-induction ED50 within 2× of fresh, S08-A as reference curve) and EE within 10% of release.',
              'Cannot reach stable, reproducible EE and potency.'])
nrows.append(['C. Translational bridge (months 9–18; only if A and B pass)', 'The effect survives human-relevant delivery (nasal-spray device, upper-airway deposition) and a second species with human-like influenza disease.',
              'Ferret heterosubtypic challenge and transmission (aged if available). Aged NHP immunogenicity with the clinical nasal device, including deposition imaging.',
              'Ferret: nasal-wash virus AUC ≥1 log₁₀ lower than i.m. benchmark, clinical score, HAI, nasal IgA. NHP: nasal ISG/GM-CSF/CCL2 ≥2× vehicle at 24–48 h (PD bridge to S01-A/S02-F); cTfh d7; HAI GMT not below i.m. benchmark with superior nasal IgA; NP/M1 ELISpot; olfactory safety; Mn in plasma/CSF.',
              'No nasal PD signal, or no mucosal advantage over the i.m. benchmark.'])
nrows.append(['D. IND-enabling (month 18 onwards)', 'Regulatory safety package.', 'GLP repeat-dose intranasal toxicity in two species with Mn toxicokinetics, local tolerance, CNS safety pharmacology.', 'Per ICH and regulatory guidance for vaccine adjuvants.', 'Standard toxicology stop rules.'])
TAB(nrows, [27 * mm, 30 * mm, 40 * mm, 53 * mm, 22 * mm], fs=5.9)
P('<b>Decision points.</b> Month 3: Gate A (audit), go or terminate. Month 9: Gate B (B1–B3), advance to C or terminate. Month 18: Gate C, advance to IND-enabling or terminate. Only Study A and the design work for B are funded before the month-3 decision.')

# =====================================================================================
H1('3. What the data show')
H2('3.1 Asset and comparators')
P('From the annotation (p.1): <b>PSLN-344</b> is the STING agonist CDN-1807 in a DPPC/DPPG/DPPE-PEG2000/cholesterol liposome, with Mn²⁺ incorporated by coordination polymerisation. <b>PSLN-212</b> is identical except that it has no Mn²⁺. It is the decisive comparator, because it isolates the contribution of Mn²⁺. <b>CMP-204</b> carries cGAMP instead of CDN-1807. R848-containing variants also appear. "<b>Sham</b>" is empty liposome given with the vaccine. All products were given intranasally at 20 µg adjuvant per animal with formalin-inactivated whole-virus vaccine (CA09 H1N1 0.5 µg HA; Aichi H3N2 1 µg HA). The BALB/c animals were female (annotation p.1); sex is not stated for the other strains.')

H2('3.2 Immunogenicity in aged mice: large, consistent, mechanistically connected')
claim('E05', 'Ifnb1 dose-response Emax/ED50 and dose matching', 'S08-A', 'S08!B3:M7', 'dose_response_S08A_emax.csv', 'Emax (Hill) fit, inverse prediction')
tab = [['Read-out [block]', 'Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212 young', 'PSLN-344 vs PSLN-212 (95% CI); p', 'RI*']]
def trow(label, key, kind, cid):
    g = {'pct': 'pct', 'gm': 'gm', 'gmf': 'gmf'}[kind]
    e = eff(key, 'mn', 'pct' if kind == 'pct' else 'fold')
    tab.append([f'{label} [{key.split("_")[0] if not key.startswith("S02-D") else "S02-D"}] ({cid})', grp(key, 'Sham', g), grp(key, 'PSLN-212', g), grp(key, 'PSLN-344', g), grp(key, 'PSLN-212(Y)', g), e, ri(key)])
    claim(cid, f'{label}: group values and PSLN-344 vs PSLN-212 contrast', key.split('_')[0], cellsof(key, ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']), 'block_group_summary.csv; block_contrasts.csv', 'Welch t' + (' on log2' if kind != 'pct' else ''))
trow('Lung Ifnb1 16 h, fold (GM)', 'S01-A_16h', 'gmf', 'E06')
trow('Lung Csf2 (GM-CSF) 36 h, fold (GM)', 'S02-F_36h', 'gmf', 'E07')
trow('Lung monocytes day 4, %', 'S01-D_4', 'pct', 'E08')
trow('Lung cDC1 72 h, %', 'S01-F', 'pct', 'E09')
trow('Lung CCR7⁺ migratory CD11b⁺ DC 72 h, %', 'S02-A', 'pct', 'E10a')
trow('MLN antigen⁺ DC 36 h, %', 'S02-C', 'pct', 'E10b')
trow('MLN CD40⁺ CD11b⁺ DC day 3, %', 'S02-D_CD40', 'pct', 'E10c')
trow('MLN ICOS-hi Tfh day 7, %', 'S04-A_ICOShi', 'pct', 'E11a')
trow('MLN Tfr (Foxp3⁺) day 7, %', 'S04-B_Foxp3', 'pct', 'E11b')
trow('MLN germinal-centre B day 7, %', 'S03-K', 'pct', 'E11c')
trow('Serum IgG anti-H1N1 d14, GMT', 'S03-A', 'gm', 'E12a')
trow('Serum IgG anti-H3N2 d14, GMT', 'S03-E', 'gm', 'E12b')
trow('HAI anti-H1N1 d14, GMT', 'S03-C', 'gm', 'E12c')
trow('HAI anti-H3N2 d14, GMT', 'S03-G', 'gm', 'E12d')
trow('Neutralising anti-H1N1 d14, GMT', 'S03-D', 'gm', 'E12e')
trow('IFN-γ⁺ CD8, H5N1 restim. d14, %', 'S05-F', 'pct', 'E13a')
trow('IFN-γ⁺ CD8, H5N1 restim. d60, %', 'S05-G', 'pct', 'E13b')
trow('Lung TRM CD8 d25, %', 'S05-I', 'pct', 'E13c')
trow('Lung GZMB⁺ CD8 d3, %', 'S05-E', 'pct', 'E13d')
P('<b>Table 1. PSLN-344 vs the Mn-free formulation in aged mice (blocks with no integrity flag; n = 5 per group).</b>')
TAB(tab, [50 * mm, 14 * mm, 17 * mm, 19 * mm, 18 * mm, 46 * mm, 9 * mm], fs=6.3)
SMALL('*RI (restoration index) = (PSLN-344 aged − PSLN-212 aged) / (PSLN-212 young − PSLN-212 aged), computed on the log₂ scale for titres and fold-changes. 1 = young level; 0 = no better than PSLN-212. Percentages are mean ± SD; effects for percentages are differences in percentage points. Csf2 has no young group. HAI values recorded as 0 (<1:10) were set to 5.')
FIGURE(FIG + 'fig1_key_efficacy_readouts.png', 'Figure 1. Selected read-outs from blocks without integrity flags (dots = animals).', 178)
FIGURE(FIG + 'fig2_restoration_index.png', 'Figure 2. Fraction of the aged-vs-young deficit closed by PSLN-344 across 32 unflagged read-outs (median 0.71, IQR 0.60–0.80) (E03).', 120)

H2('3.3 Where PSLN-344 does not restore youth, and where it adds nothing')
ey = {k: K[k].get('vsY') for k in ['S03-A', 'S03-E', 'S13-I', 'S13-J']}
t16 = K['S09-A_panel1_Tnf']; i16 = K['S09-A_panel1_Il10']; t72 = K['S09-A_panel2_Tnf']
claim('E14', 'Partial restoration: CD40/CD86, GZMB+ CD8, IgG vs young', 'S02-D; S05-E; S03-A/E; S13-I/J', cellsof('S02-D_CD40', ['PSLN-344', 'PSLN-212', 'PSLN-212(Y)']), 'block_contrasts.csv', 'Welch t; restoration index')
claim('E15', 'Aged PSLN-344 Tnf/Il10 exceed young (16 h and panel-2 72 h)', 'S09-A', 'S09!Q8:V9 (panel 1); S09!AN8:AS9 (panel 2)', 'block_contrasts.csv', 'Welch t on log scale')
claim('E16', 'Mn effect in young: Ifnb1, antigen+ DC, OT-I, cDC1; young survival', 'S01-A; S02-C; S02-E; S01-F; S09-B/D/F', 'S01!B10:F10 vs B9:F9; S02!O3:O7 vs M3:M7; S02!O10:O14 vs M10:M14; S01!V36:Z36 vs Q36:U36', 'mechanism_contrasts.csv; survival_counts.csv', 'Welch t; counts')
m_y = {c: mech(c) for c in ['Mn effect in young: Ifnb1 16 h', 'Mn effect in young: antigen+ MLN DC', 'Mn effect in young: OT-I priming', 'Mn effect in young: cDC1']}
BUL([
    f'<b>DC co-stimulation stays largely aged.</b> CD40⁺ DC are {grp("S02-D_CD40","PSLN-344")}% with PSLN-344 vs {grp("S02-D_CD40","PSLN-212(Y)")}% in young mice (RI {ri("S02-D_CD40")}). CD86⁺ DC are {grp("S02-D_CD86","PSLN-344")}% vs {grp("S02-D_CD86","PSLN-212(Y)")}% (RI {ri("S02-D_CD86")}) [S02-D] (E14).',
    f'<b>Titres remain below young.</b> IgG GMT is {ey["S03-A"]["effect"]:.2f}× ({fpe(ey["S03-A"]["p"])}) and {ey["S03-E"]["effect"]:.2f}× ({fpe(ey["S03-E"]["p"])}) of young for H1N1 and H3N2 [S03-A/E]. After a boost it is {ey["S13-I"]["effect"]:.2f}× and {ey["S13-J"]["effect"]:.2f}× of young [S13-I/J]. Early lung GZMB⁺ CD8 reach RI {ri("S05-E")} [S05-E].',
    f'<b>There is an inflammatory overshoot in aged lung (a reactogenicity flag).</b> At 16 h, Tnf is {10**K["S09-A_panel1_Tnf"]["groups"]["PSLN-344"]["mean"]:.1f}-fold with PSLN-344 vs {10**K["S09-A_panel1_Tnf"]["groups"]["PSLN-212(Y)"]["mean"]:.1f}-fold in young (ratio {t16["vsY"]["effect"]:.1f}×, {fpe(t16["vsY"]["p"])}). Il10 is {10**K["S09-A_panel1_Il10"]["groups"]["PSLN-344"]["mean"]:.1f}- vs {10**K["S09-A_panel1_Il10"]["groups"]["PSLN-212(Y)"]["mean"]:.1f}-fold ({fpe(i16["vsY"]["p"])}). In the panel that is printed as 16 h but matches the 72 h data, Tnf is {10**K["S09-A_panel2_Tnf"]["groups"]["PSLN-344"]["mean"]:.1f}- vs {10**K["S09-A_panel2_Tnf"]["groups"]["PSLN-212(Y)"]["mean"]:.2f}-fold ({fpe(t72["vsY"]["p"])}) [S09-A] (E15).',
    f'<b>In young mice, Mn²⁺ adds little.</b> Ifnb1 is {m_y["Mn effect in young: Ifnb1 16 h"].effect:.2f}× ({fpe(m_y["Mn effect in young: Ifnb1 16 h"].p_welch)}), antigen⁺ MLN DC {m_y["Mn effect in young: antigen+ MLN DC"].effect:.2f}× ({fpe(m_y["Mn effect in young: antigen+ MLN DC"].p_welch)}), OT-I priming {m_y["Mn effect in young: OT-I priming"].effect:.2f}× ({fpe(m_y["Mn effect in young: OT-I priming"].p_welch)}) and cDC1 {m_y["Mn effect in young: cDC1"].effect:.2f}× ({fpe(m_y["Mn effect in young: cDC1"].p_welch)}). Young survival is 8/8 vs 8/8 in all three young challenge studies [S09-B/D/F], and in young mice even the cGAMP formulation protected {sv("S13-E","CMP-204(Y)")} against homologous H1N1 [S13-E] (E16). The differentiation is therefore specific to aged animals, and so is the target population.'])

H2('3.4 Protection: the direction is robust, the magnitude is not verified')
claim('E17', 'Per-experiment survival and log-rank p (PSLN-344 vs PSLN-212)', 'S03-I,S03-J,S06,S15-H/L/N', 'tidy_survival.csv (cell_days / cell_event columns)', 'survival_tests.csv', 'log-rank (statsmodels survdiff); Fisher exact')
claim('E18', 'Background mortality of unchallenged aged sentinels 4/21', 'S06-E; S06-F; S06-G', 'S06!L62:L68; S06!R62:R68; S06!F99:F105', 'stats_survival_pooled.py', 'Clopper-Pearson CI')
FL = pd.read_csv(A + 'survival_strata_flags.csv').set_index('block')
srows = [['Experiment [block]', 'Vaccine; challenge', 'PSLN-344', 'PSLN-212', 'Sham', 'log-rank p (344 vs 212)', 'Integrity']]
for blk, desc in [('S03-I', 'Bivalent; 10× H1N1 homologous, d14'), ('S03-J', 'rgH5N1; WT H5N1 at d2 (age not stated)'), ('S06-A', 'H3N2; PR8 H1N1 d14'), ('S06-B', 'H3N2; PR8 H1N1 d3'),
                  ('S06-C', 'Bivalent; rgH5N1 d14'), ('S06-D', 'Bivalent; rgH5N1 d3'), ('S06-E', 'H3N2; PR8 H1N1 d60'), ('S06-F', 'Bivalent; rgH5N1 d60'), ('S06-G', 'H1N1; Perth H3N2 d60'),
                  ('S15-L', 'Bivalent; aged C57BL/6'), ('S15-N', 'Bivalent; aged Swiss Webster')]:
    srows.append([f'[{blk}]', desc, sv(blk, 'PSLN-344'), sv(blk, 'PSLN-212'), sv(blk, 'Sham'), svp(blk, 'PSLN-344', 'PSLN-212'), FL.loc[blk, 'integrity_flag'] if blk in FL.index else ''])
for blk, lab in [("S06-E'(r71-98,G-K)", "[S06-E′] 14-mo; PR8"), ("S06-F'(r71-98,M-Q)", "[S06-F′] 14-mo; Perth H3N2")]:
    srows.append([lab, 'naive / imprinted', f'{sv(blk,"Naive+PSLN-344")} / {sv(blk,"Imprinting+PSLN-344")}', f'{sv(blk,"Naive+PSLN-212")} / {sv(blk,"Imprinting+PSLN-212")}', '–',
                  f'{svp(blk,"Naive+PSLN-344","Naive+PSLN-212")} / {svp(blk,"Imprinting+PSLN-344","Imprinting+PSLN-212")}', 'moderate'])
srows.append(['[S15-H]', 'Given 3 d before H5N1', f'vaccine+PSLN-344 {sv("S15-H","3d Vaccine+PSLN-344")}', f'vaccine alone {sv("S15-H","3d Vaccine")}', f'PSLN-344 alone {sv("S15-H","3d PSLN-344")}', svp('S15-H', '3d Vaccine+PSLN-344', '3d Vaccine') + ' (vs vaccine)', 'critical (C1)'])
P('<b>Table 2. Survival at the end of observation, by experiment (aged or middle-aged animals).</b>')
TAB(srows, [22 * mm, 44 * mm, 26 * mm, 22 * mm, 20 * mm, 22 * mm, 16 * mm], fs=6.4)
SMALL('For S15-H the three columns hold vaccine + PSLN-344, vaccine alone and PSLN-344 alone. S03-J follow-up ran to day 21; all others to day 14. Integrity flags are explained in Section 4 and Appendix A.')
prow = [['Pooled analysis (stratified by experiment)', 'PSLN-344', 'PSLN-212', 'Difference (MH, pts)', 'Exact stratified p']]
for _, r in PO.iterrows():
    prow.append([r.analysis, f'{r.PSLN344_surv} ({r.PSLN344_pct:.0f}%)', f'{r.PSLN212_surv} ({r.PSLN212_pct:.0f}%)', f'{r.MH_risk_difference_pct_points:.0f}', f'{r.exact_stratified_p_one_sided:.1e}'])
TAB(prow, [92 * mm, 22 * mm, 22 * mm, 20 * mm, 18 * mm], fs=6.5)
bg = SC[SC.group == 'Untreated']
BUL([f'<b>The direction is robust.</b> PSLN-344 beats PSLN-212 in every aged experiment. The pooled advantage is 65–71 points in every scenario, including scenario F (the only experiment with no integrity flag, S06-B: {sv("S06-B","PSLN-344")} vs {sv("S06-B","PSLN-212")}, p=0.010).',
     f'<b>Frailty confounds the model.</b> Unvaccinated, unchallenged aged sentinels died during the 14-day windows: {int(bg.deaths.sum())}/{int(bg.n.sum())} (19%; 95% CI 5–42%) [S06-E/F/G] (E18). In S06-G, sentinel survival ({sv("S06-G","Untreated")}) equals PSLN-344 survival ({sv("S06-G","PSLN-344")}). Future aged studies need sentinel arms and larger n.',
     f'<b>Protection requires antigen.</b> PSLN-344 given alone 3 days before H5N1 challenge protected {sv("S15-H","3d PSLN-344")} animals, compared with {sv("S15-H","3d Vaccine+PSLN-344")} when given with vaccine [S15-H]. It is not a stand-alone antiviral, although this block is itself affected by C1.',
     f'<b>Imprinting does not blunt PSLN-344.</b> Survival was 6/7 in both naive and previously infected 14-month-old mice [S06-E′/F′]. This matters for older adults with lifelong exposure.'])
FIGURE(FIG + 'fig3_survival_strata_sensitivity.png', 'Figure 3. Per-experiment survival with integrity flag (left) and pooled sensitivity analyses (right) (E04, E17).', 178)

H2('3.5 Tolerability and safety: what exists and what does not')
claim('T01', 'Post-vaccination body-weight nadirs', 'S08-D', 'S08!B21:AE26', 'safety_S08D_bodyweight.csv', 'per-animal minimum, group mean')
claim('T02', 'CNS transcripts 36 h: PSLN-344 and CT vs PBS and Sham', 'S10-A', 'S10!A3:N7', 'safety_S10A_CNS.csv', 'Welch t on log2')
def s10(an, t, ref):
    r = S10[(S10.analyte == an) & (S10.test == t) & (S10.reference == ref)].iloc[0]; return r
n344 = S08D[S08D.group == 'PSLN-344'].iloc[0]; nr = S08D[S08D.group == 'PSLN-212/R848'].iloc[0]
BUL([f'<b>Systemic tolerability after vaccination [S08-D].</b> The mean per-animal weight nadir was {n344.mean_of_animal_nadirs:.1f}% with PSLN-344 (lowest animal {n344.lowest_animal_nadir:.1f}%), similar to vaccine alone ({S08D[S08D.group=="Vaccine"].mean_of_animal_nadirs.iloc[0]:.1f}%). With PSLN-212/R848 it was {nr.mean_of_animal_nadirs:.1f}% (lowest {nr.lowest_animal_nadir:.1f}%), and one animal was missing by day 10 (T01).',
     f'<b>CNS at 36 h [S10-A].</b> Compared with Sham, PSLN-344 changed Ifnb1 {s10("Ifnb1","PSLN-344","Sham").geo_fold:.2f}×, Tnf {s10("Tnf","PSLN-344","Sham").geo_fold:.2f}× and Isg15 {s10("Isg15","PSLN-344","Sham").geo_fold:.2f}× (all p≥{min(s10(a,"PSLN-344","Sham").p_welch_log for a in ["Ifnb1","Tnf","Isg15"]):.2f}). Cholera toxin raised them {s10("Ifnb1","CT","Sham").geo_fold:.1f}×, {s10("Tnf","CT","Sham").geo_fold:.1f}× and {s10("Isg15","CT","Sham").geo_fold:.1f}× (p≤{max(s10(a,"CT","Sham").p_welch_log for a in ["Ifnb1","Tnf","Isg15"]):.3f}). Against buffer (PBS), PSLN-344 Tnf was {s10("Tnf","PSLN-344","PBS").geo_fold:.2f}× (p={s10("Tnf","PSLN-344","PBS").p_welch_log:.3f}), and the empty vehicle contributes part of this (T02). This is encouraging but narrow: one time point, three transcripts, unspecified CNS region, no Mn measurement.',
     '<b>Not in the package:</b> Mn²⁺ content per dose; Mn biodistribution (olfactory bulb, basal ganglia); nasal, olfactory and facial-nerve histopathology; neurobehaviour; lung histopathology or BAL; repeat dosing; a second species. <i>External context, not our data: intranasal manganese reaches the brain along olfactory pathways in published rodent studies, and an enterotoxin-adjuvanted intranasal influenza vaccine was previously associated with facial-nerve (Bell\'s palsy) events. Both make this gap decision-relevant for an elderly population.</i>'])
FIGURE(FIG + 'fig4_safety.png', 'Figure 4. Tolerability and safety-relevant read-outs (T01, T02, E15).', 178)

H2('3.6 CMC and dose')
em344 = EM[EM.group == 'PSLN-344'].iloc[0]; em212 = EM[EM.group == 'PSLN-212'].iloc[0]
ee = K['S08-B']['groups']
claim('Q01', 'Encapsulation efficiency PSLN-344 vs PSLN-212', 'S08-B', 'S08!M11:O11 vs S08!D11:F11', 'block_group_summary.csv', 'mean ± SD, Welch t')
BUL([f'<b>Encapsulation.</b> Efficiency is {ee["PSLN-344"]["mean"]:.1f} ± {ee["PSLN-344"]["sd"]:.1f}% for PSLN-344 vs {ee["PSLN-212"]["mean"]:.1f} ± {ee["PSLN-212"]["sd"]:.1f}% for PSLN-212 (n = 3; p=0.29) [S08-B] (Q01). Roughly 45% of the CDN is unencapsulated. The dose unit ("20 µg of adjuvant") is not defined as CDN or total mass, and Mn content is not reported.',
     f'<b>Dose-response [S08-A].</b> Mn²⁺ raises the maximal response, not the potency: Emax {em344.Emax:.0f}- vs {em212.Emax:.0f}-fold, with ED50 {em344.ED50_ug:.1f} vs {em212.ED50_ug:.1f} µg. The response plateaus between 20 µg ({em344.mean_at_20ug:.1f}-fold) and 40 µg ({em344.mean_at_40ug:.1f}-fold). About 7–8 µg of PSLN-344 matches PSLN-212 at 20–40 µg (E05). This supports testing lower doses, which would also lower Mn exposure.'])
FIGURE(FIG + 'fig5_dose_response.png', 'Figure 5. Ifnb1 dose-response [S08-A] with Emax fits (E05).', 112)

# =====================================================================================
H1('4. Data integrity: summary of findings')
P('We checked the workbook for internal consistency (stated vs observed n, label consistency across sheets, survival vs companion body-weight records) and for duplicated values (position-matched comparisons, cross-experiment animal-trajectory matching against an empirical chance benchmark, and recomputation of derived quantities). Table 3 lists the critical and major findings; the full register is in Appendix A. <b>None of these findings is, on its own, proof of misconduct.</b> Template or copy errors can produce several of them. Only the raw records can settle it, and until then the affected blocks cannot support an investment or regulatory decision.')
irows = [['ID', 'Finding (blocks)', 'Evidence', 'What it affects']]
for _, r in IR[IR.severity.isin(['Critical', 'Major'])].iterrows():
    irows.append([f'{r.id} ({r.severity})', f'{r.finding} [{r.blocks}]', r.quantitative_evidence, r.claims_affected])
TAB(irows, [15 * mm, 62 * mm, 55 * mm, 40 * mm], fs=6.0)
FIGURE(FIG + 'fig6_integrity_evidence.png', 'Figure 6. Examples of integrity findings: (a) the same animal trajectories in two experiments; (b) the same weights in different strains, adjuvants and experiments; (c) two cell types sharing values; (d) cross-experiment trajectory matches vs chance (I01–I03).', 178)

# =====================================================================================
H1('5. Mechanism of action, built from our data')
P('Our data support the following model. Mn²⁺ co-delivery <b>raises the ceiling of the STING/type-I interferon response in the aged lung</b> (Emax about 3.4× that of PSLN-212 at a similar ED50). The signal appears to spread through gap junctions and induces Ccl2/Ccl3 and GM-CSF (Csf2). This drives <b>CCR2-dependent monocyte recruitment and IFNAR- and GM-CSF-dependent differentiation into monocyte-derived DCs</b>, together with cDC1 expansion and CCR7⁺ DC migration to the mediastinal lymph node. Downstream, <b>Tfh expand while Tfr contract</b>, germinal centres form, and high-titre HAI/neutralising antibody appears alongside <b>cross-reactive IFN-γ⁺ CD8 and lung TRM</b>. Together these plausibly explain homologous and heterosubtypic protection. Figure 7 shows each step with its evidence grade.')
mrows = [['Step', 'Evidence in our data (aged, PSLN-344 vs PSLN-212 unless stated)', 'Grade', 'Gap to close']]
r = mech('AM uptake WT vs Sftpa1/Sftpd KO'); claim('M01', 'AM uptake depends on SP-A/SP-D', 'S01-C', 'S01!B20:E21', 'mechanism_contrasts.csv', 'Welch t')
mrows.append(['Uptake', f'Alveolar macrophage uptake depends on SP-A/SP-D: {r.mean1:.1f}% vs {r.mean2:.1f}% in Sftpa1/Sftpd KO ({fpe(r.p_welch)}) [S01-C] (M01). AEC-II targeting [S01-B] and the "Mn lowers AEC uptake ~4×" result [S08-C] are unreliable (C5).', 'Moderate', 'Cell-resolved biodistribution of PSLN-344 itself (the Mn form)'])
claim('M02', 'STING/IFN-b ceiling', 'S01-A; S08-A', 'S01!B5:F9; S08!B3:M7', 'block_contrasts.csv; dose_response_S08A_emax.csv', 'Welch t; Emax fit')
mrows.append(['STING → IFN-β', f'Ifnb1 16 h {grp("S01-A_16h","PSLN-344")} vs {grp("S01-A_16h","PSLN-212")}-fold ({K["S01-A_16h"]["mn"]["effect"]:.2f}×, {fpe(K["S01-A_16h"]["mn"]["p"])}), equal to young (RI {ri("S01-A_16h")}) [S01-A]. Emax {em344.Emax:.0f} vs {em212.Emax:.0f} [S08-A]. Transient: no difference at 72 h ({fpe(K["S01-A_72h"]["mn"]["p"])}) (M02).', 'Strong', 'STING/cGAS-knockout or STING inhibitor; IFN-β protein'])
r = mech('Gap-junction blockade (CBX) on monocyte recruitment'); claim('M03', 'CBX reduces monocyte recruitment', 'S11-C', 'S11!A17:B21', 'mechanism_contrasts.csv', 'Welch t')
mrows.append(['Gap-junction spread', f'Carbenoxolone: recruited monocytes {r.mean1:.1f}% vs {r.mean2:.1f}% ({fpe(r.p_welch)}) [S11-C] (M03).', 'Moderate', 'Second, more selective blocker; cell-type-specific connexin KO'])
claim('M04', 'Chemokines and GM-CSF', 'S02-F; S09-A', 'S02!B17:K19; S09!H3:S9', 'block_contrasts.csv', 'Welch t on log2')
mrows.append(['Chemokines, GM-CSF', f'Csf2 {K["S02-F_16h"]["mn"]["effect"]:.1f}× (16 h), {K["S02-F_36h"]["mn"]["effect"]:.1f}× (36 h) [S02-F]. Ccl2 {K["S09-A_panel1_Ccl2"]["mn"]["effect"]:.0f}×, Ccl3 {K["S09-A_panel1_Ccl3"]["mn"]["effect"]:.0f}×, Ccl5 {K["S09-A_panel1_Ccl5"]["mn"]["effect"]:.1f}× at 16 h (n = 3) [S09-A] (M04).', 'Strong (S02-F)', 'Protein levels (BAL); S09-A PBS/Sham label fix (M2)'])
r1 = mech('CCR2 antagonist on monocytes'); r2 = mech('CCR2 antagonist on Ly6C+ macrophages'); r3 = mech('IFNAR-deficient BM monocyte infiltration')
claim('M05', 'CCR2-dependent monocyte influx', 'S01-D; S07-B; S12-A', 'S01!G26:P26; S07!B10:F14; S12!A3:B5', 'block_contrasts.csv; mechanism_contrasts.csv', 'Welch t')
mrows.append(['Monocyte influx', f'Day-4 monocytes {grp("S01-D_4","PSLN-344")} vs {grp("S01-D_4","PSLN-212")}% ({fpe(K["S01-D_4"]["mn"]["p"])}) [S01-D]. CCR2 antagonist: monocytes {r1.mean2:.1f} → {r1.mean1:.1f}%, Ly6C⁺ Mφ {r2.mean2:.1f} → {r2.mean1:.1f}% [S07-B]. IFNAR⁻/⁻ marrow: {r3.mean1:.1f} vs {r3.mean2:.1f}% (n = 3, {fpe(r3.p_welch)}) [S12-A] (M05).', 'Strong', 'Link to protection (CCR2 antagonist + challenge)'])
r1 = mech('moDC from IFNAR-/- vs WT BM (no cDC precursors)'); r2 = mech('GM-CSF rescue of IFNAR-/- moDC'); r3 = mech('GM-CSF added to PSLN-212 (moDC-like cells)')
claim('M06', 'IFNAR and GM-CSF drive moDC', 'S02-H; S02-G', 'S02!B30:F34; S02!B22:D26', 'mechanism_contrasts.csv', 'Welch t')
mrows.append(['moDC differentiation', f'IFNAR⁻/⁻ marrow moDC {r1.mean1:.1f} vs {r1.mean2:.1f}% ({fpe(r1.p_welch)}); GM-CSF rescue to {r2.mean1:.1f}% [S02-H]. GM-CSF + PSLN-212: {r3.mean1:.1f} vs {r3.mean2:.1f}% ({fpe(r3.p_welch)}) [S02-G] (M06).', 'Strong', 'GM-CSF neutralisation with PSLN-344'])
mrows.append(['DC mobilisation', f'cDC1 {grp("S01-F","PSLN-344")} vs {grp("S01-F","PSLN-212")}% [S01-F]; migratory DC {grp("S02-A","PSLN-344")} vs {grp("S02-A","PSLN-212")}% [S02-A]; antigen⁺ MLN DC {grp("S02-C","PSLN-344")} vs {grp("S02-C","PSLN-212")}%, pertussis-toxin arm {grp("S02-C","PTX")}% [S02-C]; co-stimulation RI only {ri("S02-D_CD40")}–{ri("S02-D_CD86")} [S02-D].', 'Moderate', 'OT-I/NP-tetramer strain check (M4); co-stimulation deficit'])
mrows.append(['Tfh / Tfr / GC', f'ICOS-hi Tfh {grp("S04-A_ICOShi","PSLN-344")} vs {grp("S04-A_ICOShi","PSLN-212")}% [S04-A]; Tfr {grp("S04-B_Foxp3","PSLN-344")} vs {grp("S04-B_Foxp3","PSLN-212")}% [S04-B]; GC B {grp("S03-K","PSLN-344")} vs {grp("S03-K","PSLN-212")}% [S03-K]; Tfr difference gone by d30 ({fpe(K["S04-C"]["mn"]["p"])}) [S04-C].', 'Strong', 'Tfh/Tfr causality; durability of GC'])
mrows.append(['Antibody', f'IgG {K["S03-A"]["mn"]["effect"]:.1f}× / {K["S03-E"]["mn"]["effect"]:.1f}×; HAI {K["S03-C"]["mn"]["effect"]:.1f}× / {K["S03-G"]["mn"]["effect"]:.1f}×; neutralising {K["S03-D"]["mn"]["effect"]:.1f}× [S03]. IgG2a/IgG1 rises 0.55 → 1.85 (H1N1) only under the S13 labels, and S03-B/F contradict this (M1).', 'Strong', 'Mucosal IgA (never measured); subclass labels'])
r = mech('Pertussis toxin on lung OT-I proliferation'); rm = mech('Pertussis toxin on MLN OT-I proliferation')
mrows.append(['CD8 / TRM', f'Ki-67⁺ CD8 {grp("S05-D","PSLN-344")} vs {grp("S05-D","PSLN-212")}% [S05-D]; H5N1-reactive IFN-γ⁺ CD8 {grp("S05-F","PSLN-344")} vs {grp("S05-F","PSLN-212")}% (d14) [S05-F]; TRM {grp("S05-I","PSLN-344")} vs {grp("S05-I","PSLN-212")}% [S05-I]. Lung priming is insensitive to pertussis toxin ({r.mean2:.0f} vs {r.mean1:.0f}%), MLN priming is sensitive ({rm.mean2:.1f} → {rm.mean1:.1f}%) [S05-C].', 'Strong', 'CD8 depletion + heterosubtypic challenge'])
mrows.append(['Suppressive milieu', f'CD206⁺ Mφ {grp("S11-E","PSLN-344")} vs {grp("S11-E","PSLN-212")}% (time point not stated) [S11-E]; lung Treg {grp("S04-D","PSLN-344")} vs {grp("S04-D","PSLN-212")}% (n = 3) [S04-D]; PSLN-212 accumulates Ly6C⁺CCR2⁺ Mφ (day 5: {K["S07-A_5"]["groups"]["PSLN-212"]["mean"]:.1f} vs {K["S07-A_5"]["groups"]["PSLN-344"]["mean"]:.1f} ×10⁵) [S07-A]; S07-C cannot be interpreted (M6).', 'Weak', 'Macrophage transfer with correct labels'])
TAB(mrows, [24 * mm, 100 * mm, 16 * mm, 32 * mm], fs=6.2)
P('<b>What the MoA does not yet show.</b> (i) Every step is either a PSLN-344 vs PSLN-212 association or a single-intervention experiment. No step has been causally linked to survival: there are no depletion or knockout experiments with challenge. (ii) STING dependence is assumed, not demonstrated: there is no STING/cGAS knockout and no STING inhibitor. (iii) The contribution of Mn²⁺ alone is untested. These are the first experiments in Study B1.')
FIGURE(FIG + 'fig7_moa.png', 'Figure 7. Mechanism of action assembled from our data, with the evidence grade of each step (M01–M06).', 172)

# =====================================================================================
H1('6. Biomarkers to validate efficacy')
claim('B01', 'Regimen-level discrimination (AUC) of 23 candidate read-outs', 'see biomarker_candidates.csv', 'per block', 'biomarkers.py', 'Mann-Whitney AUC, protective vs non-protective regimens')
claim('B02', 'HAI >=1:40 counts and homologous survival', 'S03-C; S03-I', 'S03!K3:O7; S03!A17:F51', 'biomarkers.py; survival_counts.csv', 'counts')
P('We proposed 23 candidate read-outs. All of them separate the protective regimens (aged PSLN-344, young) from the non-protective ones (Sham, aged PSLN-212) perfectly at the animal level in 22 of 23 (AUC 1.0, or 0.0 for Tfr, which falls); the exception is neutralising titre, at 0.995 (B01). <b>So our data cannot rank biomarkers by discrimination.</b> We ranked them instead by how early they read out, how Mn-specific they are, and whether they have a human-accessible analogue. All of this concordance is between groups, because challenged animals were not sampled. True correlates of protection need within-animal pre-challenge sampling, which is built into Study B1.')
brows = [['Tier / timing', 'Marker in our data [block]', 'PSLN-344 vs PSLN-212 (aged)', 'RI', 'Human-accessible analogue', 'Proposed use']]
brows.append(['1. PD, 16–36 h', 'Lung Ifnb1 16 h [S01-A]', f'{K["S01-A_16h"]["mn"]["effect"]:.2f}× ({fpe(K["S01-A_16h"]["mn"]["p"])})', ri('S01-A_16h'), 'Nasal-mucosa ISG score; IFN-β/λ in nasal lining fluid; blood ISG at 24 h', 'Target engagement; dose selection (Emax plateau)'])
brows.append(['1. PD, 16–36 h', 'Lung Csf2 36 h [S02-F]', f'{K["S02-F_36h"]["mn"]["effect"]:.1f}× ({fpe(K["S02-F_36h"]["mn"]["p"])}); PSLN-212 ≈ Sham', '–', 'Nasal GM-CSF (nasosorption)', 'Most Mn-specific marker → proof of Mn action'])
brows.append(['1. PD, 16 h', 'Lung Ccl2 [S09-A]', f'{K["S09-A_panel1_Ccl2"]["mn"]["effect"]:.0f}× (n = 3)', ri('S09-A_panel1_Ccl2'), 'Nasal/serum CCL2', 'Supportive PD'])
brows.append(['1. Safety PD, 16–72 h', 'Lung Il6/Tnf [S09-A]', f'Il6 {K["S09-A_panel1_Il6"]["mn"]["effect"]:.1f}×; Tnf above young', '–', 'Serum IL-6/TNF; solicited reactogenicity', 'Reactogenicity ceiling'])
brows.append(['2. Priming, d7', 'ICOS-hi Tfh; Tfr [S04-A/B]', f'+{K["S04-A_ICOShi"]["mn"]["effect"]:.1f} / {K["S04-B_Foxp3"]["mn"]["effect"]:.1f} pts', f'{ri("S04-A_ICOShi")} / {ri("S04-B_Foxp3")}', 'Blood cTfh (ICOS⁺PD-1⁺CXCR5⁺) and cTfh:cTfr at d7', 'Early predictor of antibody response'])
brows.append(['2. Priming, d3–7', 'Ki-67⁺ CD8 [S05-D]; GC B [S03-K]', f'+{K["S05-D"]["mn"]["effect"]:.1f} / +{K["S03-K"]["mn"]["effect"]:.1f} pts', f'{ri("S05-D")} / {ri("S03-K")}', 'Blood Ki-67⁺/CD38⁺HLA-DR⁺ CD8; plasmablasts d7', 'Early cellular signal'])
brows.append(['3. Efficacy surrogate, d14–28', 'HAI GMT [S03-C/G]', f'{K["S03-C"]["mn"]["effect"]:.1f}× / {K["S03-G"]["mn"]["effect"]:.1f}×', f'{ri("S03-C")} / {ri("S03-G")}', 'HAI GMT and fold-rise (regulatory surrogate)', 'Primary immunogenicity (GMT, not the ≥1:40 threshold)'])
brows.append(['3. Efficacy surrogate, d14', 'Neutralising [S03-D/H]; IgG [S03-A/E]', f'{K["S03-D"]["mn"]["effect"]:.1f}×; {K["S03-A"]["mn"]["effect"]:.1f}×', f'{ri("S03-D")}', 'Microneutralisation; ELISA', 'Secondary'])
brows.append(['3. Heterosubtypic arm, d14–60', 'IFN-γ⁺ CD8, H5N1 restim. [S05-F/G]', f'+{K["S05-F"]["mn"]["effect"]:.1f} pts (d14); +{K["S05-G"]["mn"]["effect"]:.1f} (d60)', f'{ri("S05-F")}', 'IFN-γ ELISpot to conserved NP/M1 peptides', 'Key differentiation marker'])
brows.append(['3. Mucosal', 'Not measured', '–', '–', 'Nasal HA-specific IgA', 'Must add: the rationale for i.n. delivery'])
TAB(brows, [24 * mm, 34 * mm, 32 * mm, 14 * mm, 40 * mm, 28 * mm], fs=6.2)
BUL([f'<b>Do not use HAI ≥1:40 as the success criterion.</b> Aged PSLN-212 mice were 5/5 at ≥1:40 against H1N1 [S03-C], yet under the same protocol 0/7 survived homologous H1N1 challenge [S03-I] (B02). Even the body-weight record that conflicts with S03-I (M3) implies no more than 3/7. Use GMT and fold-rise, together with mucosal and T-cell markers.',
     '<b>Not recommended as biomarkers:</b> the IgG2a/IgG1 ratio (its labels conflict between sheets, M1, and the subclass biology is mouse-specific); the printed Tfh:Tfr (it is derived arithmetically from Foxp3%, m5); alveolar macrophage and neutrophil counts (C3).',
     '<b>Bridging logic for the clinic.</b> Day 1–2 nasal IFN/ISG and GM-CSF show that Mn²⁺ is acting (PD). Day 7 blood cTfh and plasmablasts predict the antibody response. Day 28 HAI GMT, microneutralisation, nasal IgA and NP/M1 ELISpot are the efficacy surrogates. Studies B1 and C must show that the mouse PD markers carry over to the ferret/NHP nasal compartment.'])

# =====================================================================================
H1('7. Target demographic for TAM sizing')
P('The differentiation in our data is <b>specific to aged animals</b>. In young mice, Mn²⁺ adds no survival benefit and little immunological benefit (Section 3.3). The aged cohort is ≥20 months old (annotation p.1). By common lifespan-mapping conventions (external, not our data), that is roughly the seventh decade of human life. Our data therefore most directly support adults in their 60s and early 70s; they say nothing about the very old or frail.')
trows = [['Segment', 'Definition for market research', 'Status', 'Basis in our data']]
trows.append(['Core (base case)', 'Adults ≥65 y receiving annual seasonal influenza vaccination, in markets that preferentially recommend enhanced vaccines for this age group', 'Base case', 'Age-specific benefit: RI median 0.71 in aged vs no incremental benefit in young [S09-B/D/F, S02-C/E]'])
trows.append(['Sensitivity', 'Adults 60–64 y where national programmes start at 60', 'Sensitivity', '≥20-month cohort; imprinting model at 14 months also responsive [S06-E′/F′]'])
trows.append(['Sub-segments', '65–74; 75–84; ≥85; long-term-care residents', 'Size separately; ≥75 extrapolated', 'Very old/frail not modelled; 19% sentinel mortality shows the model is already frail [S06-E/F/G]'])
trows.append(['Upside only', 'Pandemic / pre-pandemic H5 preparedness for older adults (government procurement)', 'Only if verified', 'H5N1 protection and H5N1-reactive CD8 [S06-C/F, S05-F/G]; rapid onset [S03-J, S15-H] is compromised'])
trows.append(['Exclude', '<50 y; paediatric', 'Excluded', 'No differentiation over Mn-free formulation in young; no paediatric data'])
trows.append(['Downside haircuts', 'Possible label restrictions: Parkinson\'s disease or hepatic impairment (Mn handling); chronic rhinosinusitis or severe airway disease (intranasal STING activation); immunocompromised', 'Hypotheses pending Study B2', 'No Mn or airway-disease safety data exist; Tnf/Il10 overshoot in aged lung [S09-A]'])
TAB(trows, [24 * mm, 62 * mm, 28 * mm, 58 * mm], fs=6.4)
P('<b>Parameters market research should provide for each segment and key market:</b> population size; annual influenza vaccination coverage; share of enhanced (high-dose, adjuvanted or recombinant) vaccines; price corridor of enhanced vaccines; acceptability of and preference for needle-free intranasal delivery; prevalence of the possible label-restriction conditions above; and, for the upside case, H5 stockpile procurement volumes. <b>Note:</b> the BALB/c animals were female and sex is not stated for the other strains (annotation p.1), so the benefit in males is untested.')

# =====================================================================================
# =====================================================================================
H1('8. What we considered and ruled out')
crow = [['Option or claim considered', 'Decision', 'Reason (our data)']]
r_cmp = K['S01-A_16h']['groups']
crow.append(['Advance PSLN-344 to IND-enabling now', 'Ruled out', 'Critical integrity findings (C1–C5); no attribution control; no SoC benchmark; no Mn safety data.'])
crow.append(['Partner or out-license now', 'Ruled out', 'Partner due diligence would find the same duplications (Figure 6), creating reputational and legal exposure. Value cannot be shown until verified.'])
crow.append(['Terminate immediately', 'Considered; not the first action', 'The audit is required regardless; unflagged blocks show large, coherent effects (Table 1). Termination remains the default if the gates fail.'])
crow.append(['PSLN-212 (no Mn) as lead', 'Ruled out', f'Inferior in aged mice: IgG {K["S03-A"]["mn"]["effect"]:.0f}× lower, HAI GMT {grp("S03-C","PSLN-212","gm")} vs {grp("S03-C","PSLN-344","gm")} [S03-A/C]; pooled survival {pool.loc["B","PSLN212_surv"]} vs {pool.loc["B","PSLN344_surv"]}.'])
crow.append(['CMP-204 (cGAMP instead of CDN-1807)', 'Ruled out', f'Lower IFN ceiling: Ifnb1 {r_cmp["CMP-204"]["mean"]:.1f}- vs {r_cmp["PSLN-212"]["mean"]:.1f}-fold for PSLN-212 [S01-A]; Emax {EM[EM.group=="CMP-204"].Emax.iloc[0]:.1f} vs {em212.Emax:.1f} [S08-A]; IgG GMT {grp("S03-A","CMP-204","gm")} vs {grp("S03-A","PSLN-212","gm")} [S03-A]; aged survival {sv("S03-I","CMP-204")} [S03-I].'])
crow.append(['Adding TLR7/8 agonist R848', 'Ruled out', f'PSLN-R848 Ifnb1 only {r_cmp["PSLN-R848"]["mean"]:.1f}-fold [S01-A]; PSLN-212/R848 weight nadir {nr.mean_of_animal_nadirs:.1f}% with one animal lost [S08-D]; Tnf about {10**K["S09-A_panel1_Tnf"]["groups"]["PSLN-212/R848"]["mean"]:.0f}× and Il10 about {10**K["S09-A_panel1_Il10"]["groups"]["PSLN-212/R848"]["mean"]:.0f}× at 16 h [S09-A]; PSLN-344/R848 Emax {EM[EM.group=="PSLN-344/R848"].Emax.iloc[0]:.0f} vs {em344.Emax:.0f} for PSLN-344 [S08-A].'])
crow.append(['Young-adult or paediatric indication', 'Ruled out', 'No incremental benefit in young mice: 8/8 vs 8/8 survival in three studies [S09-B/D/F]; antigen⁺ DC and OT-I gains not significant [S02-C/E].'])
crow.append(['Stand-alone intranasal antiviral (no antigen)', 'Ruled out', f'PSLN-344 alone 3 d before H5N1: {sv("S15-H","3d PSLN-344")} survived [S15-H] (block also affected by C1).'])
crow.append(['Dose escalation above 20 µg', 'Ruled out', f'Plateau: {em344.mean_at_20ug:.1f}-fold at 20 µg vs {em344.mean_at_40ug:.1f}-fold at 40 µg [S08-A]. Explore lower doses instead.'])
crow.append(['Claim "restores a young immune system"', 'Ruled out as stated', f'Partial: median RI 0.71; DC co-stimulation RI {ri("S02-D_CD40")}–{ri("S02-D_CD86")}; titres 0.3–0.6× of young [S02-D, S03, S13].'])
crow.append(['Claims of 2–3-day onset, cross-strain protection, 180-day durability', 'Withheld', 'They rest on blocks with critical or major integrity findings (S03-J, S06-D, S15-H/I, S15-L–O, S09-F/G).'])
crow.append(['HAI ≥1:40 as success threshold', 'Ruled out', 'Aged PSLN-212: 5/5 ≥1:40 but 0/7 homologous survival [S03-C, S03-I].'])
crow.append(['IgG2a/IgG1 (Th1 skew) as evidence or biomarker', 'Ruled out pending audit', 'S03-B/F labels are cyclically permuted relative to S13-A–D (M1); mouse-specific.'])
crow.append(['AEC-II targeting as the explanation for the Mn benefit', 'Ruled out', 'S08-C says Mn lowers AEC uptake about 4×, and S01-B/S08-C share values (C5).'])
crow.append(['Aged survival endpoints without sentinels', 'Ruled out for future studies', '19% 14-day mortality in unchallenged aged mice [S06-E/F/G].'])
crow.append(['Using the current package for a regulatory filing', 'Ruled out', 'Not ALCOA+-compliant until the audit is complete.'])
TAB(crow, [52 * mm, 28 * mm, 92 * mm], fs=6.4)

# =====================================================================================
H1('9. Methods and reproducibility')
P('<b>Parsing.</b> All 15 sheets were mapped block by block to explicit cell ranges (<i>analysis/blocks.py</i>) and converted into tidy tables with a cell reference for every value (<i>tidy_continuous.csv, tidy_survival.csv, tidy_bodyweight.csv</i>). Group names were normalised (e.g. "PSLN-212Y" → "PSLN-212(Y)").')
P('<b>Statistics.</b> Titres, ratios and qPCR fold-changes were analysed on the log₂ scale (S09-A log₁₀ values converted), and percentages on the raw scale. For each block we report Welch t-tests with 95% CIs, Hedges g and Tukey HSD (the stated method; <i>block_tukey_hsd.csv</i>), with Benjamini–Hochberg q-values across all contrasts. Survival: log-rank (statsmodels <i>survdiff</i>) and Fisher exact per experiment. Pooled survival used an exact conditional (stratified) test, the convolution of per-experiment hypergeometric distributions, and a Mantel–Haenszel risk difference. The one missing day value (S03!G46) was treated as censored at day 21.')
P('<b>Integrity checks.</b> Stated vs observed n; labels across sheets; recomputation of derived quantities (IgG2a/IgG1 from S13; Tfh:Tfr from Foxp3%); survival vs companion body-weight records, using the workbook\'s carry-forward convention (≥3 identical trailing values, or missing values, counted as deaths); position-matched duplicate tests with permutation null; and cross-experiment animal-trajectory matching on live (non-carried-forward) readings against a Poisson-binomial expectation from per-day value frequencies. That benchmark is conservative, because the duplicates themselves inflate the collision rates.')
P('<b>Limitations.</b> n = 3–8 per group; female BALB/c (sex not stated for other strains); single experiments with no replicate runs; vaccine antigen was formalin-inactivated whole virus rather than licensed split/subunit antigen; mouse intranasal dosing reaches the lung, unlike a human nasal spray. External context is marked as such and carries no numbers.')

# =====================================================================================
DOC.append(('pagebreak', None))
H1('Appendix A. Full data-integrity register')
arows = [['ID', 'Severity', 'Blocks / cells', 'Finding', 'Required action']]
for _, r in IR.iterrows():
    arows.append([r.id, r.severity, f'{r.blocks}' + (f' ({r.cells})' if isinstance(r.cells, str) and r.cells else ''), r.finding, r.required_action])
TAB(arows, [10 * mm, 15 * mm, 45 * mm, 70 * mm, 32 * mm], fs=5.8)
H1('Appendix B. Deliverables')
BUL(['<b>PSLN-344_Portfolio_Proposal.pdf / .md</b>: this document.',
     '<b>PSLN-344_evidence_ledger.xlsx</b>: claims with cell references; group summaries; all contrasts; Tukey HSD; survival counts, tests and pooled sensitivity; mechanism contrasts; biomarker table; safety; dose-response; integrity register; duplication analyses.',
     '<b>figures/</b>: Figures 1–7 as PNG.',
     '<b>analysis/</b>: Python scripts, plus tidy data tables with a cell reference for every value. Run order: parse.py → surv_summary.py → stats_continuous.py → stats_survival.py → stats_survival_pooled.py → check_derived.py → bw_reconcile.py → dup_scan.py → dup_exact_bw.py → dup_trajectories.py → dup_trajectories2.py → dup_null.py → integrity_checks.py → integrity_register.py → mechanism_contrasts.py → biomarkers.py → safety_cmc_dose.py → design_power.py → keynums.py → figures.py → fig_moa.py → build_report.py → build_ledger.py. Environment: micromamba env <i>chem</i> (pandas, scipy, statsmodels, matplotlib, reportlab, openpyxl).'])

# =====================================================================================
# RENDERERS
def esc(s):
    s = str(s)
    # escape & not part of entity; keep our markup tags
    s = re.sub(r'&(?!(amp|lt|gt|#\d+);)', '&amp;', s)
    # protect allowed tags
    s = re.sub(r'<(?!/?(b|i|br|font|super|sub)\b)', '&lt;', s)
    return s
base = ParagraphStyle('base', fontName='DV', fontSize=8.6, leading=11.2, spaceAfter=4)
styles = {
    'title': ParagraphStyle('t', parent=base, fontName='DVB', fontSize=17, leading=21, spaceAfter=4, textColor=colors.HexColor('#12355b')),
    'subtitle': ParagraphStyle('st', parent=base, fontName='DV', fontSize=10, leading=13, textColor=colors.HexColor('#12355b'), spaceAfter=6),
    'h1': ParagraphStyle('h1', parent=base, fontName='DVB', fontSize=12.5, leading=15, spaceBefore=9, spaceAfter=5, textColor=colors.HexColor('#12355b')),
    'h2': ParagraphStyle('h2', parent=base, fontName='DVB', fontSize=10, leading=13, spaceBefore=6, spaceAfter=3, textColor=colors.HexColor('#1f5fa8')),
    'p': base, 'small': ParagraphStyle('sm', parent=base, fontSize=7.2, leading=9.2, textColor=colors.HexColor('#333333')),
    'cap': ParagraphStyle('cap', parent=base, fontSize=7.2, leading=9, textColor=colors.HexColor('#333333'), spaceAfter=8),
    'bul': ParagraphStyle('bul', parent=base, leftIndent=10, bulletIndent=2, spaceAfter=3),
}
def cellp(t, fs, bold=False):
    return Paragraph(esc(t), ParagraphStyle('c', fontName='DVB' if bold else 'DV', fontSize=fs, leading=fs * 1.22))
story = []
for kind, pl in DOC:
    if kind in ('title', 'subtitle', 'h1', 'h2', 'p', 'small'):
        story.append(Paragraph(esc(pl), styles[kind]))
    elif kind == 'bul':
        for it in pl:
            story.append(Paragraph(esc(it), styles['bul'], bulletText='•'))
    elif kind == 'box':
        t, col = pl
        tb = Table([[Paragraph(esc(t), ParagraphStyle('bx', parent=base, fontSize=8.6, leading=11.4))]], colWidths=[172 * mm])
        tb.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(col)), ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#12355b')),
                                ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7), ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
        story.append(tb); story.append(Spacer(1, 6))
    elif kind == 'tab':
        rows, widths, header, fs, zebra, hl = pl
        data = [[cellp(c, fs, bold=(header and i == 0)) for c in row] for i, row in enumerate(rows)]
        tb = Table(data, colWidths=widths, repeatRows=1 if header else 0)
        stl = [('GRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#9aa5b1')), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
               ('LEFTPADDING', (0, 0), (-1, -1), 3), ('RIGHTPADDING', (0, 0), (-1, -1), 3), ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]
        if header: stl.append(('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dce6f2')))
        if zebra:
            for i in range(1, len(rows)):
                if i % 2 == 0: stl.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f5f7fa')))
        tb.setStyle(TableStyle(stl)); story.append(tb); story.append(Spacer(1, 7))
    elif kind == 'fig':
        path, cap, w = pl
        from PIL import Image as PILImage
        im = PILImage.open(path); ar = im.size[1] / im.size[0]
        W = w * mm; H = W * ar
        maxH = 235 * mm
        if H > maxH: H = maxH; W = H / ar
        story.append(KeepTogether([Image(path, width=W, height=H), Paragraph(esc(cap), styles['cap'])]))
    elif kind == 'pagebreak':
        story.append(PageBreak())
def onpage(canv, doc):
    canv.saveState(); canv.setFont('DV', 7); canv.setFillColor(colors.HexColor('#666666'))
    canv.drawString(18 * mm, 10 * mm, 'PSLN-344 portfolio review proposal · data cut 1 Nov 2026 · confidential')
    canv.drawRightString(192 * mm, 10 * mm, f'page {doc.page}'); canv.restoreState()
pdf = SimpleDocTemplate(OUT + 'PSLN-344_Portfolio_Proposal.pdf', pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=15 * mm, bottomMargin=16 * mm,
                        title='PSLN-344 portfolio review proposal', author='Portfolio analysis')
pdf.build(story, onFirstPage=onpage, onLaterPages=onpage)

# Markdown
def md(s):
    s = str(s).replace('<br/>', '  \n').replace('<b>', '**').replace('</b>', '**').replace('<i>', '*').replace('</i>', '*')
    s = re.sub(r'</?(font|super|sub)[^>]*>', '', s)
    return s
L = []
for kind, pl in DOC:
    if kind == 'title': L.append('# ' + md(pl))
    elif kind == 'subtitle': L.append('*' + md(pl) + '*\n')
    elif kind == 'h1': L.append('\n## ' + md(pl))
    elif kind == 'h2': L.append('\n### ' + md(pl))
    elif kind in ('p', 'small'): L.append(md(pl) + '\n')
    elif kind == 'bul': L.extend(['- ' + md(x) for x in pl]); L.append('')
    elif kind == 'box': L.append('> ' + md(pl[0]).replace('\n', '\n> ') + '\n')
    elif kind == 'tab':
        rows = pl[0]
        L.append('| ' + ' | '.join(md(c).replace('|', '/') for c in rows[0]) + ' |')
        L.append('|' + '---|' * len(rows[0]))
        for r in rows[1:]: L.append('| ' + ' | '.join(md(c).replace('|', '/').replace('\n', ' ') for c in r) + ' |')
        L.append('')
    elif kind == 'fig': L.append(f'![{md(pl[1])}](figures/{os.path.basename(pl[0])})\n')
open(OUT + 'PSLN-344_Portfolio_Proposal.md', 'w').write('\n'.join(L))
pd.DataFrame(CLAIMS).to_csv(A + 'claims.csv', index=False)
print('PDF and MD written; claims:', len(CLAIMS))
